import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_profile_update(
    event_loop,
    jwt_token: str
):
    payload = {
        "nickname": "new nickname"
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        await client.patch("/api/v1/profiles/")