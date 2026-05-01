# MyKare Backend

A FastAPI appointment booking service for the MyKare project.

The backend exposes REST endpoints for user identification, appointment booking, rescheduling, cancellation, and slot discovery. It uses SQLite for persistence and SQLAlchemy with async support.

## Features

- User lookup and registration by phone number
- Appointment booking with duplicate-slot protection
- Appointment modification and cancellation
- User-specific appointment retrieval
- Global appointment listing with embedded user details
- Available slot calculation against booked appointments

## Requirements

- Python 3.11+
- `pip`

## Install

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -e .
```

> Windows PowerShell users can use `.ackend\.venv\Scripts\Activate.ps1`.

## Run

Start the server from the `backend` folder:

```bash
cd backend
python main.py
```

Or run with Uvicorn directly:

```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API is available at `http://127.0.0.1:8000`.

## Database

- SQLite file: `backend/test.db`
- SQLAlchemy async engine configured in `src/config/db.py`
- Tables defined in `src/models/migrations.py`

### Models

`User`

- `id` (integer, primary key)
- `name` (string)
- `phone` (string, unique)

`Appointment`

- `id` (integer, primary key)
- `user_id` (foreign key to users)
- `date` (string)
- `time` (string)
- `status` (string, default `booked`)

## API Endpoints

### Health

`GET /`

Response:

```json
{ "message": "Server is running..............." }
```

### Slots

`GET /api/v1/slots`

Returns a fixed list of example appointment slots.

### User identification

`POST /api/v1/identify_user`

Request body:

```json
{ "phone": "1234567890", "name": "Jane Doe" }
```

Response:

```json
{ "user_id": 1, "name": "Jane Doe" }
```

### Available slots

`GET /api/v1/available_slots`

Returns slots that are not already booked.

### Book appointment

`POST /api/v1/book_appointment`

Request body:

```json
{ "user_id": 1, "date": "2026-05-02", "time": "10:00 AM" }
```

Response:

```json
{
  "message": "Appointment booked",
  "date": "2026-05-02",
  "time": "10:00 AM"
}
```

### Modify appointment

`PUT /api/v1/modify/{appointment_id}`

Request body:

```json
{ "appointment_id": 1, "date": "2026-05-03", "time": "02:00 PM" }
```

Response:

```json
{ "message": "Updated" }
```

### Cancel appointment

`DELETE /api/v1/cancel/{appointment_id}`

Response:

```json
{ "message": "Cancelled" }
```

### Get user appointments

`GET /api/v1/appointments/{user_id}`

Returns all appointments for the requested user.

### Get all appointments

`GET /api/v1/all_appointments`

Returns every appointment with its user details included.

## Notes

- The backend uses CORS middleware allowing all origins.
- `main.py` defines a startup context manager to initialize database metadata.
- If you need a fresh database, remove `backend/test.db` and restart the service.

## Project structure

```text
backend/
├── main.py
├── pyproject.toml
└── src/
    ├── api/
    │   ├── heldth.py
    │   ├── identify_user.py
    │   └── slots_route.py
    ├── config/
    │   └── db.py
    └── models/
        ├── migrations.py
        └── schemas.py
```

## License

This backend does not include a license file. Add one if you plan to publish or distribute the service.
