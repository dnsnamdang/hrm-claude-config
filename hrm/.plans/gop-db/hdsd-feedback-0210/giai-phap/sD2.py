from common import *
import sys
SUBMIT = len(sys.argv)>1
with user_page('hungvq.da@tanphat.com') as page:
    go(page,'/assign/solutions/%d/manager'%SID, wait=15000)
    btn(page,'Tạo hồ sơ trình duyệt giải pháp').first.click(); page.wait_for_timeout(6000); idle(page)
    m=page.locator('#solution-review-profile-modal')
    m.locator('input[placeholder="Nhập tên hồ sơ"]').fill('Hồ sơ trình duyệt giải pháp xưởng dịch vụ 3S Hyundai Bắc Ninh - V1 (lần 2)')
    fr=page.frame_locator('#solution-review-profile-modal iframe.cke_wysiwyg_frame')
    fr.locator('body').click(); page.keyboard.type('Trình duyệt phương án bố trí thiết bị khoang sửa chữa chung và bản vẽ móng cầu nâng cho xưởng 3S Hyundai Bắc Ninh.')
    m.locator('input[placeholder="Chọn hạn duyệt"]').click(); page.wait_for_timeout(1000)
    page.locator('.mx-datepicker-main:visible td.cell:not(.not-current-month)', has_text='15').first.click(); page.wait_for_timeout(1000)
    page.mouse.move(5,5); page.wait_for_timeout(1500)
    snap(page,'08_tao_ho_so')
    f=m.locator('footer, .modal-footer').first
    icon(page, f.locator('button', has_text='Lưu & Trình duyệt'), 'btn_luu_trinh_duyet')
    icon(page, f.locator('button', has_text='Lưu').filter(has_not_text='Trình'), 'btn_luu')
    icon(page, f.locator('button', has_text='Đóng'), 'btn_dong')
    if SUBMIT:
        tr=m.locator('tr', has=page.locator('input[placeholder^="Nhập tên tài liệu"]')).first
        tr.locator('button').last.click(); page.wait_for_timeout(1500)
        page.screenshot(path=EX+'before_submit.png')
        f.locator('button', has_text='Lưu & Trình duyệt').click(); m.wait_for(state='hidden', timeout=240000); page.wait_for_timeout(3000)
        page.screenshot(path=EX+'after_submit.png')
