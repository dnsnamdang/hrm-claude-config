from common import *
def side_icon(page, loc, name, pad=12):
    bb=loc.bounding_box()
    x=max(0,bb['x']-pad); w=min(218-x, bb['width']+2*pad)
    page.screenshot(path=IC+name+'.png', clip={'x':x,'y':bb['y']-pad,'width':w,'height':bb['height']+2*pad})
with browser_page() as page:
    go(page,'/assign/bom-list')
    shot(page,'01_bom_list')
    icon(page, btn(page,'Tạo mới'), 'btn_tao_moi_bom')
    # menu
    side_icon(page, page.locator('text=CÔNG VIỆC').first, 'menu_phanhe', pad=8)
    li=page.locator('text=Làm giải pháp').first
    side_icon(page, li, 'menu_lam_giai_phap', pad=10)
    li.click(); page.wait_for_timeout(2000)
    for t,n in [('BOM Giải pháp','item_bom_gp'),('Quản lý giải pháp','item_quan_ly_gp'),('Hạng mục giải pháp','item_hang_muc_gp')]:
        icon(page, page.locator('text='+t).last, n)
    page.keyboard.press('Escape')
    go(page,'/assign/solutions')
    shot(page,'02_solution_list')
    row=page.locator('tr', has_text='DA091_GP01').first
    icon(page, row.locator('[title="Quản lý giải pháp"]').first, 'btn_quan_ly_gp_row')
    go(page,'/assign/solution-modules')
    shot(page,'03_module_list')
    icon(page, page.locator('a', has_text='DA091_GP01_HM01').first, 'link_ma_hang_muc')
    go(page,'/assign/bom-list/27'); wait_name(page)
    shot(page,'50_bom_da_duyet')
    page.screenshot(path=SH+'50_bom_da_duyet_full.png', full_page=True)
