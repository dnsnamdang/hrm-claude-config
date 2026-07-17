# elearning-hall-of-fame — Plan

- **Người phụ trách**: @junfoke
- **Design**: `.plans/elearning-hall-of-fame/design.md` | Spec: `docs/superpowers/specs/2026-07-16-elearning-hall-of-fame-design.md`
- **Plan chi tiết**: `docs/superpowers/plans/2026-07-16-elearning-hall-of-fame.md`

## Phase 1 — BE: bảng cấu hình + quyền

- [x] Migration 2 bảng `elearning_hall_of_fame_badges` + `elearning_hall_of_fame_settings` (`Modules/Elearning/.../2026_07_16_100000`) — ⏳ chờ user chạy
- [x] Entity `HallOfFameBadge` (hằng `METRICS` 7 tiêu chí + `METRIC_COMPOSITE`)
- [x] Entity `HallOfFameSetting` (hằng `PERIODS` + `current()` + `periodRange()` + `periodLabel()`)
- [x] Seeder `HallOfFameSeeder` — 4 danh hiệu mặc định (`firstOrCreate` theo name) + 1 dòng settings — ⏳ chờ user chạy
- [x] Quyền mới ID 1082 `Quản lý vinh danh học viên` trong `PermissionsTableSeeder` (verify không trùng ID)

## Phase 2 — BE: HallOfFameService + API trang chủ

- [x] `HallOfFameService::build()` — 6 query xếp hạng + composite + khử trùng theo `sort_order` + tra tên/avatar/phòng ban
- [x] Hằng `MIN_ON_TIME_ITEMS = 3` (chống 1/1 = 100% thắng 19/20 = 95%), `LESSON_DONE = 2` ≠ `ENROLLMENT_DONE = 3`
- [x] `PublicBrowseController::hallOfFame()` + route `GET v1/elearning/public/hall-of-fame` (không cần auth optional — thẻ không hiện tên khoá)

## Phase 3 — BE: CRUD cấu hình

- [x] `Modules/Training/Http/Controllers/V1/HallOfFameController.php` — index/show/store/delete/toggle/updateSetting (đặt ở Training theo tiền lệ `ExternalUserController`)
- [x] Validate: name unique, metric in 7 giá trị, top_n 1..20, `min_criteria` bắt buộc khi composite, **chặn badge composite thứ 2**
- [x] Format lỗi 422 `['error_messages' => ...]` đúng thứ `ApiErrorHandler.js` đọc
- [x] Route group `/v1/training/hall_of_fame` — mọi route gắn `checkPermission:Quản lý vinh danh học viên`; `/settings` khai trước `/{id}`

## Phase 4 — FE hrm-client: màn cấu hình

- [x] `pages/training/hall_of_fame/index.vue` — ô Kỳ tính + toggle Hiện khối + bảng danh hiệu (sửa/bật-tắt/xoá) + gate quyền
- [x] **FIX (user báo mất menu)**: thiếu `layout: 'default-sidebar'` → rơi về layout `default` nên không có sidebar trái. Mọi màn Đào tạo khác (vd `training_types/index.vue:302`) đều khai layout này. Verify Playwright: sidebar hiện, menu "Vinh danh học viên" có trong cây.

## Phase 4b — Kéo thả sắp thứ tự (user phản hồi 2026-07-16)

> User: *"thứ tự hiển thị, nhập trùng vẫn được này. trước phân loại đào tạo xử lý kéo thả để sắp xếp thứ tự hiển thị ở homepage tôi thấy có vẻ áp dụng được đấy"*.
> Đúng — ô `sort_order` gõ tay cho nhập trùng, mà `sort_order` gánh 2 vai: thứ tự hiện **và** thứ tự ưu tiên khử trùng người.
> Trùng số → luật khử trùng rơi về `id` → ai mang danh hiệu nào thành tuỳ tiện.

- [x] `HallOfFameBadge::scopeOrderByHomePosition()` — mirror `TrainingType`: `CASE WHEN sort_order = 0 THEN 1 ELSE 0 END` rồi `sort_order`, `name`. **Bẫy code cũ đã tránh sẵn**: sort_order=0 là "chưa đặt", order thẳng sẽ đẩy mục chưa đặt lên trước hạng 1
- [x] `HallOfFameController::updateSortOrder(ids[])` — reset hết về 0 rồi gán `position + 1` theo thứ tự mảng → **không thể trùng**; validate `distinct` + `exists`
- [x] Route `POST /v1/training/hall_of_fame/sort-order` (khai TRƯỚC `/{id}`)
- [x] `HallOfFameService::build()` + `index()` dùng `orderByHomePosition()`
- [x] `store()`: bỏ hẳn `sort_order` khỏi validate + attributes — sửa danh hiệu không đụng hạng đã sắp; tạo mới → `sort_order = 0` (xuống cuối)
- [x] `components/modal/sort_hall_of_fame_modal.vue` — **1 vùng kéo thả** (KHÁC màn Loại đào tạo dùng 2 vùng Hiện/Không hiện: bảng vàng đã có nút Bật/Tắt riêng, thêm vùng "Không hiện" là 2 cách làm cùng 1 việc). Danh hiệu đang tắt vẫn kéo được, có nhãn "Đã tắt". Dùng action generic `apiPostMethod` sẵn có, không thêm action mới
- [x] `add_hall_of_fame_badge_modal.vue` — bỏ ô "Thứ tự hiển thị"
- [x] **FIX layout modal (user phản hồi)**: bỏ ô "Thứ tự hiển thị" (vốn `col-lg-6` đứng cạnh "Lấy top") làm "Lấy top" trơ nửa hàng, còn "Số tiêu chí tối thiểu" vẫn `col-lg-12` nên rơi xuống dòng riêng → đổi thành `col-lg-6`. Verify Playwright: 2 ô cùng `top=396`, mỗi ô 372px, nằm cạnh nhau.
- [x] `index.vue` — nút "Sắp xếp thứ tự" + gắn modal
- [x] **Verify Playwright E2E**: mở modal → 4 thẻ đúng thứ tự → kéo "Tiến độ nổi bật" từ vị trí 4 lên 1 → Lưu → `POST sort-order` 200 → **DB đổi đúng theo thứ tự kéo**, hạng liên tục 1-4, query check trùng → không có hạng trùng. Đã trả lại thứ tự seed ban đầu sau khi test.

> ⚠️ Bài học verify: SortableJS **di chuyển DOM ngay khi kéo**, nhưng `v-model` chỉ cập nhật khi sự kiện `end` bắn. Cú kéo đầu bị Playwright timeout → nhìn DOM thấy đã đổi chỗ nên suýt kết luận nhầm "kéo thành công" trong khi save chưa hề chạy (không có request `sort-order` nào). **Phải nhìn network + DB, đừng tin DOM.**
- [x] `components/modal/add_hall_of_fame_badge_modal.vue` — ô "Số tiêu chí tối thiểu" chỉ hiện khi tiêu chí = Gương mặt tiêu biểu; lỗi inline `is-invalid` + `touched`
- [x] `store/actions.js` — thêm `addHallOfFameBadge` + `updateHallOfFameSetting` (theo mẫu `addTrainingType`)
- [x] `components/menu-sidebar.js` — subItem "Vinh danh học viên" (id 14, gate quyền mới)

## Phase 5 — FE elearning: nối API + dọn mock cuối cùng

- [x] `stores/elearning.js` — `fetchHallOfFame()` + state `hallOfFamePeriodLabel`, thêm vào `Promise.allSettled`
- [x] `components/home/HallOfFame.vue` — nhãn kỳ động, bỏ click demo + `cursor-pointer`, marquee tĩnh khi ≤3 thẻ
- [x] `views/home/HomeView.vue` — `v-if="store.hallOfFame.length"` (rỗng hoặc admin tắt → ẩn khối)
- [x] **Xoá hẳn `src/constants/mockData.js`** (291 dòng) — sau feature này không còn ai import; trang chủ elearning **hết sạch mock**

> ⚠️ **Tồn cần PR (chưa làm — tài sản chung, không tự sửa):** `elearning/CLAUDE.md` + `.claude/skills/elearning-page/SKILL.md` vẫn trỏ `src/constants/mockData.js` như nơi để mock data, trong khi file đã bị xoá. Cần PR cập nhật 2 tài liệu này.

## Phase 2b — FIX BUG: cắt top_n quá sớm (user báo "loạn", 2026-07-16)

> User: *"cách thức sắp xếp thứ tự và lấy top đang khá loạn, chỉ kéo thả thứ tự là bên vinh danh nó đã vinh danh danh hiệu khác"*.
> Điều tra bằng dữ liệu thật → **lỗi implement sai spec**: `leaderboard()` cắt `top_n` TRƯỚC khử trùng.
> Composite lấy `e:13` + `e:1100`; bảng "Top học tập tháng" và "Chất lượng bài thi" chỉ có đúng 2 người đó
> → cạn ứng viên → **2 danh hiệu biến mất**. Spec quyết định #6 ghi rõ "nhường suất cho người kế tiếp" — code không làm.

- [x] `leaderboard()` trả bảng **đầy đủ**, bỏ `array_slice`
- [x] Thêm `topSlice($board, $topN)` — chỉ dùng cho định nghĩa "lọt top" của composite (bước 2)
- [x] Bước 2 đếm `appearances` trên `topSlice` từng badge (trước: đếm trên bảng đã cắt sẵn — vô tình đúng, nhưng giờ tường minh)
- [x] Bước 3 duyệt bảng đầy đủ, bỏ `seen`, lấy tiếp tới khi đủ `top_n`
- [x] Cập nhật spec §5.1 + thêm §5.4 giải thích bug
- [x] **Verify DB thật**: trước fix 3 thẻ (2 thẻ trùng danh hiệu "Gương mặt tiêu biểu", 2 danh hiệu vắng); sau fix **4 thẻ**, "Tiến độ nổi bật" nhường suất xuống Đào Thị Thúy + Akira Lee, mỗi người vẫn đúng 1 thẻ
- [x] Chứng minh 2 danh hiệu vẫn vắng là do **cạn ứng viên thật**: "Top học tập tháng" + "Chất lượng bài thi" mỗi bảng chỉ có 2 ứng viên trong toàn hệ thống (`e:13`, `e:1100`) — cả 2 bị composite lấy. "Tiến độ nổi bật" có 4 ứng viên nên nhường được. → Dữ liệu test 3 người, không phải logic sai.

> **User chốt hướng A** (2026-07-16): giữ khử trùng "mỗi người 1 thẻ". Lý do: với hàng trăm người học, A cho ~11-12 gương mặt KHÁC NHAU được vinh danh; còn bỏ khử trùng (B) thì "số khoá hoàn thành" và "số bài học hoàn thành" tương quan mạnh → top trùng nhau → marquee lặp vài gương mặt.

## Verify

- [x] `php -l` 10 file BE — sạch; ID quyền 1082 xuất hiện đúng 1 lần
- [x] ESLint + `vite build` elearning (Node 24) — sạch, xoá mockData.js không vỡ build
- [x] Hàm thuần: `initials()` (NA/AL/M), `sortDesc()` (bằng điểm → owner_key tăng dần), `periodLabel/periodRange` cả 5 kỳ
- [x] **6 query xếp hạng chạy trên DB thật**: subject_completed 4 người, path_completed 1, certificate_earned 1, lesson_completed 5, exam_avg_score 2 (**toàn nhân viên — xác nhận learner không có exam_score**), on_time_rate 0
- [x] Composite: min_criteria=2 → 4 người, =3 → 3 người, =99 → 0 người (không lỗi)
- [x] `attachPeople`: 6 item vào → 5 thẻ ra (NV không tồn tại bị loại); learner → dept "Học viên ngoài"; nhân viên → tên phòng ban thật
- [x] Học viên ngoài "Akira Lee" (`l:5`) dẫn đầu 4/6 bảng → quyết định #8 (cho learner lên bảng) có tác dụng thật
- [ ] ⚠️ **`on_time_rate` CHƯA verify được bằng dữ liệu thật**: cả DB chỉ có 3 enrollment gắn `due_date` và không cái nào DONE → query chạy không lỗi nhưng trả rỗng. Luật ngưỡng `>= 3` mới chỉ được review code, chưa chạy thật.
- [x] User đã chạy migrate + seed + PermissionsTableSeeder (verify: 2 bảng CÓ, 4 badge, 1 setting, quyền id=1082 CÓ)
- [x] `HallOfFameController::index()` gọi thẳng qua tinker → 200, 4 badge / 5 kỳ / 7 tiêu chí
- [x] **Verify UI Playwright màn `/training/hall_of_fame`**: sidebar hiện, menu có, Kỳ tính = "30 ngày gần nhất", bảng đủ 4 danh hiệu đúng cột (composite hiện min_criteria=2, badge thường hiện "-"), API GET trả 200
- [x] 2 lỗi console `computed property "fields" already defined` — **có sẵn toàn app, KHÔNG phải do feature này**: màn `training_types` (code cũ) báo y hệt. Đã đối chứng, không sửa.
- [ ] ⏳ Verify UI trang chủ elearning (khối vinh danh hiện thẻ thật + nhãn kỳ)
- [ ] ⏳ E2E màn cấu hình: thêm/sửa/tắt/xoá danh hiệu, đổi kỳ, chặn composite thứ 2 (422)

---

### Checkpoint — 2026-07-16

Vừa hoàn thành: CODE DONE 5 phase (14 file: migration, 2 entity, seeder, permission, service, controller+route elearning, controller+route training, 2 file hrm-client + actions + menu, 3 file elearning, xoá mockData.js). Verify tĩnh sạch (php -l, eslint, vite build). Verify động qua tinker: 6 query xếp hạng + composite + attachPeople chạy đúng trên DB thật.
Đang làm dở: Không.
Bước tiếp theo: User chạy `cd hrm-api && php artisan migrate` → `db:seed --class="Modules\Elearning\Database\Seeders\HallOfFameSeeder"` → chạy lại `PermissionsTableSeeder` (đúng quy trình team: seeder truncate rồi insert lại theo ID cố định — xem memory feedback_permission_seeder_rerun) → gán quyền cho tài khoản → mở `/training/hall_of_fame` + trang chủ elearning.
Blocked: `build()` end-to-end + màn cấu hình chưa chạy được cho tới khi migrate (thiếu 2 bảng) — đúng dự kiến.
