# -*- coding: utf-8 -*-
"""Chụp bổ sung ảnh + cắt icon cho HDSD bản gọn: currencies, banks, account-banks, accounts.
Chạy: python3 _cap_fin_gon.py [slug ...]   (Playwright Python headless, trình duyệt riêng)
KHÔNG lưu/xóa/khóa thật: mở hộp xác nhận rồi bấm Hủy.
"""
import os
import sys
import time

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'http://127.0.0.1:3000'
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    LOG.append(s)
    print(s, flush=True)


SCREENS = {
    'currencies': dict(route='/finance/currencies', side=[('TÀI CHÍNH', 'menu_phanhe'), ('Danh mục', 'menu_nhom')],
                       filters=[('Trạng thái', 'o_trangthai')], hist_need=True),
    'banks': dict(route='/human/banks', side=[('DANH MỤC', 'menu_phanhe'), ('Ngân hàng', 'menu_muc_side')],
                  filters=[('Tên giao dịch quốc tế', 'o_tengiaodich'), ('Trạng thái', 'o_trangthai')],
                  extra_items=[('Chi nhánh', 'item_chinhanh')], extra_inline=[('Chi nhánh', 'btn_chinhanh_row')]),
    'account-banks': dict(route='/finance/account-banks', side=[('TÀI CHÍNH', 'menu_phanhe'), ('Danh mục', 'menu_nhom')],
                          filters=[('Chi nhánh', 'o_chinhanh'), ('Trạng thái', 'o_trangthai')], hist_need=True),
    'accounts': dict(route='/finance/accounts', side=[('TÀI CHÍNH', 'menu_phanhe'), ('Danh mục', 'menu_nhom')],
                     filters=[], nang_cao=True),
}


def wait_list(page):
    page.wait_for_selector('tbody tr', timeout=90000)
    try:
        page.wait_for_function("() => document.querySelectorAll('tbody tr .v2-row-actions').length > 0", timeout=90000)
    except Exception:
        pass
    page.wait_for_timeout(10000)


def settle(page):
    page.mouse.move(5, 5)
    page.wait_for_timeout(700)


def clip_box(page, box, path):
    page.screenshot(path=path, clip=box)


def el_shot(page, loc, path):
    loc.scroll_into_view_if_needed()
    settle(page)
    b = loc.bounding_box()
    page.screenshot(path=path, clip=b)
    return b


def sidebar(page, D, items):
    for txt, name in items:
        box = page.evaluate("""(txt)=>{
          const el=[...document.querySelectorAll('a,span,div,li,button,h4,h5,p')].filter(e=>e.offsetParent && e.innerText
             && e.innerText.trim().toUpperCase()===txt.toUpperCase() && e.getBoundingClientRect().x<230);
          if(!el.length) return null;
          el.sort((a,b)=>a.getBoundingClientRect().width*a.getBoundingClientRect().height-b.getBoundingClientRect().width*b.getBoundingClientRect().height);
          let e=el[0]; while(e && !e.querySelector('svg,i,img')) e=e.parentElement;
          const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height};}""", txt)
        if not box:
            log('  !! không thấy menu', txt)
            continue
        x0 = max(box['x'] - 12, 0)
        x1 = min(box['x'] + box['width'] + 12, 218)
        settle(page)
        clip_box(page, {'x': x0, 'y': max(box['y'] - 6, 0), 'width': x1 - x0, 'height': box['height'] + 12},
                 os.path.join(D, name + '.png'))
        log('  menu', name)


def field_box(page, label):
    return page.evaluate("""(lb)=>{
      const l=[...document.querySelectorAll('label')].find(x=>x.offsetParent&&x.innerText.trim()===lb&&x.getBoundingClientRect().y<260);
      if(!l) return null; let e=l; while(e&&e.getBoundingClientRect().height<30) e=e.parentElement;
      const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height};}""", label)


def row_titles(row):
    return row.locator('td:last-child [title]').evaluate_all('els=>els.map(e=>e.getAttribute("title"))')


def find_row(page, pred):
    rows = page.locator('tbody tr')
    for i in range(rows.count()):
        r = rows.nth(i)
        try:
            t = row_titles(r)
        except Exception:
            continue
        if pred(t):
            return r, t
    return None, None


def visible_modal(page):
    return page.locator('.modal-content:visible').last


def cancel_modal(page):
    m = visible_modal(page)
    for name in ('Hủy', 'Đóng'):
        b = m.get_by_role('button', name=name)
        if b.count():
            b.last.click()
            page.wait_for_timeout(900)
            return
    page.keyboard.press('Escape')
    page.wait_for_timeout(700)


def run(slug, page):
    cfg = SCREENS[slug]
    D = os.path.join(HERE, slug, 'icons')
    SH = os.path.join(HERE, slug, 'shots')
    log('==', slug)
    page.goto(BASE + cfg['route'], wait_until='domcontentloaded')
    wait_list(page)
    sidebar(page, D, cfg['side'])

    # ô tìm nhanh (≤ 330px)
    inp = page.locator('input[placeholder^="Tìm theo"]').first
    p = os.path.join(D, 'o_timnhanh.png')
    el_shot(page, inp, p)
    im = Image.open(p).convert('RGB')
    if im.width > 336:
        w, h = im.size
        out = Image.new('RGB', (333, h))
        out.paste(im.crop((0, 0, 330, h)), (0, 0))
        out.paste(im.crop((w - 3, 0, w, h)), (330, 0))
        out.save(p)
    log('  o_timnhanh')

    if cfg.get('nang_cao'):
        btn = page.get_by_role('button', name='Tìm kiếm nâng cao')
        if btn.count():
            el_shot(page, btn.first, os.path.join(D, 'btn_timkiemnangcao.png'))
            log('  btn_timkiemnangcao')
            btn.first.click()
            page.wait_for_timeout(1500)
            labels = page.evaluate("""()=>[...document.querySelectorAll('label')].filter(l=>l.offsetParent && l.getBoundingClientRect().y<330 && l.getBoundingClientRect().x>220).map(l=>l.innerText.trim())""")
            log('  nhãn lọc nâng cao:', labels)
            for lb in labels:
                b = field_box(page, lb) or None
                if b is None:
                    b = page.evaluate("""(lb)=>{const l=[...document.querySelectorAll('label')].find(x=>x.offsetParent&&x.innerText.trim()===lb);
                        let e=l; while(e&&e.getBoundingClientRect().height<30) e=e.parentElement; const r=e.getBoundingClientRect();
                        return {x:r.x,y:r.y,width:r.width,height:r.height};}""", lb)
                name = 'o_' + ''.join(ch for ch in lb.lower() if ch.isalnum())
                settle(page)
                clip_box(page, b, os.path.join(D, name + '.png'))
                log('  ', name, lb)
            btn.first.click()
            page.wait_for_timeout(1200)
    for lb, name in cfg.get('filters', []):
        b = field_box(page, lb)
        if not b:
            log('  !! không thấy ô lọc', lb)
            continue
        settle(page)
        clip_box(page, b, os.path.join(D, name + '.png'))
        log('  ', name)

    # nút trên dòng
    r, t = find_row(page, lambda t: 'Mở khóa' in t)
    if r:
        el_shot(page, r.locator('span[title="Mở khóa"] button'), os.path.join(D, 'btn_mokhoa_row.png'))
        log('  btn_mokhoa_row', t)
        if 'Lịch sử' in t:
            el_shot(page, r.locator('span[title="Lịch sử"] button'), os.path.join(D, 'btn_lichsu_row.png'))
            log('  btn_lichsu_row (dòng khóa)')
        for txt, name in cfg.get('extra_inline', []):
            if txt in t:
                el_shot(page, r.locator('span[title="%s"] button' % txt), os.path.join(D, name + '.png'))
                log('  ', name)
    else:
        log('  !! không có dòng đang Khóa')
    r, t = find_row(page, lambda t: 'Khóa' in t and 'Hành động khác' not in t)
    if r:
        el_shot(page, r.locator('span[title="Khóa"] button'), os.path.join(D, 'btn_khoa_row.png'))
        log('  btn_khoa_row', t)
        if 'Lịch sử' in t:
            el_shot(page, r.locator('span[title="Lịch sử"] button'), os.path.join(D, 'btn_lichsu_row.png'))
            log('  btn_lichsu_row')
    else:
        log('  (không có dòng hiện Khóa thẳng)')

    r, t = find_row(page, lambda t: 'Hành động khác' in t)
    if r:
        more = r.locator('[title="Hành động khác"]').first
        el_shot(page, more, os.path.join(D, 'btn_bacham_row.png'))
        more.click()
        page.wait_for_timeout(900)
        it = page.locator('button.v2-row-actions__item:visible')
        names = it.evaluate_all('els=>els.map(e=>e.innerText.trim())')
        log('  menu ba chấm:', names, 'dòng:', t)
        for txt, name in [('Khóa', 'item_khoa'), ('Lịch sử', 'item_lichsu')] + cfg.get('extra_items', []):
            loc = it.filter(has_text=txt)
            if loc.count():
                b = loc.first.bounding_box()
                page.screenshot(path=os.path.join(D, name + '.png'), clip=b)
                log('  ', name)
        page.keyboard.press('Escape')
        page.mouse.click(700, 860)
        page.wait_for_timeout(600)
    else:
        log('  (không có dòng có ba chấm)')

    # hộp xác nhận Khóa
    r, t = find_row(page, lambda t: 'Khóa' in t or 'Hành động khác' in t)
    opened = False
    if r is not None:
        if 'Khóa' in t:
            r.locator('span[title="Khóa"] button').click()
            opened = True
        else:
            r.locator('[title="Hành động khác"]').first.click()
            page.wait_for_timeout(700)
            loc = page.locator('button.v2-row-actions__item:visible').filter(has_text='Khóa')
            if loc.count():
                loc.first.click()
                opened = True
            else:
                page.keyboard.press('Escape')
    if opened:
        page.wait_for_timeout(1500)
        m = visible_modal(page)
        settle(page)
        page.screenshot(path=os.path.join(D, 'btn_confirm_khoa.png'), clip=m.get_by_role('button', name='Khóa').bounding_box())
        page.screenshot(path=os.path.join(D, 'btn_huy_confirm.png'), clip=m.get_by_role('button', name='Hủy').bounding_box())
        log('  btn_confirm_khoa / btn_huy_confirm, tiêu đề:', m.inner_text().split('\n')[0])
        cancel_modal(page)

    # hộp xác nhận Xóa
    r, t = find_row(page, lambda t: 'Xóa' in t)
    if r is not None:
        r.locator('span[title="Xóa"] button').click()
        page.wait_for_timeout(1500)
        m = visible_modal(page)
        settle(page)
        page.wait_for_timeout(800)
        if not os.path.exists(os.path.join(SH, '13_delete.png')):
            page.screenshot(path=os.path.join(SH, '13_delete.png'))
            log('  shot 13_delete')
        page.screenshot(path=os.path.join(D, 'btn_confirm_xoa.png'), clip=m.get_by_role('button', name='Xóa').bounding_box())
        log('  btn_confirm_xoa, tiêu đề:', m.inner_text().split('\n')[0])
        cancel_modal(page)

    # tiêu đề hộp Mở khóa
    r, t = find_row(page, lambda t: 'Mở khóa' in t)
    if r is not None:
        r.locator('span[title="Mở khóa"] button').click()
        page.wait_for_timeout(1500)
        log('  tiêu đề hộp mở khóa:', visible_modal(page).inner_text().split('\n')[0])
        cancel_modal(page)

    # 16_history: bản ghi CÓ lịch sử
    rows = page.locator('tbody tr')
    done = False
    for i in range(min(rows.count(), 10)):
        r = rows.nth(i)
        try:
            t = row_titles(r)
        except Exception:
            continue
        if 'Lịch sử' in t:
            r.locator('span[title="Lịch sử"] button').click()
        elif 'Hành động khác' in t:
            r.locator('[title="Hành động khác"]').first.click()
            page.wait_for_timeout(700)
            loc = page.locator('button.v2-row-actions__item:visible').filter(has_text='Lịch sử')
            if not loc.count():
                page.keyboard.press('Escape')
                continue
            loc.first.click()
        else:
            continue
        page.wait_for_timeout(3500)
        m = visible_modal(page)
        txt = m.inner_text()
        if 'Chưa có' not in txt:
            settle(page)
            page.wait_for_timeout(1200)
            page.screenshot(path=os.path.join(SH, '16_history.png'))
            log('  shot 16_history dòng', i + 1)
            done = True
            cancel_modal(page)
            break
        cancel_modal(page)
    if not done:
        log('  !! không tìm được bản ghi có lịch sử trong 10 dòng đầu')


def main():
    slugs = sys.argv[1:] or list(SCREENS)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        page = ctx.new_page()
        page.on('dialog', lambda d: d.dismiss())
        page.goto(BASE + '/login', wait_until='domcontentloaded')
        page.wait_for_selector('#emailaddress', timeout=60000)
        page.fill('#emailaddress', 'namdangit@gmail.com')
        page.fill('input[type=password]', '2025Dns@2')
        page.get_by_role('button', name='Đăng nhập').click()
        page.wait_for_timeout(7000)
        for s in slugs:
            try:
                run(s, page)
            except Exception as e:
                log('!! LỖI', s, repr(e)[:300])
        b.close()


if __name__ == '__main__':
    main()
