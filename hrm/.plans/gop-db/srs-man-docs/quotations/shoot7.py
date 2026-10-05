import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
exec(open('shoot_common.py').read())
def top_table(page):
    page.evaluate("() => window.scrollTo(0, document.querySelector('.products-wrap').getBoundingClientRect().top + window.scrollY - 70)"); page.wait_for_timeout(1000)
with browser_page() as page:
    goto_edit(page, 92)
    top_table(page)
    r = page.locator('tr.parent-row', has_text='Kích cá sấu').first
    r.hover(); page.wait_for_timeout(800)
    page.screenshot(path=S + 'x-hover.png')
    print(r.locator('.inline-actions-under').count(), r.locator('.inline-actions-under').inner_html()[:300] if r.locator('.inline-actions-under').count() else '')
    def suatam():
        r.locator('.inline-actions-under button', has_text='Sửa').first.click(); page.wait_for_timeout(2500)
        page.screenshot(path=S + '08f-sua-hang-tam.png')
        page.locator('.modal.show button.close').last.click(); page.wait_for_timeout(1000)
    T(suatam, 'suatam')
    T(lambda: clip(page, r.locator('.inline-actions-under button', has_text='Nhân bản').first, S + 'icon_nhanban.png'), 'nb')
    T(lambda: clip(page, r.locator('.inline-actions-under button', has_text='Thêm con').first, S + 'icon_themcon.png'), 'tc')
    T(lambda: clip(page, page.locator('.q-section-row', has_text='A — Hàng hoá').get_by_role('button', name='Thêm mới'), S + 'icon_themmoi_hang.png'), 'tm')
    T(lambda: clip(page, page.locator('.products-title').get_by_role('button', name='Thêm nhóm'), S + 'icon_themnhom.png'), 'tn')
    def themmoi():
        page.locator('.q-section-row', has_text='A — Hàng hoá').get_by_role('button', name='Thêm mới').click()
        page.wait_for_timeout(15000)
        page.screenshot(path=S + '08-them-hang.png')
        page.get_by_role('button', name='Thêm hàng tạm').click(); page.wait_for_timeout(2500)
        page.screenshot(path=S + '08d-hang-tam-taisudung.png')
        page.get_by_role('tab', name='Thêm mới thủ công').click(); page.wait_for_timeout(2500)
        page.screenshot(path=S + '08e-hang-tam-thucong.png')
    T(themmoi, 'themmoi')
    goto_edit(page, 92)
    def dichvu():
        page.locator('.q-section-row', has_text='B — Dịch vụ').get_by_role('button', name='Thêm mới').click()
        page.wait_for_timeout(10000)
        page.screenshot(path=S + '08h-them-dich-vu.png')
    T(dichvu, 'dichvu')
