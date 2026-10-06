import sys, os
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots') + '/'
URL = BASE + '/assign/report/performance-by-solutions'

def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)

with browser_page() as page:
    for i in range(3):
        try:
            page.goto(URL, wait_until='domcontentloaded', timeout=60000)
            page.get_by_text('Vui lòng bấm Tìm kiếm để xem báo cáo.').first.wait_for(timeout=60000)
            break
        except Exception as e:
            print('retry', e)
    page.wait_for_timeout(1500)
    page.screenshot(path=D + '01-mo-man.png')
    # icons menu
    page.locator('.fe-grid').first.click(); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='Công việc').first, D + 'icon_phanhe.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 600); page.wait_for_timeout(800)
    sb = page.locator('.left-side-menu a, .sidebar a, nav a', has_text='Báo cáo').first
    clip(page, sb, D + 'icon_baocao.png'); crop_w(D + 'icon_baocao.png', 110)
    sb.click(); page.wait_for_timeout(1200)
    mi = page.get_by_text('Hiệu suất làm việc theo Giải pháp', exact=True).first
    clip(page, mi.locator('xpath=..'), D + 'icon_menu.png'); crop_w(D + 'icon_menu.png', 250)
    page.mouse.click(1367, 90); page.wait_for_timeout(800)
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao').first, D + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc').first, D + 'icon_caidat.png')
    # filter: choose company
    page.get_by_role('button', name='Tìm kiếm nâng cao').first.click(); page.wait_for_timeout(2000)
    page.locator('.smart-advanced-filters .select2-selection').nth(3).click(); page.wait_for_timeout(1000)
    page.locator('.select2-results__option', has_text='CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT').first.click()
    page.wait_for_timeout(1000); page.locator('.smart-filter-actions button').nth(0).click()
    page.locator('tr.row-dept').first.wait_for(timeout=90000)
    page.wait_for_timeout(1500)
    page.screenshot(path=D + '03-bo-loc.png')
    clip(page, page.locator('.smart-filter-actions button').nth(0), D + 'icon_btn_timkiem.png')
    clip(page, page.locator('.smart-filter-actions button').nth(1), D + 'icon_lammoi.png')
    page.get_by_role('button', name='Ẩn tìm kiếm nâng cao').first.click(); page.wait_for_timeout(1000)
    page.screenshot(path=D + '02-xem-bao-cao.png')
    page.screenshot(path=D + '02-full.png', full_page=True)
    for name, fn in [('Xem chi tiết', 'icon_xemchitiet'), ('Xuất Excel', 'icon_xuatexcel'), ('In báo cáo', 'icon_in')]:
        clip(page, page.get_by_role('button', name=name).first, D + fn + '.png')
    page.get_by_role('button', name='Xem chi tiết').first.click(); page.wait_for_timeout(1000)
    clip(page, page.get_by_role('button', name='Thu gọn').first, D + 'icon_thugon.png')
    page.get_by_role('button', name='Cài đặt bộ lọc').first.click(); page.wait_for_timeout(2000)
    page.screenshot(path=D + '04-cai-dat-bo-loc.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(800)
    row = page.locator('tr.row-solution', has_text='DA020_GP01').first
    chip = row.locator('button.chip').first
    chip.scroll_into_view_if_needed()
    clip(page, chip, D + 'icon_chip.png')
    chip.click(); page.wait_for_timeout(5000)
    page.screenshot(path=D + '05-hang-muc.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(800)
    page.evaluate('window.scrollTo(0,0)')
    with page.expect_download(timeout=120000) as dl:
        page.get_by_role('button', name='Xuất Excel').first.click()
    page.wait_for_timeout(500)
    page.screenshot(path=D + '06-xuat-excel.png')
    dl.value.save_as(D + 'export.xls')
    with page.context.expect_page(timeout=60000) as pp:
        page.get_by_role('button', name='In báo cáo').first.click()
    p2 = pp.value
    p2.set_viewport_size({'width': 1440, 'height': 900})
    p2.wait_for_load_state('domcontentloaded'); p2.wait_for_timeout(12000)
    print('print url', p2.url)
    p2.screenshot(path=D + '07-in.png')
