---
name: testcase-documenter
description: Generate tài liệu test case cho feature đã triển khai — output Excel (.xlsx) + HTML
---

# Test Case Documenter — ERP TPE

## Mục đích
Generate test cases UI/API cho feature đã triển khai hoặc sắp triển khai. Output gồm:
1. **File Excel (.xlsx)** — dùng cho QA test thực tế, có dropdown Status, công thức tổng hợp
2. **File HTML** — dùng review nhanh trên trình duyệt, in ấn A4

## Khi nào dùng
- Feature đã code xong, cần test case cho QA
- Cần test case trước khi code để xác nhận scope
- User yêu cầu "tạo testcase", "tạo test case", "viết test"

## Input cần thiết

### Bắt buộc
1. Tên feature + module
2. SRS hoặc design.md (để lấy use case + business rules)

### Tùy chọn (tự thu thập từ code)
3. Code BE: Routes, Controller, Service, Entity, Migration
4. Code FE: Pages, Components chính
5. Plan.md (danh sách task đã implement)

## Quy trình generate

### Bước 1: Thu thập use cases + business rules

**Từ `docs/srs/[feature].html` hoặc `.plans/[feature]/design.md`:**
- Liệt kê tất cả use cases (UC-01, UC-02...)
- Liệt kê tất cả business rules (BR-01, BR-02...)
- Xác định actors + permissions

**Từ code (bổ sung):**
- Routes → xác định API endpoints cần test
- Request validation → điều kiện validate
- Service → business logic, edge cases
- FE components → UI interactions

### Bước 2: Phân loại test case

Mỗi test case thuộc 1 trong 4 loại:

| Loại | Tag | Mô tả |
|------|-----|--------|
| Giao diện | `tag-page` | Kiểm tra UI hiển thị đúng |
| Chức năng | `tag-func` | Kiểm tra flow hoạt động đúng |
| Edge case | `tag-edge` | Kiểm tra trường hợp biên, lỗi, concurrent |
| API/Data | `tag-api` | Kiểm tra dữ liệu, bảo mật, API response |

### Bước 3: Viết test cases

**Quy tắc viết:**
- Mỗi test case phải có: ID, Loại, Mô tả, Bước thực hiện, Kết quả mong đợi
- ID format: `{PREFIX}_{section:03d}.{tc:03d}` (ví dụ: `HDV_001.003`)
- Priority: P0 (critical), P1 (important), P2 (nice-to-have)
- Bước thực hiện phải cụ thể, có thể lặp lại
- Kết quả mong đợi phải kiểm chứng được (observable)
- Ghi rõ business rule liên quan (BR-XX) khi có

**Cấu trúc sections:**
1. Bắt đầu với các test giao diện (hiển thị đúng)
2. Tiếp theo là chức năng chính (happy path)
3. Sau đó edge cases + validation
4. Cuối cùng: data/security + E2E flow

### Bước 4: Generate output

---

## Output Format

### File Excel (.xlsx)

Dùng script Python (`generate_testcase.py`) với `openpyxl`. Cấu trúc:

**Row 1-5: Title + Test Summary**
```
A1: Testcase _ [Tên feature] ([Module]/[SubModule])
F1: TEST SUMMARY
J1: Số trường hợp kiểm thử đạt (P):     =COUNTIF(L8:L500,"Passed")
J2: Số trường hợp kiểm thử không đạt (F):  =COUNTIF(L8:L500,"Failed")
J3: Số trường hợp kiểm thử đang xem xét:   =COUNTIF(L8:L500,"Pending")
J4: Số trường hợp kiểm thử chưa thực hiện: =COUNTIF(L8:L500,"Not Executed")
J5: Tổng số trường hợp kiểm thử:           =COUNTA(L8:L500)
```

**Row 6: Header (13 cột)**
```
A: Module | B: Nhóm chức năng | C: TC ID | D: Chức năng | E: Priority
F: Tiền điều kiện | G: Bước thực hiện | H: Test Data | I: Test Data
J: Expected Result (chi tiết) | K: KQ thực tế | L: Status | M: Ghi chú
```

**Header style:** Font trắng bold 11px, nền xanh #4472C4, center+wrap

**Section row:** Merge C-M, font bold xanh đậm #1F4E79, nền xanh nhạt #D6E4F0

**Data row:** Font 11px, wrap text, border thin, even-row highlight

**Data Validation cột L (Status):** Dropdown = `Passed, Failed, Pending, Not Executed`

**Column widths:**
```python
col_widths = {
    'A': 14, 'B': 22, 'C': 16, 'D': 40, 'E': 10,
    'F': 30, 'G': 55, 'H': 22, 'I': 12, 'J': 60,
    'K': 15, 'L': 14, 'M': 15
}
```

**Helper functions:**
```python
def write_section_row(title):
    # Merge C:M, apply section_font + section_fill

def write_tc(section_num, tc_num, func, priority, precondition, steps, test_data, expected):
    # tc_id = f'{PREFIX}_{section_num:03d}.{tc_num:03d}'
    # values = [MODULE, GROUP, tc_id, func, priority, precondition, steps, test_data, '', expected, '', 'Not Executed', '']
```

**Lưu file:** `docs/srs/[feature-name]-testcases.xlsx`

### File HTML

Theo mẫu chuẩn dự án (`docs/references/handover-ui-testcases.html`). Cấu trúc:

**Header:**
```html
<h1>TEST CASES UI - TÍNH NĂNG [TÊN FEATURE]</h1>
<p>Dự án: ERP TPE - Module [Module] | Ngày: [date] | Phiên bản: [version]</p>
<div class="summary-box">Tổng hợp: N test cases | X trang UI | Y components</div>
```

**Mỗi section:**
```html
<h2>N. TÊN SECTION</h2>
<p><strong>URL:</strong> <code>/module/path</code></p>
<h3>N.M Sub-section</h3>
<table>
<tr><th>ID</th><th>Loại</th><th>Mô tả</th><th>Bước thực hiện</th><th>Kết quả mong đợi</th><th>KQ</th></tr>
<tr><td>TD-01</td><td><span class="tag tag-func">Chức năng</span></td><td>...</td><td>...</td><td>...</td><td></td></tr>
</table>
```

**Tags CSS:**
```css
.tag-page { background: #dbeafe; color: #1e40af; }   /* Giao diện */
.tag-func { background: #dcfce7; color: #166534; }   /* Chức năng */
.tag-edge { background: #fef3c7; color: #92400e; }   /* Edge case */
.tag-api  { background: #e0e7ff; color: #3730a3; }   /* API/Data */
```

**Lưu file:** `docs/srs/[feature-name]-testcases.html`

---

## Checklist coverage

Mỗi feature phải có test case cho:

- [ ] **Hiển thị giao diện** — layout, cột, badge, icon, responsive
- [ ] **CRUD chính** — tạo/sửa/xóa + validation bắt buộc
- [ ] **Bộ lọc & tìm kiếm** — từng filter riêng + kết hợp
- [ ] **Action buttons** — hiện/ẩn theo quyền + theo trạng thái
- [ ] **Business rules** — mỗi BR-XX có ít nhất 1 test case
- [ ] **Edge cases** — dữ liệu trống, concurrent, input cực đoan
- [ ] **Cô lập dữ liệu** — user chỉ thấy dữ liệu của mình (nếu áp dụng)
- [ ] **E2E flow** — happy path đầy đủ từ đầu đến cuối

## Quy tắc

- Viết bằng **tiếng Việt**, thuật ngữ kỹ thuật giữ tiếng Anh
- Mỗi business rule (BR-XX) phải có ít nhất 1 test case tương ứng
- Ghi rõ **precondition** (tiền điều kiện) cho mỗi test case
- Expected result phải **kiểm chứng được** (không mơ hồ)
- Số lượng test case tối thiểu: 30 cho feature nhỏ, 60-100 cho feature trung bình, 100+ cho feature lớn
- P0 test cases chiếm ít nhất 40% tổng số

## Không được
- Không viết test case mơ hồ ("hoạt động bình thường", "hiển thị đúng" mà không nói đúng gì)
- Không bỏ sót business rules — mỗi BR phải có test case
- Không đoán validation rules — đọc Request class thực tế
- Không tạo test case trùng lặp nội dung giữa các section

## Ví dụ file đã tạo (tham khảo)
- `docs/references/handover-ui-testcases.html` — mẫu chuẩn HTML
- `.plans/fix-handover/generate_testcase.py` — mẫu chuẩn Excel generator
- `docs/srs/my-todo-testcases.html` — My To Do test cases HTML
