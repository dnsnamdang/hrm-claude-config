from _mgr import *
with browser_page() as page:
    open_mgr(page, 151)
    page.screenshot(path=S + 'm151-tkt.png')
    for i, lb in enumerate(['Yêu cầu', 'Giải pháp', 'Nhiệm vụ', 'Vấn đề giải pháp', 'Meetings', 'Files', 'Hồ sơ', 'Báo giá', 'Gia hạn', 'Thu thập thông tin']):
        try:
            tab(page, lb); page.screenshot(path=S + 'm151-%02d.png' % (i + 1))
        except Exception as e: print('fail', lb, e)
    tab(page, 'Giải pháp'); page.get_by_text('Yêu cầu điều chỉnh GP').first.click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + 'm151-02b.png')
    open_mgr(page, 157)
    page.screenshot(path=S + 'm157-tkt.png')
    for i, lb in enumerate(['Dự án con', 'Báo giá', 'Meetings']):
        try:
            tab(page, lb); page.screenshot(path=S + 'm157-%02d.png' % (i + 1))
        except Exception as e: print('fail', lb, e)
    open_mgr(page, 153); tab(page, 'Thu thập thông tin'); page.screenshot(path=S + 'm153-form.png')
    open_mgr(page, 154); page.screenshot(path=S + 'm154-tkt.png')
    print('done')
