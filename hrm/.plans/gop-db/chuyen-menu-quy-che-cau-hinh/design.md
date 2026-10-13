# Design — Chuyển menu "Khai Quy chế – Cấu hình" sang phân hệ Bán hàng

> Phụ trách: @namdangit · Nhánh: `gop_db` (repo `hrm-client`) · 2026-09-21

## Mục tiêu
Mục menu **Khai Quy chế – Cấu hình** (`/master-data/regulation-config`) rời phân hệ **Danh mục
dùng chung** (`master-data`), xuất hiện ở phân hệ **Bán hàng** (`sale`). Giữ nguyên URL, page, BE,
quyền, DB.

## Cách làm (đối xứng với `chuyen-menu-nhom-nganh`, chiều ngược lại)
Route → phân hệ được `resolveSubsystem()` suy **từ chính khai báo menu**, nên chuyển khai báo là
sidebar/hub/tổng quan tự đổi theo — không đụng page/BE/quyền/DB.

- Menu Bán hàng KHÔNG viết tay: `saleItems` (sale.js) được SINH từ `saleHubGroups` (sale-hub.js)
  qua `buildSaleTree()`. Đổi menu Bán hàng ⇒ **chỉ sửa `sale-hub.js`**.
- Item hiện ở master-data đang `isShow: true` (KHÔNG có quyền riêng) ⇒ sang Bán hàng khai screen
  không kèm `isShow` (mặc định luôn hiện, giữ đúng hành vi cũ). KHÔNG cần thêm entry vào
  `SALE_LINK_PERMISSIONS` trong sale.js.

## Quyết định đã chốt
- Đặt vào nhóm **"Quy chế - Thiết lập" › "Thiết lập"** của Bán hàng (đúng ngữ nghĩa "quy chế"),
  ngay đầu danh sách screens.
- "Chuyển" = **gỡ hẳn** khỏi `master-data.js` (không để trùng link ở 2 phân hệ, tránh
  `findSubsystemByLink` nhập nhằng).

## Ràng buộc
- Chỉ sửa 2 file khai báo menu; KHÔNG sửa `pages/master-data/regulation-config/*`, BE,
  `PermissionsTableSeeder.php`, migration, SQL.
- Giữ line-ending LF (cả 2 file hiện LF).

## File
| File | Việc |
|---|---|
| `components/subsystem-menu/master-data.js` | Gỡ mục cấp 1 "Khai Quy chế – Cấu hình" |
| `components/subsystem-menu/sale-hub.js` | Thêm 1 screen vào nhóm "Quy chế - Thiết lập" › "Thiết lập" |
