import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def login(pg):
    await pg.goto(BASE + "/#/login")
    await pg.wait_for_timeout(1500)
    await pg.fill("input[type=text]", "demo")
    await pg.fill("input[type=password]", "demo")
    await pg.keyboard.press("Enter")
    await pg.wait_for_timeout(2500)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1000})
        await login(pg)

        # ---- 1. admin nav ----
        await pg.click("text=管理端")
        await pg.wait_for_timeout(2500)
        await pg.screenshot(path="/home/user/webapp/shots/v4_nav.png")
        print("nav ok")

        # ---- 2. chat: ask a question, capture thinking + filter popover ----
        await pg.click("text=问数")
        await pg.wait_for_timeout(2000)
        ta = pg.locator("textarea").first
        await ta.fill("各地区销售额情况")
        await pg.keyboard.press("Enter")
        # thinking animation appears quickly
        await pg.wait_for_timeout(2500)
        await pg.screenshot(path="/home/user/webapp/shots/v4_thinking.png")
        print("thinking ok")
        # wait for full answer
        await pg.wait_for_timeout(9000)
        await pg.screenshot(path="/home/user/webapp/shots/v4_done.png")
        print("done ok")

        # open filter popover: hover then click the plus circle button
        btns = pg.locator(".el-dropdown button.el-icon-plus, button .el-icon-plus")
        try:
            plus = pg.locator("button i.el-icon-plus").first
            await plus.click()
            await pg.wait_for_timeout(1200)
            await pg.screenshot(path="/home/user/webapp/shots/v4_filter.png")
            print("filter ok")
        except Exception as e:
            print("filter fail", e)

        await b.close()

asyncio.run(main())
