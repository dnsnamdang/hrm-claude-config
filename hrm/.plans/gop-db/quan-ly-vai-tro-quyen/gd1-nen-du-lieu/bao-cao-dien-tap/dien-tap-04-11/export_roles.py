"""Xuất Vai trò & Quyền sau chuyển đổi rbac — DB db_gop_3_11 (dump prod 03/11, diễn tập 04/11/2026)."""
import subprocess, io, sys, datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = sys.argv[1]
DB = 'db_gop_3_11'


def q(sql):
    r = subprocess.run(['mysql', '-uroot', '-h127.0.0.1', '-B', DB, '-e', sql], capture_output=True, text=True, check=True)
    return pd.read_csv(io.StringIO(r.stdout), sep='\t', dtype=str, keep_default_na=False, quoting=3)


roles = q("""
SELECT r.id, c.code company_code, c.name company_name, r.base_name, r.name full_name, r.status,
       (SELECT COUNT(DISTINCT h.employee_id) FROM employee_has_roles h JOIN employees e ON e.id=h.employee_id AND e.status=1
         WHERE h.role_id=r.id AND h.company_id=r.company_id) so_nv
FROM roles r JOIN companies c ON c.id=r.company_id
ORDER BY c.id, r.base_name""")

perms = q("""
SELECT r.id role_id, c.code company_code, r.base_name, p.subsystem_group, p.subsystem, p.feature, p.name perm_name, p.code,
       p.kind, rp.scope
FROM roles r JOIN companies c ON c.id=r.company_id
JOIN role_has_permissions rp ON rp.role_id=r.id
JOIN permissions p ON p.id=rp.permission_id AND p.code IS NOT NULL AND p.deprecated_at IS NULL
ORDER BY c.id, r.base_name, p.subsystem_group, p.subsystem, p.feature, FIELD(p.kind,'view','action','approve'), p.name""")

KIND = {'view': 'Xem', 'action': 'Thao tác', 'approve': 'Duyệt'}
SCOPE = {'1': 'Bộ phận', '2': 'Phòng ban', '3': 'Công ty', '4': 'Tổng công ty', '': ''}
perms['kind'] = perms['kind'].map(lambda k: KIND.get(k, k))
perms['scope'] = perms['scope'].map(lambda s: SCOPE.get(s if s != 'NULL' else '', s))

FONT = 'Arial'
HEAD_FILL = PatternFill('solid', fgColor='D8E7E1')
thin = Side(style='thin', color='BFBFBF')
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def write_sheet(ws, title_note, headers, rows, widths):
    ws.append([title_note])
    ws['A1'].font = Font(name=FONT, italic=True, size=9, color='6B7280')
    ws.append(headers)
    for i, _ in enumerate(headers, 1):
        c = ws.cell(row=2, column=i)
        c.font = Font(name=FONT, bold=True, size=10)
        c.fill = HEAD_FILL
        c.alignment = Alignment(vertical='center', wrap_text=True)
        c.border = BORDER
    for row in rows:
        ws.append(row)
    for r in ws.iter_rows(min_row=3, max_row=ws.max_row):
        for c in r:
            c.font = Font(name=FONT, size=10)
            c.border = BORDER
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = 'A3'
    ws.auto_filter.ref = f"A2:{get_column_letter(len(headers))}{ws.max_row}"


wb = Workbook()
note = f"Nguồn: DB {DB} (dump prod 03/11/2026) sau rbac:convert + rbac:grant-role-name-codes, xuất {datetime.date.today():%d/%m/%Y}. Chỉ tính mã đang dùng."

# Sheet 1 — Vai trò (số quyền đếm bằng công thức từ sheet chi tiết)
ws1 = wb.active
ws1.title = 'Vai trò'
n_detail = len(perms) + 2
rows1 = []
for i, r in enumerate(roles.itertuples(), start=3):
    rows1.append([i - 2, r.company_code, r.company_name, r.base_name, r.full_name,
                  'Hoạt động' if r.status == '1' else 'Ngừng', int(r.so_nv),
                  f"=COUNTIFS('Vai trò - Quyền'!$J$3:$J${n_detail},H{i})", int(r.id)])
write_sheet(ws1, note + " Số NV = tài khoản đang hoạt động được gán vai trò tại đúng công ty.",
            ['STT', 'Mã công ty', 'Công ty', 'Vai trò', 'Tên đầy đủ (DB)', 'Trạng thái', 'Số NV', 'Số quyền', 'ID vai trò'],
            [r[:7] + [None, r[8]] for r in rows1], [6, 12, 34, 34, 40, 12, 9, 10, 11])
# đặt công thức Số quyền sau khi ghi (tham chiếu cột I = ID vai trò)
for i in range(3, ws1.max_row + 1):
    ws1.cell(row=i, column=8, value=f"=COUNTIFS('Vai trò - Quyền'!$J$3:$J${n_detail},I{i})").font = Font(name=FONT, size=10)
    ws1.cell(row=i, column=8).border = BORDER

# Sheet 2 — chi tiết
ws2 = wb.create_sheet('Vai trò - Quyền')
rows2 = [[k + 1, p.company_code, p.base_name, p.subsystem_group, p.subsystem, p.feature, p.perm_name, p.kind, p.scope, int(p.role_id), p.code]
         for k, p in enumerate(perms.itertuples())]
write_sheet(ws2, note + " Phạm vi để trống = quyền không có phạm vi.",
            ['STT', 'Mã công ty', 'Vai trò', 'Nhóm phân hệ', 'Phân hệ', 'Chức năng', 'Quyền', 'Loại', 'Phạm vi', 'ID vai trò', 'Mã quyền'],
            rows2, [8, 11, 30, 22, 20, 30, 52, 10, 13, 11, 52])

wb.save(OUT)
print(f"vai trò: {len(roles)} · dòng quyền: {len(perms)} · NV (tổng theo vai trò): {roles['so_nv'].astype(int).sum()}")
