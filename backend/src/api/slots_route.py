from fastapi import APIRouter

router=APIRouter()

@router.get("/slots")
async def slots():
    return {
        "slots":[
            {"date": "2026-05-02", "time": "10:00 AM"},
            {"date": "2026-05-02", "time": "11:00 AM"},
            {"date": "2026-05-02", "time": "02:00 PM"},
        ]
    }