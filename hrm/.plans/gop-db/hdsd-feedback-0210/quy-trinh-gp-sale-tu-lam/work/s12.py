from common import *
with browser_page() as page:
    page.on('response', lambda r: print('RESP', r.status, r.url[:140]) if '8003' in r.url and ('review' in r.url or 'solution' in r.url) else None)
    page.goto(BASE+'/assign/prospective-projects/151/manager'); page.wait_for_timeout(8000); wait_load(page)
    page.wait_for_timeout(30000)
    tab=page.get_by_text('Hồ sơ', exact=True).first
    tab.evaluate('e=>e.click()'); 
    try: page.locator('[title="Tạo báo giá"]').first.wait_for(timeout=180000)
    except Exception as e: print('no btn')
    wait_load(page); settle(page, 3000)
    page.screenshot(path='pm151_hoso.png')
