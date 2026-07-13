import asyncio, json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width':1600,'height':900})
        await page.goto('https://ease-ui.com/', wait_until='networkidle', timeout=60000)
        await page.screenshot(path='/home/user/webapp/easeui-study/01-login.png')
        # try login with test account
        inputs = await page.query_selector_all('input')
        print('inputs:', len(inputs))
        if len(inputs) >= 2:
            await inputs[0].fill('EaseUI')
            await inputs[1].fill('123456')
            # find login button
            btn = await page.query_selector('button')
            btns = await page.query_selector_all('button')
            for b in btns:
                t = (await b.inner_text()).strip()
                print('btn:', t)
                if '登录' in t or 'login' in t.lower():
                    await b.click()
                    break
            await page.wait_for_timeout(4000)
        print('url after login:', page.url)
        await page.screenshot(path='/home/user/webapp/easeui-study/02-after-login.png')
        await page.goto('https://ease-ui.com/data/table', wait_until='networkidle', timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(path='/home/user/webapp/easeui-study/03-data-table.png', full_page=False)
        await page.screenshot(path='/home/user/webapp/easeui-study/04-data-table-full.png', full_page=True)
        print('final url:', page.url)
        await browser.close()

asyncio.run(main())
