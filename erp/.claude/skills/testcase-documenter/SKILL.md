---
name: testcase-documenter
description: Generate tài liệu test case cho feature đã triển khai — output Excel (.xlsx) đầy đủ block mô tả nghiệp vụ + summary + phân quyền + 3 cột check
---

# Test Case Documenter — ERP TPE

## Mục đích
Generate test cases cho feature/báo cáo đã hoặc sắp triển khai. Output gồm:
1. **File Excel (.xlsx)** — chuẩn QA dùng test thực tế (dropdown Status, công thức tổng hợp, 3 lần check)
2. **File HTML** (tuỳ chọn) — review nhanh, in A4

File Excel chuẩn phải có **ĐỦ 4 KHỐI** theo đúng thứ tự (xem mục Layout bên dưới):
1. Khối **MÔ TẢ TÍNH NĂNG / BÁO CÁO** (9 mục cố định)
2. Khối **TEST SUMMARY** (5 công thức COUNTIF)
3. **Header testcase** (15 cột) + (nếu có phân quyền) section **TC-ROLE**
4. **Các section testcase** đánh số La mã

## Khi nào dùng
- Feature/báo cáo đã code xong, cần test case cho QA
- User yêu cầu "tạo testcase", "viết test case", "viết test"

## Input cần thiết
1. **Bắt buộc**: Tên feature + module, SRS hoặc design.md (use case + business rules)
2. **Tự thu thập từ code**: Routes, Controller, Service, Entity, Request, FE Pages/Components, Plan.md

## Layout file Excel (chuẩn) — TUYỆT ĐỐI tuân thủ

```
Row 1  : "MÔ TẢ TÍNH NĂNG (đọc trước khi xem testcase)" (merge B1:O1, nền đậm)
Row 2  : 1. Mục đích tính năng              | <nội dung>
Row 3  : 2. Đối tượng được tính / hiển thị  | <nội dung — liệt kê đầy đủ status, điều kiện>
Row 4  : 3. Đối tượng bị ẩn / không tính    | <nội dung>
Row 5  : 4. Bộ lọc thời gian áp dụng cho    | <nội dung — chỉ rõ cột nào, range nào>
Row 6  : 5. Cấu trúc dữ liệu / cây phân cấp | <nội dung>
Row 7  : 6. Quy tắc cộng dồn / deduplicate  | <nội dung>
Row 8  : 7. Phân quyền cấp                  | <liệt kê từng permission code>
Row 9  : 8. Cách tính các ô thống kê        | <công thức từng ô>
Row 10 : 9. Ghi chú đọc bảng                | <phân trang, định dạng…>

Row 11 : "Testcase _ <Tên feature>"         (col A, merge B11:O11)
Row 11 col F: "TEST SUMMARY" (merge F11:H11)
Row 11 col I: "Số trường hợp kiểm thử đạt (P):"     | L11: =COUNTIF(L18:N500,"Passed")
Row 12 col I: "Số trường hợp kiểm thử không đạt (F):"| L12: =COUNTIF(L18:N500,"Failed")
Row 13 col I: "Số trường hợp kiểm thử đang xem xét:" | L13: =COUNTIF(L18:N500,"Pending")
Row 14 col I: "Số trường hợp kiểm thử chưa thực hiện:"| L14: =COUNTIF(L18:N500,"Not Executed")
Row 15 col I: "Tổng số trường hợp kiểm thử:"         | L15: =COUNTIF(L18:N500,"<>")

Row 16 : (trống — spacing)

Row 17 : HEADER 15 cột
  A Module | B Nhóm chức năng | C TC ID | D Chức năng | E Priority
  F Tiền điều kiện | G Bước thực hiện | H Test Data
  I Expected Result (chi tiết) | J Giải thích nghiệp vụ | K KQ thực tế
  L trạng thái check lần 1 | M trạng thái check lần 2 | N trạng thái check lần 3
  O Ghi chú

Row 18+: Data — bắt đầu bằng section "TC-ROLE" (nếu có phân quyền), sau đó section La mã
```

### Quy tắc nội dung 9 mục mô tả
- **Không bỏ mục nào**. Nếu feature không áp dụng, ghi "—" hoặc "Không áp dụng" + 1 dòng lý do
- Mục 2 & 3 (đối tượng tính / ẩn) **PHẢI liệt kê từng status / điều kiện cụ thể**, không nói chung chung
- Mục 7 (phân quyền) **PHẢI liệt kê đầy đủ tên permission code** đã định nghĩa trong code
- Mục 8 (công thức) viết dạng: `Ô X = <công thức>`, ví dụ `Ô 'Quá hạn' = COUNT(due_date < today)`

## Phân loại + đánh số section

### Section "Phân quyền & truy cập" (CHỈ khi feature phân quyền theo cấp)
- Đứng **đầu tiên** sau header (trước section La mã)
- ID format: `TC-ROLE-01`, `TC-ROLE-02`, ...
- Liệt kê 1 TC cho **TỪNG permission code** (vd: "Xem … theo tổng công ty", "… theo công ty", "… theo phòng ban", "… không có quyền")
- Nếu feature không phân cấp → bỏ qua section này

### Sections nghiệp vụ — đánh số La mã
```
I.   HIỂN THỊ TRANG & TRUY CẬP
II.  BỘ LỌC & TÌM KIẾM
III. STATS / THỐNG KÊ ĐẦU TRANG
IV.  DANH SÁCH / GRID DỮ LIỆU
V.   CHỨC NĂNG CHÍNH (CRUD / action)
VI.  EDGE CASES & VALIDATION
VII. CÔ LẬP DỮ LIỆU & BẢO MẬT
VIII.E2E FLOW
```
- Tên section là **dòng riêng**, merge C:O, font bold xanh đậm trên nền xanh nhạt
- Thứ tự cố định, bỏ section nào không áp dụng

### TC ID
- Trong section La mã: `TC_{section:02d}.{tc:03d}` — ví dụ `TC_01.001`, `TC_02.015`
- Trong section ROLE: `TC-ROLE-01`, `TC-ROLE-02`, ...

### Priority
- `P0` — critical (chiếm ≥40% tổng)
- `P1` — important
- `P2` — nice-to-have

## Quy tắc viết từng test case

| Cột | Quy tắc |
|-----|--------|
| **Module (A)** | Tên feature ngắn (vd "Lịch làm việc"). Có thể merge ô khi nhiều TC cùng module. |
| **Nhóm chức năng (B)** | Tên section không có "I./II./" (vd "HIỂN THỊ TRANG & TRUY CẬP") |
| **TC ID (C)** | `TC_NN.NNN` hoặc `TC-ROLE-NN` |
| **Chức năng (D)** | 1 câu mô tả mục tiêu test, không lặp lại tên section |
| **Priority (E)** | P0/P1/P2 |
| **Tiền điều kiện (F)** | **CỤ THỂ**, có số liệu. ❌ "User có vài task". ✅ "User có: 2 Task ngày hạn = hôm qua, 1 Issue ngày hạn = tuần trước, 3 việc ngày hạn = hôm nay" |
| **Bước thực hiện (G)** | Đánh số `1. … 2. …`, mỗi bước 1 dòng, dùng `\n` xuống dòng |
| **Test Data (H)** | Giá trị thật: ngày cụ thể `Hôm nay = 22/05/2026`, role cụ thể `User: P2`, hoặc `—` nếu không cần |
| **Expected Result (I)** | **Kiểm chứng được**, liệt kê bằng bullet `-`. Ghi rõ tên cột/badge/icon/số đếm |
| **Giải thích nghiệp vụ (J)** | Khi TC liên quan business rule: ghi công thức/quy tắc. Vd: `Công thức: due_date < today`, `BR — Mọi user đều truy cập được`, `Range: today → endOfWeek` |
| **KQ thực tế (K)** | Để trống (QA điền) |
| **L/M/N (3 lần check)** | Default `"Not Executed"`. Dropdown 4 giá trị: Passed, Failed, Pending, Not Executed |
| **Ghi chú (O)** | Để trống hoặc note đặc biệt |

## Style + format

**Description block (rows 1-10):**
- Cột A: font bold 11pt, wrap text, vertical top, nền `#FFF2CC` (vàng nhạt)
- Cột B (merge B-O): font 11pt, wrap text, vertical top
- Border thin xám

**Title row (row 11):**
- Cột A: font bold 14pt, nền `#4472C4`, chữ trắng
- F11 "TEST SUMMARY": font bold 12pt, nền `#4472C4`, chữ trắng, center
- I11-I15: font bold 11pt, align right, nền `#D9E1F2`
- L11-L15: font 11pt bold, align center, nền `#D9E1F2`

**Header row (row 17):**
- Font trắng bold 11pt, nền `#4472C4`, center + wrap, border thin
- Row height = 36

**Section title row** (merge C:O):
- Font bold 12pt màu `#1F4E79`, nền `#D6E4F0`, align left
- Row height = 26

**Data row:**
- Font 11pt, wrap text, vertical top, border thin
- Even-row highlight `#F2F2F2`
- Row height auto (≥ 30)

**Data Validation** trên `L18:N500`:
```
Dropdown list = "Passed,Failed,Pending,Not Executed"
allowBlank=True, showDropDown=False
```

**Column widths:**
```python
col_widths = {
    'A': 22, 'B': 22, 'C': 16, 'D': 42, 'E': 10,
    'F': 32, 'G': 55, 'H': 22, 'I': 65, 'J': 35,
    'K': 18, 'L': 16, 'M': 16, 'N': 16, 'O': 22
}
```

**Freeze panes:** **KHÔNG dùng** `freeze_panes`. Để user scroll tự do toàn bộ file (description block + summary + data). Lý do: 17 hàng đầu quá nhiều, freeze sẽ chiếm hết màn hình khi scroll xuống data.

## Template Python generator (copy-paste, sửa block CONFIG)

Lưu vào `docs/srs/<feature>-generate-testcase.py`, chạy `python3 <file>.py`.

```python
"""Generate testcase Excel cho feature <FEATURE_NAME>."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# =========================================================================
# CONFIG — SỬA PHẦN NÀY CHO TỪNG FEATURE
# =========================================================================
OUTPUT_FILE  = "docs/srs/<feature>-testcases.xlsx"
SHEET_NAME   = "<TenFeatureKhongDau>"
FEATURE_NAME = "<Tên feature đầy đủ>"
MODULE_NAME  = "<Tên module>"

# 9 mục mô tả (KHÔNG BỎ MỤC NÀO — ghi "—" nếu không áp dụng)
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",                 "..."),
    ("2. Đối tượng được tính / hiển thị",     "► ...\n► ..."),
    ("3. Đối tượng bị ẩn / không tính",       "► ..."),
    ("4. Bộ lọc thời gian áp dụng cho",       "..."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",    "..."),
    ("6. Quy tắc cộng dồn / deduplicate",     "..."),
    ("7. Phân quyền cấp",                     "• <permission_code_1> — ...\n• <permission_code_2> — ..."),
    ("8. Cách tính các ô thống kê",           "► Ô 'X' = ...\n► Ô 'Y' = ..."),
    ("9. Ghi chú đọc bảng",                   "..."),
]

# True nếu feature có phân quyền theo cấp → sinh section TC-ROLE
HAS_ROLE_SECTION = True
ROLE_TCS = [
    # (tc_id_suffix, function, priority, precondition, steps, test_data, expected, business_note)
    ("00", "Truy cập màn hình mặc định",
        "", "User đã đăng nhập",
        "1. Truy cập menu ...\n2. Quan sát hiển thị",
        "User bất kỳ",
        "Màn hình chỉ hiển thị dữ liệu thoả điều kiện ...",
        "Mặc định: chỉ thấy dữ liệu do mình tạo / phụ trách"),
    ("01", "Truy cập với quyền 'Xem theo tổng công ty'", "P0",
        "User có quyền 'xem_bc_xxx_tong_cty'; đã đăng nhập",
        "1. Truy cập menu ...\n2. Quan sát phạm vi dữ liệu",
        "User: quyền tổng cty",
        "Hiển thị toàn bộ dữ liệu mọi công ty.",
        "Permission: xem_bc_xxx_tong_cty"),
    # ... thêm cho từng permission code
]

# Sections nghiệp vụ — list (roman_num, section_title, [tcs...])
# Mỗi tc = (tc_num_str, function, priority, precondition, steps, test_data, expected, business_note)
SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Truy cập trang", "P0",
            "User đã đăng nhập",
            "1. Truy cập URL ...\n2. Quan sát layout",
            "User bất kỳ",
            "Trang load thành công với layout:\n- Cột trái: ...\n- Cột phải: ...",
            "BR — Mọi user đều truy cập được"),
        # ... thêm TC
    ]),
    ("II", "BỘ LỌC & TÌM KIẾM", [
        # ...
    ]),
    # ("III", ...), ("IV", ...), ...
]

# =========================================================================
# STYLES
# =========================================================================
THIN   = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

DESC_LABEL_FONT = Font(name="Calibri", size=11, bold=True)
DESC_LABEL_FILL = PatternFill("solid", fgColor="FFF2CC")
DESC_BODY_FONT  = Font(name="Calibri", size=11)
WRAP_TOP_LEFT   = Alignment(wrap_text=True, vertical="top", horizontal="left")
WRAP_TOP_CENTER = Alignment(wrap_text=True, vertical="top", horizontal="center")

TITLE_FONT      = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
TITLE_FILL      = PatternFill("solid", fgColor="4472C4")

SUMMARY_LABEL_FONT  = Font(name="Calibri", size=11, bold=True)
SUMMARY_LABEL_FILL  = PatternFill("solid", fgColor="D9E1F2")
SUMMARY_VALUE_FONT  = Font(name="Calibri", size=11, bold=True)
SUMMARY_VALUE_ALIGN = Alignment(horizontal="center", vertical="center")

HEADER_FONT  = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
HEADER_FILL  = PatternFill("solid", fgColor="4472C4")
HEADER_ALIGN = Alignment(wrap_text=True, vertical="center", horizontal="center")

SECTION_FONT = Font(name="Calibri", size=12, bold=True, color="1F4E79")
SECTION_FILL = PatternFill("solid", fgColor="D6E4F0")
SECTION_ALIGN = Alignment(wrap_text=True, vertical="center", horizontal="left", indent=1)

DATA_FONT_FILL_EVEN = PatternFill("solid", fgColor="F2F2F2")

COL_WIDTHS = {
    'A': 22, 'B': 22, 'C': 16, 'D': 42, 'E': 10,
    'F': 32, 'G': 55, 'H': 22, 'I': 65, 'J': 35,
    'K': 18, 'L': 16, 'M': 16, 'N': 16, 'O': 22
}

# =========================================================================
# BUILD
# =========================================================================
wb = Workbook()
ws = wb.active
ws.title = SHEET_NAME

# Column widths
for col, w in COL_WIDTHS.items():
    ws.column_dimensions[col].width = w

# --- ROW 1: Tiêu đề mô tả tính năng ---
ws.cell(1, 1, "MÔ TẢ TÍNH NĂNG (đọc trước khi xem testcase)").font = Font(bold=True, size=12)
ws.merge_cells("B1:O1")
ws.row_dimensions[1].height = 22

# --- ROW 2-10: 9 mục mô tả ---
for idx, (label, body) in enumerate(DESCRIPTION_BLOCK, start=2):
    a = ws.cell(idx, 1, label)
    a.font = DESC_LABEL_FONT
    a.fill = DESC_LABEL_FILL
    a.alignment = WRAP_TOP_LEFT
    a.border = BORDER
    b = ws.cell(idx, 2, body)
    b.font = DESC_BODY_FONT
    b.alignment = WRAP_TOP_LEFT
    b.border = BORDER
    ws.merge_cells(start_row=idx, start_column=2, end_row=idx, end_column=15)
    ws.row_dimensions[idx].height = max(40, body.count("\n") * 16 + 30)

# --- ROW 11: Title + Test Summary ---
t = ws.cell(11, 1, f"Testcase _ {FEATURE_NAME}")
t.font = TITLE_FONT
t.fill = TITLE_FILL
t.alignment = Alignment(vertical="center", horizontal="left", indent=1)
ws.merge_cells("B11:E11")
ws.merge_cells("F11:H11")
fs = ws.cell(11, 6, "TEST SUMMARY")
fs.font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
fs.fill = TITLE_FILL
fs.alignment = Alignment(vertical="center", horizontal="center")
ws.row_dimensions[11].height = 28

# --- ROW 11-15: Summary formulas ---
summary_rows = [
    (11, "Số trường hợp kiểm thử đạt (P):",              '=COUNTIF(L18:N500,"Passed")'),
    (12, "Số trường hợp kiểm thử không đạt (F):",         '=COUNTIF(L18:N500,"Failed")'),
    (13, "Số trường hợp kiểm thử đang xem xét (PE):",     '=COUNTIF(L18:N500,"Pending")'),
    (14, "Số trường hợp kiểm thử chưa thực hiện:",        '=COUNTIF(L18:N500,"Not Executed")'),
    (15, "Tổng số trường hợp kiểm thử:",                  '=COUNTIF(L18:N500,"<>")'),
]
for r, label, formula in summary_rows:
    lc = ws.cell(r, 9, label)
    lc.font = SUMMARY_LABEL_FONT
    lc.fill = SUMMARY_LABEL_FILL
    lc.alignment = Alignment(vertical="center", horizontal="right")
    lc.border = BORDER
    ws.merge_cells(start_row=r, start_column=9, end_row=r, end_column=11)
    vc = ws.cell(r, 12, formula)
    vc.font = SUMMARY_VALUE_FONT
    vc.fill = SUMMARY_LABEL_FILL
    vc.alignment = SUMMARY_VALUE_ALIGN
    vc.border = BORDER
    ws.merge_cells(start_row=r, start_column=12, end_row=r, end_column=15)
    if r > 11:
        ws.row_dimensions[r].height = 22

# Row 16 trống
ws.row_dimensions[16].height = 8

# --- ROW 17: Header 15 cột ---
HEADERS = [
    "Module", "Nhóm chức năng", "TC ID", "Chức năng", "Priority",
    "Tiền điều kiện", "Bước thực hiện", "Test Data",
    "Expected Result (chi tiết)", "Giải thích nghiệp vụ", "KQ thực tế",
    "trạng thái check lần 1", "trạng thái check lần 2", "trạng thái check lần 3",
    "Ghi chú",
]
for i, h in enumerate(HEADERS, start=1):
    c = ws.cell(17, i, h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.alignment = HEADER_ALIGN
    c.border = BORDER
ws.row_dimensions[17].height = 36

# KHÔNG freeze_panes — user muốn scroll tự do toàn bộ file
# (đừng thêm ws.freeze_panes = ... ở đây)

# --- DATA ROWS ---
current_row = 18
data_row_idx = 0

def write_section_row(title: str):
    global current_row
    cell = ws.cell(current_row, 3, title)
    cell.font = SECTION_FONT
    cell.fill = SECTION_FILL
    cell.alignment = SECTION_ALIGN
    cell.border = BORDER
    ws.merge_cells(start_row=current_row, start_column=3, end_row=current_row, end_column=15)
    # Fill A,B với border
    for col in (1, 2):
        ws.cell(current_row, col).fill = SECTION_FILL
        ws.cell(current_row, col).border = BORDER
    ws.row_dimensions[current_row].height = 26
    current_row += 1

def write_tc(tc_id, function, priority, precondition, steps, test_data, expected, business_note, module=MODULE_NAME, group=""):
    global current_row, data_row_idx
    values = [
        module, group, tc_id, function, priority,
        precondition, steps, test_data,
        expected, business_note, "",
        "Not Executed", "Not Executed", "Not Executed",
        "",
    ]
    fill = DATA_FONT_FILL_EVEN if data_row_idx % 2 == 1 else None
    for i, v in enumerate(values, start=1):
        c = ws.cell(current_row, i, v)
        c.font = Font(name="Calibri", size=11)
        c.alignment = WRAP_TOP_LEFT if i != 5 else WRAP_TOP_CENTER
        c.border = BORDER
        if fill:
            c.fill = fill
    # Row height heuristic
    longest = max(len(str(v)) for v in values)
    ws.row_dimensions[current_row].height = max(30, min(180, longest // 4))
    current_row += 1
    data_row_idx += 1

# Section ROLE (nếu có)
if HAS_ROLE_SECTION:
    write_section_row("Phân quyền & truy cập")
    for suffix, func, prio, pre, steps, td, exp, note in ROLE_TCS:
        write_tc(f"TC-ROLE-{suffix}", func, prio, pre, steps, td, exp, note,
                 group="Phân quyền & truy cập")

# Section La mã
for roman, title, tcs in SECTIONS:
    write_section_row(f"{roman}. {title}")
    for i, (tc_num, func, prio, pre, steps, td, exp, note) in enumerate(tcs, start=1):
        sec_idx = ["I","II","III","IV","V","VI","VII","VIII","IX","X"].index(roman) + 1
        tc_id = f"TC_{sec_idx:02d}.{int(tc_num):03d}" if tc_num.isdigit() else f"TC_{sec_idx:02d}.{tc_num}"
        write_tc(tc_id, func, prio, pre, steps, td, exp, note, group=title)

# --- DATA VALIDATION cho 3 cột check ---
dv = DataValidation(
    type="list",
    formula1='"Passed,Failed,Pending,Not Executed"',
    allow_blank=True,
    showDropDown=False,
)
dv.add(f"L18:N{current_row + 100}")
ws.add_data_validation(dv)

wb.save(OUTPUT_FILE)
print(f"✅ Generated: {OUTPUT_FILE}")
print(f"   Rows: 1-10 description, 11-15 summary, 17 header, 18-{current_row-1} data")
```

## Checklist coverage (bắt buộc kiểm trước khi báo done)

- [ ] **9 mục mô tả** đầy đủ, không bỏ mục
- [ ] Mục 2/3: liệt kê **từng status / điều kiện cụ thể**, không nói chung chung
- [ ] Mục 7: liệt kê **tên permission code** đúng như trong code
- [ ] Mục 8: viết **công thức** từng ô thống kê
- [ ] Test Summary: 5 công thức COUNTIF đúng range `L18:N500`
- [ ] Header 15 cột đúng thứ tự, dòng 17
- [ ] (Nếu phân cấp) Section `TC-ROLE-XX` đứng đầu, cover **mọi permission code**
- [ ] Section nghiệp vụ đánh **La mã** (I, II, III…)
- [ ] **Tiền điều kiện có data cụ thể** (số liệu, ngày, role)
- [ ] **Test Data có giá trị thật** (ngày cụ thể, vai trò cụ thể)
- [ ] **Expected Result kiểm chứng được** (bullet, có số/tên cụ thể)
- [ ] **Cột J (Giải thích nghiệp vụ)** điền đầy đủ cho TC liên quan BR (công thức / range / BR-XX)
- [ ] 3 cột check L/M/N default `Not Executed` + dropdown validation
- [ ] P0 ≥ 40% tổng TC
- [ ] Mỗi business rule có ≥ 1 TC
- [ ] **KHÔNG** dùng freeze_panes (scroll tự do)

## Quy tắc viết

- Tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh
- Mỗi business rule (BR-XX) PHẢI có ≥ 1 test case + ghi rõ ở cột J
- Số lượng tối thiểu: 30 TC (feature nhỏ), 60-100 (trung), 100+ (lớn)
- Section trống → vẫn ghi tên section + 1 dòng "Không áp dụng cho feature này", không bỏ section

## Không được

- Không bỏ qua bất kỳ mục nào trong 9 mục mô tả
- Không viết tiền điều kiện chung chung ("user có data") — phải có **số liệu cụ thể**
- Không viết Expected Result mơ hồ ("hiển thị đúng") — phải nói **đúng cái gì**
- Không bỏ cột J khi TC liên quan business rule
- Không tự chế permission code — phải copy đúng từ code (`spatie/laravel-permission`)
- Không thay 3 cột check bằng 1 cột (QA chạy nhiều round)
- Không đoán validation — đọc Request class thực tế

## File tham chiếu chuẩn (đọc khi cần xem mẫu)

| Mục đích | File |
|---------|------|
| Mẫu Excel chuẩn (feature) | `docs/srs/lich-lam-viec-testcases.xlsx` |
| Mẫu Excel chuẩn (báo cáo nhiều quyền) | `hrm-api/database/files/Testcase _baocao.xlsx` |
| Generator Python mẫu | `docs/srs/lich-lam-viec-generate-testcase.py` |
| Mẫu HTML | `docs/references/handover-ui-testcases.html` |
