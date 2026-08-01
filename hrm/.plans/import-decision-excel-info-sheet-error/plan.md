# Plan — Thông báo lỗi import Excel Quyết định khi sheet thông tin chung bị loại

Phụ trách: @junfoke

## Bối cảnh

KH VNPT HCM import HĐLĐ không định biên báo lỗi hàng loạt "Không tìm thấy thông tin hợp đồng lao
động trong sheet ThongTinHopDong với email: ..." + "Loại hợp đồng chưa có tỷ lệ hưởng lương hợp lệ
(1-100)." dù email khớp ở cả 2 sheet.

## Root cause

Sheet phụ chỉ nạp `infoByEmail` khi dòng sạch lỗi → 1 lỗi tra danh mục làm cả dòng bị loại → sheet
chính báo 2 thông báo sai bản chất cho mọi dòng. Chi tiết ở `design.md`.

## Phase 1 — Sửa thông báo (BE)

### `Modules/Payroll/ExcelImports/DecisionLaborContractNoManpowerImport.php`
- [x] Lớp info: thêm `$invalidLineRowByEmail` + ghi khi loại dòng + getter `getInvalidLineRowByEmail()`
- [x] Sheet chính: `$info` rỗng mà email có ở sheet phụ → báo "Dòng N của sheet ThongTinHopDong ... bị lỗi"
- [x] Chỉ validate `salary_percentage` khi có `$info`; thêm tên loại HĐ vào thông báo
- [x] `getInvalidRow()`: nhãn `[ThongTinHopDong]` chuyển sang cột `line_row`

### `DecisionLaborContractImport.php` (có định biên)
- [x] Port y hệt 4 điểm trên

### `DecisionSalaryChangeNoManpowerImport.php` + `DecisionSalaryChangeImport.php`
- [x] Port 3 điểm (2 file này không có validate `salary_percentage`), sheet phụ tên `ThongTinChung`

## Phase 2 — Hiển thị (sau khi KH chạy thử bản Phase 1, 2026-07-31)

- [x] 4 file import: `getInvalidRow()` đưa lỗi sheet phụ **lên đầu** danh sách (`array_merge`) — trước
      đó nằm cuối, KH phải kéo qua hàng trăm dòng mới thấy nguyên nhân gốc
- [x] `hrm-client/components/modal/import-excel-modal.vue`: `<pre>` thông báo lỗi không xuống dòng,
      tràn ngang bảng → thêm class `.import-error` (`white-space: pre-wrap` + `word-break: break-word`)

## Verify
- [x] Dựng harness bootstrap Laravel + `Excel::import` chạy đúng class trên **file thật của KH**
      (scratchpad, không commit): trước fix 99/99 dòng sheet phụ bị loại; sau fix thông báo trỏ đúng
      `Dòng 4 của sheet ThongTinHopDong (email: ...)` và **không còn** lỗi "tỷ lệ hưởng lương" giả
- [x] `php -l` sạch cả 4 file
- [x] Instantiate `DecisionLaborContractImport` thật → `getInvalidLineRowByEmail()` tồn tại, trả `null` với email lạ
- [ ] KH import lại trên PM để xác nhận thấy đúng lỗi danh mục (cần DB của KH — xem Blocked)

## Việc cần KH / người có quyền trên DB KH kiểm tra

- [ ] **Tên mẫu in sai**: sheet `MauIn` ghi `VNPTHCM_Hợp đồng lao động có thời hạn` nhưng cột "Tên mẫu
      in" điền `VNPTHCM_Hợp đồng có thời hạn` ở 100/100 dòng
- [ ] Đối chiếu tên trên PM: Loại HĐ `VNPTHCM_Hợp đồng có thời hạn`, Chức vụ `nhân viên`, 4 Chức danh
      (đặc biệt `VNPT_Nhân viên VNPT_Kỹ thuật địa bàn` — nhìn như bị nối 2 chuỗi), Nhiệm vụ
      `Thực hiện theo HĐ 3830` / `HĐ 1335`
- [ ] Quyền công ty của tài khoản import (xem GOTCHA `FilterByCompanyManagerScope` trong spec)
- [ ] **Lỗi dữ liệu file**: cột email sheet chính lệch 1 dòng so với tên từ dòng 11→25 (15 người) →
      import sẽ tạo HĐLĐ **gắn sai người**; dòng 108 (`CTV072179`) không có ở sheet phụ

## Checkpoint — 2026-07-31

Vừa hoàn thành: sửa thông báo lỗi ở cả 4 file import Quyết định + verify bằng harness trên file thật của KH.
Đang làm dở: không.
Bước tiếp theo: KH sửa file Excel (tên mẫu in + cột email lệch) rồi import lại; đọc thông báo mới để biết danh mục nào sai.
Blocked: không verify được danh mục nào sai trên PM của KH — DB local là snapshot tenant khác, không có dữ liệu VNPT HCM.
