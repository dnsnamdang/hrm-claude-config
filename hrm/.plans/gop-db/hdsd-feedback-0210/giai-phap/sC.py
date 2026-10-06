from common import *
with user_page('hungvq.da@tanphat.com') as page:
    go(page,'/assign/solutions/%d/manager'%SID, wait=15000)
    t=tab(page,'Nhân sự'); icon(page,t,'tab_nhan_su',pad=3)
    btn(page,'Thêm nhân sự').first.click(); page.wait_for_timeout(3000)
    m=page.locator('#add-member-modal')
    sel2(page,m,'Hạng mục','Xây dựng danh mục')
    sel2(page,m,'Thành viên','Trần Văn Sơn')
    sel2(page,m,'Vai trò dự án','Mua hàng')
    m.locator('textarea').fill('Báo giá và đặt hàng thiết bị khoang sửa chữa chung')
    page.wait_for_timeout(800)
    snap(page,'03_them_nhan_su')
    icon(page, m.locator('.modal-footer button', has_text='Thêm nhân sự'), 'btn_them_nhan_su_modal')
    icon(page, m.locator('.modal-footer button', has_text='Huỷ'), 'btn_huy_modal')
    m.locator('.modal-footer button', has_text='Huỷ').click(); page.wait_for_timeout(1500)
    # Tasks
    t=tab(page,'Nhiệm vụ'); icon(page,t,'tab_nhiem_vu',pad=3); page.wait_for_timeout(3000)
    snap(page,'06_nhiem_vu')
    icon(page, btn(page,'Tạo mới'), 'btn_tao_moi')
    row=page.locator('tr', has_text='Lập danh mục thiết bị').first
    print('TASKROW', row.locator('td').last.inner_html()[:1500])
    t=tab(page,'Vấn đề giải pháp'); icon(page,t,'tab_van_de',pad=3); page.wait_for_timeout(3000)
    snap(page,'07_van_de')
    row=page.locator('tr', has_text='Thiếu thông số điện').first
    print('ISSUEROW', row.locator('td').last.inner_html()[:1500])
    t=tab(page,'Tiến độ'); icon(page,t,'tab_tien_do',pad=3); page.wait_for_timeout(3000)
    ins=page.locator('input.weight-input')
    print('weights', ins.count())
    if ins.count()>=2:
        ins.nth(0).fill('60'); ins.nth(0).dispatch_event('input'); ins.nth(1).fill('40'); ins.nth(1).dispatch_event('input'); page.wait_for_timeout(4000)
    snap(page,'11_tien_do')
