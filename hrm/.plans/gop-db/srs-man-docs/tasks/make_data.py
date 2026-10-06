# -*- coding: utf-8 -*-
"""Tạo dữ liệu mẫu cho SRS Nhiệm vụ qua API :8003 (tài khoản admin id 13). Chạy 1 lần."""
import json, urllib.request
STATE = '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs/.auth_state.json'
s = json.load(open(STATE))
TOKEN = [i['value'] for i in s['origins'][0]['localStorage'] if i['name'] == 'access_token'][0]
API = 'http://127.0.0.1:8003/api/v1/'

def call(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + url, data=data, method=method, headers={
        'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/json', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print('ERR', e.code, e.read()[:800]); raise

def base(**kw):
    d = dict(task_type=2, assignee_ids=[], solution_id=None, solution_module_id=None, meeting_id=None,
             approver_id=13, priority=1, start_date='2026-10-03', due_date='2026-10-15', due_time='17:00',
             description='', status=1, estimated_hours=8, mode=2, tags=[], watchers=[13], checklists=[],
             children=[], linked=[], attachments=[],
             recurring={'is_active': False, 'repeat_type': 1, 'repeat_interval': 1, 'end_type': 1,
                        'week_days': [], 'month_day': None, 'cron_expression': '', 'end_date': '',
                        'max_occurrences': 10},
             progress_report={'is_active': False, 'cycle_type': 1, 'send_time': '17:00:00',
                               'week_days': [], 'month_day': None})
    d.update(kw)
    return d

created = {}
def create(key, **kw):
    r = call('POST', 'assign/tasks', base(**kw))
    data = r['data']
    ids = [x['id'] for x in data] if isinstance(data, list) else [data['id']]
    created[key] = ids
    print(key, ids)
    return ids

a = create('A_nhap', title='Soạn hồ sơ năng lực gửi Trường CĐ Cơ giới và Thủy Lợi Đồng Nai', assignee_id=148,
           project_id=113, priority=2, due_date='2026-10-15', estimated_hours=6, status=1,
           description='Tổng hợp hồ sơ năng lực, danh sách công trình tương tự và chứng chỉ ISO gửi nhà trường.',
           tags=['Hồ sơ thầu', 'Đồng Nai'], watchers=[13, 148],
           checklists=[{'content': 'Cập nhật danh sách công trình tương tự 2024-2026', 'is_done': False},
                       {'content': 'Đính kèm chứng chỉ ISO 9001', 'is_done': False},
                       {'content': 'Xin xác nhận của Ban giám đốc', 'is_done': False}])
b = create('B_dang_thuc_hien', title='Chuẩn bị tài liệu hướng dẫn vận hành cầu nâng 2 trụ', assignee_id=13,
           project_id=116, priority=3, status=4, due_date='2026-10-10', estimated_hours=8,
           description='Biên soạn tài liệu vận hành, bảo dưỡng cầu nâng 2 trụ cho kỹ thuật viên xưởng Ford Hưng Yên.',
           tags=['Đào tạo'], watchers=[13, 1142],
           checklists=[{'content': 'Thu thập catalogue của hãng', 'is_done': True},
                       {'content': 'Viết quy trình vận hành an toàn', 'is_done': False},
                       {'content': 'Chụp ảnh minh hoạ tại xưởng', 'is_done': False}])
c = create('C_cho_duyet_kq', title='Lập bảng khối lượng vật tư điện xưởng 3S Hyundai An Khánh', assignee_id=13,
           project_id=114, priority=2, status=4, due_date='2026-10-12', estimated_hours=6,
           description='Bóc tách khối lượng cáp, máng cáp, tủ điện theo bản vẽ mặt bằng điện.',
           tags=['Bóc tách khối lượng'], watchers=[13, 835],
           checklists=[{'content': 'Bóc tách cáp động lực', 'is_done': True},
                       {'content': 'Bóc tách máng cáp, ống luồn', 'is_done': True}])
call('PUT', 'assign/tasks/%d' % c[0], {
    'is_import_result': True, 'actual_hours': 7, 'progress_percent': 100,
    'result_text': 'Đã hoàn thành bảng khối lượng vật tư điện, gửi kèm file Excel để anh chị duyệt.',
    'result_attachments': [], 'progress_logs': [], 'checklists': [], 'status': 6})
d = create('D_bao_cao_tien_do', title='Theo dõi tiến độ lắp đặt thiết bị xưởng Ford Hưng Yên', assignee_id=13,
           project_id=116, priority=1, status=4, start_date='2026-09-29', due_date='2026-10-09',
           estimated_hours=24, tags=['Lắp đặt'], watchers=[13, 781],
           description='Báo cáo tiến độ lắp đặt cầu nâng, máy ra vào lốp, hệ thống khí nén hằng ngày.',
           progress_report={'is_active': True, 'cycle_type': 1, 'send_time': '17:00:00', 'week_days': [],
                            'month_day': None})
call('PUT', 'assign/tasks/%d' % d[0], {
    'is_import_result': True, 'actual_hours': None, 'progress_percent': 45,
    'result_text': '', 'result_attachments': [], 'checklists': [], 'status': 4,
    'progress_logs': [
        {'report_date': '2026-09-29', 'hours': 3, 'progress_pct': 10, 'note': 'Tập kết thiết bị tại xưởng'},
        {'report_date': '2026-09-30', 'hours': 4, 'progress_pct': 20, 'note': 'Lắp móng cầu nâng số 1'},
        {'report_date': '2026-10-01', 'hours': 4, 'progress_pct': 30, 'note': 'Lắp cầu nâng số 1, 2'},
        {'report_date': '2026-10-02', 'hours': 3.5, 'progress_pct': 45, 'note': 'Đi đường ống khí nén'},
    ]})
e = create('E_cho_phe_duyet', title='Khảo sát hiện trạng điện xưởng 2S Phương Anh', assignee_id=13,
           project_id=138, priority=1, status=2, due_date='2026-10-20', estimated_hours=4,
           description='Khảo sát nguồn điện, tủ điện tổng, vị trí đặt thiết bị.', watchers=[13])
f = create('F_co_nv_con', title='Triển khai bản vẽ bố trí thiết bị xưởng 3S Hyundai An Khánh', assignee_id=835,
           project_id=114, priority=2, status=3, due_date='2026-10-22', estimated_hours=16, watchers=[13, 835],
           tags=['Bản vẽ'],
           children=[{'title': 'Vẽ mặt bằng bố trí khu sửa chữa chung', 'assignee_id': 148,
                      'due_date': '2026-10-18', 'due_time': '17:00', 'is_done': False, 'watchers': [13, 835]},
                     {'title': 'Vẽ mặt bằng khu đồng sơn', 'assignee_id': 149,
                      'due_date': '2026-10-20', 'due_time': '17:00', 'is_done': False, 'watchers': [13, 835]}])
g = create('G_nv_chung', task_type=1, title='Cập nhật kế hoạch làm việc tuần 41 lên hệ thống', assignee_id=None,
           assignee_ids=[148, 149], status=3, priority=1, due_date='2026-10-09', estimated_hours=1, watchers=[13],
           description='Mỗi kỹ sư tự cập nhật kế hoạch tuần 41 vào màn Lịch làm việc của tôi.')
json.dump(created, open('/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/srs-man-docs/tasks/created_ids.json', 'w'))
print(created)
