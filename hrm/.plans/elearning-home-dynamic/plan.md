# elearning-home-dynamic — Plan

- **Người phụ trách**: @junfoke
- **Design**: `.plans/elearning-home-dynamic/design.md` | Spec: `docs/superpowers/specs/2026-07-15-elearning-home-dynamic-design.md`
- **Plan chi tiết**: `docs/superpowers/plans/2026-07-15-elearning-home-dynamic.md`

## Phase 1 — BE: Hoạt động gần đây

- [x] Migration index `enrolled_at`/`completed_at` cho `subject_enrollments` + `learning_path_enrollments` (`Modules/Elearning/.../2026_07_15_100000`) — ⏳ chờ user chạy
- [x] `Modules/Elearning/Services/HomeActivityService.php` — 4 query, 3 loại event, 15 dòng/30 ngày/tối đa 2 mỗi người
- [x] `PublicBrowseController::recentActivities()` + route `GET v1/elearning/public/recent-activities`

## Phase 2 — BE: Danh mục (training_types + icon)

- [x] Migration `icon` + `sort_order` cho `training_types` (`Modules/Training/.../2026_07_15_100001`) — ⏳ chờ user chạy
- [x] `Modules/Elearning/Services/HomeCategoryService.php` — đếm subject + learning_path theo `training_type_id`, 2 query group (không N+1)
- [x] `PublicBrowseController::categories()` + route `GET v1/elearning/public/categories`
- [x] `TrainingType::$fillable` thêm `icon`, `sort_order` (bảng này dùng fillable tường minh — không thêm là mất dữ liệu ngầm)
- [x] `TrainingTypeController::store()` validate `icon`/`sort_order` cả 2 nhánh create/update
- [x] `TrainingTypeListResource` trả thêm `icon`, `sort_order`

## Phase 3 — FE hrm-client: chọn icon Loại đào tạo

- [x] `constants/trainingTypeIcons.js` — 20 icon Remix + `DEFAULT_TRAINING_TYPE_ICON`
- [x] ~~ô "Icon hiển thị" dùng native `<select>`~~ → **làm lại**, xem Phase 3b
- [x] `pages/training/training_types/index.vue` — cột "Icon" (slot riêng theo pattern `cell(status)` sẵn có)

## Phase 3b — Làm lại picker icon cho trực quan (2026-07-15)

> User phản hồi: native `<select>` chỉ render được text → phải "đoán mò icon dựa vào văn bản".
> Đúng — thẻ `<option>` không render được `<i class="ri-*">`, nên spec ban đầu ("Select2 có preview") không khả thi bằng select thường.
> User chọn phương án **nút mở bảng icon (popover)** trong 3 phương án đưa ra.

- [x] `components/modal/add_training_type_modal.vue` — thay `<select>` bằng icon picker popover:
  - Control kiểu `form-control`: preview icon thật + tên + nút `x` Bỏ chọn / caret — theo idiom `SearchPicker.vue` sẵn có (không tự nghĩ pattern mới)
  - Panel lưới 7 cột × 3 hàng = 20 icon, click 1 phát chọn xong, panel tự đóng
  - Ô đang chọn: viền + nền xanh `#1f5ca9`
  - Hover icon → tên hiện ở dòng hint dưới lưới (**không dùng `title` native** — trễ ~1s)
  - `v-click-outside` (plugin `v-click-outside` đã có sẵn) → click ra ngoài đóng panel
  - `$set` khi gán `data.icon` (bản ghi từ API có thể chưa có key `icon` → gán thẳng mất reactive)
  - `z-index: 10` là đủ (panel nằm trong stacking context của modal, không cần portal)
- [x] Verify Playwright trên màn thật: mở panel OK (không bị modal cắt), hover → hint đúng, click → chọn đúng icon + panel đóng, mở lại → đúng 1 ô highlight, click ra ngoài → đóng, nút `x` → về "Chưa chọn icon" + preview về icon mặc định

### Phase 3c — Bỏ tên icon (user phản hồi lần 2, 2026-07-15)

> User: *"chọn icon xong miêu tả tên như này cũng không hợp lý. bởi tên loại đào tạo đặt có thể hoàn toàn không liên quan tên icon"*.
> Đúng: nhãn cũ đặt theo **ngành nghề** ("Hành chính - Nhân sự") → gắn cho icon của loại "Đào tạo chuyên viên" thì đọc như một phân loại thứ hai chọi với tên chính.
> Đã kiểm tra `text` chỉ dùng trong picker này, **không nơi nào khác, không lưu DB** → đổi thoải mái.

- [x] `constants/trainingTypeIcons.js` — đổi toàn bộ 20 nhãn từ tên ngành sang **mô tả hình vẽ**: "Hành chính - Nhân sự" → "Nhóm người", "Marketing" → "Loa phóng thanh", "An toàn - Bảo mật" → "Lá chắn", "Kho vận" → "Xe tải"… + comment giải thích lý do để sau không ai đặt lại theo ngành
- [x] `add_training_type_modal.vue` — ô đã chọn **chỉ hiện icon, bỏ hẳn chữ**; chưa chọn thì icon mặc định làm nhạt `#c7cdd4` + placeholder "Chưa chọn icon" (phân biệt với việc user cố tình chọn icon nhãn dán — cùng glyph)
- [x] Xoá computed `selectedIconText` (thành code chết); hint đổi thành "Di chuột lên icon để xem mô tả"
- [x] Verify Playwright: hover ô nhóm người → hint "Nhóm người"; click → ô chọn `innerText` rỗng (không còn chữ), icon = `ri-team-line`, placeholder biến mất, nút `x` hiện

### Phase 3d — Thu gọn ô chọn (user phản hồi lần 3, 2026-07-15)

> User: *"icon hiển thị nhỏ, nhưng mà lại có 1 select dài thườn thượt, không đẹp chút nào"*.
> Đúng — lỗi của Phase 3c: bỏ chữ đi nhưng vẫn giữ nguyên control rộng bằng cả cột (396px) như input text,
> nên còn mỗi glyph 22px nằm chơ vơ giữa khoảng trống mênh mông.

- [x] `add_training_type_modal.vue` — đổi control full-width thành **ô vuông gọn (swatch) 53×36px** ôm đúng icon + caret:
  - `__control` (display:flex, full width) → `__swatch` (`<button>`, width tự co theo nội dung), bọc trong `__row` flex
  - Cao 36px = khớp đúng chiều cao ô "Tên loại đào tạo" → canh hàng chuẩn với các input khác
  - Nút `x` Bỏ chọn tách ra ngoài swatch, chỉ hiện khi đã chọn; chưa chọn thì hiện chữ "Chưa chọn" xám
  - Mở panel: viền xanh + `box-shadow` focus ring (thay cho việc chỉ đổi màu viền — ô nhỏ nên cần tín hiệu rõ hơn)
- [x] Verify Playwright: swatch 53×36 (trước 396px full cột), cao khớp input tên; chọn icon → `ri-hand-coin-line`; bấm `x` → về "Chưa chọn" + icon mặc định nhạt `rgb(199,205,212)`; panel vẫn mở/đóng đúng, không bị modal cắt

### Phase 3e — Dời icon sang cạnh ô Tên (user phản hồi lần 4, 2026-07-15)

> User: *"icon hiển thị nhỏ, nhưng mà lại có 1 select dài thườn thượt"* → sau khi thu gọn swatch vẫn *"chưa đẹp"*.
> Gốc: ô icon 53px bị nhét trong `col-lg-6` rộng 396px → thừa ~340px chết **ngay giữa** 2 field.
> Đã tra web (shadcn / FontAwesome iconpicker / ngx-icon-picker): chuẩn chung = **nút trigger nhỏ + popover chứa search + lưới icon**
> → cơ chế đang làm ĐÚNG chuẩn, cái xấu nằm ở **bố cục form**, không phải picker.
> User chọn kiểu **Notion/Linear: icon đứng sát trước ô Tên**.

- [x] `add_training_type_modal.vue` — gộp Icon + Tên vào 1 hàng flex (`.icon-name-row`): icon `flex: 0 0 auto` (53px), tên `flex: 1 1 auto; min-width: 0` (ăn hết phần còn lại). Label icon rút gọn còn **"Icon"** + `title` tooltip "Hiển thị ở khối Danh mục trên trang chủ elearning" (label cũ dài 170px sẽ tự nong rộng cột, đẻ lại đúng khoảng trống vừa xoá)
- [x] "Thứ tự hiển thị" tách xuống hàng riêng (`col-lg-6`)
- [x] Nút **Bỏ chọn dời vào footer của panel** (cạnh dòng hint), bỏ nút `x` + chữ "Chưa chọn" đứng cạnh swatch — 2 thứ đó nong ô icon ra, phá thế ôm sát ô Tên
- [x] Verify Playwright: icon 53×36 + tên rộng 703px, cách nhau 12px, **khoảng trống thừa = 0px** (trước ~340px); 2 ô cùng `top` + cùng cao 36px (canh hàng chuẩn); panel mở đúng, footer có hint "Nhóm người" + nút "Bỏ chọn", panel không tràn modal
- [ ] ⏳ User xác nhận UI + lưu thử (lưu cần migrate xong mới có cột `icon`)

## Phase 4 — FE elearning: nối 2 API vào homepage

- [x] `constants/homeActivity.js` — map type → icon/gradient/nhãn hành động + `DEFAULT_CATEGORY_ICON`
- [x] `utils/timeAgo.js` — ISO → "2 phút trước" (không thêm dependency)
- [x] `stores/elearning.js` — 2 action mới, `Promise.allSettled` 3 API; xoá `categoryCount`/`mixAll`/`pickThumb`/state `courses`,`subjects`/import `THUMBS`,`COURSES`,`SUBJECTS`
- [x] `components/home/HeroBanner.vue` — feed thật, bỏ nút "Xem →", dòng clickable, trạng thái rỗng
- [x] `views/home/HomeView.vue` — ô danh mục → `/hoc-theo-loai-dao-tao?training_type_id=X`, "Xem tất cả" → list, click feed → chi tiết khoá/lộ trình
- [x] `components/base/CategoryCard.vue` — fallback icon

## Phase 5 — Phụ đề tiến độ lộ trình trong feed (chốt 2026-07-15, SAU khi Phase 1-4 đã code xong)

> Quyết định #9 spec: KHÔNG thêm event "cập nhật tiến độ" riêng (1 hành động → 4-5 dòng, phá luật max 2/người).
> Thay vào đó làm giàu dòng `complete`/`certificate` sẵn có bằng phụ đề *"2/5 trong lộ trình X"*.

- [ ] `HomeActivityService` — bước 9 `enrichPathContext()`, chạy **sau** khi cắt còn 15 dòng (không tính cho 240 dòng thô)
- [ ] 4 query gộp không N+1: `learning_path_subjects` → `learning_path_enrollments` → `learning_path_subjects` (total) → `subject_enrollments` (done)
- [ ] Chỉ áp cho `content_type = subject` + `type ∈ {complete, certificate}`; bỏ qua `start` và dòng lộ trình
- [ ] Chỉ hiện khi khoá thuộc **đúng 1** lộ trình người đó đã ghi danh (0 hoặc ≥2 → `path_context = null`)
- [ ] ⚠️ `done` đếm theo `completed_at <= occurred_at` của chính dòng đó (tiến độ tại thời điểm quá khứ, KHÔNG phải hiện tại)
- [ ] Guest + lộ trình không public → bỏ phụ đề, giữ dòng `complete`
- [ ] `total = 0` (pivot rác) → bỏ phụ đề, không chia 0
- [ ] `HeroBanner.vue` — render dòng phụ chữ nhạt dưới tên khoá, `null` thì không render; ellipsis 1 dòng; click vẫn mở khoá
- [ ] Verify 5a-5e (mục 8 spec), đặc biệt **5b**: hoàn thành khoá 3 → dòng khoá 2 vẫn phải là 2/5, không nhảy 3/5

## Phase 6 — Giới hạn 6 danh mục + sửa luật thứ tự + kéo-thả sắp xếp (2026-07-15, sau khi user migrate)

> User phản hồi sau khi chạy migrate: (1) trang chủ hiện 7 mục, muốn tối đa 6; (2) đặt "Thứ tự hiển thị = 1"
> mà mục đó lại nằm cuối; (3) muốn trực quan hơn mục nào sẽ hiện + thứ tự.

**Bug 1 — hiện 7 mục:** `HomeCategoryService::build()` trả về TẤT CẢ loại đào tạo Hoạt động, FE `v-for` render hết.
Lưới `lg:grid-cols-6` → cái thứ 7 rớt xuống hàng 2. Không có chỗ nào giới hạn.

**Bug 2 — "thứ tự 1" nằm cuối (lỗi thiết kế, không phải lỗi code):** query `orderBy('sort_order')` tăng dần,
mà cột mặc định `sort_order = 0`. Mục đặt hạng 1 → mọi mục chưa đặt (0) chen lên trước → **hễ đặt thứ tự cho
mục nào là mục đó bị đẩy xuống sau tất cả mục chưa đặt**, ngược hoàn toàn trực giác "1 là đầu tiên".
Sửa: `0` = CHƯA đặt → cho xuống cuối; đã đặt hạng lên trước.

- [x] `HomeCategoryService` — thêm `HOME_LIMIT = 6` + `limit()`
- [x] `HomeCategoryService` — `orderByRaw('CASE WHEN sort_order = 0 THEN 1 ELSE 0 END')` trước `orderBy('sort_order')->orderBy('name')`
- [x] `php -l` sạch
- [x] Verify trên trang chủ elearning thật: đúng 6 ô / 1 hàng; "Đào tạo chuyên viên" (sort_order=1, icon loa) lên **đầu tiên**; "Đào tạo sản phẩm mới" (thứ 7) rớt khỏi trang chủ

### Phase 6b — Modal kéo-thả sắp xếp danh mục trang chủ (user chọn)

> Gốc rễ của bug 2 là **ô nhập số thứ tự** — user gõ 1 rồi hoang mang. Bỏ hẳn con số, thay bằng kéo-thả.
> `vuedraggable@2.24.3` đã có sẵn trong `package.json` → không cần thêm thư viện.

**BE:**
- [x] `TrainingType` entity — hằng `HOME_CATEGORY_LIMIT = 6` + scope `orderByHomePosition()` (đặt ở Modules/Training để `Modules/Elearning` dùng lại; KHÔNG để Training phụ thuộc ngược vào Elearning)
- [x] `HomeCategoryService` — dùng hằng + scope chung
- [x] `TrainingTypeController::getAll()` — thêm `orderByHomePosition()` để modal dựng lại đúng hiện trạng
- [x] `TrainingTypeController::updateSortOrder()` — nhận mảng `ids` theo thứ tự → reset toàn bộ về 0 rồi gán `1..N`. Transaction + validate `max:6` + `distinct` + `exists`. Nhận nguyên mảng thay vì từng bản ghi (kéo đổi chỗ 2 ô là đổi cả dãy; gửi lẻ sẽ trùng số nếu request rớt giữa chừng)
- [x] Route `POST /training_types/sort-order` + `->middleware('checkPermission:Quản lý loại đào tạo')` (convention CLAUDE.md cho route thao tác dữ liệu)
- [x] `php -l` 4 file BE — sạch

**FE hrm-client:**
- [x] Nút "Sắp xếp trang chủ" trên toolbar (dùng `b-button` theo style sẵn có của trang — trang này chưa migrate sang V2BaseButton, xen 1 nút V2 vào sẽ lệch hẳn)
- [x] Modal mới `sort_training_type_modal.vue` — 2 vùng kéo-thả + counter `n/6` + số vị trí trên từng thẻ
- [x] Bỏ ô "Thứ tự hiển thị" khỏi `add_training_type_modal.vue`
- [x] Lưu xong → `@event` → reload list

**⚠️ Bug đã dính khi làm — chặn quá 6 KHÔNG dùng `:move`:**
Ban đầu gắn `:move="onMoveIntoShown"` lên vùng "Hiện" → **không chặn được**, kéo lọt lên 7/6 (đã bắt bằng test).
Nguyên nhân: SortableJS gọi `onMove` trên instance của danh sách **NGUỒN**, nên handler gắn ở vùng đích không bao giờ chạy khi kéo từ vùng "Không hiện" sang. Sửa: dùng `put` trong `:group` của vùng đích — `put` được hỏi trên group đích bất kể nguồn, và không ảnh hưởng kéo đổi chỗ nội bộ.

**Verify (Playwright, màn thật):**
- [x] Modal dựng đúng hiện trạng: 6/6, "Đào tạo chuyên viên" vị trí 1 + icon loa, "Đào tạo sản phẩm mới" ở vùng Không hiện
- [x] Kéo mục thứ 7 vào vùng hiện → **bị chặn**, vẫn 6/6, mục đó ở lại vùng Không hiện
- [x] Kéo đổi chỗ nội bộ (vị trí 6 → 1) → số vị trí tự đánh lại đúng
- [x] Bấm Lưu → modal đóng, list refresh, `Ngày cập nhật` đổi
- [x] **Trang chủ elearning đổi đúng thứ tự vừa kéo** (phát triển bản thân → chuyên viên → nhân viên → hội nhập → kỹ năng mềm → kỹ thuật), 6 ô/1 hàng, "sản phẩm mới" biến mất
- [x] Đã kéo-lưu trả lại đúng thứ tự user tự sắp trước đó (test E2E có ghi DB thật → khôi phục nguyên trạng)

## Verify

- [x] `php -l` 9 file BE — sạch
- [x] ESLint 6 file elearning (Node 24) — sạch
- [x] `vite build` — pass
- [x] Tinker DB thật: feed nhân viên 9 dòng / khách 8 dòng (luật `is_public` đúng), "Trí Lee" đúng 2 dòng (luật max 2/người)
- [x] Tinker reflection `pathEvents`: learner ngoài học lộ trình ra đúng 1 dòng (`l:6` — Trí Lee, "Test lộ trình học")
- [x] Tinker reflection `mapRows`/`limitPerUser`: `certificate` vs `complete` phân nhánh đúng; nhân viên không tra được tên bị loại; max 2/người; `owner_key` đã xoá khỏi payload
- [x] Logic đếm danh mục: 7 loại đào tạo Hoạt động, subject_counts + path_counts đúng
- [ ] ⏳ User chạy `php artisan migrate` (2 migration)
- [ ] ⏳ Verify UI browser: homepage feed + danh mục, đổi icon ở hrm-client → homepage đổi theo
- [ ] ⏳ `HomeCategoryService` chạy thật (cần cột `icon` → sau migration)
- [ ] ⏳ Nhánh `certificate` với data thật (hiện chưa có enrollment DONE nào thuộc khoá `certificate_enabled=1`)

---

### Checkpoint — 2026-07-15

Vừa hoàn thành: CODE DONE toàn bộ 4 phase (13 file: 2 migration, 2 service BE, controller+route, 3 file Training BE, 3 file hrm-client, 6 file elearning). Verify tĩnh sạch (php -l, eslint, vite build) + verify động qua tinker trên DB thật: feed ra 9 dòng nhân viên / 8 dòng khách, nhánh lộ trình + learner ngoài chạy đúng, nhánh certificate + luật max 2/người + loại dòng không tên đã chứng minh bằng reflection.
Đang làm dở: Không.
Bước tiếp theo: User chạy `cd hrm-api && php artisan migrate` (2 migration mới) → mở homepage elearning xem feed + danh mục → vào /training/training_types set icon cho vài loại đào tạo để thấy danh mục đổi icon.
Blocked: `HomeCategoryService` + màn Loại đào tạo chưa chạy được cho tới khi migrate (thiếu cột `icon`/`sort_order`) — đúng dự kiến, không phải lỗi.

### Checkpoint — 2026-07-15 (lần 2)

Vừa hoàn thành: Chốt quyết định #9 + cập nhật spec/design cho **Phase 5 — phụ đề tiến độ lộ trình**.
User hỏi có nên thêm event "cập nhật tiến độ" khi hoàn thành 1 khoá thuộc lộ trình.
→ Đã bác bỏ event riêng (dẫn chứng từ `LearningSessionService::syncLearningPathCompletion()`:
không có cột `progress`, 1 khoá thuộc nhiều lộ trình, Q2 đã bắn `complete` rồi → 1 hành động sinh 4-5 dòng, phá luật max 2 dòng/người).
→ Chốt phương án làm giàu dòng sẵn có bằng phụ đề *"2/5 trong lộ trình X"*. User đã đồng ý.
Đã cập nhật: spec (quyết định #9 + mục 4.2.1 + response `path_context` + FE + 7 edge case + testcase 5a-5e), `.plans/.../design.md` (quyết định #8 + 2 điểm cần nhớ).

Đang làm dở: Không — mới chỉ cập nhật tài liệu, **chưa code Phase 5**.

Bước tiếp theo: User quyết định code Phase 5 luôn hay để user chạy migrate + verify UI Phase 1-4 trước rồi mới làm.

Blocked: Không.
