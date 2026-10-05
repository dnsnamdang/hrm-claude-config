from common import *
import re as _re
CODE='TPE.MET.NB.26.0067'
def pick(page, kw):
    m = page.locator('.modal.show')
    m.locator('input[placeholder="Tìm theo tên, mã nhân viên"]').fill(kw)
    btn(m, 'Tìm kiếm').click(); page.wait_for_timeout(3500)
    m.locator('tbody tr', has_text=kw).first.locator('input[type=checkbox]').check(force=True); page.wait_for_timeout(1200)
with browser_page(1440, 1000) as page:
    page.goto(BASE+'/assign/meeting', wait_until='domcontentloaded'); page.wait_for_timeout(12000)
    row = page.locator('tbody tr', has_text=CODE).first
    cell = row.locator('td').last
    cell.scroll_into_view_if_needed(); settle(page, 800)
    tight(page, cell.locator('span[title="Sửa"] a'), I+'btn_sua_row.png')
    tight(page, cell.locator('span[title="Xóa"] button'), I+'btn_xoa_row.png')
    tight(page, cell.locator('button[title="Hành động khác"]'), I+'btn_bacham_row.png')
    cell.locator('button[title="Hành động khác"]').click(); page.wait_for_timeout(1200)
    page.screenshot(path=W+'menu_open.png')
    for t,f in [('In biên bản','item_inbienban'),('Lịch sử','item_lichsu')]:
        it = page.locator('.dropdown-menu.show, .v2-row-actions__menu, [role=menu]').locator(':scope *', has_text=_re.compile('^\\s*'+t+'\\s*$')).last
        try:
            tight(page, it, I+f+'.png')
        except Exception as e: print('miss', t, e)
    page.keyboard.press('Escape'); page.mouse.click(700,20); page.wait_for_timeout(500)
    cell.locator('span[title="Sửa"] a').click(); page.wait_for_timeout(12000)
    print(page.url)
    plus = page.locator('xpath=//div[contains(@class,"sec-title") and contains(.,"Phía Công ty")]/following-sibling::*[1]').first
    plus.click(); page.wait_for_timeout(6000)
    pick(page, 'Nguyễn Văn Bình'); pick(page, 'Ngô Thị Hằng')
    m = page.locator('.modal.show')
    tight(page, btn(m, 'Thêm thành viên (2)'), I+'btn_themthanhvien.png')
    btn(m, 'Thêm thành viên (2)').click(); page.wait_for_timeout(2000)
    page.locator('.cke_wysiwyg_frame').first.content_frame.locator('body').fill('Triển khai chỉ tiêu doanh số quý IV/2026 cho từng phòng kinh doanh; thống nhất kế hoạch chăm sóc khách hàng trọng điểm.')
    settle(page); page.screenshot(path=S+'04_edit.png')
    btn(page.locator('.footer'), 'Lưu và Lên lịch').click(); page.wait_for_timeout(7000)
    print(page.url); page.screenshot(path=W+'after_schedule.png')
