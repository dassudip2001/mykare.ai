import httpx
import json

url = "http://localhost:5003/api/v1/ask"

async def ask_hr_policy(question: str):
    payload = {
        "question": question
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
import asyncio

asyncio.run(ask_hr_policy("give me hr policy ?"))
