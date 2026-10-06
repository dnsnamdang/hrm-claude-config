from common import *
with browser_page() as page:
    go(page,'/assign/request-solution',30000)
    cut_side(page,'CSKH TRƯỚC BÁN','menu_cskh.png')
    cut_side(page,'Yêu cầu giải pháp','menu_ycgp.png')
    cut_side(page,'Dự án TKT','menu_duantkt.png')
    cut(page, page.get_by_role('button', name='Tạo mới').first, 'btn_taomoi.png')
    page.get_by_role('button', name='Tạo mới').first.click(); page.wait_for_timeout(35000)
    form=page.locator('.request-solution-form')
    s2(page, form, 0, 'PLC khí nén')
    page.wait_for_timeout(15000)
    page.get_by_placeholder('VD: Yêu cầu làm giải pháp dây chuyền gara...').fill('Yêu cầu làm giải pháp bàn thực hành cơ điện tử – PLC khí nén Trường CĐ Công nghiệp Hà Nội')
    page.screenshot(path='explore/c2_a.png', full_page=True)
