import pytest
from httpx import AsyncClient, ASGITransport
from main import app

from models import QuestionModel


@pytest.mark.asyncio
async def test_get_question_by_id(
    event_loop,
    question_model: QuestionModel
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        response = await client.get(f"/api/v1/questions/question_id?question_id={question_model.id}")

    assert response.status_code == 200
