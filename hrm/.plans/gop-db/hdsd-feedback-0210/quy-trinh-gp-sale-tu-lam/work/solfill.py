from common import *
def opts(page):
    return page.locator('.select2-container--open .select2-results__option')
def pick(page, box, text=None, idx=0, search=None):
    for k in range(6):
        box.scroll_into_view_if_needed(); box.click(); page.wait_for_timeout(1000)
        o=opts(page)
        t=o.all_inner_texts()
        if t and not (len(t)==1 and ('Không có' in t[0] or 'Searching' in t[0] or 'Đang' in t[0])): break
        page.keyboard.press('Escape'); page.wait_for_timeout(2500)
    print('  opts:', [x for x in o.all_inner_texts() if (text or '') in x][:8], len(o.all_inner_texts()))
    (o.filter(has_text=text).first if text else o.nth(idx)).click(); page.wait_for_timeout(800)
def fill_solution(page):
    page.locator('input[placeholder="VD: GP dây chuyền sơn xưởng ô tô tiêu chuẩn"]').fill('Giải pháp cầu nâng 2 trụ và khí nén cho xưởng dịch vụ Ô tô Thành An')
    dp=page.locator('input[placeholder="Chọn ngày..."]').first
    dp.click(); dp.fill('20/10/2026'); page.keyboard.press('Enter'); page.wait_for_timeout(500)
    page.mouse.click(700,160); page.wait_for_timeout(300)
    lab=lambda t: page.locator('label:has-text("%s")'%t).first.locator('xpath=following::span[contains(@class,"select2-selection")][1]')
    pick(page, lab('Nhóm ngành'), 'Thiết bị kiểm định')
    pick(page, lab('Nhóm giải pháp'), 'Gara ô tô tổng hợp')
    page.locator('textarea[placeholder="Nhập mô tả chi tiết giải pháp"]').fill('Cung cấp, lắp đặt 2 cầu nâng 2 trụ 4 tấn và hệ thống khí nén cho khoang sửa chữa nhanh; NVKD tự làm giải pháp.')
    for i,(dept,mem,role,desc) in enumerate([('PHÒNG THIẾT BỊ Ô TÔ 3',None,'Kỹ sư thiết kế cơ khí','Khảo sát, lập cấu hình thiết bị'),('PHÒNG THIẾT BỊ Ô TÔ 2',None,'Mua hàng','Hỏi giá thiết bị, lập BOM')]):
        page.locator('button:has-text("Thêm nhân sự")').click(); page.wait_for_timeout(800)
        row=page.locator('.staff-wide tbody tr').nth(i)
        sels=row.locator('span.select2-selection')
        pick(page, sels.nth(0), dept, 0)
        pick(page, sels.nth(1), mem, 0)
        pick(page, sels.nth(2), role, i)
        row.locator('input[placeholder^="VD: thiết kế layout"]').fill(desc)
        d=row.locator('input').last
        d.click(); d.fill('05/10/2026'); page.keyboard.press('Enter'); page.wait_for_timeout(400)
        page.mouse.click(700,160); page.wait_for_timeout(300)
