from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/prospective-projects'); page.wait_for_timeout(10000)
    r=page.locator('tbody tr').first
    page.locator('input[placeholder="Tìm theo tên dự án, mã KH, tên KH"]').fill('Ô tô Thành An')
    page.locator('button.v2-btn--primary:has-text("Tìm kiếm")').click(); page.wait_for_timeout(6000)
    tight(page, page.locator('tbody tr').first.locator('span[title="Sửa"] a'), IC+'btn_sua_row.png')
    tight(page, page.locator('tbody tr').first.locator('span[title="Tạo giải pháp"] a'), IC+'btn_taogp_row.png')
    page.goto(BASE+'/assign/prospective-projects/add'); page.wait_for_timeout(10000)
    lab=page.locator('label:has-text("Cách triển khai dự án")').first
    box=lab.locator('xpath=following::span[contains(@class,"select2-selection")][1]')
    box.click(); page.wait_for_timeout(800)
    page.locator('.select2-results__option:has-text("Tự triển khai")').first.click(); page.wait_for_timeout(800)
    page.locator('input[placeholder="Nhập tên dự án tiền khả thi"]').fill('Cung cấp và lắp đặt cầu nâng 2 trụ cho xưởng dịch vụ Ô tô Thành An')
    tight(page, box, IC+'o_cachtrienkhai.png')
    g=page.locator('.solution-section').first
    tight(page, g, SH+'02_solution_section.png', pad=4)
    page.evaluate('window.scrollTo(0, 330)'); settle(page)
    page.screenshot(path=SH+'02_add.png')
    tight(page, page.locator('button:has-text("Lưu nháp")').first, IC+'btn_luunhap.png')
    tight(page, page.locator('button.v2-btn--primary:has-text("Lưu")').last, IC+'btn_luu.png')
    tight(page, page.locator('button:has-text("Quay lại")').first, IC+'btn_quaylai.png')
