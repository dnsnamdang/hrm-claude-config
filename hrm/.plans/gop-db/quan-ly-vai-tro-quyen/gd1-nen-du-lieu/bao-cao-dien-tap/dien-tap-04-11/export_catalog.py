"""Danh mục quyền theo Nhóm phân hệ → Phân hệ → Chức năng — DB db_gop_3_11 sau rbac:convert (diễn tập 04/11/2026)."""
import subprocess, io, sys, json, datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.properties import CalcProperties

OUT = sys.argv[1]
DB = 'db_gop_3_11'


def q(sql):
    r = subprocess.run(['mysql', '-uroot', '-h127.0.0.1', '-B', DB, '-e', sql], capture_output=True, text=True, check=True)
    return pd.read_csv(io.StringIO(r.stdout), sep='\t', dtype=str, keep_default_na=False, quoting=3)


perms = q("""
SELECT p.id, p.code, p.name, p.subsystem_group, p.subsystem, p.feature, p.kind, p.allowed_scopes, p.depends_on,
       p.on_erp, p.on_hrm, p.seed_order,
       (SELECT COUNT(DISTINCT rp.role_id) FROM role_has_permissions rp WHERE rp.permission_id=p.id) so_vai_tro,
       (SELECT GROUP_CONCAT(CONCAT(IF(a.legacy_guard='web','ERP','HRM'),': ',a.legacy_name) ORDER BY a.legacy_guard DESC, a.min_scope DESC SEPARATOR '\\n')
          FROM permission_aliases a WHERE a.permission_id=p.id) ten_cu
FROM permissions p WHERE p.code IS NOT NULL AND p.deprecated_at IS NULL""")
ORDER = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'catalog_order.json')))
perms['seed_order'] = perms['code'].map(lambda c: ORDER.get(c, 10**9))
name_by_code = dict(zip(perms['code'], perms['name']))

KIND = {'view': 'Xem', 'action': 'Thao tác', 'approve': 'Duyệt'}
KIND_ORDER = {'view': 0, 'action': 1, 'approve': 2}
SCOPE = {1: 'Bộ phận', 2: 'Phòng ban', 3: 'Công ty', 4: 'Tổng công ty'}

# thứ tự theo danh mục: nhóm/phân hệ/chức năng xếp theo vị trí khai báo đầu tiên
perms['o_g'] = perms.groupby('subsystem_group')['seed_order'].transform('min')
perms['o_s'] = perms.groupby(['subsystem_group', 'subsystem'])['seed_order'].transform('min')
perms['o_f'] = perms.groupby(['subsystem_group', 'subsystem', 'feature'])['seed_order'].transform('min')
perms['o_k'] = perms['kind'].map(KIND_ORDER).fillna(9)
perms = perms.sort_values(['o_g', 'o_s', 'o_f', 'o_k', 'seed_order']).reset_index(drop=True)


def scopes(js):
    try:
        v = json.loads(js) if js and js != 'NULL' else []
    except Exception:
        v = []
    return ' · '.join(SCOPE.get(int(x), str(x)) for x in sorted(v)) if v else ''


def deps(js):
    try:
        v = json.loads(js) if js and js != 'NULL' else []
    except Exception:
        v = []
    return '\n'.join(name_by_code.get(c, c) for c in v)


def platform(r):
    return ' + '.join([x for x, f in (('ERP', r.on_erp), ('HRM', r.on_hrm)) if f == '1'])


FONT = 'Arial'
HEAD = PatternFill('solid', fgColor='D8E7E1')
thin = Side(style='thin', color='BFBFBF')
B = Border(left=thin, right=thin, top=thin, bottom=thin)
note = (f"Nguồn: danh mục quyền (Catalog) trong DB {DB} — dump prod 03/11/2026 sau rbac:convert + cấp mã GĐ3b, xuất "
        f"{datetime.date.today():%d/%m/%Y}. Chỉ quyền đang dùng.")


def header(ws, headers, widths, note_text):
    ws.append([note_text])
    ws['A1'].font = Font(name=FONT, italic=True, size=9, color='6B7280')
    ws.append(headers)
    for i in range(1, len(headers) + 1):
        c = ws.cell(row=2, column=i)
        c.font = Font(name=FONT, bold=True, size=10)
        c.fill = HEAD
        c.alignment = Alignment(vertical='center', wrap_text=True)
        c.border = B
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = 'A3'


def body_style(ws, wrap_cols=()):
    for row in ws.iter_rows(min_row=3, max_row=ws.max_row):
        for c in row:
            c.font = Font(name=FONT, size=10)
            c.border = B
            c.alignment = Alignment(vertical='top', wrap_text=c.column in wrap_cols)


wb = Workbook()
wb.calculation = CalcProperties(fullCalcOnLoad=True)

# Sheet 1 — danh sách quyền phẳng, lọc được
ws = wb.active
ws.title = 'Danh sách quyền'
H = ['STT', 'Nhóm phân hệ', 'Phân hệ', 'Chức năng', 'Quyền', 'Loại', 'Phạm vi cho phép', 'Nền tảng',
     'Cần kèm quyền', 'Tên quyền cũ (trước chuyển đổi)', 'Số vai trò đang gán', 'Mã quyền']
header(ws, H, [6, 20, 22, 34, 50, 10, 34, 11, 34, 60, 11, 50],
       note + " Phạm vi để trống = quyền không có phạm vi. 'Số vai trò đang gán' = số Vai trò (theo công ty) đang có quyền.")
for i, r in enumerate(perms.itertuples(), 1):
    ws.append([i, r.subsystem_group, r.subsystem, r.feature, r.name, KIND.get(r.kind, r.kind), scopes(r.allowed_scopes),
               platform(r), deps(r.depends_on), r.ten_cu.replace('\\n', '\n'), int(r.so_vai_tro), r.code])
body_style(ws, wrap_cols=(9, 10))
ws.auto_filter.ref = f"A2:{get_column_letter(len(H))}{ws.max_row}"
last = ws.max_row

# Sheet 2 — cây chức năng (đếm bằng công thức từ sheet 1)
ws2 = wb.create_sheet('Theo chức năng')
H2 = ['STT', 'Nhóm phân hệ', 'Phân hệ', 'Chức năng', 'Xem', 'Thao tác', 'Duyệt', 'Tổng quyền']
header(ws2, H2, [6, 20, 22, 40, 8, 10, 8, 11], note + " Số đếm là công thức từ sheet 'Danh sách quyền'.")
tree = perms[['subsystem_group', 'subsystem', 'feature']].drop_duplicates().reset_index(drop=True)
rng = lambda col: f"'Danh sách quyền'!${col}$3:${col}${last}"
for i, t in enumerate(tree.itertuples(), 1):
    r = i + 2
    cond = f"{rng('B')},B{r},{rng('C')},C{r},{rng('D')},D{r}"
    ws2.append([i, t.subsystem_group, t.subsystem, t.feature,
                f'=COUNTIFS({cond},{rng("F")},"Xem")', f'=COUNTIFS({cond},{rng("F")},"Thao tác")',
                f'=COUNTIFS({cond},{rng("F")},"Duyệt")', f'=SUM(E{r}:G{r})'])
body_style(ws2)
tot = ws2.max_row + 1
ws2.cell(row=tot, column=4, value='Tổng cộng').font = Font(name=FONT, bold=True, size=10)
for col in 'EFGH':
    c = ws2[f'{col}{tot}']
    c.value = f'=SUM({col}3:{col}{tot - 1})'
    c.font = Font(name=FONT, bold=True, size=10)
    c.border = B
ws2.auto_filter.ref = f"A2:H{tot - 1}"

wb.save(OUT)
kc = perms['kind'].value_counts().to_dict()
print(f"quyền: {len(perms)} · chức năng: {len(tree)} · Xem {kc.get('view',0)} / Thao tác {kc.get('action',0)} / Duyệt {kc.get('approve',0)}")
print('mã thiếu chức năng:', int((perms['feature'] == '').sum()), '· có tên cũ:', int((perms['ten_cu'] != '').sum()))
