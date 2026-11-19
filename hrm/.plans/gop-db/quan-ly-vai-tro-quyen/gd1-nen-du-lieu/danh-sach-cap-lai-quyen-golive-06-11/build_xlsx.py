"""Dựng danh-sach-cap-lai-quyen.xlsx từ báo cáo rbac:convert + DB đã chuyển đổi.

Chạy: python3 build_xlsx.py <thư mục chứa 3 file tsv> <thư mục gd1-nen-du-lieu>
(script đọc báo cáo ở <gd1>/bao-cao-dien-tap/chay-that — lúc go-live đổi biến SRC sang thư mục báo cáo của lần chạy go-live).

3 file tsv xuất từ DB đã chuyển đổi (mysql -N -B -e "<SQL>" > file):
  emp.tsv : select e.id, ei.fullname, ei.code, ei.status, ei.company_id from employees e join employee_infos ei on ei.id=e.employee_info_id
  cty.tsv : select id, code, name from companies
  gd2c.tsv: select h.employee_id, r.company_id, r.id, r.name, count(*) from role_has_permissions x join roles r on r.id=x.role_id
            join employee_has_roles h on h.role_id=r.id join employees e on e.id=h.employee_id
            join employee_infos ei on ei.id=e.employee_info_id and ei.status=1
            where x.scope=4 and r.company_id<>1 group by h.employee_id, r.id
"""
import csv, collections, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
S, BASE = sys.argv[1], sys.argv[2]
SRC = f'{BASE}/bao-cao-dien-tap/golive-06-11'; OUT = f'{BASE}/danh-sach-cap-lai-quyen-golive-06-11'
emp = {l.split('\t')[0]: l.rstrip('\n').split('\t') for l in open(f'{S}/emp.tsv', encoding='utf-8')}
cty = {l.split('\t')[0]: l.rstrip('\n').split('\t')[1] for l in open(f'{S}/cty.tsv', encoding='utf-8')}
act = lambda e: e in emp and emp[e][3] == '1'
def rd(f, src=SRC): return list(csv.DictReader(open(f'{src}/{f}', encoding='utf-8-sig')))

F = 'Arial'; thin = Side(style='thin', color='BFBFBF')
HDR = PatternFill('solid', fgColor='1F4E78'); FILL = PatternFill('solid', fgColor='FFF2CC')
wb = Workbook(); wb.remove(wb.active)

def sheet(title, note, headers, rows, widths, fill_cols=('Quyết định xử lý', 'Ghi chú')):
    ws = wb.create_sheet(title)
    ws['A1'] = title; ws['A1'].font = Font(name=F, bold=True, size=13, color='1F4E78')
    ws['A2'] = note; ws['A2'].font = Font(name=F, italic=True, size=10, color='595959')
    ws['A2'].alignment = Alignment(wrap_text=True, vertical='top')
    allh = list(headers) + list(fill_cols)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(allh)); ws.row_dimensions[2].height = 48
    for i, h in enumerate(allh, 1):
        c = ws.cell(row=4, column=i, value=h)
        c.font = Font(name=F, bold=True, color='FFFFFF'); c.fill = HDR if h not in fill_cols else PatternFill('solid', fgColor='BF8F00')
        c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center'); c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    ws.row_dimensions[4].height = 34
    for r, row in enumerate(rows, 5):
        for i, v in enumerate(list(row) + [''] * len(fill_cols), 1):
            c = ws.cell(row=r, column=i, value=v)
            c.font = Font(name=F, size=10); c.alignment = Alignment(wrap_text=True, vertical='top'); c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
            if i > len(headers): c.fill = FILL
    for i, w in enumerate(list(widths) + [22, 30], 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = 'A5'
    ws.auto_filter.ref = f'A4:{get_column_letter(len(allh))}{max(4, 4 + len(rows))}'
    return ws

# 1 + 1b: bit ro
r = [x for x in rd('mat-do-bit-ro.csv') if act(x['employee_id'])]
g = collections.defaultdict(list)
for x in r: g[(x['employee_id'], x['company_id'])].append(x)
rows1 = []
for (e, c), xs in sorted(g.items(), key=lambda kv: (-len(kv[1]), int(kv[0][0]))):
    names = sorted({x['ten_cu'] for x in xs})
    rows1.append([int(e), emp[e][2], emp[e][1], cty.get(emp[e][4], emp[e][4]), cty.get(c, c), len(xs),
                  sum(x['guard'] == 'api' for x in xs), sum(x['guard'] == 'web' for x in xs),
                  ' ; '.join(names[:15]) + (' ; …' if len(names) > 15 else '')])
rows1b = sorted([[int(x['employee_id']), emp[x['employee_id']][2], emp[x['employee_id']][1], cty.get(x['company_id'], x['company_id']),
                  'HRM' if x['guard'] == 'api' else 'ERP', x['ten_cu']] for x in r], key=lambda v: (v[0], v[3], v[4], v[5]))
# 2 mat cong ty
r2 = [x for x in rd('mat-do-cong-ty-qua-vai-tro.csv') if act(x['employee_id'])]
roles_old = dict(l.rstrip('\n').split('\t', 1) for l in open(f'{S}/roles_old.tsv', encoding='utf-8'))
rows2 = [[int(x['employee_id']), emp[x['employee_id']][2], x['ten_nhan_vien'], x['ma_cong_ty'],
          ', '.join(f"{i} – {roles_old.get(i, '?')}" for i in x['vai_tro'].split()), int(x['so_khoa_api']),
          int(x['so_khoa_dung_duoc_tren_giao_dien']), x['ten_dung_duoc'][:600]] for x in r2]
# 3 gd2c
gg = collections.defaultdict(list)
for l in open(f'{S}/gd2c.tsv', encoding='utf-8'):
    e, c, rid, rn, cnt = l.rstrip('\n').split('\t'); gg[(e, c)].append((rn, int(cnt)))
rows3 = [[int(e), emp[e][2], emp[e][1], cty.get(c, c), len(v), sum(n for _, n in v), ' ; '.join(f'{rn} ({n} quyền)' for rn, n in v)]
         for (e, c), v in sorted(gg.items(), key=lambda kv: (cty.get(kv[0][1], ''), int(kv[0][0])))]
# 5 thieu quyen xem
rows5 = [[int(x['role_id']), x['ten_vai_tro'], cty.get(x['company_id'], x['company_id']), x['ma'], x['ma_thieu']]
         for x in rd('thieu-quyen-xem.csv')]
# 6 du lieu tro role id
lydo = {'cong_ty_khong_co_trong_map': 'Vai trò cũ không có bản ở công ty của dòng dữ liệu', 'khong_xac_dinh_cong_ty': 'Không xác định được công ty của dòng dữ liệu'}
bang = {'companies': 'Công ty – Phó giám đốc (deputy_role)', 'self_inventory_members': 'Thành viên tự kiểm kê', 'position_inventory_members': 'Thành viên kiểm kê vị trí',
        'inland_buy_contracts': 'HĐ mua trong nước', 'inland_buy_contract_annexes': 'Phụ lục HĐ mua trong nước', 'rule_inland_buy_contracts': 'HĐ nguyên tắc mua trong nước',
        'inland_buy_contract_news': 'HĐ mua trong nước (mới)'}
rows6 = [[bang.get(x['bang'], x['bang']), x['bang'], x['cot'], int(x['role_id']), x['ten_vai_tro'], cty.get(x['company_id'], x['company_id']), int(x['so_dong']),
          lydo.get(x['ly_do'], x['ly_do']), x['ghi_chu']] for x in rd('du-lieu-tro-role-id.csv')
         if x['bang'] != 'role_permission_history' and not x['bang'].startswith('ngoai_repo')]

# Huong dan
ws = wb.create_sheet('Hướng dẫn', 0)
ws['A1'] = 'Danh sách người dùng / vai trò cần xem xét cấp lại quyền sau chuyển đổi phân quyền mới'
ws['A1'].font = Font(name=F, bold=True, size=14, color='1F4E78')
info = [
 'Nguồn: báo cáo lần chuyển đổi THẬT trên prod 06/11/2026 (rbac:convert lúc 20:41). Chỉ tính nhân viên đang làm việc.',
 'Sửa quyền ở HRM: Quản trị › Vai trò (/admin/roles) và Vai trò nhân viên (/admin/employee-roles). File này thay thế bản diễn tập 03/11.',
 'Cột màu vàng (Quyết định xử lý, Ghi chú) để quản trị viên ghi việc đã làm. Ví dụ: "Đã gán TPE_Giám đốc tại TPE – 07/11" / "Không cần – đã nghỉ phụ trách".',
 'Lập: 06/11/2026.',
]
for i, t in enumerate(info, 2):
    ws.cell(row=i, column=1, value=t).font = Font(name=F, size=10, italic=(i != 4)); ws.cell(row=i, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=5); ws.row_dimensions[i].height = 30
hdr = ['Sheet', 'Nội dung', 'Quy mô', 'Việc quản trị viên làm', 'Mức ưu tiên']
for i, h in enumerate(hdr, 1):
    c = ws.cell(row=7, column=i, value=h); c.font = Font(name=F, bold=True, color='FFFFFF'); c.fill = HDR; c.alignment = Alignment(horizontal='center', vertical='center'); c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
n1, nv1 = len(rows1), len({x[0] for x in rows1}); big = sum(x[5] > 100 for x in rows1)
guide = [
 ['1. Mất quyền do bịt rò', 'Quyền nhân viên có được CHỈ nhờ cách tính cũ không xét công ty của vai trò / dòng cấp quyền. Sau chuyển đổi bị đóng.', f'{nv1} nhân viên · {n1} cặp nhân viên × công ty · {len(rows1b)} quyền ({big} cặp mất > 100 quyền)', 'Xét từng người: quyền nào thật sự cần ở công ty đó thì gán Vai trò của chính công ty đó (màn Vai trò nhân viên) hoặc thêm quyền vào Vai trò. Xem tên từng quyền ở sheet 1b.', 'Cao (ưu tiên cặp mất nhiều quyền)'],
 ['1b. Chi tiết bịt rò', 'Từng quyền bị mất của sheet 1 (mỗi dòng 1 quyền).', f'{len(rows1b)} dòng', 'Lọc theo mã NV / công ty để biết đúng quyền cần cấp lại.', 'Tra cứu'],
 ['2. Mất truy cập công ty', 'Nhân viên MẤT HẲN quyền vào một công ty — trước có nhờ danh sách công ty gắn trên vai trò, nay vai trò không có bản ở công ty đó.', f'{len({x[0] for x in rows2})} nhân viên · {len(rows2)} dòng', 'Gán Vai trò tương ứng của từng công ty cho người cần làm việc ở đó.', 'Cao'],
 ['3. GĐ2c hạ phạm vi', 'Chủ ý (chốt 01/11): 6 công ty khác TPE tắt phạm vi Tổng công ty ⇒ quyền phạm vi Tổng công ty tính như phạm vi Công ty.', f'{len({x[0] for x in rows3})} nhân viên · {len(rows3)} cặp', 'KHÔNG cấp lại — chỉ báo người dùng biết. Muốn mở lại cho công ty nào thì bật ở màn Cấu hình phạm vi Tổng công ty.', 'Thông báo'],
 ['4. GĐ3b', 'Duyệt vượt hạn mức HĐ dự án TKT + phạm vi xoá liên hệ khách hàng (HRM) nay chỉ tính quyền ở công ty đang làm.', '1 nhân viên', 'Nếu cần duyệt ở TPE: gán Vai trò TPE_Giám đốc tại TPE.', 'Trung bình'],
 ['5. Vai trò thiếu quyền Xem', 'Vai trò có quyền thao tác (duyệt/sửa…) nhưng thiếu quyền Xem đi kèm ⇒ có nút mà không mở được màn.', f'{len({x[0] for x in rows5})} vai trò · {len(rows5)} dòng', 'Thêm quyền Xem còn thiếu vào vai trò, hoặc bỏ quyền thao tác nếu không dùng.', 'Trung bình'],
 ['6. Cấu hình trỏ vai trò', 'Cấu hình nghiệp vụ đang trỏ vào vai trò không chuyển được sang vai trò mới của đúng công ty.', f'{len(rows6)} dòng', 'Mở cấu hình tương ứng, chọn lại vai trò của đúng công ty.', 'Trung bình'],
 ['(không có sheet)', 'Vai trò không chuyển được: 0.', '', 'Không cần làm gì.', 'Không'],
]
for r_, row in enumerate(guide, 8):
    for i, v in enumerate(row, 1):
        c = ws.cell(row=r_, column=i, value=v); c.font = Font(name=F, size=10, bold=(i == 1)); c.alignment = Alignment(wrap_text=True, vertical='top'); c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
for i, w in enumerate([26, 60, 34, 60, 18], 1): ws.column_dimensions[get_column_letter(i)].width = w

sheet('1. Mất quyền do bịt rò', 'Mỗi dòng = 1 nhân viên × 1 công ty bị mất quyền do đóng chỗ "rò" (cách tính cũ không xét công ty). Sắp theo số quyền mất giảm dần. Tên từng quyền: sheet 1b.',
      ['Mã NV (id)', 'Mã nhân viên', 'Họ tên', 'Công ty trong hồ sơ', 'Công ty bị mất quyền', 'Số quyền mất', 'Trong đó HRM', 'Trong đó ERP', 'Ví dụ (tối đa 15 tên quyền)'], rows1, [10, 13, 24, 14, 14, 11, 10, 10, 90])
sheet('1b. Chi tiết bịt rò', 'Từng quyền bị mất (sheet 1). Lọc theo Mã NV / Công ty.', ['Mã NV (id)', 'Mã nhân viên', 'Họ tên', 'Công ty bị mất quyền', 'Hệ thống', 'Tên quyền'], rows1b, [10, 13, 24, 14, 10, 70])
sheet('2. Mất truy cập công ty', 'Nhân viên mất hẳn quyền vào công ty — trước có nhờ danh sách công ty gắn trên vai trò cũ.',
      ['Mã NV (id)', 'Mã nhân viên', 'Họ tên', 'Công ty bị mất', 'Vai trò cũ (id – tên)', 'Số quyền mất', 'Số quyền dùng được trên giao diện', 'Ví dụ tên quyền dùng được'], rows2, [10, 13, 24, 12, 30, 10, 14, 90])
sheet('3. GĐ2c hạ phạm vi', 'Chủ ý: công ty bị tắt phạm vi Tổng công ty ⇒ các quyền phạm vi Tổng công ty dưới đây chỉ còn hiệu lực như phạm vi Công ty. Không cần cấp lại.',
      ['Mã NV (id)', 'Mã nhân viên', 'Họ tên', 'Công ty', 'Số vai trò bị hạ', 'Số quyền bị hạ', 'Vai trò (số quyền phạm vi Tổng công ty)'], rows3, [10, 13, 24, 14, 10, 10, 90])
sheet('4. GĐ3b', 'Duyệt vượt hạn mức HĐ dự án TKT + phạm vi xoá liên hệ khách hàng ở HRM chỉ tính quyền ở công ty đang làm (đo 02/11 trên rehearsal).',
      ['Mã NV (id)', 'Họ tên', 'Vai trò Giám đốc ở công ty', 'Công ty đang làm', 'Chức năng bị ảnh hưởng', 'Cách xử lý gợi ý'],
      [[197, 'Trần Thị Hương', 'DTTDETEK', 'TPE', 'Duyệt hợp đồng vượt hạn mức (HĐ dự án TKT); xoá liên hệ khách hàng theo phạm vi', 'Gán Vai trò TPE_Giám đốc tại TPE (nếu cần duyệt ở TPE)']], [10, 22, 18, 14, 50, 40])
sheet('5. Vai trò thiếu quyền Xem', 'Vai trò có quyền thao tác nhưng thiếu quyền Xem đi kèm ⇒ có nút mà không mở được màn.',
      ['Mã vai trò (id)', 'Tên vai trò', 'Công ty', 'Quyền thao tác đang có (mã)', 'Quyền Xem còn thiếu (mã)'], rows5, [12, 40, 14, 50, 50])
sheet('6. Cấu hình trỏ vai trò', 'Dữ liệu cấu hình trỏ vào vai trò không chuyển được sang vai trò mới của đúng công ty ⇒ chọn lại.',
      ['Cấu hình', 'Bảng', 'Cột', 'Mã vai trò cũ (id)', 'Tên vai trò cũ', 'Công ty', 'Số dòng', 'Lý do', 'Ghi chú kỹ thuật'], rows6, [30, 26, 18, 12, 30, 12, 9, 34, 50])
p = f'{OUT}/danh-sach-cap-lai-quyen.xlsx'; wb.save(p); print(p)
for w in wb.worksheets: print(w.title, w.max_row)
