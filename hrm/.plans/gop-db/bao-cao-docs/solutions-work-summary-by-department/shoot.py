# -*- coding: utf-8 -*-
"""Chụp ảnh cho SRS Báo cáo tổng hợp giải pháp theo phòng ban (client :3002, headless)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from _shoot import browser_page, clip, BASE
from PIL import Image
S = os.path.join(HERE, 'shots') + '/'
URL = BASE + '/assign/report/solutions-work-summary-by-department'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"

def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)

def wait_ready(page, t=60000):
    page.wait_for_function("() => { try { const vm = %s; return vm && vm.hasSearched && !vm.loading } catch(e) { return false } }" % VM, timeout=t)
    page.wait_for_timeout(800)

def set_year(page):
    page.evaluate("async () => { const vm = %s; vm.$set(vm.filters,'time_mode','year'); vm.$set(vm.filters,'year',2026); vm.onTimeModeChange(); await vm.handleSearch(); }" % VM)
    wait_ready(page)

with browser_page() as page:
    page.set_default_timeout(60000)
    page.goto(URL, wait_until='domcontentloaded')
    wait_ready(page, 90000)
    # icons menu
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='CSKH trước bán').first, S + 'icon_phanhe.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 700); page.wait_for_timeout(800)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Báo cáo').first
    clip(page, rail, S + 'icon_baocao.png'); crop_w(S + 'icon_baocao.png', 110)
    rail.click(); page.wait_for_timeout(1500)
    grp = page.get_by_text('Báo cáo dự án tiền khả thi', exact=False).first
    clip(page, grp.locator('xpath=ancestor-or-self::*[self::a or self::button or self::div][1]'), S + 'icon_nhom.png')
    item = page.get_by_text('Báo cáo tổng hợp giải pháp theo phòng ban', exact=True).last
    clip(page, item.locator('xpath=..'), S + 'icon_man.png')
    page.keyboard.press('Escape'); page.mouse.click(1380, 90); page.wait_for_timeout(800)
    page.goto(URL, wait_until='domcontentloaded')
    wait_ready(page, 90000)
    page.screenshot(path=S + '00-mac-dinh.png')
    set_year(page)
    page.screenshot(path=S + '01-xem.png')
    for name, f in [('Tìm kiếm nâng cao', 'icon_timkiem'), ('Cài đặt bộ lọc', 'icon_caidat'),
                    ('Xuất Excel', 'icon_xuat'), ('In báo cáo', 'icon_in'), ('Xem chi tiết', 'icon_xemct')]:
        clip(page, page.get_by_role('button', name=name).first, S + f + '.png')
    # bộ lọc
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '02-bo-loc.png')
    # cài đặt bộ lọc
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '03-cai-dat.png')
    page.locator('.modal.show').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Ẩn tìm kiếm nâng cao').click(); page.wait_for_timeout(1000)
    # xem chi tiết
    page.get_by_role('button', name='Xem chi tiết').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '04-chi-tiet.png')
    clip(page, page.get_by_role('button', name='Thu gọn').first, S + 'icon_thugon.png')
    # cơ cấu tiến trình (dòng tổng)
    btn = page.locator('button.metric-link-inline').first
    clip(page, btn, S + 'icon_coca.png')
    btn.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '05-co-cau.png')
    page.locator('#solutions-summary-breakdown-modal').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    # cơ cấu nhóm ngành
    page.locator('tbody tr.row-grand td').nth(11).locator('button').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '05b-co-cau-nganh.png')
    page.locator('#solutions-summary-breakdown-modal').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    # danh sách giải pháp (YCGP đã nhận dòng tổng)
    b = page.locator('tbody tr.row-grand td').nth(2).locator('button')
    clip(page, b, S + 'icon_so.png')
    b.click(); page.wait_for_timeout(5000)
    page.screenshot(path=S + '06-danh-sach.png')
    page.locator('#solutions-flat-list-modal').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    # GP không chốt HĐ
    page.locator('tbody tr.row-grand td').last.locator('button').click(); page.wait_for_timeout(5000)
    page.screenshot(path=S + '06b-khong-chot.png')
    page.locator('#solutions-flat-list-modal').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    # xuất excel
    try:
        with page.expect_download(timeout=90000) as dl:
            page.get_by_role('button', name='Xuất Excel').first.click()
        d = dl.value; d.save_as(S + 'export.xls')
        page.wait_for_timeout(600)
    except Exception as e:
        print('download err', e)
    page.screenshot(path=S + '07-xuat.png')
    # in
    with page.context.expect_page(timeout=60000) as np:
        page.get_by_role('button', name='In báo cáo').first.click()
    pr = np.value
    pr.set_viewport_size({'width': 1440, 'height': 900})
    pr.wait_for_load_state('domcontentloaded'); pr.wait_for_timeout(12000)
    pr.screenshot(path=S + '08-in.png')
    print('print url', pr.url)
