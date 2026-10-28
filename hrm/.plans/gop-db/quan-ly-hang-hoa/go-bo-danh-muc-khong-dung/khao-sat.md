# Phase 5 — Gỡ MÀN Lĩnh vực (`scopes`) + Nhóm hàng hoá (`groups`) ở ERP, GIỮ BẢNG — khảo sát 13/10/2026 (chỉ đọc)

> A7 (thuộc lần lên prod này). Chốt cũ: giữ bảng `groups` (22/09), `scopes` (27/09). ERP `wt-erp-2d1` @ `4ec31c6ee4`.

## Hiện trạng
| | Nhóm hàng hoá (`groups`, 893 dòng) | Lĩnh vực (`scopes`, 14 dòng) |
|---|---|---|
| Route ERP | `routes/web.php:96-108` — 12 route `Sale\GroupsController` (index, create, store, fastStore, edit, update, delete, searchData, export×3, importExcel), **chưa chặn** (C-b chỉ chặn bản `pi-groups`) | `:4289-4293` — 5 route `Sale\ScopesController` (index, store, update, delete, searchData), chưa chặn |
| Menu | `topmenubar.blade.php:27` · `sidebar.blade.php:59` · `topmenubar_old.blade.php` | `topmenubar.blade.php:40` · `topmenubar_old.blade.php` |
| Chỗ khác gọi | `groups.searchData` ← select2 ở **Dịch vụ** (`sale/services/formJs`), **Lỗi thiết bị** (`sale/device_errors/formJS`), **Nhóm lỗi thiết bị** (`device_error_groups/formJS`) ⇒ **PHẢI GIỮ** (đọc). `groupFastStore` ← modal `createGroupModal` (nút "+" chỉ có ở các form hàng hoá ERP đã chặn; `quotations/form` include modal nhưng không có nút mở). `groups.importExcel` ← `product_infos/groups/list` (màn pi-groups) | `scope.store` ← modal tạo nhanh chỉ nằm trong chính màn Lĩnh vực |
| Bảng còn được đọc | `products.group_id` + 12 bảng FK (giữ nguyên) | `chapters`, `product_group_classifies`, `pi_product_group_classifies`, `product_classifies` (cây hàng hoá cũ). Các bảng HRM có `scope_id` (dự án, giải pháp, khảo sát…) trỏ `hrm_scopes`, KHÔNG phải `scopes` ERP |
| Thay thế ở HRM | Cây phân loại Tính chất › … › **Loại SP** (khác dữ liệu, không 1-1) | **Lĩnh vực Công ty kinh doanh** (`internal_business_scopes`, gốc cây catalog 2d) — khác bảng |

## Tự chốt (theo khuôn C-b, không phải nghiệp vụ mới)
- Gắn `productMovedToHrm:stopped-generic` ("Chức năng đã ngừng sử dụng.") cho mọi route màn của 2 danh mục — giống `pi-groups` (N81). Không trỏ link
  HRM vì không có màn thay 1-1.
- GIỮ mở `groups.searchData` (3 select2 module khác). Bỏ 3 link menu (+ `topmenubar_old` nếu còn render).
- Không đụng bảng, không đụng quyền ERP (`Xem nhóm`, `Xem lĩnh vực`… để admin tự dọn).
