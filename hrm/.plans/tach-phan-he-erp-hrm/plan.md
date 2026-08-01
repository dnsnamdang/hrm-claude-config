# Plan — Tách/gộp phân hệ ERP + HRM theo Sơ đồ tổng thể v1.6

## Phase 1 — Khảo sát & lập bảng gộp

- [x] Parse menu ERP thật từ `topmenubar.blade.php` (strip blade comment) → 561 màn
- [x] Parse menu HRM từ `menu.js` / `menu-sidebar.js` / `default-menu/*.js` (loại `isShow: false`) → 267 màn
- [x] Dựng sheet `Gộp phân hệ ERP-HRM` (cột Nguồn tô màu HRM/ERP/HRM+ERP/CHƯA CÓ) + `Tổng hợp gộp phân hệ`
- [x] Loại 4 phân hệ giữ nguyên bên ERP (Quản lý hàng hoá / Kho / Vận chuyển / Mua hàng) → còn 611 dòng
- [x] Đối chiếu `erp-menu-inventory.xlsx` (304 chức năng ERP chuyển sang HRM) — khớp phần đã loại

## Phase 2 — Base BE (hrm-api)

- [x] Tạo 17 module skeleton từ mẫu `Modules/Management` (module.json, composer.json, Config,
      Providers, Routes prefix `/api/v1/<alias>`, Http/Controllers/V1, Entities, Services,
      Transformers, Database, Resources, Tests)
- [x] Đăng ký `modules_statuses.json` → `php artisan module:list` = 26 module Enabled
- [x] `php -l` sạch toàn bộ file PHP mới

## Phase 3 — Base FE: registry + menu

- [x] Tạo registry `components/subsystems.js` (SUBSYSTEMS, SUBSYSTEM_GROUPS,
      SUBSYSTEM_GROUP_META, resolveSubsystem, findSubsystemByLink, getAllMenuItems)
- [x] Tạo menu phân hệ mới: `subsystem-menu/{master-data,insurance,sale,placeholder}.js`
- [x] Rút màn đã chuyển khỏi menu cũ: human (−8), decision (−7), assign (−29), để lại comment trỏ sang file mới
- [x] Đấu registry vào `layouts/default.vue`, `training-components/Sidebar.vue`, `middleware/checkPermission.js`
- [x] Tạo 17 `pages/<slug>/dashboard/index.vue` + component `SubsystemDashboardPlaceholder.vue`
- [x] Kiểm tra 0 link trùng giữa 2 phân hệ

## Phase 4 — Màn chọn phân hệ + menu chuyển nhanh

- [x] Dựng lại `pages/index.vue` theo dáng sơ đồ (băng Lõi trên, 4 cột nhóm, thanh ERP dưới)
- [x] Nới `layouts/system.vue`: container 600px → 1120px, chiều cao `100vh - 60px`
- [x] Tách `SubsystemSwitcher.vue` khỏi `BasicSubsystem.vue` (bỏ grid 3×3 hardcode 8 phân hệ)
- [x] Cân 2 cột dropdown bằng grid + `GRID_ORDER` (bỏ `column-count` vì tràn sang cột 3 bị cắt)
- [x] Vẽ 17 icon SVG (32×32, vùng vẽ ~73% khung, mỗi phân hệ 1 màu)
- [x] Chuẩn hoá `icon_rice.svg` (vùng vẽ 96% → 73%, canh giữa)
- [x] Header nhóm dùng gradient, hạ về cùng tông `#2E71C3`; 2 băng hạ tầng dùng xám trung tính
- [x] Đo bố cục vừa 1 màn: 1512×900, 1280×720, 1024×800 — không cuộn

## Phase 5 — Đồng bộ kiểu menu (phân hệ mới đi menu dọc)

- [x] Tạo `layouts/subsystem.vue` — chrome sidebar + `.subsystem-content` nạp bộ SCSS của topbar
- [x] Gắn `layout: 'subsystem'` cho 26 màn (9 màn `human/*`, 17 màn `decision|regulations/*`)
- [x] Đổi 17 dashboard stub sang `layout: 'subsystem'`
- [x] Logo + tên phân hệ ở sidebar lấy từ registry (`Sidebar.vue` thêm prop `imgLogo`)
- [x] Audit: 24/24 phân hệ đồng bộ 1 kiểu menu
- [x] Fix: `layouts/subsystem.vue` thiếu `toggleMenu` → bấm nút thu gọn menu ném lỗi ra 404

## Phase 6 — Test thực tế trên môi trường dev

- [x] Đăng nhập 127.0.0.1:3000, kiểm tra 9 màn đại diện
- [x] Fix: 14 phân hệ trắng sidebar rỗng — `Sidebar.vue::isShowMenuParent` mặc định ẩn item
      không có `subItems`; thêm `isShow: true` cho mục "Tổng quan" ở 4 file menu
- [x] Verify màn form nặng không vỡ style (`insurance-packages/add`, `customers/add`)
- [x] Verify brand "BÁN HÀNG" trên route `/assign/*` + dropdown tô sáng đúng phân hệ

## Phase 7 — Còn lại (chưa làm)

- [ ] User test 17 màn edit/detail còn lại trong nhóm 26 màn đổi layout
- [ ] Giai đoạn 2: chuyển code `/assign/*` → `/sale/*`, `/human/*` → `/master-data/*`,
      `/decision/insurance*` → `/insurance/*`
- [ ] Cờ `master-settings` bật/tắt 17 phân hệ mới (hiện luôn hiện)
- [ ] Phân quyền chi tiết cho phân hệ mới
- [ ] Dashboard thật cho phân hệ mới
- [ ] Xử lý dứt điểm xung đột 2 bản Remix Icon (local v2.4.0 vs CDN v4.3.0)
- [ ] Rà lại sheet: `Khởi tạo > Hàng hóa` (22 phiếu) + `Kế toán > Kiểm kê` (4) có trong
      inventory ERP nhưng đã bị loại khỏi sheet do xếp vào phân hệ Kho

## Checkpoint — 2026-07-30 — HOÀN THÀNH GIAI ĐOẠN 1

Vừa hoàn thành:

- Phase 1-6. BE 26 module Enabled. FE 25 phân hệ trong registry, 24/24 đồng bộ kiểu menu,
  0 link trùng, 0 phân hệ menu rỗng.
- 2 bug tự phát hiện và fix trong lúc test thật trên dev: thiếu `toggleMenu` ở layout mới
  (bấm nút thu gọn menu ra trang 404), và mục "Tổng quan" bị ẩn làm 14 phân hệ trắng có
  sidebar rỗng (`Sidebar.vue::isShowMenuParent` mặc định trả false).
- Tài liệu: `design.md` + `plan.md` (folder này) + spec đầy đủ ở
  `docs/superpowers/specs/2026-07-30-tach-phan-he-erp-hrm-design.md`. STATUS.md đã chuyển
  feature sang mục "Hoàn thành".

Đang làm dở: (không)

Bước tiếp theo:

- Tồn của giai đoạn 1: user test 17 màn edit/detail còn lại (dùng chung component form với
  màn đã test nên rủi ro thấp).
- Giai đoạn 2 (di chuyển code màn sang route mới) chưa bắt đầu — xem Phase 7. Khi làm tiếp
  thì chuyển feature về "Đang làm" trong STATUS.md trước.

Blocked: (không)
