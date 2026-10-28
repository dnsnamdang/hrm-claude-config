# Phase 11 — Bổ sung các trường FirmContract còn thiếu trên màn HĐ HRM

> Spec chi tiết. Feature `hop-dong` (có trước gộp DB) → tài liệu giữ ở `.plans/hop-dong/`.
> Nhánh: `gop_db` (cả hrm-api & hrm-client). Ngày: 2026-10-14. Phụ trách: @dangquang.

## 1. Bối cảnh & phạm vi

User rà màn Hợp đồng HRM (`/assign/contracts/_id/edit`) so với **HĐ hãng FirmContract ERP**
(được coi là chuẩn) và liệt kê các trường còn thiếu. Sau brainstorming đã **chốt làm 6 mục**, và
**để lại 2 mục** sang phase sau:

**LÀM (Phase 11):**
1. Bảng giá
2. Bên B (khách hàng): (2a) phân biệt cá nhân/tổ chức + khối Liên hệ + bỏ bắt buộc CCCD cho tổ chức;
   (2b) đổi nhãn "Số CCCD/CMND" → hiển thị CCCD (cá nhân) hoặc MST (tổ chức);
   (2c) chọn tài khoản ngân hàng khách qua dropdown
5. Địa chỉ giao hàng
6. Lắp đặt

**ĐỂ LẠI (không làm phase này):**
3. Kế hoạch giao hàng + tiến độ thanh toán theo Redmine #11252
4. Điều kiện tính thời gian thực hiện hợp đồng (HRM **đã có** đầy đủ trong khối "Thông tin chung",
   ERP không có — không đụng)

## 2. Quyết định đã chốt (với user)

| # | Quyết định | Lý do |
|---|-----------|-------|
| D1 | **Bảng giá = read-only** (chỉ hiển thị, không cho sửa) | HĐ HRM dựng từ 1 báo giá cụ thể; dòng hàng đã đóng băng giá theo `price_type_id` của báo giá (`ContractService:118`, `snapshotProductMasterPrice`). Cho đổi bảng giá sẽ phá giá đã đóng băng. |
| D2 | Phân biệt cá nhân/tổ chức qua `customers.customer_type` (==1 cá nhân, >1 tổ chức) | Dữ liệu thật: type 1 = 30.762 (cá nhân), type 2/3/5 = tổ chức. |
| D3 | **Port đầy đủ như ERP**: cả dropdown Người đại diện (bắt buộc với tổ chức) lẫn khối Liên hệ read-only | User chốt "đầy đủ". |
| D4 | TK ngân hàng Bên B làm **y hệt pattern Bên A (Phase 10)**: FK `customer_account_id` + snapshot 3 cột text | Nhất quán, đã có khuôn. |
| D5 | Địa chỉ giao hàng = ô **read-only** nguồn `customer_address` (đã snapshot) | ERP cũng để disabled; báo giá HRM không có cột delivery_place riêng nên dùng địa chỉ KH (ERP cũng fallback về customer_address). |
| D6 | **Không thêm cột `deputy_role` mới** — tái dùng cột `representative_role` đã có để snapshot chức vụ người đại diện | Tránh cột trùng nghĩa; `representative_name`/`representative_role` đã tồn tại và đang được snapshot ở ContractService:142-143/351-352. Cột mới của mục Người đại diện chỉ là `customer_deputy_id` (để reselect dropdown lúc Sửa). |

## 3. Hiện trạng code liên quan

- Màn FE: `hrm-client/pages/assign/contracts/_id/edit.vue` — **màn CŨ**, pattern local:
  `touched`/`formError`/`validateForm()` thủ công, grid `.fld-grid`/`.fld`, card tự dựng
  `<div class="c-section"><div class="section-header">`. **KHÔNG retrofit** sang V2BaseFormSection /
  vee-validate. Dropdown dùng `V2BaseSelect` (đã dùng cho Bên A ở Phase 10, dòng 96).
  - Bên B hiện ở template dòng **102-121**: đã có ô free-text `representative_name` (107),
    `representative_role` (108), `customer_id_card_number` required (109-113), ngày/nơi cấp (114-115),
    3 ô text TK `customer_bank_account_number/name/branch` (116-118).
  - `data()` form khởi tạo quanh dòng **489-497**; `validateForm()` dòng **1140**
    (dòng 1148 bắt buộc company_account_id, 1149 bắt buộc customer_id_card_number);
    `buildPayload()` dòng **1199**; edit set form từ detail quanh **1086-1094**.
- BE Service: `Modules/Assign/Services/ContractService.php`
  - `store()`: snapshot khách từ `$quotation` (dòng **103-118**: customer_id, customer_name,
    customer_tax_code, customer_address, customer_contact_name, customer_contact_phone, price_type_id);
    trường riêng HĐ từ `$data` (dòng **142-153**). Bên A company_account snapshot dòng **94-97/153**.
    ⚠️ Store **không** snapshot `customer_type`, `customer_email`.
  - `update()`: **chỉ** cập nhật trường riêng HĐ (dòng **334-362**, comment 315 "KHÔNG đụng snapshot
    báo giá"). Không đụng customer_* snapshot.
- BE Controller: `Modules/Assign/Http/Controllers/Api/V1/ContractController.php` — có `companyAccounts()`
  (Phase 10). Route: `Modules/Assign/Routes/api.php` — `GET /assign/contracts/company-accounts`.
- Resource: `Modules/Assign/Transformers/DetailContractResource.php` — trả `company_account_id`,
  `price_type_id` (Phase 10 + sẵn có).
- Model: `Modules/Assign/Entities/Contract/Contract.php` — có `company_account()` (Phase 10).
- Bảng nguồn (DB gộp `erp_hrm_check`, ưu tiên bản ERP):
  - `customers`: `id, customer_type, tax_code, identity_card_number, grant_date, grant_location, email?`
  - `customer_deputies`: `id, name, role, customer_id` (người đại diện / người ký)
  - `customer_contacts`: `id, fullname, phones, email, identity_card_number, role, customer_id` (người liên hệ)
  - `customer_has_bank_accounts`: `id, customer_id, account_number, account_name, bank_name, bank_branch, bank_province_id`
  - `price_types`: `id, name, order`

## 4. DB — migration thêm cột vào `hrm_contracts`

File: `Modules/Assign/Database/Migrations/2026_10_14_000002_add_firm_fields_to_hrm_contracts_table.php`
(guard `Schema::hasColumn` từng cột — nhiều người cùng chạy migration trên 1 DB gộp).

| Cột | Kiểu | Null | Ý nghĩa |
|---|---|---|---|
| `customer_type` | `unsignedTinyInteger` | yes | Snapshot `customers.customer_type` (1=cá nhân, >1=tổ chức) |
| `customer_deputy_id` | `unsignedBigInteger` | yes | FK logic `customer_deputies.id` (người đại diện bên B) |
| `customer_account_id` | `unsignedBigInteger` | yes | FK logic `customer_has_bank_accounts.id` (TK bên B) |
| `need_install` | `unsignedTinyInteger` | yes | Lắp đặt: 1=Có, 0=Không |

Tái dùng cột đã có (không tạo mới): `customer_tax_code`, `customer_address`, `customer_contact_name`,
`customer_contact_phone`, `customer_email`, `representative_name`, `representative_role`,
`customer_id_card_number/date/place`, `customer_bank_account_number/name/branch`, `price_type_id`.

KHÔNG dùng FK ràng buộc cứng (quy ước DB gộp). KHÔNG dùng SoftDeletes. PHPDoc trên `up()`/`down()`.

## 5. BE

### 5.1 Model `Contract`
Thêm 2 quan hệ belongsTo (bám khuôn `company_account()` Phase 10):
```php
public function customerDeputy()  { return $this->belongsTo(\Modules\Assign\Entities\...\CustomerDeputy::class, 'customer_deputy_id'); }
public function customerAccount() { return $this->belongsTo(\Modules\...\CustomerHasBankAccount::class, 'customer_account_id'); }
```
(Tra đúng namespace model `CustomerDeputy` / `CustomerHasBankAccount` trong codebase trước khi khai;
nếu chưa có model thì query qua `DB::table()` trong Service cho gọn — quyết định lúc code, không
tạo model thừa.)

### 5.2 Endpoint mới (ContractController + route) — bám khuôn `companyAccounts()`
- `GET /assign/contracts/customer-deputies?customer_id=` →
  `[{ id, name, role }]` từ `customer_deputies` theo `customer_id` (sắp theo name).
- `GET /assign/contracts/customer-bank-accounts?customer_id=` →
  `[{ id, account_number, account_name, bank_name, bank_branch }]` từ `customer_has_bank_accounts`
  theo `customer_id`. Nhãn option FE dựng: `<account_number> - <bank_name> chi nhánh <bank_branch> - <account_name>`.
- Khối Liên hệ **không cần endpoint** — render thẳng snapshot `customer_contact_*` + `customer_email`.
- Gắn route trong nhóm `assign/contracts` cạnh `company-accounts`. Chỉ đọc → không cần middleware quyền.

### 5.3 `ContractService::store()`
- Thêm vào mảng snapshot khách (sau dòng 118):
  - `customer_type` = `Customer::find($quotation->customer_id)?->customer_type` (PHP7.4: không `?->`,
    dùng biến tạm + null check). Cho cả tổ chức lẫn cá nhân.
  - `customer_email` = email người liên hệ: ưu tiên `customers.email`; nếu rỗng thử
    `customer_contacts` đầu tiên theo customer_id. Best-effort (có thể rỗng).
- Thêm vào mảng trường riêng HĐ (quanh 142-153):
  - `customer_deputy_id` = `$data['customer_deputy_id'] ?? null`.
  - Nếu có `customer_deputy_id` → set `representative_name` = deputy.name, `representative_role`
    = deputy.role (snapshot từ `CustomerDeputy::find()`), **ghi đè** giá trị free-text gửi lên
    (nguồn chuẩn là deputy đã chọn). Nếu không có deputy (cá nhân) → giữ `representative_name/role`
    từ `$data` như hiện tại.
  - TK bên B: `$customerAccount = CustomerHasBankAccount::find($data['customer_account_id'])`;
    set `customer_account_id` + snapshot `customer_bank_account_number` = account.account_number,
    `customer_bank_name` = account.bank_name, `customer_bank_branch` = account.bank_branch
    (fallback `$data` nếu account rỗng — y hệt Bên A Phase 10, dòng 94-97/153).
  - `need_install` = `$data['need_install'] ?? null`.
  - Trường định danh: nếu **cá nhân** (customer_type==1) snapshot `customer_id_card_number/date/place`
    từ `$data`; nếu **tổ chức** thì các cột id_card để null (MST đã nằm ở `customer_tax_code` snapshot
    từ quotation). FE tổ chức không gửi id_card.

### 5.4 `ContractService::update()`
- Lặp lại logic set `customer_deputy_id` + snapshot representative_*, `customer_account_id` + snapshot
  bank, `need_install`, định danh theo customer_type (quanh 351-362).
- `customer_type` đã snapshot lúc store (khách không đổi giữa các lần sửa) → update không cần set lại.
  Nhưng để an toàn với HĐ cũ chưa có snapshot: nếu `contract->customer_type` null thì set lại từ
  `customers` theo `contract->customer_id`.

### 5.5 Validation — `ContractStoreRequest` / `ContractUpdateRequest`
Xác định tổ chức ở BE: tra `customers.customer_type` theo `customer_id` của HĐ/báo giá (dùng closure
`required_if`/`sometimes` + `withValidator`, hoặc tính `$isOrg` trong `rules()` từ request).
- `customer_deputy_id`: **required khi là tổ chức** + chính thức; `nullable` khi nháp hoặc cá nhân.
  Rule `exists:customer_deputies,id` khi có giá trị.
- `customer_account_id`: `nullable` (+ `exists:customer_has_bank_accounts,id` khi có).
- `need_install`: `required|in:0,1` khi chính thức; `nullable` khi nháp.
- `customer_id_card_number`: `required` khi **cá nhân** + chính thức; **bỏ required** khi tổ chức
  (sửa đúng lỗi báo đỏ trên screenshot). `nullable` khi nháp.
- KHÔNG khai `messages()` cho rule phổ biến (lang file đã có — CLAUDE.md). Câu nghiệp vụ riêng mới viết tay.
- BE vẫn rethrow `ValidationException` (không catch chung).

### 5.6 `DetailContractResource`
Trả thêm: `customer_type`, `customer_deputy_id`, `need_install`, `price_type_name`
(tên từ `price_types` theo `price_type_id`), `customer_email`, `customer_contact_name`,
`customer_contact_phone`, `customer_address`.
- `customer_type`: trả snapshot `customer_type` ?: **suy live** từ quan hệ customer (cho HĐ cũ chưa
  snapshot) → FE luôn rẽ nhánh được.

## 6. FE — `edit.vue`

Bám pattern local (`touched`/`formError`/`validateForm`, `.fld-grid`, `V2BaseSelect`). Số quốc tế
(`,` nghìn `.` thập phân — không áp cho field này vì không có số tiền mới). Đỏ chỉ cho lỗi validate.
KHÔNG tự sửa giá trị user nhập.

### 6.1 Computed rẽ nhánh
```js
isOrganization() { return Number(this.form.customer_type || this.contract.customer_type) > 1 }
```

### 6.2 Khối "Thông tin chung" — Bảng giá (D1)
Thêm 1 `.fld` (read-only): nhãn "Bảng giá", hiển thị `contract.price_type_name` qua `V2BaseSelect`
disabled (hoặc `.ro-value` như ô "Tên khách hàng" dòng 106 — chọn kiểu read-only đang dùng trên màn).
Không nằm trong payload (không sửa).

### 6.3 Khối Bên B (template 102-121) — rẽ theo `isOrganization`
- **Tên khách hàng**: giữ read-only (dòng 106).
- **Người đại diện** (D3):
  - Tổ chức → `V2BaseSelect` "Người đại diện *" (`form.customer_deputy_id`, options từ endpoint
    customer-deputies), `@change` → đổ `representative_name` = deputy.name, `representative_role`
    = deputy.role. Ô "Chức vụ đại diện" disabled (tự fill từ deputy).
  - Cá nhân → giữ nguyên 2 ô free-text `representative_name`/`representative_role` như hiện tại.
- **Trường định danh (2b)**: 1 ô, nhãn + nguồn đổi theo loại:
  - Cá nhân: nhãn "CCCD/CMND *", `V2BaseInput` `form.customer_id_card_number` (required) +
    ô "Ngày cấp" + "Nơi cấp" (giữ như 110-115).
  - Tổ chức: nhãn "Mã số thuế", hiển thị `form.customer_tax_code` read-only (disabled),
    **không** required, **ẩn** ngày/nơi cấp.
- **Khối Liên hệ** (D3, chỉ tổ chức): read-only — Người liên hệ (`customer_contact_name`),
  Điện thoại (`customer_contact_phone`), Email (`customer_email`). Dùng `.ro-value` hoặc
  `V2BaseInput disabled`. Chữ xám, không đỏ.
- **TK ngân hàng Bên B (2c, D4)**: thay 3 ô text (116-118) → 1 `V2BaseSelect` "Số tài khoản"
  (`form.customer_account_id`, options endpoint customer-bank-accounts); `@change` đổ snapshot
  `customer_bank_account_number/name/branch`; hiển thị tên TK/NH/chi nhánh disabled (tự fill).
  Nếu khách chỉ 1 TK → tự chọn (như ERP). Reselect đúng khi Sửa.

### 6.4 Khối mới — Địa chỉ giao hàng + Lắp đặt (mục 5, 6)
Đặt sau khối Bên B hoặc trong "Thông tin chung" (chọn vị trí hợp lý theo layout, bám card `c-section`):
- **Địa chỉ giao hàng** (D5): `.ro-value` / `V2BaseInput` disabled từ `form.customer_address`.
- **Lắp đặt** (mục 6): radio "Có"/"Không" (`form.need_install`, 1/0), **bắt buộc**. Dùng
  `V2BaseRadio` nếu màn đã dùng, hoặc 2 radio theo pattern local. `field-error` + `V2BaseError`.

### 6.5 `data()` / `validateForm()` / `buildPayload()` / edit-set
- `data()` form thêm: `customer_type`, `customer_deputy_id`, `customer_account_id`, `need_install`,
  `price_type_name` (hiển thị), `customer_contact_name/phone`, `customer_email`, `customer_tax_code`,
  `customer_address`.
- `validateForm()`:
  - Tổ chức: bắt buộc `customer_deputy_id` (bỏ bắt buộc `customer_id_card_number`); cá nhân: giữ
    bắt buộc `customer_id_card_number` (dòng 1149).
  - Bắt buộc `need_install` (phải là 0 hoặc 1).
  - Giữ bắt buộc `company_account_id` (Phase 10).
- `buildPayload()` thêm: `customer_deputy_id`, `customer_account_id`, `need_install`, và (cá nhân)
  `customer_id_card_*`; (tổ chức) không gửi id_card. `price_type_id` không gửi (read-only).
- Edit set form từ detail (1086-1094): set `customer_type`, `customer_deputy_id`,
  `customer_account_id`, `need_install`, các field hiển thị liên hệ/MST/địa chỉ.
- Fetch options ở `mounted`/sau khi có `customer_id`: gọi customer-deputies + customer-bank-accounts
  (chỉ khi có customer_id). Tổ chức mới cần deputies (có thể lazy, nhưng gọi sẵn cho đơn giản 1 lần).
- Sau lưu: `markFormSaved()` + `$router.push('/assign/contracts')` (giữ như hiện tại).

## 7. Edge cases
- HĐ cũ (2 dòng test) chưa có `customer_type` snapshot → Resource suy live từ customer → FE rẽ đúng.
- Khách tổ chức không có bản ghi `customer_deputies` → dropdown rỗng → validate chặn "required" khi
  chính thức (user phải khai người đại diện ở danh mục KH trước). Ghi chú: giống ERP.
- Khách chưa có TK trong `customer_has_bank_accounts` → dropdown rỗng, `customer_account_id` nullable
  → không chặn (giống Bên A nullable? Bên A đang required; Bên B để nullable theo D4).
- Đổi loại định danh khi rẽ nhánh: ẩn/hiện ô theo `isOrganization` → **xoá lỗi** field ẩn khi đổi
  (tránh lỗi bám ô không hiển thị). `customer_id_card_number` khi tổ chức → không gửi, không validate.
- `need_install` chưa chọn ở HĐ cũ (null) → khi Sửa bắt buộc chọn trước khi lưu chính thức.

## 8. Kiểm thử (Playwright MCP — bắt buộc trước khi báo xong)
Mở `http://127.0.0.1:3000` (KHÔNG localhost). Sau khi xong: `rm -rf /Users/nguyentrancu/DEV/code/ERP-HRM/.playwright-mcp`.
1. HĐ khách **cá nhân**: ô định danh = "CCCD/CMND *" (required), có ngày/nơi cấp; không hiện khối Liên hệ,
   không hiện dropdown Người đại diện.
2. HĐ khách **tổ chức**: ô định danh = "Mã số thuế" (read-only, KHÔNG báo đỏ khi trống); hiện dropdown
   Người đại diện (bắt buộc) + chức vụ tự fill; hiện khối Liên hệ read-only.
3. Bảng giá: ô read-only hiện đúng tên price_type, không sửa được.
4. TK ngân hàng Bên B: dropdown nạp danh sách, chọn → tự fill tên TK/NH/chi nhánh; lưu OK; Sửa reselect đúng.
5. Địa chỉ giao hàng: hiện đúng địa chỉ KH, read-only.
6. Lắp đặt: radio Có/Không, bắt buộc; bấm Trình duyệt khi chưa chọn → báo đỏ.
7. Lưu cả 2 loại khách → không mất dữ liệu; mở lại Sửa thấy đúng giá trị đã lưu.
8. `php -l` sạch các file BE sửa.

## 9. Ngoài phạm vi (ghi rõ để không nhầm)
- Mục 3 (kế hoạch giao hàng + tiến độ thanh toán #11252) và mục 4 (điều kiện thời gian thực hiện HĐ)
  — để phase sau.
- Không đụng logic giá dòng hàng (đã đóng băng từ báo giá).
- Không thêm quyền mới (màn đã dùng gate sẵn có).
