import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
with browser_page() as page:
    page.goto(BASE + '/assign/handover/7', wait_until='domcontentloaded')
    page.wait_for_selector('text=Thông tin bàn giao', timeout=90000); page.wait_for_timeout(3500)
    btns = page.locator('.footer .group-select-btn').first.locator(':scope > *')
    n = btns.count()
    for i in range(n):
        print(i, repr(btns.nth(i).inner_text()), btns.nth(i).evaluate('e=>e.tagName+"."+e.className'))
    bd = btns.nth(0); bk = btns.nth(1)
    clip(page, bd, S + 'icon_duyet.png'); clip(page, bk, S + 'icon_khongduyet.png')
    bd.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '07b-duyet-xacnhan.png')
    page.locator('.modal.show .close').first.click(); page.wait_for_timeout(1200)
    bk.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '08-khongduyet.png')
    page.locator('.modal.show .close').first.click(); page.wait_for_timeout(1000)
    page.goto(BASE + '/assign/handover/add?id=6', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách cần bàn giao', timeout=120000); page.wait_for_timeout(4000)
    page.screenshot(path=S + '09-sua.png')
