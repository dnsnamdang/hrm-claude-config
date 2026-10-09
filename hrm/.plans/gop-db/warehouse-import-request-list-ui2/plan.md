# Plan — [ERP => HRM] Kế toán - HH-DV-VC - Nhập hàng - Phiếu đề nghị nhập kho: Lỗi UI 2

Nhánh `gop_db` · @namdangit · 2026-09-21
Nguồn: task Redmine "Lỗi UI 2" (Lê Huyền Trang) — màn `/finance/warehouse-import-requests`.
Nối tiếp `warehouse-import-request-list-functions` (đã đổi cột "Người tạo", thêm cột, lịch sử).

## Phân loại 6 lỗi (đối chiếu code HIỆN TẠI trên local)

| # | Lỗi | Trạng thái code hiện tại | Hành động |
|---|-----|--------------------------|-----------|
| 1 | Cột trạng thái bỏ sort | Cột `status` còn `sortable: true` (đã verify header có sort icon) | FE: bỏ `sortable` khỏi cột status |
| 2 | Thiếu bộ lọc Người yêu cầu, Người tạo, Khách hàng, Người duyệt | Chưa có 4 filter này | BE: thêm filter + nguồn options; FE: thêm 4 select |
| 3 | Thiếu chức năng Cài đặt bộ lọc | Đang dùng `V2BaseFilterPanel` (không có popup Cài đặt bộ lọc) | FE: đổi sang `V2BaseSmartFilterPanel` + schema `filterFields` (khuôn `/assign/customers`) |
| 4 | Ẩn bộ lọc Bộ phận và Nhân viên | `V2BaseCompanyDepartmentFilter` đang hiện Bộ phận + Nhân viên (`disable_employee=false`) | FE: `disable_part` + `disable_employee` = true |
| 5 | Sửa text thành "Ngày tạo đến" | **ĐÃ ĐÚNG** — label dòng 47 = "Ngày tạo đến" (verify trên local) | Không cần sửa; server đang chạy build cũ |
| 6 | Thêm dấu x khi ô search đã có kí tự | **ĐÃ CÓ** — `V2BaseFilterPanel` có `.btn-clear-quick-search` (verify: gõ "PNK" → hiện x) | Không cần sửa; server đang chạy build cũ |

> #5 + #6 chỉ cần **rebuild + redeploy server** từ gop_db mới nhất (giống vụ toggle Ràng buộc lập HĐ).

## Việc cần code: #1, #2, #3, #4

### #1 — Bỏ sort cột Trạng thái (FE, trivial)
- [x] `pages/finance/warehouse-import-requests/index.vue` cột `status`: bỏ `sortable: true` — DONE

### #3 — Migrate sang V2BaseSmartFilterPanel ("Cài đặt bộ lọc") (FE)
- [x] Đổi `<V2BaseFilterPanel>` → `<V2BaseSmartFilterPanel>` (`table="finance_warehouse_import_requests"`)
- [x] Khai `filterFields` schema (thứ tự mặc định) + slot `#field-org` cho khối công ty–phòng ban
- [x] Wire `@filter-change` / `@reset` theo khuôn customers

### #4 — Ẩn Bộ phận + Nhân viên (FE)
- [x] `V2BaseCompanyDepartmentFilter`: `:disable_part="true"` `:disable_employee="true"`
      (chỉ còn Công ty + Phòng ban — Công ty/Phòng ban vẫn gate theo quyền org của user như cũ)

### #2 — Thêm 4 filter: Người yêu cầu / Người tạo / Khách hàng / Người duyệt (BE + FE)
- [x] BE `WarehouseImportRequestController@applyFilters`: thêm where cho
      `creator_id`(=created_by) · `requester_id`(whereHas productImportRequest.created_by) ·
      `customer_id` · `approver_id`
- [x] BE endpoint `GET /filter-options` (scoped-distinct, Cách A) + helper `employeeOptions()`/`customerOptions()`
- [x] FE: thêm 4 field vào `filterFields` (type select) + initialFilters + lazy-load options

## Quyết định ĐÃ CHỐT (2026-09-21)
1. **Cách #3**: ✅ đổi sang `V2BaseSmartFilterPanel` (popup "Cài đặt bộ lọc", lưu theo user ở
   `filter_customizations`, table=`finance_warehouse_import_requests`) — giống màn Khách hàng.
2. **Nguồn options cho 4 select #2**: ✅ **Cách A** — chỉ liệt kê giá trị CÓ THẬT trong dữ liệu
   ĐNNK thuộc phạm vi quyền (distinct-scoped, giống performers lịch sử). Thêm 1 endpoint
   `filter-options` trả 4 danh sách.
3. **"Người tạo" vs "Nhân viên" đang ẩn**: ✅ đúng — ẩn "Nhân viên" (#4), "Người tạo" (`created_by`)
   thay thế vai trò lọc theo người lập.

## Checkpoint — 2026-09-21 (đã code + verify Playwright)
Vừa hoàn thành: code xong #1/#2/#3/#4 và verify bằng Playwright trên `127.0.0.1:3000`.
- BE `WarehouseImportRequestController`: 4 where-clause (`creator_id`/`approver_id`/`customer_id` +
  `requester_id` qua `whereHas('productImportRequest')`) + endpoint `filterOptions()` scoped-distinct
  + helper `employeeOptions()`/`customerOptions()`. Route `GET /filter-options` (trước `/{id}`).
- FE `pages/finance/warehouse-import-requests/index.vue`: migrate sang `V2BaseSmartFilterPanel`
  (`table=finance_warehouse_import_requests`), `filterFields` schema, slot `#field-org` với
  `disable_part`+`disable_employee`, 4 select mới + lazy-load `/filter-options`.

Kết quả verify (playwright MCP):
- #1 cột "Trạng thái" KHÔNG còn icon sort ✓
- #3 nút "Cài đặt bộ lọc" hiện ✓
- #4 slot org đã bỏ Bộ phận + Nhân viên (guard `!disable_part`/`!disable_employee`); Công ty/Phòng ban
  vẫn gate theo quyền org — user test (Trần Văn Đức, id 48) không có `is_all_company` nên khối org
  rỗng, giống hành vi trước migrate (không phải regression) ✓
- #2 panel nâng cao hiện 4 select mới; `GET /filter-options` → 200 `{requesters,creators,customers,
  approvers}` (rỗng vì scope user không có ĐNNK nào); list API với `creator_id/approver_id/customer_id/
  requester_id` đều trả 200 total 0 (không 500) ✓
- #5 label "Ngày tạo đến" đúng ✓ · #6 nút x xoá quick-search hiện khi có ký tự ✓ (2 cái này code đã
  đúng sẵn, server prod chỉ cần rebuild)

Đang làm dở: (không) — toàn bộ code UI2 + gỡ menu (sale-hub.js) CHƯA commit (chờ user yêu cầu).
Bước tiếp theo: chờ user duyệt để commit/push nhánh `gop_db` (2 repo hrm-api + hrm-client).
Blocked: (không) — nếu muốn test 4 select có option thật cần login user có ĐNNK trong scope.
