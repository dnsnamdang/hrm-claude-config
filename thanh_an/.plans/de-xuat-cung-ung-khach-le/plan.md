# Plan — Đề xuất cung ứng loại "Cung ứng khách lẻ"

> @khoipv — Tạo 16/09/2026 · [design.md](design.md) · [spec đầy đủ](../../docs/superpowers/specs/2026-09-16-de-xuat-cung-ung-khach-le-design.md)

## Phase 0 — Brainstorming & chốt spec
- [x] Đọc mockup sheet (dòng 79+)
- [x] Chốt câu hỏi nghiệp vụ với user
- [x] Fill spec chi tiết + design.md
- [x] User duyệt thiết kế (16/09/2026)

## Phase 1 — Backend
- [x] 1.1 `PermissionsTableSeeder.php:736` — đổi tên quyền id 516 → `Duyệt đề xuất cung ứng` (quy ước: quyền chỉ sửa ở seeder, KHÔNG viết migration)
- [x] 1.3 `SupplyProposal.php` — thêm `TYPE_KHACH_LE = 3`, vào `TYPES`, đổi `PERM_APPROVE_INTERNAL` → `PERM_APPROVE`, sửa `needsBoardApproval()`
- [x] 1.4 `Routes/api.php:51,53` — đổi chuỗi middleware quyền
- [x] 1.5 `SupplyProposalService::goodsPool()` — type 3 dùng `catalogItems()`
- [x] 1.6 `SupplyProposalService::store()/update()` — tách `$isInternal` / `$needApprove`, ép null `contract_id` khi không phải type 1
- [x] 1.7 Guard `assertContractHasRemaining()` khi `$contractId = null` — đã có sẵn, không cần sửa
- [x] 1.8 Hàm mới `SupplyProposalService::retailPriceMap()` (NK: GDS/GD; PPL: MAX đơn mua + HĐ mua đã duyệt, quy đổi ĐVT)
- [x] 1.9 `SupplyProposalController::productInfo()` — merge `retailPriceMap()` khi `type = 3`
- [x] 1.10 Validate BE theo bảng mục 6 của spec

## Phase 2 — Frontend
- [x] 2.1 `constants.js` — `TYPE.KHACH_LE`, `TYPE_OPTIONS`, `PERM_APPROVE`, `buildProposalSrcCols()`, helper `typeText()`
- [x] 2.2 `add.vue` — computed `isKhachLe` / `hasCustomer`, ẩn/hiện field + tab theo bảng mục 7.2
- [x] 2.3 `add.vue` — handler đổi loại, validate 3 nhánh, build payload, nhãn Loại trong export, text msgBoxConfirm duyệt
- [x] 2.4 `add.vue` — truyền `type` khi gọi `product-info`
- [x] 2.5 `GoodsPickerModal.vue` — bộ lọc HĐ chỉ cho type 1
- [x] 2.6 `ProductInfoTab.vue` — `hasContract`/`isKhachLe`, ẩn cột tên thương mại HĐ, thêm 2 cột giá (ép `Number()`)
- [x] 2.7 `index.vue` — `PERM_APPROVE`, text msgBoxConfirm

## Phase 3 — Verify
- [x] 3.1a Smoke test BE (tinker): TYPES, `type_name`, `needsBoardApproval`, `customers(1)=120` / `customers(3)=803`, `goodsPool(3)=3171`, `retailPriceMap`, permission 516
- [x] 3.1b `php -l` sạch toàn bộ file BE đã sửa
- [ ] 3.1c Chạy 11 kịch bản kiểm thử ở mục 10 của spec trên UI
- [ ] 3.2 Kiểm tra không hồi quy type 1 và type 2
- [ ] 3.3 Deploy dev + user test

### Checkpoint — 16/09/2026 (1)
Vừa hoàn thành: chốt spec đầy đủ, user duyệt thiết kế.
Đang làm dở: bắt đầu Phase 1.
Bước tiếp theo: Task 1.1 — đổi tên permission trong seeder.
Blocked: không có.

### Checkpoint — 16/09/2026 (2)
Vừa hoàn thành: XONG Phase 1 (BE) và Phase 2 (FE). Quyền 516 đã mang tên mới trên `thanhan_stag_07052026`.
Smoke test BE qua tinker đạt: `retailPriceMap` trả hh 36 → 693 / 630, hh 17 (ĐVT Hộp) → 924000 / 840000.
Đang làm dở: Phase 3 — còn 3.1c chạy 11 kịch bản trên UI.
Bước tiếp theo: user test màn `supply/supply_proposals` với loại "Cung ứng khách lẻ" (lập → gửi → BGĐ duyệt), đồng thời soát hồi quy loại 1 và 2.
Blocked: không có.

### Ghi chú phát sinh khi code (ngoài spec)
- `SupplyProposalService::customers()` cũ chỉ lấy khách có HĐ bán đã duyệt → khách lẻ không chọn được ai. Đã thêm tham số `$type`: type 3 trả toàn bộ `category_customers` đang hoạt động.
- `retailPriceMap()` phải dùng `Product::withTrashed()` khi tra `import_type_id`: hàng hóa xóa mềm (vd id 36) rơi khỏi cả nhánh NK lẫn PPL → cả 2 cột giá ra `-`.
- `PERM_APPROVE_INTERNAL` thực tế chưa được import ở đâu trong FE (chỉ export ở `constants.js`) → task 2.7 chỉ còn đổi text `msgBoxConfirm`.

### Checkpoint — 17/09/2026 (bỏ migration quyền)
Vừa hoàn thành: Xóa migration thao tác bảng `permissions` (sai quy ước dự án) — quyền chỉ khai ở `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.
  - Xóa file `Modules/Supply/Database/Migrations/2026_09_16_000003_rename_permission_duyet_de_xuat_cung_ung.php`
  - Xóa dòng tương ứng trong bảng `migrations` của `thanhan_stag_07052026` (DB đã có sẵn dữ liệu quyền đúng, không cần chạy lại gì)
  - Cập nhật spec + plan + STATUS bỏ mọi tham chiếu tới migration quyền
Đang làm dở: không có.
Bước tiếp theo: user test màn `supply/supply_proposals` loại "Cung ứng khách lẻ".
Blocked: không có.
