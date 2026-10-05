from common import *
with browser_page(1440, 1000) as page:
    load(page,'/assign/meeting/52/show',5000)
    page.screenshot(path=S+'09_complete.png')
    btn(page.locator('.footer'),'In').click(); page.wait_for_timeout(2500)
    m = page.locator('.modal.show').last
    settle(page,800); page.screenshot(path=S+'10_print_config.png')
    tight(page, btn(m,'Xem trước'), I+'btn_xemtruoc.png')
    tight(page, btn(m,'Huỷ'), I+'btn_huy_cfg.png')
    btn(m,'Xem trước').click(); page.wait_for_timeout(5000)
    settle(page,800); page.screenshot(path=S+'11_print_preview.png')
    tight(page, btn(page.locator('.modal.show').last,'In'), I+'btn_in_preview.png')
    page.goto(BASE+'/assign/meeting', wait_until='domcontentloaded')
    page.wait_for_selector('tbody tr:has-text("TPE.MET.NB.26.0067")', timeout=90000); page.wait_for_timeout(3000)
    cell = page.locator('tbody tr', has_text='TPE.MET.NB.26.0067').first.locator('td').last
    cell.scroll_into_view_if_needed(); settle(page,800)
    print(cell.inner_html()[:800])
    tight(page, cell.locator('[title="In biên bản"]').first, I+'btn_in_row.png')
