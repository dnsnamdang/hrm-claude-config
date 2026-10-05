import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
exec(open('shoot_common.py').read())
with browser_page() as page:
    page.goto(BASE + '/sale/dashboard', wait_until='domcontentloaded'); page.wait_for_timeout(6000)
    side = page.locator('.left-side-menu').get_by_text('Bán hàng', exact=True).first
    clip(page, side, S + 'icon_bh_nhom.png')
    side.hover(); page.wait_for_timeout(1500)
    page.screenshot(path=S + 'x-sale-hover.png')
    side.click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + 'x-sale-click.png')
