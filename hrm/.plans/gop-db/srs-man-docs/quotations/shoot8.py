import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
exec(open('shoot_common.py').read())
def top_table(page):
    page.evaluate("() => window.scrollTo(0, document.querySelector('.products-wrap').getBoundingClientRect().top + window.scrollY - 70)"); page.wait_for_timeout(1000)
with browser_page() as page:
    goto_edit(page, 92)
    page.evaluate("""() => { const m = window.$nuxt.$route.matched; const vm = m[m.length-1].instances.default;
 ['canApplyDiscount','canEditDiscount','showOrderDiscountSection'].forEach(k => { const w = vm._computedWatchers[k]; w.getter = () => true; w.dirty = true; });
 vm.$forceUpdate(); }""")
    page.wait_for_timeout(1000)
    page.screenshot(path=S+'x-dbg8.png'); print(page.locator('select').count(), page.locator('.price-toolbar').count())
    sels = page.locator('.price-toolbar select')
    def lamtron():
        sels.nth(1).select_option('-3'); page.wait_for_timeout(500)
        page.locator('.price-toolbar').get_by_role('button', name='Áp dụng').click(); page.wait_for_timeout(1200)
        page.screenshot(path=S + '07d-lam-tron.png')
        page.locator('.modal.show').get_by_role('button').filter(has_text='Đóng').or_(page.locator('.modal.show').get_by_role('button').filter(has_text='Hủy')).first.click(); page.wait_for_timeout(800)

    def gg():
        sels.first.select_option('1'); page.wait_for_timeout(1500)
        top_table(page)
        page.evaluate("() => { const e = document.querySelector('.products-scroll'); e.scrollLeft = 900 }"); page.wait_for_timeout(800)
        page.screenshot(path=S + '09-gg-mat-hang.png')
        sels.first.select_option('2'); page.wait_for_timeout(1500)
        if page.locator('.modal.show').count():
            page.screenshot(path=S + '09c-doi-gg.png')
            page.locator('.modal.show').get_by_role('button', name='Xác nhận').click(); page.wait_for_timeout(1000)
        page.get_by_role('button', name='Thêm khoản GG').click(); page.wait_for_timeout(800)
        scroll_to(page, '.discount-total-section')
        page.evaluate("() => window.scrollBy(0, 200)"); page.wait_for_timeout(800)
        page.screenshot(path=S + '09b-gg-tong.png')
        top_table(page)
        page.evaluate("() => { const e = document.querySelector('.products-scroll'); e.scrollLeft = 900 }"); page.wait_for_timeout(800)
        page.screenshot(path=S + '09d-gg-tong-bang.png')
    T(gg, 'gg')
    def tonghop():
        scroll_to(page, '.summary-section')
        page.screenshot(path=S + '10-tong-hop.png')
    T(tonghop, 'th')
