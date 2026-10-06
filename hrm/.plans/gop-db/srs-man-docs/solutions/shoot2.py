from _sc import *
import sys
with browser_page() as page:
    for attempt in range(6):
        go(page, '/assign/solutions'); page.wait_for_selector('text=GP39', timeout=180000)
        page.wait_for_timeout(3000)
        page.get_by_role('button', name='Tạo mới').click(); page.wait_for_timeout(6000); idle(page)
        page.wait_for_selector('.request-solution-select', timeout=120000); page.wait_for_timeout(2000)
        page.locator('.request-solution-select .select2-selection').first.click(); page.wait_for_timeout(1500)
        opts = page.locator('.select2-container--open .select2-results__option').all_inner_texts()
        print(attempt, opts[:3], flush=True)
        if any('0913' in o for o in opts):
            page.locator('.select2-container--open .select2-results__option', has_text='0913').first.click()
            break
        page.keyboard.press('Escape')
    page.wait_for_timeout(4000); idle(page)
    page.locator('input[placeholder^="VD: GP dây chuyền"]').fill('Giải pháp khoang sơn và sấy xưởng dịch vụ Kia Hải Phòng')
    page.locator('textarea[placeholder="Nhập mô tả chi tiết giải pháp"]').fill('Bố trí 2 buồng sơn sấy liên hoàn, hệ thống cấp khí nén và xử lý khí thải đạt chuẩn môi trường.')
    page.wait_for_timeout(800)
    snap(page, '06-tao-moi.png')
    snap(page, '06-tao-moi-full.png', full=True)
    clip(page, page.get_by_role('button', name='Lưu nháp'), S + 'icon_luunhap.png')
    clip(page, page.get_by_role('button', name='Lưu và gửi'), S + 'icon_luuvagui.png')
    # tab hang muc
    page.locator('.nav-link, a, button, div', has_text=re.compile(r'^\s*Quản lý hạng mục\s*$')).last.click(); page.wait_for_timeout(1500)
    page.get_by_role('button', name='Thêm hạng mục').click(); page.wait_for_timeout(1500)
    body = page.locator('.module-body').first
    pick(page, body.locator('.module-name-inline'), 'Xây dựng danh mục thiết bị', 'danh mục')
    leader = body.locator('.col-md-3', has=page.locator('label', has_text='Leader hạng mục')).first
    pick(page, leader, 'Đào Phúc Sơn', 'Đào Phúc Sơn')
    page.wait_for_timeout(800)
    di = body.locator('input[placeholder^="Chọn ngày"]').first
    di.click(); di.fill('20/11/2026'); page.keyboard.press('Enter'); page.wait_for_timeout(800)
    page.mouse.click(700, 120); page.wait_for_timeout(600)
    snap(page, '06b-tao-moi-hang-muc.png')
    clip(page, page.get_by_role('button', name='Thêm hạng mục'), S + 'icon_themhm.png')
    # tab so do
    page.locator('.nav-link, a, button, div', has_text=re.compile(r'^\s*Sơ đồ nhân sự\s*$')).last.click(); page.wait_for_timeout(1500)
    snap(page, '06c-tao-moi-so-do.png')
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        page.get_by_role('button', name='Lưu nháp').click(); page.wait_for_timeout(6000)
        snap(page, '06d-sau-luu.png')
        print(page.url)
