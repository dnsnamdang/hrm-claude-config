from common import *
with browser_page(1440, 1000) as page:
    page.goto(BASE+'/assign/meeting/create', wait_until='domcontentloaded'); page.wait_for_timeout(12000)
    page.locator('label', has_text='Họp nội bộ').first.click(); page.wait_for_timeout(2500)
    print('after', page.evaluate("()=>[...[...document.querySelectorAll('fieldset')].find(f=>f.textContent.includes('Loại meeting')).querySelectorAll('option')].map(o=>o.textContent)"))
    fs(page,'Loại meeting').locator('.select2-selection').first.click(); page.wait_for_timeout(1500)
    print(page.evaluate("()=>[...document.querySelectorAll('.select2-results__option')].map(x=>x.textContent)"))
    page.keyboard.press('Escape'); page.wait_for_timeout(500)
    fs(page,'Loại meeting').locator('.select2-selection').first.click(); page.wait_for_timeout(1500)
    print(page.evaluate("()=>[...document.querySelectorAll('.select2-results__option')].map(x=>x.textContent)"))
