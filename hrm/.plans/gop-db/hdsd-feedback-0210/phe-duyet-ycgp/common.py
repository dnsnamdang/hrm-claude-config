import sys
sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
S='shots/'; I='icons/'
def go(page,url,wait=30000):
    page.goto(BASE+url, wait_until='domcontentloaded'); page.wait_for_timeout(wait); page.mouse.move(5,5); page.wait_for_timeout(500)
def cut(page, loc, path, pad=0):
    loc.scroll_into_view_if_needed(); page.wait_for_timeout(300)
    bb=loc.bounding_box()
    page.screenshot(path=I+path, clip={'x':bb['x']-pad,'y':bb['y']-pad,'width':bb['width']+2*pad,'height':bb['height']+2*pad})
def cut_menu(page, loc, path):
    bb=loc.bounding_box()
    x=max(bb['x']-12,0); w=min(bb['x']+bb['width']+12,218)-x
    page.screenshot(path=I+path, clip={'x':x,'y':bb['y']-12,'width':w,'height':bb['height']+24})
def side(page, text):
    loc=page.get_by_text(text, exact=True)
    for i in range(loc.count()):
        bb=loc.nth(i).bounding_box()
        if bb and bb['x']<220 and bb['width']>0: return loc.nth(i)
    raise Exception('no side '+text)
def cut_side(page, text, path):
    # whole row: parent element of text
    el=side(page,text)
    bb=el.bounding_box()
    x=4; y=bb['y']-10; w=214; h=bb['height']+20
    page.screenshot(path=I+path, clip={'x':x,'y':y,'width':w,'height':h})
def s2(page, scope_loc, idx, text, pick_first=True):
    sel=scope_loc.locator('.select2-selection').nth(idx)
    sel.scroll_into_view_if_needed(); sel.click(); page.wait_for_timeout(800)
    sf=page.locator('.select2-container--open .select2-search__field')
    if sf.count(): sf.first.fill(text); page.wait_for_timeout(1500)
    print('OPTS', page.locator('.select2-container--open .select2-results__option').all_inner_texts()[:8])
    opt=page.locator('.select2-container--open .select2-results__option').filter(has_text=text).first
    opt.click(); page.wait_for_timeout(800)
def date(page, loc, val):
    loc.scroll_into_view_if_needed(); loc.click(); loc.fill(val); page.keyboard.press('Enter'); page.wait_for_timeout(500); page.mouse.click(1300,140); page.wait_for_timeout(300)
