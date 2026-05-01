# LiveKit Voice Agent

A voice-enabled LiveKit Agents service for MyKare appointment booking.

This Python service connects voice sessions to the backend appointment API and exposes tools for:

- user identification
- available slot lookup
- appointment booking
- appointment modification
- appointment cancellation
- user appointment retrieval

## Key components

- `main.py` - LiveKit agent definition, tool functions, and agent session setup
- `pyproject.toml` - Python package metadata and dependencies
- `.env.example.local` - template for required environment variables

## Requirements

- Python 3.11+
- Local backend running at `http://localhost:8000/api/v1/`
- LiveKit room and API credentials
- OpenAI API key for the `openai/gpt-4.1-mini` model
- Beyond Presence API key for avatar sessions

## Setup

1. Create and activate a Python virtual environment:

```bash
cd livekit-voice-agent
python -m venv .venv
source .venv/Scripts/activate
```

2. Install the package and dependencies:

```bash
python -m pip install -e .
```

3. Copy the environment example:

```bash
copy .env.example.local .env.local
```

4. Fill in `.env.local` with your LiveKit and OpenAI credentials:

```env
LIVEKIT_API_KEY=""
LIVEKIT_API_SECRET=""
LIVEKIT_URL=""
NEXT_PUBLIC_LIVEKIT_URL=""
OPENAI_API_KEY=""
BEY_API_KEY=""
```

> Note: `main.py` currently loads `.env.local` directly.

## Run

Start the voice agent from the `livekit-voice-agent` directory:

```bash
python main.py
```

The service launches as a LiveKit Agents process and waits for voice session connections.

## How it works

The agent uses these tool functions to operate against the backend:

- `identify_user_tool(phone, name)` - registers or finds a user and stores `user_id`
- `get_slots()` - fetches available appointment slots
- `book_appointment_tool(date, time)` - books an appointment for the identified user
- `get_user_appointments()` - lists appointments for the active user
- `modify_tool(appointment_id, date, time)` - reschedules an appointment
- `cancel_tool(appointment_id)` - cancels an appointment

The assistant enforces conversational flow rules and only calls tools when the required data is available.

## Backend dependency

This voice agent expects the MyKare backend API to be available at:

```text
http://localhost:8000/api/v1/
```

If the backend runs on a different host or port, update the `url` constant in `main.py`.

## Notes

- The current session uses:
  - `assemblyai/universal-streaming:en` for speech-to-text
  - `openai/gpt-4.1-mini` for language understanding
  - `cartesia/sonic-3` for text-to-speech
  - `silero.VAD` for voice activity detection
  - `bey.AvatarSession` for avatar presentation

- The agent is designed for medical-style appointment booking and behaves like a polite receptionist.

## License

This directory does not include a separate license file. Add one if you need to publish or distribute this service.
