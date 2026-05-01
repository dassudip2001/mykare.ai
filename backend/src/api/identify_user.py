from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.models.migrations import User,Appointment
from src.config.db import get_db
from src.models.schemas import IdentifyUserRequest,BookAppointmentRequest, ModifyAppointmentRequest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
router=APIRouter()

@router.post("/identify_user")
async def identify_user(
    data: IdentifyUserRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.phone == data.phone)
    )
    user = result.scalar_one_or_none()

    if not user:
        user = User(name=data.name, phone=data.phone)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return {"user_id": user.id, "name": user.name}

@router.get("/appointments/{user_id}")
async def get_appointments(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(Appointment.user_id == user_id)
    )
    return result.scalars().all()

@router.get("/all_appointments")
async def get_all_appointments(
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).options(selectinload(Appointment.user))
    )

    appointments = result.scalars().all()

    return [
        {
            "id": ap.id,
            "date": ap.date,
            "time": ap.time,
            "status": ap.status,
            "user": {
                "id": ap.user.id,
                "name": ap.user.name,
                "phone": ap.user.phone
            } if ap.user else None
        }
        for ap in appointments
    ]

@router.delete("/cancel/{appointment_id}")
async def cancel_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()

    if not appointment:
        raise HTTPException(status_code=404, detail="Not found")

    appointment.status = "cancelled"
    await db.commit()

    return {"message": "Cancelled"}

@router.put("/modify/{appointment_id}")
async def modify_appointment(
    data: ModifyAppointmentRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(Appointment.id == data.appointment_id)
    )
    appointment = result.scalar_one_or_none()

    if not appointment:
        raise HTTPException(status_code=404, detail="Not found")

    appointment.date = data.date
    appointment.time = data.time
    appointment.status = "rescheduled"

    await db.commit()

    return {"message": "Updated"}

@router.post("/book_appointment")
async def book_appointment(
    data: BookAppointmentRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(
            Appointment.date == data.date,
            Appointment.time == data.time,
            Appointment.status == "booked"
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Slot already booked")

    appointment = Appointment(
        user_id=data.user_id,
        date=data.date,
        time=data.time
    )

    db.add(appointment)
    await db.commit()

    return {
        "message": "Appointment booked",
        "date": data.date,
        "time": data.time
    }



@router.get("/available_slots")
async def available_slots(
    db: AsyncSession = Depends(get_db)
):
    all_slots = [
        ("2026-05-02", "10:00 AM"),
        ("2026-05-02", "11:00 AM"),
        ("2026-05-02", "02:00 PM"),
    ]

    result = await db.execute(
        select(Appointment).where(Appointment.status == "booked")
    )
    booked = result.scalars().all()

    booked_set = {(b.date, b.time) for b in booked}

    available = [
        {"date": d, "time": t}
        for d, t in all_slots
        if (d, t) not in booked_set
    ]

    return {"slots": available}