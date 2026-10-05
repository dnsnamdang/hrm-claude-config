import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)
def goto_list(page):
    page.goto(BASE + '/assign/quotations', wait_until='domcontentloaded')
    page.locator('a.v2-cell-link', has_text='BG-2026-00098').first.wait_for(timeout=180000)
    page.wait_for_timeout(2500)
def scroll_table(page, x):
    page.evaluate("x => document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = x)", x)
    page.wait_for_timeout(600)
def esc(page):
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
with browser_page() as page:
    goto_list(page)
    clip(page, page.get_by_role('button', name='Tạo báo giá'), S + 'icon_taomoi.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.locator('button[title="Cấu hình cột hiển thị"]'), S + 'icon_cot.png')
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    clip(page, page.locator('a.v2-cell-link', has_text='BG-2026-00092').first, S + 'icon_ma.png')
    row = page.locator('tr', has_text='BG-2026-00094').first
    scroll_table(page, 5000)
    for t, n in [('Sao chép báo giá', 'saochep'), ('In báo giá', 'in'), ('Lịch sử phê duyệt', 'lichsu')]:
        try: clip(page, row.locator('[title="%s"]' % t).first, S + 'icon_%s.png' % n)
        except Exception as e: print('fail', t, e)
    # history popup
    row.locator('[title="Lịch sử phê duyệt"]').first.click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '20-lichsu-popup.png'); esc(page)
    # print config
    row.locator('[title="In báo giá"]').first.click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '17-in-cauhinh.png')
    try:
        page.get_by_role('button', name='Xem trước').click(); page.wait_for_timeout(4000)
        page.screenshot(path=S + '17b-in-xemtruoc.png')
    except Exception as e: print('preview fail', e)
    esc(page); esc(page)
    goto_list(page)
    # delete confirm
    scroll_table(page, 5000)
    r92 = page.locator('tr', has_text='BG-2026-00092').first
    r92.locator('[title="Xóa"]').first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '16-xoa.png')
    page.get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(1000)
    scroll_table(page, 0)
    # filter
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '02-loc.png')
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '03-cai-dat-loc.png'); esc(page)
    page.locator('button[title="Cấu hình cột hiển thị"]').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '04-tuy-chinh-cot.png'); esc(page)
    page.get_by_role('button', name='Xuất Excel').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '05-xuat.png'); esc(page)
    # menu icons
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    page.screenshot(path=S + 'x-switcher.png')
    clip(page, page.locator('.switcher-item', has_text='CSKH trước bán').first, S + 'icon_phanhe_presale.png')
    clip(page, page.locator('.switcher-item', has_text='Bán hàng').first, S + 'icon_phanhe_bh.png')
    page.locator('.switcher-item', has_text='Bán hàng').first.click(); page.wait_for_timeout(6000)
    page.screenshot(path=S + 'x-sale.png')
    print(page.url)
