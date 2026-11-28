# Tách quyền `accounting.truong_phong_ke_toan.approve` theo màn

## Mục tiêu & lý do
Nhìn tên quyền là biết tác dụng cho màn nào. Tách mã-cờ vai trò dùng chung
`accounting.truong_phong_ke_toan.approve` thành 2 mã theo từng màn. Mirror 3 lần
tách trước (`ke_toan`, `ke_toan_kho`, `ke_toan_mua_hang`).

**Phạm vi: ERP-only** (HRM không dùng mã này — grep rỗng).

## Hiện trạng (7 điểm, 2 màn)
| Màn | Điểm dùng | Gate làm gì |
|---|---|---|
| ① Phiếu xuất giữ (`WarehousePrepickRequest`) | `WarehousePrepickRequest.php:248,270` · `HomeController.php:2140,2143` (widget "Phiếu xuất giữ chờ BKS duyệt") · `topmenubar_old.blade.php:1439,1454` (menu) | Xem **tất cả** phiếu xuất giữ + nhánh duyệt, widget dashboard, menu |
| ② Đề nghị xuất kho (`WarehouseExportRequest`) | `WarehouseExportRequest.php:1033` (`canView`) | Trưởng phòng KT xem phiếu ĐNXK chưa ở trạng thái 3 |

Đặc thù (khác 3 lần trước): đây là **cờ danh tính vai trò**, luôn đi **OR** với
`finance.giu_hang_ban_kiem_soat.approve` (BKS) và cạnh `is_warehouse_accountant`
trong luồng duyệt phiếu xuất giữ. Các toán hạng OR đó **giữ nguyên**.

## Quyết định đã chốt (user ok 2026-11-28)
1. **Tách đôi** (không gộp 1 mã).
2. Điểm ĐNXK **giữ** thành quyền xem phụ của trưởng phòng KT (`.view`), chỉ đổi mã, không đổi hành vi.
3. Slug **giữ tiền tố `truong_phong_ke_toan_<màn>`** (rõ đây là cấp vai trò).

## 2 mã mới (khai ở Catalog hrm-api, platform `erp`)
| Mã | Tên hiển thị | Thay cho `truong_phong_ke_toan.approve` tại |
|---|---|---|
| `accounting.truong_phong_ke_toan_phieu_xuat_giu.approve` | Trưởng phòng kế toán — Phiếu xuất giữ | `WarehousePrepickRequest:248,270` · `HomeController:2140,2143` · `topmenubar_old:1439,1454` |
| `accounting.truong_phong_ke_toan_de_nghi_xuat_kho.view` | Trưởng phòng kế toán — Xem đề nghị xuất kho | `WarehouseExportRequest:1033` |

## Giữ nguyên (KHÔNG đụng)
- Mọi toán hạng OR khác: `finance.giu_hang_ban_kiem_soat.approve`, `finance.phieu_hang_giu.view` (permissionScope), `is_warehouse_accountant`.
- Mã cũ `accounting.truong_phong_ke_toan.approve` **giữ trong Catalog** (deprecate sau rollout), **giữ dòng fixture MAP** trong `AccountingCatalog.php`.

## Thay đổi
**ERP (`TanPhatDev`):**
- `app/Model/Warehouse/WarehousePrepickRequest.php` — :248, :270 → mã `..._phieu_xuat_giu.approve`
- `app/Http/Controllers/HomeController.php` — :2140, :2143 → mã `..._phieu_xuat_giu.approve`
- `resources/views/layouts/topmenubar_old.blade.php` — :1439, :1454 → mã `..._phieu_xuat_giu.approve`
- `app/Model/Warehouse/WarehouseExportRequest.php` — :1033 → mã `..._de_nghi_xuat_kho.view`
- `tests/Feature/Rbac/Concerns/AccountingCatalog.php` — MAP **thêm 2 mã mới** (giữ mã cũ)

**hrm-api:**
- `app/Support/Permissions/Catalog/accounting.php` — thêm 2 entry (shape khớp mã cũ `truong_phong_ke_toan`)
- `app/Support/Permissions/TruongPhongKeToanSplitMap.php` — map 1 cũ → 2 mới
- `app/Console/Commands/RbacGrantTruongPhongKeToanSplitCommand.php` — cấp 1→2 (idempotent, `--dry-run`/`--verify`)
- `tests/Unit/Permission/TruongPhongKeToanSplit*Test.php` — DB-free, soi source ERP đổi đúng mã, giữ toán hạng OR, Catalog + fixture + wiring

## Rủi ro / gotcha
- Fixture MAP: ERP đổi gate sang mã mới → **phải** thêm 2 mã vào `AccountingCatalog::MAP`, nếu không suite RBAC ném `UnknownPermissionCode`.
- Các điểm ở màn ① có cấu trúc `if (A) { if (A) {...} }` lồng nhau (HomeController) và nhiều nhánh OR — đổi **tất cả** occurrence của mã cũ tại các file màn ①, không bỏ sót.

## Ngoài phạm vi (user tự chạy sau)
`permission:catalog-sync` (prod qua `build_tpe.sh`) → cấp 2 mã ở `/admin/roles` → chạy `rbac:grant-truong-phong-ke-toan-split` → gop_db → deprecate mã cũ sau rollout.
