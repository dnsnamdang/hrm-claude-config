import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
exec(open('shoot_common.py').read())
with browser_page() as page:
    goto_list(page)
    clip(page, page.locator('.left-side-menu a', has_text='Báo giá').first, S + 'icon_presale_baogia.png'); crop_w(S + 'icon_presale_baogia.png', 120)
    scroll_table(page, 5000)
    row = page.locator('tr', has_text='BG-2026-00094').first
    row.locator('[title="Lịch sử phê duyệt"]').first.click()
    page.locator('.log-item').first.wait_for(timeout=60000); page.wait_for_timeout(1000)
    page.screenshot(path=S + '20-lichsu-popup.png'); esc(page)
    row.locator('[title="In báo giá"]').first.click()
    page.get_by_text('Cấu hình in báo giá').first.wait_for(timeout=60000); page.wait_for_timeout(1000)
    page.screenshot(path=S + '17-in-cauhinh.png'); esc(page)
    page.goto(BASE + '/sale/dashboard', wait_until='domcontentloaded'); page.wait_for_timeout(6000)
    page.locator('.left-side-menu a', has_text='Bán hàng').nth(0).click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + 'x-sale2.png')
