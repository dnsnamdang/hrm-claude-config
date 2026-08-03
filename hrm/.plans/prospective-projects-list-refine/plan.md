# Plan — Tinh chỉnh màn Danh sách Dự án tiền khả thi

## Phase 1 — Ẩn cột/filter + đổi tên (FE)
### FE — `hrm-client/pages/assign/prospective-projects/index.vue`
- [x] Xóa cột `scope` (Nhóm ngành) và `industry` (Nhóm giải pháp) khỏi `allColumns`
- [x] Xóa slot template `#cell-scope` và `#cell-industry`
- [x] Xóa block dropdown filter "Nhóm ngành" (`scope_id`) và "Nhóm giải pháp" (`industry_id`)
- [x] Xóa `scope_id`, `industry_id` khỏi `initialStateForm` + watcher + computed `scopeFilterOptions`/`industryFilterOptions`
- [x] Đổi label+title cột `customerScope` → "Lĩnh vực kinh doanh khách hàng"
- [x] Đổi label+title cột `customerScopeGroup` → "Loại hình hoạt động khách hàng"
- [x] Đổi label+placeholder filter `customer_scope_group_id` → "Loại hình hoạt động khách hàng"
- [x] Fix merge `defaultTableColumns`: loại bỏ key cũ (scope/industry) trong cấu hình cột đã lưu (DB)

## Phase 2 — Cột Khách hàng cuối (FE)
- [x] Cập nhật slot `#cell-customerBenefit`: thêm dòng "Người liên hệ: {tên} • {sđt}", chỉ hiển thị khi `is_intermediary_customer`

## Phase 3 — Bộ lọc mới
### FE
- [x] Bật lại + đổi tên filter "Lĩnh vực kinh doanh khách hàng" (`customer_scope_id`), options `customerScopeFilterOptions`
- [x] Thêm filter autocomplete "Khách hàng cuối" (`customer_benefit_id`) — clone từ filter Khách hàng, dùng chung API `search-customers` (+ persist/restore/reset localStorage)
- [x] Thêm `customer_benefit_id` vào `initialStateForm`
### BE — `hrm-api/Modules/Assign/Services/ProspectiveProjectService.php`
- [x] Thêm xử lý param `customer_benefit_id` trong `index()` (`->where('customer_benefit_id', ...)`)

## Phase 4 — Verify
- [x] `php -l` BE OK; FE grep sạch; route chunk prospective-projects/index.js compile 200 (không lỗi build)
- [x] Verify browser Playwright (login namdangit qua token injection) — AC1,2,3,5,6 PASS:
  - AC1: header bảng + filter KHÔNG còn "Nhóm ngành"/"Nhóm giải pháp"
  - AC2: header + filter đổi đúng "Loại hình hoạt động khách hàng" + "Lĩnh vực kinh doanh khách hàng"
  - AC3: cột Khách hàng cuối hiển thị "Mã - Tên\nNgười liên hệ: {tên} • {SĐT}" cho dòng KH trung gian, "—" cho dòng thường
  - AC5: chọn "Lĩnh vực kinh doanh khách hàng" → request list có customer_scope_id=2
  - AC6: gõ ô "Khách hàng cuối" → gọi search-customers + chọn → request list có customer_benefit_id=1460
- [~] AC4 (masking SĐT KH cuối): BE đã apply CustomerPhoneVisibility cho customer_benefit_*phone (giống cột Khách hàng, theo task masking-sdt-khach-hang). namdangit có quyền tổng cty → thấy full (đúng). Cần tài khoản sales không sở hữu/không quản lý để demo SĐT che '-' trên UI — user tự kiểm chứng.

---
### Checkpoint — 2026-06-26 (DONE)
Vừa hoàn thành: Code Phase 1-3 + verify Playwright AC1/2/3/5/6 PASS
Đang làm dở: không
Bước tiếp theo: User kiểm chứng AC4 bằng tài khoản low-priv (nếu cần). Chưa commit/push (theo quy tắc).
Blocked:
