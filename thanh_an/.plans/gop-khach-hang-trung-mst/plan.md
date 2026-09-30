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

---

## Phase 8 — Kiểm tra lại trên cổng demo (2026-09-22)

- [x] Đăng nhập sẵn trên trình duyệt, gọi `/api/v1/category/customers?per_page=5000` từ `demothanhan.dnsmedia.vn`
- [x] Quét trùng MST tuyệt đối (chuẩn hoá: bỏ khoảng trắng, viết hoa) → **0 nhóm**
- [x] Quét trùng theo gốc 10 số đầu → 15 nhóm (chi nhánh khác nhau, đuôi `-00x` khác nhau → hợp lệ, không gộp)
- [x] Tổng khách hàng hiện tại: **1150** (trước gộp 1188), toàn bộ `status = 1`, 32 khách chưa nhập MST

### Kết luận
Việc gộp 39 cặp đã áp lên demo thành công, không còn khách hàng nào trùng MST.

### Checkpoint — 2026-09-22
Vừa hoàn thành: quét lại MST trùng trên cổng demo — sạch
Đang làm dở: không
Bước tiếp theo: không có (feature có thể chuyển sang "Hoàn thành" nếu production cũng đã chạy)
Blocked: không

---

## Phase 9 — Trùng MST do import thiếu số 0 ở đầu (2026-09-22)

User báo: file import làm mất số `0` đầu MST (VD `BHN_TM0580` = `101842073` vs `BHN_TM0112` = `0101842073`).
→ Phase 8 quét sạch vì so khớp **chuỗi MST nguyên văn**, không bù số 0 nên bỏ sót.

- [x] Quét lại với chuẩn hoá: MST gốc 9 số → bù `0` phía trước rồi mới so khớp
- [x] **23 nhóm trùng / 46 bản ghi** (mỗi nhóm đúng 1 cặp: 1 bản đúng + 1 bản thiếu số 0)
- [x] Toàn hệ thống có **344 bản ghi MST chỉ 9 số** (sai định dạng), trong đó 23 cái đã gây trùng
      - 274 thuộc lô gốc 03/11/2025 · 21 thuộc lô 17/09/2026 · 49 rải rác
- [x] Lô import 17/09/2026 (Tạ Ngọc Ánh): 33 KH mới → **21/33 thiếu số 0 và cả 21 đều trùng** với KH đã có
- [x] Lô này còn lỗi encode: **8 tên khách chứa `&amp;`** thay vì `&`
- [x] 2 nhóm còn lại do bản ghi **cũ** sai: `BHN_TM0269` (110162412) ↔ `BHN_TM0428` · `BHN_TM0094` (104675102) ↔ `BHN_TM0381`

### Việc cần làm (chưa bắt đầu)
- [ ] Chốt với user: hướng xử lý 23 cặp (gộp bằng `customers:merge-duplicate` giữ bản ghi nào)
- [ ] Chốt: có chuẩn hoá 321 MST 9 số còn lại (bù số 0) không
- [ ] Sửa `MergeDuplicateCustomer --scan` để nhận diện MST thiếu số 0 (hiện chỉ so nguyên văn)
- [ ] Sửa lỗi encode `&amp;` trong tên khách của lô import
- [ ] Chặn từ gốc: validate MST đủ 10 số khi import

### Checkpoint — 2026-09-22
Vừa hoàn thành: xác định 23 cặp trùng do thiếu số 0 đầu MST, khoanh vùng lô import 17/09/2026
Đang làm dở: không
Bước tiếp theo: chờ user chốt hướng xử lý
Blocked: chờ user

### Truy nguyên: vì sao tạo KH mới thay vì update (2026-09-22)

- [x] Trace code: **hệ thống KHÔNG có chức năng import khách hàng** — không có route `import` trong
      `Modules/Category/Routes/api.php`, không có class Import nào trong `Modules/Category`
      (chỉ `Modules/Payroll/ExcelImports`, `Modules/Training/ExcelImports`)
- [x] 33 KH ngày 17/09 đi qua `POST /api/v1/category/customers` → `CustomerService::store()`
      (`Modules/Category/Services/CustomerService.php:236`) — luôn `CategoryCustomer::create()` +
      `getNextCode()` sinh mã mới, **không có nhánh tìm-thấy-thì-update**
- [x] Lá chắn duy nhất: `StoreCategoryCustomerRequest.php:25`
      `'tax_code' => 'required|string|max:255|unique:category_customers,tax_code,' . $this->id`
      → so khớp **chuỗi nguyên văn**, `101842073` ≠ `0101842073` nên lọt
- [x] DB **không có unique index** trên `category_customers.tax_code` → không có chốt chặn cuối
- [x] Nguyên nhân mất số 0: Excel đọc MST như kiểu số → cắt số 0 đầu; người nhập copy nguyên chuỗi 9 số

### Hướng sửa đề xuất (CHỜ USER CHỐT — đụng Request dùng chung cho cả store & update)
- [ ] `prepareForValidation()` trong `StoreCategoryCustomerRequest`: trim + bù `0` cho MST gốc 9 số
- [ ] Thêm rule định dạng MST: 10 số, hoặc 10 số + `-` + 3 số
- [ ] FE màn thêm KH: nhập xong MST → tra cứu khách đã có → cảnh báo + link sang màn sửa
- [ ] Sau khi dọn sạch dữ liệu → thêm unique index DB cho `tax_code`
- [ ] `customers:merge-duplicate --scan`: chuẩn hoá bù số 0 trước khi so khớp

### ĐÍNH CHÍNH truy nguyên (2026-09-22)

Kết luận "không có chức năng import khách hàng" ở mục trên là **SAI** — em grep hụt vì import
không nằm trong `Modules/Category` mà nằm trong **`Modules/Payroll`**.

Luồng thật:
`pages/category/customer/index.vue:23` (nút Import Excel) → `components/modal/import-excel-modal.vue`
(`type = 'category-customer'`) → `store/actions.js:185 importOtherIncomeCustomer`
→ `POST payroll/other_incomes/importExcel/category_customer`
(`Modules/Payroll/Routes/api.php:180` → `OtherIncomeController::importExcel`)
→ **`Modules/Payroll/ExcelImports/CategoryCustomerImport.php`**

#### Nguyên nhân thật sự sinh mã mới thay vì update

`CategoryCustomerImport.php:329` — `createOrUpdateCustomer()`:
```php
$customer = CategoryCustomer::where('name', $data['ten_khach_hang'])->first();
```
→ Quyết định **update hay tạo mới** dựa trên **tên khách hàng khớp tuyệt đối**, KHÔNG dùng mã số thuế.
Tên lệch 1 ký tự → coi là khách mới → `getNextCode()` sinh mã mới.

- IDICS: bản cũ `CÔNG TY CỔ PHẦN␣␣IDICS` (2 dấu cách) vs file import `CÔNG TY CỔ PHẦN␣IDICS` (1 dấu cách)
- **19/21 cặp của lô 17/09 chỉ khác nhau ở khoảng trắng thừa hoặc `&amp;`** → chuẩn hoá tên là update đúng chỗ
- 2 cặp khác thật: `TRUNG TÂM Y TẾ KIẾN THỤY` vs `… HUYỆN KIẾN THỤY`; `CÔNG NGHỆ T&P` vs `T &amp; P`

#### Vì sao validate trùng MST không chặn

`validateDuplicateTaxCode()` được thêm ngày **21/09/2026** (commit `120feea3`, +74 dòng) — **sau** lô import
17/09 **4 ngày**. Thời điểm import chưa hề có kiểm tra trùng MST.
Và validate mới này cũng dùng `whereIn('tax_code', ...)` so **chuỗi nguyên văn** → MST thiếu số 0 vẫn lọt.

### Hướng sửa cập nhật (CHỜ USER CHỐT)
- [ ] `CategoryCustomerImport`: đổi khoá tra cứu update từ `name` → **`tax_code` đã chuẩn hoá**, fallback `name` chuẩn hoá
- [ ] Chuẩn hoá đầu vào khi đọc file: `html_entity_decode` (bỏ `&amp;`), gộp khoảng trắng thừa, trim
- [ ] Chuẩn hoá MST: bù `0` cho MST 9 số, trước cả bước validate lẫn bước lưu
- [ ] File mẫu `khach_hang.xlsx`: set cột MST kiểu Text để Excel không cắt số 0
- [ ] (đã ghi ở trên) `StoreCategoryCustomerRequest` + unique index DB + `--scan` normalize

---

## Phase 10 — Import khách hàng: so tên bỏ qua khoảng trắng (2026-09-22)

User chốt: chỗ tra cứu tên khách hàng để quyết định update/create phải bỏ phân biệt khoảng trắng.

- [x] Thêm `compactSpaces()` — bỏ mọi khoảng trắng (space, tab, CR, LF, NBSP) để so tên
- [x] Thêm `findCustomerByName()` — so `name` đã bỏ khoảng trắng ở cả 2 phía (SQL `REPLACE` lồng nhau)
- [x] `createOrUpdateCustomer()` dùng `findCustomerByName()` thay cho `where('name', ...)`
- [x] `validateDuplicateTaxCode()` cũng so tên đã bỏ khoảng trắng — nếu không, file đúng MST mà tên lệch
      dấu cách sẽ báo sai "Mã số thuế đã tồn tại" và chặn nguyên lượt import
- [x] Kiểm thử trên DB local

Giữ nguyên: phân biệt dấu / hoa-thường vẫn do collation `utf8mb4_unicode_ci` của cột xử lý như cũ.

### Kết quả kiểm thử (DB `thanhan_stag_07052026`)
| Tình huống | Trước | Sau |
|---|---|---|
| Tên file 1 dấu cách vs DB 2 dấu cách (`TRUNG TÂM KIỂM SOÁT BỆNH TẬT TỈNH ĐIỆN BIÊN␣␣(Mã QHNS…)`) | không tìm thấy → tạo mới | tìm thấy #1453 → update |
| Chữ hoa/thường + dấu | khớp | vẫn khớp (không đổi hành vi) |
| Tên rỗng / toàn khoảng trắng | — | trả `null` → tạo mới như cũ |
| Cùng MST, tên chỉ lệch dấu cách | báo sai "MST đã tồn tại", chặn import | không báo lỗi |
| Cùng MST, tên khác hẳn | báo lỗi | vẫn báo lỗi |

Ghi chú: sheet 2 (Người phụ trách) vẫn tra `whereIn('name', ...)` — không cần sửa vì
`createOrUpdateCustomer()` đã ghi đè `name` theo đúng tên trong file trước khi sheet 2 chạy.

### Checkpoint — 2026-09-22
Vừa hoàn thành: import khách hàng so tên bỏ qua khoảng trắng, test trên DB local
Đang làm dở: không
Bước tiếp theo: user deploy + import thử lại file thật
Blocked: không

---

## Phase 11 — Dọn 23 nhóm trùng do MST thiếu số 0 (2026-09-22)

User chốt hướng xử lý (**ngược với Phase 1-7**): bản ghi **MỚI** (MST thiếu số 0) là bản **GIỮ**,
bản ghi **CŨ** (MST 10 số đúng) là bản **BỎ**.

Ba bước cho mỗi nhóm:
1. Bù số `0` vào đầu `tax_code` của bản GIỮ → MST thành 10 số đúng
2. Kiểm tra bản BỎ đã được dùng ở đâu chưa (báo giá / gói thầu / hợp đồng / dự án / sale phụ trách / bảng con)
3. Chưa dùng → xóa hẳn. Đã dùng → chuyển hết tham chiếu sang bản GIỮ rồi mới xóa

### Task
- [x] Thêm chế độ `--fix-zero` vào `customers:merge-duplicate`
- [x] Nhận diện cặp: `tax_code` 9 số ↔ `'0' + 9 số` (giữ nguyên hậu tố chi nhánh `-NNN`)
- [x] Bỏ qua + cảnh báo nhóm có >1 bản mỗi phía (phải xử lý tay)
- [x] Cặp **ngược** (bản thiếu số 0 lại là bản tạo TRƯỚC) → mặc định bỏ qua, in kèm số chứng từ 2 bên,
      chỉ chạy khi có `--include-reversed`
- [x] Tách đúng "đã dùng" (chứng từ — chuyển sang bản giữ) với bảng con riêng của bản bỏ (xóa theo)
- [x] Liệt kê trường có dữ liệu ở bản BỎ mà bản GIỮ đang trống (xóa đi là mất)
- [x] Bù số 0 trước, gộp sau (để resync snapshot ghi ra MST đúng)
- [x] Dùng lại `mergePair()`, backup, `--dry-run`, `postCheck()` sẵn có
- [x] Test trên DB local (clone `thanhan_fixzero_test`)
- [ ] Chạy trên demo — **CHỜ USER DUYỆT, không tự chạy**
- [ ] Chốt hướng cho 3 cặp ngược

### Cách chạy
```bash
# 1. Xem trước, không ghi DB
php artisan customers:merge-duplicate --fix-zero --dry-run

# 2. Chạy thật (tự mysqldump backup trước, hỏi xác nhận)
php artisan customers:merge-duplicate --fix-zero

# 3. Xóa cache sau khi chạy
php artisan cache:clear
```

### Kết quả test trên DB `thanhan_fixzero_test` (clone của `thanhan_stag_18092026`)
| Chỉ tiêu | Kết quả |
|---|---|
| Cặp nhận diện được | 24 (21 thuận + 3 ngược) |
| Cặp đã xử lý | 21 — lỗi 0 |
| Bản BỎ chưa dùng → xóa thẳng | 8 |
| Bản BỎ đã dùng → chuyển rồi xóa | 13 |
| Tham chiếu đã chuyển | báo giá 28, dự án 28, hợp đồng 19, gói thầu 17, HD khách 15, khách dùng gần đây 17 |
| Khách hàng | 1146 → 1125 (-21, đúng bằng số cặp) |
| Báo giá / gói thầu / hợp đồng / dự án | không đổi số lượng |
| Tham chiếu mồ côi | 0 |
| Chạy lại lần 2 | không còn cặp nào (trừ 3 cặp ngược) |

Ví dụ kiểm chứng đúng yêu cầu của user:
- `BHN_TM0112` (IDICS, MST `0101842073`) chưa dùng ở chứng từ nào → xóa hẳn;
  `BHN_TM0580` được bù số 0 thành `0101842073`
- `BHN_BV0030` (BỆNH VIỆN 19-8) đã dùng → 6 báo giá + 2 hợp đồng + 6 dự án chuyển sang `BHN_BV0509`,
  snapshot `customer_name` trên chứng từ ghi lại theo bản giữ, rồi mới xóa bản cũ

### 3 cặp NGƯỢC — chờ user chốt
| MST đúng | Bản thiếu số 0 (cũ hơn) | Đang dùng | Bản đủ 10 số (mới hơn) | Đang dùng |
|---|---|---|---|---|
| 0104675102 | BHN_TM0094 | 0 | BHN_TM0381 | 0 |
| 0110162412 | BHN_TM0269 | 0 | BHN_TM0428 | 0 |
| 0301483745 | NĐT_BV0331 (BỆNH VIỆN MẮT) | 11 | NHCM_BV0359 | 5 |

- 2 cặp đầu: cả 2 bên đều chưa dùng → giữ bên nào cũng không ảnh hưởng chứng từ
- Cặp 3 khác bản chất: 2 mã khác vùng (`NĐT` vs `NHCM`), cả 2 đều đang có chứng từ — phải chốt tay,
  nên dùng `--keep/--drop` chứ không dùng `--fix-zero`

### Đã chạy thật trên DB local `thanhan_stag_18092026` (2026-09-22)
- 21/21 cặp xử lý xong, lỗi 0 — khách hàng 1146 → 1125
- Kiểm tra sau khi chạy:
  - Không còn nhóm trùng MST (so khớp chính xác): 0
  - Chạy lại `--fix-zero --dry-run`: chỉ còn 3 cặp ngược đang bỏ qua
  - Tham chiếu mồ côi báo giá / gói thầu / hợp đồng / dự án / HD khách: 0
  - Snapshot tên khách trên chứng từ của 21 bản GIỮ: lệch 0 dòng
- **Tồn đọng không phải do lần chạy này** (đã có sẵn từ trước):
  - `category_customer_person_charge_business` còn 6 dòng mồ côi trỏ tới id 1705 và 2103 (tạo 17/12/2025,
    không nằm trong danh sách id vừa xóa)
  - `--resync --all --dry-run` báo 280 dòng snapshot lệch trên toàn bộ khách hàng, nhưng 21 bản GIỮ đều sạch
  - Còn **324** khách hàng MST 9 số không có bản trùng đi kèm → thuộc việc chuẩn hoá MST hàng loạt,
    chưa xử lý ở phase này
- Backup tự tạo: `storage/app/gop-khach-hang/backup-thanhan_stag_18092026-20260922-155411.sql` (260 MB).
  User báo không cần backup → lần sau thêm `--skip-backup`.

### Checkpoint — 2026-09-22
Vừa hoàn thành: chế độ `--fix-zero`, test trên DB clone và chạy thật trên DB local, 21/21 cặp đúng, 0 tham chiếu mồ côi mới
Đang làm dở: không
Bước tiếp theo: user deploy code rồi chạy `--fix-zero --dry-run` trên demo, duyệt xong mới chạy thật
Blocked: chưa chốt hướng 3 cặp ngược

---

## Phase 12 — Truy vết khách hàng "mất" MST `1200337771` (2026-09-22)

- [x] Kiểm tra `category_customers` hiện tại có MST `1200337771` không → **0 dòng**
- [x] Kiểm tra bản backup TRƯỚC khi chạy merge → cũng **không có** dòng nào trong `category_customers` mang MST này
- [x] Đối chiếu id trước/sau khi chạy: đúng **21** dòng bị xóa, không dòng nào liên quan
- [x] Xác định nơi MST này còn tồn tại: `contracts.customer_tax_code` (HĐ id 11 — `HD-011/2025`) và
      `contract_versions` (JSON), đều trỏ về `customer_id = 2875`
- [x] Tìm ra nguyên nhân thật: **file import ngày 17/09 đã GHI ĐÈ khách id 2875**

### Kết luận

| | Trước 17/09 (theo snapshot HĐ id 11) | Sau import 17/09 |
|---|---|---|
| Mã | `NĐT_BV0331` | `NĐT_BV0331` (không đổi) |
| Tên | BỆNH VIỆN MẮT | BỆNH VIỆN MẮT |
| MST | `1200337771` | `301483745` |
| Tỉnh | Đồng Tháp | Hồ Chí Minh |
| Địa chỉ | 44 Phan Hiển Đạo, P. Mỹ Tho, Đồng Tháp | 280 Điện Biên Phủ, P. Xuân Hòa, TP HCM |
| SĐT | 02733873339 | 02839325364 |

Import khớp khách theo **TÊN** → dòng Excel "Bệnh Viện Mắt" (TP HCM) khớp trúng
"BỆNH VIỆN MẮT" (Đồng Tháp, id 2875) → update đè MST/tỉnh/địa chỉ/SĐT, `code` giữ nguyên
(`updated_at = 2026-09-17 17:04:33`). Sau đó lại có thêm bản mới `NHCM_BV0359` (id 2906,
MST `0301483745`) → sinh ra cặp "ngược" đã ghi ở Phase 11.

→ Lệnh `--fix-zero` **không liên quan**: thuật toán chỉ nhận MST 9 số hoặc 10 số bắt đầu bằng `0`;
`1200337771` là 10 số bắt đầu bằng `1` nên bị bỏ qua ngay từ bước gom nhóm.

### Rà quét ảnh hưởng tương tự

- [x] Quét snapshot MST trên `contracts` lệch với `category_customers.tax_code` → **2 khách**:
  - `NĐT_BV0331` (id 2875): `1200337771` → `301483745`, đổi cả tỉnh (Đồng Tháp → HCM) — **bị ghi đè nhầm**
  - `BLC_BV0002` (id 2): `5300319879` → `5300133200`, cùng tỉnh Lào Cai — cần xác nhận là sửa đúng hay sai
- [x] Quét lệch tỉnh trên `contracts` + `quotations` → chỉ duy nhất id 2875

### Việc còn phải chốt

- [ ] Khôi phục khách Bệnh viện Mắt Đồng Tháp (tạo lại bản ghi riêng hay sửa ngược id 2875?)
- [ ] Xác nhận `BLC_BV0002` đổi MST là đúng hay sai
- [ ] Sửa import: khớp theo tên rủi ro cao → nên ưu tiên khớp theo MST, và khi đổi vùng/tỉnh/nhóm
      thì phải sinh lại `code` (hiện tại không sinh lại)

### Checkpoint — 2026-09-22 (bổ sung)
Vừa hoàn thành: truy vết MST `1200337771`, xác định do import 17/09 ghi đè chứ không phải do lệnh merge
Đang làm dở: không
Bước tiếp theo: user chốt cách khôi phục Bệnh viện Mắt Đồng Tháp + xác nhận `BLC_BV0002`
Blocked: chưa chốt hướng 3 cặp ngược (Phase 11) và cách khôi phục id 2875

---

## Phase 13 — Chạy lại trên DB local mới `thanhan_stag_22092026` (2026-09-22)

- [x] Đổi `.env` sang DB mới (user tự làm) — xác nhận `DB_DATABASE=thanhan_stag_22092026`
- [x] Chạy `--fix-zero --dry-run` → 21 cặp, 2 cặp ngược bị bỏ qua
- [x] Chạy thật `--fix-zero --skip-backup --force` → 21/21 cặp, lỗi 0
- [x] `php artisan cache:clear`
- [x] Kiểm tra lại sau khi chạy

### Kết quả

| Chỉ tiêu | Trước | Sau |
|---|---|---|
| Khách hàng | 1150 | 1129 (−21) |
| Báo giá / Gói thầu / Hợp đồng / Dự án | 707 / 501 / 498 / 678 | không đổi |
| Sale phụ trách (bảng con của bản BỎ) | 3838 | 3716 (−122) |

Số dòng đã chuyển sang bản GIỮ: quotations 29, projects 29, contracts 20, bid_packages 17,
category_customer_contracts 15, customer_last_used 19.

Kiểm tra độc lập bằng SQL: nhóm trùng MST = 0; tham chiếu mồ côi ở báo giá / gói thầu / hợp đồng /
dự án / HĐ khách = 0; snapshot của 21 bản GIỮ lệch 0 dòng; chạy lại dry-run chỉ còn 2 cặp ngược.

### Khác so với lần chạy trên DB cũ `thanhan_stag_18092026`

- Mã GIỮ là dãy mã mới (`BHN_BV0509`, `BHN_TM0580`, …) vì DB mới import lại
- Chỉ còn **2** cặp ngược thay vì 3 — cặp `NĐT_BV0331` / `NHCM_BV0359` đã hết trùng vì
  id 2875 được trả lại MST `1200337771` lúc `2026-09-22 14:22:19`
- Còn **323** khách MST 9 số không có bản trùng đi kèm (trước là 324)

### Còn tồn
- [ ] `NĐT_BV0331` (id 2875): MST đã trả về `1200337771` (Đồng Tháp) nhưng
      `customer_province_name` vẫn là **Hồ Chí Minh** → còn lệch tỉnh, cần sửa nốt
- [ ] 2 cặp ngược `BHN_TM0094`/`BHN_TM0381` và `BHN_TM0269`/`BHN_TM0428` (cả 2 bên đều chưa dùng)
- [ ] 323 khách MST 9 số → chuẩn hoá hàng loạt

### Checkpoint — 2026-09-22 (Phase 13)
Vừa hoàn thành: chạy `--fix-zero` trên DB local mới `thanhan_stag_22092026`, 21/21 cặp, 0 lỗi, 0 tham chiếu mồ côi
Đang làm dở: không
Bước tiếp theo: user chốt 2 cặp ngược + sửa tỉnh cho `NĐT_BV0331`, rồi deploy chạy trên demo
Blocked: không

---

## Phase 14 — Import khớp khách theo tên phải phân biệt dấu + hoa/thường (2026-09-22)

User phản ánh: `Bệnh Viện Mắt` và `BỆNH VIỆN MẮT` phải là 2 khách khác nhau.

### Nguyên nhân

Cột `category_customers.name` dùng collation `utf8mb4_unicode_ci` → bỏ qua **cả hoa/thường lẫn dấu**:
`'BỆNH VIỆN MẮT' = 'Bệnh Viện Mắt'` → 1, `'Mắt' = 'Măt' = 'Mat'` → 1.
Nên `CategoryCustomer::where('name', ...)` trả về nhiều bản, `->first()` lấy id nhỏ nhất → ghi đè nhầm.

### 3 nhóm đang "đụng tên" trong DB

| Bản ghi | Tên | Thực tế khác nhau ở |
|---|---|---|
| 1507 `BHY_BV0072` (Hưng Yên) / 3178 `NHCM_BV0383` (HCM) | BỆNH VIỆN BỆNH NHIỆT ĐỚI | hoa/thường |
| 2875 `NĐT_BV0331` (Đồng Tháp) / 2906 `NHCM_BV0359` (HCM) | BỆNH VIỆN MẮT | hoa/thường |
| 1542 `BPT_BV0107` (Phú Thọ) / 3192 `TĐNA_BV0396` (Đà Nẵng) | Phù Ninh / Phú Ninh | 1 dấu |

### Quyết định của user

Giữ cách khớp theo **tên**, nhưng so sánh bằng `utf8mb4_bin` → phân biệt **cả dấu lẫn hoa/thường**,
vẫn bỏ qua khác biệt khoảng trắng như trước.

Đã kiểm chứng trên MySQL 8.0.30:

| Cách so | Phù ≠ Phú | MẮT ≠ Mắt | ABC ≠ Abc |
|---|---|---|---|
| `utf8mb4_unicode_ci` (cũ) | ❌ | ❌ | ❌ |
| `utf8mb4_0900_as_ci` | ✅ | ❌ | ❌ |
| **`utf8mb4_bin`** (chọn) | ✅ | ✅ | ✅ |

Rủi ro đã báo user: `CÔNG TY TNHH ABC` và `Công ty TNHH ABC` sẽ thành 2 khách trùng.

### Task

- [x] Sửa `CategoryCustomerImport::SQL_NAME_NO_SPACE` — bỏ thêm khoảng trắng cứng `U+00A0` cho khớp với `compactSpaces()` phía PHP
- [x] Sửa `CategoryCustomerImport::findCustomerByName()` — thêm `COLLATE utf8mb4_bin` ở vế cột, vế tham số dùng `CONVERT(? USING utf8mb4)`
- [x] Không đụng các lookup danh mục (`CustomerGroup`, `CustomerType`, `CustomerArea`, `CustomerProvince`) — vẫn để so lỏng như cũ
- [x] Test lại

**Lưu ý cú pháp:** không đặt `COLLATE` trực tiếp lên dấu `?` — MySQL báo
`ERROR 1253 COLLATION 'utf8mb4_bin' is not valid for CHARACTER SET 'binary'`.
Phải viết `... COLLATE utf8mb4_bin = CONVERT(? USING utf8mb4)`.

### Kết quả test (DB `thanhan_stag_22092026`)

| Tên đưa vào | Trước khi sửa | Sau khi sửa |
|---|---|---|
| `Bệnh Viện Mắt` | 2875 `NĐT_BV0331` (Đồng Tháp) ❌ | **2906 `NHCM_BV0359`** (HCM) ✅ |
| `BỆNH VIỆN MẮT` | 2875 | **2875 `NĐT_BV0331`** ✅ |
| `Bệnh   Viện    Mắt` | 2875 | 2906 ✅ (vẫn bỏ qua khoảng trắng) |
| `bệnh viện mắt` | 2875 | **không tìm thấy** → sẽ tạo khách mới (đánh đổi đã chấp nhận) |
| `Trung tâm Y tế khu vực Phù Ninh` | 1542 | 1542 `BPT_BV0107` (Phú Thọ) ✅ |
| `Trung tâm Y tế khu vực Phú Ninh` | 1542 ❌ | **3192 `TĐNA_BV0396`** (Đà Nẵng) ✅ |
| `CÔNG TY CỔ PHẦN  IDICS` | 3312 | 3312 `BHN_TM0580` ✅ |

Không đụng tới các lookup danh mục (`CustomerGroup`, `CustomerType`, `CustomerArea`,
`CustomerProvince`) — vẫn so lỏng như cũ vì đối chiếu với danh mục cố định.

**Cảnh báo cho lần import tới:** tên chỉ lệch hoa/thường so với dữ liệu trong DB giờ sẽ
**tạo khách mới** thay vì update. Nên chạy thử trên bản sao DB trước khi import file cũ.

### Checkpoint — 2026-09-22 (Phase 14)
Vừa hoàn thành: sửa `findCustomerByName()` dùng `utf8mb4_bin`, bỏ thêm khoảng trắng cứng, test 8 ca đều đúng
Đang làm dở: không
Bước tiếp theo: user commit + deploy 2 file, chạy `--fix-zero --dry-run` trên server rồi gửi output
Blocked: không
