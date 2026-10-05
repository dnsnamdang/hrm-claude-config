import sys, re; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from shoot6 import settle, go, btn
from PIL import Image
S='shots/'
with browser_page() as page:
    go(page, '/assign/request-solution/add')
    clip(page, btn(page, 'Lưu nháp').last, S+'icon_luunhap.png')
    clip(page, btn(page, 'Lưu và gửi').last, S+'icon_luuvagui.png')
    rail = page.locator('.left-side-menu .cats-list a.cat').filter(has_text=re.compile(r'^\s*Yêu cầu giải pháp\s*$')).first
    clip(page, rail, S+'icon_man_ycgp.png')
    im=Image.open(S+'icon_man_ycgp.png'); im.crop((0,0,min(185,im.width),im.height)).save(S+'icon_man_ycgp.png')
    go(page, '/assign/request-solution/37')
    b=btn(page,'Xem lịch sử').first; b.scroll_into_view_if_needed(); page.wait_for_timeout(800)
    clip(page, b, S+'icon_xemlichsu.png')
