from common import *
with browser_page(1440, 1000) as page:
    page.goto(BASE+'/assign/meeting/create', wait_until='domcontentloaded'); page.wait_for_timeout(12000)
    html = page.evaluate("""() => { const n=[...document.querySelectorAll('legend,label')].find(x=>x.textContent.includes('Loại meeting')); return n.closest('fieldset,.form-group').outerHTML }""")
    print(html[:3000])
    html = page.evaluate("""() => { const n=[...document.querySelectorAll('legend,label')].find(x=>x.textContent.includes('Bắt đầu')); return n.closest('fieldset,.form-group').outerHTML }""")
    print(html[:2000])
