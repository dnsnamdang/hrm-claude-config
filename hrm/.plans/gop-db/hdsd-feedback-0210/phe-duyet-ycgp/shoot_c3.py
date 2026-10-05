from common import *
TITLE='Yêu cầu làm giải pháp bàn thực hành cơ điện tử – PLC khí nén Trường CĐ Công nghiệp Hà Nội'
with browser_page() as page:
    go(page,'/assign/request-solution/add',35000)
    form=page.locator('.request-solution-form')
    s2(page, form, 0, 'PLC khí nén'); page.wait_for_timeout(15000)
    page.get_by_placeholder('VD: Yêu cầu làm giải pháp dây chuyền gara...').fill(TITLE)
    date(page, form.locator('input[placeholder="Chọn ngày..."]').nth(1), '05/11/2026')
    page.get_by_placeholder('Mô tả ngắn nội dung yêu cầu, phạm vi, tài liệu đầu vào...').fill('Thiết kế cấu hình 06 bàn thực hành cơ điện tử – PLC khí nén theo chương trình đào tạo của trường, kèm bố trí mặt bằng phòng 120 m².')
    page.mouse.move(5,5); page.evaluate('window.scrollTo(0,0)'); page.wait_for_timeout(800)
    page.screenshot(path=S+'n10_create.png')
    cut(page, page.locator('.footer').get_by_role('button', name='Lưu nháp'), 'btn_luunhap.png')
    cut(page, page.locator('.footer').get_by_role('button', name='Lưu và gửi'), 'btn_luuvagui.png')
    page.locator('.footer').get_by_role('button', name='Lưu nháp').click(); page.wait_for_timeout(20000)
    page.mouse.move(5,5); page.screenshot(path='explore/c3_after.png')
    print(page.url)
