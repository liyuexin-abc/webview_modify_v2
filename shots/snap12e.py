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
        await pg.wait_for_timeout(2200)

        # 可见分页容器
        conts = pg.locator(".pagination-container")
        cont = None
        for i in range(await conts.count()):
            c = conts.nth(i)
            if await c.locator(".el-pager li.number").first.is_visible():
                cont = c
                break

        async def state():
            act = await cont.locator(".el-pager li.active").inner_text()
            first_row = await pg.locator(".el-table__body tr td").first.inner_text()
            return act, first_row

        print("before:", await state())
        await cont.locator(".el-pager li.number", has_text="5").first.click()
        await pg.wait_for_timeout(1500)
        print("after 5:", await state())
        pb = await cont.bounding_box()
        clip = {"x": max(pb["x"]-8,0), "y": max(pb["y"]-8,0),
                "width": min(1920-max(pb["x"]-8,0), pb["width"]+24), "height": pb["height"]+24}
        await pg.screenshot(path="/home/user/webapp/shots/v7_pag_p5.png", clip=clip)

        await cont.locator(".el-pager li.number", has_text="6").first.click()
        await pg.wait_for_timeout(1500)
        print("after 6:", await state())
        pb = await cont.bounding_box()
        clip = {"x": max(pb["x"]-8,0), "y": max(pb["y"]-8,0),
                "width": min(1920-max(pb["x"]-8,0), pb["width"]+24), "height": pb["height"]+24}
        await pg.screenshot(path="/home/user/webapp/shots/v7_pag_p6.png", clip=clip)
        await b.close()

asyncio.run(main())
