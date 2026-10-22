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
