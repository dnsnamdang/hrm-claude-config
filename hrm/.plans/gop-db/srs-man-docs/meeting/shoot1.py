"""Chụp ảnh màn danh sách Tổng hợp meeting (chỉ thao tác đọc / mở popup, KHÔNG ghi dữ liệu)."""
import sys, os, re
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots') + '/'
URL = BASE + '/assign/meeting'


def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)


def esc(page):
    page.keyboard.press('Escape'); page.wait_for_timeout(700)


with browser_page() as page:
    page.goto(URL, wait_until='domcontentloaded', timeout=60000)
    page.get_by_text('TPE.MET.NB.26.0068').first.wait_for(timeout=90000)
    page.wait_for_timeout(2500)
    page.screenshot(path=D + 'n01_list.png')
    # icon phân hệ + menu
    page.locator('.fe-grid').first.click(); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='Meeting').first, D + 'icon_n_phanhe.png')
    esc(page); page.mouse.click(700, 700); page.wait_for_timeout(800)
    mi = page.locator('.left-side-menu a, .sidebar a, nav a', has_text='Tổng hợp meeting').first
    clip(page, mi, D + 'icon_n_menu.png'); crop_w(D + 'icon_n_menu.png', 175)
    # nút toolbar
    for name, fn in [('Tạo mới', 'taomoi'), ('Đăng ký phòng họp', 'dkphong'), ('Xuất Excel', 'xuatexcel'),
                     ('Tìm kiếm nâng cao', 'timkiemnc'), ('Cài đặt bộ lọc', 'caidat')]:
        clip(page, page.get_by_role('button', name=name).first, D + 'icon_n_%s.png' % fn)
    clip(page, page.locator('button[title="Cấu hình cột hiển thị"]').first, D + 'icon_n_cot.png')
    clip(page, page.locator('a.v2-cell-link', has_text='TPE.MET.NB.26.0067').first, D + 'icon_n_ma.png')
    # menu ⋮ của dòng nháp 44 (do admin tạo)
    row = page.locator('tr', has_text='TPE.MET.KH.26.0041').first
    row.locator('td').last.evaluate("el => el.scrollIntoView({inline: 'end', block: 'center'})")
    page.wait_for_timeout(800)
    acts = row.locator('td').last.locator('.v2-icon-btn')
    clip(page, acts.nth(0), D + 'icon_n_sua.png')
    clip(page, acts.nth(1), D + 'icon_n_xoa.png')
    clip(page, acts.nth(2), D + 'icon_n_bacham.png')
    acts.nth(2).click(); page.wait_for_timeout(1000)
    page.screenshot(path=D + 'n02_row_menu.png')
    for txt, fn in [('In biên bản', 'inbienban'), ('Tạo phiếu công tác khác', 'taophieu'), ('Lịch sử', 'lichsu')]:
        it = page.locator('.v2-row-actions__menu:visible .v2-row-actions__item', has_text=txt).first
        try:
            clip(page, it, D + 'icon_n_%s.png' % fn, pad=1)
        except Exception as e:
            print('miss', txt, e)
    # Lịch sử popup
    page.locator('.v2-row-actions__menu:visible .v2-row-actions__item', has_text='Lịch sử').first.click()
    page.wait_for_timeout(3500)
    page.screenshot(path=D + 'n03_history.png')
    esc(page); page.wait_for_timeout(800)
    page.evaluate('window.scrollTo(0,0)')
    # Tìm kiếm nâng cao
    page.get_by_role('button', name='Tìm kiếm nâng cao').first.click(); page.wait_for_timeout(2500)
    page.screenshot(path=D + 'n04_filter.png')
    clip(page, page.locator('button:visible').filter(has_text=re.compile(r'^\s*Tìm kiếm\s*$')).first, D + 'icon_n_btntimkiem.png')
    clip(page, page.locator('button:visible').filter(has_text=re.compile(r'^\s*Làm mới\s*$')).first, D + 'icon_n_lammoi.png')
    page.get_by_role('button', name='Ẩn tìm kiếm nâng cao').first.click(); page.wait_for_timeout(1000)
    # Cài đặt bộ lọc
    page.get_by_role('button', name='Cài đặt bộ lọc').first.click(); page.wait_for_timeout(2500)
    page.screenshot(path=D + 'n05_filter_setting.png')
    esc(page)
    # Cấu hình cột
    page.locator('button[title="Cấu hình cột hiển thị"]').first.click(); page.wait_for_timeout(2500)
    page.screenshot(path=D + 'n06_columns.png')
    esc(page)
    # Xuất Excel - popup chọn trường
    page.get_by_role('button', name='Xuất Excel').first.click(); page.wait_for_timeout(2500)
    page.screenshot(path=D + 'n07_export.png')
    esc(page)
    # Đăng ký phòng họp (toolbar)
    page.get_by_role('button', name='Đăng ký phòng họp').first.click(); page.wait_for_timeout(3000)
    page.screenshot(path=D + 'n08_booking.png')
    esc(page)
