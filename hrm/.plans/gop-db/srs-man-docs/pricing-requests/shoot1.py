import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)
def goto_list(page):
    page.goto(BASE + '/assign/pricing-requests', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách yêu cầu xây dựng giá', timeout=90000)
    page.wait_for_function("() => !document.querySelector('.v2-data-table .spinner-border')", timeout=60000)
    page.wait_for_timeout(4000)

with browser_page() as page:
    goto_list(page)
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    page.screenshot(path=S + '_switcher.png')
    clip(page, page.locator('.switcher-item', has_text='CSKH trước bán').first, S + 'icon_phanhe.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 870); page.wait_for_timeout(800)
    page.screenshot(path=S + '_rail.png')
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Yêu cầu tính giá bán').first
    clip(page, rail, S + 'icon_man.png')
    goto_list(page)
    page.screenshot(path=S + '01-ds.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.locator('button[title="Cấu hình cột hiển thị"]'), S + 'icon_cot.png')
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    page.evaluate("() => { const w = document.querySelectorAll('.v2-data-table .table-responsive, .v2-data-table [class*=scroll]'); w.forEach(x => x.scrollLeft = 99999) }")
    page.wait_for_timeout(1000)
    page.screenshot(path=S + '01b-ds-phai.png')
    goto_list(page)
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(4000)
    page.screenshot(path=S + '02-loc.png')
    page.get_by_role('button', name='Ẩn tìm kiếm nâng cao').click(); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '03-cai-dat-loc.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    page.locator('button[title="Cấu hình cột hiển thị"]').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '04-cot.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Xuất Excel').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '05-xuat.png')
    clip(page, page.get_by_role('button', name='Xuất file'), S + 'icon_xuatfile.png')
    with page.expect_download(timeout=90000) as dl:
        page.get_by_role('button', name='Xuất file').click()
    dl.value.save_as(S + 'export.xlsx')
    page.wait_for_timeout(1000)
