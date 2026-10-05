# -*- coding: utf-8 -*-
"""Helper chụp ảnh headless cho bộ SRS báo cáo (Playwright Python, client local :3002 → API :8003).

    from _shoot import browser_page, clip
    with browser_page() as page:
        page.goto(BASE + '/assign/report/meeting-by-projects'); page.wait_for_timeout(5000)
        page.screenshot(path=...)
        clip(page, page.get_by_role('button', name='Xuất Excel'), path)

Mỗi tiến trình mở trình duyệt RIÊNG (headless) nên chạy song song nhiều tiến trình được.
Đăng nhập 1 lần, lưu storage state ở .auth_state.json (token nằm trong localStorage của origin).
"""
import os
from contextlib import contextmanager
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:3002'
HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, '.auth_state.json')
EMAIL, PASSWORD = 'namdangit@gmail.com', '2025Dns@2'


def _login(page):
    page.goto(BASE + '/login', wait_until='domcontentloaded')
    page.wait_for_timeout(3000)
    if '/login' in page.url:
        page.fill('#emailaddress', EMAIL)
        page.fill('input[type=password]', PASSWORD)
        page.keyboard.press('Enter')
        page.wait_for_timeout(6000)


@contextmanager
def browser_page(width=1440, height=900):
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        kw = {'viewport': {'width': width, 'height': height}}
        if os.path.exists(STATE):
            kw['storage_state'] = STATE
        ctx = b.new_context(**kw)
        page = ctx.new_page()
        page.goto(BASE + '/', wait_until='domcontentloaded')
        page.wait_for_timeout(3000)
        if '/login' in page.url:
            _login(page)
            ctx.storage_state(path=STATE)
        try:
            yield page
        finally:
            b.close()


def clip(page, locator, path, pad=3):
    """Cắt ảnh đúng 1 phần tử (icon cho dòng Menu:)."""
    bb = locator.bounding_box()
    page.screenshot(path=path, clip={'x': bb['x'] - pad, 'y': bb['y'] - pad,
                                     'width': bb['width'] + 2 * pad, 'height': bb['height'] + 2 * pad})
