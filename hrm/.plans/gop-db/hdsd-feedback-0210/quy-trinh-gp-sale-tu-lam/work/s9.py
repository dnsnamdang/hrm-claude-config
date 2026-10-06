from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/solutions'); page.wait_for_timeout(14000)
    menu(page, page.get_by_text('CÔNG VIỆC').first, IC+'menu_congviec.png')
    menu(page, page.locator('a:has-text("Làm giải pháp")').first, IC+'menu_lamgp.png')
    page.screenshot(path='sollist.png')
    page.goto(BASE+'/assign/solutions/956/manager'); page.wait_for_timeout(15000); settle(page)
    page.screenshot(path='solmgr.png')
