from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/prospective-projects/add'); page.wait_for_timeout(9000)
    tight(page, page.locator('.solution-section label:has-text("Có")').first, IC+'radio_co.png')
    tight(page, page.locator('.solution-section label:has-text("Không")').first, IC+'radio_khong.png')
    page.goto(BASE+'/assign/prospective-projects/151/manager'); page.wait_for_timeout(15000); settle(page)
    page.screenshot(path='pm151.png')
    page.goto(BASE+'/assign/solutions/add?prospective_project_id=151'); page.wait_for_timeout(15000); settle(page)
    page.screenshot(path='soladd.png', full_page=True)
