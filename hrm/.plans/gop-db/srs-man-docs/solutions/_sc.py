# Helper chụp ảnh cho SRS Quản lý giải pháp (headless, client :3002)
import sys, os, re
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from contextlib import contextmanager
from playwright.sync_api import sync_playwright
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, 'shots') + '/'
LOADERS = '.loading-page:visible, .spinner-border:visible, .ri-loader-4-line:visible, .nuxt-progress:visible, .vld-overlay:visible, .b-overlay:visible'

def idle(page, extra=2500):
    for _ in range(180):
        try:
            if page.locator(LOADERS).count() == 0: break
        except Exception: pass
        page.wait_for_timeout(1000)
    page.wait_for_timeout(extra)

def go(page, path, wait=6000):
    page.goto(BASE + path, wait_until='domcontentloaded'); page.wait_for_timeout(wait); idle(page); page.wait_for_timeout(2000); idle(page)

def snap(page, name, full=False):
    page.mouse.move(5, 5); page.wait_for_timeout(800)
    page.screenshot(path=S + name, full_page=full)

def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)

@contextmanager
def user_page(email, password='HdsdGp@2026', width=1440, height=900):
    st = os.path.join(HERE, '.state_' + email.split('@')[0] + '.json')
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        kw = {'viewport': {'width': width, 'height': height}}
        if os.path.exists(st): kw['storage_state'] = st
        ctx = b.new_context(**kw); page = ctx.new_page()
        page.goto(BASE + '/', wait_until='domcontentloaded'); page.wait_for_timeout(3000)
        if '/login' in page.url:
            page.fill('#emailaddress', email); page.fill('input[type=password]', password)
            page.keyboard.press('Enter'); page.wait_for_timeout(8000)
            ctx.storage_state(path=st)
        try: yield page
        finally: b.close()

def pick(page, sel_container, text, search=None):
    """Mở select2 trong container rồi chọn option chứa text."""
    sel_container.locator('.select2-selection').first.click(); page.wait_for_timeout(900)
    f = page.locator('.select2-container--open .select2-search__field')
    if f.count():
        f.first.fill(search or text); page.wait_for_timeout(1500)
    page.locator('.select2-container--open .select2-results__option', has_text=text).first.click()
    page.wait_for_timeout(700)
