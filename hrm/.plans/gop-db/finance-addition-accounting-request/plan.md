# Plan — Phiếu yêu cầu hạch toán bổ sung (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo, code thẳng trên nhánh này — không tách nhánh riêng)
> Design: `.plans/gop-db/finance-addition-accounting-request/design.md`
> Spec: `docs/superpowers/specs/gop-db/2026-08-25-finance-addition-accounting-request-design.md`
> **Trạng thái: HOÀN THÀNH — user xác nhận xong (2026-08-26)**

**Mục tiêu:** port màn ERP `income_expenditure/addition_accounting_requests` sang HRM phân hệ Tài
chính, route `/finance/addition-accounting-requests` — 6 loại tạo mới + loại 7 chỉ xem/in, dừng ở
trạng thái *Chờ duyệt*.

**Kiến trúc:** dùng chung 5 bảng ERP (0 migration), khung BE copy từ màn Phiếu yêu cầu điều chỉnh
công nợ (`BillAdjustDeptRequest*`), FE bám khuôn `pages/assign/customers/index.vue` +
`CustomerForm.vue`, lịch sử dùng bảng chung `catalog_histories`.

**Tech:** PHP 7.4 / Laravel 8 · `nwidart/laravel-modules` · `spatie/laravel-permission` ·
`maatwebsite/excel` · Nuxt 2 / Vue 2 · Bootstrap-Vue.

## Ràng buộc xuyên suốt

- Nhánh `gop_db` cả 2 repo. **Không** dùng `mysql2` / `DB_CONNECTION_SECOND`.
- **0 migration** — không thêm/sửa bảng nào.
- Quyền mới id **1177–1180** guard `api`, tên trùng nguyên văn ERP. **Không** chạy
  `Modules/Timesheet/.../PermissionsTableSeeder` toàn bộ (khai trùng id 1117/1118 → nổ khoá).
- Cờ quyền FE mặc định `false`, không hard-code `= true`.
- Mọi FormRequest **rethrow `ValidationException`**, FE hiện lỗi inline theo `touched`.
- Select trong modal dùng `V2BaseSelectInModal`.
- Không commit / push khi user chưa yêu cầu.
- Verify BE bằng script HTTP qua kernel (`php artisan route:list` **chết sẵn** trên repo này);
  verify FE bằng compile template/script, **user tự bấm trình duyệt** — không tự chạy Playwright.

---

## Phase 0 — Brainstorming & chốt scope ✅ XONG 2026-08-25

- [x] Khảo sát màn ERP: model 1.668 dòng · controller 486 dòng · 16 route · 9 file Blade
- [x] Đo số liệu thật trên `gop_db` (1.937 phiếu, phân bố loại/trạng thái/morph type, 2 bảng nguồn)
- [x] Phát hiện loại 7 **không tạo được kể cả bên ERP** (do màn Quyết toán HĐ bán sinh)
- [x] Phát hiện loại 1/3/5 có **0 phiếu**; 2 màn nguồn của loại 1 và 5 chưa port sang HRM
- [x] Chốt 4 câu hỏi lớn với user + 2 điểm phụ (menu dòng 360 để trống, file đính kèm giữ cột ERP)
- [x] Viết spec `docs/superpowers/specs/gop-db/2026-08-25-finance-addition-accounting-request-design.md`
- [x] Viết `design.md` tóm tắt + `plan.md`, cập nhật `STATUS.md`
- [x] User duyệt design + spec

---

## Phase 1 — BE nền: Entity, quyền, danh sách ✅ XONG 2026-08-25

**File tạo:**
- `Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequest.php`
- `Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequestDetail.php`
- `Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequestDepartment.php`
- `Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequestEmployee.php`
- `Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequestBusinessCoordination.php`
- `Modules/Finance/Services/AdditionAccountingRequestService.php`
- `Modules/Finance/Http/Controllers/V1/AdditionAccountingRequestController.php`
- `Modules/Finance/Transformers/AdditionAccountingRequestResource/AdditionAccountingRequestListResource.php`
- `Modules/Finance/Database/Seeders/AdditionAccountingRequestPermissionSeeder.php`

**File sửa:** `Modules/Finance/Routes/api.php`

- [x] Entity chính: `$table`, `$fillable` (theo §3.1 spec), hằng `TYPES` (7 loại), `STATUSES` 4 trạng
      thái với **màu chuẩn HRM** (Đang tạo `secondary` · Chờ duyệt/Đang duyệt `warning` · Đã duyệt
      `success`), `OBJECT_TYPES`, `SORTABLE_COLUMNS` (`code`, `money`, `created_at`, `send_date`,
      `approver_time`, `updated_at`), `ALLOWED_TRANSITIONS` (`1→2`, `2→1`)
- [x] `use ChecksEmployeePermission` — **không** dùng `$user->can()` (guard + `model_type` mismatch)
- [x] **Không** port hook `boot()` của ERP (gán tổ chức trong `created` rồi `save()` lần 2); gán
      thẳng lúc tạo ở WriteService, thiếu thì ghi `0` vì 3 cột NOT NULL không có default
- [x] 4 Entity con + quan hệ: `details` (`parent_id`), `additionDepartments` (`parent_id`) →
      `additionEmployees` (`parent_id`), `coordination` (hasOne)
- [x] `contractable()` = `morphTo()`. **`objectable` KHÔNG dùng morphTo** — resolve thủ công theo
      chuỗi (`App\Model\Sale\Customer` → `TpCustomer`, `App\Model\Sale\Supplier` →
      `Modules\Finance\Entities\Supplier`), xem §3.3 spec
- [x] `searchByFilter()` — 2 chế độ `all` / `pending`, phạm vi 5 nhánh quyền (§5.3, §5.4 spec),
      nhánh *công ty* có vế `type = 7` theo `support_department_id`; chế độ `pending` **luôn**
      `status = 2` (vá lỗi ERP #4)
- [x] Lọc: `code`, `firm_warranty_confirm_code` (vá lỗi ERP #5), `type`, `object_id`, `status`,
      `note`, `approver_id`, `created_by`, `start_date`/`end_date` bằng `whereDate` (vá lỗi #6),
      `company_id`/`department_id`/`part_id`
- [x] `canEdit()` / `canDelete()` = `status = 1` **AND `created_by = auth()->id()`** (vá lỗi #1);
      `canReject()` = `status = 2` + quyền `Kế toán thanh toán`;
      `canCreateAccountingBill()` = 2 nhánh theo loại (§5.5 spec)
- [x] Service + Controller: `index()`, `pending()`; ListResource 13 cột + 4 cờ `is_can_*`
- [x] Cột **KH/NCC** theo thứ tự ưu tiên ERP (supplier → customer → employee → đối tượng dòng đầu);
      cột **Diễn giải** = note dòng đầu, rỗng thì note phiếu
- [x] Permission seeder id 1177–1180 (`updateOrInsert`, idempotent), gán role Super admin (18) +
      role đang giữ quyền ERP cùng tên; thêm 4 quyền vào `PermissionsTableSeeder` (chỉ thêm entry)
- [x] Chạy seeder thật trên `gop_db`

**Verify — script `scratchpad/verify_aar_phase1.php`, chạy HTTP thật qua kernel, 24 ca/tài khoản.**
Mỗi tài khoản chạy 1 TIẾN TRÌNH RIÊNG (guard auth memoize theo tiến trình). Phạm vi quyền dựng lại
bằng SQL thuần, không gọi lại code Entity.

| Tài khoản | Quyền | API `all` | SQL | API `pending` | SQL | Kết quả |
| --- | --- | --- | --- | --- | --- | --- |
| emp 13 | Super admin | 1.862 | 1.862 | 42 | 42 | 24/24 ✅ |
| emp 147 | Xem theo công ty + Kế toán TT | 1.766 | 1.766 | 42 | 42 | 24/24 ✅ |
| emp 237 | Xem theo phòng ban | 31 | 31 | 0 | 0 | 24/24 ✅ |
| emp 110 | Xem theo bộ phận (không quản bộ phận nào) | 0 | 0 | 0 | 0 | 21/21 ✅ (bỏ 2 ca sort vì 0 dòng) |
| emp 27 | Không quyền nào | 56 | 56 | 1 | 1 | 24/24 ✅ |

`all` của super admin là **1.862** chứ không phải 1.937 vì 75 phiếu nháp của người khác bị ẩn — đúng
luật ERP. Đã kiểm thêm: 8 ô lọc đều cắt đúng số dòng · `sort_by` lạ (`' OR 1=1`) rơi về mặc định ·
màn *Chờ duyệt* 0 dòng khác trạng thái 2 (vá lỗi ERP #4) · `is_can_edit` không bật cho phiếu người
khác (vá lỗ hổng ERP #1) · loại 7 không bao giờ sửa/xoá được · 3 màu badge đúng chuẩn SRS.

4 quyền **1177–1180** đã seed thật trên `gop_db`, chạy lại 2 lần không lỗi (idempotent), tự kế thừa
role đang giữ quyền ERP guard `web`: 3 / 7 / 3 / 2 role.

---

## Phase 2 — BE ghi: tạo / sửa / xoá / chuyển trạng thái ✅ XONG 2026-08-25

**File tạo:**
- `Modules/Finance/Http/Requests/AdditionAccountingRequest/AdditionAccountingRequestStoreRequest.php`
- `Modules/Finance/Services/AdditionAccountingAttachmentService.php` *(kéo lên sớm từ Phase 3 —
  FormRequest cần hằng `URL_PREFIX` để chặn URL lạ)*
- `.../AdditionAccountingRequestUpdateRequest.php`
- `.../AdditionAccountingRequestChangeStatusRequest.php`
- `Modules/Finance/Services/AdditionAccountingRequestWriteService.php`
- `Modules/Finance/Services/AdditionAccountingRequestNotifyService.php`

**File sửa:** Controller, `api.php`, `CatalogHistoryService::TABLES`

- [x] FormRequest theo §7 spec — rule chia nhánh theo `type`; bổ sung
      `employee_id required_if:object_type,3` (vá lỗi ERP #9); `attachments` bắt buộc ≥1 khi tạo,
      nullable khi sửa nếu phiếu đã có file
- [x] `store()` / `update()` **chỉ nhận `status` 1 hoặc 2** (vá lỗi #3), mọi giá trị khác → 422
- [x] `syncDetails()` — xoá rồi ghi lại dòng chi tiết, gán `objectable_type` = **chuỗi class ERP**
      thủ công, tính lại `money` = tổng dòng (chỉ loại 2/6)
- [x] Sinh mã `PYCHTBS-` + id đệm 6 số, giữ nguyên cách ERP (sinh từ `id` nên không trùng —
      **không** thêm lock, khác màn Đề nghị thu tiền)
- [x] `destroy()` qua **`DELETE /{id}`**, gate `canDelete()`, trả 403 nếu không đủ điều kiện; xoá
      kèm dòng chi tiết (vá lỗi #2)
- [x] `POST /{id}/change-status` — bảng `ALLOWED_TRANSITIONS`, gửi duyệt ghi `send_date`, từ chối
      bắt buộc `comment` + ghi `approver_id` và `approver_time` (vá lỗi #8)
- [x] NotifyService prefix `[HTBS]`, 2 sự kiện (§10 spec), deep-link
      `/finance/addition-accounting-requests/{id}` — **không** trỏ route ERP
- [x] Ghi lịch sử qua trait `LogsCatalogHistory`; khai `addition_accounting_requests` vào
      `CatalogHistoryService::TABLES`; lý do từ chối vào `note` của log
- [x] Dùng khoá ảo `details_rows` cho lịch sử bảng chi tiết (khuôn màn Finance đã có)
- [x] `GET /{id}/histories` — đọc lịch sử cho khối/popup ở màn chi tiết, lọc theo 3 nhóm hoạt động
      chuẩn (`create` / `update` / `status`) như feature `history-action-groups` đã chuẩn hoá

**Verify — script `scratchpad/verify_aar_phase2.php`, 4 lượt / 4 tiến trình riêng, tổng 81 ca pass.**

| Lượt | Tài khoản | Ca | Kết quả |
| --- | --- | --- | --- |
| `create` | emp 27 (không quyền) | 67 | ✅ |
| `cross` | emp 237 (người khác) | 4 | ✅ (1 ca `show` hoãn sang Phase 4) |
| `reject` | emp 147 (Kế toán thanh toán) | 7 | ✅ |
| `cleanup` | emp 27 | 3 | ✅ |

**Đã kiểm:** tạo nháp đủ **cả 6 loại** — mã đúng khuôn `PYCHTBS-\d{6}`, `created_by` đúng người,
3 cột tổ chức không null, `money` = tổng dòng (loại 2/6) hoặc số nhập (loại còn lại),
`objectable_type` ghi đúng **chuỗi class ERP** · sửa phiếu nháp cập nhật tiền và **không nhân đôi
dòng** · vòng đời `1 → 2 → 1` (kế toán từ chối) chạy đủ · lịch sử sinh đúng 3 loại log (`create` /
`update` / `change_status`), log từ chối **có kèm lý do**.

**9 ca xấu bị chặn 422:** nhảy cóc `status = 3` (vá lỗi ERP #3) · tạo loại 7 · gửi duyệt `details`
rỗng · tiền = 0 · loại 4/Nhân viên thiếu `employee_id` (vá lỗi ERP #9) · loại 1 thiếu phiếu xác nhận
BH · URL đính kèm ngoài S3 của màn · gửi duyệt không file · 2 dòng trùng đối tượng + hợp đồng.
Thêm 4 ca chặn theo trạng thái: gửi duyệt lại phiếu đang chờ duyệt · người lập tự từ chối phiếu
mình · sửa/xoá phiếu đang chờ duyệt (403) · gửi duyệt phiếu nháp trống.

**Ca chéo tài khoản (lỗ hổng ERP #1 + #2 đã vá):** emp 237 SỬA / XOÁ phiếu nháp của emp 27 → **403
cả hai**, gửi duyệt → 422, phiếu không đổi gì. Bên ERP cả 3 thao tác này đều lọt.

**Từ chối lưu đủ 3 thứ ERP bỏ sót:** `comment` + `approver_id` + `approver_time`.

**Dọn dữ liệu:** tổng số phiếu trở lại đúng **1.937** như trước khi test, 0 dòng chi tiết và 0 log sót.
## Phase 3 — BE tra cứu & file đính kèm ✅ XONG 2026-08-25

**File tạo:**
- `Modules/Finance/Services/AdditionAccountingLookupService.php`
- `Modules/Finance/Services/AdditionAccountingAttachmentService.php`

**File sửa:** Controller, `api.php`

- [x] `GET /meta` — danh mục loại yêu cầu, trạng thái, đối tượng, loại tiền
- [x] `GET /warranty-confirms` (`status = 3`) + `GET /warranty-confirms/{id}/accounting-data`
      (trả NCC + tổng tiền, mirror `FirmWarrantyConfirmController@getDataAdditionAccountingRequest`)
- [x] `GET /discrepancy-imports` (`status = 5`, `accounting = 1`) +
      `GET /discrepancy-imports/{id}/accounting-data` (trả **danh sách** NCC + số tiền + loại tiền;
      1 NCC → FE tự điền, nhiều NCC → FE hiện select)
- [x] `GET /search-employees` — popup chọn nhân viên cho loại 4 `object_type = 3`
- [x] **Không khai lại** `search-customers` / `search-suppliers` / `search-contracts` /
      `search-buy-contracts` — dùng endpoint sẵn có của màn Đề nghị thu tiền
- [x] AttachmentService copy `BillPaymentAttachmentService`: thư mục S3
      **`addiiton_accounting_requests`** (giữ nguyên lỗi chính tả ERP), `parse()` tách bằng dấu
      phẩy rồi `trim`, file mới **append**
- [x] `POST /upload-files` trả URL S3; `DELETE /{id}/files` xoá object S3 **thật** bằng
      `CmcS3Helper::deleteFile()` (ERP gọi `unlink(public_path())` là code chết) + gate `canEdit()`
- [x] FormRequest kiểm `attachment_urls.*` bằng `starts_with` prefix S3

**Verify — script `scratchpad/verify_aar_phase3.php`, 24/24 ca pass** (emp 13).
Mỗi endpoint so số bản ghi với `COUNT(*)` SQL viết tay:

- `/warranty-confirms` → **49/56** phiếu (lọc đúng `status = 3`), lọc theo mã cắt còn 1
- `/warranty-confirms/{id}/accounting-data` → đúng mã + NCC + tổng tiền; phiếu **chưa duyệt → 404**
- `/discrepancy-imports` → **0** phiếu, khớp SQL
- `/search-employees` → 1.085 nhân viên, phân trang đúng, tìm theo mã/tên khớp SQL
- `/currencies` → 11 loại tiền đang hoạt động, có kèm `exchange_rate`
- `/meta` → 6 loại tạo được · 7 loại để lọc · 3 loại đối tượng
- `AdditionAccountingAttachmentService`: thư mục S3 giữ đúng lỗi chính tả ERP
  (`addiiton_accounting_requests`), `parse()` tách được cả chuỗi nối `,` lẫn `, `

**Vá thêm 1 lỗi ERP (#10, phát sinh khi port):** `FirmWarrantyConfirmController@getDataAdditionAccountingRequest`
(:599-608) viết `foreach ($object->costs as $cost) { $total = $cost->amount_confirm; }` — dấu `=`
thay vì `+=` nên chỉ lấy **dòng chi phí CUỐI CÙNG**; phiếu nhiều dòng chi phí sẽ điền thiếu tiền
vào form. HRM dùng `SUM()`.

⚠️ **2 khoảng trống DỮ LIỆU (không phải lỗi code) — cần seeder ở Phase 9:**
1. Cả **3 phiếu xử lý hàng thiếu** trên DB đều để `accounting = NULL`, trong khi ERP yêu cầu
   `accounting = 1` (*Chờ hạch toán bổ sung*) mới chọn được ⇒ popup của **loại 5 hiện đang rỗng**.
2. Không có phiếu xác nhận bảo hành **đã duyệt** nào có dòng chi phí > 0 (4.000.000 đ trên bảng
   thuộc phiếu ở trạng thái khác) ⇒ ca "tổng tiền" mới chỉ chứng minh khớp SQL, chưa chứng minh
   được khác biệt với cách tính của ERP.
## Phase 4 — BE in & xuất Excel ✅ XONG 2026-08-25

**File tạo:**
- `Modules/Finance/Services/AdditionAccountingRequestPrintService.php` *(gộp luôn vai trò
  PrintResource — bản in và Excel dùng CHUNG 1 mảng nên tách 2 lớp chỉ thêm file không thêm gì)*
- `Modules/Finance/Transformers/AdditionAccountingRequestResource/AdditionAccountingRequestDetailResource.php`
- `.../AdditionAccountingRequestPrintResource.php`
- `Modules/Finance/Exports/AdditionAccountingRequestExport.php`
- `Modules/Finance/Exports/AdditionAccountingRequestListExport.php`
- blade `Modules/Finance/Resources/views/exports/addition-accounting-request.blade.php` (+ list)

- [x] `GET /{id}` — DetailResource: thông tin chung + `details` (kèm `objectable` resolve thủ công,
      `contractable` qua morph, link chi tiết hợp đồng cho loại 2/6) + `attachments[]` + 4 cờ `is_can_*`
- [x] Nhánh **loại 7**: trả thêm `coordination` (revenue, cost, monthly_bonus, quarterly_bonus,
      risk_fund_amount) + `departments[] → employees[]` + `imp_department`, `contract_code`
- [x] `GET /{id}/print-data` — bố cục mẫu ERP id 463; **letterhead lấy `companies.header` theo
      `company_id` GHI TRÊN CHỨNG TỪ**, khuôn copy `BillIncomePrintService::headerUrl()`
      (đọc `.claude/skills/print-page/SKILL.md` §4b trước khi viết)
- [x] Nội dung in theo loại: 2/6 bảng chi tiết · 1/3/4/5 các dòng `ROW_*` · 7 bảng phối hợp.
      **Vá lỗi ERP #7a** (loại 4 in đúng đối tượng theo `object_type`) và **#7b** (loại 5 in
      `inventory_discrepancy_handling_import_code`)
- [x] `GET /{id}/export` — Excel 1 phiếu; `GET /export-list` — Excel danh sách
- [x] Đọc `.claude/skills/export-excel/SKILL.md` trước: logo công ty, độ rộng cột, số tiền là
      **kiểu số** (không phải text), có dấu phân cách nghìn, SUM cộng được

**Verify — script `scratchpad/verify_aar_phase4.php`, 67/67 ca pass** (emp 13).
Dựng file Excel **thật** rồi đọc lại bằng PhpSpreadsheet (skill export-excel §7).

**Chi tiết + bản in** — chạy cho cả 4 loại đang có dữ liệu thật (2 · 4 · 6 · 7):
số dòng chi tiết khớp DB · `layout` đúng theo loại (`details` / `rows` / `coordination`) ·
loại 7 có đủ 5 chỉ tiêu + số phòng hỗ trợ khớp DB và **không cho sửa/xoá** ·
letterhead theo **công ty ghi trên chứng từ** (2 phiếu khác công ty ra 2 letterhead khác nhau —
đúng cái bẫy skill print-page §4b cảnh báo).

**Excel 1 phiếu** (4 file, mỗi loại 1 file): **0 ô số bị lưu dạng chuỗi** (quét toàn sheet tìm ô
kiểu `s` mà nội dung thuần số — đây là ô Excel cảnh báo *"formatted as text"*) · có ô gắn
`#,##0` · bề rộng cột do `WithColumnWidths` đặt (A=32 · B=28 · C=20 · D=40) ·
**logo nhúng thật: `drawings=1`** ở cả 4 file.

**Excel danh sách**: 15 trường xuất được · thứ tự cột theo **đúng thứ tự user tick**
(tick `code,type_name,money,status_name` → ra đúng 4 cột đó, không có cột thứ 5) ·
số dòng khớp bộ lọc đang áp · ô tiền là kiểu **`n`** với định dạng `#,##0` · `drawings=1`.

**Ca hoãn từ Phase 2 đã kiểm lại:** emp 237 mở phiếu nháp #28 của emp 87 → **403**
(ERP không gate `show` nên ai biết id đều mở được phiếu công ty khác).

**Gộp file so với plan ban đầu:** không tạo `AdditionAccountingRequestPrintResource` riêng — bản in
và Excel dùng chung đúng 1 mảng do `AdditionAccountingRequestPrintService::build()` trả về, tách
thêm 1 lớp chỉ để bọc lại thì thừa.
## Phase 5 — FE màn danh sách ✅ CODE XONG 2026-08-25 (chờ user bấm trình duyệt)

**File tạo:** `hrm-client/pages/finance/addition-accounting-requests/index.vue`
**File sửa:** `hrm-client/components/subsystem-menu/finance.js` (dòng 58 và 464)

- [x] 4 mixin: `PageTitleMixin`, `CheckPermission`, `filterStateMixin`, `columnCustomizationMixin`;
      `localStorageKey` = `columnScreenKey` = `finance_addition_accounting_requests` (grep kiểm trùng)
- [x] 13 cột theo §8.1 spec + 2 cột ẩn mặc định (Người/Ngày cập nhật); STT/Số phiếu/Hành động không
      tắt được; Số phiếu là `<nuxt-link>` thật
- [x] Sort mặc định `created_at DESC`; căn lề: STT/badge/hành động giữa · tiền phải · chữ và ngày trái
- [x] Trạng thái dùng `V2BaseBadge` + `utils/statusBadgeVariant.js`, text từ BE — **không** tự viết
      `statusPillClass()`
- [x] Bộ lọc **`V2BaseSmartFilterPanel` + schema `filterFields`** (10 trường → có popup Cài đặt bộ
      lọc); khối tổ chức khai đủ 4 khoá `company_id`/`department_id`/`part_id`/`employee_id` trong
      `initialStateForm`
- [x] Toolbar: Thêm mới → Xuất Excel (mở `ExportFieldsModal` trước, **không** tải thẳng) → Cấu hình cột
- [x] Cột hành động `V2BaseRowActions` — handler `switch (action)` vì component emit **chuỗi key**;
      nút không dùng được thì **ẩn** bằng `visible`, không `disabled`
- [x] 2 chế độ qua `?mode=pending`, có `watch` trên `$route.fullPath`
- [x] Nút *Lập phiếu kế toán* mở tab mới sang ERP qua `utils/erp-link.js`; `ERP_URL` trống → báo lỗi
      rõ ràng, không mở tab trắng
- [x] Nối 2 mục menu (dòng 58 → danh sách, dòng 464 → `?mode=pending`); **dòng 360 để trống**

**Verify tự động (đã chạy):**
- Compile sạch: template qua `vue-template-compiler`, script qua `@babel/parser`; `finance.js` parse sạch
- **6 lệnh grep tự kiểm của skill `erp-to-hrm-screen` đều rỗng** (`status-pill` · `interactable:` ·
  `action.key ===` · `V2BaseFilterPanel` · `advanced-filters`); riêng grep `thành công'` ra 3 dòng
  nhưng **trùng nguyên văn** 3 câu toast của màn Yêu cầu điều chỉnh công nợ đang chạy — không phải câu tự chế
- Hình dạng response khớp cái FE đọc: `data` / `total` / `lastPage` / `currentPage` / `perPage` +
  `meta` chứa `types_filter`, `statuses`, 4 cờ `can_view_*`, `is_accountant`, `is_support_accountant`
- Mỗi dòng lưới có đủ 5 cờ `is_can_*` cho cột Hành động

**Sửa 1 lỗi khi ghép FE↔BE:** `meta()` ban đầu trả danh mục ở cấp 1, trong khi khuôn lưới của phân
hệ đọc `response.meta` → đã bọc lại trong khoá `meta` và bổ sung 6 cờ quyền + `creator` (khuôn
`BillAdjustDeptRequestService::meta()`).

⚠️ **CHƯA mở trình duyệt** — theo quy ước, phần bấm tay do user làm:
từng ô lọc (so param trên tab Network) · từng nút trong cột Hành động kể cả trong menu "…" ·
vào chi tiết rồi quay lại xem bộ lọc còn nguyên · popup Cấu hình cột và Cài đặt bộ lọc.
## Phase 6 — FE form thêm/sửa + 3 popup mới ✅ CODE XONG 2026-08-25 (chờ user bấm trình duyệt)

**File tạo:**
- `pages/finance/addition-accounting-requests/create.vue`
- `pages/finance/addition-accounting-requests/_id/edit.vue`
- `pages/finance/addition-accounting-requests/components/AdditionAccountingRequestForm.vue`
- `.../components/AdditionDetailTable.vue`
- `.../components/RecordSearchModal.vue` *(GỘP 3 popup mới thành 1 component tra cứu — 3 cái chỉ
  khác tiêu đề / endpoint / danh sách cột, nhân bản 3 file y hệt là 3 chỗ phải sửa khi đổi UI)*
- `.../components/AttachmentSection.vue` *(bản sao của màn Đề nghị thanh toán, đổi 3 đường dẫn API)*
- `.../_id/edit.vue` · `create.vue`
- *(`RejectModal` chuyển sang Phase 7 — nút Từ chối nằm ở màn chi tiết, không nằm ở form)*

- [x] Form đổi trường theo `type` (§4 spec); đổi loại → xoá sạch trường phụ thuộc loại
- [x] Loại 2/6: `AdditionDetailTable` — thêm/xoá dòng, chọn đối tượng, chọn hợp đồng, tiền, ghi chú;
      cuộn dọc + dính dòng tiêu đề; chưa chọn đối tượng mà bấm chọn hợp đồng → cảnh báo
- [x] Dùng lại `ChooseErpCustomerModal` · `SupplierSearchModal` · `ContractSearchModal` — **không**
      viết popup KH/NCC/hợp đồng mới
- [x] 3 popup mới theo §8.3 spec; ô hiển thị giá trị đã chọn là `V2BaseInput` readonly + nút kính lúp
- [x] Loại 5: 1 NCC → tự điền; nhiều NCC → hiện select
- [x] File đính kèm: upload ngay khi chọn → nhận URL → xem trước được; lưu phiếu chỉ gửi
      `attachment_urls[]`
- [x] `unsavedChangesMixin` + `markFormSaved()` sau khi lưu; chưa đổi gì mà bấm Hủy → **không** hiện confirm
- [x] 2 nút lưu trong `V2Footer`: **Lưu** (status 1) và **Lưu và gửi duyệt** (status 2)
- [x] Lỗi validate hiện ngay dưới ô nhập dạng `Tên trường – Nội dung lỗi`; còn lỗi thì **không** gọi
      API lưu; nhiều lỗi thì con trỏ nhảy về ô đầu tiên
- [x] Datepicker (nếu có) gửi **ISO**, không gửi `dd/mm/yyyy` (luật `date` của Laravel hiểu `m/d/Y`)

**Verify tự động (đã chạy):** 6 file compile sạch (template + script).

**Bám ERP:** trường hiện/ẩn theo `type` đúng các `ng-if` của `form.blade.php` —
loại 1 (phiếu xác nhận BH → NCC + tiền tự điền, ô chỉ đọc) · loại 5 (phiếu xử lý hàng thiếu →
**1 NCC tự điền, nhiều NCC hiện select**, mirror `addQuotationParent()`) · loại 3 (popup NCC) ·
loại 4 (Đối tượng NCC/KH/**Nhân viên** + popup tương ứng) · loại 2/6 (bảng chi tiết, **bỏ hẳn** ô
Số tiền và Diễn giải ở đầu phiếu).
Đổi loại yêu cầu → xoá sạch trường phụ thuộc loại (mirror `ClearType()`), giữ loại tiền/tỷ giá/file.

**Thêm so với ERP:** dòng **Tổng cộng** ở chân bảng chi tiết (ERP không có, người lập phải tự cộng
nhẩm trong khi `money` của phiếu chính là tổng đó) · đổi đối tượng của 1 dòng thì **xoá hợp đồng cũ**
của dòng đó (hợp đồng cũ không còn thuộc đối tượng mới) · vào thẳng URL `/edit` của phiếu không sửa
được thì **đá về màn chi tiết** thay vì cho gõ rồi lưu mới báo lỗi.

**Bẫy đã né:** `V2BaseSelect` là wrapper select2 (không `reduce`/`label`) · lưu bằng
`apiPostMethod`/`apiPutMethod` với khoá **`payload`** · `markFormSaved()` gọi TRƯỚC khi `$emit('loaded')`
để `router.replace` ở trang Sửa không bị guard "chưa lưu" chặn · dòng chi tiết mới khai đủ khoá ngay
từ đầu (Vue 2 không reactive với property thêm sau).

⚠️ **Nợ kỹ thuật đã ghi nhận:** `AttachmentSection.vue` là **bản sao** của màn Đề nghị thanh toán,
chỉ đổi 3 đường dẫn API. CỐ Ý không sửa bản gốc thành component dùng chung vì file đó đang chạy thật
(CLAUDE.md: phải hỏi trước khi đụng code dùng chung) — gộp 2 bản thành 1 component nhận
`uploadUrl`/`deleteUrl` qua prop nên làm thành task riêng.

⚠️ **CHƯA mở trình duyệt** — user bấm tay: tạo nháp → sửa → gửi duyệt cho **cả 6 loại**;
3 popup mới trả đúng dữ liệu; popup cảnh báo chưa lưu khi thoát giữa chừng.
## Phase 7 — FE màn chi tiết (2 layout) + lịch sử ✅ CODE XONG 2026-08-25 (chờ user bấm trình duyệt)

**File tạo:**
- `pages/finance/addition-accounting-requests/_id/index.vue`
- `.../components/CoordinationDetail.vue` (loại 7)
- `.../components/RejectModal.vue` *(chuyển từ Phase 6 sang — nút Từ chối nằm ở màn chi tiết)*

- [x] Tiêu đề `Chi tiết phiếu yêu cầu hạch toán bổ sung: <mã>`, số phiếu ngay dưới tiêu đề
- [x] Khối: Thông tin chung (đọc-only) · bảng chi tiết (loại 2/6) · File đính kèm · Ghi chú duyệt ·
      Lịch sử thay đổi (**ẩn mặc định**, 3 bộ lọc, mới → cũ) — dùng lại `CatalogHistoryModal` /
      `SystemInfoSection`
- [x] Nút trong `V2Footer`: Sửa · Gửi duyệt · Từ chối · Lập phiếu kế toán · In · Xuất Excel · Quay
      lại — **đọc cùng cờ `is_can_*` của BE** như màn danh sách, không tự tính lại điều kiện
- [x] `CoordinationDetail.vue` cho loại 7: 8 trường thông tin chung + bảng *Nội dung / Số tiền* +
      bảng *Đối tượng hạch toán / Số tiền / Vụ việc*; **không có** nút Sửa/Xoá/Gửi duyệt
- [x] Vào URL `/edit` của phiếu không sửa được → đá về màn chi tiết

**Verify tự động (đã chạy):** 3 file compile sạch.

**Cách dựng:** thân trang loại 1-6 **dùng lại chính component form ở chế độ `readonly`** nên bố cục
giống hệt màn Sửa, sửa 1 chỗ là cả 2 màn đổi theo; loại 7 rẽ sang `CoordinationDetail` (2 bảng +
ô phòng ban **gộp dòng** theo số nhân viên, STT chạy liên tục qua các phòng).
Màn chi tiết tự gọi `GET /{id}` NGAY khi mở để biết `type` trước — không chờ form bắn `loaded`,
tránh nhấp nháy đổi layout giữa chừng.

**Nút footer đọc CÙNG cờ `is_can_*` với màn danh sách** (không tự suy theo trạng thái), nút không
dùng được thì **ẩn hẳn**. Nút *Lập phiếu kế toán* mở sang cổng ERP qua `utils/erp-link.js`;
`ERP_URL` trống thì báo lỗi rõ ràng thay vì mở tab trắng.

**Từ chối** đưa phiếu VỀ trạng thái *Đang tạo* (`status = 1`) — đúng như ERP, không có trạng thái
"Từ chối" riêng; lý do bắt buộc, BE cũng chặn.

⚠️ **CHƯA mở trình duyệt** — user bấm tay: mở 1 phiếu mỗi loại 1-7, so danh sách nút với màn danh
sách, mở khối Lịch sử và lọc thử 3 nhóm hoạt động.
## Phase 8 — FE màn in ✅ CODE XONG 2026-08-25 (chờ user in thử)

**File tạo:** `pages/finance/addition-accounting-requests/_id/print.vue`

- [x] Đọc `.claude/skills/print-page/SKILL.md` trước khi viết
- [x] Bố cục bám mẫu ERP id 463, FE tự dựng khung theo dữ liệu BE (**không** render HTML template ERP)
- [x] Letterhead từ `print-data` (đã theo công ty ghi trên chứng từ), giữ nguyên giá trị BE trả
- [x] Tự bật hộp thoại in; viền đủ 4 phía khi sang trang; bảng loại 7 có ô gộp không vỡ khi nhiều trang

**Verify tự động (đã chạy):** compile sạch.

**Theo skill print-page:** `layout: 'print'` (§2b — nền xám quanh giấy do layout lo, màn KHÔNG khai
`background` riêng) · khung tờ giấy A4 **dọc** 210mm, lề `15mm 22mm 22mm 20mm`, viền + bóng (§2c) ·
nút In canh **mép phải tờ giấy** bằng class riêng `.print-toolbar` (§0.2 — bám `.no-print` thì nút
bị kéo rộng bằng cả tờ giấy) · toàn bộ CSS bản in thật truyền qua `options.styles` vì scoped CSS
không sang cửa sổ in (§1) · viền đủ 4 cạnh mỗi ô để sang trang không mất viền trên (§3) ·
khối ký ép `width: 100%` + `td { width: auto }` ở CẢ preview lẫn cửa sổ in (§3b) ·
`b, strong { font-weight: 700 }` vì Times New Roman không có nét 500 · cột tiền `nowrap`.

**Dính đúng 1 bẫy của skill và đã sửa:** dấu **backtick trong chú thích CSS** nằm trong template
literal của `options.styles` làm đứt chuỗi → `@babel/parser` báo *Missing semicolon* (skill §8a).

⚠️ **Chưa đối chiếu mắt thường** — user in thử: 1 phiếu loại 2 (bảng nhiều dòng) · 1 phiếu loại 4
(dòng `ROW_*`) · 1 phiếu loại 7 (2 bảng) — kiểm viền, letterhead, không tràn lề phải.

⚠️ **1 điểm cần anh chốt:** skill print-page §8 (chốt 2026-08-22, làm cho 3 màn CSKH) nói nút In
nên mở **popup xem trước** bằng `ReportPrintPreviewModal` thay vì trang `/print` riêng. Nhưng
cách đó cần BE render sẵn HTML từ `report_templates`, trong khi màn này (và cả 3 màn Tài chính đã
port trước) chốt là **FE tự dựng khung** từ `print-data`. Tôi làm theo khuôn Tài chính cho đồng bộ;
nếu anh muốn đổi cả nhóm Tài chính sang popup thì nên làm thành 1 task riêng cho cả 4 màn.
## Phase 9 — Seeder dữ liệu test + tự kiểm ✅ XONG 2026-08-25 (còn 2 việc cần user)

**File tạo:** `Modules/Finance/Database/Seeders/AdditionAccountingRequestTestDataSeeder.php`

- [x] Seeder mã `TEST.PYCHTBS.*` theo §13 spec: mỗi loại 1–6 ít nhất 2 phiếu phủ đủ 4 trạng thái;
      loại 2 gắn đủ 3 nguồn hợp đồng bán; loại 6 gắn ≥3 loại hợp đồng mua; **loại 1 và 5 gắn vào
      `firm_warranty_confirms` / `inventory_discrepancy_handling_imports` có thật**
- [x] Seeder **không** sửa dữ liệu nghiệp vụ đã có, chỉ thêm bản ghi tiền tố `TEST.`
- [x] In danh sách KH / NCC / nhân viên để user chọn khi test tay
- [x] Chạy seeder thật trên `gop_db`
- [ ] ⏳ **CẦN USER** — **Bước 5 của skill `erp-to-hrm-screen`**: mở song song màn ERP và HRM, đối
      chiếu từng dòng bảng nghiệp vụ ở Phase 0 (đủ cột · đủ trường lọc · đủ hành động **và điều kiện
      ẩn/hiện khớp**)
- [x] Chạy hết checklist tự kiểm A–H của skill + 6 lệnh grep
- [x] Kiểm tiêu chí hoàn thành ở §15 spec
- [ ] ⏳ **CẦN USER** — test trình duyệt bằng **tài khoản không phải Super admin**, đủ 4 mức quyền

---


**Seeder đã chạy thật:** 12 phiếu `TEST.PYCHTBS.*` — đủ **6 loại × 2 trạng thái**
(*Đang tạo* để sửa/xoá/gửi duyệt, *Chờ duyệt* để từ chối), gán cho nhân viên của tài khoản dev
(tra theo email, không viết cứng id — phiếu nháp chỉ NGƯỜI TẠO mới thấy).

| Loại | Nguồn hợp đồng trong phiếu test |
| --- | --- |
| 2 — Điều chỉnh công nợ KH | `FirmContract` · `OpeningContract` · `WrServiceContract` · **`hrm_contracts`** (nguồn mới của HRM) |
| 6 — Điều chỉnh công nợ NCC | `BuyContract2` · `InlandBuyContract` · `BuyDebtContractBeginning` |

⚠️ **Seeder có đụng 1 dữ liệu nghiệp vụ của màn khác:** bật `accounting = 1` (*Chờ hạch toán bổ
sung*) cho **2 phiếu xử lý hàng thiếu** — không bật thì popup loại 5 luôn rỗng và không thử được
luồng nào. Seeder in cảnh báo + câu SQL hoàn tác, và có biến `AAR_SKIP_DISCREPANCY_FLAG=1` để bỏ
qua bước này trên môi trường thật.

**Chạy lại toàn bộ verify BE sau khi sửa `meta()` + seed dữ liệu — 100% pass:**

| Script | Kết quả |
| --- | --- |
| `verify_aar_phase1.php` × 5 tài khoản | 25 / 25 / 25 / 22 / 25 pass, **0 fail** |
| `verify_aar_phase2.php` × 4 lượt | 67 + 5 + 7 + 3 pass, **0 fail** |
| `verify_aar_phase3.php` | 29 pass, **0 fail** |
| `verify_aar_phase4.php` | **103** pass, 0 fail (tăng từ 67 vì loại 1/3/5 nay đã có dữ liệu) |

**Smoke test 2 file DÙNG CHUNG bị sửa** (`CatalogHistoryService::TABLES`,
`PermissionsTableSeeder`): 6 endpoint của 5 màn Tài chính khác vẫn **HTTP 200**, whitelist lịch sử
của 2 màn cũ còn nguyên.

**6 lệnh grep tự kiểm của skill `erp-to-hrm-screen`** trên CẢ thư mục feature: sạch. Grep
`thành công'` ra 8 dòng nhưng đều là câu chuẩn đang dùng ở các màn Tài chính khác
(*Lưu / Xóa / Xuất Excel / Cập nhật / Xóa file thành công*), không có câu tự chế.
---

## Phase 10 — Test Playwright toàn luồng ✅ XONG 2026-08-25 (user yêu cầu)

Bấm thật trên trình duyệt bằng tài khoản **DNS Admin (emp 13, Super admin)**, đối chiếu từng bước
với DB. **Tìm và sửa 7 lỗi mà compile + verify API KHÔNG bắt được.**

### 7 lỗi đã sửa

| # | Lỗi | Hậu quả nếu để nguyên |
| --- | --- | --- |
| 1 | Nút Lưu/Gửi duyệt đặt vào **slot mặc định** của `V2Footer` (component chỉ khai `dropdown` + `custom-actions`) | Form **không có nút lưu**, chỉ còn "Quay lại" — không tạo được phiếu nào |
| 2 | `loadMeta()` đọc `meta.data` trong khi BE trả `{ data: { meta: {...} } }` | Dropdown **Loại yêu cầu rỗng**, Người tạo/Phòng ban trống — form vô dụng |
| 3 | ~~Màn Sửa trống~~ | **Không phải lỗi** — tôi đo lúc dữ liệu chưa về |
| 4 | `POST /upload-files` trả `data: { urls: [...] }` còn khối file dùng chung đọc `data[0]` | File **ĐÃ lên S3** nhưng FE báo "Upload không trả về đường dẫn", không đính kèm được |
| 5 | Quan hệ `currency()` **trùng tên cột** `currency` của bảng ERP → Eloquent trả giá trị cột | Cột **"Loại tiền" trống** ở lưới, chi tiết, bản in và Excel |
| 6 | Khoá cứng ô **Số tiền** cho loại 1/5 (ERP chỉ khoá ở màn XEM) | Chứng từ nguồn không có chi phí → tiền 0, user **kẹt**: không sửa được, không gửi duyệt được |
| 7 | Thiếu override `unsavedSnapshotSource()` (mixin mặc định theo dõi `this.formSubmit`) | Popup **"Thông tin chưa lưu" không bao giờ hiện** — bấm Quay lại là mất trắng dữ liệu |

**Cải thiện thêm 2 chỗ:**
- Loại 7: `support_department_name` của ERP lưu **chính id phòng** ("44") → nay fallback sang tên
  thật trong `departments` ("PHÒNG THIẾT BỊ Ô TÔ 3").
- Gửi duyệt từ FORM chỉ sinh log `update` (nhãn *"Thay đổi thông tin"*) trong khi gửi từ màn chi
  tiết sinh `change_status` — nay cả 2 lối vào đều ghi thêm mốc **Thay đổi trạng thái**.

### Đã bấm thật và khớp DB

**Danh sách:** 10 dòng render đúng · căn lề chuẩn (STT/badge/hành động giữa · tiền phải · còn lại
trái) · ô rỗng in `—` · lọc **Loại yêu cầu** 1.874 → 7 (khớp SQL, 2 nháp người khác bị ẩn đúng luật)
· cộng dồn thêm **Trạng thái** → 1 · ô gõ tay **không tự tìm**, chờ Enter/nút Tìm kiếm ·
**Làm mới** xoá sạch cả filters lẫn select2 · tìm nhanh theo số phiếu → 12 · sort **Số phiếu** ASC,
đổi sang **Số tiền** thì **huỷ sort cột cũ** · 5 cột sortable đúng whitelist BE · đổi 5 dòng/trang
về trang 1 · **STT trang 2 = 6–10** (né bẫy `index+1`) · popup Cấu hình cột (STT/Số phiếu/Hành động
khoá, 2 cột cập nhật ẩn mặc định) · popup Cài đặt bộ lọc 9 trường · cột Hành động đúng chuẩn
2 nút chính + menu "…", nút Sửa là thẻ `<a>` (mở tab mới được).

**Tạo/sửa:** tạo nháp loại 4/Nhân viên → DB đúng từng cột, 3 cột tổ chức ép `0`, 2 nhóm đối tượng
không dùng đều NULL · **đổi loại** 4 → 2 xoá sạch trường phụ thuộc, hiện bảng chi tiết, ẩn ô Số
tiền/Diễn giải · chọn KH → chọn **hợp đồng bán** (popup đủ 3 nguồn: `hrm_contracts` + đầu kỳ +
bảo dưỡng) · dòng lưu `contractable_type = Modules\Assign\Entities\Contract\Contract` và
`objectable_type = App\Model\Sale\Customer` (chuỗi class ERP) · **Tổng cộng** tự cộng ·
**upload file thật lên S3** đúng thư mục `addiiton_accounting_requests` · gửi duyệt ghi `send_date`.

**Vòng đời:** gửi duyệt khi chưa có file → **BE chặn 422**, lỗi hiện ngay tại khối file ·
từ chối không lý do → chặn + lỗi inline · từ chối có lý do → status về 1, lưu đủ **`comment` +
`approver_id` + `approver_time`** · sau từ chối nút Sửa/Gửi duyệt/Xoá hiện lại + khối "Ghi chú
duyệt" · xoá phiếu có popup xác nhận, xoá luôn dòng chi tiết, **giữ lịch sử**.

**Lịch sử:** 4 mốc mới → cũ, có người thực hiện, in **giá trị cũ → mới từng trường** và bảng chi
tiết dạng dòng thêm (+), lý do từ chối hiển thị ngay tại mốc.

**Chi tiết/in:** cờ `is_can_*` khớp trạng thái · **loại 7** rẽ đúng layout riêng (5 chỉ tiêu + bảng
phòng ban→nhân viên có ô gộp dòng), **không có nút Sửa/Xoá** · màn in: không topbar, tờ giấy đúng
**210mm**, đủ tiêu đề/bảng/khối ký · nút **Lập phiếu kế toán** mở tab mới đúng URL ERP
`/admin/income-expenditure/bill_adjust_dept/create?addition_accounting_request_id=…` (404 ở local
chỉ vì `ERP_URL` trỏ host không tồn tại).

**Popup chứng từ nguồn:** loại 1 → 49 phiếu xác nhận BH đã duyệt, chọn xong tự điền NCC ·
loại 5 → 2 phiếu xử lý hàng thiếu (nhờ seeder bật cờ `accounting`), 1 NCC nên tự điền, không hiện select.

**Chế độ Chờ duyệt:** 48 phiếu, **100% đúng trạng thái "Chờ duyệt"** (vá lỗi ERP #4), ẩn nút Tạo mới.

### Dọn dữ liệu

Sau test, DB trở lại **đúng baseline đầu phiên**: `addition_accounting_requests` 1.949 ·
`_details` 2.863 · `customers` 43.522 · `hrm_contracts` 42 — **không ghi nhầm sang bảng nào khác**
(bẫy "phantom write" của popup dùng chung). Giữ lại 12 phiếu `TEST.PYCHTBS.*` để user tự bấm.
2 file PDF rác đã upload lên S3 trong lúc test (`aar-testpdf-*.pdf`) — vô hại, không phiếu nào trỏ tới.

### Verify tự động chạy lại sau khi sửa — vẫn 100% pass

`verify_aar_phase1` 25/25 × 4 tài khoản (+22/22 cho tài khoản 0 phiếu) · `phase2` 67+5+7+3 ·
`phase3` 29 · `phase4` 103 · 11 file FE compile sạch · 4 lệnh grep tự kiểm rỗng.

### 2 điều KHÔNG phải lỗi (ghi lại để khỏi nghi oan)

1. Cảnh báo `The computed property "fields" is already defined in data` đến từ
   `ChooseErpCustomerModal` **dùng chung** — có sẵn ở mọi màn dùng popup đó, không phải của màn này.
2. Đặt select2 bằng `jQuery.val().trigger('change')` hoặc chèn spy `JSON.stringify` vào `$emit`
   sẽ **làm chết chuỗi sự kiện** và khiến ô lọc trông như hỏng. Chỉ dùng thao tác chuột thật.

## Checkpoint

### Checkpoint — 2026-08-25 (sau test Playwright)
Vừa hoàn thành: **10 phase** — thêm Phase 10 test trình duyệt toàn luồng, tìm và sửa **7 lỗi**
compile/API không bắt được (nặng nhất: form KHÔNG có nút lưu, dropdown Loại yêu cầu rỗng, quan hệ
`currency` bị cột cùng tên che). Verify tự động chạy lại 100% pass, DB trở về đúng baseline.

### Checkpoint — 2026-08-25 (trước test)
Vừa hoàn thành: **toàn bộ 9 phase** — BE (Phase 1-4) verify tự động 100% pass, FE (Phase 5-8)
compile sạch + grep tự kiểm sạch, seeder dữ liệu test đã chạy thật (12 phiếu, đủ 6 loại × 2 trạng thái).
Đang làm dở: không.
Bước tiếp theo: **user bấm tay trên trình duyệt** — đối chiếu song song với màn ERP (bước 5 của
skill), test bằng tài khoản không phải Super admin ở đủ 4 mức quyền, in thử 3 loại phiếu.
Blocked: chờ user chốt 1 điểm ở Phase 8 (bản in dùng trang `/print` như nhóm Tài chính, hay đổi
sang popup xem trước theo skill print-page §8 — nếu đổi thì nên làm cho cả 4 màn Tài chính).
