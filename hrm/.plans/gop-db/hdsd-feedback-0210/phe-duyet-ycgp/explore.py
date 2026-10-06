import sys
sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
OUT='explore/'
with browser_page() as page:
    for name,url in [('list','/assign/request-solution'),('pending','/assign/request-solution/pending'),('add','/assign/request-solution/add'),('detail25','/assign/request-solution/25'),('edit25','/assign/request-solution/25/edit')]:
        page.goto(BASE+url, wait_until='domcontentloaded'); page.wait_for_timeout(10000); page.mouse.move(5,5)
        page.screenshot(path=OUT+name+'.png')
        print(name, page.url)
