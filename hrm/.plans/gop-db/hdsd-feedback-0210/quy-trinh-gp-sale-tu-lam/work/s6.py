from common import *
def s2pick(page, sel_container, text):
    sel_container.click(); page.wait_for_timeout(700)
    srch=page.locator('.select2-container--open .select2-search__field')
    if srch.count() and srch.first.is_visible():
        srch.first.fill(text); page.wait_for_timeout(1500)
    page.locator('.select2-container--open .select2-results__option', has_text=text).first.click(); page.wait_for_timeout(700)
with browser_page() as page:
    page.goto(BASE+'/assign/solutions/add?prospective_project_id=151'); page.wait_for_timeout(15000)
    page.locator('input[placeholder="VD: GP dây chuyền sơn xưởng ô tô tiêu chuẩn"]').fill('Giải pháp cầu nâng 2 trụ và khí nén cho xưởng dịch vụ Ô tô Thành An')
    dp=page.locator('input[placeholder="Chọn ngày..."]').first
    dp.click(); dp.fill('20/10/2026'); page.keyboard.press('Enter'); page.wait_for_timeout(500)
    page.mouse.click(700,160); page.wait_for_timeout(300)
    s=page.locator('label:has-text("Nhóm ngành")').first.locator('xpath=following::span[contains(@class,"select2-selection")][1]')
    s.click(); page.wait_for_timeout(800)
    opts=page.locator('.select2-container--open .select2-results__option').all_inner_texts(); print('scope',opts[:10])
    page.locator('.select2-container--open .select2-results__option').first.click(); page.wait_for_timeout(800)
    s=page.locator('label:has-text("Nhóm giải pháp")').first.locator('xpath=following::span[contains(@class,"select2-selection")][1]')
    s.click(); page.wait_for_timeout(800)
    opts=page.locator('.select2-container--open .select2-results__option').all_inner_texts(); print('ind',opts[:15])
    page.keyboard.press('Escape')
    page.screenshot(path='sol_fill1.png', full_page=True)
