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
    page.goto(BASE + '/assign/bom-list/29', wait_until='domcontentloaded'); wait_editor(page)
    page.evaluate("() => document.querySelector('.si-header').click()"); page.wait_for_timeout(4000)
    page.evaluate("() => document.querySelector('.si-header').scrollIntoView({block:'start'})"); page.evaluate("() => window.scrollBy(0, -80)"); page.wait_for_timeout(1500)
    page.screenshot(path=S + '24-lich-su-phieu.png')
    page.goto(BASE + '/assign/bom-list/29/edit', wait_until='domcontentloaded'); wait_editor(page)
    row = page.locator('tr.bom-parent-row', has_text='HHB').first
    row.scroll_into_view_if_needed(); page.evaluate("() => window.scrollBy(0, 150)"); row.hover(); page.wait_for_timeout(1000)
    page.screenshot(path=S + '13c-sua-hang-tam.png')
    for t, n in [('Thêm con', 'themcon'), ('Sửa', 'suadong'), ('Nhân bản', 'nhanban'), ('Xoá', 'xoadong')]:
        try: row.hover(); clip(page, row.locator('button').filter(has_text=t).first, S + 'icon_%s.png' % n)
        except Exception as e: print('miss', t, str(e)[:100])
    row.hover(); row.locator('button').filter(has_text='Sửa').first.click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '14-sua-nhanh.png')
    page.locator('.edit-modal-card').get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(800)
    page.evaluate("() => window.scrollTo(0,0)"); page.wait_for_timeout(500)
    page.locator('.bom-section-row', has_text='A — Hàng hoá').get_by_role('button', name='Thêm mới').click()
    page.wait_for_timeout(4000)
    page.wait_for_function("() => !document.body.innerText.includes('Đang tải dữ liệu...')", timeout=120000); page.wait_for_timeout(3000)
    page.screenshot(path=S + '09-them-hang.png')
    page.get_by_role('button', name='Thêm hàng tạm').click(); page.wait_for_timeout(3500)
    page.screenshot(path=S + '10-hang-tam-dung-lai.png')
    page.locator('.bom-quick-add-card').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(800)
    page.locator('.modal-footer-fixed').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Thêm nhóm').first.click(); page.wait_for_timeout(1500)
    page.locator('.modal.show input').first.type('Thiết bị đo kiểm'); page.wait_for_timeout(500)
    page.screenshot(path=S + '12-nhom.png')
    page.locator('.modal.show').get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(800)
    page.get_by_role('button', name='Import Excel').click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '15a-import-trong.png')
    page.locator('input[type=file][accept=".xlsx,.xls"]').set_input_files(S + 'BOM-2026-00029.xlsx'); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Load lên bảng').click(); page.wait_for_timeout(2500)
    page.get_by_role('button', name='Validate').click(); page.wait_for_timeout(9000)
    page.screenshot(path=S + '15-import.png')
    page.locator('.modal.show').get_by_role('button', name='Import', exact=True).click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '15c-import-phuong-thuc.png')
    page.locator('.modal.show').last.get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(800)
