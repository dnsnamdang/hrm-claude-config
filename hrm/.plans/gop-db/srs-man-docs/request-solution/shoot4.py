import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
R1 = 36
def wait_detail(page):
    page.wait_for_selector('text=Thông tin yêu cầu', timeout=180000); page.wait_for_timeout(9000)
def footer_btn(page, name):
    return page.get_by_role('button', name=name).last
with browser_page() as page:
    # Chi tiết bản nháp của mình
    page.goto(BASE + '/assign/request-solution/%d' % R1, wait_until='domcontentloaded'); wait_detail(page)
    page.screenshot(path=S + '10-ct-nhap.png')
    for nm, f in [('Sửa', 'icon_sua_ft'), ('Xóa', 'icon_xoa_ft'), ('Hủy yêu cầu làm giải pháp', 'icon_huy_ft'), ('Quay lại', 'icon_quaylai')]:
        b = page.get_by_role('button', name=nm)
        print(nm, b.count())
        if b.count(): clip(page, b.last, S + f + '.png')
    # lịch sử
    page.get_by_role('button', name='Xem lịch sử').first.scroll_into_view_if_needed()
    clip(page, page.get_by_role('button', name='Xem lịch sử').first, S + 'icon_xemlichsu.png')
    page.get_by_role('button', name='Xem lịch sử').first.click(); page.wait_for_timeout(4000)
    page.get_by_role('button', name='Thu gọn').first.scroll_into_view_if_needed(); page.wait_for_timeout(800)
    page.screenshot(path=S + '16-lichsu-nhap.png')
    page.evaluate('window.scrollTo(0,0)'); page.wait_for_timeout(500)
    # xác nhận xóa ở chi tiết
    footer_btn(page, 'Xóa').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '13b-xoa-ct.png')
    page.locator('.modal.show').get_by_role('button', name='Hủy').click(); page.wait_for_timeout(1000)
    # popup hủy, bấm Đồng ý khi trống -> lỗi
    footer_btn(page, 'Hủy yêu cầu làm giải pháp').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '14-huy.png')
    page.locator('.modal.show').get_by_role('button', name='Đồng ý').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '14b-huy-loi.png')
    page.locator('.modal.show').get_by_role('button', name='Không').click(); page.wait_for_timeout(1000)
    # Sửa bản nháp
    page.goto(BASE + '/assign/request-solution/%d/edit' % R1, wait_until='domcontentloaded'); wait_detail(page)
    page.screenshot(path=S + '11-sua-nhap.png')
    # Sửa yêu cầu bổ sung (id 25 - chỉ xem, không lưu)
    page.goto(BASE + '/assign/request-solution/25/edit', wait_until='domcontentloaded'); wait_detail(page)
    page.screenshot(path=S + '12-sua-bosung.png')
    page.goto(BASE + '/assign/request-solution/25', wait_until='domcontentloaded'); wait_detail(page)
    page.screenshot(path=S + '12b-ct-bosung.png')
    # Danh sách: hành động trên dòng bản nháp
    page.goto(BASE + '/assign/request-solution', wait_until='domcontentloaded')
    page.wait_for_selector('table.data-table tbody tr td', timeout=180000); page.wait_for_timeout(5000)
    row = page.locator('tr', has_text='TPE.YCP.TC.26.0914').first
    acts = row.locator('.v2-row-actions')
    acts.scroll_into_view_if_needed(); page.wait_for_timeout(800)
    clip(page, acts, S + 'icon_rowacts.png')
    spans = acts.locator('> span')
    for i in range(spans.count()):
        print(i, spans.nth(i).get_attribute('title'))
        clip(page, spans.nth(i), S + 'icon_row_%d.png' % i)
    page.screenshot(path=S + '01c-ds-hanhdong.png')
    spans.nth(1).locator('button, a').first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '13-xoa-ds.png')
    page.locator('.modal.show').get_by_role('button', name='Hủy').click(); page.wait_for_timeout(800)
    clip(page, row.locator('a.v2-cell-link').first, S + 'icon_ma.png')
