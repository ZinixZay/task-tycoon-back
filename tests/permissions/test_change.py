import pytest
from httpx import AsyncClient, ASGITransport
from models import UserModel
from main import app


@pytest.mark.asyncio
async def test_permissions_change(
    event_loop,
    user_model: UserModel,
    jwt_token: str
):
    payload = {
        "target_user_id": user_model.id,
        "permissions": [
            {
                "permission": "create_task",
                "state": True
            }
        ]
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.post("/api/v1/permissions/", json=payload, headers=headers)


    # no permission to change permissions
    assert response.status_code == 403
