import asyncio
import random
from typing import Optional, Dict
from playwright.async_api import async_playwright, BrowserContext, Page
from playwright_stealth import stealth_async
from .stealth import get_random_profile
import structlog

logger = structlog.get_logger(__name__)


class StealthBrowser:
    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.profile = get_random_profile()
        self.playwright = None
        self.browser = None
        self.context: Optional[BrowserContext] = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-setuid-sandbox",
        ]

        proxy_config = None
        if self.proxy_url:
            proxy_config = {"server": self.proxy_url}

        self.browser = await self.playwright.chromium.launch(
            headless=True,
            proxy=proxy_config,
            args=launch_args
        )

        self.context = await self.browser.new_context(
            user_agent=self.profile.user_agent,
            viewport=self.profile.viewport,
            device_scale_factor=1,
            has_touch=False,
            is_mobile=False,
        )

        # Apply stealth patches
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = {
                runtime: {}
            };
        """)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def new_page(self) -> Page:
        page = await self.context.new_page()
        await stealth_async(page)
        return page


async def human_delay(min_ms: int = 500, max_ms: int = 2000):
    await asyncio.sleep(random.randint(min_ms, max_ms) / 1000.0)
