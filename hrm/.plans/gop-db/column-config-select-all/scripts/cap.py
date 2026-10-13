import sys,os
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__))
ROUTES=sys.argv[1:]
BASE='http://127.0.0.1:3002'
with sync_playwright() as p:
    br=p.chromium.launch(headless=True)
    page=br.new_page(viewport={'width':1440,'height':900})
    page.goto(BASE+'/login',wait_until='domcontentloaded'); page.wait_for_timeout(3000)
    page.fill('#emailaddress','namdangit@gmail.com'); page.fill('input[type=password]','2025Dns@2')
    page.get_by_role('button',name='Đăng nhập').click(); page.wait_for_timeout(5000)
    for r in ROUTES:
        out=S+'/shots/'+r.replace('/','__')+'.png'
        try:
            page.goto(BASE+'/'+r,wait_until='domcontentloaded'); page.wait_for_timeout(9000)
            btn=page.locator('button:has(.ri-layout-column-line), a:has(.ri-layout-column-line), span:has(> .ri-layout-column-line)').first
            btn.click(); page.wait_for_selector('#column-customization-modal .column-row',state='visible',timeout=15000)
            page.wait_for_timeout(1800); page.mouse.move(5,5); page.wait_for_timeout(400)
            page.screenshot(path=out); print('OK',r)
            page.keyboard.press('Escape'); page.wait_for_timeout(600)
        except Exception as e:
            print('FAIL',r,str(e)[:200])
    br.close()
