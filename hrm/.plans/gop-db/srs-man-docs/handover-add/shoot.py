import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"
TBL = "(() => { const vm = %s; const f = (c) => { if (c.$options.name === 'HandoverItemsTable') return c; for (const k of c.$children) { const r = f(k); if (r) return r } }; return f(vm) })()" % VM

def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)

def open_add(page):
    page.goto(BASE + '/assign/handover/add', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách cần bàn giao', timeout=120000)
    page.wait_for_function("() => %s && %s.items.length > 0" % (VM, VM), timeout=120000)
    page.wait_for_timeout(2500)

with browser_page() as page:
    open_add(page)
    # menu icons
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='Công việc').first, S + 'icon_phanhe.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 860); page.wait_for_timeout(800)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Nhiệm vụ').first
    clip(page, rail, S + 'icon_nhiemvu.png'); crop_w(S + 'icon_nhiemvu.png', 110)
    rail.click(); page.wait_for_timeout(1500)
    item = page.get_by_text('Tạo bàn giao', exact=True).last
    clip(page, item.locator('xpath=..'), S + 'icon_man.png'); crop_w(S + 'icon_man.png', 150)
    page.keyboard.press('Escape'); page.wait_for_timeout(300)
    open_add(page)
    page.screenshot(path=S + '01-tao.png')
    clip(page, page.locator('.ho-tab-btn').nth(0), S + 'icon_tab_nv.png')
    clip(page, page.locator('.ho-tab-btn').nth(1), S + 'icon_tab_vd.png')
    btns = page.locator('.footer .group-select-btn').first.locator(':scope > *')
    clip(page, btns.nth(0), S + 'icon_luunhap.png'); clip(page, btns.nth(1), S + 'icon_luuvagui.png')
    # form header fields (fill)
    # tab Vấn đề
    page.locator('.ho-tab-btn').nth(1).click(); page.wait_for_timeout(1200)
    page.screenshot(path=S + '02-tab-vande.png')
    page.locator('.ho-tab-btn').nth(0).click(); page.wait_for_timeout(1200)
    # open row receiver dropdown
    sel = page.locator('tr.ho-item-row').first.locator('.select2-selection').first
    sel.scroll_into_view_if_needed(); sel.click(); page.wait_for_timeout(1200)
    page.screenshot(path=S + '03-chon-nguoi-nhan.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(600)
    # group select
    gsel = page.locator('tr.ho-group-row').first.locator('.select2-selection').first
    clip(page, page.locator('tr.ho-group-row').first.locator('button', has_text='Gán'), S + 'icon_gan.png')
    gsel.click(); page.wait_for_timeout(1200)
    page.screenshot(path=S + '04-gan-theo-du-an.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(600)
    # bulk: tick 2 checkboxes
    page.locator('tr.ho-item-row').nth(0).locator('input[type=checkbox]').check()
    page.locator('tr.ho-item-row').nth(1).locator('input[type=checkbox]').check()
    page.wait_for_timeout(1000)
    page.screenshot(path=S + '05-gan-hang-loat.png')
    clip(page, page.locator('.ho-bulk-bar button', has_text='Gán hàng loạt'), S + 'icon_ganhangloat.png')
    page.locator('.ho-bulk-bar button', has_text='Bỏ chọn').click(); page.wait_for_timeout(600)
    # progress invalid
    inp = page.locator('tr.ho-item-row').first.locator('input.ho-progress-input')
    inp.fill('150'); page.wait_for_timeout(800)
    page.screenshot(path=S + '06-tien-do-loi.png')
    inp.fill('60'); page.wait_for_timeout(500)
    # remove button icon + note
    rm = page.locator('tr.ho-item-row').first.locator('button.btn-outline-danger')
    rm.scroll_into_view_if_needed(); page.wait_for_timeout(600)
    page.screenshot(path=S + '07-bo-khoi-ds.png')
    clip(page, rm, S + 'icon_bo.png', pad=4)
    page.evaluate("() => { const t = document.querySelector('.table-responsive'); if (t) t.scrollLeft = 0 }")
    # item detail popup
    page.locator('tr.ho-item-row').first.locator('a.text-primary').first.click(); page.wait_for_timeout(4500)
    page.screenshot(path=S + '08-chi-tiet-nhiem-vu.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1500)
    # Luu nhap without receivers -> 422
    btns.nth(0).click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '09-luu-nhap-loi.png')
    # Luu va gui -> footer confirm
    btns.nth(1).click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '10a-xac-nhan-luu-gui.png')
    page.locator('.modal.show button', has_text='Đồng ý').first.click() if page.locator('.modal.show button', has_text='Đồng ý').count() else page.locator('.modal.show .modal-body button').first.click()
    page.wait_for_timeout(2000)
    page.screenshot(path=S + '10b-gui-loi.png')
