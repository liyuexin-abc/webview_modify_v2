import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def shoot(pg, name):
    # 取包含可见页码的分页容器
    conts = pg.locator(".pagination-container")
    n = await conts.count()
    for i in range(n):
        c = conts.nth(i)
        if await c.locator(".el-pager li.number").first.is_visible():
            pb = await c.bounding_box()
            clip = {"x": max(pb["x"] - 8, 0), "y": max(pb["y"] - 8, 0),
                    "width": min(1920 - max(pb["x"] - 8, 0), pb["width"] + 24),
                    "height": pb["height"] + 24}
            await pg.screenshot(path=f"/home/user/webapp/shots/{name}.png", clip=clip)
            print("shot", name, pb)
            return c
    return None

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

        c = await shoot(pg, "v7_pagination_p1")
        # 点第5页（在可见容器内）
        await c.locator(".el-pager li.number", has_text="5").first.click()
        await pg.wait_for_timeout(1200)
        await shoot(pg, "v7_pagination_p5")
        c2 = await shoot(pg, "_tmp")
        await c2.locator(".el-pager li.number", has_text="6").first.click()
        await pg.wait_for_timeout(1200)
        await shoot(pg, "v7_pagination_p6")
        await b.close()

asyncio.run(main())
