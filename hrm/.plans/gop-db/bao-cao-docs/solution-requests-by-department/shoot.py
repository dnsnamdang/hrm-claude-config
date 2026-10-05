# -*- coding: utf-8 -*-
"""Chụp ảnh cho SRS - Báo cáo Theo dõi YCLGP theo phòng KD (headless, client :3002)."""
import sys; sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S='shots/'
URL = BASE+'/assign/report/solution-requests-by-department'

def ready(page):
    page.goto(URL, wait_until='domcontentloaded')
    page.get_by_text('Tổng toàn bộ yêu cầu').wait_for(timeout=180000)
    page.wait_for_timeout(2000)

with browser_page() as page:
    ready(page)
    page.screenshot(path=S+'01-view.png')
    btn = lambda name: page.locator('button', has_text=name).first
    clip(page, btn('Tìm kiếm nâng cao'), S+'icon_timkiem.png')
    clip(page, btn('Cài đặt bộ lọc'), S+'icon_caidat.png')
    clip(page, btn('Xem chi tiết'), S+'icon_xemct.png')
    clip(page, btn('Xuất Excel'), S+'icon_xuat.png')
    clip(page, btn('In danh sách'), S+'icon_in.png')
    clip(page, page.locator('button.chip').first, S+'icon_cocau.png')
    clip(page, page.locator('button.group-toggle-btn').first, S+'icon_mo.png')

    # Mở từng cấp thủ công (chế độ thu gọn)
    page.locator('button.group-toggle-btn').first.click(); page.wait_for_timeout(500)
    page.locator('tr.row-dept button.group-toggle-btn').first.click(); page.wait_for_timeout(500)
    page.locator('tr.row-employee button.group-toggle-btn').first.click(); page.wait_for_timeout(800)
    page.screenshot(path=S+'02-expand.png')

    # Xem chi tiết / Thu gọn
    ready(page)
    btn('Xem chi tiết').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S+'04-detail.png')
    page.locator('.table-wrapper').first.evaluate('e => e.scrollLeft = 2000'); page.wait_for_timeout(800)
    page.screenshot(path=S+'04b-detail-right.png')
    clip(page, btn('Thu gọn'), S+'icon_thugon.png')

    # Bộ lọc
    ready(page)
    btn('Tìm kiếm nâng cao').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S+'03-filter.png')

    # Cài đặt bộ lọc
    btn('Cài đặt bộ lọc').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S+'05-config.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(800)

    # Popup cơ cấu
    ready(page)
    page.locator('button.chip').first.click()
    page.get_by_text('Số yêu cầu').first.wait_for(timeout=60000)
    page.wait_for_timeout(2000)
    page.screenshot(path=S+'06-status.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(800)

    # Xuất Excel
    try:
        with page.expect_download(timeout=120000) as dl:
            btn('Xuất Excel').click()
        d = dl.value
        d.save_as(S+'export.xls')
        page.wait_for_timeout(500)
        page.screenshot(path=S+'07-export.png')
    except Exception as e:
        print('export err', e)
        page.screenshot(path=S+'07-export.png')

    # In danh sách -> tab mới
    with page.context.expect_page(timeout=60000) as np:
        btn('In danh sách').click()
    p2 = np.value
    p2.wait_for_load_state('domcontentloaded')
    p2.get_by_text('Người lập').wait_for(timeout=180000)
    p2.wait_for_timeout(5000)
    p2.screenshot(path=S+'08-print.png')
    print('print url', p2.url)
    p2.close()

    # Icon menu
    page.locator('aside, .left-side-menu, nav').get_by_text('Báo cáo', exact=True).first.click()
    page.wait_for_timeout(1500)
    clip(page, page.get_by_text('Theo dõi YCLGP theo phòng KD').first, S+'icon_muc_raw.png', pad=8)
    clip(page, page.get_by_text('Báo cáo dự án tiền khả thi').first.locator('xpath=ancestor::*[self::a or self::button or self::li or self::div][1]'), S+'icon_nhom_raw.png', pad=3)
    clip(page, page.locator('aside, .left-side-menu, nav').get_by_text('Báo cáo', exact=True).first.locator('xpath=ancestor::*[self::a or self::li][1]'), S+'icon_baocao_raw.png', pad=0)
    page.mouse.click(1160,30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='CSKH trước bán').first, S+'icon_phanhe.png')
