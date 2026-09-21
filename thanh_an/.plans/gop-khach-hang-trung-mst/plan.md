# Plan — Gộp khách hàng trùng MST

**Phụ trách:** @khoipv
**Phạm vi chốt với user:** fix dữ liệu 1 lần (không làm màn UI), **thử trên local trước**, KHÔNG chạy trực tiếp trên demothanhan.dnsmedia.vn.

## Phase 0 — Khảo sát (XONG)
- [x] Lấy 1188 KH từ API demo, phát hiện 39 cặp trùng MST tuyệt đối + 15 nhóm cùng gốc MST khác đuôi chi nhánh
- [x] Xuất Excel `khach_hang_trung_mst_2dong.xlsx` (2 dòng liền nhau / cặp)
- [x] Lập bản đồ tham chiếu tới `category_customers` trên DB `thanhan_stag_07052026`
- [x] Xác nhận bảng `customers` (cũ) rỗng — mọi `customer_id` đều trỏ `category_customers`
- [x] Xác nhận `category_customers` KHÔNG có `deleted_at` → `CustomerService::delete()` là xóa cứng, không check ràng buộc

## Phase 1 — Chốt thiết kế
- [ ] User chốt danh sách mã KH cần bỏ
- [ ] Chốt cách xử lý cột snapshot trên chứng từ (A/B/C)
- [ ] Chốt cách xử lý dữ liệu con (người đại diện, STK, địa chỉ giao, HĐ khung, sale phụ trách)
- [ ] Chốt: KH bị bỏ → xóa cứng hay chuyển `status = 2`

## Phase 2 — BE (chưa bắt đầu)
- [ ] Command `customer:merge` + `--dry-run`
- [ ] Bảng log kết quả gộp
- [ ] Chạy dry-run trên local

## Phase 3 — Kiểm thử local
- [ ] Tạo fixture: KH trùng có đủ báo giá / gói thầu / hợp đồng / dự án
- [ ] Chạy gộp trong transaction rollback, đối chiếu số liệu trước/sau
- [ ] Rà màn danh sách + chi tiết chứng từ sau khi gộp

## Phase 4 — Áp lên demo
- [ ] CHỜ USER DUYỆT — tuyệt đối không tự chạy

## Phase 0b — Đo tác động trên DB local `thanhan_stag_18092026` (XONG)
- [x] User đổi DB local sang `thanhan_stag_18092026` — 1185 KH, đúng 39 nhóm trùng như demo
- [x] DB này KHÔNG có bảng `supply_proposals` / `supply_handlings` (module Cung ứng chưa có trên bản demo)
- [x] Đếm tham chiếu 78 bản ghi trùng:
      person_charge 560 · projects 88 · quotations 85 · delivery_addresses 78 · contracts 65 · bid_packages 59 · cust_contracts 42
- [x] Phân loại 39 cặp: **22 cặp chỉ 1 bên có chứng từ · 16 cặp cả 2 bên đều trống · 1 cặp CẢ HAI bên đều có chứng từ (MST 5700370069)**

### Checkpoint — 2026-09-21
Vừa hoàn thành: đo tác động thật trên DB local mới, phát hiện chỉ 1/39 cặp cần remap chứng từ hai chiều
Đang làm dở: chờ user chốt danh sách mã cần bỏ + cách xử lý sale phụ trách
Bước tiếp theo: viết command `customer:merge --dry-run`, test trên local
Blocked: chờ user chốt

## Phase 0c — Đối chiếu file note "Giữ" của user (2026-09-21)

- [x] Đọc `c:\Users\Admin\Downloads\DS khach hang trung.xlsx` — cột 14 (Hạn mức công nợ) note "Giữ"
- [x] Kiểm tra tính đủ: 39/39 cặp, mỗi cặp đúng 1 note "Giữ", không có cặp mơ hồ
- [x] Map `code` → `category_customers.id` trên `thanhan_stag_18092026`: khớp 39/39, không mã nào thiếu
- [x] Đếm tham chiếu 17 bảng (view `v_ref`) cho từng bản ghi bị bỏ

### Kết quả
- **8/39 cặp** bản ghi BỊ BỎ đã có dữ liệu nghiệp vụ (tổng 147 chứng từ):
  BPT_BV0151 (34), BSL_BV0137 (30), BBN_BV0015 (22), BQNI_BV0113 (18),
  BPT_BV0150 (14), BBN_BV0014 (11), NCT_BV0306 (9), BBN_BV0013 (9)
- **1 cặp cả 2 bên đều có dữ liệu**: MST 5700370069 — bỏ BQNI_BV0113 (18) / giữ BQNI_BV0518 (2)
- **15 cặp cả 2 bên đều trống** → gộp không rủi ro
- 16 cặp còn lại: bên bỏ trống, bên giữ đã có dữ liệu → chỉ cần xóa bên bỏ
- Toàn bộ 39 bản ghi bị bỏ đều có 1 địa chỉ giao hàng + 0..12 dòng sale phụ trách sẽ mất nếu xóa cứng

### Checkpoint — 2026-09-21
Vừa hoàn thành: đối chiếu danh sách "Giữ" với dữ liệu thật trên local
Đang làm dở: chưa viết command, đang chờ user chốt 3 quyết định (snapshot / sale phụ trách / xóa hay khóa)
Bước tiếp theo: user chốt → viết `php artisan customer:merge {keep_id} {drop_id} --dry-run`
Blocked: cần user xác nhận cách xử lý cặp MST 5700370069 (cả 2 bên đều có chứng từ)

## Phase 2 — Viết command gộp (2026-09-21)

Quyết định của user (@khoipv):
- Snapshot trên chứng từ: **ghi đè hết** theo khách được giữ (không phân biệt đã duyệt hay chưa)
- Sale phụ trách: **lấy theo bên giữ** — xóa toàn bộ sale của bên bị bỏ
- Khách bị bỏ: **xóa hẳn** (không khóa, không ghi chú)

- [x] Khảo sát schema: 17 bảng tham chiếu + 4 bảng con + 3 bảng có `customer_last_used` (json)
- [x] Xác nhận không có chứng từ nào trỏ tới `customer_contacts` / `category_customer_bank_accounts` của bên bỏ → xóa hẳn an toàn
- [x] Xác nhận cả 39 bên giữ đều đã có địa chỉ giao hàng + sale phụ trách; không bên nào có người đại diện / TK ngân hàng
- [x] Viết `hrm-thanhan-api/app/Console/Commands/MergeDuplicateCustomer.php`
- [x] Tạo `cap-gop.csv` (39 cặp, cột `keep_code,drop_code`)

Cách chạy:
```
php artisan customers:merge-duplicate --file=<duong-dan>/cap-gop.csv --dry-run
php artisan customers:merge-duplicate --file=<duong-dan>/cap-gop.csv
php artisan customers:merge-duplicate --keep=MA_GIU --drop=MA_BO --dry-run
```

## Phase 3 — Chạy thử trên local (2026-09-21)

- [x] Dry-run 39 cặp: 39 thành công / 0 lỗi
- [x] Backup DB trước khi chạy thật (`backup_truoc_gop.sql`, 249 MB, trong scratchpad session)
- [x] Chạy thật trên `thanhan_stag_18092026`: 39 thành công / 0 lỗi
- [x] Kiểm tra sau khi chạy

### Số liệu chuyển đổi
| Bảng | Số dòng |
|---|---|
| quotations | 39 |
| projects | 40 |
| contracts | 26 |
| bid_packages | 25 |
| category_customer_contracts | 17 |
| customer_last_used (3 bảng) | 25 |
| category_customer_delivery_addresses (xóa) | 39 |
| category_customer_person_charge_business (xóa) | 267 |
| category_customers (xóa) | 39 |

### Đối chiếu trước / sau
| | Khách hàng | Báo giá | Gói thầu | Hợp đồng | Dự án | Sale phụ trách |
|---|---|---|---|---|---|---|
| Trước | 1185 | 691 | 490 | 487 | 665 | 4100 |
| Sau | **1146** | 691 | 490 | 487 | 665 | **3833** |

- Không còn MST trùng (query group by tax_code having count>1 = rỗng)
- Không còn tham chiếu mồ côi tới 39 id đã xóa (= 0)
- Không còn `customer_last_used_id` trỏ tới id đã xóa (= 0)
- Không mất chứng từ nào
- Còn 10 chứng từ lệch snapshot tên khách — thuộc riêng `THT_BV0069` (tên cũ viết hoa, đã đổi từ trước), **không do gộp**; chứng từ vốn của bên giữ nên command không đụng tới

### Checkpoint — 2026-09-21
Vừa hoàn thành: gộp 39 cặp trên DB local `thanhan_stag_18092026`, kiểm tra sạch
Đang làm dở: không
Bước tiếp theo: user kiểm tra trên giao diện local; nếu ok → chạy trên demo (CHỜ USER DUYỆT, tuyệt đối không tự chạy)
Blocked: không

## Phase 3b — Đồng bộ snapshot còn lệch (2026-09-21)

- [x] Thêm chế độ `--resync` vào `MergeDuplicateCustomer` (ghi đè snapshot theo danh mục, không gộp, không xóa)
  - `--resync --file=cap-gop.csv` → chỉ 39 khách được giữ
  - `--resync --all` → toàn bộ khách hàng
- [x] Chạy thật cho 39 khách được giữ: **10 dòng** (quotations 3, bid_packages 1, contracts 3, projects 3)
- [x] Kiểm tra lại: 39 khách được giữ không còn dòng nào lệch

### Còn tồn (ngoài phạm vi gộp)
Quét toàn DB còn **286 dòng** snapshot lệch danh mục (quotations 46, bid_packages 41, contracts 152, projects 47).
Nguyên nhân: khách đổi tên / MST sau khi lập chứng từ, không liên quan việc gộp.
Riêng `contracts` phần lớn lệch ở `customer_tax_code` (127/148 trước khi gộp).
→ **User chốt (2026-09-21): KHÔNG đồng bộ.** Giữ nguyên snapshot để chứng từ phản ánh đúng thông tin tại thời điểm lập / ký. Không chạy `--resync --all`.

### Checkpoint — 2026-09-21
Vừa hoàn thành: đồng bộ snapshot 10 dòng cho 39 khách được giữ
Đang làm dở: không
Bước tiếp theo: user kiểm tra giao diện local → nếu ok thì chạy trên demo (CHỜ USER DUYỆT)
Blocked: không

## Phase 4 — Chuẩn bị chạy production (2026-09-21)

- [x] Thêm guard `findUnknownRefs()` vào command: quét `information_schema` tìm cột `%customer_id` chưa khai báo
      trong `$refTables` / `$childTables` → **DỪNG** trước khi gộp. Chặn rủi ro production có module mà local
      không có (DB local thiếu `supply_proposals`, `supply_handlings`)
- [x] Test guard: tạo bảng giả `zz_test_ref(customer_id)` → command dừng và báo đúng tên cột; đã xóa bảng test
- [x] Viết `checklist-chay-production.md` (9 bước + 5 lưu ý)
- [ ] User duyệt và tự chạy trên production

### Checkpoint — 2026-09-21
Vừa hoàn thành: guard chống bảng tham chiếu lạ + checklist chạy production
Đang làm dở: không
Bước tiếp theo: user dựng lại danh sách cặp trên dữ liệu production (không dùng lại CSV của local), rồi theo checklist
Blocked: không

## Phase 4b — Bổ sung module Supply (2026-09-21)

Guard `findUnknownRefs()` phát huy tác dụng ngay: quét DB `thanhan_stag_07052026` phát hiện 3 cột
command chưa xử lý — **DB local `thanhan_stag_18092026` không có module Supply nên trước đó không thấy**:
- `supply_proposals.customer_id` + `supply_proposals.customer_name`
- `supply_proposals.usage_customer_id` + `supply_proposals.usage_customer_name`
- `supply_handlings.customer_id` + `supply_handlings.customer_name`

- [x] Khai báo `supply_proposals` / `supply_handlings` vào `$refTables`
- [x] Thêm `$extraRefTables` cho cột phụ `usage_customer_id` (1 bảng có 2 cột tham chiếu)
- [x] Thêm `allRefs()` dùng `Schema::hasTable()` → môi trường không có module Supply tự bỏ qua, không lỗi
- [x] Test trên `thanhan_stag_18092026` (không có Supply): chạy bình thường
- [x] Test trên `thanhan_stag_07052026` (có Supply): guard không chặn nữa, `--resync --all` nhận đúng
      `supply_proposals.usage_customer_id`
- [x] Viết `01-quet-production.sql` (6 query: quét cột lạ, đếm MST trùng, chi tiết từng bản ghi,
      2 cảnh báo TK ngân hàng / người liên hệ, số liệu trước) — đã chạy thử trên cả 2 DB

### Checkpoint — 2026-09-21
Vừa hoàn thành: bổ sung module Supply + script quét production
Đang làm dở: không
Bước tiếp theo: user deploy code → chạy `01-quet-production.sql` trên production → gửi kết quả query [1] và [3]
Blocked: không

---

## Phase 5 — Gói toàn bộ quy trình vào command (bỏ SQL tay)

Lý do: user phản hồi "sao lại phải chạy sql các thứ phức tạp vậy? tôi muốn chạy 1 lệnh hay gì đó bạn tự xử lý cho tôi chứ?"

- [x] Tạo `app/ExcelExport/DuplicateCustomerExport.php` — export danh sách trùng MST (17 cột, tô màu theo cặp, cột GIỮ nổi bật, freeze pane, autofilter)
- [x] Thêm option `--scan`: tự tìm MST trùng, đếm chứng từ/sale/địa chỉ/TK/người đại diện từng bản ghi, **điền sẵn gợi ý GIỮ**, cảnh báo nhóm cả 2 bên đều có chứng từ, xuất .xlsx ra `storage/app/gop-khach-hang/`
- [x] `readPairsFromExcel()` — đọc ngược file .xlsx người dùng đã đánh dấu, validate mỗi cặp đúng 1 chữ "Giữ"
- [x] `backupDatabase()` — tự `mysqldump` trước khi gộp, mật khẩu truyền qua `MYSQL_PWD`, backup lỗi thì dừng không gộp; có `--skip-backup` để bỏ qua
- [x] Hỏi xác nhận yes/no trước khi chạy thật
- [x] Tự chạy đồng bộ snapshot cho khách được giữ sau khi gộp (bỏ bước `--resync` thủ công)
- [x] `snapshotCounts()` + `postCheck()` — tự in số liệu trước/sau, đánh giá OK/SAI, kiểm tra MST còn trùng, kiểm tra tham chiếu mồ côi toàn bộ `allRefs()`
- [x] Viết lại `checklist-chay-production.md` còn 4 bước, xóa `01-quet-production.sql`

### Kiểm thử trên local (DB `thanhan_stag_07052026`)

- [x] `php -l` sạch cả 2 file
- [x] `--scan` → tìm đúng 4 nhóm trùng / 8 bản ghi, xuất file .xlsx
- [x] Round-trip: `--file=<file .xlsx vừa xuất> --dry-run` → đọc đúng 4 cặp, 0 lỗi
- [x] Chạy thật: backup tự động 320.7 MB, xác nhận, gộp 4 cặp thành công
- [x] Tự kiểm tra sau gộp: khách hàng 1051 → 1047 (−4, OK), báo giá/gói thầu/hợp đồng/dự án/sale **không đổi**, không còn MST trùng, không có tham chiếu mồ côi
- [x] Chạy `--scan` lại → "Không có mã số thuế nào bị trùng"

### Checkpoint — 2026-09-21 10:55
Vừa hoàn thành: gói toàn bộ quy trình gộp vào command, đã test trọn luồng scan → đánh dấu → dry-run → chạy thật trên DB staging local
Đang làm dở: không
Bước tiếp theo: user pull code mới lên server rồi chạy `php artisan customers:merge-duplicate --scan`
Blocked: cần xác nhận `devhrmnew` / `/var/www/thanhan2/hrm-api` là production thật hay môi trường dev

---

## Phase 6 — Chạy được trên mọi môi trường (dev + production)

User chốt: `devhrmnew` / `/var/www/thanhan2/hrm-api` là **PRODUCTION**, và sẽ đẩy code lên cả dev lẫn production → 1 bản code phải chạy được ở mọi nơi dù schema lệch nhau.

- [x] `columnsOf()` + `hasCol()` — cache danh sách cột theo bảng
- [x] `allRefs()` lọc theo môi trường: bỏ bảng không có, bỏ bảng thiếu cột khóa, bỏ cột snapshot không có ở bảng đích **hoặc** ở `category_customers`
- [x] `availableChildTables()` / `availableLastUsedTables()` — lọc bảng con và bảng `customer_last_used` theo schema thật
- [x] `syncLastUsed()` chỉ update cột `customer_last_used_id` / `_name` nào thật sự tồn tại
- [x] `handleScan()` dùng `countRef()` (trả 0 nếu thiếu bảng/cột), `status` / `created_at` thiếu thì để trống
- [x] `printEnvReport()` — in ra bảng/cột command khai báo mà môi trường này không có; gọi ở cả `--scan` lẫn dry-run/chạy thật
- [x] `findMysqldump()` — dò PATH (`command -v` / `where`), fallback `/usr/bin`, `/usr/local/bin`, `/usr/local/mysql/bin`, `/opt/homebrew/bin`, `mariadb-dump`
- [x] `exportDir()` — dùng `storage_path('app/gop-khach-hang')`, không phụ thuộc cấu hình disk `local` của từng môi trường
- [x] Xuất Excel bằng `Excel::raw()` + `file_put_contents()` thay cho `Excel::store()` (tránh lệch root disk)
- [x] `resolveFile()` — `--file=` nhận tên file ngắn, tự tìm ở thư mục hiện tại → `base_path()` → `exportDir()`
- [x] Mật khẩu DB truyền qua `MYSQL_PWD` thay vì `--password=` (không lộ trên `ps`)

### Kiểm thử

- [x] DB `thanhan_stag_07052026` (có module Supply) → "Môi trường: đủ toàn bộ bảng / cột"
- [x] DB `thanhan_stag_18092026` (không có Supply) → tự bỏ qua 2 bảng, chạy bình thường
- [x] DB giả lập `zz_test_merge`: thiếu **20 bảng** + **14 cột snapshot**, `category_customers` không có `status`/`full_address`/`telephone`/..., `contracts` không có `customer_last_used_name`
  - `--scan` → liệt kê đúng toàn bộ bảng/cột thiếu, tìm đúng 2 nhóm trùng, cảnh báo nhóm cả 2 bên đều có chứng từ
  - Chạy thật → chuyển đúng tham chiếu, `customer_last_used` dedupe đúng, xóa đúng khách, kiểm tra sau gộp OK
  - Gọi bằng **tên file ngắn** (không đường dẫn) → vẫn tìm ra file, auto-resync ghi đè đúng 1 dòng quotations lệch
- [x] Đã xóa DB test và toàn bộ file tạm

### Checkpoint — 2026-09-21 11:00
Vừa hoàn thành: làm command độc lập schema, 1 bản code chạy được cả dev lẫn production; test trên 3 DB khác schema
Đang làm dở: không
Bước tiếp theo: user pull code (2 file) lên cả dev và production, chạy `php artisan customers:merge-duplicate --scan` ở từng nơi
Blocked: không

---

## Phase 7 — Nhúng danh sách 39 cặp vào code (--preset)

Lý do: `scp` file CSV lên server không thành công, dán tay dễ hỏng dấu tiếng Việt (BĐB, TĐL, NĐN).

- [x] Thêm property `$presetPairs` — 39 cặp [mã giữ, mã bỏ] chốt ngày 21/09/2026, kèm docblock ghi rõ đây là dữ liệu cho 1 lần dọn dẹp, lần sau phải chạy `--scan`
- [x] Thêm option `--preset`, `readPairs()` trả thẳng danh sách này (dùng được cho cả `--resync`)
- [x] Sửa thông báo lỗi khi thiếu tham số: "Cần --file, hoặc --preset, hoặc cả --keep và --drop"
- [x] Test trên `thanhan_stag_18092026` (đã gộp rồi): 0 lỗi "không tìm thấy mã giữ" / 39 lỗi "không tìm thấy mã bỏ"
      → chứng minh 39 mã giữ đọc đúng, **dấu tiếng Việt trong file PHP không bị hỏng**

### Checkpoint — 2026-09-21 11:15
Vừa hoàn thành: nhúng danh sách cặp vào code, chạy bằng `--preset` không cần file
Đang làm dở: không
Bước tiếp theo: user pull code, chạy `--preset --dry-run` trên server, ra 39 cặp / 0 lỗi thì bỏ --dry-run
Blocked: DB trên server tên `thanhan_stag` và ra đúng 39 nhóm giống bản local — cần user xác nhận đây là production hay staging
