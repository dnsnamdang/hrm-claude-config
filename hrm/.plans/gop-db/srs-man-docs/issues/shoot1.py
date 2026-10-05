import sys, re; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"
def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)
def goto_list(page):
    page.goto(BASE + '/assign/issues', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách Vấn đề', timeout=90000)
    page.wait_for_function("() => !document.querySelector('.v2-data-table .spinner-border')", timeout=60000)
    page.wait_for_timeout(4000)

with browser_page() as page:
    goto_list(page)
    # menu icons - Cong viec
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='Công việc').first, S + 'icon_phanhe_cv.png')
    clip(page, page.locator('.switcher-item', has_text='CSKH trước bán').first, S + 'icon_phanhe_cskh.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 870); page.wait_for_timeout(800)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Nhiệm vụ').first
    clip(page, rail, S + 'icon_nhom_nv.png'); crop_w(S + 'icon_nhom_nv.png', 120)
    rail.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '_flyout_cv.png')
    item = page.get_by_text('Vấn đề', exact=True).last
    clip(page, item.locator('xpath=..'), S + 'icon_man_cv.png')
    page.keyboard.press('Escape'); page.mouse.click(800, 870); page.wait_for_timeout(800)
    goto_list(page)
    page.screenshot(path=S + '01-ds.png')
    clip(page, page.get_by_role('button', name='Tạo Vấn đề'), S + 'icon_taomoi.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.locator('button[title="Cấu hình cột hiển thị"]'), S + 'icon_cot.png')
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    clip(page, page.locator('.scope-icons'), S + 'icon_scope.png')
    # scroll right to see more columns
    page.evaluate("() => { const w = document.querySelectorAll('.v2-data-table .table-responsive, .v2-data-table [class*=scroll]'); w.forEach(x => x.scrollLeft = 99999) }")
    page.wait_for_timeout(1000)
    page.screenshot(path=S + '01b-ds-phai.png')
    # quick scope
    goto_list(page)
    page.locator('.scope-icon-btn').first.click(); page.wait_for_timeout(3500)
    page.screenshot(path=S + '02b-loc-nhanh.png')
    page.locator('.scope-icon-btn').first.click(); page.wait_for_timeout(2500)
    # advanced filter
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(4000)
    page.screenshot(path=S + '02-loc.png')
    page.get_by_role('button', name='Ẩn tìm kiếm nâng cao').click(); page.wait_for_timeout(1000)
    # filter config
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '03-cai-dat-loc.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    # columns
    page.locator('button[title="Cấu hình cột hiển thị"]').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '04-cot.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    # export modal
    page.get_by_role('button', name='Xuất Excel').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '14-xuat.png')
    clip(page, page.get_by_role('button', name='Xuất file'), S + 'icon_xuatfile.png')
    with page.expect_download(timeout=90000) as dl:
        page.get_by_role('button', name='Xuất file').click()
    dl.value.save_as(S + 'export.xlsx')
    page.wait_for_timeout(1000)
