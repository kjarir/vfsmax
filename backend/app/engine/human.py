import asyncio
import random
import math
from typing import Dict, Any, List
from playwright.async_api import Page, ElementHandle


class HumanActionSimulator:
    def __init__(self, page: Page):
        self.page = page

    async def sleep(self, min_ms: int = 500, max_ms: int = 2000):
        await asyncio.sleep(random.randint(min_ms, max_ms) / 1000.0)

    async def type_slowly(self, selector: str, text: str, min_delay_ms: int = 50, max_delay_ms: int = 150):
        """Type text with variable speed and occasional errors/corrections."""
        for char in text:
            # Simulate random delay before typing each character
            await self.sleep(min_delay_ms, max_delay_ms)
            
            # Simulate rare typing errors (2%)
            if random.random() < 0.02:
                # Type a random character
                wrong_char = chr(random.randint(97, 122))
                await self.page.type(selector, wrong_char)
                # Pause and backspace
                await self.sleep(200, 500)
                await self.page.keyboard.press("Backspace")
                await self.sleep(100, 300)

            await self.page.type(selector, char)

    async def move_mouse_humanly(self, target_element: ElementHandle):
        """Move mouse in a human-like non-bezier path to the target."""
        # Get target bounding box
        box = await target_element.bounding_box()
        if not box:
            return

        # Target center with slight randomness
        target_x = box["x"] + box["width"] / 2 + random.randint(-5, 5)
        target_y = box["y"] + box["height"] / 2 + random.randint(-5, 5)

        # Get current mouse position (mocked logic or use state)
        # Playwright doesn't easily expose current mouse X, Y without custom injection
        # But we can assume it starts from somewhere random or current
        # For simplicity, we just hover for now, but a real version would use paths
        await self.page.mouse.move(target_x, target_y, steps=random.randint(10, 20))

    async def click_humanly(self, selector: str):
        """Hover, pause, and click an element."""
        element = await self.page.wait_for_selector(selector)
        if not element:
            return
            
        await self.move_mouse_humanly(element)
        await self.sleep(200, 600)
        await self.page.click(selector)

    async def scroll_randomly(self):
        """Simulate a human user scrolling to read content."""
        scroll_count = random.randint(1, 3)
        for _ in range(scroll_count):
            delta = random.randint(200, 600)
            if random.random() < 0.3: delta = -delta # occasional scroll up
            await self.page.mouse.wheel(0, delta)
            await self.sleep(500, 1500)
