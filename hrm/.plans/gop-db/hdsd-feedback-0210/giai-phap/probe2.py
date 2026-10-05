from common import *
with user_page('hungvq.da@tanphat.com') as page:
    page.on('response', lambda r: print('RESP', r.status, r.url[-80:]) if 'review-profiles' in r.url or r.status>=400 else None)
    page.on('console', lambda m: print('CONSOLE', m.type, m.text[:200]) if m.type=='error' else None)
    go(page,'/assign/solutions/%d/manager'%SID, wait=15000)
    btn(page,'Tạo hồ sơ trình duyệt giải pháp').first.click(); page.wait_for_timeout(6000); idle(page)
    m=page.locator('#solution-review-profile-modal')
    m.locator('input[placeholder="Nhập tên hồ sơ"]').fill('Hồ sơ trình duyệt giải pháp xưởng dịch vụ 3S Hyundai Bắc Ninh - V1')
    fr=page.frame_locator('#solution-review-profile-modal iframe.cke_wysiwyg_frame')
    fr.locator('body').click(); page.keyboard.type('Trình duyệt phương án bố trí thiết bị khoang sửa chữa chung và bản vẽ móng cầu nâng.')
    m.locator('input[placeholder="Chọn hạn duyệt"]').click(); page.wait_for_timeout(1000)
    page.locator('.mx-datepicker-main:visible td.cell:not(.not-current-month)', has_text='15').first.click(); page.wait_for_timeout(1000)
    tr=m.locator('tr', has=page.locator('input[placeholder^="Nhập tên tài liệu"]')).first
    tr.locator('button').last.click(); page.wait_for_timeout(1500)
    f=m.locator('footer, .modal-footer').first
    f.locator('button', has_text='Lưu & Trình duyệt').click()
    for i in range(30):
        page.wait_for_timeout(4000)
        if not m.is_visible(): print('closed', i); break
    page.screenshot(path=EX+'probe2.png')
    print(page.locator('.toasted').all_inner_texts())
