import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
def open_mgr(page, pid, extra=4000):
    page.goto(BASE + '/assign/prospective-projects/%d/manager' % pid, wait_until='domcontentloaded')
    page.wait_for_function("document.querySelectorAll('.tp-tab-shell').length === 1", timeout=240000)
    page.wait_for_timeout(extra)
def tab(page, label, wait=4000):
    page.locator('.tab-nav-align').get_by_text(label, exact=True).first.click(); page.wait_for_timeout(wait)
