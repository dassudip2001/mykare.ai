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
url = "http://localhost:8000/api/v1/"


# get available slots
@function_tool()
async def get_slots(context: RunContext) -> dict:
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{url}available_slots")
        return res.json()
    
# book appointment 
@function_tool()
async def book_appointment_tool(
    context: RunContext,
    user_id: int,
    date: str,
    time: str
):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{url}book_appointment",
            json={
                "user_id": user_id,
                "date": date,
                "time": time
            }
        )
        return res.json()
    
# modify appointment
@function_tool()
async def modify_tool(
    context: RunContext,
    appointment_id: int,
    date: str,
    time: str
):
    async with httpx.AsyncClient() as client:
        res = await client.put(
            f"{url}modify/{appointment_id}",
            json={
                "appointment_id": appointment_id,
                "date": date,
                "time": time
            }
        )
        return res.json() 

# cancel appointment
@function_tool()
async def cancel_tool(context: RunContext, appointment_id: int):
    async with httpx.AsyncClient() as client:
        res = await client.delete(
            f"{url}cancel/{appointment_id}"
        )
        return res.json()

# identify the user
@function_tool()
async def identify_user_tool(context: RunContext, phone: str, name: str):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{url}identify_user",
            json={
                "phone": phone,
                "name": name
            }
        )
        return res.json()

# 
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
            You are a booking assistant.

            RULES:
            - If user wants to book → call get_slots
            - If user selects slot → call book_appointment_tool
            - If user wants to cancel → call cancel_tool
            - If user wants to modify → call modify_tool
            - If user wants to identify → call identify_user_tool

            Never guess. Always use tools.""",
            tools=[get_slots, book_appointment_tool, cancel_tool, modify_tool, identify_user_tool],
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