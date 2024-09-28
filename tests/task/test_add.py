import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_add_task(
    event_loop,
    jwt_token: str
):
    payload = {
    "title": "test",
    "description_full": "this is test task",
    "description_short": "task4testing",
    "questions": [
    {
        "question_body": "will it pass?",
        "type": "multi",
        "content": [
        {
            "title": "content",
            "is_correct": True
        }
        ],
        "order": 0
    }
    ]
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.post(f"/api/v1/tasks/", json=payload, headers=headers)


    # no permission to change permissions
    assert response.status_code == 200
