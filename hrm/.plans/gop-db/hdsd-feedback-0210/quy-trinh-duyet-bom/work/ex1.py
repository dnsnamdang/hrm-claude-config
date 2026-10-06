import sys; sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
with browser_page() as page:
    page.goto(BASE+'/assign/bom-list/add'); page.wait_for_timeout(10000)
    page.mouse.move(5,5)
    page.screenshot(path='x_add.png', full_page=True)
    print(page.inner_text('body')[:3000])
