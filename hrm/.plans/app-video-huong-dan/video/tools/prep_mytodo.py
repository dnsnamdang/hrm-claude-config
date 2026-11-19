#!/usr/bin/env python3
"""Dựng dữ liệu quay video Việc của tôi + Nhắc việc (DB dev local, ngày tính theo HÔM NAY lúc chạy).

Ghi id đã tạo vào ~/.cache/tpe-video-work/prep_mytodo.json để dọn / tra lại.
Cần: API http://127.0.0.1:8001, JWT tài khoản 13 (DNS Admin) và 341 (Thiếu Quốc Đạt) — cấp qua tinker:
  auth("api")->login(\\App\\Models\\TpEmployee::find(ID))  → JWT13 / JWTX (biến môi trường hoặc file).
"""
import datetime as dt, json, os, subprocess, urllib.request

API = os.environ.get('API', 'http://127.0.0.1:8001/api/v1')
HRM_API = '/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-api'
PHP = '/opt/homebrew/opt/php@7.4/bin/php'
OUT = os.path.expanduser('~/.cache/tpe-video-work/prep_mytodo.json')


def jwt(emp):
    code = f'echo auth("api")->login(\\App\\Models\\TpEmployee::find({emp}));'
    r = subprocess.run([PHP, 'artisan', 'tinker', f'--execute={code}'], cwd=HRM_API, capture_output=True, text=True)
    return [l for l in r.stdout.splitlines() if l.count('.') == 2 and len(l) > 100][-1].strip()


ME, X = jwt(13), jwt(341)


def call(tok, method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=None if body is None else json.dumps(body).encode(),
                                 headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/json',
                                          'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            d = json.loads(r.read() or b'{}')
            return d.get('data', d)
    except urllib.error.HTTPError as e:
        raise SystemExit(f'{method} {path} → {e.code} {e.read()[:500]}')


today = dt.date.today()
D = lambda n: (today + dt.timedelta(days=n)).isoformat()
fri = today + dt.timedelta(days=(4 - today.weekday()) % 7)            # thứ Sáu tuần này
wed_next = today + dt.timedelta(days=7 - today.weekday() + 2)         # thứ Tư tuần sau
done = {'tasks': [], 'todos': [], 'meeting': None, 'contacts': []}

# ── Nhiệm vụ: Đạt giao cho tôi (để thẻ có vai trò / trạng thái / hạn ở đủ nhóm) ──
TASKS = [
    ('Lập báo giá cầu nâng 2 trụ cho Gara Thành Công', D(0), '16:00', 3, True),
    ('Kiểm tra tồn kho thiết bị chẩn đoán', D(1), '10:00', 1, False),
    ('Chuẩn bị hồ sơ dự thầu Trường Cao đẳng Dầu khí', fri.isoformat(), '17:00', 2, False),
    ('Cập nhật danh sách khách hàng tiềm năng quý IV', wed_next.isoformat(), '17:00', 1, False),
]
for title, due, tm, prio, doing in ([] if os.environ.get('SKIP_TASKS') else TASKS):
    t = call(X, 'POST', '/assign/tasks', {'title': title, 'priority': prio, 'status': 3, 'due_date': due, 'due_time': tm,
                                          'task_type': 2, 'assignee_id': 13, 'approver_id': 341, 'estimated_hours': 4})
    if doing:
        call(ME, 'PUT', f"/assign/tasks/{t['id']}", {'status': 4, 'is_import_result': True})
    done['tasks'].append(t['id'])

# ── Meeting hôm nay, tôi được mời mà CHƯA xác nhận (nhân bản từ meeting 2940) ──
php = f'''
$src = \\Modules\\Assign\\Entities\\Meeting\\Meeting::find(2940);
$m = $src->replicate();
$m->name = "Họp giao ban phòng kinh doanh tuần {today.isocalendar()[1]}";
$m->code = "TPE.MET.NB.VIDEO." . date("His");
$m->start_date = "{D(0)} 14:00:00"; $m->end_date = "{D(0)} 15:30:00";
$m->status = 2; $m->completed_at = null; $m->cancelled_at = null; $m->created_at = now(); $m->updated_at = now();
$m->save();
foreach (DB::table("meeting_employees")->where("meeting_id", 2940)->get() as $e) {{
  $row = (array) $e; unset($row["id"]); $row["meeting_id"] = $m->id; $row["created_at"] = now(); $row["updated_at"] = now();
  if ((int) $row["employee_id"] === 13) {{ $row["attendance_status"] = 0; $row["attendance_note"] = null; }}
  DB::table("meeting_employees")->insert($row);
}}
echo "MEETING=" . $m->id;
'''
r = subprocess.run([PHP, 'artisan', 'tinker', f'--execute={php}'], cwd=HRM_API, capture_output=True, text=True)
if 'MEETING=' not in r.stdout:
    raise SystemExit('Nhân bản meeting lỗi:\n' + r.stdout[-1500:] + r.stderr[-800:])
done['meeting'] = int(r.stdout.split('MEETING=')[1].split()[0])

# ── Nhắc việc cá nhân dựng sẵn ──
def todo(body):
    t = call(ME, 'POST', '/assign/my-todo/todos', {'list_id': 2, 'sub_items': [], **body})
    tid = t.get('id') if isinstance(t, dict) else None
    done['todos'].append(tid)
    return tid

todo({'title': 'Mua văn phòng phẩm cho phòng', 'due_date': D(1), 'due_time': None})                       # xoá ở bước 96
todo({'title': 'Gọi lại cho chị Lan báo giá lốp', 'due_date': D(-1), 'due_time': '15:00',                  # Hẹn chữ đỏ
      'contact': {'name': 'Chị Lan - Gara Minh Phát', 'phone': '0912468135', 'source': 1}})
p3 = todo({'title': 'Gửi hồ sơ năng lực cho khách', 'due_date': D(-3), 'due_time': '17:00', 'list_id': 742,
           'sub_items': [{'title': 'Cập nhật hồ sơ năng lực', 'is_completed': False}]})
if p3:
    call(ME, 'PATCH', f'/assign/my-todo/todos/{p3}/toggle')                                              # nhóm Đã kết thúc
# Lịch làm việc lãnh đạo: 1 lịch tuần này (ô vàng) + 1 lịch tuần sau (Sắp tới)
wed = today + dt.timedelta(days=(2 - today.weekday()) % 7)
todo({'title': 'Công tác Hà Nội gặp đối tác', 'list_id': 742, 'is_leader_schedule': True, 'leader_show_title': True,
      'start_date': wed.isoformat(), 'start_time': '08:00', 'due_date': (wed + dt.timedelta(days=1)).isoformat(), 'due_time': '17:00'})
tue_next = today + dt.timedelta(days=7 - today.weekday() + 1)
todo({'title': 'Dự hội thảo ngành thiết bị ô tô', 'list_id': 742, 'is_leader_schedule': True, 'leader_show_title': True,
      'start_date': tue_next.isoformat(), 'start_time': '08:00', 'due_date': tue_next.isoformat(), 'due_time': '17:00'})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({'date': today.isoformat(), **done}, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(done, ensure_ascii=False))
