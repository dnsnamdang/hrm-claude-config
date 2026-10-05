from _sc import *
with browser_page() as page:
    go(page, '/assign/request-solution'); page.wait_for_timeout(3000)
    page.screenshot(path=S+'x-rs.png')
    for lab,nm in [('Yêu cầu giải pháp','man_ycgp'),('Dự án TKT','man_duan')]:
        try:
            clip(page, page.locator('.left-side-menu a', has_text=lab).first, S+'icon_%s.png'%nm); crop_w(S+'icon_%s.png'%nm, 190)
        except Exception as e: print('fail',lab,e)
