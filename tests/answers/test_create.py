import pytest
from httpx import AsyncClient, ASGITransport
from models import UserModel, TaskModel, QuestionModel
from main import app


@pytest.mark.asyncio
async def test_answer_create(
    event_loop,
    user_model: UserModel,
    task_model: TaskModel,
    question_model: QuestionModel,
    jwt_token: str
):
    payload = {
        "task_id": task_model.id,
        "answers": [
            {
            "question_id": question_model.id,
            "content": [
                {
                "title": "will it pass?",
                "is_correct": True
                }
            ]
            }
        ]
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.post("/api/v1/answers/", json=payload, headers=headers)

    assert response.status_code == 200
    