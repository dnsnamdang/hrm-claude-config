from common import *
with user_page('hungvq.da@tanphat.com') as page:
    go(page,'/assign/solutions/%d/manager'%SID, wait=20000)
    page.wait_for_timeout(5000); idle(page)
    icon(page, btn(page,'Tạo hồ sơ trình duyệt giải pháp'), 'btn_tao_ho_so')
