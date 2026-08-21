import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":1920,"height":1080})
        pg = await ctx.new_page()
        pg.on("console", lambda m: m.type == "error" and print("ERR:", m.text[:200]))
        await pg.goto(f"{BASE}/#/login")
        await pg.wait_for_timeout(2000)
        await pg.fill('input[type="text"]', "demo")
        await pg.fill('input[type="password"]', "demo123")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(3000)
        # 输入问题
        await pg.fill('textarea', "近半年各地区的销售额和订单数是多少？")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(2000)
        await pg.screenshot(path="/home/user/webapp/shots/query_thinking.png")
        await pg.wait_for_timeout(4000)
        await pg.screenshot(path="/home/user/webapp/shots/query_result.png", full_page=False)
        # 滚动主区域到底
        await pg.evaluate("document.querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+50&&e.clientHeight>300)e.scrollTop=e.scrollHeight})")
        await pg.wait_for_timeout(800)
        await pg.screenshot(path="/home/user/webapp/shots/query_result_bottom.png")
        await b.close()

asyncio.run(main())
