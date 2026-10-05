import os
from contextlib import contextmanager
from playwright.sync_api import sync_playwright
BASE = 'http://127.0.0.1:3002'
STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.auth_khien.json')
EMAIL, PASSWORD = 'khiennd.kd3@tanphat.com', 'Handover@2026'

@contextmanager
def khien_page(width=1440, height=900):
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
            page.fill('#emailaddress', EMAIL)
            page.fill('input[type=password]', PASSWORD)
            page.keyboard.press('Enter')
            page.wait_for_timeout(7000)
            ctx.storage_state(path=STATE)
        try:
            yield page
        finally:
            b.close()
