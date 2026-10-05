import sys; sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
def pick(page, idx, text):
    inp=page.locator('.sp-wrap input.sp-field').nth(idx)
    inp.click(); page.wait_for_timeout(500)
    inp.fill(text); page.wait_for_timeout(1500)
    page.locator('.sp-dropdown:visible .sp-item').first.click(); page.wait_for_timeout(2500)
import os
D='/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/hdsd-feedback-0210/quy-trinh-duyet-bom'
SH=D+'/shots/'; IC=D+'/icons/'
def icon(page, loc, name):
    loc.scroll_into_view_if_needed(); page.wait_for_timeout(300)
    bb=loc.bounding_box()
    page.screenshot(path=IC+name+'.png', clip={'x':bb['x'],'y':bb['y'],'width':bb['width'],'height':bb['height']})
def shot(page, name, full=False):
    page.mouse.move(5,5); page.wait_for_timeout(800)
    page.screenshot(path=SH+name+'.png', full_page=full)
import re
def btn(scope, text):
    return scope.locator('button:visible').filter(has_text=re.compile(r'^\s*'+re.escape(text)+r'\s*$')).first
def tab(page, text):
    page.locator('.tab-label', has_text=re.compile(r'^\s*'+re.escape(text)+r'\s*$')).first.click()
    idle(page)
def _busy(page):
    return page.evaluate("()=>[...document.querySelectorAll('.loading-page, .nuxt-progress')].filter(e=>e.getBoundingClientRect().width>0 && getComputedStyle(e).display!=='none').length>0")
def idle(page, extra=1500, maxs=120):
    import time
    t0=time.time(); free=0
    while time.time()-t0<maxs:
        page.wait_for_timeout(1000)
        if _busy(page): free=0
        else:
            free+=1
            if free>=4: break
    page.wait_for_timeout(extra)
def go(page, path):
    page.set_default_timeout(150000)
    page.goto(BASE+path); page.wait_for_timeout(4000); idle(page)
def wait_name(page, maxs=120):
    for i in range(maxs//2):
        page.wait_for_timeout(2000)
        v=page.locator('input[placeholder="VD: BOM điều khiển dây chuyền line 01"]')
        if v.count() and v.first.input_value(): break
    idle(page)
