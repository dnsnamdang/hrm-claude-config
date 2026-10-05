import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
exec(open('shoot_common.py').read())
with browser_page() as page:
    goto_edit(page, 92)
    def imp():
        page.locator('.products-title').get_by_role('button', name='Import Excel').click(); page.wait_for_timeout(2000)
        page.screenshot(path=S + '12-import.png')
        page.locator('input[type=file][accept=".xlsx,.xls"]').set_input_files('shots/BG92_export.xlsx'); page.wait_for_timeout(1500)
        page.get_by_role('button', name='Load lên bảng').click(); page.wait_for_timeout(4000)
        page.screenshot(path=S + '12b-import-load.png')
        page.get_by_role('button', name='Validate').click(); page.wait_for_timeout(8000)
        page.screenshot(path=S + '12c-import-validate.png')
        page.locator('.qim-footer').get_by_role('button', name='Import').click(); page.wait_for_timeout(2000)
        page.screenshot(path=S + '12d-import-phuongthuc.png')
    T(imp, 'imp')
    goto_edit(page, 92)
    def submit1():
        page.get_by_role('button', name='Gửi duyệt').click(); page.wait_for_timeout(6000)
        page.screenshot(path=S + '14b-canh-bao-gia-thap.png')
        page.get_by_role('button', name='Tiếp tục gửi duyệt').click(); page.wait_for_timeout(5000)
        page.screenshot(path=S + '14-gui-duyet-c1.png')
        page.locator('.modal.show').get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(1500)
    T(submit1, 's1')
    def c3():
        inp = page.locator('tr.shipping-row input').first
        inp.scroll_into_view_if_needed(); inp.click(); inp.fill('40000000'); page.keyboard.press('Tab'); page.wait_for_timeout(1500)
        page.evaluate("() => window.scrollBy(0, -150)"); page.wait_for_timeout(800)
        page.screenshot(path=S + '10b-cap-duyet-c3.png')
        page.get_by_role('button', name='Gửi duyệt').click(); page.wait_for_timeout(6000)
        page.get_by_role('button', name='Tiếp tục gửi duyệt').click(); page.wait_for_timeout(5000)
        page.screenshot(path=S + '14c-gui-duyet-c3.png')
        page.locator('.modal.show').get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(1500)
    T(c3, 'c3')
