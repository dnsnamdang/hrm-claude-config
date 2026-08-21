# Plan — Phiếu ủy nhiệm chi (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo, code thẳng — không tách nhánh)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-20-finance-bill-payment-authorization-design.md`
> Tóm tắt: `.plans/gop-db/finance-bill-payment-authorization/design.md`

**6 ruling đã chốt (U-UNC-1…6) — đọc §8 của spec trước khi "sửa lỗi" bất cứ điểm nào.**

---

## Phase 0 — Khảo sát & chốt (XONG)

- [x] 0.1 Đọc màn ERP: controller (254 dòng) · model (635) · detail model · 9 blade (2.101 dòng) · routes
- [x] 0.2 Đo dữ liệu thật: 2.574 phiếu · 5.267 dòng · 100% status 3 · loại 1/2/6/12 · 0 phiếu loại 4
- [x] 0.3 Đo lỗi ghi sổ ERP: 433/433 phiếu nhiều dòng lệch, thiếu 111.371.119.571 đ
- [x] 0.4 Chốt 9 quyết định với user (§1 spec) + 6 ruling (§8 spec)
- [x] 0.5 Viết spec chi tiết + design tóm tắt + plan này

## Phase 1 — Nền BE: Entity + quyền

- [x] 1.1 `SHOW CREATE TABLE` 3 bảng, chốt danh sách cột ghi được (ERP khai `$fillable` thừa)
- [x] 1.2 `Entities/BillPaymentAuthorization/BillPaymentAuthorization.php` — hằng trạng thái + màu,
      `TYPES_FROM_REQUEST`, `TYPE_PAYMENT_EMPLOYEE`, 4 hằng quyền, quan hệ, hook `creating`
- [x] 1.3 `BillPaymentAuthorizationDetail.php` + `...DetailProductExportRequest.php`
- [x] 1.4 trait `BillPaymentAuthorizationAccess.php` — `canView` / `canEdit` / `canDelete`
      (chỉ status 1 + quyền `Kế toán thanh toán`); KHÔNG có `canApprove` / `canCancel` (ruling U-UNC-6)
- [x] 1.5 `generateCode()` prefix `{CTY}.UNC{mm}{yy}.` + `lockForUpdate()`
- [x] 1.6 Thêm 2 quyền api id 1515/1516 vào `PermissionsTableSeeder` (group `Phiếu ủy nhiệm chi`, type 8)
- [x] 1.7 Chạy seeder trên DB local, verify 2 quyền vào đúng, không đụng quyền cũ

## Phase 2 — BE đọc

- [x] 2.1 `BillPaymentAuthorizationService::searchByFilter()` — phạm vi theo 3 nhánh quyền +
      luật "phiếu nháp chỉ người lập thấy"; 6 ô lọc + khoảng thời gian + khối tổ chức
- [x] 2.2 `getDetail()` — port `getDataForEdit()` (eager load đề nghị, ngân hàng NCC, hợp đồng,
      phiếu xuất hàng, phân bổ)
- [x] 2.3 `searchAvailableRequests()` — lọc `status = 6` + `type_payment = 2`.
      **KHÔNG** `whereNotExists` (ruling U-UNC-2)
- [x] 2.4 Transformers: `ListResource` (9 cột + 4 cột ẩn + 2 cờ `is_can_edit`/`is_can_delete`) ·
      `DetailResource` · `DetailRowResource`
- [x] 2.5 Endpoint tra cứu: `accounts` · `company-accounts` (account_from + bank_from, chỉ status 1) ·
      `payment-employees` (tái dùng `PaymentEmployeeLookupService`)

## Phase 3 — BE ghi

- [x] 3.1 `StoreRequest` / `UpdateRequest` — port đủ 5 nhóm luật §4.5, giữ `after_or_equal:today`
      cho cả 2 (ruling U-UNC-3); thêm `type` `required|in`
- [x] 3.2 `WriteService::create()` / `update()` — `syncDetails()` (xóa sạch rồi ghi lại như ERP) +
      bảng phân bổ phiếu xuất hàng
- [x] 3.3 `syncPaymentMoneyApprove()` — đẩy số tiền duyệt về `bill_payment_request_details`
- [x] 3.4 `updateStatus()` — `approved_id` + đề nghị 6 → 8 (đọc `bill_payment_request_id` từ
      **bản ghi**, không đọc payload)
- [x] 3.5 `destroy()` — chỉ status 1, không trả trạng thái đề nghị (đúng ERP)

## Phase 4 — BE ghi sổ cái

- [x] 4.1 `BillPaymentAuthorizationAccountingService` nhánh A — 4 nhánh con:
      phiếu xuất hàng · loại 6 (`work` TTHHD) · loại 12 (chuyến giao hàng) · thường
- [x] 4.2 Bút toán Có + `AccountDetailRef`. **GIỮ `=` không đổi thành `+=`** (ruling U-UNC-1),
      kèm docblock trỏ ruling
- [x] 4.3 Nhánh B (loại 4): tái dùng `PaymentEmployeeAccountingService`, đổi `invoiceable_type`
- [x] 4.4 `invoiceable_type` ghi **tên class ERP đầy đủ**; bổ sung morphMap nếu thiếu cặp nào

### Kết quả verify sổ cái (Phase 4) — 2026-08-20

Replay **63 phiếu cũ** (loại 1 · 2 · 6 · 12, mỗi loại 12 phiếu + 15 phiếu nhiều dòng) qua
`collectAccountingInput()` + `buildEntries()`, diff **31 trường** của `account_details` và số dòng
`account_detail_refs` với sổ cái ERP đang có:

| Kết quả | Số phiếu |
| --- | --- |
| Khớp tuyệt đối từng trường | **62 / 63** |
| Lệch | 1 (phiếu #452, cột `part_id`) |

Phiếu #452 **KHÔNG phải lỗi code** — trôi dữ liệu: nhân viên 116 (người tạo hợp đồng) có
`part_id` NULL tới 2026-05-11 rồi mới thành 28. Bằng chứng: 2.100 dòng sổ cái `created_by = 116`
ghi trong khoảng 2025-08-04 → 2026-05-11 đều `part_id` NULL, 677 dòng ghi 2026-05-18 → 2026-07-27
đều `part_id = 28`. Bút toán của #452 ghi ngày 2025-10-13.

Điểm được xác nhận qua replay: bút toán Có = tiền **dòng cuối** (RULING U-UNC-1) · `created_by` là
người TẠO HỢP ĐỒNG chứ không phải người lập phiếu · `work_id = TTHHD` + `account_from_number` ở
loại 6 · `account_id` lấy tài khoản nợ CỦA PHIẾU ở loại 1/2/12 · số ref khớp từng phiếu.

## Phase 5 — Controller + route

- [x] 5.1 `BillPaymentAuthorizationController` — 8 endpoint (không submit/approve/cancel/print/export)
- [x] 5.2 Khai route, 4 route tĩnh TRƯỚC `/{id}`, gắn `checkPermission:Kế toán thanh toán` cho
      store/update/destroy
- [x] 5.3 `php -l` toàn bộ file mới + smoke test 8 endpoint bằng HTTP

## Phase 6 — FE danh sách

- [x] 6.1 `pages/finance/bill-payment-authorizations/index.vue` — khuôn Danh mục khách hàng,
      đủ 4 mixin, `columnScreenKey = finance_bill_payment_authorizations`
- [x] 6.2 `V2BaseSmartFilterPanel` + schema `filterFields` (7 ô + khối tổ chức),
      loại chi **ẩn loại 4** đúng ERP
- [x] 6.3 Cột theo bảng §5.2, 4 cột mới ẩn mặc định, sort mặc định `created_at` giảm dần
- [x] 6.4 Cột Hành động qua `V2BaseRowActions` — `switch (action)` trên **chuỗi**, không so `action.key`
- [x] 6.5 Gắn `link` cho mục menu "Phiếu ủy nhiệm chi" đã có sẵn trong `finance.js`

## Phase 7 — FE form + chi tiết

- [x] 7.1 `PaymentRequestSearchModal.vue` (bản UNC — lọc CK)
- [x] 7.2 `BillPaymentAuthorizationForm.vue` — khối chung + **5 trường riêng UNC** + khối ngân hàng
      người nhận + bảng chi tiết theo loại
- [x] 7.3 Nhánh loại 4: nút "Lấy nhân viên" + tái dùng `PaymentEmployeeTable.vue` của Phiếu chi
- [x] 7.4 2 nút **Lưu** / **Lưu và duyệt** trong `V2Footer` + kiểm tra tổng tiền trước khi duyệt
- [x] 7.5 `create.vue` · `_id/edit.vue` · `_id/index.vue` (chi tiết, không Duyệt/Hủy/In/Excel)
- [x] 7.6 `unsavedChangesMixin` + `markFormSaved()` · validate inline · `V2BaseSelectInModal`

## Phase 8 — Đối chiếu ngược ERP + verify

- [ ] 8.1 Đối chiếu 9/9 cột · 6/6 ô lọc · 2/2 hành động + điều kiện ẩn/hiện · toàn bộ trường form
- [x] 8.2 Chạy checklist skill `erp-to-hrm-screen` mục A-H + 6 lệnh grep tự kiểm
- [ ] 8.3 Baseline DB 5 bảng trước/sau; dựng phiếu thử mỗi loại (1 · 2 · 6 · 12 · 4), duyệt,
      diff từng trường sổ cái với phiếu ERP cùng loại
- [ ] 8.4 Test riêng **phiếu nhiều dòng**: khẳng định bút toán Có = tiền **dòng cuối** (đúng ERP)
- [ ] 8.5 Dọn phiếu thử, đối chiếu 0 lệch
- [x] 8.6 Compile 8/8 file Vue + `php -l` sạch
- [ ] 8.7 Bàn giao user bấm thật trên trình duyệt

---

## Phase 9 — Phát sinh trong lúc làm (ngoài plan gốc)

- [x] 9.1 Bỏ `middleware('checkPermission:...')` khỏi route (spec §4.3 bản nháp ghi SAI): trên DB
      gộp middleware chung resolve quyền qua spatie nên bỏ sót role gán từ thời ERP -> người có
      quyền thật vẫn 403. Gate bằng `applyScope()` + `canView/canEdit/canDelete` +
      `BillPaymentRequest::isAccountant()`, đúng quy ước 3 màn Finance đi trước.
- [x] 9.2 Sửa lại tài liệu: đề nghị nhảy **6 → 8** (không phải 6 → 9 như bản nháp) — đối chiếu hằng
      `BillPaymentRequest::STATUS_APPROVED_BILL_PAYMENT = 8` + 2.574/2.574 phiếu thật.
- [x] 9.3 `withSum()` cho 2 cột tổng tiền: bảng UNC KHÔNG có `sum_payment_money_approve_exchange`
      như `bill_payments` -> sort/hiện cột tiền phải qua alias subquery.
- [x] 9.4 Viết service ghi sổ RIÊNG cho cả 2 nhánh thay vì tái dùng của Phiếu chi — 2 hàm ERP khác
      nhau 6 điểm (nhánh A) và 5 điểm (nhánh B), gộp bằng cờ điều kiện sẽ hỏng cả 2 màn.
- [x] 9.6 Thêm prop `excludeFields` cho component DÙNG CHUNG
      `pages/finance/bill-payments/components/PaymentEmployeeTable.vue` (mặc định `[]` — màn Phiếu
      chi KHÔNG đổi hành vi). Lý do: ERP bản UNC chỉ ghi sổ **5 khoản**, không có "Chi phí khác"
      (mã vụ việc `CPK`); để nguyên 6 cột thì người dùng nhập được khoản đó mà tiền KHÔNG BAO GIỜ
      vào sổ cái — mất tiền im lặng. Màn UNC truyền `:exclude-fields="['other_cost']"`.
      ⚠️ Là SỬA FILE DÙNG CHUNG của feature đã nghiệm thu — cần user xác nhận.
- [ ] 9.5 **CHỜ USER XÁC NHẬN**: ERP `update()` thiếu loại 12 trong danh sách ghi sổ (`[1,2,3,6]`)
      so với `store()` (`[1,2,3,6,12]`) -> phiếu loại 12 lưu nháp rồi mở lại bấm "Lưu và duyệt" sẽ
      lên "Đã hạch toán" mà KHÔNG sinh bút toán nào. HRM đang dùng CÙNG một danh sách cho cả 2
      đường. Xem docblock `BillPaymentAuthorizationWriteService::update()`.

## Phase 10 — Test Playwright toàn luồng (2026-08-20)

Test bằng phiên trình duyệt thật, tài khoản **Trần Thị Phương (id 429)** — có `Kế toán thanh toán`
+ `Xem tất cả phiếu ủy nhiệm chi của công ty`, công ty 4, phòng 80. Phạm vi của user này là
**2/2.574 phiếu**, rất tiện để kiểm luật lọc theo quyền.

### 🐛 4 LỖI CHỈ TRÌNH DUYỆT MỚI LỘ — đã sửa

- [x] 10.1 **Ngày hạch toán không lưu được (chặn hoàn toàn màn)**. FE gửi `dd/mm/yyyy`, luật `date`
      của Laravel đọc chuỗi có dấu `/` theo kiểu **m/d/Y**:
      `20/08/2026` -> "tháng 20" -> 422 *"Không hợp lệ"*; `05/09/2026` (5 tháng 9) -> hiểu thành
      9 tháng 5 -> báo sai *"nhỏ hơn ngày hôm nay"*. ⇒ **màn không lưu được từ ngày 13 hàng tháng**.
      `WriteService` CÓ đổi `d/m/Y` -> `Y-m-d` nhưng chạy SAU validate nên không cứu được.
      **Sửa 2 lớp**: FE `value-type="YYYY-MM-DD"` (hiển thị vẫn dd/mm/yyyy) + `toIsoDate()` khi nạp
      phiếu cũ; BE thêm `prepareForValidation()` nhận cả 2 định dạng.
- [x] 10.2 **Chọn phiếu đề nghị xong bị 403, luồng đứt**. Form gọi
      `GET /bill-payment-requests/{id}` — endpoint đó gate bằng `canView()` của MÀN Đề nghị thanh
      toán, trong khi popup CỐ Ý không áp phạm vi xem. Kế toán công ty 4 chọn được phiếu của công ty
      1 rồi nhận 403. ERP không dính vì route `getData` **không gắn middleware nào**.
      **Sửa**: thêm endpoint riêng `GET /bill-payment-authorizations/payment-requests/{id}`, gate
      bằng `isAccountant()` — cùng quyền với popup và `store()`.
      ⚠️ **Màn Phiếu chi đã nghiệm thu có CÙNG lỗi này** (dùng chung endpoint) — chưa sửa, xem §Còn lại.
- [x] 10.3 **Lưu nháp trả 500** `Column 'receiver' cannot be null`. Nhánh A của UNC cố ý không có ô
      "Người nhận" / "Phòng ban chi" (đúng ERP) -> FE gửi rỗng -> middleware
      `ConvertEmptyStringsToNull` của Laravel đổi '' -> null -> 5 cột `NOT NULL` không default nổ.
      **Sửa**: `billAttributesFromClient()` ép mặc định theo ĐÚNG dữ liệu thật của 2.574 phiếu ERP
      (`receiver=''` 100%, `payment_department_id=0` 100%, `type_money_id=1`, `exchange_rate=1`).
- [x] 10.4 **Nhánh loại 4 thừa 1 cột tiền** — `PaymentEmployeeTable` dùng chung có 6 khoản, ERP bản
      UNC chỉ ghi sổ **5** (không có "Chi phí khác"/`CPK`). Người dùng nhập được khoản đó mà tiền
      KHÔNG BAO GIỜ vào sổ cái. **Sửa**: thêm prop `excludeFields` (mặc định `[]` — màn Phiếu chi
      không đổi hành vi), màn UNC truyền `['other_cost']`.

### ✅ Đã bấm thật và đạt

| # | Kịch bản | Kết quả |
| --- | --- | --- |
| 1 | Phạm vi theo quyền | **2/2.574** phiếu, khớp chính xác SQL |
| 2 | 16 kịch bản lọc (loại chi · trạng thái · người lập · người đề nghị · công ty · phòng ban · bộ phận · mã phiếu · mã đề nghị · khoảng ngày) | **16/16 khớp DB**, param gửi đúng tên |
| 3 | Ô "Loại chi" | đúng 5 option 1·2·6·10·12, **không có loại 4** (đúng ERP) |
| 4 | Cấu hình cột | 13 cột · STT/Mã/Hành động khóa · 4 cột mới ẩn mặc định · lưu qua reload |
| 5 | Sort cột tiền (alias `withSum`) | đổi thứ tự đúng, param `details_sum_payment_money_approve_exchange` |
| 6 | Ô gõ tay | KHÔNG tự gọi API, chờ nút Tìm kiếm — đúng skill list-page |
| 7 | Nút Làm mới | xóa hết điều kiện + tải lại |
| 8 | Bảng trống | hiện "Không có dữ liệu phù hợp bộ lọc." |
| 9 | Màn chi tiết | 22 trường đúng DB, đủ 5 trường riêng UNC + khối TK người nhận + bảng chi tiết + Tổng cộng |
| 10 | Cờ quyền fail-closed | phiếu đã hạch toán: footer chỉ "Quay lại", cột Hành động rỗng |
| 11 | Validate form trống | 6 lỗi inline + 6 ô viền đỏ, không gọi API lưu |
| 12 | Khối chuyển tiền | chọn ngân hàng -> tự điền tên + lọc 32 TK còn **9 TK của MB**, không tự chọn vì >1 (đúng ERP); chọn TK -> tự điền tên + số TK |
| 13 | Kéo phiếu đề nghị | 3 dòng chi tiết + tiền khớp DB, TK nợ tự điền 99, TK có 6 |
| 14 | Kẹp số tiền | gõ 999.999.999 -> tự về 442.800 (số đề nghị), quy đổi VND tính lại |
| 15 | **Lưu nháp** | mã `TPSG.UNC0826.00001` (prefix công ty đúng) · `receiver=''` · `payment_department_id=0` · org 4/80 từ người lập · **0 bút toán** · đề nghị **vẫn status 6** |
| 16 | Màn Sửa nạp lại | ngày hạch toán đúng cả 2 chiều (form ISO / ô `20/08/2026`), đủ 5 trường riêng, 3 dòng chi tiết |
| 17 | **Lưu và duyệt** | popup xác nhận -> 3 bút toán Nợ 3311 + **1 bút toán Có 1121 = 1.677.240 (đúng bằng DÒNG CUỐI, không phải tổng 4.558.680)** ⇒ **RULING U-UNC-1 tái lập chính xác** |
| 18 | Cột denormalize sổ cái | `created_by` = **590** (người TẠO HỢP ĐỒNG) ở 3 dòng Nợ nhưng **429** (người lập) ở dòng Có · `supplier_id=customer_id=11842` soi gương · ref Nợ→1121, Có→3311 · `invoice_type=1` |
| 19 | Đồng bộ ngược | đề nghị **6 → 8** + 3 dòng ghi `payment_money_approve` |
| 20 | Sinh mã tuần tự | `00001` -> `00002` |
| 21 | **Xóa phiếu nháp** | popup xác nhận đúng câu; xóa sạch **cả 3 tầng**, 0 dòng mồ côi (ERP để lại mồ côi) |
| 22 | Nháp bị xóa | đề nghị nguồn **vẫn status 6**, `payment_money_approve` vẫn NULL — không để lại dấu vết |
| 23 | Guard URL `/edit` phiếu đã hạch toán | tự đá về màn chi tiết |
| 24 | Cảnh báo "chưa lưu" | chưa sửa -> KHÔNG hỏi; sửa rồi -> popup "Thông tin chưa lưu" (Thoát / Ở lại) |
| 25 | Console | **0 lỗi** ở mọi màn (2 warning là của vue-router, có sẵn toàn dự án) |

### 🧹 Dọn dẹp — 8/8 chỉ số về đúng baseline

| Bảng | Trước | Sau |
| --- | --- | --- |
| `bill_payment_authorizations` | 2.574 | 2.574 ✓ |
| `bill_payment_authorization_details` | 5.267 | 5.267 ✓ |
| `..._detail_product_export_requests` | 0 | 0 ✓ |
| `account_details` | 972.025 | 972.025 ✓ |
| `account_detail_refs` | 1.024.994 | 1.024.994 ✓ |
| `MAX(id)` phiếu / sổ cái | 2590 / 1.001.483 | 2590 / 1.001.483 ✓ |
| Đề nghị 4153 · 4167 | status 6 | status 6 ✓ |
| Cấu hình cột user 429 | chưa có | đã xoá ✓ |

### ⚡ Hiệu năng (đo riêng phía server, tách khỏi nhiễu `artisan serve`)

| Truy vấn | Median |
| --- | --- |
| UNC danh sách (2 × `withSum`) | 161 ms |
| Phiếu chi danh sách (màn cũ, có cột tổng sẵn) | 108 ms |
| UNC chi tiết 1 phiếu | 105 ms |
| UNC popup đề nghị khả dụng | 163 ms |

Chênh 53 ms so với màn Phiếu chi là giá của 2 subquery `withSum` — chấp nhận được.
⚠️ Trên trình duyệt mỗi request mất 3–8 s và form mất ~20 s mới nạp xong, **do `php artisan serve`
chạy ĐƠN LUỒNG** (màn Phiếu chi cũ cũng 5,9 s, danh mục tiền tệ 5,4 s) — không phải lỗi của màn này.


## Phase 11 — Sửa lỗi lan sang 2 màn anh em (user chốt 2026-08-20: "có lỗi gì sửa luôn")

Rà 3 lớp lỗi của Phase 10 ra toàn phân hệ Tài chính:

| Lỗi | Phiếu chi | Phiếu thu | Kết luận |
| --- | --- | --- | --- |
| 10.1 ngày `dd/mm/yyyy` | không dính (form không có ô ngày) | không dính | grep toàn dự án: **0 chỗ** còn `value-type="DD/MM/YYYY"` |
| 10.2 **403 khi kéo đề nghị** | **DÍNH** | **DÍNH** | đã sửa cả 2 |
| 10.3 cột `NOT NULL` | không dính | không dính | `receiver` / `payer` đều `required` ở FormRequest ⇒ chuỗi rỗng bị chặn ở 422, không chạm DB |
| 10.4 cột tiền thừa | không áp dụng | không áp dụng | Phiếu chi dùng đủ 6 khoản là ĐÚNG |

- [x] 11.1 Đo mức nghiêm trọng trước khi sửa (tài khoản `Kế toán thanh toán` công ty 4):
      · Phiếu chi — popup trả **95 phiếu**, **3/3 phiếu thử đầu đều 403**
      · Phiếu thu — popup trả **33 phiếu**, **3/3 phiếu thử đầu đều 403**
      ⇒ với tài khoản này **2 màn đó thực tế KHÔNG lập được phiếu**.
- [x] 11.2 `BillPaymentController::paymentRequestDetail()` + route
      `GET /finance/bill-payments/payment-requests/{id}`, gate `isAccountant()`
- [x] 11.3 `BillIncomeController::incomeRequestDetail()` + route
      `GET /finance/bill-incomes/income-requests/{id}`, gate `isAccountant()`
- [x] 11.4 `BillPaymentForm.vue` + `BillIncomeForm.vue` trỏ sang endpoint mới; gỡ hằng
      `REQUEST_API_BASE` không còn dùng ở `BillIncomeForm`
- [x] 11.5 Verify bằng phiên trình duyệt thật: **3/3 phiếu chi + 3/3 phiếu thu + 3/3 UNC → 200 kèm
      đủ dữ liệu**, endpoint CŨ vẫn 403 (phạm vi xem của 2 màn Đề nghị **giữ nguyên**, không đụng).
      Kéo dữ liệu qua form thật ở cả `bill-payments/create` và `bill-incomes/create`: **0 lỗi console**.
- [x] 11.6 Hồi quy: 7/7 endpoint danh sách + popup của 5 màn Tài chính trả 200; 8/8 endpoint UNC
      giữ nguyên kết quả; `php -l` sạch; compile 3/3 file Vue.

⚠️ **Không đụng `show()` của 2 màn Đề nghị** — phạm vi xem của chúng là nghiệp vụ riêng, giữ nguyên.
Endpoint mới chỉ phục vụ luồng LẬP PHIẾU và gate bằng đúng quyền `Kế toán thanh toán`.


---

## Còn lại

- [ ] 8.1 Đối chiếu ngược từng dòng với giao diện ERP thật (cần mở 2 cổng song song)
- [ ] 8.3 / 8.4 / 8.5 Dựng phiếu thử loại 6 · 12 · 4 rồi diff sổ cái (đã phủ loại 1/2 qua replay +
      luồng ghi end-to-end; loại 4 KHÔNG có dữ liệu ERP để đối chiếu)
- [x] 8.7 ~~User bấm thật trên trình duyệt~~ → đã tự test Playwright toàn luồng, xem Phase 10
- [ ] 8.7b User nghiệm thu lại trên cổng dev
- [x] 10.5 ~~Báo màn Phiếu chi dính cùng lỗi 10.2~~ → user chốt sửa luôn, xem Phase 11
      (hoá ra **cả Phiếu thu cũng dính**)
- [ ] SRS / testcase / HDSD

---

## Checkpoint

### Checkpoint — 2026-08-20 11:40
Vừa hoàn thành: Phase 0 (khảo sát + đo dữ liệu + chốt 9 quyết định/6 ruling + spec + plan)
Đang làm dở: chưa động code
Bước tiếp theo: Phase 1.1 — `SHOW CREATE TABLE` 3 bảng rồi dựng Entity
Blocked:

### Checkpoint — 2026-08-20 (cuối phiên)
Vừa hoàn thành: **Phase 1-7 xong code** (BE 11 file mới + 3 sửa · FE 6 file mới + 1 sửa menu).
  · BE: Entity + trait quyền + 2 detail model · 4 service (đọc / ghi / sổ cái nhánh A / sổ cái
    nhánh B) · 2 FormRequest · 2 Resource · Controller 8 endpoint · 8 route · 2 quyền api 1515-1516.
  · FE: `pages/finance/bill-payment-authorizations/` (index · create · _id/index · _id/edit ·
    form dùng chung · popup chọn đề nghị) + gắn link mục menu đã có sẵn.
Verify đã chạy:
  · `php -l` sạch 12/12 file BE · compile template + script 6/6 file Vue · 5/5 lệnh grep tự kiểm sạch
  · **Replay sổ cái 63 phiếu cũ: 62/63 khớp tuyệt đối 31 trường** (1 phiếu lệch do trôi dữ liệu
    nhân viên, đã truy ra bằng chứng — xem mục Phase 4)
  · 8/8 endpoint GET trả 200 đúng số liệu (2.574 phiếu · lọc loại 6 ra 37 · popup 80 đề nghị khớp SQL)
  · Luồng ghi end-to-end trong transaction rồi rollback: sinh mã `TPE.UNC0826.00001` · 2 bút toán ·
    đề nghị 6 → 8 · sync số duyệt chi · **4 bảng về đúng số dòng cũ sau rollback**
  · Validate: thiếu trường → 422 đủ 10 khóa · lùi ngày hạch toán → 422 đúng câu · loại chi lạ → 422 ·
    xóa phiếu đã hạch toán → 423
Đang làm dở: không
Bước tiếp theo: user bấm thật trên trình duyệt (Phase 8.7) + xác nhận điểm 9.5
Blocked: không
