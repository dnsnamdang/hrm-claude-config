from common import *
with browser_page() as page:
    go(page,'/assign/solution-modules/954/manager')
    tab(page,'Hồ sơ')
    page.mouse.move(5,5); page.screenshot(path='x_mod_hoso_tab.png')
    go(page,'/assign/solutions/953/manager')
    page.mouse.move(5,5); page.screenshot(path='x_sol_mgr.png')
    tab(page,'Hồ sơ')
    page.mouse.move(5,5); page.screenshot(path='x_sol_hoso.png')
