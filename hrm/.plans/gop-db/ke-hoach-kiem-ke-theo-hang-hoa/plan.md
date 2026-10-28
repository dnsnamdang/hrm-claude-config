# Kế hoạch kiểm kê theo hàng hóa — Plan

> @khoipv · nhánh `feat/chuyen-doi-hang-hoa` (từ `gop_db`) · Spec: `docs/superpowers/specs/gop-db/2026-10-20-ke-hoach-kiem-ke-theo-hang-hoa-design.md`

## Phase 0 — Khảo sát
- [x] Khảo sát nghiệp vụ màn ERP `self_inventory_requests` (bảng nghiệp vụ bước 1 skill erp-to-hrm-screen)
- [x] Chốt với user 20/10: 3 quyền tên y ERP; Xóa = Đang tạo + người tạo; mở rộng picker nhiều kho; lỗi ERP giữ y (bỏ Làm mới + ô lọc chết)

## Phase 1 — BE
- [x] B1. 3 quyền trong `PermissionsTableSeeder` + `permission:sync --dry-run`
- [x] B2. Picker dùng chung: `stock_warehouse_ids[]` (ProductPickerRequest + ProductPickerService)
- [x] B3. `AccountingStockService::byAccountingWarehouse()` (tồn kế toán theo kho kế toán — port `Product::getDataForAccountingInventory`)
- [x] B4. Entities `SelfInventoryRequest/*` (STATUSES, quyền, scopedQuery, cờ, generateCode)
- [x] B5. `SelfInventoryRequestService` (list/filter/sort/export-rows/filter-options/detail)
- [x] B6. `SelfInventoryRequestWriteService` (form-options, product-stocks, store/update/destroy, kiểm phiếu treo, thông báo, lịch sử)
- [x] B7. FormRequest + Controller + routes + đăng ký `catalog_histories`
- [x] B8. In (288/287 + letterhead) + Xuất Excel 1 phiếu
- [x] B9. Smoke test HTTP kernel (list theo quyền, tạo/sửa/xóa, 409/404, phiếu treo, in, xuất) + dọn dữ liệu test theo id

## Phase 2 — FE (`pages/finance/self-inventory-requests`)
- [x] F1. Danh sách index.vue (4 mixin, SmartFilterPanel floating, cột, Cấu hình cột, Xuất Excel, In danh sách, Lịch sử)
- [x] F2. Form dùng chung (kho nhiều, popup chọn hàng, bảng rowspan, hội đồng, validate inline, unsaved, Lưu và tiếp tục, popup phiếu treo)
- [x] F3. create / _id/edit / _id/index (+ SystemInfoSection, 404)
- [x] F4. Menu `finance.js` erpPath → link
- [x] F5. Checklist skill (grep) + compile

### Fix #11876 (tester 26/10/2026)
- [x] Không tái hiện được kế hoạch trạng thái Hoàn thành: ERP không có luồng nào đưa kế hoạch về Hoàn thành (2) (chỉ Đang tạo / Đang kiểm khi
      lưu, Đã lập phiếu kiểm kê khi lập phiếu). User chốt 27/10: giữ như ERP, bỏ "Hoàn thành" khỏi ô lọc —
      `SelfInventoryRequestService::filterOptions()`; hằng số / STATUSES giữ nguyên (nhãn dữ liệu cũ). Smoke tinker OK

### Checkpoint — 2026-10-20 (BE + FE)
Vừa hoàn thành: B1–B9 + F1–F5.
- BE: 3 quyền tên y ERP (dry-run OK, CHƯA `permission:sync` thật); picker dùng chung thêm `stock_warehouse_ids[]` (kho HP 96 hàng = DB 96; 2 kho 4.889);
  `AccountingStockService::byAccountingWarehouse()` (hàm mới, không đụng `detail()`); entity + 3 service + FormRequest + controller + 14 route
  `finance/self-inventory-requests`; lịch sử ở `CatalogHistoryService::GATED_TABLES` (route chung không đọc được); in mẫu 288/287 (+ bảng ký sát phải),
  Excel phiếu 7 cột. Smoke HTTP kernel (rollback, DB sạch — max id 3 / catalog_histories 1081 như trước): Super admin 30/30, NV 429 / 504 đúng phạm vi.
- FE: `pages/finance/self-inventory-requests/` (index, create, _id/index, _id/edit, components/SelfInventoryRequestForm.vue, PendingVouchersModal.vue,
  row-actions.js, export-excel.js) + menu `finance.js`. Bám màn anh em `position-inventories` ở: bộ lọc floating, toolbar, Cấu hình cột, Xuất Excel ExcelJS,
  In danh sách, popup Lịch sử, khối V2BaseFormSection, hội đồng, footer V2Footer #custom-actions, Lưu và tiếp tục; popup chọn hàng `V2ProductPickerModal`
  (khuôn `warehouse/position-transfers`); popup cảnh báo theo `V2BaseModal`. Parse vue-template-compiler + babel OK, nuxt dev 200 ×4, grep checklist sạch.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm (CHƯA bấm thật): chọn nhiều kho, thêm hàng qua popup, đổi kho hỏi xác nhận, Lưu / Lưu và kiểm (phiếu treo → popup),
validate đỏ, Sửa / Xóa / Chi tiết, In, Xuất Excel, Lịch sử, nút Lập phiếu (mở ERP). Chạy `php artisan permission:sync` để có 3 quyền mới rồi admin gán quyền.
Blocked:

## Phase 3 — Kiểm chứng Playwright (user yêu cầu 20/10)
- [x] V1. Danh sách: nạp, tìm nhanh, Làm mới, sort Số phiếu 2 chiều, lọc Trạng thái + Tên hàng hóa (kèm nút × bỏ lọc), nhớ bộ lọc khi vào chi tiết rồi quay lại, In danh sách, Xuất Excel (popup chọn trường 8/8), Cấu hình cột (10 cột), menu dòng theo trạng thái, popup Lịch sử
- [x] V2. Tạo: validate đỏ cùng lúc + QLDA_001, chọn 2 kho (select2 nhiều), popup chọn hàng lọc tồn 2 kho (4.889 = DB), thêm hàng, chức vụ tự điền, Lưu → DB đủ bảng con
- [x] V3. Sửa: nạp lại đủ, đổi kho hỏi xác nhận + Hủy trả lại kho cũ, popup đánh dấu "Đã có", Lưu và kiểm vướng PXK-00214 → popup cảnh báo (link ERP), bỏ hàng rồi Lưu và kiểm thành công
- [x] V4. Chi tiết: nút theo cờ (không Sửa/Xóa sau khi gửi), Lập phiếu mở ERP `self_inventories/create?self_inventory_request_id=`, In (letterhead công ty phiếu, ký sát phải), Xuất Excel phiếu, khối Lịch sử (Tạo mới + Đang tạo → Đang kiểm)
- [x] V5. Xóa phiếu nháp từ danh sách: popup xác nhận → xóa cả cây con + log delete
- [x] Fix: cảnh báo Vue `sortDirection` rỗng (`filters.sort_dir || undefined`, index.vue)
- [x] Dọn dữ liệu test theo id (phiếu 7, 8 + log 1137–1140); phiếu 6 + log 1136 không phải của test, giữ nguyên

### Checkpoint — 2026-10-20 (Playwright)
Vừa hoàn thành: test Playwright MCP toàn màn trên localhost (DNS Admin) — đạt hết, 1 fix nhỏ cảnh báo Vue.
Đang làm dở: —
Bước tiếp theo: `permission:sync` + gán quyền; test bằng tài khoản không phải Super admin trên trình duyệt (đã test phạm vi qua API).
Blocked:

## Phase 4 — Fix Redmine #11814 (QA 21/10)
- [x] R1. Bộ lọc bổ sung theo ERP: Kho, Mã hàng hóa, Công ty – Phòng ban (ERP có ô nhưng BE ERP không lọc → HRM làm lọc chạy thật). BE `applyFilters` + `filterOptions` (warehouses, is_all_company) + meta list; FE `filterFields` + `V2BaseCompanyDepartmentFilter`
- [x] R2. Sort: bỏ sort cột Người tạo, thêm sort cột Ngày tạo (`created_at_full` → `created_at`)
- [x] R3. Form tạo: ô Ngày kiểm kê đã `disabled` nhưng nền trắng — rule xám `.v2-styles .v2-input:disabled` import trong style scoped không chạm `<input>` bên trong V2BaseInput → thêm `::v-deep` trong form

### Checkpoint — 2026-10-22 (#11814)
Vừa hoàn thành: R1–R3. Smoke service (Super admin): lọc kho 5→{1,2}, kho 4→{3}, mã hàng, công ty 1/4, phòng ban, sort Ngày tạo 2 chiều OK; `creator` không còn sort; filter-options trả 23 kho + is_all_company. Parse FE OK, nuxt dev 200.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm bộ lọc mới + ô Ngày kiểm kê xám.
Blocked:

## Phase 5 — Fix Redmine #11821 (QA 21/10) — màn Chi tiết
- [x] R4. Chi tiết: hiện (*) ở Ngày kiểm kê / Kho / Hàng hóa / Hội đồng kiểm kê như ERP (trước chỉ hiện ở Thêm / Sửa)
- [x] R5. Bỏ ô Số phiếu trong form (ERP không có; số phiếu đã ở thanh tiêu đề)
- [x] R6. Nút "Làm mới số liệu" (ERP `updateStock` — bản ERP nổ JS, chưa chạy bao giờ). User chốt 23/10 "làm như ERP" (theo ý định code ERP): cả Thêm / Sửa / Chi tiết, gọi lại `/product-stocks` → ghi đè SL tồn từng kho + Tổng SL, bỏ hàng hết tồn, KHÔNG tự lưu (Chi tiết chỉ hiện tạm, chốt lại mốc unsaved)

### Checkpoint — 2026-10-23 (#11821)
Vừa hoàn thành: R4 (*) luôn hiện ở Ngày kiểm kê / Kho / Hàng hóa / Hội đồng; R5 bỏ ô Số phiếu; R6 nút Làm mới số liệu `refreshStock()`
(dùng lại `/product-stocks`, chia 500 hàng/lần). Smoke service local: KH #3 làm mới → SL đổi (8→15, 10→9), 16 hàng hết tồn sẽ bị bỏ; KH #6 không đổi. Parse template + script OK.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm: bấm Làm mới ở Chi tiết (số đổi, thoát không hỏi "chưa lưu", F5 về số cũ) và ở Sửa (phải Lưu mới ghi).
Blocked:
