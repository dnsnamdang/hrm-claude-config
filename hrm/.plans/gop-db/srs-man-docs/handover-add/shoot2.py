import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"
FIND = "const f = (c, n) => { if (c.$options.name === n) return c; for (const k of c.$children) { const r = f(k, n); if (r) return r } };"
with browser_page() as page:
    page.goto(BASE + '/assign/handover/add', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách cần bàn giao', timeout=120000)
    page.wait_for_function("() => %s && %s.items.length > 0" % (VM, VM), timeout=120000)
    page.wait_for_timeout(2500)
    page.evaluate("""() => { %s const vm = %s; const form = f(vm, 'HandoverForm'); const tbl = f(vm, 'HandoverItemsTable');
        form.form.handover_date = '2026-10-15'; form.form.reason = 2; form.form.note = 'Bàn giao trước khi chuyển sang phòng Kinh doanh 2'; form.emitChange();
        vm.items.filter(it => !tbl.getItemSelectOptions(it).length).forEach(it => vm.removeItem(it)); vm.items.forEach(it => { const o = tbl.getItemSelectOptions(it); if (o.length) it.receiver_id = o[0].value; });
    }""" % (FIND, VM))
    page.wait_for_timeout(1500)
    page.screenshot(path=S + '11a-da-nhap.png')
    btns = page.locator('.footer .group-select-btn').first.locator(':scope > *')
    btns.nth(1).click(); page.wait_for_timeout(1500)
    page.locator('.modal.show button', has_text='Xác nhận').first.click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '11-gui-duyet-xac-nhan.png')
    
