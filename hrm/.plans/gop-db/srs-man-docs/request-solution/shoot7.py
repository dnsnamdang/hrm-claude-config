import sys, re; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from shoot6 import settle, go, btn
S = 'shots/'
with browser_page() as page:
    page.goto(BASE + '/assign/request-solution', wait_until='domcontentloaded')
    page.wait_for_selector('table.data-table tbody tr td', timeout=240000); settle(page)
    row = page.locator('tr', has_text='TPE.YCP.TC.26.0915').first
    acts = row.locator('.v2-row-actions')
    acts.scroll_into_view_if_needed(); page.wait_for_timeout(800)
    spans = acts.locator('> span')
    for i in range(spans.count()):
        print(i, spans.nth(i).get_attribute('title'))
    a = acts.locator('span[title="Làm giải pháp"]').first
    clip(page, a, S + 'icon_lamgp_row.png')
    page.screenshot(path=S + '17-lamgp.png')
    # Hủy R1 (36)
    go(page, '/assign/request-solution/36')
    btn(page, 'Hủy yêu cầu làm giải pháp').last.click(); page.wait_for_timeout(1500)
    page.locator('.modal.show textarea').fill('Khách hàng tạm dừng đầu tư xưởng Toyota Hải Dương sang quý 2/2027, chưa cần làm giải pháp.')
    page.locator('.modal.show').locator('button', has_text='Đồng ý').click(); page.wait_for_timeout(3000); settle(page)
    page.evaluate("() => window.scrollTo(0, 400)"); page.wait_for_timeout(800)
    page.screenshot(path=S + '14c-da-huy.png')
    b = btn(page, 'Xem lịch sử').first
    b.scroll_into_view_if_needed(); b.click(); page.wait_for_timeout(4000)
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)"); page.wait_for_timeout(1500)
    page.screenshot(path=S + '16-lichsu.png')
    btn(page, 'Bộ lọc').first.click(); page.wait_for_timeout(1500)
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)"); page.wait_for_timeout(1000)
    page.screenshot(path=S + '16b-lichsu-loc.png')
