from common import *
with user_page('hungvq.da@tanphat.com') as page:
    go(page,'/assign/solutions/%d/edit?mode=approve'%SID)
    btn(page,'Giao cho Leader').first.click(); page.wait_for_timeout(4000)
    page.screenshot(path=EX+'after_giao.png')
    print(page.url)
