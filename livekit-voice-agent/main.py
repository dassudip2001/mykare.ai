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
    """
    Retrieve available appointment slots.

    Use this tool when:
    - The user wants to book an appointment
    - The user asks for available times or slots

    This tool will:
    - Return a list of available date and time slots
    - Exclude already booked slots

    Important:
    - Call this AFTER the user is identified
    - Do NOT guess available slots manually
    - Always rely on this tool for accurate availability
    """
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{url}available_slots")
        return res.json()
    
# book appointment 
@function_tool()
async def book_appointment_tool(
    context: RunContext,
    date: str,
    time: str
):
    """
    Book an appointment for the identified user.

    Use this tool when:
    - The user selects a date and time slot
    - The user confirms they want to proceed with booking

    This tool will:
    - Create a new appointment
    - Prevent double booking
    - Confirm the booking

    Args:
        date: Appointment date (e.g., "2026-05-02")
        time: Appointment time (e.g., "10:00 AM")

    Important:
    - ONLY call this after user is identified
    - ONLY call this after user selects a valid slot
    - Do NOT call if user_id is missing
    """
    user_id = context.userdata.get("user_id")

    if not user_id:
        return {"error": "User not identified"}
    
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
    

@function_tool()
async def get_user_appointments(context: RunContext):
    """Retrieve all appointments for the identified user.
    Use this tool when:
    - The user wants to view their upcoming appointments
    This tool will:
    - Return a list of all appointments for the user
    Important:
    - ONLY call this after user is identified
    - Do NOT call if user_id is missing
    """
    user_id = context.userdata.get("user_id")

    if not user_id:
        return {"error": "User not identified"}

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{url}appointments/{user_id}")
        return res.json()    
    
# modify appointment
@function_tool()
async def modify_tool(
    context: RunContext,
    appointment_id: int,
    date: str,
    time: str
):
    """
    Modify an existing appointment.

    Use this tool when:
    - The user wants to reschedule an appointment
    - The user provides a new date and time

    This tool will:
    - Update the appointment date and time
    - Mark the appointment as rescheduled

    Args:
        appointment_id: ID of the appointment to modify
        date: New date
        time: New time

    Important:
    - Ask for appointment_id if not provided
    - Confirm new slot with user before modifying
    - Do NOT modify without user confirmation
    """
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
    """
    Cancel an existing appointment.

    Use this tool when:
    - The user wants to cancel an appointment

    This tool will:
    - Mark the appointment as cancelled

    Args:
        appointment_id: ID of the appointment to cancel

    Important:
    - Ask for appointment_id if missing
    - Confirm cancellation before proceeding
    - Do NOT cancel without explicit user confirmation
    """
    async with httpx.AsyncClient() as client:
        res = await client.delete(
            f"{url}cancel/{appointment_id}"
        )
        return res.json()

# identify the user
@function_tool()
async def identify_user_tool(context: RunContext, phone: str, name: str):
    """
    Identify or register a user in the system.

    Use this tool when:
    - The user wants to book, cancel, or modify an appointment
    - The system does not yet know who the user is
    - The user provides their name and phone number

    This tool will:
    - Create a new user if not exists
    - Return an existing user if already registered
    - Store user_id in session memory for future actions

    Args:
        phone: User's phone number (required)
        name: User's full name (required)

    Important:
    - ALWAYS call this tool before booking any appointment
    - Do NOT proceed with booking without identifying the user
    """     
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{url}identify_user",
            json={
                "phone": phone,
                "name": name
            }
        )
        data = res.json()

        # STORE USER IN SESSION
        context.userdata["user_id"] = data["user_id"]
        context.userdata["name"] = data["name"]

        return data

# 
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
            You are a professional medical booking assistant.
            
            GENERAL BEHAVIOR:
            - Always guide the user step-by-step
            - Ask for missing information instead of guessing
            - Be polite and professional like a receptionist
            - Never call a tool with incomplete data
            

            FLOW RULES:

            1. If user wants to book an appointment:
            - FIRST check if user_id exists in memory
            - If NOT → ask politely for name and phone number
            - Then call identify_user_tool

            2. After user is identified:
            - Call get_slots to show available slots

            3. When user selects a slot:
            - Call book_appointment_tool

            4. If user wants to cancel:
            - Ask for appointment_id → call cancel_tool

            5. If user wants to modify:
            - Ask for appointment_id → call modify_tool

            STRICT RULES:
            - Never book without identifying the user
            - Always be polite and professional
            - Ask one question at a time
            - Guide the user step-by-step like a real receptionist
            """,
            tools=[get_slots, book_appointment_tool, cancel_tool, modify_tool, identify_user_tool, get_user_appointments],
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