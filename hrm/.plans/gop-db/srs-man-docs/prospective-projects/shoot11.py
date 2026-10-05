from _mgr import *
def T(f):
    try: f()
    except Exception as e: print('FAIL', f.__name__, str(e)[:200])
NOLOAD = "() => !/Đang tải/.test(document.body.innerText)"
with browser_page() as page:
    def d153():
        open_mgr(page, 153); tab(page, 'Thu thập thông tin', 3000)
        page.wait_for_function(NOLOAD, timeout=180000); page.wait_for_timeout(1500)
        page.screenshot(path=S + '26-thu-thap.png')
        page.locator('button').filter(has_text='Lịch sử thay đổi').first.click(); page.wait_for_timeout(2000)
        page.wait_for_function("() => !document.querySelector('.modal.show .spinner-border, .modal.show .ri-loader-4-line')", timeout=120000)
        page.wait_for_timeout(2500)
        page.screenshot(path=S + '27-ls-phieu.png')
    T(d153)
    def d150():
        open_mgr(page, 150)
        page.locator('button').filter(has_text='Chốt giải pháp').last.click(); page.wait_for_timeout(2000)
        page.wait_for_function(NOLOAD, timeout=180000); page.wait_for_timeout(1500)
        page.screenshot(path=S + '29-chot-gp.png')
    T(d150)
    print('done11')
