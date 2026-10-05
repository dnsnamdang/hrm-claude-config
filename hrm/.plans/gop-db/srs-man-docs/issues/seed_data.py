# -*- coding: utf-8 -*-
"""Tạo dữ liệu Vấn đề qua API :8003 (tài khoản admin id 13) để chụp ảnh SRS.
Chỉ TẠO MỚI, không sửa issue có sẵn. Kết quả ghi ra seed_result.json."""
import json, urllib.request, datetime

API = 'http://127.0.0.1:8003/api/v1/'


def req(method, url, data=None, token=None):
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(API + url, data=body, method=method)
    r.add_header('Content-Type', 'application/json')
    r.add_header('Accept', 'application/json')
    if token:
        r.add_header('Authorization', 'Bearer ' + token)
    try:
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print('ERR', method, url, e.code, e.read().decode()[:500])
        raise


tok = req('POST', 'users/auth/login', {'email': 'namdangit@gmail.com', 'password': '2025Dns@2'})['access_token']
ADMIN = 13
today = datetime.date.today()


def d(n):
    return (today + datetime.timedelta(days=n)).isoformat()


BASE = dict(solution_id=955, project_id=152, issue_type='bug', priority='medium', impact_level='project',
            detected_from='self', detected_by=ADMIN, detected_at=datetime.datetime.now().isoformat(),
            due_time='17:00', affect_schedule='minor', affect_quality='no', affect_customer='no',
            sla='1d', handle_plan='', close_condition='', watcher_ids=[970], supporter_ids=[781], tags=[])

ISSUES = [
    dict(key='new', title='Sai đơn giá vật tư cáp điều khiển trong BOM tủ điện tổng', module_id=955,
         issue_type='missing_data', priority='high', status='new', handling_department_id=55, assignee_id=None,
         description='Đơn giá cáp điều khiển 4x1.5 trong BOM đang lấy giá năm 2025, chênh 12% so với báo giá NCC mới.',
         due_date=d(5), tags=['BOM', 'Đơn giá'], flow=[]),
    dict(key='assigned', title='Thiếu bản vẽ mặt bằng bố trí cầu nâng khoang 2', module_id=956,
         issue_type='missing_input', status='assigned', assignee_id=ADMIN, approver_id=148,
         description='Khách hàng chưa gửi bản vẽ mặt bằng khoang 2, chưa chốt được vị trí đặt cầu nâng 2 trụ.',
         due_date=d(3), tags=['Bản vẽ'], flow=[]),
    dict(key='in_progress', title='Chậm phản hồi thông số máy nén khí từ nhà cung cấp', module_id=956,
         issue_type='risk', priority='critical', status='assigned', assignee_id=ADMIN, approver_id=148,
         description='NCC chưa gửi catalogue máy nén khí trục vít 15kW, ảnh hưởng tiến độ lập dự toán.',
         due_date=d(-2), tags=['NCC'], flow=['in_progress']),
    dict(key='resolved', title='Báo giá thiếu chi phí nhân công lắp đặt hệ thống khí nén', module_id=955,
         issue_type='business', priority='high', status='assigned', assignee_id=ADMIN, approver_id=ADMIN,
         description='Bảng báo giá gửi khách chưa có dòng chi phí nhân công lắp đặt đường ống khí nén.',
         due_date=d(1), tags=['Báo giá'], flow=['in_progress', 'resolved']),
    dict(key='completed', title='Khách hàng đổi yêu cầu số lượng máy ra vào lốp', module_id=956,
         issue_type='customer_change', status='assigned', assignee_id=ADMIN, approver_id=None,
         description='Khách hàng tăng số lượng máy ra vào lốp từ 1 lên 2 bộ, cần cập nhật BOM và báo giá.',
         due_date=d(2), tags=['Thay đổi KH'], flow=['in_progress', 'completed']),
    dict(key='rejected', title='Sai mã hàng thiết bị cân chỉnh độ chụm trong BOM', module_id=955,
         issue_type='bug', status='assigned', assignee_id=ADMIN, approver_id=ADMIN,
         description='Mã hàng thiết bị cân chỉnh độ chụm 3D trong BOM không khớp danh mục hàng hoá.',
         due_date=d(4), tags=['BOM'], flow=['in_progress', 'resolved', ('rejected', 'Mã mới vẫn sai model, cần đối chiếu lại catalogue hãng.')]),
    dict(key='closed', title='Trùng dòng thiết bị rửa xe trong hạng mục 1', module_id=955,
         issue_type='other', priority='low', status='assigned', assignee_id=ADMIN, approver_id=None,
         description='Hạng mục 1 có 2 dòng thiết bị rửa xe áp lực cao giống nhau.',
         due_date=d(6), tags=[], flow=[('closed', 'Đã gộp dòng ở bản BOM mới.')]),
    dict(key='reopened', title='Thiếu thông số nguồn điện 3 pha cho máy chẩn đoán', module_id=956,
         issue_type='missing_data', status='assigned', assignee_id=ADMIN, approver_id=None,
         description='Thông số nguồn điện của máy chẩn đoán chưa ghi rõ 3 pha 380V hay 1 pha 220V.',
         due_date=d(7), tags=['Điện'], flow=['in_progress', 'completed', 'reopened']),
]

out = []
for it in ISSUES:
    p = dict(BASE)
    p.update({k: v for k, v in it.items() if k not in ('key', 'flow')})
    res = req('POST', 'assign/issues', p, tok)['data']
    iid = res['id']
    for st in it['flow']:
        reason = None
        if isinstance(st, tuple):
            st, reason = st
        req('PATCH', 'assign/issues/%d/status' % iid, {'status': st, 'reason': reason}, tok)
    out.append({'key': it['key'], 'id': iid, 'code': res.get('issue_code') or res.get('code'), 'title': it['title']})
    print(out[-1])

json.dump(out, open('seed_result.json', 'w'), ensure_ascii=False, indent=1)
