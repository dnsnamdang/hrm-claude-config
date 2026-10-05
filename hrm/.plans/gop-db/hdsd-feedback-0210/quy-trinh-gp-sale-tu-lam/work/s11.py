from common import *
import subprocess
def openmgr(page):
    page.goto(BASE+'/assign/solutions/956/manager'); page.wait_for_timeout(8000); wait_load(page)
with browser_page() as page:
    subprocess.run(['mysql','-uroot','local_hrm_erp','-e','update bom_lists set status=2 where id=25'])
    openmgr(page)
    wait_load(page); page.locator('button:has-text("Tạo hồ sơ trình duyệt giải pháp")').evaluate('e=>e.click()'); page.wait_for_timeout(6000)
    m=page.locator('#solution-review-profile-modal')
    m.locator('input[placeholder="Nhập tên hồ sơ"]').fill('Hồ sơ giải pháp cầu nâng 2 trụ - Ô tô Thành An')
    m.locator('iframe.cke_wysiwyg_frame').first.wait_for(timeout=30000)
    m.frame_locator('iframe.cke_wysiwyg_frame').first.locator('body').click(); page.keyboard.type('Trình phương án cung cấp 02 cầu nâng 2 trụ 4 tấn và hệ thống khí nén theo BOM tổng hợp đính kèm.'); page.wait_for_timeout(800)
    m.locator('input[placeholder="Nhập tên hồ sơ"]').click(); settle(page)
    page.screenshot(path=SH+'07_hoso.png')
    tight(page, m.locator('button:has-text("Lưu & Duyệt")'), IC+'btn_luuduyet.png')
    tight(page, m.locator('footer button:has-text("Lưu")').filter(has_not_text='Duyệt').first, IC+'btn_luu_hoso.png')
    tight(page, m.locator('button:has-text("Đóng")').last, IC+'btn_dong_hoso.png')
    resp=[]
    page.on('response', lambda r: resp.append((r.status, r.url, r.text()[:500])) if 'review-profiles' in r.url and r.request.method=='POST' else None)
    m.locator('button:has-text("Lưu & Duyệt")').evaluate('e=>e.click()'); page.wait_for_timeout(10000)
    for x in resp: print(x)
    settle(page); page.screenshot(path='after_duyet.png')
