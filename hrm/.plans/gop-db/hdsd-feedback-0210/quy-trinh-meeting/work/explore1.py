import sys; sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
W='/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/hdsd-feedback-0210/quy-trinh-meeting/work/'
with browser_page() as page:
    page.goto(BASE+'/assign/meeting', wait_until='domcontentloaded'); page.wait_for_timeout(12000)
    page.mouse.move(5,5); page.screenshot(path=W+'x_list.png')
    page.goto(BASE+'/assign/meeting/create', wait_until='domcontentloaded'); page.wait_for_timeout(12000)
    page.mouse.move(5,5); page.screenshot(path=W+'x_create.png', full_page=True)
