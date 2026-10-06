from common import *
with user_page('hungvq.da@tanphat.com') as page:
    go(page,'/assign/solutions/%d/manager'%SID, wait=15000)
    icon(page, btn(page,'Tạo version'), 'btn_tao_version')
    btn(page,'Tạo version').first.click(); page.wait_for_timeout(3000)
    m=page.locator('.modal.show').last
    m.locator('textarea, input[placeholder^="Mô tả phiên bản"]').first.fill('Điều chỉnh bố trí khoang sơn theo góp ý của khách hàng')
    m.locator('input[placeholder="Chọn ngày kết thúc"]').click(); page.wait_for_timeout(1000)
    page.locator('.mx-datepicker-main:visible td.cell:not(.not-current-month)', has_text='30').first.click(); page.wait_for_timeout(1000)
    page.mouse.move(5,5); snap(page,'10_tao_version')
    icon(page, m.locator('button', has_text='Tạo mới'), 'btn_tao_moi_version')
    icon(page, m.locator('button', has_text='Đóng'), 'btn_dong_version')
    m.locator('button', has_text='Tạo mới').click()
    for i in range(60):
        page.wait_for_timeout(4000)
        if not m.is_visible(): print('closed'); break
