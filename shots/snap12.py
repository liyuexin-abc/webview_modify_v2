import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def login(pg):
    await pg.goto(BASE + "/#/login")
    await pg.wait_for_timeout(1200)
    await pg.fill("input[type=text]", "demo")
    await pg.fill("input[type=password]", "demo")
    await pg.keyboard.press("Enter")
    await pg.wait_for_timeout(1800)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        await login(pg)

        # ---------- 1&3. 问数页：筛选条件 + 长标签 ----------
        ta = pg.locator("textarea").first
        await ta.fill("各地区销售额与告警情况")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(12000)

        await pg.click("text=各地区销售额与订单数")
        await pg.wait_for_timeout(1500)

        # 展开区域截图（标签 + 筛选条件）
        panel = pg.locator("text=筛选器").first
        box = await panel.bounding_box()
        print("filter label box:", box)
        if box:
            clip = {"x": 0, "y": max(box["y"] - 220, 0), "width": 1920, "height": 460}
            await pg.screenshot(path="/home/user/webapp/shots/v7_filter_tags.png", clip=clip)
        else:
            await pg.screenshot(path="/home/user/webapp/shots/v7_filter_tags.png")

        # 悬停长标签验证 tooltip
        tag = pg.locator(".queryDimPanel__text", has_text="近七日暂降").first
        try:
            await tag.hover()
            await pg.wait_for_timeout(900)
            tb = await tag.bounding_box()
            clip2 = {"x": max(tb["x"] - 260, 0), "y": max(tb["y"] - 110, 0), "width": 760, "height": 220}
            await pg.screenshot(path="/home/user/webapp/shots/v7_tag_tooltip.png", clip=clip2)
            print("tooltip shot ok")
        except Exception as e:
            print("tooltip skip:", e)

        # ---------- 2. 管理端指标管理：分页第5页 ----------
        await pg.click("text=管理端")
        await pg.wait_for_timeout(1500)
        await pg.click("text=指标与维度")
        await pg.wait_for_timeout(600)
        await pg.click("text=指标管理")
        await pg.wait_for_timeout(1800)

        # 点第5页
        try:
            await pg.click(".el-pager li:has-text('5')")
            await pg.wait_for_timeout(1200)
        except Exception as e:
            print("page5 click err:", e)

        pag = pg.locator(".pagination-container").first
        pb = await pag.bounding_box()
        print("pagination box:", pb)
        if pb:
            clip3 = {"x": max(pb["x"] - 10, 0), "y": max(pb["y"] - 10, 0), "width": min(1920, pb["width"] + 40), "height": pb["height"] + 30}
            await pg.screenshot(path="/home/user/webapp/shots/v7_pagination_p5.png", clip=clip3)
        await b.close()

asyncio.run(main())
