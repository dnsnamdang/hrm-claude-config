# Plan — Danh mục dịch vụ sửa chữa và chi phí khác (phân hệ CSKH)

> Nhánh: `gop_db` · Phụ trách: @junfoke · Tạo 2026-08-03
> Design: `.plans/gop-db/customer-care-cost-catalog/design.md`

## Phase 0 — Khảo sát ERP

- [x] Route `admin/accounting/costs` (6 route, **có gate `checkPermission:Quản lý chi phí`**),
      `Accounting\CostsController` (297 dòng), model `Cost`, view `accounting/costs/index.blade.php`
- [x] Bảng `costs`: 587 dòng — `kind_of=2` 524 / `kind_of=1` 57 / `kind_of=0` 6
- [x] Phát hiện **1 màn ERP phục vụ 3 mục menu** qua query `kind_of`
- [x] Phát hiện `discount` nằm ở `company_costs` **theo công ty** (424 dòng, 2 công ty)
- [x] Phát hiện model `Cost` đồng bộ CRM ở `save()` + hook `updating`
- [x] Phát hiện trùng việc với `erp-cost-catalog` (@dnsnamdang)

## Phase 1 — Chốt phạm vi (user chốt 2026-08-03)

- [x] Làm cả 2 `kind_of`, dùng chung 1 component — **nhưng làm `kind_of=2` TRƯỚC**
      (user: "kệ cái danh mục chi phí phải trả đi")
- [x] **Bỏ hẳn phần CRM** — user cho biết đã bỏ xử lý CRM
- [x] Chiết khấu theo **công ty đang chọn trên HRM** (`auth()->user()->current_company_role`)

## Phase 2 — BE `kind_of = 2`

- [x] `Entities/Cost/Cost.php` — `kind_of` 1/2, **`status` 1 = Hoạt động / 0 = Khóa** (khác các
      danh mục khác dùng 1/2), `CANNOT_EDIT_NAMES`, `usedIn()` 2 bảng chứng từ,
      `mustLockInsteadOfDelete()`, `employeeDisplayName()`
- [x] `Entities/Cost/CompanyCost.php` — bảng `company_costs`
- [x] `Services/CostService.php` — `discount` lấy bằng **selectSub** để sort/lọc được trên SQL
      (ERP phải dựng raw subquery + addBinding); `saveDiscount()` upsert/xóa theo công ty hiện tại;
      `destroy()` khóa-hoặc-xóa
- [x] `Http/Requests/Cost/CostRequest.php` — `name` unique trong nhóm `type` null
- [x] `Http/Controllers/V1/CostController.php` — có `guardKindOf()` chặn thao tác lên bản ghi
      `kind_of != 2`
- [x] `Transformers/CostResource` + `app/ExcelExport/CostExport.php` + blade
- [x] 8 route `/v1/customer-care/costs`
- [x] Quyền id **1119/1120**, `type = 24`, group `Danh mục dịch vụ bảo dưỡng`

## Phase 3 — FE

- [x] `pages/customer-care/costs/index.vue` — V2Base list, 5 bộ lọc, Xuất Excel
- [x] `components/modal/customer-care/cost-modal.vue` — thêm/sửa/xem, khóa form khi bản ghi
      thuộc danh sách chặn sửa
- [x] Mở khóa mục menu trong `components/subsystem-menu/customer-care.js`
- [x] Hộp xác nhận **đổi chữ theo kết quả `usage`**: "Xác nhận khóa" khi chi phí đã phát sinh
      chứng từ, "Xác nhận xóa" khi chưa

## Phase 4 — Verify

- [x] 🐛 **Lỗi tự gây, test bắt được**: `prepareForValidation` strip dấu phẩy (copy từ màn Tiền tệ)
      làm tỷ lệ `12,5` lưu thành **125**. 3 trường ở đây đều là PHẦN TRĂM (≤100) nên dấu phẩy là
      dấu THẬP PHÂN → đổi thành `,` → `.`. Verify lại: `12,5` → 12.5
- [x] Danh sách 524 dòng, chiết khấu theo công ty 1 chạy đúng (sort desc ra 15%)
- [x] Lọc: status 0 → 5 / status 1 → 519 / rev=1 → 434 / rev=0 → 90 / keyword "sửa chữa" → 194
- [x] Chặn cứng theo tên: id 36 "Chi phí đi lại" → `is_can_edit=false`, `is_can_delete=false`
- [x] Khóa-thay-vì-xóa: "Phí vận chuyển hàng gấp" → dùng ở Báo giá hãng + Hợp đồng hãng
- [x] CRUD round-trip: tạo (kèm chiết khấu → `company_costs` +1), sửa (bỏ chiết khấu → −1),
      xóa → DB về đúng 524 / 424
- [x] Export xlsx 83KB; 8 route đăng ký đủ; `php -l` toàn bộ + compile 2 file Vue
- [ ] ⏳ Chưa verify bằng mắt trên browser

## Phase 5 — Cắt `erp-cost-catalog` sang dùng luồng mới (user yêu cầu 2026-08-03)

- [x] Gom 2 model về 1: `Modules\Human\Entities\TpCost` giờ `extends Cost`, đánh `@deprecated`,
      giữ nguyên hằng cũ để code trên nhánh `tpe-develop-assign` merge vào vẫn chạy
- [x] Đổi 7 file đang gọi `TpCost` sang `Cost` (ErpCostController, QuotationService,
      QuotationExcelExport, ErpCostStoreRequest, BomListService, DetailBomListResource,
      DetailQuotationResource)
- [x] Bỏ `mysql2` khỏi luồng danh mục chi phí ở 4 file: `ErpCostController`, `BomListService`
      (5 chỗ), `QuotationImportService` (5 chỗ), `QuotationErpSyncService` (3 chỗ)
- [x] 🐛 **Lỗi thật 1** — `ErpCostController::store` mở transaction trên `mysql2` trong khi
      `TpCost` lưu bằng connection mặc định → **lệnh ghi nằm ngoài transaction, không rollback**
- [x] 🐛 **Lỗi thật 2** — `QuotationErpSyncService::findOrCreateCosts` insert **thiếu `kind_of`**
      (cột NOT NULL không default) và ghi nhầm `type = 2` → dòng tạo ra `kind_of = 0`, không hiện
      ở cả 2 màn danh mục. (Đã kiểm: 6 dòng `kind_of=0` trong DB là dữ liệu 2020-2021, không phải
      do hàm này sinh ra)
- [x] 🐛 **Lỗi thật 3** — `QuotationImportService::resolveOrCreateCost` ghi `type = 1` cho dòng
      `kind_of = 2`; màn danh mục kiểm trùng tên **theo nhóm `type`** nên dòng này lọt qua kiểm
      trùng → sinh 2 bản ghi cùng tên
- [x] Bỏ 4 hàm map HRM user → ERP employee (đã gộp chung bảng `employees`)
- [x] Verify: 519 dòng kind_of=2 · `resolveCostByName` ra id 35 · currency VNĐ id 1 ·
      employee id 13 · preload master data 38.278/1.126/103/142 · `php -l` sạch
- [x] **Ghi chú đầy đủ cho @dnsnamdang** ở cuối `.plans/erp-cost-catalog/plan.md`
      (mục "⚠️ SỬA TỪ NGOÀI — 2026-08-03")

## Phase — Tài liệu bàn giao (2026-08-12)

- [x] Nghiên cứu 2 file mẫu của team: `D:\CompanyProject\Document\TC mẫu phần bomlist.xlsx`
      (form testcase) và `D:\CompanyProject\Document\HDSD_Bomlist.docx` (form HDSD)
- [x] Chụp 9 ảnh thật trên cổng dev `hrm-crm.eteksofts.com` → `hdsd_costs_shots/`
      (menu, danh sách, bộ lọc, tạo mới, lỗi validate, sửa, xem, xác nhận xóa, xác nhận khóa)
- [x] `testcase.xlsx` — 139 TC (P0 56%), 10 nhóm: Phân quyền + I…IX. Bám form file mẫu:
      9 mục mô tả, TEST SUMMARY 2 khối DNS/TP, header 17 cột, dropdown check 3 lần cho mỗi khối
- [x] **Viết lại toàn bộ nội dung TC bằng ngôn ngữ nghiệp vụ** (user phản hồi 2026-08-12: tài liệu
      cho QA chứ không cho dev) — bỏ hết tên bảng/cột, id quyền, route, mã HTTP; generator có bộ
      kiểm tra regex chặn tái phạm. Xem [[feedback_tailieu_khong_dung_thuat_ngu_code]]
- [x] Sửa 2 lỗi HDSD: mục lục + danh mục hình ảnh còn nội dung template BOM (`updateFields` chỉ là
      lời mời Word, phải gọi Word COM cập nhật thật) và dòng tiêu đề trên bìa chưa được thay
- [x] `HDSD_Danh muc dich vu sua chua va chi phi khac.docx` — dựng từ khung `HDSD_Bomlist.docx`
      (giữ bìa + mục lục + danh mục hình ảnh + styles), 9 phần, 8 bảng, 9 ảnh thật
- Generator (scratchpad, chạy lại được): `gen_tc_costs.py`, `gen_hdsd_costs.py` — dùng
  `openpyxl` / `python-docx`; HDSD strip body từ heading "TỔNG QUAN", clone proto Caption có SEQ
  field, purge media mồ côi, bật `updateFields`
## Phase 6 — Sửa lỗi port: bỏ "Tên tiếng Anh" khỏi màn kind_of=2 (2026-08-04)

> **Bug:** Bản port bê nhầm trường `en_name` ("Tên tiếng Anh") vào màn `customer-care/costs`.
> ERP gốc (`accounting/costs/index.blade.php`) chỉ hiện `en_name` khi `kind_of == 1`
> (`<th ng-if="editing.kind_of == 1">`, cột datatable `visible: (paramUrl == 1)`, field modal
> `ng-if="editing.kind_of == 1"`). Màn này là `kind_of = 2` nên **không được có** trường đó.
> Cột `en_name` trong bảng `costs` GIỮ NGUYÊN (dùng chung cho kind_of=1 ở module Assign) — chỉ gỡ
> khỏi màn CSKH, KHÔNG đụng DB, KHÔNG đụng module Assign.

- [x] FE `pages/customer-care/costs/index.vue` — bỏ ô lọc "Tên tiếng Anh", bỏ cụm trong placeholder
      tìm nhanh, bỏ dòng phụ "Tên tiếng Anh" ở cột Tên, bỏ `en_name` khỏi `initialStateForm`
- [x] FE `components/modal/customer-care/cost-modal.vue` — bỏ input, bỏ khỏi `emptyData` + `payload`
- [x] BE `Http/Requests/Cost/CostRequest.php` — bỏ khỏi `prepareForValidation`/`rules`/`attributes`/`messages`
- [x] BE `Transformers/CostResource/CostResource.php` — bỏ field `en_name`
- [x] BE `Services/CostService.php` — bỏ khỏi keyword-search, filter loop, `$allowedSortFields`, `payload()`
- [x] BE `resources/views/exports/costs.blade.php` — bỏ cột "Tên tiếng Anh" + sửa `colspan` (9→8, chân ký 8→7)
- [x] Sửa `design.md`: bỏ `en_name` khỏi danh sách bộ lọc, ghi chú `en_name` chỉ thuộc kind_of=1
- [x] `Cost.php` (`$fillable`) GIỮ NGUYÊN `en_name` — base model dùng chung (Assign `TpCost extends Cost`, kind_of=1)
- [x] `php -l` 3 file BE sạch; grep xác nhận không còn `en_name` trong phạm vi CSKH (FE + BE)

### Đổi tên cột cho khớp ERP kind_of=2 (user chốt 2026-08-04, kèm ảnh đối chiếu ERP/HRM)

Đối chiếu source ERP `accounting/costs/index.blade.php`. User chọn:
- [x] **Đổi tên 3 cột** (cả list + modal + export) — giữ nguyên cơ chế chiết khấu theo công ty:
  - `Chiết khấu` → **`ĐM giảm giá`** (Định mức giảm giá) — list + export; modal label `ĐM giảm giá (%)`
  - `Tỷ lệ giá vốn` → **`% Tính giá vốn`**
  - `VAT` → **`% VAT`**
  - Sửa cả ghi chú modal: "Chiết khấu áp riêng…" → "ĐM giảm giá áp riêng…"
- [x] **Giữ cột `Phân loại`** (revenue_calculation) — user muốn giữ dù ERP kind_of=2 không có (ERP chỉ có cột "Kiểu" trùng nhau mọi dòng, vô nghĩa)
- [x] **Giữ nguyên bộ lọc** (`name`, `Phân loại`, `status`, `Người cập nhật`) — user không cắt theo ERP

### 🐛 Bug dropdown không chọn được option `id: 0` (user báo 2026-08-04, user chốt sửa gốc)

- Triệu chứng: bộ lọc "Phân loại"/"Trạng thái" hiện đủ option nhưng không click chọn được
  "Chi phí khác" / "Khóa" (đều `id: 0`).
- Gốc: [`V2BaseSelect.vue`](../../../hrm-client/components/V2BaseSelect.vue) `select2Options` map
  `id: opt.id || opt.value || opt.code` → `0 || ... = undefined` → Select2 bỏ giá trị.
- [x] Sửa `V2BaseSelect` dùng kiểm tra `!== undefined && !== null` (đồng bộ `V2BaseSelectInModal`
  vốn đã đúng) — component dùng chung, fix mọi màn có option `id=0`
- [x] Sửa luôn `V2BaseSelectRemote` dòng text fallback (`String(o.id || ...)` → dùng `id` đã tính)
- Ghi chú: `V2BaseSelectInModal` KHÔNG dính lỗi (đã xử lý đúng từ trước).

### Checkpoint — 2026-08-04
Vừa hoàn thành: (1) Gỡ sạch "Tên tiếng Anh" (`en_name`) khỏi màn kind_of=2 — FE + BE. (2) Đổi tên 3 cột theo ERP (ĐM giảm giá / % Tính giá vốn / % VAT) ở list + modal + export; giữ cột Phân loại + giữ bộ lọc. (3) Fix bug falsy-zero ở `V2BaseSelect`/`V2BaseSelectRemote` (option `id=0` không chọn được). Không đụng DB, không đụng module Assign (kind_of=1).
Đang làm dở: (không)
Bước tiếp theo: User verify browser (localhost:3000 `/customer-care/costs`): chọn được "Chi phí khác"/"Khóa" trong bộ lọc; tiêu đề cột = ĐM giảm giá / % Tính giá vốn / % VAT; không còn tiếng Anh; modal nhãn khớp; Xuất Excel 8 cột đúng tên.
Blocked:

## Việc còn lại

- [ ] `kind_of = 1` (Chi phí phải trả / Chi phí bán hàng) — user tạm gác
- [ ] Xác nhận có bỏ mục trùng "Danh mục chi phí bán hàng" khỏi menu Bán hàng không
- [ ] ⚠️ **Còn nhiều chỗ dùng `mysql2` ngoài phạm vi danh mục chi phí** — `AssignBusinessController`
      (15 chỗ), `QuotationService` (recipe_products, ngày giao hàng), `QuotationImportService`
      (`products`), `QuotationController`, `BomListController`, `ProductProjectController`,
      `TpProductUnitPrice`, `DecisionRewardService`, `BonusDistributionService`, các command
      `CheckEmployee*`. Đang đọc DB ERP CŨ trên nhánh `gop_db` — cần rà riêng
