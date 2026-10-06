import sys, time
sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
R='/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/hdsd-feedback-0210/giai-phap/'
SH=R+'shots/'; IC=R+'icons/'; EX=R+'explore/'
SID=955
def snap(page, name, full=False, wait=1500):
    page.mouse.move(5,5); page.wait_for_timeout(wait)
    page.screenshot(path=SH+name+'.png', full_page=full)
def icon(page, loc, name, pad=0):
    loc=loc.first; loc.scroll_into_view_if_needed(); page.mouse.move(5,5); page.wait_for_timeout(600)
    bb=loc.bounding_box()
    page.screenshot(path=IC+name+'.png', clip={'x':bb['x']-pad,'y':bb['y']-pad,'width':bb['width']+2*pad,'height':bb['height']+2*pad})
def menu_icon(page, loc, name):
    bb=loc.first.bounding_box(); x=max(0,bb['x']-12); y=bb['y']-12
    w=min(218-x, bb['width']+24); h=bb['height']+24
    page.screenshot(path=IC+name+'.png', clip={'x':x,'y':y,'width':w,'height':h})
LOADERS='.loading-page:visible, .spinner-border:visible, .ri-loader-4-line:visible, .nuxt-progress:visible, .vld-overlay:visible, .b-overlay:visible'
def idle(page, extra=3000):
    for _ in range(150):
        try:
            if page.locator(LOADERS).count()==0: break
        except Exception: pass
        page.wait_for_timeout(1000)
    page.wait_for_timeout(extra)
def go(page, path, wait=8000):
    page.goto(BASE+path, wait_until='domcontentloaded'); page.wait_for_timeout(wait); idle(page); page.wait_for_timeout(4000); idle(page)
def btn(page, text, scope=None):
    s = scope or page
    return s.locator('button:visible, a.btn:visible', has_text=text)

from contextlib import contextmanager
from playwright.sync_api import sync_playwright
import os
@contextmanager
def user_page(email, password='HdsdGp@2026', width=1440, height=900):
    st=R+'work/state_'+email.split('@')[0]+'.json'
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True)
        kw={'viewport':{'width':width,'height':height}}
        if os.path.exists(st): kw['storage_state']=st
        ctx=b.new_context(**kw); page=ctx.new_page()
        page.goto(BASE+'/', wait_until='domcontentloaded'); page.wait_for_timeout(3000)
        if '/login' in page.url:
            page.fill('#emailaddress', email); page.fill('input[type=password]', password)
            page.keyboard.press('Enter'); page.wait_for_timeout(8000)
            ctx.storage_state(path=st)
        try: yield page
        finally: b.close()

import re as _re
def sel2(page, scope, label, text):
    g=scope.locator('.form-group', has=page.locator('label', has_text=_re.compile('^\\s*'+_re.escape(label)))).first
    g.locator('.select2-selection').first.click(); page.wait_for_timeout(800)
    f=page.locator('.select2-container--open .select2-search__field')
    if f.count(): f.first.fill(text); page.wait_for_timeout(1200)
    page.locator('.select2-container--open .select2-results__option', has_text=text).first.click()
    page.wait_for_timeout(600)
def tab(page,label):
    idle(page,1000)
    t=page.locator('.surface-hd').get_by_text(label, exact=True).first
    t.click(timeout=240000); page.wait_for_timeout(5000); idle(page); return t
