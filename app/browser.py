import asyncio
import time
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Browser
from .config import settings

class BrowserPool:
    def __init__(self, max_contexts: int = 4):
        self._max_contexts = max_contexts
        self._playwright = None
        self._browser: Browser | None = None
        self._semaphore = asyncio.Semaphore(max_contexts)
        self._active = 0
        self._waiting = 0
        self._total_rendered = 0
        self._total_render_time = 0.0

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
        self._waiting += 1
        start = time.perf_counter()
        async with self._semaphore:
            self._waiting -= 1
            self._active += 1
            context = await self._browser.new_context()
            try:
                yield context
            finally:
                await context.close()
                self._active -= 1
                self._total_rendered += 1
                self._total_render_time += time.perf_counter() - start

    @property
    def is_ready(self) -> bool:
        return self._browser is not None and self._browser.is_connected()

    @property
    def stats(self) -> dict:
        avg_time = (self._total_render_time / self._total_rendered) if self._total_rendered > 0 else 0
        return {
            "max_concurrent": self._max_contexts,
            "active": self._active,
            "waiting": self._waiting,
            "available": self._max_contexts - self._active,
            "total_rendered": self._total_rendered,
            "avg_render_time_ms": round(avg_time * 1000, 1),
        }

browser_pool = BrowserPool(max_contexts=settings.max_browser_contexts)
