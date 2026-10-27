# Redmine #11841 — Phiếu nhập kho điều chỉnh kiểm kê: dung lượng file + sort Ngày tạo / Ngày duyệt

@khoipv

## Phase 1
### Bug 1 — validate dung lượng file đính kèm
- [x] Kiểm tra: code cũ chặn 15MB (FE `:max-size-mb="15"`, BE `MAX_KB = 15240`); ERP màn này không giới hạn
- [x] User chốt giới hạn **20MB** (26/10): BE `WarehouseInventoryImportWriteService::MAX_MB = 20` (`MAX_KB` suy ra, 2 câu báo lỗi lấy theo hằng), FE `:max-size-mb="20"` — verify: 21MB → 422 "Dung lượng tối đa 20MB", 16/20MB qua luật

### Bug 2 — sort cột Ngày tạo, Ngày duyệt
- [x] BE `WarehouseInventoryImportService`: thêm `created_at`, `approved_time` vào map sort
- [x] FE `pages/warehouse/inventory-imports/index.vue`: bật `sortable` cột Ngày tạo / Ngày duyệt; localStorage chỉ giữ sort thuộc 3 cột được sort

### Checkpoint — 2026-10-26
Vừa hoàn thành: bug 2 (sort BE + FE); bug 1 đổi giới hạn file 15MB → 20MB (BE + FE)
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm sort + upload file; commit khi user yêu cầu
Blocked:
