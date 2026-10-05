# Rà & sửa: danh mục khoá mất ở form Sửa/Xem + tên danh mục cha bị cũ (màn port ERP)

@namdangit · nhánh gop_db · bắt đầu 2026-09-23

## Quyết định đã chốt (2026-09-23)
- Phạm vi: màn port ERP + ô danh mục trên chứng từ. CHƯA làm form HRM gốc (phòng ban, hồ sơ NV…) và ô chọn nhân viên đã nghỉ.
- Serial CSKH + Module giải pháp: hiện tên SỐNG theo danh mục, fallback tên đã lưu.
- Được tạo helper chung + sửa withLockedOption, CascadePairSelect, RegulationConfigService.

## Phase 1 — Helper chung
- [x] BE `app/Support/LockedCatalogOptions.php` (includeIds / activeOrIncluded / isLocked)
- [x] FE `utils/mixins/lockedCatalogOptionsMixin.js` (loadLockedCatalog / withLockedCatalog / resetLockedCatalogs)
- [x] Màn Khu vực chuyển sang helper (mẫu)

## Phase 2 — Sửa theo nhóm
- [x] Danh mục địa lý + Dữ liệu chung (withLockedOption)
- [x] Tài chính: danh mục + chứng từ + Cấu hình quy định (+ loại A Tài khoản ngân hàng)
- [x] CSKH (ĐVT dịch vụ, loại A Serial) + loại A Module giải pháp
- [x] Giao việc / Đào tạo (+ CascadePairSelect)
- [x] Yêu cầu xuất kho: editData trả warehouse_is_locked / import_warehouse_is_locked
- [ ] Test giao diện (Playwright) — chờ user quyết
- [ ] Chốt: serial hàng ncck có hiện `product_no_sale_name` không

### Checkpoint — 2026-09-23
Vừa hoàn thành: sửa loại A (account-banks, serials, project_item_name) + loại B ~35 ô ở màn port ERP; php -l + compile Vue sạch; BE kiểm bằng tinker.
Đang làm dở: không.
Bước tiếp theo: user quyết test UI + commit/push.
Blocked: DB local thiếu bản ghi khoá ở nhiều danh mục nên chỉ kiểm được SQL.
