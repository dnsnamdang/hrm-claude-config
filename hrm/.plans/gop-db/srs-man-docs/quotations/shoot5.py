import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
exec(open('shoot_common.py').read())
with browser_page() as page:
    goto_create(page)
    row = page.locator('table.info-table tr', has_text='Dự án').first
    pick_select2(page, row, 'DA001', 'DA001')
    page.locator('.products-wrap').first.wait_for(timeout=180000); page.wait_for_timeout(5000)
    page.screenshot(path=S + '06b-tao-moi-bom.png')
    page.screenshot(path=S + '06c-tao-moi-bom-full.png', full_page=True)
    page.get_by_role('button', name='Gửi duyệt').click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '13b-gui-duyet-loi.png')
    page.screenshot(path=S + '13c-gui-duyet-loi-full.png', full_page=True)
