from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/prospective-projects/154/manager'); page.wait_for_timeout(8000); wait_load(page); page.wait_for_timeout(15000)
    tab=page.locator('main, .tp-card, .content-page').get_by_text('Báo giá', exact=True).last
    for i in range(page.get_by_text('Báo giá', exact=True).count()):
        e=page.get_by_text('Báo giá', exact=True).nth(i); bb=e.bounding_box()
        if bb and bb['x']>230 and bb['y']<130: tab=e
    tight(page, tab.locator('xpath=ancestor-or-self::*[self::button or self::a or self::li][1]'), IC+'tab_baogia_duan.png')
    tab.evaluate('e=>e.click()'); page.wait_for_timeout(8000); wait_load(page)
    try: page.locator('button:has-text("Tạo báo giá")').first.wait_for(timeout=120000)
    except Exception: print('no tao bao gia')
    settle(page, 3000); page.screenshot(path=SH+'11_khonggp_baogia.png')
    tight(page, page.locator('button:has-text("Tạo báo giá")').first, IC+'btn_taobaogia.png')
