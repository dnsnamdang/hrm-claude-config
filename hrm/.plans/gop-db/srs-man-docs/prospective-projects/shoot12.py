from _mgr import *
NOLOAD = "() => !/Đang t/.test(document.querySelector('.tp-tab-shell:not([style*=\"none\"])').innerText)"
with browser_page() as page:
    open_mgr(page, 157)
    for lb, f in [('Dự án con', 'm157-01.png'), ('Báo giá', 'm157-02.png'), ('Meetings', 'm157-03.png')]:
        tab(page, lb, 3000)
        try: page.wait_for_function("() => !/Đang tải/.test(document.body.innerText)", timeout=180000)
        except Exception as e: print('w', lb, e)
        page.wait_for_timeout(2000); page.screenshot(path=S + f)
    print('done12')
