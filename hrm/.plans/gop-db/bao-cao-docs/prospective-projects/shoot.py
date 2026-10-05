import sys, re; sys.path.insert(0, '..')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"

def set_month(page):
    page.evaluate("async () => { const vm = %s; vm.filterDraft = Object.assign({}, vm.filterDraft, {timeMode:'month', year:'2026', month:'7'}); await vm.applyFilters(); }" % VM)
    page.wait_for_timeout(4000)

def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)

with browser_page() as page:
    page.goto(BASE + '/assign/report/prospective-projects', wait_until='domcontentloaded')
    page.wait_for_timeout(8000)
    # --- icons menu
    page.mouse.click(1160, 30); page.wait_for_timeout(1200)
    clip(page, page.locator('.switcher-item', has_text='CSKH trước bán').first, S + 'icon_phanhe.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 600); page.wait_for_timeout(600)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Báo cáo').first
    clip(page, rail, S + 'icon_baocao.png'); crop_w(S + 'icon_baocao.png', 110)
    rail.click(); page.wait_for_timeout(1200)
    grp = page.get_by_text('Báo cáo dự án tiền khả thi', exact=False).first
    page.screenshot(path=S + '_flyout.png')
    clip(page, grp.locator('xpath=ancestor-or-self::*[self::a or self::button or self::div][1]'), S + 'icon_nhom.png')
    item = page.get_by_text('Báo cáo vòng đời dự án TKT', exact=True).last
    clip(page, item.locator('xpath=..'), S + 'icon_man.png')
    page.goto(BASE + '/assign/report/prospective-projects', wait_until='domcontentloaded')
    page.wait_for_timeout(8000)
    set_month(page)
    page.screenshot(path=S + '01-xem.png')
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    clip(page, page.get_by_role('button', name='Chỉ xem cấp gốc'), S + 'icon_capgoc.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.get_by_role('button', name='In báo cáo'), S + 'icon_in.png')
    # full page incl. pagination
    page.screenshot(path=S + '01-xem-full.png', full_page=True)
    # --- filter open
    page.evaluate("() => { %s.filterCollapsed = false }" % VM); page.wait_for_timeout(2500)
    page.screenshot(path=S + '02-loc.png')
    clip(page, page.locator('button:visible').filter(has_text=re.compile(r'^\s*Tìm kiếm\s*$')).first, S + 'icon_btn_timkiem.png')
    clip(page, page.locator('button:visible').filter(has_text=re.compile(r'^\s*Làm mới\s*$')).first, S + 'icon_lammoi.png')
    page.evaluate("() => { %s.filterCollapsed = true }" % VM); page.wait_for_timeout(1500)
    # --- settings
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '03-cai-dat.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    # --- root only
    page.get_by_role('button', name='Chỉ xem cấp gốc').click(); page.wait_for_timeout(1200)
    page.screenshot(path=S + '04-cap-goc.png')
    clip(page, page.get_by_role('button', name='Xem chi tiết'), S + 'icon_xemchitiet.png')
    page.get_by_role('button', name='Xem chi tiết').click(); page.wait_for_timeout(1200)
    # --- summary modal (company row status)
    rows = page.locator('tr.row-company')
    clip(page, rows.first.get_by_role('button', name='Cơ cấu tiến trình'), S + 'icon_cocau.png')
    rows.first.get_by_role('button', name='Cơ cấu tiến trình').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '05-co-cau.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    rows.first.get_by_role('button', name='Cơ cấu giai đoạn').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '05b-giai-doan.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    # --- list modal: dept row total projects
    dept = page.locator('tr.row-dept').first
    btn = dept.locator('td').nth(2).locator('button')
    clip(page, btn, S + 'icon_soluong.png')
    btn.click(); page.wait_for_timeout(3500)
    page.screenshot(path=S + '06-ds-du-an.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    # --- export
    with page.expect_download(timeout=60000) as dl:
        page.get_by_role('button', name='Xuất Excel').click()
        page.wait_for_timeout(2500)
        page.screenshot(path=S + '07-xuat.png')
    dl.value.save_as(S + 'export.xls')
    # --- print
    with page.context.expect_page() as pg:
        page.get_by_role('button', name='In báo cáo').click()
    p2 = pg.value
    p2.set_viewport_size({'width': 1440, 'height': 900})
    p2.wait_for_timeout(8000)
    p2.screenshot(path=S + '08-in.png')
