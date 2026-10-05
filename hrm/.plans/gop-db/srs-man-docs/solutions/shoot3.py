from _sc import *
with browser_page() as page:
    go(page, '/assign/solutions'); page.wait_for_selector('text=GP40', timeout=180000); page.wait_for_timeout(2000)
    snap(page, '07-danh-sach-nhap.png')
    row = page.locator('tr', has_text='DA097_GP40').first
    clip(page, row.locator('a.v2-cell-link').first, S + 'icon_ma.png')
    page.evaluate("x => document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = x)", 6000); page.wait_for_timeout(800)
    clip(page, row.locator('span[title="Sửa"]').first, S + 'icon_sua.png')
    clip(page, row.locator('span[title="Xóa"]').first, S + 'icon_xoa.png')
    r2 = page.locator('tr', has_text='DA090_GP01').first
    clip(page, r2.locator('span[title="Quản lý giải pháp"]').first, S + 'icon_quanly.png')
    row.locator('span[title="Xóa"] button').first.click(); page.wait_for_timeout(1500)
    snap(page, '10-xoa.png')
    page.locator('.modal.show').get_by_role('button', name='Hủy').click(); page.wait_for_timeout(1000)
    go(page, '/assign/solutions/957'); page.wait_for_timeout(2000); idle(page)
    snap(page, '09-chi-tiet.png')
    snap(page, '09-chi-tiet-full.png', full=True)
    go(page, '/assign/solutions/957/edit'); page.wait_for_timeout(2000); idle(page)
    snap(page, '08-sua.png')
