# Plan: Đổi tên "Nhóm lĩnh vực khách hàng" → "Loại hình hoạt động KH"

@manhcuong · Module Assign · Danh mục customer_scope_groups

Đổi nhãn hiển thị (menu/header/filter/form/export/import) + tiền tố mã NLVKH → LHHDKH (kèm di trú 21 mã cũ). Logic/FK không đổi (tham chiếu qua id). Permission name giữ nguyên.

## Phase 1 — Rename + đổi prefix mã

### BE
- [x] Entity `CustomerScopeGroup::getNextCode()` prefix 'NLVKH.' → 'LHHDKH.'
- [x] Request `CustomerScopeGroupRequest` rule code `size:10` → `size:11` (LHHDKH. = 7 + 4)
- [x] Service `CustomerScopeGroupService` regex import `/^NLVKH\./i` → `/^LHHDKH\./i` + đổi message "Mã/Tên nhóm lĩnh vực" → "loại hình hoạt động KH"
- [x] Controller `CustomerScopeGroupController` message import → "loại hình hoạt động khách hàng" (sạch "nhóm")
- [x] Blade export `customer_scope_groups.blade.php`: title + header → nhãn mới
- [x] Migration di trú 21 mã NLVKH.XXXX → LHHDKH.XXXX (giữ hậu tố), có down() — đã CHẠY THẬT (21 mã đổi, 0 NLVKH còn lại)
- [x] `php -l` các file BE — sạch

### FE
- [x] `menu-sidebar.js` label → "Loại hình hoạt động KH" (giữ permission key)
- [x] `index.vue`: filter panel title, quickSearchPlaceholder, label+placeholder filter, DataTable title + itemLabel, cột "Mã - Tên loại hình hoạt động", head title, pageTitle, import modal title, importColumns label/aliases(+giữ alias cũ)/placeholder LHHDKH, regex validate import + message, toasts/confirm/tooltip
- [x] `AddGroupModal.vue`: modal title, label "Mã/Tên" → nhãn mới, prefix NLVKH.→LHHDKH., "Lĩnh vực khách hàng thuộc nhóm" → "Danh sách lĩnh vực kinh doanh khách hàng thuộc nhóm", error toast, placeholder

### Template import
- [x] `hrm-client/static/Mau_import_Nhom_linh_vuc_khach_hang.xlsx`: header + hint LHHDKH.XXXX + sample LHHDKH (giữ tên file)

### Verify (Playwright + tinker)
- [x] AC1: menu label đổi (menu-sidebar.js)
- [x] AC2: header "Danh sách loại hình hoạt động khách hàng", filter labels, placeholder "Tìm theo mã, tên loại hình hoạt động khách hàng", cột "Mã - Tên loại hình hoạt động" — verify browser PASS, không còn text cũ
- [x] AC3: form tạo nhãn đúng + prefix LHHDKH (screenshot); rule size:11 chấp nhận LHHDKH.XXXX, từ chối hậu tố ≠4 ký tự (tinker)
- [x] AC4: export blade + import template + regex/alias import cập nhật (mã list hiển thị LHHDKH sau migrate)

### Bổ sung — cấu trúc export + import template (2026-06-24)
- [x] Export blade `customer_scope_groups.blade.php` → 10 cột: STT | Mã | Tên | Mô tả | Số lĩnh vực kinh doanh | Trạng thái | Người tạo | Ngày tạo | Người cập nhật | Ngày cập nhật (thêm Ngày tạo/Ngày cập nhật, đổi header "Mã"/"Tên" ngắn, "Số lĩnh vực thành viên"→"Số lĩnh vực kinh doanh", colspan 8→10). Render verify đúng thứ tự + ngày + count.
- [x] Import template `Mau_import_Nhom_linh_vuc_khach_hang.xlsx` (static + 2 gốc): header STT | Mã* | Loại hình hoạt động khách hàng | Trạng thái * | Mô tả; 3 sample LHHDKH.0001/SXTB/CNDT. Alias FE (Mã*/Loại hình...) khớp header (normKey verify).
- [x] E2E nhóm: export 200, import validate valid=1, import "Import thành công 1 loại hình hoạt động khách hàng", dọn record test.

## Checkpoint
### Checkpoint — 2026-06-23
Vừa hoàn thành: TOÀN BỘ rename + đổi prefix + migration 21 mã + verify AC1-AC4 + E2E THẬT (tạo LHHDKH.TEST 200, reject NLVKH.0001 422, list, export 200, import "Import thành công 1 loại hình hoạt động khách hàng", đã xóa record test) + đồng bộ 2 template gốc (Mau_import_Nhom_linh_vuc_khach_hang.xlsx + _update_LVKC.xlsx: sheet nhóm header/sample LHHDKH; sheet Lĩnh vực cập nhật mã nhóm tham chiếu cột D NLVKH→LHHDKH, giữ nhãn màn Lĩnh vực). CODE DONE + VERIFIED.
Đang làm dở: không
Bước tiếp theo: kết thúc feature (chờ user duyệt merge). Ghi chú: export là .xls OLE2 — header verify qua blade source + endpoint 200 (tooling local không parse được .xls cũ).
Blocked:

### Bổ sung — chuẩn hoá tên cột export (2026-06-29)
- [x] Blade `customer_scope_groups.blade.php`: đổi header cột "Mã" → "Mã loại hình hoạt động", "Tên" → "Tên loại hình hoạt động" cho chuẩn nghiệp vụ (giữ nguyên 10 cột)
- [x] `CustomerScopeGroupController::export`: đổi tên file tải về `danh_sach_nhom_linh_vuc_khach_hang.xls` → `danh_sach_loai_hinh_hoat_dong_khach_hang.xls`
- [x] FE `customer-scope-groups/index.vue` exportExcel: tên file tải `download` đổi `danh_sach_nhom_linh_vuc_khach_hang.xls` → `danh_sach_loai_hinh_hoat_dong_khach_hang.xls` (FE override BE, đây mới là tên thật)
