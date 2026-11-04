# Plan — Biên bản bàn giao nghiệm thu (ERP → HRM) — @khoipv

Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-11-03-bien-ban-ban-giao-nghiem-thu-design.md`

## Phase 0 — Khảo sát + chốt
- [x] Đọc ERP controller / model / 2 FormRequest / form + JS class / popup searchFirmContract / getProductsSummary
- [x] Chốt với user: 2 nguồn HĐ · theo cấp y ERP · nghiệp vụ y ERP · In danh sách + In biên bản
- [x] Viết spec + design + plan

## Phase 1 — BE (`hrm-api/Modules/CustomerCare`)
- [x] T1 Entity `HandoverAcceptanceRecord` + `…Product` + `…ProductSerial` (bảng ERP dùng chung, STATUSES màu HRM)
- [x] T2 Quyền: 4 dòng `perm()` type 4 trong `PermissionsTableSeeder`
- [x] T3 `HandoverAcceptanceRecordService`: meta, filteredQuery + applyScope, presentRows, canView/canEdit/canDelete, show, delete, lịch sử
- [x] T4 `HandoverContractSourceService`: popup HĐ (hãng/HRM), contract-data điền sẵn, SL theo HĐ 2 nguồn, kiểm "chưa xuất hết hàng", bảo hành mặc định
- [x] T5 `HandoverAcceptanceRecordRequest` (validate y ERP Store/Update) + `HandoverAcceptanceRecordStoreService` (lưu, mã, files, dòng hàng, handover_date, lịch sử)
- [x] T6 `HandoverAcceptanceRecordPrintService` (in danh sách + in biên bản)
- [x] T7 Controller + route + `ExportColumnRegistry` + `CatalogHistoryService::TABLES`
- [x] T8 Verify: php -l sạch; smoke test HTTP kernel (user 13, quyền Tạo gắn tạm trong transaction, ROLLBACK): meta/list/lọc/show/print/print list/export-rows/contracts 2 nguồn/contract-data (422 HĐ đã có BB)/store 422 (SĐT, file khi duyệt, SL vượt)/store OK/trùng HĐ/edit-data/update duyệt/409 sửa+xoá sau duyệt/xoá nháp/lịch sử 3 mốc/handover_date HĐ hãng. Chưa chạy `permission:sync` thật (dry-run còn quyền của màn khác chờ).

## Phase 2 — FE (`hrm-client/pages/assign/handover-acceptance-records`)
- [x] T9 `index.vue` danh sách (3 lối vào, lọc, cột, xuất, in, lịch sử, cấu hình cột)
- [x] T10 `HandoverAcceptanceRecordForm.vue` + bảng hàng/serial + popup chọn HĐ
- [x] T11 `create.vue` / `_id/index.vue` / `_id/edit.vue`
- [x] T12 Menu: link 2 mục có sẵn (menu-sidebar.js, lookup.js)
- [x] T13 Verify: compile vue-template-compiler + babel (11 file OK); grep checklist skill erp-to-hrm-screen sạch. Popup chọn nguồn HĐ dùng V2BaseSegmented. CHƯA mở trình duyệt (user tự kiểm).

## Phase 3 — Menu CSKH sau bán (user yêu cầu 03/11/2026)
- [x] T15 Đổi: tách thành nhóm menu riêng "Hồ sơ công việc" trong CSKH sau bán (sau nhóm Giao việc, như ERP), gỡ khỏi nhóm Giao việc
- [x] T14 Thêm mục "Biên bản bàn giao nghiệm thu" vào CSKH sau bán › Giao việc (sau Phiếu nhập kết quả), link `?type=all`; giữ 2 mục cũ (Công việc, Thông báo)

## Phase 4 — Popup chọn HĐ + test Playwright (user yêu cầu 03/11/2026)
- [x] T16 Popup "Chọn hợp đồng/đơn hàng": bỏ nút gạt HĐ hãng/HRM → BE `HandoverContractSourceService::contracts()` gộp 2 nguồn bằng UNION (mặc định sắp Ngày duyệt giảm dần; HĐ HRM chưa có ngày duyệt nằm cuối), mỗi dòng mang `source` + `contractable_type`
- [x] T17 Popup dùng khuôn danh sách: `V2BaseSmartFilterPanel floating in-modal` (ô tìm "Tìm theo số hợp đồng" + Tìm kiếm / Làm mới) + `V2BaseDataTable` (sort, phân trang, nút Chọn); bỏ prop `initial-source` ở form
- [x] T18 Cột Số hợp đồng trong popup là link tab mới qua `utils/contract-link.js` (HĐ hãng → ERP, HĐ HRM → `/assign/contracts/{id}`) — y cột ở màn danh sách
- [x] T19 Fix lỗi Playwright bắt được: popup bấm sang trang 2 → STT nhảy 11–20 nhưng KHÔNG gọi API (V2BaseDataTable tự đổi `currentPage` trước khi emit) → chặn trùng trang theo `requestedPage` như màn danh sách
- [x] T20 E2E `e2e/tests/customer-care/handover-acceptance-record.spec.ts` (21 test: danh sách, popup, tạo/sửa/chi tiết/in, duyệt, xoá, menu) — PASS hết; fixture `e2e/utils/handoverFixture.ts` tạo tạm 4 quyền + trả lại `firm_contracts.handover_date` + dọn biên bản/lịch sử theo tag
  - Chạy: `cd e2e && <node 24> node_modules/@playwright/test/cli.js test tests/customer-care/handover-acceptance-record.spec.ts --headed` (API `php artisan serve` 1 luồng → mỗi test 1–3 phút)
- [x] T21 Popup chọn HĐ bỏ cột Hành động (user 04/11/2026) → bấm vào DÒNG để chọn (khuôn popup chọn phiếu xuất kho), bấm link Số HĐ chỉ mở tab xem HĐ; e2e B1 + C2 sửa theo, PASS
- [x] T22 Rà nút theo skill button-convention (user 04/11/2026): "Thêm mới" → "Tạo mới"; icon Xóa dòng danh sách → `ri-delete-bin-line`; form Lưu → primary; footer xếp Lưu → Lưu và duyệt → Lưu và tiếp tục → Quay lại (tự dựng Lưu và tiếp tục, bỏ cờ `submit_and_continue` vì V2Footer vẽ nó trước slot); chi tiết In → primary; nút bỏ dòng serial → "Xóa dòng" + `ri-delete-bin-line` + danger; e2e kiểm thứ tự nút footer, PASS

## Việc còn lại
- [ ] Còn chưa có test tự động: Xuất Excel (tải file), upload file đính kèm thật lên S3, tạo biên bản theo HĐ HRM có hàng (vướng `exported_qty` HĐ HRM chưa ghi)
- [ ] `php artisan permission:sync` thật cho 4 quyền mới (dry-run OK) + admin gán quyền
- [ ] Chờ user quyết: vá ERP để danh sách ERP đọc được biên bản gắn HĐ HRM (morph `Modules\Assign\…\Contract` không tồn tại bên ERP)

### Checkpoint — 2026-11-03 (chiều)
Vừa hoàn thành: Phase 4 — popup chọn HĐ gộp 2 nguồn + bộ lọc khuôn danh sách + link Số HĐ; fix phân trang popup; e2e 21/21 PASS
Đang làm dở: không
Bước tiếp theo: chạy permission:sync; quyết vá ERP cho biên bản HĐ HRM
Blocked:

## Fix — Danh sách BBNT ERP nổ "Trying to get property 'code' of non-object" (2026-11-04, @khoipv)
User gửi ảnh: `dev-erp.../admin/customer-care/handover_acceptance_records?type=all` → DataTables warning, bảng không tải.
- [x] Điều tra: `HandoverAcceptanceRecordsController::searchData()` (repo ERP, nhánh `gop_db`) đọc `->code` thẳng qua 3 chuỗi
      `contractable->code` / `contractable->customer->code` / `employee_create->info->department->code` — 1 bản ghi mồ côi là sập cả bảng.
      Local `gop_db` duyệt 6.824 BBNT: 0 bản null → lỗi do dữ liệu dev (chưa vào được DB dev để chỉ đúng bản ghi)
- [x] Vá cùng khuôn `a323e97c3c` (YC lắp đặt) / `af2b9ed3d6` (giao việc): `optional()` cho cột Hợp đồng, Khách hàng (rỗng nếu thiếu),
      Người tạo (thiếu phòng ban thì chỉ hiện tên). CHƯA commit
- [x] Verify: `php -l` sạch. Chưa kiểm trên dev (cần deploy)
