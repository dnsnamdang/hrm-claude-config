# -*- coding: utf-8 -*-
"""Tạo 2 BOM riêng cho SRS BOM giải pháp (qua API :8003, tài khoản DNS Admin)."""
import json, urllib.request
S = json.load(open('/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs/.auth_state.json'))
TOK = [kv['value'] for o in S['origins'] for kv in o['localStorage'] if kv['name'] == 'access_token'][0]
API = 'http://127.0.0.1:8003/api/v1/assign/bom-lists'

def post(payload):
    req = urllib.request.Request(API, data=json.dumps(payload).encode(), method='POST',
                                 headers={'Authorization': 'Bearer ' + TOK, 'Content-Type': 'application/json',
                                          'Accept': 'application/json'})
    try:
        r = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(e.code, e.read().decode()[:800]); raise
    d = json.loads(r.read())['data']
    print(d['id'], d['code'], d['status_name'])
    return d

def erp(eid, code, name, model, brand, origin, unit, qty=1):
    return dict(product_project_id=None, erp_product_id=eid, product_type=1, cost_id=None, name=name, code=code,
                model_id=model, brand_id=brand, origin_id=origin, unit_id=unit, qty_needed=qty,
                product_attributes='', note=None, estimated_price=0, gom_key=None)

def tam(name, qty, note=None, spec=''):
    return dict(product_project_id=None, erp_product_id=None, product_type=1, cost_id=None, name=name, code='',
                model_id=None, brand_id=253, origin_id=21, unit_id=39, qty_needed=qty,
                product_attributes=spec, note=note, estimated_price=0, gom_key=None)

BASE = dict(prospective_project_id=150, solution_id=953, solution_module_id=954, customer_id=43562, currency_id=1,
            bom_list_type='component', sub_bom_list_ids=[])

a = post(dict(BASE, name='BOM bàn thực hành thủy lực – thiết bị khí nén bổ sung', status=2,
    note='Bổ sung thiết bị khí nén cho 10 bàn thực hành thủy lực',
    bom_groups=[
        dict(id=None, client_id='g_1', parent_client_id=None, name='Thiết bị thực hành khí nén', sort_order=0),
        dict(id=None, client_id='g_2', parent_client_id='g_1', name='Phụ kiện dẫn khí', sort_order=0),
        dict(id=None, client_id='g_3', parent_client_id=None, name='Vật tư lắp đặt', sort_order=1),
    ],
    groups=[
        dict(group_id='g_1', parent=dict(erp(48064, 'CH-TPDKKN', 'Bộ thực hành Điều khiển điện khí nén - chuyên dùng cho đào tạo', 38028, 328, 99, 39, 10), show_children=1), children=[]),
        dict(group_id='g_2', parent=dict(erp(48392, 'FLEX-27720:01', 'Bộ cuộn dây khí nén, chiều dài dây 20m, áp suất làm việc lớn nhất 40 bar (đã bao gồm rulo cuốn dây và dây dẫn khí nén)', 38303, 253, 21, 39, 10), show_children=1),
             children=[erp(48389, 'FLEX-9021', 'Rulo cuốn ống dẫn loại lò xo (Chưa bao gồm cuộn dây dẫn khí nén)', 38301, 253, 21, 40, 1),
                       erp(48390, 'FLEX-27720', 'Ống dẫn khí nén, dài 20 m, áp suất làm việc 40 bar, đường kính trong 1/2"', 38303, 253, 21, 42, 1)]),
        dict(group_id='g_3', parent=dict(tam('Bộ đầu nối nhanh khí nén phi 8', 20, 'Lắp cho 10 bàn', 'Đầu nối nhanh phi 8, áp suất 10 bar'), show_children=1),
             children=[tam('Đầu nối thẳng phi 8', 10), tam('Van tiết lưu một chiều phi 8', 10)]),
    ],
    service_items=[dict(id=None, cost_id=75, name='Chi phí lắp đặt, vận hành, chạy thử', code='', estimated_price=0, vat_percent=8, note='Lắp đặt tại xưởng', sort_order=0)],
))
b = post(dict(BASE, name='BOM vật tư tiêu hao bàn thực hành khí nén (nháp)', status=1, note='Đang lập, chưa chốt số lượng',
    bom_groups=[],
    groups=[dict(group_id=None, parent=dict(erp(48390, 'FLEX-27720', 'Ống dẫn khí nén, dài 20 m, áp suất làm việc 40 bar, đường kính trong 1/2"', 38303, 253, 21, 42, 5), show_children=1), children=[])],
    service_items=[]))
json.dump({'A': a['id'], 'B': b['id']}, open('created_ids.json', 'w'))
