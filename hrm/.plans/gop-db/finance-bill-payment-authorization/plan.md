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

## Phase 9 — Mặc định loại chi + lưu nháp chỉ bắt Loại chi (2026-08-27)

Yêu cầu user: màn `/finance/bill-payment-authorizations/create` vừa vào phải có sẵn Loại chi
"Chi trả nhà cung cấp" (id 1); ô đó KHÔNG cho xóa trắng, chỉ cho đổi sang loại khác; bấm
**Lưu nháp** thì chỉ bắt buộc mỗi trường Loại chi. (Cùng cách đã làm ở màn Phiếu chi 2026-08-24,
xem `.plans/gop-db/finance-bill-payment/plan.md`.)

3 lớp phải gỡ mới lưu nháp trống được — thiếu 1 lớp là vẫn 422/500:

| # | Lớp chặn | Triệu chứng nếu bỏ quên | Cách xử lý |
| --- | --- | --- | --- |
| 1 | `validateForm()` của vee-validate ở FE (`receiver` required ở nhánh loại 4) | Bấm Lưu nháp không gọi API, toast "Vui lòng kiểm tra lại dữ liệu nhập" | Chỉ chạy `validateForm()` khi bấm "Lưu và duyệt" |
| 2 | `BillPaymentAuthorizationStoreRequest::rules()` — 6 luật `required` luôn áp + 3 nhánh theo loại chi | 422 hàng loạt khi form còn trống | `required` → `nullable` khi lưu nháp, GIỮ luật định dạng (`exists`/`date`/`numeric`); riêng `type` vẫn `required` |
| 3 | Cột `bill_payment_authorizations.account_has` **NOT NULL không default** | 500 `Column 'account_has' cannot be null` | `billAttributesFromClient()` ghi `0` khi lưu nháp (giống `bill_payments`) |

Kèm 2 việc bắt buộc đi cùng số 0 đó (giống màn Phiếu chi, thiếu là đẻ bug mới):
- `prepareForValidation()` đưa `0`/`''` về `null` TRƯỚC validate — nếu không, mở lại phiếu nháp rồi
  Lưu nháp lần nữa sẽ dính `exists:accounts,id` với đúng số 0 ("Không tồn tại").
- `BillPaymentAuthorizationDetailResource` trả `null` thay cho `0` để select ở FE hiện placeholder.

🔶 **Nới RULING U-UNC-3 cho đường lưu nháp**: `date_accounting` bỏ `required|after_or_equal:today`
khi lưu nháp (chỉ còn `date`). Lý do: nháp chưa ghi sổ cái nên ngày chưa có ý nghĩa kế toán, mà giữ
luật thì phiếu nháp để qua đêm mở ra bấm Lưu nháp là 422. Đường **"Lưu và duyệt" giữ nguyên đủ luật**
— đúng tinh thần ruling (không cho *hạch toán* lùi ngày).

- [x] **BE-9.1** `BillPaymentAuthorizationStoreRequest`: thêm `savingAsDraft()` (status !== 3),
      `required` → `nullable` khi nháp (trừ `type`), mở rộng `prepareForValidation()` chuẩn hoá 0/''.
- [x] **BE-9.2** `BillPaymentAuthorizationWriteService::billAttributesFromClient()`: `account_has ?? 0`.
- [x] **BE-9.3** `BillPaymentAuthorizationDetailResource`: `account_has = 0` → trả `null`.
- [x] **FE-9.4** Ô Loại chi: `:allow-clear="false"` (bỏ nút × của select2).
- [x] **FE-9.5** Màn Tạo (không kèm `?bill_payment_request_id=`): mặc định `form.type = 1`
      (Chi trả nhà cung cấp), đặt TRƯỚC `markFormPristine()`.
- [x] **FE-9.6** `save(approve)`: chỉ chạy `validateForm()` khi `approve === true`.

**Verify Phase 9 (HTTP kernel + JWT super admin, transaction rồi rollback — 2.574 phiếu và 972.038
bút toán về đúng số cũ sau rollback):**

| Luồng | Kết quả |
| --- | --- |
| Lưu nháp **chỉ có loại chi** (loại 1) | **200**, sinh mã `TPE.UNC0826.00001`, DB `account_has = 0` · `receiver = ''` · `date_accounting = NULL` |
| Mở lại phiếu nháp đó | 200, resource trả `account_has = null` (không phải 0) |
| Lưu nháp **lần 2** trên chính phiếu đó | **200** |
| Lưu nháp với ngày hạch toán **lùi 5 ngày** | **200** (RULING U-UNC-3 đã nới cho nháp) |
| Lưu nháp **thiếu loại chi** | **422** — đúng 1 khóa `type`: "Bắt buộc chọn loại chi" |
| Lưu nháp loại chi rác (99) | **422** — `type`: "Loại chi không hợp lệ" |
| Lưu nháp đủ 5 loại còn lại (2 · 4 · 6 · 10 · 12) | **200** cả 5 |
| Lưu nháp loại 6 + 1 dòng chi tiết chưa chọn TK nợ | **200** |
| **Lưu và duyệt** form trống | **422** đủ 10 khóa như trước (`account_has` · `account_from` · `bank_from` · `bank_from_name` · `date_accounting` · `account_dept` · `bill_payment_request_id` · `source_money` · `details` · `exchange_rate`) |
| **Lưu và duyệt** ngày lùi | **422** "Ngày hạch toán không được nhỏ hơn ngày hôm nay" — ruling giữ nguyên ở đường duyệt |
| **Lưu và duyệt** payload đủ (đề nghị `TEST.DNTT-CHI.04`, loại 12) | **200** · phiếu `status = 3` · sinh **2 bút toán** · đề nghị chuyển trạng thái 6 → 8 — KHÔNG hồi quy |

### Checkpoint — 2026-08-27
Vừa hoàn thành: Phase 9 — mặc định loại chi "Chi trả nhà cung cấp" + ô Loại chi không cho xóa
trắng + lưu nháp chỉ bắt buộc Loại chi (gỡ đủ 3 lớp chặn: vee-validate FE → FormRequest →
cột `account_has` NOT NULL).
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payment-authorizations/create` xác nhận Loại chi chọn sẵn,
bấm × không xóa được, và bấm Lưu nháp với form trống.
Chưa kiểm chứng bằng mắt: FE chỉ compile (vue-template-compiler + babel), chưa mở trình duyệt;
11 luồng BE đã gọi thật.
Blocked: không.

### Kẹp trần ô "Số tiền duyệt chi" (2026-08-27)

- [x] **FE** `pages/finance/bill-payment-authorizations/components/BillPaymentAuthorizationForm.vue` — ô "Số tiền duyệt chi" khai `:max="Number(detail.payment_money_request || 0)"`.
      Lý do: bản cũ chỉ kẹp ở handler `@input` của màn (`clampApprove()`), mà ô được điền sẵn ĐÚNG
      BẰNG số đề nghị chi → kẹp về đúng giá trị đang giữ → Vue coi là "không đổi" → ô vẫn HIỆN số to
      vừa gõ tới khi rời ô. Nay `V2BaseCurrencyInput` có prop `max` kẹp ngay trong `onInput()`.
      Chi tiết + 9 ca test: `.plans/gop-db/finance-bill-income/plan.md` mục "ô vẫn hiện số to hơn trần".
      `clampApprove()` giữ nguyên làm lớp phòng thủ cho giá trị đặt bằng code.

### Bỏ "Chờ duyệt" / "Hủy" khỏi ô lọc Trạng thái (2026-08-27)

Người dùng báo: ô lọc Trạng thái đang có 4 lựa chọn, nhưng chọn "Chờ duyệt" hoặc "Hủy" luôn ra 0 dòng.

**Điều tra (không đoán):**
- Docblock `BillPaymentAuthorization` đã ghi sẵn: status 2 và 4 là TRẠNG THÁI CHẾT — bên ERP khối
  gửi duyệt (`BillPaymentAuthorizationController::update()` :178-181) và khối hủy (:202-205) đều bị
  comment; UNC chỉ có 2 đường ra là "Lưu" (status 1) và "Lưu và duyệt" (status 3) — RULING U-UNC-6.
- Đếm dữ liệu thật ngày 2026-08-27:
  `SELECT status, COUNT(*) FROM bill_payment_authorizations GROUP BY status;`
  → **status 1 = 1 phiếu · status 3 = 2.574 phiếu · KHÔNG có dòng nào status 2 hoặc 4.**

- [x] **BE-1** `Entities/BillPaymentAuthorization/BillPaymentAuthorization.php` — thêm hằng
      `STATUSES_FOR_FILTER = [1, 3]` kèm docblock giải thích. **GIỮ NGUYÊN `STATUSES` đủ 4 mục** vì
      còn dùng đổ chữ + màu badge ở `*ListResource` / `*DetailResource` — bỏ đi thì phiếu cũ mang
      status 2/4 (nếu có) sẽ hiện "—".
- [x] **BE-2** `Services/BillPaymentAuthorizationService.php` — `meta()` đổi
      `'statuses' => BillPaymentAuthorization::STATUSES` thành `$this->statusesForFilter()`, lọc theo
      hằng trên. Cùng khuôn với `typesForFilter()` đã có sẵn (cố ý bỏ loại 4).
- [x] **FE-1** `pages/finance/bill-payment-authorizations/index.vue` — bổ sung docblock cảnh báo ô
      Trạng thái chỉ còn 2 lựa chọn và `statusOptions` LUÔN lấy từ `response.statuses`.
      **KHÔNG sửa logic FE**: màn vốn đã đọc options từ BE, không hard-code danh sách.

**Verify (HTTP kernel + JWT super admin, employee_id 13):**

| Kiểm tra | Kết quả |
| --- | --- |
| `php -l` 2 file BE | No syntax errors |
| `GET /api/v1/finance/bill-payment-authorizations` | **200** |
| Khoá `statuses` trong response | `[{"id":1,"name":"Đang tạo"},{"id":3,"name":"Đã hạch toán"}]` — đúng 2 mục |

### Checkpoint — 2026-08-27
Vừa hoàn thành: gỡ 2 trạng thái chết "Chờ duyệt" / "Hủy" khỏi dropdown lọc Trạng thái (lọc ở BE
`meta()`, FE không đổi logic).
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payment-authorizations`, bấm ô Trạng thái xác nhận chỉ còn
"Đang tạo" và "Đã hạch toán".
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt; endpoint BE đã gọi thật và trả đúng 2 mục.
Blocked: không.

### Nút "Tạo ủy nhiệm chi" ở màn Đề nghị thanh toán (2026-08-27)

**Logic ERP (nguồn: `resources/views/income_expenditure/bill_payment_requests/show.blade.php:20-31`):**

```blade
@if (auth()->user()->can('Kế toán thanh toán')
     && $data['status'] == BillPaymentRequest::STATUS_AWAITING_CREATE_BILL_PAYMENT)   {{-- = 6 --}}
    @if ($data['type_payment'] == 2)   {{-- CK --}}  <a> Tạo phiếu ủy nhiệm chi </a>
    @else                              {{-- TM --}}  <a> Tạo phiếu chi </a>
    @endif
@endif
```

→ **2 nút LOẠI TRỪ NHAU**, 1 đề nghị không bao giờ hiện cả hai. Điều kiện lập UNC đúng 3 vế:
`status = 6` (Chờ tạo phiếu chi) · `type_payment = 2` (chuyển khoản) · quyền **Kế toán thanh toán**.
ERP chỉ đặt nút ở màn CHI TIẾT, không có ở màn danh sách — HRM có thêm ở danh sách (chênh lệch có
chủ ý, đã có sẵn cho nút "Tạo phiếu chi", nay làm đối xứng cho UNC theo yêu cầu user).

**KHÔNG có vế "đề nghị chưa có UNC nào"** — RULING U-UNC-2 (user chốt 2026-08-20), khớp
`BillPaymentAuthorizationService::searchAvailableRequests()` (không `whereNotExists`). Khác cờ
phiếu chi (CÓ vế này). Cố ý, đừng "sửa cho đối xứng".

**Lỗi phát hiện kèm:** cờ `is_can_create_bill_payment` cũ THIẾU vế `type_payment` → **80 đề nghị CK
đang ở status 6 hiện nhầm nút "Tạo phiếu chi"**, bấm vào là lập phiếu tiền mặt cho khoản chuyển
khoản. Dữ liệu thật chưa từng có ca này (0/2.574 UNC lập từ đề nghị TM · 0/1.188 phiếu chi lập từ
đề nghị CK) nên siết lại không làm hỏng phiếu nào đang chạy.

- [x] **BE-1** `Transformers/BillPaymentRequestResource/BillPaymentRequestDetailResource.php` —
      thêm vế `type_payment != 2` vào `is_can_create_bill_payment`; thêm cờ mới
      `is_can_create_bill_payment_authorization` (status 6 · `type_payment == 2` · quyền KTTT).
- [x] **BE-2** `Transformers/BillPaymentRequestResource/BillPaymentRequestListResource.php` —
      y hệt BE-1 cho tầng danh sách (dùng `$hasBillPaymentIds` + `$isAccountant` đã tính sẵn 1 lượt,
      KHÔNG query thêm cho cờ UNC vì cờ này không cần kiểm tra "đã có phiếu chưa").
- [x] **FE-1** `pages/finance/bill-payment-requests/index.vue` — thêm hành động dòng
      `create_bill_payment_authorization` ("Tạo ủy nhiệm chi", `ri-add-line`) trỏ
      `/finance/bill-payment-authorizations/create?bill_payment_request_id={id}` + nhánh tương ứng
      trong `handleRowAction()`. `visible` đọc cờ BE, FE KHÔNG tự suy từ `item.type_payment`.
- [x] **FE-2** `pages/finance/bill-payment-requests/components/BillPaymentRequestForm.vue` — thêm
      `V2BaseButton` "Tạo ủy nhiệm chi" cạnh nút "Tạo phiếu chi" (cùng `primary size="sm"`), thêm
      `is_can_create_bill_payment_authorization: false` vào `detailFlags` (fail-closed) + map từ
      response + method `goToCreateBillPaymentAuthorization()`.

**Verify (HTTP kernel + JWT super admin employee_id 13, chỉ ĐỌC, không ghi):**

| Kiểm tra | Kết quả |
| --- | --- |
| `php -l` 2 Resource | No syntax errors |
| Compile 3 file `.vue` (vue-template-compiler + babel) | OK cả 3 |
| Chi tiết đề nghị **CK** id 3663 (`type_payment=2`, status 6) | 200 · phiếu chi `false` · **UNC `true`** |
| Chi tiết đề nghị **TM** id 3388 (`type_payment=1`, status 6) | 200 · **phiếu chi `true`** · UNC `false` |
| Danh sách lọc status 6 (96 dòng) | phiếu chi 16 · UNC 80 · **hiện cả 2 nút: 0 dòng** |
| Đối chiếu SQL `GROUP BY type_payment` trên status 6 | TM 16 · CK 80 — khớp tuyệt đối |

### Checkpoint — 2026-08-27
Vừa hoàn thành: nút "Tạo ủy nhiệm chi" ở màn danh sách + chi tiết Đề nghị thanh toán, kèm siết cờ
"Tạo phiếu chi" về đúng đề nghị tiền mặt (2 nút loại trừ nhau theo ERP).
Đang làm dở: không.
Bước tiếp theo: user mở 1 đề nghị CK trạng thái "Chờ tạo phiếu chi" xác nhận thấy nút "Tạo ủy nhiệm
chi", bấm sang form thấy đề nghị nạp sẵn; mở 1 đề nghị TM xác nhận vẫn là nút "Tạo phiếu chi".
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt; 3 endpoint BE đã gọi thật.
Blocked: không.

### Dropdown "Loại chi" ở form UNC thiếu 2 loại (2026-08-27)

Người dùng báo: màn Thêm phiếu ủy nhiệm chi, ô Loại chi ít lựa chọn hơn ERP.

**Nguyên nhân — ERP dùng 2 DANH SÁCH KHÁC NHAU, HRM chép chung 1:**

| Nơi dùng | ERP gọi | Ra mấy loại |
| --- | --- | --- |
| **Form** lập/sửa UNC (`bill_payment_authorizations/formJs.blade.php:2`) | `type_for_select()` — KHÔNG tham số | **7**: 1·2·3·4·6·10·12 |
| **Ô lọc** màn danh sách UNC (`bill_payment_authorizations/index.blade.php:59`) | `type_for_select([4])` — bỏ loại 4 | **6**: 1·2·3·6·10·12 |

HRM cho form đọc chung `meta.types` (= danh sách của Ô LỌC) → form mất loại 4. Thêm nữa hằng
`TYPES_FOR_FILTER` viết `[1, 2, 6, 10, 12]` — **bỏ nhầm cả loại 3 "Chi thưởng NVKD"** trong khi
docblock của chính nó chỉ nói bỏ loại 4. Kết quả: form thiếu **loại 3 + loại 4**, ô lọc thiếu **loại 3**.

Comment ở `BillPaymentAuthorizationForm.vue` khẳng định "đúng ERP `type_for_select([4])`" là **sai** —
`[4]` chỉ áp cho ô lọc, không áp cho form. Đã sửa lại comment.

Không phải hạn chế có chủ ý: BE vẫn validate `Rule::in([1,2,3,4,6,10,12])`
(`BillPaymentAuthorizationStoreRequest:140`) và nhánh loại 4 (bảng nhân viên,
`BillPaymentAuthorizationEmployeeAccountingService` + `saveAccountsDetailEmployee()`) đã dựng đủ —
tức có loại chi lưu được nhưng không chọn nổi trên dropdown.

- [x] **BE-1** `Services/BillPaymentAuthorizationService.php` — sửa `TYPES_FOR_FILTER` thành
      `[1, 2, 3, 6, 10, 12]` (thêm lại loại 3); thêm hằng `TYPES_FOR_FORM = [1,2,3,4,6,10,12]`.
- [x] **BE-2** cùng file — `meta()` trả THÊM khóa `form_types`; tách `typesForFilter()` /
      `typesForForm()` dùng chung helper `mapTypes()`. `types` giữ nguyên tên cho ô lọc (không
      đổi contract cũ).
- [x] **FE-1** `bill-payment-authorizations/components/BillPaymentAuthorizationForm.vue` —
      `loadListMeta()` đọc `response.form_types` thay cho `response.types`; viết lại docblock cho
      đúng 2 nguồn của ERP.
- [x] **FE-2** cùng file — popup chọn đề nghị nhận `requestTypeOptions` (computed) thay cho
      `typeOptions`: ô lọc "Loại chi" trong popup lọc theo loại của ĐỀ NGHỊ, mà đề nghị bên ERP
      dùng `type_for_select([3,4,10])` nên chỉ có 4 loại. Hằng mới `TYPES_OF_REQUEST = [1,2,6,12]`.
      Dữ liệu thật: 4.052 đề nghị chỉ mang loại 1 (3.330) · 2 (206) · 6 (430) · 12 (86).

**Verify (HTTP kernel + JWT super admin, chỉ đọc):**

| Kiểm tra | Kết quả |
| --- | --- |
| `php -l` service · compile `BillPaymentAuthorizationForm.vue` | Sạch |
| `GET /bill-payment-authorizations?per_page=1` → `form_types` | **7 loại**: 1·2·3·4·6·10·12 — khớp `type_for_select()` ERP |
| cùng response → `types` (ô lọc) | **6 loại**: 1·2·3·6·10·12 — khớp `type_for_select([4])` ERP |
| cùng response → `statuses` | 2 mục (Đang tạo · Đã hạch toán) — không hồi quy phần sửa trước |

### Checkpoint — 2026-08-27
Vừa hoàn thành: tách nguồn Loại chi của FORM (7 loại) khỏi Ô LỌC (6 loại) đúng ERP; thêm lại loại 3
bị bỏ nhầm; thu hẹp ô lọc Loại chi trong popup chọn đề nghị về 4 loại đề nghị thật sự có.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payment-authorizations/create` xác nhận ô Loại chi đủ 7 mục,
chọn "Chi thu nhập cho nhân viên" (loại 4) thấy form rẽ sang nhánh bảng nhân viên.
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt; endpoint BE đã gọi thật.
Blocked: không.

### Bảng chi thu nhập nhân viên: thanh cuộn trên + bỏ min-height 50vh (2026-08-27)

Người dùng yêu cầu bảng ở `/finance/bill-payment-authorizations/create` dùng đúng khuôn bảng của
`customer-care/warranty-repair-requests/create`: thanh cuộn ngang Ở TRÊN, và bảng trống thì gọn.

**Rà cả màn — chỉ 1 bảng lệch:**

| Bảng | Khung bọc | Kết luận |
| --- | --- | --- |
| Nhánh A (loại 1·2·6·10·12) — `BillPaymentAuthorizationForm.vue:342` | `V2BaseTableScroll` | ✅ ĐÃ đúng khuôn tham chiếu từ trước |
| Nhánh B (loại 4) — `PaymentEmployeeTable.vue:9` | `.table-responsive` | ❌ LỆCH — đã sửa |
| Popup chọn đề nghị — `PaymentRequestSearchModal.vue:274` | `.request-table-wrap` (`max-height:52vh` + sticky thead) | ✅ khuôn popup riêng, KHÔNG dính rule global |

**Nguyên nhân bảng nhánh B:** `.table-responsive` dính rule TOÀN CỤC
`assets/scss/default.scss:85 → min-height: 50vh` nên khung bảng RỖNG (chưa chọn phòng ban, hoặc
phòng ban không có nhân viên) vẫn cao nửa màn hình; và `.table-responsive` chỉ có thanh cuộn DƯỚI,
trong khi bảng này rộng (4 cột cố định + 2 nhóm 5 cột tiền + 4 cột ngân hàng) nên luôn tràn ngang.

⚠️ `PaymentEmployeeTable.vue` là component DÙNG CHUNG của màn Phiếu chi và màn UNC.
**User chốt 2026-08-27: sửa thẳng, cho cả 2 màn cùng đổi, KHÔNG thêm prop rẽ nhánh.**

- [x] **FE-1** `pages/finance/bill-payments/components/PaymentEmployeeTable.vue` — đổi
      `<div class="table-responsive">` thành `<V2BaseTableScroll>` (đóng thẻ tương ứng ở cuối bảng),
      thêm import + khai `components`. Kèm comment nêu 2 lý do + ghi rõ đây là component dùng chung.
- [x] **FE-2** kiểm tra `.employee-table` trong `<style scoped>` — không có rule nào phụ thuộc
      `.table-responsive` (rule global chỉ đặt `border` + `min-height`), nên bỏ khung bọc không mất
      viền: `table-bordered` của Bootstrap tự lo, đúng như bảng ở màn tham chiếu.

**Verify:** compile (vue-template-compiler + babel) 4 file OK — `PaymentEmployeeTable.vue`,
`BillPaymentForm.vue` (màn Phiếu chi, dùng chung component), `BillPaymentAuthorizationForm.vue`,
`V2BaseTableScroll.vue`. Grep lại: không còn `.table-responsive` nào trong màn UNC.

**CHƯA đụng tới (ngoài phạm vi user hỏi, chỉ ghi lại):** màn Phiếu chi còn 2 chỗ dùng
`.table-responsive` nên vẫn dính `min-height: 50vh` — `BillPaymentForm.vue:250` (bảng nhánh A của
Phiếu chi) và `ApproveBillPaymentModal.vue:15`.

**Chênh lệch nhỏ còn lại so với màn tham chiếu (cosmetic, CHƯA sửa vì bảng đang chạy đúng):**
bảng nhánh A dùng class `.detail-table` (nền th `#f5f6f8`, giữ padding dọc mặc định của
`table-sm`), màn tham chiếu dùng `.v2-form-table` (nền th `#f8fafc`, `padding-top/bottom: 4px`).

### Checkpoint — 2026-08-27
Vừa hoàn thành: bảng chi thu nhập nhân viên (loại chi 4) chuyển sang `V2BaseTableScroll` — có thanh
cuộn ngang phía trên, bảng trống không còn cao 50vh. Áp dụng cho cả màn Phiếu chi (component chung).
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payment-authorizations/create`, chọn Loại chi "Chi thu nhập
cho nhân viên" xác nhận bảng gọn khi chưa chọn phòng ban và có thanh cuộn trên khi đã có dữ liệu;
mở thêm màn Phiếu chi loại 4 kiểm tra không hồi quy.
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt, chỉ compile.
Blocked: không.

### Bảng nhân viên: cột bị bóp, chữ/ô nhập bị che (2026-08-27)

Người dùng báo: chọn Loại chi "Chi thu nhập cho nhân viên", cột Nhân viên và các cột nhập số tiền
bị che mất nội dung.

**Nguyên nhân:** mọi cột khai `style="width: Xpx"`. Bảng để `table-layout: auto` (mặc định) nên
`width` chỉ là **GỢI Ý** — khi tổng bề rộng mong muốn vượt khung, trình duyệt bóp đều mọi cột cho
vừa. Bảng này 18 cột (4 cố định + 5 cột tiền đề nghị + 5 cột tiền chi + 4 cột ngân hàng/tổng, bản
Phiếu chi là 6+6) nên bị bóp rất mạnh: `V2BaseSelect` và `V2BaseCurrencyInput` bên trong ô cắt chữ
bằng "…", tên nhân viên xuống dòng/mất chữ.

`min-width` mới là ràng buộc CỨNG: bảng nở đúng bề rộng cần rồi tràn ngang — đúng lúc đó
`V2BaseTableScroll` (vừa gắn ở task trước) mới phát huy tác dụng. Đây cũng là cách màn tham chiếu
`customer-care/warranty-repair-requests` làm (`style="min-width: 260px"`).

- [x] **FE-1** `pages/finance/bill-payments/components/PaymentEmployeeTable.vue` — đổi TOÀN BỘ
      `style="width:"` của `<th>` sang `style="min-width:"`, kèm nới bề rộng:

      | Cột | Cũ | Mới |
      | --- | --- | --- |
      | STT | 50 | 50 |
      | Số tài khoản nợ | 190 | 200 |
      | Tên tài khoản | 170 | 190 |
      | **Nhân viên** | 210 | **260** |
      | Cột tiền ĐỀ NGHỊ (mỗi cột, chỉ hiện chữ) | 120 | 140 |
      | **Cột tiền CHI (mỗi cột, có ô nhập)** | 130 | **160** |
      | Số tài khoản ngân hàng | 150 | 160 |
      | Tên ngân hàng | 160 | 180 |
      | Chi nhánh | 150 | 170 |
      | Tổng cộng | 130 | 150 |

      Bề rộng bảng sau khi sửa: **~2.860px** ở màn UNC (5 khoản) · **~3.160px** ở màn Phiếu chi
      (6 khoản) -> luôn tràn ngang, thanh cuộn trên/dưới luôn hiện. Đúng chủ đích.
- [x] **FE-2** ghi comment ngay trong `<thead>` giải thích vì sao PHẢI là `min-width` — đây là bẫy
      dễ tái phạm khi thêm cột mới.

**Verify:** compile (vue-template-compiler + babel) OK; grep xác nhận không còn `style="width:"`
nào trong file. Component dùng chung nên màn Phiếu chi loại 4 cũng nới theo (user đã chốt ở task
trước: sửa thẳng cho cả 2 màn).

### Checkpoint — 2026-08-27
Vừa hoàn thành: nới bề rộng cột bảng chi thu nhập nhân viên bằng `min-width` (Nhân viên 210→260,
cột nhập tiền 130→160), hết cảnh chữ bị cắt.
Đang làm dở: không.
Bước tiếp theo: user chọn Loại chi "Chi thu nhập cho nhân viên", chọn phòng ban có nhân viên, xác
nhận đọc đủ tên nhân viên và gõ số tiền không bị khuất; kéo thanh cuộn ngang trên/dưới.
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt, chỉ compile — bề rộng thực tế cần nhìn mới chốt được.
Blocked: không.

### Test 2 loại chi mới mở + sửa loại 3 thiếu nhánh A (2026-08-27)

Trước đó CHƯA chạy thật loại 3 / loại 4 sau khi mở dropdown 7 loại — mới chỉ verify `meta` trả đủ
danh sách. Test lại thì loại 3 hỏng.

**Lỗi loại 3:** `BillPaymentAuthorization::TYPES_FROM_REQUEST` = `[1, 2, 6, 10, 12]` — THIẾU loại 3,
kèm docblock nói "loại 3 đã bị bỏ khỏi `BillPaymentRequest::TYPE`". Câu đó SAI: `TYPE` vẫn mở
`3 => 'Chi thưởng NVKD'` ở CẢ ERP lẫn HRM. Đối chiếu ERP:

```js
// resources/views/partials/classes/IncomeExpenditure/BillPayment.blade.php:39
get has_bill_payment_request() {
    return !this.type || this.type == 1 || this.type == 2 || this.type == 3
        || this.type == 6 || this.type == 10 || this.type == 12;   // <-- CÓ loại 3
}
```

Hậu quả: chọn loại 3 -> FE `isRequestBranch` false -> ô "Phiếu đề nghị" bị ẩn, bảng chi tiết rỗng
không nạp được dòng; trong khi `BillPaymentAuthorizationStoreRequest:163` vẫn xếp loại 3 vào nhánh A
(`in_array($type, [1,2,3])`) nên bắt buộc `bill_payment_request_id` -> lưu nháp 200 nhưng duyệt 422
vĩnh viễn. User chốt: "bên ERP có như nào thì làm như vậy".

- [x] **BE-1** `Entities/BillPaymentAuthorization/BillPaymentAuthorization.php` — `TYPES_FROM_REQUEST`
      thành `[1, 2, 3, 6, 10, 12]`, docblock port nguyên văn getter `has_bill_payment_request` của ERP.
- [x] **FE-1** `bill-payment-authorizations/components/BillPaymentAuthorizationForm.vue` — hằng
      `TYPES_FROM_REQUEST` đồng bộ `[1, 2, 3, 6, 10, 12]`.
- [x] **BE-2** sửa 2 docblock nói sai "loại 3 đã bị bỏ khỏi TYPE": `BillPaymentAuthorizationWriteService.php`
      (hằng `TYPES_ACCOUNTING_FROM_REQUEST`) và `BillPaymentAuthorizationStoreRequest.php` (khối nhánh A).

**Verify (HTTP kernel + JWT super admin, transaction rồi rollback — UNC về đúng 2.575, sổ cái về
đúng 972.053 dòng):**

| Kiểm tra | Kết quả |
| --- | --- |
| `php -l` 3 file BE · compile form `.vue` | Sạch |
| **Lưu nháp** cả 7 loại (1·2·3·4·6·10·12) | **200 cả 7** |
| `is_from_request` ở màn chi tiết: loại 1 · 3 · 10 | **true** cả 3 (trước khi sửa loại 3 ra `false`) |
| `is_from_request`: loại 4 | **false** — đúng, loại 4 là nhánh B |
| **Lưu và duyệt loại 4** (phòng ban 52, 2 nhân viên, TK nợ thật) | **200** · phiếu `TPE.UNC0826.00002` · `status = 3` · **sinh 3 bút toán** |
| `GET /payment-employees?department_id=52` | 200, trả 2 nhân viên |
| Lưu và duyệt loại 3 / loại 4 với form TRỐNG | 422 đúng nhóm khóa của từng nhánh (loại 3 có `bill_payment_request_id`, loại 4 không có) |

**Giới hạn còn lại của loại 3 — ĐÚNG HÀNH VI ERP, không "dọn giúp":** không lập nổi phiếu loại 3
hoàn chỉnh vì chưa từng có đề nghị thanh toán loại 3 để chọn. Cả 2 hệ đều chặn ở màn Đề nghị:
ERP `type_for_select([3,4,10])`, HRM `BillPaymentRequest::TYPES_ALLOWED = [1,2,6,12]` +
`BillPaymentRequestStoreRequest:82` `Rule::in(TYPES_ALLOWED)`. DB: 0 đề nghị loại 3, 0 UNC loại 3.
Nay ít nhất form KHÔNG còn tắc bất thường — hiện ô chọn đề nghị y như ERP, đúng nhánh A.

### Checkpoint — 2026-08-27
Vừa hoàn thành: test thật 7 loại chi; loại 4 chạy end-to-end tới sổ cái; sửa loại 3 thiếu trong
`TYPES_FROM_REQUEST` (BE + FE) theo đúng getter `has_bill_payment_request` của ERP; sửa 2 docblock sai.
Đang làm dở: không.
Bước tiếp theo: user mở form chọn lần lượt 7 loại chi, xác nhận loại 3 giờ có ô "Phiếu đề nghị"
(dù danh sách rỗng vì không có đề nghị loại 3), loại 4 hiện bảng nhân viên.
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt; toàn bộ số liệu trên lấy từ lời gọi API thật.
Blocked: không.

## Phase — Tinh chỉnh UI màn danh sách

- [x] **FE-1** cột "Mã phiếu đề nghị chi" ở `pages/finance/bill-payment-authorizations/index.vue`
      (slot `#cell-requestCode`): thêm `target="_blank" rel="noopener"` vào `<nuxt-link>` để click mở
      TAB MỚI, giống cột cùng tên ở màn Phiếu chi tiền (`pages/finance/bill-payments/index.vue:139`).
      Cột "Mã phiếu" (chi tiết UNC) giữ nguyên điều hướng cùng tab.

- [x] **FE-2** nhãn "Tài khoản nhận tiền" ở màn CHI TIẾT hiện màu ĐỎ như lỗi validate:
      `BillPaymentAuthorizationForm.vue:304` dùng `class="text-muted"`, mà 4 file SCSS toàn cục
      (`assets/scss/custom.scss:241`, `custom-theme.scss:190`, `custom-assign.scss:12`,
      `custom-timesheet.scss:16`) đều ép `.text-muted { color: #dc3545 !important }`.
      Đổi sang class scoped `.group-label` (xám #6b7280) — đúng gotcha đã ghi sẵn ở đầu `<style>`
      của chính file này nhưng chỗ nhãn nhóm bị sót.
- [x] **FE-3** cùng lỗi ở `PaymentRequestSearchModal.vue:80,83` (dòng "Đang tải..." /
      "Không có dữ liệu phù hợp." ra đỏ) → đổi sang `.v2-empty-row` xám, kèm comment cảnh báo.

**Verify:** compile template `index.vue` + `BillPaymentAuthorizationForm.vue` +
`PaymentRequestSearchModal.vue` bằng `vue-template-compiler` — 0 lỗi. Không còn `class="text-muted"`
nào trong folder feature. Chưa mở trình duyệt.

### Checkpoint — 2026-08-27
Vừa hoàn thành: FE-1 mã phiếu đề nghị chi mở tab mới; FE-2/FE-3 bỏ `.text-muted` (bị SCSS toàn cục
ép đỏ) ở nhãn "Tài khoản nhận tiền" và 2 dòng trạng thái của popup chọn phiếu đề nghị.
Đang làm dở: không.
Bước tiếp theo: user mở màn danh sách UNC click mã phiếu đề nghị chi (mở tab mới) và mở màn chi tiết
phiếu nhánh A xác nhận nhãn "Tài khoản nhận tiền" đã ra xám.
Blocked: không.

### Rà tiếp loại 4 theo ERP: TK có mặc định + bịt lỗ hổng nhánh B (2026-08-27)

User: "bên ERP như nào thì làm như vậy". Rà tiếp nhánh B (loại 4) thì thấy 2 điểm chưa port.

**1. Thiếu gán "Tài khoản có" khi chọn loại 4.** ERP UNC `formJs.blade.php::changeType()`:

```js
$scope.changeType = () => {
    if ($scope.form.type == 4) {
        $scope.form.account_has = 6;      // <-- HRM THIẾU dòng này
        $scope.form.type_money_id = 1;    // <-- HRM đã có
    }
}
```

HRM `onTypeChange()` chỉ set `type_money_id` -> ô "Tài khoản có" để trống, người dùng phải tự dò
trong danh sách tài khoản. `DEFAULT_ACCOUNT_HAS = 6` đã có sẵn nhưng chỉ dùng ở nhánh A
(`loadRequestDetail()`, port từ `addBillPaymentRequest()` — DÒNG ERP KHÁC).

⚠️ Số của UNC là **6** (TK 1121 – ngân hàng), của Phiếu chi là **2** (TK 1111 – tiền mặt,
`bill_payments/formJs.blade.php:45`). Dữ liệu thật: 117/117 phiếu chi loại 4 đều `account_has = 2`.
Tách 2 hằng riêng, đừng hợp nhất.

**2. Lỗ hổng nhánh B — ĐÃ DỰNG LẠI ĐƯỢC BẰNG LỜI GỌI API THẬT.** ERP chỉ khóa 2 ô bằng JavaScript
nên gọi thẳng API là lách được. Màn Phiếu chi đã bịt từ 2026-08-24
(`BillPaymentWriteService::billAttributesFromClient()`), UNC thì CHƯA.

Payload độc hại: `type = 4` (nhánh B) kèm `bill_payment_request_id` của đề nghị `TPE.DNTT0626.00108`
+ `account_has` lạ + `type_money_id = 2` / `exchange_rate = 25000`.

| | Trước khi sửa | Sau khi sửa |
| --- | --- | --- |
| HTTP | 200 | 200 |
| `account_has` | **1** (TK bất kỳ) | **6** |
| `type_money_id` · `exchange_rate` | **2 · 25.000** (ngoại tệ) | **1 · 1** |
| `bill_payment_request_id` | **3663** | **NULL** |
| Đề nghị `TPE.DNTT0626.00108` | **6 -> 8, BỊ ĐỔI OAN** | **giữ 6** |

Hai hệ quả thật: (a) đề nghị của người khác bị đẩy sang "Đã tạo phiếu chi" mà không có phiếu nào
thật sự chi cho nó; (b) phiếu ghi ngoại tệ trong khi
`BillPaymentAuthorizationEmployeeAccountingService:216-217` ghi cứng `currency_id = 1` /
`exchange_rate = 1.0` -> số tiền vào sổ cái bị hiểu là VND, sai âm thầm không báo lỗi.

- [x] **FE-1** `BillPaymentAuthorizationForm.vue` — thêm hằng `ACCOUNT_HAS_EMPLOYEE = 6` (docblock
      nêu rõ khác số 2 của Phiếu chi); `onTypeChange()` nhánh B gán `form.account_has`.
- [x] **FE-2** cùng file — `buildPayload()` ép `account_has` ở nhánh B (user có thể đổi tay TRƯỚC
      khi chuyển loại), và ô "Tài khoản có" thêm `:disabled="readonly || isEmployeeBranch"` —
      cùng khuôn `BillPaymentForm.vue:79-93`.
- [x] **BE-1** `BillPaymentAuthorizationWriteService.php` — thêm 2 hằng
      `PAYMENT_EMPLOYEE_ACCOUNT_HAS = 6` / `PAYMENT_EMPLOYEE_CURRENCY_ID = 1`; trong
      `billAttributesFromClient()` thêm khối nhánh B ép 4 giá trị
      (`bill_payment_request_id = null` · `account_has` · `type_money_id` · `exchange_rate = 1`).
      Đặt SAU khối chuẩn hóa `?? 0` để luôn thắng.

**Verify (HTTP kernel + JWT super admin, transaction rồi rollback):**

| Kiểm tra | Kết quả |
| --- | --- |
| `php -l` write service · compile form `.vue` | Sạch |
| Chạy LẠI đúng payload độc hại | 200 · `account_has=6` · `type_money_id=1` · `bill_payment_request_id=NULL` · **đề nghị giữ status 6** |
| Hồi quy: lưu nháp 7 loại | 200 cả 7 |
| Hồi quy: lưu và duyệt loại 4 hợp lệ | 200 · status 3 · **vẫn sinh 3 bút toán** |
| DB sau rollback | UNC 2.575 · sổ cái 972.053 — nguyên vẹn |

### Checkpoint — 2026-08-27
Vừa hoàn thành: port nốt `changeType()` của ERP cho loại 4 (điền sẵn TK có 1121) và bịt lỗ hổng
nhánh B ở BE (4 giá trị khóa cứng) — lỗ hổng đã tái hiện được và đã chứng minh bịt xong.
Đang làm dở: không.
Bước tiếp theo: user chọn Loại chi "Chi thu nhập cho nhân viên", xác nhận ô "Tài khoản có" tự điền
1121 và bị khóa; lưu và duyệt 1 phiếu thật xem bút toán đúng.
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt; toàn bộ số liệu trên từ lời gọi API thật.
Blocked: không.


## Đợt sửa nhanh — lọc Mã phiếu ở tìm kiếm nâng cao (2026-08-28)

User: "màn danh sách phiếu ủy nhiệm chi thêm lọc mã phiếu cho tôi ở tìm kiếm nâng cao, lưu ý là
đặt name khác so với cái tìm kiếm nhanh".

**Yêu cầu thật (user phải nói lại lần 2):** 2 ô **ĐỘC LẬP HOÀN TOÀN** — gõ ở ô nâng cao thì ô tìm
nhanh phải ĐỨNG YÊN. Bản làm đầu tiên hiểu ngược ("cái còn lại tự ăn theo" → đồng bộ 2 chiều bằng
watcher) và user báo lại: *"khi tôi gõ tìm kiếm ở dưới bộ lọc nâng cao thì nó cũng hiện lên trên
tìm kiếm nhanh"*. Đã gỡ hết watcher.

**Thêm một lý do phải tách khoá** (ngoài yêu cầu của user): popup "Cài đặt bộ lọc" khi user tắt một
field sẽ **xoá luôn giá trị lọc** của key đó — `V2BaseSmartFilterPanel.onConfigSaved()`
(`components/V2BaseSmartFilterPanel.vue:339-357`). Dùng chung key `code` thì ẩn ô nâng cao đi là ô
tìm nhanh bị xoá trắng theo.

- [x] **FE** `pages/finance/bill-payment-authorizations/index.vue`
      - `initialStateForm`: thêm `code_filter: ''` (khoá riêng, KHÔNG đồng bộ với `code`).
      - `filterFields`: thêm field ĐẦU TIÊN `{ key: 'code_filter', label: 'Mã phiếu', type: 'text' }`
        → panel còn 11 trường (trước 10).
      - `ignoredFields`: thêm `'code_filter'` — ô GÕ TAY, không được tự gọi API mỗi phím
        (quy tắc skill `list-page`).
      - `buildParams()` giữ nguyên: `code_filter` nằm trong `filters` nên tự đi kèm query string.
      - **KHÔNG có watcher đồng bộ** — đây là điểm user chốt.
- [x] **BE** `Modules/Finance/Services/BillPaymentAuthorizationService.php::applyFieldFilters()` —
      thêm điều kiện riêng `code_filter` → `where('code','like','%…%')`, đặt ngay sau điều kiện
      `code`. Điền cả 2 ô thì lọc **AND** (2 điều kiện LIKE trên cùng cột).

**Verify:** `php -l` sạch · `vue-template-compiler` + `@babel/parser` parse sạch cả template lẫn
script · đã grep xác nhận không còn watcher `filters.code` / `filters.code_filter`.
⚠️ Chưa mở trình duyệt — chưa kiểm chứng bằng mắt việc 2 ô KHÔNG ăn theo nhau.

⚠️ **Bẫy CRLF (lại dính)**: `index.vue` màn này và file service BE đều là **CRLF**; script Python
đọc bằng `io.open(..., encoding=...)` rồi ghi `newline=''` sẽ nuốt hết `
` → git cảnh báo
"LF will be replaced by CRLF". Sửa file bằng script thì đọc/ghi ở chế độ **nhị phân**, dò `

`
trước rồi nối lại đúng kiểu xuống dòng cũ.

⚠️ **Bài học đọc yêu cầu**: câu "để khi bấm ở 1 cái thì cái còn lại tự ăn theo" bị hiểu thành
"muốn đồng bộ" trong khi user đang **mô tả hiện tượng không mong muốn**. Yêu cầu mơ hồ về hành vi
2 chiều → hỏi lại 1 câu trước khi code, rẻ hơn làm rồi gỡ.

### Checkpoint — 2026-08-28
Vừa hoàn thành: thêm ô lọc "Mã phiếu" vào tìm kiếm nâng cao màn danh sách Ủy nhiệm chi — khoá riêng
`code_filter`, độc lập hoàn toàn với ô tìm nhanh `code`, BE lọc bằng điều kiện LIKE riêng.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payment-authorizations` → bung "Tìm kiếm nâng cao", gõ mã ở
ô nâng cao và xác nhận ô tìm nhanh KHÔNG đổi theo; bấm Tìm kiếm ra đúng phiếu; bấm Làm mới xoá cả 2.
Blocked: không.


## Đợt sửa nhanh — cột "cập nhật" + đổi tên cột tạo (2026-08-28)

User: *"Cấu hình cột tùy chỉnh: Thiếu trường Người cập nhật, Ngày cập nhật. Ngày lập và Người lập
đổi về thành Ngày tạo và Người tạo"* → đưa màn Ủy nhiệm chi về khớp màn **Phiếu chi**
(`pages/finance/bill-payments/index.vue:487-490`).

**Hiện trạng đã đo trước khi sửa** (đừng đoán lại lần sau):
- 2 cột `updatedAt` / `updatedByName` VẪN CÓ trong `allColumns` và VẪN hiện trong popup — nhưng
  khai `isVisible: false` nên **không nằm trên bảng**; popup không lọc bỏ cột nào
  (`components/modal/column-customization-modal.vue:49` `v-for` thẳng, chỉ cuộn `max-height:55vh`).
- BE trả đủ dữ liệu: `BillPaymentAuthorizationListResource.php:73-74` có `updated_at` +
  `updated_by_name`; template đã sẵn slot `#cell-updatedAt` / `#cell-updatedByName`.

- [x] **FE** `pages/finance/bill-payment-authorizations/index.vue` — `allColumns`:
      - `createdAt` "Ngày lập" → **"Ngày tạo"**, `createdByName` "Người lập" → **"Người tạo"**.
      - Bỏ `isVisible: false` ở `updatedAt` + `updatedByName`, dời 2 cột này lên NGAY SAU cặp cột
        tạo (đúng thứ tự màn Phiếu chi). Còn đúng 2 cột ẩn mặc định: Số tiền duyệt chi ·
        Ngày hạch toán.
- [x] **BE** không đụng gì.

⚠️ **Nhãn BỘ LỌC giữ nguyên** "Người lập" / "Khoảng ngày lập" / "Ngày lập từ–đến" — màn Phiếu chi
cũng vậy (`bill-payments/index.vue:429,459`). Cố ý lệch giữa nhãn cột và nhãn lọc, đừng "đồng bộ".

⚠️ **Cấu hình đã lưu của user thắng code**: `mergedColumns` lấy `isVisible` từ bản ghi
`user_column_settings` (row id 37, `user_id=13`, `screen_key=finance_bill_payment_authorizations`,
lưu 2026-08-20) — bản ghi này đang để 2 cột cập nhật `false`. Tiêu đề cột thì lấy từ code
(`{ ...defaultCol, isVisible: savedCol.isVisible }`) nên **đổi tên có hiệu lực ngay**, còn muốn 2
cột cập nhật hiện lên thì user phải **tích 1 lần** trong popup (hoặc xoá bản ghi cấu hình đó).

### Checkpoint — 2026-08-28
Vừa hoàn thành: đổi tiêu đề cột Ngày/Người lập → Ngày/Người tạo và cho cặp cột Ngày/Người cập nhật
hiện mặc định trên màn danh sách Ủy nhiệm chi.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payment-authorizations`, tích 2 cột cập nhật trong popup
"Cấu hình cột hiển thị" (cấu hình cũ đang tắt), xác nhận tiêu đề cột đã là "Ngày tạo"/"Người tạo".
Blocked: không.

## Đợt sửa — thứ tự trường form Tạo/Sửa/Chi tiết bám ERP (2026-08-28)

User: *"trong màn tạo mới, thứ tự các trường đang không được đặt thứ tự như bên erp, ví dụ phiếu đề
nghị phải lên đầu"*.

**Đối chiếu ERP** `income_expenditure/bill_payment_authorizations/form.blade.php`:
- nhánh A (:29-287): Số phiếu đề nghị *(hàng riêng)* → Mã phiếu → Tài khoản có → Tài khoản nợ
  *(type≠6)* → **Ngày hạch toán** → Loại chi → Hình thức thanh toán → Loại tiền | Tỷ giá →
  Người đề nghị → Phòng ban → Lý do chi → *(ô đối tượng)* → Phương thức thanh toán → Ngân hàng
  chuyển → Số TK chuyển khoản.
- nhánh B (:475-629): Mã phiếu → Tài khoản có → Loại chi → Hình thức thanh toán → **Người nhận
  tiền** → Loại tiền | Tỷ giá → Người đề nghị → **Phòng ban** → Lý do chi → Ngân hàng chuyển →
  Số TK chuyển khoản.

**HRM đang sai 4 chỗ**: Loại chi đứng ĐẦU (ERP đứng sau Ngày hạch toán) · Số phiếu đề nghị đứng
thứ 2 (ERP đứng đầu, chiếm riêng 1 hàng) · Phòng ban chi (nhánh B) đứng thứ 2 (ERP đứng đúng vị trí
ô Phòng ban) · Người nhận (nhánh B) đứng sau Phòng ban (ERP đứng ngay sau Hình thức thanh toán).

Màn **Phiếu chi** (`bill-payments/components/BillPaymentForm.vue:17-246`) đã nắn đúng ERP đợt
2026-08-27/28 — lần này bê nguyên quy ước đó sang: gộp 1 lưới `form-row` duy nhất, Số phiếu đề nghị
là ô ĐẦU, 2 ô "Người lập / Ngày lập" (riêng của HRM, ERP in ở góc `card-header`) xếp sát trước
Lý do chi.

- [x] **FE** `pages/finance/bill-payment-authorizations/components/BillPaymentAuthorizationForm.vue`
      — sắp lại thứ tự khối trong `form-row` thứ nhất thành: Số phiếu đề nghị · Mã phiếu ·
      Tài khoản có · Tài khoản nợ · Ngày hạch toán · Loại chi · Hình thức thanh toán · Người nhận ·
      Loại tiền · Tỷ giá · Người đề nghị · Phòng ban · Phòng ban chi · Người lập · Ngày lập ·
      Lý do chi. 2 `form-row` sau (Phương thức thanh toán/Ngân hàng chuyển/Số TK · Tài khoản nhận
      tiền) GIỮ NGUYÊN — đã đúng thứ tự ERP.
- [x] **BE** không đụng gì.

⚠️ Chỉ ĐỔI CHỖ, không đổi `v-if` / prop / handler của bất kỳ ô nào — form dùng chung cho cả
`create.vue`, `_id/edit.vue` và `_id/index.vue` (readonly).

**Verify:** `vue-template-compiler` parse template 0 lỗi · `@babel/parser` parse script OK ·
`diff` bản cũ/mới sau khi `sort` từng dòng: **không dòng nào của trường bị đổi nội dung**, chỉ đổi
vị trí + thêm comment. ⚠️ Chưa mở trình duyệt.

📌 **3 điểm LỆCH ERP còn lại — chưa sửa, chờ user quyết** (không thuộc phạm vi "thứ tự"):
1. **Thiếu hẳn khối "Đối tượng nhận tiền"** của nhánh A: ERP có 5 ô chỉ đọc chen giữa Lý do chi và
   Phương thức thanh toán — Khách hàng (:191) · Loại đối tượng (:200, loại 10) · Nhân viên (:212) ·
   Nhà cung cấp (:221) · Phí (:231). Màn **Phiếu chi đã có** (`BillPaymentForm.vue::partyFields`
   :949-977) và BE **đã trả sẵn đủ khoá** (`BillPaymentRequestDetailResource` :63-90:
   `customer_code/name`, `supplier_code/name`, `employee_code/name`, `cost_name`,
   `type_object_name`) cho endpoint `GET /bill-payment-authorizations/payment-requests/{id}`
   ⇒ thêm vào là **FE-only ở màn Tạo**; màn Sửa/Chi tiết đọc `bill_payment_request` từ resource
   khác nên phải kiểm/bổ sung BE.
2. ERP nhánh A còn dòng chữ **"Vụ việc: <mã>"** (:282-286, `type_employee_has_contract_transfer`).
3. Lệch giữa 2 nhánh — **CỐ Ý GIỮ, đừng "dọn"**: nhánh B (loại 4) của HRM hiện thêm *Tài khoản nợ*
   + *Ngày hạch toán* mà ERP không có, vì `BillPaymentAuthorizationStoreRequest` :159 + :149 bắt
   buộc 2 trường đó cho MỌI loại ≠ 6 — ẩn đi là phiếu loại 4 không lưu nổi. Riêng *Phương thức
   thanh toán* (`source_money`) BE chỉ bắt ở loại 1/2/3 nên có thể ẩn ở nhánh B nếu user muốn khớp
   ERP tuyệt đối. Ngược lại ERP nhánh B có ô *Người đề nghị* mà HRM đang ẩn.

### Checkpoint — 2026-08-28
Vừa hoàn thành: nắn lại thứ tự 16 ô của lưới "Thông tin chung" màn Ủy nhiệm chi (Tạo/Sửa/Chi tiết
dùng chung 1 component) cho khớp ERP — Số phiếu đề nghị lên ĐẦU, Loại chi lùi xuống sau Ngày hạch
toán, Phòng ban chi về đúng ô Phòng ban, Người nhận lên ngay sau Hình thức thanh toán.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payment-authorizations/create` xác nhận thứ tự ô; sau đó
quyết 3 điểm lệch ERP còn lại ở trên (nặng nhất là khối "Đối tượng nhận tiền").
Blocked: không.


## Đợt sửa (tiếp) — bù 3 điểm lệch ERP còn lại (2026-08-28)

User: *"sửa cho giống bên erp cho tôi"* → làm nốt cả 3 điểm đã liệt kê ở trên.

- [x] **FE** `BillPaymentAuthorizationForm.vue` — thêm khối **"Đối tượng nhận tiền"** 5 ô chỉ đọc
      NGAY SAU *Lý do chi*, TRƯỚC *Phương thức thanh toán* (đúng chỗ ERP :173-223): Khách hàng ·
      Loại đối tượng · Nhân viên · Nhà cung cấp · Phí.
      Điều kiện hiện/ẩn **port nguyên 6 getter ERP** (`BillPaymentRequest.blade.php` :102-173) qua
      6 computed mới (`isSupplierParty` / `isCustomerParty` / `isEmployeeParty` / `showCostField`…):
      nguồn là `requestInfo.type` + `type_object` + `supplier_type` — tức **PHIẾU ĐỀ NGHỊ**, không
      phải `form.type` ⇒ chưa chọn đề nghị thì cả 5 ô ẩn, y như ERP. Vế `type_payment == 2` của mọi
      getter bỏ đi vì UNC luôn chuyển khoản.
      ⚠️ CỐ Ý KHÁC màn Phiếu chi: bên đó dựng ô nào **có dữ liệu** (vì phiếu TIỀN MẶT bám điều kiện
      ERP là mất sạch đối tượng). UNC không có ca đó nên bám ERP y nguyên được.
- [x] **FE** — ô **"Vụ việc"** cuối hàng chuyển tiền (ERP :282-286), chỉ hiện với đề nghị loại 6.
- [x] **FE** — *Phương thức thanh toán* **ẩn ở nhánh B** (ERP khối loại 4 không có ô này; BE chỉ bắt
      `source_money` với loại 1/2/3, cột DB `nullable` → ẩn vẫn lưu được).
- [x] **FE** — *Người đề nghị* hiện ở **cả 2 nhánh** (ERP :566-572), thêm computed `proposerName`:
      nhánh A = người lập đề nghị, nhánh B = người lập phiếu (màn Tạo còn trống, đúng ERP).
- [x] **BE** `BillPaymentAuthorizationDetailResource::requestBlock()` — thêm 3 khoá cho màn Sửa/Xem:
      `type_object_name`, `cost_name`, `supplier_type` (dùng lại `BillPaymentRequestDetailResource::
      TYPE_OBJECTS` + `::supplierType()` + `BillPaymentRequest::COST`, không dịch lại lần 2).
      Đường TẠO MỚI không phải sửa: `GET /bill-payment-authorizations/payment-requests/{id}` vốn trả
      `BillPaymentRequestDetailResource` đã có sẵn đủ khoá.
- [x] **BE** `BillPaymentAuthorizationService::meta()` — thêm `work_tthhd` = `"TTHHD - <tên>"` và
      hằng `BillPaymentAuthorization::WORK_CODE_CONTRACT_BONUS`.
      ⚠️ **KHÔNG cho FE gọi `GET /v1/finance/works`**: route đó gate `checkPermission:Quản lý danh
      mục vụ việc` mà kế toán thanh toán không có → 403. Form đã gọi sẵn `GET ?per_page=1` lấy meta
      nên không tốn thêm request.

**Verify:** `php -l` sạch 3 file BE · `vue-template-compiler` + `@babel/parser` parse sạch ·
tinker: `meta()['work_tthhd']` = `"TTHHD - Thưởng thực hiện hợp đồng"` (works id 12) ·
dựng `BillPaymentAuthorizationDetailResource` trên phiếu thật 4 loại (1/2/6/12 → bill 1/42/1470/175)
trả đúng `supplier_type` · `customer_code` · `employee_code`, không lỗi. ⚠️ Chưa mở trình duyệt.

📌 **Còn giữ nguyên có chủ ý**: nhánh B vẫn có *Tài khoản nợ* + *Ngày hạch toán* dù ERP không có —
`BillPaymentAuthorizationStoreRequest` :149 + :159 bắt buộc 2 trường đó cho MỌI loại ≠ 6, ẩn đi là
phiếu loại 4 không lưu nổi.

### Checkpoint — 2026-08-28
Vừa hoàn thành: bù đủ khối "Đối tượng nhận tiền" (5 ô) + ô "Vụ việc", ẩn Phương thức thanh toán ở
nhánh B, hiện Người đề nghị ở cả 2 nhánh — màn Ủy nhiệm chi giờ khớp ERP cả thứ tự lẫn danh sách ô.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payment-authorizations/create`, chọn 1 đề nghị loại 1 (thấy ô
Nhà cung cấp), 1 đề nghị loại 2 (ô Khách hàng), 1 đề nghị loại 6 (ô Vụ việc "TTHHD - …", KHÔNG có ô
Tài khoản nợ), rồi chọn Loại chi 4 xác nhận KHÔNG còn ô Phương thức thanh toán.
Blocked: không.

### Sửa nhanh — gộp hàng (2026-08-28)

User: *"phần Phương thức thanh toán, Ngân hàng chuyển cho lên cùng hàng với Nhà cung cấp, Phí"*.

- [x] **FE** — bỏ `<div class="form-row">` riêng của khối chuyển tiền, gộp 4 ô (Phương thức thanh
      toán · Ngân hàng chuyển · Số TK chuyển khoản · Vụ việc) vào CÙNG `form-row` với các ô phía
      trên. Bootstrap tự cho chúng chảy tiếp vào chỗ trống thay vì mở hàng mới ⇒ với đề nghị NCC
      nước ngoài, một hàng là: Nhà cung cấp · Phí · Phương thức thanh toán · Ngân hàng chuyển.
      ERP cũng để chung MỘT `<div class="row">` (:32-287) nên đây là bám ERP, không phải chế thêm.
      Khối "Tài khoản nhận tiền" vẫn là `form-row` riêng vì có dòng tiêu đề nhóm `col-12`.

**Verify:** template + script parse sạch · cấu trúc còn đúng 2 `form-row` trong SECTION 1
(lưới chính đóng sau ô Vụ việc, rồi tới khối Tài khoản nhận tiền). ⚠️ Chưa mở trình duyệt.

### Sửa nhanh — bố cục 2 khối ngân hàng người nhận (2026-08-28)

User: *"phần ngân hàng và ngân hàng trung gian để bố cục giống như màn phiếu chi sửa lúc sáng cho
tôi cho dễ phân biệt"*.

Hiện trạng trước khi sửa: UNC chỉ có MỘT khối "Tài khoản nhận tiền", NCC nước ngoài thì nhét thêm
Swift / IBAN / Địa chỉ vào cuối khối đó — **KHÔNG hề có nhóm "Ngân hàng trung gian"** dù ERP
(`form.blade.php` :288-435) có đủ 2 nhóm, và điều kiện đoán nước ngoài bằng `swift_code ||
iban_number` chính là cái bẫy màn Phiếu chi đã vấp và bỏ.

- [x] **FE** — tách thành 2 khối LOẠI TRỪ NHAU theo `supplier_type` do BE trả:
      · `showInlandBankBlock` → khối "Tài khoản nhận tiền" 5 ô như cũ (giữ nguyên luật
        `supplier_banks`: không có chi nhánh / tỉnh-TP thì hiện ô "Địa chỉ");
      · `showForeignBankBlock` (`isSupplierParty && supplier_type == 3`) → **2 nhóm có tiêu đề**
        "NGÂN HÀNG NHẬN TIỀN" / "NGÂN HÀNG TRUNG GIAN", mỗi nhóm 1 ô chọn ngân hàng + 6 ô chỉ đọc
        (Số tài khoản · Tài khoản · Tên ngân hàng · Swift Code · IBAN Number · Địa chỉ).
      Bố cục copy y màn Phiếu chi (`BillPaymentForm.vue` :332-368): ô vẫn `col-md-3` hàng ngang,
      phân nhóm bằng MỘT dòng `col-12` mang class `.field-group-title` (đã copy CSS kèm — class nằm
      trong `<style>` riêng của màn Phiếu chi, KHÔNG có ở v2-styles). Khối "Tài khoản nhận tiền"
      cũng đổi sang cùng class cho 3 tiêu đề nhìn giống nhau → gỡ luôn `.group-label` đã chết.
      2 ô chọn CHỈ ĐỂ TRA CỨU: bind vào `requestInfo` (không nằm trong payload), ô trung gian khóa
      cứng — đúng ERP và đúng cách màn Phiếu chi làm.
- [x] **BE** `BillPaymentAuthorizationDetailResource::requestBlock()` — thêm `banks` + `mid_banks`
      (dùng lại `BillPaymentRequestDetailResource::supplierBanks()`). Thiếu 2 khóa này thì màn
      Sửa/Xem hiện 2 ô chọn RỖNG dù phiếu đã khai ngân hàng. Đường Tạo mới vốn đã có sẵn.

**Verify:** `php -l` sạch · template + script parse sạch · tinker trên **phiếu NCC nước ngoài thật
(bill 14)**: `supplier_type=3` · `banks=1` · `mid_banks=0` · `bank_id=221` · `mid_bank_id=null`
⇒ khối nước ngoài hiện đủ 2 nhóm, nhóm trung gian rỗng in `—` (ERP in `____`). ⚠️ Chưa mở trình duyệt.

### Sửa — nhánh B (loại chi 4) lệch trường so với ERP (2026-08-28)

User: *"sao tôi chọn loại chi là chi thu nhập cho nhân viên các trường thông tin khác với erp vậy"*.

Soát lại từng ô khối loại 4 của ERP (`form.blade.php` :475-629) — đúng 11 ô: Mã phiếu · Tài khoản
có · Loại chi · Hình thức thanh toán · Người nhận tiền · Loại tiền · Tỷ giá · Người đề nghị ·
Phòng ban · Lý do chi · Ngân hàng chuyển · Số TK chuyển khoản. HRM **thừa 2 ô**:

- [x] **FE** — ẩn **Tài khoản nợ** ở nhánh B (`v-if="isRequestBranch && !isContractBonusType"`).
- [x] **FE** — ẩn **Ngày hạch toán** ở nhánh B (`v-if="isRequestBranch"`); `onTypeChange()` gán
      `date_accounting = hôm nay` + `account_dept = null`, và `buildPayload()` LUÔN gửi hôm nay cho
      nhánh B (không gửi giá trị trong `form`: phiếu nháp loại 4 lập hôm trước mở ra bấm "Lưu và
      duyệt" sẽ ăn 422 `after_or_equal:today` vào một ô KHÔNG NHÌN THẤY). `account_dept` cấp phiếu
      cũng gửi null như loại 6.
- [x] **BE** `BillPaymentAuthorizationStoreRequest` — loại 4 **không bắt** `account_dept` cấp phiếu
      (nhánh `elseif`), và `prepareForValidation()` tự điền `date_accounting = hôm nay` khi thiếu.

🔶 **KHÁC ERP CÓ CHỦ Ý, cần biết**: ERP rơi vào nhánh `else` với loại 4 nên VẪN đòi `account_dept`
cấp phiếu, trong khi form ERP không có ô nào để nhập và không có JS nào gán mặc định ⇒ **bên ERP
mọi phiếu loại 4 đều 422 "Bắt buộc nhập" vào một ô vô hình — màn đó thực tế không lập được phiếu**.
Dữ liệu khớp: 0/2.574 phiếu loại 4 trên DB gộp. Bám ERP y nguyên ở đây = bê nguyên màn chết sang,
nên HRM bỏ luật đó. Loại 4 khai TK nợ theo TỪNG DÒNG (`details.*.account_dept` vẫn bắt buộc) và sổ
cái nhánh B chỉ đọc tài khoản của dòng — cột cấp phiếu không có vai trò gì, cột DB cũng `nullable`.
`date_accounting` thì ERP có mặc định hôm nay ngay trong constructor lớp JS (`BillPayment.blade.php`
:20) nên đây là port đúng, không phải chế thêm.

📌 **3 điểm lệch CHỮ, cố ý giữ theo màn Phiếu chi (đã nghiệm thu), chờ user quyết nếu muốn đổi**:
ERP "Người nhận tiền" ↔ HRM "Người nhận" · ERP "Phòng ban" ↔ HRM "Phòng ban chi" · ERP "Lý do chi"
là input 1 dòng ↔ HRM là textarea 2 dòng. Khối "Chi tiết" nhánh B đã khớp ERP sẵn (2 tab
"Chi tiết" / "Chi tiết vụ việc" nằm trong `PaymentEmployeeTable` dùng chung).

**Verify:** `php -l` sạch · template + script parse sạch · tinker dựng `rules()` thật cho 3 loại:
loại 1 → `account_dept` cấp phiếu `required` · **loại 4 → KHÔNG CÓ luật `account_dept` cấp phiếu,
`details.*.account_dept` required, `date_accounting` tự thành `2026-08-28`** · loại 6 → chỉ theo
dòng. ⚠️ Chưa mở trình duyệt.

### Checkpoint — 2026-08-28
Vừa hoàn thành: nhánh B (Chi thu nhập cho nhân viên) giờ hiện ĐÚNG 11 ô như ERP — bỏ 2 ô thừa
Tài khoản nợ + Ngày hạch toán, kèm nới luật BE để phiếu loại 4 lưu được (ERP không lưu nổi).
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payment-authorizations/create`, chọn Loại chi = "Chi thu nhập
cho nhân viên", đối chiếu 11 ô với ERP; chọn phòng ban → tick nhân viên → "Lưu và duyệt" xem có lưu
được không (đây là lần đầu màn này lập được phiếu loại 4).
Blocked: không.

### Sửa — 3 lỗi nhánh B khi hút nhân viên theo phòng ban (2026-08-28)

User: *"trường người đề nghị vẫn chưa lấy được thông tin"* · *"chọn phòng ban thiết bị ô tô 3 bên ERP
chỉ ra 1 nhân viên Nguyễn Đăng Long và có đủ số tài khoản nợ, tên tài khoản, mà HRM ra nhiều nhân
viên + chưa có stk nợ, tên tài khoản"*.

- [x] **1. Người đề nghị trống** — màn Phiếu chi điền ô này bằng `meta.creator` (tên người ĐANG
      ĐĂNG NHẬP, ERP lấy từ `DEFAULT_USER` của layout), bản UNC copy sang thiếu hẳn.
      **BE** `BillPaymentAuthorizationService::meta()` + khóa `creator` (name · department_name);
      **FE** `loadListMeta()` nhận vào `creatorInfo`, `proposerName` lùi về giá trị đó.
      ⚠️ CHỈ lùi ở nhánh B: nhánh A chưa chọn đề nghị mà hiện tên mình là nói sai ai đề nghị khoản
      chi (ERP để trống). KHÁC màn Phiếu chi — bên đó lùi cho cả 2 nhánh.
- [x] **2. Trống "Số tài khoản nợ" + "Tên tài khoản"** — ERP gán mặc định `account_dept = 116` cho
      TỪNG DÒNG nhánh B (`BillPaymentDetail.blade.php` :24-28, chỉ `mode == 'create'`), còn
      "Tên tài khoản" là giá trị SUY RA từ ô đó (`PaymentEmployeeTable::accountName()`). BE cố ý trả
      `account_dept = null` (câu truy vấn gộp nhiều tài khoản, khai bừa là ghi sai bút toán) nên mặc
      định đặt ở FE — màn Phiếu chi có sẵn hằng `ACCOUNT_DEPT_EMPLOYEE_DEFAULT`, bản UNC để `null`.
      **FE** thêm hằng `ACCOUNT_DEPT_EMPLOYEE_DEFAULT = 116` + dùng trong `fetchPaymentEmployees()`.
- [x] **3. 🐛 HÚT RA QUÁ NHIỀU NHÂN VIÊN — port thiếu 1 dòng, SỬA HÀM DÙNG CHUNG (user duyệt
      2026-08-28: "cứ làm như bên erp, đúng cả 2 màn là được")**
      Nút "Lấy nhân viên" của ERP gửi kèm `get_employee = 1`, tham số đó bật đúng một điều kiện
      trong `AccountDetail::getDataAdPaymentEmployee()` (:3977):
      `if ($request->get_employee) { $query->whereIn('account_id', [305, 116]); }`
      — tức chỉ cộng bút toán trên **2 tài khoản phải trả người lao động** (116 = `33481` Phải trả
      người lao động khác ngắn hạn · 305 = `33483` Phải trả NVKD - Chi phí thị trường).
      HRM cộng trên MỌI tài khoản.
      **BE** `PaymentEmployeeLookupService::forDepartment()` + hằng `PAYABLE_ACCOUNT_IDS`.
      ⚠️ 2 nhánh LOẠI TRỪ NHAU: gọi kèm 1 tài khoản cụ thể thì chỉ lọc theo tài khoản đó (ERP đi
      đường `BillPaymentDetail::fetchData()`, gửi `account_id` mà KHÔNG gửi `get_employee`).
      ⚠️ Ảnh hưởng CẢ màn **Phiếu chi** (đã nghiệm thu) — cùng service, cùng thiếu, ERP cũng dùng
      chung 1 hàm JS cho 2 màn nên đây là đưa cả 2 về đúng ERP.

**Đo thật trước/sau** trên `PHÒNG THIẾT BỊ Ô TÔ 3` (department id 44, công ty 1):
`18 nhân viên` -> **`1 nhân viên — Nguyễn Đăng Long`** (đúng cái user thấy bên ERP). Chạy lại chính
`PaymentEmployeeLookupService::forDepartment(44)` sau khi đăng nhập bằng tài khoản công ty 1: trả
đúng 1 dòng, `payment_money_request = -4.537.037` (số dư âm -> "Số tiền chi" điền sẵn 0, đúng ERP).

**Verify:** `php -l` sạch 3 file BE · template + script parse sạch · `meta()` trả đủ `creator` +
`work_tthhd`. ⚠️ Chưa mở trình duyệt.

### Checkpoint — 2026-08-28
Vừa hoàn thành: 3 lỗi nhánh B (Người đề nghị trống · thiếu TK nợ mặc định 116 · hút thừa nhân viên
do port thiếu lọc `account_id IN (305,116)`).
Đang làm dở: không.
Bước tiếp theo: user mở màn Ủy nhiệm chi → Loại chi "Chi thu nhập cho nhân viên" → chọn PHÒNG THIẾT
BỊ Ô TÔ 3, xác nhận ra đúng 1 dòng Nguyễn Đăng Long kèm TK nợ 33481 + tên tài khoản, ô Người đề nghị
có tên mình. **Kiểm tra thêm màn Phiếu chi loại 4** vì dùng chung service vừa sửa.
Blocked: không.

### Sửa — cảnh báo khi Số tiền duyệt chi vượt Số tiền đề nghị chi (2026-08-28)

User: *"chỗ số tiền duyệt chi hiện tại đang không cho nhập số lớn hơn số tiền đề nghị chi, nếu người
dùng nhập lớn hơn thì thêm cảnh báo xuống bên dưới đó cho người dùng biết"*.

Hiện trạng: ô bị kẹp CỨNG ở 2 lớp — prop `:max` của `V2BaseCurrencyInput` (kẹp ngay lúc gõ,
`:113-124`) và `clampApprove()` (kẹp sau mỗi lần nhập). Giống hệt ERP: setter
`payment_money_approve` của `BillPaymentDetail.blade.php` :129-131 gán thẳng
`_payment_money_approve = _payment_money_request` khi vượt. Số người dùng gõ biến mất không lời giải
thích.

- [x] **FE** bỏ prop `:max`; `clampApprove()` chỉ còn chặn số ÂM (âm là vô nghĩa với phiếu chi).
- [x] **FE** thêm `isApproveOverRequest(detail)` + dòng cảnh báo VÀNG ngay dưới ô:
      *"Lớn hơn số tiền đề nghị chi (<số>)"*. Chỉ so khi số đề nghị > 0 (đề nghị 0 đồng thì không có
      mốc để so, tránh dựng cảnh báo cho mọi dòng).
- [x] **FE** class `.field-warning` khai màu tại chỗ (#b45309). ⚠️ KHÔNG dùng `.text-warning` của
      Bootstrap — SCSS toàn cục hrm-client ghi đè nhóm class màu (cùng lý do `.text-muted` bị ép về
      đỏ #dc3545).
- [x] **BE** không đụng gì — `BillPaymentAuthorizationStoreRequest` vốn KHÔNG có luật `max` cho
      `details.*.payment_money_approve` (chỉ `required|numeric|min:1` khi duyệt).

⚠️ **ĐÃ NÂNG THÀNH CHẶN ngay trong ngày** — xem mục kế tiếp. Bản "chỉ cảnh báo vàng" không còn.

📌 Ô **"Số tiền chi"** của nhánh B (bảng nhân viên) VẪN kẹp cứng — nằm trong component DÙNG CHUNG
`PaymentEmployeeTable::clampToLimit()` (`bill-payments/components/`), đụng vào là đổi cả màn Phiếu
chi. Chưa sửa, chờ user yêu cầu.

**Verify:** template + script parse sạch · grep xác nhận không còn `:max` trên ô duyệt chi.
⚠️ Chưa mở trình duyệt.

### Sửa (tiếp) — nâng cảnh báo thành CHẶN LƯU (2026-08-28)

User: *"cảnh báo và chặn không cho lưu nhé"*.

- [x] **FE** dòng chữ vàng `.field-warning` -> **lỗi đỏ chuẩn** qua `V2BaseError` (`approveErrorText()`):
      *"Không được lớn hơn số tiền đề nghị chi (<số>)"*, ô cũng `:invalid` -> viền đỏ. Lỗi tại chỗ
      này ĐỨNG TRƯỚC lỗi 422 của lần lưu trước. Class `.field-warning` gỡ khỏi `<style>` (hết dùng).
- [x] **FE** `validateApproveAmounts()` chặn ngay đầu `save()` — áp cho **CẢ "Lưu nháp" lẫn "Lưu và
      duyệt"**, toast nói rõ *dòng số mấy* đang vượt. Đặt TRƯỚC `validateForm()` để lưu nháp (vốn bỏ
      qua validate FE) vẫn bị chặn.
- [x] **BE** `BillPaymentAuthorizationStoreRequest` + luật closure `approveNotOverRequestRule()` cho
      `details.*.payment_money_approve`, áp cho MỌI loại nhánh A (1·2·3·6·10·12) và cả đường nháp.
      ⚠️ Viết bằng **closure, KHÔNG dùng `lte:details.*.payment_money_request`**: luật `lte` của
      Laravel ném `InvalidArgumentException` (**500**, không phải 422) khi trường đem so vắng mặt
      trong payload — mà `payment_money_request` là ô CHỈ ĐỌC do FE kéo từ phiếu đề nghị. Vế đem so
      thiếu / không phải số / <= 0 thì bỏ qua luật, không bịa mốc.
      Chỉ THÊM closure vào luật sẵn có, không đụng `required`/`numeric`/`min` của loại 1·2·3.

**Verify (tinker, dựng `Validator` thật từ FormRequest):**
`200 > 100` -> *"Không được lớn hơn số tiền đề nghị chi"* · `100 = 100` -> không lỗi ·
thiếu `payment_money_request` -> không lỗi (KHÔNG nổ 500) · **loại 6 vượt** -> có lỗi ·
**lưu nháp mà vượt** -> có lỗi. `php -l` sạch · template + script parse sạch · grep xác nhận
`.field-warning` đã xoá hết. ⚠️ Chưa mở trình duyệt.


## Phase L — Lịch sử thay đổi phiếu Ủy nhiệm chi (user yêu cầu 2026-09-03)

User: *"xem màn phiếu ủy nhiệm chi xem có lịch sử thay đổi chưa, chưa có thì bổ sung"*.

**Kiểm tra hiện trạng: CHƯA CÓ GÌ.** `bill_payment_authorizations` không nằm trong whitelist
`CatalogHistoryService::TABLES`; BE chỉ gọi `BillPaymentRequest::logStatusHistory()` — tức ghi lịch
sử cho MÀN ĐỀ NGHỊ THANH TOÁN, không phải cho chính UNC; FE không có popup lẫn khối Lịch sử.

Phạm vi: cùng mức đã chốt ở Phiếu thu / Phiếu chi (tạo · sửa · bảng chi tiết theo TỪNG DÒNG ·
đổi trạng thái dòng riêng · xóa). Không migration — dùng bảng chung `catalog_histories`.

### Khác 2 màn trước (đọc trước khi code)

- **UNC KHÔNG có Gửi duyệt / Duyệt / Hủy** (RULING U-UNC-6): chỉ "Lưu" (status 1) và "Lưu và duyệt"
  (status 3, ghi sổ cái ngay). Status 2/4 là TRẠNG THÁI CHẾT. ⇒ dòng `change_status` chỉ sinh ra ở
  `update()` khi phiếu nháp được bấm "Lưu và duyệt"; `store()` với status 3 đã nằm trong log `create`.
- Bảng **KHÔNG có 2 cột tổng** (`sum_payment_money_*`) như Phiếu chi ⇒ không theo dõi cột tổng.
- Bảng **CÓ 6 cột riêng**: `account_dept`, `bank_from(_name)`, `account_from(_name/_number)`,
  `source_money`, `note` → phải khai vào whitelist.
- Dòng chi tiết **KHÔNG có** `customer_id` / `supplier_id` (khác Phiếu chi): đối tượng nhận diện là
  `contract_code` (nhánh A) hoặc `employee_code/_name` (nhánh B), kèm số TK + ngân hàng nhận.
- Nhánh B chỉ **5** khoản thu nhập (không có `other_cost` như Phiếu chi).

### BE

- [x] `CatalogHistoryService::TABLES` — khai `bill_payment_authorizations` + nhãn cột tiếng Việt
      + 2 khoá ẢO dạng BẢNG (`details_rows`, `export_request_rows`). KHÔNG khai `status`
      (đổi trạng thái là dòng riêng — skill §3a)
- [x] `Modules/Finance/Services/BillPaymentAuthorizationHistoryService.php` — khuôn
      `BillPaymentHistoryService`, có `forFullLog()` lọc khoá rỗng/null trước khi ghi log `delete`
- [x] `BillPaymentAuthorizationWriteService::store()` → `logCreate()` (SAU `approveAndPostToLedger()`
      vì bước đó còn ghi `approved_id` + tính lại số duyệt chi)
- [x] `...::update()` → snapshot ở ĐẦU transaction; sau khi lưu ghi `logUpdate()` +
      `logStatusChanged()` (2 dòng riêng khi bấm "Lưu và duyệt" trên phiếu nháp)
- [x] `...::destroy()` → snapshot TRƯỚC `deleteDetails()`, `logDelete()`
- [x] Mọi lời gọi bọc try/catch + `Log::error` — lỗi log không được làm rớt nghiệp vụ

### FE — ĐỦ 2 NƠI (§5.1)

- [x] `pages/finance/bill-payment-authorizations/index.vue` — mục `Lịch sử` + `CatalogHistoryModal`
- [x] `pages/finance/bill-payment-authorizations/_id/index.vue` — khối `SystemInfoSection` trong thân trang

### Verify

- [x] tinker trong transaction rồi ROLLBACK: tạo nháp → sửa → "Lưu và duyệt" → xóa
- [x] Compile FE + Playwright 2 màn, dọn sạch dữ liệu gieo

### Kiểm chứng đã chạy

**Luồng đầy đủ** (tinker, toàn bộ trong transaction rồi ROLLBACK — UNC không gửi notification nên
không phải thay service nào): tạo nháp → 1 dòng `create` · sửa người nhận + ghi chú + số chi dòng 1
+ thêm dòng 2 → **1 dòng** `update` đúng 2 trường phẳng + 1 dòng thêm + 1 dòng sửa ĐÚNG CỘT · lưu
lại y nguyên → **không sinh log rác** · "Lưu và duyệt" (1 → 3) → **2 dòng** (`update` nội dung +
`change_status` "Đang tạo → Đã hạch toán"), đề nghị nguồn sang status 8 đúng ERP · xóa → snapshot
đầy đủ + 2 dòng chi tiết đã xóa. Sau rollback: 0 dòng log, 0 phiếu thừa, đề nghị 4192 vẫn status 6.

**Trình duyệt (Playwright)**: gieo 3 dòng log cho phiếu THẬT `TPE.UNC0826.00001` (id 2606) rồi xem
giao diện, xong xoá đúng 3 dòng đó (id 290-292); phiếu 2606 giữ `updated_at = 2026-08-27 14:32:05`,
3 dòng chi tiết.
- Màn danh sách: phiếu đã hạch toán chỉ còn 1 hành động nên nút "Lịch sử" hiện thẳng ở cột Hành động.
- Popup: timeline mới → cũ, cũ ĐỎ / mới XANH, nhóm "Bảng chi tiết thêm mới / sửa thông tin",
  dòng "Thay đổi trạng thái: Đang tạo → Đã hạch toán".
- Màn chi tiết: khối "Lịch sử" badge `3` trong THÂN TRANG; `V2Footer` chỉ có "Quay lại" (phiếu đã
  hạch toán không sửa/xóa được — đúng RULING U-UNC-6). Form phía trên không vỡ vì thêm slot.
- Console: **0 lỗi** ở cả 2 màn.

`php -l` sạch 3 file BE · compile FE (vue-template-compiler + babel) sạch 3 file.

### Sửa kèm — áp cho cả màn Phiếu chi

`payment_department_id` là cột NOT NULL không có default nên luồng ghi điền **0** (dữ liệu thật ERP
cũng 0 ở phần lớn phiếu) ⇒ log in ra `Phòng ban được chi: 0`. Nay 0 được coi là "chưa chọn" (trả
null, bị `forFullLog()` lọc) ở CẢ `BillPaymentAuthorizationHistoryService` lẫn
`BillPaymentHistoryService`.

### Checkpoint — 2026-09-03
Vừa hoàn thành: lịch sử thay đổi màn Ủy nhiệm chi — từ CHƯA CÓ GÌ lên đầy đủ, BE (whitelist +
service ghi log + 4 điểm nối) và FE (popup ở danh sách + khối Lịch sử ở chi tiết).
Đang làm dở: không.
Bước tiếp theo: user nghiệm thu. Còn tồn: bẫy mảng rỗng trong `CatalogHistoryService::changesOf()`
(hàm DÙNG CHUNG) vẫn CHƯA sửa — đã trình bày phương án, chờ user chốt.
Blocked: không.
