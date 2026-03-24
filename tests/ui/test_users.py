from playwright.async_api import Page

from tests.ui.models.users import UsersPage
from tests.utils import generate_datetime_id


async def test_add_user(page: Page):
    username = f"TestUser_{generate_datetime_id()}"

    p = UsersPage(page)
    await p.navigate()
    await p.add_user(
        name="Test",
        surname="Test",
        username=username,
        role="user",
        comment="TestComment"
    )

    test_user = await p.get_user_by_username(username)
    assert test_user["name"] == "Test"
    assert test_user["surname"] == "Test"
    assert test_user["username"] == f"{username}"
    assert test_user["role"] == "user"
    assert test_user["comment"] == "TestComment"

    await p.delete_user(username)


async def test_get_user(add_test_users, page: Page):
    created_user_req_fields = add_test_users[0]
    p = UsersPage(page)

    await p.navigate()
    current_test_user = await p.get_user_by_username(created_user_req_fields["username"])

    assert created_user_req_fields["username"] == current_test_user["username"]
    assert created_user_req_fields["role"] == current_test_user["role"]
