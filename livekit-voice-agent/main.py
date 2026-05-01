from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import elevenlabs
from livekit.plugins import bey
import httpx
from livekit.agents import function_tool, Agent, RunContext

load_dotenv(".env.local")
url = "http://localhost:5003/api/v1/ask"


@function_tool()
async def lookup_user(
    context: RunContext,
    query: str,
) -> dict:
    """External API call to get information about the HR policy"""
    payload = {
        "question": query
    }
    headers = {
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            url,
            json=payload,
            headers=headers
        )
    print(response.text)
    return response.json()




class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant. call the tool and give the response best way . If you don't know the answer, just say that you don't know, don't try to make up an answer. if ask what is your name, say your name is LiveKit Assistant.""",
            tools=[lookup_user],
        )
        

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt="assemblyai/universal-streaming:en",
        llm="openai/gpt-4.1-mini",
        # tts=elevenlabs.TTS(
        #     voice_id="ODq5zmih8GrVes37Dizd",
        #     model="eleven_multilingual_v2"
        # ),
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )


    avatar = bey.AvatarSession(
        avatar_id="694c83e2-8895-4a98-bd16-56332ca3f449"  # ID of the Beyond Presence avatar to use
    )

    # Start the avatar and wait for it to join
    await avatar.start(session, room=ctx.room)


    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)