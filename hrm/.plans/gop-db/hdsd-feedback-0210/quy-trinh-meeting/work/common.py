import sys, os
sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
D='/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/hdsd-feedback-0210/quy-trinh-meeting/'
W=D+'work/'; S=D+'shots/'; I=D+'icons/'
def tight(page, loc, path):
    loc.scroll_into_view_if_needed()
    bb = loc.bounding_box()
    page.screenshot(path=path, clip={'x': bb['x'], 'y': bb['y'], 'width': bb['width'], 'height': bb['height']})
def sel2(page, container, text):
    """mở select2 trong container rồi chọn option chứa text"""
    container.locator('.select2-selection').first.click()
    page.wait_for_timeout(800)
    page.locator('.select2-container--open .select2-results__option', has_text=text).first.click()
    page.wait_for_timeout(600)
def settle(page, ms=1500):
    page.mouse.move(5,5); page.wait_for_timeout(ms)
def fs(page, label):
    return page.locator('fieldset', has=page.locator('legend', has_text=label)).first
def setdate(page, label, text):
    inp = fs(page, label).locator('input.mx-input')
    inp.click(); inp.fill(text); page.keyboard.press('Enter'); page.wait_for_timeout(500)
    page.mouse.click(700, 20); page.wait_for_timeout(400)
import re as _re
def btn(scope, text):
    return scope.locator('button:visible', has_text=_re.compile(r'^\s*' + _re.escape(text) + r'\s*$')).first
def load(page, path, extra=3000):
    page.goto(BASE+path, wait_until='domcontentloaded')
    page.wait_for_timeout(5000)
    try:
        page.wait_for_function("()=>{const n=document.querySelector('#name'); return n && n.value && n.value.length>0}", timeout=90000)
    except Exception: pass
    try:
        page.wait_for_function("()=>!document.querySelector('.nuxt-progress, .loading-overlay, .v2-loading') ", timeout=30000)
    except Exception: pass
    page.wait_for_timeout(extra); settle(page, 800)
def wait_list(page, timeout=120000):
    try: page.wait_for_url(_re.compile(r'.*/assign/meeting/?(\?.*)?$'), timeout=timeout)
    except Exception as e: print('no redirect', page.url)
    page.wait_for_timeout(2000)
