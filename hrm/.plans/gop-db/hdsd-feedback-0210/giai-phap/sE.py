from common import *
import sys
ACTION=sys.argv[1]  # reject | approve
with browser_page() as page:
    go(page,'/assign/solutions/%d/manager'%SID, wait=15000)
    t=tab(page,'Hồ sơ'); icon(page,t,'tab_ho_so',pad=3)
    r=page.locator('tr', has=page.locator('button[title="Duyệt"]')).first
    r.wait_for(timeout=180000); page.wait_for_timeout(2000)
    snap(page,'x_tab_ho_so')
    icon(page, r.locator('button[title="Duyệt"]'), 'btn_duyet_row')
    r.locator('button[title="Duyệt"]').click(); page.wait_for_timeout(6000); idle(page)
    m=page.locator('#solution-review-profile-modal')
    snap(page,'09_tp_duyet')
    f=m.locator('.modal-footer').first
    icon(page, f.locator('button', has_text='Duyệt'), 'btn_duyet')
    icon(page, f.locator('button', has_text='Từ chối'), 'btn_tu_choi')
    if ACTION=='reject':
        f.locator('button', has_text='Từ chối').click(); page.wait_for_timeout(2000)
        rm=page.locator('#modal-reject-review-profile')
        rm.locator('textarea').fill('Bổ sung bản vẽ bố trí cấp khí nén cho khoang sửa chữa chung trước khi trình lại.')
        page.wait_for_timeout(800); snap(page,'x_tu_choi')
        icon(page, rm.locator('.modal-footer button', has_text='Đồng ý'), 'btn_dong_y')
        icon(page, rm.locator('.modal-footer button', has_text='Không'), 'btn_khong')
        rm.locator('.modal-footer button', has_text='Đồng ý').click()
    else:
        f.locator('button', has_text='Duyệt').first.click()
    for i in range(60):
        page.wait_for_timeout(4000)
        if not m.is_visible(): print('closed'); break
