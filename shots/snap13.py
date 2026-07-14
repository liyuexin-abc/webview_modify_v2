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

        panel = pg.locator("text=筛选器").first
        box = await panel.bounding_box()
        if box:
            clip = {"x": 0, "y": max(box["y"] - 220, 0), "width": 1920, "height": 470}
            await pg.screenshot(path="/home/user/webapp/shots/v8_filter_tags.png", clip=clip)

        # 悬停长标签（应显示 tooltip）
        tag_long = pg.locator(".queryDimPanel__text", has_text="近七日暂降").first
        await tag_long.hover()
        await pg.wait_for_timeout(900)
        tb = await tag_long.bounding_box()
        clip2 = {"x": max(tb["x"] - 260, 0), "y": max(tb["y"] - 110, 0), "width": 760, "height": 220}
        await pg.screenshot(path="/home/user/webapp/shots/v8_tag_tooltip_long.png", clip=clip2)

        # 悬停短标签（不应显示 tooltip）
        tag_short = pg.locator(".queryDimPanel__text", has_text="销售额").first
        await tag_short.hover()
        await pg.wait_for_timeout(900)
        sb = await tag_short.bounding_box()
        clip3 = {"x": max(sb["x"] - 200, 0), "y": max(sb["y"] - 110, 0), "width": 640, "height": 200}
        await pg.screenshot(path="/home/user/webapp/shots/v8_tag_tooltip_short.png", clip=clip3)

        # 日期区间放大
        date = pg.locator(".filter-cond__date").first
        db = await date.bounding_box()
        clip4 = {"x": max(db["x"] - 130, 0), "y": max(db["y"] - 20, 0), "width": db["width"] + 200, "height": db["height"] + 40}
        await pg.screenshot(path="/home/user/webapp/shots/v8_date_range.png", clip=clip4)
        await b.close()

asyncio.run(main())
