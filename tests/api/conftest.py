import re
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any

import pytest
import pytest_asyncio
from httpx import URL, AsyncClient

from app.config import app_urls
from app.schemas.users import UserCreate
from tests.utils import log, logjson


@pytest.fixture(scope="session")
def users_url() -> URL:
    url = URL(app_urls.api_url.encoded_string() + "/users/")
    log.info(f"Using url: {url}")
    return url


@pytest_asyncio.fixture(scope="session")
async def delete_test_users(users_url: URL):
    async with AsyncClient(base_url=users_url) as client:
        resp = await client.get(users_url)
        respbody = resp.json()

        # Find IDs of test users to delete
        pattern = r"^TestUser[a-zA-Z]*_\d{8}-\d{6}\.\d{3}"
        matched_ids = [
            obj.get("id")
            for obj in respbody
            if (username := obj.get("username")) is not None and re.search(pattern, username)
        ]

        for id in matched_ids:
            await client.delete(f"{id}")

        log.info(f"Deleting users with IDs: {matched_ids}")


@pytest_asyncio.fixture(scope="function")
async def add_test_users(delete_test_users, users_url: URL) -> AsyncGenerator[list[dict]]:
    async with AsyncClient(base_url=users_url) as client:
        test_user_req_fields = UserCreate(
            username=f"TestUserRequiredFields_{datetime.now().strftime('%Y%m%d-%H%M%S.%f')[:-3]}"
        )
        test_user_all_fields = UserCreate(
            name="TestUserName",
            surname="TestUserSurname",
            username=f"TestUserAllFields_{datetime.now().strftime('%Y%m%d-%H%M%S.%f')[:-3]}",
            comment="User for testing",
            role="user",
        )

        r1add = await client.post("/", json=test_user_req_fields.model_dump())
        r1addbody: dict = r1add.json()
        logjson("Added user during setup: ", r1addbody)
        radd2 = await client.post("/", json=test_user_all_fields.model_dump())
        r2addbody: dict = radd2.json()
        logjson("Added user during setup: ", r2addbody)

        yield [r1addbody, r2addbody]

        resp = await client.get(users_url)
        respbody: list[dict[str, Any]] = resp.json()

        # Search test users in the response by username
        user_with_req_fields_dict = next(
            (user for user in respbody if user.get("username") == test_user_req_fields.username), None
        )
        assert user_with_req_fields_dict is not None, f"User with username {test_user_req_fields.username} not found"
        user_with_all_fields_dict = next(
            (user for user in respbody if user.get("username") == test_user_all_fields.username), None
        )
        assert user_with_all_fields_dict is not None, f"User with username {test_user_req_fields.username} not found"

        await client.delete(f"{user_with_req_fields_dict.get('id')}")
        await client.delete(f"{user_with_all_fields_dict.get('id')}")

        log.info(f"Deleted user during teardown with ID: {user_with_req_fields_dict.get('id')}")
        log.info(f"Deleted user during teardown with ID: {user_with_all_fields_dict.get('id')}")
