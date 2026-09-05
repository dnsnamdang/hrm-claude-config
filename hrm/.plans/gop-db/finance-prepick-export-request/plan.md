# Kế hoạch — Port cặp màn "Yêu cầu xuất giữ" + "Phiếu xuất giữ"

Thiết kế + 15 lỗi ERP + 7 quyết định đã chốt: [design.md](design.md) · Spec chi tiết:
[docs/superpowers/specs/gop-db/2026-09-03-finance-prepick-export-request-design.md](../../../docs/superpowers/specs/gop-db/2026-09-03-finance-prepick-export-request-design.md)
Nhánh dự kiến: `feat/finance-prepick-export-request` (cả 2 repo, tách từ `origin/gop_db`).
Người làm: @junfoke. Thứ tự: làm **sau** màn Điều chuyển hàng giữ.

> ⚠️ **Hai màn phải đi cùng nhau.** PXG duyệt là nơi DUY NHẤT sinh lô `prepick_details`. Làm xong
> PYCXG mà chưa có PXG thì phiếu duyệt xong không đi đâu được — không được coi là mốc bàn giao.

---

## Phase 0 — Khảo sát ERP ✅ (2026-09-03)

- [x] Đọc nguồn ERP: 2 controller (759 + 493 dòng), 2 model (925 + 445 dòng), 16 blade, 2 lớp Excel
- [x] Tra vị trí menu ERP (`topmenubar.blade.php`): PYCXG ở 3 nhóm, PXG chỉ ở nhóm Kế toán
- [x] Ghi 15 lỗi ERP sẽ vá → `design.md` mục 2
- [x] Đếm dữ liệu `gop_db`: `product_prepick_requests` 2.174 · details 26.185 ·
      `warehouse_prepick_requests` 2.062 · details 10.692
- [x] Đếm theo loại: chỉ có loại 5 (501) và 99 (1.673); bảng nguồn `contracts` 1 dòng,
      `project_contracts` 0 dòng, `wr_service_contracts` 6.676, `firm_contracts` 23.277
- [x] User chốt 7 quyết định (design.md mục 4)

## Phase 1 — Chuẩn bị nhánh + dữ liệu ✅ (2026-09-03, còn 1 việc chờ dev)

- [x] Tách nhánh `feat/finance-prepick-export-request` từ `gop_db` ở **cả 2 repo**
      (api `aad4573f2`, client `8021fa3d7`)
- [x] Sao lưu 6 bảng `bak_*_20260903`: `prepick_details` 53.832 · `prepick_logs` 110.744 ·
      `product_prepick_requests` 2.174 · `product_prepick_request_details` 26.185 ·
      `warehouse_prepick_requests` 2.062 · `warehouse_prepick_request_details` 10.692
- [ ] ⛔ **Xin dump phiếu loại 1–4 từ dev** — chặn phần nghiệm thu, không chặn code.
      ⚠️ Đã kiểm **4 bản dump ERP có sẵn trên máy** (`gop_db`, `erp_dev_30_01_26`, `erp_dev_24_09`,
      `new_erp_1_8`): **bản nào cũng CHỈ có loại 5 và 99**. Nhiều khả năng dev cũng không có →
      hỏi trước khi mất công xin dump (xem "Ghi chú dữ liệu" cuối file)

## Phase 2 — Hàm dùng chung ✅ (2026-09-03)

- [x] `AccountingStockService::detail()` — **thêm** field `in_promotion` (kho khuyến mại của công ty
      theo `companies.promo_warehouse_ids`, trừ pending phiếu `type = 15` Xuất KM HĐ hãng).
      Khối trừ pending đổi từ `sum()` sang vòng lặp để đọc được `r.type`
- [x] **Test lại**: 40 hàng hoá công ty 4 — `in_warehouse` **lệch 0/40** so với công thức cũ;
      `inStockOfProducts()` của màn Gia hạn trả đúng số cũ (13 / 83 / 1);
      `ProductTransferRequestService` khởi tạo OK. `in_promotion` chạy đúng trên hàng nằm ở kho
      khuyến mại (SP 4138 = 1 · 6237 = 3 · 4383 = 1)
- [x] Tách `PrepickApprovalRouteService` — gom công thức ngưỡng % đã thu (`account_id = 22`,
      `prepick_contract_types`, `prepick_other_value`), chặn chia 0 (lỗi ERP #15).
      2 lối vào: `needBoardApproveByLines()` (hợp đồng theo dòng — Gia hạn, Điều chuyển) và
      `needBoardApproveByContract()` (hợp đồng đầu phiếu — YCXG)
- [x] Sửa 2 màn cũ gọi lại service mới; xoá 4 hàm private trùng lặp ở mỗi màn.
      **Đối chiếu 300 phiếu thật: lệch 0** (Gia hạn 150 phiếu — 98 phải qua BGĐ; Điều chuyển
      150 phiếu — 79 phải qua BGĐ)
- [x] `PrepickStockService::addLot()` — hàm dùng chung MỚI. Test trong transaction rồi rollback:
      cộng vào lô cũ không đẻ dòng mới · lô mới ghi đúng
      `objectable_type = WarehousePrepickRequest` (log ghi `...RequestDetail`, đúng 2 chuỗi khác
      nhau của ERP) · `qty <= 0` không làm gì · DB hoàn nguyên **lệch 0 dòng, lệch 0 số lượng**

## Phase 3 — Entities + migration ✅ (2026-09-03)

- [x] `Entities/PrepickExport/ProductPrepickRequest.php` (793 dòng) — 6 trạng thái + màu chuẩn SRS
      (vá lỗi #14: ERP tô ĐỎ 4/6 trạng thái), 6 `TYPES` kèm `contract_type` + cờ `selectable`,
      `searchByFilter` + `applyAllScope` / `applyViewScope` / `orWhereApprovable` / `applyFilters` /
      `applySort`, các cờ `canEdit/canView/canApprove/canManagerApprove/canBoardOfManagerApprove/
      canReject`, `generateCode()` vá lỗi #4
- [x] `ProductPrepickRequestDetail.php` — cảnh báo `price`/`total_amount` là **varchar(16)** bên ERP
      (đọc qua `priceValue()` / `totalAmountValue()`, đừng cộng chuỗi)
- [x] `WarehousePrepickRequest.php` (485 dòng) — vá lỗi #2 (`=` → `==`, bỏ hẳn nhánh BKS) và
      **vá lỗi phạm vi**: ERP bọc nhánh `all` bằng `can("Trưởng phòng kế toán")` nên ai không có
      đúng quyền đó chỉ thấy phiếu mình lập dù đã có quyền xem theo cấp
- [x] `WarehousePrepickRequestDetail.php` — ghi rõ **bẫy lỗi #8** (`need_export` so chuỗi) ngay
      docblock; cast `need_export` về bool
- [x] 2 entity lịch sử + migration `2026_09_03_000001_create_prepick_export_request_history_tables`
      (`product_prepick_request_history` 8 action, `warehouse_prepick_request_history` 4 action).
      **Đã chạy migrate trên local**
- [x] Đối chiếu dữ liệu thật: 4 bảng đếm khớp DB (2.174 / 26.185 / 2.062 / 10.692); quan hệ
      cha–con, `statusMeta`, `typeMeta`, `attachmentList`, lọc theo Số HĐ và Tên/mã hàng đều chạy
- [x] **Kiểm phạm vi quyền — không rò rỉ**: nhân viên không quyền chỉ thấy phiếu mình lập
      (6 người: 194/116/96/87/80/80 phiếu = đúng số phiếu tự lập); người có "Xem theo phòng ban"
      (emp 24, phòng 42) thấy **251** phiếu = đúng `department_id = 42 AND status ≠ 3`

> ⚠️ **Bẫy đã dính khi kiểm**: trên `gop_db`, quyền ERP có id = **100000 + id ERP**
> (`Quản lý giữ hàng` = 100427, `Kế toán duyệt hàng giữ` = 100838…) và `guard = web`; id 427/836-841
> trong bảng `permissions` là quyền **HRM** hoàn toàn khác nghĩa. Entity tra theo **TÊN** nên đúng,
> nhưng khi viết SQL kiểm tay thì đừng dùng id ERP.

## Phase 4 — Service PYCXG ✅ (2026-09-03)

- [x] `PrepickExportContractService` — **service dùng chung MỚI**: gom 5 nhánh `if ($type == ...)`
      mà ERP lặp ở 4 chỗ (`getDataForEdit`, `getDataForShow`, `validateProducts`, `store`).
      Cấu hình bảng nguồn theo loại + `contractLines()` + `customerSnapshot()` +
      `remainingQuantities()` + `searchContracts()`
- [x] `ProductPrepickRequestService`: `searchByFilter` · `meta` · `findForShow` · `detailData` +
      `approvalRows` · `dataToCreate` · `inStockOfProducts` · `store`/`update` · `normalizeLines` +
      `syncProducts` · `approve` (TP/BGĐ) · `reject` · `destroy` · `needBoardApprove` ·
      `maxExpireDate`/`parseExpireDate`
- [x] Vá lỗi #4 (sinh mã 1 lần), #5 (bitwise `|`), #6 (reset đủ 3 cấp duyệt), #7
      (`max_prepick_date_project_contract` cho cả update), #8 (ép bool `need_export`)
- [x] `ProductPrepickRequestHistoryService` — 8 action, khoá bảng con `product_id:unit_id`,
      chỉ chụp dòng `need_export = 1`
- [x] **Đối chiếu dữ liệu thật**: `contractLines()` của HĐ hãng `HĐ_TPSG_KV3_26_0432_2507-GSMTG`
      trả **39 dòng — khớp đúng 39 dòng** trên phiếu `PYCXG-02212` mà ERP đã lập
- [x] **Test ghi (transaction + rollback)**: store nháp → update gửi duyệt → TP duyệt (rẽ BGĐ) →
      BGĐ duyệt (nhập lại hạn giữ 23/09) → từ chối (về Đang tạo + giữ dấu duyệt như ERP) → xoá.
      Lịch sử ghi đủ 6 dòng `create · send_approve · tp_approve · bgd_approve · reject · delete`.
      DB hoàn nguyên **lệch 0**
- [x] **Test validate**: SL vượt hợp đồng · không tick dòng nào · ngày quá khứ · ngày vượt trần —
      **cả 4 đều chặn đúng**, lỗi trả theo từng dòng (`products.0.qty`)

## Phase 5 — Controller + Request + Resource + route PYCXG ✅ (2026-09-03)

- [x] `ProductPrepickRequestStoreRequest` — `prepareForValidation()` **ép bool `need_export`**
      (chặn lỗi #8 ngay cửa vào) + rule riêng cho loại 99 (KH, Ghi chú, File đính kèm bắt buộc);
      `ProductPrepickRequestRejectRequest`
- [x] `ProductPrepickRequestListResource` — `status_color` do BE quyết, 5 cờ `is_can_*`;
      **cột Số hợp đồng gom theo bảng, mỗi bảng 1 truy vấn** (đo: 20 dòng chỉ tốn **16 query**)
- [x] `ProductPrepickRequestController` — 13 action, gate 423 LOCKED ở `update`/`destroy`
- [x] 13 route trong `Modules/Finance/Routes/api.php` (route tĩnh khai TRƯỚC `/{id}`)
- [x] Gọi thật: `index` 2.070 phiếu · `show` phiếu 39 dòng + 3 cấp duyệt · `contracts` 9.466 HĐ ·
      `contract-data` 39 dòng · `approved-quantities` 27 hàng
- [x] **VÁ THÊM LỖI RÒ RỈ (#16)**: `canView()` của ERP cho qua nếu có `Quản lý giữ hàng` — **546
      người** có quyền đó (so với 53 người có "Xem theo công ty") nên gần như ai cũng mở được mọi
      phiếu bằng URL, trong khi danh sách chỉ hiện phiếu của họ. HRM cho `canView()` khớp 1-1 với
      `searchByFilter()`. Đã đo lại: NV thường mở phiếu người khác → **403**, danh sách vẫn 194 phiếu

## Phase 6 — Service + Controller PXG (bước GHI TỒN) ✅ (2026-09-03)

- [x] `WarehousePrepickRequestService`: `dataFromRequest()` (chỉ nhận YCXG ở "Chờ KT duyệt", chặn
      lập trùng phiếu) · `store`/`update` · `applyStatus` · `approveAndWriteStock` · `destroy` ·
      `normalizeLines` + `assertEnoughStock` (chỉ kiểm tồn khi DUYỆT, đúng ERP) · `unitCoefficient`
- [x] Vá lỗi #9 (bọc transaction nên fail là rollback sạch), #8 (ép bool)
- [x] `WarehousePrepickRequestHistoryService` (4 action) · `...StoreRequest` · `...ListResource` ·
      `WarehousePrepickRequestController` (8 action) · 8 route
- [x] Đồng bộ trạng thái phiếu cha: nháp → cha 5 · duyệt → cha 1 + đóng dấu `approver_id` ·
      xoá → cha về 2
- [x] **TEST LUỒNG ĐẦY ĐỦ trên dữ liệu thật** (transaction + rollback): lập YCXG loại 99 → TP duyệt
      → lập PXG nháp (cha về 5) → duyệt (cha về 1) → kiểm lô sinh ra:
      `objectable_type = WarehousePrepickRequest`, `employee_id` = **người lập YC** (không phải kế
      toán), `company_id` theo YC, `qty` đúng hệ số quy đổi, `prepick_qty` ghi ngược vào dòng PXG,
      `prepick_logs` ghi `...RequestDetail` trỏ đúng id dòng. Phiếu đã duyệt `canDelete = false`.
      **DB hoàn nguyên lệch 0 ở cả 5 chỉ số**

## Phase 7 — Chặn quá hạn (`checkDueConfigs`) ✅ (2026-09-03)

- [x] `DueConfigBlockService` — **service dùng chung MỚI**, port gộp `CheckDueConfigs` +
      `DueConfigBlockService::isManagerBlocked()` của ERP. **Tra `due_configs` theo TÊN THAO TÁC**
      thay vì hard-code ~180 dòng `$block_routes[] = 'ten.route'` như ERP → thêm cấu hình ở DB là
      chạy ngay
- [x] Middleware `Modules/Finance/Http/Middleware/CheckDueConfig` + alias `dueConfig` trong
      `app/Http/Kernel.php`. Trả **423** kèm `show_overdue_modal` để FE mở popup như ERP.
      Đặt ở MIDDLEWARE vì controller nhận `FormRequest` (guard trong controller không chạy trước validate)
- [x] Gắn vào 4 route: `store` · `update` · `contract-data` (`dueConfig:Lập yêu cầu xuất giữ`) và
      `approve` (`dueConfig:Duyệt yêu cầu xuất giữ,manager`)
- [x] **Test thật**: emp 781 (còn hàng nhập thẳng quá hạn) → **423 "Có hàng nhập thẳng quá hạn!"**;
      emp 34 → 200

> ⚠️ **Thực trạng cấu hình** (`gop_db` 03/09/2026): `Lập yêu cầu xuất giữ` CHỈ có dòng ở nhóm
> **"Hàng nhập thẳng quá hạn"** (id 17, cả 5 công ty đều bật) — 2 nhóm "Hàng giữ quá hạn" và
> "Hàng mượn quá hạn" **chưa có dòng nào**, nên nhánh tương ứng trong code ERP không bao giờ chạy.
> Cấu hình tab 2 `Duyệt yêu cầu xuất giữ` (id 22) **chưa công ty nào bật** → nhánh chặn trưởng phòng
> chưa test được bằng dữ liệu thật (đã test bằng hàm trực tiếp). Đừng báo "chặn hỏng" khi thấy còn
> hàng giữ quá hạn mà vẫn lập được phiếu.

> 📌 2 màn **Gia hạn** và **Điều chuyển hàng giữ** đã port trước đây CHƯA gắn middleware này (ERP
> có chặn: `Gia hạn hàng giữ` / `Điều chuyển hàng giữ` id 18, 19). Service đã hỗ trợ sẵn tên thao
> tác của chúng — gắn thêm chỉ cần 1 dòng `->middleware(...)` ở route, nhưng là **sửa màn đang chạy
> nên phải hỏi user trước**.

## Phase 8 — FE màn danh sách PYCXG ✅ (2026-09-03)

- [x] `pages/finance/product-prepick-requests/index.vue` — 4 mixin bắt buộc,
      `localStorageKey` + `columnScreenKey` = `finance_product_prepick_requests` (grep không trùng
      màn nào), `V2BaseSmartFilterPanel` + schema `filterFields` 11 ô
- [x] 9 cột mặc định + 7 cột ẩn ở Cấu hình cột; sort mặc định ngày tạo giảm dần; key cột sort
      trùng `SORTABLE_COLUMNS` của BE (`code` · `createdAt` · `approvedTime` · `expireDate`)
- [x] `V2BaseRowActions` handler `switch (action)` (emit CHUỖI); nút không dùng được thì **ẩn**
      bằng `visible`; hành động "Lập phiếu xuất giữ" mở thẳng màn con kèm query
- [x] `components/export-excel.js` (15 trường) + `print-list.vue` khổ ngang

## Phase 9 — FE form PYCXG ✅ (2026-09-03)

- [x] `components/ProductPrepickRequestForm.vue` (1.3k dòng) — **2 khuôn bảng chi tiết** trong cùng
      một component: loại 1-5 (tick "Cần xuất" + 2 cột SL hợp đồng / Đã xuất kho, không thêm-xoá
      dòng) và loại 99 (tự thêm hàng + chọn ĐVT + xoá dòng)
- [x] `components/ContractSearchModal.vue` — **1 popup dùng cho cả 5 loại hợp đồng**: BE tự đổi bảng
      theo `type` gửi lên, nên KHÔNG phải dựng 5 popup như đã lo ở design
- [x] Popup thêm hàng dùng lại `QuotationProductSearchModal` (component chung ~40 màn), KHÔNG dựng mới
- [x] "Giữ đến ngày" `V2BaseDatePicker`; hiện sẵn dòng "Không giữ quá dd/mm/yyyy" nhưng vượt thì
      **BE báo đỏ**, FE không tự kéo về trần
- [x] `unsavedChangesMixin` + `markUserEdited()` cho dữ liệu về sau `await`; `markFormSaved()` trước
      khi rời màn
- [x] Đính kèm qua endpoint `upload-files` (13 MB, bộ đuôi đúng ERP)

## Phase 10 — FE chi tiết + duyệt PYCXG ✅ (2026-09-03)

- [x] `_id/index.vue` · `_id/edit.vue` (vào bằng URL khi hết quyền sửa thì đá về Chi tiết) ·
      `create.vue` · `_id/print.vue`
- [x] Nút footer **khớp hệt** cột Hành động ngoài danh sách, đọc cùng bộ cờ BE:
      Sửa · Xóa · In · TP/BGĐ duyệt · Từ chối · Lập phiếu xuất giữ. Tất cả trong `V2Footer`
      slot `#custom-actions`
- [x] `RejectModal` bắt buộc lý do ≤ 255; khối "Lịch sử duyệt" + `PrepickHistoryPanel` (mặc định ẩn)
- [x] Mọi thao tác xong đều `markFormSaved()` rồi **quay về danh sách**

## Phase 11 — FE cặp màn PXG ✅ (2026-09-03)

- [x] `pages/finance/warehouse-prepick-requests/` — index (9 cột, cột **YCXG là `<nuxt-link>`**
      sang phiếu cha) · create · `_id/index` · `_id/edit` · `_id/print` · print-list · export-excel
- [x] `components/WarehousePrepickRequestForm.vue` — khoá mọi thông tin lấy từ yêu cầu, kế toán chỉ
      sửa SL xuất / hạn giữ / ghi chú / đính kèm
- [x] Nút **"Duyệt giữ hàng" luôn hỏi xác nhận** trước (`$confirm`) vì đó là thao tác GHI TỒN
      không hoàn tác được; màn chi tiết hiện thêm cột **SL giữ (ĐV cơ bản)** = `prepick_qty`
- [x] Màn này KHÔNG có nút "Tạo mới" độc lập — nút đưa sang danh sách Yêu cầu xuất giữ để chọn phiếu
      (phiếu xuất giữ chỉ sinh từ 1 yêu cầu ở bước Kế toán, đúng ERP)

## Phase 12 — In + Xuất Excel ✅ (2026-09-03)

- [x] BE: `renderPrint` / `renderPrintList` / `exportData` cho cả 2 màn + 4 blade
      (`product-prepick-request[-list]`, `warehouse-prepick-request[-list]`) trong
      `Modules/Finance/Resources/views/prints/` — KHÔNG ghi vào `report_templates` dùng chung với ERP
- [x] 6 endpoint mới: `{id}/print-data` · `print-list-data` · `export` (mỗi màn)
- [x] Vá lỗi #3 (ngày duyệt null in ra hôm nay) và #11 (COLSPAN 9 ≠ 8 cột)
- [x] FE: nút Xuất mở `ExportFieldsModal` chọn trường TRƯỚC, file dựng bằng ExcelJS ở FE;
      BE trả đủ trường kể cả cột đang ẩn
- [x] Gọi thật: `printData` 13.987 ký tự HTML · `export` 2.056 dòng × 15 cột ·
      `printListData` 548 KB; phía PXG: 2.056 dòng, HTML 492 KB

## Phase 13 — Menu, quyền, checklist ✅ (2026-09-03) — còn verify trình duyệt

- [x] Gắn `link` vào **2 mục có sẵn** ở `components/subsystem-menu/finance.js` nhóm "Giữ hàng"
      (không tạo mục mới)
- [x] Chạy 8 lệnh grep tự kiểm trên CẢ 2 thư mục feature — **sạch**: không `status-pill`,
      không `interactable:`/`disabledTitle`, không `action.key ===`, không `V2BaseFilterPanel`,
      không `advanced-filters`, không `toLocaleString('vi-VN')` cho số, không HTML thô thay `V2Base*`,
      không `.text-muted`
- [x] Đối chiếu API component thật (đã sửa 3 chỗ dùng sai): `V2BaseCheckbox` nhận `value`+`disabled`
      (không phải `checked`/`interactable`); `V2BaseLabel` **không có slot `#suffix`** — icon ⓘ phải
      truyền qua prop `hint`; `formValidateMixin` chỉ có `clearServerErrors()` và gán thẳng
      `formErrors`, KHÔNG có `setFormErrors`/`clearFormErrors`
- [x] 18/18 file FE compile sạch (vue-template-compiler + babel parser); line ending CRLF đồng nhất
- [x] **Verify trình duyệt thật** (Playwright, local `:3000` + API `:8000`, nhánh feature):
      danh sách YCXG hiện đúng 9 cột · ô lọc Mã phiếu bấm thật ra đúng 1 dòng · popup Lịch sử
      mở được · cột Hành động chỉ hiện In + Lịch sử với phiếu đã duyệt (Sửa/Xóa ẩn hẳn) ·
      chi tiết `PYCXG-01862` hiện đủ thông tin + 3 dòng hàng + 2 cấp duyệt · bản in phiếu
      đúng khổ A4 dọc (793px ≈ 210mm) · in danh sách đúng khổ ngang (1122px ≈ 297mm), 17 phiếu
- [x] **Sửa 2 lỗi tìm được khi verify** (xem mục dưới)
- [x] **Verify LUỒNG ĐẦY ĐỦ trên trình duyệt** — đã cấp tạm 3 quyền duyệt cho tài khoản test
      (emp 781: `Trưởng phòng duyệt hàng giữ` 100836 · `Ban giám đốc duyệt hàng giữ` 100837 ·
      `Kế toán duyệt hàng giữ` 100838, ghi thẳng `employee_has_permissions`):
      Lập YCXG loại 5 (HĐ hãng) → chọn hợp đồng → TP duyệt → BGĐ duyệt → Kế toán **Lập phiếu
      xuất giữ** → lưu nháp → **Duyệt giữ hàng**. Kết quả DB:
      · `PYCXG-02219`: 6 → 4 → 2 → 5 → 1, đóng dấu đủ 3 cấp duyệt
      · `PXG-02190`: nháp (3) → duyệt (1)
      · `prepick_details` #53848: qty 2, `employee_id` = **781 (người YÊU CẦU, không phải kế
        toán)**, `expire_date` 25/09/2026, `objectable_type` = `WarehousePrepickRequest`
      · `prepick_logs` #110767: 0 → +2 → 2, `objectable` trỏ **dòng chi tiết** PXG (đúng ERP);
        cột `warehouse_prepick_request_detail_id` để NULL — đã đối chiếu: **0/110.745 dòng ERP
        cũ có giá trị**, cột chết, không phải thiếu sót
      · `prepick_qty` ghi ngược về dòng PXG = 2
      Danh sách PXG từ **rỗng → 878 phiếu** sau khi có quyền kế toán — xác nhận lần trước
      rỗng là **đúng phạm vi quyền**, không phải lỗi.
- [x] **Chặn quá hạn** (`dueConfig`): tắt tạm dòng `company_due_configs` (17, công ty 1) để chạy
      luồng, **khôi phục ngay sau đó** và bấm thử lại: chặn ăn ở bước chọn hợp đồng, báo
      "Có hàng nhập thẳng quá hạn!".
- [x] **Sửa giao diện form theo phản hồi user** (xem mục dưới)
- [ ] Đối chiếu ngược từng dòng bảng ở design.md mục 1 với màn ERP
- [ ] ⛔ **Gỡ 3 quyền tạm** `100836` / `100837` / `100838` của emp 781 khỏi
      `employee_has_permissions` (cấp tay để chạy luồng ở Phase 13). **Không có script
      `revert_test_perms.sql`** — phải xoá tay 3 dòng đó
- [ ] Dọn dữ liệu test (nếu muốn): `PYCXG-02219` · `PXG-02190` · lô `prepick_details` #53848 ·
      `prepick_logs` #110767
- [ ] Chạy migration `2026_09_03_000001_create_prepick_export_request_history_tables` **trên dev**
- [ ] Commit 2 repo — tính đến 2026-09-03 nhánh `feat/finance-prepick-export-request` **chưa commit**

### 5 lỗi giao diện/hiển thị tìm được khi verify luồng đầy đủ (đã sửa)

| # | Lỗi | Sửa |
|---|---|---|
| C | **Cả 2 form mất viền/nền card** — dùng đúng markup `form-card` như 4 màn Giữ hàng đã port nhưng **quên hẳn khối SCSS định nghĩa nó**; lại còn đặt `scoped` (chặn style xuống DOM của `V2Base*` con) | Chép nguyên khối chuẩn từ `PrepickExtendRequestForm.vue`, bỏ `scoped`, bọc trong `.ppr-form` / `.wpr-form`; thêm `padding-bottom: 90px` chừa chỗ cho `V2Footer` |
| D | Popup **Chọn hợp đồng** `size="lg"` (800px) hẹp hơn bảng 5 cột (881px) → cột "Giá trị HĐ" và **nút Chọn bị đẩy khỏi vùng nhìn**, phải cuộn ngang mới bấm được | Đổi sang `size="xl"` |
| E | Ô **SL đề nghị điền sẵn `0`** → user gõ `2` ra **`20`** (tương tự `qty: 1` ở loại tự thêm hàng) | Để **rỗng** + placeholder "Nhập SL"; thêm `@focus.native="$event.target.select()"` cho cả 2 form để giá trị điền sẵn (màn Sửa) bôi đen khi focus |
| F | Màn **Chi tiết YCXG**: 2 cột "SL hợp đồng" / "Đã xuất kho" luôn hiện **0** (FE hard-code 0) — người xem hiểu nhầm hợp đồng có 0 cái | `detailData()` tra lại `contractLines()` của hợp đồng nguồn (bọc `try/catch ValidationException` — hợp đồng bị xoá không được làm hỏng cả màn); tra không ra trả **null** để ô TRỐNG |
| G | Màn **Chi tiết PXG**: "SL có thể giữ" luôn **0** và "SL yêu cầu" lấy nhầm chính SL của PXG — **kế toán tưởng hết hàng nên không dám duyệt ghi tồn** | `detailData()` của PXG trả thêm `request_qty` (từ dòng phiếu CHA) và `in_stock` tra theo **người yêu cầu**; tra không ra → null → ô trống |

> ⚠️ **Bài học `formatNumber`**: cả 2 form trước đó quy đổi `null → 0 → "0"`. `null` KHÁC `0`:
> không tra được thì phải để **ô trống** (rule "ô rỗng để trống"), in "0" là **bịa số** và ở
> đây dẫn thẳng đến quyết định nghiệp vụ sai.

> ⚠️ **Bài học test select2 bằng Playwright**: `selectOption()` vào thẻ `<select>` gốc chỉ đổi
> DOM, **không bắn `change` lên Vue** — tôi đã tưởng "chọn loại xong ô Hợp đồng không hiện"
> là lỗi màn. Phải bấm `.select2-selection--single` rồi bấm `.select2-results__option`.

### 2 lỗi tìm được khi verify trình duyệt (đã sửa)

| # | Lỗi | Sửa |
|---|---|---|
| A | Cột **"Có thể giữ" luôn hiện 0 ở màn Chi tiết** — tôi chỉ nạp tồn khi ở màn Sửa. Hiện 0 làm người xem tưởng hàng đã hết | Nạp `refreshInStock()` ở CẢ màn Chi tiết; BE `detailData()` trả thêm `created_by` để FE tra tồn hộ **CHỦ PHIẾU** (không phải người đang xem). Đo lại: hàng thứ 3 ra **49** thay vì 0 |
| B | **14 file FE + 4 blade đang là LF thuần** trong khi repo dùng CRLF | Chuẩn hoá lại toàn bộ 18 file về CRLF |

> ⚠️ **Bài học đo line ending**: `grep -c $'\r' <file>` trên Git Bash Windows trả về đúng bằng
> số dòng KỂ CẢ khi file là LF thuần — tôi đã dựa vào nó và báo nhầm "CRLF đồng nhất" ở
> Phase 13. Chỉ tin phép đếm ở mức BYTE:
> `python -c "d=open(f,'rb').read(); print(d.count(b'\\n')==d.count(b'\\r\\n'))"`.

> ⚠️ **Bài học kiểm .vue**: script kiểm cú pháp mà cắt import bằng regex 1 dòng sẽ báo lỗi GIẢ
> `Unexpected token '}'` với import nhiều dòng — tôi đã mất một lượt đi tìm lỗi không có thật.
> Dùng `@babel/core.parseSync({sourceType:'module'})` trên khối script do
> `vue-template-compiler.parseComponent()` tách ra.

---

## Rủi ro đã biết

| Rủi ro | Ảnh hưởng | Giảm thiểu |
|---|---|---|
| Local không có phiếu loại 1–4 | Không nghiệm thu được 4/6 loại | Xin dump dev (Phase 1); trước khi có thì **không báo xong** |
| `contracts` / `project_contracts` gần như rỗng | Popup chọn HĐ loại 1, 2, 4 rỗng trên local | Ghi rõ khi bàn giao, test trên dev |
| Sửa `AccountingStockService` + tách `PrepickApprovalRouteService` | Có thể làm hỏng 3 màn đã nghiệm thu | Chỉ thêm field / giữ nguyên chữ ký; test lại từng màn ngay trong Phase 2 |
| Bước ghi tồn giữ | Sai là hỏng dữ liệu thật của 4 màn giữ hàng | Sao lưu trước, test trên phiếu mới, hoàn nguyên và đối chiếu số dòng |
| `need_export` so chuỗi (lỗi ERP #8) | Phiếu lưu ra 0 dòng mà không báo lỗi | Ép kiểu bool ở FormRequest + test case riêng |

---

## Ghi chú dữ liệu (2026-09-03)

Đếm trên **4 bản dump ERP có sẵn ở máy local** — phiếu Yêu cầu xuất giữ theo loại:

| DB | loại 5 (HĐ hãng) | loại 99 (khác) | loại 1–4 |
|---|---|---|---|
| `gop_db` | 501 | 1.673 | **0** |
| `erp_dev_30_01_26` | 11 | 169 | **0** |
| `erp_dev_24_09` | 11 | 168 | **0** |
| `new_erp_1_8` | 3 | 105 | **0** |

⇒ Loại 1–4 nhiều khả năng là **nhánh code chết** của ERP, không phải chuyện local thiếu dữ liệu.
Đã chốt vẫn port đủ 6 loại; nhưng nên hỏi lại bộ phận nghiệp vụ xem 4 loại đó còn dùng không
trước khi bỏ công dựng 3 popup chọn hợp đồng (HĐ bán đời cũ, HĐ dự án) mà bảng nguồn đã rỗng.
