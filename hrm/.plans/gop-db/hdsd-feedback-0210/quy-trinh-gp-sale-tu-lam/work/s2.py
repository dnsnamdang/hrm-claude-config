import sys; sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
with browser_page() as page:
    page.goto(BASE+'/assign/prospective-projects'); page.wait_for_timeout(12000)
    page.mouse.move(5,5)
    page.screenshot(path='list.png')
    page.goto(BASE+'/assign/prospective-projects/151/manager'); page.wait_for_timeout(12000)
    page.mouse.move(5,5)
    page.screenshot(path='pm151.png')
