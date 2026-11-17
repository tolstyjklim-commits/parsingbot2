"""
Парсер через браузер (Playwright) — обходит Cloudflare
"""
import asyncio
import json
import logging
from typing import Optional, Dict
from urllib.parse import urlencode
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)


class BrowserParser:
    def __init__(self, api_url: str = "https://peek.tg/api/nft/gifts/search"):
        self.api_url = api_url

    async def search(self, params: Dict, proxy: Optional[str] = None) -> Optional[Dict]:
        """Поиск подарков через браузер (обходит Cloudflare)"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                proxy={"server": proxy} if proxy else None,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-blink-features=AutomationControlled",
                ],
            )
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = await context.new_page()

            try:
                url = f"{self.api_url}?{urlencode(params)}"
                logger.info(f"🌐 Открываем: {url}")
                response = await page.goto(url, wait_until="networkidle", timeout=30000)

                if not response or response.status != 200:
                    logger.error(f"❌ HTTP {response.status if response else 'no response'}")
                    return None

                text = await page.inner_text("body")

                if text.strip().startswith("<!DOCTYPE") or "<html" in text[:100].lower():
                    logger.error("❌ Cloudflare вернул HTML вместо JSON")
                    return None

                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    logger.error(f"❌ Не JSON: {text[:200]}")
                    return None

            except Exception as e:
                logger.error(f"❌ Ошибка браузера: {e}")
                return None
            finally:
                await browser.close()
