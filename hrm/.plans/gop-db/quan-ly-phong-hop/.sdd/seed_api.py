import json, sys, urllib.request, datetime as dt
env = dict(l.strip().split('=', 1) for l in open(sys.argv[1]) if '=' in l)
BASE = 'http://127.0.0.1:8051/api/v1/'
def call(tok, path, data=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(data).encode() if data is not None else None,
        headers={'Authorization': 'Bearer ' + env[tok], 'Content-Type': 'application/json', 'Accept': 'application/json'},
        method='POST' if data is not None else 'GET')
    try:
        r = json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        raise SystemExit(f'{path} {e.code}: {e.read().decode()[:400]}')
    return r.get('data', r)
me, other = 'TOKEN13', 'TOKEN484'
out = {}
out['purposes'] = [call(me, 'meeting/room-purposes', {'name': n, 'sort_order': 0, 'status': 1})['id'] for n in ['TA Họp nội bộ', 'TA Tiếp khách']]
out['services'] = [call(me, 'meeting/room-services', {'name': n, 'unit': u, 'sort_order': 0, 'status': 1})['id']
                   for n, u in [('TA Trà', 'ấm'), ('TA Nước suối', 'chai'), ('TA Hoa quả', 'đĩa')]]
rooms = [('TA Phòng Hoa Sen', 'Tầng 3 - Toà A', 10, False, [13]),
         ('TA Phòng Hội đồng', 'Tầng 5 - Toà A', 20, True, [13]),
         ('TA Phòng Sen Vàng', 'Tầng 2 - Toà B', 6, True, [484])]
out['rooms'] = [call(me, 'meeting/rooms', {'name': n, 'location': l, 'capacity': c, 'require_approval': a, 'status': 1,
                 'manager_employee_ids': m})['id'] for n, l, c, a, m in rooms]
R1, R2, R3 = out['rooms']; P1, P2 = out['purposes']; S1, S2, S3 = out['services']
# Tạo với khung giờ hợp lệ ở tương lai (ngày +20..), giờ thật được chỉnh lại bằng SQL ở bước sau
def slot(i): d = dt.date.today() + dt.timedelta(days=20 + i); return {'start_at': f'{d} 09:00:00', 'end_at': f'{d} 10:00:00'}
plan = [  # key, token, room, purpose, title, services
  ('B1', me, R1, P1, 'TA Họp triển khai app phòng họp', [{'service_id': S1, 'quantity': 2}]),
  ('B2', me, R2, P2, 'TA Tiếp đoàn khách Kính Nổi', [{'service_id': S2, 'quantity': 10}, {'service_id': S3, 'quantity': 2}]),
  ('B3', me, R3, P1, 'TA Họp kế hoạch tháng 11', []),
  ('B4', me, R1, P1, 'TA Họp giao ban tuần', []),
  ('B5', me, R1, P1, 'TA Họp tổng kết quý (đã huỷ)', []),
  ('B6', other, R2, P2, 'TA Đào tạo sản phẩm mới', [{'service_id': S2, 'quantity': 6}, {'service_id': S3, 'quantity': 2, 'note': 'Ít ngọt'}]),
  ('B7', other, R2, P1, 'TA Họp phòng Kinh doanh 1', []),
  ('B8', other, R1, P2, 'TA Gặp nhà cung cấp', [{'service_id': S1, 'quantity': 1}]),
]
out['bookings'] = {}
for i, (k, tok, room, pur, title, sv) in enumerate(plan):
    data = {'meeting_room_id': room, 'purpose_id': pur, 'title': title, 'attendee_count': 4, **slot(i)}
    if sv: data['services'] = sv
    out['bookings'][k] = call(tok, 'meeting/room-bookings', data)['id']
json.dump(out, open(sys.argv[2], 'w'))
print(json.dumps(out))
