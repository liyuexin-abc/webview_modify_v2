import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1200})
        await pg.goto(BASE + "/#/login")
        await pg.wait_for_timeout(1500)
        await pg.fill("input[type=text]", "demo")
        await pg.fill("input[type=password]", "demo")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(2500)

        ta = pg.locator("textarea").first
        await ta.fill("各地区销售额情况")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(12000)

        await pg.click("text=各地区销售额与订单数")
        await pg.wait_for_timeout(1500)
        await pg.locator("button:visible", has_text="SQL").first.click()
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path="/home/user/webapp/shots/v5_sql.png")
        print("ok")
        await b.close()

asyncio.run(main())
