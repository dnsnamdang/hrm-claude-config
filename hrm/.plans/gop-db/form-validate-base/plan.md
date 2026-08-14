# Plan — Validate realtime trên base V2Base\*

> @khoipv · nhánh `gop_db` · repo `hrm-client`
> Design: `./design.md` · Spec: `docs/superpowers/specs/gop-db/2026-08-14-form-validate-base-design.md`

## Phase 1 — Mixin dùng chung ✅

- [x] T1.1 `utils/mixins/v2ValidateMixin.js` — `$_veeValidate.name()/.value()` + prop `invalid`
- [x] T1.2 `utils/mixins/formValidateMixin.js` — `formErrors`, `fieldError()`, `hasFieldError()`,
      `validateForm()`, `applyServerErrors()`, `clearFieldError()`

## Phase 2 — 7 base component nhập liệu ✅

- [x] T2.1 `V2BaseInput` · T2.2 `V2BaseTextarea` · T2.3 `V2BaseSelect` · T2.4 `V2BaseSelectInModal`
      · T2.5 `V2BaseSelectRemote` · T2.6 `V2BaseDatePicker` · T2.7 `V2BaseCurrencyInput`

## Phase 3 — Màn mẫu Gói bảo dưỡng ✅

- [x] T3.1–T3.6 (xem lịch sử checkpoint 2026-08-14 bên dưới)
- [x] T3.7 Rút gọn `data-vv-name` → `name`, bỏ `data-vv-as` (không đổi câu lỗi nào ở project này)

## Phase 4 — Kiểm chứng đợt 1 ✅

- [x] T4.1 Parse 10/10 file · T4.2 realtime ô Tên · T4.3 BE 422 map đúng ô · T4.4 smoke `/assign/contracts`

---

## Phase 5 — Nhân ra 15 màn gop-db còn lại

**Nguyên tắc (user chốt 2026-08-14):**
- FE chỉ `required` ô **Tên**. Các `required` khác để BE trả 422.
- Rule **định dạng** của BE thì bê nguyên sang FE: `max:255`, `email`, `numeric`, khoảng số, số chữ số…
- Được **THÊM** rule mới vào `plugins/vee-validate.js`, **KHÔNG sửa** rule cũ (~90 màn đang dùng).
- `/assign/customers` (`CustomerForm.vue`) **tạm bỏ** — form lớn nhất, dùng chung 5 màn, tách đợt sau.

**Message FE = message BE (user chốt 2026-08-14):** câu lỗi FE viết đúng nguyên văn message BE trả về
— lấy từ `FormRequest::messages()`, thiếu thì lấy `hrm-api/resources/lang/vi/validation.php`.
Riêng `max:255` giữ rule + câu cũ `Vui lòng nhập tối đa 255 ký tự.` (user chốt) — trùng luôn
`max.string` trong lang vi của BE.

### 5.0 Rule mới cho plugin (thuần thêm) ✅

- [x] T5.0 `plugins/vee-validate.js`: thêm `number_only`, `min_value`, `max_value_decimal`,
      `digits_between`, `number_vn`, `positive_vn`, `max_value_vn` + dictionary `custom` cho 3 trường
      có câu chữ riêng (`exchange_rate`, `identify_number`, `coefficient_cost_price_service`).
      **Không đụng** `min` / `max` / `max_value` cũ.
      ⚠️ Ô Tỷ giá nhập theo định dạng VN (`26.520,00`) nên phải có bộ rule `*_vn` quy đổi giống
      `prepareForValidation()` của BE — dùng `number_only` sẽ báo sai.

### 5.1 Finance (8 màn) ✅

| # | Màn | File FE sửa | Rule FE sau khi sửa |
| --- | --- | --- | --- |
| T5.1 ✅ | Tài khoản | `pages/finance/accounts/components/AccountFormComponent.vue` | `identify_number` `digits_between:3,15`; `name` `required\|max:255`. Bỏ hàm `validateIdentifyNumber()` tự viết |
| T5.2 ✅ | Loại tài khoản | `components/modal/finance/type-account-modal.vue` | `name` `required\|max:255`; `code`/`note` `max:255` |
| T5.3 ✅ | Tiền tệ | `components/modal/finance/currency-modal.vue` | `name` `required\|max:255`; `code`/`other_name` `max:255`; `exchange_rate` `number_vn\|positive_vn\|max_value_vn:999999.99` |
| T5.4 ✅ | TK ngân hàng | `pages/finance/account-banks/AccountBankModal.vue` | `account_name` `required`. Bỏ 5 chặn required tự viết |
| T5.5 ✅ | Công nợ chi phí | `pages/finance/cost-debts/CostDebtModal.vue` | `name` `required`; giữ rule nghiệp vụ "đã hạch toán → không được khóa", nay chạy realtime khi đổi trạng thái |
| T5.6 ✅ | Nguồn vốn | `pages/finance/source-capitals/SourceCapitalModal.vue` | `name` `required` |
| T5.7 ✅ | Công trình | `pages/finance/works/WorkModal.vue` | `name` `required`; giữ rule nghiệp vụ khóa như T5.5 |
| T5.8 ✅ | Đề nghị chuyển hàng | `pages/finance/product-transfer-requests/components/ProductTransferRequestForm.vue` | Không có ô Tên → bỏ hết chặn required. Giữ `note` ≤255, `qty` 1–999.999.999, ghi chú dòng ≤255, "ngày cần hàng phải sau hôm nay". Cho chạy **realtime** bằng watcher `products` deep |

### 5.2 Chăm sóc khách hàng (6 màn) ✅

| # | Màn | File FE sửa | Rule FE sau khi sửa |
| --- | --- | --- | --- |
| T5.9 ✅ | Chi phí | `components/modal/customer-care/cost-modal.vue` | `name` `required\|max:255`; `rate_value_capital` `number_only\|min_value:0`; `vat_percent`/`discount` `number_only\|min_value:0\|max_value_decimal:100` |
| T5.10 ✅ | Cấp bảo dưỡng | `components/modal/customer-care/level-modal.vue` | `name` `required\|max:255` |
| T5.11 ✅ | Ghi chú kiểm tra | `components/modal/customer-care/note-maintenance-modal.vue` | `name` `required\|max:255`; `key_name`/`description` `max:255` |
| T5.12 ✅ | Serial thiết bị | — | **Không phải sửa**: màn chỉ có danh sách + bộ lọc, BE chỉ có `index`/`filterOptions`, không có form |
| T5.13 ✅ | Cấu hình giá dịch vụ | `pages/customer-care/service-price-config/index.vue` | `coefficient_cost_price_service` `number_only\|min_value:0.01\|max_value_decimal:999.99`; `sale_max_percent` `number_only\|min_value:0\|max_value_decimal:99`. Bỏ 2 computed validate tự viết |
| T5.14 ✅ | Lỗi thiết bị | `pages/customer-care/device-errors/components/DeviceErrorFormComponent.vue` | Giữ cơ chế realtime sẵn có; bỏ required của Loại lỗi / Định mức công / Chiết khấu / VAT / Thiết bị áp dụng. Giữ `benefit_coefficient` > 0, `vat_percent` ≤ 100 |

### 5.3 Khác ✅

- [x] T5.15 `/human/banks` (`pages/human/banks/components/BankModel.vue`) — `name` `required`;
      bỏ chặn required của Mã / Tên viết tắt

### 5.4 Kiểm chứng ✅

- [x] T5.16 Parse 25 file đã sửa (`vue-template-compiler` + `@babel/parser`) + `locales/vi.json` → tất cả OK
- [x] T5.17 Nạp THẬT thân hàm `validate` trong `plugins/vee-validate.js` bằng `vm` và chạy 20 case
      (biên hợp lệ / không hợp lệ, định dạng VN, rule `max` cũ không đổi hành vi) → 20/20 đúng

### 5.5 Đối chiếu checklist chuyển đổi (Drive) ✅

Nguồn: **Checklist chuyển đổi ERP =>> HRM.xlsx** (Drive, sheet "Chi tiết chức năng") — lọc
`Trạng thái = Đã test` ra **23 màn**. Đợt trước mới phủ 16 dòng (theo khảo sát `pagination-100-rows`),
thiếu **6 màn Danh mục địa chỉ** + màn Khách hàng.

- [x] T5.18 Quốc gia — `pages/human/nations/components/NationModel.vue`
      (`name` `required|max:255`; `code` `max:50`; `postal_code` `number_only|digits_between:1,50`)
- [x] T5.19 Khu vực — `pages/human/areas/components/AreasModel.vue` (`name` `required|max:255`)
- [x] T5.20 Tỉnh/TP — `pages/human/provinces/components/ProvinceModel.vue`
      (`name` `required|max:255`; `code` `number_only|digits_between:0,10`; `license_plate` `digits_between:0,50`)
- [x] T5.21 Quận/Huyện — `pages/human/districts/components/DistrictModel.vue` (`name` `required|max:255`)
- [x] T5.22 Phường/Xã — `pages/human/wards/components/WardModel.vue`
      (`name` `required|max:255`; `code` `number_only|digits_between:0,10`)
- [x] T5.23 Đường/Phố — `pages/human/hamlets/components/HamletModel.vue` (`name` `required|max:255`)
- [x] T5.24 Danh mục khách hàng `/assign/customers` — `components/assign-components/customer/CustomerForm.vue`
      (dùng chung 5 màn: thêm / sửa / chi tiết / quản lý KH / modal thêm nhanh)

→ Đợt này phủ **23/23 màn** của checklist.

#### Chi tiết T5.24 — màn Khách hàng

Hiện trạng trước khi sửa: **không có validate FE nào**, toàn bộ dựa vào 422 (`formError`).

| Nhóm | Cách làm |
| --- | --- |
| Ô top-level (15 ô) | `v-validate` + `name` = key BE. `fullname` `required\|max:255` (ô Tên duy nhất); `email` `email\|max:255`; `tax_code` `tax_code\|max:255`; `short_name`/`website`/`apartment_number`/`gara_name`/`grant_location`/`identity_card_number` `max:255`; `mobile` `max:20`; `date_of_birth`/`grant_date` `not_future` |
| Khối LẶP (SĐT, người đại diện, người liên hệ) | Hàm `validateRepeatBlocks()` + watcher deep `form.phones` / `deputies` / `contacts` → chạy realtime. Không dùng `v-validate` vì tên field phải trùng key BE theo CHỈ SỐ (`contacts.1.email`), xoá dòng làm chỉ số dịch |
| Lỗi BE 422 | `applyServerErrors()` — key BE trùng key FE nên gắn đúng ô |

Ô `email` / `website` / `apartment_number` xuất hiện 2 lần trong template (khối Cá nhân vs Tổ chức)
nhưng nằm trong 2 nhánh `v-if` loại trừ nhau (`form.customer_type == 1` / `isOrganization`) nên chỉ
1 field đăng ký với vee-validate tại một thời điểm — không trùng tên.

Bổ sung hiển thị lỗi inline cho các ô trước đây không có: `phones.{i}`, `contacts.{i}.email`,
`contacts.{i}.identity_card_number`, `contacts.{i}.phones.{j}`.

3 rule mới trong plugin: `phone_number` (regex `^(0)[0-9]{9,11}$` — **không** dùng rule `phone` sẵn có
vì nó chỉ nhận đúng 10 số), `tax_code` (regex `^[\d\-]{1,14}$`), `not_future`.

BE chuẩn hoá thêm 2 file (`SaveCustomerRequest`, `UpdateCustomerRequest`): bỏ override
`email.email` (rơi về lang vi `Định dạng email không hợp lệ` = câu FE), gộp 3 message
`before_or_equal` về `Không được lớn hơn ngày hiện tại`.

### 5.6 Chuẩn hoá message BE (user chốt 2026-08-14)

Thay vì truyền câu lỗi vào rule FE, **sửa BE cho đồng nhất**: mọi Request bỏ message riêng theo
từng trường, dùng câu chung đúng bằng câu FE đang nói.

| Rule | Câu chuẩn | Nguồn |
| --- | --- | --- |
| `required` | `Bắt buộc phải nhập` | lang vi của BE — FE bỏ dấu chấm trong `locales/vi.json` |
| `max` (chuỗi) | `Vui lòng nhập tối đa :max ký tự.` | lang vi `max.string` — BE **bỏ** override, FE dùng rule `max` sẵn có |
| `numeric` | `Phải là số` | rule FE `number_only` |
| `min` (số) | `Không được nhỏ hơn :min` | rule FE `min_value` |
| `max` (số) | `Tối đa :max` | rule FE `max_value_decimal` / `max_value_vn` |
| `gt` (số) | `Phải lớn hơn :value` | rule FE `positive_vn` |
| `digits_between` | `Chỉ được nhập chữ số, từ :min đến :max chữ số` | rule FE `digits_between` |
| `email` | `Định dạng email không hợp lệ` | lang vi của BE — **FE đổi theo BE** trong `locales/vi.json` (user chốt). Toàn repo chỉ 1 ô đang dùng rule `email` (`pages/client/course-attendance/index.vue`) |

Hệ quả: **xoá hẳn** dictionary `custom` theo tên trường ở `plugins/vee-validate.js` — vee-validate chỉ
có 1 dictionary toàn cục theo tên trường, mà `name`/`code`/`note` trùng nhau ở hàng chục màn.

File BE đã sửa (`hrm-api`, 12 file — `php -l` sạch):
`AccountRequest` · `TypeAccountRequest` · `CurrencyRequest` · `ProductTransferRequestRequest` ·
`CostRequest` · `LevelRequest` · `NoteMaintenanceRequest` · `ServicePriceConfigRequest` ·
`DeviceErrorRequest` · `CreateNationRequest` · `CreateProvinceRequest` · `CreateDistrictRequest` ·
`CreateWardRequest` · `CreateHamletRequest`.
Giữ nguyên override của `unique` / `exists` / `in` / `not_in` / closure — FE không chạy các rule này.

📌 Sửa luôn 1 lỗi cũ: `AccountRequest` báo "từ 3 đến **10** chữ số" trong khi
`Account::MAX_IDENTIFY_NUMBER_DIGITS = 15`.

### 5.7 Ngoại lệ đã được gỡ

- `device_error_costs.price` / `price_service`: trước đây BE khai `nullable` trong khi cột DB là
  **NOT NULL** → gửi rỗng nổ SQL 1048 (500), nên FE phải tự chặn bỏ trống. **BE đã vá** thành
  `required|numeric|min:0` kèm message → FE gỡ chặn bỏ trống, chỉ còn soi định dạng (số, ≥ 0).
  Nay không còn ngoại lệ nào: FE chỉ chặn bỏ trống ở ô Tên.

## Việc còn lại (ngoài phạm vi)

- [ ] `/assign/customers` (`CustomerForm.vue`) — email, SĐT regex, mã số thuế regex, ~20 trường max:255
- [ ] Cập nhật `.claude/skills/form-validate/SKILL.md` — **tài sản chung, phải qua PR**
- [ ] Các màn `V2Base*` ngoài gop-db vẫn dùng cờ `touched` — chuyển dần khi đụng tới

---

### Checkpoint — 2026-08-14 (đợt 1)

Vừa hoàn thành: Phase 1-4 — base nhận `v-validate`, màn Gói bảo dưỡng chạy realtime.
Bước tiếp theo: Phase 5 — T5.0 thêm rule vào plugin.
Blocked:

### Checkpoint — 2026-08-14 (đợt 2)

Vừa hoàn thành: Phase 5 trọn vẹn — 7 rule mới trong `plugins/vee-validate.js` (thuần thêm) + 14 màn
gop-db đã bỏ chặn required (trừ ô Tên) và bê rule định dạng của BE sang FE, message trùng nguyên văn.
Serial không phải sửa (không có form).
Đang làm dở: chưa có.
Bước tiếp theo: user test trình duyệt 14 màn; sau đó tính tiếp `/assign/customers` (`CustomerForm.vue`).
Blocked:

### Checkpoint — 2026-08-14 (đợt 3)

Vừa hoàn thành:
1. Đối chiếu **Checklist chuyển đổi ERP =>> HRM.xlsx** trên Drive → 23 màn `Đã test`, đợt 2 mới phủ 16.
   Bổ sung **6 màn Danh mục địa chỉ** (Quốc gia / Khu vực / Tỉnh-TP / Quận-Huyện / Phường-Xã / Đường-Phố).
2. **Chuẩn hoá message BE** (14 Request) thay cho việc truyền câu lỗi vào rule FE; xoá dictionary
   `custom` theo tên trường ở `plugins/vee-validate.js`; bỏ dấu chấm ở `required` trong `locales/vi.json`.
Verify: parse 31 file FE + `vi.json`; `php -l` 15 file BE; chạy lại 20 case rule → 20/20 đúng.
Bước tiếp theo: user test trình duyệt 22 màn. Còn `/assign/customers` (user chốt để sau).
Blocked:

### Checkpoint — 2026-08-14 (đợt 4)

Vừa hoàn thành: màn **Danh mục khách hàng** (`CustomerForm.vue`, dùng chung 5 màn) → phủ đủ
**23/23 màn** của checklist. Thêm 3 rule `phone_number` / `tax_code` / `not_future`; chuẩn hoá
message của `SaveCustomerRequest` + `UpdateCustomerRequest`. Gỡ ngoại lệ ở màn Lỗi thiết bị sau khi
BE vá `costs.*.price` thành `required`.
Verify: parse `CustomerForm.vue` + `DeviceErrorFormComponent.vue` + plugin; `php -l` 3 file BE;
chạy 20 case rule cũ + 9 case rule mới → tất cả đúng.
Bước tiếp theo: user test trình duyệt.
Blocked:

### Checkpoint — 2026-08-14 (CHỐT HOÀN THÀNH)

Vừa hoàn thành: **user test trình duyệt xong đủ 23/23 màn**, chốt feature **HOÀN THÀNH**.
STATUS.md đã chuyển entry từ "Đang làm" sang "Hoàn thành".
Đang làm dở: không có.
Bước tiếp theo (không chặn hoàn thành): PR cập nhật `.claude/skills/form-validate/SKILL.md`
(bỏ `data-vv-value-path`); user tự commit khi muốn.
Blocked: không.
