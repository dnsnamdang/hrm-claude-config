import sys, os
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots') + '/'
URL = BASE + '/assign/report/performance-by-employee'
only = sys.argv[1:]

def want(k):
    return not only or k in only

def load(page):
    for i in range(3):
        try:
            page.goto(URL, wait_until='domcontentloaded', timeout=60000)
            page.get_by_text('Phòng: PHÒNG DỰ ÁN').first.wait_for(timeout=60000)
            page.wait_for_timeout(1500)
            return
        except Exception as e:
            print('retry', e)

def crop_w(path, w):
    im = Image.open(path)
    im.crop((0, 0, min(w, im.width), im.height)).save(path)

with browser_page() as page:
    load(page)
    if want('icons'):
        page.locator('.fe-grid').first.click(); page.wait_for_timeout(1500)
        it = page.locator('.switcher-item', has_text='Công việc').first
        clip(page, it, D + 'icon_phanhe.png')
        page.keyboard.press('Escape'); page.mouse.click(700, 600); page.wait_for_timeout(800)
        sb = page.locator('.left-side-menu a, .sidebar a, nav a', has_text='Báo cáo').first
        clip(page, sb, D + 'icon_baocao.png')
        sb.click(); page.wait_for_timeout(1200)
        mi = page.get_by_text('Hiệu suất làm việc theo dự án', exact=True).first
        clip(page, mi.locator('xpath=..'), D + 'icon_menu.png')
        page.screenshot(path=D + '00-menu.png')
        page.mouse.click(1367, 90); page.wait_for_timeout(800)
        for name, fn in [('Xem chi tiết', 'icon_xemchitiet'), ('Xuất Excel', 'icon_xuatexcel'),
                         ('In báo cáo', 'icon_in'), ('Tìm kiếm nâng cao', 'icon_timkiem'),
                         ('Cài đặt bộ lọc', 'icon_caidat')]:
            clip(page, page.get_by_role('button', name=name).first, D + fn + '.png')
    if want('01'):
        page.screenshot(path=D + '01-man-hinh.png')
    if want('03'):
        page.get_by_role('button', name='Tìm kiếm nâng cao').first.click(); page.wait_for_timeout(2500)
        page.screenshot(path=D + '03-bo-loc.png')
        clip(page, page.locator('.smart-filter-actions button').nth(0), D + 'icon_btn_timkiem.png')
        clip(page, page.locator('.smart-filter-actions button').nth(1), D + 'icon_lammoi.png')
        page.get_by_role('button', name='Ẩn tìm kiếm nâng cao').first.click(); page.wait_for_timeout(1000)
    if want('04'):
        page.get_by_role('button', name='Cài đặt bộ lọc').first.click(); page.wait_for_timeout(2000)
        page.screenshot(path=D + '04-cai-dat-bo-loc.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(800)
    if want('02') or want('05') or want('06') or want('07'):
        page.locator('.fe-align-justify, .button-menu-mobile').first.click() if page.locator('.button-menu-mobile').count() else None
        page.wait_for_timeout(1000)
        page.get_by_role('button', name='Xem chi tiết').first.click(); page.wait_for_timeout(1500)
        page.screenshot(path=D + '02-xem-chi-tiet.png')
        page.evaluate("() => { const w = document.querySelector('.table-wrapper'); w.scrollLeft = 2000 }")
        page.wait_for_timeout(600)
        page.screenshot(path=D + '02b-xem-chi-tiet-phai.png')
        page.evaluate("() => { const w = document.querySelector('.table-wrapper'); w.scrollLeft = 0 }")
        clip(page, page.get_by_role('button', name='Xem tổng quan').first, D + 'icon_tongquan.png')
    if want('05'):
        chip = page.locator('button.chip.clickable').first
        clip(page, chip, D + 'icon_chip.png')
        chip.click(); page.wait_for_timeout(1500)
        page.screenshot(path=D + '05-chi-tiet-nhiem-vu.png')
        page.keyboard.press('Escape'); page.wait_for_timeout(800)
    if want('06'):
        with page.expect_download(timeout=120000) as dl:
            page.get_by_role('button', name='Xuất Excel').first.click()
        page.wait_for_timeout(700)
        page.screenshot(path=D + '06-xuat-excel.png')
        dl.value.save_as(D + 'export.xls')
    if want('07'):
        with page.context.expect_page(timeout=60000) as pp:
            page.get_by_role('button', name='In báo cáo').first.click()
        p2 = pp.value
        p2.set_viewport_size({'width': 1440, 'height': 900})
        p2.wait_for_load_state('domcontentloaded'); p2.wait_for_timeout(9000)
        print('print url', p2.url)
        p2.screenshot(path=D + '07-in.png')
