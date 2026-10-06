from common import *
with browser_page() as page:
    go(page,'/assign/request-solution/34/edit',50000)
    page.evaluate('window.scrollTo(0,0)'); page.mouse.move(5,5); page.wait_for_timeout(500)
    page.screenshot(path=S+'n11_edit.png')
