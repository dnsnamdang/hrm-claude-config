# Plan — Thiết kế lại màn Quản lý phân quyền HRM

Nhánh: `gop_db`. Người phụ trách: @namdangit.
Design: `.plans/gop-db/thiet-ke-lai-phan-quyen/design.md`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-14-thiet-ke-lai-phan-quyen-design.md`

---

## Phase 0 — Brainstorm + Mockup (HOÀN THÀNH)

- [x] Khảo sát hiện trạng FE (màn `timesheet/setting/roles`, `components/setting/Permission.vue`, `subsystems.js`, phân hệ `admin` type 10)
- [x] Khảo sát BE (`PermissionsTableSeeder.php` 617 quyền, `RoleController`/`PermissionController`, `Role::syncPermissionsByCompany`, pivot `role_has_permissions.company_id`)
- [x] Phân tích dữ liệu thật nhóm quyền phân hệ Chấm công (17 quyền = 3 chức năng con × cấp)
- [x] Brainstorm & chốt mô hình: Loại (Xem/Thao tác/Duyệt) × Phạm vi (Tổng cty→Bộ phận); phân quyền theo 1 công ty
- [x] Trích style demo chuẩn từ `.plans/demo-man-hinh-ke-toan/demo/assets/style.css` + shell `app.js`
- [x] Dựng mockup tương tác: `phan-quyen.html` + `assets/permissions.js` (2 màn), thêm menu vào `app.js`, card vào `index.html`
- [x] Lặp thiết kế qua nhiều vòng feedback: layout bảng, select phạm vi, Duyệt có phạm vi, bộ lọc 1 hàng, panel tổng hợp + chip, popup "Quyền đang có", footer Lưu, icon/màu dải chức năng
- [x] Verify trực quan bằng Playwright (danh sách, popup, form phân quyền, Duyệt-scope)

## Phase 1 — Implement vào hrm-client + hrm-api (ĐÃ LÀM 2026-09-02)

> Giữ nguyên schema DB. Mở rộng phạm vi so với bản kế hoạch cũ: màn phục vụ **cả HRM lẫn ERP**
> (xem `design.md` mục "Mở rộng sang CẢ HAI HỆ").

### BE (`hrm-api`)

- [x] `config/permission_scopes.php` — map `permission_id → department|part|company`, khai sẵn
      **20 bản ghi** (17 quyền ERP + 3 bản HRM của chức năng đã chuyển). Khoá theo **ID**, không
      theo tên, để đổi tên quyền không âm thầm nới scope.
- [x] `Modules/Timesheet/Services/PermissionMatrixService.php` — dựng ma trận: tách hậu tố phạm vi,
      suy hành động (`manage`/`view`/`approve`/`other`), gom biến thể cùng quyền gốc, gắn phạm vi
      duyệt. Có `selfCheck()` bảo đảm **không rơi quyền nào**.
- [x] `GET /timesheet/permissions/matrix?guard=api|web` + middleware `checkPermission:Quản lý phân quyền`;
      controller ghi `Log::error` nếu `selfCheck` fail.
- [x] `POST /timesheet/roles/{id}/permissions` — lưu quyền của 1 chức vụ trong công ty đang đăng nhập.
      Tách khỏi `store()` để không đụng tên/ghi chú/danh sách công ty. Chặn fail-closed quyền khác
      guard (rethrow `ValidationException`), và **giữ nguyên** quyền khác guard đang gán sẵn.
- [x] `RoleService::index` — thêm bộ lọc `guard` + cột `permission_count`.
- [x] `RoleListResource` / `RoleDetailResource` — thêm `guard_name`, `system` (HRM/ERP),
      `current_company_id`, `current_permission_ids`.

### FE (`hrm-client`)

- [x] `components/subsystem-menu/admin.js` — thêm mục **Phân quyền → /admin/roles**
- [x] `utils/permission-matrix.js` — cột hành động, cấp phạm vi, nhãn phạm vi duyệt, **12 màu phân hệ
      khoá theo `type`** (không theo chỉ số mảng), gom dòng theo phân hệ
- [x] `pages/admin/roles/index.vue` — danh sách 120 chức vụ, cột `Hệ` + bộ lọc, cột "Quyền đang có"
      là nút mở popup, giữ Phân quyền hàng loạt / Lịch sử / Xuất Excel
- [x] `components/permission-matrix/RolePermissionsModal.vue` — popup "Quyền đang có" (chỉ đọc,
      có lọc phân hệ/hành động/từ khoá + chip đếm theo phân hệ)
- [x] `pages/admin/roles/_id.vue` — màn ma trận, ngữ cảnh 1 công ty + 1 hệ
- [x] `components/permission-matrix/PermissionMatrix.vue` — 1 bảng duy nhất, sticky 2 tầng,
      **render lười theo phân hệ**, bộ lọc + cấp hàng loạt theo hành động
- [x] `components/permission-matrix/ScopePickerModal.vue` — chọn 1 cấp phạm vi (radio)
- [x] `components/permission-matrix/ItemListModal.vue` — danh sách quyền trong 1 ô (popup `n/N`)
- [x] `components/permission-matrix/GrantedPanel.vue` — panel "quyền đã phân" + nút Lưu
- [x] `middleware/redirectLegacyRoles.js` — `timesheet/setting/roles`, `timesheet/setting/roles/add/{id}`,
      `human/roles` → màn mới
- [x] Cờ quyền fail-closed: cả 2 màn đẩy về 404 nếu thiếu `Quản lý phân quyền`

### Verify Playwright 1440×900 — 0 lỗi console

| Ca kiểm | Kết quả đo |
|---|---|
| Bộ tách không rơi quyền | `api 722/722` · `web 965/965` — **1.687/1.687** |
| Số dòng ma trận | 288 (HRM 151 + ERP 137) · 285 ô checkbox + 200 ô popup |
| Danh sách chức vụ | 119 dòng; lọc `Hệ = HRM` → 44, `ERP` → 75 |
| Sticky 2 tầng | `thead.top = 60` khớp đúng mép topbar (hở **0px**); dải phân hệ ghim ngay dưới |
| Một bảng duy nhất | `so_bang = 1`, `so_thead = 1`; độ rộng cột dòng 0 / 80 / 150 **bằng nhau tuyệt đối** `[320,63,119,119,121,111]` |
| Render lười | mặc định 15 dòng (1 phân hệ) → "Mở tất cả" ra 151 dòng |
| Bỏ tích `Xem` có phạm vi | 556 → 552 (xoá cả 4 cấp), nhãn phạm vi biến mất |
| Tích lại | 553, popup tự bật, radio đúng **cấp hẹp nhất** (fail-closed) |
| Chọn "Công ty" + Áp dụng | nhãn ô đổi `Công ty`, panel hiện badge `Công ty`, tổng giữ 553 |
| Popup `Duyệt` 3/3 → bỏ 1 | nút thành `2/3`, tổng 553 → 552 |
| Mở lại popup | nhớ đúng `[false, true, true]` |
| Nhãn phạm vi duyệt | id 1154 → **`Phòng ban quản lý`** (đã khai, nền cam); 2 quyền cùng nhóm → `Toàn công ty` + viền đứt ⚠ |
| Ô `Tất cả` | bật → 9 quyền (gán cấp hẹp nhất, KHÔNG mở popup); tắt → 0 |
| Cấp hàng loạt theo hành động | lọc `Duyệt` → "Cấp tất cả (26 dòng)" → 0 → 48 → bỏ cấp → 0 |
| Lưu | 638 → 634, gỡ **đúng** `205, 208, 210, 818`; 82 dòng mồ côi giữ nguyên; có ghi lịch sử |
| Chức vụ ERP (`guard = web`) | 7 dải phân hệ đúng map, 137 dòng, 82 quyền |
| Popup "Quyền đang có" | 556 khớp cột danh sách; 9 chip phân hệ cộng lại = 556 |
| Redirect màn cũ | cả 3 route cũ → `/admin/roles` (bản `add/{id}` → `/admin/roles/{id}`) |
| **Fail-closed** | không quyền: matrix `403`, lưu `403`; không token `401`; có quyền `200` |
| **Chặn chéo guard** | gán quyền `web` cho chức vụ `api` → trả lỗi validate, DB **không đổi** (638) |

### 3 lỗi tự phát hiện và đã sửa trong lúc verify

1. **Sticky chết hoàn toàn** — `#wrapper` và `.content-page` của layout để `overflow: hidden`; tổ tiên
   có overflow khác `visible` trở thành khung cuộn của phần tử sticky, mà hai div đó không tự cuộn.
   Đo được: `thead.top = -1483px` thay vì `60px`. Sửa: bật `overflow: visible` bằng class `pm-fullpage`
   trên `body`, **chỉ trong lúc màn này sống**, gỡ ở `beforeDestroy` (đã đo: rời màn thì cả hai div
   trở lại `hidden`).
2. **Dải phân hệ không ghim** — `top` đặt trên `<tr>` trong khi `position: sticky` nằm ở `<td>`;
   trình duyệt bỏ qua. Chuyển `top` sang chính `<td>`. Thêm `-1px` để dải đè mép thead, bịt khe
   ~0,5px do làm tròn subpixel.
3. **Cột "Quyền đang có" lệch 82 so với màn phân quyền** — subquery đếm thẳng `role_has_permissions`
   nên tính cả dòng trỏ vào quyền **đã bị xoá** (riêng Super admin có 82 dòng như vậy). Sửa: join
   `permissions` + khớp guard. Sau sửa: danh sách 556 = chi tiết 556.

### Việc CHƯA làm, ghi nhận sang sau

- [ ] Bổ sung ca e2e tự động cho màn mới (hiện mới verify bằng Playwright MCP thủ công)
- [x] **Chấm công: khai xong 8/8 quyền duyệt** (2026-09-05) — rà từng gate, chốt 5 giảm 45 → 37
- [ ] Khai `approve_scope` cho 37 quyền HRM + 65 quyền ERP còn lại
- [ ] Chức vụ không có dòng trong `company_roles` (1 chức vụ HRM) không hiện ở danh sách — do
      `RoleService::index` inner join `company_roles`, hành vi có sẵn từ trước, chưa đụng tới

## Phase 2 — Định danh quyền bằng `code` + cấu trúc lại seeder (MỞ 2026-09-05)

> Chốt: làm chuẩn theo `code`, chấp nhận sửa lớn. Phạm vi đợt này = **HRM** (`hrm-api` +
> `hrm-client`, ~1.760 chỗ gọi). ERP đợt sau. Chi tiết 4 quyết định: `design.md` mục
> "Triển khai `code` (2026-09-05)".

### 2.1 — Hạ tầng (không đụng call site nào) — XONG 2026-09-05

- [x] Migration `2026_09_05_000001_add_code_to_permissions_table` — `code varchar(191) NULL`,
      **unique `(code, guard_name)`** chứ không phải `code` đơn (lý do bên dưới)
- [x] `Modules/Timesheet/Services/PermissionCodeGenerator` — sinh code từ `type`/`group_category`
      + `group` + `name`, slug tiếng Việt không dấu
- [x] Command `permission:backfill-code` — mặc định CHẠY KHÔ, phải `--write` mới ghi; không bao
      giờ đè code đã có
- [x] Migration `2026_09_05_000002_merge_duplicate_currency_permissions` — gộp 1117→1115,
      1118→1116, chuyển `role_has_permissions` trước rồi mới xoá
- [x] Backfill **1.685/1.685 quyền, 0 trùng** (api 720 + web 965, không quyền nào thiếu code)
- [ ] Khai `type = 1` cho 78 quyền Chấm công đang `type = NULL` (hiện generator quy ước NULL→1,
      chưa sửa dữ liệu gốc)

**🔑 Phát hiện khi backfill — unique phải theo `(code, guard_name)`:** sinh thử cho cả 1.687 quyền
ra 30 nhóm trùng, trong đó **28 nhóm là cùng MỘT chức năng tồn tại ở cả hai hệ**
(`sale.hop_dong.approve.duyet` = api 1141 + web 100041 · `master_data.tat_ca_khach_hang.view` =
api 167 + web 100170 · 3 nhóm CSKH…). Đó là hệ quả tất yếu của việc chuyển dần chức năng ERP sang
HRM, không phải lỗi. Ép unique trên `code` đơn sẽ buộc bịa code khác nhau cho hai bản ghi cùng
nghĩa và **mất luôn cái lợi lớn nhất: sau này gộp hai hệ chỉ cần join theo `code`**. Sau khi đổi
khoá, số trùng còn đúng 2 — cặp tiền tệ trùng tên thật.

🐞 Bộ sinh bản đầu bỏ mất cấp phạm vi của quyền `other` ("Phân ca theo công ty", "Xây dựng giá bán
theo phòng") → 3 quyền dồn về một code. Sửa xong: 716 → 720 code duy nhất trên guard `api`.

### 2.2 — Chốt chặn tự động — XONG 2026-09-05

- [x] `Modules/Timesheet/Services/PermissionAuditService` — soi TĨNH, không cần DB (chạy được trong CI)
- [x] Command `permission:audit [--full]` — in báo cáo kèm `file:dòng`
- [x] `tests/Unit/PermissionAuditTest` — 5 test kiểu **RATCHET (bánh cóc)**: chốt số lỗi hiện tại
      làm mốc, chỉ cho GIẢM. Bắt CI phải xanh ngay thì hoặc phải dừng mọi việc để dọn, hoặc có
      người tắt test đi.
- [x] Đã kiểm bánh cóc thật sự chặn: tiêm 1 quyền ma giả → đỏ ngay
      (*"Số quyền ma tăng từ 21 lên 22"*); gỡ ra → 5 test xanh lại.

**Mốc đo được (HRM, chỉ tính gate viết bằng chuỗi literal):**

| Chốt | Số lỗi | Ghi chú |
|---|---|---|
| 1. Quyền MA | **21 quyền / 25 chỗ gọi** | vĩnh viễn trả `false` |
| 2. Trùng `(name, guard_name)` | **2** | cặp tiền tệ — seeder NỔ trên DB cài mới |
| 3. Trùng id | **0** | đang sạch, phải giữ sạch |
| 4. Thiếu `type` | **78** | toàn bộ là phân hệ Chấm công |
| 5. Quyền duyệt chưa khai phạm vi | **45** | đang ăn mặc định `company` (rộng nhất) |

Vùng mù: **70 gate truyền biến/hằng số** + tên ghép động (`"Xem danh sách $prefix theo bộ phận"`)
— không soi tĩnh được. Chuyển sang hằng số ở 2.5 sẽ làm con số này tăng, và đó là điều MONG MUỐN:
khi đó chính PHP bảo đảm hằng số tồn tại, không cần bộ soi nữa.

⚠️ Con số 21 khác con số **89 quyền ma** ghi trong `design.md` (khảo sát 2026-08-28): bản cũ đếm
cả ERP (61) và đếm theo cách khác, bản này chỉ HRM + chỉ gate soi tĩnh được. Không phải mâu thuẫn,
là hai phép đo khác phạm vi.

**3 dạng lỗi đã kiểm chứng tận nơi (không phải báo động giả):**
1. Dòng seeder **bị comment** mà gate vẫn gọi — `Quản lý thân nhân` (seeder dòng 597 comment, và
   id 394 của nó bị quyền khác dùng lại ngay dòng 598), `Xem danh sách loại HĐLĐ theo tổng công ty`
   + `theo công ty` (dòng 562–563 đều comment).
2. **Gõ lặp từ** — gate gọi `Xem báo cáo tổng hợp kết quả khảo sát theo theo công ty` (2 chữ "theo"),
   seeder khai `…theo công ty`. **5 chỗ gọi.**
3. **Gate đòi 4 cấp, seeder chỉ khai 2** — `Xem danh sách danh hiệu khen thưởng theo bộ phận` /
   `theo phòng ban` không tồn tại; tương tự nhóm hình thức khen thưởng và `hạng mục dự án` (4 cấp,
   seeder không khai cấp nào).

🐞 Bộ soi bản đầu báo **98** quyền ma — 77 trong đó là báo động giả, đã sửa 3 nguyên nhân:
regex `checkPermissionList` gặp tên hàm trong **comment** rồi vớ lấy mảng bất kỳ ở dòng dưới
(route path `/warehouse-import-requests` bị báo là quyền); bộ soi **quét cả chính nó** nên khớp với
các mẫu regex trong mã nguồn của mình; và **chuỗi nội suy biến** bị coi là tên tĩnh.

### 2.3 — Lớp tương thích

- [ ] 6 hàm kiểm quyền nhận **cả `name` lẫn `code`** (resolve qua map cache) — giữ nguyên tên hàm,
      chỉ đổi tham số, để chuyển cuốn chiếu mà không phải sửa hết một lượt
- [ ] `hrm-client`: `hasAPermission` nhận cả hai; store nạp thêm `code`
- [ ] `config/permission_scopes.php` khoá theo `code` thay vì id

### 2.4 — Cấu trúc lại seeder

- [ ] Lớp cơ sở `PermissionSeeder`: `updateOrInsert` theo id (**bỏ hẳn `delete()`**), chặn id ngoài dải
- [ ] Tách `PermissionsTableSeeder` 1.398 dòng thành seeder theo phân hệ
- [ ] Xoá 116 dòng `// Permission::create` chết
- [ ] ⛔ **KHÔNG đăng ký 3 seeder Finance mồ côi** cho tới khi cấp lại id — `AdditionAccountingRequest…` khai id **1177–1180** đang là quyền phân hệ Giao việc, trong đó 1179/1180 mỗi cái có **2 dòng gán thật**. Cả 3 KHÔNG kế thừa `PermissionSeeder` nên 10 chốt không bảo vệ. Xử lý đúng: cấp lại id theo dải finance **2700–2799** rồi mới đăng ký (task riêng)
- [ ] Dải id theo module (1800–1999 để trống cho Quản trị hệ thống)

### 2.5 — Chuyển call site, MỖI MODULE MỘT ĐỢT

**Thí điểm CHẤM CÔNG — XONG phần BE 2026-09-05.** User chọn module phức tạp để kiểm chứng cách làm,
và lựa chọn đó đã chứng minh giá trị ngay: nó lộ ra 2 lỗi mà module nhỏ sẽ không bao giờ chạm tới.

- [x] `Modules/Timesheet/Entities/TimesheetPermission` — **78 hằng số**, 8 nhóm. Tên hằng số suy
      máy móc từ `code` (bỏ đoạn phân hệ, chấm → gạch dưới, viết hoa) nên tra ngược được.
- [x] Đổi **217 chỗ gọi / 36 file** trong `hrm-api`
- [x] Khai `type = 1` cho 78 quyền Chấm công → **chốt 4 về 0**, hạ mốc bánh cóc 78 → 0
- [x] **Chốt 6 (mới)**: giá trị hằng số phải tồn tại trong seeder — bịt đúng lỗ do chính việc
      chuyển sang hằng số tạo ra (xem dưới). Đã kiểm bằng cách gõ thừa một chữ vào hằng số → đỏ ngay.
- [x] **FE Chấm công XONG 2026-09-05** — 65 chỗ / 27 file, xem khối riêng bên dưới
- [ ] Các module còn lại: Payroll · Human · Assign · Training · Decision · Rice · Finance · MasterData
- [ ] Bỏ nhánh tương thích khi không còn call site dùng `name`

**Một dòng = một `group` không đủ để đặt hằng số ở đâu.** 43/78 quyền Chấm công là báo cáo (20),
dashboard (3), thiết lập, phân quyền — **không Entity nào sở hữu chúng**. Nên chọn MỘT lớp hằng số
cho cả phân hệ thay vì rải lên từng Entity như chốt ban đầu. Vẫn không phải "một file 722 hằng số"
mà chốt đã bác — mỗi phân hệ một file, khớp luôn với cách tách seeder ở 2.4.

**🔑 Lỗi 1 — bộ tách hậu tố phạm vi bỏ sót dạng gạch ngang.** Seeder dùng HAI kiểu nối cấp:
`"…theo bộ phận"` và `"…- bộ phận"`. **91 quyền dùng kiểu gạch ngang** mà `splitLevel()` chỉ biết
` theo `, nên cấp bị nướng vào tên đối tượng: `timesheet.danh_sach_don_nghi_phep_bo_phan.view`
(4 đối tượng rời) thay vì `timesheet.danh_sach_don_nghi_phep.view.part` (1 đối tượng, 4 biến thể).
Sửa xong phải **phát hành lại toàn bộ code** — may là chưa có gì phụ thuộc. Ma trận cũng chính xác
hơn theo: ô checkbox 285 → 293, ô popup 200 → 192. Module nhỏ không có quyền dạng này.

**🔑 Lỗi 2 — chuyển sang hằng số làm MÙ chính bộ soi.** Sau khi đổi, chốt 1 không còn đọc được tên
quyền ở 217 chỗ vừa chuyển (`Tên quyền dùng ở gate` 509 → 440, `gate truyền hằng số` 70 → 220).
PHP chỉ bảo đảm hằng số TỒN TẠI, **không** bảo đảm giá trị khớp seeder — sửa tay một chữ trong lớp
hằng số là quay lại đúng bệnh quyền ma, nấp kỹ hơn. Vì vậy phải thêm chốt 6. **Mọi module sau đều
phải làm bước này, không được bỏ.**

🐞 Lỗi của chính bộ thay thế: nó sửa cả chuỗi **nằm trong comment** — 6 chỗ bị chèn
`TimesheetPermission::X` vào giữa câu văn giải thích, có chỗ hỏng nghĩa. Đã khôi phục đủ 6 và bổ
sung ghi chú vào script. Module sau phải dùng bản token-aware (chỉ thay trong
`T_CONSTANT_ENCAPSED_STRING`).

#### FE Chấm công (2026-09-05)

- [x] Command `permission:export-js` — **SINH** `hrm-client/utils/permissions/timesheet.js` từ lớp
      hằng số PHP. Không gõ tay hai bên: FE và BE gate cùng một bộ quyền bằng chuỗi so khớp chính
      xác, hai nguồn sự thật thì sẽ lệch — không phải "nếu" mà là "khi nào".
- [x] Đổi **65 chỗ / 27 file** (`components/menu.js` 32 chỗ)
- [x] `utils/mixins/PermissionConstants.js` + đăng ký ở `plugins/global-mixins.js`
- [x] **Chốt 7**: file JS phải khớp tuyệt đối bản PHP. Đã kiểm bằng cách sửa tay một giá trị
      trong file JS → đỏ ngay.

**🔑 Lỗi 3 — hằng số trong `<template>` làm vỡ trang.** Vue chỉ phân giải thuộc tính của
**instance** trong `<template>`, KHÔNG thấy biến `import` ở đầu file. 7 chỗ ở 3 file rơi vào
`<template>` và trang "Tổng hợp phân ca" vỡ:

    [Vue warn]: Property or method "TimesheetPermission" is not defined on the instance
    TypeError: Cannot read properties of undefined (reading 'CA_LAM_VIEC_OTHER_PHAN_CA_COMPANY')

**Build sạch, 7 test xanh — chỉ mở trang ra mới lộ.** Đúng lý do quy tắc dự án bắt kiểm Playwright
trước khi báo xong. Sửa bằng global mixin phơi hằng số ra cho mọi `<template>`, làm một lần thay vì
sửa từng file.

🐞 Bộ thay thế FE lại mắc lỗi ngữ cảnh, lần này khác kiểu BE: nó thay cả **nhãn hiển thị**
(`label:`, `title:`, `name:`) và `hasGroup()` — hàm này so `permission.group` chứ không so `.name`.
18 chỗ ở 13 file. Đã đảo ngược hết; còn lại 65 chỗ **đều nằm trong ngữ cảnh kiểm quyền thật**
(`hasAPermission` · `hasMultiplePermission` · `hasPermission` · `showMenuChild` · `isShow:`).
Bài học cho module sau: **liệt kê ngữ cảnh HỢP LỆ rồi mới thay**, đừng thay mọi chuỗi khớp tên.

Bản đầu của bộ thay thế còn chạy quá 2 phút vì tính lại mặt nạ comment sau mỗi lần thay — đã đổi
sang che một lần cho mỗi file rồi thay theo offset.

**Kiểm chứng sau khi chuyển:**

| Ca | Kết quả |
|---|---|
| Cú pháp 36 file + lớp hằng số | `php -l` sạch |
| 4 API Chấm công đã đổi gate | `200` (gồm route dùng `'checkPermission:' . Const . '|' . Const`) |
| Màn phân quyền | phân hệ **Chấm công 8 nhóm / 78 quyền**, 12 dải, 0 lỗi console |
| Màn `/timesheet/overtime-assignment` | tải 10 dòng, không 403 |
| 6 test bánh cóc | xanh |
| `route:list` lỗi | **có sẵn** — lỗi y hệt trên bản git gốc của file routes |
| 8 lỗi console màn Đăng ký làm thêm | **có sẵn** — Vue warn trùng computed/data, file FE không đụng tới |
| Màn "Tổng hợp phân ca" sau khi sửa | bảng render, menu Chấm công đủ 7 mục, **0 lỗi console** |
| Line ending FE | CRLF giữ nguyên (`menu.js` 614 → 615 CR, +1 là dòng import mới) |
| **Ca KHÔNG có quyền** | đẩy về `/pages/extras/404` "không được cấp quyền truy cập", menu ẩn |
| 7 test bánh cóc | xanh; chốt 6 và 7 đều đã thử tiêm lỗi để chắc chúng thật sự đỏ |

### 2.6 — Dọn nợ dữ liệu

- [ ] Migration cứu **1.100 dòng gán mồ côi** (161 quyền đã biến mất, 49 chức vụ) — riêng bộ khách hàng
      166/168/169 → 1517–1522 là 49 dòng của 12 chức vụ
- [ ] Xử lý 89 quyền ma (`gate-quyen-ma.md`): quyền đã bỏ thì xoá gate, gõ sai thì sửa

### Việc KHÔNG làm ở Phase 2

Không đụng ERP `TanPhatDev` · không gom 6 hàm kiểm quyền về một facade · không đẻ quyền nâng cao
(In/Export/Khoá) · không tách module `Administration`.

## Phase 0.5 — Khảo sát dữ liệu thật + mockup MA TRẬN (đối tượng × hành động)

> Khởi nguồn: user gửi ảnh Excel phác thảo mô hình ma trận (Đối tượng | Đường dẫn | Quản lý |
> Xem | Tạo | Sửa | Xóa | Duyệt | Cấp duyệt | Phạm vi dữ liệu | Quyền nâng cao) + popup
> "Quyền nâng cao" 3 nhóm. User nói rõ đó là **ý tưởng sơ bộ để tham vấn**, yêu cầu khảo sát
> rồi đề xuất phương án phù hợp.

- [x] Đếm & phân rã 627 quyền trên `gop_db` (`PermissionsTableSeeder`) theo type / group / động từ
- [x] Gộp hậu tố phạm vi → **372 quyền gốc**; quy ra **~303 đối tượng** toàn hệ thống
- [x] Đọc `PermissionHelper::checkPermissionList()` để chốt mô hình phạm vi thật đang chạy
- [x] Dựng mockup ma trận có công tắc **Bản A (10 cột) ↔ Bản C (12 cột)** trên dữ liệu THẬT
      2 phân hệ: Chấm công (78 quyền → 24 đối tượng), Tính lương (57 quyền → 18 đối tượng)
- [x] Verify Playwright 1440 — 0 lỗi console
- [ ] User chọn A hay C → chốt bộ cột
- [ ] Cập nhật `design.md` + spec theo mô hình đã chốt

**File:** `.plans/demo-man-hinh-ke-toan/demo/phan-quyen-matrix.html` + `assets/permissions-matrix.js`
(xem qua `python3 -m http.server 8977` trong thư mục `demo`).

### Kết quả khảo sát — 4 điểm ảnh lệch dữ liệu thật

| # | Ảnh phác thảo | Dữ liệu thật HRM |
|---|---|---|
| 1 | Mỗi đối tượng có Tạo/Sửa/Xóa rời | **203/303 đối tượng (67%) chỉ có ĐÚNG 1 hành động**; chỉ 10 đối tượng đủ 4. **78 đối tượng chỉ có 1 quyền "Quản lý X"** gói cứng Tạo+Sửa+Xóa — FE không tách được |
| 2 | Cột "Quyền nâng cao" (In/Export/Khóa/Sao chép…) | Trong 627 quyền: In=0, Export=0, Sao chép=0, Huỷ duyệt=0, Lưu trữ=0, Khóa=0, **Import=2**. Cả cột là quyền **đẻ mới** |
| 3 | Cột "Cấp duyệt" C1/C2/C3 dùng chung | Không có bảng cấp duyệt. Duyệt nhiều cấp mã hoá bằng **tên quyền** ("Trưởng phòng duyệt X", "Ban giám đốc duyệt X", "NSHC duyệt X") — **16 quyền**, chỉ ở Giao việc + Đào tạo, mỗi màn một bộ cấp riêng |
| 4 | Phạm vi dữ liệu **chọn nhiều**, mặc định "xem của chính mình" | `checkPermissionList()` là chuỗi `if/else` **chọn 1 cấp, cấp cao thắng** (không cộng dồn). Chỉ 4 cấp `Tổng công ty → Công ty → Phòng ban → Bộ phận`; không có "Cấp dưới"/"Phòng quản lý" (đã nằm trong "Phòng ban" = phòng mình quản lý + bản ghi mình tạo). **Không quyền = thấy RỖNG** (fail-closed), không phải thấy-của-mình |

### Quyết định đã chốt trong Phase 0.5

- **Ô check-all đổi tên "Quản lý" → "Tất cả"**: trong HRM `"Quản lý X"` là **tên quyền thật** của
  78 đối tượng, trùng chữ sẽ gây hiểu nhầm nghiêm trọng.
- **Xem + Phạm vi dữ liệu = 1 quyền**, không phải 2: trong CSDL `"Xem X theo công ty"` vốn là
  MỘT permission → select Phạm vi chỉ chọn *biến thể*, không tính riêng khi đếm.
- Select Phạm vi **khoá lại khi checkbox Xem/Quản lý tắt** (không cho chọn cấp cho quyền chưa cấp).
- Ô `–` xám = **hệ thống không có quyền tương ứng**, khác hẳn ô có checkbox chưa tích.
- Ma trận cần **full width** → panel "Quyền đã phân" 8:4 bên phải của Phase 0 không còn chỗ,
  thay bằng **thanh tổng hợp ghim đáy** (số quyền + chip theo phân hệ + nút Lưu).
- 2 ca thử được cài sẵn trong mockup để so A/C:
  `Đề nghị tra soát công` (2 bước `PD-` + `XN-`) và `Đơn nghỉ phép` (`PD-` + `NSHC`);
  `Phân ca theo công ty/phòng ban/bộ phận` = **thao tác có phạm vi** (ca ngoại lệ mô hình cũ không xử được).

### Bản D — phản hồi của user: A vỡ ở màn có quyền nghiệp vụ riêng

User nêu: *"Phiếu nhập kết quả có thêm quyền: Duyệt kết quả / Xử lý kết quả…"* → bộ cột cố định
của bản A không chứa nổi. **Đo lại: 62/346 quyền gốc (17%) không khớp 6 cột cố định**, và chúng
nằm đúng ở các màn nghiệp vụ chính:

| Đối tượng | Quyền thật không khớp cột |
|---|---|
| Phiếu giao công việc | `Nhập kết quả công việc` · `TP duyệt phiếu giao công việc` · `TP duyệt kết quả công việc` |
| Phiếu giao công tác | `Gia hạn, kết thúc sớm` · `Nhập kết quả công tác` · `Tạo/Duyệt hồ sơ thanh toán` |
| Đề nghị thanh toán / Quyết toán HĐ | `TP Duyệt` + `KT Duyệt` — **2 bên duyệt SONG SONG**, không phải cấp 1→2 |
| Báo giá | `Xây dựng giá bán` · `TP duyệt giá BOM` · `BGĐ duyệt giá BOM` |

⇒ Hai kết luận: (a) **một đối tượng có NHIỀU loại duyệt khác nhau** (duyệt phiếu ≠ duyệt kết quả),
cột `Duyệt` đơn không đủ; (b) cột `Cấp duyệt` của bản C **sai mô hình** với ca duyệt song song.

- [x] Dựng **bản D**: ma trận + cột **Quyền khác** (popup chứa quyền THẬT còn lại của chính đối tượng)
      + ô `Duyệt` nhiều loại mở popup thay vì chip
- [x] Thêm phân hệ **Giao việc** (41 quyền gốc → 5 đối tượng) làm ca thử
- [x] Nhãn đỏ **"N quyền không có chỗ"** ở bản A/C để nhìn thấy chỗ rơi quyền
- [x] Verify Playwright 1440 — 0 lỗi console

**Bằng chứng định lượng** (cùng một trạng thái đã tích, đổi bộ cột):
`Bản A = 10 quyền` · `Bản C = 10 quyền` · `Bản D = 12 quyền` — A và C **làm mất 2 quyền đã cấp**
(`Nhập kết quả công việc`, `Nhập kết quả công tác`) vì không có chỗ hiển thị.

**Khác biệt C vs D:** popup của C là **danh mục cứng** (Import/Export/Print/Khoá/Sao chép…) mà HRM
chưa có dữ liệu; popup của D là **quyền thật đang có trong CSDL** của đúng màn đó — không đẻ quyền
mới, không migration.


### Bỏ cột "Đường dẫn" (2026-08-27)

User chốt: **menu thay đổi liên tục nên KHÔNG bắt vào permission**. Đã gỡ cột `Đường dẫn` khỏi
cả 3 bộ cột A/C/D, gỡ luôn 47 trường `path` trong dữ liệu mockup và bỏ nó khỏi ô Tìm nhanh
(placeholder còn "Tìm theo tên đối tượng..."). Cột `Đối tượng` nới `min-width` 250→320px.

⇒ **Quy tắc chốt cho Phase 1**: đối tượng quyền định danh bằng **chính nó** (`permissions.group`
+ tên quyền), KHÔNG neo vào vị trí menu. Bảng ma trận còn: A 9 cột · C 11 cột · D 10 cột.

⚠️ Gotcha khi verify: sửa file JS xong mà trình duyệt vẫn hiện bản cũ — profile Chrome persistent
cache rất dai, `?v=` trên cả thẻ `<script>` lẫn URL đều KHÔNG ăn. Cách chắc ăn: **mở PORT MỚI**
(đang chạy `8991`). Xem [[playwright-mcp-cache-lock-gotcha]].


### Sticky tiêu đề + thiết kế lại cột Phạm vi dữ liệu (2026-08-27)

**1. Sticky 2 tầng khi cuộn** — tên phân hệ ghim ở `top: var(--topbar-h)`, hàng tiêu đề cột ghim
ngay dưới nó. Cuộn sâu vẫn biết đang ở phân hệ nào + cột nào.
- Bỏ `overflow-x:auto` ở desktop (`.pm-scroll{overflow:visible}`, chỉ bật scroll ngang dưới 1200px)
  — **wrapper overflow tạo scroll container làm sticky dọc chết**, đây là nguyên nhân gốc.
- Bỏ `overflow:hidden` trên `.pm-sub` (cắt mất phần tử sticky).
- Chiều cao header phân hệ **đo lúc runtime** (`pmMeasureStickyOffset()` + listener `resize`) ghi vào
  biến `--pm-subhd-h`; hardcode 41px để hở 0,7px lộ dòng dữ liệu chạy phía sau. Đo xong: khít −0,3px.

**2. Cột Phạm vi dữ liệu — bỏ `<select>`, chuyển BẬC THANG + chỉ hiện khi đã cấp Xem** (user yêu cầu)
- Chưa tích `Xem` → ô Phạm vi **trống hoàn toàn** (không phải `–`; `–` giữ nghĩa "không áp dụng").
- Tích `Xem` → hiện dải bậc `Tổng cty · Công ty · Phòng ban · Bộ phận` (chỉ cấp đối tượng đó có thật),
  **mặc định cấp HẸP NHẤT** — theo nguyên tắc fail-closed, không mặc định cấp rộng.
- Bấm lại bậc đang chọn = bỏ chọn. Bỏ tích `Xem` → xoá luôn bậc đã chọn (không giữ ngầm).
- Áp cùng cơ chế cho cột **Cấp duyệt** của bản C (gate = ô `Duyệt`).
- Gỡ sạch `pm-sel` / `pmSelChange`; `Chọn cả nhóm` nay thao tác trên bậc thang.

⇒ Lợi: bảng phẳng hơn, bớt 1 lớp control; và **không còn cảnh chọn được phạm vi cho quyền chưa cấp**.

- [x] Verify Playwright 1440: gate ẩn/hiện đúng, tổng đếm 10 → 9 → 10 khi bỏ/tích lại `Xem`


### BỎ HẲN cột Phạm vi dữ liệu → popup (2026-08-27, đợt 2)

User: *"cột Phạm vi dữ liệu vẫn luôn có ⇒ bỏ được đi, vì bản chất cột đó chỉ phục vụ cột Quyền xem.
Khi có chọn quyền xem ⇒ hiển thị popup chọn phạm vi xem."* — đúng: cột đó chiếm chiều ngang toàn
bảng nhưng chỉ có nghĩa cho ~1/3 số dòng.

- [x] **Xoá cột `Phạm vi dữ liệu`** khỏi cả 3 bộ cột. Số cột: A 9→**8** · C 11→**10** · D 10→**9**
- [x] Gộp vào chính ô `Xem`: `checkbox` + **nhãn cấp** (`⊕ Công ty`) nằm cạnh nhau
- [x] **Tích `Xem` → popup "Phạm vi xem dữ liệu" tự bật**; bấm nhãn để đổi lại
- [x] Popup: radio 1 cấp + ghi chú *"cấp cao bao hàm cấp thấp"* + cột phụ `cấp 1..4`;
      chỉ liệt kê cấp đối tượng đó **thực sự có quyền**
- [x] Bỏ tích `Xem` → nhãn ẩn + **xoá phạm vi đã chọn** (không giữ ngầm)
- [x] Áp cùng cơ chế cho `Quản lý` có phạm vi (ca `Phân ca`)
- [x] Gỡ sạch bậc thang inline của đợt trước ở cột Phạm vi (chỉ còn dùng cho `Cấp duyệt` bản C)

**Demo: đưa chức năng có `Quyền khác` lên đầu** (user yêu cầu, khỏi cuộn tìm) — sort ổn định 3 tầng:
phân hệ → nhóm → đối tượng, hạng nào có `other` xếp trước. `Giao việc` nay là phân hệ đầu tiên.
Chỉ là thứ tự **trình bày của mockup**, không phải quy tắc nghiệp vụ.

- [x] Verify Playwright: bấm nhãn mở đúng popup · tích `Xem` tự bật popup · chọn "Công ty" + Áp dụng
      → nhãn đổi thành `⊕ Công ty`, tổng 10 → 11. 0 lỗi console.

⇒ **Bảng giờ chỉ còn checkbox + vài nút popup**, không còn control nào chiếm chiều ngang cố định.


### ✅ CHỐT BẢN D — và sửa lỗi popup không lưu lựa chọn (2026-08-27, đợt 3)

User chốt: **phát triển tiếp từ bản D**. Yêu cầu kèm: *"popup chọn ở Quyền xem / Quyền khác sau khi
chọn phải hiển thị đúng data đã chọn"*.

**Nguyên nhân gốc: trạng thái đang nằm ở DOM, không nằm trong `PM_DATA`.** Kéo theo 3 lỗi:
1. `pmOpenList` (Quyền khác / Các loại duyệt) **không gán lại `onclick` cho nút "Áp dụng"** dùng chung
   → mở popup Quyền khác sau popup Phạm vi thì bấm Áp dụng chạy nhầm `pmApplyScope()`, **ghi bậy sang
   nhãn phạm vi**.
2. Không có `pmApplyList` → tích trong popup không được lưu; đóng ra là mất, nút trên bảng
   (`1/1`, `3 loại`) không đổi, số tổng không đổi.
3. `pmSetVariant` vẽ lại từ `PM_DATA` → **đổi bản A/C/D là mất sạch thao tác** của user.

**Cách sửa — `PM_DATA` là nguồn sự thật duy nhất:**
- Mọi control ghi thẳng vào data (`pmToggle` · `pmApplyScope` · `pmApplyList` · `pmChip` · `pmSegPick`
  · `pmToggleAllRow` · `pmBulkGroup`), rồi `pmRefreshRow()` / `pmRefreshObj()` vẽ lại từ data.
- `pmBindApply(handler)` — gán lại handler nút "Áp dụng" **mỗi lần mở popup** (modal dùng chung).
- `pmRecount()` đếm từ `PM_DATA` chứ không quét DOM → **đổi bản không làm số nhảy**.
- Bỏ hẳn `pmCountIn` / `pmSyncGates` / `pmLevelsOf` / `PM_SCOPE_BTN` (đều là state trên DOM).
- Ô `Duyệt` bật → cấp **bước ĐẦU** (không phải tất cả các bước); bước cụ thể chọn ở cột Cấp duyệt (bản C).
- Ô `Tất cả` của mỗi dòng nay **tự phản ánh** trạng thái (`pmObjAllOn`), không còn luôn trống.

**Verify Playwright (bản D, đối tượng `Phiếu giao công tác`):**

| Kịch bản | Kết quả |
|---|---|
| Popup Quyền khác: tích 2 mục → Áp dụng | nút `–` → **`3/3`**, tổng 12 → 14 |
| Mở lại popup Quyền khác | `[true, true, true]` — đúng cái đã chọn |
| Popup Duyệt: tích bước 3 → Áp dụng | nút **`1/3`** |
| Mở lại popup Duyệt | `[false, false, true]` — đúng bước 3 |
| Popup Phạm vi: chọn "Tổng công ty" | ô Xem hiện **`⊕ Tổng công ty`**; mở lại radio đúng |
| Đổi bản D→A→C→D | tổng **16 ở cả 3 bản**, trạng thái giữ nguyên |

⚠️ Suýt hỏng: khi thay khối popup đã xoá nhầm `pmSeg()` (bản C còn dùng cho cột Cấp duyệt)
→ `ReferenceError` lúc đổi sang bản C. Đã thêm lại.

**Bước tiếp:** cập nhật `design.md` + spec `docs/superpowers/specs/gop-db/2026-08-14-...` theo mô hình
bản D đã chốt, rồi mở Phase 1 (port vào `hrm-client`).


### Rút về 6 cột — bỏ Tạo/Sửa/Xóa, phân đôi loại đối tượng (2026-08-27, đợt 4)

User chốt: bỏ A và C, chỉ giữ D; **bỏ 3 cột Tạo/Sửa/Xóa**; và phân loại đối tượng:
- **Phiếu cá nhân** → `Xem · Duyệt · Quyền khác` (ô Quản lý = `–`)
- **Phiếu chung / danh mục** → `Quản lý · Xem · Duyệt · Quyền khác`

**Bộ cột cuối: `Đối tượng · Tất cả · Quản lý · Xem · Duyệt · Quyền khác`** (6 cột, từ 12 lúc đầu).
`Quản lý` đặt TRƯỚC `Xem` theo đúng thứ tự user liệt kê.

⚠️ **Cạm bẫy đã chặn kịp:** bỏ thẳng 3 cột Tạo/Sửa/Xóa sẽ **mất trắng 30 quyền thật** — có
**11 đối tượng chỉ có quyền CRUD rời, KHÔNG có quyền "Quản lý X"** trong CSDL (Mẫu bảng lương,
Lương P3, Thu nhập khác, Khấu trừ khác, Các thành phần khác, Bảng tổng hợp/phân công/chi trả lương,
Tạm ứng lương, Cơ cấu định biên nhân sự, Bảng chia thưởng). Xử lý: **gom chúng vào chính ô `Quản lý`**
— 1 checkbox tím `.pm-ck--bundle` bật/tắt cả cụm, tooltip ghi rõ *"Gồm 3 quyền: Tạo · Sửa · Xóa"*
(Bảng chia thưởng chỉ có `Tạo` → *"Gồm 1 quyền: Tạo"*). Số tổng vẫn đếm theo **quyền gốc**, không
phải theo ô.

**Phân bố thực tế 47 đối tượng:** 11 có quyền `Quản lý X` · 11 chỉ có CRUD rời (gom vào Quản lý)
· 25 không có cả hai → ô Quản lý là `–`, tức **phiếu cá nhân / báo cáo / dashboard**.

- [x] Gỡ toàn bộ nhánh bản A và C (`PM_VARIANT`, `pmSetVariant`, công tắc, `pmIsC/pmIsD`,
      cột `Cấp duyệt` + `pmSeg/PM_SHORT/pmSegPick`, cột `Quyền nâng cao` + `PM_ADV_GROUPS/pmOpenAdv`,
      nhãn đỏ `pmLostCount`, chip `pmChip`) — file 756 dòng
- [x] Bỏ 3 cột Tạo/Sửa/Xóa, gom vào `Quản lý`
- [x] Bộ lọc "Hành động" bám bộ cột mới (Quản lý · Xem · Duyệt · Quyền khác · Có phạm vi xem)
- [x] 🐞 Fix `TypeError: Cannot read properties of undefined (reading 'lv')` — `pmToggle` mở popup
      phạm vi vẫn đọc `o.manage.lv` cho đối tượng gom CRUD (không có `o.manage`) → thêm guard
- [x] Verify: bundle ON → tổng 12→15 (đúng 3 quyền), OFF → về 12; đếm từ data khớp 12/12; 0 lỗi console

**Còn treo (đã hỏi, user chưa chốt):** ô `Tất cả` — (a) nó bật *mọi* bước Duyệt trong khi ô `Duyệt`
chỉ bật bước đầu; (b) nó tự gán phạm vi xem **cấp hẹp nhất** mà không mở popup.


### Panel phải + dọn text hướng dẫn (2026-08-27, đợt 5)

- [x] **Bỏ nút "← Bản cũ"** (mockup cây checkbox Phase 0 không còn dùng để đối chiếu)
- [x] **Panel "quyền đã phân" bên phải** — lưới `minmax(0,1fr) / 320px`, sticky dưới topbar,
      body cuộn riêng. Nội dung dựng từ `PM_DATA`: số tổng + nút **Lưu** trên header ·
      chip đếm theo phân hệ · danh sách gom **Phân hệ → Đối tượng → quyền**, chip màu theo loại
      (Xem xanh · Quản lý tím · Duyệt cam · Quyền khác xanh dương), Xem kèm badge cấp phạm vi.
      Dưới 1360px thì panel xuống dưới bảng.
- [x] Bỏ thanh tổng hợp ghim đáy (`.pm-bar`) — panel thay thế
- [x] **Dọn sạch text hướng dẫn**: dòng mô tả dưới banner · dòng mô tả dưới tiêu đề "Ma trận phân quyền"
      · 3 khối `.pm-hint` trong popup (phạm vi / các loại duyệt / quyền khác)
- [x] Nút **Lưu** chuyển lên header panel — để ở đáy panel thì lúc chưa cuộn nó rơi ngoài màn
      (panel bắt đầu ở y≈250, cao 695 > viewport 779)

🐞 **Lỗi lệch bảng ↔ panel (đã fix):** ô `Xem` suy trạng thái từ `o.view.def` (phạm vi đã chọn)
thay vì `o.view.on` — tàn dư từ trước khi có cờ `on`. Hệ quả: **tích Xem rồi bấm Đóng popup
(không chọn cấp) → bảng hiện ô trống nhưng panel vẫn đếm quyền đó**. Nay ô luôn đọc `o.view.on`;
quyền đã cấp mà chưa chọn cấp thì nhãn hiện `⊕ Chọn phạm vi`.

Verify 4 bước trên `Quyết toán hợp đồng` — data / DOM / panel khớp nhau ở mọi bước:
đầu (off·12) → tích Xem + Đóng popup (on · trống · **☑** · 13) → chọn Công ty (on · Công ty · 13)
→ bỏ tích (off · trống · 12). 0 lỗi console.


### Gộp 1 bảng + cách "phân trang" khi lên 12 phân hệ (2026-08-27, đợt 6)

User nêu 2 vấn đề khi đưa vào ERP: (a) 12 phân hệ, rất nhiều quyền → phân trang thế nào;
(b) mỗi phân hệ 1 `<table>` nên **header lệch nhau, rối**.

**Số đo thật (chỉ riêng HRM, 627 quyền):** 279 đối tượng · 129 nhóm · 11 phân hệ.
Phân bố **rất lệch**: Giao việc 76 đối tượng/32 nhóm · Đào tạo 58 · Chấm công 33 · HCNS 33
· … · có phân hệ chỉ 1 đối tượng. Trung bình 25 đối tượng/phân hệ. Thêm ERP → cỡ 400–500 đối tượng.

**(b) GỘP VỀ MỘT BẢNG — đã làm.** Trước: N `<table>` rời, mỗi bảng tự tính độ rộng cột nên
cột không thẳng hàng, lại có N hàng tiêu đề cùng ghim. Nay **1 `<table>` + 1 `<thead>` duy nhất**;
phân hệ trở thành **dải ngang** `tr.pm-srow` (nền xanh, ghim ngay dưới thead), nhóm chức năng vẫn là
dải xám `tr.pm-grow`. Mỗi nhóm = 1 `<tbody class="pm-body" data-si data-gi>`; thu/mở phân hệ =
ẩn/hiện mọi tbody cùng `data-si`.
Verify: `so_bang = 1`, `so_thead = 1`, độ rộng cột của dòng thuộc Giao việc / Chấm công / Tính lương
**bằng nhau tuyệt đối** `[428, 77, 155, 195, 90, 122]`. Sticky 2 tầng: thead ở `top = 60` (topbar),
dải phân hệ ở `top = 90`.
⚠️ Sticky trên `<tr>` ở các `<tbody>` khác nhau **không đẩy nhau** mà **chồng lên nhau**; z-index bằng
nhau nên dải trong DOM sau vẽ đè lên — tình cờ đúng dải đang xem. Chấp nhận được, nhưng nhớ khi port.

**(a) PHÂN TRANG — kết luận: KHÔNG phân trang theo dòng.** Lý do:
- Màn phân quyền là **MỘT form, lưu MỘT lần**. Cắt trang theo dòng làm trạng thái rải rác giữa các
  trang → bấm Lưu rất dễ **mất quyền đã tick ở trang trước** (hoặc phải giữ state client phức tạp).
- Cắt trang theo dòng sẽ **cắt ngang nhóm chức năng**, mất ngữ cảnh.
- Phân bố lệch (1 → 76 đối tượng/phân hệ) khiến "N dòng/trang" vô nghĩa.

**Cách thay thế đã áp dụng — đơn vị điều hướng là PHÂN HỆ:**
- [x] Mặc định **thu gọn hết, chỉ mở phân hệ đầu** → 12 phân hệ = 12 dòng, vừa 1 màn
- [x] Dải phân hệ mang badge xanh **"đang cấp N"** → thu gọn rồi vẫn biết phân hệ nào đã phân quyền
- [x] Bộ lọc Phân hệ / Nhóm / Hành động / Tìm nhanh + nút Mở tất cả / Thu gọn để nhảy thẳng
- [x] Panel phải cho cái nhìn tổng thể những gì đã cấp — không phải cuộn bảng để kiểm tra

**Chưa làm, chỉ cần khi số đối tượng phình:** *render lười* — chỉ dựng DOM của phân hệ khi mở
(hiện dựng hết: 279 đối tượng × 6 cột ≈ 1.674 ô, ~1.116 input; lên ERP sẽ gấp đôi).
Với Vue 2 nên cân nhắc ngay ở Phase 1.


### Màu riêng cho từng phân hệ (2026-08-27, đợt 7)

Gộp về 1 bảng xong thì 12 dải phân hệ cùng một màu xanh sẽ khó phân biệt → mỗi phân hệ **một tông riêng**.

Bảng màu `PM_HUES` — **12 tông, không trùng**, mỗi tông 3 giá trị: `bg` nền nhạt · `fg` chữ đậm
· `ac` vạch nhấn/badge:

| # | Tông | nền / nhấn | # | Tông | nền / nhấn |
|---|---|---|---|---|---|
| 1 | xanh lá | `#e6f4ec` / `#16a34a` | 7 | xanh ngọc | `#e2f6fa` / `#0891b2` |
| 2 | chàm | `#eaedfe` / `#4f46e5` | 8 | olive | `#f1f7e2` / `#65a30d` |
| 3 | hổ phách | `#fdf3e3` / `#d97706` | 9 | cam | `#fdeee4` / `#ea580c` |
| 4 | xanh trời | `#e4f4fd` / `#0ea5e9` | 10 | đỏ tía | `#fbeafc` / `#c026d3` |
| 5 | tím | `#f2eafe` / `#7c3aed` | 11 | xanh dương | `#e7effd` / `#2563eb` |
| 6 | hồng đậm | `#fdeaef` / `#e11d48` | 12 | xám xanh | `#eef1f5` / `#64748b` |

- Gán theo **chỉ số phân hệ** (`pmHue(si)`), truyền xuống CSS bằng biến `--c-bg/--c-fg/--c-ac`
  đặt inline trên `td` của dải → CSS không phải sinh 12 lớp.
- Ăn theo màu: nền dải · chữ tên phân hệ · **vạch nhấn trái 4px** · mũi tên thu/mở · badge
  **"đang cấp N"** · dòng đếm.
- **Panel phải đồng bộ cùng màu**: header nhóm phân hệ (nền + vạch trái), chip đếm, và vạch trái
  của từng đối tượng → nhìn panel là biết thuộc phân hệ nào mà không phải đọc chữ.
- `:hover` dùng `filter: brightness(.97)` thay vì màu cứng, nên áp được cho mọi tông.

⚠️ Nếu Phase 1 cần màu **ổn định theo phân hệ** (không đổi khi thứ tự phân hệ thay đổi) thì phải
map theo `permissions.type` chứ không theo chỉ số mảng như mockup đang làm.


### Phạm vi quyền DUYỆT (2026-08-27, đợt 8)

User: *"Quyền duyệt cũng cần phạm vi — có quyền chỉ duyệt theo Phòng ban / Bộ phận, có quyền duyệt
toàn công ty"*, và bổ sung: *"Trưởng phòng duyệt… thì chỉ duyệt phiếu có `department_id` nằm trong
danh sách ID phòng mà user quản lý"* — đã rà ở feature **màn duyệt tổng hợp ERP**.

❌ **Tôi làm sai vòng đầu**: đếm trên seeder HRM thấy 0/40 quyền duyệt có hậu tố phạm vi → kết luận
"phạm vi duyệt là thứ phải đẻ mới" và dựng UI cho admin **tự chọn** phạm vi duyệt (select trong popup).
Sai vì chỉ nhìn HRM, chưa rà ERP.

✅ **Nguồn thật: `ERP/TanPhatDev/config/approval_inbox.php` → `permission_scopes`** (17 quyền cấp phòng):

```
'department' → phiếu.department_id ∈ phòng user QUẢN LÝ (employee_manage_departments)
'part'       → phiếu.part_id ∈ bộ phận user quản lý        (chưa quyền nào dùng)
không khai   → 'company' (mặc định)
```
12 quyền `"Trưởng phòng duyệt …"` + 5 quyền khác (`Duyệt hợp đồng`, `Duyệt kế hoạch bán hàng phòng`,
`Duyệt kế hoạch phát triển thị trường phòng`, `Duyệt chỉ tiêu kinh doanh theo phòng ban`,
`Duyệt yêu cầu đặt hàng ngoài`). BGĐ / Ban kiểm soát / Kế toán / Kế toán trưởng / Thủ quỹ → `company`.
Super Admin bỏ qua siết.

⚠️ **Kết luận thiết kế — phạm vi duyệt là THUỘC TÍNH CỐ HỮU CỦA QUYỀN, KHÔNG cho admin chọn.**
Comment ngay trong config nói rõ: *"Scope này phản chiếu gate hardcode trong controller — đổi cùng
lúc với gate."* Cho admin chọn "Tổng công ty" cho quyền `Trưởng phòng duyệt…` sẽ **không có tác dụng
thật** (controller vẫn siết theo `EmployeeManageDepartment`) mà còn khiến người phân quyền tưởng đã
cấp rộng → nguy hiểm hơn là không hiển thị gì.

- [x] Gỡ select phạm vi duyệt (bản làm sai), gỡ `st.def` / `pmApRowToggle` / `.pm-apsel`
- [x] Mỗi loại duyệt mang `scope` suy từ tên (`^TP |^Trưởng phòng` → department, còn lại company)
- [x] Ô Duyệt 1 loại: checkbox + **nhãn phạm vi CHỈ ĐỌC** (cam = phòng ban · xám = toàn công ty),
      tooltip giải thích đúng cơ chế `department_id ∈ phòng user quản lý`
- [x] Popup nhiều loại duyệt: mỗi dòng = checkbox + nhãn phạm vi chỉ đọc
- [x] Panel phải: chip Duyệt kèm badge phạm vi

Verify: `Phiếu đề xuất công việc` → *Phòng ban quản lý* · `Đề nghị thanh toán` → TP *Phòng ban quản lý*
+ KT *Toàn công ty* · `Phiếu giao công tác` → 2 TP *Phòng ban quản lý* + `Duyệt hồ sơ thanh toán`
*Toàn công ty*. 0 lỗi console.

**Việc cho Phase 1/2:** nguồn `scope` phải đọc từ `permission_scopes` thật (17 quyền), KHÔNG suy từ
tên như mockup. Nếu sau này muốn cho admin **chỉnh** phạm vi duyệt thì phải chuyển gate hardcode
trong controller sang đọc cấu hình — việc BE lớn, tính riêng.


### Chốt: scope gắn theo QUYỀN (2026-08-28)

User chốt **scope gắn theo quyền**, không theo cặp chức vụ × quyền. Chi tiết + 3 rủi ro phải xử
khi làm thật: xem `design.md` mục "Quyết định đã chốt — Phạm vi quyền DUYỆT".

- [x] Bỏ suy scope theo tên → tra từ **map khai báo** `PM_SCOPE_MAP` (mô phỏng `permission_scopes`)
- [x] Mỗi bước duyệt có `scopeDeclared`; **chưa khai → viền đứt + icon cảnh báo + tooltip**,
      phân biệt "đã xác nhận cấp công ty" với "đang ăn mặc định"
- [x] Chỉ hiển thị mức thực dùng (`Phòng ban quản lý` / `Toàn công ty`), không vẽ 4 cấp như cột Xem

Số liệu ERP làm căn cứ: **979 quyền · 105 quyền duyệt · 17 khai `department` · 0 dùng `part`**;
chỉ 12/17 mang chữ "Trưởng phòng/TP" → suy theo tên sai 29%.

Verify trên mockup (19 quyền duyệt, 4 chưa khai):
`Phiếu giao công tác` → 2 TP *Phòng ban quản lý* + `Duyệt hồ sơ thanh toán` *Toàn công ty* ⚠ chưa khai ·
`Đề nghị thanh toán` → TP *Phòng ban* + KT *Toàn công ty* (đều đã khai) ·
`Đề nghị tra soát công` → cả 2 bước ⚠ chưa khai. 0 lỗi console.


### Chốt: định danh quyền bằng `code` bất biến (2026-08-28)

User chốt **áp dụng `code`**. Quy ước + lộ trình cuốn chiếu: xem `design.md` mục
"Quyết định đã chốt — Định danh quyền bằng `code` bất biến".

`<phân hệ>.<đối tượng>.<hành động>[.<biến thể>]` — vd `timesheet.leave_request.approve.tp`.
Hành động khớp đúng bộ cột ma trận (`manage`/`view`/`approve`/`other`) ⇒ khai `code` đúng là quyền
mới **tự rơi đúng ô**, không phải sửa FE.

**Phát hiện khi khảo sát chi phí — 89 quyền "ma":**
gate trỏ vào tên quyền KHÔNG tồn tại trong seeder ⇒ **vĩnh viễn trả `false`** (HRM 28 / 44 chỗ · ERP 61 / 120 chỗ).
Gồm cả sai chính tả (`Duyệt kế hoạch bán hàng phòng **ban**` vs seeder `…phòng`) và **thừa dấu cách**
(`Xem␣␣phiếu báo hàng…`). Ca nặng nhất: `Quản lý danh mục meeting` — **22 chỗ gọi**, không có trong seeder.
→ Danh sách đầy đủ kèm file:dòng: **`.plans/gop-db/thiet-ke-lai-phan-quyen/gate-quyen-ma.md`**
→ **Việc riêng, không thuộc feature này** — nên mở ticket, rà từng ca (có thể là quyền đã bỏ, hoặc gate gõ sai).

Quy mô chuyển đổi: HRM 332 tên / **774 lời gọi** · ERP 843 tên / **3.561 lời gọi**.

- [x] Khảo sát chi phí + đối chiếu gate ↔ seeder cả 2 hệ
- [x] Chốt quy ước `code` + lộ trình 6 bước, ghi `design.md`
- [x] Cập nhật spec: `code` thành mục Phase 2 số 2; bảng rủi ro thêm hàng #0 (89 quyền ma),
      nâng hàng #4 (trùng quyền tiền tệ) lên mức **Cao** vì seeder nổ trên DB sạch
- [ ] (Việc riêng) Mở ticket xử lý 89 quyền ma
- [ ] (Phase 2) Migration `permissions.code` + backfill 1.606 quyền + 5 chốt chặn CI


### Đợt 9 — dọn giao diện + thao tác hàng loạt (2026-08-28)

- [x] **Bỏ số `(N)` quyền gốc** cạnh tên đối tượng → chuyển thành **tooltip** (`cursor:help`);
      bỏ note `N đối tượng · N quyền gốc` trên dải nhóm. Giữ dòng đếm trên dải phân hệ.
- [x] **Banner gọn**: bỏ khối "Công ty: Cty Tân Phát Hà Nội", gộp dòng "Đang phân quyền cho chức vụ…"
      vào **chung card với bộ lọc** → bớt hẳn 1 card, bảng nhô lên ~55px.
- [x] **Panel "quyền đã phân" — thêm bộ lọc**: ô tìm nhanh (khớp cả tên đối tượng lẫn tên quyền)
      + 4 chip lọc theo loại `Quản lý / Xem / Duyệt / Khác` có số đếm, bấm lại để bỏ lọc;
      header mỗi phân hệ bấm thu gọn được, có badge số quyền theo màu phân hệ.
      ⚠️ Khung panel dựng **một lần**, chỉ dựng lại phần thân khi đếm — dựng lại cả panel thì
      đang gõ ô lọc sẽ **mất focus** sau mỗi ký tự.
- [x] **Panel — sửa phân cấp bị ngược**: dòng hành động trước đây là khối màu có nền, **nổi hơn cả
      tên chức năng**. Nay: tên chức năng 12px/700/đen là cấp cha; hành động là **text thuần, xám,
      lùi 14px**, màu loại thu về **chấm tròn 5px** đầu dòng; nhãn phạm vi thành chữ nghiêng xám canh phải.
- [x] **Tên phân hệ lấy đúng phần mềm** (`hrm-client/components/subsystems.js` → `label`),
      bỏ badge nhóm tự bịa. Sửa 2 chỗ sai: `Giao việc` → **`Dự án & giao việc`**; badge
      `2. Quản lý công việc` là bịa (phân hệ này thuộc nhóm thật `2. VĂN PHÒNG SỐ`) → gỡ hẳn.
- [x] **Nút "Chọn tất cả <Hành động>"** — chỉ hiện khi ô lọc Hành động chọn 1 hành động cụ thể,
      nhãn kèm số dòng bị tác động, cạnh nút bỏ chọn hàng loạt. Quy tắc:
      chỉ tác động **các dòng đang hiện** (tôn trọng cả lọc Phân hệ/Nhóm/từ khoá) ·
      **bỏ qua dòng có ô `–`** · với `Xem` thì tự gán phạm vi **cấp hẹp nhất** ·
      **không hiện** khi lọc `Có phạm vi xem` (là tiêu chí lọc, không phải hành động cấp được).
      Verify: lọc `Duyệt` → `Chọn tất cả Duyệt (12)` → tổng 12→23 → bỏ chọn → 11
      (11 chứ không phải 12 vì `Đơn nghỉ phép` vốn đã có sẵn quyền duyệt, bị gỡ cùng).

---

### Checkpoint — 2026-09-02

**Vừa hoàn thành:** Phase 1 — port màn phân quyền vào `hrm-client` + `hrm-api` thật, mở rộng phục vụ
**cả HRM lẫn ERP** trên DB gộp. 288 dòng ma trận từ 1.687 quyền, không rơi quyền nào. Verify
Playwright 1440 với 18 ca đo bằng số lấy từ DOM/DB, 0 lỗi console; trong đó có cả ca **không có
quyền** (403) và ca **chặn gán chéo guard**.

**Đang làm dở:** (không)

**Bước tiếp theo:**
1. User rà màn thật, chốt hình rồi mới viết e2e tự động cho `/admin/roles` + `/admin/roles/{id}`.
2. Rà gate của **122 quyền duyệt chưa khai `approve_scope`** rồi bổ sung `config/permission_scopes.php`
   (nhìn được ngay trên màn: nhãn viền đứt + ⚠).
3. Vẫn treo từ Phase 0, không phụ thuộc Phase 1: **89 quyền "ma"** (`gate-quyen-ma.md`) và cặp quyền
   tiền tệ trùng tên.

**Ghi nhận khi chạy seeder ngày 2026-09-02** (`--class='Modules\Timesheet\Database\Seeders\PermissionsTableSeeder'`):
quyền `api` 597 → **722**; xuất hiện thêm phân hệ 9, 23, 24, 25. Seeder **xoá 3 quyền khách hàng cũ**
(`Quản lý khách hàng` 166 · `Xem tất cả khách hàng theo công ty` 168 · `theo phòng ban` 169) và không
tạo lại — thay bằng bộ mới `Quản lý khách hàng` type 9 (id 1517–1522). **Không có migration chuyển
gán quyền cũ sang mới**, nên 49 dòng gán của 12 chức vụ thành mồ côi (Super admin 15, Admin_TPE 6…).
Cần quyết định có viết migration chuyển đổi hay cấp lại tay.

**Blocked:** (không)

### Checkpoint — 2026-08-28

**Vừa hoàn thành:** Phase 0 khép lại. Mockup ma trận hoàn chỉnh trên dữ liệu THẬT
(3 phân hệ / 47 đối tượng), 6 cột, 1 bảng duy nhất, sticky 2 tầng, 12 màu phân hệ,
panel "quyền đã phân" có lọc, thao tác hàng loạt theo hành động. Verify Playwright 1440,
0 lỗi console (chỉ 404 favicon). **Ba tài liệu đã đầy đủ và khớp nhau**: `design.md` (7 quyết định
đã chốt) · `plan.md` (9 đợt) · spec `docs/superpowers/specs/gop-db/2026-08-14-...` (viết lại toàn bộ,
8 mục, bảng 6 rủi ro).

**Đang làm dở:** (không) — mockup đã chốt hình, tài liệu đã đồng bộ.
Mockup: `.plans/demo-man-hinh-ke-toan/demo/phan-quyen-matrix.html` + `assets/permissions-matrix.js`
(1 file JS ~62 KB chứa cả dữ liệu, logic và CSS).

**Bước tiếp theo:**
1. User đọc spec → duyệt để mở **Phase 1**.
2. Phase 1 — port vào `hrm-client` (nhánh `gop_db`, hiện local đang ở `tpe`):
   `components/subsystem-menu/admin.js` → màn danh sách chức vụ → form ma trận **có render lười**;
   BE bổ sung metadata `object` / `action` / `scope_levels` / `approve_scope` cho `PermissionController@index`.
3. Việc RIÊNG, nên mở ticket ngay vì không phụ thuộc Phase 1:
   **89 quyền "ma"** (`gate-quyen-ma.md`) và **cặp quyền tiền tệ trùng tên** khiến seeder nổ trên DB sạch.

**Blocked:** (không)

---

### Checkpoint — 2026-08-14
Vừa hoàn thành: Phase 0 — mockup tương tác hoàn chỉnh 2 màn (danh sách + form phân quyền) trong bộ demo kế toán, đúng style HRM, verify Playwright qua nhiều vòng feedback.
Đang làm dở: (không) — mockup đã chốt hình. Chưa động vào code `hrm-client`/`hrm-api` thật.
Bước tiếp theo: Bắt đầu Phase 1 — port thiết kế từ mockup sang `hrm-client` (menu admin.js → màn danh sách → form phân quyền), + điều chỉnh nhỏ BE store 1 công ty. Trước khi code, chốt: (a) cách xác định "công ty của user", (b) quy ước map dữ liệu thật 617 permission.
Blocked:


---

## Phase 1b — Màn danh sách chức vụ theo chuẩn list-page (XONG 03/09/2026)

Màn `/admin/roles` ban đầu tự dựng khung riêng (`rl-head` / `rl-filter` / `rl-card` / `rl-table` /
`rl-paging` + `b-pagination`), không dùng bộ component chuẩn của phân hệ. Đã chuyển sang đúng chuẩn,
đối chiếu màn mới nhất làm đúng chuẩn: `pages/assign/internal-business-scopes/index.vue`.

- [x] Khung: `v2-styles min-vh-100 d-flex justify-content-center pt-2` › `container-fluid`
- [x] **Bộ lọc** → `V2BaseFilterPanel`: tìm nhanh (*tên chức vụ*) + bộ lọc nâng cao thu gọn được (*Hệ*)
- [x] **Bảng** → `V2BaseDataTable`: `title="Danh sách chức vụ"`, `columns`, `pagination`, `rowActions`,
      slot `#cell-*`; STT dùng `getNumericalOrder`; cột *Chức vụ* là link `v2-cell-link` mở ma trận;
      cột *Hệ* dùng `V2BaseBadge`
- [x] **Nút** → `V2BaseButton` trong slot `#actions`: *Xuất Excel* · *Phân quyền hàng loạt*
- [x] **Hành động dòng** → `rowActions`: *Phân quyền* (`ri-shield-user-line`) · *Lịch sử thay đổi* (`ri-history-line`)
- [x] Thêm `PageTitleMixin`; giữ `CheckPermission` + chốt fail-closed y như cũ
- [x] Gỡ toàn bộ CSS `rl-*` (138 dòng) — chỉ còn 2 rule cho dòng phụ `#id · trạng thái` và nút 0 quyền
- [x] **Sửa kèm 1 lỗi có sẵn**: `exportExcel` chỉ truyền `keyword`, bỏ sót `guard` → xuất Excel không
      theo bộ lọc *Hệ*. Nay truyền cả hai.

**Phạm vi: chỉ FE, 1 file** `pages/admin/roles/index.vue` (user chốt 03/09). **Không bật `sortable`**
cho cột nào vì `RoleService::index` chỉ nhận `keyword` + `guard` và sắp xếp cứng `orderBy('roles.id','desc')`
— bật sort sẽ hứa một hành vi BE không làm được. Muốn có sort / lọc theo Trạng thái · Người sửa · Ngày sửa
thì phải mở thêm ở BE.

### 2 lỗi tự phát hiện khi verify

1. `V2BaseBadge variant="secondary"` **không hợp lệ** — validator chỉ nhận
   `muted · brand · required · status-draft · status-ok · null`. Sai variant làm Vue bắn
   **25 warning** ra console (1 warning/dòng). Đổi sang `brand` (HRM) / `muted` (ERP) → console sạch.
   *(Ghi nhận: nhiều màn khác cũng đang truyền variant không hợp lệ — `secondary` 6 chỗ, `warning` 3,
   `info` 3, `primary` 1 — lỗi có sẵn, không sửa trong lượt này.)*
2. Đặt `pagination.pageSize = 25` nhưng `V2BaseDataTable.pageSizeOptions` mặc định là
   `[5, 10, 20, 50, 100]` → ô chọn số dòng/trang không có giá trị 25, người dùng đổi đi rồi
   **không chọn lại được**. Đổi mặc định về 10 như chuẩn.

### Verify Playwright 1440×900 (đo bằng số từ DOM)

| Hạng mục | Kết quả |
| --- | --- |
| Còn class tự chế `rl-*` | **0** |
| Component chuẩn | có `V2BaseFilterPanel` + `V2BaseDataTable` |
| Cột | STT · Chức vụ · Hệ · Quyền đang có · Người sửa · Ngày sửa · Hành động |
| Lọc *Hệ* = HRM | tự bắn API, 25/25 dòng đều `HRM` (không cần bấm Tìm) |
| Tìm nhanh | gõ xong **chưa** đổi danh sách (25 dòng); bấm *Tìm kiếm* → còn **2 dòng**, cộng dồn đúng với lọc Hệ |
| *Làm mới* | xoá cả 2 ô lọc, danh sách về 25 dòng |
| Cột *Chức vụ* | bấm → điều hướng `/admin/roles/100123` (đúng ma trận) |
| Hành động dòng | 2 nút, tooltip *Phân quyền* / *Lịch sử thay đổi*; bấm Lịch sử mở đúng modal |
| Popup *Quyền đang có* | mở đúng chức vụ, hiện đủ nhóm quyền |
| Phân trang | “Hiển thị 1–10 / 119”; trang 2 bắt đầu STT **26**, dữ liệu khác trang 1 |
| Đổi số dòng/trang | 10 → đúng 10 dòng, ô chọn hiển thị đúng giá trị |
| Console | **0 lỗi** |

⚠️ **Chưa test ca không có quyền**: chốt fail-closed (`hasAPermission('Quản lý phân quyền')` → redirect 404)
được **giữ y nguyên** từ bản cũ, không sửa dòng nào; nhưng cần tài khoản thứ hai mới xác nhận được nên
lượt này chưa chạy. Việc còn treo.

### Checkpoint — 03/09/2026
Vừa hoàn thành: chuyển màn danh sách chức vụ sang chuẩn list-page của phân hệ (1 file FE),
sửa kèm lỗi xuất Excel bỏ sót bộ lọc Hệ; tự bắt & sửa 2 lỗi (badge variant sai, pageSize ngoài danh sách).
Đang làm dở: không. **CHƯA COMMIT.**
Bước tiếp theo: user duyệt; nếu cần sort/lọc mở rộng thì mở thêm ở `RoleService::index`.
Còn treo: chạy ca không có quyền bằng tài khoản thứ hai.
Blocked:


---

## Phase 1c — Màn phân quyền 1 chức vụ theo chuẩn phân hệ (XONG 03/09/2026)

3 file: `pages/admin/roles/_id.vue` · `components/permission-matrix/PermissionMatrix.vue` ·
`utils/permission-matrix.js` (+ gỡ nút chết ở `GrantedPanel.vue`).

### 1. Tiêu đề — đưa lên topbar qua `PageTitleMixin`

Bỏ hẳn khối tiêu đề tự dựng trong trang (`pr-head` / `pr-title` / `pr-role` / `pr-sys` / `pr-note`
+ nút back tự chế). Chuẩn của màn chi tiết là đẩy tiêu đề lên **topbar** qua `PageTitleMixin`
(đối chiếu `pages/assign/contracts/_id/index.vue` — `SidebarMenu.vue` render
`<h5 class="topbar-page-title" v-html>` + icon info từ `pageTitleInfo`):

- `pageTitle` → `Phân quyền: <strong>{tên chức vụ}</strong> (HRM|ERP)`
- `pageTitleInfo` → câu ngữ cảnh công ty (trước là dòng `pr-note` chiếm một hàng riêng trong trang)

### 2. Bộ lọc — `V2BaseFilterPanel`

Ma trận trước dùng khối `pm-filter` tự chế (4 `<select>`/`<input>` Bootstrap + 3 nút). Nay:
tìm nhanh + **3 bộ lọc nâng cao** (`Phân hệ` · `Nhóm chức năng` · `Hành động`) bằng
`V2BaseSelect`, thu gọn được. `<option>` thuần → `{value,label}` nên thêm 3 computed
`typeOptions` / `groupSelectOptions` / `actionOptions`.

**Tách thao tác khỏi điều kiện lọc:** *Mở tất cả* / *Thu gọn* và *Cấp hàng loạt* **không** nhồi vào
bộ lọc — chúng là cách xem / thao tác lên dữ liệu, không phải điều kiện. Đưa xuống thanh `.pm-tools`
riêng giữa bộ lọc và bảng, dùng `V2BaseButton`.

### 3. Nút chuẩn trên sticky footer — `V2Footer`

Nút *Lưu phân quyền* trước nằm trong panel bên phải (`GrantedPanel`), tự disable khi chưa sửa.
Nay dùng `V2Footer` (`:menu="{ submit_form: true }"` + `url-back="/admin/roles"`) — chuẩn dùng chung
của phân hệ, `position: fixed`, chỗ trống đáy do class `has-v2-footer` trên `<body>` chừa.

⚠️ `V2Footer` **không có trạng thái disabled**, nên chốt "chưa sửa thì đừng gửi" phải chuyển vào trong
`save()`: `!dirty` → toast cảnh báo, không bắn request rỗng. Đồng thời gỡ nút Lưu (đã chết vì trang cha
không truyền prop nữa) và 2 prop `saving`/`dirty` khỏi `GrantedPanel`.

### 4. Màu phân hệ — về MỘT tông

Bỏ bảng 12 tông `HUES` + `HUE_BY_TYPE`, thay bằng một hằng `SUBSYSTEM_HUE`
(`bg #eef4f9` · `fg #27405c` · `ac #3f6f9e`). Lý do ghi thẳng trong code: màu ở đây **không mang
thông tin** — người dùng không tra "phân hệ nào màu gì", chỉ cần thấy ranh giới giữa các dải;
12 tông rực rỡ xen kẽ làm bảng ồn và dễ bị đọc thành "màu = mức độ quan trọng".

### Verify Playwright 1440×900 (đo bằng số từ DOM)

| Hạng mục | Kết quả |
| --- | --- |
| Tiêu đề topbar | `Phân quyền: Quyền giám đốc kinh doanh (ERP)` + icon info |
| Class tự chế `pr-*` còn lại | **0** |
| Bộ lọc nâng cao | 3 nhãn *Phân hệ · Nhóm chức năng · Hành động*, 3 select |
| Lọc *Hành động = Duyệt* | hiện đúng 2 nút cấp hàng loạt: *Cấp tất cả “Duyệt” (35 dòng đang hiện)* · *Bỏ cấp “Duyệt”* + vạch phân cách + ghi chú |
| Màu dải phân hệ | **7 dải · 1 màu nền** `rgb(238,244,249)` · **1 màu chữ** · **1 màu viền** |
| Footer | `position: fixed`, cao 50px, 2 nút *Lưu* + *Quay lại* |
| Chỗ trống đáy | `<body>` có `has-v2-footer`, `padding-bottom: 66px` |
| **Cuộn hết xuống** | dòng cuối bảng & panel phải dừng ở 834, footer ở 850 → **hở 16px, KHÔNG bị đè** |
| Bấm *Lưu* khi chưa sửa | toast `warning` “Chưa có thay đổi nào để lưu” — chốt nằm trong `save()` nên **chứng minh footer đã gọi đúng `save()`** |
| Nhận biết thay đổi | tick 1 ô: 84 → 104 quyền; bỏ tick: về đúng 84 |
| *Quay lại* | điều hướng về `/admin/roles` |
| Console | **0 lỗi** (cả 2 màn) |

⚠️ **Chưa chạy POST lưu thật**: `save()` giữ nguyên phần gửi request, tôi chỉ thêm chốt `!dirty` ở đầu.
Không bấm Lưu sau khi tick để **không sửa dữ liệu quyền của chức vụ 100123** trên DB local
(đã tick rồi bỏ tick, xác nhận panel về đúng 84 quyền). Cần chạy thật thì nói.

### Checkpoint — 03/09/2026
Vừa hoàn thành: màn phân quyền 1 chức vụ theo chuẩn — tiêu đề lên topbar, bộ lọc dùng
`V2BaseFilterPanel`, nút chuẩn xuống `V2Footer` sticky, màu phân hệ về một tông.
Đang làm dở: không. **CHƯA COMMIT.**
Bước tiếp theo: user duyệt.
Còn treo: (a) ca không có quyền (cần tài khoản thứ hai) — chung với Phase 1b; (b) chạy POST lưu thật.
Blocked:


---

## Phase 1d — Bố cục: bộ lọc full width, panel chia màn cùng cấp với bảng (XONG 03/09/2026)

Trước đây bộ lọc nằm **lọt trong cột bảng** (`PermissionMatrix` là 1 grid item của `.pr-grid`,
panel là item còn lại) → bộ lọc vừa hẹp vừa lệch cấp với panel bên phải.

Cách làm: đưa panel vào **slot `side`** của `PermissionMatrix`, rồi trong component tách 2 tầng —
bộ lọc ở trên trải trọn chiều ngang, dưới là `.pm-split` (grid 2 cột) chứa
`.pm-col-main` (thanh công cụ + bảng) và `.pm-col-side` (slot panel). Gỡ `.pr-grid` khỏi `_id.vue`.

### ⚠️ Lỗi tự gây ra rồi tự bắt: panel mất `position: sticky`

Ban đầu đặt `.pm-split { align-items: start }` (copy thói quen từ `.pr-grid` cũ). Hậu quả:
cột phải **co lại bằng đúng chiều cao panel**, nên `position: sticky` của `.gp` không còn khoảng
nào để dính — panel trôi khỏi màn cùng với cột. Đo được `panelTop: -469` khi cuộn 700px
(đáng lẽ dính ở 96) và khi cuộn hết thì `panelBottom: 301`, tức panel đã biến mất khỏi vùng nhìn.

Sửa: để `align-items: stretch` (mặc định) → cột phải cao bằng cả hàng (theo cột bảng),
sticky có đủ khoảng. Ghi lý do thẳng trong CSS để không ai "tối ưu" lại thành `start`.

### Verify Playwright 1440×900 (đo bằng số từ DOM)

| Hạng mục | Kết quả |
| --- | --- |
| Bộ lọc | rộng **1195px** / khung chứa **1205px** → trải trọn chiều ngang |
| Hai cột | bảng `left 230 → right 1083`, panel `left 1095 → right 1425`; **cùng `top = 182`**, không chồng nhau |
| Vị trí tương đối | bộ lọc nằm **trên cả hai cột**; thanh công cụ nằm **trong cột bảng** |
| `thead` sticky | cuộn 400/900/1600 → dính ở **60** |
| Panel sticky | cuộn 400 → **96**; cuộn 900 & 1600 → **64**, luôn trong vùng nhìn |
| Cuộn hết xuống | dòng cuối & panel đều dừng **834**, footer **850** → hở 16px, **không bị đè** |
| Console | **0 lỗi**; 3 warning đều là sẵn có (2 deprecation `vue-router` trong `app.js`, 1 preload hot-update của dev server) |

### Checkpoint — 03/09/2026 (bố cục)
Vừa hoàn thành: bộ lọc full width, panel "Quyền đã phân" chia màn cùng cấp với bảng.
Tự gây & tự sửa lỗi mất sticky của panel do `align-items: start`.
Đang làm dở: không. **CHƯA COMMIT.**
Blocked:


### Checkpoint — 06/09/2026 (wrap up)

**Kiểm lại sau khi có session khác đụng vào.** `pages/admin/roles/index.vue` và `_id.vue` được sửa
thêm **05/09 11:15–11:16** bởi session khác (nhiều khả năng là Phase 2 — định danh quyền bằng `code`).
`PermissionMatrix.vue` · `GrantedPanel.vue` · `utils/permission-matrix.js` giữ nguyên từ 03/09.

Chạy lại Playwright hôm nay trên cả 2 màn — **toàn bộ phần chuẩn hoá vẫn còn nguyên và chạy đúng**:

| Màn | Kết quả 06/09 |
| --- | --- |
| `/admin/roles` | `V2BaseFilterPanel` + `V2BaseDataTable` còn · 7 cột đúng · “Hiển thị 1–10 / 119” · **0 class `rl-*`** · console 0 lỗi |
| `/admin/roles/{id}` | tiêu đề topbar “Phân quyền: Quyền giám đốc kinh doanh (ERP)” · bộ lọc **1267/1277px** (full width) · 2 cột cùng cấp · **7 dải phân hệ / 1 màu** · footer 2 nút *Lưu* + *Quay lại* · **0 class `pr-*`/`pm-filter`** · console 0 lỗi |

**Trạng thái:** vẫn **CHƯA COMMIT** (cả `pages/admin/roles/` lẫn `components/permission-matrix/`,
`utils/permission-matrix.js` đều là file mới chưa track). Nhánh `permiss_manager`.

**Còn treo (không đổi):**
1. Ca **không có quyền** — chốt fail-closed giữ nguyên nhưng cần tài khoản thứ hai mới xác nhận được.
2. Chưa chạy **POST lưu thật** (tránh sửa quyền chức vụ 100123 trên DB local).
3. Nếu muốn **sort / lọc mở rộng** (Trạng thái · Người sửa · Ngày sửa) thì phải mở thêm ở
   `RoleService::index` — hiện chỉ nhận `keyword` + `guard`, sắp xếp cứng `roles.id desc`.

Blocked:

---

## Phase 3 — Cấu trúc lại seeder permission + hoàn thiện Chấm công (MỞ 2026-09-09)

> **Cho người/agent thực thi:** dùng `superpowers:subagent-driven-development` hoặc
> `superpowers:executing-plans`. Mỗi step là một checkbox.

**Mục tiêu:** seeder permission thành nguồn sự thật chạy được nhiều lần trên cả DB cài mới lẫn DB
đang chạy; mỗi phân hệ một seeder trong module của nó; module Chấm công hoàn thiện trọn vẹn để
làm khuôn nhân bản cho 11 phân hệ còn lại.

**Kiến trúc:** lớp cơ sở `PermissionSeeder` (abstract) giữ toàn bộ luật an toàn — kiểm tĩnh trước
khi chạm DB, `updateOrInsert` theo `id`, không bao giờ `delete()`, cuối lượt báo quyền có trên DB
mà seeder không khai. Subclass chỉ khai dữ liệu. `PermissionsTableSeeder` đổi vai thành
orchestrator + nơi tạm trú 644 quyền của 11 phân hệ chưa tách.

**Spec:** `docs/superpowers/specs/gop-db/2026-09-09-seeder-permission-cau-truc-design.md`

**Thay thế cho:** mục 2.4 và phần Chấm công còn lại của 2.3 ở Phase 2 phía trên.

### Ràng buộc chung — áp cho MỌI task

- PHP chạy bằng `/opt/homebrew/opt/php@7.4/bin/php` (php mặc định của máy không phải 7.4).
- **DB làm việc là `hrm_erp`** (DB gộp). `.env` đang trỏ `hrm_tpe` — đổi ở Task 1, không task nào
  được chạy trước khi Task 1 xong.
- **Quyền cũ giữ nguyên 100%**: không đổi tên, không gộp, không xoá, không sắp lại id. Ngoại lệ duy
  nhất: bỏ 2 dòng khai trùng tiền tệ (id 1117, 1118) trong seeder — không bỏ thì L2 chặn, seeder
  không chạy nổi.
- **Không đụng quyền `guard = web`** (ERP) ở bất kỳ đâu.
- Không tự commit/push khi user chưa yêu cầu (quy tắc project). Các step "Commit" bên dưới chỉ thực
  hiện khi user đã đồng ý.
- File `hrm-client` phần lớn là CRLF — sửa bằng script phải giữ nguyên line ending, `git diff --stat`
  sau mỗi lần sửa.

---

### Task 1 — Chuẩn bị môi trường, dump an toàn, chốt số nền

**Files:**
- Modify: `hrm-api/.env` (dòng `DB_DATABASE`)
- Create: `.plans/gop-db/thiet-ke-lai-phan-quyen/baseline-2026-09-09.md` (ghi số nền)
- Create: dump SQL trong scratchpad

- [x] **Step 1: Dump 2 bảng trước khi đụng gì**

```bash
mysqldump -h127.0.0.1 -uroot -p'<mật khẩu trong .env>' hrm_erp permissions role_has_permissions \
  > "$SCRATCH/hrm_erp-permissions-$(date +%Y%m%d-%H%M).sql"
ls -lh "$SCRATCH"/hrm_erp-permissions-*.sql
```

Kỳ vọng: file > 100KB. **Không có dump thì không được sang step sau.**

- [x] **Step 2: Đổi `.env` sang DB gộp**

Sửa đúng 1 dòng: `DB_DATABASE=hrm_tpe` → `DB_DATABASE=hrm_erp`. Rồi:

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan config:clear
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo config("database.connections.mysql.database") . " | api=" .
  \DB::table("permissions")->where("guard_name","api")->count() . " web=" .
  \DB::table("permissions")->where("guard_name","web")->count() . PHP_EOL;'
```

Kỳ vọng: `hrm_erp | api=720 web=965`.

- [x] **Step 3: Ghi số nền của audit và test**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan permission:audit | tee /tmp/audit-truoc.txt
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Unit/PermissionAuditTest.php
```

Kỳ vọng: `722 quyền khai` · chốt 1 = **21** · chốt 2 = **2** · chốt 5 = **37** · chốt 3/4/6/7 = 0 ·
phpunit **7/7 OK**. Ghi cả 4 số vào `baseline-2026-09-09.md`.

- [x] **Step 4: Đo số nền trên màn phân quyền bằng Playwright MCP**

Mở `http://127.0.0.1:3000/admin/roles`, chọn một chức vụ **có quyền Chấm công**, vào ma trận rồi
đếm bằng DOM:

```js
document.querySelectorAll('.pm-col-side .gp input:checked, .pm-col-side .gp-item').length
```

Ghi lại: tên chức vụ, id, **số quyền đang có** (số ở panel "Quyền đã phân"), số ô tick của dải phân
hệ Chấm công. Đây là con số Task 13 sẽ so lại sau khi đổi hằng số sang `code`.
⚠️ Phải dùng `127.0.0.1:3000`, KHÔNG dùng `localhost:3000` (token nằm ở origin `127.0.0.1`).

---

### Task 2 — Lớp cơ sở `PermissionSeeder` + 7 luật kiểm tĩnh

**Files:**
- Create: `hrm-api/app/Database/Seeders/PermissionSeeder.php`
- Test: `hrm-api/tests/Feature/PermissionSeederTest.php`

**Interfaces:**
- Produces: `App\Database\Seeders\PermissionSeeder` — abstract, subclass khai
  `protected $type`, `protected $subsystem`, `abstract protected function permissions(): array`
  với hợp đồng `id => [name, group, code, display_name?, sort_order?]`
  (seeder legacy `$type = null` dùng `id => [name, group, code, display_name, sort_order, type]`).
  Hằng số public: `PermissionSeeder::idRangeFor(int $type): array` trả `[đầu, cuối]`.

- [x] **Step 1: Viết test cho 7 luật kiểm tĩnh (chưa có class → phải đỏ)**

```php
<?php
namespace Tests\Feature;

use App\Database\Seeders\PermissionSeeder;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class PermissionSeederTest extends TestCase
{
    use DatabaseTransactions;   // chạy trên DB thật, rollback sau mỗi ca

    /** Seeder giả để thử luật, không đụng dữ liệu thật. */
    private function seeder(array $rows, $type = 1, $subsystem = 'timesheet')
    {
        return new class($rows, $type, $subsystem) extends PermissionSeeder {
            private $rows;
            public function __construct($rows, $type, $subsystem)
            {
                $this->rows = $rows; $this->type = $type; $this->subsystem = $subsystem;
            }
            protected function permissions(): array { return $this->rows; }
        };
    }

    public function test_dai_id_tinh_theo_cong_thuc()
    {
        $this->assertSame([2000, 2099], PermissionSeeder::idRangeFor(1));
        $this->assertSame([2300, 2399], PermissionSeeder::idRangeFor(4));
        $this->assertSame([4400, 4499], PermissionSeeder::idRangeFor(25));
    }

    public function test_L2_trung_name_trong_mang_khai_thi_nem_loi()
    {
        $s = $this->seeder([
            2000 => ['Quyền A', 'Nhóm', 'timesheet.a.view'],
            2001 => ['Quyền A', 'Nhóm', 'timesheet.b.view'],
        ]);
        $this->expectExceptionMessageMatches('/trùng .*name/iu');
        $s->run();
    }

    public function test_L4_code_sai_tien_to_phan_he_thi_nem_loi()
    {
        $s = $this->seeder([2000 => ['Quyền A', 'Nhóm', 'payroll.a.view']]);
        $this->expectExceptionMessageMatches('/tiền tố|prefix/iu');
        $s->run();
    }

    public function test_L5_id_moi_ngoai_dai_thi_nem_loi_va_KHONG_ghi_gi()
    {
        $truoc = DB::table('permissions')->count();
        $s = $this->seeder([2500 => ['Quyền A', 'Nhóm', 'timesheet.a.view']]);
        try { $s->run(); $this->fail('Phải ném lỗi'); } catch (\RuntimeException $e) {}
        $this->assertSame($truoc, DB::table('permissions')->count());
    }

    public function test_L5_id_cu_duoi_1564_duoc_mien_kiem()
    {
        $s = $this->seeder([2 => ['Bảng chấm công tổng hợp', 'Chấm công',
            'timesheet.bang_cham_cong_tong_hop.view']]);
        $s->run();
        $this->assertSame('Bảng chấm công tổng hợp',
            DB::table('permissions')->where('id', 2)->value('name'));
    }

    public function test_L7_seeder_phan_he_ma_dong_khai_mang_type_rieng_thi_nem_loi()
    {
        $s = $this->seeder([2000 => ['Quyền A', 'Nhóm', 'timesheet.a.view', 'Quyền A', 1, 4]]);
        $this->expectExceptionMessageMatches('/type/iu');
        $s->run();
    }
}
```

- [x] **Step 2: Chạy test, xác nhận đỏ đúng lý do**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Feature/PermissionSeederTest.php
```

Kỳ vọng: đỏ với `Class "App\Database\Seeders\PermissionSeeder" not found`.

- [x] **Step 3: Viết `PermissionSeeder`**

```php
<?php

namespace App\Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use RuntimeException;

/**
 * Lớp cơ sở cho MỌI seeder permission.
 *
 * Vì sao có lớp này: seeder cũ mở đầu bằng `delete()` toàn bộ quyền `guard = api` rồi tạo lại.
 * Chạy lại trên môi trường thật là mất dòng gán — đã xảy ra 02/09/2026: 3 quyền khách hàng bị xoá
 * kéo theo 49 dòng gán của 12 chức vụ thành mồ côi. Ở đây KHÔNG có đường nào xoá dữ liệu.
 *
 * Hợp đồng dữ liệu của subclass:
 *   id => [name, group, code, display_name?, sort_order?]
 * Riêng seeder legacy (`$type = null`, nhiều phân hệ trong một file):
 *   id => [name, group, code, display_name, sort_order, type]
 */
abstract class PermissionSeeder extends Seeder
{
    /** Quyền có id ≤ mốc này là quyền CŨ — miễn kiểm dải id. */
    const LEGACY_ID_MAX = 1564;

    /** Dải id quyền mới bắt đầu từ đây. 1565–1999 để trống làm vùng đệm cho nhánh chưa merge. */
    const NEW_ID_BASE = 2000;

    /** permissions.type — phân hệ. null = seeder hỗn hợp (file cũ, chưa tách). */
    protected $type;

    /** Slug phân hệ, dùng kiểm tiền tố code. Khớp PermissionCodeGenerator::SUBSYSTEM_SLUG. */
    protected $subsystem;

    /** @return array id => [name, group, code, display_name?, sort_order?] */
    abstract protected function permissions(): array;

    /** Dải id quyền mới của một phân hệ: 2000 + (type-1)*100, rộng 100. */
    public static function idRangeFor(int $type): array
    {
        $dau = self::NEW_ID_BASE + ($type - 1) * 100;

        return [$dau, $dau + 99];
    }

    public function run()
    {
        $rows = $this->normalize($this->permissions());

        $this->guard($rows);            // ném lỗi TRƯỚC khi chạm DB
        $them = $upd = 0;
        foreach ($rows as $id => $row) {
            $this->upsert($id, $row) ? $them++ : $upd++;
        }
        $this->reportUnmanaged($rows);

        $this->command and $this->command->info(sprintf(
            'permissions: thêm %d · cập nhật %d · tổng khai %d', $them, $upd, count($rows)
        ));
    }

    /** Đưa mảng khai về dạng đầy đủ khoá. */
    private function normalize(array $raw): array
    {
        $out = [];
        foreach ($raw as $id => $r) {
            $out[$id] = [
                'name'         => $r[0],
                'group'        => $r[1],
                'code'         => $r[2],
                'display_name' => isset($r[3]) && $r[3] !== null ? $r[3] : $r[0],
                'sort_order'   => isset($r[4]) ? $r[4] : null,
                'type'         => isset($r[5]) ? $r[5] : null,
            ];
        }

        return $out;
    }

    private function guard(array $rows)
    {
        $names = $codes = [];

        foreach ($rows as $id => $r) {
            // L1 — trùng id: mảng PHP không cho trùng khoá, nhưng khai id 0/âm thì chặn ở đây.
            if (!is_int($id) || $id <= 0) {
                throw new RuntimeException("Seeder khai id không hợp lệ: " . var_export($id, true));
            }
            // L2 — trùng name trong mảng khai
            if (isset($names[$r['name']])) {
                throw new RuntimeException("Seeder khai trùng name [{$r['name']}]: id {$names[$r['name']]} và {$id}");
            }
            $names[$r['name']] = $id;
            // L3 — trùng code trong mảng khai
            if (isset($codes[$r['code']])) {
                throw new RuntimeException("Seeder khai trùng code [{$r['code']}]: id {$codes[$r['code']]} và {$id}");
            }
            $codes[$r['code']] = $id;
            // L4 — code rỗng / sai tiền tố phân hệ
            if (empty($r['code'])) {
                throw new RuntimeException("Quyền id {$id} [{$r['name']}] thiếu code");
            }
            if ($this->subsystem && strpos($r['code'], $this->subsystem . '.') !== 0) {
                throw new RuntimeException("Quyền id {$id} có code [{$r['code']}] sai tiền tố, phải bắt đầu bằng [{$this->subsystem}.]");
            }
            // L5 — id mới ngoài dải phân hệ
            if ($id > self::LEGACY_ID_MAX && $this->type !== null) {
                list($dau, $cuoi) = self::idRangeFor($this->type);
                if ($id < $dau || $id > $cuoi) {
                    throw new RuntimeException("Quyền MỚI id {$id} nằm ngoài dải {$dau}–{$cuoi} của phân hệ type {$this->type}");
                }
            }
            // L7 — seeder một phân hệ mà dòng khai lại mang type riêng
            if ($this->type !== null && $r['type'] !== null) {
                throw new RuntimeException("Quyền id {$id} khai type riêng ({$r['type']}) trong seeder của phân hệ type {$this->type}");
            }
            if ($this->type === null && $r['type'] === null) {
                throw new RuntimeException("Seeder hỗn hợp: quyền id {$id} [{$r['name']}] thiếu type");
            }
        }

        $this->guardAgainstDb($rows);
    }

    /** L6 — name/code trùng với bản ghi KHÁC id đang có trên DB (guard api). */
    private function guardAgainstDb(array $rows)
    {
        $db = DB::table('permissions')->where('guard_name', 'api')
            ->get(['id', 'name', 'code']);

        $byName = $byCode = [];
        foreach ($db as $p) {
            $byName[$p->name] = $p->id;
            if ($p->code !== null) {
                $byCode[$p->code] = $p->id;
            }
        }

        foreach ($rows as $id => $r) {
            if (isset($byName[$r['name']]) && $byName[$r['name']] != $id) {
                throw new RuntimeException("Quyền id {$id} trùng name [{$r['name']}] với quyền id {$byName[$r['name']]} đang có trên DB");
            }
            if (isset($byCode[$r['code']]) && $byCode[$r['code']] != $id) {
                throw new RuntimeException("Quyền id {$id} trùng code [{$r['code']}] với quyền id {$byCode[$r['code']]} đang có trên DB");
            }
        }
    }

    /** @return bool true nếu là bản ghi MỚI được chèn */
    private function upsert($id, array $r): bool
    {
        $moi = !DB::table('permissions')->where('id', $id)->exists();

        $data = [
            'name'         => $r['name'],
            'display_name' => $r['display_name'],
            'code'         => $r['code'],
            'group'        => $r['group'],
            'type'         => $this->type !== null ? $this->type : $r['type'],
            'guard_name'   => 'api',
            'sort_order'   => $r['sort_order'],
            'updated_at'   => now(),
        ];
        if ($moi) {
            $data['created_at'] = now();
        }

        DB::table('permissions')->updateOrInsert(['id' => $id], $data);

        return $moi;
    }

    /**
     * Bước 3 — CHỈ BÁO, không xoá. Quyền biến mất khỏi seeder mà bị xoá tự động là cách 1.100 dòng
     * gán mồ côi ra đời; xoá phải là hành động có chủ đích kèm chuyển gán sang quyền thay thế.
     */
    private function reportUnmanaged(array $rows)
    {
        if ($this->type === null || !$this->command) {
            return;
        }

        $tren_db = DB::table('permissions')
            ->where('guard_name', 'api')->where('type', $this->type)
            ->whereNotIn('id', array_keys($rows))
            ->get(['id', 'name']);

        if ($tren_db->isEmpty()) {
            return;
        }

        $this->command->warn("Quyền type {$this->type} có trên DB mà seeder KHÔNG khai (không bị xoá):");
        foreach ($tren_db as $p) {
            $gan = DB::table('role_has_permissions')->where('permission_id', $p->id)->count();
            $this->command->line("  id {$p->id}  {$p->name}  ({$gan} dòng gán)");
        }
    }
}
```

- [x] **Step 4: Chạy lại test, phải xanh**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Feature/PermissionSeederTest.php
```

Kỳ vọng: **6/6 OK**.

- [x] **Step 5: Commit** (khi user đã cho phép commit)

```bash
git add app/Database/Seeders/PermissionSeeder.php tests/Feature/PermissionSeederTest.php
git commit -m "feat(permission): lop co so PermissionSeeder + 7 luat kiem tinh"
```

---

### Task 3 — Sinh `TimesheetPermissionSeeder` (78 quyền) và chứng minh không lệch

**Files:**
- Create: `hrm-api/Modules/Timesheet/Database/Seeders/TimesheetPermissionSeeder.php`
- Create: `hrm-api/database/seeders/tools/gen_permission_seeder.php` (script sinh, dùng cho cả 11 phân hệ sau)

**Interfaces:**
- Consumes: `PermissionSeeder` từ Task 2
- Produces: `Modules\Timesheet\Database\Seeders\TimesheetPermissionSeeder`

- [x] **Step 1: Viết script sinh seeder từ DB**

`database/seeders/tools/gen_permission_seeder.php` — chạy qua `artisan tinker` hoặc `require`. Nhận
`type`, `subsystem`, `class`, `namespace`; đọc DB rồi in ra nội dung file:

```php
$rows = DB::table('permissions')->where('guard_name', 'api')->where('type', $type)
    ->orderBy('id')->get(['id', 'name', 'display_name', 'group', 'code', 'sort_order']);

foreach ($rows as $r) {
    $args = [var_export($r->name, true), var_export($r->group, true), var_export($r->code, true)];
    // display_name chỉ khai khi KHÁC name; sort_order chỉ khai khi không null
    if ($r->display_name !== $r->name || $r->sort_order !== null) {
        $args[] = var_export($r->display_name, true);
    }
    if ($r->sort_order !== null) {
        $args[] = (string) $r->sort_order;
    }
    echo "            {$r->id} => [" . implode(', ', $args) . "],\n";
}
```

- [x] **Step 2: Sinh file cho type 1 và kiểm số dòng**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
$type=1; $subsystem="timesheet"; require base_path("database/seeders/tools/gen_permission_seeder.php");' \
  | grep -c '=> \['
```

Kỳ vọng: **78**.

- [x] **Step 3: Đối chiếu ngược với 78 dòng trong file cũ — lệch một ký tự là dừng**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
$f = "Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php";
$cu = [];
foreach (file(base_path($f)) as $l) {
    $t = ltrim($l);
    if (strpos($t, "//") === 0) continue;
    if (!preg_match("/Permission::create\(\[(.+)\]\);/u", $t, $m)) continue;
    if (!preg_match("/\x27type\x27\s*=>\s*1\b/u", $m[1])) continue;
    preg_match("/\x27id\x27\s*=>\s*(\d+)/u", $m[1], $a);
    preg_match("/\x27name\x27\s*=>\s*\x27((?:[^\x27\\\\]|\\\\.)*)\x27/u", $m[1], $b);
    preg_match("/\x27group\x27\s*=>\s*\x27((?:[^\x27\\\\]|\\\\.)*)\x27/u", $m[1], $c);
    $cu[(int)$a[1]] = [stripslashes($b[1]), stripslashes($c[1])];
}
$db = \DB::table("permissions")->where("guard_name","api")->where("type",1)->pluck("name","id");
$grp = \DB::table("permissions")->where("guard_name","api")->where("type",1)->pluck("group","id");
echo "file cũ: " . count($cu) . " | DB: " . count($db) . PHP_EOL;
$lech = 0;
foreach ($cu as $id => list($n, $g)) {
    if (!isset($db[$id]) || $db[$id] !== $n || $grp[$id] !== $g) { $lech++; echo "LỆCH id $id\n"; }
}
echo $lech === 0 ? "KHỚP 78/78" : "CÓ $lech DÒNG LỆCH — DỪNG" . PHP_EOL;'
```

Kỳ vọng: `file cũ: 78 | DB: 78` và **`KHỚP 78/78`**. Lệch thì dừng, điều tra, **không sửa mò**.

- [x] **Step 4: Tạo file seeder**

```php
<?php

namespace Modules\Timesheet\Database\Seeders;

use App\Database\Seeders\PermissionSeeder;

/**
 * 78 quyền phân hệ CHẤM CÔNG (`permissions.type = 1`).
 *
 * Khai id => [name, group, code]. Quyền cũ giữ nguyên id lộn xộn (2 → 840) vì
 * `role_has_permissions` trỏ id. Quyền MỚI phải lấy id trong dải 2000–2099.
 *
 * `code` lấy nguyên từ đợt backfill (1.685/1.685, 0 trùng) — KHÔNG sinh lại bằng
 * PermissionCodeGenerator: code đã phát hành là bất biến, sinh lại theo tên mới là phá đúng
 * tính chất đang xây.
 */
class TimesheetPermissionSeeder extends PermissionSeeder
{
    protected $type = 1;
    protected $subsystem = 'timesheet';

    protected function permissions(): array
    {
        return [
            // ← dán 78 dòng sinh ở Step 2
        ];
    }
}
```

- [x] **Step 5: Chạy thử seeder trong transaction, đối chiếu DB không đổi**

⚠️ **BẮT BUỘC nâng `group_concat_max_len` trong CÙNG lệnh tinker.** Mặc định MySQL cắt
`GROUP_CONCAT` ở **1024 byte**, trong khi chuỗi thật của bảng `permissions` (1.685 dòng) dài
**302.131 byte** → checksum "toàn bảng" chỉ thực sự so ~78 dòng đầu và cho kết quả "khớp" GIẢ.
Mỗi lần gọi `tinker` là một kết nối mới, nên đặt `SET SESSION` ở lệnh khác là vô tác dụng.

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
\DB::statement("SET SESSION group_concat_max_len = 1000000");
\DB::beginTransaction();
$truoc = \DB::selectOne("SELECT COUNT(*) c, MD5(GROUP_CONCAT(CONCAT_WS(\"|\",id,name,display_name,code,`group`,type,sort_order) ORDER BY id)) h FROM permissions WHERE guard_name=\"api\" AND type=1");
(new \Modules\Timesheet\Database\Seeders\TimesheetPermissionSeeder)->run();
$sau = \DB::selectOne("SELECT COUNT(*) c, MD5(GROUP_CONCAT(CONCAT_WS(\"|\",id,name,display_name,code,`group`,type,sort_order) ORDER BY id)) h FROM permissions WHERE guard_name=\"api\" AND type=1");
echo "trước: $truoc->c / $truoc->h" . PHP_EOL . "sau  : $sau->c / $sau->h" . PHP_EOL;
echo ($truoc->h === $sau->h ? "KHÔNG ĐỔI — đúng" : "ĐÃ ĐỔI — điều tra") . PHP_EOL;
\DB::rollBack();'
```

Kỳ vọng: 2 checksum **giống hệt nhau** (`updated_at` không nằm trong checksum nên seeder ghi lại
cùng giá trị thì hash không đổi).

- [x] **Step 6: Commit**

```bash
git add Modules/Timesheet/Database/Seeders/TimesheetPermissionSeeder.php database/seeders/tools/
git commit -m "feat(permission): tach 78 quyen Cham cong ra TimesheetPermissionSeeder"
```

---

### Task 4 — `PermissionsTableSeeder` đổi vai: bỏ `delete()`, gỡ 78 dòng, legacy 644 quyền

**Files:**
- Create: `hrm-api/Modules/Timesheet/Database/Seeders/LegacyPermissionSeeder.php` (644 quyền, 11 phân hệ)
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (1.398 → ~30 dòng)

**Interfaces:**
- Consumes: `PermissionSeeder` (Task 2), `TimesheetPermissionSeeder` (Task 3)
- Produces: `PermissionsTableSeeder::GROUP_ORDER` **giữ nguyên** (`PermissionService.php:52` đang đọc)

- [x] **Step 1: Sinh 644 dòng legacy kèm `type` và `code`**

Dùng lại script Task 3, bỏ điều kiện `type = 1`, và **khai thêm type mỗi dòng** (vị trí thứ 6):

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
$rows = \DB::table("permissions")->where("guard_name","api")->where("type","!=",1)
    ->orderBy("id")->get(["id","name","display_name","group","code","sort_order","type"]);
echo "tổng: " . count($rows) . PHP_EOL;'
```

Kỳ vọng: **642** (720 − 78).

✅ **Chênh lệch đã điều tra xong 09/09/2026, không còn ẩn số** (controller chạy trước khi giao task):

```
file cũ khai      : 722
DB guard=api      : 720
CÓ trong file mà DB KHÔNG có : 2  → id 1117 "Quản lý danh mục tiền tệ", id 1118 "Xem danh mục tiền tệ"
CÓ trên DB mà file KHÔNG khai : 0
```

Đúng bằng 2 dòng khai trùng tiền tệ mà migration `2026_09_05_000002` đã gộp về 1115/1116. Không có
quyền nào trên DB bị file bỏ sót → **sinh legacy từ DB là an toàn, không sót quyền đang được gán**.
Con số 644 trong spec là đếm nhầm theo file cũ; số đúng là **642**.

- [x] **Step 2: Chạy lại lệnh đối chiếu để tự xác nhận (kết quả kỳ vọng đã ghi ở Step 1)**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
$f = base_path("Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php");
$cu = [];
foreach (file($f) as $l) {
    $t = ltrim($l);
    if (strpos($t, "//") === 0) continue;
    if (!preg_match("/Permission::create\(\[(.+)\]\);/u", $t, $m)) continue;
    preg_match("/\x27id\x27\s*=>\s*(\d+)/u", $m[1], $a);
    if (isset($a[1])) $cu[(int)$a[1]] = true;
}
$db = \DB::table("permissions")->where("guard_name","api")->pluck("name","id")->all();
echo "file cũ: " . count($cu) . " | DB: " . count($db) . PHP_EOL;
echo "CÓ trong file mà DB KHÔNG có: " . count(array_diff_key($cu, $db)) . PHP_EOL;
print_r(array_keys(array_diff_key($cu, $db)));
echo "CÓ trên DB mà file KHÔNG khai: " . count(array_diff_key($db, $cu)) . PHP_EOL;
print_r(array_slice(array_diff_key($db, $cu), 0, 20, true));'
```

Kỳ vọng: `file cũ: 722 | DB: 720` · `CÓ trong file mà DB KHÔNG có: 2` (đúng 1117 và 1118) ·
`CÓ trên DB mà file KHÔNG khai: 0`. Khác đi nghĩa là DB đã thay đổi từ 09/09 — dừng, điều tra.
(Nếu về sau có quyền **trên DB mà file không khai** thì **vẫn phải khai vào legacy seeder** — chúng
là quyền thật đang được gán, để rơi là lần cài mới tiếp theo mất quyền.)

- [x] **Step 3: Tạo `LegacyPermissionSeeder`**

```php
<?php

namespace Modules\Timesheet\Database\Seeders;

use App\Database\Seeders\PermissionSeeder;

/**
 * Nơi TẠM TRÚ của các quyền thuộc 11 phân hệ chưa tách seeder riêng.
 *
 * Mỗi lần tách thêm một phân hệ (theo khuôn TimesheetPermissionSeeder) thì gỡ các dòng của
 * phân hệ đó khỏi đây. File này chỉ được ngắn đi, không bao giờ dài ra: quyền MỚI phải vào
 * seeder của phân hệ mình.
 *
 * `$type = null` → mỗi dòng tự khai type ở vị trí thứ 6, và base bỏ qua kiểm dải id.
 */
class LegacyPermissionSeeder extends PermissionSeeder
{
    protected $type = null;
    protected $subsystem = null;

    protected function permissions(): array
    {
        return [
            // id => [name, group, code, display_name, sort_order, type]
            // ← dán các dòng sinh ở Step 1
        ];
    }
}
```

- [x] **Step 4: Viết lại `PermissionsTableSeeder` thành orchestrator**

```php
<?php

namespace Modules\Timesheet\Database\Seeders;

use Illuminate\Database\Seeder;

/**
 * Orchestrator quyền `guard = api`.
 *
 * ⚠️ KHÔNG BAO GIỜ ĐƯA `delete()` TRỞ LẠI ĐÂY. Bản cũ mở đầu bằng
 * `DB::table('permissions')->where('guard_name','api')->delete()` — chạy lại trên môi trường thật
 * là xoá quyền kèm toàn bộ dòng gán. Ngày 02/09/2026 đúng câu đó đã làm 49 dòng gán của 12 chức vụ
 * thành mồ côi. Việc thêm/sửa quyền nay do PermissionSeeder lo bằng updateOrInsert theo id.
 */
class PermissionsTableSeeder extends Seeder
{
    /**
     * Thứ tự HIỂN THỊ giữa các NHÓM quyền trên màn Phân quyền.
     * GIỮ NGUYÊN — `Modules\Timesheet\Services\PermissionService::52` đang đọc hằng số này.
     * (chép nguyên khối chú thích cũ về đây)
     */
    public const GROUP_ORDER = [];

    public function run()
    {
        $this->call(TimesheetPermissionSeeder::class);
        $this->call(LegacyPermissionSeeder::class);

        // ⛔ 3 seeder Finance CỐ Ý KHÔNG đăng ký (chốt 09/09/2026, ngược bản kế hoạch đầu).
        // AdditionAccountingRequestPermissionSeeder khai id 1177-1180 — trên DB đó đang là 4 quyền
        // phân hệ Giao việc (type 4), trong đó 1179/1180 mỗi cái có 2 dòng role_has_permissions
        // đang gán thật → gọi vào là âm thầm đổi ý nghĩa quyền của chức vụ đang dùng.
        // 2 seeder còn lại khớp dữ liệu nhưng sẽ CHÈN dòng gán mới, phá bất biến "không đổi dòng gán".
        // Cả 3 không kế thừa PermissionSeeder (kế thừa Seeder trơn + const PERMISSIONS) nên 10 chốt
        // chặn của Phase 3 không bảo vệ chúng. Muốn dùng: cấp lại id theo dải finance 2700-2799 trước.
    }
}
```

- [x] **Step 5: Kiểm 116 dòng comment chết đã biến mất và `delete()` không còn**

```bash
grep -c "Permission::create" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php   # kỳ vọng 0
grep -rn "guard_name', 'api')->delete\|->truncate()" Modules/Timesheet/Database/Seeders/     # kỳ vọng rỗng
grep -c "1117\|1118" Modules/Timesheet/Database/Seeders/LegacyPermissionSeeder.php           # kỳ vọng 0
```

- [x] **Step 6: Commit**

```bash
git add Modules/Timesheet/Database/Seeders/
git commit -m "refactor(permission): bo delete(), tach LegacyPermissionSeeder, PermissionsTableSeeder thanh orchestrator"
```

---

### Task 5 — `PermissionAuditService` quét nhiều nguồn seeder

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Services/PermissionAuditService.php` (`declaredPermissions()`, quanh dòng 50–88)
- Test: `hrm-api/tests/Unit/PermissionAuditTest.php` (chạy lại, mốc không đổi)

**Interfaces:**
- Consumes: `TimesheetPermissionSeeder`, `LegacyPermissionSeeder` (Task 3, 4)
- Produces: `declaredPermissions()` giữ nguyên chữ ký, trả `[['id','name','type','group','line'], …]`

- [x] **Step 1: Chạy audit TRƯỚC khi sửa để thấy nó vỡ như dự đoán**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan permission:audit | head -20
```

Kỳ vọng: `Quyền khai trong seeder: 0` và chốt 1 vọt lên hàng trăm — vì regex `Permission::create`
không còn khớp gì. Đây là bằng chứng mục 8 của spec là thật, không phải lo xa.

- [x] **Step 2: Sửa `declaredPermissions()` đọc thêm subclass qua reflection**

```php
/** Các seeder kế thừa PermissionSeeder — thêm module mới thì thêm một dòng ở đây. */
const SEEDER_CLASSES = [
    \Modules\Timesheet\Database\Seeders\TimesheetPermissionSeeder::class,
    \Modules\Timesheet\Database\Seeders\LegacyPermissionSeeder::class,
];

public function declaredPermissions()
{
    $out = $this->declaredFromLegacyFile();   // giữ nguyên regex cũ, phòng khi còn file kiểu cũ

    foreach (self::SEEDER_CLASSES as $class) {
        if (!class_exists($class)) {
            continue;
        }
        $ref = new \ReflectionClass($class);
        $m = $ref->getMethod('permissions');
        $m->setAccessible(true);
        $seeder = $ref->newInstanceWithoutConstructor();

        $type = $ref->getProperty('type');
        $type->setAccessible(true);
        $typeChung = $type->getValue($seeder);

        foreach ($m->invoke($seeder) as $id => $r) {
            $out[] = [
                'id'    => (int) $id,
                'name'  => $r[0],
                'type'  => $typeChung !== null ? $typeChung : (isset($r[5]) ? $r[5] : null),
                'group' => $r[1],
                'line'  => $ref->getFileName(),
            ];
        }
    }

    return $out;
}
```

- [x] **Step 3: Kiểm chứng — con số phải trở về đúng như trước khi tách**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan permission:audit | tee /tmp/audit-sau.txt
diff <(grep -E "Quyền khai|Chốt [0-9]" /tmp/audit-truoc.txt) \
     <(grep -E "Quyền khai|Chốt [0-9]" /tmp/audit-sau.txt)
```

Kỳ vọng: `Quyền khai trong seeder: **720**` · chốt 1 = **21** · chốt 3/4/6/7 = 0 ·
**chốt 2 từ 2 xuống 0**.

⚠️ Con số **720, KHÔNG phải 722**: file cũ khai 722 dòng trong đó có 2 dòng trùng tiền tệ
(id 1117/1118) đã bị bỏ ở Task 4, đúng bằng số quyền thật trên DB. Hai khác biệt so với
`/tmp/audit-truoc.txt` (722 → 720 và chốt 2: 2 → 0) là những khác biệt DUY NHẤT được phép có.
Số khác đi nghĩa là tách sai.

- [x] **Step 4: Hạ mốc bánh cóc chốt 2 về 0 rồi chạy test**

```bash
# tests/Unit/PermissionAuditTest.php: 'duplicate_names' => 2  →  0
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Unit/PermissionAuditTest.php
```

Kỳ vọng: **7/7 OK**.

- [x] **Step 5: Commit**

```bash
git add Modules/Timesheet/Services/PermissionAuditService.php tests/Unit/PermissionAuditTest.php
git commit -m "fix(permission): audit quet nhieu nguon seeder, ha moc trung ten ve 0"
```

---

### Task 6 — Test seeder trên DB thật: idempotent, không chạm ERP, báo quyền lạ

**Files:**
- Modify: `hrm-api/tests/Feature/PermissionSeederTest.php` (thêm 4 ca)

- [x] **Step 1: Thêm 4 ca test**

```php
private function checksum(): string
{
    // MySQL cắt GROUP_CONCAT ở 1024 byte theo mặc định; chuỗi thật dài 302.131 byte nên không
    // nâng giới hạn là checksum chỉ so được ~78 dòng đầu rồi báo "khớp" GIẢ.
    DB::statement('SET SESSION group_concat_max_len = 1000000');

    $r = DB::selectOne('SELECT MD5(GROUP_CONCAT(CONCAT_WS("|", id, name, display_name, code,
        `group`, type, sort_order, guard_name) ORDER BY id)) h FROM permissions');

    return $r->h;
}

public function test_chay_2_luot_khong_doi_mot_dong_nao()
{
    $this->artisan('db:seed', ['--class' => \Modules\Timesheet\Database\Seeders\PermissionsTableSeeder::class]);
    $sauLuot1 = $this->checksum();
    $ganLuot1 = DB::table('role_has_permissions')->count();

    $this->artisan('db:seed', ['--class' => \Modules\Timesheet\Database\Seeders\PermissionsTableSeeder::class]);

    $this->assertSame($sauLuot1, $this->checksum(), 'Lượt 2 làm đổi bảng permissions');
    $this->assertSame($ganLuot1, DB::table('role_has_permissions')->count(), 'Lượt 2 làm đổi dòng gán');
}

public function test_khong_cham_quyen_ERP_guard_web()
{
    $truoc = DB::table('permissions')->where('guard_name', 'web')->count();
    $this->artisan('db:seed', ['--class' => \Modules\Timesheet\Database\Seeders\PermissionsTableSeeder::class]);
    $this->assertSame($truoc, DB::table('permissions')->where('guard_name', 'web')->count());
    $this->assertSame(965, $truoc, 'Số quyền ERP trên DB gộp đã đổi — kiểm lại môi trường');
}

public function test_sua_tay_display_name_thi_seeder_sua_ve_dung()
{
    DB::table('permissions')->where('id', 2)->update(['display_name' => 'SAI BÉT']);
    $this->artisan('db:seed', ['--class' => \Modules\Timesheet\Database\Seeders\TimesheetPermissionSeeder::class]);
    $this->assertSame('Bảng chấm công tổng hợp',
        DB::table('permissions')->where('id', 2)->value('display_name'));
}

public function test_quyen_la_khong_bi_xoa_va_duoc_bao_ra()
{
    DB::table('permissions')->insert([
        'id' => 2099, 'name' => 'Quyền lạ E2E', 'display_name' => 'Quyền lạ E2E',
        'code' => 'timesheet.quyen_la_e2e.view', 'group' => 'Chấm công',
        'type' => 1, 'guard_name' => 'api',
    ]);

    // ⚠️ Laravel 8 KHÔNG có expectsOutputToContain() (chỉ có từ L9) — đọc output qua Artisan::output()
    \Artisan::call('db:seed', ['--class' => \Modules\Timesheet\Database\Seeders\TimesheetPermissionSeeder::class]);
    $this->assertStringContainsString('2099', \Artisan::output(), 'Quyền lạ không được báo ra');

    $this->assertTrue(DB::table('permissions')->where('id', 2099)->exists(), 'Quyền lạ bị xoá — sai');
}
```

- [x] **Step 2: Chạy, phải xanh**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Feature/PermissionSeederTest.php
```

Kỳ vọng: **10/10 OK**. `DatabaseTransactions` rollback nên DB thật không đổi — kiểm lại bằng
checksum ngoài test để chắc.

- [x] **Step 3: Xác nhận DB thật không đổi sau khi chạy test**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
$r = \DB::selectOne("SELECT COUNT(*) c FROM permissions WHERE guard_name=\"api\"");
echo "api = $r->c (kỳ vọng 720)" . PHP_EOL;
echo "quyền lạ 2099 còn không: " . (\DB::table("permissions")->where("id",2099)->exists() ? "CÒN — phải xoá tay" : "không") . PHP_EOL;'
```

- [x] **Step 4: Commit**

---

### Task 7 — Chạy seeder THẬT trên `hrm_erp` và đối chiếu

**Files:** không sửa file nào — đây là bước vận hành.

- [x] **Step 1: Chụp trạng thái trước**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
foreach (["api","web"] as $g) {
  $r = \DB::selectOne("SELECT COUNT(*) c FROM permissions WHERE guard_name=?", [$g]);
  echo "$g = $r->c" . PHP_EOL;
}
echo "role_has_permissions = " . \DB::table("role_has_permissions")->count() . PHP_EOL;'
```

- [x] **Step 2: Chạy seeder thật**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan db:seed \
  --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"
```

Kỳ vọng: in `thêm 0 · cập nhật 78` cho Chấm công, tương tự cho legacy, **không có dòng lỗi**.
Nếu bảng "quyền có trên DB mà seeder không khai" xuất hiện → ghi lại danh sách vào plan, **không xoá**.

- [x] **Step 3: Đối chiếu sau khi chạy**

Chạy lại lệnh Step 1. Kỳ vọng: `api = 720` · `web = 965` · `role_has_permissions` **y nguyên**.

- [x] **Step 4: Chạy lượt 2 và so checksum**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
\DB::statement("SET SESSION group_concat_max_len = 1000000");
$h1 = \DB::selectOne("SELECT MD5(GROUP_CONCAT(CONCAT_WS(\"|\",id,name,display_name,code,`group`,type,sort_order,guard_name) ORDER BY id)) h FROM permissions")->h;
echo "trước lượt 2: $h1" . PHP_EOL;'
/opt/homebrew/opt/php@7.4/bin/php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
\DB::statement("SET SESSION group_concat_max_len = 1000000");
$h2 = \DB::selectOne("SELECT MD5(GROUP_CONCAT(CONCAT_WS(\"|\",id,name,display_name,code,`group`,type,sort_order,guard_name) ORDER BY id)) h FROM permissions")->h;
echo "sau lượt 2 : $h2" . PHP_EOL;'
```

Kỳ vọng: **2 chuỗi giống hệt nhau**.

---

### Task 8 — Lớp tương thích BE: gate nhận cả `name` lẫn `code`

**Files:**
- Modify: `hrm-api/app/Helper/PermissionHelper.php` (thêm `permissionMatches()`, sửa `isCurrentEmployeeHasPermission` dòng ~20–34)
- Modify: 13 bản sao còn lại (danh sách đầy đủ bên dưới)
- Modify: `hrm-api/app/Http/Middleware/CheckPermission.php:29`
- Modify: `hrm-api/Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php` (`where('name', …)`)
- Test: `hrm-api/tests/Feature/PermissionGateTest.php`

**Interfaces:**
- Produces: `permissionMatches(string $needle, $rows): bool` — hàm global trong `PermissionHelper.php`

**13 bản sao phải sửa** (đã grep, tất cả đều `pluck('name')` + `in_array`):

```
app/CommonServices/PermissionService.php          app/Models/BaseModel.php
app/Http/Controllers/ApiController.php            app/Http/Controllers/Api/Traits/ResponseTrait.php
Modules/Training/Http/Controllers/V1/ApiController.php
Modules/Training/Http/Controllers/V1/SubjectController.php
Modules/Training/Http/Controllers/V1/TrainingRequestController.php
Modules/Training/Services/BaseService.php
Modules/Assign/Services/AssignBusinessService.php Modules/Assign/Services/JobRequestService.php
Modules/Timesheet/Services/TimesheetService.php
Modules/Human/Services/MissionService.php         Modules/Human/Services/DepartmentManpowerService.php
```

⚠️ **KHÔNG gom 14 bản làm một.** Chúng khác ngữ nghĩa thật: `PermissionHelper` và
`CommonServices/PermissionService` join `role_has_permissions` lọc `company_id = current_company_role`;
12 bản còn lại dùng `getAllPermissions()` (mọi công ty, kèm quyền gán trực tiếp). Gom là đổi ngữ
nghĩa phân quyền diện rộng — ngoài phạm vi việc này.

- [x] **Step 1: Viết test cho gate (chưa sửa gì → ca `code` phải đỏ)**

```php
<?php
namespace Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\Timesheet\Entities\Employee;
use Tests\TestCase;

class PermissionGateTest extends TestCase
{
    use DatabaseTransactions;

    /** Nhân viên đang giữ quyền id 2 (Bảng chấm công tổng hợp) qua role nào đó. */
    private function employeeCoQuyen(): Employee
    {
        $roleId = DB::table('role_has_permissions')->where('permission_id', 2)->value('role_id');
        $this->assertNotNull($roleId, 'DB không có ai giữ quyền id 2 — chọn quyền khác');
        $employeeId = DB::table('employee_has_roles')->where('role_id', $roleId)->value('employee_id');
        $this->assertNotNull($employeeId, 'Không có nhân viên nào mang role đó');

        return Employee::find($employeeId);
    }

    public function test_gate_nhan_ca_name_lan_code()
    {
        $employee = $this->employeeCoQuyen();
        $this->actingAs($employee, 'api');

        $this->assertTrue(isCurrentEmployeeHasPermission('Bảng chấm công tổng hợp'), 'gate theo name');
        $this->assertTrue(isCurrentEmployeeHasPermission('timesheet.bang_cham_cong_tong_hop.view'), 'gate theo code');
    }

    public function test_khong_co_quyen_thi_ca_hai_deu_false()
    {
        $employee = $this->employeeCoQuyen();
        $this->actingAs($employee, 'api');

        $this->assertFalse(isCurrentEmployeeHasPermission('Quyền không tồn tại XYZ'));
        $this->assertFalse(isCurrentEmployeeHasPermission('timesheet.khong_ton_tai_xyz.view'));
    }
}
```

- [x] **Step 2: Chạy, xác nhận ca `code` đỏ**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Feature/PermissionGateTest.php
```

Kỳ vọng: ca 1 đỏ ở dòng "gate theo code"; ca 2 xanh.

- [x] **Step 3: Thêm helper `permissionMatches`**

```php
/**
 * So một chuỗi quyền với danh sách quyền của nhân viên — chấp nhận CẢ `name` LẪN `code`.
 *
 * Giai đoạn quá độ: hằng số quyền đang chuyển dần từ tên sang code. Nếu chỉ so `name` thì hằng số
 * mang code sẽ trả false VĨNH VIỄN mà không có lỗi nào báo ra — đúng lớp lỗi đang đi diệt.
 */
if (!function_exists('permissionMatches')) {
    function permissionMatches(string $needle, $rows): bool
    {
        foreach ($rows as $row) {
            $name = is_array($row) ? ($row['name'] ?? null) : ($row->name ?? null);
            $code = is_array($row) ? ($row['code'] ?? null) : ($row->code ?? null);
            if ($name === $needle || ($code !== null && $code === $needle)) {
                return true;
            }
        }

        return false;
    }
}
```

- [x] **Step 4: Sửa `isCurrentEmployeeHasPermission` trong `PermissionHelper.php`**

```php
// TRƯỚC: $permissions = $permissions->distinct()->pluck('name')->toArray();
//        return in_array($permission, $permissions);
$rows = $permissions->distinct()->get(['permissions.name', 'permissions.code']);

return permissionMatches($permission, $rows);
```

- [x] **Step 5: Sửa 13 bản sao còn lại theo cùng khuôn**

Bản dùng `getAllPermissions()`:

```php
// TRƯỚC: $permissions = $employee->getAllPermissions()->pluck('name')->toArray();
//        return in_array($permission, $permissions);
return permissionMatches($permission, $employee->getAllPermissions());
```

Tự kiểm sau khi sửa — phải **rỗng**:

```bash
grep -rn "getAllPermissions()->pluck('name')\|->distinct()->pluck('name')" --include='*.php' app Modules
```

- [x] **Step 6: Sửa middleware `CheckPermission`**

```php
// TRƯỚC: $userPermissions = $employee->getAllPermissions()->pluck('name')->toArray();
//        if (array_intersect($permissionsArray, $userPermissions)) {
$rows = $employee->getAllPermissions();
foreach ($permissionsArray as $p) {
    if (permissionMatches($p, $rows)) {
        return $next($request);
    }
}
```

- [x] **Step 7: Sửa trait `ChecksEmployeePermission` (Finance)**

```php
// TRƯỚC: $permissionIds = DB::table('permissions')->where('name', $permissionName)->pluck('id');
$permissionIds = DB::table('permissions')
    ->where(function ($q) use ($permissionName) {
        $q->where('name', $permissionName)->orWhere('code', $permissionName);
    })->pluck('id');
```

- [x] **Step 8: Chạy lại toàn bộ test BE**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/
```

Kỳ vọng: tất cả xanh, gồm cả `PermissionGateTest` 2/2.

- [x] **Step 9: Commit**

---

### Task 9 — FE nhận `code`, và verify payload thật có `code`

**Files:**
- Modify: `hrm-client/utils/mixins/CheckPermission.js` (`hasAPermission`, `hasMultiplePermission`)
- Modify: `hrm-client/utils/mixins/Permission.js` (`hasPermission`, ~dòng 46)

- [x] **Step 1: Verify payload đăng nhập đã mang `code`**

Đăng nhập trên `http://127.0.0.1:3000` rồi đọc bằng Playwright MCP:

```js
JSON.parse(localStorage.getItem('vuex') || '{}')?.permissions?.[0]
```

Hoặc xem network response của `auth/me`. Kỳ vọng: object có cả `name` và `code`.
Nếu **không có `code`** → BE đang `select` cột hạn chế ở đâu đó, phải sửa trước, ghi lại chỗ sửa.

- [x] **Step 2: Sửa `CheckPermission.js`**

```js
hasAPermission(name) {
    // chấp nhận cả tên quyền lẫn code — hằng số đang chuyển dần sang code
    return this.list_permission_alls.some((p) => p.name === name || p.code === name)
},
hasMultiplePermission(names) {
    return this.list_permission_alls.some((p) => names.includes(p.name) || names.includes(p.code))
},
```

- [x] **Step 3: Sửa `Permission.js`**

```js
hasPermission(name) {
    return this.permissions.some((p) => p.name === name || p.code === name)
},
```

- [x] **Step 4: Kiểm line ending không bị phá**

```bash
cd hrm-client && git diff --stat
```

Kỳ vọng: đúng 2 file, mỗi file vài dòng. Nếu thấy cả file bị đánh dấu đổi → đã phá CRLF, trả lại ngay.

- [x] **Step 5: Commit**

---

### Task 10 — Đổi 78 hằng số `TimesheetPermission` sang `code`

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Entities/TimesheetPermission.php` (78 hằng số, chỉ đổi GIÁ TRỊ)
- Regenerate: `hrm-client/utils/permissions/timesheet.js` (bằng `permission:export-js`)

**Interfaces:**
- Consumes: lớp tương thích của Task 8, 9. **Không được làm task này trước Task 8/9** — hằng số mang
  code mà gate chưa hiểu code là mất quyền hàng loạt, im lặng.

- [x] **Step 1: Sinh bảng tra name → code cho 78 quyền**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
foreach (\DB::table("permissions")->where("guard_name","api")->where("type",1)->orderBy("id")->get(["name","code"]) as $p)
    echo str_pad($p->name, 60) . " => " . $p->code . PHP_EOL;'
```

- [x] **Step 2: Đổi giá trị 78 hằng số, giữ nguyên TÊN hằng số**

```php
// TRƯỚC
const CA_LAM_VIEC_MANAGE = 'Quản lý ca làm việc';
// SAU
const CA_LAM_VIEC_MANAGE = 'timesheet.ca_lam_viec.manage';
```

⚠️ **Không đụng 253 chỗ gọi** (188 BE + 65 FE) — đó là lý do đợt trước gom về hằng số.

- [x] **Step 3: Sinh lại file JS và kiểm chốt 7**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan permission:export-js
/opt/homebrew/opt/php@7.4/bin/php artisan permission:audit | grep "Chốt 7"
```

Kỳ vọng: `✓ Chốt 7 — File hằng số JS lệch với bản PHP: 0`.

- [x] **Step 4: Kiểm chốt 6 — mọi giá trị hằng số phải tồn tại trong seeder**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan permission:audit | grep "Chốt 6"
```

Kỳ vọng: **0**. ⚠️ Chốt 6 hiện so hằng số với **`name`** trong seeder; đổi sang code thì phải mở
rộng nó so **cả `name` lẫn `code`**, nếu không nó sẽ báo 78 lỗi giả. Sửa trong
`PermissionAuditService`, cùng lượt.

- [x] **Step 5: Chạy toàn bộ test BE**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/
```

- [x] **Step 6: Commit**

---

### Task 11 — `permission_scopes.php` khoá theo `code` cho 8 quyền duyệt Chấm công

**Files:**
- Modify: `hrm-api/config/permission_scopes.php`
- Modify: `hrm-api/Modules/Timesheet/Services/PermissionMatrixService.php` (chỗ tra `approve_scope`)

- [x] **Step 1: Liệt kê 8 quyền duyệt Chấm công đang khai theo id**

```bash
grep -n "" config/permission_scopes.php | head -60
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
foreach (array_keys(config("permission_scopes")) as $id) {
  $p = \DB::table("permissions")->where("id",$id)->first(["id","name","code","type"]);
  if ($p && $p->type == 1) echo "$p->id | $p->code | $p->name" . PHP_EOL;
}'
```

- [x] **Step 2: Đổi 8 khoá đó từ id sang code, giữ nguyên 12 khoá id của ERP**

```php
return [
    // HRM — khoá theo code (định danh bất biến)
    'timesheet.don_xin_nghi.approve.duyet' => 'department',
    // ERP — vẫn khoá theo permission id, quyền `web` chưa có code chuẩn hoá
    100041 => 'company',
];
```

- [x] **Step 3: `PermissionMatrixService` tra theo code trước, rồi tới id**

```php
$scope = $scopes[$permission->code] ?? $scopes[$permission->id] ?? null;
```

- [x] **Step 4: Verify trên màn thật**

Mở `/admin/roles/{id}` của chức vụ ở Task 1, kiểm 8 quyền duyệt Chấm công vẫn hiện **đúng nhãn
phạm vi** như trước (không rơi về `Toàn công ty` + viền đứt "chưa khai").

- [x] **Step 5: Commit**

---

### Task 12 — Bánh cóc: thêm chốt 9 và chốt 10

⚠️ **Đổi số 09/09/2026:** Task 5 đã dùng mất **chốt 8** ("seeder được gọi mà audit không đọc").
Task này dùng **chốt 9** và **chốt 10**.

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Services/PermissionAuditService.php` (2 phép soi mới)
- Modify: `hrm-api/app/Console/Commands/AuditPermissions.php` (in 2 chốt mới)
- Modify: `hrm-api/tests/Unit/PermissionAuditTest.php` (2 mốc mới)

- [x] **Step 1: Viết test trước (mốc 0 cho cả hai)**

```php
const BASELINE = [
    // …giữ nguyên các mốc cũ, 'duplicate_names' đã hạ về 0 ở Task 5
    'id_out_of_range' => 0,   // chốt 9 — quyền mới (id > 1564) nằm ngoài dải phân hệ
    'duplicate_names_in_db' => 0,   // chốt 10 — trùng name trong cùng guard trên DB
];

public function test_chot_9_id_moi_phai_nam_trong_dai_phan_he()
{
    $this->assertLessThanOrEqual(self::BASELINE['id_out_of_range'],
        count($this->audit()->idsOutOfRange()));
}

public function test_chot_10_khong_trung_name_trong_cung_guard()
{
    $this->assertLessThanOrEqual(self::BASELINE['duplicate_names_in_db'],
        count($this->audit()->duplicateNamesInDb()));
}
```

- [x] **Step 2: Chạy, xác nhận đỏ vì thiếu method**

- [x] **Step 3: Viết `idsOutOfRange()` và `duplicateNamesInDb()`**

```php
/** Chốt 9 — quyền id > LEGACY_ID_MAX phải nằm trong dải 2000 + (type-1)*100 .. +99 */
public function idsOutOfRange(): array
{
    $out = [];
    foreach ($this->declaredPermissions() as $p) {
        if ($p['id'] === null || $p['id'] <= PermissionSeeder::LEGACY_ID_MAX || $p['type'] === null) {
            continue;
        }
        list($dau, $cuoi) = PermissionSeeder::idRangeFor($p['type']);
        if ($p['id'] < $dau || $p['id'] > $cuoi) {
            $out[] = $p;
        }
    }

    return $out;
}

/** Chốt 10 — trùng (name, guard) TRÊN DB. DB gộp không có unique này nên phải tự canh. */
public function duplicateNamesInDb(): array
{
    return DB::table('permissions')
        ->select('name', 'guard_name', DB::raw('COUNT(*) c'), DB::raw('GROUP_CONCAT(id) ids'))
        ->groupBy('name', 'guard_name')->havingRaw('COUNT(*) > 1')->get()->toArray();
}
```

- [x] **Step 4: In 2 chốt mới (9 và 10) trong `permission:audit`, chạy lại**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan permission:audit | tail -20
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Unit/PermissionAuditTest.php
```

Kỳ vọng: **10/10 OK** (7 cũ + chốt 8 của Task 5 + 2 chốt mới), chốt 9 và 10 đều 0.

- [x] **Step 5: Kiểm bánh cóc THẬT SỰ chặn — tiêm lỗi giả**

Thêm tạm vào `TimesheetPermissionSeeder` một dòng `2500 => ['Quyền thử', 'Chấm công', 'timesheet.thu.view']`
(id thuộc dải type 6, không phải type 1) → chạy test → **phải đỏ chốt 9**. Rồi bỏ dòng đó ra,
chạy lại → xanh. Không làm bước này thì không biết chốt có sống hay không.

- [x] **Step 6: Commit**

---

### Task 13 — Verify bằng Playwright, đo bằng số từ DOM

**Files:** không sửa file — bước kiểm chứng bắt buộc trước khi báo xong.

- [x] **Step 1: So số quyền của chức vụ đã đo ở Task 1**

Mở `/admin/roles/{id}` đúng chức vụ đó, đếm lại **số quyền đang có** và **số ô tick dải Chấm công**.

Kỳ vọng: **bằng đúng số ghi ở Task 1**. Lệch một ô nghĩa là gate hoặc hằng số sai — dừng, điều tra.

- [x] **Step 2: Kiểm màn Chấm công có gate thật**

Vào một màn Chấm công mà tài khoản đang dùng có quyền (vd Bảng chấm công tổng hợp) — phải vào được
như trước. Đọc console: **0 lỗi**.

- [x] **Step 3: Ca KHÔNG có quyền**

Dùng tài khoản thứ hai không có quyền Chấm công (hoặc gỡ tạm quyền của một role trong transaction):
màn phải bị chặn, API trả **403**. Đây là ca fail-closed, không được bỏ.

- [x] **Step 4: Chụp màn hình lưu vào `.plans/gop-db/thiet-ke-lai-phan-quyen/screenshots/`**

- [x] **Step 5: Chạy lại TOÀN BỘ test BE lần cuối**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/
/opt/homebrew/opt/php@7.4/bin/php artisan permission:audit | tail -25
```

Kỳ vọng: tất cả xanh · 722 quyền khai · chốt 1 = 21 (không đổi) · chốt 2 = 0 · chốt 3/4/6/7/8/9/10 = 0 ·
chốt 5 = 37 (không thuộc phạm vi đợt này).

---

### Việc CỐ Ý không làm ở Phase 3

- Không dọn 1.100 dòng gán mồ côi (mục 2.6) — cần quyết định nghiệp vụ về quyền thay thế.
- Không xử lý 21 quyền ma (Assign 8 · Decision 6 · Training 5 · Human 2) — Chấm công không có cái nào.
- Không khai `approve_scope` cho 37 quyền duyệt còn lại — chốt 5 vẫn đỏ ở mốc 37.
- Không tách seeder cho 11 phân hệ còn lại — đó là việc nhân bản sau khi Chấm công chạy ổn.
- Không đổi tên / gộp / xoá bất kỳ quyền cũ nào (user rà theo từng màn ở đợt riêng).

### Checkpoint — 09/09/2026 (Phase 3 hoàn thành 13/13 task)

**Vừa hoàn thành:** toàn bộ Phase 3. **18 commit local, CHƯA PUSH** — `hrm-api` 14 commit
(`38f6167..`), `hrm-client` 4 commit (`b6b4b0763..`), cây sạch cả 2 repo.

| Mốc nghiệm thu | Kết quả |
| --- | --- |
| `permission:audit` | 720 quyền khai · **8/10 chốt sạch** · chốt1=21, chốt5=37 (nợ có sẵn) |
| `phpunit tests/` | **67/67** (159 assertions) |
| Seeder chạy THẬT trên `hrm_erp`, 2 lượt | checksum **không đổi**; `api=720 · web=965 · role_has_permissions=15087` nguyên vẹn |
| `/admin/roles/8` | **176 quyền (16/135/16/9)** — khớp tuyệt đối baseline trước khi đụng gì |
| Ca fail-closed | nhân viên không quyền → `false` cả khi gọi bằng tên lẫn code |

**Kết quả cốt lõi:** seeder permission trước đây **không ai dám chạy** (3 seeder Finance ghi thẳng
trong docblock "KHÔNG chạy file đó") nay chạy nhiều lần vô hại trên DB thật. Chốt 2 hạ **2 → 0**;
thêm 3 chốt mới (8, 9, 10), tất cả đều đã chứng minh "biết đỏ" bằng tiêm lỗi thật.

**4 lỗi trong chính kế hoạch này, do review bắt được:**
1. Phép checksum `MD5(GROUP_CONCAT(...))` bị MySQL cắt ở **1024 byte** trong khi chuỗi thật dài
   **302.131 byte** → mọi phép "khớp" trước đó là GIẢ. Đã vá 4 chỗ, bắt buộc `SET SESSION
   group_concat_max_len` cùng kết nối.
2. Chú thích "mảng PHP không cho trùng khoá" **sai** — PHP nuốt im lặng dòng trùng id. Đã đổi sang
   soi mã nguồn + **fail-closed khi mất khả năng soi**.
3. Test mẫu dùng model không implement `Authenticatable` → `TypeError`.
4. `expectsOutputToContain()` chỉ có từ Laravel 9, project chạy Laravel 8.

**Lỗi NGHIÊM TRỌNG chỉ Playwright mới bắt được (Task 13):** 12 task + hơn 20 lượt review + 67/67
test xanh đều không thấy — mở trình duyệt thì **menu Chấm công trả 404 cho người có đủ 78/78 quyền**.
`components/menu.js` khai `isShow` bằng hằng số (nay là `code`) còn `middleware/checkPermission.js`
chỉ so `.name`. Vòng sửa 1 chữa 11 file; re-review lại tìm thêm `pages/timesheet/dashboard/index.vue`
tự định nghĩa hàm kiểm quyền riêng khiến **4 thẻ thống kê bị ẩn im lặng** → vòng 2 chữa nốt + phòng
ngừa `hub.js` (dùng chung 16 phân hệ).
→ Bài học ghi lại: **"vào được trang" KHÔNG chứng minh gate bên trong còn sống — phải đo nội dung
render ra DOM.**

**Bước tiếp theo:** user review 18 commit rồi quyết định push / merge về `gop_db`.

**Việc PHẢI làm trước khi tách phân hệ tiếp theo:**
1. Sửa **14 dòng Transformer** Training/Assign (`getAllPermissions()->pluck('name')` truyền xuống các
   `canXxx()`) — hiện chưa hỏng vì 0 dòng chạm quyền Chấm công, nhưng sẽ vỡ ngay khi đổi hằng số của
   chính 2 module đó.
2. Ưu tiên cao nhất trong nhóm nợ: **37 quyền duyệt chưa khai `approve_scope`** (chốt 5) — đây là nợ
   DUY NHẤT cấp quyền RỘNG hơn dự kiến (mặc định `company`), ngược nguyên tắc fail-closed.

**Blocked:** không.

### Checkpoint — 10/09/2026 (wrap up sau nghiệm thu với user)

**Vừa hoàn thành:** sửa 2 lỗi user phát hiện khi nghiệm thu màn thật (ô "Quyền khác" mất nhãn +
tự hạ cấp quyền âm thầm), vá ở **cả hai** đường `PermissionMatrix.itemPatch()` và
`ItemListModal.toggle()`. Cập nhật spec/plan/STATUS cho khớp thực tế.

**Trạng thái code:** **23 commit local, CHƯA PUSH** — `hrm-api` **16** (`38f6167..`),
`hrm-client` **7** (`b6b4b0763..80ca37862`), cây sạch cả 2 repo, nhánh `permiss_manager`.

**Mốc nghiệm thu giữ nguyên:** `permission:audit` 720 quyền khai · 8/10 chốt sạch (chốt1=21,
chốt5=37 là nợ có sẵn) · `phpunit tests/` **67/67** · `/admin/roles/8` = **176 quyền (16/135/16/9)** ·
DB `api=720 · web=965 · role_has_permissions=15087` nguyên vẹn · **không có thao tác Lưu nào** được
thực hiện trên dữ liệu quyền trong suốt quá trình kiểm.

**Đang làm dở:** không.

**Bước tiếp theo — chờ user quyết 3 việc:**
1. **Vá lỗ hổng route ca làm việc** (mục ngay trên) — BE không chặn quyền id 8, ai đăng nhập cũng
   thêm/xoá/khoá được ca làm việc qua API.
2. **Dọn dữ liệu thừa**: 12/15 cặp (chức vụ × công ty) đang giữ cả 3 cấp Phân ca; 2 cấp hẹp không có
   tác dụng vì gate dừng ở cấp rộng nhất. Dọn về 1 cấp hay để nguyên?
3. **Push / merge về `gop_db`** — tôi không tự làm.

**Việc PHẢI làm trước khi tách phân hệ tiếp theo (không đổi):** sửa 14 dòng Transformer
Training/Assign; và **37 quyền duyệt chưa khai `approve_scope`** — nợ ưu tiên cao nhất vì là nợ duy
nhất đang cấp quyền RỘNG hơn dự kiến.

### Review tổng thể cuối — SẴN SÀNG BÀN GIAO (09/09/2026)

Review toàn nhánh lần đầu kết luận **CẦN SỬA TRƯỚC KHI BÀN GIAO**, đúng 2 việc và cả hai đều là
**tài liệu/chú thích**, không đụng logic — nhưng là loại nguy hiểm nhất: spec/plan vẫn chỉ dẫn
"đăng ký 3 seeder Finance", còn docblock của chính seeder đó ghi *"id 1177–1180 còn trống"* và
*"chạy lại nhiều lần vẫn an toàn"*, cả hai đều sai. Người sau làm theo tài liệu là ghi đè 4 quyền
đang dùng thật.

Đã sửa: spec thêm **mục 7b**, plan bỏ khối `$this->call()` Finance, docblock 3 seeder viết lại đúng
sự thật, cộng 3 việc nhỏ (`'code' => null`, `reportUnmanaged` cho legacy, FE so chặt + chặn rỗng
đồng bộ chuẩn với BE).

**Xác minh lượt cuối, đo trên dữ liệu thật:**
- FE 15 file: quét **1.118 needle** (mọi `name` + `code` user đang giữ) qua predicate cũ vs mới →
  **mất 0, thêm 0**; payload thật 559 quyền đều là chuỗi, không rỗng → đổi `==` sang `===` không thể
  làm mất khớp. Line ending 15/15 nguyên vẹn.
- `reportUnmanaged` cho legacy: chèn quyền bịa trong transaction → **báo đúng**; ca `type=1` do
  `TimesheetPermissionSeeder` báo → phủ kín. Vùng mù còn lại (`type` lạ / `type NULL`) **đã đo, đã
  ghi thẳng vào docblock**, và có chốt 4 + chốt 8 canh thay.
- `permission:audit` 720 · 21 · 0/0/0 · 37 · 0/0/0/0/0 · `phpunit tests/` **67/67** · `/admin/roles/8`
  = **176 (16/135/16/9)** · dashboard 6 thẻ có dữ liệu · working-shift 10 dòng · console đúng bằng
  nền cũ, **0 lỗi liên quan phân quyền** · `git status` sạch cả 2 repo.

### Nghiệm thu với user — 2 lỗi UX/hành vi phát hiện thêm, ĐÃ SỬA (10/09/2026)

User mở màn thật và hỏi *"các permission Phân ca chưa thấy có ở bản mới"*. Điều tra:

**Không mất quyền** — 78/78 quyền Chấm công đều nằm trong ma trận, 3 quyền Phân ca (id 412 *công ty*,
413 *phòng ban*, 414 *bộ phận*) đủ cả. Nhưng **giao diện giấu mất chúng**:

| Tầng che | Chi tiết |
| --- | --- |
| Gộp | BE gom 3 quyền thành **1 mục "Phân ca" 3 cấp**; FE có quy tắc `>1 mục → nút n/N`, nên *1 mục 3 cấp* rơi vào nhánh **checkbox trơn** |
| Mất nhãn | Checkbox đó **không nhãn, không tooltip**. Cột "Quản lý"/"Xem" còn suy được từ tiêu đề cột, cột **"Quyền khác"** thì không |
| Cấp bị ẩn | Nút chọn phạm vi chỉ hiện **sau khi tick** — chức vụ chưa có quyền thì không thấy gì |

Đo toàn hệ (guard `api`): cột "Quyền khác" có **5 ô** nút `n/N` (đọc được tên) và **23 ô checkbox trơn
không nhãn**, trong đó **1 ô** gói nhiều cấp — chính là Phân ca.

**⚠️ Lỗi thứ hai, nghiêm trọng hơn — tự hạ cấp quyền âm thầm.** `itemPatch()` khi bật một mục có
phạm vi thì **thêm cấp hẹp nhất, xoá các cấp còn lại**. Ngữ nghĩa 3 quyền phân ca là **thang loại
trừ** (gate xét công ty → phòng ban → bộ phận, trúng trước thì dừng), nhưng dữ liệu thật có
**12/15 cặp (chức vụ × công ty) đang giữ CẢ 3 cấp** — gồm Super admin ở 5 công ty, Admin_TPE,
Admin_CN Sài Gòn/Vinh/Hải Phòng, HCNS_CN Sài Gòn. Nên một cú **"Cấp tất cả"** sẽ hạ quyền phân ca
của họ **từ toàn công ty xuống chỉ bộ phận**, và thao tác đó **không mở popup** nên không ai biết.
(Mở màn rồi bấm Lưu mà không đụng gì thì an toàn — có chốt `dirty`.)

**User chốt 2 hướng, đã làm xong** (`hrm-client` `1be777456` + `80ca37862`):
1. Mọi checkbox đơn có **tooltip tên quyền gốc**; mục **nhiều cấp** render thành **nút `n/N`** mở
   popup chọn phạm vi. Đo thật trên role 19: nút `3/3`, tooltip
   *"Phân ca — 3 cấp: Công ty · Phòng ban · Bộ phận"*.
2. **Không tự hạ cấp**: bật lại mục **đã có quyền** thì giữ nguyên cấp đang có; chỉ mục **chưa có
   quyền** mới mặc định cấp hẹp nhất (fail-closed cho cái mới). Áp cho **cả hai** đường:
   `PermissionMatrix.itemPatch()` và `ItemListModal.toggle()` (nút bật-tất-cả trong popup — lỗ hổng
   thứ hai, do chính người sửa tự nêu rồi được xác nhận bằng đọc code).
   Số đo: mục đã có cấp *Công ty* → sau "Chọn cả nhóm" **vẫn là Công ty** (code cũ sẽ hạ xuống Phòng
   ban); mục chưa có quyền → vẫn nhận **cấp hẹp nhất**, fail-closed còn nguyên.
   `pickLevel()` giữ nguyên — người dùng chủ động chọn một bậc thì được phép thu hẹp.

### ⚠️ Lỗ hổng CÓ SẴN phát hiện khi trả lời user (10/09/2026) — CHƯA SỬA, chờ user quyết

User hỏi *"quyền Quản lý phân ca hiện có tác dụng gì?"*. Đính chính: hệ thống **không có quyền tên
"Quản lý phân ca"**; quyền gần nhất là **"Quản lý ca làm việc" (id 8)**, 14 dòng gán / 9 chức vụ.

**Tác dụng thật của id 8 — chỉ ở FRONTEND, 2 màn:**

| Màn | Tác dụng |
| --- | --- |
| `/timesheet/timeworking/working-shift` | Ẩn/hiện nút **Thêm mới**, và **Sửa / Khóa / Mở khóa / Xóa** trong dropdown từng dòng (`isManager`) |
| `/timesheet/timeworking/add-working-shift/{id}` | Không có quyền thì **đá về 404** ngay khi vào |

Phân biệt: id 8 là quyền **định nghĩa ca làm việc** (ca sáng/chiều, giờ vào-ra); nhóm **Phân ca**
(412/413/414) là quyền **xếp nhân viên vào ca** — hai việc khác nhau. Quyền XEM danh sách ca do
id 369/370 lo.

**🔴 Lỗ hổng: BACKEND KHÔNG KIỂM QUYỀN NÀY Ở ĐÂU CẢ.** Grep cả tên lẫn `code` trong toàn bộ
`hrm-api`: **0 chỗ dùng**. Nhóm route tương ứng (`Modules/Timesheet/Routes/api.php:80-89`) chỉ có
`auth:api`, **không có `checkPermission`**:

```php
Route::group(['prefix' => '/timesheet/timeworking', 'middleware' => 'auth:api'], function () {
    Route::post('/',                          [WorkingShiftController::class, 'store']);       // thêm ca
    Route::delete('/{id}',                    [WorkingShiftController::class, 'delete']);      // xoá ca
    Route::put('/{workingShift}/toggle-lock', [WorkingShiftController::class, 'toggleLock']);  // khoá/mở
});
```

→ **Bất kỳ ai đăng nhập được đều có thể gọi thẳng API để thêm / xoá / khoá ca làm việc**, kể cả
không có quyền id 8. Quyền hiện chỉ ẩn nút trên giao diện.

Vi phạm đúng 2 quy định trong `CLAUDE.md`: *"FE chỉ là lớp trải nghiệm — không được coi là đã chặn"*
và *route thao tác dữ liệu (store/update/destroy/toggle) phải gắn `checkPermission`*.

**Đây là lỗ hổng CÓ SẴN, không do Phase 3** — Phase 3 chỉ đổi cách định danh quyền, không đụng route
(`git log` xác nhận). **Cách vá đề xuất:** gắn
`middleware('checkPermission:' . TimesheetPermission::CA_LAM_VIEC_MANAGE)` cho 3 route ghi, giữ
nguyên route đọc. Trước khi vá phải rà 9 chức vụ đang giữ quyền này, vì siết ở BE có thể làm lộ chỗ
đang gọi API mà không có quyền. **Đang chờ user quyết.**

**4 việc để lại, không cái nào chặn merge:** `updated_at` bị bump cả 720 dòng mỗi lượt seed (hành vi
hợp lý của upsert, đã ghi rõ); 14 dòng Transformer Training/Assign; 21 quyền ma (chốt 1, fail-closed);
và **37 quyền duyệt chưa khai `approve_scope`** — nợ **ưu tiên cao nhất** vì là nợ duy nhất đang cấp
quyền RỘNG hơn dự kiến.
