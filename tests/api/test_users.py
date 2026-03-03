import httpx
import pytest

from app.schemas.users import UserRead
from tests.utils import logjson


@pytest.mark.asyncio
async def test_users_get(add_test_users, users_url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(users_url)
        respbody = resp.json()
        logjson("Got users:", respbody)

        test_user_with_req_fields_dict = next(
            (user for user in respbody if user.get("username") == add_test_users[0]), None
        )
        test_user_with_all_fields_dict = next(
            (user for user in respbody if user.get("username") == add_test_users[1]), None
        )

        test_user_with_req_fields = UserRead.model_validate(test_user_with_req_fields_dict)
        test_user_with_all_fields = UserRead.model_validate(test_user_with_all_fields_dict)
        assert resp.status_code == httpx.codes.OK
        assert test_user_with_req_fields.username == add_test_users[0]
        assert test_user_with_req_fields.name is None
        assert test_user_with_req_fields.surname is None
        assert test_user_with_req_fields.comment is None
        assert test_user_with_req_fields.role == "user"
        assert test_user_with_all_fields.username == add_test_users[1]
        assert test_user_with_all_fields.name == "TestUserName"
        assert test_user_with_all_fields.surname == "TestUserSurname"
        assert test_user_with_all_fields.comment == "User for testing"
        assert test_user_with_all_fields.role == "user"
