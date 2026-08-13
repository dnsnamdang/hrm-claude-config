---
name: testcase-documenter
description: Generate tài liệu test case cho feature đã triển khai — output Excel (.xlsx) đầy đủ block mô tả nghiệp vụ + summary + phân quyền + các cột check, viết bằng ngôn ngữ nghiệp vụ cho QA
---

# Test Case Documenter — ERP TPE

## Mục đích
Generate test cases cho feature/báo cáo đã hoặc sắp triển khai. Output là **file Excel (.xlsx)** để QA dùng test thực tế (dropdown trạng thái, công thức tổng hợp, nhiều lần check).

File Excel chuẩn phải có **ĐỦ 4 KHỐI** theo đúng thứ tự (xem mục Layout bên dưới):
1. Khối **MÔ TẢ TÍNH NĂNG / BÁO CÁO** (9 mục cố định)
2. Khối **TEST SUMMARY** (2 khối công thức: DNS và TP)
3. **Header testcase** (17 cột) + (nếu có phân quyền) section **TC-ROLE**
4. **Các section testcase** đánh số La mã

## Khi nào dùng
- Feature/báo cáo đã code xong, cần test case cho QA
- User yêu cầu "tạo testcase", "viết test case", "viết test"

---

## ⚠️ NGUYÊN TẮC SỐ 1 — NGÔN NGỮ NGHIỆP VỤ, KHÔNG PHẢI NGÔN NGỮ CODE

**Người đọc tài liệu này là QA và bộ phận nghiệp vụ, KHÔNG phải dev.** (User chốt 2026-08-12:
*"tài liệu này dev có dùng đâu mà toàn id như code thế này"*.)

**TUYỆT ĐỐI KHÔNG viết vào bất kỳ ô nào của file:**

| Cấm | Ví dụ vi phạm |
|---|---|
| Tên bảng / tên cột DB | `costs`, `company_costs`, `status`, `revenue_calculation`, `updated_by` |
| Id permission, group, type, guard | "permission id 1123", "type 24", `role_has_permissions`, "guard api" |
| Tên hàm / class / file | `CustomerListResource`, `filled()`, `has()`, `number_format` |
| Đường dẫn route / endpoint | `/api/v1/customer-care/costs`, `GET /{cost}/lock`, `checkPermission` |
| Mã HTTP | "BE trả 422", "403 Forbidden", "trả 404" |
| Tên tham số kỹ thuật | `sort_by=name`, `per_page`, `meta.total`, `current_company_role`, `localStorage`, `filterCollapsed` |

**Thay bằng đúng nhãn hiển thị trên màn hình + câu chữ người dùng hiểu được:**

| Thay vì | Viết là |
|---|---|
| `status = 0` | "trạng thái Khóa" |
| `revenue_calculation = 1` | "Có tính doanh thu" (đúng nhãn trên lưới) |
| "BE trả 422, lỗi inline tại ô X" | "hệ thống báo lỗi đỏ ngay dưới ô X, cửa sổ không đóng, dữ liệu đã nhập vẫn còn" |
| "BE trả 403 Forbidden" | "hệ thống từ chối, báo không có quyền" |
| "BE trả 404" | "hệ thống báo dữ liệu đã thay đổi, không treo trang" |
| "Postman gọi `PUT /api/v1/...`" | "dùng công cụ kiểm thử API gọi thẳng chức năng Sửa, bỏ qua giao diện" |
| `firm_quotation_costs` | "Báo giá hãng" (tên nghiệp vụ) |
| `sort_by = updated_at` | "Sắp xếp theo cột Cập nhật" |
| `meta.total` | "tổng số bản ghi khớp bộ lọc" |
| "lưu localStorage TTL 10 phút" | "hệ thống ghi nhớ bộ lọc trong 10 phút" |

**Vẫn ĐƯỢC giữ** (đây là ngôn ngữ tester, không phải jargon nội bộ):
- Tên quyền nguyên văn tiếng Việt như trong seeder ("Quản lý dịch vụ sửa chữa và chi phí khác")
- Nhóm test bảo mật gọi thẳng API — viết dạng *"dùng công cụ kiểm thử API gọi thẳng chức năng
  Xóa, bỏ qua giao diện"*. Bỏ hẳn nhóm này thì mất khả năng phát hiện lỗ hổng phân quyền; ghi
  chú ở mục 9 rằng nhóm này dành cho tester kỹ thuật.

**Bắt buộc gắn bộ kiểm tra tự động vào cuối generator** — in kết quả trước khi xuất file:

```python
import re
BANNED = [
    r"`[a-z_]{3,}`", r"\bBE\b", r"\bFE\b", r"\bHTTP\b",
    r"trả (400|403|404|422)", r"\b(400|403|404|422)\b",
    r"permission id", r"/api/v1", r"\bAPI /", r"localStorage",
    r"number_format", r"meta\.", r"sort_by", r"per_page",
    r"role_has_permissions", r"current_company_role",
]
text_all = "\n".join(mọi ô mô tả + mọi ô của từng TC)
found = {p: len(re.findall(p, text_all)) for p in BANNED if re.findall(p, text_all)}
print("!!! CON THUAT NGU KY THUAT:", found) if found else print("OK - sach")
```

⚠️ **File mẫu của team cũng vi phạm điều này** (`erp_product_id`, `CustomerListResource`,
`filterCollapsed`) — bám form TRÌNH BÀY của mẫu nhưng KHÔNG bắt chước cách viết đó.

---

## Input cần thiết
1. **Bắt buộc**: Tên feature + module, SRS hoặc design.md (use case + business rules)
2. **Tự thu thập từ code**: Routes, Controller, Service, Entity, Request, FE Pages/Components, Plan.md
3. **Nên có**: ảnh/quan sát thật màn hình trên cổng dev để lấy đúng nhãn cột, đúng chữ trên nút và
   đúng nội dung thông báo — viết TC theo tên field trong code là nguồn gốc của lỗi ngôn ngữ ở trên

## Layout file Excel (chuẩn) — TUYỆT ĐỐI tuân thủ

> **File mẫu đóng gói ngay trong skill:** `.claude/skills/testcase-documenter/assets/TC_MAU.xlsx`
> (bản gốc là `TC mẫu phần bomlist.xlsx` user đã duyệt — đã copy vào repo để ai clone về cũng có).
> Bản dựng đúng chuẩn để đối chiếu: `.plans/gop-db/customer-care-cost-catalog/testcase.xlsx`

```
Row 1  : "MÔ TẢ TÍNH NĂNG (đọc trước khi xem testcase)" (merge A1:N1, bold 12pt)
Row 2  : 1. Mục đích tính năng              | <nội dung>
Row 3  : 2. Đối tượng được tính / hiển thị  | <liệt kê đầy đủ trạng thái, điều kiện>
Row 4  : 3. Đối tượng bị ẩn / không tính    | <nội dung>
Row 5  : 4. Bộ lọc thời gian áp dụng cho    | <chỉ rõ cột nào, range nào>
Row 6  : 5. Cấu trúc dữ liệu / cây phân cấp | <nội dung>
Row 7  : 6. Quy tắc cộng dồn / deduplicate  | <nội dung>
Row 8  : 7. Phân quyền cấp                  | <liệt kê từng tên quyền tiếng Việt>
Row 9  : 8. Cách tính các ô thống kê        | <công thức từng ô, diễn giải bằng lời>
Row 10 : 9. Ghi chú đọc bảng                | <phân trang, định dạng, bẫy dễ sai…>
         (cột A nền #FFF2CC bold; cột B merge B:N)

Row 11 : A11 "Testcase _ <Tên feature> - Cập nhật ngày dd/mm/yyyy" (merge A11:E11,
             nền #4472C4, chữ trắng bold 15pt)
         F11 "TEST SUMMARY" (merge F11:H15, cùng nền xanh)
         → 2 KHỐI SUMMARY song song:
           • Khối DNS  : nhãn I:J (nền #00FF00), giá trị K:L
           • Khối TP   : nhãn M:N (nền trắng),   giá trị O:Q
Row 11 : Số trường hợp … đạt (P)            | =COUNTIF(K18:M1000,"Passed") | … | =COUNTIF(O18:Q1000,"P")
Row 12 : … không đạt (F)                    | =COUNTIF(K18:M1000,"Failed") | … | =COUNTIF(O18:Q1000,"F")
Row 13 : … đang xem xét (PE)                | =COUNTIF(K18:M1000,"Pending")| … | =COUNTIF(O18:Q1000,"PE")
Row 14 : … chưa thực hiện                   | =COUNTIF(K18:K1000,"Not Executed")
Row 15 : Tổng số trường hợp                 | =COUNTIF(K18:K1000,"<>")     | … | =COUNTIF(C18:C1000,"TC*")

Row 16 : (trống — spacing, height 8)

Row 17 : HEADER 17 cột
  A Module | B Nhóm chức năng | C TC ID | D Chức năng | E Priority
  F Tiền điều kiện | G Bước thực hiện | H Test Data
  I Expected Result (chi tiết) | J KQ thực tế
  K/L/M DNS check lần 1/2/3 | N Ghi chú | O/P/Q TP check lần 1/2/3

Row 18+: Data — section "Phân quyền & truy cập" (nếu có), sau đó section La mã
```

⚠️ **2 lỗi CÓ TRONG file mẫu — đừng copy theo:**
1. File mẫu **thiếu hẳn dòng header cột** (row 17 là section band luôn). Phải có header.
2. Công thức summary lệch range (`K12` bắt đầu từ `K18`, `K15` đếm `"Passed"` thay vì tổng).
   Dùng range thống nhất như bảng trên.

### Quy tắc nội dung 9 mục mô tả
- **Không bỏ mục nào**. Không áp dụng thì ghi "Không áp dụng" + 1 dòng lý do
- Mục 2 & 3 **PHẢI liệt kê từng trạng thái / điều kiện cụ thể**, không nói chung chung
- Mục 7 **PHẢI liệt kê đầy đủ tên quyền tiếng Việt** đúng như trong seeder
- Mục 8 viết công thức bằng lời: `Ô 'Hiển thị a–b / N' = a là dòng đầu trang, N là tổng bản ghi khớp bộ lọc`
- Mục 9 là nơi cảnh báo **các bẫy dễ sai nhất của màn** (định dạng số, dấu phẩy thập phân, ô nào
  chặn trần ô nào không…) — QA đọc mục này trước khi chạy test

## Phân loại + đánh số section

### Section "Phân quyền & truy cập"
- Đứng **đầu tiên** sau header (trước section La mã)
- ID format: `TC-ROLE-00`, `TC-ROLE-01`, ...
- Liệt kê 1 TC cho **TỪNG tên quyền** + TC "không có quyền nào" + TC bypass giao diện cho từng
  thao tác ghi dữ liệu
- Feature không phân quyền → bỏ section này

### Sections nghiệp vụ — đánh số La mã
```
I.   HIỂN THỊ TRANG & TRUY CẬP
II.  BỘ LỌC & TÌM KIẾM
III. DANH SÁCH, SẮP XẾP & PHÂN TRANG
IV.  CHỨC NĂNG CHÍNH (TẠO / SỬA / XEM)
V.   CÁC THAO TÁC TRẠNG THÁI (Khóa/Mở khóa, Duyệt/Từ chối…)
VI.  XÓA
VII. XUẤT EXCEL / IN
VIII.RÀNG BUỘC NHẬP LIỆU
IX.  CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI
X.   E2E FLOW
```
- Tên section là **dòng riêng**, merge C:Q, bold 12pt màu `#1F4E79` trên nền `#D6E4F0`
- Bỏ section không áp dụng; thứ tự giữ nguyên
- ⚠️ Đặt tên section bằng ngôn ngữ nghiệp vụ: dùng "RÀNG BUỘC NHẬP LIỆU" thay cho
  "EDGE CASES & VALIDATION"

### TC ID
- Section La mã: `TC_{section:02d}.{tc:03d}` — `TC_01.001`, `TC_02.015`
- Section quyền: `TC-ROLE-01`, `TC-ROLE-02`, ...

### Priority
`P0` critical (≥40% tổng) · `P1` important · `P2` nice-to-have

## Quy tắc viết từng test case

| Cột | Quy tắc |
|-----|--------|
| **Module (A)** | Tên feature ngắn (vd "DV sửa chữa & CP khác") |
| **Nhóm chức năng (B)** | Tên section không có số La mã |
| **TC ID (C)** | `TC_NN.NNN` hoặc `TC-ROLE-NN` |
| **Chức năng (D)** | 1 câu mô tả mục tiêu test, không lặp tên section |
| **Priority (E)** | P0/P1/P2 |
| **Tiền điều kiện (F)** | **CỤ THỂ, có số liệu**. ❌ "User có vài dịch vụ". ✅ "Dịch vụ X: công ty 1 là 5%, công ty 4 là 12%; tài khoản C thuộc công ty 1" |
| **Bước thực hiện (G)** | Đánh số `1. … 2. …`, mỗi bước 1 dòng (`\n`). Mô tả thao tác người dùng thấy được: "Bấm nút Sửa (biểu tượng bút chì)" |
| **Test Data (H)** | Giá trị thật, viết bằng nhãn màn hình: `% Tính giá vốn: 12,5`, `Trạng thái: Khóa`. `—` nếu không cần |
| **Expected Result (I)** | **Kiểm chứng được**, bullet `-`, ghi rõ tên cột/nhãn/chữ trên nút/nội dung thông báo. Chỗ nào là bẫy thì mở đầu bằng `⚠️` |
| **KQ thực tế (J)** | Để trống (QA điền) |
| **K/L/M** | DNS check 3 lần. Default `"Not Executed"`. Dropdown: Passed, Failed, Pending, Not Executed |
| **Ghi chú (N)** | Để trống hoặc note đặc biệt |
| **O/P/Q** | TP check 3 lần. Để TRỐNG. Dropdown: P, F, PE |

**Không có cột "Giải thích nghiệp vụ" riêng** (bản 15 cột cũ có cột J này). Business rule viết
thẳng vào Expected Result dưới dạng câu cảnh báo `⚠️` — QA đọc một chỗ, không phải liếc 2 cột.

## Style + format

- **Font toàn file: Times New Roman 12** (riêng title row 15pt, tiêu đề mô tả row 1 là 12pt bold)
- Description block: cột A bold + nền `#FFF2CC`; cột B merge B:N; wrap text, vertical center
- Title row 11: nền `#4472C4`, chữ trắng bold 15pt
- Summary DNS: nền `#00FF00` · Summary TP: nền trắng · đều có border thin
- Header row 17: chữ trắng bold, nền `#4472C4`, center + wrap, height 40
- Section row: bold 12pt `#1F4E79` trên nền `#D6E4F0`, merge C:Q, height 26
- Data row: nền trắng, border thin `BFBFBF`, wrap, vertical center, height auto (≥34)
- **KHÔNG dùng `freeze_panes`** — để user scroll tự do toàn bộ file

**Column widths:**
```python
COL_WIDTHS = {
    'A': 26.9, 'B': 27.1, 'C': 16, 'D': 26.6, 'E': 9,
    'F': 22.8, 'G': 18.6, 'H': 22, 'I': 43.9, 'J': 41.6,
    'K': 14, 'L': 14, 'M': 14, 'N': 20,
    'O': 11, 'P': 11, 'Q': 11,
}
```

**Data Validation:**
```python
K18:M<last+50>  →  list "Passed,Failed,Pending,Not Executed"   (allow_blank, showDropDown=False)
O18:Q<last+50>  →  list "P,F,PE"                               (allow_blank, showDropDown=False)
```

## Generator

**Dùng engine chung, KHÔNG nhân bản 1.300 dòng cho mỗi màn:**
`.claude/skills/testcase-documenter/assets/tc_engine.py` (Windows, `python` + `openpyxl`).
Nó lo toàn bộ phần dựng Excel, style, data validation, chống trùng TC ID và bộ kiểm tra thuật ngữ.

Generator của từng màn chỉ còn 3 khối CONFIG:

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build

DESCRIPTION_BLOCK = [...]   # đúng 9 mục, engine assert
ROLE_TCS = [...]            # (hậu tố, chức năng, priority, tiền điều kiện, bước, test data, expected)
SECTIONS = [...]            # (số La Mã, tên section, [tc...])

build(output_file=..., sheet_name="Trang tính1", feature_name=..., module_name=...,
      description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
```

`build()` tự in kết quả bộ kiểm tra thuật ngữ, tổng TC và tỉ lệ P0 — đọc dòng in ra trước khi báo done.

*(`assets/gen_testcase_mau.py` là bản đầy đủ một file, giữ lại để tham chiếu cách dựng; màn mới
nên dùng `tc_engine.py`.)*

**Một feature có nhiều màn** → mỗi màn một file `testcase - <Tên màn>.xlsx`, đừng gộp chung một
file. Generator có thể đặt chung một script gọi `build()` nhiều lần (xem
`.plans/gop-db/customer-care-maintenance-catalogs/gen_testcase.py`).

Lưu bản của feature vào `.plans/[feature]/gen_testcase.py` (cùng thư mục tài liệu, được version
control), output ra `.plans/[feature]/testcase.xlsx`.

⚠️ Đầu file luôn có đoạn sau, nếu không `print()` chuỗi tiếng Việt sẽ ném `UnicodeEncodeError`
(console Windows mặc định cp1252):
```python
import sys
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
```

## Checklist coverage (bắt buộc kiểm trước khi báo done)

- [ ] **Bộ kiểm tra thuật ngữ in "OK - sach"** — không còn tên bảng/cột, id quyền, route, mã HTTP
- [ ] **9 mục mô tả** đầy đủ, không bỏ mục
- [ ] Mục 2/3: liệt kê **từng trạng thái / điều kiện cụ thể**
- [ ] Mục 7: liệt kê **tên quyền tiếng Việt** đúng như trong seeder
- [ ] Mục 9: đã ghi các **bẫy dễ sai nhất** của màn
- [ ] Test Summary: 2 khối DNS + TP, range thống nhất
- [ ] **Có dòng header 17 cột ở row 17** (file mẫu thiếu — đừng quên)
- [ ] (Nếu phân quyền) Section `TC-ROLE-XX` đứng đầu, cover **mọi tên quyền** + TC bypass giao diện
- [ ] Section nghiệp vụ đánh **La mã**, tên section bằng ngôn ngữ nghiệp vụ
- [ ] **Tiền điều kiện có số liệu cụ thể**
- [ ] **Test Data viết bằng nhãn màn hình**, không phải tên field
- [ ] **Expected Result kiểm chứng được**, bẫy có gắn `⚠️`
- [ ] K/L/M default `Not Executed` + dropdown; O/P/Q để trống + dropdown
- [ ] P0 ≥ 40% tổng TC
- [ ] Mỗi business rule có ≥ 1 TC
- [ ] **Không trùng TC ID** (assert trong generator)
- [ ] **KHÔNG** dùng freeze_panes

## Quy tắc viết

- Tiếng Việt, dùng đúng nhãn hiển thị trên màn hình
- Mỗi business rule PHẢI có ≥ 1 test case
- Số lượng tối thiểu: 30 TC (feature nhỏ), 60–100 (trung), 100+ (lớn).
  Tham chiếu: màn danh mục 1 bảng + 1 modal ra ~139 TC
- Section trống → vẫn ghi tên section + 1 dòng "Không áp dụng cho feature này"

## Không được

- **Không dùng thuật ngữ code** (xem NGUYÊN TẮC SỐ 1) — lỗi nghiêm trọng nhất
- Không bỏ qua bất kỳ mục nào trong 9 mục mô tả
- Không viết tiền điều kiện chung chung ("user có data") — phải có **số liệu cụ thể**
- Không viết Expected Result mơ hồ ("hiển thị đúng") — phải nói **đúng cái gì**
- Không tự chế tên quyền — copy đúng từ `PermissionsTableSeeder`
- Không thay các cột check bằng 1 cột (QA chạy nhiều round, có 2 bên DNS và TP)
- Không đoán validation — đọc Request class thực tế rồi DIỄN GIẢI ra ngôn ngữ người dùng

## File tham chiếu

Tất cả đều nằm **trong repo** — không phụ thuộc máy cá nhân.

| Mục đích | File |
|---------|------|
| **Form mẫu (đóng gói trong skill)** | `.claude/skills/testcase-documenter/assets/TC_MAU.xlsx` |
| **Generator mẫu (đóng gói trong skill)** | `.claude/skills/testcase-documenter/assets/gen_testcase_mau.py` |
| **Bản dựng đúng chuẩn để đối chiếu** | `.plans/gop-db/customer-care-cost-catalog/testcase.xlsx` |
| Mẫu Excel báo cáo nhiều quyền | `hrm-api/database/files/Testcase _baocao.xlsx` |
