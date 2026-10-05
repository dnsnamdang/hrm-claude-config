from common import *
with browser_page() as page:
    go(page,'/assign/prospective-projects/150/manager',35000)
    page.get_by_text('Thu thập thông tin', exact=True).first.click(); page.wait_for_timeout(10000); page.mouse.move(5,5)
    page.screenshot(path='explore/c0_phieu.png', full_page=True)
