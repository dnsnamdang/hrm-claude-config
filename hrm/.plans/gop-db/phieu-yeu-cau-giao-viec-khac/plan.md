# Plan — Phiếu yêu cầu giao việc khác

> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-11-05-phieu-yeu-cau-giao-viec-khac-design.md`

## Phase 1 — Port trọn màn (2026-11-05)

### Khảo sát
- [x] T0. Khảo sát ERP (controller, model, request, 8 blade, nguồn HĐ, menu) + dữ liệu thật + chốt 3 câu hỏi với user

### BE (`hrm-api/Modules/CustomerCare`)
- [x] T1. Migration thêm `assign_other_requests.hrm_contract_id`
- [x] T2. Entity `AssignOtherRequest`: STATUSES + màu, fillable `hrm_contract_id`/`comment`, helper trạng thái
- [x] T3. `AssignOtherContractSourceService`: popup HĐ 2 nguồn + dịch vụ / QTC của HĐ
- [x] T4. `AssignOtherRequestService`: danh sách (phạm vi 3 cấp) · chi tiết · quyền · xoá · từ chối · meta · xuất · lịch sử
- [x] T5. `AssignOtherRequestStoreService` + `AssignOtherRequestRequest` (nháp / gửi) + `AssignOtherRequestNotifier`
- [x] T6. Controller + route; quyền seeder (3 quyền type 23); `ExportColumnRegistry`; `CatalogHistoryService::TABLES`; `NotificationMeta::OBJECT_LABELS`
- [x] T7. Smoke test API (transaction rollback) — super admin: CRUD/gửi/từ chối/xoá/lịch sử/2 nguồn HĐ; user 826 (không quyền) chỉ thấy 24 phiếu mình, từ chối 403; user 126 (phòng tiếp nhận 51) thấy 2.425, từ chối 200
- [x] T7b. Tách `CustomerAddressService` (địa chỉ KH y ERP — `customers` không có cột `address`); bản `WrQuotationService::customerAddressText()` còn private, CHỜ user duyệt chuyển sang gọi chung

### FE (`hrm-client`)
- [x] T8. `index.vue` danh sách (lọc, cột, hành động, xuất, cấu hình cột, lịch sử)
- [x] T9. Form dùng chung + popup HĐ + popup từ chối; trang create / edit / chi tiết
- [x] T10. Menu `sale-hub.js` + đổi link ERP → HRM: `wrAssignTaskLinks.js` (thêm `assignOtherRequestShowUrl`), `wr-assign-tasks/index.vue`, `wr-import-results/index.vue` + `WrImportResultForm.vue`, `waiting-assign-tasks/tabConfigs.js` (tab Giao việc khác `codeLink: 'hrm'` + `hrmShowPath`, `WaitingAssignTaskList.vue` đọc `hrmShowPath`)
- [x] T11. Compile FE + grep checklist skill erp-to-hrm-screen

### Còn lại
- [x] T12. Playwright local (05/11, user yêu cầu) — PASS: danh sách (8 cột, badge, tìm nhanh), tạo (validate 6 ô cùng lúc + toast QLDA_001, popup KH tự điền địa chỉ, select2 liên hệ / địa chỉ lắp đặt / phòng, popup dịch vụ, Lưu nháp), chi tiết nháp (Sửa · Xóa), sửa + chọn HĐ HRM (khoá Thêm/Xoá dịch vụ, lưu `hrm_contract_id`), bỏ HĐ, Lưu và gửi (popup xác nhận), chi tiết Chờ giao việc (Tạo phiếu giao việc · Từ chối), từ chối (trống báo lỗi, có lý do → Ghi chú duyệt), lịch sử 2 nơi, xoá ở danh sách. 0 lỗi console / API. Dữ liệu test (phiếu 2633–2635, 10 dòng lịch sử, 50 thông báo) đã dọn theo id.
  - Chưa test: Xuất Excel, Lưu và tiếp tục, popup HĐ hãng (tài khoản 13 không tạo HĐ hãng nào), luồng của tài khoản thường.
  - Ghi nhận nhỏ: ô select bị khoá (chưa chọn khách) không viền đỏ khi lỗi — chỉ có chữ lỗi bên dưới.
- [ ] T13. `php artisan permission:sync` thật (dry-run OK: +3 quyền type 23; DB local còn 35 quyền của feature khác chờ sync)
- [ ] T14. Chờ user duyệt: chuyển `WrQuotationService::customerAddressText()` sang gọi `CustomerAddressService` (bỏ bản trùng)
- [ ] T15. Chờ user quyết: vá ERP ô lọc "Từ ngày / Đến ngày" (lọc cột `expected_start_time` không tồn tại → lỗi SQL)

- [x] T16. (user yêu cầu 05/11) Popup "Chọn khách hàng" dùng chung (`components/modals/ChooseErpCustomerModal.vue`, 24 màn dùng): 3 ô lọc đổi sang khuôn ô lọc màn danh sách — `V2BaseFloatingField` + `V2BaseFilterFieldControl` (nhãn nổi trên viền, cao 32px, nút × xoá nhanh, Enter tìm). Logic tìm kiếm giữ nguyên. Playwright: nhãn nổi khi gõ, Enter gọi API đúng keyword, × và Làm mới xoá sạch.

- [x] T17. (05/11) Căn thẳng hàng nút Tìm kiếm / Làm mới với ô lọc ở popup Chọn khách hàng (bỏ `mb-2` từng nút, cao 32px) — đo Playwright: 5 phần tử cùng top/cao 32px.

- [x] T18. (05/11, chỉ kiểm) Đối chiếu nút với skill `button-convention`. Lệch: (1) footer form "Lưu nháp" phải đứng ĐẦU (§5) — đang sau "Lưu và gửi"; (2) cột Hành động danh sách: "Tạo phiếu giao việc" đứng trước Sửa (§5: Sửa → Xóa → ⋮) và có "Từ chối" (§5/list-page: phủ quyết chỉ ở chi tiết); (3) "Thêm dịch vụ" (thêm dòng) phải là `V2BaseQuickAddButton` (§6d); (4) popup xác nhận Xóa chưa nêu số phiếu (§6c); (5) popup Chọn khách hàng dùng chung: "Thêm nhanh" là `V2BaseButton secondary` thay vì `V2BaseQuickAddButton` (§6d, có từ trước). Chờ user quyết sửa.

- [x] T19. (05/11, chỉ kiểm) Rà riêng nút màn TẠO MỚI theo `button-convention`. Đúng: variant/màu/icon/chữ, `:interactable`, Quay lại tertiary đứng cuối (V2Footer), "Lưu và gửi" có $confirm, nút Xóa dòng V2BaseIconButton danger. Lệch 2 chỗ: (a) footer — "Lưu nháp" phải đứng đầu (§5); (b) "Thêm dịch vụ" đầu khối Danh sách cần giao việc phải là `V2BaseQuickAddButton` (§6d). Chờ user quyết sửa.

- [x] T20. (05/11, user "sửa đi") Sửa 2 lệch của T19 trong `AssignOtherRequestForm.vue`: footer Lưu nháp → Lưu và gửi → Lưu và tiếp tục → Quay lại; "Thêm dịch vụ" đổi sang `V2BaseQuickAddButton`. Compile OK, Playwright: thứ tự footer đúng, bấm chip mở popup Chọn dịch vụ.

### Checkpoint — 2026-11-05
Vừa hoàn thành: T0–T11 (BE + FE trọn màn, menu, link downstream). Verify: php -l, migration local, smoke API (rollback), compile FE, grep checklist.
Đang làm dở: không
Bước tiếp theo: user duyệt giao diện; T13 permission:sync
Blocked: T14, T15 chờ user

## Fix bug Redmine #12045 (2026-11-06)
- [x] B1+B2. Popup Chọn khách hàng / Chọn dịch vụ sửa chữa: ô "Số dòng/trang" + nút trang nhỏ hơn màn danh sách. Lần 1 sửa `V2BasePagination.vue` (bỏ size sm) → user đổi ý: ĐÃ HOÀN TÁC (git checkout), chuyển cả 2 popup sang `V2BaseDataTable` (B1b, B2b).
- [x] B3. `AssignOtherRequestForm.onPickCosts`: thêm xong → toast "Đã thêm N dịch vụ" + đóng popup
- [x] B4. Danh sách: bỏ sort cột Trạng thái (FE + `SORTABLE_COLUMNS`)
- [x] B5. Chi tiết phiếu: nhãn 5 trường bắt buộc luôn có (*) đỏ như ERP (`V2BaseLabel required`)
- [x] B6. Phiếu nhập kết quả: Duyệt xong (và Không duyệt từ màn duyệt) → về danh sách; Lưu nháp phiếu duyệt vẫn về chi tiết (`WrImportResultForm.vue`)
- [x] B7. Danh sách Phiếu nhập kết quả: bỏ sort cột Trạng thái (FE + `WrImportResultService::SORTABLE_COLUMNS`)
- [x] B8. (chỉ check) "Xem phiếu duyệt kết quả" ở danh sách / chi tiết PGV: hiện khi PGV có dòng con `wr_assign_tasks.parent_id` (= phiếu duyệt KQ) không ở trạng thái Đang tạo, mở trang ERP `wr_approve_results/{id}/show`. HRM đã gộp duyệt vào Phiếu nhập kết quả (khối "Kết quả duyệt") → hành động này thừa, link ra ERP. Đề xuất bỏ hoặc trỏ về chi tiết PNKQ HRM — chờ user quyết.
  - [x] B8b. (06/11, user "bỏ nút đó đi") Bỏ "Xem phiếu duyệt kết quả": hành động ở danh sách `wr-assign-tasks/index.vue` (+ hàm `openErpOrWarn` hết chỗ dùng), nút ở chi tiết `WrAssignTaskForm.vue` (+ `openUrl`, 2 field form), hàm `approveResultShowUrl` + path ERP trong `wrAssignTaskLinks.js`; BE `WrAssignTaskService::actionFlags` bỏ `is_can_view_approve_result`/`approve_result_id` + query `ctx[children]` (chỉ phục vụ nút này). Smoke API: danh sách PGV / PNKQ / YCGVK 200; sort Số hợp đồng desc đúng thứ tự.
- [x] B9. Danh sách: thêm sort Số hợp đồng (`contract_code` → `firm_contract_code`)
- Verify: compile 5 file FE OK, `php -l` 2 file BE OK. CHƯA mở trình duyệt.
- [x] B1b. (06/11, user đổi ý) Popup Chọn khách hàng `components/modals/ChooseErpCustomerModal.vue` (24 màn dùng) chuyển bảng b-table + V2BasePagination sang `V2BaseDataTable` như các popup chọn khác. Giữ nguyên vỏ b-modal id `choose-erp-customer`, props `scopeAll`/`quickAdd`, sự kiện `event`/`quick-add`, 3 ô lọc, tham số API. Click dòng bắt bằng `@click.native` + `tr.picker-row` (khuôn `HandoverContractPickerModal`, không sửa V2BaseDataTable); KH bị khoá đăng ký vẫn báo lỗi; bỏ code đồng bộ thanh cuộn tự viết (V2BaseDataTable có sẵn). Compile OK, CHƯA mở trình duyệt.
- [x] B2b. (06/11) Popup Chọn dịch vụ sửa chữa `device-errors/components/CostSearchModal.vue` (5 màn dùng) chuyển bảng + V2BasePagination sang `V2BaseDataTable`: cột ô tích (header chọn cả trang) / STT / Tên dịch vụ; bấm dòng = thêm ngay, bấm ô tích (cả ô cột đầu) = chỉ tích; giữ vỏ popup, ô tìm, nút Thêm N dịch vụ / Đóng, sự kiện `apply`/`close`. Compile OK, CHƯA mở trình duyệt.

## Fix bug Redmine #12049 (2026-11-06)
- [x] C1. Chờ giao việc → Đã giao việc (do PGV đổi) chưa ghi lịch sử. Thêm `AssignOtherRequestService::logStatusByAssignTask()` (dòng `change_status`, ghi chú "Phiếu giao việc {mã}"), gọi ở `WrAssignTaskStoreService::writeProgress` (tạo PGV → Đã giao việc) và `WrAssignTaskService` huỷ PGV (→ Chờ giao việc). Popup lịch sử danh sách + khối Lịch sử chi tiết cùng đọc `catalog_histories` nên cả 2 nơi có.
- [x] C2. Ô Người liên hệ: nút chip "Thêm nhanh" (`V2BaseQuickAddButton`, chỉ KH tổ chức + đã chọn KH) mở popup mới `AssignOtherContactQuickAddModal.vue` (Họ tên · Chức vụ · SĐT, đều bắt buộc), dùng lại API sẵn có `POST assign/customers/{id}/contacts` (Dự án / Meeting đang dùng); lưu xong thêm vào danh sách + chọn luôn.
- [x] C3. Popup Chọn dịch vụ sửa chữa (`CostSearchModal.vue`, dùng chung 5 màn): thêm cột Người tạo + sort Tên dịch vụ / Người tạo (BE `DeviceErrorController::getCostsAjax` join employees → employee_infos, `sort_by`/`sort_direction`).
- [x] C4. Lưu nháp chỉ bắt Khách hàng (user chốt): migration `2026_11_06_000001_make_date_expected_department_reception_nullable_on_assign_other_requests_table` (đã chạy local), FormRequest + FE validate chỉ bắt 2 trường khi Lưu và gửi, store service gán null. Đã soát ERP (model + blade) chịu được null.
- [x] C5. Từ chối ở chi tiết → về danh sách; 409/404 vẫn nạp lại chi tiết (`AssignOtherRejectModal` emit `submitted('success'|'conflict')`).
- Verify: `php -l` 6 file BE; compile 4 file FE OK; smoke API (transaction rollback, tài khoản 13): search-costs sort Người tạo asc/desc đúng; nháp chỉ có KH → 200, cột date/phòng NULL, chi tiết + danh sách 200; Lưu và gửi thiếu → 422 đủ 5 ô; `logStatusByAssignTask` ghi đúng dòng lịch sử. CHƯA mở trình duyệt, CHƯA chạy luồng tạo PGV thật end-to-end.

## Fix bug Redmine #12065 (2026-11-09) — UI
- [x] D1. Popup Chọn dịch vụ sửa chữa (`CostSearchModal.vue`): khung cố định `height: 82vh` → 10 dòng vẫn để trống nửa dưới. Bỏ chiều cao cố định, chỉ giữ `max-height: 82vh` (popup co theo nội dung như các popup chọn khác, nhiều dòng thì bảng cuộn).
- [x] D2. Ô Người liên hệ (`AssignOtherRequestForm.vue`): chip "Thêm nhanh" cao 22px căn giữa hàng nhãn → dính sát ô chọn bên dưới. Căn chip theo dòng chữ nhãn (không làm hàng nhãn cao hơn các cột bên cạnh), chừa khoảng hở với ô chọn. Làm: hàng nhãn `align-items-start` + chip `margin-top:-3px` (class `.aor-quick-add` scoped).
- Verify: compile template 2 file OK. CHƯA mở trình duyệt. `CostSearchModal` dùng chung (Lỗi thiết bị, YC thông tin BH-SC, YCGVK) → cả 3 màn cùng co popup.
- [x] D3. (10/11, tester mở lại) Popup Chọn dịch vụ sửa chữa đang căn giữa dọc màn hình → đưa lên sát trên cho đồng bộ các popup b-modal khác: `.modal-backdrop-lite` `align-items: flex-start` + lề trên `1.75rem` (= `$modal-dialog-margin-y-sm-up`). Áp cho cả các màn dùng chung `CostSearchModal`. Compile OK, CHƯA mở trình duyệt.

## Fix bug Redmine #12100 (2026-11-11) — sort popup Chọn dịch vụ sửa chữa
Tester: sort Tên dịch vụ / Người tạo "không ổn định, bấm vào bị vỡ"; Người tạo đang để sẵn giảm dần → về mặc định.
Nguyên nhân (đọc code, không phải BE — BE đã có cột phụ `costs.name, costs.id` nên thứ tự ổn định):
- Bấm sort → `V2BaseDataTable` thay 10 dòng bằng 1 dòng "Đang tải" + ẩn phân trang; từ D1 popup co theo bảng → popup sập còn ~1/4 rồi bung lại = "vỡ".
- Component popup KHÔNG huỷ khi đóng (`v-if` nằm trong template) → sort giữ nguyên qua các lần mở; "Làm mới" cũng không bỏ sort → mở lại thấy Người tạo ↓ sẵn.
- [x] E1. `CostSearchModal.vue`: khi đã có dữ liệu thì giữ nguyên các dòng cũ trong lúc tải (chỉ mờ đi, khoá bấm), chỉ hiện dòng "Đang tải" ở lần tải đầu → popup không co/giãn khi sort/chuyển trang.
- [x] E2. `CostSearchModal.vue`: mỗi lần mở popup + bấm "Làm mới" → bỏ sort (mũi tên ⇅, thứ tự mặc định Tên A→Z), về trang 1; mở popup luôn tải lại.
- Verify: compile template + parse script OK. BE không đổi. CHƯA mở trình duyệt. `CostSearchModal` dùng chung 5 màn (Lỗi thiết bị, YC thông tin BH-SC, Báo giá BH-SC, HĐ dịch vụ BH-SC, YCGVK) → cả 5 cùng nhận sửa.

### Checkpoint — 2026-11-06
Vừa hoàn thành: C1–C5 (#12049)
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt kiểm 5 điểm; deploy cần chạy migration 2026_11_06_000001
Blocked:
