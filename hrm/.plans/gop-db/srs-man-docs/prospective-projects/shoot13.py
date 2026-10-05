from _mgr import *
W = "() => !/Đang tải/.test(document.body.innerText)"
with browser_page() as page:
    open_mgr(page, 151)
    page.wait_for_function(W, timeout=180000); page.wait_for_timeout(1500)
    page.screenshot(path=S + 'm151-tkt.png')
    tab(page, 'Giải pháp'); page.wait_for_function(W, timeout=180000); page.wait_for_timeout(1500)
    page.screenshot(path=S + 'm151-02.png')
    page.locator('.tp-tab-shell').get_by_text('Yêu cầu điều chỉnh GP').first.click(); page.wait_for_timeout(2000)
    page.wait_for_function(W, timeout=180000); page.wait_for_timeout(1500)
    page.screenshot(path=S + '14-yc-dieu-chinh.png')
    open_mgr(page, 157); tab(page, 'Meetings'); page.wait_for_function(W, timeout=180000); page.wait_for_timeout(1500)
    page.screenshot(path=S + 'm157-03.png')
    print('done13')
