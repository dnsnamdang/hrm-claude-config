from common import *
with browser_page() as page:
    go(page,'/assign/solutions/953/manager')
    icon(page, page.locator('.tab-label', has_text='Hồ sơ').first.locator('xpath=..'), 'tab_hoso')
    tab(page,'Hồ sơ')
    shot(page,'33_gp_hoso_tab_hm_pending')
    row=page.locator('tr', has_text='HM01.001').first
    b=row.locator('[title="Duyệt"]').first
    icon(page,b,'btn_duyet_row')
    icon(page,row.locator('[title="Xem"]').first,'btn_xem_row')
    b.click(); idle(page)
    m=page.locator('.modal.show').last
    shot(page,'34_hm_duyet_popup')
    icon(page, btn(m,'Duyệt'), 'btn_duyet')
    icon(page, btn(m,'Từ chối'), 'btn_tu_choi')
    btn(m,'Từ chối').click(); page.wait_for_timeout(2500)
    r=page.locator('.modal.show').last
    r.locator('textarea').fill('Thiếu bộ van điện từ 5/2 cho bài thực hành điện – khí nén, đề nghị bổ sung vào BOM.')
    shot(page,'35_hm_tu_choi')
    icon(page, btn(r,'Đồng ý'), 'btn_dong_y')
    icon(page, btn(r,'Không'), 'btn_khong')
    btn(r,'Đồng ý').click(); idle(page)
    page.screenshot(path='x_after_reject.png')
