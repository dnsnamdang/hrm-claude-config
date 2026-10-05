from common import *
with user_page('hungvq.da@tanphat.com') as page:
    page.goto(BASE+'/assign/solutions/%d/manager'%SID, wait_until='domcontentloaded')
    for i in range(40):
        page.wait_for_timeout(5000)
        print(i*5, page.locator('.loading-page').count(), page.locator('.loading-page:visible').count(), page.locator(LOADERS).count(), flush=True)
        if i>3 and page.locator(LOADERS).count()==0: break
    page.screenshot(path=EX+'probe.png')
