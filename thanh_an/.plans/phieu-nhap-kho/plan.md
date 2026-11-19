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
- [ ] 10j. (vẫn cần) User chạy migration `php artisan module:migrate Supply` (000003 — trên stag hiện không đổi bản ghi nào) + test tay

## Phase 4 — Tạm mở quyền phiếu nhập kho (user yêu cầu 09/11/2026)
> "Tạm thời bỏ qua hết quyền tạo phiếu nhập kho, để ai cũng có thể tạo". Làm bằng công tắc config để bật lại quyền dễ dàng.
- [x] 11a. Config `warehouse.receipt_open_permission` (env `WAREHOUSE_RECEIPT_OPEN_PERMISSION`, mặc định `true`)
- [x] 11b. `WarehouseReceiptService`: bật công tắc → `canViewAll()` = true (ai cũng thấy hàng chờ / mọi PNK / mọi kho trong bộ lọc), `isKeeper()` = true (ai cũng tạo / sửa / duyệt / xóa nháp); vẫn giữ: chỉ sửa / duyệt / xóa phiếu nháp
- [x] 11c. Kiểm bằng script với nv 13 (không phải thủ kho; nay đã có quyền 526 qua role 3): bật công tắc → isKeeper(1) = true, phiếu nháp is_can_edit/approve/delete = true, phiếu đã duyệt vẫn false; tắt công tắc → isKeeper(1) = false (như cũ) — PASS

## Phase 5 — Kiểu quản lý lô / HSD / seri ở màn Quản lý hàng hóa (user yêu cầu 09/11/2026)
> Gỡ blocker "chưa chốt nơi lưu kiểu quản lý": lưu theo mã hàng ở `products`, `StockManageType::forProduct()` đọc từ đây.
- [x] 12a. Hỏi user → chốt 09/11/2026: **bắt buộc, mặc định "Không quản lý"** (hàng cũ migration gán none); **khóa đổi khi mã hàng đã có PNK đã duyệt** (chỉ nháp thì vẫn đổi, nháp giữ kiểu đã snapshot); danh sách hàng hóa thêm **cột + ô lọc (chọn 1) + xuất Excel**; **chỉ hàng hóa thường** (hàng hóa mẫu / biến thể không có ô, mặc định none)
- [x] 12b. BE: migration `Modules/Category/Database/Migrations/2026_11_09_000001_add_stock_manage_type_to_products` (string(10) default `none`, **đã chạy local** — 3303 hàng = none); `ProductService` create (chỉ TYPE_PRODUCT, sai/thiếu → none) / update (`resolveStockManageType`: không gửi / hàng mẫu / đã khóa → giữ cũ) + lọc `stock_manage_type` ở `index()`; `ProductRequest` `required|in` + closure khóa đổi khi có PNK đã duyệt (422) + messages; `ProductResource` / `DetailProductResource` trả `stock_manage_type`, `stock_manage_type_name` (+ `is_stock_manage_type_locked` ở chi tiết)
- [x] 12c. BE `StockManageType`: `forProduct()` đọc `products.stock_manage_type` (cache theo request; rỗng / lạ → config), thêm `name()`, `options()`, `isLockedForProduct()` (có dòng PNK status 3 chưa xóa)
- [x] 12d. FE: hằng `utils/constants/stockManageType.js`; ô "Quản lý lô / HSD / seri" `<Required />` (Select2, sau ô HSD) ở `GeneralComponent.vue`, khóa + ghi chú khi `is_stock_manage_type_locked`; `add.vue` mặc định `none`; danh sách `index.vue`: cột (hiện mặc định, sau HSD từ ngày SX), ô lọc chọn 1, xuất Excel (id 31); `ProductHistoryModal` nhãn + hiện tên kiểu. Hàng hóa mẫu (`product_templates`) không sửa
- [x] 12e. Kiểm: script BE trong transaction (rollback) **16/16 PASS** (khóa / không khóa, forProduct, request 422, service giữ cũ, lọc, resource); compile template + parse script 4 file FE OK. Chưa test trên trình duyệt
- [x] 12f. User yêu cầu cột "Quản lý lô / HSD / seri" ở danh sách hàng hóa đặt **trước cột Trạng thái** (cả thứ tự trong popup Xuất Excel); cấu hình cột đã lưu chưa có cột này → `placeNewColumnsBeforeStatus()` trong `index.vue` chèn trước Trạng thái (không sửa `mergeSavedColumns` dùng chung, vốn nối cột mới xuống cuối). Compile OK
- [x] 12g. User báo hàng "Hóa chất kiểm chuẩn" chọn Lô + HSD + Seri mà màn Hàng chờ nhập kho hiện "Lô + Seri" → dữ liệu vẫn đúng (`loseri`), lỗi do nhãn rút gọn viết cứng `MANAGE_INFO.loseri.short = 'Lô + Seri'` ở `pages/warehouse/receipts/constants.js` (chip ở `receipt_queue/index.vue` + badge dòng ở `ReceiptForm.vue`) → đổi thành 'Lô + HSD + Seri'; `none.text` → 'Không quản lý lô / seri' cho khớp BE `StockManageType::NAMES` (nhãn chip "Thường" giữ nguyên)
- [x] 12h. User yêu cầu màn Hàng chờ nhập kho (`receipt_queue/index.vue`) cột Hàng hóa **bỏ dòng "N dòng · SL x"**, chỉ còn chip kiểu quản lý; bỏ import `fmtQty` không còn dùng. Xuất Excel vẫn giữ cột Số dòng hàng / Tổng số lượng

## Phase 6 — Rà soát chuẩn V2 / skill các màn Hàng chờ nhập kho + Phiếu nhập kho (user yêu cầu 09/11/2026)
> Đối chiếu skill `list-page` A, `button-convention` A, `modal-popup`, `form-validate`, `select-and-input-state` cho `pages/warehouse/receipt_queue/**`, `pages/warehouse/receipts/**`.
- [x] 13a. Rà grep tự kiểm (HTML thô, text-muted, —, Người lập, id confirm, v2-styles, nút thiếu icon/size, :disabled trên V2BaseButton, b-modal tự dựng…) → lập danh sách lệch. Sạch: không input/select/button thô, không text-muted, không "—", v2-styles import đúng, BaseConfirmModal đều có id riêng, popup import seri đã dùng V2BaseModal (footer Xác nhận → Đóng đúng chuẩn)
- [x] 13b. Sửa màn Hàng chờ nhập kho (`receipt_queue/index.vue`): chip loại quản lý tự dựng `.rq-chip` → `V2BaseBadge size="sm" :color`; cột Thao tác bỏ chữ "Chỉ thủ kho lập phiếu" (không dùng được thì ẩn, gốc slot vẫn là `<div>`)
- [x] 13c. Sửa màn danh sách Phiếu nhập kho (`receipts/index.vue`): `handleConfirmDelete` thêm cờ `deleting` chống bấm kép
- [x] 13d. Sửa form / chi tiết (`ReceiptForm.vue`, `LinePanel.vue`): pill trạng thái dòng `.st-chip` → `V2BaseBadge` (màu theo 9 mã chuẩn, hàm `chipColor`); "Lưu nháp" secondary → primary; "In phiếu nhập kho" → "In"; nhãn "cận date" tự dựng → `V2BaseBadge color="#F59E0B"`. Serial*.vue giữ nguyên (ô chip seri tự dựng có ghi chú, không có V2Base tương đương)
- [x] 13e. Compile check 4 file đã sửa → OK
- [x] 13f. Bảng "Hàng hóa nhập kho" (`ReceiptForm.vue`) dựng lại theo khuôn bảng hàng `supply/purchase_orders/add` (ProductsTab `.product-table`): `table-bordered`, thead dính khi cuộn dọc (V2BaseTableScroll `max-height`), tiêu đề 1 hàng nền `#eef4f3` căn giữa, đông cứng STT / Mã hàng / Tên hàng hóa khi cuộn ngang, ô nhập/select `size="xs"` cao 28px, số căn phải, ô căn giữa dọc (user yêu cầu 09/11/2026)
- [x] 14a. Tạo component bảng dùng chung `components/V2BaseFormTable.vue` theo khuôn bảng form của hrm (V2BaseTableScroll + `table table-bordered table-sm`): khai báo `columns` (type index / width / align / wrap / freeze / required / formatter), thead dính nền `#f8fafc`, đông cứng cột trái (tự tính `left`), viền `border-collapse: separate` (không mất viền khi sticky), dòng trống / đang tải xám, cao theo nội dung, row-class có sẵn `is-active` / `is-warn`, prop `dense` cho popup; slot `cell-<key>` / `head-<key>` / `row-after` / `append` / `empty` (user yêu cầu 09/11/2026). Không sửa `V2BaseTableScroll` (bản dns đã có ResizeObserver như hrm)
- [x] 14b. Chuyển bảng "Hàng hóa nhập kho" (`ReceiptForm.vue`, computed `goodsColumns`) + bảng xem lô / seri (`LinePanel.vue`, computed `viewColumns`, dòng cận date `is-warn`) sang `V2BaseFormTable`; bỏ khối CSS `.rf-table` / `.rv` tự viết
- [x] 14c. Compile check template + SCSS 3 file → OK; render thử SSR component (đông cứng `left` cộng dồn, dòng mở rộng, dòng trống) → đúng
- [x] 14d. Sửa skill: `form-validate` thêm mục 1e (prop / cột / slot / quy tắc, bảng ánh xạ 1b + grep tự kiểm có `<table`, checklist); `list-page` A8 + `modal-popup` (mục 5, bẫy 2 lớp cuộn, checklist) trỏ về `V2BaseFormTable` — bảng viết tay trong form / modal / chi tiết CHỈ dùng component này
- [x] 15. Bỏ banner "Tạo phiếu nhập kho từ PGH-… — hàng về kho ngày … / Dòng hàng và SL thực nhận lấy từ phiếu giao hàng…" ở màn tạo mới (`ReceiptForm.vue`, nhánh `isNew` không hiện banner gì) (user yêu cầu 09/11/2026)
- [~] 14e. (bỏ — đã gỡ PNK ở Phase 7) Chờ user xem trên trình duyệt `/warehouse/receipts/create?...` + màn chi tiết PNK (bảng hàng, mở panel lô / seri, cuộn ngang cột đông cứng)
- Cố ý KHÔNG đổi (báo user): bản in 01-VT giữ "Người lập phiếu" (mẫu luật định); số cột hiện mặc định > 7; validate tự viết `receiptRules.js` (không vee-validate — viết lại rủi ro cao); 422 chỉ toast, chưa map vào ô; nút "Duyệt nhập kho" giữ chữ; `b-spinner` lúc tải giữ (supply V2 cũng dùng); SerialImportModal không đổi sang V2BaseImportModal (cái đó là import bảng nhiều cột)

- [~] 9. (bỏ — đã xóa migration 000001 ở Phase 7) Chờ user: có chuyển migration `2026_11_07_000001` từ `Modules/Warehouse/Database/Migrations/` sang `database/migrations/` (nơi các bảng kho cũ đang nằm) không

## Phase 7 — Gỡ toàn bộ Phiếu nhập kho, chỉ giữ màn PGH chờ nhập kho (user yêu cầu 09/11/2026)

> Chốt với user: gỡ hết FE + BE phiếu nhập kho; **giữ** màn `/warehouse/receipt_queue`, trạng thái PGH "Chờ nhập kho" (Phase 3), `V2BaseFormTable` + skill; **gỡ** Phase 4 (công tắc mở quyền) + Phase 5 (kiểu quản lý lô / HSD / seri ở hàng hóa). Các task 8, 9, 10j, 14e không còn ý nghĩa.

- [x] 16a. BE: tách hàng chờ ra `ReceiptQueueService` + `ReceiptQueueController` (list / count / filter-options: kho, NCC, thủ kho, hình thức), bỏ điều kiện "chưa có PNK" + lọc quyền + manage_types / is_can_create
- [x] 16b. BE: xóa Entities PNK / tồn kho (7 file), `WarehouseReceiptController`, Requests, Service, Exception, `Support/StockManageType`, Transformers PNK, migration `2026_11_07_000001`; routes chỉ còn `receipt-queue`
- [x] 16c. BE: `PurchaseDeliveryNoteService` bỏ `notifyArrived`; `DetailPurchaseDeliveryNoteResource` bỏ `receipt` từng điểm; config Warehouse về như cũ; seeder bỏ quyền 526; `ColumnCustomization` + migration 000002 chỉ còn cột `warehouse_receipt_queue`
- [x] 16d. BE: revert Phase 5 ở Category (`ProductRequest`, `ProductService`, `ProductResource`, `DetailProductResource`) + xóa migration `2026_11_09_000001`
- [x] 16e. DB local: drop 7 bảng PNK / tồn kho, cột `products.stock_manage_type`, cột `column_customizations.warehouse_receipts`; xóa dòng migrations 1326, 1328; xóa quyền 526 + role_has_permissions
- [x] 16f. FE: xóa `pages/warehouse/receipts/`, `utils/constants/stockManageType.js`; menu bỏ "Phiếu nhập kho"; `receipt_queue/index.vue` bỏ nút / thao tác lập PNK, chip kiểu quản lý, đổi API filter-options; revert Phase 5 ở màn hàng hóa (4 file)
- [x] 16g. FE chi tiết PGH: `PointCard` bỏ badge / link PNK (giữ badge "Chờ nhập kho"); banner trạng thái 7 bỏ câu "tự chuyển Hoàn thành khi có PNK duyệt"
- [x] 16h. Skill `form-validate` 1e: ví dụ không trỏ tới ReceiptForm / LinePanel nữa
- [x] 16i. Kiểm: `php -l`, compile FE, grep sót `WarehouseReceipt` / `StockManageType` / `stock_manage_type` / `/warehouse/receipts`; gọi thử API hàng chờ
- [x] 16j. E2E `dns/e2e`: xóa `tests/warehouse/phieu-nhap-kho.spec.js` + `pages/WarehouseReceiptPage.js`; thay bằng `pages/ReceiptQueuePage.js` (chỉ hàng chờ); `pgh-sang-cho-nhap-kho.spec.js` bỏ kiểm bảng `warehouse_receipts` + bước mở form PNK (test 4 chỉ còn kiểm dòng ở hàng chờ). Chưa chạy (chỉ chạy khi user bảo)
- [x] 16k. Ghi chú kết quả: hàng chờ không còn lọc "chưa có PNK" / theo quyền → mọi điểm về kho đã nhận của PGH 5 / 7 đều hiện; PGH ở "Chờ nhập kho" (7) không tự sang Hoàn thành nữa (chưa có nghiệp vụ nhập kho). Màn hàng chờ bỏ cột "Hàng hóa" (chỉ còn chip kiểu quản lý → trống) + cột Hành động; Excel vẫn có Số dòng hàng / Tổng số lượng. Badge "Chờ nhập kho" ở thẻ điểm chỉ hiện khi PGH đúng trạng thái 7. Migration Supply 000003 bỏ nhánh kiểm `warehouse_receipts`. `V2BaseFormTable` giữ lại (hiện chưa màn nào dùng)
- [x] 16l. User yêu cầu bỏ ô "Quản lý lô / HSD / seri" ở màn hàng hóa → đã kiểm: 4 file FE + 4 file BE Category không còn diff (đã revert ở 16d / 16f), cột `products.stock_manage_type` đã drop, cấu hình cột `column_customizations.products` không có cột này; sót 1 dòng `product_history` id 166 (hàng 145, nv 13 sửa 09/11 10:00) → `JSON_REMOVE` khóa `stock_manage_type` ở old/new_value (giữ các thay đổi thật khác). Các trường HSD từ ngày SX / HSD từ ngày mở là trường có sẵn từ trước, KHÔNG thuộc Phase 5 → giữ nguyên
- [x] 16m. User yêu cầu bỏ banner "Đã giao xong lúc … — chờ thủ kho nhập kho." ở chi tiết PGH trạng thái 7 (`pages/delivery/delivery_notes/_id/index.vue`)

## Phase 8 — Đồng nhất style bảng theo hrm (mẫu MISA) (user yêu cầu 09/11/2026)

> Nguyên nhân lệch: `V2BaseDataTable` dns port từ bản hrm trước 15/10/2026 (header xám, sọc xen kẽ, kẻ liền #e5e7eb); hrm đã đổi sang bộ màu MISA (`assets/scss/_misa-grid.scss`). Các bảng form / popup ở Cung ứng, Giao hàng tự đặt màu riêng trong style scoped. User đồng ý sửa component dùng chung.
> Bộ màu MISA: header nền #d8e7e1, chữ #10141b đậm, gạch dưới #7cc7ae; kẻ #ced1d6; nền dòng #fbfbfc (không sọc); hover cả dòng #e6f5ef; dòng tick #ddf1e9.

- [x] 17a. Tạo `assets/scss/_misa-grid.scss` (chỉ biến, copy hrm)
- [x] 17b. Port `V2BaseDataTable` theo hrm: style MISA + `hideHeader`, `cellSpan`, `column.tip` (port `components/report/ReportInfoTip.vue`), `itemLabel` rỗng, `dt-state-row`
- [x] 17c. `V2BaseFormTable` đổi sang bộ màu MISA
- [x] 17d. Bảng form / popup Cung ứng: purchase_orders, purchase_contracts (ProductsTab, PaymentTab, GoodsPickerModal, các modal `dd-table`), supply_proposals (GoodsTable, GoodsPickerModal, FileTable, ContractRefTab, ProductInfoTab, ViewHistoryModal), supply_handlings (HandlingGoodsTable, `sum-tbl`), contract_render modal, báo cáo purchase-demand
- [x] 17e. Bảng Giao hàng: `dn-table` (chi tiết PGH, PointCard, PickupBlock, CostTable)
- [x] 17f. Kiểm compile FE các file đã sửa — compile_check + scss_check2 (scratchpad, có nạp _misa-grid) OK 21 file + v2-detail-modal.scss
- [x] 17g. Ghi chú kết quả: `.dd-table` (6 popup chi tiết) sửa ở file chung `assets/scss/v2-detail-modal.scss` (chỉ khối bảng); `.dn-table` chỉ định nghĩa ở `delivery_notes/_id/index.vue` (PointCard / PickupBlock / CostTable ăn theo); `.sum-tbl` khai trùng ở 3 file supply_handlings. HandlingGoodsTable đổi style sang scss (`>>>` → `::v-deep`, `min()` bọc `unquote`) + bỏ tô nền xen kẽ theo khối (`blk-even`). GIỮ màu ngữ nghĩa: warning-row, swap-row, row-over, is-short, header tím 4 cột tham chiếu HĐ bán (`th.cell-ref-h`), cột mới `th.col-new`, gạch chân màu theo nhóm cột. Dòng tổng / foot-row → nền header MISA. Skill `form-validate` (1e), `list-page` (mục A8b mới: bảng biến + prop mới của V2BaseDataTable), `modal-popup` (mục 5) thêm quy định màu MISA. Chưa sửa: bảng b-table màn Kho / Kho kế toán (màn cũ), bảng in PrintTab, bảng module Hợp đồng (acceptance_report)

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

### Checkpoint — 09/11/2026
Vừa hoàn thành: Phase 4 — tạm mở quyền phiếu nhập kho bằng config `warehouse.receipt_open_permission` (env `WAREHOUSE_RECEIPT_OPEN_PERMISSION`, mặc định true) trong `Modules/Warehouse/Config/config.php`; `WarehouseReceiptService::isOpenPermission()` → `canViewAll()` / `isKeeper()` / `filterOptions.is_keeper` luôn true. FE không sửa (đọc cờ BE).
Đang làm dở: —
Bước tiếp theo: user test tay tạo / duyệt PNK bằng tài khoản bất kỳ; khi cần bật lại quyền → đặt `WAREHOUSE_RECEIPT_OPEN_PERMISSION=false` trong .env
Blocked: kiểu quản lý lô/seri chưa chốt (mặc định `none`)

### Checkpoint — 09/11/2026 (Phase 5)
Vừa hoàn thành: Phase 5 — kiểu quản lý lô / HSD / seri chọn ở màn Quản lý hàng hóa (form + cột + lọc + Excel), PNK đọc theo mã hàng; migration Category 2026_11_09_000001 đã chạy local
Đang làm dở: —
Bước tiếp theo: user test tay: sửa 1 hàng hóa sang "Lô + HSD" → lập PNK từ hàng chờ thấy panel lô / HSD; duyệt PNK → mở lại hàng hóa thấy ô bị khóa; lọc / xuất Excel danh sách
Blocked: —

### Checkpoint — 09/11/2026 (Phase 7 — gỡ PNK)
Vừa hoàn thành: 16a–16k — gỡ toàn bộ Phiếu nhập kho (FE + BE + DB local) và Phase 4, 5; màn `/warehouse/receipt_queue` chạy bằng `ReceiptQueueService` / `ReceiptQueueController` (`receipt-queue`, `/count`, `/filter-options`) — tinker: count = 1 (PGH-2026-0004), filter-options đủ 4 nhóm
Đang làm dở: —
Bước tiếp theo: user mở `/warehouse/receipt_queue` + chi tiết PGH-2026-0004 kiểm tra; chạy `php artisan module:migrate Supply` (000003) trên môi trường khác
Blocked: —

### Hỏi đáp — 09/11/2026: PGH Hoàn thành khi nào?
- [x] 17a Trace `PurchaseDeliveryNoteService::complete()` + `missingForComplete()`: chỉ duy nhất `complete()` gán `STATUS_DONE`, và chỉ khi phiếu KHÔNG về kho (giao thẳng KH / không có điểm đã giao nào gắn kho). Phiếu về kho → `STATUS_WAITING_RECEIPT` (7).
- [x] 17b Sau Phase 7 (gỡ PNK) không còn code nào chuyển 7 → 5 (luồng "duyệt đủ PNK → tự Hoàn thành" đã gỡ cùng PNK) → phiếu về kho hiện đứng mãi ở Chờ nhập kho.
- [ ] 17c (Chờ user) Có cần cơ chế chuyển Chờ nhập kho → Hoàn thành không (vd nút "Xác nhận đã nhập kho" ở màn hàng chờ)?

### Checkpoint — 09/11/2026 (wrap up)
Vừa hoàn thành: 17a–17b — trả lời "PGH Hoàn thành khi nào": chỉ `complete()` gán Hoàn thành khi phiếu không về kho; phiếu về kho → Chờ nhập kho và sau khi gỡ PNK không còn đường chuyển sang Hoàn thành
Đang làm dở: —
Bước tiếp theo: user chốt 17c (có thêm cơ chế Chờ nhập kho → Hoàn thành, vd nút "Xác nhận đã nhập kho" ở màn hàng chờ, hay giữ nguyên); chạy `php artisan module:migrate Supply` (000003) trên môi trường khác
Blocked: chờ quyết định 17c
