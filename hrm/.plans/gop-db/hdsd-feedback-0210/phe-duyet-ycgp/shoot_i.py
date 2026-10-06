from common import *
with browser_page() as page:
    go(page,'/assign/prospective-projects',35000)
    loc=page.locator('[title="Tạo yêu cầu làm giải pháp"]')
    print(loc.count())
    cut(page, loc.first, 'btn_taoycgp_row.png')
