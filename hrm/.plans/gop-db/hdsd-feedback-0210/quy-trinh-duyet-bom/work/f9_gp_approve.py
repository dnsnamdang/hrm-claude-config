from common import *
with browser_page() as page:
    go(page,'/assign/solutions/953/manager')
    tab(page,'Hồ sơ')
    shot(page,'44_gp_hoso_tab')
    row=page.locator('tr', has_text='DA091_GP01.1').first
    row.locator('[title="Duyệt"]').first.click(); idle(page)
    m=page.locator('.modal.show').last
    shot(page,'45_gp_duyet_popup')
    btn(m,'Duyệt').click(); page.wait_for_timeout(4000); idle(page)
    page.screenshot(path='x_gp_after_approve.png')
