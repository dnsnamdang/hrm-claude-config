# -*- coding: utf-8 -*-
"""Chụp icon + ảnh bổ sung cho HDSD bản gọn (Playwright Python headless, trình duyệt riêng).
python3 _cap_gon.py <slug> <route>
KHÔNG lưu / xóa / khóa thật: mở hộp xác nhận rồi bấm Hủy.
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

slug, route = sys.argv[1], sys.argv[2]
H = os.path.dirname(os.path.abspath(__file__))
IC = os.path.join(H, slug, 'icons') + '/'
SH = os.path.join(H, slug, 'shots') + '/'
BASE = 'http://127.0.0.1:3000'
info = {}


def clip(page, loc, name, d=IC):
    page.mouse.move(5, 5)
    page.wait_for_timeout(400)
    b = loc.bounding_box()
    page.screenshot(path=d + name + '.png', clip=b)
    return b


def modal(page):
    return page.locator('.modal-content:visible').last


def close_modal(page):
    for _ in range(3):
        m = page.locator('.modal-content:visible')
        if not m.count():
            return
        for t in ('Hủy', 'Đóng', 'Thoát'):
            b = m.last.get_by_role('button', name=t)
            if b.count():
                b.last.click()
                page.wait_for_timeout(800)
                break
        else:
            page.keyboard.press('Escape')
            page.wait_for_timeout(500)


with sync_playwright() as p:
    br = p.chromium.launch(headless=True)
    page = br.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(BASE + '/login', wait_until='domcontentloaded')
    page.wait_for_selector('#emailaddress', timeout=60000)
    page.fill('#emailaddress', 'namdangit@gmail.com')
    page.fill('input[type=password]', '2025Dns@2')
    page.get_by_role('button', name='Đăng nhập').click()
    page.wait_for_timeout(6000)

    def goto_list():
        page.goto(BASE + route, wait_until='domcontentloaded')
        page.wait_for_function("document.querySelectorAll('tbody tr .v2-row-actions').length > 0", timeout=90000)
        page.wait_for_timeout(10000)
        page.mouse.move(700, 600)

    goto_list()
    rows = page.locator('tbody tr')
    kinds = []
    for i in range(rows.count()):
        r = rows.nth(i)
        titles = r.locator('td:last-child [title]').evaluate_all('els => els.map(e => e.getAttribute("title"))')
        kinds.append((i, titles))
    info['rows'] = [t for _, t in kinds]

    def find(pred):
        for i, t in kinds:
            if pred(t):
                return rows.nth(i)
        return None

    r_menu = find(lambda t: 'Hành động khác' in t)
    r_lock_inline = find(lambda t: 'Khóa' in t)
    r_locked = find(lambda t: 'Mở khóa' in t)
    r_hist = find(lambda t: 'Lịch sử' in t)
    r_del = find(lambda t: 'Xóa' in t)
    info['khoa_icon_thang'] = r_lock_inline is not None
    info['has_menu'] = r_menu is not None
    if r_lock_inline is not None:
        clip(page, r_lock_inline.locator('span[title="Khóa"] button'), 'btn_khoa_row')
    if r_locked is not None:
        clip(page, r_locked.locator('span[title="Mở khóa"] button'), 'btn_mokhoa_row')
    if r_hist is not None:
        clip(page, r_hist.locator('span[title="Lịch sử"] button'), 'btn_lichsu_row')

    # ô lọc
    ph = page.locator('input[placeholder^="Tìm theo"]:visible').first
    info['placeholder'] = ph.get_attribute('placeholder')
    clip(page, ph, 'o_timnhanh')
    nc = page.get_by_role('button', name='Tìm kiếm nâng cao')
    info['nang_cao'] = nc.count() > 0
    if nc.count():
        clip(page, nc.first, 'btn_timkiemnangcao')
        nc.first.click()
        page.wait_for_timeout(1500)
    labels = page.evaluate("""() => [...document.querySelectorAll('label')].filter(l => l.offsetParent && l.getBoundingClientRect().y < 260 && l.getBoundingClientRect().x > 230).map(l => {
        let e = l; while (e && e.getBoundingClientRect().height < 30) e = e.parentElement;
        const r = e.getBoundingClientRect(); return {t: l.innerText.trim(), x: r.x, y: r.y, w: r.width, h: r.height}; })""")
    info['filters'] = [l['t'] for l in labels]
    for l in labels:
        if l['t'] == 'Trạng thái':
            page.mouse.move(5, 5); page.wait_for_timeout(300)
            page.screenshot(path=IC + 'o_trangthai.png', clip={'x': l['x'], 'y': l['y'], 'width': l['w'], 'height': l['h']})
    if nc.count():
        nc.first.click()
        page.wait_for_timeout(1000)

    # cột mở chi tiết: nút/link trong ô dòng đầu
    info['detail_col'] = rows.first.evaluate("""r => { const tds=[...r.querySelectorAll('td')];
        const i = tds.findIndex(td => td.querySelector('button, a, .v2-cell-link'));
        const th = [...document.querySelectorAll('thead th')][i]; return th ? th.innerText.trim() : i; }""")

    # menu ba chấm
    if r_menu is not None:
        more = r_menu.locator('[title="Hành động khác"]').first
        clip(page, more, 'btn_bacham_row')
        more.click()
        page.wait_for_timeout(800)
        it = page.locator('button.v2-row-actions__item:visible')
        info['menu_items'] = it.all_inner_texts()
        for t, n in (('Khóa', 'item_khoa'), ('Lịch sử', 'item_lichsu')):
            x = it.filter(has_text=t)
            if x.count():
                page.screenshot(path=IC + n + '.png', clip=x.first.bounding_box())
        page.keyboard.press('Escape')
        page.wait_for_timeout(500)

    # hộp xác nhận Khóa (lấy nút Khóa + Hủy)
    def open_action(row, title):
        b = row.locator('span[title="%s"] button' % title)
        if b.count():
            b.first.click()
        else:
            row.locator('[title="Hành động khác"]').first.click()
            page.wait_for_timeout(600)
            page.locator('button.v2-row-actions__item:visible').filter(has_text=title).first.click()
        page.wait_for_timeout(1800)

    rk = r_lock_inline or r_menu
    if rk is not None:
        open_action(rk, 'Khóa')
        m = modal(page)
        info['khoa_title'] = m.locator('.modal-title, h5, header').first.inner_text().strip()
        page.mouse.move(5, 5); page.wait_for_timeout(800)
        page.screenshot(path=IC + 'btn_confirm_khoa.png', clip=m.get_by_role('button', name='Khóa').bounding_box())
        page.screenshot(path=IC + 'btn_huy_confirm.png', clip=m.get_by_role('button', name='Hủy').bounding_box())
        close_modal(page)
    if r_locked is not None:
        open_action(r_locked, 'Mở khóa')
        info['mokhoa_title'] = modal(page).locator('.modal-title, h5, header').first.inner_text().strip()
        close_modal(page)
    if r_del is not None:
        open_action(r_del, 'Xóa')
        m = modal(page)
        info['xoa_title'] = m.locator('.modal-title, h5, header').first.inner_text().strip()
        page.mouse.move(5, 5); page.wait_for_timeout(1500)
        page.screenshot(path=SH + '13_delete.png')
        page.screenshot(path=IC + 'btn_confirm_xoa.png', clip=m.get_by_role('button', name='Xóa').bounding_box())
        close_modal(page)

    # lịch sử có dữ liệu
    info['history'] = None
    for i, t in kinds:
        if 'Lịch sử' not in t and 'Hành động khác' not in t:
            continue
        open_action(rows.nth(i), 'Lịch sử')
        txt = modal(page).inner_text()
        if 'Chưa có' not in txt:
            page.mouse.move(5, 5); page.wait_for_timeout(1500)
            page.screenshot(path=SH + '16_history.png')
            info['history'] = txt.split('\n')[0]
            close_modal(page)
            break
        close_modal(page)

    # menu thanh bên: phân hệ + nhóm
    for key, name in (('phanhe', 'menu_phanhe'), ('nhom', 'menu_nhom')):
        txt = sys.argv[3] if key == 'phanhe' else sys.argv[4]
        box = page.evaluate("""(txt) => { const el=[...document.querySelectorAll('a,span,div,li,button,h4,h5,p')].filter(e=>e.offsetParent && e.innerText && e.innerText.trim().toUpperCase()===txt.toUpperCase() && e.getBoundingClientRect().x<230);
            el.sort((a,b)=>a.getBoundingClientRect().width*a.getBoundingClientRect().height-b.getBoundingClientRect().width*b.getBoundingClientRect().height);
            let e=el[0]; while(e && !e.querySelector('svg,i,img')) e=e.parentElement; if(!e) return null;
            const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height}; }""", txt)
        if box:
            x0 = max(box['x'] - 12, 0); x1 = min(box['x'] + box['width'] + 12, 218)
            page.screenshot(path=IC + name + '.png', clip={'x': x0, 'y': max(box['y'] - 6, 0), 'width': x1 - x0, 'height': box['height'] + 12})
        info[name] = box
    br.close()

print(json.dumps(info, ensure_ascii=False, indent=1))
