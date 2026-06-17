# Plan — Đồng bộ thông tin hợp đồng gốc xuống phụ lục

**Người phụ trách:** @khoipv
**Plan chi tiết:** `docs/superpowers/plans/2026-06-08-dong-bo-thong-tin-hop-dong-xuong-phu-luc.md`

## Phase 1 — Backend
- [x] BE: Thêm import `ContractVersion` + `DB` facade vào `ContractService.php`
- [x] BE: Viết lại `updateDataAfterApprove` — gom 4 trường, bọc `DB::transaction`, update contract + đồng bộ mọi `ContractVersion`
- [x] BE: `php -l` pass

## Phase 2 — Frontend
- [x] FE: Thêm `time_progress` vào payload `callApiSubmitDataAfterApprove` (`GeneralComponent.vue`)
- [x] FE: Đồng bộ `time_progress` vào `originalData` / `initializeOriginalData` / `checkForDataChanges` cho nhất quán dirty-check (theo review chất lượng)

## Phase 4 — Backfill dữ liệu cũ (artisan command)
- [x] BE: Tạo command `contracts:sync-annex-snapshot` (`app/Console/Commands/SyncContractAnnexSnapshot.php`)
  - Option `--dry-run` (chỉ in, không ghi) và `--contract=` (giới hạn 1 HĐ)
  - Mỗi HĐ có `ContractVersion`: sync `number`/`contract_sign_time`/`contract_end_time` copy từ `contracts`; `time_progress` **tính lại** từ ngày ký/kết thúc (không copy giá trị cũ có thể sai)
  - Cập nhật cả `contracts.time_progress` nếu lệch; merge vào JSON `data` mọi snapshot (không xóa key khác); bọc transaction theo từng HĐ
- [x] BE: `php -l` pass
- [x] Chạy `--dry-run` review output → chạy thật → kiểm tra phụ lục HĐ cũ đã đổi (NGƯỜI DÙNG)

## Phase 3 — Kiểm thử thủ công
- [x] Test: Sửa 4 trường ở HĐ gốc → phụ lục hiển thị giá trị mới
- [x] Test: `time_progress` ở phụ lục khớp số ngày mới
- [x] Test: Phụ lục thời gian giữ giá trị gia hạn riêng, không bị ghi đè
- [x] Test: HĐ chưa có snapshot → lưu không lỗi
- [x] Test: Partial update (1 trường) → chỉ trường đó đổi

## Checkpoint

### Checkpoint — 2026-06-08
Vừa hoàn thành: code BE + FE xong (qua 2 vòng review spec + chất lượng), lint BE pass
Đang làm dở: không
Bước tiếp theo: người dùng kiểm thử thủ công 5 case trên UI (Phase 3)
Blocked:

### Checkpoint — 2026-06-08 (DONE)
Vừa hoàn thành: backfill (Phase 4) + kiểm thử thủ công 5 case (Phase 3) đều pass → feature hoàn thành
Đang làm dở: không
Bước tiếp theo: không — đã chuyển sang "Hoàn thành" trong STATUS.md
Blocked:
