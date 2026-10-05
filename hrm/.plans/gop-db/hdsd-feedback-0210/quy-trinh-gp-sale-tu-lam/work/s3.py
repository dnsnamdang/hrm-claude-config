from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/prospective-projects'); page.wait_for_timeout(12000)
    sb=page.locator('aside, .left-side-menu, #sidebar-menu').first
    menu(page, page.get_by_text('CSKH TRƯỚC BÁN').first, IC+'menu_cskh.png')
    menu(page, page.locator('a:has-text("Dự án TKT")').first, IC+'menu_duantkt.png')
    menu(page, page.locator('a:has-text("Yêu cầu giải pháp")').first, IC+'menu_ycgp.png')
    inp=page.get_by_placeholder('Tìm theo tên dự án, mã KH, tên KH')
    tight(page, inp, IC+'o_timnhanh.png')
    inp.fill('Ô tô Thành An'); page.locator('button.v2-btn--primary:has-text("Tìm kiếm")').click(); page.wait_for_timeout(6000)
    tight(page, page.locator('button.v2-btn--primary:has-text("Tìm kiếm")'), IC+'btn_timkiem.png')
    tight(page, page.get_by_role('button', name='Tạo mới').first, IC+'btn_taomoi.png')
    row=page.locator('tbody tr').first
    acts=row.locator('.v2-row-actions')
    acts.scroll_into_view_if_needed(); page.wait_for_timeout(500)
    print(acts.inner_html()[:2000])
    settle(page)
    page.screenshot(path=SH+'01_list_raw.png')
