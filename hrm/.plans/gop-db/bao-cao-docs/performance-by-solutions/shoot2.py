import sys, os
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots') + '/'
with browser_page() as page:
    page.goto(BASE + '/assign/report/performance-by-solutions', wait_until='domcontentloaded', timeout=60000)
    page.get_by_text('Vui lòng bấm Tìm kiếm để xem báo cáo.').first.wait_for(timeout=60000)
    page.wait_for_timeout(3000)
    page.get_by_role('button', name='Tìm kiếm nâng cao').first.click(); page.wait_for_timeout(2000)
    page.locator('.smart-advanced-filters .select2-selection').nth(3).click(); page.wait_for_timeout(1000)
    page.locator('.select2-results__option', has_text='CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT').first.click()
    page.wait_for_timeout(800); page.locator('.smart-filter-actions button').nth(0).click()
    page.locator('tr.row-dept').first.wait_for(timeout=90000); page.wait_for_timeout(1500)
    page.get_by_role('button', name='Ẩn tìm kiếm nâng cao').first.click(); page.wait_for_timeout(800)
    page.locator('.button-menu-mobile').first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=D + '02-xem-bao-cao.png')
    page.evaluate("() => { const w = document.querySelector('.table-wrapper'); w.scrollLeft = 3000 }")
    page.wait_for_timeout(600)
    page.screenshot(path=D + '02b-xem-bao-cao-phai.png')
