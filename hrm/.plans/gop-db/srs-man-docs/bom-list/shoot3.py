import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
ED = """(() => { const m = window.$nuxt.$route.matched; let root = m[m.length-1].instances.default;
  const find = (vm) => { if (vm.$options.name === 'BomBuilderEditor') return vm; for (const c of vm.$children) { const r = find(c); if (r) return r } return null };
  return find(root) })()"""
def ed(page, js):
    return page.evaluate("() => { const ed = %s; %s }" % (ED, js))
def wait_editor(page):
    page.wait_for_function("() => { try { const ed = %s; return ed && !ed.disabled } catch(e) { return false } }" % ED, timeout=120000)
    page.wait_for_timeout(2500)
with browser_page() as page:
    page.goto(BASE + '/assign/bom-list/add', wait_until='domcontentloaded'); wait_editor(page)
    page.screenshot(path=S + '06a-tao-trong.png')
    ed(page, "ed.bomForm.name = 'BOM thiết bị đo kiểm bàn thực hành thủy lực'; ed.bomForm.note = 'Bổ sung đồng hồ đo áp cho 10 bàn'; ed.handleProjectChange(150); ed.handleModuleChange(954);")
    page.wait_for_timeout(1500)
    page.screenshot(path=S + '06-tao-tp.png')
    clip(page, page.locator('.v2-styles .form-row').first.locator('.col-md-3').nth(6), S + 'icon_loaibom.png')
    clip(page, page.get_by_role('button', name='Lưu nháp'), S + 'icon_luunhap.png')
    clip(page, page.get_by_role('button', name='Lưu BOM'), S + 'icon_luubom.png')
    clip(page, page.get_by_role('button', name='Thêm nhóm').first, S + 'icon_themnhom.png')
    btn_hh = page.locator('.bom-section-row', has_text='A — Hàng hoá').get_by_role('button', name='Thêm mới')
    clip(page, btn_hh, S + 'icon_themmoi.png')
    imp = page.get_by_role('button', name='Import Excel')
    clip(page, imp, S + 'icon_import.png')
    # popup thêm hàng
    btn_hh.click(); page.wait_for_timeout(9000)
    page.screenshot(path=S + '09-them-hang.png')
    clip(page, page.get_by_role('button', name='Thêm hàng tạm'), S + 'icon_hangtam.png')
    page.get_by_role('button', name='Thêm hàng tạm').click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '10-hang-tam-dung-lai.png')
    page.get_by_role('tab', name='Thêm mới thủ công').click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '10b-hang-tam-thu-cong.png')
    page.locator('.bom-quick-add-card').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(800)
    page.locator('.modal-footer-fixed').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    # dịch vụ
    page.locator('.bom-section-row', has_text='Dịch vụ').get_by_role('button', name='Thêm mới').click(); page.wait_for_timeout(6000)
    page.screenshot(path=S + '11-dich-vu.png')
    page.locator('.modal-footer-fixed').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(1000)
    # nhóm hàng
    page.get_by_role('button', name='Thêm nhóm').first.click(); page.wait_for_timeout(1500)
    page.locator('.modal.show input').first.fill('Thiết bị đo kiểm')
    page.screenshot(path=S + '12-nhom.png')
    page.locator('.modal.show').get_by_role('button', name='Huỷ').click(); page.wait_for_timeout(800)
    # tổng hợp + chọn BL con
    page.goto(BASE + '/assign/bom-list/add', wait_until='domcontentloaded'); wait_editor(page)
    ed(page, "ed.bomForm.name = 'BOM tổng hợp hạng mục Xây dựng danh mục thiết bị – đợt 2'; ed.handleProjectChange(150); ed.handleModuleChange(954); ed.bomForm.bom_list_type = 'aggregate'; ed.handlebom_list_typeChange();")
    page.wait_for_timeout(1500)
    page.screenshot(path=S + '07-tao-th.png')
    clip(page, page.get_by_role('button', name='Chọn BL con'), S + 'icon_chonblcon.png')
    page.get_by_role('button', name='Chọn BL con').click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '08-chon-bl-con.png')
    clip(page, page.get_by_role('button', name='Gộp BOM con'), S + 'icon_gop.png')
    page.locator('.modal-card input[type=checkbox]').first.check(); page.wait_for_timeout(500)
    page.get_by_role('button', name='Gộp BOM con').click(); page.wait_for_timeout(5000)
    page.screenshot(path=S + '08b-sau-gop.png', full_page=False)
