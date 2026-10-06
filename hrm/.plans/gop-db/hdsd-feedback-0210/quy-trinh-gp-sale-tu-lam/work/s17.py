from common import *
def side(page, loc, path):
    bb=loc.bounding_box()
    w=loc.evaluate("e=>{const r=document.createRange();r.selectNodeContents(e);return r.getBoundingClientRect().right}")
    x=max(0,bb['x']-2); right=min(216, w+10)
    page.screenshot(path=path, clip={'x':x,'y':bb['y']-4,'width':right-x,'height':bb['height']+8})
def item(page, text, path):
    t=page.get_by_text(text, exact=True).filter(visible=True)
    t=[t.nth(i) for i in range(t.count()) if t.nth(i).bounding_box()['x']>230 and t.nth(i).bounding_box()['y']>120][0]
    bb=t.bounding_box()
    w=t.evaluate("e=>{const r=document.createRange();r.selectNodeContents(e);return r.getBoundingClientRect().width}")
    page.screenshot(path=path, clip={'x':bb['x']-34,'y':bb['y']-8,'width':w+42,'height':bb['height']+16})
with browser_page() as page:
    page.goto(BASE+'/assign/prospective-projects/add'); page.wait_for_timeout(8000); wait_load(page)
    side(page, page.locator('a:has-text("Dự án TKT")').first, IC+'menu_duantkt.png')
    sec=page.locator('.solution-section')
    for txt,n in [('Có','radio_co'),('Không','radio_khong')]:
        lab=sec.locator('label').filter(has_text=txt)
        lab=[lab.nth(i) for i in range(lab.count()) if lab.nth(i).inner_text().strip()==txt][0]
        bb=lab.bounding_box(); page.screenshot(path=IC+n+'.png', clip={'x':bb['x']-26,'y':bb['y']-5,'width':bb['width']+30,'height':bb['height']+10})
    inp=page.locator('input[placeholder="Tìm theo tên dự án, mã KH, tên KH"]')
    page.goto(BASE+'/assign/prospective-projects'); page.wait_for_timeout(8000); wait_load(page)
    inp=page.locator('input[placeholder="Tìm theo tên dự án, mã KH, tên KH"]'); bb=inp.bounding_box()
    page.screenshot(path=IC+'o_timnhanh.png', clip={'x':bb['x']-12,'y':bb['y'],'width':300,'height':bb['height']})
    page.goto(BASE+'/assign/solutions'); page.wait_for_timeout(8000); wait_load(page)
    side(page, page.locator('a:has-text("Làm giải pháp")').first, IC+'menu_lamgp.png')
    side(page, page.locator('a:has-text("Nhiệm vụ")').first, IC+'menu_nhiemvu.png')
    page.locator('a:has-text("Nhiệm vụ")').first.click(); page.wait_for_timeout(2500)
    item(page,'Nhiệm vụ',IC+'item_nhiemvu.png')
