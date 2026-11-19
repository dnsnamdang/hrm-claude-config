# Chuẩn bị go-live Vai trò & Quyền — tối 06/11/2026

> Đánh giá lúc 18:30–19:00 ngày 06/11, chỉ đọc code + `git fetch`, chưa đụng source, chưa vào prod.
> Số liệu merge lấy từ `git merge-tree` (không ghi vào nhánh nào). File đi kèm: `de-xuat-ma-39-ten-moi-06-11.tsv`.

## Kết luận
Bản đã diễn tập 04/11 **không còn là bản sẽ lên prod**. Chưa push được theo bảng SHA trong `cua-so-go-live-nhanh.md`.

## Việc chặn go-live
| # | Vấn đề | Số đo | Việc phải làm |
|---|---|---|---|
| 1 | `origin/gop_db` đã đi xa | Local chậm: hrm-api 110, client 92, ERP 37 commit. Commit cuối 17:15 hôm nay | Đóng băng 3 repo, merge lại |
| 2 | Xung đột merge | hrm-api 2, ERP 3, client 0 (chi tiết dưới) | Gỡ tay, chạy lại kiểm |
| 3 | Tên quyền mới chưa có mã | 38 `api` + 1 `web`. Dry-run sẽ exit 1 nếu tên có trong DB; tên chưa có alias thì màn mới bị khoá | Khai Catalog theo file `.tsv` |
| 4 | Dump diễn tập đã cũ | Mới nhất 03/11. Prod đã nhận thêm quyền và dữ liệu vai trò từ đó | Dump mới, diễn tập lại |
| 5 | `gop_db` local dính việc khác | hrm-api `91101f57d` Lịch công tác lãnh đạo: 3 migration, 25 dòng Catalog, chưa có trên origin; FE còn staged chưa commit ở hrm-client | Không push `gop_db` local. Dùng nhánh phát hành riêng |
| 6 | Hook chặn push rbac | Chỉ mở khi user tự tạo `~/.claude/allow-rbac-push` | User tạo ngay trước khối 3 |

### Xung đột
| Repo | File | Cách gỡ dự kiến |
|---|---|---|
| hrm-api | `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | Giữ đã gỡ; 38 tên chuyển sang Catalog |
| hrm-api | `Modules/Transport/Services/DeliveryContract/DeliveryContractService.php` | Giữ biến phạm vi của rbac + thêm `trim($keyword)` của origin |
| ERP | `database/seeds/PermissionsTableSeeder.php` | Giữ đã gỡ; 1 tên chuyển sang Catalog |
| ERP | `app/Http/Controllers/HomeController.php` | Giữ mã `purchase.phieu_phan_cong_nhan_vien_phu_trach_hang.create` + bản sửa select của origin |
| ERP | `app/Model/Warehouse/ProductTransferRequest.php` | Lấy phạm vi mới của origin, bỏ `hasRole('Super Admin')`, `Kế toán kho` → `accounting.ke_toan_kho.manage` |

## Rủi ro cần kiểm trong cửa sổ
- **Đường vào lúc bảo trì — chưa kiểm xong.** `php artisan down --secret` đặt cookie cho miền API; `cors.php` có `supports_credentials=false` và client không bật `withCredentials`. Nếu client khác miền API thì trình duyệt smoke sẽ nhận 503, và bước NV 13 tắt 6 công ty cũng kẹt. Cần đo miền thật. Phương án dự phòng cho bước tắt: gọi `GroupScopeCompanyService::update($id, false)` qua tinker sau khi `auth('api')->login` NV 13 để lịch sử ghi đúng người.
- **Bước tắt 6 công ty chưa diễn tập trên dump 03/11** (README 04/11 chỉ ghi mở được màn). Lần này chạy luôn.
- **Migration:** origin thêm 11 bản hrm-api + 1 bản ERP. Prod đã chạy tới đâu thì phải đọc `migrate:status` trên VPS. `2026_10_16_000002_split_…` có đổi dữ liệu.
- **Điểm lui:** bảng SHA đang ghi `d29b60688 / 48f80791c / d95e29ae12`, đã cũ. ERP tự deploy nên điểm lui ERP hiện là `ce03b6832f`; HRM phải đọc `git rev-parse` trên VPS.
- **Code mới còn nhánh Super admin** (`WarrantyRepairPermission::isSuperAdmin`, `$superAdmin ||` ở Phiếu yêu cầu giao việc khác). Không chặn vì Super Admin có đủ mã, nhưng trái nguyên tắc bỏ đặc quyền ⇒ ghi vào việc ngoài luồng.

## Đã ổn (kiểm lại hôm nay)
- `ChecksEmployeePermission`: rbac đã đổi sang `PermissionLookup`; merge không đè, các màn mới dùng trait đều đi qua alias.
- `deploy.yml` ERP local đã bỏ `db:seed PermissionsTableSeeder`, merge không xung đột. Nếu còn dòng này, deploy sẽ gọi seeder đã xoá.
- Không đổi `composer` / `package.json` trên origin từ 04/11.
- hrm-client merge sạch.
- Laravel hrm-api 8.83 có `down --secret`.

## Thứ tự làm
1. **User:** báo team dừng push `gop_db` 3 repo, lấy dump prod mới.
2. **Claude, sau khi user cho "làm":** tạo nhánh phát hành trong worktree riêng: hrm-api từ `aac684f92`, client từ `0db94d679`, ERP từ `84bec64416`; merge `origin/gop_db`, gỡ xung đột, khai Catalog. Không đụng checkout chính vì đang có việc dở (client staged, ERP `ServiceAccountingRequest.php`).
3. Nhập dump, chạy migration, dry-run, convert, B.4b, 5b, tắt 6 công ty, smoke 3 tài khoản.
4. Cập nhật bảng SHA; đổi lệnh push thành `git push origin <nhanh-phat-hanh>:gop_db`.
5. Chạy cửa sổ bảo trì theo `cua-so-go-live-nhanh.md`.

**Mốc dừng:** tới 22:00 mà diễn tập chưa đạt ⇒ dời, không vào cửa sổ.

## Lệnh chỉ đọc cho user chạy trên VPS HRM
```bash
cd /var/www/tpe/hrm-api && git rev-parse --short HEAD && git branch --show-current && php artisan migrate:status | grep -E "\| No"
grep -E '^(RBAC_GROUP_SCOPE_ADMINS|DB_DATABASE_TPE|DB_CONNECTION_TPE)=' .env | cut -d= -f1; df -h ~
mysql -h 192.168.122.103 -u hrm_tpe -p --table hrm_erp_gop -e "SELECT guard_name,COUNT(*) FROM permissions WHERE created_at>='2026-11-03' GROUP BY guard_name; SELECT guard_name,name FROM permissions WHERE created_at>='2026-11-03' ORDER BY 1,2;"
```
VPS ERP: `cd /var/www/html/TanPhatDev && git rev-parse --short HEAD && grep -c '^HRM_URL_FE=.\+' .env`

## Cập nhật tối 06/11 — user chốt
Prod down ngay, hạn xong trước 8h sáng 07/11. Lịch công tác lãnh đạo lên cùng đợt. 39 tên theo `.tsv`.

Nhánh `rbac-golive-0611` (worktree `websites/wt-rbac-dien-tap/*`, chưa push), đều chứa toàn bộ `origin/gop_db`, chậm 0:

| Repo | SHA | Đi trước origin | Điểm lui origin/gop_db lúc fetch |
|---|---|---|---|
| hrm-api | `7b71f6462` | 43 | `fc66f7439` |
| hrm-client | `43eea2a78` | 37 | `bf0986007` |
| ERP | `1998e321a1` | 27 | `ce03b6832f` |

Đã kiểm: 5 xung đột đã gỡ, không còn marker; lint PHP 299 + 44 file đạt; Catalog 938 mục, `validate` không lỗi; 39 tên mới còn thiếu 0.
Chưa kiểm: migration, convert, smoke trên dump mới; bộ test Rbac.
Lịch công tác: 2 mã `assign.lich_cong_tac_lanh_dao.announce/.configure` không có tên cũ ⇒ chỉ Super Admin có sau convert, phải cấp cho vai trò cần dùng.
Lệnh push đổi thành `git push origin rbac-golive-0611:gop_db`. Checkout chính `gop_db` giữ nguyên.

## Kết quả go-live 06/11/2026 — ĐÃ LÊN PROD
Mở ERP 20:59, HRM khoảng 21:01. Prod: hrm-api `7b71f6462`, hrm-client `43eea2a78`, ERP `1998e321a1`. Điểm lui code cũ: `fc66f7439` / `bf0986007` / `ce03b6832f`.
Dump lui: VPS HRM `~/backup_hrm_erp_gop_2026-11-06_1902_truoc_rbac.sql.gz`. Báo cáo prod: `/var/www/tpe/hrm-api/storage/app/rbac-convert/golive`.
Kết quả prod khớp diễn tập: migration 10, convert exit 0, mồ côi 12, 282 vai trò / 938 mã / 1.898 alias, 5b 18 vai trò +85, verify 441 Super Admin, hạ 2.558 dòng / 87 vai trò.

### Bài học — sửa quy trình các tenant sau
- HRM prod dùng route cache: phải `php artisan route:cache` sau khi kéo code, không thì route mới 404.
- HRM prod KHÔNG dùng config cache: `config:cache` lỗi "not serializable", bỏ bước này.
- `crontab -r` cấm dùng: crontab dùng chung nhiều tenant. Cron gọi thẳng artisan vẫn chạy khi down.
- `down --secret` phải có tiền tố `api/` (nginx chỉ đưa `/api/` vào Laravel). Đang down thì phải `up && down` mới đổi được.
- ERP `--allow=IP` không tác dụng: ERP sau proxy, `TrustProxies` không khai proxy.
- Worker TPE là `tpe-worker`, `tpe-price-inherit`. hrm-api prod chạy PHP 8.1, ERP 7.4. `composer install` lỗi trên PHP 8.1 (laminas-code), lock không đổi thì bỏ qua. Log HRM là `storage/logs/laravel.log`.

### Việc sau go-live
- Gửi quản trị viên danh sách `mat-do-bit-ro`, `mat-do-cong-ty-qua-vai-tro`, `thieu-quyen-xem` (105), `du-lieu-tro-role-id`, `vai-tro-khong-chuyen`.
- Cấp mã `assign.lich_cong_tac_lanh_dao.announce/.configure` cho vai trò dùng chức năng.
- Chốt TPA, UPS (đang bật phạm vi Tổng công ty, công ty ngừng hoạt động).
- Khởi động lại tiến trình `server_node` ERP.
- Đồng bộ `gop_db` local + `rbac` với origin; đổi 2 ca test route còn ghi tên cũ; bản chụp golden ERP theo nghiệp vụ mới.
- Code mới của origin còn nhánh `isSuperAdmin` (ghi trong việc ngoài luồng).

### Chốt phiên 06/11 tối
- Đã làm: khởi động lại `server_node` ERP (PID mới 1523699); đồng bộ checkout chính về origin; `.env` dev dùng `db_gop_6_11`.
- `hrm-client` `66871e570` (style card + nút chọn/bỏ tất cả đang lọc) đã push; user tự build trên VPS. Ca e2e đã thêm, chưa chạy.
- Còn lại: mục 1, 2, 3 việc sau go-live; dọn `wt-rbac-dien-tap` + server :8031, :3031, :8043 (giữ `db_gop_6_11`); chưa kiểm trên prod: Khách hàng, NV không quyền, NV nhiều công ty, luồng báo lịch.

### Chốt thêm 06/11 khuya
- Danh sách cho quản trị viên từ báo cáo prod: `danh-sach-cap-lai-quyen-golive-06-11/danh-sach-cap-lai-quyen.xlsx` (báo cáo gốc `bao-cao-dien-tap/golive-06-11/`).
- Đã dọn `wt-rbac-dien-tap`, nhánh `rbac-golive-0611`, server :8031 :3031 :8043. `db_gop_6_11` giữ lại cho dev.
- Đã nhắn phiên "Làm hợp đồng bán hàng mới" và "Danh sách hợp đồng wt-hop-dong-ban" (bản thứ 2 đang offline, chờ máy kết nối lại).

### Chốt cuối phiên
- `~/build_tpe.sh` đã đổi bước seeder sang `permission:catalog-sync` (bản cũ `~/build_tpe.sh.bak_truoc_catalog`). Script build 4 tenant còn lại vẫn gọi seeder, sửa khi chuyển sang gop_db.
- Tài liệu dev: `hrm-api/docs/huong-dan-phan-quyen.md` (`05a0eca9b`). Skill và CLAUDE.md: `hrm-claude-config` `4106b3f`.
- Còn lại: cấp 2 mã Lịch công tác; chốt TPA, UPS; kiểm trên prod các mục chưa kiểm; gửi file danh sách cho quản trị viên.
