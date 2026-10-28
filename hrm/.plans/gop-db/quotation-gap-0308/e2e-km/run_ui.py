import re, subprocess, time
from common import *

def sql(q):
    return subprocess.run(['mysql', '-uroot', 'local_hrm_erp', '-N', '-e', q], capture_output=True, text=True).stdout.strip()

CUST = 210
LINES = [
    {'product_type': 1, 'erp_product_id': 40405, 'code': 'ENEO-408-V5041:01', 'name': 'Dầu SJ 20W-40', 'unit_id': 83, 'qty_needed': 10, 'quoted_price': 100000, 'estimated_price': 80000, 'vat_percent': 10, 'temp_id': 't1'},
    {'product_type': 1, 'erp_product_id': 7465, 'code': 'ENEO-410-V5041', 'name': 'Dầu 1L', 'unit_id': 73, 'qty_needed': 48, 'quoted_price': 50000, 'estimated_price': 40000, 'vat_percent': 10, 'temp_id': 't2'},
    {'product_type': 1, 'erp_product_id': 7466, 'code': 'ENEO-408-V5117', 'name': 'Dầu 0.8L', 'unit_id': 61, 'qty_needed': 6, 'quoted_price': 60000, 'estimated_price': 50000, 'vat_percent': 10, 'temp_id': 't3'},
] + [{'product_type': 1, 'erp_product_id': pid, 'code': code, 'name': code, 'unit_id': 87, 'qty_needed': 6, 'quoted_price': 900000, 'estimated_price': 800000, 'vat_percent': 10, 'temp_id': 'm%d' % pid}
     for pid, code in [(21882, 'MARA-P1261'), (33834, 'MARA-P1309'), (21874, 'MARA-P1258'), (7017, 'MARA-P1034'), (7019, 'MARA-P0270')]]

st, js = api('POST', 'assign/quotations', {'price_type_id': 1, 'customer_id': CUST, 'name': '[E2E KM] UI test', 'products': LINES, 'service_items': [], 'quotation_discounts': [],
                                          'delivery_address': 'Số 1 Test KM, Hà Nội'})
QID = (js.get('data') or {}).get('id')
check('Tạo báo giá test qua API', st == 200 and QID, js)
print('QID', QID)

console_errors, req_log = [], []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1500, 'height': 1000})
    page = ctx.new_page()
    page.on('console', lambda m: console_errors.append(m.text) if m.type == 'error' or (m.type == 'warning' and 'Vue warn' in m.text) else None)
    page.on('pageerror', lambda e: console_errors.append('PAGEERROR ' + str(e)))
    page.on('request', lambda r: req_log.append((r.method, r.url, r.post_data)) if '/assign/quotations' in r.url and r.method in ('PUT', 'POST') else None)
    page.goto(FE + '/login', wait_until='domcontentloaded')
    page.evaluate('t => localStorage.setItem("access_token", t)', TOKEN)

    def goto(path, sel):
        page.goto(FE + path, wait_until='domcontentloaded', timeout=180000)
        page.wait_for_selector(sel, timeout=180000)
        page.wait_for_timeout(1500)

    def inp(dt):
        loc = page.locator(f'[data-test="{dt}"]').first
        if loc.evaluate('e => e.tagName') != 'INPUT':
            loc = loc.locator('input').first
        return loc

    def type_into(dt, val):
        i = inp(dt); i.click(); i.press('ControlOrMeta+a'); i.press('Backspace')
        if val != '': i.type(str(val))
        page.wait_for_timeout(300)

    def err_near(dt):
        return inp(dt).evaluate('e => (e.closest("td") || e.parentElement).innerText').strip()

    def summary_rows():
        loc = page.locator('[data-test="qp-gift-summary"] tbody tr')
        return [[c.strip() for c in loc.nth(i).locator('td').all_inner_texts()] for i in range(loc.count())]

    def save_draft(expect_ok):
        n = len(req_log)
        page.get_by_role('button', name=re.compile('Lưu nháp')).click()
        page.wait_for_timeout(4000)
        return req_log[n:]

    # ---------- màn Sửa ----------
    goto(f'/assign/quotations/{QID}/edit', 'text=Chương trình khuyến mại')
    check('Sửa: có mục "Chương trình khuyến mại" + nút Thêm chương trình', page.locator('[data-test="qp-add"]').count() == 1)
    check('Sửa: chưa có CT → "Chưa áp dụng chương trình khuyến mại nào."', page.get_by_text('Chưa áp dụng chương trình khuyến mại nào.').count() == 1)
    page.locator('[data-test="qp-add"]').click()
    page.wait_for_selector('tr[data-category]', timeout=60000)
    ids = page.locator('tr[data-category]').evaluate_all('es => es.map(e => +e.dataset.category)')
    check('Popup: liệt kê 472/474/482, không có CT ngoài phạm vi (480/481/478 nhóm KH khác)', {472, 474, 482} <= set(ids) and not ({480, 481, 478} & set(ids)), ids)
    kw = inp('qpp-keyword'); kw.type('mafra'); page.wait_for_timeout(1500)
    ids2 = page.locator('tr[data-category]').evaluate_all('es => es.map(e => +e.dataset.category)')
    check('Popup: tìm tên "mafra" → chỉ 472', ids2 == [472], ids2)
    kw.fill('');
    pk = inp('qpp-product'); pk.type('MARA-P1261'); page.wait_for_timeout(1500)
    ids3 = page.locator('tr[data-category]').evaluate_all('es => es.map(e => +e.dataset.category)')
    check('Popup: tìm hàng "MARA-P1261" → 472 + 474', sorted(ids3) == [472, 474], ids3)
    pk.fill('XYZ_KHONG_CO'); page.wait_for_timeout(1500)
    check('Popup: không khớp → "Không tìm thấy chương trình khuyến mại nào"', page.get_by_text('Không tìm thấy chương trình khuyến mại nào').count() == 1)
    page.get_by_role('button', name='Làm mới').click(); page.wait_for_timeout(1500)
    check('Popup: Làm mới → hiện lại đủ', page.locator('tr[data-category]').count() == len(ids))
    for cid in (482, 474):
        page.locator(f'tr[data-category="{cid}"] [data-test="qpp-pick"]').click()
        page.wait_for_selector(f'tr[data-category="{cid}"] >> text=Đã chọn', timeout=60000)
    check('Popup: bấm Chọn → dòng chuyển "Đã chọn"', page.locator('tr[data-category] >> text=Đã chọn').count() == 2)
    page.locator('.modal.show').get_by_role('button', name='Đóng').click(); page.wait_for_timeout(800)
    check('Sửa: hiện 2 chương trình', page.locator('[data-test="qp-cat-482"]').count() == 1 and page.locator('[data-test="qp-cat-474"]').count() == 1)

    vis = page.locator('[data-test="qp-cat-482"] [data-test^="qp-camp-"]').evaluate_all('es => es.map(e => e.dataset.test)')
    check('Lọc "Chỉ hiện mã có hàng trong báo giá": 482 hiện 5 mã chứa hàng của báo giá (4976/4977/4983/4988/4990)', sorted(vis) == ['qp-camp-4976', 'qp-camp-4977', 'qp-camp-4983', 'qp-camp-4988', 'qp-camp-4990'], vis)
    srch = page.locator('[data-test="qp-cat-482"] input[placeholder="Tìm theo tên, mã, model hàng hoá"]')
    srch.type('V5117'); page.wait_for_timeout(500)
    vis2 = page.locator('[data-test="qp-cat-482"] [data-test^="qp-camp-"]').evaluate_all('es => es.map(e => e.dataset.test)')
    check('Ô tìm trong CT: "V5117" → 4983 + 4990', sorted(vis2) == ['qp-camp-4983', 'qp-camp-4990'], vis2)
    srch.fill(''); page.wait_for_timeout(500)
    page.locator('[data-test="qp-cat-482"]').get_by_text('Chỉ hiện mã có hàng trong báo giá').click(); page.wait_for_timeout(500)
    n_all = page.locator('[data-test="qp-cat-482"] [data-test^="qp-camp-"]').count()
    check('Bỏ tick → hiện đủ 31 mã', n_all == 31, n_all)
    page.locator('[data-test="qp-cat-482"]').get_by_text('Chỉ hiện mã có hàng trong báo giá').click(); page.wait_for_timeout(500)
    sl_bg = page.locator('[data-test="qp-camp-4977"] tbody tr').first.locator('td').nth(5).inner_text().strip()
    check('Cột "SL trong báo giá" quy đổi 48 lít → 2 thùng', sl_bg == '2', sl_bg)

    # đơn lẻ: 10 thùng → 4 mốc
    type_into('qp-qty-4976-40405', 10)
    check('Nhập 10 thùng → hiện 4 ô chọn quà (mốc 9/3/2/1)', all(page.locator(f'[data-test="qp-select-{o}"]').count() == 1 for o in (22287, 22288, 22289, 22290)))
    type_into('qp-select-22287', 1); type_into('qp-select-22288', 1)
    rows = summary_rows()
    check('Bảng Hàng tặng: 1 Thùng + 2 Chai 0.8 lít', any(r[1] == 'ENEO-408-V5041:01' and r[3] == 'Thùng' and r[4] == '1' for r in rows) and any(r[3] == 'Chai 0.8 lít' and r[4] == '2' for r in rows), rows)
    # quà theo nhóm: 4983 mua 6 thùng → 5006 (áo) Q=6
    type_into('qp-qty-4983-7466', 6)
    check('Quà theo nhóm 5006 hiện khi mua mã trong nhóm', page.locator('[data-test="qp-gift-5006"]').count() == 1)
    q_text = page.locator('[data-test="qp-gift-5006"] tbody tr').first.locator('td').nth(1).inner_text().strip()
    check('Quà nhóm 5006: Tổng SL hàng mua = 6', q_text == '6', q_text)
    type_into('qp-select-22364', 6)
    # combo 474: 3 combo
    type_into('qp-combo-4871', 3)
    check('Combo 3 → hiện ô chọn quà 21827', page.locator('[data-test="qp-select-21827"]').count() == 1)
    type_into('qp-select-21827', 3)
    rows = summary_rows()
    check('Hàng tặng có 6 áo + 3 can Wax', any(r[1] == 'ENEO-AOPHONGDEN' and r[4] == '6' for r in rows) and any(r[1] == 'MARA-P0594' and r[4] == '3' for r in rows), rows)

    # sai định dạng: chặn, không gọi API
    type_into('qp-qty-4976-40405', -1)
    check('Gõ "-1" vào SL mua → dấu trừ bị chặn (ô chỉ nhận 1)', inp('qp-qty-4976-40405').input_value() == '1', inp('qp-qty-4976-40405').input_value())
    type_into('qp-qty-4976-40405', 10)
    type_into('qp-select-22288', 1.5)
    check('SL chọn quà lẻ 1.5 → "Không hợp lệ"', 'Không hợp lệ' in err_near('qp-select-22288'))
    sent = save_draft(False)
    check('Còn lỗi định dạng → bấm Lưu nháp KHÔNG gửi request, ở lại màn Sửa', not [r for r in sent if r[0] == 'PUT'] and '/edit' in page.url, sent)
    type_into('qp-select-22288', 1)
    check('Sửa lại → hết lỗi', 'Không hợp lệ' not in err_near('qp-select-22288'))

    # lỗi nghiệp vụ từ BE (422) hiện đúng ô
    type_into('qp-select-22289', 1)  # 9+1+2 = 12 > 10
    sent = save_draft(False)
    check('Tổng quà vượt SL mua → BE 422, báo dưới ô', 'vượt SL mua (10)' in err_near('qp-select-22289'), err_near('qp-select-22289'))
    check('…và vẫn ở màn Sửa', '/edit' in page.url)
    type_into('qp-select-22289', 0)
    type_into('qp-select-22288', 0); type_into('qp-select-22290', 0)
    type_into('qp-qty-4976-40405', 10)
    type_into('qp-select-22288', 4)  # 4 lần x 2 chai = 8 > còn 6 ; nhưng mốc 1×4 + 9 = 13 > 10 -> dùng mốc 9 = 0
    type_into('qp-select-22287', 0)
    save_draft(False)
    check('Quà vượt SL còn lại → "chỉ còn 6"', 'chỉ còn 6' in err_near('qp-select-22288'), err_near('qp-select-22288'))
    type_into('qp-select-22288', 1); type_into('qp-select-22287', 1)
    type_into('qp-qty-4977-7465', 3)   # 3 thùng > 2 thùng có trong báo giá
    save_draft(False)
    check('SL mua vượt SL trong báo giá → báo dưới ô SL mua', 'vượt SL hàng' in err_near('qp-qty-4977-7465'), err_near('qp-qty-4977-7465'))
    type_into('qp-qty-4977-7465', 2)
    sent = save_draft(True)
    put = [r for r in sent if r[0] == 'PUT']
    check('Hợp lệ → Lưu nháp gửi PUT và quay về danh sách', put and page.url.rstrip('/').endswith('/assign/quotations'), (page.url, sent[-1:] if sent else None))
    rows_db = sql(f'select count(*), sum(combo_category_id=482), sum(combo_category_id=474) from quotation_promotions where quotation_id={QID}')
    check('DB: lưu 482 (31 mã + 2 quà) + 474 (4 mã) = 37 dòng', rows_db.split('\t')[0] == '37', rows_db)
    st, d = api('GET', f'assign/quotations/{QID}')
    gifts = {(g['code'], g['unit_name']): g['quantity'] for g in d['data']['promotions']['gifts']}
    exp = {('ENEO-408-V5041:01', 'Thùng'): 1, ('ENEO-408-V5041:01', 'Chai 0.8 lít'): 2, ('ENEO-AOPHONGDEN', 'Cái'): 6, ('MARA-P0594', 'Can 4.5L'): 3}
    gifts_n = {k: float(v) for k, v in gifts.items()}
    check('API chi tiết: hàng tặng đúng', all(gifts_n.get(k) == v for k, v in exp.items()), gifts)

    # mở lại: giữ nguyên
    goto(f'/assign/quotations/{QID}/edit', '[data-test="qp-cat-482"]')
    vals = {dt: inp(dt).input_value() for dt in ('qp-qty-4976-40405', 'qp-qty-4977-7465', 'qp-qty-4983-7466', 'qp-combo-4871', 'qp-select-22287', 'qp-select-22288', 'qp-select-22364', 'qp-select-21827')}
    check('Mở lại màn Sửa: giữ nguyên SL mua / combo / quà đã chọn', vals == {'qp-qty-4976-40405': '10', 'qp-qty-4977-7465': '2', 'qp-qty-4983-7466': '6', 'qp-combo-4871': '3', 'qp-select-22287': '1', 'qp-select-22288': '1', 'qp-select-22364': '6', 'qp-select-21827': '3'}, vals)

    # xoá CT: huỷ rồi xoá thật + cảnh báo chưa lưu
    page.locator('[data-test="qp-remove-474"]').click()
    page.wait_for_selector('.modal.show >> text=Xóa chương trình khuyến mại')
    page.locator('.modal.show').get_by_role('button', name=re.compile('Hủy|Huỷ|Đóng|Không')).first.click(); page.wait_for_timeout(600)
    check('Xoá CT → bấm Huỷ: CT vẫn còn', page.locator('[data-test="qp-cat-474"]').count() == 1)
    page.locator('[data-test="qp-remove-474"]').click()
    page.wait_for_selector('.modal.show >> text=Xóa chương trình khuyến mại')
    page.locator('.modal.show button', has_text='Xóa').last.click(); page.wait_for_timeout(600)
    check('Xoá CT → bấm Xóa: CT biến mất', page.locator('[data-test="qp-cat-474"]').count() == 0)
    page.get_by_role('button', name=re.compile('Quay lại')).first.click(); page.wait_for_timeout(1500)
    check('Thoát khi chưa lưu → hiện cảnh báo chưa lưu', page.locator('.modal.show').count() > 0 and '/edit' in page.url, page.url)
    if page.locator('.modal.show').count():
        page.locator('.modal.show').get_by_role('button').filter(has_text=re.compile('Ở lại|Hủy|Huỷ|Tiếp tục sửa|Không')).first.click(); page.wait_for_timeout(500)
    save_draft(True)
    check('Lưu sau khi xoá 474 → DB còn 33 dòng (chỉ 482)', sql(f'select count(*) from quotation_promotions where quotation_id={QID}') == '33')

    # ---------- màn Chi tiết ----------
    goto(f'/assign/quotations/{QID}', '[data-test="qp-cat-482"]')
    check('Chi tiết: không có ô nhập, không có nút Thêm/Xoá', page.locator('[data-test^="qp-qty-"], [data-test^="qp-select-"], [data-test="qp-add"], [data-test^="qp-remove-"]').count() == 0)
    check('Chi tiết: nhãn lọc "Chỉ hiện mã đã áp dụng"', page.get_by_text('Chỉ hiện mã đã áp dụng').count() >= 1)
    vis = page.locator('[data-test="qp-cat-482"] [data-test^="qp-camp-"]').evaluate_all('es => es.map(e => e.dataset.test)')
    check('Chi tiết: chỉ hiện mã đã áp dụng (4976/4977/4983)', sorted(vis) == ['qp-camp-4976', 'qp-camp-4977', 'qp-camp-4983'], vis)
    rows = summary_rows()
    check('Chi tiết: bảng Hàng tặng 3 dòng (thùng, chai, áo)', len(rows) == 3, rows)

    # ---------- màn Tạo mới ----------
    goto('/assign/quotations/create', 'text=Chương trình khuyến mại')
    check('Tạo mới: chưa chọn KH → gợi ý "Chọn khách hàng trước…", không có nút Thêm', page.get_by_text('Chọn khách hàng trước để thêm chương trình khuyến mại.').count() == 1 and page.locator('[data-test="qp-add"]').count() == 0)
    b.close()

errs = [e for e in console_errors if 'favicon' not in e and 'socket' not in e.lower() and '422' not in e]  # 422 = các bước cố tình gửi sai
check('Không có lỗi console / Vue warn', not errs, errs[:8])
open(os.path.join(HERE, 'ui_qid.txt'), 'w').write(str(QID))
summary()
