from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.api.heldth import  router as he
from src.api.slots_route import router as slots
from src.api.identify_user import router as identify
from src.config.db import Base,engine
from contextlib import asynccontextmanager
app=FastAPI()


# database init
@asynccontextmanager
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


origins=[
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(he)
app.include_router(prefix="/api/v1",router=slots)
app.include_router(prefix="/api/v1",router=identify)

if __name__ == '__main__':
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)