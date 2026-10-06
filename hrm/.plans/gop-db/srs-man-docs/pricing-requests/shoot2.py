import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
SCROLL = "() => { document.querySelectorAll('*').forEach(x => { if (x.scrollWidth > x.clientWidth + 20 && getComputedStyle(x).overflowX.match(/auto|scroll/)) x.scrollLeft = 99999 }) }"
def goto_list(page):
    page.goto(BASE + '/assign/pricing-requests', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách yêu cầu xây dựng giá', timeout=90000)
    page.wait_for_function("() => !document.querySelector('.v2-data-table .spinner-border')", timeout=60000)
    page.wait_for_timeout(4000)
with browser_page() as page:
    goto_list(page)
    page.evaluate(SCROLL); page.wait_for_timeout(1000)
    page.screenshot(path=S + '01b-ds-phai.png')
    # row actions of status-2 row (YCBG-2026-00004 = first row)
    row = page.locator('tr', has_text='YCBG-2026-00004').first
    acts = row.locator('td').last
    clip(acts.page, acts, S + '_row4_actions.png')
    btn = row.locator('button, a').filter(has=page.locator('i.ri-price-tag-3-line')).first
    clip(page, btn, S + 'icon_taobaogia.png')
    btn.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '10-taobaogia-xacnhan.png')
    page.get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(800)
    clip(page, page.locator('a', has_text='YCBG-2026-00002').first, S + 'icon_ma.png')
    # detail of status 4 row
    page.goto(BASE + '/assign/pricing-requests/2', wait_until='domcontentloaded'); page.wait_for_selector('text=Thời gian giao hàng', timeout=60000); page.wait_for_timeout(3000)
    page.screenshot(path=S + '06-chitiet.png')
    page.goto(BASE + '/assign/pricing-requests/4', wait_until='domcontentloaded'); page.wait_for_selector('text=Thời gian giao hàng', timeout=60000); page.wait_for_timeout(3000)
    page.screenshot(path=S + '06b-chitiet-cho.png')
