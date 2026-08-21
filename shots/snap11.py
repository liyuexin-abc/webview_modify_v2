import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1000})
        await pg.goto(BASE + "/#/login")
        await pg.wait_for_timeout(1500)
        await pg.fill("input[type=text]", "demo")
        await pg.fill("input[type=password]", "demo")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(3000)
        # default collapsed
        await pg.screenshot(path="/home/user/webapp/shots/v6_history_collapsed.png", clip={"x":0,"y":380,"width":300,"height":500})
        # expand first group
        labels = pg.locator(".history-sidebar__group-label")
        n = await labels.count()
        print("groups:", n)
        if n:
            await labels.first.click()
            await pg.wait_for_timeout(600)
            await pg.screenshot(path="/home/user/webapp/shots/v6_history_expanded.png", clip={"x":0,"y":380,"width":300,"height":500})
        print("ok")
        await b.close()

asyncio.run(main())
