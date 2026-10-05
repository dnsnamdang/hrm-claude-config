import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
exec(open('shoot_common.py').read())
with browser_page() as page:
    page.goto(BASE + '/sale/dashboard', wait_until='domcontentloaded'); page.wait_for_timeout(6000)
    a = page.locator('.left-side-menu a:visible', has_text='Bán hàng').first
    T(lambda: (clip(page, a, S + 'icon_bh_nhom.png'), crop_w(S + 'icon_bh_nhom.png', 130)), 'nhom')
    a.click(); page.wait_for_timeout(2000)
    T(lambda: clip(page, page.locator(':visible', has_text='Báo giá').locator('xpath=self::*[normalize-space(text())="Báo giá"]').first, S+'x.png'), 'x')
    T(lambda: clip(page, page.get_by_text('Danh sách báo giá', exact=True).locator('visible=true').first.locator('xpath=..'), S + 'icon_bh_dsbaogia.png'), 'ds')
    goto_edit(page, 92)
    page.evaluate("() => window.scrollTo(0, document.querySelector('.products-wrap').getBoundingClientRect().top + window.scrollY - 70)"); page.wait_for_timeout(800)
    r = page.locator('tr.parent-row', has_text='Kích cá sấu').first
    r.hover(); page.wait_for_timeout(800)
    T(lambda: clip(page, r.locator('.inline-actions-under button', has_text='Nhân bản').first, S + 'icon_nhanban.png'), 'nb')
    r.hover(); page.wait_for_timeout(500)
    T(lambda: clip(page, r.locator('.inline-actions-under button', has_text='Thêm con').first, S + 'icon_themcon.png'), 'tc')
    T(lambda: clip(page, r.locator('button[title="Xoá"]').first, S + 'icon_xoadong.png'), 'xd')
