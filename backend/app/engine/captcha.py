import base64
import requests
import asyncio
from typing import Optional, Dict, Any
from app.core.config import settings
import structlog
from openai import OpenAI

logger = structlog.get_logger(__name__)


class CaptchaSolver:
    def __init__(self):
        self.two_captcha_key = settings.TWOCAPTCHA_API_KEY
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def solve_image_captcha(self, base64_image: str) -> Optional[str]:
        """Layer 2: AI Vision Solver using GPT-4o Vision API."""
        try:
            logger.info("Solving image CAPTCHA via GPT-4o Vision...")
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "This is a CAPTCHA image from a visa application website. Please identify the text/objects requested. Return ONLY the answer string and nothing else."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                        ]
                    }
                ],
                max_tokens=10
            )

            answer = response.choices[0].message.content.strip()
            logger.info("GPT-4o Vision solved CAPTCHA", answer=answer)
            return answer
        except Exception as e:
            logger.error("GPT-4o Vision CAPTCHA solving failed", error=str(e))
            return None

    async def solve_with_2captcha(self, site_key: str, page_url: str, captcha_type: str = "recaptcha") -> Optional[str]:
        """Layer 1: External Solvers using 2captcha API."""
        if not self.two_captcha_key:
            return None

        # Logic for 2captcha (Simplifying for now)
        # 1. Create task
        # 2. Poll for solution
        # 3. Return token
        logger.info("Solving CAPTCHA via 2captcha...", type=captcha_type)
        # Mocking 2captcha interaction
        await asyncio.sleep(20) # Simulating wait
        return "mocked-2captcha-token"

    async def determine_captcha_type_and_solve(self, page_element: Any) -> Optional[str]:
        """Main dispatcher for CAPTCHA solving."""
        # Detect if it's Recaptcha (v2/v3), hCaptcha, or Image-based
        # For now, let's assume image-based for image tags and recaptcha for others
        return await self.solve_image_captcha("mock-base64")
        
    async def bypass_cloudflare(self, page: Any):
        """Bypass Cloudflare by waiting for the 5-second challenge."""
        logger.info("Waiting for Cloudflare bypass...")
        await page.wait_for_selector("iframe", state="hidden", timeout=30000)
        logger.info("Cloudflare challenge bypassed!")
