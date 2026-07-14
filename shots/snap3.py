import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def shoot(pg, path):
    await pg.screenshot(path=path)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w,h,tag in [(1920,1080,"1920"),(1366,768,"1366")]:
            ctx = await b.new_context(viewport={"width":w,"height":h})
            pg = await ctx.new_page()
            await pg.goto(f"{BASE}/#/login")
            await pg.wait_for_timeout(2000)
            await pg.fill('input[type="text"]', "demo")
            await pg.fill('input[type="password"]', "demo123")
            await pg.keyboard.press("Enter")
            await pg.wait_for_timeout(2500)
            await shoot(pg, f"/home/user/webapp/shots/welcome_{tag}.png")
            await pg.fill('textarea', "近半年各地区的销售额和订单数是多少？")
            await pg.keyboard.press("Enter")
            await pg.wait_for_timeout(6500)
            # 展开查询步骤
            heads = await pg.query_selector_all(".aiCollapse .el-collapse-item__header")
            if heads: await heads[0].click()
            await pg.wait_for_timeout(1200)
            await shoot(pg, f"/home/user/webapp/shots/result_{tag}.png")
            if tag == "1920":
                # 打开 SQL 弹窗
                btns = await pg.query_selector_all("button")
                for btn in btns:
                    t = (await btn.text_content() or "").strip()
                    if t == "SQL":
                        await btn.click(); break
                await pg.wait_for_timeout(1000)
                await shoot(pg, "/home/user/webapp/shots/sql_dialog.png")
            await ctx.close()
        await b.close()

asyncio.run(main())
