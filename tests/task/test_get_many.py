import pytest
from httpx import AsyncClient, ASGITransport
from models import TaskModel
from main import app


@pytest.mark.asyncio
async def test_get_many_tasks(
    event_loop
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        response = await client.get(f"/api/v1/tasks/")

    # no permission to change permissions
    assert response.status_code == 200
