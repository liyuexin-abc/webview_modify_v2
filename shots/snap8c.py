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

        await pg.click("text=管理端")
        await pg.wait_for_timeout(2000)
        await pg.click("text=数据源管理")
        await pg.wait_for_timeout(1500)
        await pg.click("text=新建数据源")
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path="/home/user/webapp/shots/v3_ds_dialog.png")
        print("ok")
        await b.close()

asyncio.run(main())
