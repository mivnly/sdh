from playwright.async_api import Page


class BasePage:
    url = "http://localhost:5173/"

    def __init__(self, page: Page):
        self.page = page

    async def navigate(self):
        await self.page.goto(self.url)
        await self.page.wait_for_load_state(state="load")
