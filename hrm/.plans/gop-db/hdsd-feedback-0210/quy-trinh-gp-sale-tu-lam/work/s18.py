from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/prospective-projects/153/manager'); page.wait_for_timeout(8000); wait_load(page); page.wait_for_timeout(12000)
    page.get_by_text('Thu thập thông tin', exact=True).last.evaluate('e=>e.click()'); page.wait_for_timeout(8000); wait_load(page); settle(page)
    page.screenshot(path='form154.png')
    b=page.locator('button:has-text("Lưu phiếu")')
    print(b.count())
    if b.count(): tight(page, b.first, IC+'btn_luuphieu.png')
