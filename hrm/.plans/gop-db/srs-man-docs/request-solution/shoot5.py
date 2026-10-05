import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
def wait_detail(page):
    page.wait_for_selector('text=Thông tin yêu cầu', timeout=180000); page.wait_for_timeout(9000)
with browser_page() as page:
    page.goto(BASE + '/assign/request-solution/34', wait_until='domcontentloaded'); wait_detail(page)
    page.screenshot(path=S + '10b-ct-cho.png')
    for nm, f in [('Tiếp nhận', 'icon_tiepnhan_ft'), ('Từ chối', 'icon_tuchoi_ft')]:
        b = page.get_by_role('button', name=nm, exact=True)
        print(nm, b.count())
        if b.count(): clip(page, b.last, S + f + '.png')
    tabs = ['Dự án tiền khả thi', 'Meetings', 'Phiếu thu thập thông tin']
    for i, t in enumerate(tabs):
        el = page.get_by_text(t, exact=True).first
        clip(page, el.locator('xpath=ancestor-or-self::*[self::a or self::button or self::li][1]'), S + 'icon_tab_%d.png' % (i + 1))
        el.click(); page.wait_for_timeout(5000)
        page.screenshot(path=S + '10%s-tab-%d.png' % ('cde'[i], i + 1))
    page.get_by_text('Thông tin yêu cầu', exact=True).first.click(); page.wait_for_timeout(1500)
    clip(page, page.get_by_text('Thông tin yêu cầu', exact=True).first.locator('xpath=ancestor-or-self::*[self::a or self::button or self::li][1]'), S + 'icon_tab_0.png')
    page.get_by_role('button', name='Tiếp nhận', exact=True).last.click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '15-tiepnhan.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    page.goto(BASE + '/assign/request-solution/34', wait_until='domcontentloaded'); wait_detail(page)
    page.get_by_role('button', name='Từ chối', exact=True).last.click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '15b-tuchoi.png')
    page.locator('.modal.show').get_by_role('button', name='Không').click(); page.wait_for_timeout(800)
    # Meetings tab: nut Tao moi
    page.get_by_text('Meetings', exact=True).first.click(); page.wait_for_timeout(4000)
    b = page.locator('.modal.show, body').get_by_role('button', name='Tạo mới')
    print('meet tao moi', b.count())
    if b.count(): clip(page, b.first, S + 'icon_taomeeting.png')
