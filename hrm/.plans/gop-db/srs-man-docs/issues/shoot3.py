import sys, re; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
def goto_list(page):
    page.goto(BASE + '/assign/issues', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách Vấn đề', timeout=90000)
    page.wait_for_timeout(6000)
def row(page, code):
    return page.locator('tr', has=page.get_by_text(code, exact=True)).first
def close_modal(page):
    page.locator('.modal.show .modal-footer').last.get_by_role('button', name=re.compile('Đóng')).click()
    page.wait_for_timeout(1500)
def status_picker(page):
    return page.locator('.modal.show .form-group', has_text='Trạng thái Vấn đề').locator('.sp-input').first
def open_handle(page, code, shot, pick=None):
    row(page, code).locator('.v2-row-actions [title="Xử lý"]').first.click()
    page.wait_for_timeout(5000)
    status_picker(page).click(); page.wait_for_timeout(1200)
    page.screenshot(path=S + shot + '.png')
    if pick:
        page.locator('.modal.show').get_by_text(pick, exact=True).last.click(); page.wait_for_timeout(1200)
        page.screenshot(path=S + shot + '-chon.png')
    else:
        page.locator('.modal.show h5').first.click(); page.wait_for_timeout(500)
    close_modal(page)

with browser_page() as page:
    goto_list(page)
    open_handle(page, 'ISS-202610-0005', '08-xuly')
    open_handle(page, 'ISS-202610-0006', '09-duyet', pick='Từ chối')
    open_handle(page, 'ISS-202610-0007', '10-molai')
    # detail with comment + history section
    row(page, 'ISS-202610-0004').get_by_text('ISS-202610-0004', exact=True).click(); page.wait_for_timeout(5000)
    page.evaluate("() => { const b=[...document.querySelectorAll('.modal.show .modal-body')].pop(); b.scrollTop = 99999 }")
    page.wait_for_timeout(1500)
    page.screenshot(path=S + '12-binhluan.png')
    clip(page, page.locator('.modal.show').get_by_role('button', name=re.compile('Gửi')).first, S + 'icon_gui.png')
    page.locator('.modal.show').get_by_role('button', name=re.compile('Xem lịch sử')).click(); page.wait_for_timeout(3500)
    page.evaluate("() => { const b=[...document.querySelectorAll('.modal.show .modal-body')].pop(); b.scrollTop = 99999 }")
    page.wait_for_timeout(1000)
    page.screenshot(path=S + '13b-lichsu-chitiet.png')
    close_modal(page)
