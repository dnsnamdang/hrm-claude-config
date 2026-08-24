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
