# Plan — Phiếu yêu cầu lắp đặt, bàn giao (ERP → HRM) — @khoipv

## Phase 0 — Khảo sát & chốt
- [x] Đọc ERP: controller, model, StoreRequest, blade index/form/show/edit, JS class, `FirmContract::getInstallableAvailableQty`, popup HĐ
- [x] Đối chiếu HRM: entity `AssemblyRequest` (PGV đọc), quyền catalog có sẵn, menu, màn khuôn `assign-other-requests`
- [x] Chốt: 2 nguồn HĐ · phân quyền y ERP · sửa/xoá y ERP · subagent Opus 5.5
- [x] Chốt: ĐƯỢC sửa hàm dùng chung `AssignOtherContractSourceService::contracts()` (thêm tham số tùy chọn bỏ lọc "HĐ đã có phiếu", mặc định giữ hành vi cũ) · HĐ HRM chỉ lấy `need_install = 1`

## Phase 1 — BE (hrm-api `Modules/CustomerCare`)
- [x] B1 Migration `2026_11_16_000001_add_hrm_contract_id_to_assembly_requests_table.php`: `hrm_contract_id` nullable + `firm_contract_id` nullable — đã migrate local. `need_site_survey` có sẵn trên DB local (không tạo lại)
- [x] B2 Entity `AssemblyRequest` mở rộng (fillable, STATUSES màu SRS thứ tự theo luồng, `CONTRACT_TYPES`, `contractSource()/contractId()`, `files()`)
- [x] B3 Quyền: thêm `hrm` vào platforms `phieu_yeu_cau_lap_dat_ban_giao.view` + `..._truong_phong.approve` (`phieu_cho_giao_viec.view` đã có hrm); `permission:catalog-sync` local đã chạy (sync cả các mã người khác thêm: +6, ngừng 1 `sale.bao_cao_giu_hang.view`)
- [x] B4 `Services/InstallableContractQtyService.php` (firm + hrm, HRM chỉ `need_install = 1`). Sửa hàm dùng chung `AssignOtherContractSourceService::contracts()` thêm `$options` (`exclude_used`, `hrm_need_install`) — so cũ/mới 48/48 giống
- [x] B5 `AssemblyRequestService` danh sách (all / wait-approve / index qua `HrmScopeContext` + OR mình tạo), lọc ngày theo `date_expected`, sort, meta, export-rows (`ExportColumnRegistry`)
- [x] B6 `AssemblyRequestRequest` + `AssemblyRequestStoreService` (details lấy thông tin hàng ở máy chủ, kiểm SL ≤ còn yêu cầu được, progress `contract_type` theo nguồn, files, mã `YCLDBG`, thông báo `AssemblyRequestNotifier`), xoá cứng. Lệch ERP: Người liên hệ bắt buộc khi `customer_type` ≠ 1 (ERP chỉ = 2); SL tích phải > 0; chặn xoá khi đã có PGV (422)
- [x] B7 Approve / Reject (`approve_comment`) / Change department (403/409), show + edit-data (+`available_qty`), không xem được → 404. Bổ sung canView: nhân viên phòng tiếp nhận xem được phiếu Chờ giao việc (để bấm Tạo PGV / Từ chối / Chuyển phòng)
- [x] B8 Lịch sử (whitelist `assembly_requests` + 2 khoá ảo bảng), in 1 phiếu (dùng lại `Modules\Assign\Services\AssemblyRequestPrintService` mẫu 368 — letterhead theo công ty phiếu), in danh sách mẫu 367 (trần 2.000, "Tất cả"), Excel 1 phiếu `AssemblyRequestExport` + blade `customercare::exports.assembly_request`
- [x] B9 Downstream: `WrAssignTaskSourceService`, `WrAssignTaskService`, `WrAssignTaskStoreService::writeAssemblyProgress` (contract_type), `Modules/Assign WaitingAssignTaskService`, `InstallDeliveryRepairReportService` (snapshot trước/sau trùng khít). CHƯA: `InstallDeliveryRepairDetailReportService` tab Lắp đặt (chỉ HĐ hãng)
- [x] B10 Smoke HTTP qua kernel (4 kịch bản, rollback): danh sách / meta / popup / contract-data / validate / tạo nháp / gửi duyệt / duyệt / từ chối / chuyển phòng / xoá / in / Excel / lịch sử / nguồn HĐ HRM / PGV source-data / phiếu chờ giao việc. API contract ghi ở spec mục 9

### Checkpoint — 2026-11-16
Vừa hoàn thành: Phase 1 BE (B1–B10)
Đang làm dở: —
Bước tiếp theo: Phase 2 FE theo spec mục 9; FE thêm case `hrm` ở `report/install-delivery-repair/format.js docLink`, icon prefix `YCLDBG`
Blocked: DB local chưa ai có mã quyền mới (smoke dùng vai trò tạm trong transaction) — cần cấp ở `/admin/roles` khi test trình duyệt

- [x] B11 ERP (`D:\laragon\www\erp`, nhánh gop_db, CHƯA commit): null-safe mã HĐ khi phiếu gắn HĐ HRM (`firm_contract_id` NULL) — `AssemblyRequest::getPrintDataAttribute` / `printListData`, `AssemblyRequestController@searchData` cột Số HĐ. Còn: ERP `WrAssignTasksController` ~646 lấy `firm_contract.code` → rỗng với phiếu nguồn HRM (không lỗi)

## Phase 2 — FE (hrm-client `pages/customer-care/assembly-requests`)
- [x] F1 index.vue (khuôn assign-other-requests; 4 mixin + exportFields + reportPrintPreview, SmartFilterPanel floating, cấu hình cột, In danh sách `GET /print` (khuôn wr-assign-tasks), Xuất Excel `/export-rows`, lịch sử popup, `?type=all|wait-approve` — bộ lọc lưu riêng từng lối `assembly_requests_<type>`, watcher `$route.query.type`; lối chờ duyệt bỏ ô Trạng thái)
- [x] F2 Form dùng chung `components/AssemblyRequestForm.vue` (popup KH ChooseErpCustomerModal / người liên hệ + thêm nhanh / HĐ 2 nguồn / địa chỉ lắp đặt + thêm nhanh, bảng thiết bị tích chọn + chọn tất cả, SL lỗi theo dòng `details.N.qty`, Cần khảo sát V2BaseSegmented + V2BaseAttachmentSection `upload-attachment`, validate inline FE = BE)
- [x] F3 create / `_id/edit` / `_id` + footer Duyệt (confirm) / Tạo PGV / Sửa / Chuyển phòng (`AssemblyChangeDepartmentModal`, V2BaseSelectInModal) / In / Xuất Excel / Từ chối / Xóa + Ghi chú duyệt + Lịch sử SystemInfoSection; 403/404 → `/pages/extras/404`
- [x] F4 Menu `sale-hub.js` (link `?type=all`) + `menu-sidebar.js` chờ duyệt (link + codes TP duyệt); link ERP → HRM: `wrAssignTaskLinks.js` (`assemblyRequestShowUrl`, `assemblyContractLink` HĐ HRM), `wr-assign-tasks/index.vue`, `wr-import-results/index.vue` + `WrImportResultForm.vue`, `waiting-assign-tasks` (tab Lắp đặt link HRM, Xuất Excel endpoint HRM, cột HĐ có link HĐ HRM khi `hrm_contract_id`), `report/install-delivery-repair/format.js` (case `hrm` + YC lắp đặt HRM), `utils/notificationIcon.js` (`YCLDBG`)
- [x] F5 Compile (vue-template-compiler + @babel/parser, 20 file OK) + grep checklist skill erp-to-hrm-screen (sạch, còn dương tính giả: V2BaseSelectRemote khai `height` dòng dưới; câu fallback "… không thành công" của apiErrorMessage; `text-muted` chỉ trong comment)

Ghi chú lệch / quyết định FE (16/11/2026):
- Sửa component dùng chung của màn Giao việc khác (giữ mặc định cũ): `AssignOtherContractPickerModal` thêm prop `apiPrefix`/`subtitle`/`emptyText`/`filterTable`; `AssignOtherRejectModal` thêm `modalId`/`apiPrefix`/`commentField`. `AssignOtherContactQuickAddModal` dùng nguyên. → test lại popup chọn HĐ + Từ chối ở màn Giao việc khác.
- "Thêm nhanh" Địa chỉ lắp đặt: HRM chưa có API thêm địa điểm giao lẻ cho KH → chỉ ghi trên phiếu (`delivery_place`, `delivery_place_id` null), KHÔNG lưu vào KH như ERP. Cần BE nếu muốn y ERP.
- Chọn HĐ không còn hàng lắp được → toast "Không có sản phẩm để lắp đặt", giữ nguyên HĐ/bảng cũ. Bỏ HĐ / đổi KH → xoá bảng thiết bị.
- Tạo phiếu giao việc mở tab mới (khuôn Giao việc khác). Duyệt ở danh sách chỉ điều hướng chi tiết.
- `menu-sidebar.js` nhóm "Tiếp nhận công việc" còn mục chữ trần `YC Lắp đặt bàn giao` (cùng kiểu mục YCGVK chưa gắn link) — chưa gắn, chờ user chốt (nhiều khả năng ứng với tab chờ giao việc).

- [x] F6 Dòng danh sách BE trả thêm `department_reception_id` → popup chuyển phòng (mở từ danh sách) bỏ phòng hiện tại theo id

## Phase 3 — Verify
- [ ] V1 Smoke API + compile; user bấm trình duyệt
  - 16/11/2026: chạy E2E Playwright (53 test, `e2e/tests/customer-care/assembly-requests.spec.ts`) — user cho DỪNG giữa chừng. Đã qua nhóm Menu; bắt + sửa 1 lỗi phạm vi Tập đoàn chỉ thấy phiếu mình tạo (`AssemblyRequestService::applyScope`). Các nhóm còn lại CHƯA chạy. Đã thu hồi role tạm 100246, không còn phiếu test.

### Checkpoint — 2026-11-16
Vừa hoàn thành: BE B1–B11 (smoke HTTP rollback đạt), FE F1–F6 (compile + grep sạch).
Đang làm dở: không.
Bước tiếp theo: user cấp 2 mã quyền ở /admin/roles rồi bấm trình duyệt; chốt 3 điểm chờ (thêm nhanh địa chỉ lưu vào KH? · mục 'YC Lắp đặt bàn giao' nhóm Tiếp nhận công việc trỏ đâu · 4 điểm BE lệch ERP); thử lại popup HĐ + Từ chối màn Giao việc khác.
Blocked:

## Fix Redmine #12234 — CSS popup Chọn hợp đồng (19/11/2026)
- [x] Popup "Chọn hợp đồng" ở form tạo phiếu: câu rỗng dài (~870px) > khung popup lg, ô bảng `nowrap` → chữ tràn 2 bên, bảng cuộn ngang lệch, cắt tiêu đề cột. Sửa cục bộ `AssignOtherContractPickerModal.vue` (`::v-deep .dt-state-inner { white-space: normal }`), không đụng `V2BaseDataTable` dùng chung. Áp cho cả màn YC giao việc khác (cùng popup). Compile template + scss OK; chưa mở trình duyệt.
- [x] 21/11/2026 — user giao lại #12234: kiểm tra thấy fix đã có ở commit `2abab7b51` (hrm-client, đã lên `origin/develop`), issue chưa được chuyển trạng thái sau khi fix. Không sửa thêm code; chờ dev build lại để tester kiểm.

## Fix Redmine #12242 — 5 điểm QA màn Phiếu YC lắp đặt, bàn giao (21/11/2026)
- [x] 1. Popup "Chọn khách hàng" nhỏ lại + bỏ khoảng trắng dưới bảng — `ChooseErpCustomerModal` dùng chung 25 màn, user chốt SỬA CHUNG: cao theo nội dung (max 94vh, bảng cuộn), rộng 95vw trần 1640px (vừa tổng cột ~1580px); bỏ media query 1350px chết (bị `95vw !important` đè). Fullscreen giữ 100vh. node-sass không nhận `min()` → dùng width + max-width.
- [x] 2. Popup Thêm nhanh người liên hệ: nút × xoá nhanh trong 3 ô (khuôn `picker-text-field__clear` của PlanPickerModal)
- [x] 3. File đính kèm mất dung lượng khi Sửa/Xem: BE thêm `GET assembly-requests/{id}/attachment-sizes` (khuôn HandoverRecord), FE truyền `sizes-url`
- [x] 4. Bộ lọc thiếu so với ERP: thêm ô Số phiếu yêu cầu · Số hợp đồng · Tên/Mã hàng hóa (BE đã nhận `code`/`contract_code`/`product_keyword`)
- [x] 5. Cột "Người tạo" → "Người yêu cầu" y ERP (bảng + xuất Excel)

### Checkpoint — 21/11/2026
Vừa hoàn thành: 5 mục #12242 (FE: ChooseErpCustomerModal, AssignOtherContactQuickAddModal, AssemblyRequestForm sizes-url, index.vue 3 ô lọc + cột "Người yêu cầu"; BE: route/controller/service `attachment-sizes`, ExportColumnRegistry). Compile template + babel + node-sass OK; smoke HTTP: attachment-sizes 200 / id lạ 404, lọc `code` 200.
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt kiểm popup Chọn KH (ít/nhiều dòng, fullscreen ở Meeting) + nút × + dung lượng file (local không có phiếu nào có file).
Blocked:
