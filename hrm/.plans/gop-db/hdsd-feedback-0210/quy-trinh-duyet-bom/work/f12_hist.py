from common import *
with browser_page() as page:
    go(page,'/assign/bom-list/27'); wait_name(page)
    b=btn(page,'Xem lịch sử'); b.scroll_into_view_if_needed(); page.evaluate("()=>window.scrollBy(0,200)"); page.wait_for_timeout(800)
    icon(page,b,'btn_xem_lich_su'); b.evaluate("e=>e.click()"); page.wait_for_timeout(4000); idle(page)
    page.evaluate("()=>{const e=document.querySelector('.si-header'); e.scrollIntoView({block:'start'}); window.scrollBy(0,-80)}"); page.wait_for_timeout(1000)
    shot(page,'51_lich_su')
    print(page.locator('.si-body').inner_text()[:1500])
