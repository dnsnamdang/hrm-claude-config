"""Form Tạo meeting nhánh Họp đối tác: chọn Loại meeting có khách hàng để hiện khối KH (không lưu)."""
import sys, os
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots') + '/'
with browser_page() as page:
    page.goto(BASE + '/assign/meeting/create', wait_until='domcontentloaded')
    page.get_by_text('Thành phần — Phía Công ty').first.wait_for(timeout=90000)
    page.wait_for_timeout(8000)
    page.mouse.click(620, 357); page.wait_for_timeout(1500)
    page.screenshot(path=D + '_dbg1.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(500)
    page.get_by_text('Họp nội bộ', exact=True).first.click(); page.wait_for_timeout(800)
    page.get_by_text('Họp đối tác', exact=True).first.click(); page.wait_for_timeout(800)
    page.mouse.click(620, 357); page.wait_for_timeout(1500)
    page.screenshot(path=D + '_dbg2.png')
    opt = page.locator('.select2-results__option', has_text='Meeting với khách hàng')
    if opt.count():
        opt.first.click(); page.wait_for_timeout(2500)
        page.mouse.wheel(0, 420); page.wait_for_timeout(1200)
        page.screenshot(path=D + 'n15_create_partner.png')
        print('ok')
