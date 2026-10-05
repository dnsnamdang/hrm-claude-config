from _sc import *
with browser_page() as page:
    go(page, '/assign/solutions'); page.wait_for_selector('text=GP40', timeout=180000); page.wait_for_timeout(2000)
    page.locator('tr', has_text='DA097_GP40').first.locator('a.v2-cell-link').first.click()
    page.wait_for_selector('text=Thông tin dự án', timeout=240000); page.wait_for_timeout(4000); idle(page)
    snap(page, '09-chi-tiet.png'); snap(page, '09-chi-tiet-full.png', full=True)
    clip(page, page.get_by_role('button', name='Sửa').last, S + 'icon_sua_footer.png')
    page.get_by_role('button', name='Sửa').last.click()
    page.wait_for_selector('text=Thông tin dự án', timeout=240000); page.wait_for_timeout(5000); idle(page)
    snap(page, '08-sua.png')
