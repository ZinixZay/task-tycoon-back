import pytest
from httpx import AsyncClient, ASGITransport
from models import TaskModel, UserModel
from main import app



@pytest.mark.asyncio
async def test_stats_get_resulting_attempt(
    event_loop,
    task_model: TaskModel,
    user_model: UserModel,
    jwt_token: str
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.get(f"/api/v1/stats/attempt/resulting?task_id={task_model.id}&user_id={user_model.id}", headers=headers)


    # no permission to change permissions
    assert response.status_code == 200
