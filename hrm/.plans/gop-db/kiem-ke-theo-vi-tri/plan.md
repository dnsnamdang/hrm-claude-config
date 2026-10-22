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
- [x] Fix K7 (user 20/10, chọn "sửa gốc"): header khối trên hrm-crm khác local — chuẩn header chung 19/10 (`body .card .card-header.section-header`, commit `53421e1cb` @dnsnamdang) nằm trong style của `V2BaseFormSection.vue` nên chỉ ăn khi trang đã nạp component đó. Chuyển nguyên khối sang `assets/scss/default.scss` (nạp toàn cục qua app.scss; xác nhận bundle server dùng bản .scss, không phải default.css), bỏ bản trong V2BaseFormSection. Dọn rule `.section-header` tự khai ở 3 form họ Kho: PositionInventoryForm, PositionInventoryResultForm, PositionTransferForm. Phạm vi tự đổi theo: 49 file có `card-header section-header` (`inventory.py --has "card-header[^\"]*section-header"`); màn có selector riêng mạnh hơn (v2-attach-card, form giữ hàng) giữ kiểu cũ
- [x] Fix K8 (user 20/10 "sửa giống màn bảo hành"): 3 màn họ Kho (Kế hoạch kiểm kê · Phiếu kiểm kê · Điều chuyển vị trí) bỏ `.card` + `.card-header` tự dựng → `V2BaseFormSection class="mb-2"` (khuôn `customer-care/warranty-repair-requests`); AttachmentSection + SystemInfoSection `mb-2`; khối Chi tiết điều chuyển (`card-body p-0` cũ) bọc `.section-flush { margin:-10px }`; 9 trang vỏ create/edit/_id bỏ `v2-styles min-vh-100 pt-2` + `container-fluid` → `<div>` như màn Bảo hành. Compile 12 file OK, nuxt dev 200 ×3; CHƯA mở trình duyệt

## Fix 20/10 — dấu * trường bắt buộc (đối chiếu rule BE)
- [x] Ngày kiểm kê thêm `*` (đồng bộ màn Kế hoạch #11772)
- [x] Cột "ĐVT kiểm kê" thêm `*` khi nhập (BE `results.*.unit_id` required) — prop `unit-required` của DetailTable dùng chung (mặc định tắt, màn Kế hoạch không đổi)
- Đã đủ từ trước: Kho vật lý, Nhà/Dãy/Khoang/Vị trí, Chi tiết, Thực kiểm (lúc nhập kết quả), Hội đồng kiểm kê + Nhân viên + Chức vụ. Kế hoạch kiểm kê = tuỳ chọn (BE nullable)

## Fix 20/10 — popup Chọn kế hoạch lệch ERP (user: "sửa cho giống ERP")
- [x] `PositionInventoryResultService::plansQuery()` bám ERP `searchByFilter` nhánh `wait-approve` (M:774-778): bỏ ngoại lệ Super admin (ERP Super admin vẫn phải là thủ kho) + đổi "kho ĐẦU TIÊN là kho mình" → "có kho BẤT KỲ trong kế hoạch là kho mình" (`whereHas warehouses`). `planData()` / `store()` giữ `canCreateResult()` (= ERP `canApprove()` dùng kho đầu + Super admin bypass)
  - Verify: php -l OK; tinker dựng query với employee 13 → SQL đúng (`status=1 AND id IN (pivot kho thủ kho) AND type=0`), local không có kế hoạch Đang kiểm nên count=0. CHƯA thử trên hrm-crm

## Redmine #11803 — Tạo mới (21/10)
- [x] K1. Ẩn tooltip (hint) ô Kho vật lý
- [x] K2. Nút "Lấy vị trí" lên header khối Phạm vi kiểm kê (màn Kế hoạch đã có sẵn trong working tree)
- [x] K3. Nút "Thêm dòng" lên header khối Hội đồng kiểm kê
- [x] K4. Ô Nhân viên / Chức vụ rộng bằng nhau (đo dev: chữ cùng 12px, chỉ lệch rộng 638 vs 479px) — áp cả màn Kế hoạch
- [x] K5. Chi tiết: ẩn khối File đính kèm khi chưa có file (trừ lúc nhập kết quả) — ERP chỉ đính kèm ở bước nhập kết quả, không thêm vào form tạo
  - FE `PositionInventoryResultForm.vue` (K1–K5, bỏ class `.pi-soft` hết chỗ dùng) + `position-inventories/components/PositionInventoryForm.vue` (K4). Verify: vue-template-compiler + babel OK. Chưa mở trình duyệt.

## Redmine #11787 — In (22/10)
- [x] I1. In danh sách: tiêu đề cột "Kế hoạch KK" → "Kế hoạch kiểm kê" (`PositionInventoryResultPrintService::listHtml`)
- [x] I2. In chi tiết: vùng thông tin lệch (mẫu 286 khai ô px cứng 228/160/169 + căn giữa dọc) và khối ký lệch dòng (ô "Trưởng bộ phận kho" thừa `<div>&nbsp;</div>`) → `alignResultLayout()` dựng lại 2 bảng lúc in (không sửa `report_templates`): 3 ô `colgroup` 38/22/40% căn trên; bảng ký 3 cột căn trên
- [x] I3. In chi tiết: bảng nhảy sang trang 2 — CSS in chung `tr { page-break-inside: avoid }` + ô gộp Nhà kho/Vị trí (rowspan cả nhóm) → Chrome không cắt, đẩy cả bảng. Dòng mở ô gộp gắn inline `break-inside: auto` (chỉ bản in, không đụng Excel)
  - Verify: php -l OK; tinker dựng HTML phiếu id 139 + CSS `buildReportPrintCss('body')` → Chrome headless in PDF: trước 5 trang (trang 1 chỉ đầu phiếu), sau 4 trang (bảng bắt đầu trang 1); chụp ảnh vùng thông tin + ký thẳng hàng. Chưa mở popup thật trên trình duyệt

## Redmine #11786 — Danh sách (22/10) — khuôn #11770/#11771 (Kế hoạch) + R1–R3 (Điều chuyển vị trí)
- [x] L1. Đổi tên tiêu đề trang + tiêu đề bảng → "Kiểm kê theo vị trí" (menu đã đúng sẵn)
- [x] L2+L3. Bộ lọc Công ty → khối chuẩn `V2BaseCompanyDepartmentFilter` (slot `#field-org`, xem được cả công ty đã khoá; `is_company` theo quyền "Xem phiếu kiểm kê vị trí - theo công ty") + BE lọc `department_id`
- [x] L4. Người tạo / Người duyệt = toàn bộ nhân viên (`$store.state.employeeOptions`); BE `filterOptions()` bỏ `creators`/`approvers`/`companies`
- [x] L5. Bảng: bỏ sort Trạng thái / Người tạo / Người duyệt / Ngày duyệt; thêm sort Kho (key `warehouse_names`, BE sắp theo MIN(tên kho) qua pivot); sort mặc định trống → icon trung tính (BE vẫn `created_at desc`); thêm cột Ngày cập nhật + Người cập nhật (join `updated_by`) ở bảng + Xuất Excel
  - Verify: vue-template-compiler + babel OK; php -l OK; HTTP kernel: filter-options 200, list có updated_at_full/updater_name, lọc phòng ban 72 → 5 = DB 5, sort Kho asc/desc đúng thứ tự, sort status bị bỏ qua. Chưa mở trình duyệt
