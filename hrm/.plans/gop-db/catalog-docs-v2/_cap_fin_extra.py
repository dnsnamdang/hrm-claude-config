# -*- coding: utf-8 -*-
"""Chụp phần riêng: banks (Tra cứu, cửa sổ Chi nhánh), accounts (In danh sách). Không lưu gì."""
import os
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'http://127.0.0.1:3000'

def settle(p): p.mouse.move(5, 5); p.wait_for_timeout(700)
def shot(p, loc, path):
    loc.scroll_into_view_if_needed(); settle(p); p.screenshot(path=path, clip=loc.bounding_box()); print('  ', os.path.basename(path))
def modal(p): return p.locator('.modal-content:visible').last

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True); page = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
    page.on('dialog', lambda d: d.dismiss())
    page.goto(BASE + '/login'); page.wait_for_selector('#emailaddress', timeout=60000)
    page.fill('#emailaddress', 'namdangit@gmail.com'); page.fill('input[type=password]', '2025Dns@2')
    page.get_by_role('button', name='Đăng nhập').click(); page.wait_for_timeout(7000)

    # ---- banks
    D = os.path.join(HERE, 'banks', 'icons'); SH = os.path.join(HERE, 'banks', 'shots')
    page.goto(BASE + '/human/banks'); page.wait_for_selector('tbody tr .v2-row-actions', timeout=90000); page.wait_for_timeout(10000)
    page.get_by_role('button', name='Tạo mới').first.click(); page.wait_for_timeout(2500)
    m = modal(page)
    print('form:', m.inner_text()[:200].replace('\n', ' | '))
    tc = m.get_by_role('button', name='Tra cứu')
    if tc.count(): shot(page, tc.first, os.path.join(D, 'btn_tracuu.png'))
    gy = m.locator('input[placeholder*="Nhập tên/mã ngân hàng"]')
    if gy.count(): shot(page, gy.first, os.path.join(D, 'o_goiy.png'))
    m.get_by_role('button', name='Đóng').last.click(); page.wait_for_timeout(1200)
    if page.locator('.modal-content:visible').count():
        t = modal(page).inner_text()
        if 'chưa lưu' in t:
            modal(page).get_by_role('button', name='Thoát').click(); page.wait_for_timeout(800)
    # cửa sổ chi nhánh: dòng có ba chấm -> Chi nhánh
    rows = page.locator('tbody tr')
    for i in range(rows.count()):
        r = rows.nth(i)
        more = r.locator('[title="Hành động khác"]')
        if more.count():
            more.first.click(); page.wait_for_timeout(700)
            page.locator('button.v2-row-actions__item:visible').filter(has_text='Chi nhánh').first.click()
            break
    page.wait_for_timeout(3500)
    m = modal(page)
    print('chi nhánh:', m.inner_text()[:300].replace('\n', ' | '))
    tm = m.get_by_role('button', name='Tạo mới')
    if tm.count(): shot(page, tm.first, os.path.join(D, 'btn_taomoi_chinhanh.png'))
    brow = m.locator('tbody tr')
    info = []
    for i in range(min(brow.count(), 10)):
        info.append(brow.nth(i).locator('td:last-child [title]').evaluate_all('els=>els.map(e=>e.getAttribute("title"))'))
    print('branch rows actions:', info)
    # ba chấm của chi nhánh
    bm = m.locator('tbody tr [title="Hành động khác"]')
    if bm.count():
        shot(page, bm.first, os.path.join(D, 'btn_bacham_chinhanh.png'))
        bm.first.click(); page.wait_for_timeout(700)
        it = page.locator('button.v2-row-actions__item:visible')
        print('ba chấm chi nhánh:', it.evaluate_all('els=>els.map(e=>e.innerText.trim())'))
        for txt, n in [('Khóa', 'item_khoa_chinhanh'), ('Lịch sử', 'item_lichsu_chinhanh')]:
            l = it.filter(has_text=txt)
            if l.count(): page.screenshot(path=os.path.join(D, n + '.png'), clip=l.first.bounding_box()); print('  ', n)
        page.keyboard.press('Escape'); page.wait_for_timeout(500)
    # tiêu đề hộp xóa chi nhánh
    xb = m.locator('tbody tr span[title="Xóa"] button')
    if xb.count():
        xb.first.click(); page.wait_for_timeout(1500)
        mm = modal(page); print('hộp xóa chi nhánh:', mm.inner_text().split('\n')[0])
        mm.get_by_role('button', name='Hủy').click(); page.wait_for_timeout(900)

    # ---- accounts
    D = os.path.join(HERE, 'accounts', 'icons')
    page.goto(BASE + '/finance/accounts'); page.wait_for_selector('tbody tr .v2-row-actions', timeout=90000); page.wait_for_timeout(10000)
    inb = page.get_by_role('button', name='In', exact=True)
    if not inb.count(): inb = page.locator('button:has-text("In")').filter(has_not_text='Import')
    shot(page, inb.first, os.path.join(D, 'btn_in.png'))
    inb.first.click(); page.wait_for_timeout(6000)
    m = modal(page)
    print('in preview:', m.inner_text()[:120].replace('\n', ' | '))
    for n in ['In', 'Đóng']:
        l = m.get_by_role('button', name=n, exact=True)
        if l.count(): shot(page, l.last, os.path.join(D, 'btn_%s_preview.png' % ('in' if n == 'In' else 'dong')))
    b.close()
