import sys, os
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots') + '/'
with browser_page() as page:
    page.goto(BASE + '/assign/prospective-projects'); page.wait_for_timeout(7000)
    page.screenshot(path=S + '01-danh-sach.png')
    print(page.url)
