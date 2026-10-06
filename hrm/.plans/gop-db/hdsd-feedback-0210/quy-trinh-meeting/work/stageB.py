from common import *
from stageA2 import fill_base
def pick(page, kw):
    m = page.locator('.modal.show')
    inp = m.locator('input[placeholder="Tìm theo tên, mã nhân viên"]')
    inp.fill(kw); btn(m, 'Tìm kiếm').click(); page.wait_for_timeout(3500)
    row = m.locator('tbody tr', has_text=kw).first
    row.locator('input[type=checkbox]').check(force=True); page.wait_for_timeout(1200)
with browser_page(1440, 1000) as page:
    # list + icons
    page.goto(BASE+'/assign/meeting', wait_until='domcontentloaded'); page.wait_for_timeout(12000); settle(page)
    page.screenshot(path=S+'01_list.png')
    tight(page, btn(page, 'Tạo mới'), I+'btn_taomoi.png')
    tight(page, page.locator('a', has_text='Tổng hợp meeting').first, I+'menu_tonghop_raw.png')
    fill_base(page)
    plus = page.locator('xpath=//div[contains(@class,"sec-title") and contains(.,"Phía Công ty")]/following-sibling::*[1]').first
    tight(page, plus, I+'btn_plus_congty.png')
    plus.click(); page.wait_for_timeout(6000)
    pick(page, 'Nguyễn Văn Bình')
    pick(page, 'Ngô Thị Hằng')
    settle(page); page.screenshot(path=S+'03_pick_staff.png')
    m = page.locator('.modal.show')
    tight(page, btn(m, 'Tìm kiếm'), I+'btn_timkiem_popup.png')
    tight(page, btn(m, 'Đóng'), I+'btn_dong_popup.png')
    btn(m, 'Đóng').click(); page.wait_for_timeout(2000)
    settle(page); page.screenshot(path=S+'02_create.png')
    for name, f in [('Lưu nháp','btn_luunhap'),('Lưu và Lên lịch','btn_luulenlich'),('Lưu và Chốt lịch','btn_luuchotlich'),('Quay lại','btn_quaylai')]:
        tight(page, btn(page.locator('.footer'), name), I+f+'.png')
    btn(page.locator('.footer'), 'Lưu nháp').click(); page.wait_for_timeout(6000)
    print(page.url)
    settle(page); page.screenshot(path=W+'after_draft.png')
