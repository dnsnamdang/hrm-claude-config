import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
ED = """(() => { const m = window.$nuxt.$route.matched; let root = m[m.length-1].instances.default;
  const find = (vm) => { if (vm.$options.name === 'BomBuilderEditor') return vm; for (const c of vm.$children) { const r = find(c); if (r) return r } return null };
  return find(root) })()"""
def ed(page, js):
    return page.evaluate("() => { const ed = %s; %s }" % (ED, js))
def wait_editor(page):
    page.wait_for_function("() => { try { const ed = %s; return ed && !ed.disabled && (ed.bomDetailLoaded || !ed.bomId) } catch(e) { return false } }" % ED, timeout=120000)
    page.wait_for_timeout(3000)
with browser_page() as page:
    # ---- chi tiết BOM 29
    page.goto(BASE + '/assign/bom-list/29', wait_until='domcontentloaded'); wait_editor(page)
    page.screenshot(path=S + '17-chi-tiet.png')
    ft = page.locator('.bom-detail-footer')
    for t, n in [('Sửa', 'ct_sua'), ('In', 'ct_in'), ('Xuất Excel', 'ct_xuat'), ('Sao chép', 'ct_saochep'), ('Quay lại', 'quaylai')]:
        clip(page, ft.locator('button').filter(has_text=t).first if t != 'In' else ft.locator('button').nth(1), S + 'icon_%s.png' % n)
    ft.locator('button').filter(has_text='Xuất Excel').first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '16-xuat-bom.png')
    with page.expect_download(timeout=90000) as dl:
        page.locator('#bom-export-modal').get_by_role('button', name='Xuất Excel').click()
    dl.value.save_as(S + 'BOM-2026-00029.xlsx'); page.wait_for_timeout(1500)
    ft.locator('button').nth(1).click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '20-in-cau-hinh.png')
    clip(page, page.get_by_role('button', name='Xem trước'), S + 'icon_xemtruoc.png')
    page.get_by_role('button', name='Xem trước').click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '21-in-xem-truoc.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
    # lịch sử phiếu (khối cuối màn)
    page.goto(BASE + '/assign/bom-list/29', wait_until='domcontentloaded'); wait_editor(page)
    hdr = page.locator('.si-header').first
    page.evaluate("() => document.querySelector('.si-header').click()"); page.wait_for_timeout(4000)
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)"); page.wait_for_timeout(1000)
    page.screenshot(path=S + '24-lich-su-phieu.png')
    # ---- chi tiết BOM 26 đã duyệt
    page.goto(BASE + '/assign/bom-list/26', wait_until='domcontentloaded'); wait_editor(page)
    page.screenshot(path=S + '23-da-duyet.png')
    # ---- lịch sử popup ở danh sách (BOM 26)
    page.goto(BASE + '/assign/bom-list', wait_until='domcontentloaded')
    page.wait_for_function("() => !document.querySelector('.v2-data-table .spinner-border')", timeout=90000); page.wait_for_timeout(3000)
    r = page.locator('tr', has_text='BOM-2026-00026').first
    page.wait_for_selector('text=BOM-2026-00026', timeout=60000); page.wait_for_timeout(1500)
    page.screenshot(path=S + '_dbg.png')
    b = page.locator('tr', has_text='BOM-2026-00026').first.locator('span[title="Lịch sử"] button')
    b.scroll_into_view_if_needed(); b.click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '22-lich-su.png')
    # ---- sửa BOM 29
    page.goto(BASE + '/assign/bom-list/29/edit', wait_until='domcontentloaded'); wait_editor(page)
    page.screenshot(path=S + '13-sua.png')
    page.evaluate("() => window.scrollBy(0, 330)"); page.wait_for_timeout(800)
    page.screenshot(path=S + '13b-sua-luoi.png')
    row = page.locator('tr.bom-parent-row', has_text='Bộ đầu nối nhanh').first
    for t, n in [('Thêm con', 'themcon'), ('Sửa', 'suadong'), ('Nhân bản', 'nhanban'), ('Xoá', 'xoadong')]:
        try: clip(page, row.get_by_role('button', name=t), S + 'icon_%s.png' % n)
        except Exception as e: print('miss', t, e)
    gr = page.locator('tr.bom-group-row').first
    clip(page, gr.get_by_role('button', name='Thêm nhóm con'), S + 'icon_themnhomcon.png')
    row.get_by_role('button', name='Sửa').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '14-sua-nhanh.png')
    page.locator('.edit-modal-card').get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(800)
    # popup thêm hàng + tái sử dụng
    page.locator('.bom-section-row', has_text='A — Hàng hoá').get_by_role('button', name='Thêm mới').click()
    page.wait_for_function("() => !document.body.innerText.includes('Đang tải dữ liệu...')", timeout=120000); page.wait_for_timeout(3000)
    page.screenshot(path=S + '09-them-hang.png')
    page.get_by_role('button', name='Thêm hàng tạm').click(); page.wait_for_timeout(3500)
    page.screenshot(path=S + '10-hang-tam-dung-lai.png')
    page.locator('.bom-quick-add-card').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(800)
    page.locator('.modal-footer-fixed').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    # nhóm hàng
    page.get_by_role('button', name='Thêm nhóm').first.click(); page.wait_for_timeout(1500)
    page.locator('.modal.show input').first.type('Thiết bị đo kiểm'); page.wait_for_timeout(500)
    page.screenshot(path=S + '12-nhom.png')
    page.locator('.modal.show').get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(800)
    # import
    page.get_by_role('button', name='Import Excel').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '15a-import-trong.png')
    page.locator('input[type=file][accept=".xlsx,.xls"]').set_input_files(S + 'BOM-2026-00029.xlsx'); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Load lên bảng').click(); page.wait_for_timeout(2500)
    page.get_by_role('button', name='Validate').click(); page.wait_for_timeout(8000)
    page.screenshot(path=S + '15-import.png')
    page.locator('.modal.show').get_by_role('button', name='Import', exact=True).click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '15c-import-phuong-thuc.png')
    page.locator('.modal.show').last.get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(800)
