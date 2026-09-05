# Plan — Phiếu yêu cầu điều chỉnh công nợ (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo, code thẳng trên nhánh này — không tách nhánh riêng)
> Design: `.plans/gop-db/finance-bill-adjust-dept-request/design.md`
> Spec: `docs/superpowers/specs/gop-db/2026-08-17-finance-bill-adjust-dept-request-design.md`
> **Trạng thái: HOÀN THÀNH — user xác nhận xong (2026-08-24), cả 18 phase đã nghiệm thu.**

---

## Phase 0 — Brainstorming & chốt scope

- [x] Khảo sát màn ERP (model 1.439 dòng · controller · 21 route · view Blade)
- [x] Đo số liệu thật trên DB `gop_db` (10.172 phiếu, phân bố loại / trạng thái / contractable_type)
- [x] Chốt 11 quyết định lớn với user
- [x] Viết spec chi tiết `docs/superpowers/specs/gop-db/2026-08-17-...-design.md`
- [x] Viết `design.md` tóm tắt + `plan.md`
- [x] User đọc lại spec và duyệt

## Phase 1 — BE nền (đọc) ✅ XONG 2026-08-17

- [x] `Entities/BillAdjustDeptRequest/BillAdjustDeptRequest.php` — bảng ERP, 6 trạng thái, `$fillable`, `ALLOWED_TRANSITIONS`
- [x] `BillAdjustDeptRequestDetail.php` + `BillAdjustDeptRequestDetailItem.php` — quan hệ 2 cấp, morph `contractable`
- [x] `Relation::morphMap()` — **không phải sửa gì**: `FinanceServiceProvider` đã đăng ký sẵn đủ 10 class ERP mà màn này dùng (`FirmContract`, `OpeningContract`, `WrServiceContract`, 4 nguồn HĐ mua…)
- [x] Phạm vi quyền 4 cấp trong `BillAdjustDeptRequest::searchByFilter()` + `canView/canEdit/canDelete/canReject/canSendApprove`
- [x] Sinh mã `{mã công ty}.DNDCCN{mmyy}.{5 số}` bọc transaction + `lockForUpdate`
- [x] `BillAdjustDeptRequestPermissionSeeder` — 4 quyền **id 1169–1172** guard `api` (1162–1168 đã thuộc màn Yêu cầu nhập hàng), thêm vào `PermissionsTableSeeder`; **đã chạy thật**, tự kế thừa role đang giữ quyền ERP guard `web` (18/63/15/10 nhân viên)
- [x] `BillAdjustDeptRequestService` (đọc) + Route 4 endpoint + Controller
- [x] `ListResource` (13 cột) + `DetailResource` (bảng 2 cấp)
- [x] **Verify HTTP thật** (JWT, 4 mức quyền) — số bản ghi khớp SQL **tuyệt đối**:

| Người dùng | Quyền | API total | SQL | Khớp |
| --- | --- | --- | --- | --- |
| emp 13 | Super admin | 10.171 | 10.171 | ✅ |
| emp 24 | Xem theo phòng ban | 1.078 | 1.078 | ✅ |
| emp 27 | Không quyền | 101 | 101 | ✅ |
| emp 30 | Không quyền | 72 | 72 | ✅ |
| emp 13 | `pending` (kế toán) | 40 | 40 | ✅ |

Chi tiết 2 cấp trả đúng cho cả loại KH (1 dòng "từ" → 2 dòng "đến") lẫn loại NCC (số dư, hợp đồng mua).
`generate-code` trả `TPE.DNDCCN0826.00001`. Script verify: `scratchpad/verify_phase1.php`.

⚠️ Ghi nhận: `php artisan route:list` **chết sẵn** trên repo này (`PermissionHelper::isCurrentEmployeeHasPermission` gọi `auth()->user()` lúc đăng ký route) — không phải lỗi của feature này, verify route bằng HTTP kernel thay thế.

## Phase 2 — BE ghi ✅ XONG 2026-08-17

- [x] ~~2 migration bảng lịch sử~~ → **ĐỔI: dùng bảng log CHUNG `catalog_histories`** (skill entity-history §5.1) thay vì tạo bảng riêng ⇒ **feature này KHÔNG thêm bảng nào**, và FE dùng lại được `CatalogHistoryModal` + `SystemInfoSection` ở Phase 5. Chỉ khai `bill_adjust_dept_requests` vào `CatalogHistoryService::TABLES` (thuần thêm 1 entry).
- [x] `StoreRequest` / `UpdateRequest` / `ChangeStatusRequest` — rethrow `ValidationException`, `note_reject` bắt buộc khi từ chối
- [x] `syncDetails()` — tách nhánh KH / NCC, tính `total_amount` (quy đổi VNĐ khi NCC ngoại tệ), xoá 2 cấp bằng 2 câu lệnh
- [x] 6 luật validate bám ERP + 4 luật bổ sung HRM; thêm `validateTotalsOfSavedModel()` cho nút Gửi duyệt ở màn chi tiết (ERP không có → phiếu nháp lệch tiền vẫn gửi được)
- [x] `POST /` · `PUT /{id}` · `DELETE /{id}` · `POST /{id}/change-status` (chặn nhảy cóc bằng `ALLOWED_TRANSITIONS`)
- [x] `BillAdjustDeptRequestNotifyService` — prefix `[DCCN]`, 2 sự kiện, deep-link `/finance/bill-adjust-dept-requests/{id}`
- [x] Ghi lịch sử qua trait `LogsCatalogHistory` — lý do từ chối vào `note` của log (skill §4.1)
- [x] **Verify HTTP thật: 34/34 pass** + 5 ca chéo tài khoản, dữ liệu test dọn sạch (0 phiếu, 0 log sót)

**Ca đã kiểm** — tạo nháp (tiền/trạng thái/cấp tổ chức/chi tiết đúng) · 7 ca xấu bị chặn 422 (lệch tổng tiền · `status=4` nhảy cóc · HĐ "đến" trùng "từ" · `details` rỗng · dòng "từ" không có dòng "đến" · tiền = 0 · NCC thiếu `supplier_new_id`) · sửa phiếu (tiền cập nhật, sync không nhân đôi dòng con) · vòng đời `1 → 2 → 6 → 2` · từ chối không lý do bị chặn · lý do + người từ chối lưu đúng · gửi lại xoá lý do cũ · 5 mốc lịch sử đúng, log `update` **chỉ ghi 3 trường đã đổi** · xoá phiếu chờ duyệt bị 403, xoá phiếu nháp xoá sạch 2 cấp.

**Ca chéo tài khoản** (lỗ hổng ERP đã vá): emp27 XEM / SỬA / XOÁ phiếu nháp của emp13 → **403 cả ba**, gửi duyệt → 422, dữ liệu phiếu không đổi. Bên ERP cả 3 thao tác này đều lọt.

⚠️ **Phải chạy trên môi trường khác**: migration `2026_08_16_000001_create_catalog_histories_table` (của app chung, không phải của feature này) **chưa từng chạy trên `gop_db`** — đã chạy riêng bằng `--path`. Môi trường nào chưa có bảng `catalog_histories` thì luồng ghi sẽ 500.

Script verify: `scratchpad/verify_phase2.php` + `verify_cross_user.php`.

## Phase 3 — BE tra cứu ✅ XONG 2026-08-17

- [x] `GET /search-bill-income-reports` + `GET /bill-income-report-details` (lọc theo công ty người đăng nhập)
- [x] `GET /search-customers` + `GET /search-suppliers` — **cùng bảng `customers`**, NCC lọc `is_supplier = 1` (bảng `suppliers` trên DB gộp có 0 dòng)
- [x] `GET /search-contracts` — hợp đồng bán **3 nguồn: `hrm_contracts` + `opening_contracts` + `wr_service_contracts`**; `firm_contracts` đã bị loại khỏi luồng tạo mới đúng yêu cầu
- [x] `GET /search-buy-contracts` + `GET /buy-contract-detail` + `GET /contract-detail` — 4 nguồn hợp đồng mua ERP
- [x] `BillAdjustDeptDebtService` — công nợ TK 1311/3311 + số dư đầu kỳ, giữ nguyên công thức ERP
- [x] `GET /currencies`
- [x] **Verify: 14/14 pass**

| Kiểm tra | Kết quả |
| --- | --- |
| Công nợ 50 hợp đồng thật vs công thức ERP | **lệch 0** |
| `remainDebtMany` (1 query gom) vs tính từng cái | **lệch 0** |
| Popup hợp đồng bán | 140 dòng — HRM 40 · đầu kỳ 50 · dịch vụ 50; **không còn `FirmContract`** |
| Popup hợp đồng mua | 200 dòng, đủ 4 nguồn |
| Chi tiết phiếu báo có | số dòng API = số dòng SQL |

**2 lỗi tên cột đã sửa** (đều do đoán tên theo thói quen, DB ERP đặt khác):
`bill_income_report_details.parent_id` (không phải `bill_income_report_id`) · `customers.address_text` (không phải `address`).

⚠️ Khác ERP có chủ đích: ERP `getDeptAccountGroup()` nạp **toàn bộ** sổ cái (971.914 dòng) mỗi lần mở popup; bản HRM chỉ gom đúng các hợp đồng đang hiển thị.

Script verify: `scratchpad/verify_phase3.php`.

## Phase 4 — FE ✅ XONG 2026-08-17

- [x] `index.vue` — 12 cột + cột Hành động, 11 nhóm bộ lọc, **1 file cho cả 2 chế độ** (`?mode=pending`) đúng cách màn Đề nghị thanh toán làm; có watcher `mode` (bắt buộc, menu đổi query không dựng lại component)
- [x] 2 mục menu ở `components/subsystem-menu/finance.js` — **2 mục placeholder đã có sẵn**, chỉ gắn link; mục chờ duyệt gate `isShow: ['Kế toán thanh toán']`
- [x] `BillAdjustDeptRequestForm.vue` (khuôn `CustomerForm.vue`) + `create.vue` + `_id/edit.vue`
- [x] `AdjustDetailTable.vue` — bảng 2 cấp gộp dòng (`rowspan`), tự đổi cột theo loại phiếu (thêm cột Số dư) và theo ngoại tệ (tách đôi mỗi cột tiền), dòng tổng + cảnh báo lệch tiền theo từng nhóm
- [x] **3 popup** thay vì 5: `PartySearchModal` (KH/NCC chung, đổi bằng prop `mode`) · `ContractSearchModal` (HĐ bán/mua chung) · `BillIncomeReportSearchModal`. Gộp vì mỗi cặp chỉ khác endpoint + nhãn 1 cột — tách ra là nhân bản nguyên file
- [x] `_id/index.vue` — chi tiết + **khối Lịch sử trong thân trang** (`SystemInfoSection`, không phải nút footer) + nút theo cờ `is_can_*` BE trả, ẩn hẳn khi không dùng được · `RejectModal.vue` bắt buộc nhập lý do
- [x] `unsavedChangesMixin` (form con) + `unsavedChildFormMixin` (trang vỏ) — đúng cặp theo skill
- [x] Cờ quyền **fail-closed**: `scopeMeta` khởi tạo `false`, chỉ nhận từ `meta` BE; không có literal `true` nào
- [x] Verify: **9/9 file compile sạch** (vue-template-compiler + babel); không đặt prop tên `errors`/`fields`

**1 lỗi đã sửa**: `Required` nằm ở `@/components/common/Required`, không phải `@/components/Required.vue`.

Script verify FE: `scratchpad/check_vue.js` (hrm-client không có ESLint chạy được trên Node 14).

## Phase 5 — In, Excel, lịch sử, dữ liệu test ✅ XONG 2026-08-17

- [x] `BillAdjustDeptRequestPrintResource` + `GET /{id}/print-data` — 3 khuôn bảng chọn bằng `layout`
- [x] `_id/print.vue` — khổ **ngang**, `id="content"`, bố cục bằng inline style, CSS viền truyền qua `options.styles`, **mỗi nhóm ô gộp là 1 `<tbody>` + `page-break-inside: avoid`** (skill print-page §5)
- [x] `BillAdjustDeptRequestExport` (1 phiếu) + `BillAdjustDeptRequestListExport` (danh sách) + 2 blade trong module
- [x] Lịch sử: **popup ở màn danh sách** (`CatalogHistoryModal`) + **khối ở màn chi tiết** (`SystemInfoSection`) — đủ 2 nơi theo skill entity-history §5.1, dùng bộ chung nên không viết component mới
- [x] `BillAdjustDeptRequestTestDataSeeder` — 6 phiếu (3 trạng thái × 2 loại), 1 phiếu ngoại tệ để thử khuôn 14 cột
- [x] **Verify: 22/22 pass**

| Kiểm tra | Kết quả |
| --- | --- |
| `print-data` 3 khuôn | `customer` 4 cột · `supplier` 5 cột · `supplier_fx` 7 cột mỗi bên — đúng |
| `rowspan` nhóm | = số dòng "điều chỉnh đến" |
| Quy đổi ngoại tệ | số dư **chia** tỷ giá (lưu VNĐ) · số tiền **nhân** tỷ giá (nhập ngoại tệ) — 2 chiều ngược nhau đúng như ERP |
| Excel 1 phiếu × 3 khuôn | file xlsx hợp lệ, 19–20 dòng |
| Excel danh sách | 9 dòng = 3 tiêu đề + 6 phiếu test |

**2 điểm sửa trong seeder sau khi đo thực tế**: gán `created_by` theo **email** tài khoản dev (gán nhầm người thì phiếu *Đang tạo* không ai thấy — chính là luật ẩn nháp của người khác); tiền phiếu ngoại tệ nhập **bằng ngoại tệ** và số dư lưu **VNĐ**, nếu không bản in ra 150 tỷ / 0,06 USD.

⚠️ **Khác spec có lý do**: không render mẫu HTML `report_templates` id 209 của ERP. Mẫu đó là HTML ghép tay cho trang in Blade, không dùng lại được trong màn in Vue và không kiểm soát nổi ngắt trang / giữ viền mà skill print-page yêu cầu. Bố cục và nội dung vẫn bám mẫu ERP.

---

### Checkpoint — 2026-08-17
Vừa hoàn thành: **CODE DONE 5/5 phase**. BE 17 file mới + 4 file sửa · 20 route · 4 quyền id 1169–1172 · 2 seeder. FE 10 file mới + 1 file sửa (menu).
Đang làm dở: không.
Bước tiếp theo: **user bấm tay trên trình duyệt** — dữ liệu sẵn: 6 phiếu `TEST.DNDCCN.*` (2 nháp · 2 chờ duyệt · 2 bị từ chối, có 1 phiếu NCC ngoại tệ). Cần thử: tạo phiếu từ popup Phiếu báo có · đổi loại phiếu (bảng phải xoá sạch) · gộp dòng khi thêm nhiều dòng "đến" · gửi duyệt / từ chối · in (kiểm ngắt trang khi nhiều nhóm) · xuất Excel · popup + khối Lịch sử.
Blocked: không.

## Phase 6 — Test trên trình duyệt (Playwright) ✅ XONG 2026-08-17

User yêu cầu test bằng Playwright. Chạy thật trên `localhost:3000` (API `:8000`), tài khoản `DNS Admin`.

**Đã bấm qua**: danh sách (13 cột, cờ quyền theo trạng thái) · chi tiết phiếu NCC ngoại tệ ·
form tạo mới · popup Phiếu báo có → nạp 6 dòng chi tiết · đổi loại phiếu KH ↔ NCC · chọn ngoại tệ ·
popup NCC · popup hợp đồng mua (lọc đúng theo NCC đã chọn) · nhập tiền + dòng tổng quy đổi ·
**lưu nháp thành công** · màn in · popup Lịch sử · cảnh báo "chưa lưu".

### 10 lỗi phát hiện — đã sửa hết

| # | Lỗi | Mức |
| --- | --- | --- |
| 1 | **Luật chống trùng hợp đồng bắn nhầm khi cả 2 bên bỏ trống hợp đồng** (`null == null`). 9.715/10.480 dòng phiếu thật không gắn hợp đồng ⇒ luật bê từ ERP sẽ chặn gần hết phiếu | **Chặn nghiệp vụ** |
| 2 | Cột NOT NULL: `note`, và `customer_old_id/name` + `customer_new_id/name` với phiếu NCC → **500 khi lưu**. ERP lưu `0` / `''` cho các cột này | **Chặn luồng lưu** |
| 3 | Gọi sai action store: dùng `apiPost/apiPut` (nhận url CHUỖI) với object → URL thành `/api/v1/[object Object]` → 404. Đúng là `apiPostMethod`/`apiPutMethod` + khoá `payload` | **Chặn luồng lưu** |
| 4 | Dùng nhầm API component: `V2BaseSelect` là wrapper **select2**, không có `reduce`/`label`/`clearable` (đó là vue-select) → **select Loại phiếu và Tiền tệ không đổi được giá trị** | **Chặn form** |
| 5 | `AdjustDetailTable` quy đổi số dư **sai chiều** (nhân tỷ giá thay vì chia) — số dư lưu VNĐ. `PrintResource` làm đúng nên 2 nơi lệch nhau | Sai số liệu |
| 6 | Cột "Số tiền" ở danh sách gắn hậu tố `currency_name` cho `total_amount` đã quy đổi VNĐ → hiện "36.000.000 USD" trong khi đó là 36 triệu VNĐ | Sai số liệu |
| 7 | `meta.creator.name` lấy `$user->fullname` — tên nằm ở `employee_infos` → ô "Người lập" luôn trống | Hiển thị |
| 8 | Letterhead bản in `v-html` chuỗi đường dẫn ảnh → in ra chữ `/uploads/xxx.png`. Sửa thành `<img>` URL tuyệt đối, ẩn khi ảnh lỗi (skill print-page §4) | Hiển thị |
| 9 | Popup Phiếu báo có hiện ngày ISO `2026-07-27` thay vì `27/07/2026` | Hiển thị |
| 10 | `display_name` ghép cứng `code . ' - '` → khách hàng không có mã hiện `- NGUYỄN THỊ THÚY` | Hiển thị |

**Sau khi sửa, chạy lại toàn bộ**: Phase 2 34/34 · Phase 3 14/14 · Phase 5 22/22 · 11/11 file Vue compile sạch · dữ liệu test dọn sạch (phiếu tạo lúc test đã xoá cùng chi tiết + log).

⚠️ Rút ra: verify bằng compile + gọi API **không bắt được** nhóm lỗi 3 và 4 (sai chữ ký hàm phía FE) — chỉ mở trình duyệt mới lộ.

## Phase 7 — Sửa cửa vào "Phiếu báo có" cho đúng ERP ✅ XONG 2026-08-17

User hỏi lại "bên ERP có chỗ chọn phiếu báo có đâu" → tra kỹ ERP thì **đúng là không có popup**.
Luồng ERP: màn **Chi tiết phiếu báo có** → tích checkbox từng dòng → nút *"Tạo phiếu yêu cầu điều
chỉnh công nợ"* → sang màn tạo kèm `?bill_income_report_detail_ids=`.
**User chốt: bỏ popup, làm đúng như ERP.**

Popup mình làm trước đó bỏ mất 3 ràng buộc, gây lệch nghiệp vụ thật:

| Ràng buộc của ERP | Popup cũ | Số liệu |
| --- | --- | --- |
| Chỉ phiếu báo có **loại khách hàng** (`type=1`), trạng thái 2 | không lọc | 3.714/3.825 phiếu |
| Chỉ dòng **còn tiền chưa điều chỉnh** (`money − money_adjusted > 0`) | nạp mọi dòng | chỉ **968/10.199** dòng (9,5%) hợp lệ |
| Người dùng **tích chọn từng dòng** | nạp cả phiếu | — |

⇒ Popup cũ cho điều chỉnh trùng trên ~90% số dòng, và nạp `money` gốc thay vì phần còn lại.

**Đã làm:**
- [x] Xoá `BillIncomeReportSearchModal.vue`, gỡ endpoint `search-bill-income-reports`
- [x] `bill-income-report-details` nhận **`?ids=1,2,3`** (id DÒNG), trả `money_old` = phần **còn lại**, kèm cả 2 vế `money_old_foreign` / `money_old_vnd`, `has_begin` (dòng đầu kỳ bị chặn trần bằng số dư đầu kỳ)
- [x] Port nốt 3 khối logic ERP đã sót: **khoá loại phiếu** theo loại thu của phiếu báo có (trừ khi mọi dòng là "khách không rõ") · **tự điền tiền tệ + tỷ giá** cho phiếu NCC · chọn vế tiền theo loại phiếu · gán NCC mặc định "KHÁCH KHÔNG RÕ" cho dòng thiếu đối tượng
- [x] Form đọc `$route.query.bill_income_report_detail_ids`, ô "Số phiếu báo có" chỉ hiện khi có

**Verify trên trình duyệt (2 nhánh):**
- `?ids=10227,10228,10229` (mọi dòng "khách không rõ") → 3 dòng, tiền 2.903.526 / 432.000 / 2.943.000, tổng 6.278.526, loại phiếu **không khoá** ✓
- `?ids=215,216` (khách hàng thật) → 2 dòng có KH + mã hợp đồng, tiền 5.891.400 / 4.464.000, loại phiếu **bị khoá** (select disabled + dòng chú thích) ✓

Regression sau sửa: Phase 2 34/34 · Phase 3 **17/17** (thêm 5 ca mới) · Phase 5 22/22 · FE 10/10 compile sạch.

⚠️ **Hệ quả**: HRM chưa port màn Phiếu báo có nên **chưa có nút nào** dẫn sang luồng này — chỉ chạy khi mở URL trực tiếp. Tạo phiếu không gắn báo có thì dùng bình thường.

## Phase 8 — Đối chiếu form + bảng chi tiết với ERP ✅ XONG 2026-08-17

User chỉ ra: màn tạo ERP **không có ô Mã phiếu**, và bảng chi tiết khác ERP. Đọc lại
`form.blade.php` + `partials/customer_form.blade.php` + `partials/supplier_form.blade.php` — đúng,
**7 chỗ lệch**:

| # | ERP | Bản mình (sai) |
| --- | --- | --- |
| 1 | Ô **Mã phiếu** `ng-if="form.id"` — chỉ ở màn SỬA | Hiện ở cả màn tạo, còn gọi thừa API `generate-code` |
| 2 | **Diễn giải BẮT BUỘC** (`required-label`) | Để nullable ở cả FE lẫn BE |
| 3 | Loại phiếu `ng-disabled="form.id \|\| request_type_locked"` — **khoá cả khi SỬA** | Chỉ khoá khi tạo từ phiếu báo có |
| 4 | Bảng KH **5 cột mỗi bên** — có cột **Số dư cuối kỳ** | Chỉ 4 cột, **thiếu hẳn cột Số dư** |
| 5 | Mỗi nhóm có **dòng "Số tiền còn lại"** (`money_old − Σ money_new`) | Không có |
| 6 | Nút **"Thêm điều chỉnh"** trong từng nhóm; nút **thêm dòng "từ"** nằm ở **header bảng** | Một nút "Thêm dòng điều chỉnh" rời bên dưới |
| 7 | Tạo từ phiếu báo có → bên "Điều chỉnh từ" **chỉ đọc** (không nút chọn, không sửa tiền, không xoá nhóm, không thêm nhóm) | Cho sửa tất cả |

Nhãn cũng đã sửa cho khớp: **NVKD** (phiếu KH) / **Nhân viên** (phiếu NCC) · **Hợp đồng/Đơn hàng** ·
**Số dư cuối kỳ** (KH) / **Số dư** (NCC). `rowspan = items.length + 3` đúng như ERP.

Bảng NCC vốn đã đúng số cột (5 nội tệ / 7 ngoại tệ).

**Verify**: BE 34/34 + 17/17 + 22/22, thêm 5 ca mới cho luật Diễn giải bắt buộc (thiếu → 422,
chỉ khoảng trắng → 422, có → 200, lưu đúng, dọn sạch). FE 3/3 file sửa compile sạch.

⚠️ **Chưa mở lại trình duyệt để xem bảng mới**: phiên Chrome của Playwright đang bị khoá
(`Browser is already in use`), mình không tự tắt vì có thể là trình duyệt bạn đang dùng.
Phần giao diện của Phase 8 **chưa được nhìn tận mắt**.

**Chưa làm (ngoài phạm vi, ERP có)**: nút **"Chọn nhanh hợp đồng"** trong mỗi nhóm — popup chọn
nhiều hợp đồng một lượt.

## Phase 9 — Dùng lại component sẵn có, bỏ đồ tự chế ✅ XONG 2026-08-17

User chỉ ra 2 điều, đều đúng: bảng **không dùng V2Base**, và **popup chọn KH / hợp đồng đã có sẵn**
từ các màn trước.

**Đã sửa:**

| Chỗ | Trước (tự chế) | Sau (dùng chung) |
| --- | --- | --- |
| Ô chọn KH/HĐ trong bảng | `<button class="btn-pick">` + CSS riêng | **`V2BaseInput`** readonly + class `picker-input` + `@click.native` — đúng khuôn `BillPaymentRequestDetailTable.vue` |
| Nút thêm/xoá dòng | `<button class="btn-icon">` + CSS riêng | **`V2BaseIconButton`** (`danger` cho nút xoá) |
| Nút "Thêm điều chỉnh" | `<button class="btn-link-add">` | **`V2BaseButton`** tertiary |
| Popup chọn khách hàng | `PartySearchModal.vue` (tự viết) | **`components/modals/ChooseErpCustomerModal.vue`** |
| Popup chọn NCC | `PartySearchModal.vue` (tự viết) | **`SupplierSearchModal`** của màn Đề nghị thu tiền |
| Popup chọn hợp đồng | `ContractSearchModal.vue` (tự viết) | **`ContractSearchModal`** của màn Đề nghị thu tiền (`type` 1 = HĐ bán, 2 = HĐ mua) |

⇒ **Xoá 2 file component** (6 → 3), **gỡ 3 endpoint BE trùng lặp** (`search-suppliers`,
`search-contracts`, `search-buy-contracts`) và toàn bộ code tra hợp đồng đi kèm — `BillAdjustDeptLookupService`
từ **475 → 306 dòng**. Popup hợp đồng dùng chung vốn đã lấy nguồn **`hrm_contracts` + đầu kỳ +
bảo dưỡng**, đúng quyết định firm→hrm nên không mất gì.

**Giữ lại có lý do:**
- `search-customers` — ô lọc KH/NCC ở màn danh sách là **một ô gộp cả hai nhóm**, popup dùng chung tách làm 2 nên không thay được.
- `contract-detail` / `buy-contract-detail` — popup dùng chung **không trả tên nhân viên phụ trách**, mà bảng ERP có cột NVKD ⇒ gọi bổ sung sau khi chọn, thay vì sửa popup dùng chung (CLAUDE.md: không tự sửa code dùng chung).

**Verify**: BE 34/34 + **15/15** (Phase 3 cập nhật: 3 endpoint đã gỡ trả 404, popup dùng chung vẫn
chạy) + 22/22 + 5/5 · FE 8/8 file compile sạch · `contract-detail` trả đúng `created_by_name`
("Vương Văn Duy").

## Phase 10 — Khảo sát dữ liệu để user tự test ✅ XONG 2026-08-17

User tự test, yêu cầu chỉ ra KH/NCC đã đủ dữ liệu (fake nếu thiếu).
**Kết quả: dữ liệu thật đã đủ mọi nhánh, KHÔNG phải tạo dữ liệu giả.**
Chi tiết: **`.plans/gop-db/finance-bill-adjust-dept-request/du-lieu-test.md`**

| Nhánh | Dữ liệu sẵn có |
| --- | --- |
| Phiếu KH tạo tay | 6 khách hàng có hợp đồng kèm công nợ (43669 · 916 · 36250 · 13102 · 43235) |
| Phiếu NCC tạo tay | 5 NCC có hợp đồng mua; NCC **21015** có 8/10 HĐ số dư dương |
| Từ phiếu báo có — khoá loại phiếu | dòng 10182, 10181 (`TPV.PBC0726.00024`, KH rõ ràng) |
| Từ phiếu báo có — không khoá | dòng 10227–10229 (`TPE.PBC0726.00078`, khách không rõ) |
| Từ phiếu báo có — **ngoại tệ** | dòng 7105 (`TPE.PBC0426.00046`, USD, tỷ giá 26.015) |
| Sửa/duyệt/từ chối/in/Excel | 6 phiếu seeder `TEST.DNDCCN.*` |

Tất cả đã kiểm **qua đúng API mà popup gọi**, không chỉ đọc DB.

### ⚠️ Đính chính số liệu đã báo sai 3 lần trước

Đã báo *"`hrm_contracts` có 0 dòng trong `account_details` ⇒ công nợ hợp đồng HRM luôn hiện 0"* —
**SAI**. Thực tế **33/40 hợp đồng HRM có bút toán TK 1311**, tổng ~25,9 tỷ (`HĐ-TEST-DNTT-*`).
Nguyên nhân: truy vấn qua shell nuốt dấu `\` trong `contractable_type` nên `WHERE` không khớp dòng nào.
⇒ Quyết định #4 (firm → hrm) **không kéo theo hệ quả mất công nợ** như đã cảnh báo.
Đã sửa lại trong `design.md`, spec, `STATUS.md` và memory.
Bài học: đếm theo `contractable_type` phải dùng `LIKE '%Assign%Contract%'`.

## Phase 11 — Sửa lệch cột bảng + nới cột Số tiền ✅ XONG 2026-08-17

User báo: cột Số tiền nhỏ, và **2 nút xoá đứng nhầm chỗ của nhau**. Đếm lại từng ô của ERP
(`customer_form.blade.php`) thì bảng ERP có **12 cột**, bảng mình chỉ **11** — thiếu đúng 1.

**Cấu trúc đúng của ERP** (loại KH, nội tệ):

```
| ←──── Điều chỉnh từ (5) ────→ | ←──── Điều chỉnh đến (6) ────→ | (1) |
                                  5 cột dữ liệu + cột nút xoá DÒNG   nút xoá NHÓM
```

- Khối "đến" `colspan=6` — **cột nút xoá từng dòng "đến" nằm TRONG khối này**
- Cột thứ 12 (cuối bảng, `rowspan` cả nhóm) mới là **nút xoá cả nhóm**; header của cột này là nút `+` thêm nhóm

Bản mình để khối "đến" `colspan=5` ⇒ nút xoá nhóm bị đẩy vào đúng ô của nút xoá dòng — hệt điều user thấy.

**Đã sửa:**
- Thêm computed `toBlockColspan` = số cột dữ liệu + cột nút, dùng cho: header khối "đến", ô trống dòng đầu, dòng nút "Thêm điều chỉnh"
- Dòng "Số tiền còn lại" và dòng "Tổng cộng" tính lại số ô cho khớp (tfoot thiếu 1 ô)
- **Cột Số tiền 150px → 200px** (đúng `style="width: 200px"` của ERP), cột Số tiền (VNĐ) 140 → 170px

⚠️ **Lần đầu nới không ăn** — user báo cột vẫn nhỏ. Nguyên nhân: `width` trên `<th>` chỉ là **gợi ý**
với bảng auto-layout, cột nào khai `min-width` (Khách hàng 200px, Hợp đồng 190px) sẽ giành hết chỗ
còn cột chỉ có `width` bị bóp lại. Đã đổi **toàn bộ cột tiền/số dư sang `min-width`**
(Số tiền 200px · Số tiền VNĐ 170px · Số dư 150px) + CSS: ô căn phải `white-space: nowrap`,
ô nhập tiền `width: 100%`. Bảng rộng quá thì `.table-responsive` lo cuộn ngang.
Kiểm bằng `scratchpad/do_be_rong_cot.js` (render rồi liệt kê bề rộng khai báo từng cột).

**Verify bằng cách đếm cột thật** (`scratchpad/dem_cot_bang.js` — dựng bảng bằng `vue-server-renderer`
rồi cộng `colspan`/`rowspan` từng dòng, vì **lệch cột không làm compile lỗi**):

| Biến thể | Số cột từng dòng |
| --- | --- |
| KH · nội tệ · sửa được | 12 12 12 12 12 12 12 12 ✓ |
| KH · nội tệ · chỉ đọc | 10 × 7 ✓ |
| KH · tạo từ phiếu báo có | 12 × 8 ✓ |
| NCC · nội tệ | 12 × 8 ✓ |
| NCC · **ngoại tệ** | 16 × 8 ✓ |
| NCC · ngoại tệ · chỉ đọc | 14 × 7 ✓ |

**12 cột cho loại KH nội tệ khớp chính xác ERP.** Kiểm thêm vị trí nút (`kiem_vi_tri_nut.js`):
nút "Xoá nhóm" ở ô cuối dòng đầu ✓ · nút "Xoá dòng" ở ô cuối dòng item ✓ · dòng item có đúng 6 ô ✓.

Regression: BE 34/34 + 15/15 · FE 8/8 compile sạch.

## Phase 12 — Màn chi tiết dùng lại chính form ✅ XONG 2026-08-17

User báo khối "Thông tin phiếu" ở màn Chi tiết **khác form**. Đúng: mình tự dựng lại khối đó bằng
`<div class="field-line">` với bộ trường và bố cục riêng.

Đối chiếu ERP: `formShow.blade.php` **bám đúng bố cục `form.blade.php`** (cùng card "Thông tin chung",
cùng `col-md-6`, label + input disabled), **khác duy nhất** ô **"Ghi chú không duyệt"**.

**Đã sửa:** màn Chi tiết giờ render **chính `BillAdjustDeptRequestForm` với `:readonly="true"`** —
sửa form một chỗ là cả 3 màn (Tạo / Sửa / Chi tiết) đổi theo, không thể lệch nhau nữa.

Kèm theo, đồng bộ nốt với ERP:
- Nhãn card: "Thông tin phiếu" → **"Thông tin chung"**, "Chi tiết điều chỉnh" → **"Chi tiết"**
- Góc phải header hiện **"người tạo - ngày tạo"** (ERP `form.creator - form.created_time`) + badge trạng thái
- Chế độ chỉ đọc: thêm ô **"Ghi chú không duyệt"**, ẩn dấu `*` bắt buộc
- Phiếu đã lưu lấy **người lập / phòng ban của chính phiếu**, không phải người đang đăng nhập (mở phiếu người khác mà hiện tên mình là sai)

**Verify** (`scratchpad/so_form_vs_chitiet.js` — render cả 2 chế độ rồi so nhãn + khối):

```
Khối card   — Sửa: Thông tin chung | Chi tiết      ⇄  Chi tiết: Thông tin chung | Chi tiết   ✓
Nhãn        — Sửa: Loại phiếu · Mã phiếu · Người lập · Phòng ban · Diễn giải
              Chi tiết: … y hệt … + Ghi chú không duyệt                                      ✓
Bảng nhận đúng cờ readonly                                                                   ✓
```

Regression: FE 8/8 compile sạch · đếm cột 6/6 biến thể đủ cột · BE 34/34.

### Việc còn lại (không chặn)
- [x] **Xem lại trên trình duyệt** (Phase 8–12 chưa nhìn tận mắt) — user tự test
- [x] User bấm lại để xác nhận, nhất là: bản in nhiều nhóm (ngắt trang), xuất Excel tải file thật, luồng từ chối bằng tài khoản có quyền `Kế toán thanh toán` không phải Super admin
- [ ] Cân nhắc bổ sung nút "Chọn nhanh hợp đồng" nếu nghiệp vụ cần
- [ ] Khi port màn **Phiếu báo có**: nhớ thêm cột checkbox (chỉ hiện khi `money_remain > 0`, phiếu loại KH + trạng thái 2) và nút *"Tạo phiếu yêu cầu điều chỉnh công nợ"* trỏ sang `/finance/bill-adjust-dept-requests/create?bill_income_report_detail_ids=`
- [ ] Dọn 6 phiếu test khi nghiệm thu xong: chạy lại seeder rồi xoá, hoặc `DELETE ... WHERE code LIKE 'TEST.DNDCCN%'` (seeder tự dọn 2 cấp chi tiết + log)
- [ ] Môi trường khác phải chạy migration `2026_08_16_000001_create_catalog_histories_table` trước khi dùng luồng ghi

---

## Phase 13 — Test Playwright toàn bộ trường hợp (TH1–TH19) ✅ XONG 2026-08-17

User yêu cầu: *"test playwright thật kỹ lại tất cả các trường hợp, test chi tiết từng logic,
trường hợp 1 nhé. nếu thiếu dữ liệu thì viết seeder tạo dữ liệu test"*.

Trước khi test đã **nâng cấp seeder** để các dòng chi tiết mang **hợp đồng thật có công nợ**
(KH: `HĐ-TEST-DNTT-11/12/15` — 6,53 tỷ / 5,93 tỷ / 3,50 tỷ · NCC: `PI: HHC18290` — số dư 269,4 tỷ).

### Kết quả từng trường hợp

| TH | Nội dung | Kết quả |
| --- | --- | --- |
| 1 | Màn danh sách: 13 cột, dữ liệu, badge trạng thái | ✅ |
| 2 | Màn "Chờ duyệt" (`?mode=pending`) | ✅ |
| 3 | Màn chi tiết phiếu KH | ❌ → **sửa**: cột "Số dư cuối kỳ" luôn 0 |
| 4 | Màn sửa | ✅ |
| 5 | Gửi duyệt | ✅ |
| 6 | Từ chối (bắt buộc lý do, ghi người duyệt) | ✅ |
| 7 | Lịch sử | ❌ → **sửa**: hiện chữ thô `change_status` |
| 8 | In phiếu (14 cột ngoại tệ, quy đổi) | ✅ |
| 9 | Tạo phiếu bằng tay + chọn hợp đồng | ✅ |
| 10 | Tạo từ phiếu báo có + **đổi loại phiếu** | ❌ → **sửa**: đổi loại xoá sạch bảng |
| 11 | Lưu phiếu NCC ngoại tệ (2 vế tiền) | ✅ |
| 12 | Chi tiết phiếu NCC ngoại tệ (số dư USD/VNĐ) | ✅ |
| 13 | Xóa phiếu (xóa kèm 2 cấp chi tiết + ghi log) | ✅ |
| 14 | 11 ô lọc + phân trang + sắp xếp | ❌ → **bổ sung**: thiếu sắp xếp cột Số tiền |
| 15 | Chạy lại toàn bộ script cũ (hồi quy) | ✅ 76/76 |
| 16 | Popup Lịch sử ở màn danh sách + bộ lọc | ✅ |
| 17 | Khối Lịch sử ở màn chi tiết | ✅ |
| 18 | Quyền `Kế toán thanh toán` (KHÔNG Super admin) | ✅ 12/12 |
| 19 | Trang in | ✅ (logo không có file ở máy dev) |

### 4 lỗi đã sửa trong đợt này

**1. Cột "Số dư cuối kỳ" luôn bằng 0 (TH3).** `BillAdjustDeptRequestDetailResource` không trả
`remain_debt`. Thêm `BillAdjustDeptRequestService::attachRemainDebt()` — port `getDataForEdit()`
của ERP, gom tất cả cặp (id hợp đồng, loại) của **cả 2 cấp** rồi tra bằng **một** query.
Sau khi sửa: 6.530.125.000 / 5.929.766.250 / 3.503.592.820.

**2. Lịch sử hiện chữ thô `change_status` (TH7).** `CatalogHistoryService::ACTION_LABELS` thiếu
khóa. Thêm nhãn *"Thay đổi trạng thái"* + màu `#d97706` (sửa cộng thêm, không đụng khóa cũ).

**3. Đổi loại phiếu XOÁ SẠCH bảng chi tiết (TH10) — nặng nhất.** ERP `onRequestTypeChange()`
(`create.blade.php` :209-231) **giữ nguyên** phiếu báo có + các dòng, chỉ:
- sang NCC + có phiếu báo có → lấy **tiền tệ + tỷ giá của phiếu báo có**, gán NCC mặc định
  *"KHÁCH KHÔNG RÕ"* cho dòng chưa có đối tượng;
- về KH → bỏ tiền tệ + tỷ giá;
- **remap vế tiền** (`remapMoneyOld()`): KH dùng số VNĐ, NCC-ngoại tệ dùng số nguyên tệ.

Bản port lại xoá `bill_income_report_id` + `form.details` → **mất trắng dữ liệu vừa nạp từ phiếu
báo có**, đúng luồng chính của màn. Đã viết lại bám ERP; mỗi dòng giữ 2 vế `_money_old_vnd` /
`_money_old_foreign` để đổi qua lại. Tên KH mặc định lấy từ BE (`undefined_customer_name`) thay vì
viết cứng như ERP.

Kiểm lại: `?bill_income_report_detail_ids=7105` → đổi sang NCC giữ nguyên phiếu `TPE.PBC0426.00046`,
tiền tệ USD, tỷ giá 26.015, NCC `29TPHPTH-203 - KHÁCH KHÔNG RÕ`, tiền 5.672 (nguyên tệ) ⇄ 147.557.080.

**4. Thiếu sắp xếp cột "Số tiền" (TH14).** ERP mở `orderable` cho **đúng một cột** này
(`index.blade.php` :46-58); bản port bỏ qua `sort_by` nên bấm sort không đổi gì. Thêm
`BillAdjustDeptRequest::SORTABLE_COLUMNS` (whitelist 1 khóa) + `sortable: true` ở FE. Cột ngoài
whitelist bị bỏ qua, luôn chốt `id DESC` cuối cùng để lật trang không lặp/mất bản ghi.

### Verify

- Bộ lọc: **19/19** (`scratchpad/verify_filters.php` — mỗi ô lọc đối chiếu SQL tương đương)
- Quyền kế toán: **12/12** (`scratchpad/verify_accountant.php`, chạy 2 tiến trình riêng — auth guard
  chỉ resolve một lần mỗi tiến trình nên 2 token trong cùng tiến trình sẽ chạy chung danh tính)
- Hồi quy: BE 34/34 + 15/15 + 22/22 + 5/5 · liên-người-dùng 5/5 · FE compile sạch

### Dọn dữ liệu test
Đã xoá các phiếu sinh ra khi test (10286, 10294, 10295, 10297, 10299, 10300) + log của chúng; chạy
lại seeder nên bộ dữ liệu test về đúng 6 phiếu `TEST.DNDCCN.00001-00006` (3 trạng thái × 2 loại).
Phiếu `TPE.DNDCCN0826.00003` ("DIễn giải test") **giữ nguyên** — do bạn tự tạo trên trình duyệt.

### Checkpoint — 2026-08-17
Vừa hoàn thành: TH1–TH19 + sửa 4 lỗi (số dư, nhãn lịch sử, đổi loại phiếu, sắp xếp cột Số tiền)
Đang làm dở: không
Bước tiếp theo: bạn mở trình duyệt nghiệm thu; cân nhắc nút "Chọn nhanh hợp đồng" nếu nghiệp vụ cần
Blocked:

## Phase 14 — Bổ sung nút xuất Excel danh sách ✅ XONG 2026-08-17

User hỏi lại: *"bạn chưa bổ sung xuất excel ở màn danh sách à?"* — đúng. BE đã có sẵn
`/export-list` + `BillAdjustDeptRequestListExport` + blade từ Phase 5, nhưng **FE chỉ có xuất từng
phiếu** trong menu `⋮`; thiếu hẳn nút xuất cả danh sách.

ERP có nút này (`index.blade.php` :94 `export_link` + :97-103 `.export-button`) và **gộp bộ lọc
đang chọn** vào link trước khi tải.

**Đã thêm:** nút `V2BaseButton secondary` (icon `ri-file-excel-2-line`) cạnh nút Tạo mới, dùng
helper chung `downloadExcel`. Gửi `...filters` + `mode`, **bỏ `page`/`per_page`** để file chứa toàn
bộ kết quả lọc chứ không riêng trang đang xem; cờ `exporting` khoá nút trong lúc chờ.

**Verify** (`scratchpad/verify_export_list.php` — tải file thật rồi đọc bằng PhpSpreadsheet): 6/6
— lọc trạng thái 3/3 · lọc loại phiếu NCC 10/10 và mọi dòng đúng loại · lọc mã phiếu 6/6 ·
chế độ Chờ duyệt chỉ một trạng thái · không lọc thì chặn trần 5.000 dòng.
Bấm thật trên trình duyệt: tải về `Danh-sach-yeu-cau-dieu-chinh-cong-no-2026-08-17.xlsx`
(13 cột, đúng tiêu đề).

Cùng lúc: **bỏ badge trạng thái + "người tạo - ngày tạo"** ở header card "Thông tin chung" của màn
XEM CHI TIẾT theo yêu cầu user (màn Tạo/Sửa giữ nguyên như ERP).

---

## Phase 15 — Rà trạng thái phiên làm việc ✅ 2026-08-18

Không đụng code. Kiểm lại nhánh + tình trạng repo trước khi làm tiếp:

- [x] Cả 2 repo đang đứng trên nhánh `gop_db` (đúng quy tắc phần gộp DB)
- [x] **Đính chính**: code feature **ĐÃ COMMIT**, không còn nằm ở working tree như các phase trước ghi
  - `hrm-api`: `757a9baf7 phiếu yêu cầu điều chỉnh công nợ` → `30f3578a5 fix lich su` → `e04418092 fix quyen`
  - `hrm-client`: `c96c87f62 phiếu yêu cầu điều chỉnh công nợ` → `53bf38cd0 fix lich su`
- [x] Working tree sạch (`hrm-api` 0 file; `hrm-client` chỉ lệch `package-lock.json`, không liên quan feature)
- [x] Xác nhận file thật còn đủ: BE 22 file `BillAdjustDept*` trong `Modules/Finance`, FE 7 file trong
  `pages/finance/bill-adjust-dept-requests/`

### Việc còn lại (giữ nguyên từ Phase 14, chưa việc nào được làm thêm)
- [x] User nghiệm thu trên trình duyệt — bản in nhiều nhóm (ngắt trang), xuất Excel danh sách, luồng từ chối bằng tài khoản `Kế toán thanh toán` (không phải Super admin)
- [ ] Nút **"Chọn nhanh hợp đồng"** (popup chọn nhiều HĐ một lượt) — ERP có, bản port chưa làm, chờ user chốt có cần không
- [ ] Dọn 6 phiếu test `TEST.DNDCCN.00001-00006` khi nghiệm thu xong
- [ ] Khi port màn **Phiếu báo có**: thêm cột checkbox (chỉ hiện khi `money_remain > 0`, phiếu loại KH + trạng thái 2) + nút *"Tạo phiếu yêu cầu điều chỉnh công nợ"* trỏ sang `/finance/bill-adjust-dept-requests/create?bill_income_report_detail_ids=`
- [ ] Môi trường khác: chạy migration `2026_08_16_000001_create_catalog_histories_table` trước khi dùng luồng ghi
- [ ] Chưa sinh SRS / testcase / HDSD cho màn này

### Checkpoint — 2026-08-18
Vừa hoàn thành: rà trạng thái nhánh + repo, đính chính "chưa commit" → đã commit ở cả 2 repo
Đang làm dở: không — code 15 phase đã xong và đã commit
Bước tiếp theo: user nghiệm thu trên trình duyệt; nếu nghiệp vụ cần thì làm nút "Chọn nhanh hợp đồng"
Blocked:

---

## ✅ FEATURE HOÀN THÀNH — 2026-08-18

User chốt chuyển trạng thái sang **Hoàn thành**. Entry trong `.plans/gop-db/STATUS.md` đã chuyển từ
mục *Đang làm* → *Hoàn thành*.

Các việc mở còn lại **không chặn** và không thuộc phạm vi feature nữa:
- Nút "Chọn nhanh hợp đồng" của ERP — mở lại thành task riêng nếu nghiệp vụ cần
- Sinh SRS / testcase / HDSD cho màn này
- Dọn 6 phiếu mẫu `TEST.DNDCCN.00001-00006` trên DB local khi không cần nữa
- Khi port màn **Phiếu báo có**: thêm checkbox chọn dòng + nút *"Tạo phiếu yêu cầu điều chỉnh công nợ"*
- Môi trường khác: chạy migration `2026_08_16_000001_create_catalog_histories_table` trước khi dùng luồng ghi

---

## Phase 16 — Feedback nghiệm thu màn danh sách (2026-08-18)

User rà màn danh sách sau nghiệm thu, báo 6 điểm. Đều nằm ở **màn danh sách**
(`pages/finance/bill-adjust-dept-requests/index.vue`) + resource/entity phía BE.

**Chốt với user trước khi code:**
- Sort mở cho **Mã phiếu + cả 3 cột ngày** (Ngày tạo, Ngày cập nhật, Ngày nhận)
- 2 cột mới (Ngày cập nhật, Người cập nhật) **mặc định HIỆN**

### BE — `hrm-api`
- [x] `BillAdjustDeptRequest`: thêm quan hệ `employee_update` (`belongsTo Employee, updated_by`)
- [x] `BillAdjustDeptRequest::SORTABLE_COLUMNS`: thêm `code`, `createdAt`, `updatedAt`, `sendApproveDate`
      (ghi rõ đây là **mở rộng có chủ đích so với ERP** — ERP chỉ cho sort cột Số tiền)
- [x] `BillAdjustDeptRequestListResource`: `created_at` đổi `d/m/Y` → **`d/m/Y H:i`**
- [x] `BillAdjustDeptRequestListResource`: thêm `updated_at` (`d/m/Y H:i`) + `updated_by` + `updated_by_name`
- [x] `BillAdjustDeptRequestService`: eager load `employee_update.info` (chặn N+1)

### FE — `hrm-client`
- [x] Gắn `columnCustomizationMixin` + `columnScreenKey = 'bill_adjust_dept_requests'`
      (BE lưu key-value ở `user_column_settings` → **không cần migration**)
- [x] Đổi computed `tableColumns` → `allColumns`; khoá `index` / `code` / `actions` bằng `locked: true`
- [x] Nút **Cấu hình cột hiển thị** (`ri-layout-column-line`) + đặt `<ColumnCustomizationModal>`
- [x] `mounted`: `await loadColumnFields()` TRƯỚC `loadData()`
- [x] Thêm 2 cột **Ngày cập nhật** / **Người cập nhật** (mặc định hiện) + 2 template cell
- [x] `sortable: true` cho `code`, `createdAt`, `updatedAt`, `sendApproveDate`
- [x] Đổi nhãn **Ngày lập → Ngày tạo**, **Người lập → Người tạo** (cả cột bảng lẫn bộ lọc:
      "Ngày lập từ/đến", "Người lập", placeholder, tiêu đề nhóm lọc)
- [x] Nút **Xuất Excel** đổi `secondary` → `secondary status="success"` (xanh lá — skill button-convention §2b)

### Verify
- [x] `php -l` sạch cho file BE sửa
- [x] Compile template + script FE sạch
- [x] SQL: sort 4 khoá mới trả đúng thứ tự; khoá lạ không đổi kết quả
- [x] User mở trình duyệt nghiệm thu (FE không tự test bằng Playwright)

### Ngoài danh sách 6 việc — làm thêm cho nhất quán
- [x] Blade `exports/bill_adjust_dept_request_list.blade.php`: header cột đổi *Ngày lập/Người lập*
      → *Ngày tạo/Người tạo* (file Excel dùng lại đúng mảng của ListResource nên cột Ngày tạo
      **tự có giờ:phút** theo mục 3, không phải sửa gì thêm)

- [x] Nhãn **"Người lập"** trong form tạo/sửa (`BillAdjustDeptRequestForm.vue` :51) → **"Người tạo"**
      (user chốt 2026-08-18, sau khi hỏi lại)

### CỐ Ý KHÔNG ĐỔI — cần user xác nhận nếu muốn đổi
- Nhãn **"Người lập:"** trên bản in phiếu (`_id/print.vue` :35) và blade in của BE — đây là **ô chữ ký**
  trên chứng từ kế toán, đổi chữ là lệch mẫu chứng từ
- File Excel danh sách **không thêm** 2 cột Ngày/Người cập nhật, và **không chạy theo cấu hình cột**
  của user — giữ đúng tiền lệ đã chốt ở màn Khách hàng (file xuất giữ bộ cột cố định)

### Kết quả verify (2026-08-18)
- `php -l` sạch: Entity · ListResource · Service
- Compile FE sạch (vue-template-compiler + @babel/parser) — hrm-client không có ESLint config
- SQL sort thật (đăng nhập id 13): `code / createdAt / updatedAt / sendApproveDate / totalAmount`
  ra đúng `order by <cột> asc, id desc`; khoá lạ (`hack_col`) và khoá rỗng đều rơi về
  `created_at desc, id desc` — không nhét chuỗi lạ vào ORDER BY
- Resource thật 10 dòng: `created_at` / `updated_at` ra `17/08/2026 16:45`, `updated_by_name` có dữ liệu
- **Không N+1**: `employees` và `employee_infos` đều nạp theo lô `in (...)`, tổng 34 query/trang
  (12 query `master_settings` là nhiễu sẵn có của hệ thống, không thuộc màn này)
- Endpoint lưu cấu hình cột chạy đúng với khoá `bill_adjust_dept_requests` (đã xoá bản ghi thử nghiệm)

### Checkpoint — 2026-08-18
Vừa hoàn thành: 6 việc feedback màn danh sách (BE 3 file + 1 blade, FE 1 file), verify BE bằng dữ liệu thật
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt nghiệm thu — bấm nút Tùy chỉnh cột (tick/bỏ tick + kéo thứ tự, F5 xem có giữ), bấm sort 4 cột mới, kiểm giờ:phút ở 2 cột ngày, xem màu nút Xuất Excel
Blocked:

---

## Phase 17 — Bản in bám nguyên mẫu ERP (2026-08-18)

User báo *"màn in phiếu form, font chữ các thứ chưa giống với bên erp"*.

**Gốc rễ tìm được:** ERP nạp `erp/public/css/pdf.css` — file này đặt
`body { font-family: Times New Roman !important; font-size: 16px }` +
`td, th { border: 1px solid black; padding: 5px 8px }`. **`hrm-client/static/css/` KHÔNG có
`pdf.css`** (plugin `print-content.js` :10 khai nạp nhưng file không tồn tại) → cửa sổ in HRM thiếu
toàn bộ rule đó. Chữ vẫn ra Times New Roman nhờ `editor.css` (`body.document-editor`), nhưng cỡ chữ
và rule bảng thì lệch; còn **preview trên trình duyệt** thì lệch hẳn vì nằm trong khung app
(`v2-styles`, Nunito Sans, full width) trong khi ERP dựng trang giấy 297mm.

**Nguồn chuẩn đã đối chiếu:** `report_templates` id 209 · `buildCustomerPrintTable()` /
`buildSupplierPrintTable()` (`erp/app/Model/IncomeExpenditure/BillAdjustDeptRequest.php`) ·
`erp/public/css/pdf.css` · `erp/resources/views/print_landscape.blade.php`.

**User chốt: copy Y NGUYÊN ERP** (kể cả lỗi của mẫu ERP).

### FE — `_id/print.vue` (viết lại)
- [x] Preview dựng thành **trang giấy** như `print_landscape.blade.php`: nền xám, tờ 297mm,
      lề 15mm, viền + bóng, Times New Roman 16px. Style bọc trong `.bill-adjust-print`
      (KHÔNG scoped nhưng cũng KHÔNG để `#content` trần — style Nuxt là toàn cục, sẽ đè màn in khác)
- [x] Cửa sổ in: tự bù phần `pdf.css` còn thiếu trong `options.styles`
      (TNR 16px · `td,th{border:1px solid black;padding:5px 8px}` · `.no-border td{border:none}` · `.block{avoid}`)
- [x] **KHÔNG** thêm `/css/pdf.css` vào `static/` — tài sản dùng chung, thêm là đổi bản in của mọi màn khác
- [x] Tiêu đề 18px · dòng ngày 18px, **bỏ in nghiêng**, đổi thành *"Ngày dd Tháng mm Năm yyyy"*
- [x] Letterhead đổi `max-height: 90px` → `width: 100%` như ERP
- [x] Khối thông tin còn **đúng 5 trường ERP**: Mã phiếu · Mã phiếu báo có · Người tạo · Phòng ban ·
      Diễn giải → **bỏ** *Loại phiếu* và *Tỷ giá*
- [x] **Bỏ dòng "Tổng cộng"** (bảng in ERP không có)
- [x] Bảng chi tiết: `<td>` ở thead + `<b>` như ERP · bỏ `colgroup` + `table-layout: fixed`
      (ERP để cột tự co) · ô đối tượng căn giữa, ô hợp đồng/NVKD `vertical-align: top`, tiền căn phải
- [x] Khối chữ ký thay 2 ô bằng **nguyên khối 6 ô của ERP** + dòng ngày tháng bên phải

### Cố ý giữ lỗi của mẫu ERP (user chốt — đừng "sửa cho đúng")
- Hàng trên khối chữ ký khai 5 `<td>` nhưng hàng dưới có 6
- **"NGƯỜI NỘP TIỀN" lặp 2 lần** (ô 3 và ô 5)
- **"THỦ QUỸ" để `font-size: 1px`** nên gần như tàng hình
- **"BAN GIAM ĐỐC"** thiếu dấu sắc
- Dòng *Diễn giải* chỉ có 1 `<td>` (không colspan) nên với `table-layout: fixed` chỉ chiếm nửa trang trái

### CỐ Ý KHÁC ERP — 2 chỗ, đã báo user
1. Giữ `page-break-inside: avoid` cho từng nhóm ô gộp (mỗi nhóm 1 `<tbody>`). Mẫu ERP để
   `page-break-inside: auto` nên phiếu dài sẽ có **ô gộp TRỐNG ở đầu trang sau** (skill print-page §5).
   Không nhìn thấy khác biệt khi phiếu vừa 1 trang.
2. Số tiền vẫn định dạng **vi-VN** (`1.234.567`), ERP dùng `number_format` kiểu Anh (`1,234,567`).
   Đổi thì lệch với toàn bộ màn khác của HRM → chờ user chốt.

### Thêm đơn vị tiền vào tiêu đề cột (user yêu cầu 2026-08-18)
User: *"trên header thêm đơn vị tiền vào giúp tôi nữa"* → chốt: đặt vào **tiêu đề cột**, không phải
khối thông tin đầu phiếu.

- [x] `BillAdjustDeptRequestPrintResource::columns()`:
      · KH → `Số tiền` → **`Số tiền (VNĐ)`**
      · NCC nội tệ → `Số dư` / `Số tiền` → **`Số dư (VNĐ)` / `Số tiền (VNĐ)`**
      · NCC ngoại tệ → giữ nguyên (vốn đã có `(USD)` / `(VNĐ)`)
- [x] Cột `Số dư` của NCC nội tệ cũng ghi đơn vị: để 1 cột có đơn vị 1 cột không thì đọc như 2 loại
      tiền khác nhau; khuôn ngoại tệ vốn đã ghi cả 2
- [x] **File Excel phiếu tự ăn theo** — `BillAdjustDeptRequestExport` dùng chung
      `BillAdjustDeptRequestPrintResource`, blade lặp `$data['columns']`
- [x] Verify trên 30 phiếu thật, đủ 3 khuôn:
      `customer` · `supplier` · `supplier_fx` đều ra nhãn đúng
- ⚠️ Mẫu ERP để trống đơn vị → đây là chỗ HRM **cố ý** khác ERP theo yêu cầu user

### Chưa đụng — chờ user chốt
- [ ] File **Excel phiếu** (`exports/bill_adjust_dept_request.blade.php`) vẫn còn *Loại phiếu* ·
      *Người lập* · *Tỷ giá* · *Tổng cộng* · khối ký 2 ô — tức lệch ERP y như bản in trước khi sửa.
      ERP dùng chung 1 mẫu cho cả in lẫn Excel. Có đồng bộ nốt không?

### Bug phát sinh khi đổi font — MẤT CHỮ ĐẬM (fix 2026-08-18)
User báo *"sao tôi không thấy in đậm các thứ vậy?"*.

**Gốc rễ:** `assets/scss/custom/components/_reboot.scss` :21 đặt TOÀN CỤC
`b, strong { font-weight: $font-weight-medium }` = **500**. Times New Roman chỉ có 2 nét
(Regular + Bold), KHÔNG có nét 500 → trình duyệt rơi về **Regular**, chữ đậm mất sạch
(tiêu đề, nhãn trường, đầu bảng). Trước đây màn dùng Nunito Sans (font nhiều nét) nên 500 vẫn
trông hơi đậm → lỗi chỉ lộ ra sau khi đổi sang Times New Roman ở Phase 17.

- [x] Preview: thêm `b, strong { font-weight: 700 }` trong khối `.bill-adjust-print #content`
      (specificity 1-1-0 > 0-0-1 của `_reboot.scss` nên thắng chắc)
- [x] Cửa sổ in: thêm `#content b, #content strong { font-weight: 700 !important }` vào `options.styles`
- [x] **KHÔNG sửa `_reboot.scss`** — file dùng chung toàn project (CLAUDE.md). Ghi nhận để user quyết:
      31 màn `print.vue` khác cũng dùng Times New Roman, màn nào chỉ dựa vào `<b>`/`<strong>` trần
      mà không tự khai `font-weight` thì đang dính đúng lỗi này.

### Bug phát sinh — SỐ TIỀN BỊ NGẮT XUỐNG DÒNG (fix 2026-08-18)
User báo *"số tiền nó đang bị ngắt xuống dòng"*. **Do mình tự thêm, không phải của ERP.**

**2 gốc rễ:**
1. `word-break: break-word` đặt cho mọi `td/th` (bê từ file cũ sang; `pdf.css` của ERP KHÔNG có).
   Bảng để auto-layout, khi bảng chật thì rule này cho phép cắt **giữa con số** — `1.234.567` rớt dòng.
2. Preview đặt `#content { width: 297mm; max-width: 100% }`. Màn hẹp hơn 297mm thì `max-width`
   **bóp tờ giấy nhỏ lại** → cột co → chữ xuống dòng khác hẳn bản in thật.

- [x] Bỏ `word-break` / `overflow-wrap` khỏi `td, th` ở CẢ preview lẫn `options.styles` (về đúng ERP)
- [x] Thêm `td.money-cell { white-space: nowrap }` + gắn class cho **8 ô tiền**
      (Số dư · Số dư VNĐ · Số tiền · Số tiền VNĐ, mỗi bên 4 ô)
- [x] Bỏ `max-width: 100%` ở `#content`, chuyển sang `overflow-x: auto` trên `.bill-adjust-print`
      → tờ giấy luôn đúng 297mm, màn hẹp thì cuộn ngang (đúng cách `print_landscape.blade.php` làm)

### Verify
- [x] Compile sạch: template + script + scss
- [x] SCSS biên dịch ra đúng `.bill-adjust-print #content b, … strong { font-weight: 700 }`
      và `.bill-adjust-print #content td.money-cell { white-space: nowrap }`
- [x] Không còn rule `word-break` nào hoạt động trong file (chỉ còn dòng ghi chú cảnh báo)
- [x] User mở trình duyệt đối chiếu trực tiếp với bản in ERP

### Checkpoint — 2026-08-18
Vừa hoàn thành: viết lại `_id/print.vue` bám nguyên mẫu ERP id 209
Đang làm dở: không
Bước tiếp theo: user mở 1 phiếu → bấm In, đối chiếu cạnh bản in ERP; chốt 2 chỗ cố ý khác + Excel phiếu
Blocked:

---

## Phase 18 — Lưu nháp chỉ bắt buộc "Loại phiếu" (2026-08-24)

User báo: *"finance/bill-adjust-dept-requests/create màn này lưu nháp cũng chỉ bắt validate trường
loại phiếu cho tôi thôi"*.

**Hiện trạng (trước fix)** — bấm **Lưu nháp** vẫn bị chặn bởi 3 luật ở FE và 8 rule ở BE:

| Nơi chặn | Luật |
| --- | --- |
| FE `validateBeforeSubmit()` | Diễn giải bắt buộc · phải có ≥1 dòng điều chỉnh · tỷ giá > 0 |
| BE `BillAdjustDeptRequestStoreRequest` | `note` required · `details` required min:1 · `details.*.money_old` required gt:0 · `details.*.items` required min:1 · `items.*.money_new` required gt:0 · `customer_old_id` / `customer_new_id` (hoặc `supplier_new_id`) required · `currency_id` required (loại NCC) · `exchange_rate` required gt:0 (ngoại tệ) |

⇒ Lệch quy ước chung của team (`.claude/skills/form-validate` mục 1: *"Lưu nháp mọi trường đều được
bỏ trống"*, required khác do BE quyết **theo `status`*).

**Chốt phạm vi:** chỉ nới cho `status = 1` (Lưu nháp). `status = 2` (Gửi duyệt) giữ nguyên đủ luật —
kể cả luật khớp tổng tiền và luật trùng đối tượng.

### Bẫy phải xử cùng lúc (nếu không sẽ đổi lỗi 422 thành lỗi 500)

3 cột **NOT NULL không có default** sẽ nhận `null` khi lưu nháp dở dang:
`bill_adjust_dept_request_details.customer_old_id` · `.customer_old_name` ·
`bill_adjust_dept_request_detail_items.customer_new_id` · `.customer_new_name`
(`money_old` NOT NULL nhưng `self::money()` đã trả 0). MySQL của máy dev **không bật
`STRICT_TRANS_TABLES`**, nhưng INSERT 1 dòng ghi thẳng `NULL` vào cột NOT NULL vẫn nổ 1048 →
phải tự ép `0` / `''` như nhánh NCC đang làm.

Ép `0` lại sinh bẫy thứ 2: mở lại phiếu nháp rồi lưu tiếp → `sameTarget(0, 0) = true` →
báo oan *"Khách hàng điều chỉnh đến trùng với khách hàng điều chỉnh từ"*.

### BE
- [x] `BillAdjustDeptRequestStoreRequest::rules()` — rẽ theo `status`: nháp thì `note` ·
      `details` · `money_old` · `items` · `money_new` · `customer_old_id` · `customer_new_id` ·
      `supplier_new_id` · `currency_id` · `exchange_rate` đều `nullable` (giữ nguyên rule ĐỊNH DẠNG:
      `integer` / `numeric` / `array`). Gửi duyệt giữ y nguyên rule cũ
- [x] `BillAdjustDeptRequestWriteService::syncDetails()` — nhánh khách hàng ép
      `customer_old_id ?? 0`, `customer_old_name ?? ''`, `customer_new_id ?? 0`, `customer_new_name ?? ''`
      (bám đúng cách nhánh NCC đang làm)
- [x] `sameTarget()` — coi `0` / `''` là RỖNG, không phải "trùng nhau"
- [x] `BillAdjustDeptRequestDetailResource` — trả `customer_old_id` / `customer_new_id` = `null`
      khi giá trị là 0 để FE không hiện đối tượng ma và không gửi ngược 0 lên

### FE (`BillAdjustDeptRequestForm.vue`)
- [x] `validateBeforeSubmit(status)` — nháp chỉ kiểm **Loại phiếu**; 3 luật cũ (diễn giải · ≥1 dòng ·
      tỷ giá) chuyển vào nhánh `status === 2`
- [x] Cờ `touched` chỉ bật khi **Gửi duyệt** → bấm Lưu nháp không tô đỏ Diễn giải / tỷ giá / bảng

### Verify
- [x] `php -l` 4 file BE · parse template + script FE
- [x] Gọi API thật: lưu nháp form TRỐNG (chỉ `request_type`) → 200, phiếu vào DB, không 500
- [x] Lưu nháp có 1 dòng chi tiết chưa chọn khách → 200; mở lại sửa rồi lưu nháp tiếp → vẫn 200
      (không dính bẫy `sameTarget(0,0)`)
- [x] Gửi duyệt phiếu thiếu diễn giải → vẫn 422 đúng như trước
- [ ] User mở trình duyệt bấm tay 2 nút

### Checkpoint — 2026-08-24
Vừa hoàn thành: Phase 18 — Lưu nháp chỉ bắt buộc "Loại phiếu" (3 file BE + 1 file FE)
Đang làm dở: không
Bước tiếp theo: user mở `/finance/bill-adjust-dept-requests/create` → bấm **Lưu nháp** với form trống
(chỉ chọn Loại phiếu) xem có lưu được không, rồi thử **Gửi duyệt** xem còn chặn đủ luật
Blocked:

**Đã tự kiểm bằng script (18/18 ca PASS, ghi trong transaction rồi rollback — DB không còn dòng nào):**
`php -l` 3 file BE sạch · parse template + script FE sạch · nháp trống / nháp có dòng chi tiết trống /
nháp NCC ngoại tệ thiếu tỷ giá đều KHÔNG lỗi · thiếu Loại phiếu vẫn lỗi · gửi duyệt vẫn bắt đủ
`note` + `details` + khách hàng 2 vế + tiền > 0 + tỷ giá · ghi DB không dính 1048 · mở lại phiếu nháp
lưu tiếp không báo oan "trùng khách hàng" · trùng khách hàng THẬT vẫn chặn · cổng gửi duyệt ngoài
danh sách chặn phiếu nháp trống và cho qua phiếu đủ dữ liệu.

**Lỗ hổng vá kèm (do nới nháp mà lộ ra):** trước Phase 18, nút **Gửi duyệt ở màn danh sách / chi tiết**
(`changeStatus`) chỉ kiểm TỔNG TIỀN. Nháp nới ra rồi thì đó thành đường vòng qua mặt mọi luật còn lại
⇒ `validateTotalsOfSavedModel()` nay kiểm thêm: diễn giải · tỷ giá (NCC ngoại tệ) · khách hàng "từ" ·
đối tượng "đến" · số tiền 2 vế > 0.

---

## Phase 19 — 2 điểm nghiệm thu màn tạo/sửa (2026-08-24)

### 19.1 Bỏ dòng "{Người tạo} - {ngày tạo}" ở góc card "Thông tin chung"
User: *"DNS Admin bỏ text này trên card đi cho tôi"*.

- [x] `BillAdjustDeptRequestForm.vue` — xoá `<span>{{ createdInfo }}</span>` ở `card-header`
- [x] Xoá luôn computed `createdInfo` (không còn nơi dùng — đã grep cả thư mục màn)
- [x] **GIỮ** badge trạng thái bên cạnh (user chỉ chỉ vào phần chữ "DNS Admin - …")
- ℹ️ Thông tin người tạo vẫn còn nguyên ở ô **"Người tạo"** trong thân form, không mất dữ liệu gì

### 19.2 Bảng chi tiết: dùng `V2BaseTableScroll` như màn Yêu cầu bảo hành sửa chữa
User: *"bảng chi tiết chưa có scroll ngang bên trên à"* → sau đó chốt tiếp: *"dùng table như màn
`/customer-care/warranty-repair-requests/create` này, khi chưa có dữ liệu thì bảng chiếm ít chiều
cao như này thôi"*.

**2 vấn đề cùng 1 gốc — class `.table-responsive`:**

| Vấn đề | Gốc |
| --- | --- |
| Không có thanh cuộn ngang ở trên | `.table-responsive` chỉ có thanh cuộn dưới; bảng rộng 12 cột (KH) → 16 cột (NCC ngoại tệ) |
| Bảng trống vẫn cao ~429px | `assets/scss/default.scss` ép `.table-responsive { min-height: 50vh }` — hợp với màn danh sách, sai với bảng trong form (skill `form-validate` mục 1c đã ghi nhận) |

⇒ Thay `.table-responsive` bằng **`components/V2BaseTableScroll.vue`** — đúng thứ màn
`warranty-repair-requests/create` đang dùng: thanh cuộn ngang ở CẢ TRÊN LẪN DƯỚI, tự ẩn khi bảng
không tràn, và không dính rule `min-height: 50vh`.

- [x] `AdjustDetailTable.vue` — bọc bảng bằng `<V2BaseTableScroll>`, bỏ `<div class="table-responsive">`
- [x] Import + đăng ký `V2BaseTableScroll`
- [x] Gỡ bản thanh cuộn TỰ CHẾ viết ở lượt trước (refs `topScroll`/`tableWrapper`, 3 hàm sync,
      hook `mounted`/`updated`/`beforeDestroy`, `data.scrollSyncing`, 2 khối SCSS) — component dùng
      chung làm tốt hơn: có `ResizeObserver`, tự ẩn thanh khi bảng vừa khung
- [x] Sửa ghi chú SCSS còn nhắc `.table-responsive`
- ℹ️ Bảng đã sẵn dòng trống *"Chưa có dòng điều chỉnh nào."* nên form mới vào chỉ còn cao bằng
      header + 1 dòng, giống hệt màn bảo hành sửa chữa
- ℹ️ Màn CHI TIẾT (`_id/index.vue`) dùng lại chính component này nên ăn theo, không phải sửa gì

### Verify
- [x] Parse sạch template + script cả 2 file `.vue`
- [x] Biên dịch SCSS sạch; grep xác nhận không còn sót ref/hàm/CSS của bản thanh cuộn tự chế
- [x] Grep toàn thư mục màn: không còn tham chiếu `createdInfo` nào
- [ ] User mở trình duyệt: card không còn dòng tên người tạo · form mới vào bảng chỉ cao bằng
      header + 1 dòng trống · kéo thanh cuộn trên thấy bảng chạy theo (và ngược lại), thử cả
      loại NCC ngoại tệ (16 cột)

### Checkpoint — 2026-08-24 (2)
Vừa hoàn thành: Phase 19 — bỏ text người tạo trên card + thêm thanh cuộn ngang trên bảng chi tiết
Đang làm dở: không
Bước tiếp theo: user bấm tay trên trình duyệt cả Phase 18 lẫn Phase 19
Blocked:

---

## Phase 20 — Fix: đổi đối tượng KHÔNG xoá hợp đồng đã chọn (2026-09-03)

User báo: *"trong bảng chi tiết chỗ điều chỉnh đến, khi chọn khách hàng và hợp đồng rồi sau đó
tôi chọn khách hàng khác thì thông tin hợp đồng,... chưa clear đi vẫn để thông tin của hợp đồng cũ"*.

### Gốc lỗi
`BillAdjustDeptRequestForm.vue :: applyParty()` chỉ gán `customer_*_id` / `customer_*_name`
(hoặc `supplier_*`), **không đụng tới các khoá hợp đồng của cùng dòng**.

ERP làm ngược lại — 4 chỗ đều có khối "đổi đối tượng thì reset hợp đồng":

| File ERP | Hàm | Xoá gì |
| --- | --- | --- |
| `partials/classes/IncomeExpenditure/BillAdjustDeptRequestDetail.blade.php:258` | `chooseCustomer` | `contractable_id/type`, `contract_old_id/code/created_by/type` |
| `…RequestDetailItem.blade.php:191` | `chooseCustomer` | `contractable_id/type`, `contract_new_id/code/created_by/type` |
| `…RequestDetail.blade.php:368` | `chooseSupplier` | + `buy_contract_old_*`, `balance_old = 0` |
| `…RequestDetailItem.blade.php:289` | `chooseSupplier` | + `buy_contract_new_*`, `balance_new/contract_value/remaining_debt = 0` |

Hậu quả không chỉ là hiển thị: popup hợp đồng lọc theo đối tượng
(`activeContractObjectId`), nên phiếu lưu xuống DB có cặp **khách hàng A + hợp đồng của khách
hàng B**, kèm `contractable_id` trỏ sai → sang bước tạo phiếu kế toán là ghi sổ nhầm công nợ.

### FE — `components/BillAdjustDeptRequestForm.vue`
- [x] Thêm `clearContractOf(row, side)` — xoá `contractable_id/type` + bộ khoá hợp đồng của đúng
      bên (`old`/`new`) và đúng loại phiếu (KH: `contract_*`; NCC: `buy_contract_*`), kèm các số
      liệu ăn theo hợp đồng (`balance_old/new`, `contract_value`, `remaining_debt`, `remain_debt`)
- [x] `applyParty()` gọi `clearContractOf()` **chỉ khi id đối tượng thực sự đổi** (chọn lại đúng
      đối tượng cũ thì giữ nguyên hợp đồng — đúng như ERP so `!=` trước khi reset)
- [x] Áp cho CẢ 2 bên "Điều chỉnh từ" và "Điều chỉnh đến" (cùng 1 hàm, ERP cũng làm cả 2 bên)

### CỐ Ý KHÁC ERP — 1 chỗ
ERP quên xoá `remain_debt` khi đổi khách hàng → cột **"Số dư cuối kỳ"** vẫn hiện số dư của hợp
đồng cũ dù ô hợp đồng đã trống. HRM xoá luôn (`remain_debt = 0`) vì đây chính là phần *"thông
tin hợp đồng,…"* user báo còn sót.

### Verify
- [x] Parse sạch template + script `BillAdjustDeptRequestForm.vue`
- [ ] User mở trình duyệt `/finance/bill-adjust-dept-requests/create`: dòng "Điều chỉnh đến" chọn
      KH → chọn HĐ → đổi sang KH khác ⇒ ô Hợp đồng, NVKD, Số dư cuối kỳ đều trống/0; chọn lại
      đúng KH cũ thì hợp đồng KHÔNG bị xoá; thử tiếp bên "Điều chỉnh từ" và phiếu loại NCC
      (ngoại tệ) xem Số dư / Giá trị HĐ / Công nợ còn lại có về 0 không

---

## Phase 21 — Lỗi lệch tổng tiền hiện INLINE ngay dưới đối tượng của nhóm (2026-09-03)

User: *"chỗ validate tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh từ phải thông báo
validate ngay xuống dưới của khách hàng nào luôn"*.

Hiện trạng: luật khớp tổng tiền chỉ bắn **1 toast chung**
(`validateBeforeSubmit()` — "Tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh từ"),
bảng có 5-10 nhóm thì user không biết nhóm nào lệch, phải tự dò dòng "Số tiền còn lại".

### FE — `components/AdjustDetailTable.vue`
- [x] Thêm prop `touched` (mặc định `false`) — bảng chưa hề có cờ này, trước giờ không có lỗi inline nào
- [x] Thêm `isGroupUnbalanced(detail)` = `touched && !readonly && |moneyRemaining(detail)| > 0.0001`
      (dùng lại `moneyRemaining()` sẵn có, cùng ngưỡng `0.0001` với `validateBeforeSubmit()` và BE)
- [x] Vị trí neo lỗi — **user chốt sau 2 lần đổi (2026-09-03)**: cột **Số tiền bên "Điều chỉnh đến"**,
      đặt ở **dòng cuối của nhóm** (ngay dưới cột số vừa được cộng lại, trên dòng "Số tiền còn lại").
      Hiện `invalid-feedback d-block` kèm số tiền còn thiếu/thừa. Chỉ 1 lần cho cả nhóm.
      *(Đã thử rồi bỏ: dưới ô Khách hàng bên "từ" → dưới ô Số tiền bên "từ".)*
- [x] SCSS: ô lỗi nằm trong `td.text-right` đang bị `white-space: nowrap` (rule cho số tiền) →
      thêm `td.text-right .invalid-feedback { white-space: normal; text-align: left }`, nếu không
      câu thông báo dài kéo cột tiền rộng ra và tràn bảng
- [x] Chỉ hiện ở màn tạo/sửa, KHÔNG hiện ở màn Chi tiết (`readonly` dùng lại chính component này)

### FE — `components/BillAdjustDeptRequestForm.vue`
- [x] Truyền `:touched="touched"` xuống `AdjustDetailTable`
- [x] Giữ nguyên toast tổng ở `validateBeforeSubmit()` — bảng dài, nhóm lệch có thể nằm ngoài
      màn hình; toast cho biết vì sao bấm Gửi duyệt mà không đi, inline chỉ đúng nhóm nào

### Quyết định
- Chỉ hiện **1 thông báo cho cả nhóm** (dòng "đến" cuối cùng), không lặp ở từng dòng — tổng lệch
  là của cả nhóm, từng dòng "đến" không tự chịu trách nhiệm được
- Chỉ hiện sau lần bấm **Gửi duyệt** đầu tiên (`touched` chỉ bật khi `status === 2`) — Lưu nháp
  cho phép lệch, đúng Phase 18

### Verify
- [x] Parse sạch template + script cả 2 file `.vue`
- [x] **Playwright trên `localhost:3000` (user yêu cầu tự test, 2026-09-03)** — dựng 2 nhóm
      (nhóm 1: từ 1.000.000, đến 250.000 + 150.000 → lệch 600.000; nhóm 2: khớp 500.000), bấm
      **Gửi duyệt** thật: đúng **1** thông báo đỏ, nằm trong ô Số tiền của dòng "đến" cuối nhóm 1
      ("còn thiếu 600,000"), nhóm khớp KHÔNG có; `white-space: normal`, `text-align: left`,
      cột tiền vẫn đúng 200px (không phình), bảng không tràn thêm
- [x] Xác minh bundle dev đang chạy có code mới (grep chunk `/_nuxt/…a657569d.js`): form cha truyền
      `touched: _vm.touched`, bảng khai prop, render có nhánh `isGroupUnbalanced`
- [ ] User bấm lại trên máy mình — **nhớ Ctrl+Shift+R** (HMR của Nuxt 2 hay không thay component
      của route, đây là lý do lần trước chưa thấy); thử thêm phiếu NCC ngoại tệ

---

## Phase 22 — Lỗi 422 của BE đổ về ĐÚNG TỪNG Ô trong bảng (2026-09-03)

User: *"hiển thị hết validate ở trường nào ra cho tôi, khách hàng, số tiền,... hiển thị xuống trường
đó cho tôi"* — kèm ví dụ `{"details.1.items.0.customer_new_id": ["Bắt buộc phải nhập"]}`.

Hiện trạng: `submit()` bắt 422 rồi chỉ **toast lỗi ĐẦU TIÊN**, vứt toàn bộ khoá field. Bảng 5-10
nhóm thì không biết ô nào sai. ERP làm đúng từ đầu (blade in
`errors['details.'+$parent.$index+'.items.'+$index+'.customer_new_id'][0]` dưới mỗi ô).

### FE — `BillAdjustDeptRequestForm.vue`
- [x] `data.serverErrors = {}` — giữ NGUYÊN khoá Laravel. **Không đặt tên `errors`**: vee-validate v2
      chiếm sẵn `errors`/`fields` trên mọi component, prop/data trùng tên bị che
- [x] `submit()`: xoá `serverErrors` ở đầu mỗi lần bấm; nhánh `catch` gán `data.errors || {}`
- [x] Truyền `:server-errors="serverErrors"` xuống `AdjustDetailTable`
- [x] Nối lỗi cho các ô NGOÀI bảng: `request_type`, `currency_id`, `exchange_rate`, `note`
      (dùng `V2BaseError` — component chuẩn, nhận cả String lẫn Array của Laravel)
- [x] Khoá `details` (không có chỉ số) — lỗi cấp cả bảng (khớp tổng tiền, trùng đối tượng
      "đến"/"từ") → `V2BaseError` ngay dưới bảng
- [x] Giữ toast: ô sai có thể nằm ngoài màn hình, toast là bản tóm tắt

### FE — `AdjustDetailTable.vue`
- [x] Prop `serverErrors` + `errorAt(fields, detailIndex, itemIndex)` — `itemIndex` bỏ trống là dòng
      "từ" (`details.{i}.<field>`), có `itemIndex` là dòng "đến" (`details.{i}.items.{j}.<field>`)
- [x] 3 hàm theo ô, mỗi hàm tra NHIỀU khoá vì tên cột đổi theo loại phiếu (KH `customer_*`/`contract_*`,
      NCC `supplier_*`/`buy_contract_*`) — khỏi rẽ nhánh trong template:
      `partyError()` · `contractError()` (kèm `contractable_id/type`) · `moneyError()`
- [x] `itemsError(i)` cho khoá `details.{i}.items` (nhóm chưa có dòng "đến" nào) → đặt ở dòng nút
      "Thêm điều chỉnh" của chính nhóm đó
- [x] 6 ô trong bảng: `:invalid="!!xxxError(...)"` (viền đỏ qua `v2ValidateMixin`) + `<V2BaseError>`
      ngay dưới — đối tượng/hợp đồng/số tiền, cả bên "từ" lẫn bên "đến"

### Verify — Playwright trên `localhost:3000`, bấm Gửi duyệt thật (2026-09-03)
- [x] **Đúng ca user đưa**: nhóm 1 thiếu KH bên "đến" → BE trả
      `{"details.1.items.0.customer_new_id":["Bắt buộc phải nhập"]}` → chữ đỏ "Bắt buộc phải nhập"
      hiện trong **ô Khách hàng của dòng "đến" nhóm 1**, ô viền đỏ; nhóm 0 (đủ dữ liệu) sạch
- [x] Ca số tiền: nhóm 1 để `money_old = 0` và `money_new = 0` (FE thấy khớp nên không chặn) → BE trả
      `details.1.money_old` + `details.1.items.0.money_new` → 2 chữ đỏ nằm đúng **2 ô Số tiền**
      (một bên "từ", một bên "đến"), cả 2 viền đỏ
- [x] Parse sạch template + script cả 2 file

### Phase 22b — Câu lỗi nửa Anh nửa Việt (2026-09-03)

User: *"The Số tiền điều chỉnh từ must be greater than 0. sao lại vừa tiếng anh vừa tiếng việt vậy"*.

**Gốc:** Laravel ghép **khuôn câu** (lấy từ `resources/lang/vi/validation.php`) với **`:attribute`**
(nhãn tiếng Việt khai ở `attributes()` của Request). File `lang/vi` là bản copy tiếng Anh **mới dịch
lác đác** — còn **52 khoá nguyên văn tiếng Anh**, trong đó có `gt`/`integer`/`array`/`string`/`boolean`;
`required`/`numeric`/`in`/`min`/`max` thì đã dịch. Nhãn Việt + khuôn Anh = câu lai.

**User chốt: KHÔNG sửa file lang dùng chung**, chỉ khai đè trong Request của màn này.

- [x] `BillAdjustDeptRequestStoreRequest::messages()` — thêm `gt`, `integer`, `array`, `string`,
      `boolean` (khoá chỉ có TÊN RULE, không kèm tên field, nên áp cho mọi field của request:
      `FormatsMessages::getInlineMessage()` tra `"{field}.{rule}"` rồi mới tới `"{rule}"`)
- [x] `BillAdjustDeptRequestUpdateRequest` ăn theo — class này `extends` Store, không cần sửa
- [x] `BillAdjustDeptRequestChangeStatusRequest::messages()` — thêm `string`
- [x] `php -l` sạch cả 2 file
- [x] **Playwright**: bấm Gửi duyệt lại đúng ca cũ → BE trả `{"details.1.money_old":["Phải lớn hơn 0"],
      "details.1.items.0.money_new":["Phải lớn hơn 0"]}`, hiện đúng 2 ô Số tiền, **hết tiếng Anh**

ℹ️ Còn tồn: `lang/vi/validation.php` vẫn còn ~52 khoá tiếng Anh — màn khác dùng rule chưa dịch sẽ
gặp lại đúng hiện tượng này. Muốn dứt điểm toàn hệ thống thì phải dịch file lang chung (user đã
cân nhắc và chọn không làm ở lần này).

---

## Phase 22c — Toast chỉ nói chung, chi tiết để inline (2026-09-03)

User: *"trên toast vẫn phải hiện là vui lòng kiểm tra dữ liệu nhập chứ?"*.

Đúng — sau Phase 22 mọi lỗi đều có chỗ hiện tại ô, nên nhắc lại nguyên văn ("Phải lớn hơn 0") ở góc
màn hình vừa thừa vừa vô nghĩa: user không biết là của ô nào.

### FE — `BillAdjustDeptRequestForm.vue`
- [x] `saveErrorToast(data)` cho nhánh 422: lỗi nào **đã hiện inline** (`details*`, `request_type`,
      `currency_id`, `exchange_rate`, `note`) → toast `"Vui lòng kiểm tra dữ liệu nhập"`.
      Lỗi **không có chỗ inline** (vd `status`: *"Bạn không có quyền gửi duyệt phiếu này"*) thì vẫn
      đọc nguyên văn ra toast — bỏ đi là mất hẳn thông tin. Không dùng `data.message` cho 422
      (Laravel trả "The given data was invalid.", tiếng Anh)
- [x] `failInline()` cho 5 luật validate FE (Loại phiếu / Diễn giải / bảng rỗng / Tỷ giá / lệch tiền)
      → cùng một câu `"Vui lòng kiểm tra dữ liệu nhập"`
- [x] Bổ sung inline còn thiếu cho **Loại phiếu** + cờ `submitted` (bật cả khi Lưu nháp) — `touched`
      chỉ bật lúc Gửi duyệt nên không dùng được cho luật duy nhất áp cho cả bản nháp

### Verify — Playwright, gọi `submit()` thật + bẫy `$toasted` để đọc nguyên văn
| Ca | Toast | Inline |
| --- | --- | --- |
| Lưu nháp chưa chọn Loại phiếu | Vui lòng kiểm tra dữ liệu nhập | "Vui lòng chọn loại phiếu" dưới ô Loại phiếu |
| Gửi duyệt thiếu Diễn giải | Vui lòng kiểm tra dữ liệu nhập | dưới ô Diễn giải |
| Gửi duyệt lệch tổng tiền | Vui lòng kiểm tra dữ liệu nhập | ô Số tiền bên "đến" |
| BE 422 tiền = 0 | Vui lòng kiểm tra dữ liệu nhập | 2 ô Số tiền ("Phải lớn hơn 0") |

- [x] `saveErrorToast()` đơn lẻ: khoá `status` → giữ nguyên văn "Bạn không có quyền gửi duyệt phiếu
      này"; trộn `status` + `details.0.money_old` → vẫn ưu tiên câu của `status`; lỗi 500 → `data.message`;
      rỗng → "Lưu thất bại"
- [x] Parse sạch template + script

### Checkpoint — 2026-09-03
Vừa hoàn thành: Phase 20 (đổi đối tượng phải xoá hợp đồng) · Phase 21 (lỗi lệch tổng tiền hiện inline
ở cột Số tiền bên "Điều chỉnh đến") · Phase 22 + 22b + 22c (lỗi 422 đổ về đúng từng ô · dịch câu lỗi
`gt`/`integer`/`array`/`string`/`boolean` trong Request · toast rút về "Vui lòng kiểm tra dữ liệu nhập").
Đang làm dở: không
Bước tiếp theo: user tự bấm nghiệm thu trên trình duyệt — **nhớ Ctrl+Shift+R** (HMR Nuxt 2 hay giữ
component cũ, chính là lý do lượt đầu user không thấy thay đổi). Chưa kiểm chứng: phiếu **NCC ngoại tệ**
(16 cột) và màn **sửa** phiếu có dữ liệu thật — dùng chung component nên logic giống hệt.
Blocked: không

**File đã đụng lượt này (5)**
| Repo | File |
| --- | --- |
| hrm-client | `pages/finance/bill-adjust-dept-requests/components/AdjustDetailTable.vue` |
| hrm-client | `pages/finance/bill-adjust-dept-requests/components/BillAdjustDeptRequestForm.vue` |
| hrm-api | `Modules/Finance/Http/Requests/BillAdjustDeptRequest/BillAdjustDeptRequestStoreRequest.php` |
| hrm-api | `Modules/Finance/Http/Requests/BillAdjustDeptRequest/BillAdjustDeptRequestChangeStatusRequest.php` |
| — | *(`BillAdjustDeptRequestUpdateRequest.php` ăn theo Store, không phải sửa)* |

**Còn nợ (giữ nguyên từ 2026-08-24, chưa động tới lượt này):** Excel phiếu lệch ERP · nút "Chọn nhanh
hợp đồng" · SRS/testcase/HDSD · dọn 6 phiếu `TEST.DNDCCN.*`.
Nợ mới: `hrm-api/resources/lang/vi/validation.php` còn ~52 khoá tiếng Anh — màn khác dùng rule chưa
dịch sẽ lại ra câu nửa Anh nửa Việt (user đã cân nhắc, chọn không sửa file chung ở lượt này).

---

## Phase 22d — Từ chối xong thì về màn danh sách (2026-09-03)

User: *"khi tôi từ chối phiếu yêu cầu điều chỉnh công nợ thì quay lại màn danh sách cho tôi,
hiện tại vẫn ở lại màn chi tiết"*.

**Gốc:** `changeStatus()` dùng chung cho cả *Gửi duyệt* lẫn *Từ chối*, kết thúc luôn bằng
`this.$router.go(0)` (nạp lại chính màn chi tiết để form lấy dữ liệu mới và footer đổi nút theo
trạng thái). Với *Gửi duyệt* thì đúng — user còn xem tiếp phiếu vừa gửi. Với *Từ chối* thì phiếu
đã xong việc của người duyệt, ở lại chi tiết là thừa một bước bấm quay lại.

### FE — `pages/finance/bill-adjust-dept-requests/_id/index.vue`
- [x] `changeStatus(status, noteReject = null, backToList = false)` — thêm tham số thứ 3;
      `backToList` → đóng popup rồi `$router.push('/finance/bill-adjust-dept-requests')`,
      còn lại giữ nguyên `$router.go(0)` như cũ (Gửi duyệt không đổi hành vi)
- [x] `changeStatus()` trả `true/false` theo thành công/lỗi (trước đây không trả gì)
- [x] `doReject()` gọi `changeStatus(6, reason, true)`; **chỉ đóng popup khi thành công** —
      trước đây `changeStatus` nuốt lỗi nên popup luôn đóng, user mất luôn lý do vừa gõ
- [x] Parse sạch template + script (`vue-template-compiler` + `@babel/core`)

⚠️ Chưa mở trình duyệt kiểm chứng — theo thoả thuận user tự test UI.

### Checkpoint — 2026-09-03
Vừa hoàn thành: Phase 22d — từ chối phiếu xong thì điều hướng về màn danh sách thay vì reload màn chi tiết.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt bấm **Từ chối** trên 1 phiếu ở trạng thái *Chờ duyệt* → xác nhận nhảy về `/finance/bill-adjust-dept-requests`; thử ca lỗi (BE trả 422) → popup lý do phải ở lại, không mất nội dung.
Blocked:

---

## Phase 23 — Nút "+" ở header bảng chi tiết bám khuôn màn Đề nghị thu tiền (2026-09-03)

User: *"button thêm mới ở bảng chi tiết đang không giống với màn đề nghị thu tiền, sửa lại cho tôi"*.

Khuôn nguồn: `pages/finance/bill-income-requests/components/BillIncomeRequestForm.vue:143-151` —
nút thêm dòng là **link icon teal KHÔNG viền** đặt trong header bảng:
`<a href="javascript:void(0)" class="text-primary" title="Thêm dòng"><i class="ri-add-line"></i></a>`.
Màn này đang dùng `V2BaseIconButton` (nút CÓ viền) nên nhìn khác hẳn.

### Phạm vi — user chốt bằng mockup: **CHỈ nút "+" ở header**
Bảng này có 2 nút thêm nên đã hỏi trước khi sửa. User chọn giữ nguyên nút "Thêm điều chỉnh"
(nút viền full-width dưới mỗi nhóm) và 2 nút xóa (`V2BaseIconButton danger`).

- [x] `AdjustDetailTable.vue` — đổi nút header từ `V2BaseIconButton` sang thẻ `<a class="text-primary">`
- [x] `title` đổi "Thêm dòng điều chỉnh từ" → **"Thêm dòng"** (chữ chuẩn skill `button-convention` §4.2
      cho hành động "Thêm 1 dòng vào bảng trong form"; cũng đúng bằng title của màn nguồn)
- [x] Giữ `v-if="!fromLocked"` — phiếu tạo từ phiếu báo có vẫn không được thêm dòng "từ"
- [x] Giữ `import V2BaseIconButton` (2 nút xóa vẫn dùng)
- [x] Giữ `width: 70px` cho cột (màn nguồn 46px nhưng cột này còn chứa nút xóa nhóm CÓ viền)

### Verify — Playwright, so trực tiếp với khuôn nguồn
- [x] `tag=A` · `class=text-primary` · `title=Thêm dòng` · `icon=ri-add-line` — **khớp 4/4** với màn
      Đề nghị thu tiền
- [x] `border: 0px none`, nền trong suốt, màu chữ `rgb(26,188,156)` (teal `#1abc9c`)
- [x] Header không còn nút viền nào
- [x] Bấm thật: `form.details` 0 → 1 dòng, chức năng không đổi
- [x] Parse sạch template + script

### 23.1 Nút "+" bị dính đáy ô header (fix 2026-09-03)

User: *"cho button nó lên giữa đi, sao lại lệch xuống dưới vậy"*.

**Gốc:** Bootstrap đặt `.table thead th { vertical-align: bottom }` (`bootstrap.css:1674`). Ô này
`rowspan="2"` nên cao bằng CẢ 2 tầng header (71px) → nút bám đáy khối đó. Trước đây dùng
`V2BaseIconButton` hộp cao hơn nên đỡ lộ; đổi sang link icon (cao 14px) là thấy rõ.

- [x] Thêm class `align-middle` vào `<th>` chứa nút

### Verify
- [x] Playwright đo trực tiếp: `vertical-align` của `<th>` = `middle`; ô cao 71px, nút cao 14px,
      **lệch tâm dọc = 0px** (chính giữa)

## Phase 24 — Cột NVKD trong bảng chi tiết quá hẹp (2026-09-03)

User: *"màn phiếu yêu cầu điều chỉnh công nợ, cột NVKD giãn cột ra cho tôi, hiện tại đang hẹp quá"*.

**Gốc:** đúng cái bẫy đã ghi ngay trong `<style>` của file (dòng 594): bảng dùng auto-layout nên
`width` trên `<th>` chỉ là GỢI Ý — cột nào khai `min-width` sẽ giành hết chỗ. Cột NVKD (và cột
"Nhân viên" ở phiếu NCC) là cột DUY NHẤT còn khai `style="width: 140px"`, các cột hàng xóm
(đối tượng 200px, hợp đồng 190px, số dư/số tiền 150-200px) đều khai `min-width` → NVKD bị bóp
lại còn rất hẹp, tên nhân viên xuống 2-3 dòng.

- [x] `AdjustDetailTable.vue:47` — đổi `width: 140px` → `min-width: 180px` cho cột `employeeLabel`
      bên **"Điều chỉnh từ"**
- [x] `AdjustDetailTable.vue:60` — đổi tương tự cho cột `employeeLabel` bên **"Điều chỉnh đến"**
      (2 chỗ phải khớp nhau, lệch là 2 khối header so le)
- [x] Component dùng chung cho cả 3 màn tạo / sửa / xem chi tiết → sửa 1 chỗ ăn cả 3;
      bản in (`_id/print.vue`) có bảng riêng, KHÔNG đụng tới

### Verify
- [x] `vue-template-compiler` parse template: 0 lỗi · `@babel/parser` parse script: OK
- [ ] **Chưa mở trình duyệt** — user tự xem lại độ rộng thực tế (Ctrl+Shift+R nếu Nuxt HMR
      giữ component cũ)

---

## Phase 24 — Màn CHI TIẾT hiện "Người tạo - Ngày tạo" như ERP (2026-09-03)

User: *"trong màn xem chi tiết hiển thị thêm cho tôi người tạo, ngày tạo như bên erp nhé"*.

ERP đặt ở **góc phải header card "Thông tin chung"** của màn xem:
`formShow.blade.php:21-26` → `<% form.creator %> - <% form.created_time %>`.

- [x] `BillAdjustDeptRequestForm.vue` — thêm computed `createdInfo` = `created_by_name - created_at`
      (thiếu vế nào bỏ vế đó) + render ở góc phải header, **chỉ khi `readonly`**
      (`v-else-if`, đi sau nhánh badge trạng thái của màn tạo/sửa)
- [x] Màn tạo/sửa GIỮ NGUYÊN không có dòng này — Phase 19.1 đã bỏ có lý do (lúc tạo phiếu chưa có
      ngày tạo, chỉ còn trùng mỗi tên người tạo với ô ngay bên dưới)
- [x] BE `BillAdjustDeptRequestDetailResource` — `created_at` đổi `d/m/Y` → **`d/m/Y H:i`** cho khớp
      cột "Ngày tạo" màn danh sách (`ListResource` vốn đã `d/m/Y H:i`). `php -l` sạch.
      Đã soát: `created_at` của API chi tiết chỉ dùng cho chỗ này ở FE

### 24.1 Chữ ra MÀU ĐỎ (fix cùng ngày)

User: *"để text khác màu đỏ đi"*.

**Gốc — bẫy toàn hệ thống, không phải của màn này:** class `text-muted` ở `hrm-client` KHÔNG phải xám
mà là **ĐỎ** — 3 file style dùng chung cùng ép `!important`:
`assets/scss/custom.scss:242` · `custom-theme.scss:191` · `custom-timesheet.scss:18`
đều khai `.text-muted { color: #dc3545 !important }`.

- [x] Bỏ class `text-muted`, đặt màu thẳng `style="color: #6b7280"` (inline nên không rule nào đè được)
- [x] Ghi chú ngay tại chỗ để người sau không lặp lại

⚠️ **Còn 2 chỗ trong màn này vẫn đang đỏ oan** (chưa sửa, chờ user chốt vì đụng tới hiển thị đang
nghiệm thu rồi):
- `AdjustDetailTable.vue:249` — dòng *"Chưa có dòng điều chỉnh nào."* của bảng rỗng
- `BillAdjustDeptRequestForm.vue:53` — dòng *"Loại phiếu lấy theo phiếu báo có, không đổi được"*

Sửa hẳn 3 file scss chung thì cả hệ thống hết đỏ, nhưng đó là style dùng chung → phải hỏi trước.

### Verify
- [x] Parse sạch template + script; `php -l` sạch resource
- [x] Dữ liệu nguồn có thật: `bill_adjust_dept_requests` id 10316 → `created_by = 13`,
      `created_at = 2026-08-24 13:57:27`, `employee_infos.fullname = "Nguyễn Thị Cẩn"`
- [ ] **CHƯA kiểm chứng trên trình duyệt** — dev server cổng 3000 đã tắt giữa chừng
      (`ERR_CONNECTION_REFUSED`), cần bật lại `npm run dev` rồi mở
      `/finance/bill-adjust-dept-requests/10316` xem góc phải header

---

## Phase 25 — Fix: khối Lịch sử cách nội dung quá xa ở màn chi tiết (2026-09-04)

User: *"trong màn chi tiết phần lịch sử đang bị cách xa phần nội dung bên trên quá"*.

**Gốc:** `BillAdjustDeptRequestForm.vue:3` cứng `style="padding-bottom: 70px"` — khoảng chừa cho
`V2Footer` **của chính form**. Footer đó lại có `v-if="!readonly"` ⇒ ở màn CHI TIẾT form không
render footer, 70px thành khoảng trắng chết nằm GIỮA card "Chi tiết" và `SystemInfoSection`
(cộng `mt-3` của trang = hụt ~86px).
Màn chi tiết đã tự chừa `padding-bottom: 70px` ở container ngoài (`_id/index.vue:3`) cho footer
riêng của nó → 70px trong form là thừa hẳn. Màn tạo/sửa thì VẪN CẦN
(`create.vue` / `_id/edit.vue` bọc bằng `container-fluid` không có padding).

- [x] `BillAdjustDeptRequestForm.vue` — buộc `padding-bottom: 70px` theo `!readonly`
      (`:style`), không bỏ hẳn
- [x] Không đụng `SystemInfoSection.vue` (component dùng chung nhiều màn; `margin-top` của nó
      vốn đã bị comment sẵn — không phải thủ phạm)

### Verify
- [x] Parse template + script: vue-template-compiler 0 lỗi · @babel/parser OK
- [ ] Mở trình duyệt `/finance/bill-adjust-dept-requests/<id>` — user tự xem

---

## Phase 26 — In phiếu: đổi sang POPUP xem trước theo skill print-page §8 (2026-09-04)

User: *"sửa lại phần in phiếu mở popup như skill cho tôi"*.

**Hiện trạng sai chuẩn:** nút In (cả màn danh sách lẫn chi tiết) `window.open('/…/print', '_blank')`
→ mở TAB MỚI. Skill print-page §8 chốt 2026-08-22: mở popup xem trước ngay tại chỗ, vì mở tab mới
làm mất ngữ cảnh danh sách + bộ lọc. Khuôn tham chiếu: `borrow-export-requests` (feature liền trước,
cùng phân hệ, làm đúng chuẩn).

Bộ dùng chung PHẢI dùng lại, không viết lại: `components/print/ReportPrintPreviewModal.vue` +
`utils/mixins/reportPrintPreviewMixin.js` + `utils/print/reportPrintStyle.js`.
Mixin gọi đúng endpoint đã có sẵn `GET /{id}/print-data`, nhưng đọc khoá **`template`** (HTML do BE
fill) — hiện BE trả dữ liệu có cấu trúc cho FE tự dựng ⇒ phải chuyển việc dựng HTML về BE.

### BE
- [x] Blade mới `Modules/Finance/Resources/views/prints/bill-adjust-dept-request.blade.php` —
      port nguyên bố cục `print.vue` (mẫu ERP 209): letterhead · tiêu đề + dòng ngày · khối 5 trường ·
      bảng "Điều chỉnh từ / đến" 3 khuôn (`customer` 8 cột · `supplier` 10 · `supplier_fx` 14) ·
      khối ký giữ nguyên 3 chỗ "lỗi" của ERP (5 td/6 td · NGƯỜI NỘP TIỀN 2 lần · THỦ QUỸ 1px)
- [x] `BillAdjustDeptRequestPrintService` mới — `render()` dùng lại
      `BillAdjustDeptRequestPrintResource` (một nguồn số liệu với Excel, không lệch)
- [x] Letterhead theo **`company_id` GHI TRÊN PHIẾU** + URL tuyệt đối + fallback `ERP_URL`
      (CLAUDE.md · skill §4b). Resource hiện lấy theo công ty NGƯỜI TẠO → sai khuôn.
      **KHÔNG sửa trong Resource** để không đổi luôn nội dung file Excel (dùng chung khoá `header`)
- [x] `printData()` trả `{ template }` như `BorrowExportRequestController`
- [x] CSS riêng của mẫu đặt trong `<style>` NGAY TRONG chuỗi HTML trả về (đi kèm sang cả popup lẫn
      iframe in) — KHÔNG đụng `reportPrintStyle.js` (tài sản dùng chung)

### FE
- [x] `_id/index.vue` — bỏ `window.open`, dùng `reportPrintPreviewMixin` + `ReportPrintPreviewModal`
- [x] `index.vue` — như trên cho hành động In của từng dòng
- [x] Khổ **NGANG** (`landscape: true`): phiếu NCC ngoại tệ 14 cột, khổ dọc là tràn (ERP cũng
      `print_landscape`) ⇒ gọi `loadPrintPreview(..., true)` thay `openPrintDetail` (mixin mặc định dọc)
- [x] Xoá `_id/print.vue` — thành mã chết, và là **nguồn CSS thứ hai** của cùng một bản in (đúng
      thứ skill §8a cấm)

### Verify
- [x] `php -l` sạch · `vue-template-compiler` + `@babel/parser` parse 2 màn FE: 0 lỗi
- [x] Gọi thật `GET /api/v1/finance/bill-adjust-dept-requests/10316/print-data` qua HTTP kernel
      (kèm JWT) → **HTTP 200**, `data` chỉ còn khoá `template`, HTML 5.121 ký tự, đủ
      `bad-doc`/`bad-table`/`bad-group`/`Điều chỉnh từ`/`Điều chỉnh đến`
- [x] Kiểm CẤU TRÚC bảng in trên **12 phiếu thật, đủ 3 khuôn** (customer 6 · supplier 5 ·
      supplier_fx 1) bằng DOMXPath: mọi dòng đều đúng `2 × số cột mỗi bên` sau khi tính rowspan gộp
- [x] Letterhead ra URL TUYỆT ĐỐI: `https://erp.eteksofts.com/uploads/1751696586ts-hn.png`
      (trước đây Resource trả path tương đối)
- [ ] **Mở trình duyệt — user tự xem** (chưa kiểm chứng bằng mắt: khung popup, khổ ngang, ảnh letterhead)

### 26.1 Khối ký dồn về bên trái (fix cùng ngày)

User: *"BAN GIAM ĐỐC … NGƯỜI NỘP TIỀN chỗ này căn lại cho đều giúp tôi, hiện tại đang lệch về bên trái"*.

**Gốc — đúng bẫy skill print-page §3b, nằm trong MẪU ERP chứ không phải code màn:** bảng ký khai
2 bộ độ rộng chọi nhau — hàng trên `width:275px` + `300px`×3 (tổng 1.175px = khổ giấy ERP), hàng
dưới `width:20%`×6 (tổng **120%**). Trình duyệt co các cột về trái, ô cuối hụt so với mép phải của
bảng dữ liệu. Bảng lại mang class `no-border` nên các rule ép `width:100%` cho bảng thường không
với tới nó.

- [x] Bỏ HẾT `width` inline trên từng `<td>`, chuyển sang `<colgroup>` 6 `<col>`
- [x] `table-layout: fixed !important` cho `.bad-sign` — chỉ ở chế độ này trình duyệt mới lấy độ
      rộng từ `<col>`; để `auto` thì nó tự tính lại theo nội dung và cột lại dồn trái
- [x] Chia **20% cho 5 chức danh nhìn thấy được, cột THỦ QUỸ = 0** — giữ nguyên ô THỦ QUỸ của mẫu
      ERP (cỡ chữ 1px, gần như tàng hình) mà 5 chức danh vẫn trải đều hết bề ngang giấy.
      Để cột thứ 6 cũng ~17% thì bên phải hở một khoảng trống, nhìn vẫn lệch trái
- [x] `text-align: center` cho ô ký — mẫu ERP không khai nên chữ dính mép trái từng cột, cột đều
      rồi mà nhìn vẫn lệch

### Verify 26.1
- [x] Render phiếu 10316, soi bằng DOMXPath: `<colgroup>` đúng 6 `<col>` = `20% | 20% | 20% | 20% |
      20% | 0`; **0 ô còn khai `width` inline**; hàng 1 giữ 5 ô, hàng 2 giữ 6 ô + đủ 6 chức danh
      (3 chỗ "lỗi cố ý" của ERP còn nguyên)
- [ ] **Mở trình duyệt — user tự xem** (CSS căn cột chỉ đo được thật trên trình duyệt)

---

## Phase 27 — Ô không có dữ liệu: bỏ dấu gạch ngang, để TRỐNG (2026-09-04)

User: *"hiện tại màn danh sách, màn chi tiết Dữ liệu trống vẫn đang ở dạng - => sửa về hiển thị trống"*.

Đúng chuẩn team đã chốt: skill `list-page` **§3b-3** (chốt 2026-08-24, Redmine #11171) — ô rỗng để
trống hẳn, KHÔNG chèn `—` / `-` / `N/A`; dấu gạch trông như một giá trị thật và mỗi màn chèn một
kiểu thì bảng rất bẩn. Màn này port trước ngày chốt nên còn sót.

Rà đủ **5 nơi** skill yêu cầu (đây là chỗ đã sót 2 lần ở các màn khác):

- [x] 1. Màn danh sách — `index.vue`: **11 chỗ** (mã phiếu, loại phiếu, mã phiếu báo có, đối tượng,
      ngày tạo, người tạo, ngày sửa, người sửa, phòng ban, ngày nhận, người duyệt)
- [x] 2. Màn chi tiết — `AdjustDetailTable.vue` (bảng chi tiết ở chế độ `readonly`): **6 chỗ**
      (đối tượng / hợp đồng / nhân viên, cả vế "từ" lẫn vế "đến").
      `BillAdjustDeptRequestForm.vue` đã sạch sẵn — hiển thị qua ô nhập disabled nên rỗng là trống
- [x] 3. Popup — `RejectModal.vue` sạch; popup Lịch sử dùng chung giữ chữ **"(trống)"**, đây là
      NGOẠI LỆ đúng nghĩa của skill (mang nghĩa "trường này trước/sau khi sửa không có giá trị")
- [x] 4. Bản in / file xuất — blade in + 2 blade Excel: đã sạch, không có fallback nào
- [x] 5. BE Resource — `Transformers/BillAdjustDeptRequestResource/`: đã sạch, máy chủ không trả `'—'`

Xử lý riêng **badge Trạng thái**: bỏ `|| '—'` trơn sẽ vẽ ra một pill có màu mà rỗng ruột, xấu hơn
cả dấu gạch → đổi thành `v-if="item.status_name"`, không có trạng thái thì không vẽ badge.

### Verify
- [x] `grep -rn "|| '—'" pages/finance/bill-adjust-dept-requests/` → **RỖNG** (tự kiểm của skill §3b-3)
- [x] `grep -rn "'—'" Modules/Finance/Transformers/BillAdjustDeptRequestResource/` → **RỖNG**
- [x] Parse template + script 2 file sửa: 0 lỗi. `—` còn lại trong repo chỉ nằm ở phần chú thích
- [ ] **Mở trình duyệt — user tự xem**

⚠️ **Skill `list-page` đang tự mâu thuẫn, cần PR sửa (KHÔNG tự sửa — tài sản chung):** dòng 1077
vẫn ghi *"Cột số/tiền: … ô trống hiển thị `—` và vẫn căn phải"*, trái với §3b-3 chốt sau đó
(2026-08-24). Làm theo §3b-3 vì mới hơn; nên bỏ vế `—` ở dòng 1077 để người sau khỏi làm ngược.

---

## Phase 28 — Cột "Ngày nhận" đổi định dạng cho khớp "Ngày cập nhật" (2026-09-04)

User: *"cột ngày nhận sửa lại định dạng cho giống cột ngày cập nhật cho tôi"*.

Lệch: `updated_at` trả `d/m/Y H:i`, còn `send_approve_date` trả `d/m/Y` — 2 cột ngày đứng cạnh nhau
trên cùng lưới mà một cột có giờ, một cột không.

Đã kiểm trước khi sửa (thêm giờ chỉ có nghĩa nếu dữ liệu thật sự có giờ): cột
`bill_adjust_dept_requests.send_approve_date` kiểu **`datetime`**, và **10.175/10.175** dòng có
`TIME() <> 00:00:00` ⇒ thêm `H:i` là thêm thông tin thật, không phải bày ra một dãy `00:00`.

- [x] `BillAdjustDeptRequestListResource` — `d/m/Y` → **`d/m/Y H:i`**.
      File Excel danh sách dùng LẠI chính Resource này (`Controller::exportList()`) nên đổi một chỗ
      là lưới và file Excel cùng đổi, không lệch nhau
- [x] `BillAdjustDeptRequestDetailResource` — đổi theo cho khớp. FE chưa hiển thị trường này ở màn
      chi tiết, nhưng để lệch là đúng cái bẫy Phase 24 đã dính với `created_at`
- [x] `index.vue` — `width` cột "Ngày nhận" `110px` → **`140px`**, bằng đúng cột "Ngày cập nhật";
      110px vốn đo cho `d/m/Y`, giữ nguyên thì chữ xuống dòng

### Verify
- [x] `php -l` sạch 2 Resource · parse template + script `index.vue`: 0 lỗi
- [x] Gọi thật `GET /api/v1/finance/bill-adjust-dept-requests?per_page=8` (HTTP kernel + JWT) →
      **HTTP 200**, 2 cột ra cùng khuôn: `24/08/2026 13:57` · `17/08/2026 16:45`.
      Phiếu chưa gửi duyệt trả **rỗng** (không phải `—`) — xác nhận luôn Phase 27 chạy đúng ở API
- [ ] **Mở trình duyệt — user tự xem**

---

## Phase 29 — Thêm "Từ chối" vào màn danh sách (điều hướng sang chi tiết) — 2026-09-04

User: *"những phiếu chờ tạo phiếu kế toán có button từ chối trong màn chi tiết mà màn danh sách lại
không có"* → *"nếu bấm vào từ chối thì sẽ mở vào màn chi tiết bên trong cho tôi"*.

**Không phải lỗi BE**: `BillAdjustDeptRequestListResource` VỐN đã trả `is_can_reject` (dòng 64),
khớp 10/10 với API chi tiết — chỉ có `getRowActions()` ở FE không dùng tới cờ đó.

`canReject()` = trạng thái **2 (Chờ tạo phiếu kế toán)** + là **Kế toán thanh toán** + **cùng công ty**
với phiếu. Đúng đối tượng user mô tả.

- [x] `index.vue::getRowActions()` — thêm `{ key: 'reject', title: 'Từ chối', danger: true,
      to: '/finance/bill-adjust-dept-requests/{id}', visible: !!item.is_can_reject }`.
      Khai `to` → `V2BaseRowActions` render `<nuxt-link>` (chuột phải mở tab mới được) và **không
      cần** thêm nhánh trong `handleRowAction` — link tự điều hướng
- [x] Đặt TRƯỚC "In phiếu": phiếu ở trạng thái chờ thì `is_can_edit`/`is_can_delete` đều `false`,
      nên "Từ chối" nổi lên thành nút chính ngoài dòng thay vì nằm trong menu `⋮`
- [x] `_id/index.vue` — sửa lại chú thích cũ đã sai sự thật ("cùng bộ hành động với dòng ngoài màn
      danh sách"), chính chỗ này làm người đọc tưởng 2 màn phải giống hệt nhau

### ⚠️ Cố ý LỆCH skill — cần biết khi review
Skill `list-page` mục "Cột Hành động" §1 (chốt 2026-08-24) ghi: **bỏ hẳn hành động phủ quyết
("Hủy phiếu", "Không duyệt") khỏi danh sách**, lý do là ở danh sách chúng chỉ còn là link sang chi
tiết nên "thêm 1 dòng menu mà không làm được gì tại chỗ".

User chốt 2026-09-04 làm ngược lại cho màn này: vẫn bày "Từ chối" ở danh sách, chấp nhận nó chỉ là
link — để người duyệt nhìn lưới là biết ngay phiếu nào mình từ chối được, không phải mở từng phiếu.
**Không mở popup nhập lý do tại dòng** (vẫn tôn trọng phần lý do của skill: phải đọc chứng từ trước
khi từ chối). Skill là tài sản chung → nếu muốn hợp thức hoá thì sửa skill bằng PR, không sửa lẻ.

### Verify
- [x] Parse template + script 2 màn: 0 lỗi
- [x] Đối chiếu API thật (HTTP kernel + JWT) trên 10 phiếu: `is_can_reject` của danh sách khớp
      **10/10** với API chi tiết — `true` đúng ở 4 phiếu *Chờ tạo phiếu kế toán*, `false` ở
      *Đang tạo* / *Từ chối*
- [ ] **Mở trình duyệt — user tự xem**

### Còn bỏ ngỏ (chưa làm, chờ user)
"Gửi duyệt" hiện chỉ có ở màn chi tiết, danh sách không bày. Nếu muốn đối xứng thì thêm y hệt kiểu
trên — nhưng user chưa yêu cầu nên chưa đụng.

---

## Phase 30 — Lịch sử: bảng chi tiết in theo TỪNG DÒNG thay vì một đoạn văn (2026-09-04)

User: *"phần lịch sử thay đổi chỗ bảng chi tiết xuống dòng cho dễ nhìn, hiện tại như này đang rất khó nhìn"*
(kèm ảnh: khối "Bảng chi tiết" là một đoạn đỏ + một đoạn xanh dài mấy dòng liền).

**Gốc — không phải lỗi xuống dòng của giao diện, mà là BE ghi log sai kiểu.** Màn này khai khoá ảo
`details_summary` là **một CHUỖI GỘP** (`detailsSummary()` nối cả bảng bằng `;` và `+`), nên với bộ
log nó chỉ là một trường phẳng: đổi 1 số tiền cũng in lại **toàn bộ bảng** ở cả vế cũ lẫn vế mới.
Đúng thứ skill `entity-history` §3b cấm: *"TUYỆT ĐỐI không tự ghép chuỗi mô tả rồi nhét vào 1 cột
ảo — cả bảng dồn thành một đoạn văn dài, người xem không biết dòng nào đổi cái gì"* (Redmine #11163).
Màn `bill_income_requests` / `addition_accounting_requests` cùng phân hệ đã dùng đúng khoá
`details_rows` dạng BẢNG từ trước.

Bảng chi tiết ở màn này có **2 CẤP** nên tách **2 khoá** (skill §3: bảng con nhiều cấp phải tách
khoá riêng kèm cột nhận diện chủ sở hữu — nhét cấp con vào chuỗi của cha thì sửa 1 đích là in lại
nguyên dòng dài của cha và mọi đích còn lại):

- [x] `details_rows` → nhãn **"Dòng điều chỉnh"** (vế *điều chỉnh từ*)
- [x] `detail_items_rows` → nhãn **"Đối tượng nhận điều chỉnh"** (vế *điều chỉnh đến*), có cột
      `Điều chỉnh từ` để biết đích này thuộc dòng nguồn nào
- [x] Nhãn chọn sao cho ghép với hậu tố của `rowListChange()` đọc xuôi: *"Dòng điều chỉnh đã xóa"*,
      *"Đối tượng nhận điều chỉnh sửa thông tin"*
- [x] `__key` dùng **khoá tự nhiên** (đối tượng + hợp đồng), KHÔNG dùng id — `syncDetails()` xoá
      sạch rồi tạo lại mỗi lần lưu nên id đổi liên tục, ghép cặp theo id là dòng nào cũng thành
      "xoá cũ + thêm mới". `__key` của đích gồm cả khoá dòng cha (2 dòng nguồn khác nhau vẫn có thể
      điều chỉnh đến cùng một đối tượng)
- [x] Bỏ 2 cột `Khách hàng`/`Hợp đồng` khỏi phụ chú — chúng đã là TÊN của dòng (`__name`), in thêm
      là mỗi dòng log đọc thấy cùng một chuỗi hai lần
- [x] `catalogDisplay()` chặn 2 khoá này TRƯỚC nhánh rỗng, trả nguyên mảng (ép chuỗi là log ra "Array";
      để rơi vào nhánh rỗng thì "xoá hết dòng chi tiết" không sinh log)
- [x] `CatalogHistoryService::TABLES` — thêm 2 nhãn mới, **GIỮ `details_summary`** để log CŨ vẫn
      hiện được. Không sửa dữ liệu log cũ (skill §6)

**FE: KHÔNG phải sửa gì.** Popup trong ảnh (`CatalogHistoryModal`) lấy ruột là chính
`SystemInfoSection` — component này đã render nhóm có nhãn theo §4b từ trước (`rowsOf` / `groupLabel`
/ `.si-group-label` / `.si-row-detail`). Nó in ra một đoạn dài chỉ vì BE gửi xuống một trường phẳng.

### Verify
- [x] `php -l` sạch 2 file BE
- [x] Chạy thật trên phiếu **id 1487** (9 dòng nguồn / 9 đích): gọi CHÍNH `detailRows()` +
      `detailItemRows()` qua reflection (chỉ ĐỌC dữ liệu), mô phỏng 1 lần sửa, đẩy qua
      `CatalogHistoryService::getLogs()`. Kết quả in ra đúng khuôn §4b:
      ```
      ### Dòng điều chỉnh
        [Dòng điều chỉnh đã xóa]
          - 14TQUPDO-2 - CÔNG TY TNHH HOÀNG ANH ĐÔNG TRIỀU / HĐ_TPE_KD3_25_0069_1121 — NVKD: Đỗ Văn Sáng; Số tiền: 1,108,100
      ### Đối tượng nhận điều chỉnh
        [Đối tượng nhận điều chỉnh đã xóa]
          - … / HĐ_TPE_HN_KD3_25_0062_602 — Điều chỉnh từ: …; NVKD: Đỗ Văn Sáng; Số tiền: 1,108,100
        [Đối tượng nhận điều chỉnh sửa thông tin]
          - … / HĐ_TPE_HN_KD3_25_0068_608: Số tiền: 2,930,000 -> 199,960
      ```
      Dòng SỬA chỉ liệt kê đúng trường đã đổi, không in lại cả bản ghi
- [x] Dọn sạch: 3 dòng log thử đã xoá (id 305, 306, 307). **Không đụng dữ liệu nghiệp vụ**
- [x] Không sinh nhiễu ở lần lưu đầu sau khi đổi: `details_summary` đã ra khỏi `catalogColumns()`
      nên không có mặt ở cả `$before` lẫn `$after` → không tạo diff giả
- [ ] **Mở trình duyệt — user tự xem** (log MỚI mới có định dạng này; log cũ giữ nguyên đoạn văn dài)

---

## Phase 30 — Nút "Gửi duyệt": thêm lớp tải + chặn bấm 2 lần (2026-09-04)

User: *"khi click gửi duyệt thì thêm loading vào cho tôi"*.

Màn này có **2 nút mang chữ "Gửi duyệt"** — cả hai đều thiếu lớp tải, sửa cả hai:

| Nút | Ở đâu | Hàm |
| --- | --- | --- |
| Gửi duyệt (đổi trạng thái) | `_id/index.vue` — footer màn chi tiết | `changeStatus(2)` |
| Gửi duyệt (lưu + gửi) | `BillAdjustDeptRequestForm.vue` — footer màn tạo/sửa | `submit(2)` |

Theo skill `button-convention` **§6b**: lệnh GHI phải bật `$safeLoadingStart()` ngay trước lệnh gọi
và `$safeLoadingFinish()` trong **`finally`** (đặt cuối `try` thì gọi API lỗi là màn kẹt lớp che).
Dùng `$safeLoadingStart` chứ KHÔNG gọi thẳng `$nuxt.$loading.start()` — lúc tải lại trang
`$nuxt.$loading` có thể chưa tồn tại, ném lỗi là nuốt luôn lệnh gửi.

- [x] `_id/index.vue::changeStatus()` — `$safeLoadingStart` + `$safeLoadingFinish` trong `finally`
      (che cả nhánh **Từ chối**, cùng đi qua hàm này) + chốt chặn `if (this.submitting) return`
- [x] `BillAdjustDeptRequestForm.vue::submit()` — như trên với cờ `saving`; chặn đặt SAU
      `validateBeforeSubmit()` để form sai vẫn tô đỏ như cũ

### Lỗi im lặng phát hiện kèm — `:disabled` trên V2BaseButton KHÔNG có tác dụng
`components/V2BaseButton.vue:7` tự bind `:disabled="tag === 'button' && !interactable ? true : null"`
⇒ `disabled` truyền từ ngoài bị chính binding này ghi đè, **nút vẫn bấm được** trong lúc đang gửi.
Đúng cái bẫy skill §6b cảnh báo. Màn này dính **3 nút**:

- [x] `RejectModal.vue:29` — nút "Từ chối" trong popup
- [x] `BillAdjustDeptRequestForm.vue` — nút "Lưu nháp" và "Gửi duyệt"
- [x] Đổi hết sang `:interactable="!saving"` / `:interactable="!submitting"`
- [x] 2 nút mới thêm ở footer chi tiết (Gửi duyệt · Từ chối) khai `:interactable` ngay từ đầu

### Verify
- [x] Parse template + script 4 file: 0 lỗi
- [x] `grep ":disabled" … | grep V2BaseButton` trong cả thư mục màn → chỉ còn 2 dòng CHÚ THÍCH
- [x] Đọc `V2BaseButton.vue` xác nhận cơ chế: prop hợp lệ là `interactable`, `disabled` không có
      trong `props`
- [ ] **Mở trình duyệt — user tự xem**

### ⚠️ 2 việc còn bỏ ngỏ (chưa làm — chờ user chốt)
1. **Chưa có popup xác nhận cho "Gửi duyệt"**, trong khi skill `button-convention` **§6c**
   (chốt 2026-08-27) bắt buộc MỌI nút đổi trạng thái phiếu phải hỏi xác nhận trước, câu hỏi nêu tên
   phiếu + hệ quả, `textAccept` đúng chữ trên nút. Không tự thêm vì user chỉ yêu cầu lớp tải, mà
   thêm popup là đổi hẳn thao tác đang nghiệm thu.
2. **`V2BaseButton` có prop CHẾT `isShowLoading`** — khai ở `props` nhưng không hề dùng trong
   template (không render spinner, không bind class). Ai tưởng nó bật spinner trên nút là nhầm.
   Là component dùng chung → muốn có spinner trên nút thì phải sửa qua PR, không sửa lẻ.

---

## Phase 31 — Cửa vào "Tạo phiếu kế toán" (2026-09-04)

User: *"màn phiếu yêu cầu điều chỉnh công nợ này có cả chức năng tạo phiếu kế toán mà? bạn chưa làm à"*.

**Đúng — thiếu thật, và là lỗ hổng do quyết định cũ hết hạn.** Quyết định #3 của `design.md`
(2026-08-17) ghi *"dừng ở Chờ tạo phiếu kế toán — không port màn phiếu kế toán, kế toán sang ERP
tạo"*, nên `_id/index.vue` có hẳn chú thích *"Nút Tạo phiếu kế toán KHÔNG có ở HRM"*.
Lý do đó **không còn đúng từ 2026-08-28**: màn Phiếu kế toán đã port xong
(`.plans/gop-db/finance-bill-adjust-dept/`, quyết định #6 gỡ hẳn ràng buộc "HRM không ghi sổ").

Phía sau đã sẵn sàng từ lâu, **chỉ thiếu đúng cái nút**:
- BE `BillAdjustDeptSourceService::fromAdjustRequest()` + `loadForCreate()` nhận
  `bill_adjust_dept_request_id` (cửa vào số 2/5, plan feature kia đánh `[x]` mục 5.3)
- BE có sẵn hook vòng đời cập nhật ngược trạng thái phiếu đề nghị: `onBillCreated` ·
  `onBillApproved` · `onBillDeleted` · `onBillCancelled`
- FE `BillAdjustDeptForm.vue:455` đã đọc `bill_adjust_dept_request_id` từ `$route.query`
- ⇒ Trước Phase này **không có chỗ nào trong ứng dụng trỏ tới**, chỉ gõ tay URL mới vào được

### Bám ERP
`income_expenditure/bill_adjust_dept_requests/show.blade.php` :19-22 — nút nằm ở **màn chi tiết**,
`@if` chung với nút "Không duyệt": quyền `Kế toán thanh toán` + trạng thái *Chờ tạo phiếu kế toán*.
`canReject()` của HRM chính là bản port helper đó (`canCreateBillAdjustDept()` :1051).

### BE
- [x] `BillAdjustDeptRequest::canCreateAccounting()` — **gọi lại `canReject()`**, không chép biểu
      thức (chép ra 2 bản là sớm muộn 2 nút lệch điều kiện). Tách hàm riêng vì 2 hành động khác hẳn
      nhau về nghiệp vụ, ngày nào điều kiện tách đôi thì sửa đúng một chỗ
- [x] `ListResource` + `DetailResource` — thêm cờ `is_can_create_accounting` (fail-closed, FE không
      tự suy theo trạng thái)

### FE
- [x] `_id/index.vue` — nút **"Tạo phiếu kế toán"** ở footer, đặt TRƯỚC "Từ chối"
      (skill button-convention §5: chính → phụ → danger), `primary` + `ri-add-line`,
      **không hỏi xác nhận** (§6c: chỉ điều hướng, chưa ghi gì)
- [x] `index.vue` — hành động cùng tên ở cột Hành động, dạng `to` (nuxt-link), theo đúng kiểu vừa
      làm cho "Từ chối" ở Phase 29
- [x] Sửa 2 chú thích đã hết hạn ở `_id/index.vue` (docblock + chú thích footer)

### Verify
- [x] `php -l` sạch 3 file BE · parse template + script 2 màn FE: 0 lỗi
- [x] API danh sách (HTTP kernel + JWT): cờ `is_can_create_accounting` = `true` ĐÚNG 4 phiếu
      *Chờ tạo phiếu kế toán*, `false` ở *Từ chối* / *Đang tạo*; API chi tiết khớp
- [x] **Deep-link chạy thật**: `GET /finance/bill-adjust-depts/source-data?bill_adjust_dept_request_id=10316`
      → HTTP 200, trả `source` / `header` / `details`, điền sẵn **2 dòng định khoản**,
      `header.bill_adjust_dept_request_id = 10316`, `code = TPE.DNDCCN0826.00004`
- [ ] **Mở trình duyệt — user tự xem** (bấm nút → sang màn phiếu kế toán đã điền sẵn)

⚠️ Nhãn nút để nguyên **"Tạo phiếu kế toán"** (4 từ) dù skill button-convention §4.1 giới hạn 3 từ:
đây là tên chứng từ đích, rút ngắn thành "Tạo phiếu KT" là mất nghĩa. Giữ đúng chữ ERP đang dùng.

### Cần rà lại `design.md` của feature
Quyết định #3 và mục "Scope → Ngoài" của `.plans/gop-db/finance-bill-adjust-dept-request/design.md`
vẫn ghi *"không port màn phiếu kế toán / HRM không ghi sổ cái"* — đã lỗi thời từ 2026-08-28.
Chưa sửa vì đó là bản ghi quyết định lịch sử; nên thêm dòng đính chính ở lần `wrap up` tới.

---

## Phase 32 — Vào màn danh sách: hiện "Đang tải" ngay, không nháy "Không có dữ liệu" (2026-09-04)

User: *"màn danh sách … khi vừa vào thì bảng danh sách cho load luôn giúp tôi đi, hiện tại đang để
dòng text Không có dữ liệu phù hợp bộ lọc rồi mới load"*.

**Gốc — khoảng hở giữa 2 lệnh `await` trong `mounted()`:**

```js
async mounted() {
    this.restoreSavedFilters()
    await this.loadColumnFields()   // 1 request — suốt lúc này loading = false, tableData = []
    await this.loadData()           // tới đây mới bật loading = true
}
```

`V2BaseDataTable` chọn nhánh theo thứ tự `v-if="loading"` → `v-else-if="!data.length"`. Trong khoảng
chờ `loadColumnFields()` thì `loading` vẫn là `false` (khởi tạo ở `data()`) mà `tableData` đã là `[]`
⇒ bảng rơi vào nhánh **Empty state**, người dùng đọc được "Không có dữ liệu phù hợp bộ lọc" trong
khi API danh sách còn chưa được gọi.

- [x] `index.vue` — `loading: false` → **`loading: true`** ở `data()`. Lần vẽ đầu tiên là dòng
      "Đang tải", `loadData()` tự tắt trong `finally`

**Đã kiểm 2 rủi ro kẹt spinner trước khi đổi (đều không xảy ra):**
- `loadColumnFields()` tự nuốt lỗi trong `catch` + set cờ trong `finally` ⇒ không ném ra, `mounted()`
  không bao giờ dừng giữa chừng, `loadData()` luôn chạy
- `loadData()` có nhánh `return` sớm `if (this.isDuplicateLoad(params)) return` KHÔNG đụng `loading`
  — nhưng `DedupeLoadMixin` khởi tạo `lastLoadKey = null` nên lần gọi đầu không thể bị coi là trùng

Đây cũng là cách **màn mẫu** của skill list-page làm sẵn: `pages/assign/customers/index.vue:402`
và `pages/finance/borrow-export-requests/index.vue:301` đều `loading: true`. Màn này lệch chuẩn.

### Verify
- [x] Parse template + script: 0 lỗi · xác nhận `loading: true` tại `index.vue:352`
- [x] Đọc `V2BaseDataTable.vue:104-124` xác nhận thứ tự nhánh loading → empty → data
- [ ] **Mở trình duyệt — user tự xem** (vào màn phải thấy spinner "Đang tải" ngay từ đầu)

⚠️ **Màn ANH EM dính y hệt, CHƯA sửa**: `pages/finance/bill-adjust-depts/index.vue:341` cũng
`loading: false` + cùng khuôn `mounted()`. Thuộc feature khác (`.plans/gop-db/finance-bill-adjust-dept/`)
nên chưa đụng — mọi thay đổi phải có task trong plan của chính feature đó (CLAUDE.md).

---

## Phase 33 — "Chọn nhanh hợp đồng" trong bảng chi tiết (2026-09-04)

User: *"bên erp có chức năng thêm nhanh hợp đồng, bên hrm chưa có, xem kỹ lại logic bên erp rồi bổ
sung"* → chốt: *"làm giống như bên erp, giờ dùng chung db rồi nên lấy được hết dữ liệu"*.

### Đọc kỹ ERP — hoá ra là 2 popup KHÁC NHAU

| | Phiếu **KH** | Phiếu **NCC** |
| --- | --- | --- |
| Nút | `detail.chooseFastContract($index)` (`partials/customer_form.blade.php` :199) | `detail.chooseFastBuyContract($index)` (`supplier_form.blade.php` :195) |
| Modal | `#chooseFastContract` (dựng thẳng trong `create/edit.blade.php`) | `#chooseFastBuyContract` (`partials/choose_fast_buy_contract_modal.blade.php`) |
| Endpoint | `bill_adjust_dept_request.getContractAdjustFrom` | `…getBuyContractsForAdjustList` → `SearchController::collectSupplierBuyContractRows` |
| Áp dụng | `apply()` → `validateInput()` → `handleAdjustTo()` | `applyBuyContracts()` |
| Ghi đè | Xóa mọi dòng **cùng khách hàng** rồi chèn lại | Xóa dòng **trùng mã HĐ mua** rồi chèn lại |
| Chặn | Σ > "điều chỉnh từ" ⇒ chặn; điều chỉnh vào HĐ không nợ ⇒ **hỏi xác nhận, vẫn cho qua** | Σ > "điều chỉnh từ" ⇒ **chặn hẳn**, tô đỏ đúng dòng vượt |
| Ngoại tệ | không | 2 cột "Số tiền điều chỉnh đến": ngoại tệ + VNĐ quy đổi |

### 2 nhánh của ERP CỐ Ý KHÔNG PORT — có bằng chứng, không phải bỏ sót

`is_rule_contract` (checkbox *"Số dư đầu kì"*) và nhóm **dòng con "phiếu xuất hàng / hàng bán mượn"**
dưới mỗi hợp đồng chỉ bật khi `contractable_type = App\Model\Sale\Contract` **VÀ** hợp đồng thuộc
loại *HĐ nguyên tắc / PL HĐNT* (`renderContractableData()` :571, :585).

- Nguồn hợp đồng bán của HRM (popup dùng chung `ContractSearchModal`,
  `BillIncomeRequestService::searchSellContracts()`) chỉ có **3 bảng**: `hrm_contracts` ·
  `opening_contracts` · `wr_service_contracts` — **không có** `contracts` của ERP. Đây là hệ quả
  quyết định #4 (`firm_contracts` → `hrm_contracts`), không phải thiếu dữ liệu
- Đếm trên **13.336 dòng "điều chỉnh đến" thật**: `exportable_id` khác null = **0 dòng**;
  `is_begin = 1` = **0 dòng**; `contractable_type = …Sale\Contract` = **0 dòng**
  (thực tế: FirmContract 11.037 · WrServiceContract 1.584 · OpeningContract 692 · Contract HRM 6)

⇒ Port 2 nhánh đó vào HRM sẽ tạo ra một nhánh **không bao giờ có dữ liệu**. Nếu sau này muốn, phải
thêm `contracts` ERP vào popup chọn hợp đồng trước (đi ngược quyết định #4) — **hỏi user**.

### BE
- [x] `BillAdjustDeptFastPickService` mới:
      · `customerContracts()` — union đúng **3 nguồn** của popup dùng chung + lọc mã HĐ,
        công nợ lấy theo lô bằng `BillAdjustDeptDebtService::remainDebtMany()` (TK 1311)
      · `supplierBuyContracts()` — union **5 nguồn** HĐ mua như `searchBuyContracts()`,
        số dư bằng `supplierBalance()` (TK 3311, `có − nợ`)
- [x] 2 route TĨNH đặt TRƯỚC `/{id}` + 2 method controller
- [x] KHÔNG bê `contract_link` (HTML thẻ `<a>` sang ERP) — HRM trả mã, FE tự dựng

### FE
- [x] `FastContractModal.vue` (KH) · `FastBuyContractModal.vue` (NCC) — select trong modal dùng
      `V2BaseSelectInModal` (CLAUDE.md)
- [x] `AdjustDetailTable.vue` — nút "Chọn nhanh hợp đồng" cạnh "Thêm điều chỉnh", bắn sự kiện kèm
      `detailIndex` (component không tự gọi API — giữ đúng kiến trúc sẵn có)
- [x] `BillAdjustDeptRequestForm.vue` — hứng sự kiện, mở modal, ghi kết quả vào `details[i].items`
      theo đúng quy tắc ghi đè của ERP

### Verify
- [x] `php -l` sạch 4 file BE · parse template + script 3 file FE: 0 lỗi
- [x] Gọi thật qua HTTP kernel + JWT:
      · thiếu tham số → **422** đúng như thiết kế
      · `fast-contracts?customer_id=18505` → HTTP 200, **81 hợp đồng**, đủ 3 nguồn
        (`Assign\Contract` · `OpeningContract` · `WrServiceContract`), có tên NVKD
      · `fast-buy-contracts?supplier_id=11591` → HTTP 200, **9 hợp đồng mua**, đủ số dư 3311
      · lọc `contract_code` ăn trên MỌI nhánh union: 9 → 1 dòng
      · `search-customers?is_supplier=1` → 50 dòng, kiểm từng dòng đều `is_supplier = 1`
- [x] **Đối chiếu số tiền với truy vấn tay**: công nợ HĐ-TEST-DNTT-01 API trả `976,487,940`,
      truy vấn thẳng `account_details` (TK 1311, nợ − có) ra `976,487,940` → **KHỚP**
- [x] Sắp xếp nợ giảm dần đúng như bộ so sánh ERP

- [ ] **Mở trình duyệt — user tự xem** (chưa kiểm chứng bằng mắt: bố cục popup, nhập tiền, Áp dụng)

### 33.1 Chưa chọn KH/NCC vẫn mở được popup hợp đồng (fix cùng ngày)

User: *"khi chưa chọn khách hàng, nhà cung cấp vẫn đang cho mở popup hợp đồng mua/đơn hàng,
disable lại cho tôi, phải chọn khách hàng/NCC trước thì mới cho chọn"*.

Ô chọn hợp đồng ở bảng chi tiết (cả vế "từ" lẫn vế "đến") là `V2BaseInput readonly` + `@click.native`
→ bấm lúc nào cũng mở popup, kể cả khi ô đối tượng còn trống.

- [x] `AdjustDetailTable.vue` — thêm `hasParty(row, side)` (bám **ID** chứ không phải tên: dòng nạp
      từ phiếu báo có có thể có id mà chưa có tên) + `requirePartyHint`
- [x] `:disabled="!hasParty(...)"` — phần NHÌN: nền `#f1f5f9`, chữ `#475569`, con trỏ `not-allowed`
      (style chung `v2-styles.scss` lo sẵn, skill select-and-input-state §3 — không tự đặt màu)
- [x] `@click.native` gọi `pickContract()` có chặn đầu hàm + toast nhắc, thay cho `$emit` thẳng
- [x] `:title` đổi thành câu nhắc khi ô đang khoá (rê chuột biết vì sao không bấm được)

⚠️ **`:disabled` MỘT MÌNH KHÔNG chặn được** — bẫy phải biết: `V2BaseInput` có thẻ gốc là
`<div class="v2-input__wrapper">` bọc ngoài `<input>`, nên `@click.native` gắn vào **DIV**. Input bên
trong bị `disabled` thì trình duyệt vẫn phát click trên div và popup vẫn mở như cũ. Chốt chặn thật
bắt buộc nằm trong handler (đúng tinh thần skill select-and-input-state §3 cho ô tự dựng bằng `<div>`).

### Verify 33.1
- [x] Parse template + script: 0 lỗi
- [x] Đọc `V2BaseInput.vue` :1-12 xác nhận thẻ gốc là `<div>`, `$attrs` mới xuống tới `<input>`
- [x] Lớp sau cùng vẫn fail-closed sẵn: gọi thẳng API thiếu tham số →
      `search-contracts` **422 "Vui lòng chọn khách hàng trước"** ·
      `search-buy-contracts` **422 "Vui lòng chọn nhà cung cấp trước"**
- [ ] **Mở trình duyệt — user tự xem**

---

## Phase 31 — "Số tiền còn lại" ra `-0`, "Tổng cộng" bị làm tròn (2026-09-04)

User (kèm ảnh): *"Số tiền còn lại và tổng cộng đang bị làm tròn => Hiển thị đúng gt thực"*.

Tái hiện bằng đúng số trên ảnh (4 dòng `10` + 1 dòng `1,999,960.15`, số tiền từ `2,000,000`):

| | Giá trị THẬT | Đang hiện |
| --- | --- | --- |
| Tổng cộng | 2,000,000.15 | **2,000,000** |
| Số tiền còn lại | −0.15 | **−0** |

**2 lỗi chồng nhau, không phải 1:**

1. `formatMoney(value, digits)` đặt `maximumFractionDigits: digits`, mà phiếu KH gọi với
   `digits = 0` ⇒ **cắt mất phần lẻ có thật**. Đây mới là cái user nhìn thấy.
2. Dòng "Số tiền còn lại" tô đỏ theo `moneyRemaining(detail) !== 0` — **so sánh float chính xác**.
   `0.1 + 0.2 !== 0.3`, nên nhóm chia hết đúng vẫn còn dư ~1e-10 ⇒ in ra `-0` **và bị tô đỏ oan**.
   Lỗi này ẩn dưới lỗi 1, sửa mỗi lỗi 1 là nó lộ ra ngay.

- [x] `formatMoney()` — `digits` thành số lẻ TỐI THIỂU:
      `maximumFractionDigits: Math.max(digits, 2)`. Số tròn vẫn in gọn `2,000,000`, số có lẻ in đủ
      `2,000,000.15`; ngoại tệ vẫn luôn 2 số lẻ như cũ
- [x] Thêm `remainingOf(detail)` — khử sai số dấu phẩy động, `|remaining| < 0.0001` thì trả thẳng `0`.
      Dùng ĐÚNG ngưỡng `0.0001` mà `isTotalBalanced()`, `isGroupUnbalanced()` và luật BE
      (`validateBusinessRules()`: `abs($sumNew - $moneyOld) > 0.0001`) đang dùng — 3 nơi không được
      kết luận khác nhau trên cùng một phiếu
- [x] Dòng "Số tiền còn lại" đổi sang `remainingOf` cho cả giá trị lẫn class `text-danger`
- [x] Soát chỗ hiển thị số dư lệch còn lại (dòng 207-208, "còn thiếu / thừa"): đã có `v-if`
      `isGroupUnbalanced()` chặn bằng ngưỡng `0.0001` nên không dính nhiễu float; số lẻ giờ cũng
      hiện đúng nhờ `formatMoney` mới → giữ nguyên

### Verify
- [x] Parse template + script: 0 lỗi
- [x] Chạy lại đúng thuật toán trên 5 kịch bản:

      | Kịch bản | Còn lại | Tô đỏ | Tổng cộng |
      | --- | --- | --- | --- |
      | Ảnh user (lệch 0.15) | −0.15 | có | 2,000,000.15 |
      | Chia hết chính xác | 0 | không | 2,000,000 |
      | Chia hết nhưng sai số float (0.1+0.2 vs 0.3) | 0 | không | 0.3 |
      | Số tròn, chia hết | 0 | không | 5,000,000 |
      | Còn thừa nhiều | 1,500,000 | có | 500,000 |

- [ ] **Mở trình duyệt — user tự xem**

⚠️ Chỉ sửa HIỂN THỊ, KHÔNG đụng dữ liệu đã lưu (CLAUDE.md). Phiếu trên ảnh đang lệch **0.15** thật —
sau khi sửa nó sẽ hiện `-0.15` màu đỏ đúng như bản chất, và BE vốn đã chặn gửi duyệt bằng cùng
ngưỡng đó. Đây là hiện đúng lỗi sẵn có, không phải phát sinh lỗi mới.

---

## Phase 34 — Phiếu NCC: ô Tỷ giá + bố cục đầu phiếu (2026-09-04)

User: *"Thêm mới loại phiếu = Điều chỉnh công nợ NCC: Chọn tiền tệ = VND bị mất ô tỷ giá, chọn các
loại tiền tệ khác thì k tự động fill tỷ giá tương ứng, cái tiền tệ cho lên cùng dòng với phần phòng
ban"* → *"cho cái diễn giải lên cùng hàng luôn"*.

### 34.1 Chọn VNĐ là mất ô Tỷ giá
ERP `form.blade.php` :71 chỉ xét `ng-if="request_type == 2"` — ô Tỷ giá hiện với **mọi** loại tiền
của phiếu NCC. HRM gài thêm `v-if="isForeignCurrency"` nên chọn VNĐ là ô biến mất.

- [x] Bỏ điều kiện `isForeignCurrency` khỏi `v-if` của ô Tỷ giá
- [x] Dấu **bắt buộc** thì vẫn chỉ gắn khi NGOẠI TỆ (`isForeignCurrency`): VNĐ luôn là 1, không phải
      nhập — đúng như ERP (nhãn "Tỷ giá" của ERP không có `required-label`)

### 34.2 Đổi loại tiền không tự điền tỷ giá
ERP có `BillAdjustDeptRequest::changeCurrency()` (`exchange_rate = currency.exchange_rate || 1`),
HRM chưa port → chọn USD xong ô Tỷ giá vẫn đứng nguyên số cũ, người lập phải tự tra rồi gõ tay.

- [x] BE `currencies()` — trả thêm cột **`exchange_rate`** (bảng `currencies` vốn đã có sẵn dữ liệu
      thật: VNĐ 1 · USD 26.520 · EUR 30.792,68 · JPY 166,01 …)
- [x] FE `onChangeCurrency()` — điền tỷ giá của đúng loại tiền vừa chọn, thiếu số thì lùi về **1**
      (KHÔNG để trống — trống là bảng chi tiết chia cho 0), rồi `remapMoneyOld()` vì đổi giữa
      nội tệ ↔ ngoại tệ là đổi luôn vế tiền
- [x] `onChangeRequestType()` — chuyển sang phiếu NCC mà chưa có loại tiền thì mặc định **VNĐ (id 1)
      kèm đúng tỷ giá của nó**, port setter `request_type` của ERP; không thì ô Tỷ giá vừa hiện ra
      đã trống

### 34.3 Gộp bố cục đầu phiếu về MỘT hàng
Trước: 3 `form-row` rời (Loại phiếu/Mã phiếu/Người tạo/Phòng ban — Số phiếu báo có/Tiền tệ/Tỷ giá —
Diễn giải) làm đầu phiếu bị chia vụn.

- [x] Gộp còn **1 `form-row`**, thứ tự: Loại phiếu · Mã phiếu (khi Sửa) · Người tạo · Phòng ban ·
      **Tiền tệ · Tỷ giá** (NCC) · Số phiếu báo có (khi có) · **Diễn giải** (md-6)
- [x] "Số phiếu báo có" thu từ `col-md-4` → `col-md-3` cho khớp lưới 4 cột của hàng

### Verify
- [x] `php -l` sạch · parse template + script: 0 lỗi
- [x] Gọi thật `GET /finance/bill-adjust-dept-requests/currencies` → HTTP 200, khoá trả về đúng
      `id, code, name, exchange_rate`
- [ ] **Mở trình duyệt — user tự xem**: tạo phiếu NCC → ô Tỷ giá hiện cả khi VNĐ; đổi sang USD thì
      tỷ giá tự nhảy 26.520; đầu phiếu còn 1 hàng

### 34.4 VNĐ: tỷ giá = 1 và KHOÁ không cho sửa (2026-09-04)

User: *"khi chọn vnd thì tỉ giá là 1 và không được sửa nữa chứ"*.

⚠️ **Đây là chỗ HRM CỐ Ý chặt hơn ERP.** ERP để ô tỷ giá gõ được với mọi loại tiền — ô
`<input ng-model="form.exchange_rate">` (`form.blade.php` :76, :95) **không có** `ng-disabled`.
User chốt khoá lại vì tỷ giá VNĐ khác 1 là vô nghĩa.

- [x] FE — `:disabled="readonly || !isForeignCurrency"` cho ô Tỷ giá
- [x] FE — chọn VNĐ thì **chốt cứng 1**, không lấy theo `currencies.exchange_rate` (phòng khi danh
      mục bị sửa nhầm)
- [x] BE — `normalizedExchangeRate()`: phiếu NCC + `currency_id = VNĐ` ⇒ **ép 1**; phiếu KH ⇒ `null`.
      Không dựa vào FE khoá ô (defense-in-depth, CLAUDE.md)

**Đã soát ảnh hưởng trước khi sửa:** `syncDetails()` vốn đã bỏ qua tỷ giá khi không phải ngoại tệ
(`$useRate = $isSupplier && isForeignCurrency() && $rate > 0`) nên `total_amount` KHÔNG bị ảnh hưởng
bởi thay đổi này — chuẩn hoá chỉ để dữ liệu lưu xuống không nói dối.

### Verify 34.4
- [x] `php -l` sạch · parse template + script: 0 lỗi
- [x] **Gọi THẲNG API** (bỏ qua giao diện) `POST /bill-adjust-dept-requests` với
      `currency_id = 1` + `exchange_rate = 26520` → HTTP 200, đọc lại DB:
      `currency_id=1, exchange_rate=1.0000` ⇒ BE ép đúng, không dựa vào FE
- [x] Đã xoá bản ghi kiểm tra (id 10317). `generateCode()` sinh mã theo `MAX(...)` nên xoá xong số
      thứ tự trả về như cũ, không để lại lỗ hổng mã
- [ ] **Mở trình duyệt — user tự xem**

### 34.5 Bỏ tự điền "KHÁCH KHÔNG RÕ" khi đổi loại phiếu sang NCC (2026-09-04)

User: *"hiện tại đang tự động fill tên KH khi đổi Loại phiếu sang NCC: 29TPHPTH-203 - KHÁCH KHÔNG RÕ,
bỏ đi cho tôi"*.

**Soát lại ERP thì đây là HRM gắn thêm, không phải port đúng.** ERP chỉ đặt mặc định "KHÁCH KHÔNG RÕ"
ở **luồng nạp dòng từ PHIẾU BÁO CÓ** (`formJs.blade.php` :91-98 và `create.blade.php` :214-219 — điều
kiện `response.data.currency_id && exchange_rate && request_type == 2`). Setter `request_type` của
ERP chỉ lo tiền tệ + `remapMoneyOld()`, **không đụng tới nhà cung cấp**. HRM lại gắn vào
`onChangeRequestType()` nên vừa đổi sang NCC là ô đã có sẵn tên, người lập tưởng đã chọn xong.

- [x] Bỏ khối tự gán `supplier_old_id`/`supplier_old_name` trong `onChangeRequestType()`
- [x] **GIỮ** nhánh phiếu báo có (`detailFromReportRow()` :669) — đó mới là chỗ ERP đặt mặc định
- [x] Dọn state chết do thay đổi này để lại: `undefinedCustomerName` không còn chỗ nào đọc
      (nhánh báo có dùng chuỗi riêng), bỏ luôn cả dòng gán trong `loadMeta()`.
      `undefinedCustomerId` vẫn giữ vì nhánh báo có còn dùng

**Đã soát an toàn trước khi bỏ:** `details.*.supplier_old_id` ở `StoreRequest` là `nullable|integer`
và cột `bill_adjust_dept_request_details.supplier_old_id` là **NULL = YES** ⇒ để trống không làm vỡ
validate hay 500 khi lưu.

### Verify 34.5
- [x] Parse template + script: 0 lỗi
- [x] `grep undefinedCustomer` — chỉ còn 4 chỗ, đều thuộc nhánh phiếu báo có
- [ ] **Mở trình duyệt — user tự xem**: tạo phiếu mới → đổi Loại phiếu sang NCC → ô Nhà cung cấp
      phải TRỐNG; còn vào màn từ nút "Tạo phiếu YC điều chỉnh" ở phiếu báo có thì vẫn điền như ERP

---

## Phase 35 — Xuất Excel: đưa về đúng chuẩn skill export-excel (2026-09-04)

User: *"sửa lại xuất excel màn này theo chuẩn skill cho tôi"*.

Rà 2 file xuất của màn (1 phiếu + danh sách) theo checklist mục 8 của skill, thấy **2 nhóm lỗi**:

### 35.1 Ô tiền là CHUỖI, không phải số (skill mục 1)
Blade dùng `number_format((float) $x)` → ra `"2,135,916"`, ô vào Excel kiểu **CHUỖI**: tam giác xanh
*"The number in this cell is formatted as text"*, SUM/lọc/pivot ra 0. Dính **12 ô**: `balance`,
`balance_vnd`, `money`, `money_vnd` (cả 2 vế từ/đến), `total_from`, `total_to`, `exchange_rate`,
và `total_amount` của bản danh sách.

- [x] Thêm closure `$num()` in **số thô** (khuôn `excelNumber()` của skill), mốc `rtrim` là dấu
      **thập phân `.`** — dùng nhầm `,` là ăn xuyên dấu ngăn nghìn (bẫy 1 mục 1b)
- [x] Gắn `data-format` theo **từng nhóm cột**, không dùng chung 1 mã (mục 1a):
      `#,##0` cho cột VNĐ · `#,##0.00` cho cột nguyên tệ của phiếu ngoại tệ và ô Tỷ giá.
      **Không** dùng `#,##0.##` — mã đó ép cứng 2 số lẻ, số tròn ra `5.00` (bẫy 2 mục 1b)
- [x] Giữ `text-align: right` tay cho cột tiền (ô rỗng là chuỗi, Excel canh trái sẽ lệch cột)

### 35.2 Letterhead in ra CHỮ, không phải ảnh (skill mục 4)
Blade cũ `{!! $data['header'] !!}` — HTML reader của PhpSpreadsheet **không tải ảnh từ URL**, nên ô
đó chỉ hiện chuỗi đường dẫn. Thêm nữa khoá `header` của Resource là **path tương đối theo công ty
NGƯỜI TẠO**, sai cả khuôn letterhead của CLAUDE.md.

- [x] `BillAdjustDeptRequestExport` — thêm `WithDrawings` + `WithEvents` + trait dùng chung
      `EmbedsCompanyLetterhead`; `fitLetterheadRow()` chỉ nới cao dòng khi ảnh vào được thật
- [x] Blade — dòng 1 để **TRỐNG** làm chỗ neo ảnh A1
- [x] Controller `export()` — đổ `header` bằng `BillAdjustDeptRequestPrintService::headerUrl()`
      (theo `company_id` GHI TRÊN CHỨNG TỪ, URL tuyệt đối). Đổi `headerUrl()` thành `public`:
      **một nguồn duy nhất cho cả bản in lẫn Excel**

### Verify — dựng file THẬT rồi đọc lại bằng PhpSpreadsheet (skill mục 7)
- [x] `php -l` sạch 3 file BE
- [x] **Phiếu KH** (id 10316): 1 drawing trong file · cao dòng 1 = 58 · **0 ô "số lưu dạng chuỗi"** ·
      ô tiền kiểu `n` `fmt=#,##0` → `300,000`
- [x] **Phiếu NCC ngoại tệ** (id 10307): 1 drawing · **0 ô "số lưu dạng chuỗi"** · 15 ô số, đúng 2
      mã: `#,##0.00` → `25,000.00` (tỷ giá) và `10,777,542.19` (nguyên tệ) · `#,##0` →
      `269,438,554,800` (VNĐ quy đổi)
- [x] **Bản danh sách** (30 dòng): **0 ô "số lưu dạng chuỗi"**, `F4 fmt=#,##0 → 300,000`
- [x] Ảnh letterhead **tải được ở local** (`companies.header` đã là URL tuyệt đối) — không phải chỉ
      suy luận
- [x] Đã xoá file .xlsx kiểm tra khỏi scratchpad
- [ ] **Mở file trong Excel — user tự xem** (dấu ngăn cách hiển thị theo Regional Settings của máy;
      nếu ra dấu phẩy thì đổi Windows Regional format sang Vietnam, KHÔNG sửa code — skill mục 1b)

**Không đụng bản in**: 2 nhánh dùng blade riêng (`prints/` vs `exports/`), sửa `exports/` không ảnh
hưởng bản in — đã soát theo cảnh báo mục 2 của skill.

---

## Phase 36 — Excel: logo, wrap, in đậm nhãn, 5 chức vụ ký, lỗi xuất danh sách (2026-09-04)

User liệt kê 5 điểm + báo *"Click Xuất toàn bộ danh sách, k lọc đang báo lỗi máy chủ"*.

### 36.1 "Mất logo" — KHÔNG phải code, là MẠNG
File tải qua đúng đường HTTP có `xl/media/*.png` + drawing `letterhead 808x72 @A1`. Nhưng đo 4 lượt
liên tiếp bắt được **1 lượt hỏng**: 8,6s và `drawings = 0`.

Cơ chế: trait `EmbedsCompanyLetterhead::fetchLetterheadImage()` tải ảnh từ
`https://erp.eteksofts.com/uploads/...` **mỗi lần xuất**, có timeout; máy chủ API không với tới host
đó trong thời gian chờ ⇒ trait bỏ ảnh (cố ý — "mất logo còn hơn mất cả file") và người dùng thấy
"mất logo" ngẫu nhiên.
- [x] Xác minh code đúng: 3 lượt sau đó đều `drawings = 1`, mỗi lượt 0,2-0,3s
- [ ] **Chưa xử lý gốc** — cách chặn hẳn là **cache ảnh** thay vì tải lại mỗi lần, nhưng
      `EmbedsCompanyLetterhead` là **trait DÙNG CHUNG** (Phiếu thu/Phiếu chi… cũng dùng) ⇒
      CLAUDE.md bắt hỏi trước khi sửa. **Chờ user chốt.**

### 36.2 Căn xuống dòng cho cột chữ dài
- [x] File **1 phiếu** — `AfterSheet`: wrap + căn TRÊN cho cả vùng, tính từ `getHighestRow()`
      (không viết cứng số dòng, skill mục 5). Đã kiểm: ô tên KH `A15` có `wrapText = true`
- [x] File **danh sách** — CHỈ wrap **hàng tiêu đề**. Lý do ở mục 36.5

### 36.3 Định dạng cột tiền
- [x] Đã xong từ Phase 35; đo lại trên file tải thật: **0 ô "số lưu dạng chuỗi"** ở CẢ 2 file

### 36.4 In đậm nhãn + đủ 5 chức vụ ký
- [x] In đậm 7 nhãn khối thông tin (Mã phiếu, Loại phiếu, Số phiếu báo có, Người lập, Phòng ban,
      Tỷ giá, Diễn giải) — kiểm trên file: `Mã phiếu:` có `bold = true`
- [x] Khối ký từ **2 → 5 chức vụ** đúng bản in: BAN GIAM ĐỐC · KẾ TOÁN TRƯỞNG · NGƯỜI NỘP TIỀN ·
      NGƯỜI LẬP PHIẾU · NGƯỜI NỘP TIỀN, kèm dòng ngày ở trên. Giữ nguyên 2 quirk của mẫu ERP
      (thiếu dấu "BAN GIAM ĐỐC", "NGƯỜI NỘP TIỀN" lặp 2 lần).
      **KHÔNG** đưa ô "THỦ QUỸ" sang: mẫu in để cỡ chữ 1px (tàng hình), Excel không có khái niệm đó
      nên đưa sang là hiện ra chức vụ thứ 6 mà bản in không có

### 36.5 Xuất toàn bộ danh sách báo lỗi máy chủ — TÌM RA GỐC
Đo bằng query log, tách 3 chặng trên 5.000 dòng:

| Chặng | Trước | Sau |
| --- | --- | --- |
| `allForExport` | 0,59s · 21 query | 0,63s · 24 query |
| `ListResource` | **15,41s · 15.004 query** | **1,95s · 4 query** |
| Dựng file Excel | 17,46s | 17,46s |
| **Tổng endpoint** | **38,1s** · 348 MB | **22,9s** |

**Gốc: N+1.** Docblock của `ListResource` ghi rõ service phải `with('employee_update.info')` cho cột
"Người cập nhật", nhưng `allForExport()` **thiếu đúng quan hệ đó** → 5.000 dòng đẻ ~15.000 query.
`searchByFilter()` (bản phân trang) thì có, nên lỗi chỉ lộ ở xuất Excel.

- [x] Bổ sung `employee_update.info` vào `allForExport()` → **15.004 → 4 query**
- [x] Gỡ wrap toàn vùng ở bản danh sách: `getStyle('A1:L5003')` tốn thêm **~18 giây**
      (22,9s → 38s) vì PhpSpreadsheet style theo TỪNG Ô
- [ ] **Còn 22,9s** — phần lớn là 17,5s dựng file của HTML reader (60.000 ô). Chờ user chốt hướng
      (giảm trần dòng / đổi sang `FromArray`)

### Verify
- [x] `php -l` sạch 4 file BE
- [x] Tải file THẬT qua HTTP kernel rồi đọc ngược bằng PhpSpreadsheet — cả 2 file: 0 ô số dạng chuỗi,
      wrap đúng chỗ, nhãn in đậm, khối ký 5 chức vụ, `drawings = 1`
- [x] Đã xoá file .xlsx kiểm tra khỏi scratchpad
- [ ] **Mở bằng Excel — user tự xem**

### 36.6 Xuất danh sách chuyển `FromView` → `FromArray` (user chốt 2026-09-04)

Sau khi sửa N+1 vẫn còn 22,9s, trong đó **17,5s là bước HTML reader** phân tích lại blade
(5.000 dòng × 12 cột = 60.000 ô). User chốt đổi hẳn cách dựng file.

- [x] `BillAdjustDeptRequestListExport` viết lại theo `FromArray` — nạp thẳng mảng vào sheet,
      không qua vòng HTML
- [x] Tiêu đề lớn / in đậm tên cột / viền / định dạng số / autofilter chuyển sang `AfterSheet`,
      vùng ô tính từ `getHighestRow()`
- [x] Xoá blade `exports/bill_adjust_dept_request_list.blade.php` (không còn dùng)
- [x] KHÔNG đóng băng hàng tiêu đề (skill mục 4c, user chốt 2026-08-25)

**2 bẫy đã dính khi làm, ghi lại kẻo lặp:**
1. **Dòng trống phải là `['']`, không phải `[]`** — mảng rỗng bị bỏ qua khi ghi vào sheet nên cả
   bảng dồn lên 1 dòng, hàng tên cột rơi xuống dòng 2 (đo thật: `A3` ra `"1"` thay vì `"STT"`).
2. **Ghép dải ô `$headingRange . ':' . $lastColumn . $lastRow` cho ra `A3:L3:L5003`** — dải 3 vế
   KHÔNG hợp lệ, PhpSpreadsheet **nuốt im lặng**: file ra không có viền, autofilter sai, không lỗi
   nào báo. Phải dựng dải ô từ đầu.

**Đo lại sau khi sửa** — kẻ viền đủ cả bảng mà vẫn nhanh: chi phí style cao lúc trước là do sheet
dựng từ HTML (mỗi ô một style riêng), không phải do kẻ viền.

| | Ban đầu | Sau sửa N+1 | Sau `FromArray` |
| --- | --- | --- | --- |
| Thời gian | **38,1s** | 22,9s | **5,4-8,7s** |
| Bộ nhớ đỉnh | 348 MB | — | **162 MB** |
| Query | 15.025 | 28 | 28 |

### Verify 36.6
- [x] Tải file THẬT qua HTTP: danh sách HTTP 200 · 5.003 dòng · `A3="STT"` in đậm · viền `thin`
      tới B4 · autofilter `A3:L5003` · `F4` kiểu `n` `fmt=#,##0` → `300,000` · 0 ô số dạng chuỗi
- [x] File 1 phiếu HTTP 200 · 0,7s · `drawings = 1` (logo) · wrap ô tên KH · **đủ 5 chức vụ ký**
- [x] Đã xoá file .xlsx kiểm tra khỏi scratchpad

### 36.7 Cache letterhead — CHƯA LÀM, user chốt tự báo team
Logo thỉnh thoảng mất do trait `EmbedsCompanyLetterhead` tải ảnh từ `erp.eteksofts.com` **mỗi lần
xuất** (bắt được 1 lượt hỏng: 8,6s + `drawings = 0`). Cách chặn hẳn là cache ảnh, nhưng trait là
**tài sản dùng chung** (Phiếu thu/Phiếu chi cũng dùng) → user tự đưa ra PR cho cả hệ thống.

---

## Phase 37 — Điều tra: ô chọn hợp đồng HRM ra 3, ERP ra 2 (2026-09-04)

User: *"Chọn KH = CÔNG TY CP VIN HN → HRM hiển thị 3 hợp đồng nhưng ERP chỉ 2. Check lại logic"*.

### Dữ liệu thật của KH id 3021 (`35TNIHBA-2`)

| Bảng | Mã | `created_by` | Ghi chú |
| --- | --- | --- | --- |
| `hrm_contracts` | HĐ-TEST-DNTT-03 | 13 | status 9 |
| `opening_contracts` | HĐ-TEST-DNTT-DK-03 | 13 | |
| `wr_service_contracts` | HĐ-TEST-DNTT-BD-03 | 13 | status 3, type 1 |
| `firm_contracts` | HĐ_TPE_HN_KD3_26_0594_Q27-07 | **72** (Hồ Thị Xuân) | status 1, type 1 |

### KHÔNG phải lỗi — 2 hệ đọc 2 bảng hợp đồng khác nhau

`SearchContractService::searchAllContract()` nhánh `create_bill_adjust_dept_request` (:190-193):
nguồn = `firm_contract` + `wr_contract` + `opening_contract`, **KHÔNG có** `hrm_contracts`
(bảng của HRM, ERP không biết).

HRM đổi nguồn hợp đồng bán `firm_contracts` → `hrm_contracts` theo **quyết định #4** của chính
feature này. Nên:
- **ERP = 2**: đầu kỳ + bảo dưỡng. Hợp đồng `firm_contracts` bị loại vì `created_by = 72` ≠ người
  đăng nhập (13) — ERP chỉ cho chọn hợp đồng **do chính mình tạo**
- **HRM = 3**: đầu kỳ + bảo dưỡng + **`hrm_contracts` HĐ-TEST-DNTT-03** (nguồn ERP không có)

Đã gọi API thật xác nhận đúng 3 dòng đó (`/bill-income-requests/search-contracts?customer_id=3021`).

### ⚠️ 2 LỖ HỔNG THẬT phát hiện kèm — HRM đang LỎNG hơn ERP

1. **Thiếu lọc `created_by = người đang đăng nhập`.** ERP áp cho **cả 3 nguồn**
   (`extrated()` :292 `$query->where('created_by', $user_id)`, cộng thêm 1 lần nữa trên
   `opening_contract` ở :192). HRM không lọc ⇒ người lập thấy cả hợp đồng của người khác.
   Bộ dữ liệu này tình cờ không lộ (cả 3 dòng đều `created_by = 13`).
2. **Thiếu lọc trạng thái/loại** cho `opening_contracts` + `wr_service_contracts`:
   - ERP `wr_contract`: status NOT IN [Đang tạo, Chờ duyệt, Hủy] **và** type IN [Hợp đồng]
   - ERP `firm_contract`: status NOT IN [Đang tạo, Chờ duyệt, Từ chối] **và**
     type IN [Hợp đồng, HĐ dự án, Đơn hàng nguyên tắc]
   - HRM: `hrm_contracts` có lọc status (6,8,9,10,11,12) nhưng `opening`/`wr` **không lọc gì**

### Chưa sửa — chờ user chốt
Endpoint `bill-income-requests/search-contracts` **DÙNG CHUNG** với màn Đề nghị thu tiền ⇒ CLAUDE.md
bắt hỏi trước khi đổi. Cách sửa **không đụng màn kia**: `ContractSearchModal` đã có sẵn prop
`extraParams`, truyền `{ only_mine: 1 }` từ riêng màn này là đủ cho lỗ hổng #1
(`searchSellContracts()` đã hỗ trợ `only_mine`, hiện áp cho `hrm` + `wr`, **chưa** áp cho `opening`).

### 37.1 Bịt 2 lỗ hổng (user chốt 2026-09-04)

Làm theo hướng **OPT-IN bằng cờ `usage`**, KHÔNG đổi hành vi mặc định của endpoint dùng chung —
mỗi màn của ERP có bộ lọc hợp đồng riêng (cùng bảng `wr_service_contracts` mà màn Đề nghị thu tiền
`create_bill_income` lọc trạng thái khác hẳn), nên áp mặc định là hỏng màn khác.

- [x] BE `BillIncomeRequestService` — thêm `USAGE_ADJUST_DEPT_REQUEST` + khối lọc:
      · `created_by = người đang đăng nhập` cho **cả 3 nguồn** (`hrm_contracts` · `opening_contracts`
        · `wr_service_contracts`) — port `extrated()` :292 + :192.
        Fail-closed: chưa đăng nhập trả rỗng, KHÔNG rơi về `created_by is null`
      · `wr_service_contracts`: `status NOT IN [0,1,2]` (Hủy · Đang tạo · Chờ duyệt) **và**
        `type = 1` (Hợp đồng) — port `extrated()` :288-291
      · `opening_contracts` KHÔNG lọc trạng thái/loại — ERP cũng không, chỉ lọc người tạo
- [x] **Cố ý KHÔNG gộp vào cờ `only_mine`** sẵn có: cờ đó của màn Đề nghị thanh toán, có ghi chú rõ
      là *không* áp cho hợp đồng đầu kỳ; màn này thì ERP CÓ lọc. 2 màn 2 luật
- [x] FE — `ContractSearchModal` nhận `:extra-params="{ usage: 'bill_adjust_dept_request' }"`,
      chỉ ở màn này

### Verify 37.1
- [x] `php -l` sạch · parse template + script FE: 0 lỗi
- [x] **Lỗ hổng #1 đã bịt** — đăng nhập bằng **id 72** (không tạo hợp đồng nào của KH 3021):
      trước **3 hợp đồng** (thấy cả của người khác) → sau **0**
- [x] **Không đổi màn khác** — cùng KH, không truyền cờ: vẫn đúng **3** hợp đồng như cũ
- [x] Đăng nhập id 13 (chủ cả 3 hợp đồng) + có cờ: vẫn **3** — lọc không bắt oan
- [x] **Lỗ hổng #2**: trên 6.690 hợp đồng bảo dưỡng, chỉ **2.295** đạt điều kiện ERP;
      **4.395 dòng** trước đây chọn được mà lẽ ra không
- [x] Rà toàn bộ FE: chỉ 2 màn truyền `extraParams` cho popup dùng chung — màn này (`usage`) và
      Đề nghị thanh toán (`only_mine`); các màn còn lại không truyền gì ⇒ không đổi
- [ ] **Mở trình duyệt — user tự xem**

⚠️ **Vẫn còn chênh 3 (HRM) vs 2 (ERP) và đó là ĐÚNG**: hợp đồng thứ 3 là `hrm_contracts`
HĐ-TEST-DNTT-03 — nguồn mà ERP không có (quyết định #4). Không phải lỗi, không sửa.

### 37.2 Đối chứng thêm: KH "XÍ NGHIỆP XE BUÝT CẦU BƯƠU…" (id 14545)

User yêu cầu kiểm tra khách hàng này có bị tương tự không → **CÓ, và nặng hơn nhiều**.

KH này chỉ có **14 dòng ở `wr_service_contracts`** (0 hợp đồng HRM · 0 đầu kỳ · 0 `firm_contracts`):

| Nhóm | Số dòng | `type` | `status` | Người tạo |
| --- | --- | --- | --- | --- |
| `HDDV_TPE_HN_KD1_*` | 5 | 1 = **Hợp đồng** | 3, 5 | 28 – Nguyễn Thành Bộ |
| `TPE.PBH.*` | 9 | 2 = **Bảo hành** | 2 = Chờ duyệt | 237, 242 |

⇒ **9 dòng `TPE.PBH.*` không phải hợp đồng mà là PHIẾU BẢO HÀNH đang CHỜ DUYỆT** — ERP không bao giờ
cho chọn (trượt cả 2 điều kiện `type = 1` và `status NOT IN [0,1,2]`), HRM trước đây cho chọn hết.

Đo bằng API thật, trước/sau khi bật cờ `usage`:

| Người đăng nhập | Trước | Sau |
| --- | --- | --- |
| id 28 – Nguyễn Thành Bộ (người tạo 5 hợp đồng) | **14** | **5** ✅ |
| id 242 – Vũ Đình Cẩn | **14** | **0** ✅ |
| id 237 – Nguyễn Tiến Đệ | **14** | **0** ✅ |
| id 13 – Nguyễn Thị Cần | **14** | **0** ✅ |

Khớp đúng ERP: chỉ người lập hợp đồng mới chọn được, và chỉ chọn được HỢP ĐỒNG đã qua duyệt.

---

## Phase 38 — Nền header "Thông tin chung" / "Chi tiết" khác nhau giữa local và server (2026-09-04)

User: *"cùng 1 code mà trên server chỗ header Thông tin chung, Chi tiết background lại không giống
dưới local"*.

### Gốc — class `.section-header` KHÔNG có trong style dùng chung
`grep` toàn bộ `assets/scss/`: **không có** `.section-header`. Class này chỉ tồn tại trong `<style>`
của **hơn 20 file .vue** riêng lẻ, mỗi màn khai lại y hệt nhau.

`BillAdjustDeptRequestForm.vue` **dùng class mà không khai** (file trước đây không có `<style>` nào,
create/edit/detail chỉ `@import v2-styles.scss`). Nên nó chỉ hiển thị đúng khi CSS của một màn KHÁC
tình cờ đã được nạp:

| Môi trường | Vì sao khác |
| --- | --- |
| **Local** `npm run dev` | CSS chèn thẳng vào `<head>` theo module; ghé qua màn Tài chính khác (Phiếu thu/Phiếu chi/Ủy nhiệm chi — 3 màn này khai `.section-header` **không scoped**) là style còn nằm đó ⇒ nhìn ĐÚNG |
| **Server** (bản build) | CSS tách theo từng route. Vào thẳng `/finance/bill-adjust-dept-requests/create` thì không route nào nạp `.section-header` ⇒ đầu card rơi về `.card-header` mặc định của Bootstrap (nền xám) |

Cùng một commit, khác nhau chỉ vì **thứ tự màn đã ghé thăm** — nên rất khó tái hiện ở local.

- [x] Thêm `<style scoped>` vào `BillAdjustDeptRequestForm.vue`, tự khai `.card-header.section-header`
- [x] Giá trị copy nguyên từ 3 màn Tài chính đã nghiệm thu (`BillIncomeForm` · `BillPaymentForm` ·
      `BillPaymentAuthorizationForm` — cả 3 khai **giống hệt nhau**, và bản `scoped` trong
      `BillIncomeRequestForm` cũng trùng): nền `#fff`, viền dưới `#e5e7eb`, padding ngang 10px,
      chữ tiêu đề 14px `#1f2937`
- [x] Dùng `scoped` — 2 thẻ mang class này nằm trong chính template của component, không cần lan ra

### Verify
- [x] Parse template + script: 0 lỗi · SFC có đúng **1 style block, `scoped = true`**
- [x] Biên dịch SCSS bằng `sass`: OK
- [ ] **Mở trình duyệt trên CẢ 2 môi trường — user tự xem** (đây là lỗi chỉ lộ ở bản build)

⚠️ **Vấn đề hệ thống, nên đưa ra PR riêng (KHÔNG tự sửa — tài sản chung):** `.section-header` đang
bị nhân bản ở 20+ file, không màn nào chắc chắn có nó. Đưa 1 lần vào `assets/scss/v2-styles.scss`
là hết hẳn nhóm lỗi "local đẹp / server xấu" này cho mọi màn.

---

## Phase 39 — Dòng "Người tạo - Ngày tạo": bỏ giờ phút + thêm vào màn tạo mới (2026-09-04)

User: *"trong màn xem chi tiết `DNS Admin - 26/08/2026 21:45` bỏ giờ phút đi, thêm tương tự cho màn
thêm mới nữa"*.

### 39.1 Bỏ giờ phút
- [x] BE `BillAdjustDeptRequestDetailResource` — `created_at` từ `d/m/Y H:i` → **`d/m/Y`**
- [x] Đã soát trước khi đổi: `created_at` của API CHI TIẾT chỉ được FE dùng cho đúng dòng này
      (`createdInfo`); cột "Ngày tạo" của lưới đọc từ `ListResource` nên **không ảnh hưởng**
- [x] `ListResource` **giữ nguyên `d/m/Y H:i`** — cột lưới cần giờ để phân biệt các phiếu lập cùng
      ngày. Đây là chỗ CỐ Ý để 2 Resource khác định dạng nhau, ngược với Phase 28 (khi đó đồng bộ
      `send_approve_date`); ghi rõ vào docblock kẻo người sau "sửa cho đồng bộ"

### 39.2 Thêm dòng này cho màn TẠO MỚI
Phase 19.1 từng bỏ dòng này khỏi màn tạo/sửa với lý do *"lúc tạo phiếu chưa có ngày tạo"*. Nay user
chốt hiện lại.

- [x] `createdInfo` lùi về **người đang đăng nhập + NGÀY HÔM NAY** khi phiếu chưa tồn tại
      (lưu xong chính là ngày này)
- [x] `todayText` tự ghép `dd/mm/yyyy` có số 0 ở đầu — không dùng `toLocaleDateString`, tránh phụ
      thuộc locale của máy
- [x] Gộp badge trạng thái + dòng này vào CÙNG một khối góc phải; badge vẫn chỉ hiện ở màn tạo/sửa
      (`!readonly`), dòng thông tin hiện ở mọi chế độ

### Verify
- [x] `php -l` sạch · parse template + script: 0 lỗi
- [x] Gọi thật API: chi tiết trả `created_by_name = DNS Admin`, `created_at = 24/08/2026`
      (**hết giờ phút**); danh sách vẫn `24/08/2026 13:57`
- [ ] **Mở trình duyệt — user tự xem**

⚠️ Dòng này giờ hiện ở **cả màn SỬA** (cùng component, cùng nhánh điều kiện). Ở đó nó có nghĩa
(phiếu đã có ngày thật) nên tôi để hiện; user muốn bỏ riêng màn sửa thì báo.

---

## Phase 32 — Khoảng trắng đáy trang vẫn dài: chừa chỗ HAI LẦN cho footer (2026-09-04)

User (kèm ảnh màn chi tiết): *"khoảng trắng này vẫn hơi dài"* — dải trắng giữa khối Lịch sử và
thanh nút.

**Gốc — và nó bác luôn kết luận của Phase 25.** `V2Footer` **tự chừa chỗ** cho chính nó bằng class
gắn lên `<body>`:

```scss
body.has-v2-footer { padding-bottom: 66px; }   /* components/V2Footer.vue, style GLOBAL cuối file */
```

Docblock của `V2Footer` còn ghi rõ **KHÔNG dùng khối chừa chỗ đặt tại chỗ**, vì V2Footer hay nằm
giữa trang và phần render SAU nó (đúng là khối Lịch sử) vẫn bị che.

⇒ Mọi `padding-bottom: 70px` khai thêm ở màn đều là **chừa lần thứ hai**: 66 + 70 = **136px** trắng.

- [x] `_id/index.vue` — bỏ `padding-bottom: 70px` ở `container-fluid`
- [x] `BillAdjustDeptRequestForm.vue` — bỏ luôn phần `:style` mà **Phase 25 vừa thêm**.
      Ghi chú Phase 25 nói *"màn tạo/sửa vẫn cần"* là **SAI**: `create.vue` / `_id/edit.vue` bọc
      bằng `container-fluid` trần chính vì đã có `body.has-v2-footer` lo. Màn tạo/sửa cũng đang
      thừa 70px y hệt, chỉ là chưa ai để ý vì cuối form không có khối nào đứng sau footer
- [x] Phase 25 vẫn đúng phần TRIỆU CHỨNG (70px chen giữa card "Chi tiết" và khối Lịch sử) và đã
      hết bằng cách buộc theo `readonly`; nhưng cách sửa đúng là **bỏ hẳn** như trên

### Verify
- [x] Parse template + script 2 file: 0 lỗi
- [x] `grep -rn "padding-bottom: 70px" pages/finance/bill-adjust-dept-requests/` → **RỖNG**
- [ ] **Mở trình duyệt — user tự xem** (còn đúng 66px của `body.has-v2-footer`, bằng mọi màn khác)

⚠️ Đây là bẫy TOÀN HỆ THỐNG, không riêng màn này: màn nào tự khai `padding-bottom` quanh
`V2Footer` đều thừa. Chưa rà các màn khác (ngoài phạm vi user yêu cầu) — nếu muốn dọn đại trà thì
đó là việc riêng, và theo quy tắc team thì sửa dần khi có dịp đụng vào.

---

## Phase 40 — Thêm logo cho file Excel DANH SÁCH (2026-09-04)

User: *"xuất excel tất cả các phiếu đang không có logo à? thêm vào cho tôi"* — đúng, bản danh sách
chưa từng có letterhead (Phase 35 mới chỉ làm cho file 1 phiếu).

- [x] `BillAdjustDeptRequestPrintService` — tách `companyHeaderUrl($companyId)` dùng chung, thêm
      `currentCompanyHeaderUrl()`: bản DANH SÁCH lấy letterhead theo **công ty NGƯỜI ĐANG ĐĂNG NHẬP**
      (danh sách gộp phiếu nhiều công ty nên không thuộc công ty nào — skill print-page mục 4b,
      cùng cách `BorrowExportRequestService::renderPrintList()`)
- [x] `BillAdjustDeptRequestListExport` — thêm `WithDrawings` + trait `EmbedsCompanyLetterhead`
- [x] Controller `exportList()` đổ URL vào qua `withHeader()`

### ⚠️ Bẫy lớn: thêm `WithDrawings` làm TOÀN BỘ bảng tụt xuống 1 dòng
Đo thật (thí nghiệm tách bạch có/không ảnh, cùng bộ dữ liệu):

| | `array()` trả | Sheet thực tế |
| --- | --- | --- |
| Không ảnh | 5 dòng | tiêu đề dòng 1, tên cột dòng 3 |
| **Có ảnh** | 5 dòng | **tiêu đề dòng 2, tên cột dòng 4** |

Hậu quả nếu đếm dòng bằng hằng số: tiêu đề gộp nhầm dòng, định dạng `#,##0` rơi vào **hàng tên cột**
(ô chữ), autofilter lệch, chiều cao dòng nới sai chỗ — **tất cả đều SAI IM LẶNG**, file vẫn tải về
bình thường.

- [x] `WithCustomStartCell('A1')` **KHÔNG chữa được** — đã thử, vẫn tụt
- [x] Cách chốt: `findHeadingRow()` **dò ô `STT` ở cột A** trên chính sheet rồi suy mọi vùng từ đó;
      không tìm thấy thì lùi về 4 chứ không ném lỗi
- [x] **Bỏ dòng trống tự chèn** cho letterhead: khi có ảnh maatwebsite đã tự chừa dòng 1: tự chèn
      thêm là ra HAI dòng trống chồng nhau
- [x] `fitLetterheadRow($sheet)` nới **dòng 1** — ảnh luôn neo A1, không dời theo bảng
      (lần đầu tôi nới nhầm theo `titleRow` nên `cao dòng 1 = -1`, ảnh đè lên tiêu đề)

### Verify
- [x] `php -l` sạch 3 file BE
- [x] Dựng file thật, đọc lại bằng PhpSpreadsheet, đủ **6 tổ hợp**: có/không logo × 0/1/3 dòng —
      bố cục đúng ở mọi tổ hợp, ô tiền luôn `kiểu n` + `fmt=#,##0`
      · không logo: dòng1 = tiêu đề · dòng3 = tên cột
      · có logo: dòng1 = ảnh (cao 58) · dòng2 = tiêu đề · dòng4 = tên cột
- [ ] **Mở bằng Excel — user tự xem**

### 40.1 Logo quá bé — nới theo bề rộng bảng (2026-09-04)

User: *"logo hơi bé, cho rộng ra giúp tôi"*.

Trait `EmbedsCompanyLetterhead` mặc định ép ảnh theo **CHIỀU CAO** (72px) → letterhead vốn rất ngang
(nguồn 2648×236, tỉ lệ ~11,2) chỉ ra **808px**, chưa tới nửa bề rộng bảng. Chính docblock của trait
đã ghi cách xử lý: truyền `$widthPx`.

- [x] Cả 2 export thêm `tableWidthPx()` (7px/ký tự + 5px padding) rồi truyền vào
      `letterheadDrawings($url, 'A1', $this->tableWidthPx())` — khuôn copy
      `BillPaymentRequestExport::tableWidthPx()`, không tự chế công thức

| File | Trước | Sau | Cao dòng 1 |
| --- | --- | --- | --- |
| 1 phiếu (14 cột) | 808×72 | **2002×178** | 134pt |
| Danh sách (12 cột) | 808×72 | **1852×165** | 124pt |

⚠️ **Cần user xác nhận độ lớn**: skill export-excel mục 4b ghi lại **Redmine #11230** — kéo
letterhead bằng cả bảng thì "ảnh cao gấp đôi bản in giấy", và team đã chốt **trần 900px + căn giữa**
cho nhánh xuất file ở FE. Ở đây tôi làm theo yêu cầu "cho rộng ra" + khuôn BE sẵn có (trải hết bảng).
Nếu thấy cao quá thì chốt 1 con số trần (vd 1200px) là chỉnh 1 dòng.

### Verify 40.1
- [x] `php -l` sạch · tải file thật qua HTTP, đọc lại bằng PhpSpreadsheet: kích thước ảnh + chiều cao
      dòng 1 đúng như bảng trên, `drawings = 1` ở cả 2 file

### 40.2 Cột "KH / NCC" tràn chữ — bật wrap text (2026-09-05)

User: *"cột KH/NCC dữ liệu nhiều quá thì cho xuống dòng"*. `object_name` là chuỗi `{mã} - {tên}`
(tên công ty đầy đủ) — cột E rộng 34 ký tự nên chữ tràn sang ô bên phải / bị cắt khi ô kế bên có
dữ liệu.

- [x] `BillAdjustDeptRequestListExport`: thêm hằng `OBJECT_COLUMN = 'E'`, trong `AfterSheet` bật
      `setWrapText(true)` + `setVertical(VERTICAL_TOP)` cho vùng `E{heading+1}:E{lastRow}`
- [x] Giữ nguyên `columnWidths()` (E = 34) và **không** `setRowHeight()` — để Excel tự co giãn chiều
      cao theo số dòng wrap; đặt cứng là mất dòng thứ 2
- [x] Chỉ style **1 cột**, không đụng cả vùng `A:L` (docblock lớp đã cảnh báo: style toàn vùng
      5.000 dòng tốn thêm ~18 giây)

### Verify 40.2
- [x] `php -l` sạch
- [x] Dựng file thật (3 dòng, tên KH 90 ký tự), đọc lại bằng PhpSpreadsheet:
      `E4..E6 wrap=true vert=top`, hàng tiêu đề `E3 wrap=true vert=center` (không đổi),
      cột tiền vẫn `[n] fmt=#,##0`, `width E=34`, `row height=-1` (auto)
- [ ] **Mở bằng Excel — user tự xem**
