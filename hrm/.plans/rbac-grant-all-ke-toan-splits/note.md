# Lệnh TỔNG cấp-lại quyền-cờ 4 đợt tách kế toán — `rbac:grant-all-ke-toan-splits`

**Yêu cầu user:** "viết 1 cái rbac chung cho tất cả 4 quyền đã tách từ đầu đến giờ để chỉ cần chạy 1 lệnh thôi".

## Cách làm — ỦY NHIỆM, không lặp logic
File mới `hrm-api/app/Console/Commands/RbacGrantAllKeToanSplitsCommand.php` (Kernel tự nạp qua `$this->load(__DIR__.'/Commands')`), gọi lại CẢ 4 lệnh con qua `$this->call()`, theo thứ tự tách từ sớm → mới:
1. `rbac:grant-ke-toan-split`
2. `rbac:grant-ke-toan-kho-split`
3. `rbac:grant-ke-toan-mua-hang-split`
4. `rbac:grant-truong-phong-ke-toan-split`

KHÔNG sửa 4 lệnh con (2 đã lên prod). Mỗi lệnh con giữ nguyên tiền-kiểm, idempotent, CSV riêng.

## 3 option truyền tiếp y nguyên
`--dry-run` / `--verify` / `--report-dir` → forward cho cả 4. Report-dir dùng CHUNG 1 thư mục (mặc định `storage/app/rbac-grant-all-ke-toan-splits/<Ymd_His>`): 4 lệnh con ghi CSV tên khác nhau (`cap-ma`/`doi-chieu` × ke-toan / -kho / -mua-hang / -truong-phong-ke-toan) nên không đè nhau — cả 8 file dồn 1 chỗ.

Exit code: 0 nếu MỌI lệnh con exit 0; 1 nếu bất kỳ lệnh con nào exit 1 (vd mã chưa catalog-sync). Vẫn chạy hết 4 lệnh dù 1 lệnh hỏng.

## Cách dùng
```
php artisan rbac:grant-all-ke-toan-splits --dry-run --report-dir=/tmp/kt   # chỉ báo cáo cả 4
php artisan rbac:grant-all-ke-toan-splits --report-dir=/tmp/kt             # ghi cả 4
php artisan rbac:grant-all-ke-toan-splits --verify --report-dir=/tmp/kt    # đối chiếu cả 4 (chỉ đọc)
```

## Kiểm chứng (TDD, DB-free)
- Test `tests/Unit/Permission/RbacGrantAllKeToanSplitsWiringTest.php` (3 case) — RED→GREEN: có signature riêng, gọi đủ 4 signature con, truyền tiếp 3 option.
- `php artisan list | grep rbac:grant` → lệnh đăng ký; `--help` parse đúng 3 option.
- **Rủi ro đã kiểm tới gốc:** `$this->call()` truyền `'--dry-run' => false` cho option kiểu cờ (VALUE_NONE). Thử thực nghiệm ArrayInput (Symfony bản Laravel 8): child đọc `getOption('dry-run') === false` — KHÔNG ném, KHÔNG bật nhầm cờ. Chế độ GHI (false,false) chạy đúng chế độ ghi ở cả 4 lệnh con.
- 77/77 test DB-free `tests/Unit/Permission` xanh (253 assertions). `php -l` sạch.
- (1 Feature test `RbacGrantKeToanKhoSplitTest::test_dry_run_khong_ghi` fail `insert`≠`skip` — do DB local đã sẵn 36 mã kho, KHÔNG liên quan thay đổi này.)

## Chưa làm
KHÔNG commit/push. Rollout thật vẫn cần `permission:catalog-sync` trước (mã mới chưa đồng bộ thì lệnh con tiền-kiểm sẽ exit 1).

### Checkpoint — 2026-11-28 17:30 (wrap up cuối ngày)
Vừa hoàn thành: Lệnh tổng `rbac:grant-all-ke-toan-splits` (ủy nhiệm 4 lệnh con qua `$this->call()`, không sửa lệnh con) + wiring test 3 case xanh. Xác nhận ở code: cả 4 lệnh con idempotent (`exists ? 'skip' : 'insert'` cho pivot Vai trò + pivot NV) → chạy lại nhiều lần an toàn, còn bắt kịp holder mới; report-dir mặc định có dấu thời gian nên mỗi lần ra thư mục CSV mới.
Đang làm dở: CHƯA commit/push (hrm-api develop: `RbacGrantAllKeToanSplitsCommand.php`, `RbacGrantAllKeToanSplitsWiringTest.php` untracked). Phụ thuộc lệnh con `rbac:grant-truong-phong-ke-toan-split` (cũng chưa commit).
Bước tiếp theo: Commit cùng đợt tách quyền Trưởng phòng KT → rollout: `permission:catalog-sync` → `rbac:grant-all-ke-toan-splits --dry-run` → chạy thật → `--verify`.
Blocked:
