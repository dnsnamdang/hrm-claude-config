import sys
sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
OUT='explore/'
with browser_page() as page:
    page.goto(BASE+'/assign/request-solution/pending', wait_until='domcontentloaded'); page.wait_for_timeout(10000)
    # click Phê duyệt in sidebar
    page.get_by_text('Phê duyệt', exact=True).first.click(); page.wait_for_timeout(2500); page.mouse.move(700,850)
    page.screenshot(path=OUT+'menu_pheduyet.png')
    # app switcher
    page.keyboard.press('Escape'); page.wait_for_timeout(500)
    page.locator('header, .navbar-custom, #page-topbar').first.screenshot(path=OUT+'topbar.png')
    page.goto(BASE+'/assign/request-solution/add', wait_until='domcontentloaded'); page.wait_for_timeout(25000); page.mouse.move(5,5)
    page.screenshot(path=OUT+'add.png')
    page.goto(BASE+'/assign/request-solution/25', wait_until='domcontentloaded'); page.wait_for_timeout(25000); page.mouse.move(5,5)
    page.screenshot(path=OUT+'detail25.png', full_page=True)
