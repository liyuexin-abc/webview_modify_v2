import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1000})
        await pg.goto(BASE + "/#/login")
        await pg.wait_for_timeout(1500)
        await pg.fill("input[type=text]", "demo")
        await pg.fill("input[type=password]", "demo")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(2500)

        ta = pg.locator("textarea").first
        await ta.fill("各地区销售额情况")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(2500)
        await pg.screenshot(path="/home/user/webapp/shots/v4_thinking.png")
        print("thinking ok")

        await pg.wait_for_timeout(10000)
        await pg.screenshot(path="/home/user/webapp/shots/v4_done.png")
        print("done ok")

        try:
            plus = pg.locator("button i.el-icon-plus").first
            await plus.click(timeout=8000)
            await pg.wait_for_timeout(1200)
            await pg.screenshot(path="/home/user/webapp/shots/v4_filter.png")
            print("filter ok")
        except Exception as e:
            print("filter fail", repr(e)[:200])

        await b.close()

asyncio.run(main())
