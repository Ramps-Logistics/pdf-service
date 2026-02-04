import asyncio
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Browser

class BrowserPool:
    def __init__(self, max_contexts: int = 4):
        self._max_contexts = max_contexts
        self._playwright = None
        self._browser: Browser | None = None
        self._semaphore = asyncio.Semaphore(max_contexts)

    async def start(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=True,
            args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"]
        )

    async def stop(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    @asynccontextmanager
    async def acquire_context(self):
        async with self._semaphore:
            context = await self._browser.new_context()
            try:
                yield context
            finally:
                await context.close()

    @property
    def is_ready(self) -> bool:
        return self._browser is not None and self._browser.is_connected()

browser_pool = BrowserPool()
