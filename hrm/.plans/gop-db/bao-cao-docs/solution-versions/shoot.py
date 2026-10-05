import sys; sys.path.insert(0, '..')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"

def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)

def wait_loaded(page, extra=1500):
    page.wait_for_timeout(800)
    page.wait_for_function("() => !document.body.innerText.includes('Đang tải dữ liệu')", timeout=120000)
    page.wait_for_timeout(extra)

with browser_page() as page:
    page.goto(BASE + '/assign/report/solution-versions', wait_until='domcontentloaded')
    page.wait_for_selector('text=Bộ lọc theo dõi version giải pháp', timeout=90000)
    wait_loaded(page, 3000)
    # --- icons menu
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='Công việc').first, S + 'icon_phanhe.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 700); page.wait_for_timeout(800)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Báo cáo').first
    clip(page, rail, S + 'icon_baocao.png'); crop_w(S + 'icon_baocao.png', 110)
    rail.click(); page.wait_for_timeout(1500)
    item = page.get_by_text('Theo dõi chỉ số hoàn thành GP theo version', exact=True).last
    clip(page, item.locator('xpath=..'), S + 'icon_man.png')
    page.screenshot(path=S + '00-menu.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(300)
    page.mouse.click(800, 820); page.wait_for_timeout(1000)
    page.screenshot(path=S + '01-xem.png')
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    clip(page, page.get_by_role('button', name='Xem chi tiết'), S + 'icon_xemchitiet.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.get_by_role('button', name='In báo cáo'), S + 'icon_in.png')
    # --- filter open
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(2500)
    if page.get_by_role('button', name='Ẩn tìm kiếm nâng cao').count() == 0:
        page.evaluate("() => { %s.filterCollapsed = false }" % VM); page.wait_for_timeout(2500)
    page.screenshot(path=S + '02-loc.png')
    # custom range
    page.evaluate("async () => { const vm = %s; vm.filterDraft = Object.assign({}, vm.filterDraft, {time_mode:'custom', month: undefined, year: undefined, from_date:'2026-09-01', to_date:'2026-10-31'}); await vm.applyFilters(); }" % VM)
    wait_loaded(page, 2000)
    page.screenshot(path=S + '02b-loc-tuy-chinh.png')
    page.evaluate("() => { %s.filterCollapsed = true }" % VM); page.wait_for_timeout(1500)
    # --- settings
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '03-cai-dat.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # --- expand
    page.get_by_role('button', name='Xem chi tiết').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '04-chi-tiet.png')
    clip(page, page.get_by_role('button', name='Chỉ xem cấp gốc'), S + 'icon_capgoc.png')
    page.evaluate("() => { const w = document.querySelector('.table-wrapper'); w.scrollLeft = 2000; w.dispatchEvent(new Event('scroll')); }")
    page.wait_for_timeout(800)
    page.screenshot(path=S + '04b-chi-tiet-phai.png')
    page.evaluate("() => { const w = document.querySelector('.table-wrapper'); w.scrollLeft = 520; w.dispatchEvent(new Event('scroll')); }")
    page.wait_for_timeout(800)
    # --- drill: modules on first version row
    ver = page.locator('tr.row-version').first
    links = ver.locator('.link-cell')
    clip(page, links.nth(0), S + 'icon_hangmuc.png', pad=6)
    clip(page, links.nth(1), S + 'icon_nhansu.png', pad=6)
    page.screenshot(path=S + '04c-chi-tiet-giua.png')
    links.nth(0).click(); page.wait_for_timeout(4000)
    page.screenshot(path=S + '05-hang-muc.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    links.nth(1).click(); page.wait_for_timeout(4000)
    page.screenshot(path=S + '06-nhan-su.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # --- collapse via toggle and screenshot single company toggles
    # --- export
    with page.expect_download(timeout=120000) as dl:
        page.get_by_role('button', name='Xuất Excel').click()
    dl.value.save_as(S + 'export.xls')
    page.wait_for_timeout(600)
    page.screenshot(path=S + '07-xuat.png')
    # --- print
    with page.context.expect_page() as pg:
        page.get_by_role('button', name='In báo cáo').click()
    p2 = pg.value
    p2.set_viewport_size({'width': 1440, 'height': 900})
    p2.wait_for_timeout(15000)
    p2.screenshot(path=S + '08-in.png')
    clip(p2, p2.locator('button.btn-primary').first, S + 'icon_nutin.png')
