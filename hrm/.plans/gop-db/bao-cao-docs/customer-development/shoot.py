import sys, re; sys.path.insert(0, '..')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
URL = BASE + '/assign/report/customer-development'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"

def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)

def set_month(page):
    page.evaluate("() => { const vm = %s; Object.assign(vm.filterDraft, {time_mode:'month', year:2026, month:7}); }" % VM)
    page.wait_for_timeout(6000)

with browser_page() as page:
    page.goto(URL, wait_until='domcontentloaded'); page.wait_for_timeout(8000)
    page.goto(URL, wait_until='domcontentloaded'); page.wait_for_timeout(8000)
    page.screenshot(path=S + '00-mac-dinh.png')
    set_month(page)
    page.screenshot(path=S + '02-loc.png')
    clip(page, page.get_by_role('button', name='Ẩn tìm kiếm nâng cao'), S + 'icon_antimkiem.png')
    clip(page, page.locator('button:visible').filter(has_text=re.compile(r'^\s*Tìm kiếm\s*$')).first, S + 'icon_btn_timkiem.png')
    clip(page, page.locator('button:visible').filter(has_text=re.compile(r'^\s*Làm mới\s*$')).first, S + 'icon_lammoi.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '03-cai-dat.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    page.evaluate("() => { %s.filterCollapsed = true }" % VM); page.wait_for_timeout(1500)
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    page.screenshot(path=S + '01-xem.png')
    clip(page, page.get_by_role('button', name='Xem chi tiết'), S + 'icon_xemchitiet.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.get_by_role('button', name='In báo cáo'), S + 'icon_in.png')
    page.get_by_role('button', name='Xem chi tiết').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '04-chi-tiet.png')
    page.screenshot(path=S + '04-chi-tiet-full.png', full_page=True)
    clip(page, page.get_by_role('button', name='Chỉ xem cấp gốc'), S + 'icon_capgoc.png')
    # drill-down: employee row care total
    page.evaluate("() => { const w = document.querySelector('.table-wrapper'); w.scrollLeft = w.scrollWidth }"); page.wait_for_timeout(800)
    page.screenshot(path=S + '04b-chi-tiet-cuon.png')
    emp = page.locator('tr.row-emp').filter(has=page.locator('td:nth-child(9) .link-cell')).first
    cell = emp.locator('td').nth(8).locator('span')
    clip(page, cell, S + 'icon_so.png', pad=6)
    cell.click(); page.wait_for_timeout(4000)
    page.screenshot(path=S + '05-ds-kh.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    # export
    with page.expect_download(timeout=90000) as dl:
        page.get_by_role('button', name='Xuất Excel').click()
        page.wait_for_timeout(3000)
        page.screenshot(path=S + '06-xuat.png')
    dl.value.save_as(S + 'export.xls')
    with page.context.expect_page() as pg:
        page.get_by_role('button', name='In báo cáo').click()
    p2 = pg.value
    p2.set_viewport_size({'width': 1440, 'height': 900})
    p2.wait_for_timeout(9000)
    p2.screenshot(path=S + '07-in.png')
