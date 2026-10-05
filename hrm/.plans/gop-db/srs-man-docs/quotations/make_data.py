# -*- coding: utf-8 -*-
"""Tạo dữ liệu mẫu cho SRS Báo giá (local, API :8003, tài khoản admin id 13 — Sale phụ trách dự án 154).

Chạy: /opt/homebrew/bin/python3 make_data.py <tên> <kịch bản>
  kịch bản: draft | l2 | l3 | approved
Ghi id vào created.json.
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN = open('/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/95b31591-97d1-4390-9e6c-499b30ca0f38/scratchpad/q_token.txt').read().strip()
API = 'http://127.0.0.1:8003/api/v1/'


def call(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + url, data=data, method=method, headers={
        'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print('HTTP', e.code, body[:800])
        raise


TERMS = ('<p><strong>Ghi chú:</strong></p><p>- Báo giá trên theo tỷ giá hiện tại.</p>'
         '<p>- {{VAT_NOTE}} và {{VAN_CHUYEN_NOTE}}.</p>'
         '<p><strong>Thanh toán:</strong></p>'
         '<p>- Lần 1: Đặt cọc 30% tổng giá trị ngay khi ký hợp đồng.</p>'
         '<p>- Lần 2: Thanh toán 70% còn lại sau khi bàn giao, nghiệm thu thiết bị.</p>')


def payload(sale_factor=1.0, ship_import=1500000):
    """sale_factor < 1 kéo giá bán hàng tạm xuống để ép cấp duyệt cao hơn."""
    groups = [
        {'id': None, 'temp_id': 'g1', 'name': 'Thiết bị nâng hạ', 'sort_order': 0, 'parent_id': None, 'parent_temp_id': None},
        {'id': None, 'temp_id': 'g2', 'name': 'Dụng cụ cầm tay', 'sort_order': 1, 'parent_id': None, 'parent_temp_id': None},
    ]

    def row(**kw):
        base = dict(price_id=None, temp_id=None, quotation_group_id=None, parent_id=None, parent_temp_id=None,
                    product_type=1, erp_product_id=None, code='', gom_key=None, name='', model_id=None,
                    brand_id=None, origin_id=None, unit_id=39, qty_needed=1, product_attributes=None, note=None,
                    show_children=1, sort_order=0, estimated_price=0, quoted_price=0, vat_percent=8,
                    discount_input_mode=None, discount_percent=0, discount_amount=0, allocated_discount_amount=0)
        base.update(kw)
        return base

    products = [
        row(temp_id='p_1', quotation_group_id='g1', erp_product_id=48422, code='GC-GC-40PROA:03',
            name='Cầu nâng 2 trụ thủy lực có cổng 4 tấn (3 pha, màu xám RAL7016)', qty_needed=2,
            estimated_price=27884625, quoted_price=44900000, sort_order=1),
        row(temp_id='p_2', quotation_group_id='g1', name='Kích cá sấu thủy lực 3 tấn tay dài', brand_id=698,
            origin_id=6, unit_id=40, qty_needed=2, estimated_price=3200000,
            quoted_price=round(4800000 * sale_factor), product_attributes='Tải trọng 3 tấn; chiều cao nâng 85–500 mm',
            sort_order=2),
        row(temp_id='p_3', quotation_group_id='g2', erp_product_id=48419, code='CH-YT-38811',
            name='Bộ tuýp cờ lê tay vặn tổng hợp 150 món Yato YT-38811', qty_needed=3,
            estimated_price=4305556, quoted_price=6300000, sort_order=3),
        row(temp_id='p_4', quotation_group_id='g2', name='Xe đẩy dụng cụ 7 ngăn kèm bộ dụng cụ', brand_id=372,
            origin_id=10, qty_needed=1, estimated_price=9500000, quoted_price=round(14500000 * sale_factor),
            sort_order=4),
        row(temp_id='p_5', quotation_group_id='g2', parent_temp_id='p_4', name='Xe đẩy 7 ngăn có khóa',
            brand_id=372, origin_id=10, unit_id=40, qty_needed=1, estimated_price=5500000, quoted_price=0,
            sort_order=5),
        row(temp_id='p_6', quotation_group_id='g2', parent_temp_id='p_4', name='Khay dụng cụ 220 chi tiết',
            brand_id=372, origin_id=10, qty_needed=1, estimated_price=4000000, quoted_price=0, sort_order=6),
    ]
    services = [
        dict(id=None, cost_id=186, name='Chi phí dựng cầu nâng', unit_id=None, qty=1, estimated_price=3000000,
             quoted_price=5000000, vat_percent=8, discount_input_mode=None, discount_percent=0, discount_amount=0,
             allocated_discount_amount=0, note=''),
        dict(id=None, cost_id=74, name='Chi phí cho chuyên gia đào tạo chuyển giao công nghệ', unit_id=None, qty=1,
             estimated_price=round(8000000 * 0.85), quoted_price=8000000, vat_percent=8, discount_input_mode=None,
             discount_percent=0, discount_amount=0, allocated_discount_amount=0, note=''),
    ]
    return dict(project_id=154, currency_id=1, price_type_id=1, project_phase_id=3, delivery_time=30,
                warranty_time=12, payment_terms=TERMS, note='<p>Khách cần giao trước 15/11.</p>',
                customer_email='thanchaugarage@gmail.com', discount_method=None, rounding_mode=0,
                shipping_cost=2000000, shipping_vat_percent=8, shipping_discount=0, shipping_allocated_discount=0,
                shipping_import_price=ship_import, products=products, groups=groups, service_items=services,
                quotation_discounts=[])


def main():
    name, scen = sys.argv[1], sys.argv[2]
    path = os.path.join(HERE, 'created.json')
    created = json.load(open(path)) if os.path.exists(path) else {}
    if scen == 'draft':
        p = payload()
    elif scen == 'l2':
        p = payload(sale_factor=0.80, ship_import=1500000)
    elif scen == 'l3':
        p = payload(sale_factor=0.80, ship_import=40000000)
    else:
        p = payload()
    r = call('POST', 'assign/quotations', p)
    qid = r['data']['id']
    print('created', qid, r['data']['code'])
    if scen in ('l2', 'l3', 'approved'):
        lv = call('POST', 'assign/quotations/%d/calculate-level' % qid, {})
        print('level', lv['data']['level'], lv['data'].get('profit_margin_percent'))
        s = call('POST', 'assign/quotations/%d/submit' % qid, {})
        print('submit', s['message'])
        if scen == 'approved':
            if s['data'].get('can_self_approve'):
                a = call('POST', 'assign/quotations/%d/self-approve' % qid, {})
                print('self', a['message'])
    created[name] = {'id': qid, 'code': r['data']['code'], 'scenario': scen}
    json.dump(created, open(path, 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
