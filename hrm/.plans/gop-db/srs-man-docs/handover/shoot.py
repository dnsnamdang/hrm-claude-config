import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'

def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)

def goto_list(page):
    page.goto(BASE + '/assign/handover', wait_until='domcontentloaded')
    page.wait_for_selector('text=BG.2026.0001', timeout=120000)
    page.wait_for_timeout(2500)

def row(page, code):
    return page.locator('tr', has_text=code).first

with browser_page() as page:
    goto_list(page)
    # menu icons
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='Công việc').first, S + 'icon_phanhe.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 700); page.wait_for_timeout(800)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Nhiệm vụ').first
    clip(page, rail, S + 'icon_nhiemvu.png'); crop_w(S + 'icon_nhiemvu.png', 110)
    rail.click(); page.wait_for_timeout(1500)
    item = page.get_by_text('Phiếu bàn giao', exact=True).last
    clip(page, item.locator('xpath=..'), S + 'icon_man.png'); crop_w(S + 'icon_man.png', 150)
    page.keyboard.press('Escape'); page.wait_for_timeout(300)
    goto_list(page)
    page.screenshot(path=S + '01-ds.png')
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.get_by_role('button', name='Tạo phiếu'), S + 'icon_taophieu.png')
    clip(page, page.locator('button[title="Cấu hình cột hiển thị"]'), S + 'icon_cot.png')
    r = row(page, 'BG.2026.0003')
    r.locator('span[title="Sửa"]').first.scroll_into_view_if_needed(); page.wait_for_timeout(800)
    page.screenshot(path=S + '01b-ds-hanhdong.png')
    clip(page, r.locator('span[title="Sửa"]').first, S + 'icon_sua.png')
    clip(page, r.locator('span[title="Xóa"]').first, S + 'icon_xoa.png')
    clip(page, r.locator('span[title="Lịch sử"]').first, S + 'icon_lichsu.png')
    clip(page, row(page, 'BG.2026.0001').locator('a.v2-cell-link').first, S + 'icon_maphieu.png')
    # filter
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '02-loc.png')
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(1000)
    # settings
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '03-caidat.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # columns
    page.locator('button[title="Cấu hình cột hiển thị"]').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '04-cot.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # export modal
    page.get_by_role('button', name='Xuất Excel').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '05-xuat.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # history popup (row A)
    r = row(page, 'BG.2026.0001')
    r.locator('span[title="Lịch sử"]').first.scroll_into_view_if_needed()
    r.locator('span[title="Lịch sử"]').first.click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '11-lichsu.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # delete confirm (row B draft)
    row(page, 'BG.2026.0003').locator('span[title="Xóa"]').first.scroll_into_view_if_needed()
    row(page, 'BG.2026.0003').locator('span[title="Xóa"]').first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '10-xoa.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)

    # detail A
    page.goto(BASE + '/assign/handover/3', wait_until='domcontentloaded')
    page.wait_for_selector('text=Thông tin bàn giao', timeout=90000); page.wait_for_timeout(3500)
    page.screenshot(path=S + '06-chitiet.png')
    page.get_by_role('button', name='Xem lịch sử').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '06b-chitiet-lichsu.png', full_page=True)
