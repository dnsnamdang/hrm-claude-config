from common import *
with browser_page() as page:
    go(page,'/assign/bom-list')
    page.locator('text=Làm giải pháp').first.click(); page.wait_for_timeout(2000)
    page.mouse.move(700,500); page.wait_for_timeout(500)
    page.screenshot(path='x_menu.png')
    print(page.locator('aside, .left-side-menu, #sidebar-menu').first.inner_text()[:800])
