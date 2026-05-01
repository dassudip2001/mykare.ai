from pydantic import BaseModel
from typing import Optional

class IdentifyUserRequest(BaseModel):
    name: Optional[str]
    phone: str


class BookAppointmentRequest(BaseModel):
    user_id: int
    date: str
    time: str


class ModifyAppointmentRequest(BaseModel):
    appointment_id: int
    date: str
    time: str


class EndConversationRequest(BaseModel):
    user_id: int
    summary: str