"""E2E bổ sung các nhánh chưa có ở run_api/run_ui — chạy SAU seed_test_data.py.  python3 run_extra.py
(Đang giữ ≠ 0, Hàng tự khai thác trọn luồng, nhu cầu theo dự án, áp mẫu ở báo giá CÓ dự án, Hỏi giá với hàng giá 1đ thật)."""
from playwright.sync_api import sync_playwright
from common import *

KH, Q, QP, P_STOCK, P_LOW = 210, 219, 92, 43508, 3900
TMP = sql("select id, code from products where name='[TEST] Hàng tự khai thác – đã vào kinh doanh'")[0]
ERR = []

# ---- API
st, r = api('POST', 'assign/quotations/stock-info', {'quotation_id': Q, 'items': [{'product_id': P_STOCK}]})
row = r['data'][0]
check('Đang giữ: namdangit giữ 2 cái CH-ER-BDCD cho KH 210 ⇒ cột Đang giữ = 2', row['prepick_qty'] == 2, row)
check('Có thể LR: CH-ER-BDCD > 0', row['join_qty'] > 0, row)
st, r = api('POST', 'assign/quotations/stock-info', {'quotation_id': Q, 'items': [{'product_id': P_STOCK}]}, tok=token('tok_cannt'))
check('Đang giữ theo NGƯỜI LẬP báo giá (người khác mở vẫn thấy 2)', r['data'][0]['prepick_qty'] == 2, r['data'][0])
base = 'master-data/products/product-picker/search?company_id=1&scope=all&include_uncataloged=1&per_page=50&columns[]=creator_name&product_cate=hang_tu_khai_thac'
st, r = api('GET', base)
hit = [x for x in r['data'] if x['id'] == int(TMP[0])]
check('Hàng tự khai thác: hàng tạm mới lọc ra được theo loại', len(hit) == 1, [x['code'] for x in r['data']])
check('Hàng tự khai thác: có tên người tạo để hỏi giá', hit and hit[0].get('creator_name'), hit)

# ---- UI
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1600, 'height': 1000})
    page = ctx.new_page()
    page.on('pageerror', lambda e: ERR.append(str(e)))
    page.on('dialog', lambda d: d.accept())
    ui_login(page)

    # Báo giá CÓ dự án: ô nhu cầu chỉ xem, hiện nhu cầu của dự án; áp Báo giá mẫu + Lưu nháp
    page.goto(FE + f'/assign/quotations/{QP}/edit', wait_until='domcontentloaded'); page.wait_for_timeout(15000)
    row = page.locator('tr', has=page.locator('th', has_text='Nhu cầu khách hàng')).first
    check('UI dự án: ô nhu cầu là ô CHỌN, có dấu *', '*' in row.locator('th').first.inner_text() and row.locator('.select2-selection').count() == 1)
    check('UI dự án: điền sẵn nhu cầu của dự án (có mã meeting)', 'Cầu nâng' in row.inner_text() and 'TPE.MET' in row.inner_text(), row.inner_text())
    row.locator('.select2-selection').first.click(); page.wait_for_timeout(600)
    page.keyboard.type('khí nén'); page.wait_for_timeout(700); page.keyboard.press('Enter'); page.wait_for_timeout(500)
    check('UI dự án: đổi sang nhu cầu meeting khác của khách được', 'Hệ thống khí nén' in row.inner_text(), row.inner_text())
    page.evaluate("(js) => { const v = eval(js)('stockOf'); v.$confirm = async () => true; window.__d = false; v.onPickQuotationTemplate(3).then(() => window.__d = true) }", VM_JS)
    page.wait_for_function('() => window.__d === true', timeout=90000)
    with page.expect_response(lambda r: r.url.endswith(f'/assign/quotations/{QP}') and r.request.method == 'PUT', timeout=90000) as ri:
        page.locator('button:has-text("Lưu nháp")').last.click()
    check('UI dự án: áp Báo giá mẫu cho báo giá CÓ dự án rồi Lưu nháp thành công', ri.value.status == 200, ri.value.text()[:300])
    check('UI dự án: Lưu nháp ghi nhu cầu đã đổi', sql(f'select customer_demand_id from quotations where id={QP}')[0][0] == sql("select id from meeting_investment_demands where scope_name='[TEST] Hệ thống khí nén KH210'")[0][0])
    page.wait_for_timeout(3000)

    # Hỏi giá với hàng giá 1đ thật: thêm TEWI-828127 qua popup chọn hàng ⇒ hiện nút ⇒ mở phiếu đúng hàng
    page.goto(FE + f'/assign/quotations/{Q}/edit', wait_until='domcontentloaded'); page.wait_for_timeout(15000)
    page.locator('tbody.q-section-head-tbody button:has-text("Thêm mới")').first.click(); page.wait_for_timeout(9000)
    page.locator('.modal-backdrop-lite input[placeholder^="Tìm theo mã"]').first.fill('TEWI-828127')
    page.keyboard.press('Enter'); page.wait_for_timeout(5000)
    page.locator('.modal-backdrop-lite .ppp-name').first.click(); page.wait_for_timeout(2000)
    check('UI Hỏi giá: chọn hàng giá 1đ có hỏi lại "Vẫn chọn / Không" (cảnh báo sẵn có)', page.locator('button:has-text("Vẫn chọn")').count() >= 1)
    page.locator('button:has-text("Vẫn chọn")').first.click(); page.wait_for_timeout(4000)
    page.locator('.modal-backdrop-lite button:has-text("Đóng")').last.click(); page.wait_for_timeout(2000)
    added = page.evaluate("(js) => eval(js)('stockOf').products.some(p => Number(p.erp_product_id) === 3900)", VM_JS)
    check('UI Hỏi giá: thêm được TEWI-828127 qua popup (bấm tên hàng)', added)
    check('UI Hỏi giá: hàng giá 1đ ⇒ hiện nút Hỏi giá', page.locator('button:has-text("Hỏi giá")').count() == 1)
    with ctx.expect_page() as np_:
        page.locator('button:has-text("Hỏi giá")').click()
    np_.value.wait_for_load_state('domcontentloaded')
    check('UI Hỏi giá: tab mới chứa đúng mã hàng 3900', '3900' in np_.value.url, np_.value.url)
    np_.value.wait_for_timeout(12000)
    check('UI Hỏi giá: phiếu hỏi giá hiện TEWI-828127', 'TEWI-828127' in np_.value.content())
    np_.value.close()
    # tồn của hàng vừa thêm trên lưới (cột Đang giữ của CH-ER-BDCD chỉ có khi thêm hàng đó — kiểm qua API ở trên)
    # Thanh tải Nuxt (lớp phủ .loading-page) khi chọn mẫu: hiện trong lúc tải, tắt khi xong
    page.goto(FE + f'/assign/quotations/{Q}/edit', wait_until='domcontentloaded'); page.wait_for_timeout(15000)
    for label, js in [
        ('Báo giá mẫu', "(js) => { const v = eval(js)('stockOf'); v.$confirm = async () => true; window.__d = false; v.onPickQuotationTemplate(3).then(() => window.__d = true) }"),
        ('BOM mẫu', "(js) => { const v = eval(js)('stockOf'); v.$confirm = async () => true; window.__d = false; v.onPickBomTemplate(1).then(() => window.__d = true) }"),
        ('Dữ liệu mẫu', "(js) => { const v = eval(js)('stockOf'); window.__d = false; v.onApplyDataTemplate({ templateId: 2, groupId: null }).then(() => window.__d = true) }"),
    ]:
        page.evaluate("() => { window.__d = false }")
        page.evaluate(js, VM_JS)
        hits = []
        for _ in range(120):
            hits.append(page.evaluate("() => !!document.querySelector('.loading-page')"))
            if page.evaluate('() => window.__d'):
                break
            page.wait_for_timeout(150)
        page.wait_for_timeout(400)
        check(f'UI thanh tải: chọn {label} ⇒ hiện lớp phủ đang tải, xong thì tắt', any(hits) and not page.evaluate("() => !!document.querySelector('.loading-page')"), hits[:10])
    # Ô "Báo giá mẫu" / "BOM mẫu" giữ tên mẫu đã áp; Huỷ thì giữ giá trị cũ; áp mẫu kia thì ô này về trống
    page.goto(FE + f'/assign/quotations/{Q}/edit', wait_until='domcontentloaded'); page.wait_for_timeout(15000)
    def pick(row, text, btn):
        page.locator(f'tr:has(th:has-text("{row}")) .select2-selection').first.click(); page.wait_for_timeout(500)
        page.keyboard.type(text, delay=20); page.wait_for_timeout(800); page.keyboard.press('Enter'); page.wait_for_timeout(1200)
        page.locator(f'.modal.show button:has-text("{btn}")').last.click(); page.wait_for_timeout(6000)
        shown = lambda r: page.locator(f'tr:has(th:has-text("{r}")) .select2-selection__rendered').first.inner_text()
        return shown('Báo giá mẫu'), shown('BOM mẫu')
    qt, bt = pick('Báo giá mẫu', 'trạm sạc Schneider', 'Xác nhận')
    check('UI mẫu: áp Báo giá mẫu xong ô vẫn hiện tên mẫu đã chọn', 'Báo giá trạm sạc Schneider' in qt, qt)
    qt, bt = pick('Báo giá mẫu', 'BMW', 'Hủy')
    check('UI mẫu: chọn mẫu khác rồi Huỷ ⇒ ô giữ mẫu cũ', 'Báo giá trạm sạc Schneider' in qt, qt)
    qt, bt = pick('BOM mẫu', 'khoang sửa chữa', 'Xác nhận')
    check('UI mẫu: áp BOM mẫu ⇒ ô BOM mẫu hiện tên, ô Báo giá mẫu về trống', 'BOM mẫu khoang sửa chữa' in bt and 'Schneider' not in qt, (qt, bt))
    b.close()
check('Không lỗi JS', not ERR, ERR[:3])
sql(f'update quotations set customer_demand_id=null where id={Q}')
summary()
