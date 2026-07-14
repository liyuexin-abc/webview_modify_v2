import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        await pg.goto(BASE + "/#/login")
        await pg.wait_for_timeout(1200)
        await pg.fill("input[type=text]", "demo")
        await pg.fill("input[type=password]", "demo")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(1800)

        await pg.click("text=管理端")
        await pg.wait_for_timeout(1800)
        await pg.locator(".el-menu-item", has_text="指标管理").first.click()
        await pg.wait_for_timeout(2000)

        conts = pg.locator(".pagination-container")
        n = await conts.count()
        for i in range(n):
            print(i, await conts.nth(i).bounding_box())

        pagers = pg.locator(".el-pager li.number")
        pn = await pagers.count()
        print("pager numbers:", pn)
        for i in range(pn):
            t = await pagers.nth(i).inner_text()
            bx = await pagers.nth(i).bounding_box()
            print("  ", t, bx)

        await pg.screenshot(path="/home/user/webapp/shots/v7_metric_page_full.png", full_page=False)
        await b.close()

asyncio.run(main())
