# SDD ledger — plan: .plans/gop-db/quan-ly-phong-hop/plan.md

Workspace: `.plans/gop-db/quan-ly-phong-hop/.sdd/` (HRM/ không phải git repo — hrm-api và hrm-client
là 2 repo riêng, nên ledger đặt cạnh plan thay vì `<repo>/.superpowers/sdd/`).

## Pre-flight scan (17/09/2026)

| # | Task ↔ Task | Producer → Consumer | Kết quả |
|---|---|---|---|
| 1 | T1 ↔ T5, T6 | `Modules/Meeting/Routes/api.php` khung prefix `v1` → 2 nhóm route | CLEAN — module routes đã nạp dưới prefix `api` (`Modules/Assign/Providers/RouteServiceProvider.php:64`) ⇒ URL cuối `/api/v1/meeting/...`, khớp e2e spec |
| 2 | T2 ↔ T3 | tên bảng migration → `$table` của entity | CLEAN |
| 3 | T2 ↔ T3 | `meeting_room_bookings` → `MeetingRoom::isCanDelete()`, `upcomingBookingCount()` | CLEAN — bảng tạo ngay phase 1 đúng như plan ghi |
| 4 | T3 ↔ T6, T7, T8 | `STATUS_ACTIVE=1 / STATUS_INACTIVE=2` → Resource, badge FE | CLEAN |
| 5 | T4 ↔ T5, T6, T7, T8, T9 | 4 chuỗi tên quyền → middleware, cờ FE, `isShow` menu | CLEAN — đối chiếu từng chữ, khớp cả 5 nơi |
| 6 | T5, T6 ↔ e2e utils | code mẫu dùng `api` / `noPermApi` | **CONFLICT** → Ruling R1 |
| 7 | T10 | assertion `.v2-footer` trên màn danh mục | **CONFLICT** → Ruling R2 |
| 8 | T6 ↔ T8 | cờ `is_can_delete` trong Resource → ẩn nút Xóa | CLEAN (đã bổ sung bước 6b khi self-review plan) |
| 9 | T9 ↔ T7, T8 | link menu `/meeting/room-amenities`, `/meeting/rooms` → đường dẫn page | CLEAN |
| 10 | T2 (tự nhất quán) | `meetings.meeting_room_id` thêm ở phase 1 nhưng tới phase 4 mới dùng | CLEAN — cố ý, tránh migration lặt vặt |

## Rulings

- **R1 — e2e không có helper `api`/`noPermApi` dùng chung.** `e2e/utils/` chỉ có fixture theo nghiệp vụ.
  Quyết định: mỗi spec tự dựng `APIRequestContext` theo khuôn `tests/assign/customer-demand-link.api.spec.ts`
  (đọc `.auth/api.json`); ca "không quyền" dùng `test.use({ storageState: '.auth/user-nocost.json' })`
  (tài khoản nocost đã có sẵn, sinh bởi `auth/login-nocost.setup.ts`). Nếu `api-setup` đỏ trên DB gộp
  (bẫy đã biết: thiếu bảng `hrm_employees`) thì chạy spec lẻ bằng `--no-deps`.
  *Sai thì tốn*: viết lại phần khởi tạo context của 3 spec (~15 phút).
- **R2 — `.v2-footer` không tồn tại trên màn danh mục** (V2Footer chỉ dùng ở màn chi tiết/form; màn danh mục
  lý do hủy cuộc họp không có). Phép đo trong plan sẽ nổ vì `boundingBox()` trả null.
  Quyết định: thay bằng 2 phép đo có thật — (a) footer của `V2BaseModal` vẫn nằm trong viewport khi body
  modal cuộn; (b) `document.body.scrollWidth <= clientWidth` (bảng không đẩy trang tràn ngang).
  *Sai thì tốn*: thiếu 1 phép đo khuôn giao diện, lộ ở phase sau.
- **R3 — KHÔNG commit git** (CLAUDE.md dự án cấm commit/push; user instruction thắng skill).
  Ledger ghi theo file thay đổi thay vì commit hash; review package dựng bằng `git diff -- <paths>`
  cộng nội dung file mới. *Sai thì tốn*: không có điểm rollback theo task, phải dựa `git diff` thủ công.
- **R4 — làm thẳng trên nhánh `gop_db` ở cả 2 repo, KHÔNG tạo worktree.** CLAUDE.md bắt buộc `gop_db`;
  worktree `hrm-api` làm hỏng autoload vendor (ghi chú đã có của dự án).
  *Sai thì tốn*: thay đổi nằm lẫn trong checkout chung, phải lọc khi merge.

## Tiến độ

**Baseline 17/09/2026**: `hrm-api` @ 6aea12365 (sạch) · `hrm-client` @ b85478388 — ⚠️ đang có 4 file sửa dở
KHÔNG phải của plan này (`components/V2BaseSmartFilterPanel.vue`, `components/print/ReportPrintPreviewModal.vue`,
`pages/assign/report/potential-customer-care/**`) → nhiều session chạy song song, TUYỆT ĐỐI không stash,
không revert, không đụng 4 file đó. `e2e/` không nằm trong git repo nào → file spec mới không có diff, review
đọc thẳng nội dung file.

**Môi trường 17/09/2026**: API đã chạy sẵn ở `127.0.0.1:8000` (php, PID 17717), Nuxt dev ở
`127.0.0.1:3000` (node, PID 16338) — **của session khác, KHÔNG tự tắt/khởi động lại, không `pkill`**.
DB `hrm_erp` chưa có bảng `meeting_room%` nào (0 bảng) trước Task 2.
Đã vá plan + brief 5/6/10 theo Ruling R1 (cách dựng APIRequestContext + tài khoản nocost) và R2 (2 phép đo
thay cho `.v2-footer`).

- **R5 — THAY THẾ R4: làm trong WORKTREE** (user yêu cầu 17/09/2026: nhánh `gop_db` đang dùng ở phiên khác).
  `hrm-worktrees/phong-hop-api` + `hrm-worktrees/phong-hop-client`, nhánh `feat/quan-ly-phong-hop` (cắt từ `gop_db`).
  Bẫy vendor đã né đúng cách: **copy `vendor/` thật + `composer dump-autoload` chạy TRONG worktree**
  (KHÔNG symlink) → `autoload_psr4.php` dùng `$baseDir` suy từ `__DIR__`, trỏ về `Modules/` của worktree.
  `node_modules` copy thật (752M). Server riêng: API `:8001`, Nuxt `:3001`; server `:8000`/`:3000` của phiên
  khác không đụng tới. DB **dùng chung** `hrm_erp` (không tách được) → migration Task 2 ảnh hưởng cả 2 phiên,
  nhưng chỉ thêm bảng `meeting_room*` mới nên không va vào việc đang làm ở nhánh kia.
  *Sai thì tốn*: phải merge `feat/quan-ly-phong-hop` về `gop_db` thay vì có sẵn trên nhánh.

Task 1: DONE_WITH_CONCERNS (module `Modules/Meeting` + `modules_statuses.json`), đã **di dời khỏi checkout
chính sang worktree**; checkout chính trả về sạch (`git status` rỗng). `module:list` trong worktree báo
`Meeting | Enabled | …/phong-hop-api/Modules/Meeting`.
  Concern của implementer: `artisan route:list` crash `Trying to get property 'employee_info_id' of non-object`
  (`app/Helper/PermissionHelper.php:23`) — đã xác nhận là **bug sẵn có của repo**, `route:list --path=assign`
  cũng crash y hệt, KHÔNG liên quan module mới. Ruling: không sửa (ngoài scope Phase 1); các task sau kiểm
  route bằng **gọi HTTP thật** thay vì `route:list`.

**e2e cho worktree**: đã sinh `.auth/user-wt.json` + `.auth/user-nocost-wt.json` (copy của bản gốc, đổi
origin `:3000` → `:3001`) vì storageState của Playwright gắn theo origin — dùng nhầm `user.json` trên cổng
3001 sẽ bị đẩy về `/login`. File gốc giữ nguyên cho phiên khác. Server worktree đã sống: API `:8001` trả 401
(có auth = server chạy), Nuxt `:3001` đang build lần đầu.

Task 1: review — Spec ✅ / Chất lượng Approved, 1 Important + 2 Minor.
  Important: `module:make` để lại scaffold demo `Routes/web.php` (route `GET /meeting`, KHÔNG auth) +
  `Http/Controllers/MeetingController.php` trả `view('meeting::index')` trong khi `Resources/views` đã xóa
  → route vỡ nếu bị chạm. Đã vào **fix round 1/5** (resume implementer): xóa controller demo, để `web.php`
  rỗng route (không xóa hẳn vì `RouteServiceProvider::mapWebRoutes()` còn trỏ tới file).
  Minor (ghi nhận, không sửa): `Services/`, `Transformers/` chưa tồn tại (stub không sinh — task sau tự tạo);
  `modules_statuses.json` mất newline cuối do chính tool ghi.

- **R6 — e2e của dự án HỎNG SẴN trên DB gộp, không phải do worktree.** Bằng chứng: `api-setup` chết với
  `Table 'hrm_erp.hrm_employees' doesn't exist` (đúng bẫy đã biết); tài khoản fixture `e2e_assign@test.local`
  KHÔNG tồn tại trong bảng `employees` (0 bản ghi `%e2e%`, tổng 1095 nhân viên); token trong
  `.auth/api.json` và `.auth/user.json` đều trả **401 ở CẢ `:8000` lẫn `:8001`** (token chưa hết hạn —
  exp 02/10/2026 — nhưng đã bị vô hiệu) ⇒ không phải lỗi origin, không phải lỗi worktree.
  Quyết định: **KHÔNG sửa `e2e/auth/api.setup.ts` và `database/e2e_provision.php`** (tài sản dùng chung,
  CLAUDE.md bắt sửa qua PR). Thay vào đó thêm **Task 4b** vào plan: dựng đường đăng nhập riêng cho worktree
  (mint JWT bằng tinker cho 1 tài khoản có quyền + 1 tài khoản không quyền, ghi ra `.auth/api-wt.json`,
  `.auth/user-wt.json`, `.auth/user-nocost-wt.json`), chạy spec bằng `--no-deps`.
  Task 4b đặt SAU Task 4 vì phải có 5 quyền mới thì tài khoản "có quyền" mới cấp được.
  *Sai thì tốn*: nếu cách mint token không khớp guard `auth:api`, phải quay lại dùng luồng login thật và
  tạo tài khoản e2e trong DB (thêm ~1 task).
  Ghi chú phụ: `model_has_roles` KHÔNG tồn tại trên DB gộp — phân vai dùng quan hệ `Employee::roles` +
  `role_has_permissions.company_id = employees.current_company_role` (xem `app/Helper/PermissionHelper.php:19-34`).

Task 1: fix round 1/5 (1 addressed, 0 open — dọn scaffold demo: xóa `MeetingController.php`, `Routes/web.php`
  còn rỗng route; `RouteServiceProvider::mapWebRoutes()` require thẳng file nên KHÔNG xóa được file).
Task 1: complete (không commit theo R3; file: `Modules/Meeting/**` + `modules_statuses.json` trong worktree;
  re-review sạch — `module:list` Enabled, `GET :8001/meeting` → 404).

Task 2: DONE_WITH_CONCERNS (8 migration, batch 396). Concern: implementer bị chặn quyền khi chạy
  `migrate:rollback` → **người điều phối tự chạy bước kiểm chứng** (không phải sửa code):
  `migrate:rollback --path=Modules/Meeting/Database/Migrations --step=8` → sau rollback còn **0** bảng
  `meeting_room*`, **0** cột `meetings.meeting_room_id`, **0** cột `general_regulations.meeting_room_*`;
  `migrate` lại → đủ **6** bảng + 1 + 5 cột, index `mrb_room_time_index` có mặt. ⇒ `down()` chạy thật, đúng.
  Batch cao nhất đã kiểm trước khi rollback: đúng và chỉ 8 migration của plan này (an toàn cho DB dùng chung).
Nuxt worktree `:3001` đã build xong, trả 200 ở `/login`.

Task 2: review — Spec ✅ (đối chiếu từng cột với spec 4.1-4.7) / Chất lượng Approved; 1 Important
  (thiếu index `meeting_room_booking_recurrences.meeting_room_id`) + 1 Minor (comment không dấu).
  2 mục ⚠️ "không kiểm chứng được" của reviewer (schema thật của 3 bảng còn lại) → **người điều phối tự
  kiểm bằng `SHOW CREATE TABLE`**: cả 3 bảng khớp spec, xác nhận đúng là thiếu index thật.
Task 2: fix round 1/5 (2 addressed, 0 open — thêm `index('meeting_room_id')`, sửa comment có dấu).
  Người điều phối chạy rollback 3 + migrate lại → index
  `meeting_room_booking_recurrences_meeting_room_id_index` đã có mặt trong DB.
Task 2: complete (8 migration + index, không commit theo R3).
Task 3: DONE — 2 entity + `tests/Unit/MeetingRoomConfigTest.php`, test đỏ trước rồi xanh: OK (2 tests,
  7 assertions). Đang chờ review.

- **R7 — KHÔNG chạy `PermissionsTableSeeder` toàn phần trên DB dùng chung.** Đo thật trước khi quyết:
  seeder khai 856 quyền, DB đang có 740 quyền `guard=api`, và **472 quyền trong DB KHÔNG được seeder khai**
  → chạy seeder sẽ XÓA 472 dòng đó (seeder `delete()` mọi permission `guard_name='api'` rồi tạo lại).
  Giảm nhẹ: đã đếm được **0 grant** nào trong `role_has_permissions` trỏ vào 472 quyền đó (quyền mồ côi),
  nhưng vẫn là thay đổi diện rộng trên DB người khác đang dùng.
  Quyết định: Task 4 **vẫn sửa file seeder** (nguồn chân lý cho lúc deploy), nhưng **KHÔNG chạy seeder**;
  thay vào đó INSERT thẳng 5 quyền mới (id 1574-1578) + cấp cho role `Super admin` (id 18) với
  `company_id = 1`, idempotent. Không đụng 740 quyền cũ.
  *Sai thì tốn*: DB local lệch nhẹ so với một lần seed sạch (thiếu 116 quyền mới của nhánh khác chưa seed) —
  không ảnh hưởng phần phòng họp.

Task 3: review — Spec ✅ / Approved. Important (N+1 khi gọi `isCanDelete()`/`upcomingBookingCount()` trong
  vòng lặp danh sách) **không phải lỗi Task 3** (brief chỉ yêu cầu logic từng bản ghi) → Ruling: không mở fix
  round, chuyển thành **ràng buộc bắt buộc trong brief Task 5 và Task 6** (tính theo lô bằng 1 query
  `groupBy`, kèm `with('amenities')`). Minor về type-hint: mâu thuẫn có sẵn trong brief, bỏ qua.
  Mục ⚠️ của reviewer (không đối chiếu được cột bảng pivot) → đã có bằng chứng từ gói Task 2:
  `meeting_room_room_amenity` có đúng `meeting_room_id`, `meeting_room_amenity_id`, `quantity`, `note`
  + unique `mr_amenity_unique` ⇒ quan hệ `belongsToMany` khai đúng cột.
Task 3: complete (2 entity + unit test xanh, review sạch, không commit theo R3).

Task 4: DONE — 5 quyền id 1574-1578 vào seeder (nguồn chân lý) + INSERT idempotent vào DB + cấp cho role
  `Super admin` (18) với `company_id=1`. Kiểm chứng: `COUNT(*) permissions WHERE guard_name='api'` = **745**
  (740 cũ + 5 mới ⇒ không mất dữ liệu phiên khác); chạy lại SQL lần 2 vẫn 745 (idempotent thật).
  Đang chờ review.
Task 4b: đang chạy (dựng token e2e cho worktree).

Task 4: complete (review sạch — Spec ✅, Approved, không issue; tên quyền khớp từng ký tự kể cả dấu,
  diff chỉ có dòng thêm).

Task 4b: complete. Tài khoản test: **id 34** `thuydt.qttt@tanphat.com` (role 18 Super admin,
  `current_company_role=1`, 578 quyền — có `Quản lý danh mục phòng họp`) và **id 25**
  `cannt.kd1@tanphat.com` (10 quyền, không có quyền phòng họp).
  Phát hiện hạ tầng: bảng nối role thật tên là **`employee_has_roles`** (KHÔNG phải `model_has_roles`),
  Spatie cấu hình `teams => false` nên `getAllPermissions()` không lọc `company_id`.
  File sinh ra: `.auth/api-wt.json`, `.auth/user-wt.json`, `.auth/user-nocost-wt.json`,
  `e2e/tests/meeting/_auth-smoke.spec.ts` (spec smoke giữ lại), `.sdd/mint-auth.php`.
  **Người điều phối tự kiểm chứng lại**: admin token → 200 ở route có gate (`assign/reason_project_failures`),
  nocost token → **403** ở đúng route đó, route không gate → 200; 3 file auth gốc của phiên khác giữ nguyên
  mtime 14/09 (không bị ghi đè). UI smoke pass kèm đối chứng âm (storageState rỗng → bị đẩy `/login`).
  **Ruling: KHÔNG dispatch reviewer riêng cho 4b** — task hạ tầng, không có code chạy production, bằng chứng
  đã được người điều phối kiểm trực tiếp. *Sai thì tốn*: nếu file auth sai khuôn, Task 5-10 sẽ đỏ ngay ca đầu
  và lộ ra lập tức.
  ⚠️ Lưu ý cho task sau: route `assign/meeting_cancel_reasons` KHÔNG dùng để test quyền được (gate của nó
  chưa cấp cho role nào); không có endpoint HTTP liệt kê quyền user.

Task 5: DONE — 5 file BE + route group + `e2e/tests/meeting/room-amenity.api.spec.ts`; TDD đúng thứ tự
  (đỏ: 1 failed + 3 "did not run" vì chưa có route → xanh: **4 passed (5.4s)**). Chống N+1 bằng gom
  `groupBy` (nhưng đặt ở biến STATIC trên Resource — đã yêu cầu reviewer soi kỹ điểm này).
  Concern implementer: chưa có ca "xóa bị chặn vì tiện nghi đang gắn phòng" (cần dữ liệu phòng của Task 6).
  Đang chờ review. Task 6 chạy song song.

Task 5: review — Spec ✅ nhưng **CHƯA Approved**, 4 Important:
  (1) biến static `$usedCounts` trên Resource không có `try/finally` → state rò sang request sau;
  (2) ca test "trùng mã → 422" assert `toContain('code')` **rỗng nghĩa** — mọi response của dự án đều có key
      `"code": <httpStatus>` nên luôn pass kể cả khi validate hỏng;
  (3) mã test cố định `E2E_PROJ`… → lần chạy trước bị kill là lần sau đỏ giả;
  (4) N+1 còn sót: accessor `employee_create_name`/`employee_update_name` của `BaseModel` tự load quan hệ
      từng dòng (tới 4 query/dòng), thiếu `with('employee_create.info','employee_update.info')`.
  **Ruling**: finding (4) mâu thuẫn với chỉ thị "copy đúng khuôn `MeetingCancelReasonService`" (khuôn gốc cũng
  dính lỗi này) → **quy tắc "cấm N+1" của CLAUDE.md thắng**; sửa ở màn mới, KHÔNG sửa màn cũ (ngoài scope).
  *Sai thì tốn*: 2 màn danh mục lệch nhau một chút về cách eager load — chấp nhận được.
  Đã vào fix round 1/5.

Task 6: DONE — 5 file BE + route `meeting/rooms` + `e2e/tests/meeting/meeting-room.api.spec.ts`.
  TDD: đỏ `1 failed ... 4 did not run` → xanh **5 passed (8.5s)**, chạy lại lần 2 **5 passed (11.5s)**,
  chạy chung với bộ Task 5 → **9 passed (12.7s)**. Đã tránh được lỗi static của Task 5 (gán
  `used_booking_count` vào từng model); đo N+1 bằng `DB::enableQueryLog()`: `with('amenities')` = 1 query gộp
  cho 5 phòng, đếm booking = 1 query gộp. Tự nhận còn dính N+1 `employee_create_name`/`employee_update_name`
  (giống finding (4) của Task 5) → sẽ gộp vào fix round sau review. Đang chờ review.

Task 5: fix round 1/5 — implementer báo 4/4 addressed: bỏ static (gán `used_count` vào model, Resource có
  fallback cho bản ghi lẻ); spec parse JSON assert `body.errors.code` thay cho `toContain('code')`; mã test có
  hậu tố `Date.now()` + `beforeAll` dọn rác `E2E_%`; thêm `with(['employee_create.info','employee_update.info'])`.
  Đo thật: khuôn cũ **50 query** cho 6 bản ghi → sau fix **9 query**, phẳng theo số dòng. Chạy spec 2 lần:
  4 passed / 4 passed. Đang chờ re-review xác nhận.

Task 5: complete (re-review: 4/4 ADDRESSED, không hỏng mới, re-reviewer tự chạy lại **4 passed (5.8s)**,
  không ca nào "did not run"). Ghi chú nhỏ: re-reviewer nhẩm ra 7 query thay vì 9 như implementer báo —
  chênh lệch không đổi kết luận (số query cố định theo lô, không tăng theo số dòng).

Task 6: review — Spec ✅ nhưng **KHÔNG Approved**: 2 Critical + 2 Important.
  **Critical 1 (bảo mật thật)**: route `GET /meeting/rooms/{id}` KHÔNG gắn `checkPermission` (chỉ `auth:api`),
  mà `DetailMeetingRoomResource` trả thẳng `checkin_qr_token` → **mọi nhân viên đăng nhập lấy được credential
  dùng để check-in hộ bằng QR ở Phase 5**. Fix 2 lớp: gate route + chỉ trả token cho người có quyền
  `Quản lý danh mục phòng họp`, kèm ca e2e nocost → 403.
  **Critical 2**: lặp lại assertion rỗng nghĩa `toContain('code')` (đúng lỗi Task 5 vừa sửa).
  Important: (3) N+1 `employee_create_name`/`employee_update_name` — thiếu `with()`; (4) mã test cố định.
  Minor ghi nhận, KHÔNG sửa (deferred): `destroy()` không `lockForUpdate` (race hiếm, hệ quả nhẹ);
  `unlock()` không kiểm điều kiện đối xứng với `lock()`.
  Đã vào fix round 1/5.
Task 7 (FE màn tiện nghi): đang chạy.

Task 6: fix round 1/5 — implementer báo 4/4 addressed. Gate route `show` + `when(isCurrentEmployeeHasPermission(
  'Quản lý danh mục phòng họp'))` cho `checkin_qr_token`; spec parse JSON assert `body.errors.code`;
  `with(['amenities','employee_create.info','employee_update.info'])` → đo **40 → 10 query** cho 5 dòng;
  mã test có hậu tố + `beforeAll` dọn theo đúng thứ tự FK. Test: 6 passed ×2 lần, cả thư mục `tests/meeting`
  **10 passed**, không ca nào "did not run".
  **Người điều phối tự kiểm chứng lỗ bảo mật đã bịt**: tạo phòng thật qua API → nocost `GET /meeting/rooms/{id}`
  trả **403**, admin trả **200 kèm `checkin_qr_token`**, dọn phòng thử xong (200).
  Đang chờ re-review.

Task 6: complete (re-review 4/4 ADDRESSED; `MeetingRoomResource` của DANH SÁCH cũng đã kiểm là không lộ
  `checkin_qr_token`; re-reviewer tự chạy `tests/meeting` → **10 passed (13.1s)**).
  ⚠️ Khoảng hở coverage reviewer nêu: ca e2e nocost bị chặn ngay ở lớp ROUTE nên **lớp Resource
  (`when(isCurrentEmployeeHasPermission(...))`) chưa có ca nào chạm tới**. Ruling: **thêm ca bắt buộc vào
  Task 10** — cấp tạm quyền 1575 (`Xem danh mục phòng họp`) cho role của nhân viên id 25, kiểm `GET` trả 200
  nhưng body KHÔNG có `checkin_qr_token`, rồi thu hồi quyền. *Sai thì tốn*: nếu quên thu hồi, tài khoản test
  giữ thừa 1 quyền trên DB chung — đã yêu cầu kiểm lại bằng truy vấn sau khi chạy.

Task 7: DONE — `pages/meeting/room-amenities/index.vue` + `components/RoomAmenityModal.vue`; smoke UI trên
  trình duyệt thật **1 passed (18.4s)**, đo DOM từng bước (0 dòng → 1 dòng → badge "Hoạt động"→"Khóa"→
  "Hoạt động" → xóa về placeholder), dọn sạch dữ liệu.
  **2 phát hiện quan trọng của Task 7:**
  (a) `$store.state.permissions` là **mảng OBJECT** `{id, name, ...}` — `perms.includes('<tên quyền>')` luôn
      false ⇒ cờ quyền fail-closed vĩnh viễn mà console không báo gì. Phải dùng `.some(p => p.name === ...)`.
      Brief gốc của tôi viết sai chỗ này → đã sửa brief Task 8.
  (b) `V2BaseModal` thiếu method `hide()` mà `unsavedModalMixin` gọi → bấm "Thoát" modal đứng im, không lỗi.
      Đã tái hiện bằng Playwright trước khi sửa.
  **USER DUYỆT giữ thay đổi component dùng chung** `components/modal/V2BaseModal.vue` (+4 dòng, alias
  `hide() { this.close() }`, không đụng `show()`/`close()`). Đã ghi vào `plan.md` (mục riêng + việc cần nêu khi
  merge), `design.md` (Quyết định đã chốt) và spec mục 9.7.
Task 8 (FE màn phòng họp): đang chạy. Review Task 7: đang chạy.

Task 7: review — **không Approved**: (1) spec smoke FLAKY (reviewer chạy lần 1 fail ở assert badge "Khóa",
  lần 2 pass; DB cho thấy BE khóa đúng ⇒ lỗi timing của test) và **không dọn rác khi fail** (reviewer phải tự
  xoá bản ghi sót) — vi phạm quy tắc "phải dọn dữ liệu test"; (2) cờ `canView` tính mà không dùng.
  **Ruling về gate route**: `middleware/checkPermission.js` là middleware TOÀN CỤC đọc `isShow` từ registry
  menu → chặn URL trực tiếp là việc của **Task 9 (đăng ký menu)**, không phải của page ⇒ bỏ hẳn `canView`
  (dead code), giữ `canManage`. Đã ghi cơ chế này vào brief Task 9 và thêm **ca bắt buộc** vào brief Task 10:
  tài khoản thiếu quyền vào thẳng URL phải bị redirect VÀ bảng không render.
  Minor: chuyển `canManage` sang `computed` + mixin `CheckPermission.hasAPermission()` (helper có sẵn).
  Đã vào fix round 1/5.

Task 7: fix round 1/5 — implementer báo 3/3 addressed: bỏ hết `Promise.all([waitForResponse, click])` thay
  bằng assertion tự retry của Playwright; thêm `beforeAll` quét rác + `afterEach` xoá bản ghi của lần chạy
  **bất kể pass/fail**; bỏ hẳn `canView`; `canManage` thành `computed` dùng mixin `CheckPermission`.
  Bằng chứng: chạy 3 lần liên tiếp đều xanh, và **cố tình ép fail giữa chừng** → bản ghi vẫn bị dọn sạch.
  Đang chờ re-review (yêu cầu tự chạy 2 lần + truy vấn rác DB).

Task 7: complete (re-review 3/3 ADDRESSED; grep tự kiểm rỗng; re-reviewer tự chạy spec **2/2 lần xanh**
  (30.8s, 26.6s) — hết flaky; DB không còn rác thuộc phạm vi Task 7).
  ⚠️ Re-reviewer thấy 2 dòng rác `E2EUI_AM1_*`, `E2EUI_AM2_*` trong `meeting_room_amenities` — **thuộc spec
  của Task 8** (`_room-ui.smoke.spec.ts`), phải yêu cầu Task 8 dọn.

Task 8: DONE — `pages/meeting/rooms/index.vue` + `components/MeetingRoomModal.vue`; smoke UI **1 passed**,
  đo DOM (0→1 dòng, 2 chip tiện nghi, badge "Hoạt động"→"Khóa"), grep tự kiểm rỗng.
  3 nghi vấn implementer nêu, người điều phối đã xác minh 1 phần:
  (a) **API KHÔNG trả `company_name`/`manager_name`** — đã grep `MeetingRoomResource.php` xác nhận chỉ có
      `company_id`, `manager_employee_id`. FE đang tra tên từ store → rủi ro cột hiện RỖNG âm thầm khi store
      chưa/không có nhân viên đó. Đã đưa vào review để chốt hướng (nhiều khả năng BE phải trả 2 field).
  (b) `form-options` thỉnh thoảng bắn 2 lần khi mở modal → đang nhờ review xác định nguyên nhân thật.
  (c) Rác test: truy vấn DB hiện tại `meeting_room_amenities` + `meeting_rooms` không còn bản ghi `E2E%` ⇒ sạch.
  Đang review. Task 9 (menu) chạy song song.

Task 9: DONE — `components/subsystem-menu/meeting.js` sửa đúng 2 chỗ (`numstat 11/2`, EOL không bị phá).
  Spec `_menu.smoke.spec.ts`: **4 passed (26.9s)**. Đo DOM: nhóm "Quản lý phòng họp" 2 mục, "Danh sách phòng
  họp" có href đúng, "Đăng ký phòng họp" KHÔNG có href (đúng, Phase 2); bấm vào render bảng thật.
  **Ca gate quan trọng nhất đã xanh**: tài khoản thiếu quyền vào thẳng `/meeting/rooms` và
  `/meeting/room-amenities` → bị đá về `/pages/extras/404`, bảng đếm 0 phần tử ⇒ gate còn sống.
  Implementer tự dò DOM phát hiện sidebar phân hệ Meeting là kiểu **HUB** (`SaleHubSidebar.vue`,
  `.sale-cats`/`.misa-detail`), không phải cây UBold `#side-menu` như brief tôi viết → brief sai, code đúng.
  Đang chờ review.

Task 9: complete (review APPROVED, không issue Critical/Important). Reviewer tự đối chiếu 4 tên quyền trong
  `isShow` với DB (`permissions` id 1574-1577) — khớp từng ký tự; `isShow` là mảng; numstat gọn, EOL nguyên;
  ca thiếu quyền assert CẢ url `/pages/extras/404` LẪN `table.data-table` = 0; không dùng `networkidle`;
  reviewer tự chạy lại spec **4 passed (22.8s)**.

Task 8: review — **KHÔNG Approved**. Important: (1) không dùng mixin `CheckPermission` như ràng buộc (tự viết
  `perms.some(...)` trong `mounted`) + còn `canView` dead code; (2) spec e2e **không chắc dọn dữ liệu khi fail**
  (phòng test chỉ xoá ở bước cuối happy path).
  **Phát hiện dữ liệu đáng giá**: reviewer lần ra `$store.state.employees` nạp bằng `Employee::getAll(true)` —
  **chỉ nhân viên đang làm việc** (`Modules/Timesheet/Entities/Employee.php:78-83`) ⇒ phòng có người quản lý
  đã nghỉ việc sẽ hiện "—" dù DB còn dữ liệu. Sai âm thầm, chắc chắn xảy ra theo thời gian.
  **Ruling**: KHÔNG để lại thành task follow-up như reviewer gợi ý — sửa ngay ở BE (`MeetingRoomResource` trả
  `company_name`/`manager_name` + eager load, FE bỏ tra store, bổ sung ca e2e API). Lý do: Phase 1 mà bàn giao
  màn hiển thị sai tên là nợ lộ ra ở tay người dùng, chi phí sửa bây giờ rất nhỏ (2 field + 1 eager load).
  *Sai thì tốn*: thêm ~1 vòng fix + đo lại số query.
  Minor: guard chống gọi trùng `form-options` (không đụng `V2BaseModal`), đổi ô lọc sang `V2BaseSelect`.
  Đã vào fix round 1/5.

Task 8: fix round 1/5 — implementer báo xong 5 mục: mixin `CheckPermission` + bỏ `canView`; e2e có
  `beforeAll` quét + `afterEach` dọn (chứng minh bằng ép fail thật rồi gỡ assertion tạm); BE thêm quan hệ
  `company()`/`manager()` + 2 field `company_name`/`manager_name` ở cả 2 Resource, eager load ở index/show/
  updateOrCreate; FE bỏ tra store; guard `loadingFormOptions`; ô lọc đổi sang `V2BaseSelect`.
  **Bằng chứng đáng giá**: kiểm bằng nhân viên đã NGHỈ VIỆC thật (id 26 "Bùi Văn Long") → `manager_name`
  nay ra đúng tên, trong khi store FE không hề có nhân viên này ⇒ đúng bản chất lỗi đã sửa.
  Bộ `tests/meeting --project=api` (11 ca) xanh. Đang chờ re-review.
Task 10 (bộ e2e UI chính thức): đang chạy — gồm ca bảo mật lớp Resource và ca gate route.

Task 8: complete (re-review 5/5 ADDRESSED, không hỏng mới).
  Re-reviewer **tự đo độc lập** thay vì tin báo cáo: chạy tinker với N=2 và N=4 phòng → số query đụng
  `companies` = 1 và `employees` = 3 ở CẢ hai lần ⇒ đúng O(1) theo lô, không tăng theo số dòng.
  Cũng tự truy ngược để bác bỏ rủi ro "quan hệ dính scope lọc nhân viên đang làm việc": `Employee extends Model`
  (không phải BaseModel), không có `addGlobalScope`; bộ lọc `status=1` chỉ nằm ở `Employee::getAll(true)` dùng
  cho store FE, KHÔNG áp vào quan hệ Eloquent mới ⇒ `manager_name` ra đúng tên cả với nhân viên đã nghỉ.
  Test: `tests/meeting --project=api` **11 passed**, UI smoke **1 passed**; DB sạch rác.

Task 10: DONE — `e2e/tests/meeting/meeting-room.spec.ts` (5 nhóm, 11 ca UI) phủ đủ 8 nhóm ca, gồm **ca bảo mật
  lớp Resource** (`checkin_qr_token`) và **ca gate route**. Xoá 3 spec smoke đã bị phủ
  (`_room-ui`, `_room-amenity-ui`, `_menu`), giữ `_auth-smoke` + 2 spec API.
  Chạy: chromium **11 passed** ×2 lần (1.6m), api **11 passed** ×2 lần (13s). DB sạch rác `E2E%`;
  quyền cấp tạm (1575/role 20) đã thu hồi, `permissions guard=api` vẫn **745**.
  ⚠️ **Ruling R2 của tôi có lỗi, implementer sửa đúng**: code mẫu tôi đưa cuộn `.modal.show .modal-body`,
  nhưng DOM thật cho thấy phần tử đó KHÔNG cuộn (CSS của `V2BaseModal` tắt overflow) — phần tử cuộn thật là
  `.v2-modal-body`. Nếu giữ nguyên, ca "footer luôn trong viewport" sẽ **xanh giả**. Đây là lần thứ 2 trong
  plan này gặp assertion vô nghĩa ⇒ đã yêu cầu reviewer soi riêng loại lỗi này.
  Đang chờ review.

Task 10: review — **APPROVED** (Spec ✅) nhưng 1 Important + 1 Minor.
  Reviewer tự đo lại bằng Playwright MCP và xác nhận ca khuôn giao diện KHÔNG xanh giả:
  `.modal-body` scrollHeight=clientHeight=760, `overflow-y:hidden` (đúng là no-op như R2 sai),
  `.v2-modal-body` scrollHeight=714 > clientHeight=699, cuộn thật đổi `scrollTop` → footer bottom 849 ≤ 919.
  Cũng tự truy DB + đọc `CheckPermission.php` để xác nhận ca bảo mật chạm ĐÚNG lớp Resource (tài khoản có
  "Xem" đi qua được lớp route, nên `when(...)` trong Resource mới là thứ chặn token).
  **Important**: gom spec làm **mất ca "cảnh báo chưa lưu"** (`unsavedModalMixin`) và báo cáo KHÔNG khai —
  đúng hành vi mà Task 7 phải sửa `V2BaseModal` để có. Đã vào fix round 1/5 để bù ca + khai đủ coverage đã bỏ.
  Minor: thêm assert nút "Tạo mới" = 0 ở ca tài khoản trắng quyền.
  Reviewer tự chạy: api **11 passed (14.6s)**, chromium **11 passed (1.6m)**; DB sạch; `grant_tam=0`;
  `permissions guard=api` = 745.

Task 10: fix round 1/5 (2 addressed) → **complete**. Bù ca C1 "cảnh báo chưa lưu" đủ 4 nhịp (popup hiện với
  TEXT cụ thể → "Ở lại" giữ nguyên giá trị ô nhập → "Thoát" đóng modal → số dòng KHÔNG tăng) + assert nút
  "Tạo mới" = 0 ở D1/D2; báo cáo khai đủ coverage đã bỏ.
  **Re-reviewer làm đối chứng âm**: comment dòng gõ phím cho form không dirty → ca C1 **ĐỎ đúng chỗ**
  (popup không hiện), hoàn nguyên → **12 passed (1.7m)**. ⇒ ca test bắt lỗi thật, không xanh giả.

## PHASE 1 — HOÀN THÀNH 11/11 TASK (18/09/2026)
Tổng kết test: `tests/meeting --project=chromium` **12 passed**, `--project=api` **11 passed**, mỗi bộ chạy
≥2 lần, không ca nào "did not run". DB sạch rác `E2E%`; `permissions guard=api` = 745 (không mất dữ liệu).
Còn treo (deferred minors, đã ghi rõ ở trên): `destroy()` không `lockForUpdate` (race hiếm);
`unlock()` không kiểm điều kiện đối xứng với `lock()`; 2 ca đo sidebar menu-rail không port vào bộ chính thức.

## REVIEW TỔNG CẢ NHÁNH (18/09/2026) — kết luận: CẦN SỬA TRƯỚC KHI BÀN GIAO
Phát hiện 5 lỗi chỉ lộ khi nhìn toàn nhánh (từng task riêng lẻ đều đã Approved):
- **(A) LỖI THẬT, có bằng chứng trong DB ngay lúc này**: `MeetingRoomService::destroy()` không `detach()` tiện nghi,
  pivot lại không có FK ⇒ **78 dòng `meeting_room_room_amenity` mồ côi**. Kèm theo, 2 nơi tính cùng một luật lại
  lệch nhau (controller đếm pivot THÔ, `isCanDelete()` join `meeting_rooms`) ⇒ tiện nghi từng gắn phòng đã xóa sẽ
  **mãi mãi mất nút Xóa mà không lời giải thích**.
- **(B)** `form-options` chỉ trả tiện nghi đang hoạt động, select Người quản lý lấy từ store chỉ có nhân viên đang
  làm việc ⇒ mở màn Sửa của phòng dùng tiện nghi đã khóa / quản lý đã nghỉ thì ô trống, **lưu lại là mất dữ liệu**.
  Đúng quy tắc `utils/select2LockedOption.js` của dự án. (Trước đó mới sửa phần HIỂN THỊ `manager_name`, chưa sửa FORM.)
- **(C)** `meeting-room.spec.ts` hard-code đường dẫn worktree ⇒ người khác chạy là `ENOENT`, `serial` làm mọi ca sau
  in "did not run".
- **(D)** route `GET /room-amenities/{id}` thiếu `checkPermission` (lệch với route phòng đã gate).
- **(E)** `getAll` của tiện nghi là code chết, không nơi nào gọi.
Cộng 2 ca **xanh giả** còn sót trong spec API (assert `not.toContain` chạy trên body 403; vòng lặp trên mảng rỗng),
thiếu ca cho nhánh CHẶN XÓA, mất coverage menu, và `department_id`/`part_id` bị `BaseModel` điền âm thầm theo người tạo.
Đã dispatch **1 đợt fix gom A→H** (kèm FK cascade cho pivot + `unique('code')` cho `meeting_room_bookings` — bảng đang
0 dòng nên sửa bây giờ miễn phí).
**Deferred có ruling** (không chặn bàn giao): `destroy()` thiếu `lockForUpdate` → **điều kiện tiên quyết của Phase 2**
(hiện chưa ai ghi được vào bảng phiếu nên cửa sổ lỗi chưa tồn tại); `unlock()` không đối xứng `lock()` (hệ quả thấp);
`quantity`/`note` của pivot chưa dùng; `upcoming-bookings` trả `items: []` cứng.

Đợt fix sau review tổng: DONE A→H. Pivot mồ côi **78 → 0**; migration mới thêm FK cascade 2 chiều cho pivot +
  `unique('code')` cho `meeting_room_bookings`. Bộ test: api **14/14** ×3 lần, chromium **14/14** ×3 lần,
  không flaky, DB sạch, `permissions guard=api` vẫn 745.
  Mục B được kiểm 2 đường: ca e2e API + **kiểm trên trình duyệt thật** (tạo phòng dùng tiện nghi đã khóa +
  người quản lý đã nghỉ id 26 `status=0`, mở màn Sửa đo DOM thấy `🔒 Bùi Văn Long` và `🔒 Tiện nghi verify khóa`,
  lưu lại rồi gọi API đọc lại → **2 giá trị còn nguyên**, không bị nuốt).
  Không làm được 1 ca (đã khai): "phòng đã có phiếu đặt thì chặn xóa" — Phase 2 chưa có endpoint tạo phiếu,
  dựng bằng SQL thô phải đoán cột nghiệp vụ nên KHÔNG bịa ca giả. Ghi vào backlog Phase 2.
  Đang chờ re-review cuối (yêu cầu có đối chứng âm chứng minh FK cascade chạy thật).

Fix vòng 2 (residual sau re-review cuối): **complete**.
  - Ca 6 `room-amenity.api.spec.ts` hết xanh giả: nay assert **thẳng số dòng pivot = 0**. Đối chứng âm:
    comment `detach()` + `DROP FOREIGN KEY` 2 chiều → ca **ĐỎ đúng chỗ** (Expected 0, Received 1), hoàn nguyên
    đầy đủ (`git diff` của service rỗng, 2 FK về nguyên trạng) → xanh lại.
  - Gate `GET /meeting/rooms/form-options` bằng `checkPermission` (lệch cuối cùng so với các route khác);
    kiểm trên trình duyệt thật: admin mở modal load đủ options, token nocost gọi thẳng → **403**.
**NGƯỜI ĐIỀU PHỐI TỰ KIỂM LẦN CUỐI (18/09/2026)**: FK pivot = 2, unique `mrb_code_unique` = 1, pivot mồ côi = 0,
rác E2E = 0/0, `permissions guard=api` = **745**, grant tạm còn sót = 0, `meetings.meeting_room_id` có mặt.
Tự chạy: `tests/meeting --project=api` → **14 passed (23.8s)**; `--project=chromium` → **14 passed (2.0m)**.

- **R8 — GIỮ lại thư mục `.sdd/`** (quy trình mặc định là xoá sau khi review sạch vì "git history là bản ghi").
  Ở dự án này **cấm commit**, nên không có git history nào ⇒ xoá `.sdd/` là mất sạch báo cáo 11 task, các ruling
  và bằng chứng kiểm chứng. *Sai thì tốn*: thừa ~20 file tài liệu trong `.plans/` (có thể dọn sau khi merge).

## PHASE 1 ĐÃ XONG — CHỜ USER QUYẾT CÁCH MERGE

**18/09/2026 — 2 server của worktree bị hệ thống tắt vì máy hết RAM** (sau khi Phase 1 đã xong, không mất việc gì).
Server của phiên khác (`:8000`, `:3000`) vẫn sống, không bị ảnh hưởng.
Lệnh bật lại khi cần làm tiếp:
```bash
# API worktree :8001
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api && \
  /opt/homebrew/opt/php@7.4/bin/php artisan serve --host=127.0.0.1 --port=8001
# Nuxt worktree :3001 (node 12 + heap 8192)
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-client && \
  PATH="$HOME/.nvm/versions/node/v12.22.12/bin:$PATH" NODE_OPTIONS=--max-old-space-size=8192 npm run dev
```

# ===== PHASE 2 — Đặt phòng + duyệt (bắt đầu 18/09/2026, user duyệt plan) =====
Khảo sát trước khi lên plan, đo được 3 bẫy (đã ghi vào đầu mọi brief Phase 2):
- **Bẫy 1**: `sendToAllNotification()` nhận `employee_info_id`, bảng phòng họp lưu `employees.id`;
  đo thật: **chỉ 2/1099 nhân viên có `id == employee_info_id`** ⇒ truyền thẳng là thông báo tới NHẦM NGƯỜI,
  không lỗi không log. Bắt buộc 1 helper map dùng chung + ca test đọc DB kiểm người nhận.
- **Bẫy 2**: `getNextCode()` khuôn dự án dùng `max('id')+1`, mà Phase 1 đã thêm `unique('code')` ⇒ 2 request
  song song = 1 cái chết bằng lỗi SQL 1062 hiện thành 500. Phải sinh mã trong transaction + retry 1062.
- **Bẫy 3**: nợ Phase 1 đến hạn — `MeetingRoomService::destroy()` không `lockForUpdate`; bật luồng đặt phòng
  là cửa sổ lỗi thành thật. Vá ở Task 11 TRƯỚC khi mở API tạo phiếu.
Plan Phase 2: 8 task (11-18), user duyệt.

Task 11: DONE — `MeetingRoomBooking` + `MeetingRoomBookingParticipant` + `tests/Unit/MeetingRoomBookingOverlapTest.php`.
  TDD: đỏ (class not found) → xanh **OK (1 test, 4 assertions)**; chạy chung với test cũ: OK (2 tests, 7 assertions).
  Công thức giao giờ `startA < endB && endA > startB` (chạm mép KHÔNG trùng), phủ cả ca qua đêm.
  **Vá bẫy 3**: `MeetingRoomService::destroy()` nay kiểm phiếu bằng `lockForUpdate()` bên trong transaction.
  e2e API vẫn **14 passed (40.1s)** ⇒ không phá luồng xóa phòng của Phase 1.
  Concern implementer: `meeting_room_booking_participants` KHÔNG có cột `created_by`/`updated_by` nên `$fillable`
  cố ý bỏ 2 cột đó (đã đối chiếu `SHOW COLUMNS`) — hợp lý, không phải lỗi.
  Đang review. Task 12 (2 quyền) chạy song song.

Task 12: DONE — 2 quyền id **1579** (`Xem tất cả phiếu đặt phòng họp`) + **1580** (`Duyệt phiếu đặt phòng họp`),
  group `Quản lý phòng họp`. Seeder sửa + INSERT idempotent + cấp role Super admin (18) `company_id=1`.
  Kiểm: `permissions guard=api` = **747** (745 + 2), chạy lại SQL lần 2 vẫn 747. Không chạy `db:seed` (R7).
  Đang review.

Task 12: complete (review Approved, 0 issue; tên quyền khớp từng dấu, diff chỉ có dòng thêm, tổng 747).
Task 11: review — Approved, 2 Important:
  (1) `overlaps()` **nuốt input rỗng/null thành `now()`** — reviewer kiểm thực tế `Carbon::parse(null)` không ném
      lỗi mà trả về thời điểm hiện tại ⇒ tầng gọi truyền thiếu giờ là so sai mà không báo gì;
  (2) 4 method `isCan*` chưa có test nào, lại phụ thuộc `Carbon::now()` (phải dùng `Carbon::setTestNow()`).
  Cả 2 đều là nền cho Task 13/14 nên cho fix ngay. Nghi vấn Minor của reviewer về `unique('code')`: người điều phối
  tự xác minh — nằm ở migration `2026_09_18_000001` (đặt tên theo FK nhưng gộp cả unique, có comment), không thiếu.
Task 13 (API phiếu + chống trùng — phần khó nhất) chạy song song với fix Task 11.

Task 11: fix round 1/5 (2 addressed) → **complete**. Guard input rỗng/null ném `InvalidArgumentException`
  (test 8 tổ hợp, assert cả LOẠI exception lẫn THÔNG ĐIỆP nêu đúng tên tham số); test `isCan*` dùng
  `Carbon::setTestNow()` phủ 3 mốc biên giây (13:59:59 true / 14:00:00 false / 14:00:01 false) + `tearDown` reset.
  **Re-reviewer làm 2 đối chứng âm**: bỏ guard → 8/8 ca đỏ; đổi biên `lt` → `lte` → đỏ đúng dòng biên.
  Hoàn nguyên `diff` IDENTICAL. Tổng: **OK (25 tests, 47 assertions)**.

Task 13: DONE — Service/Controller/Request/2 Resource + route `meeting/room-bookings` + 19 ca e2e.
  TDD: đỏ (tắt route → 404, 18 ca sau "did not run") → xanh **19 passed (36.3s)**; chạy cả thư mục
  **33 passed (1.2m)** (19 mới + 14 của Phase 1) ⇒ không phá gì.
  Ca đua 2 request: đúng 1×200 + 1×422, không 500, và **đếm SQL thật xác nhận DB chỉ có 1 phiếu**.
  Ca sửa phiếu đã tới giờ → **423**, dựng trạng thái bằng SQL (không dùng sleep → không mong manh).
  Concern implementer: `ValidationException` ném từ Service ra khuôn `{message, errors}` của Laravel, khác
  `{code, errors}` của `BaseRequest` ⇒ FE phải xử 2 khuôn. Đã đưa vào review để chốt hướng thống nhất.
  ⚠️ Người điều phối yêu cầu reviewer soi riêng 1 điểm nghi ngờ: `lockForUpdate` trên **tập RỖNG** không khóa
  được gì (bảng chưa có dòng nào xung đột) → ca test song song có thể xanh nhờ may mắn, nhất là khi
  `artisan serve` xử lý tuần tự 1 request/lần.

Task 13: reviewer (opus) **bị treo** (không tiến triển 600s, chết ngay trước bước chạy e2e) → người điều phối
  tự làm phần nặng: chạy `tests/meeting --project=api` → **33 passed (1.1m)**, và **tự phân tích đoạn khóa**.
  **Ruling R9 — 2 phát hiện tự đo, không phỏng đoán:**
  1. `assertNoOverlap()` chạy `SELECT ... FOR UPDATE` trên tập **có thể RỖNG**. Đo: MySQL **8.0.43**,
     isolation **REPEATABLE-READ** ⇒ InnoDB có **gap lock** nên hiện tại vẫn chặn được chèn vào khoảng trống —
     code đúng, nhưng **đúng nhờ cấu hình**, không nhờ thiết kế. Production chạy `READ-COMMITTED` là gap lock
     gần như tắt ⇒ 2 phiếu trùng giờ lọt cả hai, âm thầm. → yêu cầu khóa **mutex trên dòng phòng** trước khi
     kiểm trùng (1 dòng, đúng bất kể isolation).
  2. **Ca test "2 request song song" không chứng minh được gì**: API chạy bằng `php -S` (`artisan serve`) —
     built-in server **xử lý tuần tự 1 request/lần**, nên `Promise.all` bị xếp hàng ở tầng web server; ca đó
     **xanh kể cả khi bỏ sạch khóa**. → yêu cầu đổi tên ca cho trung thực + thêm **ca đua THẬT ở tầng DB**
     (2 kết nối, 2 transaction) kèm **đối chứng âm** (bỏ khóa phải lọt 2 phiếu).
  *Sai thì tốn*: nếu mutex phòng gây chờ lâu khi nhiều người đặt cùng 1 phòng thì phải đổi sang khóa hẹp hơn.
  Kèm việc 3: thống nhất khuôn lỗi `{code, errors}` để FE map lỗi inline không phải đoán 2 khuôn.

Task 13: fix round 1/5 — 3 việc xong, **có bằng chứng số cho luật quan trọng nhất của feature**:
  script `.sdd/task-13-race-check.php` (2 kết nối PDO riêng, `proc_open`, không qua HTTP, không bootstrap Laravel):
  - không mutex + READ-COMMITTED → **lọt 2 phiếu** (tái hiện 2 lần) ⇒ rủi ro R9 là THẬT, không phải lý thuyết
  - có mutex + READ-COMMITTED → **1 phiếu**, đo được kết nối B chờ khóa **0.508s**
  - có mutex + REPEATABLE-READ → 1 phiếu
  Implementer tự phát hiện và sửa 1 lỗi trong bản nháp script (đặt delay SAU insert thay vì sau bước kiểm →
  hóa ra chỉ test khóa dòng thường, không test đúng khe TOCTOU) — đã yêu cầu reviewer soi lại đúng điểm này.
  Ca đua qua HTTP được **đổi tên cho trung thực** (chỉ kiểm "đặt trùng giờ liên tiếp thì lần sau 422").
  Khuôn lỗi thống nhất về `{code, errors}` như `BaseRequest`. Bộ e2e: **33 passed**, DB sạch.

Task 13: review gộp (gốc + fix 1) — 3 việc vòng 1 **đều đúng và đối chiếu được với code thật**: mutex đứng
  trước bước kiểm trùng và áp cho **cả `store` lẫn `update`**; script đua đặt delay **đúng khe TOCTOU**
  (sau bước kiểm, trước INSERT — không dính bẫy bản nháp); khuôn lỗi khớp `BaseRequest::failedValidation()`.
  Nhưng **KHÔNG Approved**, thêm 4 việc:
  1. **BUG MẤT DỮ LIỆU**: `update()` validate bằng giá trị fallback nhưng **lưu bằng giá trị request thô**
     ⇒ PUT không kèm `attendee_count` là ghi đè thành `null` âm thầm (cùng rủi ro với `host_employee_id`).
     33 ca hiện tại không bắt được.
  2. **N+1 thật**: Resource gọi `isCurrentEmployeeHasPermission()` cho TỪNG dòng (~40-60 query/trang 20 dòng).
  3. Cờ `is_can_approve/reject/cancel` chưa có ca kiểm phần **actor** ⇒ bỏ gate đi vẫn xanh (fail-open cho Task 14).
  4. **Bằng chứng khóa không nằm trong bộ test tự động**: xóa dòng mutex thì 33/33 ca vẫn xanh
     ⇒ yêu cầu chuyển script đua thành test PHPUnit 2 kết nối, có đối chứng âm ngay trong test.
  Minor: `created_at` ở Resource danh sách là ISO-8601 còn ở Resource chi tiết là `d/m/Y H:i:s` (spec 6.4 bắt ISO).
  Parked (ngoài phạm vi): khuôn lỗi 422 của 2 controller cũ khác khuôn mới — Task 17 cần biết.
  Đã vào fix round 2/5.

Task 13: fix round 2/5 — 5 việc xong:
  1. **Bug mất dữ liệu đã sửa** (chỉ ghi đè field khi request có gửi; validate và lưu dùng CÙNG giá trị).
     Ca e2e D6 được kiểm ngược: tạm gỡ fix → thấy `Expected: 10, Received: null` ⇒ ca bắt lỗi thật.
  2. **N+1: 89 → 9 query** cho 20 dòng (tính quyền 1 lần, gán vào từng model — KHÔNG dùng static trên Resource).
  3. Ca F1/F2 kiểm actor gate. Phát hiện phụ đáng ghi: **token admin đã sẵn quyền 1580** nên không dùng làm
     "người ngoài" được — phải đổi cách dựng dữ liệu để cô lập đúng biến cần kiểm.
  4. **Giải được bài toán "test khóa DB hay flaky"**: thay vì đo thời gian, test thứ 3 reflect vào
     `assertNoOverlap()` thật và dùng `DB::listen()` khẳng định có câu `FOR UPDATE` chạy trên `meeting_rooms`
     ⇒ **gỡ dòng mutex là đỏ ngay, không phụ thuộc timing**. Đã bác bỏ phương án dùng `artisan tinker` con
     (đo được ~1.15s khởi động, vượt cửa sổ đua 0.7s → flaky).
  5. ISO-8601 thống nhất giữa Resource danh sách và chi tiết.
  Kết quả: e2e **36 passed**, PHPUnit `--filter MeetingRoom` **28 passed**, DB sạch. Đang re-review.

Task 13: complete (re-review 5/5 ADDRESSED; **re-reviewer tự làm lại đối chứng âm**: comment dòng mutex →
  test khóa ĐỎ đúng thông điệp, hoàn nguyên → `OK (3 tests, 7 assertions)`; tổng PHPUnit **28 passed
  (54 assertions)**; xác nhận không có đường console/job nào gọi `attachDisplayNames()` khi `auth()` rỗng).
  Ghi nhận rủi ro còn lại (chấp nhận): 2 test mô phỏng SQL trần dùng `usleep(700000)` cố định → về lý thuyết
  flaky nếu round-trip DB > 700ms trên máy quá tải.

Task 14: code đã xong (3 endpoint `approve`/`reject`/`cancel` + luật nhìn thấy phiếu), nhưng agent **kẹt trong
  vòng chờ test nền**, kết thúc lượt 3 lần mà không báo cáo → người điều phối tự chạy:
  `tests/meeting --project=api` → **51 passed (7.4m) NHƯNG 1 FLAKY**, đúng ca **G1 — luật trọng tâm của task**
  (duyệt 1 trong 3 phiếu trùng giờ → 2 phiếu kia tự từ chối, kiểm bằng DB thật).
  **Ruling R10**: flaky ở ca kiểm luật lõi **không được cho qua**, và **cấm "sửa" bằng tăng timeout/thêm retry**
  (đó là giấu lỗi). Yêu cầu truy nguyên nhân gốc từ `test-results/` rồi phân loại: lỗi THẬT trong luồng duyệt
  (thiếu khóa → thứ tự auto-reject không xác định, hoặc đọc DB trước khi commit xong) hay lỗi của chính ca test
  (chờ sai mốc / dựng dữ liệu phụ thuộc thứ tự / trùng rác lần trước). Chạy lại 2 lần liên tiếp, dòng tổng kết
  phải **không có dòng `flaky`**.
  *Sai thì tốn*: nếu là lỗi luồng duyệt thật mà bỏ qua, production sẽ có lúc duyệt lọt 2 phiếu trùng giờ.

Task 14: DONE — 3 endpoint `approve`/`reject`/`cancel` + `applyVisibilityScope()`/`canView()` + 2 Request mới
  + 16 ca e2e (nhóm G/H/I/J). Chạy lại **2 lần foreground: 52 passed, KHÔNG còn dòng `flaky`**.
  Kết luận về ca flaky (R10): implementer truy được flaky **nhảy qua 3 ca không liên quan** (A1, G1, J3-hook)
  đúng lúc có phiên Playwright khác chạy song song trên máy, và biến mất hẳn khi phiên kia kết thúc ⇒ chữ ký của
  **tranh chấp tài nguyên máy**, không phải bug logic. Có sửa 1 vấn đề hiệu năng độc lập tìm được (gom SQL dọn
  dẹp ở `afterAll`), **không** tăng timeout/retry để che.
  ⚠️ Trung thực ghi nhận: trace gốc của lần fail **đã bị phiên khác ghi đè** trước khi đọc được ⇒ kết luận dựa
  trên review code + tương quan thời điểm, KHÔNG phải bằng chứng trực tiếp. Đã yêu cầu reviewer thẩm định lại
  bằng cách đọc code (thứ tự auto-reject có xác định không, ca G1 chọn phiếu duyệt theo id cố định hay theo
  thứ tự DB trả về).
  3 ca trọng tâm PASS: G1 (duyệt 1/3 → 2 phiếu tự từ chối, kiểm bằng SQL trực tiếp) · I6 (hủy phiếu `source=2`
  → 423 cho CẢ chủ phiếu lẫn quản lý phòng) · J1/J2 (quản lý phòng không quyền 1579 vẫn thấy phiếu phòng mình,
  người ngoài bị chặn).

Task 14: review — **Approved**, và reviewer **thẩm định lại kết luận flaky bằng đọc code, ĐỒNG Ý**: `approve()`
  tự-chối TẤT CẢ phiếu trùng (không có nhánh "chọn phiếu đầu tiên") nên thứ tự DB trả về không ảnh hưởng;
  ca G1 chọn phiếu duyệt bằng **id cố định** `bookingIds[0]` nên tự nó xác định; `DB::transaction` commit trước
  khi trả response nên không có race đọc-ghi. ⇒ khép lại giả thuyết "bug logic".
  **Important reviewer tự tìm ra khi rà thứ tự khóa (không ai yêu cầu)**: `approve()` khóa **Room → Booking**
  (khớp `store()`), nhưng `update()` (từ Task 13) khóa **Booking → Room** — **thứ tự khóa ngược chiều**, đúng
  khuôn deadlock kinh điển. 1 người sửa phiếu đúng lúc 1 người duyệt cùng phiếu → MySQL giết 1 giao dịch, và
  Controller `catch (Exception)` chung nên **lỗi SQL thô lọt ra thành 500**. Comment trong code khẳng định
  "đã giữ đúng thứ tự khóa" — chỉ đúng khi so với `store()`, **sai khi so với `update()`**.
  Đã cho fix: thống nhất 1 thứ tự khóa toàn module + **thêm test chứng minh `approve()` thật sự lấy mutex phòng**
  (kỹ thuật `DB::listen`, đỏ ngay khi gỡ khóa, không phụ thuộc timing) + bỏ `Log::error` cho nhánh 403/423 hợp lệ.

Task 14: fix round 1/5 — thống nhất thứ tự khóa (`update()` nay khóa Room trước, cùng chiều `store()`/`approve()`),
  sửa lại docblock khẳng định sai, gom 6 catch thành `handleServiceException()` chỉ `Log::error` cho mã ngoài
  [403,422,423]. **Thêm test chứng minh `approve()` lấy mutex phòng** bằng `DB::listen` + **đối chứng âm tự làm**:
  gỡ `lockForUpdate()` → test ĐỎ, khôi phục → `OK (1 test, 3 assertions)`.
  Kết quả: PHPUnit **29 tests / 57 assertions OK**; e2e 2 lần foreground **52 passed** (1.3m, 1.6m), không `flaky`.
  Đang re-review (yêu cầu tự làm lại đối chứng âm + rà xem còn đường ghi nào khóa ngược chiều không, gồm cả
  `MeetingRoomService` của Phase 1 khi xóa phòng).
Task 15 (5 loại thông báo — task chứa bẫy 1 "gửi nhầm người") chạy song song.

Task 14: re-review fix 1 — 3/3 ADDRESSED (re-reviewer **tự làm lại đối chứng âm**: gỡ `lockForUpdate` trong
  `approve()` → test đỏ đúng thông điệp, khôi phục → OK; xác nhận gom catch KHÔNG đổi mã HTTP nhánh nào và
  KHÔNG nuốt `ValidationException`; bác bỏ nghi ngờ "`$room` cũ/mới" — `update()` luôn lấy phòng ĐÍCH từ request).
  **NHƯNG phát hiện cửa deadlock còn mở ở file khác**: `MeetingRoomService::destroy()` (code Phase 1) khóa
  **Booking trước → Room sau** (`delete()` lấy khóa Room ở bước cuối vì `MeetingRoom` không dùng SoftDeletes),
  ngược quy ước vừa thống nhất. Reviewer dựng kịch bản cụ thể bằng **gap lock** của InnoDB: `destroy()` trên
  phòng CHƯA có phiếu vẫn đặt gap lock trên khoảng `meeting_room_id = X`, trong khi `store()` giữ khóa Room X
  → chờ chéo → deadlock → 500.
  Đã cho fix round 2 (chỉ đụng `MeetingRoomService.php`), kèm yêu cầu **liệt kê TOÀN BỘ `lockForUpdate()` trong
  module + chiều khóa từng chỗ**, tính cả khóa Room "ngầm" do `DELETE`/`UPDATE`.

Task 14: fix round 2 — **agent lại kẹt vòng chờ** (kết thúc lượt với "I'll wait for this monitor notification"),
  người điều phối tự kiểm file: `MeetingRoomService::destroy()` (dòng 204-220) **đã khóa Room trước** rồi mới
  khóa Booking, có comment ghi quy ước. Rà nhanh mọi `lockForUpdate` trong `Modules/Meeting`: các cặp đều theo
  chiều **Room → Booking** (`MeetingRoomService` 208→211; `MeetingRoomBookingService` 214→218, 310→312).
  **Hoãn audit chi tiết + chạy test sang vòng review GỘP sau khi Task 15 xong** — vì Task 15 đang sửa
  `MeetingRoomBookingService.php` và Controller để thêm thông báo, audit/chạy test lúc này sẽ lạc hậu ngay.
  ⚠️ Ghi nhận về agent Task 14: 5 lần kết thúc lượt trong trạng thái "đang chờ test/monitor" mà không báo cáo
  → từ giờ mọi dispatch phải ghi rõ "chạy foreground, cấm đẩy nền rồi kết thúc lượt".

  → Đã **TaskStop** agent Task 14 (lặp vô ích, ~400k token chỉ để chờ). Code fix round 2 đã ở trong worktree và
  người điều phối đã tự xác minh; phần kiểm chứng chạy test gộp vào vòng review sau Task 15.

Task 15: DONE — 5 loại thông báo `[DPH]` + 3 helper dùng chung (`mapEmployeeIdsToEmployeeInfoIds()` cho bẫy 1,
  `buildNotificationContent()` tự cắt 50/120 ký tự, `sendBookingNotification()` bọc try/catch không làm hỏng
  nghiệp vụ) + 7 ca nhóm K đọc **thẳng bảng `notifications`**.
  **Bẫy 1 được chứng minh bằng số đo thật**: employee 34 → `employee_info_id` **23**; employee 25 → **13**
  (đều KHÁC `employees.id`) ⇒ nếu truyền thẳng id nhân viên thì thông báo bay sang người khác. Ca K1 assert
  `notifiable_id == 13` (không phải 25).
  Bắt được 1 lỗi thật của công cụ test: `mysql` CLI chế độ batch **nhân đôi dấu `\`** làm hỏng chuỗi `\uXXXX`
  của `json_encode()` khi đọc cột `data` → phải thêm cờ `--raw`; lỗi này lộ ra dưới dạng ca K1 ĐỎ thật, không
  phải dương tính giả.
  Kết quả: **59 passed**, chạy 2 lần foreground, không `flaky`. DB sạch (0 phòng/phiếu/thông báo sót).
  Ghi nhận concern: `sendBookingNotification()` giả định luôn có `auth()->user()` (mọi route đều sau `auth:api`)
  — nếu sau này có job nền gọi tới thì phải bổ sung nhánh CLI như `MeetingService::notifyMeetingEmployees()`.
  Đang review GỘP cùng fix round 2 của Task 14 (kèm audit toàn bộ điểm khóa trong module).

Review GỘP (Task 14 fix2 + Task 15): **Approved có điều kiện**.
  Phần A — audit khóa toàn module đã làm đủ: lập bảng 6 hàm, **không còn chỗ nào khóa Booking trước Room**;
  `reject()`/`cancel()` chỉ khóa 1 bảng nên không tạo được chu trình chờ. Luồng xóa phòng Phase 1 giữ nguyên
  hành vi + thông điệp lỗi.
  Phần B — bẫy 1 đạt (chỉ **đúng 1** lệnh gọi `sendToAllNotification` trong module, luôn qua helper map);
  5 loại thông báo gắn đúng chỗ; `url`/`type` đúng; gửi lỗi **không** rollback nghiệp vụ (try/catch nuốt gọn).
  Nhóm K được khen: assert **đúng số lượng người nhận** (`toEqual` mảng id đã sort, `length` cụ thể) nên bắt
  được cả trường hợp gửi DƯ — không phải kiểu "tồn tại ≥ 1".
  **2 Important còn lại → đã cho fix:**
  1. **Luật cắt chuỗi làm MẤT LÝ DO TỪ CHỐI**: vượt 120 ký tự thì code **xóa sạch ghi chú** thay vì cắt ngắn,
     trong khi skill quy định "cắt Ghi chú trước". Với loại Từ chối, lý do (tới 500 ký tự) **biến mất hoàn toàn**
     khỏi thông báo — người nhận không biết vì sao bị từ chối. Chưa có ca test nào phủ tên > 50 ký tự.
  2. `MeetingRoomService::destroy()` chưa có test chứng minh thứ tự khóa (chỉ xác minh bằng mắt) — yêu cầu thêm
     test `DB::listen` kiểm **THỨ TỰ** (Room trước Booking), kèm đối chứng âm đảo 2 lệnh khóa.
  Minor ghi nhận, không sửa: `reject()`/`cancel()` đọc `manager_employee_id` không khóa (tiền tồn tại).

Task 15: fix round 1/5 — 2 Important xong:
  1. `buildNotificationContent()` nay **cắt ngắn ghi chú theo hạn mức còn lại** (kèm `...`), chỉ đụng tên đối
     tượng khi đã hết ngân sách — đúng thứ tự skill. Thêm `tests/Unit/MeetingRoomBookingNotificationContentTest.php`
     (9 ca): tên > 50 ký tự bị cắt 47 + `...`; **ca đúng kịch bản lỗi** (Từ chối + tiêu đề dài + lý do dài →
     nội dung vẫn còn PHẦN THẬT của lý do, không phải chỉ còn nhãn "Lý do:"); data provider 5 tổ hợp xấu nhất
     chứng minh tổng ≤ 120.
  2. Thêm `test_destroy_that_su_dung_lockForUpdate_dung_thu_tu_room_truoc_booking()` — assert **THỨ TỰ** (vị trí
     câu `for update` trên `meeting_rooms` < vị trí câu trên `meeting_room_bookings`). **Đối chứng âm**: đảo 2
     lệnh khóa → ĐỎ ("Failed asserting that 1 is less than 0"), khôi phục → XANH.
  Bổ sung mục "Fix round 2" còn thiếu vào `.sdd/task-14-report.md`.
  Kết quả: PHPUnit **39 tests / 80 assertions OK** (×2 lần), e2e **59 passed** (×2 lần), DB sạch.
  Đang re-review. Task 16 (FE màn danh sách phiếu) chạy song song.

Task 15: complete (re-review 2/2 ADDRESSED). Re-reviewer **tự tính lại dữ liệu test để chứng minh nhánh cắt có
  chạy thật**: ca trọng tâm dùng title 71 ký tự + note 176 ký tự → budget ~47-50 ⇒ chắc chắn kích hoạt nhánh cắt;
  và assert **nội dung thật** (`assertStringStartsWith` 10 ký tự đầu của lý do gốc) chứ không chỉ độ dài ≤ 120.
  Tự làm đối chứng âm cho test khóa `destroy()`: đảo thứ tự → ĐỎ ("1 is less than 0"), hoàn nguyên → 39/39 OK,
  `diff` xác nhận worktree sạch sau khi kiểm.
  **Ghi nhận trung thực của re-reviewer**: 2/5 tổ hợp trong data provider KHÔNG chạm ngưỡng cắt (chỉ xác nhận
  "không hỏng khi không cần cắt"), và riêng ca "tổng ≤ 120" thì một bản cài SAI THỨ TỰ vẫn có thể pass — rủi ro
  đó được bịt bởi ca (b) kiểm nội dung. ⇒ Không có ca nào xanh giả với đúng loại lỗi đã tìm ra.

Task 16: DONE — `pages/meeting/bookings/index.vue` + `BookingDetailModal.vue` (popup XEM) + điền link menu
  `Đăng ký phòng họp` (`git diff --numstat` gọn: 8 thêm / 2 xóa). Spec smoke **5 passed (1.0m)**.
  Đo DOM: 10 tiêu đề cột đúng thứ tự; dòng **"Chờ duyệt" có 5 nút** hành động, dòng **"Đã duyệt" có 3**
  (Duyệt/Từ chối = 0) ⇒ chứng minh cờ BE được tôn trọng chứ không phải FE tự suy.
  Lần chạy đầu bắt được lỗi **của chính ca test** (kỳ vọng `'0'` trong khi `attendee_count` null thì FE hiện `'—'`)
  → sửa assertion, không sửa code.
  3 concern ghi nhận: (1) nhánh "mặc định BẬT công tắc Chỉ phiếu của tôi khi thiếu quyền 1579" **hiện không có
  tài khoản thật nào chạm tới** (mọi role có quyền danh mục phòng đều đã có 1579) — cần xác nhận ở mức sản phẩm;
  (2) nút Sửa đang mở popup xem, form thật là việc của Task 17; (3) luồng Từ chối/Hủy có bắt buộc nhập lý do
  **chưa được bấm thật trên trình duyệt** → đưa vào Task 18.
Task 17 (modal đặt phòng) đang chạy.

Task 17: DONE — `BookingFormModal.vue` (form thật, tạo + sửa), nối vào màn danh sách; spec smoke **2 passed**,
  chạy lại spec Task 16 **5 passed** (không hồi quy).
  Đo DOM thật: dải giờ bận đúng 1 khoảng → 2 khoảng sau khi thêm phiếu; cảnh báo vượt sức chứa hiện khi
  nhập 10 > sức chứa 5 và **giữ nguyên số 10 user gõ** (không tự sửa), tắt khi nhập 3; lỗi trùng giờ hiện
  `.v2-error` **nằm trong đúng khối ô "Từ giờ"**, khối "Đến giờ" 0 lỗi, và **0 phần tử toast** ⇒ chứng minh
  lỗi inline chứ không phải toast.
  2 bug tự tìm + tự tái hiện trước khi sửa: (a) `V2BaseSelectInModal` trả `meeting_room_id` kiểu **string**
  trong khi `id` của option là **number** → so sánh hụt, rơi vào option khóa ảo có `capacity = 0`;
  (b) phím **Escape** trong datepicker nổi bọt lên đóng luôn cả modal (bẫy đã biết của dự án).
- **Ruling R11 — lỗ hổng thiết kế do Task 17 phát hiện**: spec quyết định #8 cho **mọi nhân viên đặt phòng**,
  nhưng `GET meeting/rooms` + `form-options` lại gate quyền danh mục ⇒ nhân viên thường mở form thấy select
  phòng **RỖNG, không lỗi, không giải thích** — tính năng vô dụng với đa số người dùng.
  Quyết định: **KHÔNG nới gate danh mục**, thêm endpoint riêng `GET meeting/rooms/bookable` (chỉ `auth:api`),
  chỉ trả phòng đang hoạt động + cùng công ty hoặc `allow_cross_company`, **không trả `checkin_qr_token`**,
  kèm ca test: nocost gọi `/rooms` vẫn 403 nhưng `/rooms/bookable` 200 và không rỗng.
  *Sai thì tốn*: nếu sau này cần lọc phòng theo quyền chi tiết hơn thì phải mở rộng endpoint này.

Task 17: fix round 1 — endpoint `GET meeting/rooms/bookable` đã vào code (route KHÔNG gắn checkPermission,
  Resource gọn riêng `BookableMeetingRoomResource` không có `checkin_qr_token`), FE đổi sang dùng nó.
  **Người điều phối tự kiểm bằng request thật** (agent lại kẹt vòng chờ → đã TaskStop):
  nocost `GET /meeting/rooms` → **403** (gate danh mục giữ nguyên), `GET /meeting/rooms/bookable` → **200**,
  body **không chứa** `checkin_qr_token`. ⇒ R11 đã bịt đúng cách.
  Tự chạy: API **60 passed (2.0m)**.
⚠️ **UI ĐỎ — đúng bẫy CLAUDE.md đã cảnh báo**: `tests/meeting --project=chromium` →
  `1 failed / 1 did not run / 19 passed`. Ca đỏ là **F1** (viết ở Task 10) khẳng định *"Đăng ký phòng họp
  KHÔNG có href"* — đúng ở Phase 1, nhưng Task 16 vừa điền link cho mục đó nên **giả định cũ hết hiệu lực**.
  Bộ test chạy `serial` nên ca đỏ kéo theo 1 ca sau "did not run" (không phải passed).
  → Đã giao Task 16 cập nhật ca F1 theo hành vi mới + rà các ca khác còn giả định menu cũ.
  **Bài học lặp lại lần 3 trong plan này**: agent kết thúc lượt trong lúc chờ test nền; từ giờ mọi dispatch có
  chạy test đều ghi in hoa "CHẠY FOREGROUND".

Task 16: fix round 1 — cập nhật ca **F1** theo hành vi mới (`Đăng ký phòng họp` nay CÓ href, bấm vào phải render
  bảng phiếu thật — đo DOM chứ không chỉ đo URL), đổi cả tên ca cho khớp assertion; rà cả thư mục không còn ca
  nào giả định menu cũ. Chạy foreground: **21 passed (3.6m)**, không failed/did not run/flaky. DB sạch.
Task 18 (gom bộ e2e chính thức Phase 2 + bổ sung ca Duyệt/Từ chối/Hủy bấm thật trên trình duyệt) đang chạy.

Task 18: DONE (agent kẹt vòng chờ lần thứ 4 → **TaskStop**, người điều phối tự kiểm + tự chạy).
  Bộ e2e chính thức: `meeting-room-booking.spec.ts` (11 ca UI, gồm C1 Từ chối bắt buộc lý do / C2 Hủy / C3 Duyệt
  / E1 gate route) + `meeting-room.spec.ts`; 2 spec smoke `_bookings-ui`, `_booking-form-ui` đã xoá; giữ `_auth-smoke`.
  **Người điều phối tự chạy**: API **60 passed (1.5m)**; UI **25 passed (4.9m)** và **25 passed (4.7m)** lần 2
  ⇒ ổn định, không flaky, không "did not run".
- **BÁO ĐỘNG HỤT (ghi lại để không ai xoá nhầm sau này)**: truy vấn thấy **cả 7 quyền phòng họp (1574-1580) được
  cấp cho role `E2E No Cost` (id 100125)** → thoạt nhìn giống rác quyền cấp tạm chưa thu hồi. **Đã KHÔNG xoá mà
  truy nguồn trước**: `hrm-api/database/e2e_provision.php:164` cho thấy role này là của **chính script provision
  của dự án**, thiết kế là *"copy mọi quyền company_id=1 của Super admin TRỪ quyền 1045 (giá vốn)"* ⇒ script tự
  nhân bản 7 quyền mới sang đó, **không phải rác của mình**. Người mang role đó là nhân viên **1181**
  (`e2e_assign_nocost@test.local`), KHÔNG phải nhân viên 25 mà bộ test dùng làm tài khoản thiếu quyền
  (nhân viên 25 mang role 100003 + 20). ⇒ Không cần dọn, không ảnh hưởng tính đúng đắn của các ca kiểm quyền.
  *Bài học*: dữ liệu trông giống rác trên DB dùng chung thì phải truy nguồn trước khi xoá.


## REVIEW TỔNG PHASE 2 (18/09/2026) — kết luận: CẦN SỬA TRƯỚC KHI BÀN GIAO
4 lỗi mức hậu quả thật, **cả 4 nằm ở CHỖ NỐI giữa các task** nên review từng task không thấy:
- **(A) Nhân viên thường không vào nổi màn đặt phòng**: menu khai `isShow` = 2 quyền DANH MỤC, mà middleware
  dùng chính `isShow` làm gate URL ⇒ bị đá 404 trước khi modal kịp mở. Quyết định #8 ("mọi nhân viên đặt phòng
  được") **không thực hiện được**, và endpoint `/rooms/bookable` lập ở R11 chỉ phục vụ người VỐN ĐÃ có quyền —
  **bịt đúng kỹ thuật nhưng bịt ở tầng không ai đi qua**. Tệ hơn: ca E1 **đóng đinh hành vi sai thành kỳ vọng**.
- **(B) Thông báo dẫn tới màn trống**: BE gửi deep-link `?open_booking=<id>` nhưng FE **không đọc tham số đó**;
  cộng thêm `defaultOnlyMine()` bật bộ lọc "Chỉ phiếu của tôi" ⇒ **phiếu cần chính quản lý phòng duyệt bị lọc mất**.
  Đúng điều skill `notification-convention` cấm. Nhóm ca K xanh vì chỉ assert `url` đúng khuôn, **không ca nào bấm thật**.
- **(C) `content` vẫn bị null hóa** — cùng họ bug đã sửa ở Task 13 nhưng **sót field thứ 3**; ca D6 chỉ phủ 2 field
  kia ⇒ bug lọt qua đúng cái lưới vừa dựng để bắt nó.
- **(D) `approve()` KHÔNG gọi `assertNoOverlap()`** ⇒ còn đường tạo **2 phiếu Đã duyệt trùng giờ cùng phòng
  KHÔNG CẦN ĐUA**: phòng đang có phiếu Chờ duyệt → admin đổi `require_approval` về 0 → người khác đặt trùng giờ
  (chỉ so với phiếu Đã duyệt nên lọt) → quản lý bấm Duyệt phiếu cũ → 2 phiếu cùng Đã duyệt. Spec edge case 6
  yêu cầu đúng việc còn thiếu.
⚠️ **Dòng "DB sạch" tôi ghi ở Task 18 đã LẠC HẬU**: reviewer đo được **118 dòng participants mồ côi** + **21 thông
  báo `[DPH]` rác** từ 2 spec smoke đã xóa (`afterAll` xóa phiếu nhưng không xóa participants/thông báo).
Ghi nhận tốt (giữ nguyên): bộ `MeetingRoomBookingRaceTest.php` (đối chứng âm 2 kết nối + `DB::listen` bắt cả sự
  tồn tại lẫn THỨ TỰ khóa); quy ước khóa Room→Booking **nhất quán ở mọi đường ghi**; `attachDisplayNames()` gom
  quyền/tên 1 lần, fail-closed; `/rooms/bookable` dùng lại `canBeBookedByCompany()` thay vì chép luật.
Đã dispatch 1 đợt fix gom A→F (kèm dọn rác + thêm FK cascade cho participants).
Ghi chú: prefix `[DPH]` reviewer nghi chưa hỏi user — thực tế **đã hỏi và user chốt "đúng chuẩn skill"**, xem mục
  trao đổi trước Task 11.

Đợt fix sau review tổng Phase 2: **agent kẹt vòng chờ lần thứ 5 → TaskStop**; người điều phối tự kiểm code +
  tự chạy toàn bộ. Cả 6 mục A→F đã vào code:
  A. `isShow: true` cho mục "Đăng ký phòng họp" (2 màn danh mục vẫn gate) — nhân viên thường vào được màn đặt phòng.
  B. FE đọc `?open_booking=<id>`, tự mở popup phiếu đó và **tắt** bộ lọc "Chỉ phiếu của tôi" trong lượt vào đó.
  C. `content` nay có guard `$request->has('content')` như 2 field kia.
  D. `approve()` gọi `assertNoOverlap()` sau khi cầm mutex phòng (có comment ghi rõ kịch bản 4 bước đã bịt).
  E. Migration mới `2026_09_18_000002` thêm FK cascade cho `meeting_room_booking_participants`;
     **participants mồ côi 118 → 0**.
  F. Bỏ 2 khối catch code chết, thêm `exists:employees,id`, chặn duyệt/từ chối phiếu đã tới giờ.
  **Người điều phối tự chạy**: PHPUnit **39 tests / 80 assertions OK**; e2e API **61 passed (1.7m)**;
  e2e UI **26 passed (5.1m)**; 2 lệnh grep FE rỗng.
⚠️ **Dữ liệu còn trong DB KHÔNG phải rác**: phòng `B1 "Phòng B nhỏ"` (id 1618) + phiếu `DPH-2026-00001
  "test lần 1"` (09:00-12:00 ngày 19/09) + 2 thông báo — **do chính user tạo tay khi dùng thử app**
  (`namdangit@gmail.com`, employee 13). KHÔNG đụng vào. Đây cũng là bằng chứng end-to-end tốt nhất:
  phòng không cần duyệt → phiếu vào thẳng **Đã duyệt**, và thông báo bay tới **`employee_info_id = 13`**
  (đúng cơ chế map của bẫy 1 — nếu sai thì đã gửi nhầm người).

Re-review đợt fix cuối: **5/6 mục ADDRESSED đầy đủ, kết luận SẴN SÀNG BÀN GIAO PHASE 2.**
  Reviewer tự kiểm bằng code + DB + PHPUnit (báo cáo của agent bị dừng nên không có file để đọc).
  Xác nhận 3 ca quan trọng nhất là **ca thật, không xanh giả**:
  - **G5** dựng đúng kịch bản 4 bước của lỗ hổng duyệt trùng giờ, assert **422** rồi **query DB thật** xác nhận
    phiếu A vẫn Chờ duyệt / phiếu C vẫn Đã duyệt ⇒ sẽ đỏ nếu thiếu `assertNoOverlap()` trong `approve()`.
  - **E1** dựng sẵn phiếu của NGƯỜI KHÁC rồi assert `toHaveCount(0)` ⇒ không phải kiểu "vào được là xong".
  - **F1** dùng đúng tài khoản **quản lý phòng** (người đặt là account khác) mở thẳng `?open_booking=` và đo mã
    phiếu trong popup ⇒ đúng kịch bản sinh bug gốc.
  Xác nhận không đụng dữ liệu thật của user (phòng B1, phiếu DPH-2026-00001 còn nguyên).
  **Residual duy nhất (parked, không chặn bàn giao)**: thiếu ca test cho nhánh **423 "phiếu đã tới giờ"** ở
  `approve()`/`reject()` — code đúng và đồng nhất với `update()`/`cancel()` (2 hàm này đã có ca D5/I5), nhưng
  nếu lần sửa sau ai xoá nhầm nhánh đó thì **không test nào báo đỏ** (rủi ro hồi quy im lặng).
  *Ruling*: parked, ghi vào nợ kỹ thuật trong `plan.md`. Lý do: đây là khoảng trống coverage, không phải lỗi
  đang tồn tại; và theo quy trình, sau 1 đợt fix + 1 vòng re-review thì residual không load-bearing sẽ được
  ghi nhận chứ không mở thêm vòng.

## PHASE 2 — HOÀN THÀNH 8/8 TASK (18/09/2026), CHỜ USER QUYẾT CÁCH MERGE

# ===== PHASE 3 — Màn theo dõi tình trạng phòng (bắt đầu 18/09/2026) =====
Phase 2 đã commit: BE `35e5fe7d7`, FE `1625e51c6` (nhánh `feat/quan-ly-phong-hop`, không push, không merge).
Plan Phase 3: 6 task (19-24), 5 bẫy đã ghi vào đầu mọi brief:
  (1) KHÔNG có FullCalendar resource-timeline (bản Premium) ⇒ lưới Phòng × Giờ phải tự dựng bằng CSS grid;
  (2) đo layout trong watcher + `$nextTick` ra DOM CŨ ⇒ phải kèm `requestAnimationFrame`;
  (3) phiếu QUA ĐÊM phải hiện ở mọi ngày nó chạm + khung giờ tự nới (nếu không: phòng đang bị giữ mà lưới
      trông như trống);
  (4) CẤM `networkidle` (màn tự refresh 60s) + phải `clearInterval` khi rời màn;
  (5) 1 request cho cả lưới, cấm gọi mỗi phòng 1 request.

Task 19: DONE — 3 endpoint `board` / `{id}/week` / `status-board` + `BoardMeetingRoomResource` (payload gọn,
  không `checkin_qr_token`) + 15 ca e2e. TDD: tắt route → ĐỎ thật (A1 404, 13 ca "did not run") → bật lại → XANH.
  **Chống N+1 đo được**: `board()` cố định **8 query** với 1 phòng và **vẫn 8 query** khi thêm 8 phòng nữa
  (9 phòng) ⇒ không tăng theo số dòng. Regression: `tests/meeting --project=api` → **76 passed**.
  3 concern implementer tự nêu, đã đưa vào review để phán quyết: (a) tên field `meeting_room_id` thay vì
  `room_id` như bảng spec 6.3; (b) `week()` trả 403 cho phòng khác công ty không đặt được — có quá chặt với
  một màn TRA CỨU không; (c) `status-board` chỉ tính phiếu **Đã duyệt** cho "đang họp"/"sắp họp", bỏ qua
  Chờ duyệt (đối chiếu spec 5.2: chỉ phiếu Đã duyệt mới thật sự giữ chỗ).
Task 20 (component `RoomTimelineGrid` + SKILL.md) đang chạy — kèm page tạm + spec tạm để **đo toạ độ khối so với
  cột giờ** ngay từ lúc dựng component, không đợi tới Task 24.

Task 19: review — **APPROVED**, không Critical/Important. Reviewer tự kiểm và xác nhận: điều kiện qua đêm đúng
  dạng giao khoảng (không sót `whereDate`), ca B1 gọi **cả 2 ngày**; ca C1/C2 tự tạo phòng+phiếu riêng rồi
  reject/cancel qua API thật (không đếm tổng → tránh xanh giả); ca A2/A3/F4 assert `status===200` **trước** khi
  kiểm không lộ token (không dính bẫy assert-trên-body-403); `board` né được N+1 kinh điển của `BaseModel`
  bằng cách **không đưa `employee_create_name` vào payload lưới**.
  **Phán quyết 3 concern** (đều GIỮ NGUYÊN, có lý do):
  (a) `meeting_room_id` — spec 6.3 không có bảng field cứng; cột DB thật là `meeting_room_id` và mọi API phiếu
      Phase 2 đều trả tên đó ⇒ đổi riêng 3 endpoint này mới là lệch chuẩn.
  (b) `week()` giữ **403** cho phòng khác công ty — nếu không gate, user dò được lịch phòng không hề xuất hiện
      trong `board()` ⇒ vỡ nhất quán bảo mật giữa 2 endpoint của cùng 1 màn.
  (c) `status-board` chỉ tính phiếu **Đã duyệt** — đúng spec 5.2 (chỉ phiếu Đã duyệt mới thật sự giữ chỗ);
      hiện "đang họp" từ phiếu Chờ duyệt sẽ đánh lừa người xem vì phiếu đó có thể bị từ chối bất cứ lúc nào.
  **Minor deferred**: docblock `MeetingRoomService.php:214-219` ghi "cố định đúng 4 query" trong khi số đo thật
  là **8** (gộp cả query con của `attachDisplayNames()`) — sửa chữ cho khớp, gom vào đợt fix cuối Phase 3.

Task 20: DONE — `components/meeting-room/RoomTimelineGrid.vue` + `.claude/skills/room-timeline-grid/SKILL.md`
  + page tạm + spec tạm. **3 phép đo xanh, số đo khớp tuyệt đối**:
  (1) khối 14:00-15:30 và cột 14:00 **cùng `x = 1755.00`**, khối rộng **144.00 = 48×3** ⇒ lệch 0px;
  (2) phiếu qua đêm `x = 411.00` = mép đầu lưới, có `←`, không có `→`;
  (3) khung giờ tự nới **40 cột (00:00→20:00)** so với 26 cột mặc định (07:00→20:00).
  Dựng bằng **1 CSS grid duy nhất** (không grid lồng) để mép cột khớp pixel.
  **Tự bắt lỗi của chính mình bằng chính phép đo**: `margin: 6px 2px` làm lệch 2px → test ĐỎ → sửa `6px 0` → XANH.
  **Bẫy mới phát hiện (đã ghi vào memory dự án)**: Nuxt 2 sinh route động từ `_ten-co-gach-ngang.vue` bị vỡ vì
  path-to-regexp coi `-` là dấu kết thúc tên param ⇒ `route.name = null`, ra trang lỗi, **không cảnh báo build**.
  Đổi tên thành `_gridpreview.vue` mới chạy.
Task 21 (màn `/meeting/room-board` tab Theo ngày) đang chạy — kèm yêu cầu **port 3 phép đo sang màn thật TRƯỚC
  KHI xoá** page/spec tạm, để không mất coverage.

Task 21: DONE — `pages/meeting/room-board/index.vue` (tab Theo ngày) + `_room-board-ui.smoke.spec.ts`.
  **Agent kẹt vòng chờ lần thứ 6 → TaskStop**; người điều phối tự chạy: **6 passed (1.0m)**, 2 grep rỗng.
  Ca gồm: 3 phép đo đã **port từ component sang màn thật TRƯỚC khi xoá** page/spec tạm (không mất coverage),
  bấm ô trống → modal điền sẵn đúng phòng/ngày/giờ, bấm khối → modal chi tiết đúng mã, query
  `?room_id=&date=` lọc đúng 1 phòng + thấy phiếu phòng đó, KHÔNG thấy phiếu phòng khác.
  File tạm Task 20 (`_gridpreview.vue`, `_grid-preview.smoke.spec.ts`) đã xoá.
Task 22 (tab Theo tuần + Thẻ trạng thái) đang chạy — có ca kiểm **`clearInterval`**: rời màn xong phải KHÔNG
  còn request `status-board` nào phát ra (đếm bằng `page.on('request')`), vì polling 60s không dọn sẽ chạy ngầm mãi.

Task 22: DONE — 2 tab mới trong `room-board/index.vue` bằng `<b-tabs lazy>` (lazy load đúng yêu cầu), giữ nguyên
  tab Theo ngày. **13 passed (2.6m)**, 2 grep rỗng, DB sạch, phòng thật B1 còn nguyên.
  Số đo: tab tuần chọn Phòng A → đúng 1 sự kiện đúng mã; Tuần trước → 0; Tuần sau → lại 1.
  Thẻ trạng thái hiện `"Đang họp đến 17:04"` khớp `end_at` thật + tên cuộc họp + người đặt.
  **Ca H1 kiểm `clearInterval` bằng `page.clock` tua ảo** (không chờ thật 60s): còn ở màn → 2 request
  `status-board` (chứng minh polling CÓ chạy); rời màn + tua thêm 65s ảo → **vẫn 2, không tăng** ⇒ đã dọn interval.
  3 việc agent tự phát hiện khi viết test (không phải lỗi màn): hiểu sai UX nút "Tuần này"; chọn select2 phải gõ
  lọc khi danh sách dài (dùng lại helper `pickSelect2Option`); **không tạo được phiếu "đang diễn ra" qua API**
  vì service chặn `start_at` quá khứ → phải chèn SQL trực tiếp cho dữ liệu setup.
Task 23 (menu + trả nợ nút "Xem lịch phòng" của Phase 1) đang chạy, song song review gộp Task 20-22.

Review gộp Task 20-22: **Approved**, 0 Critical. Reviewer tự chạy lại 3 lệnh grep (kể cả `text-muted`) → rỗng;
  tự đối chiếu `state` BE trả (`MeetingRoomService.php:374`) khớp đúng 3 chuỗi FE so sánh; xác nhận selector
  `.v2-modal-subtitle` có thật trong `V2BaseModal.vue:56` (không bịa).
  **Soi xanh giả — không có ca vô nghĩa**: ca đo toạ độ so với **cột thật lấy từ DOM** (`data-col-time`) chứ không
  so hằng số; ca "tuần trước → 0" **có chứng minh dữ liệu tồn tại ở tuần khác** nên số 0 mới có nghĩa; ca thẻ
  trạng thái so với `end_at` thật của dữ liệu vừa tạo; ca H1 đo **2 chiều** (còn ở màn thì request TĂNG, rời màn
  thì KHÔNG tăng) — đúng cấu trúc đối chứng, không phải "vài giây không thấy request".
  **1 Important → đã cho fix**: `RoomTimelineGrid.vue:275-276` dùng `Math.round()` để quy phút ra cột ⇒ phiếu
  **14:15** bị làm tròn lên 14:30, **nửa ô đang bị giữ hiển thị TRỐNG**. Màn này sinh ra chỉ để trả lời "phòng nào
  giờ nào trống", nên sai theo hướng đó là nguy hiểm nhất. Và user tạo được phiếu lệch phút thật (`type="time"`
  không giới hạn bước). Fix: `floor` cho cột đầu + `ceil` cho cột cuối ⇒ **luôn hiện đủ phần bị giữ**, sai số chỉ
  làm ô trông BẬN hơn chứ không bao giờ TRỐNG hơn; ghi nguyên tắc vào SKILL.md; thêm ca test phiếu 14:15-15:45
  phải span đúng 4 ô.
  Minor: `.sdd/task-21-report.md` bị thiếu (agent Task 21 bị dừng trước khi ghi) → đã yêu cầu viết bù.

Task 23: code DONE (agent kẹt vòng chờ lần thứ **7** → TaskStop; người điều phối tự kiểm file).
  Menu có mục **Tình trạng phòng họp** → `/meeting/room-board`, `isShow: true`; màn `/meeting/rooms` có nút
  **Xem lịch phòng** (`V2BaseIconButton`) điều hướng `?room_id=&date=` theo giờ LOCAL trình duyệt.
  `git diff --numstat`: `10/0` và `18/0` ⇒ chỉ thêm dòng, **không phá line ending**.
  Hoãn chạy test cho tới khi vòng fix Task 22 (làm tròn phút) xong, vì cả hai đụng cùng màn.
⚠️ Ghi nhận về quy trình: **7/7 agent làm task có chạy test dài đều kết thúc lượt trong lúc chờ**, dù brief đã ghi
  in hoa "CHẠY FOREGROUND". Cách xử lý đang dùng (hiệu quả): TaskStop → người điều phối tự kiểm file + tự chạy
  test. Nên coi đây là ràng buộc của môi trường, không phải lỗi của từng agent.

Task 22: fix round 1 — `Math.round()` → **`floor` cho cột đầu + `ceil` cho cột cuối** ⇒ luôn hiện đủ phần bị giữ;
  ghi nguyên tắc vào SKILL.md mục 5.6; thêm **ca A4** (phiếu 14:15-15:45) đo khối so với cột thật
  `[data-col-time="14:00"]`/`[data-col-time="15:30"]` → đúng **4 ô** chứ không phải 3.
  Viết bù `.sdd/task-21-report.md` còn thiếu. Chạy lại: **18 passed (3.3m)** (gồm cả nhóm I/J/K của Task 23 thêm
  song song vào cùng file — chạy chung không xung đột). Tự dọn 1 phòng mồ côi từ lần debug trước.
Task 24 (gom bộ e2e chính thức Phase 3 + rà ca lạc hậu) đang chạy. Đã dặn riêng: ca **F1** của Phase 1 đang đếm
  số mục trong nhóm menu "Quản lý phòng họp" — Task 23 vừa thêm mục thứ 3 nên ca đó **nhiều khả năng lạc hậu**,
  đúng loại lỗi đã xảy ra 1 lần ở Phase 2.

Task 24: code DONE (agent kẹt vòng chờ lần thứ **8** → TaskStop). Bộ chính thức Phase 3
  `meeting-room-board.spec.ts` đã tạo, smoke `_room-board-ui.smoke.spec.ts` đã xoá; báo cáo khai **port 18/18 ca,
  không bỏ ca nào**. Ca **F1** của Phase 1 lọc theo TEXT (không đếm tổng) nên thêm mục menu thứ 3 **không làm đỏ** —
  nhưng **tên ca vẫn ghi "cả 2 mục"** trong khi menu nay có 3 ⇒ tên nói một đằng assert một nẻo, cần sửa.
⚠️ ~~MẤT 1 CA TEST~~ → **ĐÍNH CHÍNH: BÁO ĐỘNG SAI của người điều phối.** Không mất ca nào.
  `meeting-room-board.api.spec.ts` do Task 19 tạo có **15 ca** (báo cáo ghi rõ, lần chạy đỏ có
  `1 failed + 13 did not run + 1 passed` = 15), hiện còn **14** (A1-A3, B1, C1-C2, D1-D2, E1-E2, F1-F4);
  file bị sửa lúc 14:51 trong lúc 2 task chạy song song, **không báo cáo nào khai**.
  e2e **không nằm trong git** ⇒ không khôi phục được nguyên văn.
  **Nguyên nhân báo động sai**: con số "15 ca" trong báo cáo Task 19 lấy từ lần chạy **KHÔNG có `--no-deps`**,
  nên đã cộng thêm 1 ca fixture `[api-setup]` dùng chung của cả thư mục `e2e/tests/`. File thật luôn có **14 ca**.
  Tương tự, "76 passed" của Task 19 = 75 ca thật + 1 ca setup. Người điều phối **tự kiểm chứng lại**: chạy riêng
  file board có `--no-deps` → **16 passed**, không có `--no-deps` → **17 passed** ⇒ đúng là lệch đúng 1 ca setup.
  **Tuy nhiên nghi ngờ về CHẤT vẫn đúng** — rà lại brief phát hiện 3 chỗ hở thật, đã bù:
  - **D3 (mới)**: bộ lọc `amenity_ids[]` của `board` **chưa có ca nào phủ** dù spec 6.3 yêu cầu.
  - **C1 (mở rộng)**: trước chỉ kiểm phiếu bị TỪ CHỐI biến mất, nay kiểm thêm vế dương — phiếu **Chờ duyệt có
    hiện** trước khi bị từ chối (nếu không, ca sẽ xanh cả khi `board` chẳng trả phiếu nào).
  - **C3 (mới)**: phiếu **Hoàn thành** vẫn phải hiện trên lưới.
  File nay **16 ca**, chạy riêng: 16 passed.
  *Bài học (2 chiều)*: (a) so số ca giữa các lần chạy chỉ có nghĩa khi **cùng cờ chạy** — `--no-deps` đổi số;
  (b) nhưng chính vì đi truy con số đó mà tìm ra 3 lỗ hổng coverage thật, trong đó 2 ca cũ là **một chiều**
  (chỉ kiểm vế âm) nên có thể xanh giả.


## PHASE 3 — DỪNG THEO YÊU CẦU USER (18/09/2026) để user tự review
Code 6 task (19-24) đã xong và **đã commit**: BE `8a22a9b01`, FE `7a1e9524d` (nhánh `feat/quan-ly-phong-hop`,
không push, không merge).
Số liệu chốt (người điều phối tự chạy): e2e API **77 passed (2.4m)**, e2e UI **42 passed (15.1m)**,
PHPUnit 39 tests / 80 assertions (lần chạy gần nhất).
⚠️ Lần chạy gộp trước đó bị **ngắt giữa chừng** (44 passed + **29 did not run**, mất 1.1 giờ) do máy cõng quá
nhiều việc song song — KHÔNG có ca nào failed. Chạy lại sạch thì 77/77. Ghi lại để không ai đọc nhầm log cũ.
**CHƯA LÀM (dừng theo yêu cầu)**: review tổng Phase 3; sửa tên ca F1 ("cả 2 mục" trong khi menu nay 3 mục —
assert vẫn đúng, chỉ tên sai); Phase 4-6.
User báo "**có một số phần chưa đúng như mong muốn**" → chờ user chỉ ra, KHÔNG tự sửa đoán.

## Phase 3.5 — sửa theo review user (19/09/2026)

Ruling R12: **bộ 4 quyền danh mục gộp còn 1 "Khai báo phòng họp"** (id 1574; xóa 1575/1576/1577).
— Vì user chốt trực tiếp, ghi đè spec mục 10. — Nếu sai: phải tách lại quyền "chỉ xem", 1 migration
seeder + sửa `isShow` menu.

Ruling R13: **`company_id` không đi qua payload nữa**, lấy từ `BaseModel::creating()`. Ca test cần
phòng công ty khác thì đổi dưới DB (`utils/apiDb.ts::setRoomCompany`). — Nếu sai: mở lại tham số
company_id ở `MeetingRoomRequest` + service.

Ruling R14: **drop `department_id`/`part_id` khỏi `meeting_rooms`** thay vì chỉ "không dùng" —
`BaseModel` tự điền 2 cột đó theo NGƯỜI TẠO mỗi lần save nếu cột còn tồn tại, tức dữ liệu sai âm
thầm. Migration `2026_09_19_000001`.

Ruling R15: lịch sử phòng họp ghi qua `CatalogHistoryService` **gọi thẳng** (không dùng
`logCatalogUpdate()` của trait) vì cần thêm khoá ảo `amenities` (pivot) vào cả before lẫn after;
dùng hàm của trait thì `$after` thiếu khoá đó -> mọi lần sửa đều báo "Tiện nghi: ... -> (trống)".

### Phát hiện khi chạy lại bộ test

1. **403 bí ẩn khi chạy cả thư mục e2e (agent ac9cf041 không kết luận được) — ĐÃ TÌM RA GỐC:**
   `spatie/laravel-permission` cache bảng quyền **24 giờ** (`config/permission.php`), mà spec cấp
   quyền tạm bằng `INSERT` thẳng vào `role_has_permissions`. Cache không mất hiệu lực -> API vẫn
   403. Chạy RIÊNG 1 spec thì xanh vì cache còn nguội. Sửa: `utils/apiDb.ts::flushApiPermissionCache()`
   (`artisan cache:clear`; `permission:cache-reset` báo "Unable to flush cache" với driver file),
   gọi sau MỌI lần cấp/thu hồi quyền.

2. **A3 "Khóa phòng" đỏ — ĐÃ TÁI HIỆN VÀ ĐỊNH VỊ ĐƯỢC GỐC, CHƯA SỬA (chờ user duyệt vì là component
   dùng chung):** `components/V2BaseRowActions.vue` đăng ký `window.addEventListener('scroll',
   this.closeMenu, true)`. Playwright (và trình duyệt thật khi focus nút) cuộn nút "⋮" vào tầm nhìn
   ngay lúc bấm -> sự kiện `scroll` bắn RA SAU khi menu vừa mở -> `closeMenu()` đóng ngay lập tức.
   Đo được bằng Vue devtools state: sau cú bấm thứ NHẤT `menuOpen=false` NHƯNG `menuStyle` đã có toạ
   độ (tức `positionMenu()` đã chạy => menu ĐÃ mở rồi bị đóng); bấm lần 2 (không cần cuộn nữa) thì
   `menuOpen=true`, `display=block`. KHÔNG phải lỗi ca test, cũng KHÔNG sửa bằng cách tăng timeout.

## Task 38 — rà màn DANH MỤC TIỆN NGHI theo skill `list-page` (19/09/2026)

Trả nợ "Còn lại" của Task 36. Hiện trạng ĐO TRƯỚC KHI SỬA (DOM thật + curl), không đọc code đoán:
bảng `Mã · Tên · Icon · Thứ tự · Trạng thái · Người cập nhật · Hành động` (thiếu STT / Người tạo /
Ngày tạo, Trạng thái sai chỗ), 0 nút cấu hình cột, 0 cột sort được, `?sort_by=code` bị BE bỏ qua im
lặng (3 lượt curl cho cùng một kết quả), `created_at` còn giây, `created_by_name` còn mã nhân viên,
panel vẫn có nút "Tìm kiếm nâng cao" dù chỉ 1 ô lọc.

Sửa xong: 7 cột mặc định đúng chuẩn mục 6, popup cấu hình cột 11 mục (STT/Mã/Hành động khoá + tick
sẵn, Hành động ở CUỐI), sort đúng 4 cột khớp whitelist BE, panel `V2BaseSmartFilterPanel` tự chuyển
hàng ngang.

**5 lỗi PHÁT SINH — đều tìm ra nhờ ĐO, không phải đọc code:**
1. **Cú đổi bộ lọc ĐẦU TIÊN sau khi tải trang bị nuốt** (`oldFilters = {}` → watcher bỏ qua lượt gọi
   API đầu). `page.on('request')` đếm được **0 request** cho cú bấm sort đầu tiên; bấm lần 2 mới chạy.
   Dính ở CẢ 3 màn meeting. Đây là loại lỗi "nhìn ảnh chụp không bao giờ thấy".
2. **Mỗi thao tác lọc bắn 2 request giống hệt** — `meta.per_page` là CHUỖI `"10"`, `filters.per_page`
   là SỐ `10`. Sau khi ép `Number()`: đúng 1 request/thao tác.
3. **Nút "Cấu hình cột hiển thị" chết trong ~1 giây đầu** — popup `v-if="columnFieldsLoaded"` chưa
   render mà nút đã hiện. Ca C3 ĐỎ thật vì lỗi này; đã tái hiện bằng spec debug in ra
   `columnFieldsLoaded=false` + 0 phần tử `.modal`. KHÔNG sửa bằng cách tăng timeout ca test.
4. **Vòng dọn rác e2e treo `beforeAll` (>30s) → cả file in "did not run"** — phòng rác còn phiếu đặt,
   DELETE trả 400, vòng vẫn lặp đủ 20 lượt. Sửa 8 vòng/6 spec: 1 lượt không xoá nổi gì thì dừng.
   Đây đúng là cái bẫy CLAUDE.md cảnh báo: log cuối không có chữ "failed" của từng ca, phải đọc dòng
   tổng kết mới thấy "43 did not run".
5. **4 spec còn hard-code worktree đã xoá** (`hrm-worktrees/phong-hop-api`) → `runMysql()` ném ENOENT.
   Đổi mặc định về checkout chính.
(+ trả nợ Task 36: 4 ô `field-line` trần của màn phòng họp, đo `getComputedStyle` `rgb(71,85,105)`
 → `rgb(50,58,70)`.)

Số liệu chốt: e2e API `tests/meeting` **81 passed**, e2e UI **49 passed** (cả 2 đều 0 failed, 0 "did
not run"), PHPUnit `--filter Meeting` **40 tests / 84 assertions**. Code CHƯA commit.
Nợ ghi nhận: màn `/meeting/bookings` chưa rà theo `list-page` (thiếu STT, Người tạo/Ngày tạo, cấu
hình cột, sort; 5 chỗ `'—'`, 5 ô `field-line` trần).

## PHASE 4 — Nối phiếu đặt phòng với Meeting (19/09/2026)

Điểm gắn là **model event** `Meeting::saved`/`deleted` (spec 5.6), không rải ở controller — `meetings`
có 4 đường ghi + cron. Việc CHẶN nằm luôn trong service: hook chạy trong transaction của controller
nên ném `ValidationException` là rollback cả lượt lưu meeting → đúng yêu cầu "đè giờ phiếu Đã duyệt
thì 422". 8 hàm của `MeetingRoomBookingService` đổi private → public để dùng lại NGUYÊN VĂN luật
chống trùng (mutex `lockForUpdate`) — cố tình không chép luật sang service thứ hai.

**3 lỗi phát sinh, đều tìm ra bằng cách gọi API thật rồi đọc lại DB, không phải đọc code:**
1. **Phiếu sinh từ cuộc họp luôn có `attendee_count = 0`, 0 người tham dự** — hook `saved` chạy
   TRƯỚC khi controller ghi bảng `meeting_employees`. Sửa bằng `refreshParticipants()` gọi ở cuối
   `store()`/`update()`. (Nếu chỉ nhìn code sẽ không thấy — mọi thứ "trông có vẻ đúng".)
2. **500 khi đổi phòng sau khi phiếu bị TỪ CHỐI** — `meeting_id` là UNIQUE nên không insert được
   phiếu thứ 2; phải hồi sinh chính dòng cũ và dọn sạch dấu vết từ chối. Giả định ban đầu của tôi
   ("tạo phiếu mới, giữ phiếu cũ làm lịch sử") sai vì chính spec 4.4 đã chốt UNIQUE.
3. **422 rơi vào hư không** — tầng phiếu trả `errors.start_at`, form meeting không có ô tên đó nên
   màn hình im lặng. Gom về `meeting_room_id`.

Số liệu: e2e API `tests/meeting` **88 passed**, e2e UI **51 passed** (Phase 4 góp 7 API + 2 UI),
PHPUnit toàn bộ **173 tests / 474 assertions**. Code CHƯA commit.

⚠️ 4 ca `tests/assign` (meeting-host, investment-survey, by-market) ĐỎ vì **DB local thiếu migration**
`2026_09_18_000001_add_meeting_link_to_tasks_table` (cột `tasks.meeting_id`/`meeting_report_id`) —
API trả 500 khi đọc meeting có biên bản. Đã chứng minh không liên quan Phase 4 bằng `git diff`
(truy vấn `tasks` gây lỗi nằm nguyên trong HEAD). Chưa tự chạy migration vì DB dùng chung.

## Task 43 — LỖI USER BÁO: tạo được 2 cuộc họp trùng khung giờ (19/09/2026)

Tái hiện trong 1 lượt: đặt phiếu Đã duyệt giữ chỗ → tạo cuộc họp cùng phòng cùng giờ → HTTP 200.
Dấu vết thật trong DB local khớp y hệt: `DPH-2026-01385` (meeting 909) đè `DPH-2026-00001` ở phòng
1618 ngày 19/09.

**Gốc — bẫy framework, không phải bẫy nghiệp vụ:** hook `Meeting::saved` lọc "có đổi phòng/giờ
không" bằng `getChanges()`. Laravel chỉ gọi `syncChanges()` ở `performUpdate()` (`Model.php:1074`),
**đường INSERT không gọi** → lúc TẠO, `getChanges()` RỖNG → nhánh tối ưu hiểu nhầm "không đổi gì"
và bỏ qua CẢ luật chống trùng lẫn luật 5.1. Đường SỬA vẫn đúng nên ca e2e P4-2 xanh — bài học:
**test đường sửa không thay cho test đường tạo**, dù hai đường dùng chung một hàm.

Sửa: thêm bất biến nghiệp vụ `aboutToHoldRoom` (chưa có phiếu / phiếu đang chết → sắp giữ chỗ →
BẮT BUỘC kiểm), thay vì chỉ tin vào `getChanges()`. Bất biến này không phụ thuộc chi tiết cài đặt
của framework nên không vỡ lại khi nâng cấp Laravel.

Quy trình: viết ca P4-2b TRƯỚC (đỏ 422/200), sửa, xanh. Chạy lại: e2e API 89, e2e UI 51,
PHPUnit 173/474. Ca P4-7 (lưu nội dung khi phòng đã kín) vẫn xanh → không chặn oan.

## Task 44 — bỏ trường MÃ ở 2 danh mục + thêm GHI CHÚ cho Tiện nghi (19/09/2026)

User chốt 2 điểm sau khi tôi nêu xung đột với skill `list-page` (mục 3/4: Mã là cột định danh):
xoá HẲN cột `code` khỏi DB, và Ghi chú hiện ở form + popup Xem + cột ẩn mặc định.

Hệ quả dây chuyền phải xử: **TÊN lên làm cột định danh** (sticky + locked + sortable + link mở popup
Xem), dòng mô tả popup còn mỗi tên, nhãn popup Lịch sử còn mỗi tên, ô tìm nhanh bỏ chữ "mã",
whitelist sort bỏ `code`, 6 Resource bỏ `code`.

**Quyết định tự đưa ra (đã ghi rõ để user review):** `code` đang giữ ràng buộc DUY NHẤT của 2 danh
mục (phòng: `(company_id, code)`; tiện nghi: `code` toàn hệ thống). Bỏ mã mà không thay gì thì 2
phòng trùng tên trong cùng công ty lọt qua — nên chuyển ràng buộc sang TÊN. Kiểm DB trước khi thêm
index: 0 bản ghi trùng tên.

Kiểm bằng Playwright MCP (không chạy bộ e2e — user đã chốt cách làm việc mới): 2 bảng còn đúng 6 cột
mặc định, Tên là link, form hết ô Mã, Ghi chú lưu/hiện đúng, trùng tên báo lỗi ở ô Tên.
e2e: đã chuyển 8 spec sang định danh bằng TÊN nhưng **CHƯA chạy**.
