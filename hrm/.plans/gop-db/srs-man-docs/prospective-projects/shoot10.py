from _mgr import *
def T(f):
    try: f()
    except Exception as e: print('FAIL', f.__name__, str(e)[:200])
with browser_page() as page:
    def lst():
        page.goto(BASE + '/assign/prospective-projects', wait_until='domcontentloaded')
        page.wait_for_selector('text=CTV_NV.2026.DAC001', timeout=240000); page.wait_for_timeout(2500)
        page.evaluate("document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = 9000)"); page.wait_for_timeout(800)
        r = page.locator('tr', has_text='HN_DA.UD.0137.2026.DA091').first
        r.scroll_into_view_if_needed(); page.wait_for_timeout(600)
        clip(page, r.locator('[title="Tạo yêu cầu làm giải pháp"]').first, S + 'icon_taoycgp.png')
        clip(page, r.locator('[title="Sửa"]').first, S + 'icon_sua.png')
    T(lst)
    def add():
        page.goto(BASE + '/assign/prospective-projects/add', wait_until='domcontentloaded')
        page.wait_for_selector('text=Thông tin khách hàng', timeout=240000); page.wait_for_timeout(3000)
        b = page.locator('button').filter(has_text='Lưu').filter(has_not_text='nháp').last
        clip(page, b, S + 'icon_luu.png')
        clip(page, page.locator('button').filter(has_text='Lưu nháp').last, S + 'icon_luunhap.png')
    T(add)
    def det151():
        open_mgr(page, 151)
        page.get_by_role('button', name='Đóng dự án').last.click(); page.wait_for_timeout(3000)
        page.screenshot(path=S + '31-dong-du-an.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(1500)
        tab(page, 'Giải pháp'); page.locator('.tp-tab-shell').get_by_text('Yêu cầu điều chỉnh GP').first.click(); page.wait_for_timeout(4000)
        page.screenshot(path=S + '14-yc-dieu-chinh.png')
        clip(page, page.locator('.tp-tab-shell').get_by_text('Yêu cầu điều chỉnh GP').first, S + 'icon_subtab_dc.png', pad=5)
        b = page.locator('.tp-tab-shell button').filter(has_text='Tạo yêu cầu').first
        clip(page, b, S + 'icon_taoyc.png')
        b.click(); page.wait_for_timeout(2500)
        page.screenshot(path=S + '14b-tao-yc-dieu-chinh.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(1000)
        tab(page, 'Báo giá')
        clip(page, page.locator('.tp-tab-shell button').filter(has_text='Tạo báo giá').first, S + 'icon_taobg.png')
    T(det151)
    print('done10')
