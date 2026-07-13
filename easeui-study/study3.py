import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width':1600,'height':1000})
        await page.goto('https://ease-ui.com/', wait_until='networkidle', timeout=60000)
        inputs = await page.query_selector_all('input')
        await inputs[0].fill('EaseUI'); await inputs[1].fill('123456')
        for b in await page.query_selector_all('button'):
            if '立即登录' in (await b.inner_text()):
                await b.click(); break
        await page.wait_for_timeout(3000)
        await page.goto('https://ease-ui.com/data/table', wait_until='networkidle', timeout=60000)
        await page.wait_for_timeout(2000)
        # find scrollable container
        info = await page.evaluate("""() => {
          const els = document.querySelectorAll('*');
          const out = [];
          els.forEach(e => { if (e.scrollHeight - e.clientHeight > 500) out.push({tag:e.tagName, cls:e.className && e.className.toString().slice(0,60), sh:e.scrollHeight, ch:e.clientHeight}); });
          return out.slice(0,10);
        }""")
        print(info)
        # scroll inner container
        for i, y in enumerate([1400, 2800, 4200, 5600, 7000]):
            await page.evaluate(f"""() => {{
              const els = document.querySelectorAll('*');
              for (const e of els) {{ if (e.scrollHeight - e.clientHeight > 500) {{ e.scrollTop = {y}; break; }} }}
            }}""")
            await page.wait_for_timeout(600)
            await page.screenshot(path=f'/home/user/webapp/easeui-study/scroll-{i}.png')
        await browser.close()

asyncio.run(main())
