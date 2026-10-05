import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from PIL import Image
S = 'shots/'
def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)
def goto_list(page):
    page.goto(BASE + '/assign/bom-list', wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách BOM List', timeout=90000)
    page.wait_for_function("() => !document.querySelector('.v2-data-table .spinner-border')", timeout=90000)
    page.wait_for_timeout(3000)
with browser_page() as page:
    goto_list(page)
    # icons menu
    page.mouse.click(1160, 30); page.wait_for_timeout(1500)
    clip(page, page.locator('.switcher-item', has_text='Công việc').first, S + 'icon_phanhe.png')
    page.keyboard.press('Escape'); page.mouse.click(700, 870); page.wait_for_timeout(800)
    rail = page.locator('.left-side-menu .cats-list a.cat', has_text='Làm giải pháp').first
    clip(page, rail, S + 'icon_nhom.png'); crop_w(S + 'icon_nhom.png', 150)
    rail.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '_flyout.png')
    item = page.get_by_text('BOM Giải pháp', exact=True).last
    clip(page, item.locator('xpath=..'), S + 'icon_man.png')
    page.keyboard.press('Escape'); page.mouse.click(800, 870); page.wait_for_timeout(800)
    goto_list(page)
    clip(page, page.get_by_role('button', name='Tạo mới'), S + 'icon_taomoi.png')
    clip(page, page.get_by_role('button', name='Xuất Excel'), S + 'icon_xuat.png')
    clip(page, page.locator('button[title="Cấu hình cột hiển thị"]'), S + 'icon_cot.png')
    clip(page, page.get_by_role('button', name='Tìm kiếm nâng cao'), S + 'icon_timkiem.png')
    clip(page, page.get_by_role('button', name='Cài đặt bộ lọc'), S + 'icon_caidat.png')
    row30 = page.locator('tr', has_text='BOM-2026-00030').first
    clip(page, row30.locator('a', has_text='BOM-2026-00030'), S + 'icon_ma.png')
    row30.locator('span[title="Sửa"]').scroll_into_view_if_needed(); page.wait_for_timeout(800)
    page.screenshot(path=S + '01b-ds-phai.png')
    clip(page, row30.locator('span[title="Sửa"]'), S + 'icon_sua.png')
    clip(page, row30.locator('span[title="Xóa"]'), S + 'icon_xoa.png')
    clip(page, row30.locator('button[title="Hành động khác"]'), S + 'icon_more.png')
    row30.locator('button[title="Hành động khác"]').click(); page.wait_for_timeout(1000)
    print(page.evaluate("() => { const m=[...document.querySelectorAll('*')].filter(e=>e.textContent.trim()==='In BOM List' && e.children.length===0); return m.map(e=>e.outerHTML+' | '+e.parentElement.outerHTML.slice(0,300)) }"))
    page.screenshot(path=S + '_more.png')
    for t, n in [('Sao chép', 'saochep'), ('In BOM List', 'in'), ('Lịch sử', 'lichsu')]:
        loc = page.locator('.dropdown-menu.show, .v2-row-actions__menu, [role=menu]').get_by_text(t, exact=True).first
        try:
            clip(page, loc.locator('xpath=..'), S + 'icon_%s.png' % n)
        except Exception as e:
            print('miss', t, e)
    page.keyboard.press('Escape'); page.mouse.click(700, 870); page.wait_for_timeout(500)
    goto_list(page)
    page.get_by_role('button', name='Tìm kiếm nâng cao').click(); page.wait_for_timeout(5000)
    page.screenshot(path=S + '02-loc.png')
    page.get_by_role('button', name='Ẩn tìm kiếm nâng cao').click(); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Cài đặt bộ lọc').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '03-cai-dat-loc.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    page.locator('button[title="Cấu hình cột hiển thị"]').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '04-cot.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Xuất Excel').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '05-xuat.png')
    clip(page, page.get_by_role('button', name='Xuất file'), S + 'icon_xuatfile.png')
    with page.expect_download(timeout=90000) as dl:
        page.get_by_role('button', name='Xuất file').click()
    dl.value.save_as(S + 'export_list.xlsx')
    page.wait_for_timeout(1500)
    # delete confirm on BOM 30
    goto_list(page)
    b = page.locator('tr', has_text='BOM-2026-00030').first.locator('span[title="Xóa"] button'); b.scroll_into_view_if_needed(); b.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '19-xoa.png')
    page.get_by_role('button', name='Hủy').last.click(); page.wait_for_timeout(800)
