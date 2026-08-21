import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":1920,"height":1080})
        pg = await ctx.new_page()
        await pg.goto(f"{BASE}/#/login")
        await pg.wait_for_timeout(2000)
        await pg.fill('input[type="text"]', "demo")
        await pg.fill('input[type="password"]', "demo123")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(2500)
        # 管理端
        await pg.click("text=管理端")
        await pg.wait_for_timeout(2500)
        await pg.screenshot(path="/home/user/webapp/shots/admin_home.png")
        # 尝试点击语义模型菜单
        for label in ["模型与映射","语义模型","数据模型"]:
            try:
                await pg.click(f"text={label}", timeout=2000)
                await pg.wait_for_timeout(1500)
                break
            except Exception:
                pass
        await pg.screenshot(path="/home/user/webapp/shots/admin_menu.png")
        await b.close()

asyncio.run(main())
