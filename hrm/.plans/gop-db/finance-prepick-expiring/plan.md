# Hàng sắp hết hạn giữ (ERP → HRM) — PLAN

> Đọc [design.md](./design.md) trước. File này chỉ liệt kê **việc phải làm theo thứ tự**.
> Trạng thái: **CODE XONG + ĐÃ VERIFY TRÌNH DUYỆT** (2026-09-03) — xem mục Tiến độ cuối file.

## Môi trường

| | |
|---|---|
| Nhánh gốc | **`gop_db`** (bắt buộc — feature này nằm trong đợt gộp DB) |
| Nhánh làm việc | `feat/finance-prepick-expiring` (đã tạo ở cả 2 repo, cắt từ `gop_db`) |
| Worktree BE | `hrm-api/.worktrees/finance-prepick-expiring` (tái sử dụng worktree cũ của YC nhập hàng — đã có `vendor/`) |
| Worktree FE | `hrm-client/.worktrees/finance-prepick-expiring` (đã có `node_modules/` + `.nuxt/`) |
| Nhánh cũ | `feat/finance-product-import-request` **giữ nguyên**, đã đẩy hết lên origin, chỉ là không còn checkout ở worktree nào |

## Nguyên tắc xuyên suốt

1. **KHÔNG viết service mới.** Toàn bộ truy vấn dùng lại `PrepickStockReportService` của màn
   Danh sách hàng giữ. Màn mới chỉ khác **một điều kiện ngày**.
2. `applyPrepickFilters()` là **choke point duy nhất** — đã được gọi ở cả 5 chỗ (tầng 1 dòng 393,
   tầng 2+3 dòng 658, export/print dòng 1058). Thêm điều kiện ở đó là mọi tầng đều ăn theo.
3. **KHÔNG sửa điều kiện ngày của ERP** (user chốt) — bê nguyên `hôm nay BETWEEN expire_date AND
   expire_date + warning_day`.
4. Đụng vào file đang chạy của màn khác (`PrepickStockReportService`, `PrepickExtendRequestService`)
   → **test lại màn đó** ngay trong cùng bước.

---

## Giai đoạn 1 — BE: hàm dùng chung `warning_day`

**1.1** Tạo `Modules/Finance/Services/PrepickConfigService.php`:

- `warningDay(): int` — đọc `configs.warning_day` (1 dòng bảng `configs` của ERP, không cache tĩnh).
- `maxPrepickDate(): int`.
- `warningDate(): Carbon` = `today + warningDay`.
- Docblock ghi rõ **"Nơi đang dùng"**: màn Yêu cầu gia hạn hàng giữ + màn Hàng sắp hết hạn giữ.

**1.2** `PrepickExtendRequestService`: bỏ 2 hàm `private config()` / `warningDate()` (dòng ~204-237),
inject `PrepickConfigService` qua constructor, sửa 3 chỗ gọi (`maxExpireDate()`, `warningDate()`,
`dataToCreate()` dòng 254).

**1.3 ⚠️ Test lại màn Yêu cầu gia hạn hàng giữ** — mở form Thêm, xác nhận bảng lô vẫn ra đúng số
dòng như trước khi tách. Đây là điều kiện để đi tiếp.

---

## Giai đoạn 2 — BE: cờ `expiring_only` trong service báo cáo

**2.1** `PrepickStockReportService`:

- Thêm hằng + method `applyExpiringWindow($query, string $alias)`:

      $alias.expire_date <= CURDATE()
      AND $alias.expire_date >= DATE_SUB(CURDATE(), INTERVAL :warning_day DAY)

  (viết đúng nghĩa `whereRaw` cho dễ đọc, tương đương `? BETWEEN expire_date AND expire_date + N`
  của ERP — xem design.md mục 3).
- Trong `applyPrepickFilters()`: `if ($request->boolean('expiring_only')) { $this->applyExpiringWindow(...); }`
- Inject `PrepickConfigService`.
- Bổ sung docblock đầu class: service này giờ phục vụ **2 màn**, liệt kê cả 2.

**2.2 ⚠️ Test lại màn Danh sách hàng giữ** — không gửi `expiring_only` thì kết quả phải y hệt trước.

**2.3** `PrepickExpiringController` (`Modules/Finance/Http/Controllers/V1/`):

- Copy khuôn `PrepickStockController` (139 dòng), **6 endpoint** `index / meta / details / logs / export / print`.
- Mỗi endpoint `$request->merge(['expiring_only' => 1])` **trước** khi gọi service.
  *(Riêng `logs` không cần — `logsOfLot()` nhận thẳng 4 id, không đi qua `applyPrepickFilters()`.)*
- Gate quyền: dùng lại `$this->service->canAccess()`; câu 403 đổi thành
  `Bạn không có quyền xem danh sách hàng sắp hết hạn giữ`.
- **KHÔNG** gắn middleware spatie (quyền ERP `guard_name = web`, middleware sẽ ném `PermissionDoesNotExist`).
- **GIỮ endpoint `logs`** (khảo sát lại 2026-09-03 — xem mục cuối file). Copy y nguyên từ `PrepickStockController::logs()`, gọi `logsOfLot()` đã có sẵn.

**2.4** `Modules/Finance/Routes/api.php`: thêm nhóm `/prepick-expiring` ngay sau nhóm
`/prepick-stocks` (dòng 590-599), **route tĩnh khai trước**.

---

## Giai đoạn 3 — FE: màn danh sách

**3.1** Copy `pages/finance/prepick-stocks/` → `pages/finance/prepick-expiring/`
(`index.vue` 879 dòng · `print.vue` 248 dòng · `components/export-excel.js` 129 dòng).

**3.2** Sửa trong bản copy:

| Việc | Chi tiết |
|---|---|
| Khóa lưu cấu hình | `columnScreenKey` + `localStorageKey` → `finance_prepick_expiring` (**grep kiểm trùng** trước khi đặt) |
| Đường dẫn API | `/v1/finance/prepick-stocks` → `/v1/finance/prepick-expiring` (5 chỗ) |
| Tiêu đề màn | `Hàng sắp hết hạn giữ` (`PageTitleMixin`) |
| Ô lọc Kho | **GIỮ** (user chốt 2026-09-03) — để đồng bộ với màn Danh sách hàng giữ, nơi lọc Kho đã hoạt động thật qua `applyProductFilters()` dòng 320-330. Không sửa gì trong bản copy |
| Ô lọc Trạng thái | Chỉ để **Hết hạn / Đến hạn** — dữ liệu màn này không bao giờ có *Trong hạn* (xem design.md mục 8) |
| Khối tổ chức | Giữ nguyên `company_id` / `department_id` / `part_id` / `employee_id` trong `initialStateForm` — Vue 2 không reactive với property chưa khai |
| Cột Kho | Màn anh em không có cột Kho ở tầng 1 → không phải làm gì (ERP có cột này nhưng `prepick_details` không gắn kho, số hiển thị sẽ vô nghĩa) |

**3.3** Nút **Lịch sử giữ hàng** ở cột Hành động: **GIỮ**. Modal đã là component dùng chung
`components/finance/prepick/PrepickStockLogModal.vue` → chỉ cần giữ nguyên bản copy, không sửa gì.
Nút chỉ hiện ở dòng `_level === 2` (tầng 3 — từng lô); tầng 0/1 để trống.

**3.4** ⚠️ **Bỏ hết `|| '—'` trong bản copy.** Màn anh em đang in dấu `—` cho ô rỗng
(index.vue dòng 125, 162, 166, 187) — đó là rule CŨ, rule hiện hành (22/08/2026) là **ô rỗng để
TRỐNG**. Copy nguyên là mang cái sai sang màn mới.

**3.5** Cột **Hạn giữ** + **Trạng thái** đã có sẵn trong khuôn copy — chúng chỉ có giá trị ở
**tầng 3** (mỗi lô một hạn), tầng 1 và tầng 2 để trống. Đây là đúng, không phải thiếu dữ liệu:
một hàng hoá gộp từ nhiều lô có hạn khác nhau.

**3.6** Gắn `link: '/finance/prepick-expiring'` vào
[`components/subsystem-menu/finance.js:178`](hrm-client/components/subsystem-menu/finance.js#L178)
(mục `{ label: 'Hàng sắp hết hạn giữ' }` đang thiếu `link`).

---

## Giai đoạn 4 — Đối chiếu ngược + tự kiểm (Bước 5-6 của skill)

**4.1** Mở song song 2 màn, đối chiếu từng dòng bảng nghiệp vụ ở design.md mục 2:

- Màn ERP (dữ liệu thật): `http://erp-crm.eteksofts.com/admin/warehouse/warehouse_infos/accountingExpiringPrepick`
- Màn HRM vừa dựng.
- **Số dòng tầng 1 phải bằng nhau.** Lệch = cờ `expiring_only` hoặc `applyViewScope()` sai.
- ⚠️ Tầng 2+3 của ERP **luôn rỗng** (lỗi E1) → không có gì để đối chiếu; bản HRM phải ra dữ liệu.
  Kiểm chéo bằng cách mở cùng hàng hoá đó trên màn **Danh sách hàng giữ** của HRM.

**4.2** Chạy grep tự kiểm trên **cả thư mục** `pages/finance/prepick-expiring/`:

    grep -rn "status-pill\|statusPillClass"   pages/finance/prepick-expiring/
    grep -rn "interactable:\|disabledTitle"   pages/finance/prepick-expiring/
    grep -rn "action\.key ==="                pages/finance/prepick-expiring/
    grep -rn "V2BaseFilterPanel"              pages/finance/prepick-expiring/
    grep -rn "advanced-filters"               pages/finance/prepick-expiring/

**4.3** Checklist bấm thật trên trình duyệt (Playwright, **chờ ≥3s** sau mỗi lần đổi bộ lọc):

- [ ] Bấm **từng ô lọc**, đối chiếu param trên tab Network với tên field BE đọc
      (`product_code` / `product_name` / `brand_id` / `model_id` / `status` / `employee_id` / khối tổ chức)
- [ ] Nút **Làm mới** xóa điều kiện **và** nạp lại danh sách
- [ ] Vào chi tiết rồi quay lại → bộ lọc còn nguyên
- [ ] Bung/thu tầng 2+3, đổi **Đơn vị** → mọi số lượng của cả 3 tầng quy đổi theo
- [ ] Phân trang: mặc định 10, đổi số dòng nhảy về trang 1
- [ ] Sort từng cột có `sortable`, sort cột mới hủy sort cột cũ
- [ ] **Cấu hình cột**: STT / Mã / Hành động không tắt được
- [ ] **Xuất Excel**: mở popup chọn trường trước, thứ tự cột theo thứ tự tick, file có token (không 401)
- [ ] **In**: bố cục gom Phòng ban → Nhân viên → Hàng hoá, nút In canh phải
- [ ] Bảng rỗng hiện "Không có dữ liệu phù hợp"
- [ ] Ô rỗng để **TRỐNG** (không `—`, không `-`)
- [ ] Số theo chuẩn quốc tế `1,234,567.89`; ngày `dd/mm/yyyy`
- [ ] Đăng nhập bằng tài khoản **không** có quyền `Quản lý giữ hàng` → không thấy mục menu, API trả 403
- [ ] **Đóng browser Playwright** khi xong

---

## Không làm trong đợt này

- Không sửa điều kiện ngày cho xuôi (user chốt giữ ERP).
- Không port bản cá nhân `expiringPrepick` thành màn riêng.
- Không tạo migration — dùng lại quyền `Quản lý giữ hàng` (100427) và 3 quyền phạm vi (100839/840/841).
- Không đụng `PrepickStockService` (nơi duy nhất **GHI** `prepick_details` / `prepick_logs`).

---

## Điểm cần user xác nhận khi bắt đầu code

1. ~~Ô lọc Kho~~ → **chốt GIỮ** (2026-09-03), đồng bộ với màn Danh sách hàng giữ.
2. ~~Popup Lịch sử giữ hàng~~ → **chốt GIỮ** (2026-09-03). Khảo sát lại cho thấy:
   - **Chi phí gần bằng 0**: modal đã tách sẵn thành component dùng chung
     `components/finance/prepick/PrepickStockLogModal.vue`, truy vấn `logsOfLot()` đã viết xong
     (dòng 704-780, kèm cả phần dựng link chứng từ). Endpoint mới chỉ là 8 dòng copy.
   - **Bỏ lại tốn công HƠN giữ**: không còn hành động nào thì cột "Hành động" rỗng hoàn toàn →
     theo rule phải bỏ luôn cột, mà cột này đang `locked: true` trong cấu hình cột → phải sửa
     thêm cả `columnConfigList`.
   - **Hợp ngữ cảnh hơn cả màn gốc**: màn này toàn lô ĐÃ quá hạn, câu hỏi tiếp theo của user luôn
     là "lô này đã gia hạn / điều chuyển / hủy gì chưa" — đúng là nội dung sổ biến động.
   - Cùng lý do đã chốt cho ô lọc Kho: **2 màn anh em phải đồng bộ**.


---

## Tiến độ

### Checkpoint — 2026-09-03

**Vừa hoàn thành:**

- [x] **1.1** `Modules/Finance/Services/PrepickConfigService.php` — mới (`warningDay` / `maxPrepickDate` /
      `warningDate` / `maxExpireDate`), docblock ghi "Nơi đang dùng".
- [x] **1.2** `PrepickExtendRequestService` — bỏ 2 hàm `private`, inject `PrepickConfigService`,
      sửa 3 chỗ gọi. Diff 9+/19- (không phá CRLF).
- [x] **1.3** Test lại màn Gia hạn: `warning_day=7`, `max_prepick_date=30` →
      `warningDate=2026-09-10`, `maxExpireDate=2026-10-03`; `dataToCreate(781, 1)` trả **161 dòng**,
      không lỗi. DI container resolve được cả 2 service.
- [x] **2.1** `PrepickStockReportService` — inject config service, thêm `applyExpiringWindow()` +
      cờ `expiring_only` trong `applyPrepickFilters()`; docblock đầu class ghi rõ phục vụ 2 màn.
- [x] **2.2** **Đối chiếu SQL với ERP**: điều kiện ERP `CURDATE() BETWEEN expire_date AND
      expire_date + 7` và bản HRM `expire_date <= CURDATE() AND >= CURDATE() - 7` cho **cùng
      13 lô / 13 hàng hoá** trên DB local → khớp 100%.
- [x] **2.3** `PrepickExpiringController` — 6 endpoint, `scoped()` tự merge cờ, hằng
      `MSG_FORBIDDEN`. `logs` KHÔNG merge cờ (có lý do trong docblock).
- [x] **2.4** Route `/prepick-expiring` — 6 route đã đăng ký đúng controller.
- [x] **BE verify qua HTTP thật** (`php artisan serve :8199`, JWT của `namdangit@gmail.com`):
      `index` 200 total **13** · `meta` 200 · `details` 200 (1 NV, 1 lô, "Hết hạn") ·
      `logs` 200 (1 dòng, chứng từ ĐCHG-01224) · `export` 200 **13 dòng** · `print` 200
      (`over_limit=false`, 7.346 ký tự HTML). Màn cũ `prepick-stocks` vẫn 200 total **895**.
- [x] **3.1-3.6** FE: copy `pages/finance/prepick-expiring/` (index + print + export-excel),
      đổi `columnScreenKey`/`localStorageKey`/`pathsToKeep`/`modal-id`/5 đường dẫn API/tiêu đề,
      bỏ hết `|| '—'` (10 chỗ), lọc "Trong hạn" khỏi ô Trạng thái, gắn `link` menu
      `finance.js:184`. Compile sạch bằng `vue-template-compiler` + `@babel/parser`.
- [x] 5 lệnh grep tự kiểm của skill: **sạch**.

**⚠️ Đã đụng 1 file dùng chung — CẦN USER BIẾT:**
`components/finance/prepick/PrepickStockLogModal.vue` thêm prop `apiPath`
(mặc định `'finance/prepick-stocks/logs'`). Thay đổi **thuần bổ sung**, màn Danh sách hàng giữ
không khai prop nên chạy y như cũ. Màn mới truyền `finance/prepick-expiring/logs` để đi đúng gate
quyền của nó.

**Bước tiếp theo:** chạy checklist bấm thật trên trình duyệt (mục 4.3) — Nuxt dev đang lên ở
`http://127.0.0.1:3010`, API worktree ở `http://127.0.0.1:8199`.

**Blocked:** không.

### Ghi chú phát sinh

- Ô lọc **Trạng thái** đã chốt: bỏ lựa chọn *Trong hạn* (hằng FE `STATUS_TRONG_HAN`), vì cửa sổ
  ngày của màn không bao giờ sinh ra dòng nào ở trạng thái đó.
- Màn cũ *Danh sách hàng giữ* vẫn đang in `—` cho ô rỗng — **không sửa** (ngoài phạm vi yêu cầu),
  chỉ bỏ ở bản copy.
- Mục menu phân hệ Tài chính **không có khoá `permission`** cho bất kỳ mục nào, nên màn mới cũng
  không gate ở menu — giống hệt màn anh em. Chốt chặn thật là 403 của BE (`canAccess()`).
  Nếu muốn gate cả menu thì phải đổi cho **cả nhóm**, không làm riêng 1 mục.


### Checkpoint 2 — 2026-09-03, đã bấm thật trên trình duyệt

Chạy `php artisan serve :8199` (worktree BE) + `nuxt dev :3010` (worktree FE), đăng nhập
`namdangit@gmail.com`, bấm thật bằng Playwright:

| Hạng mục | Kết quả |
|---|---|
| Vào màn `/finance/prepick-expiring` | 200, tiêu đề "Hàng sắp hết hạn giữ", **13 bản ghi**, phân trang 10/trang, console 0 lỗi |
| 9 ô lọc | Đủ: Mã hàng hóa · Tên hàng hóa · **Lọc theo kho** · Thương hiệu · Model · Trạng thái · Nhân viên · Công ty · Phòng ban. Placeholder đúng chuẩn `Chọn <X>` |
| Ô Trạng thái | Chỉ còn **Hết hạn / Đến hạn** — đã bỏ "Trong hạn" |
| Lọc Trạng thái = Đến hạn | 0 dòng + đúng câu "Không có dữ liệu phù hợp bộ lọc." |
| Nút **Làm mới** | Xoá điều kiện **và** nạp lại → về 13 dòng |
| Cây 3 tầng | Bung ra đúng: hàng hoá → `Đào Phúc Sơn / PHÒNG DỰ ÁN` → lô `SL 1, 31/08/2026, Hết hạn` |
| Nút **Lịch sử giữ hàng** | Mở popup, gọi ĐÚNG `/finance/prepick-expiring/logs`, hiện sổ biến động + chứng từ ĐCHG-01224 |
| **Cấu hình cột** | 11 cột, 3 cột khoá (STT / Mã / Hành động) |
| **Xuất Excel** | Popup "Chọn trường xuất Excel" mở trước; tải về `hang_sap_het_han_giu.xlsx` — 15 dòng (1 tiêu đề + 1 header + **13 dữ liệu**), tiêu đề "DANH SÁCH HÀNG SẮP HẾT HẠN GIỮ" |
| **In** | `/finance/prepick-expiring/print` render đúng: gom Phòng ban → Nhân viên → Hàng hoá, 2 phòng ban / 2 NV / 13 mục |
| Ô rỗng | **Trống hoàn toàn**, không còn dấu `—` nào trên bảng |
| Màn cũ `/finance/prepick-stocks` | Vẫn chạy bình thường, lọc Trạng thái = Đến hạn → 0 dòng; tiêu đề bản in vẫn "DANH SÁCH HÀNG GIỮ" |

**Sửa thêm trong lúc verify:**

1. Còn sót **4 chỗ** `<span v-else class="field-line">—</span>` (cột Model / Thương hiệu / Trạng
   thái / Tổng SL) — grep `|| '—'` không bắt được vì đây là nhánh `v-else`. Đã bỏ hết.
2. Bản in dùng chung blade `finance::prints.prepick-stock-list` nên tiêu đề vẫn ra "DANH SÁCH HÀNG
   GIỮ". Đã cho blade nhận biến `$title` (**mặc định giữ nguyên chuỗi cũ** → màn cũ không đổi),
   `renderPrintList($request, $title)` thêm tham số có giá trị mặc định, controller màn mới truyền
   "DANH SÁCH HÀNG SẮP HẾT HẠN GIỮ". Đã thử lại cả 2 màn: mỗi màn ra đúng tiêu đề của mình.

**Còn lại / chưa làm được:**

- **Chưa thử tài khoản KHÔNG có quyền** `Quản lý giữ hàng` (chỉ có 1 tài khoản test, là admin).
  Gate 403 dùng CHUNG `canAccess()` với màn Danh sách hàng giữ nên tin được về mặt code, nhưng
  **chưa nghiệm thu bằng tài khoản thật**.
- Chưa đối chiếu số dòng với **cổng ERP thật** (`erp-crm.eteksofts.com`) — mới đối chiếu bằng SQL
  trên DB local: 2 cách viết điều kiện cho cùng 13 lô / 13 hàng hoá.
- Popup Lịch sử (component dùng chung) vẫn in `—` ở ô Khách hàng rỗng — **không sửa** vì màn cũ
  đang dùng chung; cần user quyết có đồng bộ rule "ô rỗng để trống" cho component này không.


### Checkpoint 3 — 2026-09-04, nghiệm thu PHÂN QUYỀN

Nghiệm thu bằng **JWT phát trực tiếp** (`JWTAuth::fromUser()`) cho 5 nhân viên thật rồi gọi API —
**KHÔNG gán/sửa/xoá một dòng quyền nào**, DB giữ nguyên. Cả 5 nhánh của `applyViewScope()` đều có
sẵn người giữ đúng hồ sơ quyền nên không cần cấp thêm.

| Nhánh | Nhân viên | `/prepick-expiring` | `/prepick-stocks` | `can_view_all_companies` |
|---|---|---|---|---|
| KHÔNG có `Quản lý giữ hàng` | 25 – Nguyễn Thị Cần | **403** | 403 | 403 |
| `Xem theo tổng công ty` | 100 – Nguyễn Minh Tân | 200 · 11 | 200 · 895 | `true` |
| `Xem theo công ty` | 157 – Trần Thị Thu Hương | 200 · 11 | 200 · **620** | `false` |
| `Xem theo phòng ban` | 148 – Đỗ Đăng Hiếu (quản lý phòng 55) | 200 · 11 | 200 · **56** | `false` |
| Không quyền phạm vi nào | 27 – Chu Khương Duy | 200 · **0** | 200 · 70 | `false` |

- **Cả 6 endpoint** (`index/meta/details/logs/export/print`) đều trả 403 với câu riêng của màn:
  *"Bạn không có quyền xem danh sách hàng sắp hết hạn giữ"*; màn cũ vẫn giữ câu
  *"...danh sách hàng giữ"* → hai màn không lẫn thông báo.
- Nhánh **phòng ban** kiểm chứng đúng chất: NV 148 quản lý phòng 55 — đúng phòng của NV 781 đang
  giữ 11 lô → xổ chi tiết ra thấy `Đào Phúc Sơn / PHÒNG DỰ ÁN`. (Lần thử đầu ra 0 vì chọn nhầm
  người quản lý phòng 81, không phải lỗi code.)
- Nhánh **không quyền phạm vi** chứng minh fallback "chỉ thấy lô của mình": màn expiring 0 dòng
  nhưng màn Danh sách hàng giữ vẫn 70 — họ có hàng giữ riêng, chỉ là không lô nào đang trong cửa sổ.
- Số thu hẹp dần đúng thứ tự phạm vi: 895 (tổng) > 620 (công ty) > 70 (cá nhân) > 56 (phòng ban).

⚠️ **Cửa sổ ngày là ĐỘNG** — đồng hồ sang 04/09 giữa buổi test, 2 lô hạn 27/08 rơi khỏi cửa sổ
`[hôm nay-7, hôm nay]` nên số hàng hoá đổi **13 → 11**. Con số trong Checkpoint 2 (13) và
Checkpoint 3 (11) đều đúng tại thời điểm đo. Khi QA đối chiếu với ERP phải đo **cùng ngày**.

**Trạng thái: hết việc trong plan.** Còn duy nhất 1 điểm chưa làm được tại chỗ: đối chiếu số dòng
với cổng ERP thật `erp-crm.eteksofts.com` (mới đối chiếu bằng SQL trên DB local).


### Checkpoint 4 — 2026-09-04, đối chiếu với ERP dev `erp-crm.eteksofts.com`

⚠️ **DB dev KHÁC DB local** (dev 885 hàng hoá có tồn giữ, local 895) nên **không đối chiếu được số
dòng**. Đối chiếu 2 thứ đối chiếu được: **bộ cột/bộ lọc** và **ngữ nghĩa cửa sổ ngày**.

**Khớp bảng nghiệp vụ ở design.md mục 2 — không sót, không thừa:**

| Hạng mục | ERP dev | Bản HRM |
|---|---|---|
| Cột tầng 1 | Tên hàng hóa · Đơn vị · **Kho** · Model · Mã hàng hóa · Thương hiệu · Tổng SL trong kho · SL giữ | khớp, trừ cột Kho (bỏ có chủ đích) |
| Bộ lọc | Lọc theo kho · Phòng ban · Nhân viên · Thương hiệu · Model · Tên hàng · Mã hàng | khớp, + Trạng thái/Công ty theo chuẩn HRM |
| Ô Đơn vị | select đổi đơn vị trên từng dòng (7/7 dòng) | khớp |
| Nút Thêm/Sửa/Xoá/Xuất/In/Import | **KHÔNG có nút nào** trên toolbar | khớp (HRM bổ sung Xuất/In theo chuẩn) |

**3 điều kiểm chứng được bằng dữ liệu thật trên dev:**

1. **Lỗi E1 tái hiện 100%** — bung chi tiết ở **mọi** hàng hoá đều ra "Chưa có dữ liệu". Không còn
   là suy đoán từ code nữa. Bản HRM ra dữ liệu thật → tốt hơn ERP.
2. **Cột "Kho" trên dev in ra `-` ở mọi dòng** → cột này vô nghĩa vì `prepick_details` không gắn
   kho. Xác nhận quyết định bỏ cột Kho là đúng.
3. **Cửa sổ ngày đúng như phân tích.** Gọi thẳng `prepickSearchData?type=accounting_expiring` trên
   dev (tầng 1 có trả `expire_date` dù bảng không hiện): 7/7 dòng có hạn **29/08 · 31/08 · 02/09 ·
   31/08 · 30/08 · 30/08 · 30/08** — tất cả `<= hôm nay (04/09)` và `>= hôm nay - 7`,
   **KHÔNG một ngày nào ở tương lai**. Đây là bằng chứng sống rằng màn ERP lọc hàng **ĐÃ quá hạn
   trong `warning_day` ngày qua**, khớp đúng công thức bản HRM đang giữ.

**Lỗi E4 cũng tái hiện luôn:** gọi tầng 1 KHÔNG kèm `type` (màn Danh sách hàng giữ) thì
`expire_date` trả về toàn ngày **2025** — là hạn của **một lô bất kỳ** trong nhóm `GROUP BY
product_id`, không phải hạn thật của lô nào đang xét. Vì thế **không thể** lọc lại tập đó bằng
công thức ngày để so với tập 7 dòng của màn expiring — phép so đó vô nghĩa, không phải bản HRM
lệch. Bản HRM đã bỏ hẳn 2 cột `employee_id`/`expire_date` khỏi tầng 1 nên không dính lỗi này.

**Tương đương công thức** đã chứng minh riêng bằng SQL trên **cùng một DB** (local): điều kiện ERP
`CURDATE() BETWEEN expire_date AND expire_date + 7` và bản HRM
`expire_date <= CURDATE() AND >= CURDATE() - 7` cho **cùng bộ lô, cùng bộ hàng hoá**.

**→ Hết việc trong plan. Không còn hạng mục treo.**


### Checkpoint 5 — 2026-09-04, sau khi merge: dropdown "Lọc theo kho"

User đối chiếu ảnh 2 cổng, thấy danh sách kho khác nhau. Khảo sát ra **khác BẢNG**, không phải khác
dữ liệu do khác DB — chi tiết ở design.md mục 8b.

- **Nguồn kho: GIỮ NGUYÊN** `accounting_warehouses`. Không đổi sang kho vật lý như ERP vì bộ lọc và
  cột "Tổng SL trong kho" đều chạy trên `accounting_stocks.accounting_warehouse_id`.
- **Kho đã khóa: bỏ, CHỈ ở màn mới.** `warehouseOptions(bool $onlyActive = false)` — mặc định giữ
  hành vi cũ; `filterMeta()` truyền `$request->boolean('expiring_only')`.
- Đo lại: màn Hàng sắp hết hạn giữ **45 kho** (hết "SG03 - Chờ xóa"), màn Danh sách hàng giữ vẫn
  **55 kho** y như trước.
- Commit `7bccb5e23`, đã fast-forward vào `gop_db`.

⚠️ Ghi để lần sau khỏi mất công: `Employee::getAccountingWarehousesAttribute()` của ERP **tên là
accounting_warehouses nhưng query bảng `warehouses`** (kho vật lý), lọc theo `warehouse_accountants`.
Đọc tên hàm mà suy ra bảng là sai.
