from common import *
with browser_page() as page:
    go(page,'/assign/bom-list/24'); wait_name(page)
    shot(page,'x24_detail')
    btn(page,'Sao chép').click(); page.wait_for_timeout(3000); wait_name(page)
    print(page.url)
    page.mouse.move(5,5); page.screenshot(path='x_copy.png', full_page=True)
