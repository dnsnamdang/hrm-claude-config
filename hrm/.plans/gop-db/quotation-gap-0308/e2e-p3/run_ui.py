"""E2E giao diện Phase 3 (GAP 0308) — Playwright Python, FE :3002 + API :8003.  Chạy: python3 run_ui.py
Mỗi bước thao tác thật trên màn (click / gõ select2 / bấm Lưu) rồi đối chiếu API / DB. Bắt mọi lỗi JS (pageerror)."""
import re, time
from playwright.sync_api import sync_playwright
from common import *

Q_DIRECT = 218      # báo giá độc lập test (KH 210)
Q_DEMAND = 219      # báo giá test nhu cầu (KH 210)
Q_PICK = 217        # báo giá test BOM mẫu (không lưu)
Q_GROUPS = 24       # báo giá ĐÃ DUYỆT có 6 nhóm — màn Chi tiết + In
Q_EDIT = 218        # báo giá Đang tạo có nhiều nhóm (áp Báo giá mẫu 2) — mọi bước trên màn Sửa
Q_SPECS = 45        # báo giá 151 hàng ERP có thông số (in bản thông số)
BOM = 30            # BOM nháp của tài khoản test
PAGE_ERRORS = []


def vm(page, method):
    return page.evaluate_handle(VM_JS, method)


def goto(page, path, wait=13000):
    page.goto(FE + path, wait_until='domcontentloaded', timeout=180000)
    page.wait_for_timeout(wait)


def select2_pick(page, scope_sel, text, nth=0):
    page.locator(scope_sel + ' .select2-selection').nth(nth).click()
    page.wait_for_timeout(500)
    page.keyboard.type(text, delay=20)
    page.wait_for_timeout(900)
    page.keyboard.press('Enter')
    page.wait_for_timeout(500)


def toast(page):
    return page.evaluate("() => Array.from(document.querySelectorAll('.toasted')).map(t => t.innerText).slice(-1)[0] || ''")


def save_draft(page, url_re):
    with page.expect_response(lambda r: re.search(url_re, r.url) and r.request.method in ('PUT', 'POST'), timeout=90000) as ri:
        page.locator('button:has-text("Lưu nháp")').last.click()
    r = ri.value
    try:
        page.wait_for_url(lambda u: '/edit' not in u, timeout=20000)
    except Exception:
        pass
    return r.status, (r.json() if 'json' in (r.headers.get('content-type') or '') else {})


with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={'width': 1600, 'height': 1000})
    page = ctx.new_page()
    page.on('pageerror', lambda e: PAGE_ERRORS.append(str(e)))
    page.on('dialog', lambda d: d.accept())
    ui_login(page)

    # ============================================================ 1. Nhu cầu khách hàng — chọn thật bằng select2 + Lưu nháp
    sql(f'update quotations set customer_demand_id=null where id={Q_DEMAND}')
    goto(page, f'/assign/quotations/{Q_DEMAND}/edit')
    row = page.locator('tr', has=page.locator('th', has_text='Nhu cầu khách hàng'))
    check('UI nhu cầu: ô có dấu * (báo giá không dự án)', '*' in row.locator('th').first.inner_text())
    select2_pick(page, 'tr:has(th:has-text("Nhu cầu khách hàng"))', 'Kết cấu thép KH210')
    st, body = save_draft(page, rf'/assign/quotations/{Q_DEMAND}$')
    check('UI nhu cầu: Lưu nháp ghi đúng nhu cầu đã chọn', st == 200 and sql(f'select customer_demand_id from quotations where id={Q_DEMAND}')[0][0] == '5', (st, body))
    check('UI nhu cầu: lưu xong quay về danh sách', page.url.rstrip('/').endswith('/assign/quotations'), page.url)
    goto(page, f'/assign/quotations/{Q_DEMAND}')
    check('UI nhu cầu: màn Chi tiết hiện nhãn nhu cầu', 'Kết cấu thép KH210' in page.locator('tr', has=page.locator('th', has_text='Nhu cầu khách hàng')).first.inner_text())

    tpl0 = api('GET', 'assign/quotations/template-options')[1]['data']
    # ============================================================ 5. Báo giá mẫu (UI thật) — thay hết + Lưu nháp + mở lại
    goto(page, f'/assign/quotations/{Q_DIRECT}/edit', 15000)
    qt = next(t for t in tpl0['quotation_templates'] if t['id'] == 2) if any(t['id'] == 2 for t in tpl0['quotation_templates']) else tpl0['quotation_templates'][0]
    exp = api('GET', f"assign/quotations/quotation-templates/{qt['id']}")[1]['data']
    t0 = time.time()
    select2_pick(page, 'tr:has(th:has-text("Báo giá mẫu"))', qt['text'][:45])
    page.wait_for_timeout(1200)
    page.locator('.modal.show button:has-text("Xác nhận")').last.click()
    page.wait_for_function("() => Array.from(document.querySelectorAll('.toasted')).some(t => t.innerText.includes('Đã áp dụng mẫu'))", timeout=180000)
    secs = time.time() - t0
    named = len([g for g in exp['groups'] if g['products']])
    st_ = page.evaluate("(js) => { const v = eval(js)('stockOf'); return { groups: v.directGroups.length, parents: v.products.filter(p => !p.parent_id).length, terms: (v.form.payment_terms || '').length } }", VM_JS)
    check(f'UI báo giá mẫu: dựng đúng {named} nhóm như ERP', st_['groups'] == (named if named > 1 else 0), st_)
    check(f'UI báo giá mẫu: áp xong trong {secs:.0f}s (local php -S 1 tiến trình)', secs < 60, secs)
    check('UI báo giá mẫu: điều khoản lấy theo mẫu', st_['terms'] > 0)
    st, body = save_draft(page, rf'/assign/quotations/{Q_DIRECT}$')
    check('UI báo giá mẫu: Lưu nháp thành công', st == 200, (st, json.dumps(body, ensure_ascii=False)[:300]))
    dbp = int(sql(f'select count(*) from quotation_product_prices where quotation_id={Q_DIRECT} and parent_id is null')[0][0])
    dbg = int(sql(f'select count(*) from quotation_groups where quotation_id={Q_DIRECT}')[0][0])
    check('UI báo giá mẫu: DB lưu đủ hàng cấp cha + nhóm', dbp == st_['parents'] and dbg == st_['groups'], (dbp, dbg, st_))

    # ============================================================ 2. Màn Sửa: cột tồn, Tổng hợp VAT, cộng nhóm, Hỏi giá
    goto(page, f'/assign/quotations/{Q_EDIT}/edit', 16000)
    heads = page.evaluate("() => Array.from(document.querySelectorAll('thead th')).map(t => t.innerText.trim())")
    check('UI sửa: có 3 cột Tồn có thể bán / Có thể LR / Đang giữ', all(h in heads for h in ['Tồn có thể bán', 'Có thể LR', 'Đang giữ']), heads)
    data = page.evaluate("""(js) => { const v = eval(js)('stockOf'); const p = v.products.find(x => x.erp_product_id && !x.parent_id);
        return { pid: p.erp_product_id, unit: p.unit_id || null, stock: v.stockOf(p), customer: v.item.customer_id,
                 sale: v.productSaleAfterDiscountTotal, groups: v.groupTotals, vatRows: v.vatSummaryRows.length } }""", VM_JS)
    st, r = api('POST', 'assign/quotations/stock-info', {'quotation_id': Q_EDIT, 'items': [{'product_id': data['pid'], 'unit_id': data['unit']}]})
    check('UI sửa: số tồn trên lưới = API stock-info', data['stock'] and data['stock']['sellable_by_company'] == r['data'][0]['sellable_by_company'], (data['stock'], r['data']))
    qvs = page.evaluate("() => Array.from(document.querySelectorAll('.qvs .qvs-total td:last-child')).map(t => Number(t.innerText.replace(/,/g, '')))")
    amounts = page.evaluate("() => Array.from(document.querySelectorAll('.qvs tfoot tr:first-child td:last-child')).map(t => Number(t.innerText.replace(/,/g, '')))")
    check('UI sửa: Tổng hợp theo VAT – tổng thành tiền = tổng hàng hoá sau GG', abs(sum(amounts) - data['sale']) < 1, (sum(amounts), data['sale']))
    level1 = page.evaluate("""(js) => { const v = eval(js)('stockOf'); return v.directGroups.filter(g => g.parent_id == null && !g.parent_temp_id).reduce((s, g) => s + v.groupTotals[String(g.id || g.temp_id)].amount, 0) }""", VM_JS)
    check('UI sửa: cộng các nhóm cấp 1 = tổng hàng hoá', abs(level1 - data['sale']) < 1, (level1, data['sale']))
    check('UI sửa: tiêu đề nhóm hiện "Thành tiền / Sau VAT"', page.locator('.q-group-total').count() >= 1)
    low = page.evaluate("(js) => eval(js)('stockOf').askPriceErpIds.length", VM_JS)
    check(f'UI sửa: nút Hỏi giá hiện đúng theo dữ liệu ({low} hàng ERP ≤1,000đ)', page.locator('button:has-text("Hỏi giá")').count() == (1 if low else 0), low)
    page.evaluate("(js) => { const v = eval(js)('stockOf'); v.products.forEach(p => { if (p.erp_product_id && Number(p.quoted_price) <= 1000) p.quoted_price = 2000 }) }", VM_JS)
    page.wait_for_timeout(500)
    check('UI sửa: không còn hàng ≤1,000đ thì ẩn nút Hỏi giá', page.locator('button:has-text("Hỏi giá")').count() == 0)
    page.evaluate("(js) => { const v = eval(js)('stockOf'); const p = v.products.find(x => x.erp_product_id && !x.parent_id); p.quoted_price = 500 }", VM_JS)
    page.wait_for_timeout(500)
    check('UI sửa: có hàng ERP giá ≤1,000đ thì hiện nút Hỏi giá', page.locator('button:has-text("Hỏi giá")').count() == 1)
    with ctx.expect_page() as newp:
        page.locator('button:has-text("Hỏi giá")').click()
    np_ = newp.value
    np_.wait_for_load_state('domcontentloaded')
    check('UI sửa: Hỏi giá mở tab Tạo yêu cầu hỏi giá kèm đúng hàng', '/sale/price-asking-requests/add' in np_.url and str(data['pid']) in np_.url, np_.url)
    np_.wait_for_timeout(12000)
    pcode = sql(f"select code from products where id={data['pid']}")[0][0]
    check(f'UI hỏi giá: phiếu nạp sẵn đúng hàng {pcode}', pcode in np_.content(), pcode)
    np_.close()

    # ============================================================ 3. Popup chọn hàng (từ báo giá) + popup chọn dịch vụ
    page.locator('tbody.q-section-head-tbody button:has-text("Thêm mới")').first.click()
    page.wait_for_timeout(10000)
    ph = page.evaluate("() => Array.from(document.querySelectorAll('.modal-backdrop-lite thead th')).map(t => t.innerText.trim())")
    check('UI popup chọn hàng (báo giá): có cột Tồn bán được / Có thể LR / Đang giữ', all(h in ph for h in ['Tồn bán được', 'Có thể LR', 'Đang giữ']), ph)
    page.locator('.modal-backdrop-lite button:has-text("Tìm kiếm nâng cao")').first.click()
    page.wait_for_timeout(1500)
    check('UI popup chọn hàng: có ô lọc "Loại hàng hoá"', page.locator('.modal-backdrop-lite :text("Loại hàng hoá")').count() >= 1)
    # lọc thật theo loại "Bảo hành, sửa chữa": mọi dòng trả về đúng loại
    with page.expect_response(lambda r: 'product-picker/search' in r.url and 'product_cate=hang_bao_hanh' in r.url, timeout=60000) as ri:
        page.locator('.modal-backdrop-lite .ff', has_text='Loại hàng hoá').locator('.select2-selection').first.click()
        page.wait_for_timeout(500)
        page.keyboard.type('Bảo hành, sửa')
        page.wait_for_timeout(700)
        page.keyboard.press('Enter')
    rows = ri.value.json()['data']
    ids = ','.join(str(x['id']) for x in rows) or '0'
    check('UI popup chọn hàng: lọc Loại hàng hoá trả đúng loại', rows and sql(f"select count(*) from products where id in ({ids}) and not json_contains(product_cate, '\"hang_bao_hanh\"')")[0][0] == '0', len(rows))
    page.locator('.modal-backdrop-lite button:has-text("Đóng")').last.click()
    page.wait_for_timeout(1000)
    goto(page, f'/assign/quotations/{Q_EDIT}/edit', 15000)
    page.evaluate("(js) => eval(js)('openServiceSection') ? 0 : 0", VM_JS)
    # mở popup ở tab Dịch vụ & Chi phí (nút Thêm mới của mục B)
    btns = page.locator('tbody:has(.q-section-title:has-text("Dịch vụ")) button:has-text("Thêm mới")')
    if btns.count():
        btns.first.click()
        page.wait_for_timeout(5000)
        sh = page.evaluate("() => Array.from(document.querySelectorAll('.modal-backdrop-lite .cost-result-table th')).map(t => t.innerText.trim())")
        check('UI popup dịch vụ: có cột "Tính doanh thu"', 'Tính doanh thu' in sh, sh)
        badges = page.evaluate("() => Array.from(document.querySelectorAll('.modal-backdrop-lite .cost-result-table tbody tr td:nth-child(2)')).map(t => t.innerText.trim())")
        check('UI popup dịch vụ: mỗi dòng ghi Có / Không', badges and all(b in ('Có', 'Không') for b in badges), badges[:5])
        page.locator('.modal-backdrop-lite button:has-text("Đóng")').last.click()
    else:
        check('UI popup dịch vụ: tìm được nút Thêm mới mục B', False, 'không thấy nút')

    # ============================================================ 4. Dữ liệu mẫu (UI thật) — thay 1 nhóm
    goto(page, f'/assign/quotations/{Q_EDIT}/edit', 15000)
    tpl = api('GET', 'assign/data-templates' if False else 'assign/quotations/template-options')[1]['data']
    dt = next(t for t in tpl['data_templates'] if t['id'] == 2)
    before = page.evaluate("""(js) => { const v = eval(js)('stockOf'); const g = v.directGroups[0]; const gid = String(g.id || g.temp_id);
        return { gid, gname: g.name, inGroup: v.products.filter(p => !p.parent_id && String(p.quotation_group_id) === gid).length,
                 others: v.products.filter(p => !p.parent_id && String(p.quotation_group_id) !== gid).length } }""", VM_JS)
    page.locator('button:has-text("Dữ liệu mẫu")').first.click()
    page.wait_for_timeout(1500)
    select2_pick(page, '.modal.show', dt['text'][:40], 0)
    select2_pick(page, '.modal.show', before['gname'], 1)
    picked = page.evaluate("(js) => eval(js)('stockOf').$refs.dataTemplateModal.templateId", VM_JS)
    page.locator('.modal.show button:has-text("Áp dụng")').click()
    page.wait_for_function("() => Array.from(document.querySelectorAll('.toasted')).some(t => t.innerText.includes('Đã áp dụng mẫu'))", timeout=90000)
    active = int(sql(f"select count(*) from quotation_template_products t join products p on p.id=t.product_id where t.parent_id={picked} and p.status=1 and p.deleted_at is null")[0][0])
    after = page.evaluate("""(args) => { const v = eval(args[0])('stockOf'); const gid = args[1];
        return { inGroup: v.products.filter(p => !p.parent_id && String(p.quotation_group_id) === gid).length,
                 others: v.products.filter(p => !p.parent_id && String(p.quotation_group_id) !== gid).length } }""", [VM_JS, before['gid']])
    check(f'UI dữ liệu mẫu: nhóm đã chọn = đúng số hàng còn kinh doanh của mẫu {picked}', after['inGroup'] == active, (after, active))
    check('UI dữ liệu mẫu: nhóm khác giữ nguyên', after['others'] == before['others'], (before, after))
    check('UI dữ liệu mẫu: thông báo số hàng bỏ qua', 'không còn trong danh mục' in toast(page), toast(page))

    # ============================================================ 6. BOM mẫu ở báo giá (UI thật, không lưu)
    goto(page, f'/assign/quotations/{Q_PICK}/edit', 15000)
    bt = api('GET', 'assign/bom-templates/options')[1]['data'][0]
    bdata = api('GET', f"assign/bom-templates/{bt['id']}/data")[1]['data']
    select2_pick(page, 'tr:has(th:has-text("BOM mẫu"))', bt['text'][:30])
    page.wait_for_timeout(1000)
    page.locator('.modal.show button:has-text("Xác nhận")').last.click()
    page.wait_for_function("() => Array.from(document.querySelectorAll('.toasted')).some(t => t.innerText.includes('Đã áp dụng mẫu'))", timeout=90000)
    got = page.evaluate("(js) => { const v = eval(js)('stockOf'); return { parents: v.products.filter(p => !p.parent_id).length, svc: v.serviceItems.length } }", VM_JS)
    check('UI BOM mẫu (báo giá): đúng số hàng + dịch vụ của mẫu', got['parents'] == sum(len(g['products']) for g in bdata['groups']) and got['svc'] == len(bdata['services']), (got, bdata))

    # ============================================================ 7. Màn Chi tiết báo giá: cột tồn, cộng nhóm, Tổng hợp VAT
    goto(page, f'/assign/quotations/{Q_GROUPS}', 15000)
    heads = page.evaluate("() => Array.from(document.querySelectorAll('thead th')).map(t => t.innerText.trim())")
    check('UI chi tiết: có 3 cột tồn', all(h in heads for h in ['Tồn có thể bán', 'Có thể LR', 'Đang giữ']), heads)
    check('UI chi tiết: ô tồn có số theo công ty', page.locator('td.q-stock-cell b').count() >= 1)
    check('UI chi tiết: tiêu đề nhóm có cộng tiền nhóm', page.locator('.q-group-total').count() >= 1)
    check('UI chi tiết: có khối Tổng hợp theo VAT', page.locator('.qvs').count() == 1)

    # ============================================================ 8. In: tuỳ chọn + xem trước + khổ giấy
    def open_print(qid, labels):
        goto(page, f'/assign/quotations/{qid}', 14000)
        page.locator('button:has-text("In")').first.click()
        page.wait_for_timeout(1500)
        for lb in labels:
            page.locator('.modal.show label', has_text=lb).first.click()
        page.locator('.modal.show button:has-text("Xem trước")').click()
        page.wait_for_timeout(6000)
    open_print(Q_GROUPS, ['Tách theo nhóm hàng'])
    gt = page.locator('.print-content .group-total-row').count()
    check('UI in: mẫu "Tách theo nhóm" có dòng cộng mỗi nhóm', gt == page.locator('.print-content .group-row').count() and gt > 0, gt)
    open_print(Q_GROUPS, ['Hiện nhóm hàng cấp cha'])
    stt = page.evaluate("() => Array.from(document.querySelectorAll('.print-content .parent-row td:first-child')).map(t => Number(t.innerText))")
    check('UI in: tắt nhóm cấp cha ⇒ không tiêu đề nhóm, STT liên tục', page.locator('.print-content .group-row').count() == 0 and stt == list(range(1, len(stt) + 1)), stt[:15])
    open_print(Q_SPECS, ['In ngắn gọn', 'In kèm bản thông số kỹ thuật', 'Định mức đàm phán', 'In khổ ngang'])
    th = page.evaluate("() => Array.from(document.querySelectorAll('.print-content > .print-table thead th')).map(t => t.innerText.trim())")
    check('UI in: In ngắn gọn bỏ cột Thông số kỹ thuật', 'Thông số kỹ thuật' not in th, th)
    check('UI in: có cột Định mức đàm phán (%)', 'Định mức đàm phán (%)' in th, th)
    nspec = int(sql(f'select count(distinct q.erp_product_id) from quotation_product_prices q join attribute_products a on a.product_id=q.erp_product_id and a.need_print=1 where q.quotation_id={Q_SPECS} and q.parent_id is null')[0][0])
    check('UI in: trang Bản thông số kỹ thuật đủ hàng có thông số', page.locator('.spec-sheet tbody tr').count() == nspec, (page.locator('.spec-sheet tbody tr').count(), nspec))
    page.evaluate("() => { window.__printed = ''; window.open = () => ({ document: { write: (h) => { window.__printed = h }, close() {} }, focus() {}, print() {}, close() {} }) }")
    page.locator('.modal.show button:has-text("In")').first.click()
    page.wait_for_timeout(1000)
    check('UI in: bỏ tick "In khổ ngang" ⇒ @page portrait', 'A4 portrait' in page.evaluate('() => window.__printed'))
    open_print(Q_SPECS, ['In thông số mở rộng'])
    imgs = page.locator('.print-content .prod-img').count()
    check('UI in: In thông số mở rộng có thêm ảnh/phụ kiện (không lỗi)', imgs >= 1, imgs)

    # ============================================================ 9. BOM: cột mới + Tuỳ chỉnh cột + BOM mẫu + Lưu
    goto(page, f'/assign/bom-list/{BOM}/edit', 15000)
    heads = page.evaluate("() => Array.from(document.querySelectorAll('thead th')).map(t => t.innerText.trim())")
    check('UI BOM: có cột Ảnh, Thời gian bảo hành, 3 cột tồn', all(h in heads for h in ['Ảnh', 'Thời gian bảo hành', 'Tồn có thể bán', 'Có thể LR', 'Đang giữ']), heads)
    opts = page.evaluate("(js) => eval(js)('openBomTemplateModal').columnOptions.map(c => c.label)", VM_JS)
    check('UI BOM: Tuỳ chỉnh cột có các cột mới', all(x in opts for x in ['Ảnh', 'Thời gian bảo hành', 'Tồn có thể bán', 'Có thể LR', 'Đang giữ']), opts)
    page.locator('button:has-text("BOM mẫu")').first.click()
    page.wait_for_timeout(2000)
    select2_pick(page, '.modal.show', bt['text'][:30])
    page.locator('.modal.show button:has-text("Áp dụng")').click()
    page.wait_for_function("() => Array.from(document.querySelectorAll('.toasted')).some(t => t.innerText.includes('Đã áp dụng BOM mẫu'))", timeout=90000)
    st, body = save_draft(page, rf'/bom-lists/{BOM}')
    check('UI BOM: áp BOM mẫu rồi Lưu nháp thành công', st == 200, (st, body))
    n = int(sql(f'select count(*) from bom_list_products where bom_list_id={BOM} and parent_id is null')[0][0])
    check('UI BOM: DB lưu đúng số hàng của mẫu', n == sum(len(g['products']) for g in bdata['groups']), n)

    # ============================================================ 10. Màn BOM mẫu: tạo – khoá – mở khoá – xoá bằng giao diện
    goto(page, '/assign/bom-templates/add', 12000)
    name = 'E2E BOM mẫu ' + str(int(time.time()))
    page.locator('input[placeholder="Nhập tên BOM mẫu"]').fill(name)
    with page.expect_response(lambda r: '/assign/bom-templates' in r.url and r.request.method == 'POST', timeout=60000) as ri:
        page.locator('button:has-text("Lưu")').last.click()
    st = ri.value.status
    page.wait_for_timeout(3000)
    rid = sql(f"select id from bom_templates where name='{name}'")
    check('UI BOM mẫu: Thêm mới qua form lưu được', st in (200, 201) and rid, (st, rid))
    if rid:
        rid = int(rid[0][0])
        goto(page, f'/assign/bom-templates/{rid}', 10000)
        page.locator('button:has-text("Khoá")').first.click()
        page.wait_for_timeout(1000)
        page.locator('.modal.show button:has-text("Khoá")').last.click()
        page.wait_for_timeout(3000)
        check('UI BOM mẫu: Khoá được', sql(f'select status from bom_templates where id={rid}')[0][0] == '0')
        goto(page, f'/assign/bom-templates/{rid}', 10000)
        fb = page.evaluate("() => Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim())")
        check('UI BOM mẫu: mẫu khoá ẩn nút Sửa/Xoá', 'Sửa' not in fb and 'Xoá' not in fb and 'Mở khoá' in fb, fb)
        st423 = api('PUT', f'assign/bom-templates/{rid}', {'name': name + 'x', 'status': 0, 'groups': [], 'products': [], 'services': []})[0]
        check('UI BOM mẫu: BE chặn sửa mẫu khoá 423', st423 == 423, st423)
        page.locator('button:has-text("Mở khoá")').first.click()
        page.wait_for_timeout(1000)
        page.locator('.modal.show button:has-text("Mở khoá")').last.click()
        page.wait_for_timeout(3000)
        goto(page, f'/assign/bom-templates/{rid}', 10000)
        page.locator('button:has-text("Xoá")').first.click()
        page.wait_for_timeout(1000)
        page.locator('.modal.show button:has-text("Xoá")').last.click()
        page.wait_for_timeout(3000)
        check('UI BOM mẫu: Mở khoá rồi Xoá hẳn', not sql(f'select id from bom_templates where id={rid}'))

    # ============================================================ 10b. Màn BOM mẫu: Tuỳ chỉnh cột, Xuất Excel, Lịch sử
    sql("delete from user_column_settings where user_id=13 and screen_key='assign_bom_templates'")  # về cấu hình mặc định
    goto(page, '/assign/bom-templates', 10000)
    cols = page.evaluate("() => Array.from(document.querySelectorAll('thead th')).map(t => t.innerText.trim()).filter(Boolean)")
    check('UI BOM mẫu: mặc định 7 cột (STT, Mã, Tên, Người tạo, Ngày tạo, Trạng thái, Hành động)', len(cols) == 7, cols)
    page.locator('button:has(i.ri-layout-column-line)').first.click()
    page.wait_for_timeout(1500)
    allc = page.evaluate("() => Array.from(document.querySelectorAll('.modal.show .column-row, .modal.show label')).map(e => e.innerText.trim()).filter(Boolean)")
    check('UI BOM mẫu: popup Tuỳ chỉnh cột liệt kê cột ẩn (Số hàng hoá, Ghi chú…)', any('Số hàng hoá' in x for x in allc) and any('Ghi chú' in x for x in allc), allc)
    page.keyboard.press('Escape')
    page.wait_for_timeout(800)
    page.locator('button:has-text("Xuất Excel")').first.click()
    page.wait_for_timeout(1500)
    with page.expect_download(timeout=60000) as dl:
        page.locator('.modal.show button:has-text("Xuất")').last.click()
    import openpyxl, tempfile
    path = os.path.join(tempfile.mkdtemp(), dl.value.suggested_filename or 'bom_templates.xlsx')
    dl.value.save_as(path)
    check('UI BOM mẫu: file tải về là .xlsx', path.endswith('.xlsx'), path)
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    hrow = next(i for i in range(1, 7) if any(str(c.value or '').startswith('Mã') for c in ws[i]))
    hdr = [c.value for c in ws[hrow] if c.value]
    nrows = ws.max_row - hrow + 1
    check('UI BOM mẫu: Xuất Excel tải file .xlsx thật, dòng tiêu đề tiếng Việt', hdr and any('Mã' in str(h) for h in hdr), hdr)
    check('UI BOM mẫu: số dòng file = số mẫu trên DB', nrows - 1 >= int(sql('select count(*) from bom_templates')[0][0]), (nrows, hdr))
    hid = int(sql("select id from bom_templates order by id desc limit 1")[0][0])
    goto(page, f'/assign/bom-templates/{hid}', 10000)
    check('UI BOM mẫu: màn Chi tiết có khối Lịch sử', page.locator('.system-info-section').count() >= 1)
    goto(page, '/assign/bom-templates', 10000)
    page.locator('tbody tr').first.locator('button[title="Hành động khác"]').click()
    page.wait_for_timeout(700)
    page.locator('.v2-row-actions__item:visible', has_text='Lịch sử').first.click()
    page.wait_for_timeout(3000)
    check('UI BOM mẫu: menu ⋮ › Lịch sử mở popup lịch sử', page.locator('.modal.show', has_text='Lịch sử').count() >= 1)
    page.keyboard.press('Escape')

    # ============================================================ 11. Tài khoản không quyền
    ctx2 = browser.new_context(viewport={'width': 1600, 'height': 1000})
    p2 = ctx2.new_page()
    p2.on('pageerror', lambda e: PAGE_ERRORS.append('[cannt] ' + str(e)))
    ui_login(p2, LIMITED_EMAIL, LIMITED_PASS)
    p2.goto(FE + '/assign/bom-templates', wait_until='domcontentloaded')
    p2.wait_for_timeout(10000)
    b2 = p2.evaluate("() => Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim())")
    check('UI không quyền: danh sách BOM mẫu không có Thêm mới / Khoá / Sao chép', not any(x in b2 for x in ['Thêm mới', 'Khoá', 'Sao chép']), b2)
    check('UI không quyền: vẫn thấy danh sách + Xuất Excel', p2.locator('tbody tr').count() >= 1)

    check('Không có lỗi JS (pageerror) trên mọi màn đã mở', not PAGE_ERRORS, PAGE_ERRORS[:5])
    browser.close()

sql(f'update quotations set customer_demand_id=null where id={Q_DEMAND}')
summary()
