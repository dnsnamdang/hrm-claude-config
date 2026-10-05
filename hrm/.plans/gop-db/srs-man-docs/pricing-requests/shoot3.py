import sys, os; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from playwright.sync_api import sync_playwright
S = 'shots/'
SCROLL = "() => { document.querySelectorAll('*').forEach(x => { if (x.scrollWidth > x.clientWidth + 20 && getComputedStyle(x).overflowX.match(/auto|scroll/)) x.scrollLeft = 99999 }) }"
def goto_list(page):
    page.goto(BASE + '/assign/pricing-requests', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách yêu cầu xây dựng giá', timeout=90000)
    page.wait_for_function("() => !document.querySelector('.v2-data-table .spinner-border')", timeout=60000)
    page.wait_for_selector('a:has-text("YCBG-2026-0000")', timeout=90000)
    page.wait_for_timeout(2500)
# user 27
STATE27 = 'shots/_state27.json'
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, storage_state=STATE27)
    page = ctx.new_page()
    goto_list(page)
    page.screenshot(path=S + '07-ds-nv.png')
    page.evaluate(SCROLL); page.wait_for_timeout(2500); page.mouse.move(700,700); page.wait_for_timeout(800)
    page.screenshot(path=S + '07b-ds-nv-phai.png')
    row = page.locator('tr', has_text='YCBG-2026-00006').first
    clip(page, row.locator('a, button').filter(has=page.locator('i.ri-edit-line')).first, S + 'icon_sua.png')
    clip(page, row.locator('a, button').filter(has=page.locator('i.ri-delete-bin-line')).first, S + 'icon_xoa.png')
    row.locator('a, button').filter(has=page.locator('i.ri-delete-bin-line')).first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '09-xoa.png')
    page.get_by_role('button', name='Hủy').click(); page.wait_for_timeout(800)
    clip(page, page.locator('tr', has_text='YCBG-2026-00006').first.locator('td').last, S + '_row6_actions.png')
    page.goto(BASE + '/assign/pricing-requests/6', wait_until='domcontentloaded'); page.wait_for_selector('text=Thời gian giao hàng', timeout=60000); page.wait_for_timeout(3000)
    page.screenshot(path=S + '06c-chitiet-nhap.png')
    page.goto(BASE + '/assign/pricing-requests/6/edit', wait_until='domcontentloaded'); page.wait_for_selector('text=Thời gian giao hàng', timeout=60000); page.wait_for_timeout(3000)
    page.screenshot(path=S + '08-sua.png')
    clip(page, page.get_by_role('button', name='Lưu nháp'), S + 'icon_luunhap.png')
    clip(page, page.get_by_role('button', name='Lưu và gửi'), S + 'icon_luugui.png')
    # validation: clear warranty
    page.locator('input').nth(2).fill('')
    page.screenshot(path=S + '_dbg.png')
    b.close()
