from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/bom-list/add'); page.wait_for_timeout(10000)
    pick(page,0,'DA091')
    page.get_by_role('button', name='Thêm mới').first.click(); page.wait_for_timeout(15000)
    page.fill('input[placeholder="Tìm theo tên, mã, model hàng hoá"]','xi lanh'); page.keyboard.press('Enter'); page.wait_for_timeout(8000)
    page.screenshot(path='x_pop2.png')
