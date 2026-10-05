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
    page.goto(BASE + '/assign/bom-list/29/edit', wait_until='domcontentloaded'); wait_editor(page)
    page.get_by_role('button', name='Import Excel').click(); page.wait_for_timeout(2000)
    page.locator('input[type=file][accept=".xlsx,.xls"]').set_input_files(S + 'BOM-2026-00029.xlsx'); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Load lên bảng').click(); page.wait_for_timeout(2500)
    page.locator('.bom-import-toolbar button').filter(has_text='Validate').first.click(); page.wait_for_timeout(9000)
    page.screenshot(path=S + '15-import.png')
    page.locator('.bom-import-footer button').first.click(); page.wait_for_timeout(2000)
    page.screenshot(path=S + '15c-import-phuong-thuc.png')
    page.locator('.modal.show').last.get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(800)
    # tổng hợp + chọn BL con (chờ lâu hơn)
    page.goto(BASE + '/assign/bom-list/add', wait_until='domcontentloaded'); wait_editor(page)
    ed(page, "ed.bomForm.name = 'BOM tổng hợp hạng mục Xây dựng danh mục thiết bị – đợt 2'; ed.handleProjectChange(150); ed.handleModuleChange(954); ed.bomForm.bom_list_type = 'aggregate'; ed.handlebom_list_typeChange();")
    page.wait_for_timeout(1500)
    page.get_by_role('button', name='Chọn BL con').click()
    page.wait_for_selector('text=Chọn BOM con để gộp', timeout=120000); page.wait_for_timeout(2000)
    page.screenshot(path=S + '08-chon-bl-con.png')
    page.locator('.modal-card input[type=checkbox]').first.check(); page.wait_for_timeout(500)
    page.get_by_role('button', name='Gộp BOM con').click()
    page.wait_for_selector('text=Chọn BOM con để gộp', state='detached', timeout=120000); page.wait_for_timeout(3000)
    page.screenshot(path=S + '08b-sau-gop.png')
    # sao chép BOM 29
    page.goto(BASE + '/assign/bom-list/add?copy_from=29', wait_until='domcontentloaded'); wait_editor(page)
    page.screenshot(path=S + '18-sao-chep.png')
