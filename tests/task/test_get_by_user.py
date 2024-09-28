import pytest
from httpx import AsyncClient, ASGITransport
from models import TaskModel, UserModel
from main import app


@pytest.mark.asyncio
async def test_get_task_by_user(
    event_loop,
    jwt_token: str
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.get(f"/api/v1/tasks/user_id", headers=headers)


    # no permission to change permissions
    assert response.status_code == 200
