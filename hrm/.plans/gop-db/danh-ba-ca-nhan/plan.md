# Danh bạ cá nhân gắn vào Nhắc việc — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **ĐÃ CODE XONG 07/11/2026** (user cho phép: hrm-api + hrm-client gop_db local, 2 migration vào db_gop_6_11, TPE_APP develop chồng working tree). CHƯA COMMIT (user tự báo). Nhật ký + 20 ruling: `execution-ledger.md` cùng thư mục.

**Goal:** Mỗi user có danh bạ riêng (Tên*, SĐT*, Địa chỉ, Ghi chú), gắn được 1 liên hệ vào nhắc việc cá nhân ngay trong form (web + app), xem lại liên hệ cùng mọi nhắc việc với họ.

**Architecture:** hrm-api thêm bảng `personal_contacts` (theo user) + cột `personal_todos.contact_id`; `PersonalContactService` lo CRUD / chống trùng theo SĐT chuẩn hoá / tra KH công ty theo đúng SĐT; form nhắc việc gửi `contact_id` hoặc `contact` (liên hệ mới) — liên hệ chỉ được tạo lúc lưu nhắc việc. Web (Nuxt 2) và app (Flutter) mỗi bên có: sheet / popup chọn liên hệ, form liên hệ mới, màn Danh bạ, chi tiết liên hệ.

**Tech Stack:** Laravel (Modules/Assign, PHPUnit feature test `DatabaseTransactions`), Nuxt 2 + Bootstrap-Vue V2 components, Flutter (TPE_APP, `fvm flutter test`), Pencil mockup.

**Spec:** `.plans/gop-db/danh-ba-ca-nhan/design.md` (đọc kèm) · mockup `meeting-mobile.pen` Nhóm ② DB-01…DB-09 (x 25400, y −1580).

## Global Constraints

- Nhánh: hrm-api + hrm-client `gop_db`; TPE_APP `develop`. App có 3 bản build: `tpeLocal` → API máy local 127.0.0.1:8000 (checkout `gop_db`); `tpeDev` → dev-hrm.eteksofts.com (server dev deploy từ `develop`); `tpeProd` → hrm.eteksofts.com (prod TPE build từ `gop_db` bằng `build_tpe.sh`, 06/11). ⇒ API làm ở `gop_db` là đủ cho local + prod; chỉ cherry-pick sang `develop` (worktree tách origin, KHÔNG kèm rbac) nếu muốn kiểm trên tpeDev — hỏi user lúc xin phép code.
- Migration chạy lẻ bằng `--path`, liệt kê tên file + DB đích, `migrate --pretend` trước, chỉ chạy khi user cho phép.
- Chuẩn hoá SĐT: bỏ mọi ký tự không phải số trừ `+` ở đầu; `+84…` / `84…` (11–12 chữ số) → `0…`. Hiển thị giữ dạng người dùng nhập.
- Liên hệ duy nhất theo `(user_id, phone_normalized)`; trùng → dùng lại bản cũ, KHÔNG ghi đè tên.
- Tên ≤ 100 ký tự, SĐT bắt buộc; Địa chỉ ≤ 255, Ghi chú ≤ 1000 (Claude chốt độ dài). Validate báo đồng thời mọi ô.
- Tra KH công ty: chỉ khi SĐT chuẩn hoá ≥ 9 chữ số; khớp ĐÚNG TOÀN BỘ số với `customers.mobile` và `customer_contacts.phones` (cả 2 có thể nhiều số ngăn dấu phẩy: `CONCAT(',', REPLACE(col,' ',''), ',') LIKE '%,{số},%'`); không xét quyền xem KH; phạm vi KH như popup `ChooseErpCustomerModal` khi gửi `phone_exact_bypass`; tối đa 5 dòng.
- Chỉ nhắc việc GỐC (`parent_id IS NULL`) gắn liên hệ. Mọi phép đếm chỉ tính nhắc việc gốc của chính user.
- Liên hệ KHÔNG xuất hiện ở API / màn Lịch làm việc lãnh đạo và thông báo toàn công ty.
- Xoá liên hệ: `personal_todos.contact_id` → NULL, không xoá nhắc việc; trả số nhắc việc bị ảnh hưởng.
- Chữ UI (nguyên văn): "Gắn liên hệ" · "Liên hệ" · "Gần đây" · "Thêm mới" · "{N} người trong danh bạ của bạn" · "Trong danh bạ của bạn" · "Khách hàng công ty · khớp số điện thoại" · "Tạo liên hệ mới với số {số}" · "Liên hệ mới" · "Chọn từ danh bạ điện thoại" (app) · "hoặc nhập tay" · "Lưu nhắc việc xong, liên hệ tự vào danh bạ của bạn" · "Danh bạ cá nhân" · "Hẹn {dd/MM HH:mm} · {tiêu đề}" · "Nhắc việc với {tên}" · "Sắp tới" · "Đã xong" · "Lưu vào danh bạ điện thoại" (app) · "Xoá {tên} khỏi danh bạ?" · "{N} nhắc việc đang gắn với {tên} vẫn được giữ nguyên, chỉ bỏ phần liên hệ. Danh bạ trên điện thoại không bị ảnh hưởng."
- FE: không dùng prop `trim` trên ô nhập (cắt lúc lưu); nút mobile luôn có icon, Huỷ/Đóng cuối bên phải; web giữ style V2.
- FE phải kiểm bằng Playwright MCP (đo DOM) bằng tài khoản namdangit trước khi báo xong; sửa/thêm spec e2e nhưng KHÔNG tự chạy cả bộ e2e (chỉ khi user yêu cầu, `--workers=1`).
- Deploy: mục menu web mới "Danh bạ cá nhân" phải báo user thêm key ở "Cài đặt phân hệ" nếu chưa bàn giao (mục mới không tự ẩn).

## Review Focus

1. **Số dạng `+84 912 345 678` từ danh bạ máy** trùng liên hệ `0912345678` đã có → dùng lại, không tạo bản 2. Test Task 2 `test_trung_so_dang_84_dung_lai`.
2. **Huỷ form nhắc việc sau khi đã chọn "Tạo liên hệ mới"** → không có liên hệ nào được tạo. Test Task 4 `test_lien_he_moi_chi_tao_khi_luu_nhac_viec` (BE: không có endpoint tạo trước) + Task 6/9 widget test "huỷ form không gọi API liên hệ".
3. **Gõ 4–8 số** → không trả KH công ty (chống dò danh mục). Test Task 3 `test_chua_du_9_so_khong_tra_kh`.
4. **User A đọc / gắn / sửa / xoá liên hệ của user B qua API** (đoán id) → 404, không lộ. Test Task 2 `test_khong_dung_lien_he_nguoi_khac` + Task 4 `test_gan_contact_id_nguoi_khac_bi_tu_choi`.
5. **Nhắc việc bật lịch lãnh đạo có gắn liên hệ** → API đọc lịch lãnh đạo không có khoá `contact`. Test Task 4 `test_lich_lanh_dao_khong_lo_lien_he`.

---

### Task 1: Lược đồ + model + chuẩn hoá SĐT (hrm-api)

**Files:**
- Create: `Modules/Assign/Database/Migrations/2026_11_08_000001_create_personal_contacts_table.php`
- Create: `Modules/Assign/Database/Migrations/2026_11_08_000002_add_contact_id_to_personal_todos.php`
- Create: `Modules/Assign/Entities/MyTodo/PersonalContact.php`
- Create: `Modules/Assign/Support/PhoneNormalizer.php`
- Modify: `Modules/Assign/Entities/MyTodo/PersonalTodo.php` (fillable/casts `contact_id`, quan hệ `contact()`)
- Test: `Modules/Assign/Tests/Unit/PhoneNormalizerTest.php`, `Modules/Assign/Tests/Feature/PersonalContact/PersonalContactSchemaTest.php`

**Interfaces:**
- Produces: bảng `personal_contacts(id, user_id, name, phone, phone_normalized, address NULL, note NULL, company_name NULL, source TINYINT [1=tay,2=máy,3=KH công ty], source_customer_id NULL, last_used_at NULL, created_by, updated_by, timestamps)`, unique `(user_id, phone_normalized)`; `personal_todos.contact_id` BIGINT NULL + index (KHÔNG khoá ngoại — theo quy ước DB gộp); `PhoneNormalizer::normalize(?string $raw): ?string`; `PersonalContact` (scope `ofUser($userId)`); `PersonalTodo::contact()` belongsTo.

- [x] **Step 1: Test** `PhoneNormalizerTest`: `'0912 345 678'→'0912345678'`, `'+84 912.345.678'→'0912345678'`, `'84912345678'→'0912345678'`, `'(024) 3855-1234'→'02438551234'`, `''→null`, `null→null`, `'abc'→null`. `PersonalContactSchemaTest`: `Schema::hasColumns('personal_contacts', [...])`, `hasColumn('personal_todos','contact_id')`, insert 2 dòng cùng user + cùng `phone_normalized` → `QueryException`.
- [x] **Step 2:** Chạy `php vendor/bin/phpunit --filter 'PhoneNormalizerTest|PersonalContactSchemaTest'` → FAIL.
- [x] **Step 3:** Viết 2 migration + model + `PhoneNormalizer`. `migrate --pretend --path=...` cho từng file, đưa user xem; chỉ chạy `migrate --path=<file>` từng bản khi user cho phép.
- [x] **Step 4:** Chạy lại → PASS.
- [x] **Step 5:** Commit `feat(my-todo): bảng danh bạ cá nhân + contact_id`.

### Task 2: API CRUD liên hệ (hrm-api)

**Files:**
- Create: `Modules/Assign/Services/MyTodo/PersonalContactService.php`
- Create: `Modules/Assign/Http/Controllers/Api/V1/PersonalContactController.php`
- Create: `Modules/Assign/Http/Requests/MyTodo/StorePersonalContactRequest.php`, `UpdatePersonalContactRequest.php`
- Create: `Modules/Assign/Transformers/MyTodoResource/PersonalContactResource.php`
- Modify: `Modules/Assign/Routes/api.php:1533` (trong group `/assign/my-todo`, đặt route tĩnh TRƯỚC `{id}`)
- Test: `Modules/Assign/Tests/Feature/PersonalContact/PersonalContactApiTest.php`

**Interfaces:**
- Consumes: Task 1.
- Produces (prefix `/assign/my-todo/contacts`, user = `auth()->id()` employee như các route my-todo):
  - `GET /` `?q=` → `{data: [ContactResource], recent: [ContactResource ≤8 theo last_used_at desc], total}`; lọc `q` theo tên LIKE hoặc `phone_normalized` bắt đầu bằng số chuẩn hoá; xếp tên A→Z.
  - `GET /{id}` → `{data: ContactResource + todos: {upcoming: [...], done: [...]}}` (nhắc việc gốc của user có `contact_id`; upcoming = chưa xong, hạn gần trước, không hạn xuống cuối; done = `completed_at` desc; mỗi item `{id,title,due_date,due_time,is_completed,completed_at,list_name}`).
  - `POST /` (thêm thủ công DB-06) → trùng SĐT trả bản cũ + `meta.existed=true`, 200.
  - `PUT /{id}` → đổi SĐT trùng liên hệ khác → 422 `phone`.
  - `DELETE /{id}` → `{affected_todos: int}`.
  - `ContactResource`: `{id, name, phone, address, note, company_name, source, next_due: {todo_id,title,due_date,due_time}|null}` — `next_due` = nhắc việc chưa xong có hạn sớm nhất (kể cả quá hạn).
  - `PersonalContactService::resolveOrCreate(int $userId, array $data): PersonalContact` (dùng ở Task 4), `touch(int $contactId)` cập nhật `last_used_at`.

- [x] **Step 1: Test** `PersonalContactApiTest` (actAs NV 13 như `MyTodoPayloadFieldsTest`): `test_tao_va_liet_ke`, `test_trung_so_dang_84_dung_lai` (tạo `0912345678`, POST `+84 912 345 678` tên khác → cùng id, tên cũ giữ nguyên, `meta.existed`), `test_sua_so_trung_bao_422`, `test_xoa_go_lien_he_khoi_nhac_viec` (2 todo gắn → `affected_todos=2`, todo còn, `contact_id` NULL), `test_khong_dung_lien_he_nguoi_khac` (GET/PUT/DELETE id của NV khác → 404), `test_validate_bao_dong_thoi` (thiếu name + phone → 422 có cả 2 khoá), `test_next_due_lay_viec_chua_xong_som_nhat`, `test_chi_tiet_chia_sap_toi_da_xong`.
- [x] **Step 2:** Chạy `--filter PersonalContactApiTest` → FAIL.
- [x] **Step 3:** Viết service/controller/request/resource + route.
- [x] **Step 4:** Chạy → PASS; chạy lại `--filter MyTodo` + `Modules/Assign/Tests/Feature/LeaderSchedule` để chắc không vỡ (dọn rác test theo memory "PHPUnit chạy trên DB .env").
- [x] **Step 5:** Commit `feat(my-todo): API danh bạ cá nhân`.

### Task 3: Tra KH công ty theo đúng SĐT (hrm-api)

**Files:**
- Modify: `Modules/Assign/Services/MyTodo/PersonalContactService.php` (thêm `lookupCompanyByPhone`)
- Modify: `Modules/Assign/Http/Controllers/Api/V1/PersonalContactController.php` + route `GET /assign/my-todo/contacts/company-lookup` (đặt TRƯỚC `/{id}`)
- Test: `Modules/Assign/Tests/Feature/PersonalContact/CompanyPhoneLookupTest.php`

**Interfaces:**
- Produces: `lookupCompanyByPhone(string $raw): array` → `[{person_name, phone, customer_id, customer_name, address, kind: 'customer'|'contact'}]` ≤ 5. `kind='contact'` khi khớp `customer_contacts.phones` (person_name = tên người liên hệ), `'customer'` khi khớp `customers.mobile` (person_name = tên KH). Điều kiện phạm vi KH: đọc query `CustomerService::index` với `phone_exact_bypass=1` + `hide_individual` như `ChooseErpCustomerModal` gửi, dùng lại đúng điều kiện (không thêm luật mới); không áp `applyVisibilityScope`.

- [x] **Step 1: Test** (dựng fixture KH + người liên hệ trong transaction): `test_chua_du_9_so_khong_tra_kh` (`0912345` → `[]`), `test_khop_dung_so_kh`, `test_khop_so_nguoi_lien_he`, `test_so_trong_chuoi_nhieu_so` (`mobile='0901111111, 0912345678'`), `test_dang_84_van_khop`, `test_khop_mot_phan_khong_tra` (`091234567` không ra `0912345678`), `test_khong_xet_quyen_xem_kh` (KH do người khác tạo vẫn ra).
- [x] **Step 2:** FAIL → **Step 3:** code → **Step 4:** PASS.
- [x] **Step 5:** Commit `feat(my-todo): tra KH công ty theo SĐT cho danh bạ`.

### Task 4: Gắn liên hệ vào nhắc việc (hrm-api)

**Files:**
- Modify: `Modules/Assign/Http/Requests/MyTodo/StorePersonalTodoRequest.php`, `UpdatePersonalTodoRequest.php`
- Modify: `Modules/Assign/Services/MyTodo/MyTodoService.php` (`storeTodo` :151, `updateTodo` :271, `normalizeItem` :690 khối `if ($type === 'personal')` :770)
- Test: `Modules/Assign/Tests/Feature/PersonalContact/TodoContactAttachTest.php`

**Interfaces:**
- Consumes: `PersonalContactService::resolveOrCreate`, `touch` (Task 2).
- Produces: payload lưu nhắc việc nhận **một trong hai**: `contact_id` (int, phải thuộc user) hoặc `contact: {name, phone, address?, note?, source (1|2|3), source_customer_id?, company_name?}`; `contact_id: null` = bỏ gắn; không gửi khoá = giữ nguyên. Bản ghi có `parent_id` mà gửi liên hệ → 422. Item personal trong GET my-todo / calendar / lists/{id}/todos có `contact: {id, name, phone, company_name}|null`.

- [x] **Step 1: Test**: `test_gan_lien_he_co_san`, `test_lien_he_moi_chi_tao_khi_luu_nhac_viec` (POST todo kèm `contact` mới → 1 liên hệ; validate todo lỗi → 0 liên hệ), `test_lien_he_moi_trung_so_dung_lai`, `test_gan_contact_id_nguoi_khac_bi_tu_choi` (422), `test_buoc_con_khong_gan_duoc`, `test_bo_gan_bang_null`, `test_payload_co_contact`, `test_lich_lanh_dao_khong_lo_lien_he` (todo `is_leader_schedule=1` + contact → `GET /assign/leader-schedules` không có chuỗi tên/SĐT liên hệ), `test_touch_last_used_at`.
- [x] **Step 2:** FAIL → **Step 3:** code (resolve liên hệ TRONG cùng transaction lưu todo) → **Step 4:** PASS + chạy lại `Modules/Assign/Tests/Feature/LeaderSchedule`.
- [x] **Step 5:** Commit `feat(my-todo): gắn liên hệ vào nhắc việc`.

### Task 5: Web — gắn liên hệ trong form nhắc việc (hrm-client)

**Files:**
- Create: `pages/assign/my-todo/components/contacts/ContactPickerModal.vue` (DB-02/03: ô tìm, Gần đây, danh sách theo chữ cái, nhóm KH công ty khi đủ 9 số, "Tạo liên hệ mới với số …")
- Create: `pages/assign/my-todo/components/contacts/ContactFormFields.vue` (Tên*, SĐT*, Địa chỉ, Ghi chú — dùng chung Task 6)
- Create: `pages/assign/my-todo/components/contacts/ContactCard.vue` (avatar viết tắt + màu cố định theo id, tên, SĐT, công ty, nút sao chép số + link `tel:`, ✕)
- Create: `pages/assign/my-todo/components/contacts/avatarColor.js` (`avatarColor(id) → {bg, fg}` từ 6 cặp: `#CCFBF1/#0F766E`, `#E0F2FE/#0369A1`, `#FEF3C7/#B45309`, `#FCE7F3/#BE185D`, `#EDE9FE/#6D28D9`, `#E0E7FF/#4338CA`)
- Modify: `pages/assign/my-todo/components/TodoFormModal.vue` (dòng link "Gắn liên hệ" ngay dưới Tiêu đề; chọn xong thay bằng nhãn "Liên hệ" + `ContactCard`; gửi `contact_id` hoặc `contact` khi Lưu)
- Test: e2e `HRM/e2e/tests/assign/my-todo-contact.spec.ts` (viết, không tự chạy cả bộ)

**Interfaces:**
- Consumes: API Task 2–4.
- Produces: `ContactPickerModal` emit `pick({id?, name, phone, address, note, company_name, source, source_customer_id})` (chưa có id = liên hệ mới, chỉ tạo khi lưu form); `ContactFormFields` props `value`, `errors`, emit `input`; `avatarColor` dùng lại ở Task 6.

- [x] **Step 1:** Viết spec e2e: mở form → có link "Gắn liên hệ", KHÔNG có ô Tên/SĐT; chọn liên hệ có sẵn → thẻ hiện tên + SĐT; gõ 7 số → không có nhóm "Khách hàng công ty"; tạo mới + Huỷ form → `GET contacts` không tăng; tạo mới + Lưu → liên hệ có trong danh bạ.
- [x] **Step 2:** Code.
- [x] **Step 3:** Playwright MCP (namdangit): đo DOM — form không dùng liên hệ có đúng số ô như trước (đếm `.form-group`), toạ độ link ngay dưới Tiêu đề, popup không tràn màn 1280, thẻ liên hệ hiện đủ; chặn API `company-lookup` để thấy trạng thái tải.
- [x] **Step 4:** Commit `feat(my-todo-web): gắn liên hệ trong form nhắc việc`.

### Task 6: Web — màn Danh bạ cá nhân (hrm-client)

**Files:**
- Create: `pages/assign/my-todo/contacts/index.vue` (trái: ô tìm + danh sách theo chữ cái, dòng cam "Hẹn …"; phải: chi tiết liên hệ — thông tin, nút sao chép SĐT, "Tạo nhắc việc" mở `TodoFormModal` gắn sẵn, "Nhắc việc với {tên}" Sắp tới / Đã xong, menu Sửa / Xoá)
- Modify: `pages/assign/my-todo/components/TodoCalendarSidebar.vue` (nút "Danh bạ cá nhân" dưới khối danh sách → `/assign/my-todo/contacts`)
- Modify: menu registry hub nếu my-todo khai mục con ở đó (kiểm `subItems` theo memory "Menu hub khai subItems")
- Test: e2e `HRM/e2e/tests/assign/my-todo-contacts-page.spec.ts`

**Interfaces:**
- Consumes: Task 2 API, `ContactFormFields`, `avatarColor`, `TodoFormModal` (prop mới `presetContact`).

- [x] **Step 1:** Spec e2e: danh sách có chữ cái nhóm; tìm theo SĐT lọc đúng; chi tiết chia Sắp tới / Đã xong đúng số; Xoá → confirm có câu "{N} nhắc việc đang gắn…" → nhắc việc vẫn còn, không còn thẻ liên hệ; Sửa SĐT trùng → báo lỗi tại ô.
- [x] **Step 2:** Code (route Nuxt tĩnh, không dùng tên file có gạch ngang cho route động).
- [x] **Step 3:** Playwright MCP đo: 2 cột không tràn ở 1366/1440, danh sách dài cuộn riêng, nhãn confirm đúng nguyên văn.
- [x] **Step 4:** Commit `feat(my-todo-web): màn Danh bạ cá nhân`.

### Task 7: App — model + API service (TPE_APP)

**Files:**
- Create: `lib/data/lib/src/repository/source/remote/api/model/personal_contact.dart` (`PersonalContact.fromJson`, `initials`, `avatarColors` cùng bảng 6 màu Task 5)
- Create: `lib/data/lib/src/repository/source/remote/api/api_services/app_server/contact_api_service.dart`
- Modify: `lib/data/lib/src/repository/source/remote/api/model/work_item.dart` (đọc `contact`)
- Modify: `lib/di/` đăng ký `ContactApiService` như `MyTodoApiService`
- Test: `test/ui/my_todo/personal_contact_model_test.dart`

**Interfaces:**
- Produces: `ContactApiService.list({String? q}) → Future<ContactPage{List<PersonalContact> items, recent; int total}>`, `show(int id) → Future<ContactDetail{contact, upcoming, done}>`, `lookupCompany(String phone) → Future<List<CompanyPhoneMatch>>`, `store(Map) / update(int, Map) → Future<PersonalContact>`, `delete(int) → Future<int affectedTodos>`; `WorkItem.contact` (`PersonalContact?`).

- [x] **Step 1:** Test parse JSON mẫu (có/không `next_due`, `company_name`), `initials('Trần Thị Lan')=='TL'`, màu cố định theo id.
- [x] **Step 2:** `fvm flutter test test/ui/my_todo/personal_contact_model_test.dart` → FAIL → code → PASS.
- [x] **Step 3:** Commit `feat(my-todo-app): model + API danh bạ`.

### Task 8: App — gắn liên hệ trong form (TPE_APP)

**Files:**
- Create: `lib/ui/my_todo/contacts/contact_picker_sheet.dart` (DB-02/03), `lib/ui/my_todo/contacts/new_contact_sheet.dart` (DB-04, có "Chọn từ danh bạ điện thoại"), `lib/ui/my_todo/contacts/contact_avatar.dart`
- Modify: `lib/ui/my_todo/personal_todo_form_page.dart` (dòng "Gắn liên hệ" dưới Tiêu đề; thẻ liên hệ + gọi + ✕; payload `contact_id` / `contact`)
- Modify: `pubspec.yaml` — thêm 1 thư viện bộ chọn liên hệ hệ thống (chỉ trả về người được chọn, KHÔNG xin quyền đọc toàn bộ) + thư viện mở `tel:` / `sms:` nếu chưa có; khai `NSContactsUsageDescription` chỉ khi thư viện bắt buộc.
- Test: `test/ui/my_todo/personal_todo_form_contact_test.dart`

**Interfaces:**
- Consumes: Task 7.
- Produces: `ContactPickerSheet.show(context) → Future<ContactDraft?>`; `ContactDraft {int? id; name; phone; address; note; companyName; int source; int? sourceCustomerId}` (`id==null` = mới, chỉ gửi lúc Lưu); `ContactAvatar(contact, size)` dùng lại Task 9.

- [x] **Step 1:** Widget test (fake API như `personal_todo_form_save_test.dart`): form không gắn → không có ô Tên/SĐT; chọn liên hệ có sẵn → payload `contact_id`; tạo mới rồi Lưu → payload `contact{...}`, KHÔNG gọi `ContactApiService.store`; tạo mới rồi thoát form → không gọi API nào của liên hệ; gõ 8 số → không gọi `lookupCompany`, gõ 10 số → gọi.
- [x] **Step 2:** FAIL → code → PASS.
- [x] **Step 3:** Máy ảo (tpeLocal, namdangit): so với DB-01…DB-05; bộ chọn danh bạ máy điền đúng Tên/SĐT; số `+84` lưu xong dùng lại liên hệ cũ.
- [x] **Step 4:** Commit `feat(my-todo-app): gắn liên hệ trong form nhắc việc`.

### Task 9: App — Danh bạ + chi tiết liên hệ + menu (TPE_APP)

**Files:**
- Create: `lib/ui/my_todo/contacts/contacts_page.dart` (DB-06), `lib/ui/my_todo/contacts/contact_detail_page.dart` (DB-07, menu ⋮ DB-08, xác nhận xoá DB-09)
- Modify: `lib/ui/module_shell/module_menus.dart:282` — thêm `DrawerEntry('Danh bạ cá nhân', icon: Icons.contacts_outlined, onTap: → ContactsRoute())` ngay SAU mục lịch lãnh đạo
- Modify: router auto_route (đăng ký `ContactsRoute`, `ContactDetailRoute(id)`) + chạy build_runner theo quy trình repo
- Test: `test/ui/my_todo/contacts_page_test.dart`

**Interfaces:**
- Consumes: Task 7, `ContactAvatar` (Task 8), form nhắc việc nhận tham số `presetContact`.

- [x] **Step 1:** Widget test: dòng "Hẹn …" chỉ hiện khi `next_due` có; chi tiết chia Sắp tới / Đã xong; Xoá hiện câu nguyên văn có N; "Tạo nhắc việc" mở form có sẵn liên hệ; "Lưu vào danh bạ điện thoại" gọi màn thêm liên hệ hệ thống với tên/SĐT/địa chỉ.
- [x] **Step 2:** FAIL → code → PASS.
- [x] **Step 3:** Máy ảo so DB-06…DB-09; nút Gọi / Nhắn tin mở đúng ứng dụng.
- [x] **Step 4:** Commit `feat(my-todo-app): màn Danh bạ cá nhân`.

---

## Self-review (đã chạy)
- Phủ spec: §3.1–3.3 → T3/T4 · §3.4–3.5 → T5/T8 · §3.6 → T6/T9 · §3.7 → T8/T9 · §3.8 → T2/T6/T9 · §3.9 → T5/T6 · §5.1 → T1/T2 · §5.2 → T4 + T6/T9 (Hẹn) · §5.3 → T3 · §6 → T5/T6 · §7 → T7–T9 · §8 → Global Constraints.
- Tên thống nhất: `PersonalContactService::resolveOrCreate/touch/lookupCompanyByPhone`, route `/assign/my-todo/contacts[/company-lookup|/{id}]`, payload `contact_id` / `contact`, `ContactDraft`, `ContactAvatar`, `avatarColor`.
- Claude chốt trong plan (user soát): độ dài trường; `source` 1/2/3; không khoá ngoại; xếp "Không hạn" cuối nhóm Sắp tới; nút "Danh bạ cá nhân" ở sidebar my-todo web; icon `Icons.contacts_outlined`.
- Ngoài phạm vi plan này: đổi "Danh sách" → "Loại nhắc việc" (xem `my-todo/design.md`) — 2 việc cùng sửa `TodoFormModal.vue` / form app, làm nối tiếp thì rebase cẩn thận.

---

## Bổ sung 07/11/2026 — spec §5.2: liên hệ trên thẻ / chi tiết nhắc việc (user chốt "Có làm")
Mockup: DB-10 (`meeting-mobile.pen`, Nhóm ②). BE KHÔNG đổi: item personal đã có `contact {id,name,phone,company_name}` ở GET my-todo, calendar, lists/{id}/todos (Task 4).
Chưa có lệnh code — xin phép riêng.

### Task 10: Web — dòng liên hệ trên thẻ nhắc việc (hrm-client)
**Files:** Modify `pages/assign/my-todo/components/TodoItem.vue`; Modify `pages/assign/my-todo/contacts/index.vue` (đọc `?id=` chọn sẵn liên hệ); Test: e2e `HRM/e2e/tests/assign/my-todo-contact.spec.ts` (thêm ca).
- Item personal có `contact` → thêm 1 dòng dưới dòng hạn: icon `ri-user-line` + tên (link `/assign/my-todo/contacts?id={id}`, `@click.stop` không mở form) + "· {SĐT}" + nút sao chép SĐT (icon, `@click.stop`, toast "Đã sao chép số điện thoại"). Không có liên hệ → không có dòng.
- Ô lịch tháng/tuần (WorkItemCard, MonthGrid, WeekGrid) KHÔNG thêm (ô quá chật) — Claude chốt; bấm vào việc đã mở form có thẻ liên hệ.
- [x] Step 1: e2e: việc có liên hệ hiện tên + SĐT; bấm tên → URL `/assign/my-todo/contacts?id=` và liên hệ đó được chọn; bấm tên KHÔNG mở form; việc không liên hệ không có dòng.
- [x] Step 2: Code → Playwright MCP đo (namdangit): dòng nằm trong thẻ, không tràn ở 1280, click không mở form.

### Task 11: App — dòng liên hệ trên thẻ + khối Liên hệ ở chi tiết nhắc việc (TPE_APP)
**Files:** Modify `lib/ui/my_todo/widget/work_item_card.dart`, `lib/ui/my_todo/personal_todo_detail_page.dart`; Test: `test/ui/my_todo/work_item_card_contact_test.dart`.
- WorkItemCard (dùng ở tab Danh sách + agenda tab Lịch): `item.contact != null` → dòng `Icons.person_outline` + tên (màu module, chạm → `ContactDetailRoute(id)`) + " · SĐT" (xám) + nút gọi tròn 30 px bên phải (`launchUrl(tel:)` trực tiếp, lỗi → snackbar). Chạm dòng/nút KHÔNG mở thẻ.
- PersonalTodoDetailPage: khối "Liên hệ" dưới tiêu đề/hạn: `ContactAvatar` + tên + SĐT + công ty (nếu có) + nút Gọi (icon + chữ); chạm khối → `ContactDetailRoute`. Không liên hệ → không có khối.
- [x] Step 1: Widget test: có/không contact; chạm tên gọi navigator đúng route (fake); chạm nút gọi không gọi onTap thẻ.
- [x] Step 2: Code → `fvm flutter test test/ui/my_todo` + analyze → controller bấm thử simulator (DB-10).

### Checkpoint — 07/11/2026 (wrap up)
Vừa hoàn thành: 11/11 task (9 gốc + bổ sung §5.2 Task 10–11), final review + fix wave, Info.plist NSContactsUsageDescription, 2 bug user báo trên simulator: (1) sheet "Gắn liên hệ" co vào giữa khi danh bạ trống (stretch + ẩn thanh chữ cái), (2) bộ chọn danh bạ iOS phải chạm thêm 1 số (selectPhoneNumber → selectContact, báo lỗi/không có số). User xác nhận đã thêm liên hệ từ danh bạ máy thành công. Nút Gọi trên simulator báo "Không mở được ứng dụng gọi điện" là ĐÚNG (simulator không có app Điện thoại — simctl openurl tel: lỗi 115).
Đang làm dở: —
Bước tiếp theo: user kiểm máy thật (Gọi, Lưu vào danh bạ điện thoại, Android toàn bộ); kiểm CI Flutter ≥ 3.41; user tự commit 3 repo (hrm-api + hrm-client gop_db, TPE_APP develop — TPE_APP còn 29 file staged của Lịch lãnh đạo, tách khi commit); deploy: ẩn menu `assign::Danh bạ cá nhân` ở Cài đặt phân hệ, chạy 2 migration 2026_11_08_000001/2.
Blocked: —
Ghi chú: test data local đã dọn; LeaderSchedule PHPUnit 12 fail có sẵn (dữ liệu quyền DB local, R7 — chưa kiểm cây sạch). Nhật ký + 23 ruling: execution-ledger.md.

### Checkpoint — 08/11/2026 (wrap up)
Vừa hoàn thành: code + kiểm (Playwright web, máy ảo app, e2e my-todo) → ĐÃ COMMIT + PUSH 08/11: hrm-api gop_db `cc12bd91d`, hrm-client gop_db `2a4b888ff`, TPE_APP develop `73b82b4` (rebase lên 14 commit develop: gộp thẻ meeting "Đã báo vắng" + `!closed`; giữ TodoListPickerSheet thay showAppPickSheet; sinh lại notification.freezed).
Đang làm dở: —
Bước tiếp theo: deploy — migration 2026_11_08_000001/2 + 2026_11_09_000001/2/3, `~/build_tpe.sh` (catalog-sync đổi tên 2 quyền LCT), thêm key ẩn menu mới ở Cài đặt phân hệ nếu chưa bàn giao; build app mới. Còn treo nhẹ: kiểm máy thật (Gọi / Lưu danh bạ máy / Android) cho Danh bạ.
Blocked:

### Checkpoint — 08/11/2026 (wrap up 2)
Vừa hoàn thành: góp ý test máy thật iPhone 14 Pro Max — Lưu báo lịch không treo (terminating + Content-Length), sửa nhắc việc xong về đúng màn, chọn danh bạ máy ở sheet đầu (user đã thử OK). ĐÃ PUSH: hrm-api gop_db `7ee51d6a5`, TPE_APP develop `1ae3033`. Prod tpe: php-fpm 8.1 + QUEUE=database có worker ⇒ prod không treo.
Đang làm dở: — (tiến trình còn chạy cho máy thật: API `php -S 0.0.0.0:8001` PID 39832; `flutter run --release` iPhone PID 57178 — tắt theo PID khi không cần)
Bước tiếp theo: deploy prod (5 migration 2026_11_08_000001/2 + 2026_11_09_000001/2/3, ~/build_tpe.sh catalog-sync, key ẩn menu mới, build app); đẩy .plans bằng ~/bin/push-plans.sh.
Blocked:
