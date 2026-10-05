import sys, re; sys.path.insert(0, '..')
from _shoot import browser_page, clip, BASE
S = 'shots/'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"
with browser_page() as page:
    page.goto(BASE + '/assign/report/prospective-projects', wait_until='domcontentloaded')
    page.wait_for_timeout(8000)
    page.evaluate("async () => { const vm = %s; vm.filterDraft = Object.assign({}, vm.filterDraft, {timeMode:'month', year:'2026', month:'7'}); await vm.applyFilters(); }" % VM)
    page.wait_for_timeout(4000)
    page.evaluate("() => { document.querySelector('.table-wrapper').scrollLeft = 900 }")
    page.wait_for_timeout(800)
    page.screenshot(path=S + '01b-xem-cuon.png')
    # info tooltip on title
    page.mouse.move(500, 31); page.wait_for_timeout(1200)
    page.screenshot(path=S + '_tip.png')
