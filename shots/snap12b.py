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

        # 子菜单默认展开，直接点菜单项
        item = pg.locator(".el-menu-item", has_text="指标管理").first
        await item.click()
        await pg.wait_for_timeout(2000)

        for target in ["5", "6", "1"]:
            try:
                await pg.click(f".el-pager li:text-is('{target}')")
                await pg.wait_for_timeout(1000)
            except Exception as e:
                print("click", target, "err:", e)
            pag = pg.locator(".pagination-container").first
            pb = await pag.bounding_box()
            print("page", target, "box:", pb)
            if pb:
                clip = {"x": max(pb["x"] - 10, 0), "y": max(pb["y"] - 10, 0),
                        "width": min(1920 - max(pb["x"] - 10, 0), pb["width"] + 40),
                        "height": pb["height"] + 30}
                await pg.screenshot(path=f"/home/user/webapp/shots/v7_pagination_p{target}.png", clip=clip)
        await b.close()

asyncio.run(main())
