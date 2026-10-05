import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
exec(open('shoot_common.py').read())
with browser_page() as page:
    goto_list(page)
    scroll_table(page, 5000)
    page.locator('tr', has_text='BG-2026-00081').first.locator('[title="Hành động khác"]').first.click(); page.wait_for_timeout(800)
    page.locator('.v2-row-actions__item:visible', has_text='Sao chép báo giá').first.click()
    page.wait_for_timeout(8000)
    page.screenshot(path=S + '18-sao-chep.png')
    print(page.url)
    if 'create' in page.url:
        page.locator('.products-wrap').first.wait_for(timeout=120000); page.wait_for_timeout(4000)
        page.screenshot(path=S + '18b-ban-sao.png')
