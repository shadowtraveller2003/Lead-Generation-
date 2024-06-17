import asyncio
from playwright.async_api import Playwright, async_playwright

from py_lead_generation.src.misc.writer import CsvWriter
from py_lead_generation.src.engines.playwright_config import PlaywrightEngineConfig


class BaseEngine(PlaywrightEngineConfig):
    async def run(self) -> None:
        async with async_playwright() as playwright:
            self.playwright: Playwright = playwright
            await self._setup_browser()
            await self._open_url_and_wait(self.url)
            urls: list[str] = await self._get_search_results_urls()
            self._entries: list[dict] = await self._get_search_results_entries(urls)
            await self.browser.close()

    def save_to_csv(self, filename: str = None) -> None:
        if filename:
            self.FILENAME = filename

        if not self.FILENAME.endswith('.csv'):
            raise ValueError('Use .csv file extension')
        if not self._entries:
            raise NotImplementedError(
                'Entries are empty, call .run() method first to save them'
            )
        csv_writer = CsvWriter(self.FILENAME, self.FIELD_NAMES)
        csv_writer.append(self._entries)

    @property
    def entries(self) -> list[dict]:
        if not self._entries:
            raise NotImplementedError(
                'Entries are empty, call .run() method first to create them'
            )
        return self._entries

    @entries.setter
    def entries(self, _) -> None:
        raise ValueError('Cannot set value to data. This is not allowed')

    async def _open_url_and_wait(self, url: str, sleep_duration_s: int = 3) -> None:
        await self.page.goto(url)
        await asyncio.sleep(sleep_duration_s)

    async def _get_search_results_entries(self, urls: list[str]) -> list[dict]:
        entries = []
        for url in urls:
            await self._open_url_and_wait(url, 1.5)
            html = await self.page.content()
            data = self._parse_data_with_soup(html)
            entry = dict(zip(self.FIELD_NAMES, data))
            entries.append(entry)

        return entries
