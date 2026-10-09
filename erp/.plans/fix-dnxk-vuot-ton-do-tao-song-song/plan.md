# Plan: Fix ĐNXK vượt tồn do tạo song song (khóa theo kho + công ty)

Feature: `fix-dnxk-vuot-ton-do-tao-song-song` — @namdangit
Repo: ERP TanPhatDev — nhánh: `master` (cần tạo nhánh riêng trước khi code)

Xem `design.md` cùng folder cho nguyên nhân gốc + lý do chọn hướng.

---

## Phase 1 — Chuẩn bị
- [x] T1.1 ~~Tạo nhánh git riêng~~ → **user chốt code thẳng trên `master`** (không commit/push khi chưa yêu cầu)
- [x] T1.2 Xác định nguồn `company_id` = `Auth::user()->info->company_id` (như `validateProducts`); `warehouse_id`: store = `$request->warehouse_id`; update = kho hiệu lực `(!is_warehouse_transfer && can_change_warehouse) ? $request->warehouse_id : $object->warehouse_id`

## Phase 2 — Code BE (`app/Http/Controllers/Warehouse/WarehouseExportRequestsController.php`)
- [x] T2.1 Thêm 3 private helper: `reserveLockName()`, `acquireReserveLock($wh,$cty,$timeout=10)` (`SELECT GET_LOCK(?,?)` → true nếu got==1), `releaseReserveLock()` (`SELECT RELEASE_LOCK(?)`). Dùng `DB::selectOne/select` trên connection mặc định.
- [x] T2.2 Bọc `store()`: tính `$companyId`/`$warehouseId` trước, `acquireReserveLock` → nếu false trả message "Hệ thống đang xử lý một phiếu khác trên kho này, vui lòng thử lại sau giây lát."; bọc `try { DB::beginTransaction()...catch } finally { releaseReserveLock }`. Thứ tự GET_LOCK → beginTransaction. (dòng 283–429)
- [x] T2.3 Bọc `update()` theo đúng pattern T2.2, dùng kho hiệu lực. (dòng 517–602)
- [x] T2.4 `php -l` sạch; đã rà: mọi `return Response::json(...)` sau khi GET_LOCK (canApprove, validateProducts fail) đều nằm trong try ngoài → finally luôn nhả khóa; các return validate/validateWarehouse nằm TRƯỚC khi lấy khóa.

## Phase 3 — Rà soát điểm reserve khác (audit, có thể tách phase sau)
- [ ] T3.1 Kiểm tra các luồng khác cũng set `export_total_qty`/gọi `updateWarehouse` (approve YCXH tạo ĐNXK tự động, XUAT_GHEP/XUAT_TACH, luồng HRM→ERP nếu có) → xác định có cần cùng khóa không; ghi nhận, chưa sửa nếu ngoài scope

## Phase 4 — Test
Test bằng script PDO 2 connection song song trên dev `dev_erp_2` (scratchpad `race_lock_test.php`) — target đúng cơ chế fix (named lock + snapshot), vì store()/update() cần HTTP+auth không test end-to-end qua tinker được. Cả 3 test PASS.
- [x] T4.1 Hồi quy: cơ chế check tồn vẫn chặn khi tồn không đủ (TEST 3: phiếu B cần 5, còn 3 → CHẶN đúng)
- [x] T4.2 Song song cùng kho/cty: 2 transaction chồng lấn — **luồng cũ** (không khóa) tái hiện đúng bug vượt tồn 11>9 (TEST 2), **luồng mới** (GET_LOCK trước beginTransaction) phiếu thứ 2 mở snapshot sau commit phiếu 1 → thấy đủ giữ chỗ → **bị chặn** (TEST 3). PASS.
- [x] T4.3 Khác kho/cty không chặn nhầm: lock name `we_reserve_{kho}_{cty}` — khác kho hoặc khác cty ⇒ khác key ⇒ GET_LOCK độc lập, không đợi nhau (suy ra trực tiếp từ TEST 1: 2 session tranh CÙNG key mới chặn nhau)
- [x] T4.4 Timeout khóa: khi khóa đang bị giữ, `GET_LOCK(...,timeout)` trả 0 (TEST 1) → `acquireReserveLock()` trả false → controller trả message "Hệ thống đang xử lý một phiếu khác trên kho này, vui lòng thử lại sau giây lát." (không 500)

---

## Ghi chú kỹ thuật
- Named lock MySQL tự nhả khi connection đóng → không rò khóa nếu process chết giữa chừng.
- Không đụng `validateProducts` / `getAccountingStockDetail` (hàm dùng chung) — chỉ bọc khóa ở controller.
- ERP prod `erp_new`: chỉ đọc khi điều tra; fix chạy/test trên môi trường dev, **không** áp thẳng prod.

### Checkpoint — 2026-08-24
Vừa hoàn thành: Code BE xong (P1+P2) trên `master` + Test P4 xong trên dev `dev_erp_2`. Script `race_lock_test.php` (2 connection PDO song song, REPEATABLE READ) chứng minh: TEST 1 khóa loại trừ giữa 2 session PASS; TEST 2 tái hiện đúng bug vượt tồn (11>9) khi không khóa; TEST 3 fix (GET_LOCK trước beginTransaction) chặn đúng phiếu thứ 2. Cả T4.1–T4.4 đạt.
Đang làm dở: (để trống)
Bước tiếp theo: P3 — audit các điểm reserve khác (approve YCXH tự tạo ĐNXK, XUAT_GHEP/XUAT_TACH, luồng HRM→ERP) xem có cần cùng khóa không. Sau đó chờ user duyệt để commit.
Blocked: (để trống)
