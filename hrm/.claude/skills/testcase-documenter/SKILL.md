---
name: testcase-documenter
description: Generate tài liệu test case cho feature đã triển khai — output Excel (.xlsx) đầy đủ block mô tả nghiệp vụ + summary + phân quyền + các cột check, viết bằng ngôn ngữ nghiệp vụ cho QA
---

# Test Case Documenter — ERP TPE

## Mục đích
Generate test cases cho feature/báo cáo đã hoặc sắp triển khai. Output là **file Excel (.xlsx)** để QA dùng test thực tế (dropdown trạng thái, công thức tổng hợp, nhiều lần check).

> **CHUẨN CHUNG (chốt 03/11/2026): tab "13. DM quốc gia"** — bản sao `assets/TC_MAU_QUOC_GIA.xlsx` — và checklist
> **`assets/CHECKLIST_TC_SRS.xlsx`** tab "Testcase" (299 case cần kiểm tra theo Nhóm → Phân nhóm). Sinh file bằng
> **`assets/tc_chuan.py` → `build_chuan(...)`**, tự kiểm bằng **`assets/check_tc.py`** (phải 0 lỗi). Bản cũ của skill (nhóm
> `TC-ROLE` đầu tab, nhóm "TẠO / SỬA / XEM", "E2E FLOW"…) đã bị QA báo lệch chuẩn — 19 tab phải làm lại ngày 03/11/2026.

File Excel chuẩn phải có **ĐỦ 4 KHỐI** theo đúng thứ tự (xem mục Layout bên dưới):
1. Khối **MÔ TẢ TÍNH NĂNG / BÁO CÁO** (9 mục cố định)
2. Khối **TEST SUMMARY** (2 khối công thức: DNS và TP) + dòng 16 "Tổng số testcase"
3. **Header testcase** (17 cột)
4. **Các nhóm testcase** đánh số La Mã liên tục, đúng thứ tự chuẩn — **PHÂN QUYỀN là nhóm CUỐI**, không còn section `TC-ROLE` đầu tab

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
| URL / đường dẫn màn hình (chốt 2026-09-25) | `http://hrm-crm.eteksofts.com/customer-care/services/create`, `/customer-care/services/{id}/edit`, "gõ thẳng đường dẫn …" — cột Bước thực hiện / Tiền điều kiện chỉ ghi **đường bấm menu + nút** |
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
- Tên quyền nguyên văn tiếng Việt như `name` trong Catalog ("Quản lý dịch vụ sửa chữa và chi phí khác")
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
Row 8  : 7. Phân quyền cấp                  | <liệt kê từng tên quyền tiếng Việt; quyền Xem ghi kèm các mức phạm vi cho phép>
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

Row 16 : Tổng số testcase                   | =COUNTIF(C18:C1000,"TC_*")   (tab "Tổng hợp" của file Drive trỏ K16)

Row 17 : HEADER 17 cột
  A Module | B Nhóm chức năng | C TC ID | D Chức năng | E Priority
  F Tiền điều kiện | G Bước thực hiện | H Test Data
  I Expected Result (chi tiết) | J KQ thực tế
  K/L/M DNS check lần 1/2/3 | N Ghi chú | O/P/Q TP check lần 1/2/3

Row 18+: Data — các nhóm La Mã (dòng tiêu đề nhóm rồi tới case). A Module + B Nhóm chức năng chỉ ghi ở
         case ĐẦU MỖI NHÓM. J + K/L/M để TRỐNG (DNS tự điền khi chạy test — không điền sẵn "Passed").
```

⚠️ **2 lỗi CÓ TRONG file mẫu — đừng copy theo:**
1. File mẫu **thiếu hẳn dòng header cột** (row 17 là section band luôn). Phải có header.
2. Công thức summary lệch range (`K12` bắt đầu từ `K18`, `K15` đếm `"Passed"` thay vì tổng).
   Dùng range thống nhất như bảng trên.

### Quy tắc nội dung 9 mục mô tả
- **Không bỏ mục nào**. Không áp dụng thì ghi "Không áp dụng" + 1 dòng lý do
- Mục 2 & 3 **PHẢI liệt kê từng trạng thái / điều kiện cụ thể**, không nói chung chung
- Mục 7 **PHẢI liệt kê đầy đủ tên quyền tiếng Việt** đúng như `name` trong Catalog. Quyền Xem có phạm vi là
  **một** quyền kèm các mức (vd "Xem phiếu đề nghị thu — mức: Tổng công ty / Công ty / Phòng ban / Bộ phận",
  đọc `scopes` của mã), KHÔNG viết thành 4 quyền "Xem … theo công ty / theo phòng ban…" (tên cũ)
- Mục 8 viết công thức bằng lời: `Ô 'Hiển thị a–b / N' = a là dòng đầu trang, N là tổng bản ghi khớp bộ lọc`
- Mục 9 là nơi cảnh báo **các bẫy dễ sai nhất của màn** (định dạng số, dấu phẩy thập phân, ô nào
  chặn trần ô nào không…) — QA đọc mục này trước khi chạy test

## Phân loại + đánh số section

### Nhóm testcase — tên + thứ tự CHUẨN (theo tab Quốc gia + checklist, chốt 03/11/2026)

Bỏ nhóm màn không có; nhóm có mặt phải đúng thứ tự dưới đây, đánh La Mã LIÊN TỤC (I, II, III…). `check_tc.py` chặn sai.

| Loại (`loai`) | Thứ tự nhóm |
|---|---|
| `danh_muc` | HIỂN THỊ TRANG & TRUY CẬP · TÌM KIẾM & LỌC DANH SÁCH · THÊM MỚI · CHỈNH SỬA · XÓA · KHÓA / MỞ KHÓA · LỊCH SỬ THAY ĐỔI · XEM CHI TIẾT <ĐỐI TƯỢNG> · TÙY CHỈNH CỘT · XUẤT DANH SÁCH EXCEL · IMPORT TỪ FILE EXCEL · RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC · PHÂN QUYỀN |
| `phieu` | HIỂN THỊ TRANG & TRUY CẬP · TÌM KIẾM & LỌC DANH SÁCH · THÊM MỚI · CHỈNH SỬA · XÓA · KHÓA / MỞ KHÓA · GỬI DUYỆT · DUYỆT PHIẾU · KHÔNG DUYỆT PHIẾU · HỦY PHIẾU · LỊCH SỬ THAY ĐỔI · XEM CHI TIẾT <PHIẾU> · IN PHIẾU · TÙY CHỈNH CỘT · XUẤT DANH SÁCH EXCEL · IMPORT TỪ FILE EXCEL · RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC · PHÂN QUYỀN |
| `bao_cao` | HIỂN THỊ TRANG & TRUY CẬP · TÌM KIẾM & LỌC DANH SÁCH · SỐ LIỆU BÁO CÁO · XEM CHI TIẾT <…> (popup) · TÙY CHỈNH CỘT · XUẤT DANH SÁCH EXCEL · IN BÁO CÁO · RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC · PHÂN QUYỀN |

Đặt case vào nhóm (mỗi dòng checklist ÁP DỤNG ĐƯỢC phải có ≥ 1 case):
- **HIỂN THỊ**: mở từ menu (mọi LỐI VÀO — xem mục dưới), tiêu đề, nút, cột mặc định hiện/ẩn, trạng thái, rỗng / không khớp lọc,
  **phân trang** (số dòng mặc định, đổi số dòng, trước/sau, đầu/cuối, trạng thái nút, STT liên tục, tổng số, về trang 1) và
  **sắp xếp** (mặc định, tăng, giảm, ngày tạo/cập nhật, cột không sắp xếp, giữ khi chuyển trang, về trang 1).
- **TÌM KIẾM & LỌC**: từ khoá chính xác/một phần/hoa-thường/có dấu/không tồn tại/ký tự đặc biệt/khoảng trắng/giới hạn/xoá/Enter;
  từng ô lọc, kết hợp, mặc định, tổng & phân trang sau lọc, Làm mới; lưu trạng thái (chuyển màn quay lại, F5, tab mới, tài khoản khác).
- **THÊM MỚI / CHỈNH SỬA**: validate từng trường (trống, định dạng, ký tự, đúng/vượt độ dài, trùng, khoảng trắng, lỗi biến mất), Lưu
  và tiếp tục / Lưu nháp / Lưu và gửi duyệt, Đóng/X/Thoát/Ở lại/nhập rồi xoá hết, bấm Lưu liên tục, trùng đồng thời 2 tab; sửa: fill
  đúng, trường không sửa được, giữ nguyên của chính mình, không đổi thì không ghi lịch sử, bản ghi khoá / bị xoá / 2 người sửa.
- **Phiếu**: tác động số liệu (tồn, công nợ, hàng giữ, bút toán) nằm TRONG nhóm thao tác gây ra nó; luồng nhiều màn → RÀNG BUỘC.
- **Báo cáo**: mỗi cột/chỉ tiêu, dòng tổng, định dạng số, lập chứng từ rồi kiểm số tăng/giảm → SỐ LIỆU BÁO CÁO.
- **PHÂN QUYỀN** (cuối): 1 case cho TỪNG tên quyền + không có quyền nào; ẩn nút khi thiếu quyền; mở URL trực tiếp khi thiếu quyền;
  đổi quyền giữa thao tác; phạm vi dữ liệu theo quyền: **1 case cho TỪNG mức phạm vi** của quyền Xem (Vai trò cấp mức đó
  → thấy đúng tập bản ghi, không thấy bản ghi ngoài mức); người có 2 Vai trò khác mức → áp mức lớn hơn; đổi công ty đang
  làm việc → quyền tính lại theo công ty mới, không thấy dữ liệu công ty khác. KHÔNG viết case "gọi thẳng API / Postman".
- Tên nhóm là **dòng riêng**, merge C:Q, bold 12pt màu `#1F4E79` trên nền `#D6E4F0` (engine tự làm).
- KHÔNG dùng các nhóm cũ: "Phân quyền & truy cập" đầu tab, "BỘ LỌC & TÌM KIẾM", "DANH SÁCH, SẮP XẾP & PHÂN TRANG",
  "TẠO / SỬA / XEM", "RÀNG BUỘC NHẬP LIỆU", "CÔ LẬP DỮ LIỆU…", "E2E FLOW".

Câu chữ bắt chước tab Quốc gia: Chức năng là cụm ngắn ("Mở màn hình từ menu", "Thiếu Tên quốc gia thì bị chặn", "Bấm Hủy thì không
xóa"); Tiền điều kiện 1 câu; Bước "1. …\n2. …"; Expected mỗi ý 1 dòng bắt đầu "-  ", nhãn/thông báo NGUYÊN VĂN.

### Bắt buộc: test ĐỦ CÁC LỐI VÀO của màn (chốt 2026-08-26)

Nhiều màn có **một đường dẫn nhưng nhiều mục menu trỏ vào**, khác nhau ở query string, mỗi lối vào
ra một danh sách khác hẳn: không kèm gì (chỉ phiếu của mình) · `?type=all` (theo phạm vi quyền) ·
`?type=waiting_handle` / `?type=waiting_information` / `?type=waiting_create_quotation` (việc đang
chờ chính mình hoặc phòng mình). ⚠️ Màn Báo giá dịch vụ đặt tên tham số là `permission`, không phải
`type`.

Chỉ test một lối vào là bỏ lọt cả một màn nghiệp vụ. Trong section **I. HIỂN THỊ TRANG & TRUY CẬP**
phải có, cho MỖI lối vào:

| TC | Nội dung |
| --- | --- |
| Mở đúng lối vào | **Cột "Bước thực hiện" phải ghi ĐƯỜNG BẤM đầy đủ** — `Vào phân hệ CSKH → nhóm "Kiểm tra bảo hành sửa chữa" → bấm "Yêu cầu kiểm tra sửa chữa - bảo hành"` — chứ không phải "mở link ?type=all". QA bấm theo menu như người dùng thật, không gõ tay đường dẫn. Rồi đếm số bản ghi đúng phạm vi lối vào đó; tiền điều kiện ghi rõ số liệu (vd "tài khoản A lập 6 phiếu, phòng A quản lý 12 phiếu") |
| Cùng màn, vào từ phân hệ KHÁC | Cùng một màn nhưng vào từ Bán hàng và từ CSKH cho ra **hai danh sách khác nhau** — phải có TC riêng cho từng phân hệ, so số bản ghi hai bên |
| Đổi bộ lọc rồi mở lối vào khác | Đường link phải THẮNG bộ lọc lần trước, không được giữ phạm vi cũ |
| Bấm "Làm mới" | Xoá điều kiện lọc nhưng **giữ nguyên phạm vi** đang xem |
| Sửa tay tham số trên thanh địa chỉ thành giá trị lạ | Hệ thống bỏ qua, quay về phạm vi mặc định — KHÔNG lỗi, KHÔNG lộ thêm dữ liệu |
| Tài khoản không có quyền xem theo cấp mở lối vào "xem tất cả" | Vẫn chỉ thấy phiếu của chính mình (đường link là cách xem, không phải cấp quyền) |

**Lấy danh sách lối vào ở đâu**: đếm từ menu ERP (`topmenubar.blade.php`) và các nhánh
`if ($request->type == ...)` trong `searchByFilter()` — đừng suy từ tên màn. Với **mỗi** mục menu
tìm được, đọc ngược lên lấy **tên phân hệ và tên nhóm** chứa nó để ghi vào cột Bước thực hiện.

⚠️ **Mục menu vào ROUTE TRẦN (không kèm tham số) cũng là một lối vào phải test**, và mặc định của
nó thường là *chỉ bản ghi của mình* chứ không phải "xem tất cả" — controller ERP gán
`$type = $request->type ?? 'index'`. Bỏ qua nó là bỏ lọt đúng lối vào mà phần lớn nhân viên dùng
hằng ngày (đã dính thật 2026-08-27).

**Ra số liệu mong đợi mà không đoán**: ERP và hệ thống mới chạy trên CÙNG một cơ sở dữ liệu ở máy
phát triển, nên đếm được cả hai bên với cùng một người dùng rồi so từng lối vào. Lệch thì phải truy
nguyên trước khi viết vào cột kết quả mong đợi — đã có lần lệch hoá ra do **quyền chưa được cấp**
bên hệ thống mới chứ không phải logic sai.

### TC ID
- Một kiểu duy nhất: `TC_{số nhóm:02d}.{tc:03d}` — `TC_01.001`, `TC_02.015` (kể cả nhóm PHÂN QUYỀN). Không còn `TC-ROLE-NN`.

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
| **Tiền điều kiện (F)** | **CỤ THỂ, có số liệu**. ❌ "User có vài dịch vụ". ✅ "Dịch vụ X: công ty 1 là 5%, công ty 4 là 12%; tài khoản C thuộc công ty 1". Nhiều ý → **mỗi ý một dòng** |
| **Bước thực hiện (G)** | Đánh số `1. … 2. …`, **mỗi bước một DÒNG RIÊNG trong ô** (xuống dòng thật). Mô tả thao tác người dùng thấy được: "Bấm nút Sửa (biểu tượng bút chì)" |
| **Test Data (H)** | Giá trị thật, viết bằng nhãn màn hình: `% Tính giá vốn: 12,5`, `Trạng thái: Khóa`. Nhiều giá trị → **mỗi giá trị một dòng**. `—` nếu không cần |
| **Expected Result (I)** | **Kiểm chứng được**, gạch đầu dòng `-`, **mỗi ý một DÒNG RIÊNG trong ô**, ghi rõ tên cột/nhãn/chữ trên nút/nội dung thông báo |
| **KQ thực tế (J)** | Để trống (QA điền) |
| **K/L/M** | DNS check 3 lần. Default `"Not Executed"`. Dropdown: Passed, Failed, Pending, Not Executed |
| **Ghi chú (N)** | Để trống hoặc note đặc biệt |
| **O/P/Q** | TP check 3 lần. Để TRỐNG. Dropdown: P, F, PE |

**Không có cột "Giải thích nghiệp vụ" riêng** (bản 15 cột cũ có cột J này). Business rule viết
thẳng vào Expected Result thành **một gạch đầu dòng riêng** — QA đọc một chỗ, không phải liếc 2 cột.

### ⛔ 2 lỗi trình bày bị cấm (user chốt 2026-09-15)

**1. KHÔNG dùng emoji/icon trong nội dung ô** — không `⚠️`, không `✅`, không `❌`, không `🔒`.
Cần nhấn mạnh một cái bẫy thì viết bằng CHỮ: mở đầu gạch đầu dòng bằng `Lưu ý:` hoặc viết hoa
cụm từ khoá (`KHÔNG được…`, `PHẢI…`). Lý do: file là tài liệu bàn giao cho QA và khách, icon
làm bảng rối và hiển thị lệch font trên máy khác.
*(Emoji trong chính file SKILL.md này là để cho người đọc skill, KHÔNG được bê vào ô testcase.)*

**2. Ô nhiều ý thì PHẢI xuống dòng thật trong ô, không nhồi một dòng dài.**
Áp cho cả 4 cột Tiền điều kiện · Bước thực hiện · Test Data · Expected Result.

```
❌ SAI (nhồi 1 dòng)
G: 1. Đăng nhập. 2. Mở phân hệ Giao việc. 3. Quan sát menu trái.
I: - Menu ghi 'Nhiệm vụ'. - Không còn chữ 'Task'.

✅ ĐÚNG (mỗi ý 1 dòng trong cùng 1 ô)
G: 1. Đăng nhập.
   2. Mở phân hệ Giao việc.
   3. Quan sát menu trái.
I: - Menu ghi 'Nhiệm vụ'.
   - Không còn chữ 'Task'.
```

- **File .xlsx** (`tc_engine.py`): đưa `\n` vào chuỗi + ô đã bật `wrap_text=True`.
- **Dán thẳng lên Google Sheet**: dựng TSV thì ô có xuống dòng **phải bọc trong dấu nháy kép**
  (`"1. …\n2. …"`), nháy kép bên trong nhân đôi (`""`). Không bọc thì Sheets cắt thành nhiều DÒNG
  bảng, lệch toàn bộ khối bên dưới.
- Tự kiểm trước khi bàn giao: mở ngẫu nhiên 3 ô cột G và 3 ô cột I — phải thấy nhiều dòng; và
  `grep -P '[\x{2190}-\x{2BFF}\x{1F300}-\x{1FAFF}]'` trên nội dung sinh ra phải RỖNG.

## Sửa tab testcase ĐÃ CÓ trên Google Sheet (bài học 28/09/2026)

Tab online có tester sửa tay SONG SONG với mình — số hàng đổi bất cứ lúc nào.
- **Dump lại tab NGAY trước khi chạy script sửa**, không dùng bản dump từ đầu buổi. 28/09 tester
  vừa xoá 4–10 hàng ở 3 tab (Cấp DV, Ghi chú KT, Chi phí) giữa lúc soạn và lúc chạy → mọi số hàng
  trong kế hoạch lệch; chạy vào là dán đè nhầm case.
- **Peek các ô mốc trước khi chạy** (hàng chèn, hàng đầu nhóm, TC ID ở ô sửa) và so với dump. Lệch
  1 ô là dừng, rebase kế hoạch theo dump mới — không "chạy thử xem sao".
- Rebase xong vẫn phải báo user: edit nhắm vào case người khác đã xoá thì BỎ (không thêm lại case
  họ đã xoá); ô họ vừa sửa chữ mà edit của mình ghi đè cả ô thì nêu ra để user quyết.
- **Theo giọng văn tester đang chuẩn hoá** trên chính tab đó: 28/09 tester đổi hàng loạt
  "nạp lại" → "**tải lại**" và xoá các case kiểu "gọi thẳng API / bỏ qua giao diện" (testcase là góc
  nhìn người dùng cuối). Case mới đừng viết ngược lại hướng đó; muốn giữ case API thì hỏi user.
- Tester đang thao tác trên tab thì hỏi user thời điểm chạy, đừng chạy chèn hàng hàng loạt cùng lúc.
- Chữ chép từ ô cũ mang theo lỗi gõ (`có2 nút`, `tên  đừng`) — ô đã viết lại thì sửa luôn.
- **Emoji cấm cả khi mô tả ô chọn có biểu tượng ổ khoá**: viết "có biểu tượng ổ khóa trước tên",
  KHÔNG ghi `🔒 Tên` (đã lỡ dán vào tab Ngân hàng, Gói BD ngày 28/09 — phải sửa lại).

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

**Dùng `assets/tc_chuan.py` → `build_chuan()`** (bọc engine chung `assets/tc_engine.py` rồi chỉnh đúng khuôn tab Quốc gia).
KHÔNG gọi `tc_engine.build` trực tiếp cho màn mới (sẽ ra khuôn cũ). Generator của từng màn chỉ còn 2 khối CONFIG:

```python
import os, sys
sys.path.insert(0, r"<đường dẫn tới>\.claude\skills\testcase-documenter\assets")
from tc_chuan import build_chuan

DESCRIPTION_BLOCK = [...]   # đúng 9 mục, engine assert
SECTIONS = [...]            # (số La Mã, TÊN NHÓM CHUẨN, [(stt, chức năng, priority, tiền điều kiện, bước, test data, expected)...])
                            # phân quyền = nhóm "PHÂN QUYỀN" cuối cùng, KHÔNG dùng ROLE_TCS nữa

build_chuan(output_file=..., sheet_name="Trang tính1", feature_name=..., module_name=...,
            description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai="danh_muc" | "phieu" | "bao_cao")
```

`build_chuan()` tự in bộ kiểm tra thuật ngữ, tổng TC, tỉ lệ P0 và kết quả `check_tc` (phải "DAT", 0 lỗi) — đọc trước khi báo
done. Kiểm lại 1 file bất kỳ: `python assets/check_tc.py <file.xlsx> <loai>`.

Đẩy lên file Drive "Testcase chuyển đổi" (1 file nhiều tab + tab "Tổng hợp"): file đó là .xlsx thật → chèn/thay tab bằng Excel COM,
script mẫu `.plans/gop-db/danh-muc-kho/docs/chen_tab_testcase.ps1` (`-Replace` để thay tab cũ, giữ tên/vị trí + trỏ lại Tổng hợp).

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
- [ ] Mục 7: liệt kê **tên quyền tiếng Việt** đúng như `name` trong Catalog
- [ ] Mục 9: đã ghi các **bẫy dễ sai nhất** của màn
- [ ] Test Summary: 2 khối DNS + TP, range thống nhất + dòng 16 "Tổng số testcase"
- [ ] **Có dòng header 17 cột ở row 17** (file mẫu thiếu — đừng quên)
- [ ] **`check_tc.py` báo 0 lỗi**: nhóm đúng tên + thứ tự chuẩn, La Mã liên tục, mã `TC_NN.NNN`, A/B chỉ ở case đầu nhóm
- [ ] (Nếu phân quyền) nhóm **PHÂN QUYỀN đứng CUỐI**, cover **mọi tên quyền** + **từng mức phạm vi** + ẩn nút + URL trực tiếp + đổi công ty
- [ ] **Đối chiếu checklist `assets/CHECKLIST_TC_SRS.xlsx`**: mỗi dòng áp dụng được có ≥ 1 case
- [ ] **Tiền điều kiện có số liệu cụ thể**
- [ ] **Test Data viết bằng nhãn màn hình**, không phải tên field
- [ ] **Expected Result kiểm chứng được**, bẫy ghi bằng chữ (`Lưu ý:` / viết hoa từ khoá)
- [ ] **KHÔNG có emoji/icon trong bất kỳ ô nào** (`⚠️ ✅ ❌ 🔒` …)
- [ ] **Ô nhiều ý đã xuống dòng thật** ở cả 4 cột Tiền điều kiện / Bước thực hiện / Test Data / Expected Result
- [ ] J + K/L/M + O/P/Q để TRỐNG (có dropdown) — DNS/TP tự điền khi chạy test, KHÔNG điền sẵn "Passed"
- [ ] P0 ≥ 40% tổng TC
- [ ] **Có TC cho ĐỦ mọi lối vào của màn** (mỗi `?type=` / `?permission=` một bộ TC), gồm cả giá trị lạ và tài khoản thiếu quyền
- [ ] Mỗi business rule có ≥ 1 TC
- [ ] **Không trùng TC ID** (assert trong generator)
- [ ] **KHÔNG** dùng freeze_panes

## Quy tắc viết

- Tiếng Việt, dùng đúng nhãn hiển thị trên màn hình
- Mỗi business rule PHẢI có ≥ 1 test case
- Số lượng tối thiểu: 30 TC (feature nhỏ), 60–100 (trung), 100+ (lớn).
  Tham chiếu: màn danh mục 1 bảng + 1 modal ra ~139 TC
- Nhóm màn không có (vd không có Import, không có Khóa) → BỎ hẳn nhóm đó (như tab Quốc gia), không ghi dòng "Không áp dụng"

## Không được

- **Không dùng thuật ngữ code** (xem NGUYÊN TẮC SỐ 1) — lỗi nghiêm trọng nhất
- Không bỏ qua bất kỳ mục nào trong 9 mục mô tả
- Không viết tiền điều kiện chung chung ("user có data") — phải có **số liệu cụ thể**
- Không viết Expected Result mơ hồ ("hiển thị đúng") — phải nói **đúng cái gì**
- Không tự chế tên quyền — copy đúng `name` trong Catalog
- Không thay các cột check bằng 1 cột (QA chạy nhiều round, có 2 bên DNS và TP)
- Không đoán validation — đọc Request class thực tế rồi DIỄN GIẢI ra ngôn ngữ người dùng
- **Không chèn emoji/icon vào ô** (`⚠️ ✅ ❌ 🔒` …) — nhấn mạnh bằng chữ
- **Không nhồi nhiều ý vào một dòng** — bước `1. 2. 3.` và gạch đầu dòng `-` phải xuống dòng thật trong ô

## File tham chiếu

Tất cả đều nằm **trong repo** — không phụ thuộc máy cá nhân.

| Mục đích | File |
|---------|------|
| **CHUẨN CHUNG — tab "13. DM quốc gia"** | `.claude/skills/testcase-documenter/assets/TC_MAU_QUOC_GIA.xlsx` |
| **Checklist case cần kiểm tra (tab Testcase) + nội dung SRS (tab SRS)** | `.claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx` |
| **Hàm sinh đúng khuôn + bộ kiểm** | `assets/tc_chuan.py` (`build_chuan`) · `assets/check_tc.py` |
| Form mẫu cũ (bomlist — chỉ tham khảo style ô) | `.claude/skills/testcase-documenter/assets/TC_MAU.xlsx` |
| Generator mẫu cũ (khuôn cũ, KHÔNG dùng cho màn mới) | `.claude/skills/testcase-documenter/assets/gen_testcase_mau.py` |
| Mẫu Excel báo cáo nhiều quyền | `hrm-api/database/files/Testcase _baocao.xlsx` |
