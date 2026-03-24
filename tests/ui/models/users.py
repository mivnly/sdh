from typing import Literal

from playwright.async_api import Locator, Page

from tests.utils import log
from tests.ui.models.base import BasePage


class UsersPage(BasePage):
    url = BasePage.url + "users/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = page.locator("xpath=//h1[contains(text(), 'Users')]")
        self.table = UserTable(self.page)
        self.modal = AddUserModal(self.page)
        self.button_add_user = page.locator("xpath=//text()[contains(., 'Добавить пользователя')]/parent::button")

    async def add_user(
        self,
        username: str,
        role: Literal["user", "admin"],
        name: str | None = None,
        surname: str | None = None,
        comment: str | None = None,
    ) -> None:
        await self.button_add_user.click()
        await self.modal.fill_form(
            name=name,
            surname=surname,
            username=username,
            role=role,
            comment=comment,
        )
        await self.modal.button_add.click()

    async def get_user_by_username(self, username: str) -> dict[str, str]:
        users_table = self.table.columns_dict
        log.info(users_table)
        return {
            k: await self.page.locator(f"xpath=//tbody//td[text()='{username}']/parent::tr/td[{v}]").inner_text()
            for k, v in users_table.items()
        }

    async def edit_user(
        self,
        current_username: str,
        name: str | None = None,
        surname: str | None = None,
        username: str | None = None,
        role: str | None = None,
        comment: str | None = None,
    ) -> None:
        b = self.table.get_edit_button_by_username(current_username)
        await b.click()

        await self.modal.fill_form(
            name=name,
            surname=surname,
            username=username,
            role=role,
            comment=comment,
        )

        await self.modal.button_add.click()

    async def delete_user(self, username: str) -> None:
        b = self.table.get_delete_button_by_username(username)
        await b.click()


class AddUserModal:
    def __init__(self, page: Page):
        self.modal = page.locator("xpath=//h2[contains(text(), 'Новый пользователь')]/parent::div")

        self.name = page.locator("xpath=//input[@placeholder='Name']")
        self.surname = page.locator("xpath=//input[@placeholder='Surname']")
        self.username = page.locator("xpath=//input[@placeholder='Username']")
        self.role = page.locator("xpath=//input[@placeholder='Role']")
        self.comment = page.locator("xpath=//input[@placeholder='Comment']")

        self.button_add = page.locator(
            "xpath=//h2[text()='Новый пользователь' or text()='Редактировать пользователя']/parent::div//button[text()='Добавить' or text()='Сохранить']"
        )
        self.button_cancel = page.locator(
            "xpath=//h2[text()='Новый пользователь' or text()='Редактировать пользователя']/parent::div//button[contains(text(), 'Отмена')]"
        )

    async def fill_form(
            self,
            *,
            name: str | None = None,
            surname: str | None = None,
            username: str | None = None,
            role: str | None = None,
            comment: str | None = None,
        ) -> None:
            field_map = {
                "name": self.name,
                "surname": self.surname,
                "username": self.username,
                "role": self.role,
                "comment": self.comment,
            }

            data = {
                "name": name,
                "surname": surname,
                "username": username,
                "role": role,
                "comment": comment,
            }

            for field, locator in field_map.items():
                value = data[field]
                if value is not None:
                    await locator.fill(value)


class UserTable:
    def __init__(self, page: Page):
        self.page = page

        self.id = page.locator("xpath=//th[text()='ID']")
        self.name = page.locator("xpath=//th[text()='Name']")
        self.surname = page.locator("xpath=//th[text()='Surname']")
        self.username = page.locator("xpath=//th[text()='Username']")
        self.role = page.locator("xpath=//th[text()='Role']")
        self.comment = page.locator("xpath=//th[text()='Comment']")
        self.actions = page.locator("xpath=//th[text()='Действия']")

    @property
    def columns_dict(self) -> dict[str, int]:
        return {attr: idx for idx, attr in enumerate(self.__dict__.keys()) if idx > 0}

    def get_edit_button_by_username(self, username: str) -> Locator:
        return self.page.locator(f"xpath=//tbody//td[text()='{username}']/parent::tr//button[@title='Редактировать']")

    def get_delete_button_by_username(self, username: str) -> Locator:
        return self.page.locator(f"xpath=//tbody//td[text()='{username}']/parent::tr//button[@title='Удалить']")
