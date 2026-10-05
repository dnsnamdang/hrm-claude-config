from common import *
with browser_page(1440, 1000) as page:
    load(page,'/assign/meeting/53/show',5000)
    btn(page.locator('.footer'),'Hủy').click(); page.wait_for_timeout(2500)
    m = page.locator('#cancel-meeting-modal')
    m.locator('.select2-selection').first.click(); page.wait_for_timeout(1000)
    page.locator('.select2-container--open .select2-results__option', has_text='Hủy do mình bận đột xuất').first.click(); page.wait_for_timeout(600)
    m.locator('textarea').fill('Trưởng phòng đi công tác đột xuất, sẽ lên lịch họp lại vào tuần sau.')
    settle(page,800); page.screenshot(path=S+'12_cancel.png')
    tight(page, btn(m,'Xác nhận hủy'), I+'btn_xacnhanhuy.png')
    tight(page, btn(m,'Đóng'), I+'btn_dong_modal.png')
    btn(m,'Xác nhận hủy').click(); page.wait_for_timeout(6000)
    load(page,'/assign/meeting/53/show',5000); page.screenshot(path=W+'f_cancelled.png')
    # xoá 54
    page.goto(BASE+'/assign/meeting', wait_until='domcontentloaded')
    page.wait_for_selector('tbody tr:has-text("TPE.MET.NB.26.0069")', timeout=90000); page.wait_for_timeout(3000)
    cell = page.locator('tbody tr', has_text='TPE.MET.NB.26.0069').first.locator('td').last
    cell.scroll_into_view_if_needed(); cell.locator('span[title="Xóa"] button').click(); page.wait_for_timeout(2000)
    settle(page,800); page.screenshot(path=S+'14_delete.png')
    cm = page.locator('#confirm-delete-meeting')
    tight(page, btn(cm,'Xóa'), I+'btn_confirm_xoa.png')
    tight(page, btn(cm,'Hủy'), I+'btn_huy_confirm.png')
    btn(cm,'Xóa').click(); page.wait_for_timeout(5000)
