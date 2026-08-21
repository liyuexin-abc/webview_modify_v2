import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8080"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1000})
        await pg.goto(BASE + "/#/login")
        await pg.wait_for_timeout(1200)
        await pg.fill("input[type=text]", "demo")
        await pg.fill("input[type=password]", "demo")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(1800)

        await pg.click("text=管理端")
        await pg.wait_for_timeout(1500)
        await pg.click("text=数据表管理")
        await pg.wait_for_timeout(1500)
        await pg.click("text=注册视图")
        await pg.wait_for_timeout(1500)
        n = await pg.locator(".sql-editor__textarea").count()
        print("sql editor textareas:", n)
        sql = "SELECT p.patient_id, p.patient_name, COUNT(v.visit_id) AS visit_cnt, SUM(v.total_fee) AS total_fee FROM dim_patient p LEFT JOIN dws_visit_df v ON p.patient_id = v.patient_id WHERE v.dt >= '2026-01-01' GROUP BY p.patient_id, p.patient_name ORDER BY total_fee DESC LIMIT 100"
        await pg.locator(".sql-editor__textarea").first.fill(sql)
        await pg.wait_for_timeout(400)
        try:
            await pg.locator(".sql-editor__format").first.click(timeout=3000)
            await pg.wait_for_timeout(400)
        except Exception as e:
            print("format skip:", e)
        await pg.locator(".sql-editor__textarea").first.click()
        await pg.wait_for_timeout(300)
        await pg.screenshot(path="/home/user/webapp/shots/v3_sql_editor.png")
        print("sql editor shot ok")

        # 直接刷新页面回管理端拍数据源弹窗
        await pg.goto(BASE + "/#/index")
        await pg.wait_for_timeout(1500)
        await pg.click("text=管理端")
        await pg.wait_for_timeout(1500)
        await pg.click("text=数据源管理")
        await pg.wait_for_timeout(1200)
        await pg.click("text=新建数据源")
        await pg.wait_for_timeout(900)
        await pg.screenshot(path="/home/user/webapp/shots/v3_ds_dialog.png")
        print("ds dialog shot ok")

        await b.close()

asyncio.run(main())
