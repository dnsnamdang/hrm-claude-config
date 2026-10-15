# Plan — Đồng bộ quyền bằng seeder an toàn (HRM + ERP)

> Phụ trách: @namdangit · Nhánh: `gop_db` (`hrm-api` + `TanPhatDev`) · Bắt đầu: 2026-10-14
> Design: `.plans/gop-db/permission-seeder-sync/design.md`
> Spec: `docs/superpowers/specs/gop-db/2026-10-14-permission-seeder-sync-design.md`

Code ở 2 worktree riêng: `HRM/worktrees/perm-sync-api` + `HRM/worktrees/perm-sync-erp`, nhánh `feature/permission-seeder-sync` (checkout từ `origin/gop_db`). `.env` 2 worktree trỏ DB thử `perm_sync_test` (copy 6 bảng của `local_hrm_erp`).

## Phase 0 — Chuẩn bị

### BE
- [x] Tạo worktree riêng cho `hrm-api` và `TanPhatDev` từ `origin/gop_db`
- [x] Copy bảng quyền sang DB thử `perm_sync_test`, chụp bản gốc (`bk_permissions`, `bk_rhp`, `bk_ehp`)
- [x] Rà deploy: `~/build_tpe.sh` dev + prod chạy `migrate` rồi `db:seed` seeder quyền HRM → giữ nguyên

## Phase 1 — Dọn dữ liệu + schema (hrm-api)

### BE
- [x] Migration `2026_10_14_000001`: cột `seed_order` + gộp quyền trùng tên (chuyển gán quyền) + unique `(name, guard_name)`, không bọc transaction
- [x] Lệnh `permission:cleanup {--dry-run}`: xoá gán quyền mồ côi (CSV backup), báo cáo gán chéo guard
- [x] Bỏ 2 dòng khai trùng 1117/1118 khỏi seeder HRM

## Phase 2 — Engine + seeder HRM (hrm-api)

### BE
- [x] `app/Support/Permissions/PermissionSync.php` + trait `DeclaresPermissions`: kiểm khai báo → gộp trùng → đổi tên → upsert → nhận gán id cũ → gỡ → cảnh báo → xoá cache, có dry-run
- [x] Bảng tra id cũ `permission_legacy_ids.php` (sinh từ seeder trước chuyển đổi) để lần sync đầu không mất gán quyền
- [x] Script chuyển seeder HRM: 837 dòng `$this->perm`, bỏ `id` + `guard_name`; thêm `RENAMED` / `REMOVED`
- [x] Lệnh `permission:sync {--dry-run}`
- [x] `PermissionService::sortByDisplayOrder`: khoá phụ `seed_order` (fallback `id`)
- [x] PHPUnit `tests/Feature/PermissionSyncTest.php` 19/19
- [x] Sync lần đầu trên DB thử: id cũ giữ nguyên, lần 2 báo 0 thay đổi

## Phase 3 — Engine + seeder ERP (TanPhatDev)

### BE
- [x] Chép `PermissionSync` + `DeclaresPermissions` sang `app/Support/Permissions/` (bản giống hệt)
- [x] Script chuyển seeder ERP: 958 dòng `$this->perm`, bỏ helper `createPermission` + `ID_OFFSET`, giữ BOM; bảng tra id cũ (+100000)
- [x] Lệnh `permission:sync {--dry-run}` bản ERP (chạy PHP 7.4)
- [x] `RolesController`: helper `erpPermissions()` sắp `seed_order` rồi `id` (3 chỗ)
- [x] `BackfillPermissionGroupCategory`: đọc dòng `$this->perm`, chỉ guard `web`
- [x] Sync lần đầu trên DB thử: thêm 2 (đúng id cũ 101049/101050), 0 sửa, 9 cảnh báo

## Phase 4 — Kiểm thử chéo

### BE
- [x] Chạy HRM ↔ ERP 2 vòng: 0 thay đổi; quyền `web` không đổi id / tên / nhóm
- [x] Quyền thực tế từng NV (NV × công ty × guard × tên) trước = sau: 178.775 cặp, 0 mất, 0 thêm
- [x] `checkPermission` thật: NV có vai trò → 200, không vai trò → 403
- [x] `permission:cleanup` thật trên DB thử: xoá 1.030 dòng mồ côi, chạy lại 0

### FE
- [x] So thứ tự màn Phân quyền HRM (`getLists`) + màn vai trò ERP bằng dữ liệu
- [x] E2E Playwright trên DB copy đủ (15/10): A chuyển đổi 12 TK + 334/943 NV + 6 vai trò UI · B 11 kịch bản dev · C 4 kịch bản ERP/độc lập — xem spec mục 8
- [x] Sửa 2 lỗi RENAMED (đổi tên nối tiếp, mục cũ trỏ quyền đã bỏ) + quy tắc không xoá mục cũ; PHPUnit 24/24

## Phase 5 — Tài liệu + bàn giao

### BE
- [x] Viết lại bẫy #11 trong `.plans/gop-db/design.md`
- [x] Cập nhật `CLAUDE.md` mục Permission + skill `erp-to-hrm-screen` Bước 2
- [x] HDSD Excel cho dev/vận hành: `HDSD - Khai báo quyền bằng seeder.xlsx` (9 sheet)
- [ ] Báo team: nhánh đang thêm `Permission::create(['id' => …])` vào seeder sẽ conflict → đổi dòng đó sang `$this->perm([...])`, bỏ `id` / `guard_name`
- [x] Commit + merge về `gop_db` cả 2 repo cùng đợt (15/10): hrm-api `180147fab`, TanPhatDev `bd2a8d4c6a`
- [x] Deploy PROD 15/10: backup `~/backup_perm/perm_before_20261015_114201.sql` (hrm-prod) → dry-run → `~/build_tpe.sh` (migrate + seeder: chỉ gộp 1117→1115, 1118→1116) → ERP `permission:sync` (0 thay đổi) · quyền thực tế 236.207 cặp trước = sau
- [x] PROD `permission:cleanup` 15/10: xoá 1.033 dòng mồ côi, CSV `storage/app/permission-cleanup/20261015_114512/`; quyền thực tế vẫn = trước
- [ ] Dev server: deploy + cleanup
- [ ] Chủ màn ERP quyết 9 quyền cảnh báo (7 quyền dọn 01/10 + 2 "tờ khai khải quan"); "Xem tất cả PI" vẫn dùng trong code ERP
- [ ] Xoá 2 file `permission_legacy_ids.php` khi mọi môi trường đã sync ≥ 1 lần

### Checkpoint — 2026-10-14 17:00
Vừa hoàn thành: Phase 0–4 + tài liệu. Code ở 2 worktree `perm-sync-api` / `perm-sync-erp`, CHƯA commit.
Đang làm dở: không.
Bước tiếp theo: user review diff → commit/merge 2 repo cùng đợt → `permission:cleanup` từng môi trường.
Blocked:
