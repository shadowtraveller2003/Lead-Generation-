from playwright.async_api import Browser, Page, BrowserType


class PlaywrightEngineConfig:
    BROWSER_PARAMS = {'headless': False, 'proxy': None, 'slow_mo': 150}
    PAGE_PARAMS = {'java_script_enabled': True, 'bypass_csp': True}

    async def _setup_browser(self) -> None:
        chromium: BrowserType = self.playwright.chromium
        self.browser: Browser = await chromium.launch(**self.BROWSER_PARAMS)
        self.page: Page = await self.browser.new_page(**self.PAGE_PARAMS)
