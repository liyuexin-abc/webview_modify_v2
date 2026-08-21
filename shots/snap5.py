import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def login(pg):
    await pg.goto(f"{BASE}/#/login")
    await pg.wait_for_selector("input[type=text]")
    await pg.fill("input[type=text]", "demo")
    await pg.fill("input[type=password]", "demo")
    await pg.keyboard.press("Enter")
    await pg.wait_for_timeout(2500)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        pg.on("console", lambda m: m.type == "error" and print("CONSOLE ERR:", m.text[:200]))
        await login(pg)

        # 1) TopNav switch
        await pg.screenshot(path="/home/user/webapp/shots/v2_topnav.png", clip={"x": 1100, "y": 0, "width": 820, "height": 60})

        # 2) agent config dialog (click plus in sidebar header)
        await pg.click(".agent-sidebar__header button, .agent-sidebar .add-btn, .agent-sidebar__add", timeout=5000)
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path="/home/user/webapp/shots/v2_agent_dialog.png")
        # close
        await pg.click("text=取消")
        await pg.wait_for_timeout(600)

        # 3) chat flow
        await pg.fill("textarea", "各区域销售额是多少")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(6000)
        await pg.screenshot(path="/home/user/webapp/shots/v2_chat.png", full_page=False)

        # 4) admin -> field mapping -> register view dialog
        await pg.click("text=管理端")
        await pg.wait_for_timeout(1000)
        await pg.click("text=数据表管理")
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path="/home/user/webapp/shots/v2_fieldmapping.png")
        # try open register view
        try:
            await pg.click("text=注册视图", timeout=4000)
            await pg.wait_for_timeout(1200)
            await pg.screenshot(path="/home/user/webapp/shots/v2_regview.png")
            # type SQL to see editor
            await pg.click(".sql-editor__textarea")
            await pg.type(".sql-editor__textarea", "SELECT patient_id,\n       patient_name,\n       COUNT(1) AS visit_cnt\nFROM ods_visit\nGROUP BY patient_id, patient_name")
            await pg.wait_for_timeout(500)
            await pg.click("text=执行并解析")
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path="/home/user/webapp/shots/v2_regview_sql.png")
        except Exception as e:
            print("regview:", e)
        await b.close()

asyncio.run(main())
