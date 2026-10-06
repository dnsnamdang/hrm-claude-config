from common import *
with user_page('hungvq.da@tanphat.com') as page:
    go(page,'/assign/solutions/%d/manager'%SID, wait=15000)
    t=tab(page,'Vấn đề giải pháp')
    page.locator('tr', has_text='Cầu nâng đề xuất').first.wait_for(timeout=180000); page.wait_for_timeout(3000)
    snap(page,'07_van_de')
    r=page.locator('tr', has_text='Cầu nâng đề xuất').first
    print(r.locator('button[title]').evaluate_all("els=>els.map(e=>e.title)"))
    icon(page, r.locator('button[title="Sửa"]'), 'btn_sua_issue')
    icon(page, r.locator('button[title="Xoá"]'), 'btn_xoa_issue')
with user_page('sondp.da@tanphat.com') as page:
    go(page,'/assign/solutions/%d/manager'%SID, wait=15000)
    t=tab(page,'Vấn đề giải pháp')
    r=page.locator('tr', has_text='Thiếu thông số điện').first
    r.wait_for(timeout=180000); page.wait_for_timeout(3000)
    print(r.locator('button[title]').evaluate_all("els=>els.map(e=>e.title)"))
    icon(page, r.locator('button[title="Xử lý"]'), 'btn_xu_ly_issue')
