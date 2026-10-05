from common import *
import time
with browser_page() as page:
    go(page,'/assign/bom-list/24/edit')
    for i in range(40):
        page.wait_for_timeout(3000)
        v=page.locator('input[placeholder="VD: BOM điều khiển dây chuyền line 01"]')
        txt = v.input_value() if v.count() else None
        print(i, page.url, txt)
        if '/edit' not in page.url or txt: break
    page.wait_for_timeout(3000)
    page.screenshot(path='x_bom24_edit.png')
