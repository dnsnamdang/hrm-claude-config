# Plan — Danh mục khu vực kinh doanh (#11623)

> @junfoke · design: `design.md`

## Phase 1 — BE (hrm-api)

- [x] Migration `business_areas` + `business_area_wards` (UNIQUE ward_id) — chưa chạy migrate (chờ user)
- [x] Entity `BusinessArea` (extends BaseModel), phường/xã qua belongsToMany bảng nối
- [x] Service: list (lọc/sort/phân trang), detail, store/update (sync phường/xã, chặn phường/xã đã thuộc khu vực khác), delete, lock/unlock, lịch sử (`catalog_histories`)
- [x] Endpoint phường/xã theo tỉnh kèm khu vực đang giữ
- [x] Request validate (tên unique trong tỉnh), middleware chặn sửa/xoá khi khoá (423)
- [x] Export (DynamicExport + ExportColumnRegistry) + Import (validate/import)
- [x] Đăng ký `business_areas` vào `CatalogHistoryService::TABLES`
- [x] Routes `/human/business-areas`

## Phase 2 — FE (hrm-client)

- [x] Menu Danh mục › Địa lý › Khu vực kinh doanh
- [x] `pages/human/business-areas/index.vue` (copy pattern `pages/human/wards/index.vue`)
- [x] `pages/human/business-areas/components/BusinessAreaModal.vue` (Tạo/Sửa/Xem + bảng tick phường/xã + chip lọc)
- [x] Import modal + file mẫu `buildImportTemplate`
- [x] Kiểm Playwright (danh sách, Sửa, chip, xác nhận đổi tỉnh, Xem→Sửa, dòng khoá ẩn Sửa/Xóa)

## Phase 3 — Bàn giao

- [x] Chạy migrate (user cho phép 10/10) + test API toàn luồng (tạo/trùng tên/phường đã gán/sai tỉnh/sửa/khoá 423/lịch sử/sort/lọc/xuất/import/xoá)

### Checkpoint — 2026-10-10
Vừa hoàn thành: code BE + FE xong (chưa chạy được vì MySQL/API/client local đang tắt). Đã fast-forward `gop_db` local lên `origin/develop` ở cả 2 repo theo yêu cầu user (chưa push).
Đang làm dở: kiểm thử — cần bật MySQL + chạy migration `2026_10_10_000001_create_business_areas_tables` (chờ user cho phép).
Bước tiếp theo: migrate → bật API :8000 + client :3000 → Playwright kiểm toàn luồng (tạo/sửa/xem/khoá/xoá/lịch sử/xuất/import).
Blocked: quyền chạy migrate.

### Checkpoint — 2026-10-10 (2)
Vừa hoàn thành: migrate + kiểm API & UI. Sửa 3 lỗi phát hiện khi test: sort Người tạo/cập nhật (employee_infos không có employee_id sau gộp DB), checkbox "chọn tất cả" tự bỏ tick khi đổi chip, Xem→Sửa bị reset về Tạo.
Đang làm dở: không.
Bước tiếp theo: user duyệt → commit 2 repo (chưa commit). Dữ liệu test local: 3 khu vực (Cầu Giấy, Hoàn Kiếm[Khóa], Hoàn Kiếm mới).
Blocked:
