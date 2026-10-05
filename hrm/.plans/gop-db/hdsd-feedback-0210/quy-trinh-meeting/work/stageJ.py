from common import *
with browser_page(1440, 1000) as page:
    page.goto(BASE+'/assign/meeting', wait_until='domcontentloaded'); page.wait_for_timeout(12000); settle(page)
    hdr = page.locator('header, .navbar-custom, .topbar').first
    print(page.evaluate("()=>[...document.querySelectorAll('header *[title], .navbar-custom *[title]')].map(e=>e.tagName+':'+e.title).slice(0,20)"))
    # icon lưới phân hệ ~ (1160,30)
    el = page.evaluate("()=>{const e=document.elementFromPoint(1160,30); return e.outerHTML.slice(0,300)+' || '+e.parentElement.outerHTML.slice(0,300)}")
    print(el)
    page.mouse.click(1160,30); page.wait_for_timeout(3000)
    page.screenshot(path=W+'j_grid.png')
