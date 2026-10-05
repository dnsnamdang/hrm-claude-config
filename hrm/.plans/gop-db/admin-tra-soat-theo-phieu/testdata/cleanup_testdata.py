"""Xoá phiếu mẫu do seed_testdata.py tạo + mọi đề nghị tra soát admin/lượt chấm công test sinh ra trên các phiếu đó."""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, 'created_ids.json')
ids = json.load(open(f))
def run(sql):
    r = subprocess.run(['mysql', '-uroot', 'local_hrm_erp'], input=sql, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr)
sql = []
# đề nghị tra soát admin tạo trong lúc test (ngày 29/09) + lượt chấm công của nó
sql.append("""CREATE TEMPORARY TABLE _w AS SELECT id FROM admin_request_update_workings WHERE DATE(from_date)='2026-09-29';
CREATE TEMPORARY TABLE _x AS SELECT x.id, x.timesheet_id FROM admin_request_update_working_employee_timesheets x
  JOIN admin_request_update_working_employees e ON e.id=x.admin_request_update_working_employee_id WHERE e.admin_request_update_working_id IN (SELECT id FROM _w);
DELETE FROM admin_request_update_working_employee_timesheets WHERE id IN (SELECT id FROM _x);
DELETE FROM timesheets WHERE id IN (SELECT timesheet_id FROM _x);
DELETE FROM admin_request_update_working_employees WHERE admin_request_update_working_id IN (SELECT id FROM _w);
DELETE FROM admin_request_update_workings WHERE id IN (SELECT id FROM _w);""")
for t in ['job_assignment_employees', 'job_assignment_note_details', 'job_assignment_notes', 'business_trip_employees', 'business_trip_assigns',
          'overtime_assignment_employees', 'overtime_assignments', 'assign_request_employees', 'assign_business_tasks', 'assign_requests']:
    if ids.get(t): sql.append(f"DELETE FROM {t} WHERE id IN ({','.join(map(str, ids[t]))});")
run('\n'.join(sql))
os.remove(f)
print('Đã xoá dữ liệu test #11523')
