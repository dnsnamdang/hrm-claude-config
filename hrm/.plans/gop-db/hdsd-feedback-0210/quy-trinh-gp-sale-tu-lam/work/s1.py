import sys; sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
with browser_page() as page:
    page.goto(BASE+'/assign/prospective-projects/add'); page.wait_for_timeout(10000)
    page.mouse.move(5,5)
    page.screenshot(path='add_full.png', full_page=True)
    page.screenshot(path='add_view.png')
