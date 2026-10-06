import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
def goto_list(page):
    page.goto(BASE + '/assign/bom-list', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách BOM List', timeout=90000)
    page.wait_for_function("() => !document.querySelector('.v2-data-table .spinner-border')", timeout=90000)
    page.wait_for_timeout(3000)
with browser_page() as page:
    goto_list(page)
    page.screenshot(path=S + '01-ds.png')
    row = page.locator('tr', has_text='BOM-2026-00030').first
    print(row.inner_html()[-3000:])
    print(page.locator('.switcher-item').count())
