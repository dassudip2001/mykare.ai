# MyKare

MyKare is a multi-service appointment booking and voice assistant project built with FastAPI, Next.js, and LiveKit. The repository includes:

- `backend/`: FastAPI appointment service with SQLite persistence.
- `frontend/`: Next.js UI for listing appointments and interacting with the backend.
- `livekit-fe/`: LiveKit Agents React frontend for voice interaction.
- `livekit-voice-agent/`: Python LiveKit Agents voice assistant with booking tools.

## Repository Structure

```
mykare/
├── backend/                # FastAPI appointment API
├── frontend/               # Next.js frontend app
├── livekit-fe/             # LiveKit voice agent React frontend
├── livekit-voice-agent/    # Python LiveKit Agents voice service
└── Readme.md               # Repository overview
```

## Backend Service (`backend/`)

The backend is a FastAPI app serving appointment and user operations.

### Key features

- SQLite database stored in `backend/test.db`
- Automatically creates tables on startup
- Appointment booking, cancellation, modification, and listing
- User identification by phone number

### Endpoints

- `GET /api/v1/` - health check
- `GET /api/v1/slots` - static available slots
- `GET /api/v1/all_appointments` - list all appointments with user details
- `GET /api/v1/appointments/{user_id}` - appointments for a specific user
- `POST /api/v1/identify_user` - identify or register a user
- `POST /api/v1/book_appointment` - create a new appointment
- `PUT /api/v1/modify/{appointment_id}` - reschedule an appointment
- `DELETE /api/v1/cancel/{appointment_id}` - cancel an appointment

### Run backend

```bash
cd backend
python main.py
```

The service launches on `http://127.0.0.1:8000` by default.

### API docs

OpenAPI documentation is available at:

- `http://127.0.0.1:8000/docs`

## Frontend App (`frontend/`)

This Next.js application currently fetches appointment data from the backend API.

### Local development

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3001` in your browser.

### Notes

- App is configured to call `http://localhost:8000/api/v1/all_appointments`
- Uses Next.js 16 and TypeScript
- UI can be extended via `frontend/app/page.tsx`

## LiveKit React Frontend (`livekit-fe/`)

A LiveKit Agents starter frontend with voice session UI and audio visualizers.

### Install and run

```bash
cd livekit-fe
npm install
npm run dev
```

The app uses `.env.local` for LiveKit and agent configuration.

### Environment variables

Copy `.env.example` to `.env.local` and fill in values:

```env
LIVEKIT_API_KEY=""
LIVEKIT_API_SECRET=""
LIVEKIT_URL=""
NEXT_PUBLIC_LIVEKIT_URL=""
OPENAI_API_KEY=""
BEY_API_KEY=""
```

## LiveKit Voice Agent (`livekit-voice-agent/`)

This Python service is a LiveKit Agents assistant configured to manage appointments via the backend API.

### Features

- Uses `livekit-agents` for voice sessions
- Custom agent logic for booking, rescheduling, cancelling, and retrieving appointments
- Contains tool functions that call the backend API
- Loads environment variables from `.env.local`

### Run voice agent

```bash
cd livekit-voice-agent
python main.py
```

### Dependencies

The service uses:

- `livekit-agents`
- `python-dotenv`
- `httpx`
- `torch`

## Database model

The backend stores two tables:

- `users`
  - `id`
  - `name`
  - `phone`
- `appointments`
  - `id`
  - `user_id`
  - `date`
  - `time`
  - `status`

## Quick start

1. Start the backend:
   ```bash
   cd backend
   python main.py
   ```
2. Start the frontend UI:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Start the LiveKit voice frontend (optional):
   ```bash
   cd livekit-fe
   npm install
   npm run dev
   ```
4. Start the LiveKit voice agent (optional):
   ```bash
   cd livekit-voice-agent
   python main.py
   ```

## Notes

- If you change the backend URL or ports, update the frontend fetch URL and the voice agent `url` constant in `livekit-voice-agent/main.py`.
- The API supports appointment workflows and can be extended to add authentication or calendar integration.

## License

This repository does not contain a unified license file at the root. Check each service directory for its own license or add one if required.
