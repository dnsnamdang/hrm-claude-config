from common import *
import re as _re
with browser_page() as page:
    go(page,'/assign/solutions/%d/manager'%SID, wait=15000)
    t=tab(page,'Nhân sự')
    icon(page, btn(page,'Phân công'), 'btn_phan_cong')
    icon(page, btn(page,'Xem lịch sử phân công'), 'btn_ls_phan_cong')
    icon(page, btn(page,'Thêm nhân sự'), 'btn_them_nhan_su')
    btn(page,'Phân công').first.click(); page.wait_for_timeout(4000); idle(page)
    m=page.locator('#assign-manager-modal')
    m.get_by_text('Phân công PM', exact=True).click(); page.wait_for_timeout(1500)
    sel2(page,m,'Vai trò mới','Kỹ sư thiết kế cơ khí'); page.wait_for_timeout(1000)
    g=m.locator('.form-group', has=page.locator('label', has_text=_re.compile('^\\s*Hạng mục cho PM cũ'))).first
    g.locator('.select2-selection').first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=EX+'hm_pm_cu.png')
    print(page.locator('.select2-container--open .select2-results__option').all_inner_texts())
    page.locator('.select2-container--open .select2-results__option').first.click(); page.wait_for_timeout(800)
    g=m.locator('.form-group', has=page.locator('label', has_text=_re.compile('^\\s*PM mới'))).first
    g.locator('.select2-selection').first.click(); page.wait_for_timeout(1500)
    print(page.locator('.select2-container--open .select2-results__option').all_inner_texts())
    page.locator('.select2-container--open .select2-results__option', has_text='Trần Văn Sơn').first.click(); page.wait_for_timeout(800)
    m.locator('textarea').fill('Chuyển PM sang anh Trần Văn Sơn do anh Vũ Quang Hưng được điều động sang dự án khác từ tháng 10/2026.')
    page.wait_for_timeout(1000); snap(page,'04_doi_pm')
    icon(page, m.locator('.modal-footer button', has_text='Xác nhận phân công'), 'btn_xac_nhan_phan_cong')
    icon(page, m.locator('.modal-footer button', has_text='Đóng'), 'btn_dong_pc')
