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
        pg = await b.new_page(viewport={"width": 1920, "height": 1000})
        await login(pg)

        # 1. 发起问数, 抓思考中动画帧
        await pg.fill("textarea", "各区域销售额是多少")
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path="/home/user/webapp/shots/v3_thinking.png")

        # 2. 等结果, 全流程截图(序号/框条/渐变卡片)
        await pg.wait_for_timeout(9000)
        await pg.screenshot(path="/home/user/webapp/shots/v3_chat_full.png", full_page=False)

        # 3. 展开查数看筛选标签圆角
        try:
            await pg.click("text=查询", timeout=3000)
            await pg.wait_for_timeout(800)
            await pg.screenshot(path="/home/user/webapp/shots/v3_query_tags.png")
        except Exception as e:
            print("query expand skip:", e)

        # 4. 智能体配置弹窗(留白)
        await pg.click(".agent-sidebar__add, [class*='agent-sidebar'] button", timeout=4000)
        await pg.wait_for_timeout(1000)
        await pg.screenshot(path="/home/user/webapp/shots/v3_agent_dialog.png")
        await pg.keyboard.press("Escape")
        await pg.click("text=取消")
        await pg.wait_for_timeout(600)

        # 5. 管理端 - 注册视图(SQL 编辑器高亮)
        await pg.click("text=管理端")
        await pg.wait_for_timeout(1200)
        await pg.click("text=模型与映射")
        await pg.wait_for_timeout(600)
        await pg.click("text=数据表管理")
        await pg.wait_for_timeout(1200)
        await pg.click("text=注册视图")
        await pg.wait_for_timeout(1000)
        sql = "SELECT p.patient_id, p.patient_name, COUNT(v.visit_id) AS visit_cnt, SUM(v.total_fee) AS total_fee FROM dim_patient p LEFT JOIN dws_visit_df v ON p.patient_id = v.patient_id WHERE v.dt >= '2026-01-01' GROUP BY p.patient_id, p.patient_name ORDER BY total_fee DESC LIMIT 100"
        await pg.fill(".sql-editor__textarea", sql)
        await pg.wait_for_timeout(500)
        # 点击格式化
        try:
            await pg.click(".sql-editor__format", timeout=2000)
            await pg.wait_for_timeout(500)
        except Exception as e:
            print("format skip:", e)
        await pg.screenshot(path="/home/user/webapp/shots/v3_sql_editor.png")
        await pg.click("text=取消")
        await pg.wait_for_timeout(600)

        # 6. 新建数据源弹窗(留白 + 渐变按钮)
        await pg.click("text=数据接入")
        await pg.wait_for_timeout(500)
        await pg.click("text=数据源管理")
        await pg.wait_for_timeout(1000)
        await pg.click("text=新建数据源")
        await pg.wait_for_timeout(900)
        await pg.screenshot(path="/home/user/webapp/shots/v3_ds_dialog.png")

        await b.close()
        print("done")

asyncio.run(main())
