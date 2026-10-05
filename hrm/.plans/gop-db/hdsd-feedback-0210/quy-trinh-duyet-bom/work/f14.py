from common import *
with browser_page() as page:
    go(page,'/assign/bom-list/27'); wait_name(page)
    b=page.locator('.si-header button').last
    page.evaluate("()=>{const d=document.createElement('div');d.style.height='600px';document.querySelector('.si-header').parentElement.after(d);document.querySelector('.si-header').scrollIntoView({block:'center'})}"); page.wait_for_timeout(800)
    print(b.bounding_box(), b.inner_text())
    page.screenshot(path=IC+'btn_xem_lich_su.png', clip=b.bounding_box())
