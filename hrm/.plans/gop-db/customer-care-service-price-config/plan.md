# Plan — Cập nhật nhanh giá dịch vụ (CSKH)

**Người phụ trách:** @junfoke — 2026-08-06
**Nhánh:** `gop_db`
**Design:** `.plans/gop-db/customer-care-service-price-config/design.md`
**Spec:** `docs/superpowers/specs/gop-db/2026-08-06-customer-care-service-price-config-design.md`

## Ràng buộc chung

- Không commit / không push git.
- Bảng quyền SỐNG là `permissions`, KHÔNG phải `hrm_permissions`.
- Không đổi schema `service_price_config` / `services` / `service_levels`, không đổi công thức.
- Cờ quyền FE khởi tạo `false`, chỉ set từ `$store.state.permissions`.
- Mọi form có validate: BE rethrow `ValidationException`, FE hiện lỗi inline theo flag `touched`.

---

## Phase 0 — Chuẩn bị

- [x] **0.1 Ghi lại số liệu gốc để đối chiếu cuối bài**

```sql
SELECT * FROM service_price_config;
SELECT COUNT(*) FROM services;                      -- kỳ vọng 207
SELECT COUNT(*) FROM service_levels;                -- kỳ vọng 242
SELECT SUM(base_price) FROM service_levels;         -- checksum
SELECT SUM(coefficient_cost_price_service), SUM(sale_max_percent) FROM services;
```

- [x] **0.2 Đọc skill `button-convention` + `modal-popup`** (màn có nút Lưu + popup xác nhận).

---

## Phase 1 — Backend

- [x] **1.1 Entity `ServicePriceConfig`**

Create: `hrm-api/Modules/CustomerCare/Entities/ServicePriceConfig/ServicePriceConfig.php`
— `$table = 'service_price_config'`, fillable 2 trường nghiệp vụ + `created_by`/`updated_by`.

- [x] **1.2 `ServicePriceConfigRequest`**

Create: `hrm-api/Modules/CustomerCare/Http/Requests/ServicePriceConfig/ServicePriceConfigRequest.php`

```php
'coefficient_cost_price_service' => 'required|numeric|min:0.01|max:999.99',
'sale_max_percent' => 'nullable|numeric|min:0|max:99',
```

- [x] **1.3 `ServicePriceConfigService`**

Create: `hrm-api/Modules/CustomerCare/Services/ServicePriceConfigService.php`

- `show()` → cấu hình hiện tại + `affected_services_count` + `affected_levels_count`.
- `update(Request)` trong 1 transaction: `firstOrNew` (không `find(1)` cứng) → ghi `updated_by` →
  nếu hệ số đổi thì tính lại `base_price = floor(work_price × quota_work × hệ số)` →
  luôn ghi đè `coefficient_cost_price_service`, ghi `sale_max_percent` khi client gửi (kể cả `0`).
- Duyệt bằng `chunkById(200)` + eager load `serviceLevels`, `company` (tránh N+1).
- Gói không resolve được `work_price` → **bỏ qua**, đếm vào `skipped` (ERP ghi giá về 0).

- [x] **1.4 Controller + Resource + route**

Create `ServicePriceConfigController` (`show`, `update`) + `ServicePriceConfigResource`;
thêm group route `/service-price-config` (GET + PUT), cả 2 gắn
`checkPermission:Cập nhật nhanh giá dịch vụ`.

- [x] **1.5 Kiểm cú pháp + route**

`php -l` từng file · liệt kê route bằng `Route::getRoutes()` trong tinker
(`route:list` đang 500 vì lỗi có sẵn `PermissionHelper:22`).

---

## Phase 2 — Quyền & menu

- [x] **2.1 ~~Migration đưa quyền 100320 về CSKH~~ → ĐÃ ROLLBACK, đổi cách làm**

Đã viết + chạy migration đổi `type = 24`, nhưng khi verify thì **lộ ra quyền 100320 có
`guard_name = web`**, còn HRM chạy guard `api`:

- `store.state.permissions` của FE (573 quyền) **không chứa quyền guard web nào** — kể cả
  `Xem khách hàng` (100057) đã đổi `type = 9` từ đợt trước → middleware
  `hrm-client/middleware/checkPermission.js:56` đá về `/pages/extras/404`.
- Middleware BE `checkPermission` đọc qua Spatie với guard `api` nên cũng luôn 403.

→ Đã `migrate:rollback` + **xóa file migration** (quyền 100320 trở về `type = NULL`,
group `Kế toán làm giá` như cũ).

- [x] **2.1b Tạo quyền HRM guard `api` TRÙNG TÊN (user chốt)**

Thêm vào `PermissionsTableSeeder`: `id 1130`, name/display_name `Cập nhật nhanh giá dịch vụ`,
`guard_name = api`, group `Danh mục dịch vụ bảo dưỡng`, `type = 24`. Spatie chỉ yêu cầu duy nhất
theo cặp `(name, guard_name)` nên trùng tên với bản ERP là hợp lệ.
Đã chèn tay vào DB local + gán cho role 18 để verify.

Route đổi `checkPermission` → **`erpPermission`** (khớp theo TÊN, không quan tâm guard) → ai có
quyền ở ERP (bản web, 3 chức vụ hiện có) **hoặc** ở HRM (bản api) đều dùng được màn.

⚠️ `PermissionsTableSeeder` vừa được người khác thêm 3 quyền gói bảo dưỡng (1126-1128) nên quyền
serial trong seeder dời thành **1129** trong khi DB local đang là **1126** — lệch seeder↔DB vốn đã
là hiện trạng của dự án (1119-1124 seeder vs 1115-1120 DB), không đụng.

- [x] **2.2 Kiểm sau khi đổi quyền**

Quyền 1130 `guard = api`, `type = 24`; quyền 100320 giữ nguyên `web` / `type = NULL` /
group `Kế toán làm giá`; `role_has_permissions` của 100320 vẫn **4 dòng**; group
`Danh mục dịch vụ bảo dưỡng` chỉ có 1 giá trị `type`; `Employee::getAllPermissions()` của user test
đã thấy quyền.

- [x] **2.3 Điền link menu**

Modify: `hrm-client/components/subsystem-menu/customer-care.js` — mục
`Cập nhật nhanh giá dịch vụ` thêm `link: '/customer-care/service-price-config'` +
`isShow: ['Cập nhật nhanh giá dịch vụ']`; cập nhật chú thích đầu file.
Kiểm bất biến: `grep -rn "customer-care/service-price-config" components/subsystem-menu/` → 1 kết quả.

---

## Phase 3 — Frontend

- [x] **3.1 Màn form**

Create: `hrm-client/pages/customer-care/service-price-config/index.vue`,
`layout: 'default-sidebar'`, V2Base. 2 ô nhập + lỗi inline theo `touched`, dòng phụ hiện thời điểm
và người cập nhật gần nhất, nút Lưu mở `BaseConfirmModal` nêu số gói / số cấp bị ảnh hưởng.
Cờ `canUpdate` fail-closed.

---

## Phase 4 — Verify

- [x] **4.1 BE — đọc & validate**

`GET` trả đúng cấu hình + số lượng khớp SQL · hệ số rỗng → 422 · `sale_max_percent = 100` → 422 ·
`= 0` → nhận · không quyền → 403 · không token → 401.

- [x] **4.2 BE — lưu KHÔNG đổi hệ số**

`base_price` từng dòng `service_levels` giữ nguyên (so checksum trước/sau);
`services.sale_max_percent` được áp giá trị mới.

- [x] **4.3 BE — lưu ĐỔI hệ số, rồi khôi phục**

Đổi hệ số → đối chiếu `base_price` với `floor(work_price × quota_work × hệ số)` trên mẫu vài dòng;
sau đó **đặt lại hệ số cũ** và xác nhận checksum trở về giá trị ban đầu ở bước 0.1.

- [x] **4.4 FE (Playwright)**

Mở màn (`matched = 1`, 0 console error) · bỏ trống hệ số → lỗi inline, không gọi API ·
sửa giá trị → popup hiện đúng 207/242 → xác nhận → toast thành công, dữ liệu reload đúng ·
menu CSKH hiện mục mới, bấm vào đúng màn.

- [x] **4.5 Dữ liệu nguyên trạng**

Chạy lại toàn bộ truy vấn ở 0.1 — phải khớp giá trị ban đầu.

---

## Kết quả thực thi — 2026-08-06

### Số liệu gốc (DB `gop_db` local)

`service_price_config`: 1 dòng, hệ số `2.00`, định mức `5.00`, updated 2025-09-04 10:33:33 (by 215).
`services` 207 · `service_levels` 242 · `SUM(base_price) = 734.438.356` ·
`SUM(coefficient) = 412` · `SUM(sale_max_percent) = 1035`.

### Verify BE

| Case | Kết quả |
| --- | --- |
| `GET` | 200, hệ số 2 / định mức 5 / 207 / 242 / "04/09/2025 10:33 — Nguyễn Thị Thanh Nhàn" |
| Hệ số rỗng · hệ số chữ · `sale_max_percent` = 100 · = -1 | 422 (đủ 4 case) |
| Không token | 401 |
| Lưu **không đổi** hệ số (2), định mức 5 → 7 | `SUM(base_price)` **giữ nguyên** 734.438.356; `SUM(smp)` 1035 → 1449 = 207 × 7 ✔ |
| Lưu **đổi** hệ số 2 → 2.5 | 242/242 dòng khớp `FLOOR(work_price × quota_work × 2.5)`, **0 dòng lệch**; `SUM(base_price)` 734.438.356 → 865.987.492 |
| Khôi phục từ backup | `SUM(base_price)` về đúng 734.438.356, 0 dòng phải sửa lại |

### Verify FE (Playwright)

`matched = 1`, **0 console error** · bỏ trống hệ số + bấm Lưu → hiện lỗi inline "Bắt buộc phải
nhập", **popup không mở, không gọi API** · nhập hợp lệ → popup hiện đúng "tất cả **207** gói bảo
dưỡng" và "**242** cấp dịch vụ" · Đồng ý → `PUT` 200 → tự `GET` lại, dòng phụ đổi thành
"06/08/2026 14:42 — DNS Admin".

### Ghi nhận

- 🐞 **Lỗi tự gây đã sửa**: `this.$nuxt.$loading.start()` gọi trong `mounted()` → `TypeError: not a
  function` ($loading chưa sẵn sàng ở thời điểm đó). Đã đổi sang `$loading?.start?.()`.
- 🗑 **Đã bỏ nút "Khôi phục"** (user chỉ ra khi rà màn): nút này tôi tự thêm, ERP không có, và nhãn
  khiến người dùng hiểu là *hoàn tác về cấu hình cũ* trong khi nó chỉ gọi lại API lấy dữ liệu hiện
  tại — chức năng hoàn tác không tồn tại. Màn giờ chỉ còn đúng 1 nút **Lưu**.
- ⚠️ **Chưa verify được mục menu trong sidebar**: sidebar CSKH nay là hub kiểu MISA, chỉ render
  rail nhóm; link con nằm trong panel mở động mà Playwright click/hover không bung ra được.
  Registry đã đúng (`grep` ra đúng 1 kết quả `/customer-care/service-price-config` trong
  `subsystem-menu/`), vào thẳng URL chạy tốt → cần **user nhìn mắt**.
- ⚠️ **1 sai lệch dữ liệu KHÔNG khôi phục được**: `SUM(coefficient_cost_price_service)` của
  `services` từ **412 → 414**. Lần lưu BE đầu tiên (trước khi tôi kịp sao lưu) đã ghi đè 1 gói có
  hệ số `NULL` thành `2` — đúng hành vi ghi đè hàng loạt của ERP, nhưng không suy ngược được gói
  nào (207 gói đều có `updated_at` mới sau lần lưu đó). Chỉ ảnh hưởng DB local.
  **Bài học: sao lưu cột bị ghi đè TRƯỚC lần gọi API ghi đầu tiên, không phải sau.**
- `php artisan route:list` vẫn 500 do lỗi có sẵn `PermissionHelper:22` → kiểm route bằng
  `Route::getRoutes()`.

## Checkpoint — 2026-08-06

Vừa hoàn thành: toàn bộ Phase 0-4 (trừ phần nhìn mắt menu). BE 5 file mới + 2 route; FE 1 page +
link menu; quyền: rollback migration đổi type, thay bằng quyền api id 1130 trùng tên + gate
`erpPermission`. Verify BE 7 nhóm case + FE Playwright. Dữ liệu về baseline (trừ 1 sai lệch ghi ở
trên).
Đang làm dở: không.
Bước tiếp theo: user rà bằng mắt `/customer-care/service-price-config` + kiểm mục menu trong
sidebar CSKH.
Blocked: không.

## Phase — Tai lieu ban giao (2026-08-13)

- [x] `testcase.xlsx` — 57 TC (P0 63%); generator `gen_testcase.py`
- [x] `HDSD_Cap nhat nhanh gia dich vu.docx` — 11 trang; generator `gen_hdsd.py`
- [x] Anh nguon `hdsd_shots/` (CHI LOCAL, khong commit)
- Ghi nhan khi chup anh tren cong dev: dong ghi chu duoi 2 o hien "0 goi bao duong" trong khi hop
  xac nhan hien 221 goi -> con so trong dong ghi chu co the chua kip nap luc mo man. CAN KIEM LAI
