from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/solution-modules/954/manager'); page.wait_for_timeout(12000)
    shot(page,'30_hm_manager')
    b=page.get_by_role('button', name='Tạo hồ sơ trình duyệt'); icon(page,b,'btn_tao_hstd_hm')
    b.click(); page.wait_for_timeout(5000)
    m=page.locator('.modal.show').last
    m.locator('input[placeholder="Nhập tên hồ sơ"]').fill('Hồ sơ trình duyệt BOM hạng mục Xây dựng danh mục thiết bị')
    ed=m.frame_locator('iframe').first.locator('body'); ed.click(); page.keyboard.type('Trình PM duyệt danh mục thiết bị và BOM tổng hợp hạng mục cho 10 bàn thực hành khí nén.')
    dp=m.locator('input[placeholder="Chọn hạn duyệt"]'); dp.click(); page.wait_for_timeout(500); page.locator('.mx-datepicker-main:visible td[title="2026-10-09"]').first.click(); page.wait_for_timeout(800)
    m.locator('.modal-title, h5').first.click(); page.wait_for_timeout(500)
    shot(page,'31_hm_hoso_tao')
    icon(page, m.get_by_role('button', name='Lưu & Trình duyệt'), 'btn_luu_trinh_duyet')
    icon(page, btn(m,'Lưu'), 'btn_luu_hoso')
    icon(page, btn(m,'Đóng'), 'btn_dong_hoso')
    m.get_by_role('button', name='Lưu & Trình duyệt').click(); page.wait_for_timeout(6000)
    page.screenshot(path='x_after_submit.png')
