from common import *
with browser_page() as page:
    go(page,'/assign/solution-modules/954/manager')
    tab(page,'Hồ sơ')
    shot(page,'38_hm_hoso_rejected_list')
    btn(page,'Tạo hồ sơ trình duyệt').click(); page.wait_for_timeout(3000); idle(page)
    m=page.locator('.modal.show').last
    m.locator('input[placeholder="Nhập tên hồ sơ"]').fill('Hồ sơ trình duyệt BOM hạng mục Xây dựng danh mục thiết bị (lần 2)')
    ed=m.frame_locator('iframe').first.locator('body'); ed.click(); page.keyboard.type('Đã bổ sung van điện từ theo ý kiến PM, trình duyệt lại BOM tổng hợp hạng mục.')
    dp=m.locator('input[placeholder="Chọn hạn duyệt"]'); dp.click(); page.wait_for_timeout(500); page.locator('.mx-datepicker-main:visible td[title="2026-10-09"]').first.click(); page.wait_for_timeout(800)
    m.locator('h5').first.click(); page.wait_for_timeout(500)
    page.screenshot(path='x_hm2.png')
    btn(m,'Lưu & Trình duyệt').click(); page.wait_for_timeout(4000); idle(page)
    go(page,'/assign/solutions/953/manager')
    tab(page,'Hồ sơ')
    row=page.locator('tr', has_text='HM01.002').first
    row.locator('[title="Duyệt"]').first.click(); idle(page)
    m=page.locator('.modal.show').last
    shot(page,'39_hm_duyet_popup_lan2')
    btn(m,'Duyệt').click(); page.wait_for_timeout(4000); idle(page)
    page.screenshot(path='x_after_approve.png')
