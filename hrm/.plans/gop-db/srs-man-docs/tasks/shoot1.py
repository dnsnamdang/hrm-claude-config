import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
VM = "(() => { const m = window.$nuxt.$route.matched; return m[m.length-1].instances.default })()"
def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)
def goto_list(page):
    page.goto(BASE + '/assign/tasks', wait_until='domcontentloaded')
    page.wait_for_selector('text=TPE.TASK.NB.26.0986', timeout=180000)
    page.wait_for_timeout(2500)
def scroll_table(page, x):
    page.evaluate("x => document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = x)", x)
    page.wait_for_timeout(600)
with browser_page() as page:
    goto_list(page)
    page.screenshot(path=S + '01-danh-sach.png')
    scroll_table(page, 2000); page.screenshot(path=S + '01b-danh-sach-phai.png')
    scroll_table(page, 1500); page.screenshot(path=S + '01c-danh-sach-giua.png')
    row = page.locator('tr', has_text='TPE.TASK.NB.26.0977').first
    scroll_table(page, 5000)
    clip(page, row.locator('span[title="Sửa"]').first, S + 'icon_sua.png')
    clip(page, row.locator('span[title="Xóa"]').first, S + 'icon_xoa.png')
    clip(page, row.locator('span[title="Lịch sử"]').first, S + 'icon_lichsu.png')
    r8 = page.locator('tr', has_text='TPE.TASK.NB.26.0978').first
    clip(page, r8.locator('span[title="Nhập kết quả"]').first, S + 'icon_nhapkq.png')
    r9 = page.locator('tr', has_text='TPE.TASK.NB.26.0979').first
    clip(page, r9.locator('span[title="Duyệt"]').first, S + 'icon_duyet.png')
    scroll_table(page, 0)
    clip(page, row.locator('button.v2-cell-link').first, S + 'icon_ma.png')
    clip(page, page.get_by_role('button', name='Tạo mới'), S + 'icon_taomoi.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.locator('button[title="Cấu hình cột hiển thị"]'), S + 'icon_cot.png')
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    clip(page, page.locator('.scope-icons').first, S + 'icon_locnhanh.png')
    # menu icons
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='Công việc').first, S + 'icon_phanhe_cv.png')
    clip(page, page.locator('.switcher-item', has_text='CSKH trước bán').first, S + 'icon_phanhe_presale.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 700); page.wait_for_timeout(800)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Nhiệm vụ').first
    clip(page, rail, S + 'icon_nhom_nhiemvu.png'); crop_w(S + 'icon_nhom_nhiemvu.png', 120)
    rail.click(); page.wait_for_timeout(1500)
    it = page.get_by_text('Nhiệm vụ', exact=True).nth(2)
    try:
        clip(page, page.locator('a[href="/assign/tasks"]').last, S + 'icon_man_nhiemvu.png')
    except Exception as e:
        print('item clip fail', e)
    page.screenshot(path=S + 'x-flyout.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(500)
    # quick scope: Task toi lam
    goto_list(page)
    page.locator('button.scope-icon-btn[title="Task tôi làm"]').click()
    page.wait_for_timeout(4000)
    page.screenshot(path=S + '02b-loc-nhanh.png')
    page.locator('button.scope-icon-btn[title="Task tôi làm"]').click(); page.wait_for_timeout(3000)
    # advanced filter
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '02-loc.png')
    page.screenshot(path=S + '02-loc-full.png', full_page=True)
    # settings
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '03-cai-dat-loc.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # columns
    page.locator('button[title="Cấu hình cột hiển thị"]').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '04-tuy-chinh-cot.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1200)
    # export popup
    page.get_by_role('button', name='Xuất Excel').click(); page.wait_for_timeout(1800)
    page.screenshot(path=S + '14-xuat.png')
    with page.expect_download(timeout=180000) as dl:
        page.get_by_role('button', name='Xuất file').click()
    dl.value.save_as(S + 'export.xlsx')
    page.wait_for_timeout(1500)
    # presale entry
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    page.locator('.switcher-item', has_text='CSKH trước bán').first.click(); page.wait_for_timeout(5000)
    page.screenshot(path=S + 'x-presale.png')
    try:
        clip(page, page.locator('.left-side-menu a', has_text='Nhiệm vụ').first, S + 'icon_presale_nhiemvu.png')
        crop_w(S + 'icon_presale_nhiemvu.png', 130)
    except Exception as e:
        print('presale clip fail', e)
