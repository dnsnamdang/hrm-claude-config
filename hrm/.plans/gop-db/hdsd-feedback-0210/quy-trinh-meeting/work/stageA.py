from common import *
with browser_page(1440, 1000) as page:
    page.goto(BASE+'/assign/meeting/create', wait_until='domcontentloaded'); page.wait_for_timeout(12000)
    page.locator('label', has_text='Họp nội bộ').first.click(); page.wait_for_timeout(2500)
    sel2(page, fs(page,'Loại meeting'), 'Meeting nội bộ')
    sel2(page, fs(page,'Hình thức'), 'Trực tiếp')
    page.fill('#name', 'Họp triển khai kế hoạch kinh doanh quý IV/2026')
    page.locator('input[placeholder="VD: Phòng 302, Trụ sở Hà Nội"]').fill('Phòng họp tầng 3, trụ sở Hà Nội')
    setdate(page, 'Bắt đầu', '05/10/2026 09:00')
    setdate(page, 'Kết thúc', '05/10/2026 10:30')
    page.screenshot(path=W+'a1.png')
    plus = page.locator('.card', has_text='Thành phần — Phía Công ty').locator('button').first
    tight(page, plus, W+'i_plus.png')
    plus.click(); page.wait_for_timeout(5000)
    page.screenshot(path=W+'a2.png')
