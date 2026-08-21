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

        ta = pg.locator("textarea").first
        await ta.fill("各地区销售额与告警情况")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(12000)

        await pg.click("text=各地区销售额与订单数")
        await pg.wait_for_timeout(1500)

        # 整体筛选区（含多选值胶囊 + 日期胶囊）
        panel = pg.locator("text=筛选器").first
        box = await panel.bounding_box()
        if box:
            clip = {"x": 0, "y": max(box["y"] - 30, 0), "width": 1920, "height": 240}
            await pg.screenshot(path="/home/user/webapp/shots/v9_filters.png", clip=clip)

        # 测量每个 filter-cond 宽度，验证日期胶囊与其他一致
        conds = pg.locator(".filter-cond")
        n = await conds.count()
        widths = []
        for i in range(n):
            bb = await conds.nth(i).bounding_box()
            if bb:
                widths.append(round(bb["width"], 1))
        print("filter-cond widths:", widths)

        # 多选胶囊放大截图
        msel = pg.locator(".filter-cond__value--select").first
        mb = await msel.bounding_box()
        if mb:
            clip2 = {"x": max(mb["x"] - 240, 0), "y": max(mb["y"] - 20, 0), "width": 460, "height": mb["height"] + 40}
            await pg.screenshot(path="/home/user/webapp/shots/v9_multiselect.png", clip=clip2)

        await b.close()

asyncio.run(main())
