# Menu HDSD ở popup chuyển phân hệ (không có số Redmine) — @cuong61n

## Phase 1
### FE (hrm-client, nhánh `gop_db`)
- [x] 17/11/2026 — Thêm nút "HDSD" vào popup chuyển phân hệ VÀ nhụy hoa màn chọn phân hệ `/`, nhóm QUẢN TRỊ (cạnh Thông tin NS · Danh mục · Quản trị); bấm mở https://help.eteksofts.com/ ở tab mới. (Hiểu sai lần đầu: đã làm thành mục trong sidebar Quản trị, đã hoàn lại hết.)
  - Kỹ thuật: `components/subsystems.js` thêm phân hệ giả `hdsd` (`hidden` + `erpGhost` + `erpLink` + cờ mới `newTab`) — không vào Phân quyền, Cài đặt phân hệ; màn chọn phân hệ `pages/index.vue` `coreItems` nhận thêm `erpGhost`, nhụy hoa đổi từ 3 nhị (tam giác) sang 4 nhị lưới 2x2 (`STAMEN_POS` + CSS `.st-nw/.st-ne/.st-sw/.st-se`); `SubsystemSwitcher.vue` + `pages/index.vue` mở `window.open` khi có `newTab`; icon mới `assets/images/icon_hdsd.svg`.
  - Kiểm: đọc diff + rà các nơi duyệt SUBSYSTEMS; chưa chạy trình duyệt. Trạng thái: sửa trong worktree `worktrees/gop_db-client` (nhánh gop_db), chưa commit/push.

## Phase 2 — ERP cũng hiện HDSD (user báo 27/11/2026: "từ ERP không nhìn thấy phần chọn HDSD")
### ERP (TanPhatDev, nhánh `gop_db`)
- [x] 27/11/2026 — Popup chuyển phân hệ trên ERP (icon ô vuông góc phải header) thêm mục "HDSD" vào nhóm QUẢN TRỊ (sau Thông tin NS · Danh mục · Quản trị), bấm mở https://help.eteksofts.com/ ở tab mới — khớp HRM Phase 1. Nguyên nhân thiếu: popup ERP là bản copy tĩnh của registry HRM (`resources/views/layouts/topheader.blade.php`), lúc làm Phase 1 chỉ sửa HRM.
  - Kỹ thuật: mảng `$switcher_groups` thêm item có khoá mới `ext` (link ngoài tuyệt đối, `target="_blank" rel="noopener"`); template `href` ưu tiên `hrm` → `ext` → `erp`; copy icon `public/images/icon-hrm/icon_hdsd.svg` từ hrm-client.
  - Kiểm: biên dịch blade bằng PHP 7.4 + `php -l` không lỗi; sau deploy `curl` icon trên prod trả 200, trang chủ 302 → login bình thường, log Laravel không có lỗi mới. Chưa đăng nhập prod để nhìn popup bằng mắt.
  - Trạng thái: commit `64d24fd238` gop_db (đã push) · **đã deploy prod ERP 27/11/2026** (`git pull --ff-only` + `view:clear` trên erp-prod). ERP dev (develop_02) chưa kéo.
