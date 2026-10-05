import sys, re; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"
def goto_list(page):
    page.goto(BASE + '/assign/issues', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách Vấn đề', timeout=90000)
    page.wait_for_timeout(6000)
def row(page, code):
    return page.locator('tr', has=page.get_by_text(code, exact=True)).first
def close_modal(page):
    page.locator('.modal.show .modal-footer').last.get_by_role('button', name=re.compile('Đóng')).click()
    page.wait_for_timeout(1500)
def modal_shots(page, prefix):
    page.wait_for_timeout(4500)
    page.screenshot(path=S + prefix + '-a.png')
    page.evaluate("() => { const b=[...document.querySelectorAll('.modal.show .modal-body')].pop(); if(b) b.scrollTop = 99999 }")
    page.wait_for_timeout(1200)
    page.screenshot(path=S + prefix + '-b.png')
    page.evaluate("() => { const b=[...document.querySelectorAll('.modal.show .modal-body')].pop(); if(b) b.scrollTop = 0 }")

with browser_page() as page:
    goto_list(page)
    # scroll table right
    page.evaluate("""() => { [...document.querySelectorAll('*')].filter(e => e.scrollWidth > e.clientWidth + 50 && getComputedStyle(e).overflowX !== 'visible' && e.closest('.v2-styles')).forEach(e => e.scrollLeft = 99999) }""")
    page.wait_for_timeout(1200)
    page.screenshot(path=S + '01b-ds-phai.png')
    r = row(page, 'ISS-202610-0003')
    acts = r.locator('.v2-row-actions')
    clip(page, acts, S + 'icon_rowacts_new.png', pad=4)
    clip(page, acts.locator('[title="Sửa"]').first, S + 'icon_sua.png', pad=3)
    clip(page, acts.locator('[title="Xóa"]').first, S + 'icon_xoa.png', pad=3)
    r5 = row(page, 'ISS-202610-0005').locator('.v2-row-actions')
    clip(page, r5.locator('[title="Xử lý"]').first, S + 'icon_xuly.png', pad=3)
    clip(page, r5.locator('[title="Lịch sử"]').first, S + 'icon_lichsu.png', pad=3)
    # Ma link
    clip(page, row(page, 'ISS-202610-0004').get_by_text('ISS-202610-0004', exact=True), S + 'icon_ma.png', pad=3)
    # ---- Tao moi
    page.get_by_role('button', name='Tạo Vấn đề').click()
    modal_shots(page, '05-tao')
    page.locator('.modal.show').get_by_role('button', name=re.compile('Lưu thông tin')).click(); page.wait_for_timeout(1500)
    # clear title -> error (title empty by default) -> description empty
    page.screenshot(path=S + '05-tao-loi.png')
    close_modal(page)
    # ---- Chi tiet (0004 assigned)
    row(page, 'ISS-202610-0004').get_by_text('ISS-202610-0004', exact=True).click()
    modal_shots(page, '06-chitiet')
    close_modal(page)
    # ---- Sua (0003 new)
    r = row(page, 'ISS-202610-0003').locator('.v2-row-actions')
    r.locator('[title="Sửa"]').first.click()
    modal_shots(page, '07-sua')
    close_modal(page)
    # ---- Xoa
    r = row(page, 'ISS-202610-0003').locator('.v2-row-actions')
    r.locator('[title="Xóa"]').first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '11-xoa.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    # ---- Lich su popup (0006)
    r6 = row(page, 'ISS-202610-0006').locator('.v2-row-actions')
    r6.locator('[title="Lịch sử"]').first.click(); page.wait_for_timeout(3500)
    page.screenshot(path=S + '13-lichsu.png')
    close_modal(page); page.wait_for_timeout(1000)
