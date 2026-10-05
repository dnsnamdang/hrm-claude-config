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
with browser_page() as page:
    goto_list(page)
    page.screenshot(path=S + '01-danh-sach.png')
    scroll_table(page, 5000); page.screenshot(path=S + '01b-danh-sach-phai.png')
    scroll_table(page, 1800); page.screenshot(path=S + '01c-danh-sach-giua.png')
    row = page.locator('tr', has_text='BG-2026-00092').first
    scroll_table(page, 5000)
    for t, n in [('Sửa / Làm giá', 'sua'), ('Xóa', 'xoa')]:
        try: clip(page, row.locator('[title="%s"]' % t).first, S + 'icon_%s.png' % n)
        except Exception as e: print('fail', t, e)
    page.screenshot(path=S + 'x-row.png')
    # menu ⋮
    try:
        row.locator('.v2-row-actions__more, [title="Thêm"], button:has(i.ri-more-2-fill)').first.click(); page.wait_for_timeout(1000)
        page.screenshot(path=S + '01d-menu-them.png')
    except Exception as e: print('more fail', e)
