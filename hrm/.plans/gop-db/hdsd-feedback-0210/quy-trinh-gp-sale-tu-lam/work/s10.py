from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/solutions'); wait_idle(page)
    page.locator('input[placeholder^="Tìm theo mã giải pháp"]').fill('CTV_NV.UD.0101.2026.DA001')
    page.locator('button.v2-btn--primary:has-text("Tìm kiếm")').click(); wait_idle(page)
    row=page.locator('tbody tr').first
    print(row.locator('.v2-row-actions').inner_html()[:1500])
    row.locator('.v2-row-actions').scroll_into_view_if_needed(); settle(page)
    page.screenshot(path=SH+'05_sol_list.png')
    tight(page, row.locator('span[title="Quản lý giải pháp"] a'), IC+'btn_quanlygp_row.png')
    page.goto(BASE+'/assign/solutions/956/manager'); wait_idle(page, 5000); settle(page)
    page.screenshot(path='solmgr.png')
