import pytest
from httpx import AsyncClient, ASGITransport
from models import TaskModel
from main import app


@pytest.mark.asyncio
async def test_get_task_patch(
    event_loop,
    task_model: TaskModel,
    jwt_token: str
):
    payload = {
        "task_id": task_model.id,
        "title": "new title",
        "description_full": "new description wow!",
        "description_short": "new descr",
        "questions": []
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.patch(f"/api/v1/tasks/", json=payload, headers=headers)


    # no permission to change permissions
    assert response.status_code == 200
