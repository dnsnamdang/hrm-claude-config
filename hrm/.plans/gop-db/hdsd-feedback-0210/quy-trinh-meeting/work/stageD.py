from common import *
with browser_page(1440, 1000) as page:
    load(page,'/assign/meeting/52/show',5000); page.screenshot(path=S+'06_confirm_attend.png')
    ac = page.locator('.ac-actions')
    tight(page, btn(ac,'Có mặt'), I+'btn_comat.png')
    tight(page, btn(ac,'Vắng có lý do'), I+'btn_vangcolydo.png')
    for name,f in [('Sửa','btn_sua_footer'),('In','btn_in_footer'),('Hủy','btn_huy_footer')]:
        try: tight(page, btn(page.locator('.footer'), name), I+f+'.png')
        except Exception as e: print('miss',name)
    btn(ac,'Vắng có lý do').click(); page.wait_for_timeout(1500)
    settle(page,500); page.screenshot(path=W+'d_absent_modal.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(800)
    btn(ac,'Có mặt').click(); page.wait_for_timeout(3000)
    load(page,'/assign/meeting/52/edit',5000); page.screenshot(path=S+'05_schedule_edit.png')
    tight(page, btn(page.locator('.footer'),'Lưu'), I+'btn_luu.png')
    btn(page.locator('.footer'),'Lưu và Chốt lịch').click(); page.wait_for_timeout(7000)
    print(page.url)
