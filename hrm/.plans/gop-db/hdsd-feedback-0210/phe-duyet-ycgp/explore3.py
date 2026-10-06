import sys,time
sys.path.insert(0,'/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, BASE
with browser_page() as page:
    pend={}
    page.on('request', lambda r: pend.__setitem__(r.url,(time.time(),r.method)) if '8003' in r.url else None)
    page.on('requestfinished', lambda r: print('done %.1fs'%(time.time()-pend.pop(r.url,(time.time(),))[0]), r.url[:120]) if r.url in pend else None)
    page.on('requestfailed', lambda r: print('FAIL', r.url[:120], r.failure))
    page.on('console', lambda m: print('CONSOLE', m.type, m.text[:200]) if m.type=='error' else None)
    page.goto(BASE+'/assign/request-solution/add', wait_until='domcontentloaded'); page.wait_for_timeout(40000)
    print('PENDING', list(pend.keys()))
    page.screenshot(path='explore/add3.png')
