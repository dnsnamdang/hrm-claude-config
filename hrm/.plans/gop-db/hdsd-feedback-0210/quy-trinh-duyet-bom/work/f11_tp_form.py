from common import *
with browser_page() as page:
    go(page,'/assign/bom-list/add')
    page.fill('input[placeholder="VD: BOM điều khiển dây chuyền line 01"]','BOM thiết bị bàn thực hành thủy lực')
    pick(page,0,'DA091')
    pick(page,1,'HM01')
    sel=page.locator('.select2-selection').first
    sel.click(); page.wait_for_timeout(800)
    page.locator('.select2-results__option', has_text='BOM LIST thành phần').first.click(); page.wait_for_timeout(1500)
    # confirm modal maybe
    if page.locator('.modal.show').count():
        print('confirm:', page.locator('.modal.show').last.inner_text()[:200])
    page.fill('input[placeholder="BOM dùng cho giải pháp triển khai demo."]','Trang bị 10 bàn thực hành thủy lực')
    icon(page, page.locator('.select2-selection').first, 'o_loai_bom')
    th=page.get_by_role('button', name='Thêm mới').first; icon(page, th, 'btn_them_moi_hang')
    th.click(); page.wait_for_timeout(5000); idle(page)
    page.fill('input[placeholder="Tìm theo tên, mã, model hàng hoá"]','thủy lực'); page.keyboard.press('Enter'); page.wait_for_timeout(4000); idle(page)
    rows=page.locator('.modal-card tbody tr:has(input[type=checkbox])')
    for i in range(3):
        rows.nth(i).locator('input[type=checkbox]').check(); page.wait_for_timeout(300)
    shot(page,'11_popup_them_hang')
    icon(page, btn(page.locator('.modal-card'),'Thêm 3 hàng hoá'), 'btn_them_n_hang')
    icon(page, btn(page.locator('.modal-card'),'Đóng'), 'btn_dong_popup_hang')
    btn(page.locator('.modal-card'),'Thêm 3 hàng hoá').click(); page.wait_for_timeout(3000)
    btn(page.locator('.modal-card'),'Đóng').click(); page.wait_for_timeout(2500)
    shot(page,'10_tao_bom_tp')
