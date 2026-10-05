import sys, os
sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
ROOT='/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/hdsd-feedback-0210/quy-trinh-gp-sale-tu-lam'
SH=ROOT+'/shots/'; IC=ROOT+'/icons/'
def tight(page, loc, path, pad=0):
    loc.scroll_into_view_if_needed(); page.wait_for_timeout(300)
    bb=loc.bounding_box()
    page.screenshot(path=path, clip={'x':bb['x']-pad,'y':bb['y']-pad,'width':bb['width']+2*pad,'height':bb['height']+2*pad})
def menu(page, loc, path):
    bb=loc.bounding_box()
    x=max(0,bb['x']-12); y=bb['y']-12; w=min(218-x, bb['width']+24); h=bb['height']+24
    page.screenshot(path=path, clip={'x':x,'y':y,'width':w,'height':h})
def settle(page, ms=1500):
    page.mouse.move(5,5); page.wait_for_timeout(ms)
def wait_text(page, text, timeout=60000, extra=4000):
    page.get_by_text(text).first.wait_for(state='visible', timeout=timeout); page.wait_for_timeout(extra)
def wait_idle(page, extra=3000):
    try: page.wait_for_load_state('networkidle', timeout=60000)
    except Exception as e: print('idle timeout')
    page.wait_for_timeout(extra)
def wait_load(page, extra=2500, timeout=120000):
    page.wait_for_timeout(3000)
    try: page.locator('.loading-page').first.wait_for(state='hidden', timeout=timeout)
    except Exception: print('loading-page still visible')
    page.wait_for_timeout(extra)
