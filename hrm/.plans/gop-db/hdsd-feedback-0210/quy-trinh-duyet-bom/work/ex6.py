from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/solution-modules/954/manager')
    for i in range(30):
        page.wait_for_timeout(3000)
        print(i, page.evaluate("()=>[...document.querySelectorAll('.loading-page')].map(e=>{const s=getComputedStyle(e);const r=e.getBoundingClientRect();return [s.display,s.visibility,s.opacity,r.width,r.height]})"))
