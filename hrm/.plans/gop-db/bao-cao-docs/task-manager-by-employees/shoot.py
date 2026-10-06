import sys; sys.path.insert(0, '..')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"

def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)

def wait_loaded(page, extra=1500):
    page.wait_for_timeout(800)
    page.wait_for_function("() => !document.body.innerText.includes('Đang tải dữ liệu')", timeout=180000)
    page.wait_for_timeout(extra)

with browser_page() as page:
    page.goto(BASE + '/assign/report/task-manager-by-employees', wait_until='domcontentloaded')
    page.wait_for_selector('text=Bộ lọc phân bổ nguồn lực (Gantt)', timeout=90000)
    wait_loaded(page, 3000)
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='Công việc').first, S + 'icon_phanhe.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 700); page.wait_for_timeout(800)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Báo cáo').first
    clip(page, rail, S + 'icon_baocao.png'); crop_w(S + 'icon_baocao.png', 110)
    rail.click(); page.wait_for_timeout(1500)
    item = page.get_by_text('Phân bổ nguồn lực theo nhân viên', exact=True).last
    clip(page, item.locator('xpath=..'), S + 'icon_man.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(300)
    page.mouse.click(800, 860); page.wait_for_timeout(1000)
    page.screenshot(path=S + '01-xem.png')
    page.screenshot(path=S + '01-xem-full.png', full_page=True)
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.get_by_role('button', name='In báo cáo'), S + 'icon_in.png')
    clip(page, page.get_by_role('button', name='Ẩn lịch Gantt'), S + 'icon_angantt.png')
    # --- filter
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '02-loc.png')
    page.get_by_text('Chỉ hiển thị nhân viên có nhiệm vụ trong kỳ').first.click(); page.wait_for_timeout(500)
    page.locator('.smart-filter-actions button').first.click()
    wait_loaded(page, 2500)
    page.screenshot(path=S + '02b-loc-co-nhiem-vu.png')
    page.evaluate("() => { %s.filters.time_mode = 'custom' }" % VM); page.wait_for_timeout(1500)
    page.screenshot(path=S + '02c-loc-tuy-chon.png')
    page.evaluate("() => { const vm = %s; vm.filters.time_mode = 'month'; vm.filterCollapsed = true; vm.handleSearch() }" % VM)
    wait_loaded(page, 2500)
    page.screenshot(path=S + '03-gantt.png')
    # --- settings
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '04-cai-dat.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # --- detail modal by employee (Vu Quang Minh)
    row = page.locator('tr.row-emp', has_text='Vũ Quang Minh').first
    btn = row.locator('button.metric-link-btn').first
    clip(page, btn, S + 'icon_nhiemvu.png', pad=6)
    btn.click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '05-chi-tiet-nv.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    bar = row.locator('.gantt-bar').first
    clip(page, bar, S + 'icon_thanhgantt.png', pad=4)
    bar.click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '06-chi-tiet-du-an.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # --- collapse dept
    page.locator('tr.row-dept').first.click(); page.wait_for_timeout(800)
    page.screenshot(path=S + '07-thu-gon.png')
    clip(page, page.locator('tr.row-dept').first.locator('td').first, S + 'icon_thugon.png', pad=2)
    page.locator('tr.row-dept').first.click(); page.wait_for_timeout(800)
    # --- hide gantt
    page.get_by_role('button', name='Ẩn lịch Gantt').click(); page.wait_for_timeout(1200)
    page.screenshot(path=S + '08-an-gantt.png')
    clip(page, page.get_by_role('button', name='Xem lịch Gantt'), S + 'icon_xemgantt.png')
    page.get_by_role('button', name='Xem lịch Gantt').click(); page.wait_for_timeout(1200)
    # --- export
    with page.expect_download(timeout=180000) as dl:
        page.get_by_role('button', name='Xuất Excel').click()
    dl.value.save_as(S + 'export.xls')
    page.wait_for_timeout(600)
    page.screenshot(path=S + '09-xuat.png')
    # --- print
    with page.context.expect_page() as pg:
        page.get_by_role('button', name='In báo cáo').click()
    p2 = pg.value
    p2.set_viewport_size({'width': 1440, 'height': 900})
    p2.wait_for_timeout(15000)
    p2.screenshot(path=S + '10-in.png')
    clip(p2, p2.locator('button.btn-primary').first, S + 'icon_nutin.png')
