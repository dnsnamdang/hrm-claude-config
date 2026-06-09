# Plan: Đổi tên "Lĩnh vực khách hàng" → "Lĩnh vực kinh doanh KH"

@manhcuong · Module Assign · Danh mục customer_scopes

Đổi nhãn (menu/header/filter/form/cột/export/import) + tiền tố mã LVKH → LVKDKH (di trú 121 mã cũ) + field "Nhóm lĩnh vực khách hàng" → "Loại hình hoạt động khách hàng" (đồng bộ task trước). FK qua id (an toàn). Permission name giữ nguyên. Nhãn field tên = "Lĩnh vực kinh doanh khách hàng".

## Phase 1
### BE
- [x] Request `CustomerScopeRequest` code `size:9`→`size:11` + message nhóm→loại hình
- [x] Service `CustomerScopeService` regex `/^LVKDKH\./i` + toàn bộ message → "lĩnh vực kinh doanh khách hàng"/"loại hình hoạt động khách hàng"
- [x] Controller message import → "lĩnh vực kinh doanh khách hàng"
- [x] Blade export `customer_scopes.blade.php`: title + 3 header cột (Mã/Lĩnh vực kinh doanh + Loại hình hoạt động)
- [x] Seeder `UpdateCustomerScopeGroupsSeeder`: LVKH.→LVKDKH. + NLVKH.→LHHDKH. (fix stale)
- [x] Migration `2026_06_24_000001` di trú 121 mã → LVKDKH, ĐÃ CHẠY (121 đổi, 0 sót)
- [x] php -l sạch

### FE
- [x] `menu-sidebar.js` → "Lĩnh vực kinh doanh KH"
- [x] `index.vue`: filter title + placeholder + filter labels + DataTable title/itemLabel + cột "Mã - Tên lĩnh vực kinh doanh khách hàng" + cột "Loại hình hoạt động khách hàng" + head/pageTitle + import modal + importColumns(+alias cũ)+placeholder LVKDKH + GroupCode→Loại hình(LHHDKH) + regex/message + toasts/confirm
- [x] `AddScopeModal.vue`: modal title + "Mã lĩnh vực kinh doanh KH" + prefix LVKDKH. + "Lĩnh vực kinh doanh khách hàng" + "Loại hình hoạt động khách hàng"(+placeholder) + error toast

### Template import
- [x] `hrm-client/static/Mau_import_LVKH.xlsx` (header+hint LVKDKH+sample+cột Loại hình LHHDKH) + 2 file gốc (Mau_import_LVKH.xlsx, _update_LVKC.xlsx) đồng bộ

### Verify
- [x] AC1 menu; AC2 header/filter "Danh sách lĩnh vực kinh doanh khách hàng" (browser PASS); AC3 form nhãn + prefix LVKDKH + rule size:11 (reject LVKH.0001=422); AC4 export 200 + import "Import thành công 1 lĩnh vực kinh doanh khách hàng"; e2e tạo LVKDKH.TST1=200 + dọn sạch

### Bổ sung — cấu trúc file mẫu IMPORT (2026-06-24)
- [x] Template `Mau_import_LVKH.xlsx` (static + 2 sheet gốc) theo spec user: header STT | Mã lĩnh vực kinh doanh khách hàng | Tên lĩnh vực kinh doanh khách hàng | Mã loại hình hoạt động KH | Trạng thái * | Mô tả; hint LVKDKH.XXXX; sample tên "Lĩnh vực khách hàng 1/2", mã loại hình "LHHDKH.0001,LHHDKH.SXTB,LHHDKH.CNDT" / "LHHDKH.CNDT"
- [x] FE importColumns alias bổ sung khớp header template (Code: "Mã lĩnh vực kinh doanh khách hàng"; Name: "Tên lĩnh vực kinh doanh khách hàng"; GroupCode: "Mã loại hình hoạt động KH"). Verify normKey (lowercase+bỏ space): cả 5 cột map đúng header.

### Bổ sung — cấu trúc cột export (2026-06-24)
- [x] Blade `customer_scopes.blade.php` đổi sang đúng 10 cột user yêu cầu: STT | Mã lĩnh vực | Tên lĩnh vực kinh doanh khách hàng | Loại hình hoạt động khách hàng | Mô tả | Trạng thái | Người tạo | Ngày tạo | Người cập nhật | Ngày cập nhật (thêm Ngày tạo/Ngày cập nhật, đổi header "Mã lĩnh vực" + "Tên lĩnh vực kinh doanh khách hàng", colspan 8→10). Render verify đúng thứ tự + có ngày.

## Checkpoint
### Checkpoint — 2026-06-24
Vừa hoàn thành: TOÀN BỘ rename scope + prefix LVKDKH + migration 121 mã + seeder + verify AC1-AC4 + e2e + đồng bộ template gốc + chỉnh 10 cột export theo yêu cầu. CODE DONE + VERIFIED.
Đang làm dở: không
Bước tiếp theo: kết thúc feature (chờ user duyệt). Deploy môi trường khác: chạy `php artisan migrate`.
Blocked:

### Bổ sung — chuẩn hoá tên cột export (2026-06-29)
- [x] Blade `customer_scopes.blade.php`: đổi header cột "Mã lĩnh vực" → "Mã lĩnh vực kinh doanh" cho chuẩn nghiệp vụ (giữ nguyên 10 cột)
- [x] `CustomerScopeController::export`: đổi tên file tải về `danh_sach_linh_vuc_khach_hang.xls` → `danh_sach_linh_vuc_kinh_doanh_khach_hang.xls`
- [x] FE `customer-scopes/index.vue` exportExcel: tên file tải `download` đổi `danh_sach_linh_vuc_khach_hang.xls` → `danh_sach_linh_vuc_kinh_doanh_khach_hang.xls` (FE override BE, đây mới là tên thật)
