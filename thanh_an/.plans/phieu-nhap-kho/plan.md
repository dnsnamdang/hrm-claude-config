# Phiếu nhập kho — Plan

> Người phụ trách: @khoipv · Bắt đầu: 07/11/2026
> Design: `.plans/phieu-nhap-kho/design.md` · Spec: `docs/superpowers/specs/2026-11-07-phieu-nhap-kho-design.md`

**Goal:** Làm thật 2 màn theo demo `demo-phieu-nhap-kho.html`: (1) Phiếu giao hàng chờ nhập kho, (2) Phiếu nhập kho (danh sách + tạo / sửa / xem, lô–HSD–seri, Lưu nháp / Duyệt nhập kho / Xóa nháp, in 01-VT).

## Global Constraints
- Không commit / push git. Migration chỉ index, không khóa ngoại.
- Không sửa `components/setting/Permission.vue` (dùng chung) — quyền mới để type 7.
- FE đọc skill list-page (A), modal-popup, form-validate, select-and-input-state, button-convention (A) trước khi code; `<Required />`; ô lọc select chọn 1; `Number()` cho số từ API.
- Kiểm BE bằng script trong scratchpad, chạy trong `DB::beginTransaction()` … `rollBack()` (DB local là staging).

## Phase 0 — Thiết kế
- [x] 1. Đọc demo `demo-phieu-nhap-kho.html` (3 màn, validate dòng, phân bổ mục đích, popup seri Excel, in 01-VT, thông báo)
- [x] 2. Khảo sát code: `PurchaseDeliveryNoteService` (điểm kho, `deliverPoint`, `complete`), bảng `warehouses` / `warehouse_stockers`, `purchase_order_products.purposes`, menu `MenuWarehouse.js`, quyền type 7
- [x] 3. Chốt câu hỏi với user: sổ tồn + thẻ kho làm luôn; quyền spatie riêng; thủ kho xóa được nháp; kiểu quản lý lô/seri **chốt sau**
- [x] 4. Viết spec chi tiết + design tóm tắt

## Phase 1 — BE
- [x] 1. Migration 7 bảng + quyền 526 `Xem phiếu nhập kho` (insert nếu chưa có) + config `warehouse.default_manage_type`
- [x] 2. Entities WarehouseReceipt / Item / Lot / Serial, StockBalance / StockSerial / StockLedger; `StockManageType`
- [x] 3. `WarehouseReceiptService`: queue (list + count), prepare, list, show, save (draft/approve), validate, approve (ghi tồn + thẻ kho + seri), delete, checkSerials, thông báo
- [x] 4. Request + Resource + Controller + routes
- [x] 5. Thông báo thủ kho khi PGH hoàn thành có điểm kho (`PurchaseDeliveryNoteService::complete`)
- [x] 6. Script kiểm BE (queue, prepare, draft, approve, validate lỗi, seri trùng kho, xóa nháp, 2 người tạo cùng PGH)

## Phase 2 — FE
- [x] 0a. BE bổ sung: migration `2026_11_07_000002` thêm cột cấu hình cột `warehouse_receipts` / `warehouse_receipt_queue` vào `column_customizations` (+ cast trong `ColumnCustomization` — file dùng chung, chỉ thêm); lọc queue `note_code`, `person`; lọc PNK `code`, `invoice_no`, `created_*`, `approved_by`, `approved_*`; sort whitelist `code/import_date/created_at/approved_at`
- [x] 0b. User yêu cầu 2 màn nằm ở phân hệ Kho → đã ở `pages/warehouse` + `MenuWarehouse.js` (layout map `/warehouse`), breadcrumb "Quản lý kho"
- [x] 1. Menu `MenuWarehouse.js` nhóm Nhập kho
- [x] 2. Màn PGH chờ nhập kho `pages/warehouse/receipt_queue/index.vue`
- [x] 3. Màn danh sách PNK `pages/warehouse/receipts/index.vue` (Tạo mới → sang hàng chờ, kèm số PGH chờ)
- [x] 4. Form PNK `components/ReceiptForm.vue` dùng chung 3 trang `create.vue` (?point_id) / `_id/index.vue` (xem) / `_id/edit.vue` — Thông tin phiếu, bảng hàng 2 tầng tiêu đề, panel lô / seri / mục đích (`LinePanel`), validate realtime (`receiptRules.js`), seri trùng kho (check-serials)
- [x] 5. Popup import seri Excel (`SerialImportModal`), xác nhận Duyệt nhập kho / Xóa (BaseConfirmModal id riêng), rời trang chưa lưu (beforeRouteLeave + beforeunload)
- [x] 6. In phiếu nhập kho 01-VT (`printReceipt.js`, mở cửa sổ mới)
- [x] 7. Kiểm cú pháp: compile template (vue-template-compiler) + parse script (@babel/parser) — OK 5 file (dự án không có eslint trong node_modules)
- [x] 7b. Bỏ khung ghi chú xanh đầu màn PGH chờ nhập kho (user yêu cầu) — xóa markup + style `.rq-note` trong `receipt_queue/index.vue`
- [ ] 8. User test tay trên trình duyệt: tạo từ hàng chờ → Lưu nháp → Sửa → Duyệt → In; xóa nháp; tài khoản không phải thủ kho chỉ xem
- [x] 8b. Playwright E2E (user yêu cầu, chạy `--headed` để theo dõi): `e2e/tests/warehouse/phieu-nhap-kho.spec.js` + `e2e/pages/WarehouseReceiptPage.js`. DB stag chưa có PGH chờ nhập kho → fixture tạm: PGH-2026-0002 (point 432) set Hoàn thành + kho 1 + SL giao = SL kế hoạch, employee 13 (token e2e) làm thủ kho kho 1; afterAll xóa cứng PNK/sổ kho phát sinh + khôi phục snapshot. Luồng: hàng chờ → tạo → Lưu nháp → danh sách → xem → Xóa nháp → quay lại hàng chờ → tạo lại → Duyệt → In — **6/6 pass (07/11/2026)**, DB đã khôi phục sạch
- [x] 8c. User phàn nàn chạy `--headed` cửa sổ cứ ẩn/hiện → chạy 1 tab: `auth/auth.setup.js` ghi storageState thẳng từ ACCESS_TOKEN (kiểm token qua API, không mở trình duyệt); spec dùng chung 1 context/page cho 5 test serial; bước In thay `window.open` bằng cửa sổ giả rồi `setContent` bản in vào chính tab đó. Sửa selector: tiêu đề màn lọc `visible` (menu ẩn trùng chữ), nút footer bỏ qua ký tự icon remixicon ở đầu tên
- [x] 8d. E2E luồng PGH → chờ nhập kho chạy thật trên UI (user muốn xem): `e2e/tests/warehouse/pgh-sang-cho-nhap-kho.spec.js`. PGH-2026-0002 (Đang xử lý, phụ trách = nv 13, NCC giao về kho): trước khi hoàn thành không có ở hàng chờ → điểm 1 nhập SL thực nhận + chọn kho nhận → "Xác nhận kho đã nhận hàng" → tick "không phát sinh chi phí" → Hoàn thành giao hàng → hàng chờ có PGH "Chờ nhập kho" → mở form tạo PNK thấy đủ dòng (không lưu). afterAll khôi phục PGH/điểm/dòng hàng/chi phí/thông báo/job + gỡ thủ kho tạm — **4/4 pass (07/11/2026)**, DB đã khôi phục. Phát hiện thêm: thông báo sinh cả job `BroadcastNotificationCreated` → bổ sung điều kiện dọn job ở cả 2 spec, đã xóa 6 job broadcast còn sót của 2 lượt chạy hôm nay
## Phase 3 — PGH trạng thái "Chờ nhập kho" (user yêu cầu 07/11/2026)
> Hoàn thành giao hàng mà PGH về kho → PGH sang **Chờ nhập kho** (7) thay vì Hoàn thành; mọi điểm về kho đã có PNK **được duyệt** → PGH tự sang **Hoàn thành**. User chốt **phương án A + C** (07/11/2026): A = PGH 7 → 5 khi mọi điểm về kho có PNK được duyệt; C = từng điểm hiện trạng thái nhập kho + link PNK — làm dạng **hiển thị suy ra từ PNK** (không thêm cột trạng thái điểm).
- [x] 10a. BE entity `PurchaseDeliveryNote`: `STATUS_WAITING_RECEIPT = 7` "Chờ nhập kho" (`#0EA5E9`), hằng `DELIVERED_STATUSES = [5, 7]`
- [x] 10b. `PurchaseDeliveryNoteService::complete` → về kho (dest ≠ kh và có điểm đã nhận có kho) thì 7, còn lại 5; thông báo người gửi "đã giao xong, chờ nhập kho"; `usedByPair` tính SL đã giao cho cả 7 (không thì "Còn phải gửi" của đơn mua bị cộng lại)
- [x] 10c. `WarehouseReceiptService`: hàng chờ + `ensurePointWaiting` nhận PGH ở 5 hoặc 7; duyệt PNK xong → nếu mọi điểm về kho của PGH đã có PNK duyệt thì PGH 7 → 5 (trong cùng transaction)
- [x] 10d. Migration `Modules/Supply/Database/Migrations/2026_11_07_000003_...`: PGH 5 về kho còn điểm kho chưa có PNK duyệt → 7; down: 7 → 5
- [x] 10e. FE `pages/delivery/delivery_notes`: `constants.js` thêm trạng thái 7 (lọc + badge); chi tiết: banner "Đã hoàn thành giao hàng … — chờ thủ kho nhập kho", các điều kiện đang so `DONE` tính cả 7
- [x] 10f. Kiểm: script BE trong transaction + chạy lại 2 spec E2E (`pgh-sang-cho-nhap-kho` assert trạng thái 7, `phieu-nhap-kho` fixture set 7 + assert duyệt xong PGH về 5)
- [x] 10g. User hỏi đề xuất luồng trạng thái PGH ↔ PNK (07/11/2026) → đưa 3 phương án (A tối thiểu / B thêm "Nhập kho một phần" / C trạng thái nhập kho theo điểm) → user chọn **A + C**
- [x] 10h. (C) BE `DetailPurchaseDeliveryNoteResource`: mỗi điểm kèm `receipt` {id, code, status, status_name, status_hex, approved_at} của PNK chưa xóa; FE `PointCard.vue`: badge "Chờ nhập kho" (chưa có PNK) / "Đang nhập kho" (nháp) / "Đã nhập kho" (đã duyệt) + mã PNK là link `/warehouse/receipts/:id`
- [x] 10i. Kiểm: script BE (migration up/down, PGH giữ 7 khi chưa có PNK / PNK nháp, duyệt → 5, gọi lại không đổi, resource đúng badge, `usedByPair` 5 = 7) — PASS; E2E `pgh-sang-cho-nhap-kho` **4/4**, `phieu-nhap-kho` **6/6** (thêm test 4b: chi tiết PGH thấy "Đã nhập kho" + link PNK); DB đã khôi phục sạch
- [x] 10k. Chi tiết PGH: bỏ ô "Kho nhận" ở khối Thông tin chung (user yêu cầu) — xóa ô + computed `warehouseText` trong `pages/delivery/delivery_notes/_id/index.vue`; kho nhận vẫn hiện ở từng điểm
- [x] 10l. User hỏi: PGH-2026-0004 đang Chờ nhập kho mà `/warehouse/receipt_queue` trống → đã trace: dữ liệu PGH đủ điều kiện (status 7, điểm 500 đã nhận, kho 1, chưa có PNK); không phải lỗi code — nv 13 không phải thủ kho kho 1 (chỉ nv 15, 17) và chưa role nào có quyền 526 nên hàng chờ lọc mất. Chạy `queueCount` theo user: 13 → 0, 15 → 1, 17 → 1. Cách xử lý: gán thủ kho ở Danh mục kho hoặc cấp quyền 526 (chỉ xem)
- [ ] 10j. User chạy migration `php artisan module:migrate Supply` (000003 — trên stag hiện không đổi bản ghi nào) + test tay

- [ ] 9. Chờ user: có chuyển migration `2026_11_07_000001` từ `Modules/Warehouse/Database/Migrations/` sang `database/migrations/` (nơi các bảng kho cũ đang nằm) không

### Checkpoint — 07/11/2026
Vừa hoàn thành: spec + design + plan
Đang làm dở: —
Bước tiếp theo: Phase 1 task 1 (migration)
Blocked: kiểu quản lý lô/seri chưa chốt (tạm mặc định `none` qua env)

### Checkpoint — 07/11/2026 (FE xong)
Vừa hoàn thành: Phase 2 task 4–7 — form Phiếu nhập kho (tạo / sửa / xem), in 01-VT, kiểm cú pháp
Đang làm dở: —
Bước tiếp theo: user test tay luồng Hàng chờ → Tạo PNK → Lưu nháp → Duyệt → In; chốt vị trí migration 000001
Blocked: kiểu quản lý lô/seri của hàng hóa chưa chốt (mặc định `none` qua env `WAREHOUSE_DEFAULT_MANAGE_TYPE`)

### Checkpoint — 07/11/2026 (Phase 3 dở)
Vừa hoàn thành: 10a (hằng STATUS_WAITING_RECEIPT = 7, DELIVERED_STATUSES) + 10b (complete → 7 khi về kho, usedByPair tính cả 7)
Đang làm dở: 10c — chưa sửa `WarehouseReceiptService` (queueBase dòng ~149, ensurePointWaiting dòng ~359, save() nhánh duyệt)
Bước tiếp theo: chờ user chốt phương án trạng thái (A tối thiểu / B thêm "Nhập kho một phần" / C trạng thái điểm "Đã nhập kho") rồi làm 10c–10f
Blocked: ⚠️ hiện tại BE đang lệch — Hoàn thành giao hàng về kho ra 7 nhưng hàng chờ nhập kho vẫn chỉ lọc 5 → PGH mới hoàn thành sẽ KHÔNG vào hàng chờ cho tới khi làm 10c

### Checkpoint — 07/11/2026 (Phase 3 xong)
Vừa hoàn thành: 10c–10i — phương án A + C: Hoàn thành giao hàng về kho → PGH "Chờ nhập kho" (7); duyệt PNK của điểm kho cuối cùng → PGH tự "Hoàn thành" (5); chi tiết PGH hiện trạng thái nhập kho từng điểm + link PNK; migration 000003 cho dữ liệu cũ
Đang làm dở: —
Bước tiếp theo: user chạy `php artisan module:migrate Supply` + test tay (task 8, 10j); chốt vị trí migration 000001 (task 9)
Blocked: kiểu quản lý lô/seri của hàng hóa chưa chốt (mặc định `none`)

### Checkpoint — 07/11/2026 11:57 (wrap up)
Vừa hoàn thành: 10k bỏ ô Kho nhận ở Thông tin chung chi tiết PGH; 10l trace hàng chờ trống với PGH-2026-0004 (do tài khoản không phải thủ kho, chưa role nào có quyền 526 — không phải lỗi code)
Đang làm dở: —
Bước tiếp theo: user chọn cách thấy phiếu (đăng nhập nv 15/17, gán nv 13 làm thủ kho kho 1, hoặc cấp quyền 526) → test tay luồng tạo / duyệt PNK (task 8); chạy migration Supply 000003 (10j); chốt vị trí migration 000001 (task 9)
Blocked: kiểu quản lý lô/seri của hàng hóa chưa chốt (mặc định `none`). Ghi nhận thêm, chưa xử lý: `column_customizations` thiếu cột `delivery_notes` → log lỗi SQL lúc 11:50:15, chờ user quyết
