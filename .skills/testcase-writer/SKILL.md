# Testcase Writer — ERP TPE

## Mục đích

Generate file testcase (.xlsx) cho chức năng đã triển khai hoặc đang triển khai, dựa trên code thực tế + design document + business rules.

## Khi nào dùng

- Feature đã code xong hoặc đang code, cần file testcase để QA kiểm thử
- User yêu cầu "viết testcase", "tạo testcase", "tạo file test"

## NGUYÊN TẮC TỐI QUAN TRỌNG — Góc nhìn người dùng cuối

**MẶC ĐỊNH: CHỈ viết testcase theo góc nhìn người dùng cuối (QA thủ công dùng trình duyệt).
KHÔNG viết testcase cho backend / API / database.**

Chỉ viết thêm testcase BE khi user yêu cầu rõ ràng (ví dụ: "viết cả testcase API", "cả FE và BE"). Nếu mơ hồ → hỏi lại, mặc định chỉ UI.

### Quy tắc viết:

1. **Mọi thuật ngữ kỹ thuật đều bị cấm.** Nếu một tester không biết code đọc qua mà không hiểu, tức là viết sai. Cụ thể, không dùng:
   - Thuật ngữ hạ tầng: API, endpoint, HTTP method, status code, payload, request, response, JSON, JWT, header, token
   - Thuật ngữ DB: database, table, column, query, join, index, transaction, tên cột/bảng cụ thể
   - Thuật ngữ code: tên class, method, file, biến, hàm, thuộc tính, CSS class, framework directive (v-model, v-if...)
   - Thuật ngữ ORM/framework: Eloquent relation, whereHas, orderBy, middleware, service, controller, resource

2. **Bước thực hiện mô tả thao tác vật lý của người dùng:** click, nhập, chọn, kéo, mở, đóng, scroll, hover. Không mô tả request/response.

3. **Expected Result mô tả thứ người dùng nhìn/nghe thấy trên UI:** text hiển thị, màu sắc, icon, toast, modal, chuyển trang, trạng thái nút (enable/disable), cập nhật bảng. Không mô tả trạng thái DB hay cấu trúc JSON.

4. **Tên trường dùng chính label trên giao diện**, không dùng tên biến/cột. Ví dụ dùng "Tiến độ (%)" thay vì `progress_pct`, dùng "Trạng thái" thay vì `status`.

5. **Trạng thái / enum dùng tên hiển thị**, không dùng giá trị số/const. Ví dụ dùng "Đã duyệt" thay vì `status=5`, "theo tuần" thay vì `cycle_type=2`.

### Bỏ qua các loại test sau (thuộc phạm vi BE/unit test):

- Authentication, quyền gọi API, token hết hạn (giả định: user đã đăng nhập đúng quyền)
- Validation cấu trúc payload (thiếu field, sai kiểu dữ liệu trong request body)
- Trạng thái DB sau hành động (INSERT/UPDATE record, foreign key)
- Logic query filter BE (whereHas, join, orderBy)
- Format/schema response (đủ field, đúng kiểu)

Thay vào đó, test HÀNH VI user nhìn thấy khi các tình huống trên xảy ra:

| Thay vì test trực tiếp BE                | Test hành vi UI tương ứng                                                  |
| ---------------------------------------- | -------------------------------------------------------------------------- |
| "Server trả 500"                         | "Hiển thị toast đỏ thông báo lỗi"                                          |
| "Validate payload thiếu field → 422"     | (Không xảy ra với user vì UI chặn trước — bỏ qua, hoặc test validation FE) |
| "Insert record vào DB"                   | "Sau khi lưu, bản ghi xuất hiện trên danh sách"                            |
| "BE filter theo quyền phòng ban"         | "User phòng A chỉ nhìn thấy bản ghi của phòng A trên bảng"                 |
| "API trả đúng 3 item"                    | "Bảng hiển thị 3 dòng"                                                     |
| "Status chuyển từ DRAFT sang SUBMITTED"  | "Nhãn trạng thái đổi từ 'Nháp' sang 'Chờ duyệt' màu cam"                   |

### Checklist tự kiểm tra trước khi xuất file:

- [ ] Bước thực hiện có dùng động từ thao tác UI (click, nhập, chọn...) không?
- [ ] Expected Result có kiểm chứng được chỉ bằng mắt nhìn vào trình duyệt không?
- [ ] Không có đoạn nào nhắc đến API, DB, code, framework không?
- [ ] Tên trường/trạng thái dùng label hiển thị, không dùng tên biến/số không?
- [ ] Một QA không biết code đọc qua có hiểu và thực hiện được ngay không?

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

| #     | Section            | Ví dụ                                                       |
| ----- | ------------------ | ----------------------------------------------------------- |
| I     | Trang danh sách    | Hiển thị, tìm kiếm, lọc, phân trang, sort, row actions      |
| II    | Tạo mới            | Form validation, cascading, save draft, save, auto-gen code |
| III   | Sửa                | Load data, edit theo status, save                           |
| IV    | Xoá                | Điều kiện xoá, confirm, cascade delete                      |
| V     | Xuất Excel         | (nếu có) Popup chọn cột, format file                        |
| VI    | Import Excel       | (nếu có) Template, preview, validate, import                |
| VII   | Trang chi tiết     | Readonly, actions, layout                                   |
| VIII+ | Chức năng đặc biệt | Duyệt, tổng hợp, version, v.v.                              |

Tuỳ chức năng mà thêm/bớt section. Đặt tên section dạng: `I. TRANG DANH SÁCH [TÊN] ([route])`.

### Bước 3: Viết testcase theo format

Mỗi testcase là 1 dòng trong bảng Excel, gồm các cột:

| Cột | Field           | Mô tả                                              | Bắt buộc                    |
| --- | --------------- | -------------------------------------------------- | --------------------------- |
| A   | Module          | Tên module (VD: BOM List)                          | Có                          |
| B   | Nhóm chức năng  | Tên nhóm (VD: BOM List)                            | Có                          |
| C   | TC ID           | Mã testcase, format: `PREFIX_NNN.NNN`              | Có                          |
| D   | Chức năng       | Mô tả ngắn testcase                                | Có                          |
| E   | Priority        | P0 (critical), P1 (important), P2 (nice-to-have)   | Có                          |
| F   | Tiền điều kiện  | Trạng thái cần có trước khi test                   | Không                       |
| G   | Bước thực hiện  | Các bước số, xuống dòng bằng `\n`                  | Có                          |
| H   | Test Data       | Dữ liệu test cụ thể                                | Không                       |
| I   | Test Data       | (cột phụ, merge header với H)                      | Không                       |
| J   | Expected Result | Kết quả mong đợi chi tiết                          | Có                          |
| K   | KQ thực tế      | QA điền khi test                                   | Không                       |
| L   | Status          | Dropdown: Passed / Failed / Pending / Not Executed | Có (mặc định: Not Executed) |
| M   | Ghi chú         | Ghi chú thêm                                       | Không                       |

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
