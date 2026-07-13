import asyncio, json
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

        # Extract computed styles of key table elements
        styles = await page.evaluate("""() => {
            const pick = (el, props) => {
                if(!el) return null;
                const cs = getComputedStyle(el);
                const o = {};
                props.forEach(p => o[p] = cs.getPropertyValue(p));
                return o;
            };
            const res = {};
            const table = document.querySelector('table');
            res.table = pick(table, ['border-radius','border','box-shadow','font-size','background-color','border-collapse','border-spacing']);
            const th = document.querySelector('th');
            res.th = pick(th, ['background-color','color','font-size','font-weight','height','padding','border-bottom','text-transform','letter-spacing']);
            const td = document.querySelector('td');
            res.td = pick(td, ['color','font-size','height','padding','border-bottom','background-color','line-height']);
            const trs = document.querySelectorAll('tbody tr');
            if (trs.length>1) res.tr_even = pick(trs[1], ['background-color']);
            // table wrapper
            const wrap = table ? table.closest('div') : null;
            res.wrapper = pick(wrap, ['border-radius','border','box-shadow','background-color','overflow']);
            // page background & fonts
            res.body = pick(document.body, ['background-color','font-family','color','font-size']);
            // root CSS variables
            const rootCS = getComputedStyle(document.documentElement);
            const vars = {};
            // Grab from stylesheets any --xly / -- variables on :root
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules) {
                        if (rule.selectorText === ':root' || (rule.selectorText||'').includes(':root')) {
                            for (const name of rule.style) {
                                if (name.startsWith('--')) vars[name] = rule.style.getPropertyValue(name).trim();
                            }
                        }
                    }
                } catch(e){}
            }
            res.cssVars = vars;
            // sidebar & header
            const aside = document.querySelector('aside') || document.querySelector('[class*="sidebar"]') || document.querySelector('[class*="aside"]');
            res.aside = pick(aside, ['background-color','width','border-right','box-shadow']);
            const header = document.querySelector('header') || document.querySelector('[class*="header"]');
            res.header = pick(header, ['background-color','height','border-bottom','box-shadow']);
            // buttons
            const btn = document.querySelector('button[class*="primary"], .xly-btn--primary, button');
            res.button = pick(btn, ['background-color','color','border-radius','height','font-size','padding','border','box-shadow']);
            // pagination active
            const pgActive = document.querySelector('[class*="active"]');
            res.pgActive = pick(pgActive, ['background-color','color','border-radius','width','height','font-size']);
            return res;
        }""")
        print(json.dumps(styles, ensure_ascii=False, indent=1)[:6000])

        # scroll and take more shots of table variants
        await page.evaluate("window.scrollTo(0, 1200)")
        await page.wait_for_timeout(500)
        await page.screenshot(path='/home/user/webapp/easeui-study/05-variants1.png')
        await page.evaluate("window.scrollTo(0, 2600)")
        await page.wait_for_timeout(500)
        await page.screenshot(path='/home/user/webapp/easeui-study/06-variants2.png')
        await page.evaluate("window.scrollTo(0, 4200)")
        await page.wait_for_timeout(500)
        await page.screenshot(path='/home/user/webapp/easeui-study/07-variants3.png')
        await browser.close()

asyncio.run(main())
