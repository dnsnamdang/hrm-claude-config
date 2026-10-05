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
        page.wait_for_selector('text=Thông tin khách hàng', timeout=240000); page.wait_for_timeout(12000)
        page.set_viewport_size({'width': 1440, 'height': 1480}); page.wait_for_timeout(1000)
        page.screenshot(path=S + '08-sua-nhap.png')
        page.goto(BASE + '/assign/prospective-projects/158/edit', wait_until='domcontentloaded')
        page.wait_for_selector('text=Thông tin khách hàng', timeout=240000); page.wait_for_timeout(12000)
        page.screenshot(path=S + '08b-sua-chinh-thuc.png')
        clip(page, page.get_by_role('button', name='Lưu', exact=True), S + 'icon_luu.png')
        page.set_viewport_size({'width': 1440, 'height': 900}); page.wait_for_timeout(800)
    T(edit_draft)
    # detail 151: tab icons, footer, modals
    def det158():
        open_mgr(page, 158); tab(page, 'Gia hạn'); page.screenshot(path=S + '25-tab-gia-han.png')
        page.screenshot(path=S + 'm158-tkt.png')
    T(det158)
    def det157():
        open_mgr(page, 157); page.screenshot(path=S + 'm157-tkt.png'); tab(page, 'Dự án con'); page.screenshot(path=S + 'm157-01.png')
        clip(page, page.get_by_role('button', name='Thêm dự án con').first, S + 'icon_themdac.png')
        clip(page, page.locator('.tab-nav-align').get_by_text('Dự án con', exact=True).first, S + 'icon_tab_duancon.png', pad=6)
        clip(page, page.locator('.tab-nav-align').get_by_text('Thông tin chung', exact=True).first, S + 'icon_tab_ttchung.png', pad=6)
        tab(page, 'Báo giá')
        T(lambda: clip(page, page.get_by_role('button', name='Tạo báo giá tổng').first, S + 'icon_taobgtong.png'))
        page.screenshot(path=S + 'm157-02.png')
    T(det157)
    def dac():
        page.goto(BASE + '/assign/prospective-projects/add?parent_id=157', wait_until='domcontentloaded')
        page.wait_for_selector('text=Thông tin khách hàng', timeout=240000); page.wait_for_timeout(12000)
        page.set_viewport_size({'width': 1440, 'height': 1480}); page.wait_for_timeout(1500)
        page.screenshot(path=S + '24b-them-dac.png')
    T(dac)
    print('done9')
