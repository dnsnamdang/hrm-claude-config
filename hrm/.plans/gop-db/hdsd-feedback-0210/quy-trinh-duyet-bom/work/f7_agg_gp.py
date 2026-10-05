from common import *
with browser_page() as page:
    go(page,'/assign/bom-list/add')
    page.fill('input[placeholder="VD: BOM điều khiển dây chuyền line 01"]','BOM tổng hợp giải pháp thực hành khí nén – thủy lực')
    pick(page,0,'DA091')
    page.fill('input[placeholder="BOM dùng cho giải pháp triển khai demo."]','Gộp BOM các hạng mục đã duyệt để trình duyệt giải pháp')
    b=btn(page,'Chọn BL con'); icon(page,b,'btn_chon_bl_con'); b.click(); page.wait_for_timeout(3000)
    page.locator('.modal-card tr', has_text='BOM-2026-00026').locator('input[type=checkbox]').check()
    shot(page,'40_chon_bl_con_gp')
    g=btn(page.locator('.modal-card'),'Gộp BOM con'); icon(page,g,'btn_gop_bom_con'); g.click(); page.wait_for_timeout(6000); idle(page)
    shot(page,'41_bom_tong_hop_gp_form')
    btn(page,'Lưu BOM').click(); page.wait_for_timeout(5000); idle(page)
    print(page.url)
