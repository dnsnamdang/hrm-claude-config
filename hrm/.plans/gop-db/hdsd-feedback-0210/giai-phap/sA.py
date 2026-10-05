from common import *
with browser_page() as page:
    go(page,'/assign/solutions')
    inp=page.locator('input[placeholder^="Tìm theo mã giải pháp"]').first
    inp.fill('DA090_GP01'); inp.press('Enter'); page.wait_for_timeout(8000)
    snap(page,'x_list_row')
    # menu icons
    menu_icon(page, page.locator('text=CÔNG VIỆC'), 'menu_cong_viec')
    menu_icon(page, page.locator('text=Làm giải pháp'), 'menu_lam_giai_phap')
    page.locator('text=Làm giải pháp').first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=EX+'menu_open.png')
    page.screenshot(path=EX+'menu_open.png')
    it=page.get_by_text('Quản lý giải pháp', exact=True).first
    bb=it.bounding_box(); page.screenshot(path=IC+'menu_quan_ly_giai_phap.png', clip={'x':bb['x']-30,'y':bb['y']-8,'width':bb['width']+40,'height':bb['height']+16})
    page.keyboard.press('Escape'); page.mouse.click(900,800); page.wait_for_timeout(1000)
    row=page.locator('tr', has_text='DA090_GP01').first
    icon(page, row.locator('span[title="Giao cho Leader"] a'), 'btn_giao_leader_row')
    icon(page, row.locator('span[title="Quản lý giải pháp"] a'), 'btn_quan_ly_row')
    icon(page, row.locator('span[title="Sửa"] a'), 'btn_sua_row')
    # approve page
    go(page,'/assign/solutions/%d/edit?mode=approve'%SID)
    snap(page,'05_pm_duyet')
    icon(page, btn(page,'Giao cho Leader'), 'btn_giao_leader')
    icon(page, btn(page,'Quay lại'), 'btn_quay_lai')
    page.locator('text=Quản lý hạng mục').first.click(); page.wait_for_timeout(2500)
    snap(page,'x_pm_duyet_hm')
    icon(page, page.locator('text=Quản lý hạng mục').first, 'tab_quan_ly_hang_muc', pad=4)
