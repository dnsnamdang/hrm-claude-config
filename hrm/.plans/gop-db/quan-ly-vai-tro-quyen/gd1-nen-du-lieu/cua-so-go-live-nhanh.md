# Go-live nhanh — Vai trò & Quyền (GĐ1 → GĐ3 + GĐ2c), CHỈ TPE

> ⚠️ **06/11 18:50: bảng SHA dưới đây ĐÃ CŨ, chưa push theo bảng này.** Đọc `chuan-bi-go-live-06-11.md` trước.

> Viết 01/11/2026. **Cập nhật SHA 04/11** (sau diễn tập dump prod 03/11 — `bao-cao-dien-tap/dien-tap-04-11/README.md`); origin còn chạy nên sáng G fetch lại và sửa bảng. Bản rút gọn để chạy theo của `runbook-go-live.md` (runbook vẫn là nguồn chi tiết + mục C khôi phục).
> Lịch: **sáng diễn tập trên bản sao prod mới → tối cửa sổ bảo trì 60–90 phút.** Không có lệnh nào trong file này được chạy
> tự động: người chạy dán từng khối, xem kết quả, đạt cổng mới sang khối sau.

## Số liệu nền (đo trên máy dev 01/11 — đối chiếu lại lúc G)

| | hrm-api | hrm-client | ERP TanPhatDev |
|---|---|---|---|
| `origin/gop_db` hiện tại = **ĐIỂM LUI code** (fetch 04/11) | `d29b60688` | `48f80791c` | `d95e29ae12` |
| `gop_db` local sẽ push (rbac + GĐ2c + GĐ3b, kéo origin 04/11) | `aac684f92` (+41, gồm Catalog 42 alias) | `0db94d679` (+35) | `84bec64416` (+26) |
| Nhánh `rbac` (04/11: + Catalog 42 alias) | `757b32e4b` | `d663e7ac9` | `b4f666abe1` |
| Migration mới đợt này | 7: `2026_11_01_000001..000005`, `2026_11_02_000001`, `2026_11_02_000010` | — | **0** |
| Đổi composer / package.json | không | không ⇒ **bỏ `npm ci`, chỉ build** | không |

- `rbac:convert` chạy thật trên bản sao: **16 giây**. `mysqldump` prod 12 GB ≈ **5 phút** (đo 20/10).
- ERP **tự deploy khi push `gop_db`** (`.github/workflows/deploy.yml`: pull · `composer install` · `migrate --force` · `config/route/view:cache`
  · `queue:restart` · `optimize`) ⇒ push ERP là bước **muộn nhất**, sau khi DB đã chuyển đổi.

## Rút gọn so với runbook (đã cân nhắc)

| Bỏ / dời | Lý do |
|---|---|
| **A.3 cấp lại quyền trong hệ thống cũ trước go-live** ⇒ dời sang SAU go-live | Runbook viết khi chưa có màn sửa quyền. Nay đã có `/admin/roles` + `/admin/employee-roles` ⇒ quản trị viên sửa trên hệ thống mới. Danh sách lấy từ báo cáo diễn tập sáng G. |
| Chụp lại golden Purchase ERP, chạy bộ e2e | Không chặn go-live. ⚠️ **4 mã chỉ có phạm vi Tổng công ty nay CHẶN go-live** (01/11 user chốt tắt `allow_group_scope` cho 6 công ty ≠ 1 ⇒ phải thêm phạm vi Công ty vào Catalog 4 mã đó trước, nếu không người 6 công ty mất quyền). |
| `npm ci` hrm-client | `package.json` / lock không đổi. |
| Build hrm-client trong cửa sổ | **Tuỳ chọn:** build sẵn ở thư mục phụ buổi chiều rồi đổi thư mục trong cửa sổ (khối 6b). |

**KHÔNG bỏ:** diễn tập sáng G trên bản sao mới · `mysqldump` trước chuyển đổi · thứ tự push ERP sau chuyển đổi · smoke 3 tài khoản.

---

## Phần A — Sáng G: diễn tập (không downtime, ~1,5–2 giờ)

- [ ] **A1. Bản sao prod mới** → `hrm_erp_rbac_rehearsal` (dump prod sáng G; nhân bản lần trước 10 phút). Ghi thời gian dump.
- [ ] **A2. Migration** trên bản sao (worktree `wt-rbac/hrm-api` hoặc checkout gop_db): `migrate:status` ⇒ chạy các bản `gop_db` còn chờ
      **trước** (liệt kê + hỏi user như CLAUDE.md) ⇒ 7 bản đợt này chạy lẻ `--path` (xem `--pretend` trước).
- [ ] **A3. Chuyển đổi:** `rbac:convert --dry-run --report-dir=… --scope-decisions=scope-decisions.csv` (mã thoát 0, `chenh-lech-khac.csv`
      chỉ tiêu đề) ⇒ chạy thật ⇒ B.4b (3 câu SQL runbook) ⇒ `permission:catalog-sync --dry-run` = 0 thay đổi. Ghi thời gian.
- [ ] **A3b. Cấp mã GĐ3b** (thay kiểm Vai trò theo tên): `rbac:grant-role-name-codes --dry-run --report-dir=…` ⇒ so `cap-ma-vai-tro.csv`
      với rehearsal 02/11 (18 Vai trò · thêm 85; TGĐ 7 mã, GĐ 10 mã, Kế toán F14, CSKH F13b, Quản lý/Quản lý đào tạo F15) ⇒ chạy thật
      ⇒ `--verify` "Dòng lệch: 0". Chi tiết + cách đọc lệch: khối 5b.
- [ ] **A4. Kiểm:** 2 bộ `tests/Feature/Rbac` (DB test) + Playwright 3 tài khoản (1 công ty, nhiều công ty, NV không quyền) trên bản sao.
- [ ] **A5. Danh sách gửi quản trị viên** (sửa sau go-live): `mat-do-bit-ro`, `mat-do-cong-ty-qua-vai-tro`, `thieu-quyen-xem`,
      `du-lieu-tro-role-id`, `vai-tro-khong-chuyen` từ **báo cáo A3**.
- [ ] **A6. Chuẩn bị prod (không đổi hành vi):**
  - `.env` HRM prod `/var/www/tpe/hrm-api`: thêm `RBAC_GROUP_SCOPE_ADMINS=13`; kiểm có đủ `DB_CONNECTION_TPE` … `DB_DATABASE_TPE`
    (thiếu ⇒ màn Tài khoản 500 "Unsupported driver []").
  - `.env` ERP prod: `HRM_URL_FE` phải có giá trị (rỗng ⇒ `/admin/roles` ERP chuyển hướng về chính nó, lặp vô hạn — diễn tập 04/11).
  - Chép `scope-decisions.csv` lên VPS HRM (`/tmp/rbac-golive/`).
  - Xác nhận **etek / toyota không tự kéo `gop_db`** (go-live chỉ TPE — code mới + DB chưa chuyển đổi = khoá toàn bộ người dùng).
  - Báo người dùng giờ bảo trì; chốt **hạn chót khôi phục** (sau mốc này không lui bằng dump vì mất dữ liệu nhập mới).
- [ ] **A7. Đóng băng `gop_db` 3 repo** từ lúc A1 tới khi mở app. Có commit mới ⇒ soát (vụ 31/10: commit lọc guard `'web'` làm dropdown
      chức vụ rỗng sau chuyển đổi). **Không push `gop_db` hrm-api/client trước cửa sổ** (ai deploy hotfix lúc đó = khoá người dùng).

---

## Phần B — Tối G: cửa sổ bảo trì

Mở 2 phiên: **VPS HRM** `ssh -p 2225 erp_tpe@124.158.4.24` · **VPS ERP** `erp_tpe@erptpe`. Máy dev giữ 3 repo `gop_db` sẵn để push.

### Khối 0 — biến (VPS HRM, dùng suốt)
```bash
export API=/var/www/tpe/hrm-api
export CLI=/var/www/tpe/hrm-client
export DB=hrm_erp_gop
export REPORT=storage/app/rbac-convert/golive
alias M='mysql -h 192.168.122.103 -u hrm_tpe -p --table $DB'
cd $API && git rev-parse --short HEAD    # ghi lại — phải = SHA điểm lui ở bảng trên (04/11: d29b60688)
df -h ~                                   # trống ≥ 25 GB cho dump
```

### Khối 1 — hạ app (~2 phút)
```bash
# VPS ERP
cd /var/www/html/TanPhatDev && php artisan down --message="Đang nâng cấp hệ thống" --allow=<IP quản trị>
# VPS HRM
cd $API && php artisan down --secret="<chuoi-bi-mat>"
crontab -l > ~/crontab.bak && crontab -r            # tắt schedule:run (bật lại ở khối 9)
```
⚠️ Cron ERP: tắt tương tự trên VPS ERP nếu có.

### Khối 2 — sao lưu (~5 phút) — ĐIỂM LUI DUY NHẤT
```bash
mysqldump -h 192.168.122.103 -u hrm_tpe -p --single-transaction --quick --routines --triggers --no-tablespaces --set-gtid-purged=OFF $DB \
  | gzip > ~/backup_${DB}_$(date +%F_%H%M)_truoc_rbac.sql.gz
zcat ~/backup_${DB}_*_truoc_rbac.sql.gz | tail -1     # PHẢI: -- Dump completed
```

### Khối 3 — code hrm-api + migration (~5 phút)
Máy dev: `git -C HRM/hrm-api push origin gop_db` (và hrm-client cùng lúc — client chưa build thì chưa chạy). **CHƯA push ERP.**
```bash
cd $API && git fetch origin && git checkout gop_db && git pull && git rev-parse --short HEAD   # = SHA gop_db local đã push (04/11: aac684f92)
composer install --no-dev -o
php artisan migrate:status | grep -E "\| No"          # chỉ được thấy 7 bản đợt này (+ bản gop_db đã duyệt ở A2)
php artisan migrate --force                            # đúng danh sách vừa xem
php artisan config:cache
```
Cổng: `migrate:status` không còn bản chờ · `M -e "SELECT COUNT(*) FROM permission_aliases; SELECT COUNT(*) FROM companies WHERE allow_group_scope<>1;"` = `0 · 0` (lúc này vẫn = 0; tắt 6 công ty ở bước GĐ2c sau chuyển đổi).

> **01/11 — tắt phạm vi Tổng công ty cho 6 công ty ≠ TPE** (user chốt): sau `rbac:convert` + lệnh cấp mã GĐ3b, TRƯỚC khi mở app, NV 13 vào `/admin/group-scope-companies` bấm "Không cho cấp" cho TPHP, TPV, TPSG, ETEK GREEN CU, DTTDETEK, EG (ghi lịch sử đúng người). Cổng: `SELECT id FROM companies WHERE allow_group_scope=1` = chỉ `1`. Rehearsal: 2,719 dòng quyền / 87 vai trò / 244 NV bị hạ xuống Công ty.

### Khối 4 — chuyển đổi (< 1 phút chạy)
```bash
cd $API && php artisan rbac:convert --erp-da-bao-tri --report-dir=$REPORT --scope-decisions=/tmp/rbac-golive/scope-decisions.csv; echo "exit=$?"
php artisan rbac:convert --print-rollback --report-dir=$REPORT > $REPORT/rollback.sql
```
Mã thoát ≠ 0 ⇒ bảng xử lý ở `runbook-go-live.md` B.4. **1 kèm "DDL lỗi"** ⇒ `--resume-ddl`.

### Khối 5 — B.4b + kiểm SQL (~5 phút)
3 câu SQL ở `runbook-go-live.md` B.4b (thiếu `company_employees` phải 0 · dọn `employee_has_roles` mồ côi có bản lưu · báo cáo mất quyền
quản lý tài khoản), rồi:
```bash
cd $API && php artisan tinker --execute='\App\Support\Permissions\PermissionChecker::flush(); cache()->forget("spatie.permission.cache");'
php artisan permission:catalog-sync --dry-run        # 0 thay đổi
M -e "SHOW COLUMNS FROM role_has_permissions LIKE 'company_id'; SELECT COUNT(*) FROM roles WHERE company_id IS NULL; SELECT COUNT(*) FROM rbac_role_map;"
# kỳ vọng: rỗng · 0 · > 0 và khớp số diễn tập
```

### Khối 5b — cấp mã GĐ3b (< 1 phút chạy) — SAU B.4b, TRƯỚC bước tắt 6 công ty (GĐ2c)
Code ERP/HRM mới kiểm MÃ thay cho tên Vai trò (Giám đốc, Tổng giám đốc, Kế toán, CSKH, Quản lý đào tạo…). Thiếu bước này ⇒ GĐ/TGĐ mất
quyền BGĐ, ô lọc Công ty, duyệt vượt hạn mức… ngay khi mở app. Mã mới (17) do `rbac:convert` đồng bộ Catalog nên khối 5 đã thấy
`catalog-sync --dry-run` = 0; nếu vẫn báo "thêm" ⇒ chạy `permission:catalog-sync` thật trước (thiếu mã ⇒ ERP kiểm quyền trả false/500).
```bash
cd $API && php artisan rbac:grant-role-name-codes --dry-run --report-dir=$REPORT/gd3b-dry
#   so số với diễn tập A3b (rehearsal 02/11: "Vai trò: 18 · thêm: 85 · nâng: 0") — lệch ⇒ dừng, đọc cap-ma-vai-tro.csv
php artisan rbac:grant-role-name-codes --report-dir=$REPORT/gd3b      # chạy lại không nhân bản (bỏ qua dòng đã có)
php artisan rbac:grant-role-name-codes --verify --report-dir=$REPORT/gd3b-verify
php artisan tinker --execute='\App\Support\Permissions\PermissionChecker::flush(); cache()->forget("spatie.permission.cache");'
```
Cổng: `Dòng lệch: 0`. Đọc `doi-chieu-vai-tro-ma.csv` nếu ≠ 0:
- `employee_id` không có trong `employees` ⇒ dòng `employee_has_roles` mồ côi (rehearsal 02/11: 20 dòng của NV 21, 23 — B.4b dọn mồ côi
  thì phải hết) ⇒ bỏ qua được.
- Chạy `--verify` SAU khi tắt 6 công ty ⇒ dòng mức 4 ở công ty tắt được đếm riêng ("trong đó N dòng … GĐ2c") — đúng chủ ý design 4.4.
- NV giữ vai trò **Super Admin**: dòng cũ 0 → mới 1 là ĐÚNG CHỦ Ý (user chốt 04/11 — bước 5 convert cấp đủ mọi mã, kể cả 17 mã GĐ3b; diễn tập 04/11: 441 dòng / 12 NV).
- Còn lại ⇒ dừng, báo. Thời gian rehearsal 02/11: cấp 0,67 s · verify 0,75 s.
Lui riêng bước này (không cần dump): lệnh chỉ THÊM `role_has_permissions` (không hạ/xoá) + 1 dòng `role_permission_history` mỗi Vai trò
(changed_by NULL) — xoá đúng các dòng trong `$REPORT/gd3b/cap-ma-vai-tro.csv` (role_id × mã). Code cũ không đọc các mã này nên để nguyên cũng vô hại.

### Khối 6 — ERP + client (song song, ~10–15 phút)
- **ERP:** máy dev `git -C ERP/TanPhatDev push origin gop_db` ⇒ GitHub Actions tự deploy. Theo dõi job xanh, rồi VPS ERP:
  ```bash
  cd /var/www/html/TanPhatDev && git rev-parse --short HEAD     # = SHA gop_db ERP đã push (04/11: 84bec64416)
  composer dump-autoload -o && php artisan config:cache && sudo systemctl reload apache2
  ```
- **6a. Client build tại chỗ** (VPS HRM, node 12):
  ```bash
  cd $CLI && git fetch origin && git checkout gop_db && git pull && git rev-parse --short HEAD   # = SHA gop_db client đã push (04/11: 0db94d679)
  NODE_OPTIONS=--max-old-space-size=8192 npm run build
  sudo /etc/init.d/hrm-client-tpe start     # KHÔNG pm2 restart trần (socket ⇒ 502)
  ```
- **6b. (tuỳ chọn, nhanh hơn)** chiều G đã build sẵn ở `/var/www/tpe/hrm-client-next` (clone `gop_db` local đã push sang nhánh tạm,
  chép `.env`, `npm ci` + build). Trong cửa sổ: `sudo pm2 stop hrm-client-tpe` ⇒ `mv hrm-client hrm-client-prev && mv hrm-client-next hrm-client`
  ⇒ `sudo /etc/init.d/hrm-client-tpe start`. Lui: đổi ngược thư mục. ⚠️ Cần push `gop_db` client sớm sang **nhánh tạm**, KHÔNG phải `gop_db`.

### Khối 7 — worker + cache
```bash
cd $API && sudo supervisorctl restart laravel-worker:* && php artisan queue:restart
```
ERP đã `queue:restart` trong workflow. **Không** `cache:clear` trên Redis dùng chung.

### Khối 8 — smoke (15 phút, qua đường bypass bảo trì)
| Tài khoản | Kiểm |
|---|---|
| NV 13 (TPE) | HRM: menu Quản trị › Vai trò / Vai trò nhân viên / Cấu hình phạm vi Tổng công ty mở được; 1 danh sách có phạm vi (vd khách hàng) ra dữ liệu. ERP: đăng nhập, 1 màn đơn hàng, dropdown chức vụ người ký **có dữ liệu** |
| 1 NV nhiều công ty | đổi công ty ⇒ quyền đổi theo công ty |
| 1 NV không quyền | màn quản trị 404/403 |
| TPE_APP | đăng nhập được, `permissions[].name` là tên cũ |
So số dòng với Playwright diễn tập A4.

### Khối 9 — mở
```bash
cd $API && php artisan up && crontab ~/crontab.bak
cd /var/www/html/TanPhatDev && php artisan up      # VPS ERP
```

### Sau khi mở (cùng tối / sáng hôm sau)
- Gửi quản trị viên danh sách A5 để sửa quyền ở màn mới.
- Theo dõi `storage/logs/laravel-<ngày>.log` (403 bất thường, "Unsupported driver", lỗi cột).
- Merge `gop_db` ngược về `rbac` (đồng bộ bản sửa `Role::activeForDropdown`).

---

## Lui (điểm dừng hỏng, không sửa được trong cửa sổ)

1. Hạ cả 2 app (khối 1).
2. `gunzip < ~/backup_${DB}_<giờ>_truoc_rbac.sql.gz | mysql -h 192.168.122.103 -u hrm_tpe -p $DB`
3. Code về điểm lui **cả 3 repo**: theo bảng đầu file (04/11: hrm-api `d29b60688` · hrm-client `48f80791c` · ERP `d95e29ae12`) — **ghi lại SHA thật lúc khối 0**
   (VPS: `git checkout <sha>` + `composer install` / build client; ERP: nếu đã push `gop_db` thì **revert trên `gop_db` rồi push** để workflow
   deploy lại bản cũ — không force-push).
4. `config:cache`, restart worker, reload apache, `/etc/init.d/hrm-client-tpe start`, mở app.

Lỗi **trước khối 4** (chưa chuyển đổi): chỉ cần code về điểm lui, không cần khôi phục dump.

Lỗi **chỉ ở khối 5b** (cấp mã GĐ3b) mà chuyển đổi đã đạt: không cần dump — xem "Lui riêng bước này" ở khối 5b. Nhưng code ERP/HRM mới
KHÔNG chạy đúng khi thiếu mã (GĐ/TGĐ mất quyền) ⇒ hoặc sửa và chạy lại 5b (idempotent), hoặc lui cả code theo mục 3.
