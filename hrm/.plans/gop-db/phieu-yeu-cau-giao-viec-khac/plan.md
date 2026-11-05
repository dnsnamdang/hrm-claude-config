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
