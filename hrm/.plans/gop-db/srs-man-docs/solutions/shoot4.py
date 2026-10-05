from _sc import *
def tab(page, label):
    idle(page, 1000)
    t = page.locator('.surface-hd').get_by_text(label, exact=True).first
    t.click(timeout=240000); page.wait_for_timeout(4000); idle(page)
    return t
with browser_page() as page:
    go(page, '/assign/solutions'); page.wait_for_selector('text=GP40', timeout=180000); page.wait_for_timeout(2000)
    page.evaluate("x => document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = x)", 6000); page.wait_for_timeout(800)
    page.locator('tr', has_text='DA090_GP01').first.locator('span[title="Quản lý giải pháp"] a').first.click()
    page.wait_for_selector('.surface-hd', timeout=240000); page.wait_for_timeout(5000); idle(page, 5000)
    snap(page, '11-quan-ly-tong-quan.png')
    snap(page, '11-quan-ly-tong-quan-full.png', full=True)
    # tab icons
    for lab, nm in [('Tổng quan','tongquan'),('Thông tin','thongtin'),('Hồ sơ','hoso'),('Nhân sự','nhansu'),('Nhiệm vụ','nhiemvu'),('Vấn đề giải pháp','vande'),('Meeting','meeting'),('Tiến độ','tiendo'),('Files','files'),('YC Điều chỉnh','ycdc')]:
        try: clip(page, page.locator('.surface-hd').get_by_text(lab, exact=True).first, S + 'icon_tab_%s.png' % nm)
        except Exception as e: print('tab icon fail', lab, e)
    # alert modal
    try:
        page.get_by_text('Nhiệm vụ sắp tới hạn').first.click(); page.wait_for_timeout(4000); idle(page)
        snap(page, '12-canh-bao.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(1500)
    except Exception as e: print('alert fail', e)
    tab(page, 'Thông tin'); snap(page, '13-tab-thong-tin.png')
    tab(page, 'Meeting'); snap(page, '24-tab-meeting.png')
    tab(page, 'Files'); snap(page, '26-tab-files.png')
    tab(page, 'YC Điều chỉnh'); snap(page, '27-tab-ycdc.png')
    tab(page, 'Nhân sự'); snap(page, '15-tab-nhan-su.png')
    clip(page, page.locator('button', has_text=re.compile(r'^\s*Phân công\s*$')).first, S + 'icon_phancong.png')
    clip(page, page.get_by_role('button', name='Xem lịch sử phân công'), S + 'icon_lsphancong.png')
    clip(page, page.get_by_role('button', name='Thêm nhân sự'), S + 'icon_themnhansu.png')
    page.get_by_role('button', name='Xem lịch sử phân công').click(); page.wait_for_timeout(3000); idle(page)
    snap(page, '18-lich-su-phan-cong.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1500)
    btn = page.locator('button[title="Sửa phân công"], [title="Sửa phân công"]').first
    try:
        clip(page, btn, S + 'icon_suapc.png')
        clip(page, page.locator('[title="Khóa thành viên"]').first, S + 'icon_khoatv.png')
        clip(page, page.locator('[title="Xóa khỏi giải pháp"]').first, S + 'icon_xoatv.png')
        btn.click(); page.wait_for_timeout(2500)
        snap(page, '19-sua-phan-cong.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(1500)
        page.locator('[title="Khóa thành viên"]').first.click(); page.wait_for_timeout(2000)
        snap(page, '20-khoa-thanh-vien.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(1500)
    except Exception as e: print('member fail', e)
