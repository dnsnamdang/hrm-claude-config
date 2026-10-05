import sys, re; sys.path.insert(0, '..')
from _shoot import browser_page, clip, BASE
S = 'shots/'
with browser_page() as page:
    page.goto(BASE + '/assign/report/prospective-projects', wait_until='domcontentloaded')
    page.wait_for_timeout(8000)
    page.mouse.click(1160, 30); page.wait_for_timeout(3000)
    loc = page.locator('.switcher-item:visible', has_text='CSKH trước bán')
    print(loc.count(), [loc.nth(i).bounding_box() for i in range(loc.count())])
    page.mouse.move(10, 880); page.wait_for_timeout(1500)
    page.screenshot(path='/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/95b31591-97d1-4390-9e6c-499b30ca0f38/scratchpad/sw.png')
    clip(page, loc.first, S + 'icon_phanhe.png')
