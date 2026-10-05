import sys, re; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
with browser_page() as page:
    page.goto(BASE + '/assign/issues', wait_until='domcontentloaded'); page.wait_for_timeout(6000)
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    page.locator('.switcher-item', has_text='CSKH trước bán').first.click(); page.wait_for_timeout(7000)
    rails = page.locator('.left-side-menu .cats-list a.cat')
    print([rails.nth(i).inner_text() for i in range(rails.count())])
    rail = rails.filter(has_text=re.compile(r'^\s*Vấn đề\s*$')).first
    clip(page, rail, S + 'icon_man_cskh.png')
    im = Image.open(S + 'icon_man_cskh.png'); im.crop((0, 0, min(120, im.width), im.height)).save(S + 'icon_man_cskh.png')
    rail.click(); page.wait_for_timeout(6000)
    page.screenshot(path=S + '_cskh.png')
