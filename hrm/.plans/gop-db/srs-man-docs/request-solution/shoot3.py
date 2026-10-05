import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from _vm import vm_eval
S = 'shots/'
def wait_form(page):
    page.wait_for_selector('text=Thông tin yêu cầu', timeout=90000)
    page.wait_for_function("() => !document.querySelector('.nuxt-progress') || true")
    page.wait_for_timeout(9000)
with browser_page() as page:
    # 1. lỗi validate
    # 2. lối vào từ Dự án TKT
    page.goto(BASE + '/assign/prospective-projects', wait_until='domcontentloaded')
    page.wait_for_selector('table.data-table tbody tr td', timeout=180000); page.wait_for_timeout(4000)
    page.screenshot(path=S + '_tkt.png')
    row = page.locator('tr', has_text='Mazda Thái Bình').first
    row.scroll_into_view_if_needed(); page.wait_for_timeout(800)
    btn = row.locator('a[href*="request-solution/add"]')
    print('inline', btn.count())
    if btn.count():
        clip(page, btn.first, S + 'icon_taoycgp_row.png')
        page.screenshot(path=S + '08-tkt-ds.png')
    else:
        row.locator('[title="Hành động khác"]').first.click(); page.wait_for_timeout(800)
        page.screenshot(path=S + '08-tkt-ds.png')
        clip(page, page.locator('.v2-row-actions__item', has_text='Tạo yêu cầu làm giải pháp').first, S + 'icon_taoycgp_row.png')
        page.keyboard.press('Escape')
    page.goto(BASE + '/assign/prospective-projects/156', wait_until='domcontentloaded'); page.wait_for_timeout(10000)
    b = page.get_by_role('button', name='Tạo yêu cầu làm giải pháp')
    print('detail btn', b.count())
    if b.count():
        clip(page, b.first, S + 'icon_taoycgp_btn.png')
        page.screenshot(path=S + '08b-tkt-ct.png')
    # 3. tạo từ dự án 156, Lưu và gửi
    page.goto(BASE + '/assign/request-solution/add?prospective_project_id=156', wait_until='domcontentloaded'); wait_form(page)
    print(vm_eval(page, 'RequestSolutionForm', """
        vm.request.title = 'Yêu cầu làm giải pháp cầu nâng và thiết bị bảo dưỡng nhanh xưởng Mazda Thái Bình';
        vm.request.receive_dept = 51;
        vm.request.customer_need_quote_date = '2026-12-05';
        vm.request.note = 'Khách hàng cần phương án 4 khoang bảo dưỡng nhanh, ưu tiên cầu nâng cắt kéo âm nền; gửi kèm bản vẽ mặt bằng xưởng.';
        return vm.request.project_key + ' ' + vm.request.project_phase_id""", None))
    page.wait_for_timeout(2500)
    page.screenshot(path=S + '09-tao-tu-tkt.png')
    page.get_by_role('button', name='Lưu và gửi').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '09b-xac-nhan-gui.png')
    m = page.locator('.modal.show')
    clip(page, m.get_by_role('button', name='Xác nhận'), S + 'icon_xacnhan.png')
    m.get_by_role('button', name='Xác nhận').click(); page.wait_for_timeout(6000)
    print(page.url)
