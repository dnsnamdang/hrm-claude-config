"""Tạo phiếu mẫu ngày 29/09/2026 để test #11523 trên DB local (local_hrm_erp).
Nhân bản từ phiếu thật (đủ cột bắt buộc) rồi đổi ngày/mã/nhân viên. Id tạo ra ghi vào created_ids.json
để cleanup_testdata.py xoá sạch. Chạy lại được: tự dọn bộ cũ trước khi tạo."""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
D = '2026-09-29'
# employees.id / employee_infos.id
A = (1169, 1603)  # Vũ Thị Phương Linh 12611039
B = (1168, 1602)  # Phạm Trung Đức 12611038
C = (1167, 1601)  # Đào Quốc Trung 12611037

def run(sql):
    r = subprocess.run(['mysql', '-uroot', '-N', 'local_hrm_erp'], input=sql, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr)
    return r.stdout.strip()

def clone(table, src_where, sets):
    """Nhân bản 1 dòng, trả id mới."""
    set_sql = ', '.join(f'{k}={v}' for k, v in {'id': 'NULL', 'created_at': 'NOW()', 'updated_at': 'NOW()', **sets}.items())
    return int(run(f"""
DROP TEMPORARY TABLE IF EXISTS _t; CREATE TEMPORARY TABLE _t AS SELECT * FROM {table} WHERE {src_where} LIMIT 1;
ALTER TABLE _t MODIFY id BIGINT UNSIGNED NULL; UPDATE _t SET {set_sql};
INSERT INTO {table} SELECT * FROM _t; SELECT LAST_INSERT_ID();"""))

def q(s): return "'" + s.replace("'", "''") + "'"

if os.path.exists(os.path.join(HERE, 'created_ids.json')):
    subprocess.run(['python3', os.path.join(HERE, 'cleanup_testdata.py')], check=True)

ids = {k: [] for k in ['job_assignment_notes', 'job_assignment_note_details', 'job_assignment_employees', 'business_trip_assigns',
                       'business_trip_employees', 'overtime_assignments', 'overtime_assignment_employees', 'assign_requests',
                       'assign_request_employees', 'assign_business_tasks']}
def add(t, i): ids[t].append(i); return i

# 1-2. Phiếu giao việc: GV01 chung A+B, GV02 riêng A
for code, text, start, end, emps in [('PGV-TEST-01', 'TEST11523 Gặp KH chung A-B', '08:00', '17:00', [A, B]),
                                     ('PGV-TEST-02', 'TEST11523 Gặp KH riêng A', '13:00', '17:00', [A])]:
    n = add('job_assignment_notes', clone('job_assignment_notes', 'id=28741', {'code': q(code), 'status': 2}))
    add('job_assignment_note_details', clone('job_assignment_note_details', 'id=28851', {
        'job_assignment_note_id': n, 'object_value': q(text),
        'intend_start_at': q(f'{D} {start}:00'), 'intend_end_at': q(f'{D} {end}:00')}))
    for _, ei in emps:
        add('job_assignment_employees', clone('job_assignment_employees', 'job_assignment_note_id=28741', {'job_assignment_note_id': n, 'employee_id': ei}))

# 3. Phiếu công tác (cũ) chung A+B
bt = add('business_trip_assigns', clone('business_trip_assigns', 'id=10389', {
    'status': 2, 'erp_id': 'NULL', 'customer_name': q('TEST11523 Công tác chung A-B'),
    'time_to_go': q(f'{D} 08:00:00'), 'from_time': q(f'{D} 08:00:00'), 'to_time': q(f'{D} 17:00:00')}))
for _, ei in [A, B]:
    add('business_trip_employees', clone('business_trip_employees', 'business_trip_assign_id=10389', {
        'business_trip_assign_id': bt, 'employee_id': ei, 'to_time_actual': 'NULL'}))

# 4. Phiếu làm thêm chung A+B (18:00-21:00)
ot = add('overtime_assignments', clone('overtime_assignments', 'id=4497', {
    'code': q('PLT-TEST-01'), 'overtime_assignment_status': 2, 'allow_app': 1, 'employee_id': A[1],
    'overtime_start_at': q(f'{D} 18:00:00'), 'overtime_end_at': q(f'{D} 21:00:00'),
    'recess_start_at': 'NULL', 'recess_end_at': 'NULL', 'customer_name': q('TEST11523 Làm thêm chung A-B')}))
for _, ei in [A, B]:
    add('overtime_assignment_employees', clone('overtime_assignment_employees', 'overtime_assignment_id=4497', {'overtime_assignment_id': ot, 'employee_id': ei}))

# 5. Phiếu công tác kỹ thuật chung A+B, có 2 công việc được giao
kt = add('assign_requests', clone('assign_requests', 'id=13326', {
    'code': q('PCT-TEST-KT'), 'from_time': q(f'{D} 08:00:00'), 'to_time': q(f'{D} 17:00:00')}))
for src in (17925, 17928):
    add('assign_business_tasks', clone('assign_business_tasks', f'id={src}', {'assign_request_id': kt}))
for emp, _ in [A, B]:
    add('assign_request_employees', clone('assign_request_employees', 'assign_request_id=13326', {'assign_request_id': kt, 'employee_id': emp}))

# 6. Phiếu công tác khác chung A+B+C
kc = add('assign_requests', clone('assign_requests', 'id=13100', {
    'code': q('PCT-TEST-KC'), 'from_time': q(f'{D} 08:00:00'), 'to_time': q(f'{D} 17:00:00'),
    'customer_code': q('TEST11523'), 'customer_name': q('Công tác khác chung A-B-C')}))
for emp, _ in [A, B, C]:
    add('assign_request_employees', clone('assign_request_employees', 'assign_request_id=13100', {'assign_request_id': kc, 'employee_id': emp}))

json.dump(ids, open(os.path.join(HERE, 'created_ids.json'), 'w'), indent=1)
print(json.dumps(ids))
