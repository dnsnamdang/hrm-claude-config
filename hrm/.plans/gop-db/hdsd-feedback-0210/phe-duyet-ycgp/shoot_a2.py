from common import *
with browser_page() as page:
    go(page,'/assign/request-solution/pending',30000)
    page.screenshot(path=S+'h02_pending.png')
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(3000); page.mouse.move(5,5)
    page.screenshot(path=S+'h03_filter.png')
    row=page.locator('tbody tr').filter(has_text='TPE.YCP.TC.26.0912').first
    acts=row.locator('td').last
    cut(page, acts.locator('[title="Tiếp nhận"]').first, 'btn_tiepnhan_row.png')
    cut(page, acts.locator('[title="Yêu cầu bổ sung thông tin"]').first, 'btn_ycbs_row.png')
    page.evaluate('window.scrollTo(0,0)')
    side(page,'Phê duyệt').click(); page.wait_for_timeout(2500); page.mouse.move(900,700)
    page.screenshot(path=S+'h01_menu.png')
    cut(page, page.get_by_text('Giải pháp - Dự án',exact=True).first.locator('xpath=..'), 'item_giaiphap_duan.png')
    cut(page, page.get_by_text('Yêu cầu làm giải pháp',exact=True).first.locator('xpath=..'), 'item_yclgp.png')
