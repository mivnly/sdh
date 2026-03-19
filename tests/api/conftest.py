import asyncio
import re
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any

import pytest
import pytest_asyncio
from httpx import URL, AsyncClient, codes

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
        # Defining test users to be created
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

        # Creating test users
        r1add = await client.post("/", json=test_user_req_fields.model_dump())
        r1addbody: dict = r1add.json()
        assert r1add.status_code == codes.CREATED
        logjson("Added user during setup: ", r1addbody)
        r2add = await client.post("/", json=test_user_all_fields.model_dump())
        r2addbody: dict = r2add.json()
        assert r1add.status_code == codes.CREATED
        logjson("Added user during setup: ", r2addbody)

        # Gathering IDs of created users
        rget = await client.get("/")
        rgetbody: list[dict[str, Any]] = rget.json()
        test_usernames = (test_user_req_fields.username, test_user_all_fields.username)
        assert test_usernames is not None, "No test users were created (possible error during creating)"
        created_users_ids = [user.get("id") for user in rgetbody if user.get("username") in test_usernames]
        log.info(f"IDs of created users: {created_users_ids}")

        yield [r1addbody, r2addbody]

        # Removing created users
        delete_tasks = [client.delete(f"/{id}") for id in created_users_ids]
        results = await asyncio.gather(*delete_tasks)

        if all(r.status_code == 200 for r in results):
            log.info(f"Users with IDs {created_users_ids} has been deleted successfully")
        else:
            log.error(f"Error occured during deleting test users. Got status: {[r for r in results if r != 200]}")
