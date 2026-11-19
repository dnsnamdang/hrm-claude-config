# Regulation-config — sửa layout thừa khoảng trống cho khớp các màn khác

> Nhánh: `gop_db` (develop). Phụ trách: @dangquang.tom

## Bối cảnh

Yêu cầu user (kèm ảnh màn `/assign/regulation-config`): "khai báo quy chế 2 bên thừa nhiều
khoảng trống, sửa layout cho khớp các màn khác trong hệ thống".

Màn dùng chung component `components/regulation-config/RegulationConfigScreen.vue` (3 page
`extends`: `/sale`, `/assign`, `/finance` regulation-config — chỉ khác data `subsystem`). Sửa style
ảnh hưởng cả 3 (cùng 1 vấn đề whitespace → sửa 1 lần).

## Nguyên nhân (đã xác định trong `<style scoped>`)

1. **Lề trống 2 bên** — `.rc-page` (dòng 3164-3166): `max-width: 1320px; margin: 0 auto;` → viewport
   rộng > 1320px sinh lề trống 2 bên. Các màn khác bọc `<Nuxt />` trong `.container-fluid`
   (layouts/default.vue:106) = FULL WIDTH, KHÔNG có max-width cứng.
2. **Khoảng trống dưới card** — `.detail` (dòng 3226-3227): `min-height: 420px;` → tab ít nội dung
   (vd "Quy chế khác" 3 ô) vẫn cao 420px → vùng trống lớn dưới.

## Hướng sửa (khớp `container-fluid` các màn khác)

- `.rc-page`: bỏ `max-width: 1320px` + `margin: 0 auto` → full-width như container-fluid. Padding 2
  bên nâng `8px` → `15px` cho khớp padding mặc định `.container-fluid` của Bootstrap.
- `.detail`: bỏ `min-height: 420px` → card co theo nội dung (giữ `overflow: hidden` để clip bo góc).

## Tasks

- [x] **Task 1: Sửa `.rc-page`** — bỏ max-width + margin auto, padding `14px 15px 40px`. ✔
- [x] **Task 2: Sửa `.detail`** — bỏ `min-height: 420px`, giữ `overflow: hidden`. ✔
- [x] **Task 3: Verify Playwright** — PASS. ✔
  - `/sale` @viewport 1600: `.rc-page` width **1355** ≈ `.container-fluid` 1365 (chênh 10px = padding),
    rule `max-width` = (none), `.detail` min-height rule = (none) → computed `auto`, card co còn **375px**.
  - `/assign` (màn trong ảnh user) @1600: `.rc-page` width **1360** full-width, `.detail` min-height
    `auto` (card "Kỹ thuật" cao 426px = theo nội dung thật, không ép), bảng Lịch sử nằm sát dưới.
    Ảnh full-page xác nhận nội dung trải hết chiều rộng, hết lề trống 2 bên. 0 console error.

### Checkpoint — 2026-10-16
Vừa hoàn thành: Task 1 (bỏ max-width 1320 + margin auto, padding 15px) + Task 2 (bỏ min-height 420px)
  + Task 3 (verify Playwright PASS /sale + /assign, đã resize 1600 chứng minh hết lề 2 bên; dọn PNG).
Đang làm dở: (không) — feature hoàn tất code.
Bước tiếp theo: chờ user yêu cầu commit (gộp với YC9 #2 cùng chưa commit).
Blocked: (không)

**File đã sửa (CHƯA commit):**
- hrm-client: `components/regulation-config/RegulationConfigScreen.vue` (`.rc-page` bỏ max-width/margin
  + padding 15px; `.detail` bỏ min-height 420px). Component dùng chung 3 màn `/sale` `/assign`
  `/finance` regulation-config → sửa 1 lần khớp cả 3 (cùng 1 vấn đề whitespace).
