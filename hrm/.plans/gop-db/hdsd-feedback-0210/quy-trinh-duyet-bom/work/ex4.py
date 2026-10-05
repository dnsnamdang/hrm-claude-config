from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/solution-modules/954/manager'); page.wait_for_timeout(12000)
    page.mouse.move(5,5)
    page.screenshot(path='x_mod_mgr.png')
    page.get_by_role('button', name='Tạo hồ sơ trình duyệt').click(); page.wait_for_timeout(5000)
    page.mouse.move(5,5)
    page.screenshot(path='x_mod_profile.png')
    print(page.locator('.modal.show').last.inner_text()[:3000])
