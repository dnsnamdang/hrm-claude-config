import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
exec(open('shoot_common.py').read())
with browser_page() as page:
    goto_edit(page, 92)
    page.screenshot(path=S + '07-lam-gia.png')
    if page.get_by_text('Đơn giá hàng hoá đã thay đổi').count():
        page.screenshot(path=S + '15b-cap-nhat-gia.png'); page.get_by_role('button', name='Từ chối').click(); page.wait_for_timeout(1000)
    page.screenshot(path=S + '07-lam-gia-full.png', full_page=True)
    T(lambda: clip(page, page.get_by_role('button', name='Lưu nháp'), S + 'icon_luunhap.png'), 'luu')
    T(lambda: clip(page, page.get_by_role('button', name='Gửi duyệt'), S + 'icon_guiduyet.png'), 'gui')
    T(lambda: clip(page, page.get_by_role('button', name='Import Excel'), S + 'icon_import.png'), 'imp')
    T(lambda: clip(page, page.locator('.products-title').get_by_role('button', name='Xuất Excel'), S + 'icon_xuat_ct.png'), 'xuat')
    # bảng giá
    page.locator('.products-title').get_by_role('button', name='Ẩn cột chi tiết').click(); page.wait_for_timeout(800)
    page.evaluate("() => window.scrollTo(0, document.querySelector('.products-wrap').getBoundingClientRect().top + window.scrollY - 70)"); page.wait_for_timeout(1000)
    page.screenshot(path=S + '07b-bang-gia.png')
    page.evaluate("() => { const e = document.querySelector('.products-scroll'); e.scrollLeft = 5000 }"); page.wait_for_timeout(800)
    page.screenshot(path=S + '07c-bang-gia-phai.png')
    page.evaluate("() => { const e = document.querySelector('.products-scroll'); e.scrollLeft = 0 }"); page.wait_for_timeout(500)
    # them nhom
    def nhom():
        page.locator('.products-title').get_by_role('button', name='Thêm nhóm').click(); page.wait_for_timeout(1200)
        page.screenshot(path=S + '08c-them-nhom.png'); esc(page)
    T(nhom, 'nhom')
    # sua hang tam
    def suatam():
        page.locator('tr.parent-row', has_text='Kích cá sấu').get_by_role('button', name='Sửa').click(); page.wait_for_timeout(2500)
        page.screenshot(path=S + '08f-sua-hang-tam.png'); esc(page)
    T(suatam, 'suatam')
    def xoadong():
        page.locator('tr.parent-row', has_text='Kích cá sấu').locator('button[title="Xoá"]').click(); page.wait_for_timeout(1200)
        page.screenshot(path=S + '08g-xoa-dong.png'); page.get_by_role('button', name='Đóng').last.click(); page.wait_for_timeout(800)
    T(xoadong, 'xoadong')
    T(lambda: clip(page, page.locator('tr.parent-row', has_text='Kích cá sấu').get_by_role('button', name='Nhân bản'), S + 'icon_nhanban.png'), 'nb')
    # them moi hang hoa
    def themmoi():
        page.locator('.q-section-row', has_text='A — Hàng hoá').get_by_role('button', name='Thêm mới').click()
        page.wait_for_timeout(12000)
        page.screenshot(path=S + '08-them-hang.png')
        page.get_by_role('button', name='Thêm hàng tạm').click(); page.wait_for_timeout(2500)
        page.screenshot(path=S + '08d-hang-tam-taisudung.png')
        page.get_by_role('tab', name='Thêm mới thủ công').click(); page.wait_for_timeout(2500)
        page.screenshot(path=S + '08e-hang-tam-thucong.png')
        page.locator('.bom-quick-add-title', has_text='Thêm hàng tạm').locator('xpath=..').locator('button.close').click(); page.wait_for_timeout(800)
        page.locator('.modal-footer-fixed').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    T(themmoi, 'themmoi')
    def dichvu():
        page.locator('.q-section-row', has_text='B — Dịch vụ').get_by_role('button', name='Thêm mới').click()
        page.wait_for_timeout(8000)
        page.screenshot(path=S + '08h-them-dich-vu.png')
        page.locator('.modal-footer-fixed').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    T(dichvu, 'dichvu')
    # lam tron
    def lamtron():
        sel = page.locator('.price-toolbar select').nth(1)
        print(page.locator('.price-toolbar select').count())
        page.screenshot(path=S + 'x-toolbar.png')
    T(lamtron, 'lamtron')
    # GG
    def gg():
        page.locator('.price-toolbar select').first.select_option('1'); page.wait_for_timeout(1500)
        page.evaluate("() => window.scrollTo(0, document.querySelector('.products-wrap').getBoundingClientRect().top + window.scrollY - 70)"); page.wait_for_timeout(800)
        page.evaluate("() => { const e = document.querySelector('.products-scroll'); e.scrollLeft = 400 }"); page.wait_for_timeout(800)
        page.screenshot(path=S + '09-gg-mat-hang.png')
        page.locator('.price-toolbar select').first.select_option('2'); page.wait_for_timeout(1500)
        page.get_by_role('button', name='Thêm khoản GG').click(); page.wait_for_timeout(800)
        scroll_to(page, '.discount-total-section')
        page.screenshot(path=S + '09b-gg-tong.png')
    T(gg, 'gg')
    def tonghop():
        scroll_to(page, '.summary-section')
        page.evaluate("() => window.scrollBy(0, 150)"); page.wait_for_timeout(800)
        page.screenshot(path=S + '10-tong-hop.png')
    T(tonghop, 'tonghop')
    def dieukhoan():
        scroll_to(page, '.bottom-section')
        page.evaluate("() => window.scrollBy(0, 300)"); page.wait_for_timeout(1500)
        page.screenshot(path=S + '11-dieu-khoan.png')
    T(dieukhoan, 'dk')
