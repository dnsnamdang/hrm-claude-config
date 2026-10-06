from common import *
with browser_page() as page:
    go(page,'/assign/request-solution/pending')
    page.screenshot(path=S+'h02_pending.png')
    cut_side(page,'Phê duyệt','menu_pheduyet.png')
    cut(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), 'btn_timkiemnangcao.png')
    cut(page, page.get_by_role('button', name='Cài đặt bộ lọc'), 'btn_caidatboloc.png')
    # header phân hệ
    cut_side(page,'CÔNG VIỆC','menu_congviec.png')
    # row action icons
    row=page.locator('tbody tr').first
    acts=row.locator('td').last
    acts.screenshot(path=I+'_row_actions_pending.png')
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(3000); page.mouse.move(5,5)
    page.screenshot(path=S+'h03_filter.png')
    side(page,'Phê duyệt').click(); page.wait_for_timeout(2500); page.mouse.move(900,700)
    page.screenshot(path=S+'h01_menu.png')
    cut(page, page.get_by_text('Giải pháp - Dự án',exact=True).first, 'item_giaiphap_duan.png')
    cut(page, page.get_by_text('Yêu cầu làm giải pháp',exact=True).first, 'item_yclgp.png')
