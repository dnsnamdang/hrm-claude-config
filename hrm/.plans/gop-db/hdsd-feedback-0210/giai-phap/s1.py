import sys; sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
D='/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/hdsd-feedback-0210/giai-phap/explore/'
with browser_page() as page:
    page.goto(BASE+'/assign/solutions', wait_until='domcontentloaded'); page.wait_for_timeout(10000)
    inp=page.locator('input[placeholder^="Tìm theo mã giải pháp"]').first
    inp.fill('DA090_GP01'); inp.press('Enter'); page.wait_for_timeout(5000)
    page.mouse.move(5,5); page.screenshot(path=D+'list.png')
    row=page.locator('tr', has_text='DA090_GP01').first
    print(row.inner_html()[-3000:])
