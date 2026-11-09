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

## Fix #12011 — Danh sách BBNT: 7 góp ý QA (2026-11-05, @khoipv)
Redmine http://quanly.dnsmedia.vn/issues/12011
- [x] 1. Nút "Thêm mới" → "Tạo mới" (đã đúng từ T22 — kiểm lại)
- [x] 2. Đồng bộ icon Tùy chỉnh cột: `V2BaseIconButton` → `V2BaseButton secondary size="sm" btn-icon` (skill list-page)
- [x] 3. Bỏ sort cột Trạng thái, thêm sort cột Số hợp đồng (FE + `SORTABLE_COLUMNS`)
- [x] 4. NVKD / NV kỹ thuật / Người tạo dạng "Tên - Mã phòng" (`employeeAuditLabel`, nạp theo lô) — danh sách, in, xuất
- [x] 5. Thêm cột Ngày cập nhật + Người cập nhật (danh sách, sort Ngày cập nhật, in, xuất `ExportColumnRegistry`)
- [x] 6. Ngày BGNT có giờ — user chốt đổi cột `handover_acceptance_records.date` DATE → DATETIME (migration); form chọn ngày giờ; validate `Y-m-d H:i` (nhận cả `Y-m-d`), không lớn hơn hôm nay; serial `handover_date` vẫn lấy phần ngày
- [x] 7. In danh sách: giãn khoảng "Người lập" ↔ tên (khuôn `signature-space` 15px, #11918)
- [x] ERP (repo `erp`, nhánh `develop_02` con của gop_db): lọc Ngày BGNT `where('date', …)` → `whereDate` (`app/Model/Customers/HandoverAcceptanceRecord.php`) — cột thành DATETIME thì so bằng sẽ lọt biên bản có giờ. CHƯA commit
- [x] Verify: migration chạy local (cột = datetime); php -l sạch; smoke HTTP kernel (Super admin): list 200, sort `contract_code` asc đúng, Ngày BGNT `dd/mm/yyyy HH:mm`, 4 cột người dạng "Tên - Mã phòng", có Ngày/Người cập nhật; in danh sách có 2 cột mới + `signature-space`; rule `before:tomorrow` (hôm nay 23:59 qua, mai 00:00 trượt); compile 3 file FE OK. CHƯA test lưu form thật trên trình duyệt

### Checkpoint — 2026-11-05
Vừa hoàn thành: Fix #12011 (7 mục) BE + FE + vá lọc ERP
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt kiểm form tạo/sửa (ô ngày giờ) + danh sách + in; deploy nhớ chạy migration `2026_11_05_000002`
Blocked:

## Fix #12018 — Tạo mới: popup Chọn hợp đồng + lỗi "không có quyền" (2026-11-05, @khoipv)
Redmine http://quanly.dnsmedia.vn/issues/12018
- [x] 1. "ERP 3182 HĐ, HRM 2994" — điều tra: KHÔNG do phân quyền (cả 2 cùng lọc công ty người tạo). ERP `SearchController::searchFirmContract` hiện cả HĐ ĐÃ có biên bản (chọn vào mới báo lỗi); HRM loại sẵn (phụ đề popup đã ghi). Local cty 1: 2884 HĐ, 196 đã có BB. User chốt: GIỮ loại sẵn, trả lời QA
- [x] 2. Popup rộng hơn, không đè menu trái — `dialog-class="hcp-dialog"`, lúc mở đo mép trái `.content-page` ghi biến `--hcp-sidebar-right` trên body (≥ 992px), đóng thì gỡ
- [x] 3. Sort cột Loại hợp đồng — UNION thêm cột `contract_type_text` (CASE nhãn HĐ hãng / "Hợp đồng HRM"), sort theo nhãn
- [x] 4. Ngày duyệt có giờ (`d/m/Y H:i`)
- [x] 5. Upload/Lưu báo "không có quyền": `viewer()['perm_create']` cho Super admin bỏ qua quyền → nút Tạo mới hiện, nhưng middleware `checkPermission` chỉ nhận quyền tick thật. User chốt: cờ Tạo theo quyền thật (bỏ đặc cách Super admin), admin tick quyền ở Phân quyền
  - `perm_create` đọc quyền đúng cách middleware đọc (`getAllPermissions`, chung cache `perm_all_by_emp:`); `is_can_edit` / `is_can_delete` thêm điều kiện quyền Tạo (route PUT/DELETE cũng gắn middleware đó — chỉ ẩn nút vốn đã bị chặn, không đổi điều kiện nghiệp vụ)
- [x] Verify: php -l sạch; compile popup OK; smoke HTTP kernel: sort Loại HĐ asc/desc 200, ngày duyệt `d/m/Y H:i`; Super admin id 34 CHƯA tick quyền → meta `can_create=false`, edit/delete 0, upload 403 (khớp); id 13 có quyền → `can_create=true`. CHƯA mở trình duyệt xem độ rộng popup

### Checkpoint — 2026-11-05 (2)
Vừa hoàn thành: Fix #12018 (mục 2–5; mục 1 trả lời QA)
Đang làm dở: không
Bước tiếp theo: user xem popup trên trình duyệt; trên dev admin tick quyền "Tạo biên bản bàn giao nghiệm thu" cho vai trò (và chạy permission:sync nếu dev chưa có quyền)
Blocked:

## Bỏ tiêu đề "Bộ lọc danh sách" ở bộ lọc trong MỌI popup (user yêu cầu 05/11/2026, @khoipv)
- [x] `components/V2BaseSmartFilterPanel.vue` (hàm chung — user yêu cầu áp toàn bộ popup): `hideTitle` = `in-modal` HOẶC panel nằm trong `.modal` (đo lúc mount — 3 popup Task trễ quên `in-modal` vẫn ăn). Ẩn icon + tiêu đề (+ `title-suffix`); header không còn nút (bộ lọc ≤ 3 ô, không slot) thì bỏ cả dòng; còn nút thì dồn phải. Màn danh sách thường không đổi
- [x] Rà: 18 popup dùng panel; tiêu đề riêng đang có ("Bộ lọc nhân sự", "Bộ lọc lịch sử meeting", "Bộ lọc lịch sử phân ca", "Bộ lọc công nợ theo khách hàng", `Bộ lọc <tên popup>` ở my-job) đều ẩn theo
- [x] Verify: compile OK. CHƯA mở trình duyệt

## Fix #12021 — Tạo mới: nút Lưu nháp, trạng thái Đang tạo, câu lỗi SL nghiệm thu (2026-11-05, @khoipv)
Redmine http://quanly.dnsmedia.vn/issues/12021
- [x] 1. Nút "Lưu" → "Lưu nháp" (form Tạo / Sửa)
- [x] 2. Nhãn trạng thái 1 "Đang cập nhật" → "Đang tạo" (đồng bộ BB bàn giao sơ bộ, YC xử lý BH…) — chỉ đổi nhãn HRM `STATUSES`; ERP giữ nhãn ERP; log lịch sử cũ giữ chữ cũ
- [x] 3. Câu lỗi ô "Số lượng đã nghiệm thu" thay "Không hợp lệ" bằng câu nói rõ số so sánh — FE `validateForm` + BE `withValidator` cùng câu
- [x] Sửa e2e `handover-acceptance-record.spec.ts` theo nhãn / nút mới
  - Câu mới: vượt SL → "Số lượng đã nghiệm thu không được lớn hơn số lượng đã xuất (X)" (có SL đã trả → "…tổng số lượng đã xuất và đã trả (X)"); hàng bắt buộc seri → "Hàng bắt buộc nhập seri: số dòng seri (n) phải bằng số lượng đã nghiệm thu (q)"; Lưu và duyệt → "Lưu và duyệt: số lượng đã nghiệm thu phải bằng số lượng đã xuất (X)"
- [x] Verify: php -l sạch; compile 2 file FE OK; tinker: STATUSES = Đang tạo / Chờ duyệt / Đã duyệt, 2 nhánh câu vượt SL đúng số. CHƯA chạy lại e2e, CHƯA mở trình duyệt

### Phản hồi #12021 (QA 06/11/2026, @khoipv)
- [x] Sai màu nút Lưu nháp: `primary` → `secondary` (skill button-convention §1/§5) — `HandoverAcceptanceRecordForm.vue`
- [x] Thu gọn câu lỗi ô SL nghiệm thu (tiêu đề cột đã nói tên trường) — FE `handoverBuild.js` + BE `HandoverAcceptanceRecordRequest` cùng câu: "Không được lớn hơn số lượng đã xuất (X)" / "Không được lớn hơn tổng số lượng đã xuất và đã trả (X)" / "Phải bằng số dòng seri (n)" / "Phải bằng số lượng đã xuất (X)"
- [x] Căn đều: ô `text-right` làm câu lỗi căn phải lởm chởm → `V2BaseError class="text-left"` — `HandoverProductTable.vue`
- [x] Verify: php -l sạch; compile 2 file .vue + parse js OK. CHƯA mở trình duyệt

## Fix #12023 — Lịch sử: dòng duyệt mang nhãn "Duyệt" thay vì "Thay đổi trạng thái" (2026-11-05, @khoipv)
Redmine http://quanly.dnsmedia.vn/issues/12023
- [x] Nguyên nhân: `HandoverAcceptanceRecordService::logStatus()` rẽ action `approved` khi sang Đã duyệt (nhãn "Duyệt"); các màn khác dùng bộ nhãn chuẩn `change_status` (skill entity-history §0, §3a)
- [x] Sửa: luôn ghi `change_status`. Log cũ (action `approved`) giữ nguyên, không sửa dữ liệu

## Fix #12060 — Popup Chọn hợp đồng: không hiện HĐ chưa xuất hết hàng (2026-11-06, @khoipv)
Redmine http://quanly.dnsmedia.vn/issues/12060
- [x] Triệu chứng: nhập đủ thông tin, bấm Lưu mới báo "Hợp đồng chưa xuất hết hàng" dưới ô Hợp đồng → chọn được HĐ mà không bao giờ lưu được
- [x] Sửa BE `HandoverContractSourceService::contracts()` + hàm mới `whereFullyExported()`: loại HĐ còn dòng `quantity > exported + returned` (SQL y hệt `pendingProductIds()` — HĐ gốc + PL bổ sung 2/5/9; HĐ HRM theo `qty_needed`)
- [x] FE `HandoverContractPickerModal.vue`: phụ đề + câu rỗng thêm "đã xuất hết hàng"
- [x] Verify: php -l sạch; tinker cty 1: trước 2688 HĐ hãng (1184 còn hàng chưa xuất) + 11 HĐ HRM → sau 1515, khớp đúng số HĐ `pendingProductIds()` rỗng; quét toàn bộ 1515 dòng popup: 0 HĐ còn hàng chưa xuất. HĐ trong ảnh QA (HD_TPE_HN_KD3_26_0818_1510) chỉ có trên dev. CHƯA mở trình duyệt
  - Lưu ý: HĐ HRM có hàng sẽ biến khỏi popup tới khi luồng xuất kho ghi `exported_qty` (trước đó chọn được nhưng cũng không lưu được)

## Fix #12083 — Form Tạo mới: 6 góp ý QA (2026-11-09, @khoipv)
Redmine http://quanly.dnsmedia.vn/issues/12083
- [x] 1. "Lưu nháp" / "Lưu và tiếp tục" chỉ BẮT BUỘC hợp đồng (bỏ bắt buộc SĐT người nhận, Ngày bàn giao, NV kỹ thuật, ngày bàn giao dòng chi tiết, seri / ghi chú theo luật nhóm). Ô có nhập vẫn kiểm định dạng. "Lưu và duyệt" giữ đủ luật — FE `validateForm` + BE `HandoverAcceptanceRecordRequest`
- [x] 2. Nút × xoá nhanh ở ô Người nhận bàn giao + SĐT người nhận khi ô có ký tự (dựng tại form qua slot `suffix`, không sửa `V2BaseInput` dùng chung)
- [x] 3. Đổi chỗ: SĐT người nhận lên vị trí NV kỹ thuật (cạnh NVKD / Phòng ban — cùng lấy từ HĐ)
- [x] 4. SL đã nghiệm thu: gõ chữ bị lọc nhưng vẫn tự thêm dòng chi tiết → bỏ qua khi giá trị không đổi; SL = 0/rỗng không thêm dòng
- [x] 5. Popup Chọn hợp đồng: thêm ô lọc Loại hợp đồng (3 loại HĐ hãng + Hợp đồng HRM) — FE filterFields + BE `contracts()` param `contract_type`
- [x] 6. SĐT người nhận: luật giống SĐT khách hàng `/^(0)[0-9]{9,11}$/`, câu "Số điện thoại không đúng định dạng" — FE + BE
- [x] Verify: php -l sạch; tinker validator — nháp chỉ HĐ: OK · thiếu HĐ: "Bắt buộc phải chọn 1 hợp đồng" · SĐT `12345`: "Số điện thoại không đúng định dạng" · duyệt thiếu: đủ 4 lỗi (SĐT, NVKT, ngày, file); lưu nháp chỉ HĐ qua StoreService (transaction rollback, không để lại dữ liệu) → `technical_staff_id=0`, phone '', date NULL, không nổ NOT NULL; lọc popup cty 1: tất cả 1515 = 1246 (bán hàng) + 162 (dự án) + 96 (ĐHNT) + 11 (HRM), giá trị lạ → không lọc; compile 3 file .vue + parse js OK; e2e C1 (trống → "Bạn chưa nhập đầy đủ thông tin.") vẫn đúng vì thiếu HĐ. CHƯA mở trình duyệt
  - Lưu ý: biên bản nháp không có NV kỹ thuật lưu `technical_staff_id = 0` (cột NOT NULL, bảng chung ERP) — ERP mở chi tiết biên bản nháp đó cần kiểm lại

### Checkpoint — 2026-11-09
Vừa hoàn thành: Fix #12083 (6 mục) BE + FE
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt kiểm form Tạo (vị trí ô, nút ×, gõ chữ vào SL nghiệm thu, lọc Loại HĐ trong popup)
Blocked:

## Fix #12084 — Chi tiết: nút Xóa đổi màu + placeholder ô lấy từ HĐ (2026-11-09, @khoipv)
Redmine http://quanly.dnsmedia.vn/issues/12084
- [x] 1. Bấm Xóa → bấm ra ngoài popup xác nhận → nút Xóa đổi màu. Nguyên nhân: `confirmDelete()` bật `submitting = true` TRƯỚC `$confirm`; plugin dùng chung `plugins/confirm-dialog.js` chỉ resolve khi bấm nút / × trong popup — đóng bằng backdrop / ESC thì Promise treo mãi → `submitting` kẹt true → nút `:interactable=false` ra màu disabled (danh sách cũng dính: lần Xóa sau bị `return` im lặng)
  - Sửa trong màn: `deleteRecord(vm, id, { onConfirmed })` — chỉ khoá nút SAU khi user bấm "Xóa" xác nhận; áp cả form chi tiết lẫn `index.vue`
  - CHƯA sửa gốc ở plugin dùng chung (248 chỗ gọi `$confirm`) — chờ user đồng ý: resolve `false` khi modal `hidden` (backdrop / ESC)
- [x] 2. Placeholder "Tự điền theo hợp đồng" (khuôn `ProductPrepickRequestForm.vue`) cho 6 ô khoá: Khách hàng, CMT/MST, Số điện thoại, Địa chỉ, NV kinh doanh, Phòng ban — chỉ Tạo/Sửa, Chi tiết để trống
- [x] Verify: compile form + index.vue, parse handoverActions.js OK. CHƯA mở trình duyệt

### Checkpoint — 2026-11-09 (2)
Vừa hoàn thành: Fix #12084 (2 mục)
Đang làm dở: không
Bước tiếp theo: user quyết có sửa gốc `plugins/confirm-dialog.js` (đóng ngoài popup → trả false) không; mở trình duyệt kiểm
Blocked:
