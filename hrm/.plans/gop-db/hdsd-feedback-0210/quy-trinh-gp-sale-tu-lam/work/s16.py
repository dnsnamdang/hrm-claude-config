from common import *
def item(page, text, path):
    t=page.get_by_text(text, exact=True).filter(visible=True)
    t=[t.nth(i) for i in range(t.count()) if t.nth(i).bounding_box()['x']>230][0]
    bb=t.bounding_box()
    # đo độ rộng chữ thật
    w=t.evaluate("e=>{const r=document.createRange();r.selectNodeContents(e);return r.getBoundingClientRect().width}")
    page.screenshot(path=path, clip={'x':bb['x']-34,'y':bb['y']-8,'width':w+42,'height':bb['height']+16})
with browser_page() as page:
    page.goto(BASE+'/assign/solutions'); page.wait_for_timeout(8000); wait_load(page)
    page.locator('a:has-text("Làm giải pháp")').first.click(); page.wait_for_timeout(2500)
    item(page,'Quản lý giải pháp',IC+'item_quanlygp.png'); item(page,'BOM Giải pháp',IC+'item_bomgp.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(800)
    page.locator('a:has-text("Nhiệm vụ")').first.click(); page.wait_for_timeout(2500)
    page.screenshot(path='sb4.png')
    menu(page, page.locator('a:has-text("Nhiệm vụ")').first, IC+'menu_nhiemvu.png')
    item(page,'Nhiệm vụ',IC+'item_nhiemvu.png'); item(page,'Vấn đề',IC+'item_vande.png')
