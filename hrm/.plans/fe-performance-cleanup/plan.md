# Plan — Tối ưu hiệu năng FE hrm-client

Repo: `hrm-client` | Nhánh: `tpe-develop-assign` | Working dir: `HRM/hrm-client`

## Phase 1 — Config build

### FE
- [x] `config.devtool` khi dev: `source-map` → `eval-cheap-module-source-map`; khi build chỉ bật nếu `BUILD_SOURCEMAP=true`
- [x] `build.devtools` chỉ bật ở dev (trước đó `true` cả bản production)
- [x] ~~Thêm `defer` cho script jQuery~~ → **ĐÃ REVERT**: gây `Uncaught ReferenceError: jQuery is not defined`.
      Bundle Nuxt được inject chạy TRƯỚC script defer ở head, trong khi `plugins/select2-custom.js`
      và `plugins/jquery.doubleScroll.js` cần biến toàn cục `jQuery` ngay lúc bootstrap.
      → **KHÔNG đặt `defer`/`async` cho jQuery**, đã ghi chú ngay trong `nuxt.config.js`.

## Phase 2 — Xoá import rác

### FE
- [x] Xoá 6 dòng `import { f | data | computed }` từ `vue-grid-layout` / `vue-slide-bar` / `vue-knob-control` (auto-import IDE nhầm)
- [x] Xoá `plugins/axios_bk.js` (backup chết)

## Phase 3 — Loại route rác

### FE
- [x] Thêm `ignore` cho `pages/**/{components,component,utils,mixins,helpers,constants}/**`
- [x] Kiểm chứng: router.js 960KB → 560KB, `path:` 5160 → 3344, dòng `components/` 2270 → 0

## Phase 4 — Bỏ nuxt-i18n (phần mềm chỉ dùng tiếng Việt)

### FE
- [x] Xác minh: 24/28 chỗ `$t(item.label)` truyền nhãn đã là tiếng Việt, en.json không có key → không dịch gì
- [x] 4 chỗ còn lại dịch ra "My Account" (tiếng Anh) → thay bằng "Tài khoản của tôi"
- [x] Thay toàn bộ `$t(x)` → `x` (7 file: Sidebar, human-slidebar, assign-slidebar, HumanMenu, AssignMenu, ExamToDoMenu)
- [x] Gỡ `nuxt-i18n` khỏi `modules` + xoá khối config `i18n`
- [x] Xoá `locales/{en,fr,es,ar,zh}.json`; GIỮ `vi.json` (vee-validate đang dùng)

## Phase 5 — Code-splitting & lazy-load lib nặng

### FE
- [x] Bật lại `optimization.splitChunks` (bỏ `maxSize` vì băm bundle quá vụn), thêm nhóm `heavy` (markgojs/exceljs/firebase)
- [x] `store/auth.js` + `plugins/fireauth.js`: chuyển firebase sang dynamic import (trước đó import tĩnh → firebase nằm trong bundle mọi trang dù không dùng)
- [x] KHÔNG xoá `store/auth.js` — nhiều màn đọc `$store.state.auth.user` không có optional-chaining, xoá sẽ ném TypeError

## Phase 6 — Gỡ plugin toàn cục không dùng

### FE
- [x] Quét theo TAG template (không chỉ `import`) → gỡ 6 plugin: draggable, vue-slidebar, tour, vue-lightbox, chartist, string-filter
- [x] GIỮ `vue-star-rating` (13 chỗ dùng) và `vue-grid-layout` (4 chỗ dùng)

## Phase 7 — Dọn icon font & code chết

### FE
- [x] Gỡ remixicon local v2.4.0 (trùng `@font-face` với CDN v4.3.0, không có icon nào CDN thiếu)
- [x] Gỡ `feather` + `weather-icons` (0 lượt dùng)
- [x] GIỮ materialdesignicons (909), fontawesome (2905), boxicons — đều dùng thật
- [x] Xoá 13 file `_bk`/`_bak` không tham chiếu (584KB)
- [ ] BỎ QUA: gỡ style trang demo Minton trong `app.scss` — chỉ 100KB, lời không bù rủi ro vỡ giao diện

## Phase 8 — Sửa lỗi do chính đợt tối ưu gây ra (phát hiện khi test Playwright)

- [x] **`jQuery is not defined`** — do thêm `defer` vào script jQuery. Đã revert, ghi chú cấm đặt lại
- [x] **App treo ở màn loading, không route được** — `middleware/authenticated.js:14` so sánh `route.name === 'login___en'`.
      `___en` là hậu tố nuxt-i18n; gỡ i18n xong route chỉ còn tên `login` → không khớp → `redirect('/login')`
      vô hạn ngay tại `/login`. Đã đổi sang so sánh `route.path`
- [x] **Bundle dev 97MB, trình duyệt tải không nổi** — `eval-cheap-module-source-map` nhúng map vào JS.
      Theo yêu cầu user: **tắt hẳn sourcemap** (`devtool = false`), bật lại qua `BUILD_SOURCEMAP=true`. Còn 39.5MB
- [x] **splitChunks phản tác dụng** — `chunks:'all'` biến charts/editor/heavy thành chunk KHỞI TẠO,
      trang login cũng tải ~15MB. Đã bỏ, dùng mặc định Nuxt
- [x] **Mất nút chọn phân hệ trên topbar** — gỡ nhầm `@import 'icons/feather'`. Feather dùng tiền tố
      `fe-` chứ không phải `feather-` → phép đo "0 lượt dùng" của tôi sai, thực tế **57 lượt**
      (`fe-grid` = nút chọn phân hệ, `fe-x`, `fe-menu`, `fe-bell`, `fe-log-out`, `fe-maximize`). Đã khôi phục

### Đã kiểm chứng bằng Playwright (đăng nhập thật)
- Trang login hiển thị đúng, 0 lỗi
- `/assign/my-todo`: topbar + sidebar + icon + nội dung đúng
- `/human/dashboard`: topbar đủ 4 icon, chart chạy, dropdown chọn phân hệ mở đủ 8 phân hệ, 0 lỗi console
- Lỗi còn lại `CreateIssueModal.vue: computed "errors" already defined in data` là **có sẵn từ trước**, không thuộc 40 file đã sửa

### Rà soát lần 2 (theo yêu cầu user) — kết quả

Rà tĩnh theo **tiền tố class/tag thực tế**, tất cả sạch:
- Tàn dư nuxt-i18n (`$t`/`$tc`/`v-t`/`$i18n`/`localePath`/so sánh `route.name` có `___`): 0
- Import locale đã xoá: 0 | Import plugin đã xoá: 0 | Tham chiếu file `_bk`/`_bak`: 0
- Icon: `fe-` 57 (đã khôi phục), `wi-` 0 (bỏ đúng), `ri-` 2471, `mdi-` 835, `fa-` 3035, `bx` 22 — đều còn font
- Tag/directive của 6 plugin đã gỡ: đều 0 lượt dùng

Duyệt 8 màn bằng Playwright (đăng nhập thật), **tất cả hiển thị đúng**:
`/login`, `/` (chọn phân hệ), `/assign/my-todo`, `/assign/tasks`, `/assign/quotations`,
`/human/dashboard`, `/payroll/dashboard`, `/training/dashboard`, `/decision/dashboard`,
`/timesheet/dashboard`, `/timesheet/attendance/add` (form)

### LỖI CÓ SẴN trong codebase (KHÔNG do đợt tối ưu — 2 file này không nằm trong 40 file đã sửa)
- `pages/timesheet/attendance/add.vue:3` — `<PageHeader :items="items">` nhưng `items` không khai trong `data` → Vue warn ×5
- `components/modals/AddEmployee.vue:101` — `fields` khai ở cả `data` lẫn `computed` → Vue warn
- `pages/assign/issues/components/CreateIssueModal.vue` — `errors` khai ở cả `data` lẫn computed (xung đột vee-validate)
- 8 tên icon remixicon không tồn tại ở cả bản local lẫn CDN (xem mục dưới)

### Bài học
Chỉ chạy `nuxt build` (exit 0) là KHÔNG đủ — không bắt được lỗi runtime lẫn kích thước bundle dev.
Khi gỡ thư viện/icon phải tra đúng **tiền tố class thực tế**, không tra theo tên package.

## Còn lại (chưa làm)

- [ ] Gỡ package khỏi `package.json` (node-zklib, pusher-js, @nuxtjs/laravel-echo, vue-count-to, vue-number-input-spinner, vue-qrcode, vue-switches...) — LƯU Ý: không còn được import nên **không ảnh hưởng tốc độ build**, chỉ giảm dung lượng `node_modules` + thời gian `npm install`. Vài package còn bị `assets/scss` import CSS (vue-form-wizard, chartist, c3) → phải gỡ SCSS trước
- [ ] BE: `hrm-api/.env` đang `APP_DEBUG=true` + `LOG_LEVEL=debug` với 2.212 route API
- [ ] Bug rời (không thuộc hiệu năng): 8 tên icon không tồn tại ở cả 2 bản remixicon — `ri-check-circle-line`, `ri-handshake-line`, `ri-list-check-2-line`, `ri-sigma-line`, `ri-spin`, `ri-spin-fill`, `ri-table-2-line`, `ri-user-check-line`

---

## Checkpoint — 2026-08-12
Vừa hoàn thành: Phase 1-7. Build sạch `npx nuxt build` (Node 14.21.3) **exit 0, không lỗi, 4m48s**.

Kết quả đo được:
| | Trước | Sau |
|---|---|---|
| `.nuxt/router.js` | 960 KB | **232 KB** (−76%) |
| Số `path:` | 5.160 | **814** (−84%) |
| Route `/fr` `/es` `/ar` | 2.502 | **0** |
| Code chết đã xoá | — | 584 KB (13 file `_bk`/`_bak`) |

Cảnh báo `[BABEL] router.js exceeds 500KB` đã hết.

Đang làm dở: đã thêm `pages/**/partials/**` vào `ignore` SAU khi build xong → dòng này chưa qua build kiểm chứng (cùng cơ chế với các pattern đã verify nên rủi ro rất thấp).

Bước tiếp theo:
1. Chạy `nvm use 14.21.3 && npm run dev`, bấm thử **sidebar/menu** (chỗ thay `$t()`), màn có **star-rating**, **grid-layout**
2. Chưa đo được thời gian build TRƯỚC khi sửa (không có mốc) → nếu muốn con số so sánh thì stash thay đổi rồi build 1 lần lấy baseline

Blocked: không

Lưu ý: user tự commit `8c06f9059` "fix meeting" lúc 11:59 giữa session — chỉ gồm 4 file của user, không lẫn thay đổi tối ưu. Toàn bộ thay đổi ở plan này vẫn chưa commit.
