# Plan — Phiếu nhập kết quả CSKH (ERP → HRM) — @khoipv

Spec: `docs/superpowers/specs/gop-db/2026-11-02-phieu-nhap-ket-qua-design.md` · Khảo sát: `khao-sat-A-*.md`, `khao-sat-B-*.md`

## Phase 0 — Khảo sát + chốt
- [x] T0 Khảo sát ERP (2 agent song song) → khao-sat-A / khao-sat-B; user chốt 5 điểm (02/11)

## Phase 1 — BE nền + danh sách / chi tiết / xóa / không duyệt
- [x] T1 Entities `WrImportResult/*` (16 bảng) + `AssignTaskSerialProgress` + `WrAssignTaskTimesheet`; hằng status + `status_color`; `canView/canEdit/canApproveResult`
  - `Entities/WrImportResult/` 16 file (bảng `wr_import_result_services` đặt tên `WrImportResultPaidService` để không trùng service); `WrAssignTask/AssignTaskSerialProgress` + `WrAssignTaskTimesheet` (không dùng lại `TpWrAssignTaskTimesheet` vì thiếu `time_actual`); thêm `AssignTaskProgress::serialProgress()`, `WrAssignTask::timesheets()`.
  - canView/canEdit/canApproveResult đặt ở `WrImportResultService` (viewer cache 1 lần/request, cờ danh sách không N+1). Màu: 1 xám #6B7280 · 2/4/5 vàng · 3 xanh · 6 đỏ.
- [x] T2 Seeder 4 quyền type 24 + `permission:sync --dry-run`
  - 4 dòng `perm` group "Phiếu nhập kết quả" ngay sau quyền PGV. Dry-run: thêm 15 (4 quyền PNKQ + 11 quyền của màn khác chưa sync local: 3 PGV, 7 hạch toán DV, 1 chuyến xe) · sửa/đổi tên/gỡ 0. CHƯA chạy sync thật.
- [x] T3 `WrImportResultService` list (searchByFilter y ERP, sort, keyword) + meta + resource danh sách
  - Route `/v1/customer-care/wr-import-results` (auth:api, không checkPermission). Phạm vi port nguyên 4 nhánh (kể cả `wait_approve_result` không quyền / type lạ = không bó). Mặc định `type=index`. Sort `code|wr_assign_task_code|created_at|status`.
  - Smoke NV13 (SA) `type=all` total 6 916 = SELECT tay; NV1010 (không quyền) 28 = SELECT tay; 13 bộ lọc/sort chạy 200.
- [x] T4 Show (port getForEdit + hậu xử lý show) + 403
  - Port y ERP (delivery_qty=qty, rate_effort SC kiểu boolean, BH type_status không guard → ném lỗi; DB hiện 0 ca). Thông tin KH ghi đè từ PGV như JS ERP. Ảnh → mảng URL `publicUrl()` (path tương đối ghép ERP_URL). Trả thêm `timesheets`, `wr_assign_task`, cờ quyền.
  - LỆCH: chưa ghép `serials`/`product_stock_qty` từ `getListProductOfCustomer` (màn Xem không hiển thị) → làm ở T7/T8. Smoke 7041/7047/7045/7046/7034(BH)/226(SC không lỗi) 200; 404; NV1010 xem 7041 → 403.
- [x] T5 Delete (port y ERP + 409 + lịch sử) · Reject (port y ERP + thông báo + lịch sử)
  - Delete: Eloquent y ERP (bỏ sót bảng con, GVK không guard → lỗi 400 + rollback); 403 không phải người tạo, 409 trạng thái; log `delete` + log PGV change_status. Reject: 422/409/403, ATP 6 nhánh, `is_assign` tính lại cho MỌI PGV có HĐ (y ERP — chỉ tab BH đọc cột này), thông báo `[PNKQ] Không duyệt` sau commit (`WrImportResultNotifier`).
  - Test trong transaction + rollBack: delete 6573/2761 (GVK), 5389/3999 (BH), 4644 (HĐ) + 403 + 409; reject 7047/7034/7031/7025/7020 + 409 + 422 — số dòng đổi khớp ERP, rollback sạch. Thông báo dùng bản giả (không gửi thật).
- [x] T6 Print + Export (`ExportColumnRegistry`) + `CatalogHistoryService::TABLES`
  - `WrImportResultPrintService` tự dựng HTML (ERP không có mẫu in) theo khung mẫu PGV 440; `/print` trần 2 000 dòng. `/export` (DynamicExport, 56 dòng ~12s) + `/export-rows` (khuyên dùng). Registry `wr_import_results` 10 cột; TABLES `wr_import_results`; lịch sử qua route chung `catalog-histories/wr_import_results/{id}`.

### Checkpoint — 02/11/2026
Vừa hoàn thành: Phase 1 BE T1–T6 (chưa commit)
Đang làm dở: —
Bước tiếp theo: T7 `CustomerDeviceListService` (port `Customer::getListProductOfCustomer`) rồi T8 source-data / edit-data
Blocked: 

## Phase 2 — BE form tạo / sửa
- [x] T7 `CustomerDeviceListService` (port `Customer::getListProductOfCustomer`)
  - `Services/CustomerDeviceListService::forCustomer()` chỉ đọc: Tân Phát (UNION phiếu xuất HT + mượn/bán, gộp `product_id-code-name` cùng thiết bị cũ) + NCC khác; `serials` đang dùng (tp khớp product_id; ncck khớp id+tên+tên không bán). KHÁC ERP: không dựng `device_errors` / `services` (PNKQ không đọc). Không đụng `CustomerManagerService`.
  - Show / edit-data: BH / SC phiếu có HĐ dịch vụ gắn `serials` + `product_stock_qty` (key `product_id|product_type`, tpc→tp) như getForEdit. `WrImportResultService::show()` → `detail($id, show|edit)`.
- [x] T8 `source-data` (port getForDataImportResult + create) · `edit-data` (port getForEdit + edit)
  - `Services/WrImportResultSourceService`: `GET /source-data?wr_assign_task_id=` (không kiểm quyền, 404) trả `{wr_assign_task, timesheets, creator_name, created_time}`; `GET /{id}/edit-data` (404/403 canEdit) — edit: SC `type_status` không guard, lắp đặt lấy lại `rate_effort/exportable_*`, P3 tự thêm `new=true`, rate_effort `|| 0` boolean.
  - `workerQtyConfig` chép lại (bản PGV protected — không sửa service màn khác).
- [x] T9 `WrImportResultRequest` + `checkValidateSerial` + `hasProductExport`
  - FormRequest port nguyên (rule ghi đè giữ hành vi; SC closure chết → `nullable`); câu required = "Bắt buộc phải nhập" (lang vi). `prepareForValidation` decode 5 mảng chuỗi JSON.
  - `Services/WrImportResultValidationService`: trả 422 `{success:false, type:'check_serial', message}` / `{type:'check_product_export', message:'Cảnh báo !', data:{exportable_id: HTML}}`.
- [x] T10 Store / Update (sync 14 bảng + PGV status + ATP 6 nhánh + serial progress + is_assign) + thông báo Gửi duyệt + upload-galleries S3
  - `Services/WrImportResultStoreService` (precheck → transaction → notify sau commit), giữ lỗi ERP 7.3-7.8/7.13/7.17-7.21; code tạm `TMP-uuid` rồi `{cty}.PNKQ.{YYYY}{id6}`; ảnh URL `ERP_URL…` cắt về path tương đối; lịch sử create/update/change_status + PGV change_status.
  - `WrImportResultNotifier::notifyWaitingApproval()` — `[PNKQ] Chờ duyệt`, người có quyền "Duyệt phiếu nhập kết quả" cùng công ty người thao tác, `url` = ERP_URL + `/admin/customer-care/wr_approve_results/create?wr_import_result_id=`.
  - `POST /upload-galleries` (`files[]`, `kind`) → S3 `wr_import_result_construction|handover`, so đuôi bằng closure, ≤5MB.
  - Smoke (NV13, transaction + rollBack, max id giữ 7047): source-data 5 loại (14574/14580/14307/14581/14559) 200, 404; edit-data 7041/7047/7045/7034/6573/3999 (đăng nhập người tạo, status tạm 1) 200, NV13 → 403; store→edit-data→update×2 cho SC/BH/PL/BD/bán thêm/lắp đặt/GVK/P3 200 — BH sửa nhân bản dịch vụ (1→2→3), device_errors mồ côi tăng mỗi lần sửa, PGV 1→7/2, ATP + serial progress cập nhật; lỗi: required, trùng phiếu, PCT, ảnh bắt buộc, P3 > ĐM, trùng khi sửa, 404, check_serial, serial SP khác / trùng danh sách, check_product_export; upload sai đuôi / >5MB / kind 422. CHƯA: upload S3 thật, gửi thông báo thật (dùng bản giả).

### Checkpoint — 02/11/2026 (Phase 2 BE)
Vừa hoàn thành: T7–T10 BE (chưa commit)
Đang làm dở: —
Bước tiếp theo: T11 FE danh sách / T12 form (contract API trong docblock `WrImportResultController::save()` + `WrImportResultRequest`)
Blocked: deep-link thông báo là URL ERP tuyệt đối — chuông FE `$router.push(url)` không mở được URL ngoài (cần FE xử lý http → window.open)

- [x] T10b Thông báo "Chờ duyệt" đổi deep-link từ URL ERP tuyệt đối sang chi tiết HRM `/customer-care/wr-import-results/{id}` (chuông FE mở bằng `$router.push`, URL ngoài không mở được; chi tiết có nút "Duyệt kết quả" mở ERP) — tránh sửa hàm dùng chung `CustomNotifyHeader` (02/11). `WrImportResultNotifier.php`, `php -l` OK

## Phase 3 — FE
- [x] T11 Danh sách `index.vue` (+ In/Xuất/Cấu hình cột/Lịch sử, Không duyệt popup)
  - `pages/customer-care/wr-import-results/index.vue`: 3 lối vào `?type=all|wait_approve_result|(index)`, khoá `wr_import_results_{type}` riêng cho bộ lọc / cấu hình cột / cài đặt bộ lọc. 12 cột (Số PNKQ → chi tiết HRM; Số PGV → HRM tab mới; Số HĐ: HĐ/PL → `wr-service-contracts`, BH (type 2) → `wr-warranties`, lắp đặt → HĐ bán ERP qua `utils/contract-link.js`; Số Y/C → ERP qua `ERP_ASSIGN_PATHS` của `wrAssignTaskLinks.js`). Sort `code|wr_assign_task_code|created_at|status`. Lọc: keyword (tìm nhanh) + 8 ô nâng cao, tên khoá trùng `WrImportResultService::filteredQuery`.
  - Hành động: Sửa (`to` edit) · Xóa ($confirm QLDA_006 → toast câu BE) · Duyệt kết quả (ERP tab mới) · Không duyệt kết quả · Lịch sử (`CatalogHistoryModal`, bảng `wr_import_results`). Toolbar: In danh sách (`reportPrintPreviewMixin` → `/print`) · Xuất Excel (`ExportFieldsModal` + `exportListFile` → `/export-rows`, 10 trường trùng `ExportColumnRegistry`) · Cấu hình cột.
  - Popup Không duyệt: KHÔNG tạo component mới — dùng `$confirm` (base-confirm-modal) có sẵn `showInput` + `requiredInput` (lỗi inline `is-invalid` + `invalid-feedback`, tự `trim()`). Gói options + PUT reject + toast vào `components/wrImportResultActions.js` (`REJECT_CONFIRM_OPTIONS`, `rejectImportResult(vm, id)`, `openApproveResult(vm, id)`, `API_PREFIX`, `LIST_URL`) để màn chi tiết (T12) gọi y hệt. (`components/modal/V2BaseRejectApproveModal.vue` cũng có nhưng lỗi inline không viền đỏ, thiếu câu hỏi → không dùng.)
  - Đã bám màn **Phiếu giao việc** `pages/customer-care/wr-assign-tasks/index.vue` ở khối vỏ trang / lối vào theo `?type=` / filterStateMixin + lưu nhãn KH / lọc KH remote / phân trang / In / Xuất export-rows / Lịch sử / link chứng từ nguồn; popup lý do bám `base-confirm-modal` (skill modal-popup §3a).
  - Verify: vue-template-compiler + babel parse OK; grep tự kiểm skill erp-to-hrm-screen sạch (2 dòng "không thành công" là câu dự phòng lỗi, 1 dòng V2BaseSelectRemote có `height` ở dòng dưới); smoke API NV13: list/13 bộ lọc + 4 sort/wait_approve_result/meta/print/export-rows đều 200, khoá dòng đủ field FE dùng. CHƯA mở trình duyệt.
  - ⚠️ Lệch skill `list-page` (chốt 24/08: "Không duyệt" chỉ ở màn chi tiết, Duyệt ở danh sách chỉ điều hướng chi tiết) — làm theo spec mục 2 (ERP có ở danh sách; Duyệt → ERP). Chờ user xác nhận.
- [x] T12 `WrImportResultForm.vue` + bảng con + `create.vue` / `_id/edit.vue` / `_id/index.vue`
  - Logic thuần `components/wrImportResultBuild.js` (port class JS ERP, chạy được bằng node): `buildForm(data, create|edit|show)` = `set wr_assign_task` + `calculate*()` + `after()`/setter KẸP lúc nạp; `productApprove` / `extendServiceApprove` / `computeTotals` (`rate_effort_main` bỏ BH khi có SC/BD — lỗi ERP giữ); `buildPayload` y `submit_data` (3 mảng lắp đặt/SC/BH chuỗi JSON); `validateForm` FE = BE; `clearNewSerials` (check_serial); `hourDifference`.
  - UI: `WrImportResultForm.vue` (3 tab `V2BaseTabNavigation` — tab Ảnh đỏ khi lỗi ảnh; card A theo nguồn · B P3 + II Tổng công định mức · C bán thêm · Ghi chú duyệt chỉ đọc · `SystemInfoSection` · `V2Footer`; popup `check_product_export` = `V2BaseModal` v-html câu BE + nút Đóng mặc định) + bảng con `WrImportResult{Device,Maintain,Assembly,RevenueCost,P3Work,Merchandise,Timesheet}Table.vue`, ô `WrImportResultPercentCell` (kẹp % y ERP: < 100 / tick = 100; BD > 100 → 100), `WrImportResultSerialCell`, `WrImportResultGallery` (chặn đuôi / 5MB FE → `POST upload-galleries` ngay → `AttachmentGallery` có sẵn: thumbnail / icon file / xem trước `FilePreviewModal` / × gỡ khỏi mảng).
  - Trang: `create.vue` (`?wr_assign_task_id=` sai → 404; source-data 404 → 404, lỗi khác → toast câu BE + về chi tiết PGV), `_id/edit.vue` (403/404 → 404, `markFormPristine` sau nạp), `_id/index.vue` (tiêu đề "Chi tiết phiếu nhập kết quả: {code}" + badge `buildStatusTitle`, X-Silent-Errors). Quay lại = nơi đi vào (`from.fullPath`), mặc định `?type=all`.
  - Nút: Lưu (secondary `ri-save-3-line`, status 1) · Lưu và gửi duyệt (primary `ri-send-plane-line`, status 2, LUÔN `$confirm` — không có mục hoàn thành thì câu ERP "Phiếu không hoàn thành công việc, bạn có đồng ý không?"). Chữ "Lưu và gửi duyệt" thay "Lưu & Gửi duyệt" (button-convention §4.1 cấm `&`, khớp #11978 PGV "Lưu và duyệt"). Chi tiết: Sửa · Duyệt kết quả (ERP tab mới) · Không duyệt (`rejectImportResult` dùng chung danh sách) · Xóa.
  - Đã bám màn **Phiếu giao việc** (`WrAssignTaskForm.vue`) ở vỏ form / khối Thông tin KH (`v2-linked-field`, `CreatorInfoLine`) / bảng con (`V2BaseTableScroll` + `v2-form-table`, dòng tổng, "Không có dữ liệu" trong bảng) / ô số (tái dùng `WrAssignTaskNumberCell`, `wrAssignTaskCalc.fmt`) / P3 thêm-xoá đúng index (`removeRowErrors`) / validate (mọi ô đỏ cùng lúc + `scrollToFirstError`, 422 map khoá dòng, khoá lạ toast) / trang vỏ + unsaved; màn **Danh sách PNKQ** (`wrImportResultActions.js`) ở Không duyệt / Duyệt kết quả / Xóa; **Hồ sơ nhân sự** (`AttachmentGallery`) ở khối ảnh.
  - Verify: vue-template-compiler + babel parse 19 file OK; grep tự kiểm skill erp-to-hrm-screen sạch (hit "thành công'" chỉ là câu dự phòng lỗi). Node chạy logic FE trên API thật: source-data 8 PGV (14574 HĐ, 14580 BH, 14307 PL, 14581 lắp đặt, 14559 GVK, 14538 SC+BD, 14496 bán thêm, 14569 vật tư) + show 7041/7047/7045/7034 + edit-data 5389/4644 (người tạo; NV13 → 403). Tổng công FE = số ERP trong DB: 7041 SC 1.9 · 7047 lắp đặt 0.07 + P3 1.8 · 7034 BH 0 + P3 0.5 · 7045 GVK 0.7 (DB 1.00 do bước duyệt, setter ERP kẹp về ĐM 0.7).
  - POST/PUT payload FE dựng qua HTTP kernel trong transaction + rollBack (thông báo giả, max id giữ 7047): 13 ca 200 (tạo SC/BH/PL/lắp đặt/GVK/SC+BD/vật tư; sửa 7047/7034/7045/7041) — số dòng bảng con khớp; 9 ca lỗi FE = BE đúng khoá + câu (ảnh bắt buộc, BH serial bắt buộc / "Không ghi nhận số 0", P3 tên + ĐM bắt buộc, CK > ĐM, serial lắp đặt trùng / bắt buộc); PCT chưa duyệt → 422 `{success:false,message}` (FE toast).
  - Phát hiện khi đo BE: serial SC KHÔNG bắt buộc (rule khoá cụ thể `nullable` ghi đè rule wildcard — Laravel) → FE bỏ bắt buộc serial SC cho khớp (docblock `WrImportResultRequest` ghi "wildcard vẫn áp" là sai, hành vi = ERP nên không sửa BE).
  - CHƯA kiểm chứng: mở trình duyệt (bố cục, tab, rowspan serial, popup Cảnh báo, cảnh báo chưa lưu); upload S3 thật (`upload-galleries`); nhánh `check_serial` / `check_product_export` chỉ đọc code (chưa có dữ liệu dựng ra).
- [x] T13 Menu + nối PGV (Nhập kết quả / Xem phiếu nhập KQ → HRM)
  - [x] Menu: `components/subsystem-menu/customer-care.js` nhóm Giao việc thêm "Phiếu nhập kết quả" → `/customer-care/wr-import-results?type=all` ngay sau "Phiếu giao việc được giao", không `isShow` (như các mục PGV bên cạnh, ERP không gate). Grep các file menu khác (`components/*.js`, `default-menu`, `layouts`, `utils`…) không còn chỗ nào khai màn PGV/PNKQ → không thêm nơi khác.
  - [x] Nối PGV (`wrAssignTaskLinks.js`, `wr-assign-tasks/index.vue`, `WrAssignTaskForm.vue`) → HRM
    - `importResultCreateUrl(taskId)` → `/customer-care/wr-import-results/create?wr_assign_task_id=`; `importResultShowUrl(id)` → `/customer-care/wr-import-results/{id}`, id 0/null → '' (bỏ 2 path ERP khỏi `ERP_ASSIGN_PATHS`).
    - Danh sách PGV: 2 hành động dùng `to:` (nuxt-link, chuột phải mở tab mới); chi tiết PGV: `$router.push` cùng tab.
    - "Xem phiếu nhập kết quả" khi chưa có phiếu (BE `is_can_view_import_result` theo trạng thái PGV, `import_result_id = 0`): ERP mở `0/show` ra "không tìm thấy" → HRM **ẩn nút** (skill: nút không dùng được thì ẩn; giữ y ERP thì user bấm ra trang 404).
    - `WrAssignTaskForm.vue` đang có thay đổi chưa commit của người khác (#11978 "Lưu và duyệt") — chỉ sửa đúng 2 chỗ nút, không đụng phần kia.

## Phase 4 — Verify
- [x] T14 Kiểm tổng (02/11): `php -l` sạch mọi file BE mới/sửa; 13 route gọi thật qua HTTP kernel (NV 13): meta, list all (6.916) / index, show 7041·7047·7045·7034, id lạ 404, source-data 14574·14581, print, lịch sử, list PGV — đều đúng mã; compile 17 file FE + 4 file PGV/menu OK; bộ grep skill sạch
  - ⚠️ CHƯA mở trình duyệt; CHƯA upload S3 thật; CHƯA gửi thông báo thật; `check_serial` / `check_product_export` FE chỉ đọc code; 4 quyền chưa `permission:sync` thật
  - Lỗi ERP giữ nguyên có chủ ý (user chốt): serial lắp đặt `is_serial` reset khi đổi SL, "Công khoán chính" bỏ công BH khi có SC/BD, nhãn "Không duyệt" như ERP
  - ⚠️ `WrAssignTaskForm.vue` đang lẫn sửa đổi chưa commit của #11978 (cuộc trò chuyện khác) — commit thì tách đúng phần

### Checkpoint — 02/11/2026 (code xong, chờ test trình duyệt)
Vừa hoàn thành: T0–T14 (BE + FE trọn bộ, nối PGV, menu)
Đang làm dở: —
Bước tiếp theo: `php artisan permission:sync` local + gán 4 quyền cho role test → user mở trình duyệt test: PGV → Nhập kết quả → Lưu / Lưu và gửi duyệt (5 loại) → danh sách → chi tiết → Sửa → Xóa / Không duyệt; thử upload ảnh S3
Blocked:

- [x] Chốt sau Phase 1 (02/11, user: "cứ làm như erp cho tôi"): giữ y ERP (1) Không duyệt tính lại `wr_service_contracts.is_assign` cho MỌI PGV có HĐ (kể cả HĐ/PL — cột chỉ tab BH đọc); (2) `type=wait_approve_result` không có quyền duyệt = không bó phạm vi. Code đã đúng như vậy, không sửa gì.
