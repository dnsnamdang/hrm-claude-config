from _mgr import *
from PIL import Image
def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)
def goto_list(page):
    page.goto(BASE + '/assign/prospective-projects', wait_until='domcontentloaded')
    page.wait_for_selector('text=CTV_NV.2026.DAC001', timeout=240000); page.wait_for_timeout(2500)
def scroll(page, x):
    page.evaluate("x => document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = x)", x); page.wait_for_timeout(700)
def T(f):
    try: f()
    except Exception as e: print('FAIL', f.__name__ if hasattr(f,'__name__') else '', e)
with browser_page() as page:
    goto_list(page)
    # tree expand
    def tree():
        row = page.locator('tr', has_text='CTV_NV.2026.DAC001').first
        row.locator('button.group-toggle-btn').click(); page.wait_for_timeout(4000)
        row.scroll_into_view_if_needed(); page.wait_for_timeout(500)
        page.screenshot(path=S + '01d-cay-cha-con.png')
        clip(page, row.locator('button.group-toggle-btn'), S + 'icon_morong.png')
        child = page.locator('tr', has_text='CTV_NV.UD.0101.2026.DA004').first
        scroll(page, 9000)
        page.screenshot(path=S + '10-tao-giai-phap-icon.png')
        clip(page, child.locator('[title="Tạo giải pháp"]').first, S + 'icon_taogp.png')
        r150 = page.locator('tr', has_text='HN_DA.UD.0137.2026.DA091').first
        clip(page, r150.locator('[title="Tạo yêu cầu làm giải pháp"]').first, S + 'icon_taoycgp.png')
        clip(page, r150.locator('[title="Sửa"]').first, S + 'icon_sua.png')
    T(tree)
    def delete():
        scroll(page, 9000)
        r = page.locator('tr', has_text='Nâng cấp thiết bị khoang bảo dưỡng nhanh').first
        r.scroll_into_view_if_needed()
        clip(page, r.locator('[title="Xóa"]').first, S + 'icon_xoa.png')
        r.locator('[title="Xóa"]').first.click(); page.wait_for_timeout(1500)
        page.screenshot(path=S + '09-xoa.png')
        page.get_by_role('button', name='Hủy').last.click(); page.wait_for_timeout(800)
    T(delete)
    # edit draft
    def edit_draft():
        page.goto(BASE + '/assign/prospective-projects/160/edit', wait_until='domcontentloaded')
        page.wait_for_selector('text=Thông tin khách hàng', timeout=240000); page.wait_for_timeout(6000)
        page.set_viewport_size({'width': 1440, 'height': 1480}); page.wait_for_timeout(1000)
        page.screenshot(path=S + '08-sua-nhap.png')
        page.goto(BASE + '/assign/prospective-projects/158/edit', wait_until='domcontentloaded')
        page.wait_for_selector('text=Thông tin khách hàng', timeout=240000); page.wait_for_timeout(7000)
        page.screenshot(path=S + '08b-sua-chinh-thuc.png')
        clip(page, page.get_by_role('button', name='Lưu', exact=True), S + 'icon_luu.png')
        page.set_viewport_size({'width': 1440, 'height': 900}); page.wait_for_timeout(800)
    T(edit_draft)
    # detail 151: tab icons, footer, modals
    def det151():
        open_mgr(page, 151)
        for lb, k in [('Dự án','tab_duan'),('Yêu cầu','tab_yeucau'),('Giải pháp','tab_giaiphap'),('Nhiệm vụ','tab_nhiemvu'),('Vấn đề giải pháp','tab_vande'),('Meetings','tab_meetings'),('Files','tab_files'),('Hồ sơ','tab_hoso'),('Báo giá','tab_baogia'),('Gia hạn','tab_giahan'),('Thu thập thông tin','tab_thuthap')]:
            T(lambda: clip(page, page.locator('.tab-nav-align').get_by_text(lb, exact=True).first, S + 'icon_%s.png' % k, pad=6))
        for lb, fn_ in [('Nhiệm vụ','m151-03.png'),('Meetings','m151-05.png'),('Files','m151-06.png')]:
            tab(page, lb, 2000)
            try: page.wait_for_function("!document.querySelector('.tp-tab-shell').innerText.includes('Đang tải dữ liệu')", timeout=120000)
            except Exception as e: print('wait', lb, e)
            page.wait_for_timeout(1500); page.screenshot(path=S + fn_)
        tab(page, 'Dự án', 1500)
        clip(page, page.get_by_role('button', name='Sửa').last, S + 'icon_ft_sua.png')
        clip(page, page.get_by_role('button', name='Gia hạn').last, S + 'icon_ft_giahan.png')
        clip(page, page.get_by_role('button', name='Đóng dự án').last, S + 'icon_ft_dong.png')
        page.get_by_role('button', name='Gia hạn').last.click(); page.wait_for_timeout(2000)
        page.screenshot(path=S + '30-gia-han.png')
        page.get_by_role('button', name='Gửi đề xuất').click(); page.wait_for_timeout(1000)
        page.screenshot(path=S + '30b-gia-han-loi.png')
        page.get_by_role('button', name='Đóng', exact=True).last.click(); page.wait_for_timeout(1000)
        page.get_by_role('button', name='Đóng dự án').last.click(); page.wait_for_timeout(2500)
        page.screenshot(path=S + '31-dong-du-an.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(1000)
        tab(page, 'Giải pháp'); page.get_by_text('Yêu cầu điều chỉnh GP').first.click(); page.wait_for_timeout(3000)
        page.screenshot(path=S + '14-yc-dieu-chinh.png')
        b = page.get_by_role('button', name='Tạo yêu cầu')
        clip(page, b.first, S + 'icon_taoyc.png')
        clip(page, page.get_by_text('Yêu cầu điều chỉnh GP').first, S + 'icon_subtab_dc.png', pad=5)
        b.first.click(); page.wait_for_timeout(2000)
        page.screenshot(path=S + '14b-tao-yc-dieu-chinh.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(800)
        tab(page, 'Báo giá')
        T(lambda: clip(page, page.get_by_role('button', name='Tạo báo giá').first, S + 'icon_taobg.png'))
    T(det151)
    def det150():
        open_mgr(page, 150)
        clip(page, page.get_by_role('button', name='Chốt giải pháp').last, S + 'icon_ft_chotgp.png')
        page.get_by_role('button', name='Chốt giải pháp').last.click(); page.wait_for_timeout(3500)
        page.screenshot(path=S + '29-chot-gp.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(800)
        tab(page, 'Hồ sơ'); page.screenshot(path=S + 'm150-hoso.png')
    T(det150)
    def det153():
        open_mgr(page, 153); tab(page, 'Thu thập thông tin', 6000)
        page.screenshot(path=S + '26-thu-thap.png')
        clip(page, page.get_by_role('button', name='Lịch sử thay đổi').first, S + 'icon_lsphieu.png')
        clip(page, page.get_by_role('button', name='Lưu phiếu').first, S + 'icon_luuphieu.png')
        clip(page, page.get_by_role('button', name='Xem mẫu in').first, S + 'icon_xemmauin.png')
        page.get_by_role('button', name='Lịch sử thay đổi').first.click(); page.wait_for_timeout(3000)
        page.screenshot(path=S + '27-ls-phieu.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(1000)
        page.get_by_role('button', name='Xem mẫu in').first.click(); page.wait_for_timeout(3000)
        page.screenshot(path=S + '28-mau-in.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(800)
    T(det153)
    def det158():
        open_mgr(page, 158); tab(page, 'Gia hạn'); page.screenshot(path=S + '25-tab-gia-han.png')
        page.screenshot(path=S + 'm158-tkt.png')
    T(det158)
    def det157():
        open_mgr(page, 157); tab(page, 'Dự án con')
        clip(page, page.get_by_role('button', name='Thêm dự án con').first, S + 'icon_themdac.png')
        clip(page, page.locator('.tab-nav-align').get_by_text('Dự án con', exact=True).first, S + 'icon_tab_duancon.png', pad=6)
        clip(page, page.locator('.tab-nav-align').get_by_text('Thông tin chung', exact=True).first, S + 'icon_tab_ttchung.png', pad=6)
        tab(page, 'Báo giá')
        T(lambda: clip(page, page.get_by_role('button', name='Tạo báo giá tổng').first, S + 'icon_taobgtong.png'))
        page.screenshot(path=S + '23-bg-cha.png', full_page=True)
    T(det157)
    print('done6')
