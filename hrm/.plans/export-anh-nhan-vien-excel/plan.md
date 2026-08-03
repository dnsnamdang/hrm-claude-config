# Plan: Nhúng ảnh nhân viên vào Excel

**Feature:** export-anh-nhan-vien-excel · @namdangit · 2026-07-01
**Spec:** `docs/superpowers/specs/2026-07-01-export-anh-nhan-vien-excel-design.md`

---

## Phase 0 — Verify tiền đề (làm trước khi code)

- [x] Kiểm tra định dạng field `image` thực tế → **full URL https** (S3 CMC), 1094 bản ghi có ảnh
- [x] Kiểm tra GD extension → **có** (`imagecreatefromstring` OK)
- [x] Chốt cách tải bytes ảnh → **`file_get_contents` + stream context** (ssl verify off, timeout 10)

## Phase 1 — Backend

### BE
- [x] Controller `EmployeeInfoController@getEmployeeByField`: thêm `'image' => $data->image` vào mỗi item `$result`
- [x] Controller: đổi `$fileName` sang `.xlsx` (`danh_sach_ho_so_nhan_su.xlsx` / `danh_sach_nhan_su_nghi_viec.xlsx`)
- [x] Controller: thêm `@set_time_limit(300)` + `@ini_set('memory_limit','512M')` đầu nhánh export
- [x] Blade `employee_info_report.blade.php`: tiêu đề đổi `colspan` `+1` → `+2`
- [x] Blade: thêm `<td>Ảnh</td>` header (cột đầu, trước STT)
- [x] Blade: thêm `<td></td>` rỗng đầu mỗi `<tr>` data (chỗ chứa ảnh)
- [x] `EmployeeInfoExport`: implement thêm `WithDrawings, WithColumnWidths, WithEvents`
- [x] `EmployeeInfoExport::columnWidths()`: cột `A` width 14
- [x] `EmployeeInfoExport::registerEvents()` AfterSheet: set chiều cao dòng data (dòng 3 → 3+count-1) 48pt
- [x] `EmployeeInfoExport::drawings()`: loop data, tải ảnh → MemoryDrawing neo `A{3+index}`, height 60px, offset căn giữa
- [x] `drawings()`: bỏ qua khi ảnh rỗng/tải lỗi/`imagecreatefromstring`=false (try/catch, không throw)
- [x] `php -l` các file BE sửa → sạch

## Phase 2 — Frontend

### FE
- [x] `export-list-employee-modal.vue` dòng 146: đổi tên file tải xuống `.xls` → `.xlsx`

## Phase 3 — Verify

- [x] Test export với 3 bản ghi (có ảnh + không ảnh + ảnh lỗi) → ảnh neo đúng `A3`, NV không ảnh/ảnh lỗi ô trống (Total drawings=1)
- [x] Test ảnh URL lỗi/404 → export vẫn ra file, ô để trống (không throw)
- [x] Mở file `.xlsx` bằng IOFactory → không corrupt, cột `A=Ảnh B=STT C=Họ tên...` dịch đúng
- [x] Test full controller thật (Auth::setUser id=13, lọc tên "DNS Admin") → file `.xlsx`, ảnh S3 thật nhúng `A3` (h=60,w=174)
- [ ] (Tùy chọn) Playwright UI: bấm nút Xuất Excel — backend đã verify E2E, FE chỉ đổi đuôi tên file

---

## Ghi chú
- Nếu GD không có → fallback `Drawing` + file tạm (`setPath`) thay `MemoryDrawing`, dọn file sau export.
- Nếu `WithDrawings`+`FromView` neo sai ô → kiểm tra lại số dòng thực tế sinh từ HTML reader, chỉnh offset dòng.

---

### Checkpoint — 2026-07-01
Vừa hoàn thành: CODE DONE + VERIFIED E2E toàn bộ feature nhúng ảnh nhân viên vào Excel.
Đang làm dở: (không có)
Bước tiếp theo: (tùy chọn) Playwright UI test bấm nút Xuất Excel; hoặc bàn giao review.
Blocked:

## Phase 4 — Ảnh thành trường chọn được (theo yêu cầu bổ sung)

Đổi cột "Ảnh" từ cố định → 1 trường chọn được như các trường khác (id 45).

- [x] EmployeeInfoExport arrayField: thêm `45 => 'image'`
- [x] EmployeeInfoExport: helper `isImageSelected()` (check id 45 trong $this->fields); `drawings()`, `columnWidths()`, `registerEvents()` chỉ chạy khi chọn Ảnh
- [x] Blade: bọc header `<td>Ảnh</td>` + cell rỗng trong `@if(isset($field_export['image']))`; colspan trả về `+1`
- [x] FE modal: thêm `{id:45,text:'Ảnh'}` vào danh sách Select2 (đầu list) + thêm 45 vào checkAllField
- [x] VERIFY 2 case: chọn Ảnh → A2=Ảnh, cột A ảnh, DRAWINGS=1; không chọn Ảnh → A2=STT, không cột Ảnh, DRAWINGS=0, cột không dịch. php -l sạch.

### Checkpoint — 2026-07-01 (Phase 4)
Vừa hoàn thành: Ảnh thành trường chọn được (id 45), verify 2 case pass.
Đang làm dở: (không có)
Bước tiếp theo: (tùy chọn) Playwright UI.
Blocked:
