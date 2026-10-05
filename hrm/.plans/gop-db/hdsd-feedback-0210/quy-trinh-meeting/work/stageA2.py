from common import *
import re
def fill_base(page, name='Họp triển khai kế hoạch kinh doanh quý IV/2026', d1='05/10/2026 09:00', d2='05/10/2026 10:30'):
    page.goto(BASE+'/assign/meeting/create', wait_until='domcontentloaded'); page.wait_for_timeout(4000)
    page.wait_for_function("()=>{const f=[...document.querySelectorAll('fieldset')].find(f=>f.textContent.includes('Loại meeting')); return f && f.querySelectorAll('option').length>=1}", timeout=120000)
    page.wait_for_timeout(3000)
    page.locator('label', has_text='Họp nội bộ').first.click(); page.wait_for_timeout(2500)
    sel2(page, fs(page,'Loại meeting'), 'Meeting nội bộ')
    sel2(page, fs(page,'Hình thức'), 'Trực tiếp')
    page.fill('#name', name)
    page.locator('input[placeholder="VD: Phòng 302, Trụ sở Hà Nội"]').fill('Phòng họp tầng 3, trụ sở Hà Nội')
    setdate(page, 'Bắt đầu', d1)
    setdate(page, 'Kết thúc', d2)
if __name__ == '__main__':
  with browser_page(1440, 1000) as page:
    fill_base(page)
    plus = page.locator('xpath=//div[contains(@class,"sec-title") and contains(.,"Phía Công ty")]/following-sibling::*[1]').first
    print(plus.evaluate("e=>e.outerHTML"))
    tight(page, plus, W+'i_plus.png')
    plus.click(); page.wait_for_timeout(6000)
    settle(page); page.screenshot(path=W+'a2.png')
