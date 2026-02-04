import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from playwright.async_api import Browser, BrowserContext, async_playwright

from app.config import settings


class BrowserPool:
    def __init__(self, max_contexts: int = settings.MAX_BROWSER_CONTEXTS):
        self._browser: Browser | None = None
        self._playwright = None
        self._semaphore = asyncio.Semaphore(max_contexts)
        self._started = False

    async def start(self) -> None:
        if self._started:
            return
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=True)
        self._started = True

    async def stop(self) -> None:
        if not self._started:
            return
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
        self._started = False

    @property
    def is_ready(self) -> bool:
        return self._started and self._browser is not None

    @asynccontextmanager
    async def acquire_context(self) -> AsyncGenerator[BrowserContext, None]:
        if not self.is_ready:
            raise RuntimeError("Browser pool not started")
        async with self._semaphore:
            context = await self._browser.new_context()
            try:
                yield context
            finally:
                await context.close()


browser_pool = BrowserPool()
