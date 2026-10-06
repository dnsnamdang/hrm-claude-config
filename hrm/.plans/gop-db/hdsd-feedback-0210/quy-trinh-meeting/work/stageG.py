from common import *
import re as _re
with browser_page(1440, 1000) as page:
    page.on('response', lambda r: print('RESP', r.status, r.url, (r.text()[:600] if 'assign/meeting/52' in r.url and r.request.method=='POST' else '')) if r.request.method=='POST' else None)
    load(page,'/assign/meeting/52/edit',5000)
    tabs = page.locator('.v2-tab-nav, [class*=tab-nav]').first
    tab_dd = page.locator('button, a, div', has_text=_re.compile(r'^\s*Điểm danh\s*$')).last
    tight(page, tab_dd, I+'tab_diemdanh.png')
    tab_bb = page.locator('button, a, div', has_text=_re.compile(r'^\s*Biên bản\s*$')).last
    tight(page, tab_bb, I+'tab_bienban.png')
    tab_dd.click(); page.wait_for_timeout(1500)
    b = btn(page, 'Điểm danh nhanh: Tất cả có mặt')
    tight(page, b, I+'btn_diemdanhnhanh.png'); b.click(); page.wait_for_timeout(800)
    row = page.locator('.attendance-table tbody tr', has_text='Ngô Thị').first
    row.locator('button.att-chip', has_text='Vắng có lý do').click(); page.wait_for_timeout(400)
    row.locator('input').last.fill('Đi công tác Đà Nẵng, đã báo trước')
    r1 = page.locator('.attendance-table tbody tr').first
    tight(page, r1.locator('.att-chip-group'), I+'chips_diemdanh.png')
    settle(page,800); page.screenshot(path=S+'07_attendance.png')
    btn(page.locator('.footer'),'Lưu').click(); page.wait_for_timeout(2500); wait_list(page)
    print(page.url)
