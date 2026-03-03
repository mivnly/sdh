import re
from datetime import datetime

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
    async with AsyncClient() as client:
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
            await client.delete(str(users_url) + f"{id}")

        log.info(f"Deleting users with IDs: {matched_ids}")


@pytest_asyncio.fixture(scope="function")
async def add_test_users(delete_test_users, users_url: URL) -> list[str]:
    async with AsyncClient() as client:
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

        r1 = await client.post(users_url, json=test_user_req_fields.model_dump())
        r1body = r1.json()
        logjson("Added user: ", r1body)
        r2 = await client.post(users_url, json=test_user_all_fields.model_dump())
        r2body = r2.json()
        logjson("Added user: ", r2body)

        return [test_user_req_fields.username, test_user_all_fields.username]
