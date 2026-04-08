# Testcase Writer — ERP TPE

## Mục đích
Generate file testcase (.xlsx) cho chức năng đã triển khai hoặc đang triển khai, dựa trên code thực tế + design document + business rules.

## Khi nào dùng
- Feature đã code xong hoặc đang code, cần file testcase để QA kiểm thử
- User yêu cầu "viết testcase", "tạo testcase", "tạo file test"

## Input cần thiết
1. Tên chức năng + module (VD: BOM List, module Assign)
2. `.plans/[feature]/design.md` (nếu có)
3. `.plans/[feature]/plan.md` (nếu có)
4. Code BE: Routes, Controller, Service, Entity/Model (đọc constants, relationships, validation rules)
5. Code FE: Pages, Components chính (đọc UI flow, form fields, actions, filters)

## Quy trình

### Bước 1: Thu thập thông tin từ code

**BE — đọc theo thứ tự:**
```
1. Routes/api.php → danh sách endpoint (CRUD + action đặc biệt)
2. Controller → method nào, request validation nào
3. Request → rules validation (required, format, điều kiện)
4. Service → business logic, điều kiện xoá, điều kiện chuyển trạng thái
5. Entity/Model → constants (STATUS_*), relationships, accessor (is_can_delete, is_can_edit)
6. Resource/Transformer → data trả về cho FE
```

**FE — đọc theo thứ tự:**
```
1. Trang danh sách → columns, filters, actions, phân trang, sort
2. Trang tạo/sửa → form fields, validation FE, cascading logic, submit flow
3. Trang chi tiết → readonly fields, actions (sửa, xuất, xoá)
4. Components đặc biệt → modal, import, export, popup
5. constants.js → trạng thái, loại
```

### Bước 2: Phân nhóm testcase

Chia thành các nhóm (section) theo luồng chức năng. Mỗi chức năng CRUD thường có:

| # | Section | Ví dụ |
|---|---------|-------|
| I | Trang danh sách | Hiển thị, tìm kiếm, lọc, phân trang, sort, row actions |
| II | Tạo mới | Form validation, cascading, save draft, save, auto-gen code |
| III | Sửa | Load data, edit theo status, save |
| IV | Xoá | Điều kiện xoá, confirm, cascade delete |
| V | Xuất Excel | (nếu có) Popup chọn cột, format file |
| VI | Import Excel | (nếu có) Template, preview, validate, import |
| VII | Trang chi tiết | Readonly, actions, layout |
| VIII+ | Chức năng đặc biệt | Duyệt, tổng hợp, version, v.v. |

Tuỳ chức năng mà thêm/bớt section. Đặt tên section dạng: `I. TRANG DANH SÁCH [TÊN] ([route])`.

### Bước 3: Viết testcase theo format

Mỗi testcase là 1 dòng trong bảng Excel, gồm các cột:

| Cột | Field | Mô tả | Bắt buộc |
|-----|-------|-------|----------|
| A | Module | Tên module (VD: BOM List) | Có |
| B | Nhóm chức năng | Tên nhóm (VD: BOM List) | Có |
| C | TC ID | Mã testcase, format: `PREFIX_NNN.NNN` | Có |
| D | Chức năng | Mô tả ngắn testcase | Có |
| E | Priority | P0 (critical), P1 (important), P2 (nice-to-have) | Có |
| F | Tiền điều kiện | Trạng thái cần có trước khi test | Không |
| G | Bước thực hiện | Các bước số, xuống dòng bằng `\n` | Có |
| H | Test Data | Dữ liệu test cụ thể | Không |
| I | Test Data | (cột phụ, merge header với H) | Không |
| J | Expected Result | Kết quả mong đợi chi tiết | Có |
| K | KQ thực tế | QA điền khi test | Không |
| L | Status | Dropdown: Passed / Failed / Pending / Not Executed | Có (mặc định: Not Executed) |
| M | Ghi chú | Ghi chú thêm | Không |

### Quy tắc đặt TC ID:
- Format: `PREFIX_NNN.NNN`
- PREFIX: viết tắt của chức năng (VD: BOM, TASK, ISSUE)
- NNN đầu: số thứ tự section (001 = Danh sách, 002 = Tạo mới, ...)
- NNN sau: số thứ tự testcase trong section (001, 002, ...)
- Ví dụ: `BOM_001.001`, `BOM_002.003`, `TASK_003.005`

### Quy tắc Priority:
- **P0**: Luồng chính, CRUD cơ bản, validation bắt buộc, phân quyền, hiển thị đúng data
- **P1**: Filter nâng cao, format hiển thị, edge case quan trọng
- **P2**: UI polish, tuỳ chỉnh cột, kéo thả, trải nghiệm phụ

### Quy tắc viết nội dung:
- **Bước thực hiện**: Đánh số `1. ... \n2. ...`, ngắn gọn, cụ thể
- **Expected Result**: Chi tiết, có thể kiểm chứng được. Nếu liên quan DB thì ghi rõ table + field
- **Tiền điều kiện**: Ghi rõ trạng thái, role, data cần có
- **Test Data**: Ghi giá trị cụ thể nếu cần (VD: `Keyword: PLC`, `Từ: 01/03/2026`)

### Bước 4: Generate file Excel bằng Python (openpyxl)

Dùng script Python với openpyxl để tạo file `.xlsx`. **BẮT BUỘC** tuân thủ format sau:

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "[Tên sheet]"

# === STYLES ===
thin_border = Border(
    left=Side(style='thin', color='FF000000'),
    right=Side(style='thin', color='FF000000'),
    top=Side(style='thin', color='FF000000'),
    bottom=Side(style='thin', color='FF000000'),
)

title_font = Font(bold=True, size=14, color='FF1F4E79')
header_font = Font(bold=True, size=11, color='FFFFFFFF')
header_fill = PatternFill(start_color='FF4472C4', end_color='FF4472C4', fill_type='solid')
header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

section_font = Font(bold=True, size=11, color='FF1F4E79')
section_fill = PatternFill(start_color='FFD6E4F0', end_color='FFD6E4F0', fill_type='solid')

data_font = Font(size=11, color='FF000000')
data_alignment = Alignment(vertical='top', wrap_text=True)

summary_font = Font(size=11, color='FF000000')

# === COLUMN WIDTHS ===
col_widths = {
    'A': 14, 'B': 18, 'C': 16, 'D': 35, 'E': 10,
    'F': 30, 'G': 45, 'H': 20, 'I': 12, 'J': 50,
    'K': 15, 'L': 14, 'M': 15
}
for col_letter, width in col_widths.items():
    ws.column_dimensions[col_letter].width = width

# === ROW 1: Title + Test Summary ===
ws.merge_cells('A1:E1')
ws['A1'] = f'Testcase _ [Tên chức năng]'
ws['A1'].font = title_font

ws.merge_cells('F1:I1')
ws['F1'] = 'TEST SUMMARY'
ws['F1'].font = summary_font

# Summary formulas (rows 1-5, columns J-K)
summary_labels = [
    ('Số trường hợp kiểm thử đạt (P):', '=COUNTIF(L8:L500,"Passed")'),
    ('Số trường hợp kiểm thử không đạt (F):', '=COUNTIF(L8:L500,"Failed")'),
    ('Số trường hợp kiểm thử đang xem xét (PE):', '=COUNTIF(L8:L500,"Pending")'),
    ('Số trường hợp kiểm thử chưa thực hiện:', '=COUNTIF(L8:L500,"Not Executed")'),
    ('Tổng số trường hợp kiểm thử:', '=COUNTA(L8:L500)'),
]
for i, (label, formula) in enumerate(summary_labels):
    ws.cell(row=i+1, column=10, value=label).font = summary_font
    ws.cell(row=i+1, column=11, value=formula).font = summary_font

# === ROW 6: Header ===
headers = ['Module', 'Nhóm chức năng', 'TC ID', 'Chức năng', 'Priority',
           'Tiền điều kiện', 'Bước thực hiện', 'Test Data', 'Test Data',
           'Expected Result (chi tiết)', 'KQ thực tế', 'Status', 'Ghi chú']
ws.row_dimensions[6].height = 30
for col_idx, header in enumerate(headers, 1):
    cell = ws.cell(row=6, column=col_idx, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_alignment
    cell.border = thin_border

# === DATA ROWS ===
current_row = 7  # Bắt đầu từ row 7

def write_section_row(row, title):
    """Viết dòng section header (merge C:M, nền xanh nhạt)"""
    ws.merge_cells(f'C{row}:M{row}')
    cell = ws.cell(row=row, column=3, value=title)
    cell.font = section_font
    cell.fill = section_fill

def write_tc_row(row, module, group, tc_id, func, priority,
                 precondition='', steps='', test_data='',
                 expected='', status='Not Executed'):
    """Viết 1 dòng testcase"""
    values = [module, group, tc_id, func, priority,
              precondition, steps, test_data, '', expected, '', status, '']
    for col_idx, val in enumerate(values, 1):
        cell = ws.cell(row=row, column=col_idx, value=val)
        cell.font = data_font
        cell.alignment = data_alignment
        cell.border = thin_border

# Viết data...
# write_section_row(current_row, 'I. TRANG DANH SÁCH ...')
# current_row += 1
# write_tc_row(current_row, ...)
# current_row += 1

# === DATA VALIDATION cho cột Status ===
from openpyxl.worksheet.datavalidation import DataValidation
dv = DataValidation(
    type='list',
    formula1='"Passed,Failed,Pending,Not Executed"',
    allow_blank=True,
)
dv.error = 'Chọn 1 trong 4 giá trị'
dv.errorTitle = 'Giá trị không hợp lệ'
ws.add_data_validation(dv)
dv.add(f'L8:L500')

# === SAVE ===
output_path = '.plans/[feature]/Testcase_[Name].xlsx'
wb.save(output_path)
print(f'Saved: {output_path}')
```

### Bước 5: Review & bổ sung

Sau khi generate, kiểm tra:
1. Đủ section cho tất cả luồng chức năng không?
2. Có cover edge case quan trọng không? (empty state, quyền, concurrent, data lớn)
3. TC ID có liên tục, không trùng?
4. Expected Result có đủ chi tiết để QA verify?

## Checklist testcase cần cover cho mỗi loại màn hình

### Trang danh sách:
- [ ] Hiển thị layout đúng (tiêu đề, cột)
- [ ] Tìm kiếm nhanh
- [ ] Từng filter nâng cao (1 TC / filter)
- [ ] Reset filter
- [ ] Phân trang + sort
- [ ] Row actions hiện theo điều kiện (status, quyền, owner)
- [ ] Phân quyền xem (nếu có: theo công ty/phòng ban/bộ phận)
- [ ] Data chỉ hiện cho owner (nếu có trạng thái nháp)

### Trang tạo mới:
- [ ] Cascading field (chọn A → tự fill B)
- [ ] Validation từng field bắt buộc
- [ ] Lưu nháp (nếu có)
- [ ] Lưu chính thức
- [ ] Auto-gen code/mã
- [ ] Thêm/xoá item con
- [ ] company/department/part tự fill từ user

### Trang sửa:
- [ ] Load data đúng
- [ ] Button hiện/ẩn theo status
- [ ] Form disabled theo status
- [ ] Save + reload đúng

### Xoá:
- [ ] Điều kiện xoá (status, owner, quyền)
- [ ] Confirm modal
- [ ] Cascade delete (xoá con trước)

### Xuất Excel (nếu có):
- [ ] Popup chọn cột
- [ ] Select all / deselect all
- [ ] Format file đúng (font, số tiền, header)
- [ ] Xuất từ danh sách vs chi tiết

### Import Excel (nếu có):
- [ ] Download template
- [ ] Preview
- [ ] Validate từng rule
- [ ] Import thành công
- [ ] Mapping data đúng (cha/con, lookup)

### Trang chi tiết:
- [ ] Readonly — không có input
- [ ] Ẩn action buttons
- [ ] Layout không lệch
- [ ] Footer actions (sửa, xuất)

### Duyệt/Phê duyệt (nếu có):
- [ ] Ai được duyệt (quyền)
- [ ] Duyệt thành công → chuyển status
- [ ] Từ chối + lý do
- [ ] Không duyệt lại hồ sơ đã duyệt

## Output
File `.xlsx` lưu tại: `.plans/[feature]/Testcase_[Tên chức năng].xlsx`
