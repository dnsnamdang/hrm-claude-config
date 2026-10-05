from common import *
with browser_page() as page:
    go(page,'/assign/solutions/953/manager')
    shot(page,'42_gp_manager')
    b=btn(page,'Tạo hồ sơ trình duyệt giải pháp'); icon(page,b,'btn_tao_hstd_gp'); b.click(); page.wait_for_timeout(3000); idle(page)
    m=page.locator('.modal.show').last
    m.locator('input[placeholder="Nhập tên hồ sơ"]').fill('Hồ sơ trình duyệt giải pháp thực hành khí nén – thủy lực')
    ed=m.frame_locator('iframe').first.locator('body'); ed.click(); page.keyboard.type('Trình duyệt giải pháp và BOM tổng hợp cấp giải pháp để chuyển phòng kinh doanh lập báo giá.')
    dp=m.locator('input[placeholder="Chọn hạn duyệt"]'); dp.click(); page.wait_for_timeout(500); page.locator('.mx-datepicker-main:visible td[title="2026-10-12"]').first.click(); page.wait_for_timeout(800)
    m.locator('h5').first.click(); page.wait_for_timeout(500)
    shot(page,'43_gp_hoso_tao')
    btn(m,'Lưu & Trình duyệt').click(); page.wait_for_timeout(4000); idle(page)
    page.screenshot(path='x_gp_after_submit.png')
