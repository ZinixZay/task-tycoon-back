import pytest
from httpx import AsyncClient, ASGITransport
from models import TaskModel
from main import app


@pytest.mark.asyncio
async def test_get_task_by_id_to_observe(
    event_loop,
    task_model: TaskModel,
    jwt_token: str
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.get(f"/api/v1/tasks/task_id/to_observe?id={task_model.id}", headers=headers)


    # no permission to change permissions
    assert response.status_code == 200
