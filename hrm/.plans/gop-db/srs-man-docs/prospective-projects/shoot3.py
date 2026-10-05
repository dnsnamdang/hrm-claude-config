import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
with browser_page() as page:
    page.goto(BASE + '/assign/prospective-projects/add', wait_until='domcontentloaded')
    page.wait_for_selector('text=Thông tin khách hàng', timeout=180000); page.wait_for_timeout(4000)
    page.screenshot(path=S + '05-tao-moi.png')
    page.screenshot(path=S + '05-tao-moi-full.png', full_page=True)
    print(page.evaluate("document.body.scrollHeight"))
