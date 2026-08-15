# STATUS.md — Phần GỘP DATABASE (nhánh `gop_db`)

> File này chỉ theo dõi các feature làm trên nhánh `gop_db` (hoặc nhánh checkout ra từ `gop_db`).
> Feature trên nhánh khác → ghi ở `.plans/STATUS.md`.

## ⚠️ Nền tảng — đọc TRƯỚC khi làm việc trên nhánh `gop_db`

**`.plans/gop-db/design.md`** — nhánh `gop_db` (cả 2 repo) gộp DB ERP + HRM thành DB duy nhất `local_hrm_erp`.
Ảnh hưởng tới MỌI feature làm trên nhánh này: bảng trùng tên ưu tiên bản ERP (bản HRM đổi tên `hrm_*`, 24 bảng),
`roles`/`permissions`/`files`/`groups` là của **ERP** — dữ liệu HRM nằm ở `hrm_*`;
riêng **`employees` + `employee_infos` đã gộp chung từ 2026-08-03** → `auth()->user()->id` là id nhân viên
duy nhất, `hrm_employees` là bảng cũ bỏ đi (xem mục 0b của design.md);
`mysql2` vẫn trỏ DB ERP CŨ (nguồn bug id lệch); kèm 7 gotcha bắt buộc biết khi port màn ERP → HRM.
Việc gộp DB **không có migration trong repo** → không tái tạo được từ code, phải xin dump.

**Quy tắc bắt buộc (chi tiết ở `CLAUDE.md` mục "Phần GỘP DATABASE"):**
- Nhận biết bằng **nhánh git đang đứng**, không đoán theo tên feature: đang ở `gop_db` hoặc nhánh checkout ra từ `gop_db` → áp dụng quy tắc này
- Tài liệu: feature làm trên nhánh đó nằm trong **`.plans/gop-db/[feature]/`**, spec chi tiết ở `docs/superpowers/specs/gop-db/`
- Code: chỉ làm **trên nhánh `gop_db`** hoặc nhánh **checkout ra từ `gop_db`**, merge trả về `gop_db`
- KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND` cho tính năng mới

## Tài liệu TC + HDSD theo form mẫu của team (2026-08-13)

Sinh lại **testcase** theo form mẫu chuẩn (17 cột, 2 khối summary DNS/TP) và **HDSD Word**
cho **7 màn chuyển phân hệ của @junfoke** — tổng **623 test case** và **7 file HDSD**.
Ảnh HDSD chụp thật trên cổng dev `hrm-crm.eteksofts.com` (22 ảnh, chỉ để local).

| Màn hình | TC | P0 | HDSD |
| --- | --- | --- | --- |
| Danh mục tiền tệ | 117 | 49% | 17 trang |
| Danh mục tài khoản | 128 | 66% | 16 trang |
| Danh mục loại tài khoản | 104 | 61% | 16 trang |
| Cấp dịch vụ bảo dưỡng | 75 | 56% | 11 trang |
| Danh mục ghi chú kiểm tra bảo dưỡng | 75 | 55% | 11 trang |
| Danh mục serial thiết bị làm dịch vụ | 67 | 63% | 11 trang |
| Cập nhật nhanh giá dịch vụ | 57 | 63% | 11 trang |

Đóng gói thêm 2 engine dùng chung vào skill (trước đây mỗi feature phải nhân bản ~1.300 dòng):
`.claude/skills/testcase-documenter/assets/tc_engine.py` và
`.claude/skills/hdsd-documenter/assets/hdsd_engine.py`.
Generator của từng màn nằm cùng thư mục tài liệu (`gen_testcase*.py`, `gen_hdsd*.py`).

Đã xóa 2 file `testcase.xlsx` bản cũ (format 15 cột, gộp nhiều màn) ở `finance-account-catalog` và
`customer-care-maintenance-catalogs` — user chốt 2026-08-13, thay bằng file tách theo từng màn.

## Tài liệu SRS + Testcase (2026-08-07)

Đã sinh `srs.html` + `srs.docx` + `testcase.xlsx` cho **6 màn nghiệp vụ của @junfoke**
(tổng 438 test case, P0 54-62%).
Bám code thật: validation lấy từ Request class, schema từ Entity, API từ Routes, business rule từ Service.

| Feature | TC | Feature | TC |
| --- | --- | --- | --- |
| finance-account-catalog | 98 | customer-care-cost-catalog | 82 |
| finance-currency-catalog | 68 | customer-care-serial-catalog | 58 |
| customer-care-maintenance-catalogs | 74 | customer-care-service-price-config | 58 |

**Chưa sinh:** `bank-account-catalog` và `customer-care-services-catalog` (của @khoipv — chủ feature tự làm);
nhóm hạ tầng/refactor (tach-phan-he-erp-hrm, bo-sung-menu-phan-he, chuyen-code-phan-he,
customer-cut-mysql2, banks-cut-mysql2) — không phải màn nghiệp vụ.

⚠️ **2 việc phát hiện khi soát code để viết tài liệu:**

1. `PermissionsTableSeeder` khai TRÙNG quyền tiền tệ: id 1115/1116 và 1117/1118 cùng `name` cùng guard `api`
   → chạy seeder trên DB sạch sẽ nổ lỗi trùng khóa. Cần bỏ 1 cặp.
2. `bank-account-catalog` (@khoipv) có design.md + plan.md, code đã xong nhưng **chưa có mục trong STATUS.md này**
   → nhờ @khoipv bổ sung.

## Đang làm

- finance-product-import-request → @junfoke → .plans/gop-db/finance-product-import-request/plan.md
  Trạng thái: **XONG PHASE 1-7, ĐÃ VERIFY** (2026-08-14). Chờ so cạnh nhau trên dev.
  Phase 7: đã merge `gop_db` (cả 2 repo, 0 conflict) và áp bộ chuẩn UI mới — cột Hành động cuối
  bảng bằng `V2BaseRowActions`, link mã phiếu `.v2-cell-link`, popup xác nhận dùng
  `base-confirm-modal`, thứ tự request theo `list-page` mục 8, chuẩn nút (Tạo mới / Xóa /
  Xuất Excel xanh lá), sắp xếp theo độ khớp ở BE.
  Danh sách (4 preset theo quyền) + form Tạo/Sửa **7/8 loại** (loại 11 bị loại có chủ đích vì
  ERP sinh tự động từ Phiếu YC nhập khẩu) + chi phí nội địa + dòng con khách hàng
  + màn Chi tiết với 4 luồng duyệt (Kế toán kho / BKS / BGĐ / TP) + tab lịch sử.
  + In (mẫu ERP 44) + xuất Excel + xoá file S3.
  Verify: 16/16 route, luồng end-to-end trên trình duyệt, 0 migration, đối chiếu 2 cổng ở mức code
  (12 trạng thái + 17 tên loại + mẫu in 44 trùng khớp).
  2 việc đã chốt: (a) lỗ hổng "mọi trưởng phòng duyệt được phiếu phòng ban khác" — **giữ nguyên
  như ERP**; (b) NCC/KH rỗng — **chỉ DB local thiếu bản ghi, trên dev đủ**, không phải lỗi.
  Port màn ERP "Phiếu Yêu cầu nhập hàng"
  (`productImportRequest.all`) sang phân hệ **Tài chính**, slot `finance.js:95`.
  Chốt: 1 mục menu + 1 màn danh sách nhận `?type=` với 4 preset (all/for_approve/managerApprove/
  departmentManagerApprove), form 8 loại — danh sách hiện 12 loại, quyền dùng lại ERP qua
  `erpPermission` + bản ghi `guard=api` trùng tên. Worktree riêng ở cả 2 repo, nhánh
  `feat/finance-product-import-request`.

- unsaved-changes-catalogs → @junfoke → .plans/gop-db/unsaved-changes-catalogs/plan.md
  Trạng thái: **CODE DONE, CHƯA TEST TRÌNH DUYỆT** (2026-08-12). Popup "Thông tin chưa lưu"
  khi thoát màn form — đợt 1: 14 màn danh mục customer-care + finance.
  Thêm 2 mixin MỚI (`unsavedModalMixin` cho modal, `unsavedChildFormMixin` cho trang vỏ);
  **không sửa** `unsavedChangesMixin` cũ — phương án gộp chờ anh Nam chốt.
  Còn lại ~147 form trang + ~180 modal của các phân hệ cũ → đợt 2/3.

- filter-customization → .plans/gop-db/filter-customization/plan.md
  Trạng thái: **CODE DONE Phase 1–3 — chờ chạy migration + user test** (2026-08-12, nhánh `gop_db`, cả 2 repo).
  Cho user tự chọn trường lọc hiển thị + **kéo thả sắp xếp vị trí** (popup "Cài đặt bộ lọc"), giống "Tuỳ chỉnh cột" nhưng cho bộ lọc; mặc định hiện đủ. UX tham chiếu demo kế toán `demo 3/assets/app.js` (`setupFilterSettings` chưa kéo thả + `setupColumnConfig` có kéo thả) → ghép 2 cái, lưu BE thay localStorage.
  Chốt: bảng mới **generic** `filter_customizations (created_by, table, config json)` unique(created_by, table) — KHÔNG copy schema cột-mỗi-màn của `column_customizations` (Entity đó 25 cột trong `$casts`, thêm màn là phải migration); khoá màn = tên bảng chính (`'customers'`); `config = [{key,isVisible}]`, thứ tự mảng = thứ tự hiển thị, không lưu label; bỏ tick = **ẩn hẳn + reset giá trị lọc** (tránh lọc ngầm); không có field locked; **component mới**, KHÔNG sửa `V2BaseFilterPanel`.
  BE (`gop_db-api`): migration + `FilterCustomization` (có khai `$table`) + Service + FormRequest + Controller + 2 route `human/filter-customizations`, không thêm quyền.
  FE (`gop_db-client`): `components/V2BaseSmartFilterPanel.vue` (schema field + slot escape hatch `#field-<key>` + `wrapperClass`/`hideLabel`/`resetKeys` cho field gom nhiều control) + `components/modal/filter-customization-modal.vue` (checkbox + vuedraggable). **Merge DB ↔ schema nằm trong component**: key mất khỏi FE → bỏ hẳn, key mới → append cuối và hiện ⇒ bổ sung trường lọc sau này không lỗi.
  Pilot: `pages/assign/customers/index.vue` — 15 field khai báo bằng `filterFields`, khối Công ty/PB/NV và CascadePairSelect đi qua slot. Class wrapper đổi `advanced-filters` → `smart-advanced-filters` để dropdown CascadePairSelect không bị cắt (rule scoped cũ ở page đã bỏ).
  Spec: docs/superpowers/specs/gop-db/2026-08-12-filter-customization-design.md
  Bước tiếp: chạy `php artisan migrate` (module Human) → build FE → user test popup Cài đặt bộ lọc trên `/assign/customers`.

- customer-list-empty-placeholder → .plans/gop-db/customer-list-empty-placeholder/plan.md
  Trạng thái: **CODE DONE — CHỜ USER TEST TRÌNH DUYỆT** (2026-08-12, nhánh `gop_db`, 2 file).
  Ô "không có dữ liệu" ở màn `/assign/customers` hiển thị không đồng nhất: mọi cột ra `—` (em dash),
  riêng **SĐT ra `-`** vì `CustomerListResource` tự chèn sẵn chuỗi `'-'` từ BE (cả khi trống lẫn khi
  bị che do không phải KH của mình) → FE nhận chuỗi khác rỗng nên `|| '—'` không chạy.
  Fix: BE trả `null`, placeholder do FE quyết định; popup chọn KH thêm slot fallback `#cell()`
  (7 cột trước đây để ô trắng, riêng SĐT ra `-`) → tất cả về `—`.
  Giữ nguyên `'-'` trong file xuất CSV/Excel (`CustomerExportFormatter::taxCodeOrMobile`) — theo mẫu ERP,
  ngữ cảnh file bàn giao khác màn hình. Không migration, không quyền mới.

- list-page-action-column → @junfoke → .plans/gop-db/list-page-action-column/plan.md
  Trạng thái: **CODE DONE — CHỜ USER VERIFY UI** (2026-08-12). Chuẩn hoá cột "Hành động" cho màn danh sách,
  màn mẫu `/assign/customers`: cột Hành động chốt cuối bảng, tối đa 3 nút (2 chính + menu "⋮" dọc),
  bỏ hành động Xem (tên KH thành link chi tiết), cột Trạng thái dời xuống ngay trước cột Hành động,
  nút Khóa/Mở khóa chuyển từ ô Trạng thái sang cột Hành động.
  Component dùng chung mới: `components/V2BaseRowActions.vue` (menu appendChild ra body + position fixed
  vì bảng có overflow sẽ cắt mất menu). Hành động chuyển trang khai `to` → render `<nuxt-link>` để mở tab mới được.
  Tóm tắt: .plans/gop-db/list-page-action-column/design.md

- fix-employee-fk-remap → @junfoke → .plans/gop-db/fix-employee-fk-remap/plan.md
  Trạng thái: **CODE DONE, DRY PASS — CHƯA CHẠY THẬT** (2026-08-04). Vá các cột FK `employees`
  bị `ReconcileEmployeesSeeder` bỏ sót khi gộp DB: **42 cột / 20.231 dòng** đang trỏ SAI NGƯỜI (gồm 4 cột remap có điều kiện).
  Nguyên nhân: seeder gốc dò cột theo **danh sách tên cột cứng** (39 tên) nên bỏ qua mọi cột tên "lạ"
  (`main_sale_employee_id`, `actor_id`, `pm_id`, `member_id`, `salary_change_employee_id`…), và bộ
  phân loại đòi **100%** giá trị nằm trong `hrm_employees` nên loại nhầm 40 cột chỉ vì vài dòng trỏ
  nhân viên đã xoá. Nó cũng bỏ qua cột `varchar` chứa id và cột JSON chứa mảng id.
  ⚠️ Hỏng **im lặng**: id sai vẫn lọt dải hợp lệ → trỏ sang NGƯỜI KHÁC, không sinh lỗi FK.
  Ví dụ: Sale mất quyền thao tác báo giá dự án của chính mình (`QuotationController:161`).
  Đã làm: `FixMissedEmployeeFkSeeder` (3 dạng lưu int/varchar/JSON, DRY mặc định, không drop
  `hrm_employees`) · sửa gốc `ReconcileEmployeesSeeder` sang **dò theo dữ liệu + fail-closed**
  (còn cột chưa phân loại thì DỪNG, không remap gì) + mốc `gop_db_steps` chống chạy lại + xử lý cột JSON.
  🐛 **Lỗi nền tảng phát hiện được**: `GopDbHelper::run(string $sql)` trùng tên `Seeder::run()` →
  method của class thắng method của trait → **đệ quy vô hạn, 5/7 seeder GopDb chưa từng chạy được**
  (không ai biết vì trên DB đã gộp chúng luôn thoát ở nhánh SKIP). Đã đổi tên thành `exec()`, sửa 44 chỗ.
  ⚠️ **164 id vừa là id HRM cũ của người này vừa là id ERP mới của người khác** → chạy remap lần hai
  là hỏng nặng hơn. TUYỆT ĐỐI không chạy `ReconcileEmployeesSeeder` trên DB đã gộp khi
  `hrm_employees` còn tồn tại.
  Bước tiếp: user backup DB → chạy `GOP_DB_APPLY=1` cho `FixMissedEmployeeFkSeeder`.
  Đã kiểm thử thật trên schema nhân bản 44 bảng: 0 bảng đổi số dòng, **1.005 cột ngoài danh sách không bị đụng**,
  42 cột đích 0 sai map, chạy lần 2 bị chặn. Đối chiếu độc lập: BH 718/718 khớp `created_by`, rice 927/927 khớp `employee_info_id`.
  📌 **Bài học**: vòng đầu chỉ đọc BE nên 6 cột bị xếp "chưa kết luận"; đọc thêm FE (`hrm-client`) thì cả 6 đều
  kết luận được và lộ thêm 1 cột nữa. Không còn cột nào chờ quyết định.
  Spec: docs/superpowers/specs/gop-db/2026-08-04-fix-employee-fk-remap-design.md | Tóm tắt: .plans/gop-db/fix-employee-fk-remap/design.md

- customer-cut-mysql2 → .plans/gop-db/customer-cut-mysql2/plan.md
  Trạng thái: **HOÀN TẤT + ĐÃ TEST** (2026-08-01, nhánh `gop_db`). Khách hàng còn ĐÚNG 1 luồng `/assign/customers`.
  Gồm: cắt hết `mysql2` khỏi luồng KH (35 file) · xoá 6 bảng `hrm_customer_*` + migration `2026_08_01_000001_drop_hrm_customer_tables` (đã test round-trip) ·
  gỡ toàn bộ tầng sync 2 chiều · xoá màn `/human/customers` + `/timesheet/setting/customers` · chuyển 10 picker sang luồng mới · thêm `GET assign/customers/search`.
  Test: 52/52 endpoint HTTP + 12 màn browser + luồng ghi (tạo/sửa/thêm liên hệ, có rollback). **7 lỗi thật đã sửa** (xem plan.md Phase 11-12).
  ⚠️ Đọc trước khi làm tiếp trên nhánh này: `.plans/gop-db/design.md`.

## Hoàn thành

- form-validate-base → @khoipv → .plans/gop-db/form-validate-base/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-14)**, nhánh `gop_db`. Sửa **base** để gắn được
  `v-validate` (vee-validate v2) thẳng lên `V2Base*` ở mọi màn → lỗi hiện **realtime**, không phải
  bấm Lưu mới biết.
  2 mixin mới: `utils/mixins/v2ValidateMixin.js` (khai `$_veeValidate.name()/.value()` + prop
  `invalid`) và `utils/mixins/formValidateMixin.js` (gộp lỗi FE realtime + lỗi BE 422 vào
  `fieldError()` / `hasFieldError()` / `validateForm()` / `applyServerErrors()`).
  7 component đã gắn: Input, Textarea, Select, SelectInModal, SelectRemote, DatePicker, CurrencyInput.
  ⚠️ Phát hiện kèm: `:class="{'is-invalid':…}"` truyền vào `V2Base*` trước nay **không đổi màu viền**
  (class rơi vào thẻ bọc, Bootstrap chỉ style `.form-control.is-invalid`) → nay base tự tô.
  Màn mẫu: **Gói bảo dưỡng** — theo skill `form-validate`, FE chỉ còn `required` ô **Tên**; Mã /
  Công ty / file / ma trận để BE trả 422.
  **Đợt 2 (cùng ngày)**: nhân ra **14 màn gop-db còn lại** (8 Finance + 5 CSKH + `/human/banks`;
  Serial không có form nên không phải sửa). Mỗi màn: bỏ chặn required tự viết (trừ ô Tên) và bê
  rule ĐỊNH DẠNG của BE sang FE. **Message FE viết đúng nguyên văn message BE** (user chốt) — lấy từ
  `FormRequest::messages()`, thiếu thì lấy `hrm-api/resources/lang/vi/validation.php`.
  Thêm 7 rule vào `plugins/vee-validate.js` (**thuần thêm, không sửa rule cũ** — user chốt giữ
  `max:255` với câu cũ): `number_only`, `min_value`, `max_value_decimal`, `digits_between`,
  `number_vn`/`positive_vn`/`max_value_vn` (ô Tỷ giá nhập định dạng VN `26.520,00`) + dictionary
  `custom` cho 3 trường có câu chữ riêng.
  ⚠️ Ngoại lệ giữ lại 1 chặn required: `device_error_costs.price`/`price_service` — BE khai
  `nullable` nhưng cột NOT NULL, gửi rỗng nổ SQL 1048 (500) chứ không phải 422.
  Verify: parse 25 file + `vi.json`; nạp thật thân hàm rule bằng `vm` chạy 20 case → 20/20 đúng.
  **Đợt 3 (cùng ngày)**: đối chiếu **Checklist chuyển đổi ERP =>> HRM.xlsx** trên Drive
  (sheet "Chi tiết chức năng", lọc `Đã test` = **23 màn**) → đợt 2 mới phủ 16, bổ sung nốt
  **6 màn Danh mục địa chỉ** (Quốc gia / Khu vực / Tỉnh-TP / Quận-Huyện / Phường-Xã / Đường-Phố)
  → phủ **22/23**, còn `/assign/customers` user chốt để sau.
  ⚠️ Đổi hướng về message: thay vì truyền câu lỗi vào rule FE, **chuẩn hoá BE** (user chốt) —
  14 FormRequest bỏ message riêng theo trường, dùng câu chung đúng bằng câu FE nói
  (`Phải là số` · `Không được nhỏ hơn :min` · `Tối đa :max` · `Chỉ được nhập chữ số, từ :min đến :max chữ số`
  · `max` chuỗi để rơi về lang vi `Vui lòng nhập tối đa :max ký tự.`). Xoá hẳn dictionary `custom`
  theo tên trường ở FE (vee-validate chỉ có 1 dictionary toàn cục, `name`/`code`/`note` trùng nhau
  ở hàng chục màn). Giữ override của `unique`/`exists`/`in`/`not_in`/closure.
  📌 Vá luôn 1 lỗi cũ: `AccountRequest` báo "từ 3 đến **10** chữ số" trong khi hằng số là **15**.
  Verify: parse 31 file FE + `vi.json`, `php -l` 15 file BE, chạy lại 20 case rule → 20/20 đúng.
  **Đợt 4 (cùng ngày)**: làm nốt màn **Danh mục khách hàng** (`CustomerForm.vue`, dùng chung 5 màn)
  → **phủ đủ 23/23 màn** của checklist. Màn này trước đó KHÔNG có validate FE nào.
  Ô top-level dùng `v-validate` (`fullname` là ô Tên duy nhất có `required`; email / mã số thuế /
  SĐT / độ dài / ngày không tương lai); khối LẶP (SĐT, người đại diện, người liên hệ) dùng hàm
  `validateRepeatBlocks()` + watcher deep vì tên field phải trùng key BE theo chỉ số.
  Thêm 3 rule `phone_number` (regex `^(0)[0-9]{9,11}$` — rule `phone` cũ chỉ nhận đúng 10 số),
  `tax_code`, `not_future`. Chuẩn hoá message `SaveCustomerRequest` + `UpdateCustomerRequest`.
  ✅ Gỡ được ngoại lệ duy nhất còn lại: BE đã vá `costs.*.price`/`price_service` thành
  `required|numeric|min:0` → màn Lỗi thiết bị bỏ chặn bỏ trống ở FE. Nay FE chỉ chặn bỏ trống ô Tên.
  ✅ User đã test trình duyệt đủ **23/23 màn** (2026-08-14).
  Còn lại (không chặn hoàn thành): PR cập nhật `.claude/skills/form-validate/SKILL.md`
  (bỏ `data-vv-value-path`).
  Spec: docs/superpowers/specs/gop-db/2026-08-14-form-validate-base-design.md | Tóm tắt: .plans/gop-db/form-validate-base/design.md

- finance-bill-income-request → @khoipv → .plans/gop-db/finance-bill-income-request/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-14)**, nhánh `gop_db`.
  Xong toàn bộ 7 phase (BE + FE), đã verify.
  FE (9 file mới + 1 file menu): danh sách · chờ duyệt · thêm/sửa · chi tiết + Không duyệt · in ·
  3 popup (hợp đồng bán / hợp đồng mua / nhà cung cấp). Màn chờ duyệt DÙNG LẠI màn danh sách qua prop
  `pendingMode` để 2 màn không bao giờ lệch cột/bộ lọc.
  Verify: contract FE↔BE tự động (endpoint · field đọc · field gửi · fail-closed) 0 vấn đề ·
  vòng đời phiếu chạy bằng ĐÚNG payload FE dựng 13/13 đạt · Playwright mở thật 4 màn **0 lỗi console** ·
  màn in đo theo skill `print-page`: tràn mép phải **0px**, viền đủ 4 cạnh, logo tải được.
  🐛 **Lỗi thật bắt được khi test**: màn chờ duyệt đá về 404 với **Super admin** —
  `middleware/checkPermission.js` chỉ so tên quyền trong store, KHÔNG có nhánh bỏ qua cho super admin,
  trong khi BE cho phép. Role 18 giữ 2.148 quyền api nhưng thiếu 5 quyền mới → đã gán qua seeder.
  🐛 **Lỗi thứ 2 — user phát hiện khi review**: form/chi tiết ban đầu chép khuôn từ
  `ProductTransferRequestForm.vue` chứ không bám màn mẫu khách hàng như đã dặn. Các class
  `form-card` / `form-header` / `readonly-cell` **KHÔNG có trong `v2-styles.scss`** (chỉ có trong
  `<style>` riêng của màn đó) → 2 màn render bằng div trơn, mất hết khung. **Đã sửa** sang đúng khuôn
  `CustomerForm.vue`: `.card` + `card-header py-2` + `<h6>` · `<Required />` · `text-small-error` ·
  `V2BaseInput :disabled`. Đo Playwright khớp 100% với `/assign/customers/add`
  (card bg/#viền/radius/margin, header bg `rgb(237,239,241)`, h6 12px).
  📌 **Bài học chung**: chép khuôn từ màn khác thì phải kiểm class nằm ở `v2-styles.scss` (dùng chung)
  hay ở `<style>` riêng của màn đó — chép template mà bỏ style là mất sạch giao diện.
  🔁 **Đợt sửa 3 (user yêu cầu "form giống form ERP")**: dựng lại bố cục + luồng nhập theo
  `form.blade.php` của ERP — 2 cột `col-md-6`, Loại tiền + Tỷ giá chung 1 cột, tỷ giá có addon **VND**,
  bỏ ô "Người nộp tiền" (ERP không có), bảng chỉ hiện sau khi chọn Loại thu, **header bảng 2 tầng**
  (cột tiền tách đôi khi ngoại tệ), nút **+** thêm dòng ở header bảng, và **chọn khách hàng + hợp đồng
  THEO TỪNG DÒNG** bằng ô readonly + kính lúp.
  ⚠️ Chọn theo dòng là yêu cầu DỮ LIỆU chứ không phải thẩm mỹ: đếm trên DB thật có
  **1.128/2.411 phiếu (46%) gom từ 2 khách hàng trở lên**, cao nhất 25 KH/phiếu — mô hình 1 KH/phiếu
  không nhập nổi gần nửa số phiếu thực tế.
  ⚠️ Ghi nhận khi chốt hoàn thành (user chốt không cần làm thêm): **không** đối chiếu trực tiếp trên
  **giao diện ERP** (thiếu môi trường + tài khoản ERP) và chỉ test **3/4 cấp quyền**
  (super admin / kế toán / không quyền).
  📌 Ghi nhận không sửa: `ChooseErpCustomerModal.vue` có cảnh báo Vue "computed 'fields' đã định nghĩa trong data" —
  lỗi CÓ SẴN của component dùng chung, hiện ở mọi màn nhúng nó.
  Phase 3 (3 endpoint popup): `search-contracts` UNION 3 nguồn (hrm_contracts thay firm_contracts + HĐ đầu kỳ
  + HĐ bảo dưỡng) — total khớp SQL thuần, loại đúng HĐ HRM status 2/3, không còn dòng FirmContract nào;
  `search-buy-contracts` UNION 5 nguồn — NCC 127 ra 19 dòng, chia đúng từng nguồn 11/5/2/1/0 khớp SQL;
  `search-suppliers` 9.547 dòng = đúng `is_supplier=1`, không lọt khách hàng thường.
  ⚠️ Bẫy đã tránh: gọi `where()` thẳng trên builder UNION thì điều kiện **chỉ dính nhánh đầu tiên** →
  phải bọc `fromSub()` rồi mới lọc. Tên bảng/cột đối chiếu `information_schema` trước khi viết (plan ghi
  thiếu: `wr_service_contracts` CÓ `total_after_vat`, `opening_contracts` KHÔNG có `status`).
  📌 Tham số `has_dept=1` popup ERP gửi là **tham số chết** (grep toàn repo ERP không nơi nào dùng) → không port.
  Phase 2 (BE ghi): tạo/sửa/xoá nháp · gửi duyệt · Không duyệt — 12 nhóm kiểm thử HTTP đều đạt.
  Siết validate mạnh hơn ERP (7/7 ca xấu bị 422: `status=4` lách sang "Đã hạch toán", `object_type` lạ,
  `exchange_rate=0`, `details` rỗng…); 403 đúng chỗ khi người khác sửa/xoá; thông báo gửi duyệt tới
  **29 kế toán cùng công ty**, nội dung đúng chuẩn `notification-convention`
  (`[DNTT] Chờ duyệt: <b>{mã phiếu}</b>. Người đề nghị: … Số tiền: …` + deep-link kèm ID).
  📌 **Seeder dữ liệu test** (user chốt 2026-08-14): `Modules/Finance/Database/Seeders/BillIncomeRequestTestDataSeeder.php`
  — mặc định DRY-RUN, chạy thật bằng `FINANCE_TEST_DATA=1`. Đã sinh 8 hợp đồng HRM `HĐ-TEST-DNTT-01..08`
  (dựng từ báo giá thật; 6 cái đúng tập trạng thái popup + 2 cái phải bị loại) · 2 phiếu mẫu `TEST.DNTT.*` ·
  gán 5 quyền HRM mới cho đúng role đang giữ quyền ERP cùng tên (23 dòng `role_has_permissions`).
  Phase 1 (BE nền: entity + morphMap + list/show): 15 file mới + 3 file sửa ở `hrm-api`.
  `GET /v1/finance/bill-income-requests` trả **2.398/2.411 phiếu ERP** (ẩn đúng 13 nháp của người
  khác), `/pending` lọc đúng công ty kế toán, `/{id}` trả đủ chi tiết — **7562/7562 dòng resolve
  được hợp đồng qua morphMap**, công nợ khớp 100% SQL thuần. 5 quyền mới id 1148-1152 đã INSERT DB dev.
  ⚠️ **Quyết định đáng nhớ**: KHÔNG dùng middleware `checkPermission` cho nhánh kế toán — nó resolve
  quyền qua spatie `getAllPermissions()` (lọc `model_type`), mà **1.252/1.691 dòng `employee_has_roles`
  trên DB gộp là `model_type='App\Employee'` (từ ERP)**; đo thật: 2/2 kế toán có quyền đều bị spatie
  trả `false` → middleware 403 oan. Gate bằng `BillIncomeRequest::isAccountant()` query thẳng pivot
  (tiền lệ `ProductTransferRequestController::reject()`).
  📌 3 chỗ **plan/spec ghi sai, đã sửa khi làm**: `Supplier` là bảng `customers` + `is_supplier=1`
  (bảng `suppliers` có thật nhưng 0 dòng) · `Modules\Assign\Entities\Customer` không tồn tại →
  `App\Models\TpCustomer` · filter `customer_name` của ERP là code chết (gọi quan hệ `customer()`
  không khai) → lọc qua `details.customer`.
  🐛 Tự phát hiện & sửa: `canView()` fail-open khi chưa đăng nhập (`approved_id == auth()->id()`
  với cả 2 vế NULL → true).
  ⚠️ **`hrm_contracts` đang 0 dòng trên DB dev** → Phase 2/3 chưa có hợp đồng HRM để test popup + tạo phiếu.
  Cần user chốt: có gộp 3 method quyền của `ProductTransferRequest` sang trait mới
  `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php` không (sửa code đang chạy).
  Bước tiếp: **Phase 2 — BE ghi** (store/update/destroy/changeStatus + thông báo gửi duyệt).
  ---
  Plan 7 phase / 20 task. Port màn ERP
  "Phiếu đề nghị thu tiền" (`admin/income-expenditure/bill_income_requests`) sang HRM phân hệ
  **Tài chính** (slot xám `finance.js:46` / `:82` / `:403`).
  Chốt: dùng chung bảng ERP (không đổi schema) · giữ logic ERP 1:1, chỉ đổi nguồn hợp đồng
  `firm_contracts` → **`hrm_contracts`** · công nợ vẫn đọc `account_details` TK 1311/3311
  (HĐ HRM sẽ hiển thị 0 tới khi có hạch toán) · giữ cả 2 loại thu · bỏ nhánh HĐ nguyên tắc +
  phân bổ phiếu YCXH · 5 quyền mới id 1148–1152 guard `api` · **không đụng repo ERP**.
  Màn Phiếu thu sẽ port ở feature sau → đợt này chưa có nút "Tạo phiếu thu".
  ⚠️ Rủi ro chấp nhận: phiếu do HRM tạo mở bên ERP sẽ lỗi `Class not found` (ERP không có class
  trỏ `hrm_contracts`).
  Base UI danh sách bám `pages/assign/customers/index.vue`.
  Spec: docs/superpowers/specs/gop-db/2026-08-13-finance-bill-income-request-design.md | Tóm tắt: .plans/gop-db/finance-bill-income-request/design.md

- device-errors-load-data → @khoipv → .plans/gop-db/device-errors-load-data/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-13)**, nhánh `gop_db`.
  Màn `customer-care/device-errors` vào là hiện "Không có dữ liệu phù hợp bộ lọc." dù bảng có 2768 dòng:
  `mounted()` `await loadOptionsData()` (2 API dropdown tuần tự ~8s) TRƯỚC `loadData()`, mà `loading`
  khởi tạo `false` nên bảng in nhầm empty text trong lúc chờ. Sửa 1 file FE: `loading: true`,
  `loadOptionsData()` chạy nền, 2 request options gọi song song. Không đụng BE.
  Spec: docs/superpowers/specs/gop-db/2026-08-13-device-errors-load-data-design.md | Tóm tắt: .plans/gop-db/device-errors-load-data/design.md

- pagination-100-rows → @khoipv → .plans/gop-db/pagination-100-rows/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-13)**, nhánh `gop_db`.
  Thêm option **100** vào ô "Số dòng/trang" cho các màn đã chuyển sang HRM ở phần gop-db.
  Khảo sát ra **1 điểm sửa duy nhất**: default prop `pageSizeOptions` của `components/V2BaseDataTable.vue`
  (`[5,10,20,50]` → `[5,10,20,50,100]`) — 16 màn gop-db (8 finance + 6 customer-care +
  `/assign/customers` + `/human/banks`) đều dùng default này, không màn nào tự truyền list thiếu 100.
  `V2BasePagination` và 3 modal tìm kiếm gop-db đã có sẵn 100 từ trước.
  ⚠️ User chốt sửa thẳng **component dùng chung** (93 file đang dùng, 75 file ngoài gop-db cũng có thêm 100)
  thay vì truyền prop 16 chỗ — chỉ THÊM option, không màn nào mất lựa chọn cũ. Giữ option `5` để user
  đang để 5 dòng/trang không bị select lệch giá trị.
  BE **không phải sửa dòng nào** (đã soát thật): phần lớn endpoint truyền thẳng `per_page` vào
  `paginate()`; 3 chỗ cap `min(100, …)` (`DeviceErrorController:303`, `ServiceService:484`/`:719`)
  thì 100 đúng bằng trần nên vẫn lọt; `/human/banks` dùng param `limit` (FE-BE khớp, không cap).
  ⚠️ Muốn thêm option `200`/`500` sau này thì 3 chỗ cap đó sẽ âm thầm ghim lại 100 → phải sửa BE trước.
  📌 Ghi nhận: repo có **2 component phân trang song song** với default lệch nhau
  (`V2BaseDataTable` `[5,10,20,50]` vs `V2BasePagination` `[10,20,50,100]`) — đợt này không gộp;
  ai sửa phân trang lần sau nhớ có 2 nơi.
  Spec: docs/superpowers/specs/gop-db/2026-08-13-pagination-100-rows-design.md | Tóm tắt: .plans/gop-db/pagination-100-rows/design.md

- customer-date-no-future → @khoipv → .plans/gop-db/customer-date-no-future/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-13)**, nhánh `gop_db`.
  Chặn chọn/nhập **ngày tương lai** ở 3 ô ngày màn KH `/assign/customers`: Ngày cấp (`grant_date`),
  Sinh nhật KH (`date_of_birth`), Sinh nhật người liên hệ (`contacts[].date_of_birth`) — hôm nay vẫn hợp lệ.
  Chặn **2 lớp** vì `V2BaseDatePicker` để `editable` mặc định `true` (xám lịch thôi là gõ tay vẫn lọt):
  FE thêm method `disableFutureDate()` + prop `:disabled-date`; BE thêm `before_or_equal:today`
  vào `SaveCustomerRequest` + `UpdateCustomerRequest` kèm 6 message tiếng Việt.
  📌 **KHÔNG phải sửa component dùng chung**: `V2BaseDatePicker` đã khai sẵn prop `disabledDate`
  (`Function`, mặc định `() => false`) truyền thẳng xuống `vue2-datepicker` → màn nào cần chặn ngày
  chỉ việc truyền prop, khỏi đụng file dùng chung của ~93 màn.
  Sửa 1 chỗ `CustomerForm.vue` → 5 màn cùng ăn (add · edit · chi tiết · quản lý KH · modal thêm nhanh).
  📌 2 ô của KH nằm trong khối `v-if="form.customer_type == 1"`, khớp đúng nhánh rule BE cho KH cá nhân.
  Không migration, không quyền mới, **không đụng dữ liệu cũ** — KH đang có ngày tương lai vẫn hiện
  bình thường nhưng lần sửa sau sẽ bị BE chặn tới khi user sửa lại ngày.
  Verify tự động: compile template + parse script, `php -l`, chạy thật `disableFutureDate` (hôm nay
  false / mai true) và Laravel Validator (hôm nay + null PASS, mai FAIL đúng 3 trường, message tiếng Việt).
  ⚠️ Lưu ý vận hành: `before_or_equal:today` so theo timezone app Laravel, không phải timezone trình duyệt.
  Ngoài phạm vi (user chốt): ô ngày ở các màn khác (hồ sơ nhân sự, hợp đồng…).
  Spec: docs/superpowers/specs/gop-db/2026-08-13-customer-date-no-future-design.md | Tóm tắt: .plans/gop-db/customer-date-no-future/design.md

- chuyen-menu-nhom-giai-phap → @khoipv → .plans/gop-db/chuyen-menu-nhom-giai-phap/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong (2026-08-12)**, nhánh `gop_db`.
  **Không test Playwright** (user chốt) — chất lượng dựa vào bộ check tự động nạp thật module menu;
  user rà bằng mắt lúc tiện.
  Đưa 2 mục menu **Nhóm giải pháp** (`/assign/solution-groups`) + **Ứng dụng** (`/assign/application`)
  từ Bán hàng (Danh mục → Dự án - Giải pháp) sang phân hệ **Danh mục dùng chung**, thành 2 mục
  cấp 1 phẳng đứng sau Nhóm ngành. Cùng khuôn với `chuyen-menu-nhom-nganh` làm trước đó cùng ngày.
  Phạm vi user chốt: **CHỈ menu** — 3 file `hrm-client`: `subsystem-menu/sale-hub.js` (bỏ 2 mục,
  nhóm còn 4), `subsystem-menu/sale.js` (bỏ 2 gate quyền đã thành code chết),
  `subsystem-menu/master-data.js` (thêm 2 mục, giữ nguyên link + 4 tên quyền cũ,
  icon `ri-lightbulb-line` / `ri-apps-2-line`). **Giữ nguyên route, code FE/BE, quyền/seeder/DB.**
  4 mục còn lại của nhóm `Dự án - Giải pháp` (Hạng mục / Giai đoạn / Vai trò dự án / Lý do thất bại)
  ở lại Bán hàng theo yêu cầu.
  ✅ Hệ quả tốt: 3 link chéo giữa các màn (`industry-groups → solution-groups`,
  `industry-groups → application`, `solution-groups → application`) giờ nằm **cùng 1 phân hệ**
  → hết cảnh bấm sang là nhảy về sidebar Bán hàng.
  **Phase 4 (cùng ngày) — thử rồi HOÀN TÁC**: user yêu cầu "chuyển tiếp menu Loại hình hoạt động
  kinh doanh khách hàng" — khảo sát ra màn `/assign/customer-scope-groups` **đã ở Danh mục dùng chung
  từ trước**, chỉ nằm trong nhóm cấp 2 `Đối tác` → tách lên cấp 1, sau đó **user đổi ý: giữ nguyên ở
  nhóm Đối tác** → đã trả về y nguyên bản gốc (`git diff` vùng đó rỗng, nhóm Đối tác đủ 8 mục).
  📌 Lần sau **không đề xuất tách mục này lên cấp 1**.
  ⚠️ Nợ giữ nguyên như đợt Nhóm ngành: 4 quyền vẫn `group = 'Danh mục'` → màn Phân quyền vẫn
  xếp ở tab Giao việc › Danh mục (đổi mỗi `type` là vô ích hoặc kéo nhầm cả nhóm quyền Giao việc).
  Verify: mini-loader Node nạp thật `subsystems.js` + `hub.js` + 3 file menu → `resolveSubsystem()`,
  `deriveHubNavLinks()`, `hubNavLinksFor()` (4 kịch bản quyền), đối chiếu khai trùng link + icon.
  📌 Bẫy khi test: tài khoản dev đang đăng nhập có **0 quyền** → `middleware/checkPermission.js`
  đẩy mọi màn gated về `/pages/extras/404`.
  Spec: docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-giai-phap-design.md | Tóm tắt: .plans/gop-db/chuyen-menu-nhom-giai-phap/design.md

- chuyen-menu-nhom-nganh → @khoipv → .plans/gop-db/chuyen-menu-nhom-nganh/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong (2026-08-12)**, nhánh `gop_db`.
  Đưa mục menu **Nhóm ngành** (`/assign/industry-groups`) từ phân hệ Bán hàng (Danh mục →
  Danh mục chung) sang phân hệ **Danh mục dùng chung**, thành mục cấp 1 phẳng đứng sau Ngân hàng.
  Phạm vi user chốt: **CHỈ menu** — 3 file ở `hrm-client`: `subsystem-menu/sale-hub.js` (bỏ mục),
  `subsystem-menu/sale.js` (bỏ gate quyền đã thành code chết), `subsystem-menu/master-data.js`
  (thêm mục, giữ nguyên link + 2 tên quyền cũ). **Giữ nguyên route, code FE/BE, quyền/seeder/DB.**
  Không phải sửa gì thêm vì `resolveSubsystem()` map route → phân hệ theo link khai trong menu,
  `default-sidebar.vue` chọn sidebar hub theo `HUB_SUBSYSTEMS` (master-data đã có sẵn),
  `deriveHubNavLinks()` tự biến mục cấp 1 phẳng thành nút rail.
  ⚠️ **Quyết định đáng nhớ**: KHÔNG đổi `type` quyền 983/998 sang phân hệ mới — `Permission.vue`
  gom khối **chỉ theo tên `group`**, mà 983/998 dùng chung group `Danh mục` với 29 quyền Giao việc
  → đổi mỗi `type` là vô ích hoặc kéo nhầm cả 29 quyền sang tab khác. Hệ quả chấp nhận:
  màn Phân quyền vẫn xếp 2 quyền này ở tab Giao việc › Danh mục.
  Test: Playwright xác minh trong app đang chạy (Bán hàng còn 3 mục ở "Danh mục chung";
  Danh mục chung có `Nhóm ngành → /assign/industry-groups`, ẩn đúng khi thiếu quyền;
  `/human/banks` không vỡ) + user tự test nốt phần cần tài khoản có quyền.
  📌 **Bẫy khi test**: tài khoản dev đang đăng nhập có **0 quyền** → mọi màn gated bị
  `middleware/checkPermission.js` đẩy về `/pages/extras/404`, kể cả màn không đụng tới.
  Spec: docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-nganh-design.md | Tóm tắt: .plans/gop-db/chuyen-menu-nhom-nganh/design.md

- customer-history → @khoipv → .plans/gop-db/customer-history/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-12)**, nhánh `gop_db`.
  Lịch sử thay đổi khách hàng cho `/assign/customers` ở **cả màn danh sách và màn chi tiết**, dùng lại
  base của báo giá: endpoint chung `GET /assign/system-logs/{type}/{id}` (thêm `type=customer`) +
  `SystemLogService` (adapter `customerLogs()` map về DTO dùng chung) + modal timeline cũ ĐỎ → mới XANH.
  Chốt với user: track **tất cả** (cột `customers` + danh sách con: người liên hệ / người đại diện /
  TK ngân hàng / nhóm KH / loại hình / lĩnh vực / hãng xe / địa điểm giao hàng + ảnh, video, tài liệu);
  action `create` (gồm import Excel) · `update` · `update_media` · `lock` · `unlock`; KH cũ chưa có log →
  dựng 2 dòng từ cột audit; **không permission riêng**.
  BE: bảng mới `customer_history` (subset-diff, snapshot lưu **giá trị hiển thị** chứ không lưu id) ·
  `CustomerHistoryService` · hook trong `CustomerService::save/setStatus/updateMedia/deleteAttachmentFile`.
  FE: **màn danh sách** — nút icon `ri-history-line` trong cột thao tác mở
  `components/assign/customer/CustomerHistoryModal.vue`; **màn chi tiết** — dùng base dùng chung
  `components/assign/SystemInfoSection.vue` (`entity-type="customer"`) đặt DƯỚI CÙNG form, đúng như
  màn chi tiết Task (thu gọn mặc định, lazy load, badge số dòng + Làm mới). Chỉ render khi
  `readonly && !modalMode` nên nhánh thêm/sửa/quản lý KH không đổi; `V2Footer` giữ Sửa · Quay lại.
  Ghi nhận 1: endpoint lịch sử không kiểm tra phạm vi xem KH (đúng quyết định "không quyền riêng") —
  cần siết thì thêm `isVisible()` vào adapter.
  Ghi nhận 2 (phát hiện khi user test): KHÔNG track 4 trường màn KH không có ô nhập nhưng luồng lưu
  vẫn ghi đè — `district` (`CustomerForm.buildPayload()` gửi cố định `district_id: null` vì đã bỏ cấp
  huyện ⇒ **mỗi lần lưu KH cũ là xoá luôn Quận/Huyện trong DB**), 2 hạn mức công nợ, và
  `type_calculate_interest`. Thêm `SystemLogService::CUSTOMER_HIDDEN_FIELDS` để log đã sinh trước đó
  cũng không hiện dòng rác.
  Spec: docs/superpowers/specs/gop-db/2026-08-11-customer-history-design.md

- customer-lock → @khoipv → .plans/gop-db/customer-lock/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-12)**, nhánh `gop_db`.
  Khóa / Mở khóa khách hàng cho `/assign/customers`, tương đương ERP
  (`Sale\CustomersController@delete` / `@unlock`): khóa = `customers.status = 0`, mở khóa = `1`,
  **không** chặn điều kiện nghiệp vụ (ERP `canDelete()` luôn true), gate bằng **quyền ERP
  `Xóa khách hàng`** (FE đã có sẵn `perm.delete`) → không thêm permission, không migration.
  BE: `CustomerService::setStatus()` (set `updated_by` tường minh bằng ERP employee id — BaseModel
  tự gán sẽ ra HRM user id, sai hệ id) · `CustomerController::lock/unlock` ·
  2 route `POST /assign/customers/{id}/lock|unlock` (ERP dùng GET, HRM đổi sang POST).
  FE `pages/assign/customers/index.vue`: nút `ri-lock-line`/`ri-lock-unlock-line` đặt trong **cột
  Trạng thái** cạnh badge — theo khuôn màn danh mục `finance/currencies` (user chốt vị trí này) —
  + `BaseConfirmModal` xác nhận → gọi API → toast → `loadData()` giữ trang/bộ lọc.
  ⚠️ PHÁT HIỆN LÀM GỌN PHẠM VI: popup chọn KH của form Dự án TKT / Meeting / Phiếu chuyển hàng dùng
  chung `components/modals/ChooseErpCustomerModal.vue` và **đã lọc `status: 1` sẵn** → chỉ còn ô
  "Công ty mẹ" (`CustomerService::parentOptions()`) phải thêm `where status = 1`. 21 chỗ còn lại lấy
  danh sách KH đều là **ô lọc** → giữ nguyên (user chốt: ô lọc vẫn hiện KH khóa để tra cứu dữ liệu cũ).
  Ghi nhận không sửa: `filteredCustomers` trong `pages/assign/meeting/components/GeneralInfo.vue` là
  code chết (gán nhưng không render).
  Spec: docs/superpowers/specs/gop-db/2026-08-11-customer-lock-design.md
- customer-care-service-price-config → @junfoke → .plans/gop-db/customer-care-service-price-config/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-12)**, nhánh `gop_db`.
  Chuyển "Cập nhật nhanh giá dịch vụ" từ ERP sang **CSKH** — 1 form 2 trường lưu vào
  `service_price_config` (1 dòng) + ghi đè hàng loạt 207 gói bảo dưỡng / 242 cấp dịch vụ,
  2 route `/v1/customer-care/service-price-config`. Màn danh mục thứ 6 của phân hệ.
  ⚠️ GOTCHA: **quyền ERP dùng guard `web`, HRM dùng guard `api`** — FE chỉ nạp quyền guard api nên
  gate menu bằng tên quyền ERP sẽ đá về 404, `checkPermission` ở BE cũng luôn 403. Cách làm: thêm
  quyền api **1130** trùng tên + gate route bằng **`erpPermission`**. Bấm Lưu **ghi đè hệ số +
  định mức cho MỌI gói**, kể cả gói đã chỉnh riêng → đã thêm popup xác nhận nêu rõ số gói.
  Spec: docs/superpowers/specs/gop-db/2026-08-06-customer-care-service-price-config-design.md | Tóm tắt: .plans/gop-db/customer-care-service-price-config/design.md

- customer-column-config → @khoipv → .plans/gop-db/customer-column-config/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-11)**, nhánh `gop_db`.
  Nút **Cấu hình cột hiển thị** cho `/assign/customers` (ẩn/hiện + kéo thả thứ tự, lưu theo user),
  tương đương "Tùy chỉnh cột" của ERP nhưng lưu DB thay vì localStorage.
  Dùng lại hạ tầng sẵn có: `components/modal/column-customization-modal.vue` + API `human/column-customizations`.
  Chốt: **18 cột** = 10 cột cũ + 8 cột ẩn của ERP (Tên đơn vị, Tên viết tắt, Địa chỉ xuất HĐ, Công ty mẹ,
  Hãng xe, Cấp đại lý, Người tạo, Người sửa — mặc định ẩn) · **khoá** STT + Mã KH-Tên KH bằng cách
  KHÔNG truyền vào modal (tránh sửa component dùng chung của 20+ màn) · cột Nhóm KH khi đó để tạm `'—'`
  (**đã nối dữ liệu thật ở việc `customer-form-group`, 2026-08-10**) ·
  file xuất CSV/Excel giữ bộ cột cố định.
  Migration thêm cột JSON `customers` vào `column_customizations` (đã chạy) + cast Entity.
  ⚠️ GOTCHA 1: 4 cột Công ty mẹ/Hãng xe/Người tạo/Người sửa cần 5 leftJoin → `COUNT` phân trang chậm
  ~3,7 lần (42.077 KH: 0,12s→0,43s). `index()` dùng chung với popup chọn KH nên gate sau cờ
  **`with_extra_columns`**; FE chỉ gửi khi user thực sự bật ≥1 trong 4 cột; `exportQuery()` tự join.
  ⚠️ GOTCHA 2: modal chung dùng `b-form-checkbox :value="column.key"` → cột hiện mặc định PHẢI khai
  `isVisible: '<đúng key>'`; để `undefined` là modal bỏ tích hết, bấm OK ẩn sạch bảng.
  Verify: 3 luồng query (popup/danh sách/export) đúng như thiết kế · round-trip lưu-đọc cấu hình ·
  17/17 check logic cột FE (nạp thẳng source computed, 4 kịch bản gồm cấu hình cũ khi thêm cột mới).
  Ghi nhận không sửa: `ColumnCustomizationService` nhét thẳng `$request->table` vào tên cột SQL, không whitelist.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-column-config-design.md

- customer-form-group → @khoipv → .plans/gop-db/customer-form-group/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-11)**, nhánh `gop_db`.
  Thêm trường **Nhóm khách hàng** (chọn nhiều, không bắt buộc) vào form KH cho giống ERP.
  Sửa ở component dùng chung `CustomerForm.vue` → 5 màn cùng có (add · edit · xem chi tiết readonly ·
  quản lý KH · modal thêm nhanh). BE chỉ thêm 2 dòng validate — pivot `customer_has_groups`,
  API `customer-groups`, `syncGroups()` và `show()->group_ids` đều đã có sẵn.
  ⚠️ Sửa kèm 1 lỗi MẤT DỮ LIỆU có sẵn: `syncGroups()` xoá-rồi-ghi vô điều kiện trong khi form chưa
  bao giờ gửi `groups` → mỗi lần sửa KH trên HRM là xoá sạch nhóm KH do ERP gán. `buildPayload()`
  giờ LUÔN gửi `groups`.
  Kèm theo: **cột "Nhóm KH" trên màn danh sách trước đây luôn hiện `—`** vì `CustomerListResource`
  hardcode placeholder (di sản của `customer-column-config`) → nối dữ liệu thật bằng subquery tương quan
  `groupNamesSql()` dùng chung cho `index()` + `exportQuery()`. Đo: COUNT 17.544 KH vẫn 308 ms
  (subquery ở SELECT nên không đụng COUNT), lấy 20 dòng 9 ms.
  Không migration, không permission mới.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-form-group-design.md

- customer-export-file → @khoipv → .plans/gop-db/customer-export-file/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-11)**, nhánh `gop_db`.
  Bổ sung 3 nút **Xuất CSV** / **Xuất Excel** / **Xuất PDF** cho `/assign/customers`, tương đương ERP
  (`Sale\CustomersController@exportCSV|exportExcel|exportPDF`).
  Chốt: Excel **tải trực tiếp** (ERP đẩy queue + gửi mail) · bộ cột giống ERP (CSV 5 cột / Excel 20 cột) ·
  quyền ERP `Xuất dữ liệu khách hàng` (thêm key `export` vào `ErpPermissionHelper`) ·
  **không giới hạn số dòng**, tối ưu bằng `FromQuery` + chunk 5.000 + select 26 cột cần thay `customers.*` (59 cột)
  + cột phụ bằng JOIN/subquery (không N+1) + `StringValueBinder` + bỏ `ShouldAutoSize` ·
  **giữ luật che SĐT** của màn danh sách trong file xuất (KH cá nhân không phải "của mình" → `-`).
  Sửa 3 lỗi của bản ERP: thiếu header *Chức vụ liên hệ* (19 th/20 td → lệch cột) · CSV không BOM UTF-8 (vỡ dấu) ·
  SĐT/MST mất số 0 đứng đầu do binder mặc định.
  Đo thực tế 17.542 KH: CSV 25,3s→~13s · XLSX 60,2s→~32s (RAM đỉnh 206 MB).
  Không migration, không thêm permission vào seeder (quyền ERP đã có sẵn, id 100074).
  **Đợt bổ sung 2026-08-10**: mẫu Excel theo chuẩn HRM (logo · tiêu đề gộp ô đậm · header nền xám có viền ·
  dữ liệu có viền · đóng băng dòng header · autofilter) → xuất 17.544 KH ~32s lên **~44s**, RAM 206→266 MB.
  Thêm **Xuất PDF**: cài `barryvdh/laravel-dompdf ^1.0` (⚠️ team phải `composer install` sau khi kéo nhánh),
  5 cột như ERP, A4 ngang, `App\PdfExport\CustomerPdfExport` dùng chung trait format với CSV/Excel.
  ⚠️ GOTCHA PDF 1: blade PHẢI đặt `font-family: "DejaVu Sans"` — font mặc định dompdf không có dấu tiếng Việt.
  ⚠️ GOTCHA PDF 2: dompdf giữ 1 Cellmap cho mỗi `<table>` → chia 200 dòng/bảng nâng trần từ ~1.000 lên
  ~3.000 dòng. **Vẫn KHÔNG xuất nổi toàn bộ 17.544 KH** (512M: 3.000 dòng = 436 MB/30,7s; 4.000 dòng vỡ).
  User chốt không giới hạn số dòng nên code không chặn → bấm Xuất PDF khi không lọc sẽ chết request
  (memory exhausted là fatal error, try/catch không bắt được).
  **CÒN NỢ (không chặn nghiệm thu, xử lý sau nếu cần)**: chọn 1 trong 3 hướng — chặn số dòng /
  nâng `memory_limit` riêng cho action / đẩy queue + mail.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-export-file-design.md

- customer-import-excel → @khoipv → .plans/gop-db/customer-import-excel/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong (2026-08-11)**, nhánh `gop_db`.
  Bổ sung Import Excel cho `/assign/customers` —
  chức năng ERP có (`Sale\CustomersController@importExcel`) mà HRM thiếu.
  Chốt: **25 cột** = 24 cột file mẫu ERP + 1 cột Lĩnh vực kinh doanh dạng cặp `MãLoạiHình:MãLĩnhVực`
  (gộp Loại hình vào chung 1 cột, đúng cách màn `/assign/application`; loại hình suy ra từ vế trái) · danh mục tra theo tên KHÔNG tự tạo mới (chung `gop_db`, tránh rác địa danh ERP) ·
  bỏ trống cột Tên = dòng con (thêm liên hệ / TK ngân hàng) · trùng MST/CCCD báo lỗi, chỉ tạo mới ·
  `V2BaseImportModal` 4 bước · import gọi lại đúng `CustomerService::save()`.
  Không migration, không permission mới (dùng `erpPermission:Thêm khách hàng`).
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-import-excel-design.md

- customer-care-serial-catalog → @junfoke → .plans/gop-db/customer-care-serial-catalog/plan.md
  Trạng thái: **CODE DONE + ĐÃ VERIFY (BE + trình duyệt)** (2026-08-06).
  Scope: chuyển "Danh mục serial thiết bị làm dịch vụ" (`serials`, 21.632 dòng) từ ERP sang **CSKH**
  — 1 màn danh sách READ-ONLY + Xuất Excel, 2 route `/v1/customer-care/serials`, quyền mới **1126**.
  Màn danh mục thứ 5 của phân hệ.
  ⚠️ GOTCHA: 7/9 route của `SerialController` ERP **không thuộc màn này** (thuộc màn Quản lý khách
  hàng, HRM đã có) → không port. Xuất Excel **dựng ở FE** (ExcelJS + fetch theo lô), BE không có
  route export vì 21 nghìn dòng dựng ở BE sẽ timeout trên server.
  Còn treo: user rà bằng mắt; chốt cách lọc 13 bản ghi `status` 0/3 (xem design.md).
  Spec: docs/superpowers/specs/gop-db/2026-08-06-customer-care-serial-catalog-design.md | Tóm tắt: .plans/gop-db/customer-care-serial-catalog/design.md

- chuyen-code-phan-he → @junfoke → .plans/gop-db/chuyen-code-phan-he/plan.md
  Trạng thái: **XONG 3 phân hệ, ĐÃ VERIFY TRÌNH DUYỆT** (2026-08-05) — giai đoạn 2 của
  `tach-phan-he-erp-hrm`: đưa **code** màn về đúng phân hệ, không chỉ menu.
  Scope: 3 phân hệ ở trạng thái "menu đã chuyển, code chưa chuyển" →
  **Danh mục chung** 10 màn (122 route `/v1/master-data/*`),
  **Bảo hiểm xã hội** 7 màn (38 route `/v1/insurance/*`),
  **Bán hàng** 27 màn qua 3 đợt — Danh mục+Thiết lập 11 → Báo cáo 8 → Dự án TKT+Phê duyệt 8
  (313 route `/v1/sale/*`). Tổng **98 cặp redirect** giữ URL cũ sống, **6 migration quyền**.
  Chốt xuyên suốt: chuyển cả 3 lớp (FE route + BE module + dọn quyền), giữ nguyên tên đoạn cuối
  route cho dễ đối chiếu, redirect vĩnh viễn ở `nuxt.config.js::extendRoutes`, verify sau mỗi đợt.
  Kèm 2 việc chuẩn hoá: **layout hub (kiểu MISA) thành chuẩn chung** cho phân hệ mới —
  sidebar + màn Tổng quan đều dùng component chung, thêm phân hệ chỉ cần khai `key` trong
  `HUB_SUBSYSTEMS`; và **tách quyền / đưa 10 quyền khách hàng về đúng phân hệ**.
  ⚠️ 3 route `/v1/assign/quotations/erp-contract/*` **cố ý giữ URL cũ** — hợp đồng tích hợp với
  codebase ERP ngoài repo, đổi là ERP gọi hỏng.
  Đã sửa 10 lỗi trong quá trình làm (6 lỗi có sẵn chặn màn + 4 lỗi tự gây) — chi tiết ở plan.md.
  Còn nợ: 7 màn địa lý-ngân hàng chưa có permission nào; bộ quyền KH cũ của HRM (id 166-169)
  còn song song, chưa quyết gộp/bỏ; verify màn Tạo phiếu BH ở môi trường có thông báo còn hiệu lực.
  Bước tiếp: các phân hệ còn lại chưa tới lượt chuyển code.
  **Phase 17-19 (2026-08-06), ĐÃ VERIFY TRÌNH DUYỆT**: chuẩn hub phủ **14/17 phân hệ** (thêm CSKH,
  Tài chính + 9 phân hệ mới); menu Tài chính gom 24 → 11 nhóm bám mega-menu `Kế toán` của ERP qua
  cờ `hubGroup`; sửa 3 lỗi có sẵn — sidebar hub không lọc quyền, `deriveHubGroups()` nuốt `erpPath`,
  icon rail hardcode túi Bán hàng.
  ⚠️ GOTCHA: gate quyền Bán hàng nằm ở `sale-hub.js::SALE_LINK_PERMISSIONS`, không phải `sale.js`.
  Còn nợ: `master-data` mới gate 2/10 màn (7 màn địa lý-ngân hàng chưa có permission nào trong DB).
  Spec: docs/superpowers/specs/gop-db/2026-08-04-chuyen-code-phan-he-master-data-insurance-design.md
  và docs/superpowers/specs/gop-db/2026-08-06-hub-menu-customer-care-finance-design.md | Tóm tắt: .plans/gop-db/chuyen-code-phan-he/design.md

- customer-care-cost-catalog → @junfoke → .plans/gop-db/customer-care-cost-catalog/plan.md
  Trạng thái: **BE + FE DONE, verify BE xong** (2026-08-03) — chuyển "Danh mục dịch vụ sửa chữa và
  chi phí khác" (`costs`, `kind_of=2`, 524 dòng) sang phân hệ CSKH. 8 route
  `/v1/customer-care/costs`, quyền 1119/1120.
  Màn này khác 3 màn trước ở 4 điểm: (1) **1 màn ERP phục vụ 3 mục menu** qua `?kind_of=`;
  (2) cột Chiết khấu nằm ở `company_costs` **theo từng công ty** — lấy theo
  `auth()->user()->current_company_role`, dùng selectSub để sort/lọc được trên SQL;
  (3) `status` là **1 = Hoạt động / 0 = Khóa**, khác các danh mục khác dùng 1/2;
  (4) xóa thực chất là **"khóa hoặc xóa"** — đã phát sinh ở báo giá/hợp đồng hãng thì chỉ set
  `status=0`. `canEdit`/`canDelete` của ERP **chặn cứng theo TÊN** ("Chi phí đi lại",
  "Chi phí vận chuyển").
  User chốt: bỏ hẳn phần đồng bộ CRM có trong model ERP; làm `kind_of=2` trước, `kind_of=1`
  (Chi phí phải trả / Chi phí bán hàng) tạm gác.
  🐛 Lỗi tự gây đã sửa: copy `prepareForValidation` từ màn Tiền tệ nên strip dấu phẩy → tỷ lệ
  `12,5` lưu thành **125**. 3 trường ở màn này đều là phần trăm (≤100) nên dấu phẩy là dấu thập
  phân → đổi `,` thành `.`.
  **Phase 5 (2026-08-03)** — cắt luôn `erp-cost-catalog` (@dnsnamdang) sang dùng luồng mới: gom
  `TpCost` thành alias `@deprecated` của `Cost` (giữ hằng cũ để nhánh kia merge vào vẫn chạy), đổi
  7 file sang `Cost`, **bỏ `mysql2` khỏi 4 file** của luồng danh mục chi phí. Phát hiện **3 lỗi
  thật**: transaction mở trên `mysql2` trong khi model ghi connection mặc định (không rollback);
  `findOrCreateCosts` insert thiếu `kind_of` NOT NULL → dòng tạo ra `kind_of=0` không hiện ở màn nào;
  `resolveOrCreateCost` ghi `type=1` cho `kind_of=2` làm lọt kiểm trùng tên. Đã ghi chú đầy đủ cho
  @dnsnamdang ở cuối `.plans/erp-cost-catalog/plan.md`.
  ⚠️ **Còn nhiều chỗ dùng `mysql2` ngoài phạm vi danh mục chi phí** (AssignBusinessController 15 chỗ,
  QuotationService, ProductProjectController…) — vẫn đọc DB ERP CŨ trên nhánh này, cần rà riêng.
  Bước tiếp: user verify bằng mắt `/customer-care/costs`.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-customer-care-cost-catalog-design.md | Tóm tắt: .plans/gop-db/customer-care-cost-catalog/design.md

- finance-product-transfer-request → @khoipv → .plans/gop-db/finance-product-transfer-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong (2026-08-07).** Code Phase 1–7 (D1–D17) + final review + fix wave, **đã commit**: `hrm-api 3a0acce08` · `hrm-client ed0abb049` (+ `690515fc4` fix bug), nhánh `gop_db`.
  Đã xong: BE (3 entity + searchByFilter phân quyền 4 cấp + CRUD + reject + notification chuông HRM + in template 87 + export Excel + 4 API phụ trợ form) · FE (list + form create/edit + chi tiết + print + menu finance.js:134) · Phase 7 (dùng chung QuotationProductSearchModal của màn báo giá, dọn conflict marker subsystems.js, `testcase.xlsx` 127 TC). Verify D12: ma trận quyền 6 nhóm × 6 action khớp SQL, Playwright toàn luồng PASS, round-trip 2 cổng tầng dữ liệu PASS, DB nguyên trạng. Ledger: sdd-progress.md.
  User đã xử lý xong (2026-08-07): verify browser bằng mắt · 5 mục "Chờ xác nhận PO" trong plan.md (thông báo cổng ERP, scope canView B1, SL lẻ, template 87, task rà quyền) · ENV DEPLOY `ERP_URL` cả 2 repo · **SQL DEPLOY đã chạy môi trường thật** (INSERT quyền 1129-1133 + `UPDATE permissions SET type = NULL WHERE id IN (100878,100879,100880,100881)`).
  ⚠️ Phát hiện quan trọng — **CHƯA mở task, còn nợ team**: middleware `CheckPermission` hỏng trên gop_db (spatie bỏ sót role gán từ ERP do model_type mismatch) → route reject của feature này phải bỏ middleware, chặn bằng `canApprove()`. Cần TASK RIÊNG rà mọi route khác đang gắn `checkPermission` + mapping quyền FE (accounts/currencies/account-banks 404 với mọi user — lỗi có sẵn của môi trường, không phải regression).
  Tồn: nội dung chốt của 5 mục PO chưa ghi ngược vào plan.md (mục "Chờ xác nhận PO / task riêng" vẫn đang để dạng câu hỏi).
  — Bối cảnh port gốc: màn ERP `admin/warehouse/product_transfer_requests?type=all`, 3 bảng, mã `PYCCH-xxxxx`, 13 trạng thái → phân hệ **Tài chính** → nhóm **Xuất hàng** (slot `finance.js:134`).
  **HRM là bản thay thế lâu dài**, 2 cổng song song cùng bảng, KHÔNG đổi schema. HRM chỉ ghi status 2↔3; 1, 4–12 do chuỗi kho ERP đẩy.
  Chốt 6 QĐ: port đầy đủ (nút Tổng hợp mở tab ERP) · dùng lại quyền ERP + "Kế toán kho" · 1 màn list duy nhất (=type=all) · form đủ popup hàng + Xem tồn + giá/ĐVT · xóa giữ ERP (status=3 + người tạo) · nới validate after:today khi sửa.
  **Đợt chỉnh 2026-08-13 (Phase 8, @khoipv) — CODE DONE, CHỜ USER TEST:** chuẩn hoá footer 2 màn
  (form `create`/`edit` + màn chi tiết) sang `V2Footer` dùng chung. Nhãn đổi theo chuẩn footer:
  "Lưu" → **"Lưu nháp"**, "In yêu cầu" → **"In"**, "Hủy" → **"Quay lại"**; nút **Lưu & Gửi duyệt giờ
  có popup xác nhận**; thứ tự nút màn chi tiết thành *Sửa · In · Không duyệt · Tổng hợp · Quay lại*
  (Tổng hợp qua slot `custom-actions`). Mất icon spinner ở 3 nút — guard chống bấm 2 lần vẫn còn trong JS.
  Spec: docs/superpowers/specs/gop-db/2026-08-05-finance-product-transfer-request-design.md | Tóm tắt: .plans/gop-db/finance-product-transfer-request/design.md

- customer-care-services-catalog → @khoipv → .plans/gop-db/customer-care-services-catalog/plan.md
  Trạng thái: **CODE DONE P1–P5, user xác nhận xong (2026-08-05)** — port trọn màn "Danh mục gói
  bảo dưỡng" (ERP `Sale\ServiceController`, `services` 207 dòng + 5 bảng con) sang
  `/customer-care/services`: BE `Modules/CustomerCare` (4 entity + ServiceRequest + ServiceService +
  resource/export + controller, 12 route), FE list + form 5 khối (ma trận bảo dưỡng × cấp, giá vốn
  theo công ty, popup hàng hóa/nhóm theo UX popup báo giá với 17 bộ lọc, đính kèm S3), in template 191.
  Phase 5: 7 cụm chỉnh theo user (bỏ cột Hành động, VAT nullable, copy giữ đính kèm, fix auto-print…).
  🐛 Đã sửa 2 lỗi CRITICAL `key_word` shape `{text}` (88/207 gói có nguy cơ hỏng màn báo giá DV ERP).
  ⚠️ Bug HỆ THỐNG chưa sửa (file chung, cần báo team): `V2BaseSelect.vue:59` rớt option id=0.
  F3 (sửa gói xóa hết dòng ma trận = no-op im lặng) giữ nguyên theo ERP — user ruling trong sdd-progress.md.
  ⚠️ **Khi DEPLOY phải chạy tay 3 SQL** (chi tiết sdd-progress.md Task 1.5): UPDATE permissions
  type=24 (101023-101025) · mirror `employee_has_roles` sang model_type HRM · INSERT
  `role_has_permissions` cho Super admin; DB local còn thiếu quyền CSKH 1115-1120 của 2 feature trước.
  Tồn: checklist "Verify tổng thể" cuối plan.md chưa tick (regression 4 màn CSKH cũ, round-trip ERP↔HRM 2 chiều).
  **Đợt chỉnh 2026-08-13 (Phase 11j-11l, @khoipv) — CODE DONE, CHỜ USER TEST:**
  · **11j** — file xuất Excel hết cảnh báo "Number stored as text" ở cột Mã: `ServiceExport` ép cả vùng
    B..F thành text + `app/ExcelExport/IgnoredErrorsPatcher.php` vá thẻ `<ignoredErrors>` vào
    `sheet1.xml` (phpspreadsheet 1.25 chưa có API `getIgnoredErrors()`; thẻ PHẢI đứng trước `<drawing>`).
  · **11k** — file Excel đổi hết "dịch vụ" → "gói bảo dưỡng" (tên file `Danh_sach_goi_bao_duong.xlsx`
    ở CẢ `index.vue` lẫn `ServiceController::export()`, tiêu đề + 4 header cột); độ rộng cột chuyển về
    khai 1 chỗ `ServiceExport::COLUMN_WIDTHS` (blade không khai `width` nữa); cột Giá tách **mỗi cấp
    dịch vụ 1 dòng** bằng `<br>` — Html Reader đổi thành `\n` và tự bật wrap.
    Tên danh mục "cấp dịch vụ" GIỮ NGUYÊN (là danh mục riêng, không đổi theo).
  · **11l** — form Thêm/Sửa dùng footer chuẩn `V2Footer` thay hàng nút tự dựng: `menu.submit_form`
    (nút Lưu), Sao chép qua slot `custom-actions`, "Hủy" → "Quay lại" (`url-back`), `.service-form`
    chừa `padding-bottom: 90px`. ⚠️ Đánh đổi user đã chốt: **nút Lưu mất icon spinner** (chống bấm 2
    lần vẫn còn ở đầu `save()`); popup "Thông tin chưa lưu" không ảnh hưởng vì nằm ở `beforeRouteLeave`
    của trang vỏ.
  Spec: docs/superpowers/specs/gop-db/2026-08-04-customer-care-services-catalog-design.md | Ledger: .plans/gop-db/customer-care-services-catalog/sdd-progress.md

- bo-sung-menu-phan-he → @junfoke (Phase 11: @khoipv) → .plans/gop-db/bo-sung-menu-phan-he/plan.md
  Trạng thái: **CODE DONE + KIỂM THỬ TỰ ĐỘNG PASS** (2026-08-03) — Phase 0-9 xong.
  **PHASE 11 (2026-08-12, @khoipv)**: dọn nhãn menu phân hệ **Danh mục chung** theo yêu cầu user —
  bỏ tiền tố "Danh mục" ở toàn bộ 15 nhãn, tách `Ngân hàng` khỏi nhóm địa lý thành **item cấp 1
  riêng** (`ri-bank-line` → `/human/banks`), nhóm địa lý đổi tên `Địa lý` (còn 6 mục),
  nhóm đối tác đổi thành `Đối tác` (bỏ "(KH - NCC)"). Chỉ đụng `subsystem-menu/master-data.js`.
  Đã verify bằng Node: `walkMenu()` thu cả link ở item cấp 1 → `resolveSubsystem('/human/banks')`
  không đổi; `/human/banks` vẫn khai đúng 1 lần; icon có thật trong `_remixicon.scss`.
  → Chốt luôn tồn đọng "Danh mục ngân hàng liệt kê ở 2 phân hệ": **chỉ giữ ở Danh mục chung**.
  Khai 355 mục menu trên 14 phân hệ theo sheet `Gộp phân hệ ERP-HRM` (10 mục link thật sang ERP, 345 mục xám mờ),
  Chỉ đụng `hrm-client`. Kiểm thử bằng cách render THẬT `Sidebar.vue`
  qua `vue-server-renderer`; regression 11 bộ menu cũ cho kết quả render-identical với bản `git show HEAD`.
  Phase 8 đã sửa trực tiếp sheet gộp (đã sao lưu bản gốc trước khi sửa).
  **PHASE 9 (2026-08-03, user đổi ý)**: Mua hàng / Kho / Vận chuyển **KHÔNG ẩn nữa** — vẫn hiện card ở màn chọn phân hệ + dropdown, bấm vào thì **điều hướng sang ERP**. Bỏ cờ `hidden`, dùng `external: true` + `erpPath`; `openERP()` ở `pages/index.vue` và `SubsystemSwitcher.vue` nhận tham số subsystem để ghép `ERP_URL + erpPath`; `getPermissionSubsystemGroups()` đổi `!s.hidden` → `!s.external` (3 phân hệ này không còn khối quyền ở màn Phân quyền, nhưng GIỮ NGUYÊN `permissionType` 20/21/22). ⚠️ **ERP không có trang landing riêng cho 3 phân hệ này** (topmenubar ERP chỉ có Danh mục/Khởi tạo/Kinh doanh/Kế toán/CSKH/QTTT) nên `erpPath` phải trỏ MÀN ĐẠI DIỆN: Mua hàng → `/admin/orders/inland_order_summary_new`, Kho → `/admin/warehouse/product_import_requests/all`, Vận chuyển → `/admin/warehouse/delivery_trips/all`. Card ERP tổng không khai `erpPath` → vẫn về trang chủ ERP.
  ⚠️ **BUG PHÁT HIỆN KHI KIỂM THỬ — CHƯA SỬA, không thuộc feature này**: sau commit `564125504 gop database khach hang`, mục "Khách hàng" ở `subsystem-menu/master-data.js` đổi link sang `/assign/customers`, **trùng** với mục "Khách hàng" nhóm Danh mục của `subsystem-menu/sale.js`. Vi phạm bất biến *mỗi link chỉ thuộc đúng 1 phân hệ* mà `resolveSubsystem()` dựa vào → mở `/assign/customers` giờ LUÔN hiện sidebar **Danh mục chung** (đứng trước trong mảng `SUBSYSTEMS`), không bao giờ ra Bán hàng. Cần bỏ 1 trong 2 mục.
  Bước tiếp: **Phase 10 — verify browser thật, CHƯA LÀM** (độ mờ mục xám, sidebar Bán hàng 184 mục / Tài chính 104 mục).
  8 gotcha + bài học (ẩn phân hệ làm khuất màn phân hệ khác, bẫy khớp dòng trong sheet, `Sidebar.vue` chỉ render `router-link`…): xem plan.md.
  Spec: docs/superpowers/specs/gop-db/2026-08-01-bo-sung-menu-phan-he-design.md | Tóm tắt: .plans/gop-db/bo-sung-menu-phan-he/design.md

- customer-care-maintenance-catalogs → @junfoke → .plans/gop-db/customer-care-maintenance-catalogs/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE)** (2026-08-03) — chuyển "Cấp dịch vụ bảo dưỡng" (`levels`)
  + "Danh mục ghi chú kiểm tra bảo dưỡng" (`note_maintenances`) từ ERP sang **phân hệ CSKH**; là 2 màn ĐẦU TIÊN của
  phân hệ này (`Modules/CustomerCare` trước đó rỗng, chưa có quyền `type=24` nào).
  BE 13 file + 16 route `/v1/customer-care`, quyền 1115-1118, FE 2 màn danh sách + 2 modal.
  Sửa 2 lỗi ERP: `levels` chỉ kiểm 1/6 bảng khi xóa, `note_maintenances` không chặn xóa gì.
  ⚠️ Phát sinh: **ERP + HRM đã gộp chung `employees` / `employee_infos`** → gỡ toàn bộ lớp map ERP employee id
  khỏi Finance + CSKH (Phase 1 trong plan.md). Còn nợ: `ErpPermissionHelper` + `Modules/Assign` vẫn qua `mysql2`.
  Bước tiếp: user verify bằng mắt `/customer-care/levels` + `/customer-care/note-maintenances`.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-customer-care-maintenance-catalogs-design.md | Tóm tắt: .plans/gop-db/customer-care-maintenance-catalogs/design.md

- finance-currency-catalog → @junfoke → .plans/gop-db/finance-currency-catalog/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE + cron)** (2026-08-03) — màn thứ 3 của phân hệ Tài chính.
  Bám sát ERP (danh sách + modal CRUD + xóa + lọc + Xuất Excel), không đổi schema `currencies`.
  8 route, quyền 1113/1114. Chuyển luôn cron tỷ giá sang HRM (`finance:update-exchange-rate`, 03:00)
  và **đã tắt lịch bên ERP** → HRM là nơi duy nhất chạy tự động.
  Sửa 4 lỗi của cron ERP, nặng nhất: đồng tiền đứng ĐẦU file XML không bao giờ được cập nhật (AUD đứng im ~16 tháng).
  ⚠️ Trước khi lên thật: `hrm-api/.env` chưa cấu hình mail nên `emailOutputTo` chưa gửi được.
  Bước tiếp: user verify bằng mắt `/finance/currencies`.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-finance-currency-catalog-design.md | Tóm tắt: .plans/gop-db/finance-currency-catalog/design.md

- finance-account-catalog → @junfoke → .plans/gop-db/finance-account-catalog/plan.md
  Trạng thái: **PHASE 1-6 + 8 CODE DONE + VERIFIED** (2026-08-01) — 2 màn "Danh mục tài khoản" +
  "Danh mục loại tài khoản" từ ERP sang phân hệ **Tài chính**; là màn đầu tiên của phân hệ nên phải dựng luôn khung
  `Modules/Finance` + `components/subsystem-menu/finance.js`.
  Port trọn bộ: CRUD + khóa/mở + lịch sử + Xuất/Import Excel + In danh sách (template DB id 459).
  26 route, quyền 1107-1110 (`type=8`). Verify HTTP thật 33 case + browser Playwright toàn luồng, DB trả nguyên trạng.
  Bước tiếp: Phase 7 đối chiếu 2 cổng (cần bật ERP local) + tạo 2 file mẫu Excel trong `hrm-client/static/`.
  Toàn bộ gotcha/bài học (4 lỗi FE khi chạy thật, 4 bài học phân trang, icon phải lấy từ codebase,
  tên `group` permission phải duy nhất…): xem plan.md.
  Spec: docs/superpowers/specs/gop-db/2026-07-30-finance-account-catalog-design.md | Tóm tắt: .plans/gop-db/finance-account-catalog/design.md

- tach-phan-he-erp-hrm → @junfoke → .plans/gop-db/tach-phan-he-erp-hrm/plan.md
  Trạng thái: **XONG GIAI ĐOẠN 1 (khung phân hệ + menu) — 2026-07-30.** Đã test thật 9 màn trên dev. Tồn: user test 17 màn edit/detail. Giai đoạn 2 (di chuyển code màn sang route mới) chưa bắt đầu — xem Phase 7 trong plan.md.
  Scope: Quy hoạch lại phân hệ ERP + HRM theo Sơ đồ tổng thể v1.6 → 24 phân hệ / 5 nhóm. Dựng base 17 phân hệ mới (BE 17 module skeleton, FE registry `components/subsystems.js` + menu + dashboard stub + icon SVG), dựng lại màn chọn phân hệ + menu chuyển nhanh, phân hệ mới đi menu dọc (`layouts/subsystem.vue`).
  ⚠️ GOTCHA: (1) mỗi link chỉ được thuộc ĐÚNG 1 phân hệ, trùng là `resolveSubsystem` trả sai. (2) layout dùng SidebarMenu phải có method `toggleMenu`, thiếu thì bấm thu gọn menu ra trang 404. (3) item menu không có `subItems` phải khai `isShow: true`, quên thì sidebar rỗng. (4) dự án nạp 2 bản Remix Icon xung đột codepoint → icon phân hệ dùng SVG tự vẽ.
  Spec: docs/superpowers/specs/gop-db/2026-07-30-tach-phan-he-erp-hrm-design.md | Tóm tắt: .plans/gop-db/tach-phan-he-erp-hrm/design.md
