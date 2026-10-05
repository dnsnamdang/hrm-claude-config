import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)
with browser_page() as page:
    page.goto(BASE + '/assign/handover', wait_until='domcontentloaded')
    page.wait_for_selector('text=BG.2026.0001', timeout=120000); page.wait_for_timeout(2000)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Phê duyệt').first
    clip(page, rail, S + 'icon_pheduyet.png'); crop_w(S + 'icon_pheduyet.png', 110)
    rail.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + 'pheduyet-panel.png')
    g = page.get_by_text('Bàn giao - Lắp đặt', exact=True).last
    clip(page, g.locator('xpath=..'), S + 'icon_bg_lapdat.png', pad=2); crop_w(S + 'icon_bg_lapdat.png', 160)
    g.click(); page.wait_for_timeout(1200)
    page.screenshot(path=S + 'pheduyet-panel2.png')
    it = page.get_by_text('Bàn giao công việc', exact=True).last
    clip(page, it.locator('xpath=..'), S + 'icon_bgcv.png'); crop_w(S + 'icon_bgcv.png', 170)
    page.keyboard.press('Escape'); page.wait_for_timeout(300)
    # bell
    page.goto(BASE + '/assign/handover', wait_until='domcontentloaded')
    page.wait_for_selector('text=BG.2026.0001', timeout=120000); page.wait_for_timeout(2000)
    clip(page, page.locator('.noti-icon, .notification-list a, [class*=bell]').first, S + 'icon_chuong.png', pad=4)
