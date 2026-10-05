import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
with browser_page() as page:
    page.goto(BASE + '/assign/prospective-projects/150/manager', wait_until='domcontentloaded')
    page.wait_for_timeout(12000)
    clip(page, page.locator('.left-side-menu .cats-list a.cat', has_text='Dự án TKT').first, S + 'icon_duan.png')
    tab = page.get_by_text('Hồ sơ', exact=True).first
    clip(page, tab.locator('xpath=..'), S + 'icon_tab_hoso.png')
    tab.click(); page.wait_for_selector('.profile-code-link', timeout=120000); page.wait_for_timeout(3000)
    page.screenshot(path=S + '11a-hoso.png')
    btn = page.locator('.row-actions button').filter(has=page.locator('i.ri-price-tag-3-line')).first
    clip(page, btn, S + 'icon_ycxdg.png')
    btn.click(); page.wait_for_selector('#pricing-request-form-modal .bom-banner', timeout=60000); page.wait_for_timeout(2500)
    page.screenshot(path=S + '11-tao.png')
    page.locator('#pricing-request-form-modal').get_by_role('button', name='Lưu và gửi').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '11b-tao-loi.png')
