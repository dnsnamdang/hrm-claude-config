import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)
def goto_list(page):
    page.goto(BASE + '/assign/prospective-projects', wait_until='domcontentloaded')
    page.wait_for_selector('text=HN_DA.UD.0137.2026.DA020', timeout=180000)
    page.wait_for_timeout(2500)
with browser_page() as page:
    goto_list(page)
    clip(page, page.get_by_role('button', name='Tạo mới'), S + 'icon_taomoi.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.locator('button[title="Cấu hình cột hiển thị"]'), S + 'icon_cot.png')
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    clip(page, page.locator('a.v2-cell-link', has_text='HN_DA.UD.0137.2026.DA020'), S + 'icon_ma.png')
    m = page.locator('.left-side-menu a', has_text='Dự án TKT').first
    clip(page, m, S + 'icon_menu_duan.png'); crop_w(S + 'icon_menu_duan.png', 140)
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='CSKH trước bán').first, S + 'icon_phanhe_presale.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 700); page.wait_for_timeout(800)
    # row actions
    page.evaluate("document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = 9000)"); page.wait_for_timeout(800)
    page.screenshot(path=S + '01b-danh-sach-phai.png')
    page.evaluate("document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = 1700)"); page.wait_for_timeout(800)
    page.screenshot(path=S + '01c-danh-sach-giua.png')
    page.evaluate("document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = 0)"); page.wait_for_timeout(500)
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '02-loc.png')
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '03-cai-dat-loc.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    page.locator('button[title="Cấu hình cột hiển thị"]').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '04-tuy-chinh-cot.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    page.get_by_role('button', name='Xuất Excel').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '20-xuat.png')
    with page.expect_download(timeout=180000) as dl:
        page.get_by_role('button', name='Xuất file').click()
    dl.value.save_as(S + 'export.xlsx')
