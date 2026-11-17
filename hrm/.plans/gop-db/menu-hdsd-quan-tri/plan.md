# Menu HDSD ở popup chuyển phân hệ (không có số Redmine) — @cuong61n

## Phase 1
### FE (hrm-client, nhánh `gop_db`)
- [x] 17/11/2026 — Thêm nút "HDSD" vào popup chuyển phân hệ VÀ nhụy hoa màn chọn phân hệ `/`, nhóm QUẢN TRỊ (cạnh Thông tin NS · Danh mục · Quản trị); bấm mở https://help.eteksofts.com/ ở tab mới. (Hiểu sai lần đầu: đã làm thành mục trong sidebar Quản trị, đã hoàn lại hết.)
  - Kỹ thuật: `components/subsystems.js` thêm phân hệ giả `hdsd` (`hidden` + `erpGhost` + `erpLink` + cờ mới `newTab`) — không vào Phân quyền, Cài đặt phân hệ; màn chọn phân hệ `pages/index.vue` `coreItems` nhận thêm `erpGhost`, nhụy hoa đổi từ 3 nhị (tam giác) sang 4 nhị lưới 2x2 (`STAMEN_POS` + CSS `.st-nw/.st-ne/.st-sw/.st-se`); `SubsystemSwitcher.vue` + `pages/index.vue` mở `window.open` khi có `newTab`; icon mới `assets/images/icon_hdsd.svg`.
  - Kiểm: đọc diff + rà các nơi duyệt SUBSYSTEMS; chưa chạy trình duyệt. Trạng thái: sửa trong worktree `worktrees/gop_db-client` (nhánh gop_db), chưa commit/push.
