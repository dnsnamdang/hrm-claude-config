from common import *
import re as _re, sys
SAVE = len(sys.argv)>1
with browser_page(1440, 1000) as page:
    page.on('response', lambda r: print('RESP', r.status, r.url, r.text()[:300]) if r.request.method=='POST' and 'assign/meeting/52' in r.url else None)
    load(page,'/assign/meeting/52/edit',5000)
    page.locator('button, a, div', has_text=_re.compile(r'^\s*Biên bản\s*$')).last.click(); page.wait_for_timeout(1500)
    for t,f in [('Thêm dòng','btn_themdong'),('Thêm tài liệu','btn_themtailieu')]:
        tight(page, btn(page,t), I+f+'.png')
    btn(page,'Thêm dòng').click(); page.wait_for_timeout(800)
    page.locator('textarea[placeholder="Nội dung trao đổi..."]').first.fill('Phân bổ chỉ tiêu doanh số quý IV cho 3 phòng kinh doanh')
    page.locator('textarea[placeholder="Phương án xử lý..."]').first.fill('Mỗi phòng lập kế hoạch chi tiết theo tuần, gửi Ban giám đốc duyệt')
    pf = page.locator('text=Chọn người thực hiện').first
    tight(page, pf, I+'o_nguoithuchien.png')
    pf.click(); page.wait_for_timeout(5000)
    m = page.locator('.modal.show')
    m.locator('input[placeholder="Tìm theo tên, mã nhân viên"]').fill('Nguyễn Văn Bình')
    btn(m,'Tìm kiếm').click(); page.wait_for_timeout(4000)
    m.locator('tbody tr', has_text='Nguyễn Văn Bình').first.locator('input[type=checkbox]').check(force=True); page.wait_for_timeout(1000)
    tight(page, btn(m,'Thêm thành viên (1)'), I+'btn_themthanhvien1.png')
    btn(m,'Thêm thành viên (1)').click(); page.wait_for_timeout(1500)
    row = page.locator('textarea[placeholder="Nội dung trao đổi..."]').first.locator('xpath=ancestor::div[contains(@class,"row")][1]')
    di = row.locator('input.mx-input').first
    di.click(); di.fill('15/10/2026'); page.keyboard.press('Enter'); page.mouse.click(700,20); page.wait_for_timeout(500)
    btn(page,'Thêm tài liệu').click(); page.wait_for_timeout(800)
    page.locator('input[placeholder="Nhập tên tài liệu..."]').last.fill('Kế hoạch kinh doanh quý IV/2026')
    tight(page, page.locator('label.upload-btn').last, I+'btn_chontep.png')
    page.locator('input[type=file][accept*=docx]').last.set_input_files(W+'Ke_hoach_kinh_doanh_Q4_2026.docx'); page.wait_for_timeout(2500)
    fr = page.locator('.cke_wysiwyg_frame:visible').last.content_frame
    fr.locator('body').click(); page.keyboard.type('Thống nhất chỉ tiêu doanh số quý IV/2026 cho 3 phòng kinh doanh. Các phòng gửi kế hoạch chi tiết trước ngày 15/10/2026.')
    page.wait_for_timeout(800); page.locator('.sec-title', has_text='Các nội dung khác').first.scroll_into_view_if_needed()
    page.evaluate("window.scrollTo(0,0)"); settle(page,800)
    page.screenshot(path=S+'08_report.png', full_page=False)
    page.set_viewport_size({'width':1440,'height':1700}); page.wait_for_timeout(1500); page.evaluate("window.scrollTo(0,0)"); settle(page,800)
    page.screenshot(path=S+'08_report_tall.png')
    tight(page, page.locator('.v2-btn', has_text='Excel').first.locator('xpath=..').locator('.v2-btn').first, I+'btn_in_bienban.png')
    tight(page, btn(page.locator('.footer'),'Hoàn thành'), I+'btn_hoanthanh.png')
    if SAVE:
        btn(page.locator('.footer'),'Lưu').click(); wait_list(page)
        load(page,'/assign/meeting/52/edit',5000)
        page.screenshot(path=S+'09_complete.png')
        btn(page.locator('.footer'),'Hoàn thành').click(); wait_list(page)
