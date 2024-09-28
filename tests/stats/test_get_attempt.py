import pytest
from httpx import AsyncClient, ASGITransport
from models import AttemptStatsModel
from main import app


@pytest.mark.asyncio
async def test_stats_get_attempt(
    event_loop,
    attempt_model: AttemptStatsModel,
    jwt_token: str
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.get(f"/api/v1/stats/attempt?attempt_id={attempt_model.id}", headers=headers)


    # no permission to change permissions
    assert response.status_code == 200
