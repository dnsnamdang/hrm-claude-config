# Deploy lên VPS production — Báo cáo phát triển thị trường - Khách hàng

Màn: `/assign/report/customer-market-development` · Quyền mới **1187-1189** · Nhánh `tpe`.
Viết 14/09/2026, sau khi code đã push lên VPS.

> Đọc hết mục **2. Bẫy** trước khi gõ lệnh — có 2 chỗ làm HỎNG DỮ LIỆU ĐANG CHẠY nếu làm sai
> (seeder quyền `truncate` cả bảng, và `config:cache` làm chết kết nối ERP của **toàn hệ thống**).

**Đã kiểm trước khi viết tài liệu này**: 7 file BE mới `php -l` sạch trên **PHP 7.4** và không dùng
cú pháp PHP 8 (`?->`, `match`, `enum`) — chạy được trên môi trường hiện tại của VPS.

---

## 0. Tóm tắt 1 phút

| Việc | Bắt buộc? | Hỏng gì nếu bỏ qua |
|---|---|---|
| `migrate` (2 cột trên `meetings`) | ✅ | Màn chết (lỗi cột không tồn tại) |
| `db:seed BackfillMeetingProvinceSeeder` | ✅ | Meeting cũ không lên báo cáo, bảng gần như trống |
| Cấp quyền 1187-1189 **đúng `company_id`** | ✅ | Báo cáo rỗng, không báo lỗi |
| Build lại `hrm-client` | ✅ | Không có menu, vào URL ra 404 |
| `permission:cache-reset` + đăng nhập lại | ✅ | Cờ quyền phía FE còn cũ |
| Queue / cron / biến môi trường mới | ❌ | Không có |

---

## 1. Việc phải làm khi deploy — đúng thứ tự

### Bước 1 — `hrm-api`: migration (BẮT BUỘC, không có là màn chết)

```bash
php artisan migrate --path=database/migrations/2026_09_14_000001_add_province_columns_to_meetings_table.php --force
```

Thêm 2 cột `meetings.province_id` + `meetings.province_name` và 1 index `meetings_province_id_index`.
Migration **idempotent** (có `hasColumn` / `hasIndex`), chạy lại không lỗi. Không có khoá ngoại
(bảng `provinces` nằm ở DB ERP).

⚠️ `ALTER TABLE meetings` khoá ghi trong lúc chạy. MySQL 8 thêm cột là `INSTANT`, MySQL 5.7 phải
dựng lại bảng. Kiểm số dòng trước để biết nên chạy giờ thấp điểm hay không:

```sql
SELECT COUNT(*) FROM meetings;    -- máy local chỉ 96 dòng, prod chắc chắn lớn hơn nhiều
```

### Bước 2 — `hrm-api`: seeder vá dữ liệu cũ (BẮT BUỘC, không có là báo cáo trống trơn)

```bash
php artisan db:seed --class="Modules\Assign\Database\Seeders\BackfillMeetingProvinceSeeder" --force
```

Meeting cũ tạo trước khi có tính năng thì 2 cột snapshot đang NULL → **không lên báo cáo**.
Seeder vá cả **thị trường** lẫn **tên/mã khách hàng** còn trống (2 cột `customer_name` /
`customer_code` xưa nay hay bị bỏ trống — đo trên DB test: 47/73 meeting trống → báo cáo gom theo
Khách hàng ra dòng không tên).

- **Đọc DB ERP** (`mysql2`) → bước này chỉ chạy được khi `DB_*_SECOND` trên VPS trỏ đúng ERP prod
  và VPS mở được kết nối tới host đó. Kiểm trước bằng bước 0 ở mục 2.1.
- Chunk 1000 khách hàng / lượt, gom theo tỉnh để mỗi tỉnh chỉ 1 câu `UPDATE`.
- **Chạy lại nhiều lần được**, chỉ đụng dòng còn thiếu (đã kiểm lại hôm nay: lần 2 chỉ vá 2 dòng
  mới sinh, các dòng cũ không bị ghi đè).
- Đọc kỹ **dòng cuối** nó in ra:
  `Còn lại N meeting chưa có thị trường (thuộc M khách hàng không có tỉnh hoặc không còn bên ERP).`
  N > 0 là bình thường — đó là khách hàng nước ngoài không có tỉnh/TP, hoặc khách đã bị xoá bên ERP.
  Số này rơi vào nhóm **"Chưa xác định thị trường"** trên báo cáo (user đã chốt giữ nguyên tên).

### Bước 3 — `hrm-api`: cấp 3 quyền 1187-1189

**TUYỆT ĐỐI KHÔNG chạy `PermissionsTableSeeder` trên prod** — xem mục 2.2. Chèn tay:

```sql
-- 3 quyền (id cố định, khớp seeder trong repo)
INSERT IGNORE INTO permissions (id, guard_name, name, display_name, `group`, type, created_at, updated_at) VALUES
(1187,'api','Xem báo cáo phát triển thị trường - khách hàng theo tổng công ty','Xem báo cáo phát triển thị trường - khách hàng theo tổng công ty','Báo cáo phát triển thị trường - khách hàng',4,NOW(),NOW()),
(1188,'api','Xem báo cáo phát triển thị trường - khách hàng theo công ty','Xem báo cáo phát triển thị trường - khách hàng theo công ty','Báo cáo phát triển thị trường - khách hàng',4,NOW(),NOW()),
(1189,'api','Xem báo cáo phát triển thị trường - khách hàng theo phòng ban','Xem báo cáo phát triển thị trường - khách hàng theo phòng ban','Báo cáo phát triển thị trường - khách hàng',4,NOW(),NOW());
```

3 cấp xem, chọn đúng cấp cho từng role:
| Quyền | Thấy được |
|---|---|
| 1187 | Toàn bộ công ty (tổng công ty) |
| 1188 | Công ty của mình |
| 1189 | Phòng ban của mình |

#### ⚠️ `company_id` KHÔNG phải lúc nào cũng bằng 1

Hàm gác quyền so `role_has_permissions.company_id` với **`current_company_role` của người đăng
nhập**. Cấp thiếu công ty là người thuộc công ty đó **không thấy gì mà cũng không báo lỗi**.
Đo trên DB: quyền đang được cấp theo **5 công ty khác nhau** (`company_id` = 1, 2, 3, 4, 8 trên
tổng số 8 công ty) — nên câu lệnh phải cấp theo ĐÚNG tập công ty của từng role, đừng gõ cứng `1`.

**Cách an toàn nhất — nhân bản y hệt quyền của báo cáo anh em "Kết quả CSKH tiềm năng"**
(1179/1180/1181 trùng khớp 3 cấp với 1187/1188/1189), lấy đúng role + đúng công ty mà báo cáo đó
đang được cấp:

```sql
INSERT IGNORE INTO role_has_permissions (role_id, permission_id, company_id)
SELECT rhp.role_id, rhp.permission_id + 8, rhp.company_id      -- 1179->1187, 1180->1188, 1181->1189
FROM role_has_permissions rhp
WHERE rhp.permission_id IN (1179, 1180, 1181);
```

Kiểm trước khi chạy (xem sẽ cấp cho ai, công ty nào) và sau khi chạy (2 dòng phải ra cùng số):

```sql
SELECT permission_id, COUNT(*) n, GROUP_CONCAT(DISTINCT company_id) cong_ty
FROM role_has_permissions WHERE permission_id IN (1179,1180,1181) GROUP BY permission_id;

SELECT permission_id, COUNT(*) n, GROUP_CONCAT(DISTINCT company_id) cong_ty
FROM role_has_permissions WHERE permission_id IN (1187,1188,1189) GROUP BY permission_id;
```

Muốn cấp tay cho 1 role cụ thể thì nhớ kèm đủ các công ty role đó đang dùng:

```sql
INSERT IGNORE INTO role_has_permissions (role_id, permission_id, company_id)
SELECT DISTINCT rhp.role_id, p.id, rhp.company_id
FROM role_has_permissions rhp
JOIN roles r ON r.id = rhp.role_id
CROSS JOIN (SELECT 1187 AS id UNION SELECT 1188 UNION SELECT 1189) p
WHERE r.name IN ('Tên role cần cấp' /*, ... */);
```

Không có quyền nào thì báo cáo **rỗng có chủ ý** (fail-closed, đã kiểm 0/0 dòng) — không báo lỗi.

Sau khi chèn:

```bash
php artisan permission:cache-reset   # hoặc: php artisan cache:clear
```

Gác quyền ở **backend đọc thẳng DB**, không qua cache — nhưng **cờ quyền phía FE** lấy từ
`getAllPermissions()` của spatie (CÓ cache), nên phải reset cache và **người dùng đăng nhập lại**
mới thấy dữ liệu.

⚠️ **Menu KHÔNG bị ẩn theo quyền.** `components/menu-sidebar.js` không khai quyền và
`Sidebar.filterMenuItems()` trả nguyên danh sách — nghĩa là **ai cũng thấy mục "Phát triển thị
trường - Khách hàng"**, người chưa được cấp quyền bấm vào sẽ thấy **báo cáo trống**. Giống hệt các
màn báo cáo anh em trong nhóm. Nên **cấp quyền xong rồi mới thông báo cho người dùng**, nếu không
sẽ nhận một loạt câu hỏi "sao báo cáo không có số?".

### Bước 4 — `hrm-client`: build lại FE

```bash
# Node 12 + heap 8192 (mặc định heap không đủ, build OOM)
NODE_OPTIONS=--max-old-space-size=8192 npm run build
# đổi branch/xoá cache cũ thì dùng: npm run build:fresh
```

Menu **"Phát triển thị trường - Khách hàng"** nằm trong nhóm *Báo cáo* của phân hệ Giao việc,
sinh từ `components/menu-sidebar.js` nên có ngay sau khi build.

### Bước 5 — không cần gì thêm

Không có queue mới, không cron mới, không biến môi trường mới, không đụng bảng nào khác ngoài
`meetings` (2 cột) và `permissions` / `role_has_permissions`.

---

## 2. Bẫy — đọc trước khi gõ lệnh

### 2.1. Kết nối ERP (`mysql2`) phải sống, nếu không báo cáo thiếu hẳn cột "KH mới"

Màn đọc DB ERP ở **đúng 2 chỗ**: seeder backfill (bước 2) và cột **"KH mới"** (HRM không có bảng
khách hàng riêng). Kiểm trước khi deploy:

```bash
php artisan tinker --execute="dd(DB::connection('mysql2')->select('SELECT COUNT(*) c FROM '.env('DB_DATABASE_SECOND').'.customers'));"
```

- ERP chết / sai cấu hình → cột "KH mới" = 0 và **không có lỗi nào hiện ra màn**, rất dễ tưởng
  "kỳ này không có khách mới".
- Riêng lúc **LƯU MEETING**: hook snapshot có `try/catch` + ghi `Log::warning`
  `[meeting-market-snapshot]` → ERP chết cũng **không làm hỏng việc lưu phiếu**, chỉ là 2 cột
  snapshot còn trống; lần lưu sau nó tự vá lại. Grep log khi nghi ngờ:
  ```bash
  grep meeting-market-snapshot storage/logs/laravel-$(date +%F).log
  ```

### 2.2. ⛔ KHÔNG chạy `PermissionsTableSeeder` trên prod

`Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` dòng 35 có
**`DB::table('permissions')->truncate()`** — chạy trên prod là **xoá sạch bảng quyền** rồi dựng lại
theo file trong repo: mọi quyền prod có mà repo chưa có sẽ mất, và `role_has_permissions` trỏ tới
id cũ thành rác → **cả hệ thống mất phân quyền**. Dùng câu `INSERT` ở bước 3.

### 2.3. ⛔ KHÔNG bật `php artisan config:cache` trên VPS

Code đọc tên DB ERP bằng `env('DB_DATABASE_SECOND')` **ngoài file config** — Laravel khi đã
`config:cache` thì KHÔNG nạp `.env` nữa, `env()` trả `null`, tên bảng thành `.customers` → lỗi SQL.
Không phải lỗi riêng màn này: **115 file** trong `hrm-api` đang dùng kiểu đó. Nếu VPS đang có
`bootstrap/cache/config.php` thì phải `php artisan config:clear` (nhớ `route:clear`, `view:clear`
sau khi deploy code mới).

### 2.4. Link Xuất Excel mang JWT trên query string

Nút *Xuất Excel* tải trực tiếp từ server bằng `...?token=<JWT>` (phải làm vậy vì kiểu
blob + `<a download>` hỏng trên Safari/webview — xem `hrm-export-download-safari-bug`).
Hệ quả trên prod: **token nằm trong access log của nginx**. Nếu log được gom/gửi ra ngoài thì nên
lọc tham số `token` trong cấu hình log.

### 2.5. Bản in / letterhead

Bản in lấy letterhead từ `companies.header` theo **công ty đang lọc**, không lọc thì theo công ty
của người đăng nhập. Công ty nào bỏ trống `header` thì bản in mất phần đầu trang — kiểm:

```sql
SELECT id, name, header IS NULL OR header = '' AS thieu_header FROM companies;
```

### 2.6. Bộ e2e KHÔNG nằm trong repo

`HRM/e2e/` không thuộc repo git nào → 2 spec (`customer-market-development.spec.ts`,
`customer-market-development.api.spec.ts`) + `utils/cmdFixture.ts` **chỉ có trên máy dev**, push
không mang theo. Fixture PHP (`database/e2e_customer_market_dev_seed.php`) thì đã nằm trong
`hrm-api` — và nó **chèn quyền + tạo tài khoản test**, nên **đừng chạy trên prod**.

---

## 3. Hiệu năng — ĐÃ XỬ LÝ BẰNG PHÂN TRANG (14/09/2026)

> ✅ **Cập nhật**: rủi ro nêu ở bản đầu tài liệu này **đã được sửa** — bảng theo dõi và popup nay
> đều **phân trang Ở BACKEND** (đúng nguyên tắc "luôn phân trang phía BE" trong `CLAUDE.md`).
> Trường hợp nặng nhất (*Năm nay · Khách hàng*, 3.263 dòng cấp 1) đo lại:
> **payload 4,3 MB → 67 KB**, tải + vẽ **46,3s → 0,87s**, bung hết cấp **73,4s → 0,19s**.
> Bảng theo dõi: **50 dòng cấp 1/trang** (chọn 20/50/100), dòng TỔNG luôn hiện, STT giữ số thật.
> Popup: **20 dòng/trang**; lọc/sắp xếp/phân trang đều ở BE, KPI + chip + In + Excel vẫn lấy
> **toàn tập đã lọc**. Phần bên dưới giữ lại **số đo TRƯỚC khi phân trang** để biết vì sao phải làm.

Server vốn đã nhanh, **chỗ nghẽn nằm ở trình duyệt**: tiêu chí **Khách hàng** đẻ 1 dòng cho MỖI
khách hàng, mà "KH mới" tính cả khách chưa phát sinh meeting nào → kỳ càng dài, bảng càng khổng lồ.

Đo trên máy dev (dữ liệu ERP thật, **bản Nuxt DEV** nên prod sẽ nhanh hơn vài lần) — **trước khi
phân trang**:

| Kỳ · Tiêu chí | API (đo trực tiếp) | JSON | Số dòng bảng | Trình duyệt dựng xong |
|---|---|---|---|---|
| Tháng này · Thị trường | 0,15s | 5 KB | 4 | 3,9s |
| Tháng này · Khách hàng | — | — | 6 | 2,2s |
| Năm nay · Thị trường | 0,18s | 625 KB | 38 | 9,1s |
| Quý này · Khách hàng | — | — | 376 | 11,5s |
| **Năm nay · Khách hàng** | **0,25s** | **4,3 MB** | **3.264** | **46,3s** |
| **Năm nay · Khách hàng + bung hết cấp** | — | — | **9.046** | **+73,4s** |

Cột cuối đo **từ lúc bấm tới lúc bảng vẽ xong**, gồm cả dọn bảng cũ — mấy dòng đầu (4-38 dòng mà
vẫn 2-9s) là **nhiễu của bản dev** chạy ngay sau lần dựng 9.046 dòng, đừng coi là con số thật; điều
chắc chắn là **xu hướng**: số dòng tăng thì thời gian tăng theo, và mốc 3.264 dòng là không dùng nổi.

- Tải mạng + `JSON.parse` 4.3 MB chỉ mất **~1.1s** → **không phải lỗi API**, mà là chi phí dựng
  ~3.3k dòng × 6 ô bấm được ≈ 20.000 component Vue.
- Đã thử `Object.freeze` cả cây (bỏ reactivity): **không ăn thua** (75s) → muốn chữa thật thì phải
  **phân trang hoặc ảo hoá bảng**, không phải chỉnh vặt.
- Mặc định của màn là **Tháng này · Thị trường** (4 dòng) nên mở màn vẫn nhẹ. Rủi ro chỉ xảy ra khi
  người dùng tự chọn *Khách hàng* + *Quý này / Năm nay*.
- Con số phụ thuộc **lượng khách hàng tạo mới trong kỳ** bên ERP (DB đang đo có 3.208 khách trong
  năm). Prod nhiều khách hơn thì nặng hơn.

**Còn lại sau khi đã phân trang ở BE:**
1. ✅ Bảng theo dõi + popup: xong. Payload còn 67 KB/trang, màn hiện trong ~1s.
2. ⚠️ **Bản in *Tổng hợp*** của tiêu chí Khách hàng + Năm nay vẫn ra **6,5 MB HTML** — bản in theo
   định nghĩa là in ĐỦ mọi dòng nên **cố ý KHÔNG phân trang**; popup xem trước sẽ nặng. Dặn người
   dùng lọc bớt (Công ty / Phòng ban / Nhân viên) trước khi in cả năm theo tiêu chí Khách hàng.
   Xuất Excel cùng trường hợp thì nhẹ (1-2s), khuyến khích dùng Excel thay vì in.
3. ℹ️ `per_page` bị **chặn trần 200** ở BE — ai gọi API tay với `per_page` khổng lồ cũng không kéo
   sập được trình duyệt.

Xuất Excel không nằm trong nhóm rủi ro: Năm nay chỉ **1.4s / 64 KB**.

---

## 4. Kiểm tra sau khi deploy (làm lần lượt, ~5 phút)

1. Vào `/assign/report/customer-market-development` bằng tài khoản **đã cấp quyền** → bảng có số,
   dải tổng hợp có số.
2. Vào bằng tài khoản **chưa cấp quyền** → bảng rỗng (đúng ý đồ fail-closed), không văng lỗi 500.
3. Bấm 1 con số bất kỳ → popup mở, có danh sách; bấm **Xem tổng hợp** → hiện 3 hộp KPI + dải chip;
   bấm 1 chip → danh sách lọc hẹp lại và quay về trang 1.
3b. Chọn tiêu chí **Khách hàng** + kỳ **Năm nay** → bảng phải hiện trong ~1-2 giây kèm thanh phân
   trang "Hiển thị 1-50 / N Khách hàng"; sang trang 2 thì STT bắt đầu từ 51 và dòng TỔNG vẫn còn.
3c. Trong popup: bấm sang trang 2, đổi ô lọc, bấm 1 chip → mỗi thao tác đều gọi API mới; dòng TỔNG
   trên KPI không đổi theo trang. Bấm **Xuất Excel danh sách** → file `.xlsx` tải về từ server.
4. Nút **In báo cáo** (2 chế độ) và **In danh sách** trong popup → bản xem trước có đầu trang công ty.
5. Nút **Xuất Excel** ở màn và trong popup → file tải về mở được (thử cả Safari nếu có máy Mac).
6. Kiểm số liệu: dòng **TỔNG** phải bằng tổng các dòng cấp 1 ở cả 6 cột số.
7. Kiểm dữ liệu vá được tới đâu:
   ```sql
   SELECT COUNT(*) FROM meetings WHERE customer_id IS NOT NULL AND province_id IS NULL;
   SELECT COUNT(*) FROM meetings WHERE customer_id IS NOT NULL AND (customer_name IS NULL OR customer_name = '');
   ```
8. `tail -n 200 storage/logs/laravel-$(date +%F).log` → không có `[meeting-market-snapshot]`.

---

## 5. Lùi lại (rollback)

- **FE**: build lại từ commit trước là xong, không có trạng thái gì để dọn.
- **BE**: revert code. **2 cột `province_id` / `province_name` cứ để nguyên** — không có chúng thì
  code cũ vẫn chạy bình thường, còn `migrate:rollback` sẽ **mất sạch dữ liệu đã vá**, lần deploy sau
  phải backfill lại từ đầu.
- **Quyền**: xoá 3 dòng trong `role_has_permissions` là người dùng hết thấy số liệu; không cần xoá
  bản ghi trong `permissions`.

---

## 6. 🔔 Nhắc cho lần merge sang nhánh gộp DB

Khi HRM và ERP về **chung 1 database**, phải đổi lại cách query (join thẳng, bỏ `mysql2` /
`TpCustomer` / `env('DB_DATABASE_SECOND')`), nếu không **số liệu sai âm thầm** vì `mysql2` trỏ DB
ERP CŨ, id lệch. Mọi chỗ đụng ERP đều gắn mốc:

```bash
grep -rn "@TODO-GOPDB" hrm-api/Modules/Assign
```

2 cột snapshot trên `meetings` thì **GIỮ NGUYÊN** (vẫn cần chụp thị trường tại thời điểm họp), chỉ
đổi chỗ resolve bên trong `MeetingMarketSnapshotService`. Chi tiết từng chỗ: mục *"NỢ KỸ THUẬT"*
cuối `plan.md`.
