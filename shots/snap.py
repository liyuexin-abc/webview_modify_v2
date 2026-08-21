import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":1920,"height":1000})
        pg = await ctx.new_page()
        await pg.goto(f"{BASE}/#/login")
        await pg.wait_for_timeout(2500)
        html_btns = await pg.eval_on_selector_all("button", "els => els.map(e => e.textContent.trim())")
        print("buttons:", html_btns)
        await pg.fill('input[type="text"]', "demo")
        await pg.fill('input[type="password"]', "demo123")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(4000)
        print("url:", pg.url)
        await pg.screenshot(path="/home/user/webapp/shots/newbi_1920.png")
        await b.close()

asyncio.run(main())
