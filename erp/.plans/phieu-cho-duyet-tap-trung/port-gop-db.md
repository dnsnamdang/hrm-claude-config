# Đưa "Phiếu chờ duyệt tập trung" + "Báo cáo phê duyệt" sang `gop_db`

> **22/10/2026 — THAY THẾ**: user chuyển sang làm hộp duyệt chung ERP + HRM trên worktree riêng. Hồ sơ mới:
> `HRM/.plans/phieu-cho-duyet-tap-trung-erp-hrm/README.md`. Không port nguyên bản develop_01 theo file này.

Ngày: 22/10/2026 · Repo: `ERP/TanPhatDev` · Nhánh đích: `gop_db` (prod từ go-live 20/10)

## Hiện trạng (soát 22/10)

- Feature chỉ có trên `develop_01`: merge `6134e90` (Phase 1–5 + UX, 67 commit) + merge `46ab7152`
  (live-hook 47 loại + `--prune` + cron, commit `c94528d3d1`, 65 file).
- `origin/gop_db` KHÔNG có file nào của feature; DB `hrm_erp_21_10_prod` (dump prod 21/10) KHÔNG có bảng
  `approval_inbox` ⇒ prod chưa từng có feature.
- `develop_01` còn ~140 commit việc khác ⇒ KHÔNG merge develop_01, chỉ lấy 2 merge của feature.

## Mô phỏng merge (git merge-tree, không đụng working tree)

- Bước 1 (`6134e90`): xung đột `routes/web.php`.
- Bước 2 (`46ab7152`): xung đột `routes/web.php`, `Warehouse/WarehouseExportRequestsController.php`,
  `Warehouse/WarehouseImportRequestsController.php`. Còn lại ~30 file auto-merge.

## Điểm phải sửa tay khi port

1. **Quyền**: develop_01 thêm `Permission::create(['id' => 1038/1039 ...])` kiểu cũ. `gop_db` đã đổi seeder
   sang đồng bộ theo TÊN (`$this->perm([...])`, không khai id, id web +100000). ⇒ viết lại 2 dòng:
   - `Xem phiếu chờ duyệt tập trung`, `Xem báo cáo phê duyệt` — group `Phiếu chờ duyệt tập trung`,
     group_category `Cấu hình hệ thống` (`Hệ thống` không tồn tại trên DB gộp).
   - Ghi DB bằng `php artisan permission:sync --dry-run` rồi chạy thật (KHÔNG chạy cả seeder kiểu cũ).
2. **Bỏ ngoại lệ Super Admin** (user chốt 22/10): `ApprovalInbox::pendingBuilderForUser` bỏ
   `$isSuperAdmin` — Super Admin xét scope quyền như mọi người.
3. Quyền/công ty: `can()`/`hasRole()` trên `gop_db` đã theo công ty (`Employee.php`), `info->company_id`
   còn ⇒ không cần đổi. 41/43 tên quyền feature tham chiếu có trong DB gộp; 2 tên thiếu
   ("Nhân viên mua hàng duyệt … (theo phân công hãng)") chỉ là nhãn cho phiếu chỉ định `approver_id`.
4. Backfill trên DB gộp: chạy `approval-inbox:backfill` để phát hiện bảng/cột lệch (xem memory
   merge-gop-db-doi-cach-query-erp).

## Migration sẽ chạy (DB `hrm_erp_21_10_prod`, chạy lẻ `--path`)

| File | Việc |
|---|---|
| 2026_08_12_000001_create_approval_inbox_table | tạo bảng `approval_inbox` |
| 2026_08_12_000002_create_approval_inbox_logs_table | tạo bảng `approval_inbox_logs` |
| 2026_08_12_000003_add_partner_to_approval_inbox | thêm cột đối tác |
| 2026_08_14_000001_change_document_date_to_datetime_on_approval_inbox | `document_date` DATE → DATETIME |
| 2026_08_14_000002_add_submitted_at_to_approval_inbox | thêm `submitted_at` |

Chỉ tạo/sửa bảng mới, không UPDATE/DELETE dữ liệu cũ.

## Các bước

1. `git cherry-pick -n -m 1 6134e90` → giải xung đột `routes/web.php` (không commit, theo quy ước user).
2. `git cherry-pick -n -m 1 46ab7152` → giải 3 xung đột.
3. Sửa tay: seeder quyền, bỏ ngoại lệ Super Admin. `php -l` toàn bộ file đổi.
4. Migrate 5 bản trên, `permission:sync`, `approval-inbox:backfill` (+ `--prune`), tạo role tạm cấp 2 quyền.
5. Playwright (ERP local `php -S` 8093): màn Phiếu chờ duyệt + Báo cáo — đo DOM số dòng/badge, deep-link,
   Excel; ca có quyền + không quyền; 1 vòng duyệt thật xem registry resolve. Gỡ role tạm.

## Để sau (ngoài đợt này)

- Deploy prod (migrate + permission:sync + backfill + gán quyền cho vai trò + cron) — hỏi riêng.
- Nhóm B 30 luồng pending=0; nghi vấn prune 0 dòng stale trên dev.
