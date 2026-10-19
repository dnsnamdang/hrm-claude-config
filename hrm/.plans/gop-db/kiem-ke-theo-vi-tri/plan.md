# Kiểm kê theo vị trí (Phiếu kiểm kê) — Plan

> @khoipv · nhánh `develop` (từ `gop_db`) · Spec: `docs/superpowers/specs/gop-db/2026-10-19-kiem-ke-theo-vi-tri-design.md`

## Phase 0 — Khảo sát
- [x] Đọc controller/model/blade/JS class ERP `position_inventory_results` (danh sách, chi tiết, form, quyền, trạng thái, luồng)
- [x] Chốt với user 19/10: làm hết như ERP (điều chuyển vị trí → link ERP); 5 quyền tên y ERP type 21; bật phân hệ Kho, menu Kiểm kho như ERP; xóa không trả kế hoạch (như ERP); tách hàm cây dùng chung; subagent Opus 5.5

## Phase 1 — BE (`Modules/Finance`)
- [x] B1. 5 quyền (tên y ERP, type 21) trong `PermissionsTableSeeder` + `permission:sync --dry-run`
- [x] B2. Tách `PositionInventoryTreeService` dùng chung (syncItems nhiều dòng kết quả/ĐVT, syncMembers, deleteItemTree, itemsTree có results + units) — màn Kế hoạch gọi qua đó, hành vi giữ nguyên
- [x] B3. Entities `PositionInventoryResult` (type=1, KK_STATUSES, scopedQuery, cờ quyền, generateCode KKVT) + `PositionInventoryItemProductDetailResult`
- [x] B4. `PositionInventoryResultService` (list/filter/sort/export-rows/filter-options/detail/plans picker)
- [x] B5. `PositionInventoryResultWriteService` (store/update/destroy, updateResult + đính kèm S3, approve/reject, inventoryAll, complete, thông báo)
- [x] B6. FormRequest + Controller + routes `/position-inventory-results`
- [x] B7. Lịch sử (catalog_histories) + In (mẫu 286, 285) + Xuất Excel phiếu
- [x] B8. Màn Kế hoạch: `is_can_create_result` link HRM (bỏ `erp_result_url`), smoke test lại màn Kế hoạch
- [x] B9. Smoke test tinker toàn luồng (tạo từ kế hoạch / tay, đổi ĐVT, gửi, lưu kết quả, duyệt có/không thiếu, không duyệt, xử lý, hoàn thành, 409, 404, phạm vi) + dọn dữ liệu test theo id

### Checkpoint — 2026-10-19 (BE Phase 1)
Vừa hoàn thành: B1–B9 — 5 quyền (dry-run OK), `PositionInventoryTreeService` dùng chung (màn Kế hoạch gọi qua, baseline trước/sau giống hệt trừ field mới `result_create_path`), entity `PositionInventoryResult` + service đọc/ghi/đính kèm/in, FormRequest, controller, 27 route `/position-inventory-results`, lịch sử, in mẫu 286/285, Excel phiếu. Smoke test HTTP kernel 89/89 PASS (rollback, DB sạch).
Đang làm dở: không
Bước tiếp theo: Phase 2 FE (F1–F6) theo spec mục 8 "API contract THỰC TẾ"; F5 đổi nút "Lập phiếu kiểm kê" sang `result_create_path` rồi báo BE bỏ `erp_result_url`.
Blocked:

## Phase 2 — FE
- [x] F1. Bật phân hệ Kho (`subsystems.js`) + menu `warehouse.js` nhóm Kiểm kho
- [x] F2. Danh sách `pages/warehouse/position-inventory-results/index.vue`
- [x] F3. Form dùng chung (Thêm/Sửa/Chi tiết): chọn kế hoạch, cây tick, Lấy vị trí, ĐVT kiểm kê tách dòng, hội đồng, nhập kết quả, đính kèm, ghi chú duyệt, xử lý
- [x] F4. create.vue / _id/edit.vue / _id/index.vue + footer theo cờ + lịch sử + 404
- [x] F5. Màn Kế hoạch: nút Lập phiếu kiểm kê → màn HRM mới (+ BE gỡ `erp_result_url` / `ERP_RESULT_CREATE_PATH` / `erpResultUrl()`)
- [x] F6. Checklist skill erp-to-hrm-screen (grep) + compile

### Checkpoint — 2026-10-19 (FE Phase 2)
Vừa hoàn thành: F2–F6.
- Danh sách `index.vue` — đã bám màn Kế hoạch `finance/position-inventories/index.vue` ở khối bộ lọc floating / chuỗi Kho→Vị trí / toolbar / Cấu hình cột / Xuất Excel ExcelJS (`components/export-excel.js` khuôn `position-inventories/components/export-excel.js`) / In danh sách / popup Lịch sử. Khoá duy nhất `warehouse_position_inventory_results` (columnScreenKey = localStorageKey = table lọc). Cột thêm: Kế hoạch kiểm kê (link HRM tab mới), Người duyệt, Ngày duyệt; ô lọc thêm Người duyệt; Tạo mới theo `meta.can_create` (cờ mặc định false).
- Form `components/PositionInventoryResultForm.vue` — đã bám `PositionInventoryForm.vue` (card section-header, hội đồng, Lấy vị trí, đổi kho hỏi xác nhận), dùng lại `ScopePicker.vue` + `DetailTable.vue` (thêm prop `with-results` / `extra-columns` + slot `extra-head` / `extra-cells` / `unit-cell`, mặc định giữ nguyên màn Kế hoạch). Popup chọn kế hoạch `PlanPickerModal.vue` bám `bill-adjust-depts/components/BillAdjustDeptRequestPickerModal.vue`; ô chọn + × bám `BillAdjustDeptForm.vue` (`.picker-input`, `.source-link-box`). File đính kèm = `bill-payment-requests/components/AttachmentSection.vue` qua `api-base`. ĐVT kiểm kê tách dòng: `components/result-units.js` (port `changeUnit`, test node: 119 → 5×Hộp20 + 19×Cái).
- Trang vỏ create/edit/_id (khuôn trang vỏ màn Kế hoạch; `_id/index.vue` gắn thêm `unsavedChildFormMixin` vì Chi tiết có nhập liệu). Footer theo cờ BE, không popup xác nhận (như ERP show.blade.php), thao tác xong markFormSaved → danh sách.
- F5: row-actions + form màn Kế hoạch dùng `result_create_path` (nuxt-link / router), BE `PositionInventoryService` gỡ `erp_result_url` (grep sạch cả 2 repo).
- Verify: vue-template-compiler + babel parse 13 file OK; nuxt dev :3000 build chunk 4 trang mới + chunk chung màn Kế hoạch không lỗi. CHƯA bấm thử trên trình duyệt.
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt test luồng: lập từ kế hoạch (nút ở màn Kế hoạch + popup) / lập tay, đổi ĐVT tách dòng, Lưu & gửi, Nhập kết quả + file, Duyệt có thiếu / không thiếu, Không duyệt, Xử lý tick Tổng kiểm kê + Hoàn thành, Tạo phiếu điều chuyển (ERP). Cần gán 5 quyền mới (`permission:sync`) cho tài khoản test trừ Super admin.
Blocked:

## Phase 3 — Sửa theo user (19/10: "menu, UI, phân hệ Kho làm khác các phân hệ khác")
- [x] Fix K1: phân hệ Kho chưa vào chuẩn hub (`HUB_SUBSYSTEMS`) → vẫn sidebar dọc kiểu cũ + Tổng quan placeholder. Thêm `warehouse` vào `components/subsystem-menu/hub.js`; `pages/warehouse/dashboard` → `SubsystemHubOverview` + layout `default-sidebar` (như Sản xuất / Tài chính)
- [x] Fix K2: menu `warehouse.js` bám nguyên mega-menu ERP `Kho` (Tồn kho đầu kỳ · Nhập kho · Xuất kho · Điều chuyển · Kiểm kho › Theo vị trí · Báo cáo kho), màn đã port → `link`, còn lại `erpPath` (cách làm như `finance.js`); bỏ 3 mục giữ chỗ của sheet. Nhóm "Vận chuyển - Bốc xếp" để ở phân hệ Vận chuyển
- [x] Fix K3 (user 19/10): menu Kho bỏ hết `erpPath` (18 mục) — màn chưa port chỉ để `label` → xám + báo "đang phát triển" như các phân hệ khác
- [x] Fix K4 (user 19/10): khối Phạm vi kiểm kê thiếu dấu `*` — ERP (cả form Kế hoạch lẫn Phiếu) gắn `(*)` cho Nhà/Dãy/Khoang/Vị trí → `ScopePicker.vue` `V2BaseLabel :required="!disabled"` (áp cả màn Kế hoạch)
- [x] Fix K5 (user 19/10): Ghi chú duyệt chuyển vào popup xác nhận — `components/ApproveNoteModal.vue` (khuôn `bill-adjust-dept-requests/components/RejectModal.vue`, V2BaseModal): Duyệt kết quả (ghi chú tuỳ chọn, popup = bước xác nhận §6c) / Không duyệt (bắt buộc lý do); màn Chi tiết bỏ hẳn khối Ghi chú duyệt (user 19/10: không hiện cả bản chỉ đọc; ghi chú nằm ở Lịch sử)
- [x] Fix K6 (user 19/10): nút Hoàn thành (bước Xử lý) hỏi `$confirm()` trước lớp tải (button-convention §6c)
