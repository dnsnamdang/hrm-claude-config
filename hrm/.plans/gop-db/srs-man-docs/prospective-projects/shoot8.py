from _form import *
from _mgr import open_mgr, tab
def go(page, q=''):
    page.goto(BASE + '/assign/prospective-projects/add' + q, wait_until='domcontentloaded')
    page.wait_for_selector('text=Thông tin khách hàng', timeout=240000); page.wait_for_timeout(5000)
with browser_page(height=1100) as page:
    go(page)
    page.get_by_placeholder('Nhấn vào đây để chọn thông tin khách hàng').first.click(); page.wait_for_timeout(4000)
    page.get_by_placeholder('Nhập tên / mã khách hàng').fill('29TPHXHO-1'); page.keyboard.press('Enter')
    page.wait_for_selector('#choose-erp-customer tbody tr:has-text("29TPHXHO-1")', timeout=120000); page.wait_for_timeout(1000)
    page.locator('#choose-erp-customer tbody tr', has_text='29TPHXHO-1').first.click(); page.wait_for_timeout(10000)
    try:
        for i in range(3):
            f = field(page, 'Ứng dụng'); f.locator('.select2-selection').first.click(); page.wait_for_timeout(2500)
            opts = page.locator('.select2-container--open .select2-results__option')
            if opts.count() and 'No results' not in opts.first.inner_text() :
                opts.first.click(); break
            page.keyboard.press('Escape'); page.wait_for_timeout(4000)
        page.wait_for_timeout(2500)
        page.get_by_role('button', name='Xem giải pháp').click(); page.wait_for_timeout(3000)
        page.wait_for_function("!document.body.innerText.includes('Đang tải dữ liệu')", timeout=180000)
        page.wait_for_timeout(1500)
        page.screenshot(path=S + '09-ds-giai-phap.png')
    except Exception as e: print('app', e)
with browser_page() as page:
    open_mgr(page, 153); tab(page, 'Yêu cầu', 6000); page.screenshot(path=S + 'm153-yeucau.png')
    open_mgr(page, 144); tab(page, 'Báo giá', 3000)
    try: page.wait_for_function("!document.querySelector('.tp-tab-shell').innerText.includes('Đang tải')", timeout=120000)
    except Exception as e: print(e)
    page.wait_for_timeout(1500)
    page.screenshot(path=S + 'm144-baogia.png')
    print('done8')
