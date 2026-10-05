from common import *
with user_page('hungvq.da@tanphat.com') as page:
    go(page,'/assign/solutions/%d/manager'%SID, wait=15000)
    t=tab(page,'Nhiệm vụ')
    page.locator('tr', has_text='Khảo sát mặt bằng khoang sơn').first.wait_for(timeout=180000); page.wait_for_timeout(2000)
    snap(page,'06_nhiem_vu')
    r=page.locator('tr', has_text='Khảo sát mặt bằng khoang sơn').first
    for k,n in [('Sửa','btn_sua_task'),('Xoá','btn_xoa_task')]:
        icon(page, r.locator('button[title="%s"]'%k), n)
    t=tab(page,'Vấn đề giải pháp')
    page.locator('tr', has_text='Thiếu thông số điện').first.wait_for(timeout=180000); page.wait_for_timeout(2000)
    snap(page,'07_van_de')
    r=page.locator('tr', has_text='Thiếu thông số điện').first
    print(r.locator('button[title]').evaluate_all("els=>els.map(e=>e.title)"))
    for k,n in [('Sửa','btn_sua_issue'),('Xoá','btn_xoa_issue')]:
        if r.locator('button[title="%s"]'%k).count(): icon(page, r.locator('button[title="%s"]'%k), n)
    icon(page, btn(page,'Tạo mới'), 'btn_tao_moi')
    # review profile
    btn(page,'Tạo hồ sơ trình duyệt giải pháp').first.click(); page.wait_for_timeout(5000); idle(page)
    m=page.locator('#solution-review-profile-modal')
    m.locator('input[placeholder="Nhập tên hồ sơ"]').fill('Hồ sơ trình duyệt giải pháp xưởng dịch vụ 3S Hyundai Bắc Ninh - V1')
    ed=m.locator('[contenteditable=true]').first
    print('editable', m.locator('[contenteditable=true]').count())
    ed.click(); page.keyboard.type('Trình duyệt phương án bố trí thiết bị khoang sửa chữa chung và bản vẽ móng cầu nâng cho xưởng 3S Hyundai Bắc Ninh.')
    page.wait_for_timeout(1000)
    page.screenshot(path=EX+'review_open.png')
    print(m.inner_text()[:1500])
