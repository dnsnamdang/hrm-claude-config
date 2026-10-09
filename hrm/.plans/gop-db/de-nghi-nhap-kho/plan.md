# Plan — Đề nghị nhập kho (PDNNK)

Nhánh `gop_db` · @namdangit · Spec: `docs/superpowers/specs/gop-db/2026-08-25-de-nghi-nhap-kho-design.md`

## Phase 1 — Backend (Module Finance)

- [x] Migration `2026_08_25_000002_add_emplement_contract_to_warehouse_import_requests_table.php`
      (mirror template PIR: emplement_contract_id/type/code, guard hasColumn) — đã migrate
- [x] Entity `WarehouseImportRequest` (Modules/Finance/Entities/WarehouseImportRequest/)
      — 7 STATUS_*, getStatusList, getTypeName/getAllTypesForFilter proxy PIR::TYPE_NAMES,
      generateCode PDNNK, relations, files(), scopeForHrmContract
- [x] Entity `WarehouseImportRequestDetail` (DETAIL_TYPE_HANG_HOA, parent())
- [x] Service `WarehouseImportRequestService`
      — createFromImportRequest, updateDraft, approve (thủ kho), deny, cancel
      — qtyByProduct + syncDetails + buildDetailAttributes (snapshot dòng phẳng, fallback brand/model)
      — comment GÁC tầng 3 (warehouse_exported_qty type 4/9)
- [x] Transformer `WarehouseImportRequestResource` (cột list+chi tiết, cờ quyền fail-closed)
- [x] Controller `WarehouseImportRequestController`
      — scopedQuery, index, typeOptions, show(+attachSourcePrices), warehouseImportData,
        storeWarehouseImportRequest, editData, update, cancel, approve, deny,
        uploadAttachments/deleteAttachment, guards (assertCanEdit/Cancel/Approve/StockerApprove)
      — index/show adapt Finance ApiController (không có apiGetList → paginate thủ công, responseJson)
- [x] Routes `Modules/Finance/Routes/api.php`
      — group /warehouse-import-requests (static trước /{id}) + 2 route lập từ YCNH trong /product-import-requests
      — KHÔNG gắn checkPermission (spatie model_type mismatch với quyền ERP) → gate trong Controller
- [x] Permission seeder: 4 quyền "Xem đề nghị nhập kho theo {tổng công ty|công ty|phòng ban|bộ phận}" (id 1539-1542)
- [x] Chạy migrate + seeder; smoke test route (index/show/warehouse-import-data)
      — index/show/typeOptions OK; write path dry-run (createFromImportRequest) OK, rollback

## Phase 2 — Frontend (hrm-client, pages/finance/warehouse-import-requests/)
- [x] Index (filter 4 cấp + type + status) — `index.vue`, cột NCC/Kho nhập/Mã YCNH, envelope Finance {items,total,lastPage,currentPage,perPage}, column-customization key `finance_warehouse_import_requests`
- [x] Chi tiết — `_id/index.vue`, info + dòng hàng (đơn giá/thành tiền) + file; actionbar In/Sửa/Duyệt/Từ chối/Hủy/Quay lại (gate cờ BE fail-closed); modal Từ chối bắt buộc lý do; In = window.print + @media print
- [x] Form Lập từ YCNH — `create.vue`, prefill kho từ YCNH, Lưu nháp(3)/Gửi thủ kho(2), payload products:[{product_id,qty}], upload đính kèm sau khi có id, unsavedChangesMixin
- [x] Form Sửa — `_id/edit.vue`, edit-data + PUT, đính kèm add/xoá realtime, unsavedChangesMixin
- [x] Rewire nút "Tạo đề nghị nhập kho" ở màn Yêu cầu nhập hàng → `goCreateWarehouseImportRequest` route nội bộ (gate `data.is_can_approve`), giữ nút "Tạo phiếu nhập hàng" mở ERP (tầng 3 chưa port)

## Fix phát sinh (QA logic duyệt)
- [x] **TP duyệt trước khi lập đề nghị nhập kho** — đối chiếu ERP: chỉ 2 loại trả lại (BAN_TRA_LAI=4, NHAP_BAN_MUON_TRA_LAI=9) mới auto nhảy status 2→12 "Chờ TP duyệt"; các loại khác đi thẳng Chờ duyệt → Kế toán kho lập đề nghị ngay. Nút "Tạo đề nghị nhập kho" gate bằng `is_can_approve` = `canApprove()` (yêu cầu status==CHO_DUYET) nên tự ẩn khi còn Chờ TP duyệt — HRM đã đúng.
- [x] Vá lỗ hổng: `ProductImportRequestService::handleAfterSubmit` (:1475) trước chỉ bump type 4 → thêm type 9 (in_array 4|9) để khớp ERP :699-701/:987-989. Type 9 vẫn nằm trong CREATABLE nên nếu tạo tay phải qua TP duyệt (nguồn borrow-sell loại 21 vẫn PENDING ở feature nhap-ban-tra-lai-hd21, tách riêng). Cả create(:219) + update(:248) dùng chung method → 1 chỗ vá đủ. `php -l` OK.

- [x] **Lọc dòng SL yêu cầu = 0 ở form Lập đề nghị nhập kho** — QA thấy dòng qty=0 vẫn hiện (báo lỗi validate đỏ). ERP `getDataForWarehouseImportRequest` (:750) lọc `->where('qty','>',0)`; HRM `warehouseImportData` (:213) thiếu → thêm `->where('qty','>',0)`. Chỉ ảnh hưởng form Lập (create); form Sửa đọc dòng đã lưu (mặc nhiên >0). `php -l` OK.

- [x] **Thông tin chung + độ rộng ô Kho nhập ở form Lập** — QA: (1) ô "Kho nhập" dài hết màn hình xấu; (2) luôn hiện "Nhà cung cấp: —" kể cả loại trả lại (4). Đối chiếu ERP `form.blade.php` (Kho nhập col-md-6 = nửa hàng) + `getPrintDataAttribute` (:857 type∈{4,9,14} → Khách hàng, còn lại NCC). Fix: BE `warehouseImportData` eager-load thêm `customer`, trả `use_customer` + `partner_name` (loại 4/9/14 lấy customer, còn lại supplier); FE `create.vue` label động NCC/KH + chặn width ô Kho nhập bằng **inline `style="max-width:520px"`** trên `.fld-grid` (KHÔNG dùng scoped CSS 2-cột vì Nuxt2 HMR không nạp lại `<style scoped>` — template/inline reload ngay). Form Sửa (`_id/edit.vue`) áp cùng inline max-width; không hiện đối tác nên không đổi label. QA: user xác nhận hiển thị đúng (Khách hàng + Kho nhập nửa hàng). `php -l` OK.

- [x] **Bug: tải đính kèm thất bại khi "Gửi thủ kho"** — root cause: `uploadAttachments` gate bằng `assertCanEdit` (chỉ cho `STATUS_DANG_TAO=3`). FE tạo phiếu với status người dùng chọn (2=Gửi thủ kho / 3=Lưu nháp) RỒI mới POST `/attachments` → khi chọn "Gửi thủ kho" phiếu đã sang status 2 → `assertCanEdit` trả 422 → upload fail (FE hiện toast "Tải tệp đính kèm thất bại"). FormData/headers OK (`getCommonOptions` không ép Content-Type, axios tự set multipart). Fix: thêm gate riêng `assertCanUploadAttachment` cho phép người tạo tải khi status ∈ {3, 2} (còn ở bước lập, chưa thủ kho duyệt/nhập kho/hạch toán/hủy) — đúng ERP (file store atomic). `php -l` OK. **Lưu ý:** ĐNXK (`Modules/Assign`) có cùng lỗ hổng (uploadAttachments cũng dùng assertCanEdit draft-only) — feature khác, chưa đụng, chờ user quyết.

- [x] **Đưa "File đính kèm" lên trên bảng hàng hoá ở màn Sửa + Chi tiết** — cho khớp màn Tạo (thứ tự: Thông tin chung → File đính kèm → Danh sách hàng hoá). Trước đó edit.vue + _id/index.vue để File dưới bảng. Chi tiết: block sec-files vẫn nằm trong `#print-area` nên bản in giữ đúng thứ tự.

- [x] **Gắn link menu "Đề nghị nhập kho"** — QA: bấm menu không đi đâu. `components/subsystem-menu/finance.js:112` mục "Đề nghị nhập kho" chỉ có `label`, thiếu `link` → thêm `link: '/finance/warehouse-import-requests'` (giống mẫu "Đề nghị xuất kho" :132). Các mục cùng nhóm còn lại (Phiếu nhập kho…) vẫn chưa link vì thuộc tầng 3.

## Tầng 3 (feature tách sau)
- [ ] Phiếu nhập kho thực + hạch toán (ghi tồn + sổ), tabs, warehouse_exported_qty, thông báo

---

### Checkpoint — 2026-08-25 (khởi tạo)
Vừa hoàn thành: spec chi tiết + design tóm tắt + plan; đã đọc toàn bộ template ERP/HRM.
Đang làm dở: bắt đầu P1 — migration + Entity.
Bước tiếp theo: viết migration warehouse_import_requests emplement + 2 Entity.
Blocked:

### Checkpoint — 2026-08-25 (P2 FE xong)
Vừa hoàn thành: TOÀN BỘ Phase 2 FE — 4 trang `pages/finance/warehouse-import-requests/`
(index.vue, _id/index.vue, create.vue, _id/edit.vue) mirror ĐNXK nhưng adapt:
- Namespace API `finance/…` (không phải `assign/…`); envelope Finance {code,message,data}
  (index đọc data.items + map pagination {total,lastPage,currentPage,perPage}; show đọc data.detail).
- Bỏ phần tồn kho (SL được xuất/đang giữ) — nhập kho không cần; cột "Nhà cung cấp" thay "Khách hàng",
  "Kho nhập" thay "Kho xuất"; payload products:[{product_id,qty}].
- Chi tiết thêm nút Thủ kho Duyệt/Từ chối (BE mình có, ĐNXK không) + modal lý do từ chối + In (window.print).
- Rewire nút "Tạo đề nghị nhập kho" ở màn YCNH (`product-import-requests/_id/index.vue`) từ openErpScreen
  sang route nội bộ `goCreateWarehouseImportRequest` (giữ gate cờ BE `data.is_can_approve`).
Đang làm dở: không có — P2 đóng.
Bước tiếp theo: user QA trên trình duyệt (login Kế toán kho + thủ kho); nếu OK thì đóng feature (chờ tầng 3 tách sau).
Blocked: chưa chạy dev server để smoke UI (môi trường này không bật FE); cần user verify.

## Fix UI (2026-08-26): màn Sửa thiếu trường ở "Thông tin chung"
- [x] `_id/edit.vue`: khối "Thông tin chung" chỉ có Mã phiếu + Số hợp đồng → user không biết đang nhập kho **loại nào**. Bổ sung dòng readonly: Loại nhập kho (`type_name`), Mã YCNH (`product_import_request_code`), NCC/Khách hàng (`supplier_name`/`customer_name`), Phòng ban (`department_name`), Người lập (`creator_name`), Ngày tạo (`created_at`).
- [x] **BE `editData` (root cause thực)**: endpoint `/{id}/edit-data` tự build mảng `request` bằng tay, KHÔNG dùng full Resource → chỉ có 7 field, thiếu type_name/product_import_request_code/department_name/creator_name/created_at/supplier_name/customer_name → FE hiện label nhưng value đều "—". Fix: eager-load `creator.info.department`, `productImportRequest`, `supplier`, `customer` + bổ sung các field vào mảng `request` (tính giống Resource). `V1/WarehouseImportRequestController@editData`.

## Nối tầng 3 (2026-08-26): "Duyệt" ĐNNK → "Tạo phiếu nhập kho" (deep-link ERP, mirror ĐNXK)
Chốt phương án **B** (user: "làm logic giống luồng xuất hàng"): HRM KHÔNG dựng lại phiếu nhập kho vật lý /
hạch toán. ĐNNK dùng chung bảng `warehouse_import_requests` với ERP → sau "Chờ duyệt", thủ kho bấm
"Tạo phiếu nhập kho" mở màn ERP `admin/warehouse/warehouse_imports/create?warehouse_import_request_id=`,
chính ERP gọi `WarehouseImportRequest::approve()` đẩy status 2→1→6→7→4 trên cùng record. HRM chỉ đọc lại status.
Đối chiếu ERP: `WarehouseImportRequest::canApprove()` = thủ kho của kho + status==2, **KHÔNG loại type nào**
(khác export loại type=5) → import cho mọi loại.
- [x] BE Resource `WarehouseImportRequestResource`: bỏ cờ `is_can_approve`; thêm `is_can_create_warehouse_import`
  = `canCreateWarehouseImport($status)` (status==Chờ duyệt(2) + Super Admin hoặc thủ kho kho qua `warehouse_stockers`;
  copy `canCreateWarehouseExport` bỏ điều kiện type=5). Giữ `is_can_deny`.
- [x] BE gỡ nhánh "Duyệt" đứng một mình (kiểm soát status chỉ do ERP đẩy): xóa route `POST /{id}/approve`,
  method `approve` (Controller) + `WarehouseImportRequestService::approve()`. Giữ `deny`/`cancel` +
  `assertCanStockerApprove` (deny còn dùng).
- [x] FE `_id/index.vue`: bỏ nút "Duyệt" + `confirmApprove()`; thêm nút "Tạo phiếu nhập kho"
  (gate `is_can_create_warehouse_import`) → `goCreateWarehouseImport()` mở tab ERP (dùng `process.env.tp_url`).
  Giữ Từ chối / Hủy / Sửa / In.
- URL ERP xác nhận: `warehouse_imports` cùng nhóm `admin/warehouse/` với `warehouse_exports` (routes/web.php:847,1445).
- Blocked: user QA trên trình duyệt (login thủ kho + Super Admin), kiểm nút hiện đúng ở status Chờ duyệt và
  màn ERP mở đúng, status quay về HRM cập nhật 1→6→7→4.

### Checkpoint — 2026-08-25 (P1 xong)
Vừa hoàn thành: TOÀN BỘ Phase 1 BE — migration (đã migrate trên erp_hrm_check), 2 Entity,
Service, Resource, Controller (11 method + 4 guard), routes (12 route đã register đúng thứ tự
static→dynamic), 4 permission (id 1539-1542, đã seed). Smoke test tinker: typeOptions/index/show
200 OK; write path createFromImportRequest dry-run tạo WIR + snapshot detail + chuyển YCNH→7, rollback.
Sửa lỗi lúc test: eager-load supplier/customer dùng cột `fullname` (customers không có `name`).
Quyết định: KHÔNG gắn middleware checkPermission cho route ghi (spatie getAllPermissions filter
model_type=Timesheet\Employee → bỏ sót "Kế toán kho" gán từ ERP model_type=App\Employee) — gate
trong Controller bằng isCurrentEmployeeHasPermission (PermissionHelper query pivot).
Đang làm dở: không có — P1 đóng.
Bước tiếp theo: Phase 2 FE (pages/finance/warehouse-import-requests/) — index/chi tiết/form lập từ YCNH/
duyệt-từ chối-hủy/in + rewire nút "Tạo đề nghị nhập kho" ở màn Yêu cầu nhập hàng.
Blocked:

## Fix ticket "Lỗi UI + Thiếu nút" màn list (2026-09-19) — Lê Huyền Trang → Trần Cư
Screen `/finance/warehouse-import-requests`. Ticket 2 vấn đề:
- **Lỗi 1 — UI ô lọc ngày**: label "Đến" → "Ngày tạo đến"; thêm placeholder "Từ ngày"/"Đến ngày".
- **Lỗi 2 — thiếu nút**: (a) "Tạo mới" · (b) "Xuất Excel".
Quyết định user: **Tạo mới = Option A (KHÔNG thêm)** — ĐNNK lập từ YCNH (create-from-YCNH), không tạo trực tiếp;
giữ đúng kiến trúc như màn ĐNXK (twin). **Xuất Excel = làm** ("A, xuất excel thì cứ làm").
Pattern chuẩn: **bám màn twin ĐNXK** (`warehouse-export-requests`) — BE `export()` trả JSON rows thô theo
đúng filter+scope, FE dựng .xlsx bằng ExcelJS (`components/export-excel.js`) + popup chọn trường `ExportFieldsModal`.
- [x] Lỗi 1: `index.vue` sửa nhãn "Ngày tạo đến" + thêm placeholder "Từ ngày"/"Đến ngày" (lines 42-49).
- [x] BE route `GET finance/warehouse-import-requests/export` (đặt TRƯỚC `/{id}`, sau `/type-options` — api.php:507), KHÔNG gate riêng (scope trong scopedQuery, mirror twin). php -l sạch.
- [x] BE refactor filter của `index()` → `applyFilters($query,$request)` dùng chung (Controller:99); thêm `export()` trả `{rows, filter_text}` (Controller:162) + helper `exportFilterText()` (Controller:211). php -l sạch.
- [x] FE `components/export-excel.js` (ĐNNK) — 13 cột mirror list: Mã phiếu · Loại · Mã YCNH · Số hợp đồng · Nhà cung cấp · Khách hàng · Kho nhập · Người lập · Ngày tạo · Trạng thái · Người duyệt · Ngày nhận · Ngày duyệt (+STT tự chèn).
- [x] FE `index.vue`: thêm nút "Xuất Excel" (trước nút cấu hình cột — line 77) + `ExportFieldsModal` (line 167) + `openExportModal()`/`exportExcel()` (line 438-460) + cờ `exporting` + computed `exportFields`.
- [x] Verify Playwright (login emp 48 `ductv.kd2@tanphat.com`, đã khôi phục mật khẩu gốc). ✓ Lỗi 1: nhãn "Ngày tạo từ"/"Ngày tạo đến" + placeholder "Từ ngày"/"Đến ngày". ✓ Lỗi 2b: nút "Xuất Excel" hiện trước nút cấu hình cột → popup "Chọn trường xuất Excel" 13 trường → request `GET .../export` trả 200 → tải `danh_sach_de_nghi_nhap_kho.xlsx` (tiêu đề + STT + 13 cột + khối ký). BE row-mapping xác minh bằng tinker trên phiếu thật: 13 cột map đúng (mã/loại/YCNH/HĐ/NCC/KH/kho/người lập/ngày/trạng thái/người duyệt/ngày nhận/ngày duyệt).
- [ ] Trả lời reporter: "Tạo mới" là chủ ý thiết kế (lập từ YCNH), không bổ sung. (còn lại — user gửi Redmine)
- [x] Commit + push `gop_db` (2026-09-19): hrm-api `427565235`→push (Finance controller+routes; +commit ĐNXK comment `79724d738`), hrm-client (import `427565235`, export `f7dc9f528`). Cả 2 repo push OK lên origin/gop_db.

### Checkpoint — 2026-09-19
Vừa hoàn thành: code-complete cả Lỗi 1 + Lỗi 2. BE route+export()+applyFilters()+exportFilterText() (php -l sạch, route đúng thứ tự). FE export-excel.js + index.vue (nút + modal + imports + cờ + computed + methods). Line ending giữ nguyên LF (khớp file gốc). Static check pass hết.
Đang làm dở: chờ verify UI.
Bước tiếp theo: bật dev server :8000/:3000 → Playwright smoke (nút Xuất Excel hiện, mở popup chọn trường, tải .xlsx) → rồi trả lời reporter.
Blocked: cả 2 dev server đang tắt → chưa smoke được UI.

## Fix bug "Lập ĐNNK: mất dữ liệu + không có quyền dù tk có quyền" (2026-09-22)
Redmine (status → Phản hồi): *"Lập đề nghị nhập kho đang mất dữ liệu, ko có quyền để lập mặc dù tk này có quyền"*.

**Nguyên nhân gốc (đã xác minh code + schema + data thật):** luồng LẬP dùng 2 cơ chế kiểm quyền "Kế toán kho" LỆCH nhau.
- Nút "Tạo đề nghị nhập kho" hiện theo cờ `is_can_approve` = `ProductImportRequest::canApprove()` → dùng trait
  `Concerns/ChecksEmployeePermission::currentEmployeeHasPermission` (query pivot RAW: quyền trực tiếp + role, KHÔNG
  lọc model_type/guard/company). RỘNG & đúng cho DB gộp.
- Nạp form `GET .../warehouse-import-data` (Controller:436) và Lưu `POST` (Controller:493) đều gọi `assertCanCreate()`
  → global `isCurrentEmployeeHasPermission()` (`app/Helper/PermissionHelper.php:20`): roleIds qua quan hệ spatie
  `$employee->roles` (LỌC `model_type=Timesheet\Employee`) + lọc `role_has_permissions.company_id=current_company_role`
  + KHÔNG đọc quyền trực tiếp. HẸP.
- ⇒ Người có "Kế toán kho" qua role ERP (`model_type=App\Employee`) / quyền trực tiếp / role khác công ty hiện tại:
  THẤY nút (trait) nhưng GET trả 422 → **form rỗng = "mất dữ liệu"**, và POST trả 422 = **"không có quyền dù tk có quyền"**.
  (Checkpoint 2026-08-25 chọn global helper vì TƯỞNG nó "query pivot" robust — thực tế vẫn qua spatie lọc model_type.)

**Bằng chứng dữ liệu (erp_hrm_check):** quyền "Kế toán kho" (2 id trùng tên 1136+100080): 13 NV bắt qua role Timesheet
(cũ thấy), **57 NV chỉ có qua role ERP `App\Employee` → helper cũ BỎ SÓT**, 0 NV quyền trực tiếp. Ca cụ thể employee 34
(`current_company_role=NULL`): gate CŨ=false (chặn) vs gate MỚI `canApprove()`=true (cho lập).

**Bác bỏ giả thuyết phụ:** "mất dữ liệu do buildDetailAttributes bỏ backfill brand_name/model_name" KHÔNG đúng —
nguồn `product_import_request_details` có các cột đó NOT NULL và 0/47.743 dòng NULL. (Lỗi tiềm ẩn RIÊNG: `qtyByProduct()`
gộp khoá theo `product_id`, 2 dòng trùng product_id sẽ đè SL — chưa sửa, không phải bug đang phản hồi.)

- [x] Sửa `assertCanCreate()` (WarehouseImportRequestController.php:729) → uỷ quyền quyền LẬP về `$req->canApprove()`
      (1 nguồn chân lý = cổng của nút), bỏ check quyền global + check `cùng công ty` tự thêm (nút không có → chính là
      chỗ lệch); giữ 2 thông điệp cụ thể `is_import_direct` + `Chờ duyệt`. php -l sạch, giữ LF.
- [x] Xác minh data-level (13 vs 57 vs 0) + end-to-end tinker (employee 34: CŨ=false, MỚI=true).
- [x] **CHỐT A (2026-09-22): GIỮ ĐNXK NGUYÊN, không sửa.** User chọn A — ĐNXK đang nhất quán (FE+BE đều HẸP), không ai báo lỗi; không nới quyền. Không đụng code màn ĐNXK.
- [~] **Màn sibling "Đề nghị xuất kho" — ĐẢO KẾT LUẬN, KHÔNG sửa BE-only.** Điều tra lại (2026-09-22)
      chứng minh premise "ĐNXK cũng dính bug thấy-nút-nhưng-bị-chặn" là SAI: nút "Tạo ĐNXK" ở FE gate bằng
      `hasAPermission('Kế toán kho')` = `store.permissions` (nguồn từ `AuthNewController::userProfile` → cũng
      spatie `$employee->roles->pluck('id')` + lọc `role_has_permissions.company_id=current_company_role` → HẸP),
      còn BE `assertCanApprove` dùng global `isCurrentEmployeeHasPermission` (cũng HẸP). ⇒ FE và BE của ĐNXK
      **ĐỀU HẸP = ĐÃ NHẤT QUÁN**, không có ca "thấy nút nhưng bị chặn". (Khác ĐNNK: nút ĐNNK gate bằng cờ BE
      `is_can_approve`=`canApprove()` RỘNG → mới lệch với gate HẸP.) Nếu mù quáng làm BE ĐNXK robust sẽ tạo
      lệch NGƯỢC (BE cho, FE ẩn) → phạm quy ước CLAUDE.md "nút thấy = làm được". Muốn "sửa đồng bộ" thật cho ĐNXK
      = phải MỞ RỘNG cả FE (đổi nút sang cờ BE robust) LẪN BE (thêm trait+canApprove()+cờ resource) — việc này
      NỚI quyền lập ĐNXK cho NV có KTK qua role ERP/khác công ty → là **quyết định nghiệp vụ**, chờ user chốt A/B.
- [x] **Lỗi `qtyByProduct` gộp theo product_id — ĐÃ SỬA + verify.** 1 YCNH có thể có nhiều dòng trùng product_id
      (data thật: parent 11613 product 26723 = 6 dòng; ~969 nhóm trùng toàn hệ). Key theo product_id → gộp mất SL.
      Fix END-TO-END theo `product_import_request_detail_id` (id dòng nguồn):
      - BE `WarehouseImportRequestService`: `qtyByProduct()` → `resolveSelection()` trả 2 map (byDetailId ưu tiên,
        byProduct fallback client cũ); `syncDetails()` khớp theo `$line->id`. php -l sạch, LF.
      - BE `WarehouseImportRequestController::editData()` (line 533): trả thêm `product_import_request_detail_id`.
      - FE `create.vue`: row map giữ `product_import_request_detail_id: p.id` (GET warehouse-import-data trả id dòng
        nguồn) + POST gửi kèm. FE `_id/edit.vue`: row map giữ `p.product_import_request_detail_id` (từ editData) + PUT gửi kèm.
      - Verify: (a) tinker trên data trùng thật — NEW keying tạo 6 dòng SL đúng từng dòng (tổng 670), OLD product_id
        keying gộp còn 1 SL (tổng 630, SAI). (b) Playwright end-to-end (login emp 125 có KTK): form hiện 3 dòng →
        đổi SL dòng 1=9, bỏ chọn dòng 3 → Lưu nháp → POST body có `product_import_request_detail_id` [61612:9, 61613:1]
        → DB `warehouse_import_request_details` tạo đúng 2 dòng link đúng src_detail_id + SL từng dòng. Đã dọn phiếu test
        (DNNK 8540 + details + catalog_histories) và khôi phục YCNH 12206 về status=2.
- [x] Commit + push `gop_db` (fix quyền LẬP + fix qtyByProduct) — hrm-api `6ce777ff6` (controller+service), hrm-client `bbfb8d45f` (create.vue+edit.vue, rebase lên origin/gop_db). Cả 2 repo push OK. ĐNXK để riêng sau khi user chốt.

### Checkpoint — 2026-09-22
Vừa hoàn thành: fix root-cause bug "Lập ĐNNK mất dữ liệu + chặn quyền sai" — `assertCanCreate` uỷ quyền về `canApprove()`
(trait raw-pivot) thay cho global `isCurrentEmployeeHasPermission`. php -l sạch, LF nguyên. Xác minh bằng data thật
+ tinker (employee 34 CŨ=false→MỚI=true).
Đang làm dở: chưa commit (chờ user).
Bước tiếp theo: user chốt (a) có sửa đồng bộ màn ĐNXK không, (b) có sửa qtyByProduct không, (c) commit+push.
Blocked:

### Checkpoint — 2026-09-22 (b) — "xử lý luôn"
Vừa hoàn thành:
- **qtyByProduct fix XONG + verify end-to-end** (BE service resolveSelection/syncDetails theo detail_id + editData trả
  detail_id + FE create/edit giữ&gửi detail_id). Tinker chứng minh trên data trùng thật (670 đúng vs 630 sai) +
  Playwright login emp 125: POST body có detail_id, DB tạo đúng dòng, đã dọn phiếu test + khôi phục YCNH 12206.
- **ĐNXK: đảo kết luận** — FE(store.permissions HẸP) + BE(global helper HẸP) ĐÃ nhất quán, KHÔNG có bug thấy-nút-bị-chặn;
  sửa BE-only sẽ tạo lệch ngược. "Sửa đồng bộ" thật = nới quyền (FE+BE) = quyết định nghiệp vụ → chờ user chốt A/B.
Đang làm dở: — (2 fix ĐNNK đã commit+push: hrm-api `6ce777ff6`, hrm-client `bbfb8d45f`).
Bước tiếp theo: — (user chốt A: giữ ĐNXK nguyên, không sửa. Feature ĐNNK khép lại cho 2 bug Redmine này.)
Blocked:
