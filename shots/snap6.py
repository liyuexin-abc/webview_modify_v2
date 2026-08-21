import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def login(pg):
    await pg.goto(f"{BASE}/#/login")
    await pg.wait_for_selector("input[type=text]")
    await pg.fill("input[type=text]", "demo")
    await pg.fill("input[type=password]", "demo")
    await pg.keyboard.press("Enter")
    await pg.wait_for_timeout(2500)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # 1440 chat
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await login(pg)
        await pg.fill("textarea", "各区域销售额是多少")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(6000)
        await pg.screenshot(path="/home/user/webapp/shots/v2_1440_chat.png")
        await pg.close()

        # 2560 welcome + admin
        pg = await b.new_page(viewport={"width": 2560, "height": 1300})
        await login(pg)
        await pg.screenshot(path="/home/user/webapp/shots/v2_2560_welcome.png")
        await pg.click("text=管理端")
        await pg.wait_for_timeout(1500)
        # open new data source dialog
        try:
            await pg.click("text=新建数据源", timeout=4000)
            await pg.wait_for_timeout(1200)
            await pg.screenshot(path="/home/user/webapp/shots/v2_2560_dsform.png")
        except Exception as e:
            print("dsform:", e)
        await b.close()

asyncio.run(main())
