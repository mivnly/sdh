import httpx
import pytest

from app.schemas.users import UserCreate, UserRead
from tests.utils import logjson


@pytest.mark.asyncio
async def test_users_add(add_test_users: list[dict]):
    created_user_req_fields = add_test_users[0]
    created_user_all_fields = add_test_users[1]

    assert UserCreate.model_validate(created_user_req_fields)
    assert UserCreate.model_validate(created_user_all_fields)


@pytest.mark.asyncio
async def test_users_get(add_test_users: list[dict], users_url):
    async with httpx.AsyncClient() as client:
        created_user_req_fields = add_test_users[0]
        created_user_all_fields = add_test_users[1]

        resp = await client.get(users_url)
        respbody = resp.json()
        logjson("Got users:", respbody)

        # Search test users in the response by username
        user_with_req_fields_dict = next(
            (user for user in respbody if user.get("username") == created_user_req_fields.get("username")), None
        )
        user_with_all_fields_dict = next(
            (user for user in respbody if user.get("username") == created_user_all_fields.get("username")), None
        )

        test_user_with_req_fields = UserRead.model_validate(user_with_req_fields_dict)
        test_user_with_all_fields = UserRead.model_validate(user_with_all_fields_dict)

        assert resp.status_code == httpx.codes.OK
        assert created_user_req_fields == test_user_with_req_fields.model_dump(exclude={"id"})
        assert created_user_all_fields == test_user_with_all_fields.model_dump(exclude={"id"})
