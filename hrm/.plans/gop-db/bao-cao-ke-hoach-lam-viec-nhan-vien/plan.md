# Plan — Báo cáo kế hoạch & kết quả làm việc theo nhân viên (Mockup UI)

**Người phụ trách:** @dnsnamdang
Xem `design.md` cùng thư mục cho spec đã chốt.
File duy nhất: `bao-cao-ke-hoach-lam-viec-nhan-vien.html` (standalone) + `screenshots/`.

## Global Constraints (áp cho MỌI task)

- Mockup HTML tĩnh 1 file, KHÔNG thư viện ngoài; toàn bộ tiếng Việt.
- Port nguyên khối `<style>` của `../../bao-cao-phat-trien-thi-truong-khach-hang/`; phần riêng để CUỐI khối style dưới nhãn *"BỔ SUNG RIÊNG MÀN KẾ HOẠCH LÀM VIỆC"*.
- Data demo sinh bằng **LCG có hạt giống** (không `Math.random`) — demo không nhảy số. Thêm trường mới phải tính bằng công thức theo số thứ tự, KHÔNG gọi `demoRnd()`, nếu không lệch toàn bộ số liệu đã chốt.
- Định nghĩa chỉ tiêu **bám Entity thật** trong `hrm-api/Modules/Assign` — không bịa trạng thái.
- Mọi diễn giải / công thức nằm trong tooltip icon `i`, không viết chữ ra màn.
- **Task đụng giao diện BẮT BUỘC verify Playwright trên trình duyệt thật, ĐO BẰNG SỐ LẤY TỪ DOM** — không chỉ nhìn ảnh.
- ⚠️ `scrollWidth` của phần tử **có icon ⓘ** KHÔNG đáng tin: tooltip `::after` absolute 246px luôn thổi phồng nó. Đo bề rộng chữ thật bằng `Range.selectNodeContents()`.

## Phase 1 — Dựng màn (2026-09-07)

### Task 1: Brainstorming + chốt spec
- [x] Đọc mockup mẫu + `design.md` của `bao-cao-phat-trien-thi-truong-khach-hang`.
- [x] Rà Entity thật để định nghĩa 5 nguồn: `meetings` · `tasks` · `issues` · `assign_business` · `assign_jobs`.
- [x] Chốt 5 quyết định lớn: 10 cột · **overlap** với kỳ · tính cho **mọi người tham gia** · nháp/huỷ **vẫn tính** (⇒ tách 4 nhóm trạng thái) · bỏ mọi chỉ số bình quân.
- [x] Ghi `design.md`; user chốt **bỏ `plan.md` giai đoạn dựng**, dựng thẳng mockup.

### Task 2: Dựng file mockup
- [x] Port CSS + dựng markup (topbar · toolbar · dải tổng hợp · bảng · drawer · 2 popup · toast · `#print-area`).
- [x] Data demo: 2 công ty · 10 phòng ban · 30 NV · **2.560 chứng từ** phẳng hoá thành cặp (chứng từ × người).
- [x] Cây dựng **từ danh mục tổ chức** (không từ dữ liệu) → thứ tự dòng cố định + hiện được NV có 0 việc.
- [x] Popup drill-down · drawer chi tiết đầu việc · in A4 2 chế độ · xuất Excel `.xls`.
- [x] Verify Playwright 1600×900: **0 sai lệch / 19 dòng cha × 7 cột số**; 4 nhóm chia hết tổng; cấp Bộ phận chỉ hiện ở phòng có chia; **0 lỗi console**.

### Task 3: Fix lỗi phát hiện khi đo
- [x] Meta khối tổng hợp `nowrap` tràn **94px** khỏi khối 300px → đè tiêu đề. Rút ngắn meta + nới khối lên **404px** theo số đo.
- [x] Bản vá đầu đặt `overflow:hidden` lên tiêu đề → **cắt mất tooltip**. Giới hạn chỉ cắt ở `.rsum-blk__money`.
- [x] KPI popup thứ 3 đang là "bình quân" — trái yêu cầu đã chốt → đổi thành *Tỷ lệ việc chủ trì*.
- [x] Meeting không có % tiến độ → drawer đổi ô "Tiến độ" thành "Biên bản họp".

## Phase 2 — Tinh chỉnh theo phản hồi user (2026-09-07 → 08)

### Task 4: Cột thời gian có giờ (2026-09-07)
- [x] Cột **Kết thúc / Hạn** thêm giờ; sau đó chốt **MỌI ô thời gian đều ngày + giờ**, không trừ loại nào.
- [x] Khoá sắp xếp cộng cả giờ (trước chỉ so ngày → việc cùng ngày hoà nhau, nhìn như sắp sai).
- [x] Phát hiện `.drill-table { min-width: 1740px }` — số cứng của bảng **14 cột** màn mẫu — ép bảng 12 cột giãn ra, khiến **sửa `colgroup` hoàn toàn vô tác dụng**. Khai lại `table-layout: fixed` + `min-width` đúng của màn.
- [x] Verify: **2.054/2.054 ô** đúng dạng `dd/mm/yyyy HH:MM`; 974 cặp cùng ngày sắp đúng theo giờ.
- [ ] ⚠️ **Nợ backend**: `tasks` có `due_time` nhưng **KHÔNG có `start_time`** → muốn giờ bắt đầu của Task đúng như mockup phải bổ sung cột.

### Task 5: Luật ẩn cột/ô lọc theo chiều đã cố định (2026-09-07)
- [x] Gom 4 nguồn cố định vào `drillHiddenDims()`: path của node · metric là 1 loại · metric là 1 nhóm trạng thái · cờ "Chỉ tính việc chủ trì".
- [x] 2 luật phụ: metric `task`/`issue` bỏ cột **Vai trò** (DB chỉ có 1 `assignee_id`); phòng không chia bộ phận bỏ cột **Bộ phận**.
- [x] Số cột đổi theo popup ⇒ `min-width` khai **inline** theo tổng colgroup; In/Excel dùng `drillColumns(key)`.
- [x] Verify **quét 63 popup**: số cột co giãn 7–12, **không còn cột nào lặp 1 giá trị** (trừ 2 ca do dữ liệu ngẫu nhiên — giữ theo luật "chỉ ẩn theo chiều cố định, không ẩn theo dữ liệu").

### Task 6: Tiêu đề popup chữ thường + thêm cột sắp xếp (2026-09-07)
- [x] Ghi đè `text-transform: uppercase` của khuôn gốc → khớp bảng chính (`none` / `12px` / `letter-spacing: 0`).
- [x] Thêm sort cho **Bộ phận · Nhân viên · Trạng thái**; "—" (chưa có bộ phận) đẩy xuống cuối khi tăng dần.

### Task 7: Dòng meta tô màu theo loại (2026-09-07)
- [x] Tách `typeBreakdownHtml()` (có màu, chỉ dùng trên màn) khỏi `typeBreakdown()` (chữ thuần cho `data-tip` + bản in — nhét thẻ vào thuộc tính là hỏng tooltip).
- [x] Verify màu khớp 100% giữa **3 nơi**: dòng meta · chip lọc · ô số trong bảng.

### Task 8: Ô "Loại công việc" thành multi-select (2026-09-07)
- [x] Dropdown checkbox bám đúng thông số `.calendar-filter-select` (30px · `#cbd5e1` · 6px · 12px) — KHÔNG dùng `<select multiple>` (bung nhiều dòng, phá bố cục, mất chấm màu).
- [x] Nhãn co theo số loại; "Tất cả loại" có trạng thái **indeterminate**; mỗi dòng kèm **số đầu việc theo bộ lọc hiện tại**.
- [x] Fix: bản đầu dựng lại panel sau mỗi tick → **thay mới checkbox, mất focus**. Tách `renderTypeValue` / `buildTypePanel` / `syncTypePanel`; verify **tick không đổi tham chiếu node**.

### Task 9: Popup chỉ còn 1 cột trạng thái (2026-09-08)
- [x] Bỏ cột trạng thái gốc; cột 4 nhóm đổi tên **"Tình trạng" → "Trạng thái"**; sort chuyển sang thứ tự `BUCKETS`; xoá `STATUS_ORDER` (thành code chết).
- [x] Drawer giữ trạng thái gốc dưới tên **"Trạng thái chứng từ"** để 2 ô không trùng tên.
- [x] Đổi đồng bộ nhãn toàn màn (ô lọc, khối *Trạng thái xử lý*, bản in) — bớt 1 cột nên popup **hết phải cuộn ngang**.

## Phase 3 — Đồng bộ mẫu bản 2026-09-08

### Task 10: Port 4 thay đổi của mockup mẫu
- [x] **Style bảng**: nền dòng cha tách theo cấp (`d0/d1/d2`) · vạch cấp `::before` nấc thang 22px · kẻ đậm 2px trên dòng cấp 0.
- [x] **Khối summary popup**: mặc định **thu gọn**, nút *Xem tổng hợp* ↔ *Thu gọn*, ẩn bằng `hidden` (không `style.display`). Bổ sung so với mẫu: **xoá nội dung cũ khi thu** để popup B không giữ số của popup A.
- [x] **Select chọn cấp** thay nút "Ẩn/Hiện chi tiết" — bung theo **TÊN CẤP** nên phòng không chia bộ phận không lòi nhân viên ra sớm. Xoá CSS `.rsum-tb__toggle-all` (code chết).
- [x] **Icon sort 2 mũi tên** chồng nhau, cả 2 mờ khi chưa sắp.
- [x] Verify: 10 → 19 → 49 dòng theo 3 nấc; **0 nhân viên lọt ra** ở nấc *Đến Bộ phận*; bản in vẫn đủ 50 dòng.

### Task 11: Nhân viên chưa có việc trong kỳ (2026-09-08)
- [x] User báo ô *"Chỉ hiện NV có việc"* bấm không thấy đổi gì — đo lại: **30/30 NV đều có việc**.
- [x] Chọn 6 người làm nhóm rảnh, tách khỏi `ACTIVE_EMPLOYEES`; lô chứng từ riêng nằm gọn **01/07 – 22/08** (kết thúc trước kỳ mặc định) ⇒ kỳ 09/2026 hiện 0 nhưng kỳ *Năm nay* vẫn có việc — không phải nhân viên ma.

### Task 12: Đồng bộ danh mục tổ chức + đưa nút lên thanh tiêu đề (2026-09-08)
- [x] Thay danh mục bằng bộ của mẫu: **2 công ty · 10 phòng ban · 2 bộ phận · 43 nhân viên** (tên thật Tân Phát), bỏ trường `markets`.
- [x] Nhóm 6 NV rảnh chọn **ngay trong 43 người**, không đẻ thêm người ngoài danh mục.
- [x] 2 nút **In / Xuất Excel** dồn về góc phải thanh tiêu đề navy (26px) — toolbar **118 → 68px**, bảng lên **y=308**.
- [x] Verify lại toàn bộ bất biến trên danh mục mới: **0 sai lệch / 12 dòng cha × 7 cột**; 530+266+174+70 = **1.040**; tắt Issue → 932; chủ trì → 659; 37/43 NV có việc.

---

### Checkpoint — 2026-09-08
**Vừa hoàn thành:** Task 12 — đồng bộ danh mục tổ chức của báo cáo phát triển thị trường (43 NV) và đưa 2 nút In / Xuất Excel lên thanh tiêu đề. Đã verify Playwright, console 0 lỗi.
**Đang làm dở:** không có. Mockup ở trạng thái dùng được, `design.md` (35KB) đã đầy đủ spec + gotcha + nhật ký đo.
**Bước tiếp theo:** chờ user chốt mockup. Sau khi chốt thì các việc còn lại là (1) viết SRS + testcase nếu cần, (2) port sang Vue thật ở `pages/assign/report/`, (3) dựng API BE.
**Blocked:** không có. Còn 1 mục nợ backend đã ghi ở Task 4 (`tasks.start_time`).

## Phase 3 — Chốt tên + cơ chế đếm trước khi port sang code (2026-09-21)

### Task 13: Đổi tên màn + định nghĩa báo cáo
- [x] Tên màn: **Báo cáo kế hoạch & kết quả làm việc theo nhân viên** — sửa `<title>`, `h1` topbar, `<h2>` bản in, tên file Excel (`Bao-cao-ke-hoach-ket-qua-lam-viec-theo-nhan-vien.xls`). **Giữ nguyên tên file mockup** để không phải sửa lại đường dẫn ở plan / ảnh chụp.
- [x] Định nghĩa báo cáo mới (tooltip ⓘ cạnh tiêu đề, đổi nhãn *MỤC TIÊU* → *ĐỊNH NGHĨA BÁO CÁO*): *theo dõi khối lượng và kết quả làm việc của từng nhân viên, biết ai đang nhiều việc, có khả năng thực hiện công việc hay không*.

### Task 14: Cơ chế đếm khi 1 phiếu có nhiều người tham gia
- [x] `metrics(list, byDoc)` + `groupByDoc(list)`: cấp **Nhân viên** +1 cho mỗi người tham gia; cấp **Bộ phận / Phòng ban / Công ty / dòng TỔNG / dải tổng hợp** đếm **theo phiếu**.
- [x] `typeCounts()` cũng đếm theo phiếu — trước đó panel *Loại công việc* đếm theo cặp nên **lệch với cột của dòng TỔNG**.
- [x] Nói rõ hệ quả *"dòng cha nhỏ hơn tổng dòng con"* ở **4 chỗ**: tooltip tiêu đề màn · ⓘ cột `Tổng` · ⓘ ô "Nội dung theo dõi" · chú thích dưới bảng + meta bản in.
- [x] **Không thêm cột "Lượt tham gia"** (user chốt): 2 con số nằm trong `title` ô `Tổng` của dòng cha — *"659 phiếu · 1040 lượt tham gia"*.

### Task 15: Popup chi tiết gộp theo phiếu
- [x] `drillByDoc(key)` — popup mở từ cấp cha gộp **1 dòng / phiếu**, ô Nhân viên / Phòng ban / Bộ phận hiện đại diện kèm `+N`, hover ra đủ tên (đại diện đứng đầu). **Bỏ cột + ô lọc Vai trò**.
- [x] **LỌC TRƯỚC trên cặp `(phiếu × người)` rồi MỚI GỘP** — làm ngược lại thì lọc 1 nhân viên vẫn kéo cả người khác trong phiếu ra.
- [x] Bản in chi tiết dùng `DETAIL_COLUMNS` + gộp theo phiếu để số dòng khớp con số ở đầu bản in.
- [x] KPI thứ 3 đổi tên thành *Tỷ lệ phiếu đơn vị chủ trì* ở popup gộp, và **ẩn hẳn** khi không cố định đơn vị nào (dòng TỔNG) vì luôn ra 100%.
- [x] Verify Playwright 1600×900, console **0 lỗi** — chi tiết phép đo ghi ở cuối `design.md`; ảnh `screenshots/klv-18-doi-ten-va-cach-dem-moi.png`.

---

### Checkpoint — 2026-09-21
**Vừa hoàn thành:** Task 13–15 — đổi tên màn, chốt định nghĩa báo cáo, đổi cơ chế đếm theo cấp và gộp popup theo phiếu. Đã verify Playwright (số đo trong `design.md`), console 0 lỗi, body không cuộn ngang.
**Đang làm dở:** không có.
**Bước tiếp theo:** port sang Vue ở `pages/assign/report/` + dựng API BE. Khi dựng BE nhớ tách **2 câu đếm**: cấp nhân viên `COUNT(*)` trên bảng người tham gia, cấp đơn vị `COUNT(DISTINCT <khoá phiếu>)`.
**Blocked:** không có. Vẫn còn nợ backend `tasks.start_time` (ghi ở Task 4).

---

## Phase 4 — Triển khai code (BE + FE)

> **Cho người/agent thực thi:** dùng skill `superpowers:subagent-driven-development` (khuyến nghị)
> hoặc `superpowers:executing-plans`, làm **từng task một**, không nhảy cóc.
>
> **Spec bắt buộc đọc trước:** `design.md` (nghiệp vụ + giao diện đã chốt trên mockup) và
> `design-phase4.md` (đường dẫn, hợp đồng API, ánh xạ DB, phân quyền). Plan này lập luận từ 2 file
> đó — thiếu 1 trong 2 là làm sai.
>
> **Mục tiêu:** đưa mockup `bao-cao-ke-hoach-lam-viec-nhan-vien.html` thành màn thật
> `/assign/report/employee-work-performance`, nằm trong phân hệ **CSKH trước bán** và **Công việc**.
>
> **Cách làm:** BE dựng `EmployeeWorkPerformanceService` gom 5 nguồn thành các cặp
> `(phiếu × người)`, đếm 2 kiểu theo cấp, trả cây + popup + in + Excel. FE copy nguyên bộ khung của
> `pages/assign/report/customer-market-development/` (cùng ngôn ngữ thiết kế, cùng component).
>
> **Stack:** PHP 7.4 · Laravel 8 · `Modules/Assign` · Nuxt 2 / Vue 2 · `V2Base*` · PHPUnit ·
> Playwright.

### Ràng buộc áp cho MỌI task của Phase 4

- **Nhánh `gop_db`** ở CẢ 2 repo. Kiểm trước khi gõ dòng code đầu tiên:
  `git -C hrm-api branch --show-current` và `git -C hrm-client branch --show-current`.
- **KHÔNG dùng connection `mysql2` / `DB_CONNECTION_SECOND`** — trỏ DB ERP cũ, id lệch.
- **Không commit, không push** (quy tắc HRM). Người thực thi tự quyết thời điểm commit.
- **Cờ quyền FE fail-closed** — khởi tạo `false`, chỉ set từ `hasAPermission()`. Cấm `= true`.
- **Element form dùng `V2Base*`**, cấm HTML thô. Tự kiểm — ⚠️ **KHÔNG để dấu cách sau tên thẻ**:
  ```bash
  grep -rn '<input\|<textarea\|<select\|<button\|<label\|class="btn \|class="form-control' \
    pages/assign/report/employee-work-performance/ | grep -v V2Base
  ```
  Lệnh cũ viết `'<button '` (có dấu cách) **né mất thẻ xuống dòng**
  (`<button\n    type="button"`) — đã lọt 1 thẻ thô ở Task 6 mà lệnh vẫn báo sạch.

  ⚠️ **NGOẠI LỆ đã được user chốt (2026-09-21)** — áp cho **3 loại nút**, đều là bản sao 1:1 từ 3 màn
  báo cáo anh em và đều **không phải element form**:
  1. nút **"Thu gọn / Mở rộng"** của dải tổng hợp và của khối tổng hợp trong popup
  2. **ô SỐ bấm được** mở popup chi tiết (`DrillCell.vue`)
  3. nút **caret** bung / thu từng dòng của bảng theo dõi
  Cả 3 dùng **`<button>` thô**, KHÔNG dùng `V2BaseButton`. Lý do: 3 màn báo
  cáo anh em (`DevelopmentSummary.vue:26` và 2 màn khác) đều làm vậy, kèm ghi chú cố ý *"không phải
  element form nên không thuộc luật V2Base*"* (`ResultSummaryBlocks.vue:40`). Đổi riêng màn này sang
  `V2BaseButton` bắt phải ghép selector `.rsum-toggle.v2-btn` để thắng style component — thêm một
  mẹo CSS chỉ để hợp lệ một luật mà team đã có ngoại lệ. **Grep sẽ khớp dòng này; đó là ngoại lệ hợp
  lệ, không phải lỗi.** Mọi `<button>` thô KHÁC vẫn là lỗi.
- **Số**: FE `toLocaleString('en-US')`, BE `number_format()` mặc định. Cấm kiểu `vi-VN` cho SỐ.
- **Nút cùng cụm** khai `class="mr-2 mb-2"`, nút cuối cụm chỉ `mb-2` (đo được phải cách 12px).
- **Chữ xám `#6b7280`** cho ghi chú — `.text-muted` trong hrm-client là màu ĐỎ.
- **FormRequest chỉ khai `rules()`**, KHÔNG khai `messages()` (câu chuẩn đã có ở lang file).
- Mỗi task đụng giao diện: **mở Playwright MCP đo bằng số lấy từ DOM** trước khi báo xong. Luôn mở
  `http://127.0.0.1:3000` (KHÔNG `localhost`).

---

### Task 1: Quyền 3 cấp + đường vào màn

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm sau dòng 1095)
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (thêm sau dòng 1235)
- Create: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/EmployeeWorkPerformanceReportController.php`
- Create: `hrm-client/pages/assign/report/employee-work-performance/index.vue`
- Modify: `hrm-client/components/subsystem-menu/presale.js` (nhóm *Báo cáo*)
- Modify: `hrm-client/components/menu-sidebar.js` (nhóm *Báo cáo* của `menuItemsAssign`, quanh dòng 131)

**Interfaces:**
- Produces: 3 tên quyền (dùng nguyên văn ở Task 3 và ở FE):
  `Xem báo cáo kế hoạch & kết quả làm việc theo công ty` ·
  `... theo phòng ban` · `... theo bộ phận`
- Produces: `EmployeeWorkPerformanceReportController::index/drill/export/printListData`

- [x] **Bước 1: Chọn id quyền còn trống**

⚠️ **Max id trong FILE seeder KHÔNG phải max id thật.** Đo ngày 2026-09-21: file có max `1589`
nhưng DB `hrm_erp` đang có permission `guard_name='api'` tới **1611** — 22 quyền (1590…1611) nằm
trong DB mà KHÔNG có trong seeder, là của nhánh khác chưa merge. Lấy id theo file là đụng nhau lúc
merge, mà git **không báo xung đột** (seeder là file phẳng).

Phải kiểm CẢ HAI nguồn rồi lấy max:

```bash
cd hrm-api
# max trong file (bỏ dòng đã comment)
grep -E "^\s*Permission::create" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php \
  | grep -oE "'id' => [0-9]+" | grep -oE "[0-9]+" | sort -n | tail -1
# max trong DB
P=$(grep -m1 "^DB_PASSWORD=" .env | cut -d= -f2-)
mysql -h127.0.0.1 -uroot -p"$P" hrm_erp -N -e "SELECT MAX(id) FROM permissions WHERE guard_name='api';"
```

Kết quả đo được: file `1589`, DB `1611` → dùng **1612 / 1613 / 1614**.

- [x] **Bước 2: Thêm 3 quyền vào seeder**

```php
// Báo cáo kế hoạch & kết quả làm việc theo nhân viên (feature bao-cao-ke-hoach-lam-viec-nhan-vien).
// 3 cấp, KHÔNG có cấp "tổng công ty" và KHÔNG có fallback "chỉ xem việc của mình" —
// user chốt 2026-09-21: không có quyền nào thì không được xem báo cáo này.
Permission::create(['id' => 1612, 'guard_name' => 'api', 'name' => 'Xem báo cáo kế hoạch & kết quả làm việc theo công ty', 'display_name' => 'Xem báo cáo kế hoạch & kết quả làm việc theo công ty', 'group' => 'Báo cáo kế hoạch & kết quả làm việc', 'type' => 4]);
Permission::create(['id' => 1613, 'guard_name' => 'api', 'name' => 'Xem báo cáo kế hoạch & kết quả làm việc theo phòng ban', 'display_name' => 'Xem báo cáo kế hoạch & kết quả làm việc theo phòng ban', 'group' => 'Báo cáo kế hoạch & kết quả làm việc', 'type' => 4]);
Permission::create(['id' => 1614, 'guard_name' => 'api', 'name' => 'Xem báo cáo kế hoạch & kết quả làm việc theo bộ phận', 'display_name' => 'Xem báo cáo kế hoạch & kết quả làm việc theo bộ phận', 'group' => 'Báo cáo kế hoạch & kết quả làm việc', 'type' => 4]);
```

- [x] **Bước 3: Kiểm id KHÔNG trùng — seeder là file phẳng, git không báo xung đột**

```bash
cd hrm-api
# id trùng trong FILE — nhớ bỏ dòng đã comment, nếu không ra id trùng GIẢ (7, 8, 16…)
grep -E "^\s*Permission::create" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php \
  | grep -oE "'id' => [0-9]+" | grep -oE "[0-9]+" | sort -n | uniq -d
# 3 id mới đã ai dùng trong DB chưa
P=$(grep -m1 "^DB_PASSWORD=" .env | cut -d= -f2-)
mysql -h127.0.0.1 -uroot -p"$P" hrm_erp -N -e \
  "SELECT id, name FROM permissions WHERE id IN (1612,1613,1614);"
```
Kỳ vọng: **cả 2 lệnh không in ra gì**. Lệnh 2 mà in ra dòng nào nghĩa là id đã bị chiếm — lấy
`MAX(id)+1` mới và báo lại, ĐỪNG đè lên quyền của người khác.

- [x] **Bước 4: Chạy seeder + xoá cache quyền**

```bash
cd hrm-api
php artisan db:seed --class="Modules\\Timesheet\\Database\\Seeders\\PermissionsTableSeeder"
php artisan cache:clear
```
⚠️ `PermissionsTableSeeder` **truncate cả bảng** rồi tạo lại — chạy xong phải kiểm
`role_has_permissions` còn dữ liệu; quyền gán cho role cần `company_id = 1`.
⚠️ `spatie` cache quyền 24h — **không `cache:clear` là API trả 403 dù đã gán quyền**.

- [x] **Bước 5: Viết controller (4 method, chưa có service — trả mảng rỗng)**

```php
<?php

namespace Modules\Assign\Http\Controllers\Api\V1;

use App\Http\Controllers\Api\BaseApiController;
use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Log;
use Illuminate\Validation\ValidationException;
use Symfony\Component\HttpKernel\Exception\HttpException;

/**
 * Báo cáo "Kế hoạch & kết quả làm việc theo nhân viên".
 * Gom 5 nguồn: meeting · task · issue · phiếu công tác · phiếu giao việc.
 */
class EmployeeWorkPerformanceReportController extends BaseApiController
{
    public function __construct()
    {
        parent::__construct();
    }

    public function index(Request $request)
    {
        try {
            return $this->responseSuccess(['tree' => [], 'total' => [], 'summary' => []]);
        } catch (ValidationException $e) {
            // RETHROW, KHÔNG nuốt: ValidationException extends Exception nên `catch (Exception)`
            // bên dưới sẽ biến 422 thành 400 và nuốt mất cấu trúc {errors:{company_id:[...]}},
            // FE hết gắn được lỗi vào ô. CLAUDE.md cấm catch chung ở form có validate.
            throw $e;
        } catch (HttpException $e) {
            // Tương tự: abort(403) của gate phân quyền cũng là Exception — nuốt là FE không
            // phân biệt được "không có quyền" với "lỗi hệ thống".
            throw $e;
        } catch (Exception $e) {
            Log::error('Error in EmployeeWorkPerformanceReportController@index: ' . $e->getMessage());

            return $this->responseErrors(Response::HTTP_BAD_REQUEST, $e->getMessage() ?: 'Lỗi khi lấy dữ liệu báo cáo');
        }
    }

    public function drill(Request $request)
    {
        try {
            return $this->responseSuccess(['data' => []]);
        } catch (Exception $e) {
            Log::error('Error in EmployeeWorkPerformanceReportController@drill: ' . $e->getMessage());

            return $this->responseErrors(Response::HTTP_BAD_REQUEST, $e->getMessage() ?: 'Lỗi khi lấy danh sách chi tiết');
        }
    }

    public function printListData(Request $request)
    {
        try {
            // Giữ `response()->json()` chứ KHÔNG dùng responseSuccess(): khoá `template` nằm
            // thẳng trong `data` là contract của reportPrintPreviewMixin.js
            return response()->json(['data' => ['template' => '']]);
        } catch (Exception $e) {
            Log::error('Error in EmployeeWorkPerformanceReportController@printListData: ' . $e->getMessage());

            return $this->responseErrors(Response::HTTP_BAD_REQUEST, $e->getMessage() ?: 'Lỗi khi dựng bản in');
        }
    }

    public function export(Request $request)
    {
        try {
            return $this->responseSuccess(['data' => []]);
        } catch (Exception $e) {
            Log::error('Error in EmployeeWorkPerformanceReportController@export: ' . $e->getMessage());

            return $this->responseErrors(Response::HTTP_BAD_REQUEST, $e->getMessage() ?: 'Lỗi khi xuất Excel báo cáo kế hoạch & kết quả làm việc theo nhân viên');
        }
    }
}
```

- [x] **Bước 6: Khai 4 route** (trong nhóm `assign/report` có sẵn, sau dòng 1235)

```php
// Báo cáo kế hoạch & kết quả làm việc theo nhân viên.
// KHÔNG gắn checkPermission ở route: gate 3 cấp + ràng buộc company_id nằm trong service
// (route chỉ chặn được có/không, không phân biệt được cấp xem).
Route::get('/employee-work-performance', [EmployeeWorkPerformanceReportController::class, 'index']);
Route::get('/employee-work-performance/drill', [EmployeeWorkPerformanceReportController::class, 'drill']);
Route::get('/employee-work-performance/export', [EmployeeWorkPerformanceReportController::class, 'export']);
// Tên `print-list-data` là contract của utils/mixins/reportPrintPreviewMixin.js — ĐỪNG ĐỔI
Route::get('/employee-work-performance/print-list-data', [EmployeeWorkPerformanceReportController::class, 'printListData']);
```
Nhớ thêm `use Modules\Assign\Http\Controllers\Api\V1\EmployeeWorkPerformanceReportController;` ở đầu file.

- [x] **Bước 7: Kiểm route đã đăng ký**

```bash
cd hrm-api && php artisan route:list --path=employee-work-performance
```
Kỳ vọng: in ra đúng **4 dòng**.

- [x] **Bước 8: Trang FE rỗng**

```vue
<template>
    <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
        <div class="container-fluid">Báo cáo kế hoạch &amp; kết quả làm việc theo nhân viên</div>
    </div>
</template>

<script>
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

export default {
    // Phân hệ dạng hub BẮT BUỘC khai layout này, thiếu là màn biến mất im lặng
    layout: 'default-sidebar',
    head() {
        return { title: 'Báo cáo kế hoạch & kết quả làm việc theo nhân viên' }
    },
    mixins: [PageTitleMixin],
    computed: {
        pageTitle() {
            return 'Báo cáo kế hoạch & kết quả làm việc theo nhân viên'
        },
        pageTitleInfo() {
            return 'Theo dõi khối lượng và kết quả làm việc của từng nhân viên, biết được ai đang nhiều việc, có khả năng thực hiện công việc hay không.'
        },
    },
}
</script>
```

- [x] **Bước 9: Khai menu ở CẢ 2 phân hệ**

Trong `components/subsystem-menu/presale.js`, nhóm *Báo cáo*, thêm vào cuối `subItems`:

```js
{
    label: 'Báo cáo kế hoạch & kết quả làm việc theo nhân viên',
    link: '/assign/report/employee-work-performance',
    isShow: [
        'Xem báo cáo kế hoạch & kết quả làm việc theo công ty',
        'Xem báo cáo kế hoạch & kết quả làm việc theo phòng ban',
        'Xem báo cáo kế hoạch & kết quả làm việc theo bộ phận',
    ],
},
```

Trong `components/menu-sidebar.js`, nhóm *Báo cáo* của `menuItemsAssign` (quanh dòng 131), thêm
**đúng object trên** kèm ghi chú:

```js
// Khai ở CẢ presale.js — subsystems.js cho phép 1 link nằm ở 2 phân hệ,
// thanh bên nhớ phân hệ user đang làm việc nên không nhảy ngữ cảnh.
```

- [x] **Bước 10: Verify bằng Playwright MCP — đo từ DOM, không nhìn ảnh**

Khởi động: API `:8000`, client `:3000`. Mở `http://127.0.0.1:3000/assign/report/employee-work-performance`.

Đo đủ 4 điểm:
1. `document.querySelector('h1, .page-title').textContent` chứa đúng tên màn.
2. `document.querySelectorAll('.sidebar a[href*="employee-work-performance"]').length === 1`
   khi đang ở phân hệ CSKH trước bán, và cũng `=== 1` khi ở phân hệ Công việc.
3. Console **0 lỗi**.
4. Gỡ 3 quyền khỏi role rồi tải lại → mục menu **biến mất** (kiểm fail-closed).
   Gán lại quyền thì phải `php artisan cache:clear` mới có hiệu lực.

- [x] **Bước 11: Cập nhật `.plans/gop-db/STATUS.md`** — feature chuyển sang *Đang làm (Phase 4)*.

---

### Task 2: Lõi đếm — `WorkAssignment` + `WorkMetrics` (TDD thuần logic)

Task này KHÔNG đụng DB: chỉ là 2 lớp nhận mảng đã chuẩn hoá và trả số. Nhờ vậy luật đếm (phần dễ
sai nhất) được chốt bằng unit test chạy trong vài giây, trước khi dính vào query.

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Report/EmployeeWorkPerformance/WorkMetrics.php`
- Test: `hrm-api/tests/Unit/EmployeeWorkMetricsTest.php`

**Interfaces:**
- Produces: `WorkMetrics::of(array $pairs, bool $byDoc): array` — trả
  `['meeting'=>int,'task'=>int,'issue'=>int,'trip'=>int,'job'=>int,'total'=>int,'done'=>int,
    'doing'=>int,'late'=>int,'cancel'=>int,'seats'=>int,'by_doc'=>bool,'completion_rate'=>float]`
- Produces: `WorkMetrics::groupByDoc(array $pairs): array` — gộp về 1 dòng/phiếu, kèm `mates`
- Consumes: mỗi phần tử `$pairs` là mảng
  `['doc_key'=>'meeting#12','type'=>'meeting','bucket'=>'done','emp_id'=>1,'role'=>'host', ...]`

- [x] **Bước 1: Viết test thất bại**

```php
<?php
namespace Tests\Unit;

use Tests\TestCase;
use Modules\Assign\Services\Report\EmployeeWorkPerformance\WorkMetrics;

class EmployeeWorkMetricsTest extends TestCase
{
    /** 1 meeting 3 người dự + 1 task 1 người */
    private function pairs(): array
    {
        return [
            ['doc_key' => 'meeting#1', 'type' => 'meeting', 'bucket' => 'done',  'emp_id' => 1, 'role' => 'host'],
            ['doc_key' => 'meeting#1', 'type' => 'meeting', 'bucket' => 'done',  'emp_id' => 2, 'role' => 'member'],
            ['doc_key' => 'meeting#1', 'type' => 'meeting', 'bucket' => 'done',  'emp_id' => 3, 'role' => 'member'],
            ['doc_key' => 'task#1',    'type' => 'task',    'bucket' => 'doing', 'emp_id' => 1, 'role' => 'host'],
        ];
    }

    public function test_cap_nhan_vien_dem_moi_luot_tham_gia()
    {
        $m = WorkMetrics::of($this->pairs(), false);

        $this->assertSame(4, $m['total']);      // 3 lượt meeting + 1 task
        $this->assertSame(3, $m['meeting']);
        $this->assertSame(4, $m['seats']);
        $this->assertFalse($m['by_doc']);
    }

    public function test_cap_don_vi_dem_theo_phieu()
    {
        $m = WorkMetrics::of($this->pairs(), true);

        $this->assertSame(2, $m['total']);      // 1 meeting + 1 task
        $this->assertSame(1, $m['meeting']);
        $this->assertSame(4, $m['seats']);      // vẫn giữ số lượt để tooltip đối chiếu
        $this->assertTrue($m['by_doc']);
    }

    public function test_bon_nhom_trang_thai_chia_het_tong()
    {
        foreach ([true, false] as $byDoc) {
            $m = WorkMetrics::of($this->pairs(), $byDoc);
            $this->assertSame($m['total'], $m['done'] + $m['doing'] + $m['late'] + $m['cancel']);
        }
    }

    public function test_id_trung_giua_hai_bang_khong_bi_gop_nham()
    {
        // meetings.id = 1 và tasks.id = 1 là HAI phiếu khác nhau -> doc_key phải kèm loại
        $m = WorkMetrics::of($this->pairs(), true);
        $this->assertSame(2, $m['total']);
    }

    public function test_group_by_doc_lay_nguoi_chu_tri_lam_dai_dien()
    {
        $rows = WorkMetrics::groupByDoc($this->pairs());

        $this->assertCount(2, $rows);
        $meeting = $rows[0];
        $this->assertSame(1, $meeting['emp_id']);       // host, dù không phải phần tử đầu sau khi lọc
        $this->assertSame('host', $meeting['role']);
        $this->assertCount(3, $meeting['mates']);
    }

    public function test_group_by_doc_khong_co_host_thi_lay_nguoi_dau_tien()
    {
        $rows = WorkMetrics::groupByDoc([
            ['doc_key' => 'meeting#9', 'type' => 'meeting', 'bucket' => 'doing', 'emp_id' => 7, 'role' => 'member'],
            ['doc_key' => 'meeting#9', 'type' => 'meeting', 'bucket' => 'doing', 'emp_id' => 8, 'role' => 'member'],
        ]);

        $this->assertSame(7, $rows[0]['emp_id']);
        $this->assertCount(2, $rows[0]['mates']);
    }

    public function test_ty_le_hoan_thanh_mau_so_bang_khong_tra_ve_khong()
    {
        $m = WorkMetrics::of([], true);
        $this->assertSame(0.0, $m['completion_rate']);
        $this->assertSame(0, $m['total']);
    }
}
```

- [x] **Bước 2: Chạy test để chắc nó ĐỎ**

```bash
cd hrm-api && vendor/bin/phpunit --filter EmployeeWorkMetricsTest
```
Kỳ vọng: FAIL — `Class "…\WorkMetrics" not found`.

- [x] **Bước 3: Viết `WorkMetrics`**

```php
<?php

namespace Modules\Assign\Services\Report\EmployeeWorkPerformance;

/**
 * Bộ chỉ tiêu của 1 tập cặp (phiếu × người) — 2 CÁCH ĐẾM, chốt 2026-09-21:
 *
 *   byDoc = false -> đếm theo CẶP: dùng cho CẤP NHÂN VIÊN, cứ có tham gia là +1.
 *   byDoc = true  -> đếm theo PHIẾU (distinct `doc_key`): dùng cho BỘ PHẬN / PHÒNG BAN /
 *                    dòng TỔNG / dải tổng hợp. 1 phiếu 5 người vẫn là 1 đầu việc của đơn vị.
 *
 * ⚠️ HỆ QUẢ: dòng cha KHÔNG bằng tổng dòng con (nhỏ hơn — phần chênh là việc làm chung), và
 * cộng các phòng ban LỚN HƠN dòng TỔNG khi 1 phiếu có người ở 2 phòng. `seats` giữ số lượt
 * tham gia để tooltip đối chiếu được 2 con số.
 *
 * ⚠️ `doc_key` BẮT BUỘC kèm loại (`meeting#12`) — 5 bảng nguồn có id trùng nhau.
 */
class WorkMetrics
{
    const TYPES   = ['meeting', 'task', 'issue', 'trip', 'job'];
    const BUCKETS = ['done', 'doing', 'late', 'cancel'];

    public static function of(array $pairs, bool $byDoc): array
    {
        $m = ['total' => 0, 'seats' => count($pairs), 'by_doc' => $byDoc];

        foreach (array_merge(self::TYPES, self::BUCKETS) as $k) {
            $m[$k] = 0;
        }

        $seen = [];

        foreach ($pairs as $p) {
            if ($byDoc) {
                if (isset($seen[$p['doc_key']])) {
                    continue;
                }
                $seen[$p['doc_key']] = true;
            }

            $m['total']++;
            $m[$p['type']]++;
            $m[$p['bucket']]++;
        }

        $m['completion_rate'] = $m['total'] ? round($m['done'] * 100 / $m['total'], 1) : 0.0;

        return $m;
    }

    /**
     * Gộp các cặp về ĐÚNG 1 DÒNG / PHIẾU cho popup mở từ cấp cha — để số dòng popup khớp
     * con số vừa bấm trên bảng.
     *
     * Dòng đại diện ưu tiên NGƯỜI CHỦ TRÌ nếu người đó nằm trong phạm vi đang xem;
     * `mates` giữ nguyên mọi người tham gia để FE hiện "+N" và tooltip.
     */
    public static function groupByDoc(array $pairs): array
    {
        $rows = [];

        foreach ($pairs as $p) {
            $key = $p['doc_key'];

            if (!isset($rows[$key])) {
                $rows[$key] = $p + ['mates' => []];
                $rows[$key]['mates'][] = $p;
                continue;
            }

            $rows[$key]['mates'][] = $p;

            if ($p['role'] === 'host' && $rows[$key]['role'] !== 'host') {
                foreach (['emp_id', 'emp_name', 'role', 'department_id', 'department_name', 'part_id', 'part_name'] as $f) {
                    if (array_key_exists($f, $p)) {
                        $rows[$key][$f] = $p[$f];
                    }
                }
            }
        }

        return array_values($rows);
    }
}
```

- [x] **Bước 4: Chạy lại test — phải XANH**

```bash
cd hrm-api && vendor/bin/phpunit --filter EmployeeWorkMetricsTest
```
Kỳ vọng: `OK (7 tests)`.

---

### Task 3: Gom 5 nguồn thành cặp `(phiếu × người)` + gate quyền

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Report/EmployeeWorkPerformance/WorkAssignmentCollector.php`
- Create: `hrm-api/Modules/Assign/Services/Report/EmployeeWorkPerformanceService.php`
- Test: `hrm-api/tests/Unit/EmployeeWorkBucketTest.php`

**Interfaces:**
- Consumes: `WorkMetrics` (Task 2), `WorkItemPeriod`, `WorkItemStatusGroup`, `MyTodoOwnershipScope`
- Produces: `WorkAssignmentCollector::bucketOf(string $type, $status, Carbon $end, Carbon $today): string`
- Produces: `WorkAssignmentCollector::collect(Request $r, array $empIds): array` — mảng cặp
- Produces: `EmployeeWorkPerformanceService::permissionLevel(): string` → `company|department|part|none`
- Produces: `EmployeeWorkPerformanceService::assertCanView(Request $r): void` — ném 403 / 422

- [x] **Bước 1: Test thất bại cho `bucketOf` (luật 4 nhóm)**

```php
<?php
namespace Tests\Unit;

use Carbon\Carbon;
use Tests\TestCase;
use Modules\Assign\Services\Report\EmployeeWorkPerformance\WorkAssignmentCollector;

class EmployeeWorkBucketTest extends TestCase
{
    private $today;

    protected function setUp(): void
    {
        parent::setUp();
        $this->today = Carbon::parse('2026-09-26');
    }

    private function bucket($type, $status, $end)
    {
        return WorkAssignmentCollector::bucketOf($type, $status, Carbon::parse($end), $this->today);
    }

    public function test_huy_thang_hoan_thanh_va_qua_han()
    {
        // Meeting HUY = 4 — dù hạn đã qua vẫn KHÔNG tính quá hạn (đã dừng thì hết hạn để trễ)
        $this->assertSame('cancel', $this->bucket('meeting', 4, '2026-09-01'));
    }

    public function test_hoan_thanh_thang_qua_han()
    {
        // Meeting HOAN_THANH = 3, hạn đã qua -> vẫn là done
        $this->assertSame('done', $this->bucket('meeting', 3, '2026-09-01'));
    }

    public function test_chua_xong_va_qua_han_thi_late()
    {
        $this->assertSame('late', $this->bucket('meeting', 2, '2026-09-01'));
    }

    public function test_chua_xong_con_trong_han_thi_doing()
    {
        $this->assertSame('doing', $this->bucket('meeting', 2, '2026-09-30'));
    }

    public function test_issue_status_chuoi_khong_roi_nham_nhom()
    {
        // PHP 7.4: 'resolved' == 0 cho TRUE nếu so lỏng -> phải so nghiêm ngặt
        $this->assertSame('done', $this->bucket('issue', 'resolved', '2026-09-01'));
        $this->assertSame('cancel', $this->bucket('issue', 'rejected', '2026-09-01'));
    }

    public function test_phieu_giao_viec_da_duyet_ket_qua_la_done()
    {
        $this->assertSame('done', $this->bucket('assign_job', 6, '2026-09-01'));
    }
}
```

- [x] **Bước 2: Chạy — phải ĐỎ**

```bash
cd hrm-api && vendor/bin/phpunit --filter EmployeeWorkBucketTest
```

- [x] **Bước 3: Viết `bucketOf` dựng TRÊN `WorkItemStatusGroup`**

```php
/**
 * 4 nhóm theo dõi của báo cáo, dựng TRÊN WorkItemStatusGroup (nguồn duy nhất của 5 bộ
 * trạng thái — CLAUDE.md cấm map lại).
 *
 *   stopped        -> cancel   (Dừng / Huỷ / Từ chối)
 *   done           -> done
 *   end < TODAY    -> late     (xét SAU cancel và done: đã dừng hoặc đã xong thì hết hạn để trễ)
 *   còn lại        -> doing
 *
 * ⚠️ Task "Tạm dừng" nằm ở nhóm `stopped` của helper nên rơi vào `cancel`, khác mockup
 * (mockup xếp vào "đang thực hiện"). Theo helper — xem design-phase4.md §4b; nhãn nhóm thứ 4
 * trên màn vì vậy là "Dừng / Huỷ / Từ chối".
 */
public static function bucketOf(string $type, $status, Carbon $end, Carbon $today): string
{
    $group = WorkItemStatusGroup::of($type, $status);

    if ($group === WorkItemStatusGroup::STOPPED) {
        return 'cancel';
    }

    if ($group === WorkItemStatusGroup::DONE) {
        return 'done';
    }

    return $end->lt($today) ? 'late' : 'doing';
}
```
`$type` dùng ĐÚNG khoá của helper: `meeting` · `task` · `issue` · `assign_business` · `assign_job`
(khoá hiển thị của báo cáo là `trip` / `job` — đổi ở chỗ dựng cặp, không đổi khi gọi helper).

- [x] **Bước 4: Chạy lại — phải XANH** (`OK (6 tests)`)

- [x] **Bước 5: Viết `collect()` — 5 truy vấn, mỗi loại 1 câu**

Quy tắc bắt buộc, lấy từ `design-phase4.md` §3:

```php
/**
 * 5 truy vấn, KHÔNG hơn. Mỗi bản ghi phẳng hoá thành các cặp (phiếu × người).
 *
 * ⚠️ 4 cái bẫy đã đo trên DB thật, đừng suy từ mockup:
 *   1. assign_job_employees dùng `employee_info_id` (employee_infos.id), KHÔNG phải employees.id
 *      -> join employees.employee_info_id mới ra khoá của cây tổ chức. Dùng nhầm là gán việc
 *         cho NHÂN VIÊN KHÁC mà không có lỗi nào báo.
 *   2. meeting_employees chứa cả người phía KHÁCH HÀNG (type = 2, employee_id NULL)
 *      -> bắt buộc lọc type = 1.
 *   3. assign_business KHÔNG có company_id/department_id/part_id -> phòng ban suy từ hồ sơ
 *      nhân viên trong đoàn.
 *   4. tasks không có start_time -> giờ bắt đầu luôn 00:00, KHÔNG bịa.
 *
 * Khoảng thời gian lấy từ WorkItemPeriod::of(); trả null (task/issue chưa đặt hạn) thì rơi về
 * [created_at, created_at] — báo cáo khối lượng KHÔNG được để rơi mất việc như màn lịch.
 */
```

Mỗi cặp là mảng:

```php
[
    'doc_key'   => 'meeting#' . $m->id,     // BẮT BUỘC kèm loại: 5 bảng có id trùng
    'doc_id'    => $m->id,
    'type'      => 'meeting',               // meeting|task|issue|trip|job (khoá HIỂN THỊ)
    'code'      => $m->code,
    'name'      => $m->name,
    'emp_id'    => $row->employee_id,
    'emp_name'  => $info->fullname,
    'role'      => 'host'|'member',
    'department_id' => $info->department_id, 'department_name' => …,
    'part_id'       => $info->part_id,       'part_name'       => …,
    'start'     => $period['start'],  'end' => $period['end'],
    'bucket'    => WorkAssignmentCollector::bucketOf('meeting', $m->status, $period['end'], $today),
]
```

Lọc kỳ: **giao nhau** — `start <= $to && end >= $from` (KHÔNG lọc theo ngày tạo, KHÔNG chỉ theo
ngày bắt đầu).

Viết đủ 5 nhánh theo đúng khuôn dưới đây. Nhánh **phiếu giao việc** là nhánh dễ sai nhất (khoá
người là `employee_info_id`), viết nguyên văn:

```php
/** Phiếu giao việc — người thực hiện nằm ở assign_job_employees.employee_info_id */
private function fromAssignJobs(Carbon $from, Carbon $to, array $empIds, Carbon $today): array
{
    // employees.id <- employee_infos.id : bảng pivot lưu employee_info_id nên phải bắc cầu,
    // KHÔNG so thẳng với employees.id (sẽ ra NHÂN VIÊN KHÁC, không lỗi nào báo).
    $infoIdOf = Employee::query()
        ->whereIn('id', $empIds)
        ->pluck('id', 'employee_info_id');          // [employee_info_id => employees.id]

    $jobs = AssignJob::query()
        ->with(['employees'])
        ->where('time_start_request', '<=', $to)
        ->where(function ($q) use ($from) {
            $q->where('deadline', '>=', $from)->orWhereNull('deadline');
        })
        ->whereHas('employees', function ($q) use ($infoIdOf) {
            $q->whereIn('employee_info_id', $infoIdOf->keys());
        })
        ->get();

    $pairs = [];

    foreach ($jobs as $job) {
        $period = WorkItemPeriod::of($job, 'assign_job');
        // Báo cáo khối lượng KHÔNG được để rơi mất việc như màn lịch -> rơi về ngày tạo
        $period = $period ?: ['start' => $job->created_at, 'end' => $job->created_at];
        $bucket = self::bucketOf('assign_job', $job->status, $period['end'], $today);

        foreach ($job->employees as $row) {
            $empId = $infoIdOf[$row->employee_info_id] ?? null;
            if (!$empId) {
                continue;                            // ngoài phạm vi quyền
            }

            $pairs[] = $this->makePair('job', 'assign_job', $job, $empId,
                // Người LẬP phiếu là chủ trì (design.md §"Định nghĩa 5 nguồn")
                (int) $job->created_by === (int) $empId ? 'host' : 'member',
                $period, $bucket);
        }
    }

    return $pairs;
}
```

4 nhánh còn lại cùng khuôn, khác đúng 3 chỗ — **bảng người tham gia · khoá người · ai là chủ trì**:

| Loại | Lấy người từ | Chủ trì là |
|---|---|---|
| `meeting` | `meeting_employees` **lọc `type = 1`** (type 2 là người phía khách hàng, `employee_id` NULL) | `meetings.host_employee_id` |
| `task` | chính `tasks.assignee_id` (1 người) | luôn `host` |
| `issue` | chính `issues.assignee_id` (1 người) | luôn `host` |
| `trip` | `assign_business_employees.employee_id` | `is_leader = 1` |

- [x] **Bước 6: Viết gate quyền trong `EmployeeWorkPerformanceService`**

```php
/** Cấp quyền cao nhất user đang có. KHÔNG có cấp 'all_company', KHÔNG fallback 'self'. */
public function permissionLevel(): string
{
    if ($this->levelCache !== null) {
        return $this->levelCache;
    }
    if (isCurrentEmployeeHasPermission('Xem báo cáo kế hoạch & kết quả làm việc theo công ty')) {
        return $this->levelCache = 'company';
    }
    if (isCurrentEmployeeHasPermission('Xem báo cáo kế hoạch & kết quả làm việc theo phòng ban')) {
        return $this->levelCache = 'department';
    }
    if (isCurrentEmployeeHasPermission('Xem báo cáo kế hoạch & kết quả làm việc theo bộ phận')) {
        return $this->levelCache = 'part';
    }

    return $this->levelCache = 'none';
}

/**
 * Chặn ngay đầu mọi endpoint. 2 điều kiện, KHÔNG được bỏ điều kiện nào:
 *   · phải có 1 trong 3 quyền                      -> 403
 *   · company_id bắt buộc và phải đúng công ty user đang làm việc -> 422 / 403
 * `spatie` lưu quyền theo từng công ty (role_has_permissions.company_id) nên quyền ở công ty A
 * KHÔNG nói gì về công ty B.
 */
public function assertCanView(Request $request): void
{
    if ($this->permissionLevel() === 'none') {
        abort(403, 'Bạn không có quyền xem báo cáo này.');
    }
    if (!$request->filled('company_id')) {
        abort(422, 'Bắt buộc phải nhập');
    }
    if ((int) $request->company_id !== (int) auth()->user()->current_company_role) {
        abort(403, 'Bạn không có quyền xem báo cáo của công ty này.');
    }
}
```

- [x] **Bước 7: Danh sách nhân viên trong phạm vi quyền**

```php
/**
 * employees.id được phép xuất hiện trên báo cáo. Dùng cho `whereIn` của cả 5 truy vấn -> gate
 * quyền chỉ viết MỘT chỗ, không rải điều kiện vào từng loại (assign_business không có cột
 * department_id để mà rải).
 */
private function allowedEmployeeIds(Request $request): array
```
- `company` → mọi nhân viên `employee_infos.company_id = company_id`
- `department` → `whereIn('department_id', listManageDepartmentIds())`
- `part` → `whereIn('part_id', listManagePartIds())`
- rồi thu hẹp tiếp theo ô lọc `department_id` / `part_id` / `employee_id` user chọn.

- [x] **Bước 8: Kiểm bằng `tinker` trên DB thật**

```bash
cd hrm-api && php artisan tinker --execute="
\$s = new Modules\Assign\Services\Report\EmployeeWorkPerformance\WorkAssignmentCollector();
\$r = new Illuminate\Http\Request(['company_id' => 1, 'period' => 'year']);
\$p = \$s->collect(\$r, []);
echo count(\$p), ' cặp / ', count(array_unique(array_column(\$p, 'doc_key'))), ' phiếu', PHP_EOL;
"
```
Kỳ vọng: số cặp **>=** số phiếu, và số phiếu **<=** tổng 5 bảng (856 + 19 + 0 + 163 + 353 = 1.391
trên DB local hiện tại). Ra 0 cặp thì kiểm lại 4 cái bẫy ở Bước 5 trước khi đi tiếp.

---

### Task 4: `getData()` — dải tổng hợp + dòng TỔNG + cây 3 cấp

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/EmployeeWorkPerformanceService.php`
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/EmployeeWorkPerformanceReportController.php`
- Test: `hrm-api/e2e` → `e2e/tests/assign/employee-work-performance.api.spec.ts` (dựng ở Task 10)

**Interfaces:**
- Consumes: `WorkMetrics::of()` (Task 2), `WorkAssignmentCollector::collect()` (Task 3)
- Produces: `EmployeeWorkPerformanceService::getData(Request $r): array` — hình dạng ở
  `design-phase4.md` §6
- Produces: `resolvePeriodRange(Request $r): array` — **copy nguyên**
  `CustomerMarketDevelopmentService.php:96-128` (8 mốc kỳ + nhánh `custom`), Task 5 dùng lại
- Produces: `applyViewFilters(array $pairs, Request $r): array` — lọc `types` · `bucket` ·
  `host_only` trên từng cặp; Task 5 dùng lại

- [x] **Bước 0: `applyViewFilters()`**

```php
/**
 * 3 ô lọc chỉ đổi GÓC NHÌN, không đổi phạm vi quyền -> lọc trên cặp đã gom, không nhét vào
 * 5 truy vấn (nhét vào query là phải sửa 5 chỗ mỗi lần thêm ô lọc).
 *
 * `busy_only` KHÔNG nằm ở đây — nó ẩn DÒNG NHÂN VIÊN có Tổng = 0 chứ không bỏ cặp nào,
 * xử lý ở buildTree().
 */
private function applyViewFilters(array $pairs, Request $request): array
{
    $types  = $request->filled('types') ? explode(',', $request->types) : WorkMetrics::TYPES;
    $bucket = $request->filled('bucket') ? $request->bucket : null;
    $hostOnly = $request->boolean('host_only');

    return array_values(array_filter($pairs, function ($p) use ($types, $bucket, $hostOnly) {
        if (!in_array($p['type'], $types, true)) {
            return false;
        }
        if ($bucket && $p['bucket'] !== $bucket) {
            return false;
        }

        return !$hostOnly || $p['role'] === 'host';
    }));
}
```

- [x] **Bước 1: `buildTree()` — copy khuôn đã bỏ cấp rỗng**

Copy `CustomerMarketDevelopmentService.php:666-728` rồi sửa 3 chỗ:
1. `dims` cố định `['dept', 'part', 'emp']` (màn này không có bộ tiêu chí đổi chiều).
2. `metrics` gọi `WorkMetrics::of($rows, $head !== 'emp')` — **đây là điểm khác cốt lõi**.
3. Thứ tự dòng theo **thứ tự danh mục tổ chức**, không theo số lượng giảm dần: cây dựng từ danh
   mục nên bỏ tick *Chỉ hiện NV có việc* vẫn hiện được người 0 đầu việc.

```php
'metrics' => WorkMetrics::of($group['rows'], $head !== 'emp'),
```

**Cấp `emp` dựng từ DANH MỤC, không từ dữ liệu** — nếu không thì người 0 đầu việc không bao giờ
có dòng để mà hiện:

```php
/**
 * Cấp nhân viên đi từ `allowedEmployeeIds()` chứ KHÔNG từ các cặp đang có, để:
 *   · thứ tự dòng cố định theo danh mục tổ chức
 *   · bỏ tick "Chỉ hiện NV có việc" là hiện được cả người có 0 đầu việc
 * `busy_only` (mặc định BẬT) lọc bỏ node nhân viên `metrics.total === 0`, rồi bỏ tiếp node cha
 * không còn con nào.
 */
```

- [x] **Bước 2: `getData()`**

```php
public function getData(Request $request): array
{
    $this->assertCanView($request);

    [$from, $to] = $this->resolvePeriodRange($request);
    $empIds = $this->allowedEmployeeIds($request);
    $pairs  = (new WorkAssignmentCollector())->collect($request, $empIds);
    $pairs  = $this->applyViewFilters($pairs, $request);   // types · bucket · host_only

    return [
        'period'           => ['from' => $from->toDateString(), 'to' => $to->toDateString()],
        'permission_level' => $this->permissionLevel(),
        // Dải tổng hợp là số CẤP CÔNG TY -> luôn đếm theo phiếu
        'summary'          => WorkMetrics::of($pairs, true) + [
            'employees_with_work' => count(array_unique(array_column($pairs, 'emp_id'))),
            'employees_in_scope'  => count($empIds),
        ],
        'total'            => WorkMetrics::of($pairs, true),
        'tree'             => $this->buildTree($pairs, ['dept', 'part', 'emp'], 'n'),
    ];
}
```

- [x] **Bước 3: Nối controller vào service** — `index()` gọi `$service->getData($request)`,
      giữ nguyên khối `try/catch` + `Log::error` đã viết ở Task 1.

- [x] **Bước 4: Gọi thử API và kiểm 4 bất biến bằng `jq`**

```bash
TOKEN=$(jq -r .token ../e2e/.auth/api.json)
curl -s -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' \
  'http://127.0.0.1:8000/api/v1/assign/report/employee-work-performance?company_id=1&period=year' \
  > /tmp/ewp.json

# (a) 4 nhóm trạng thái chia hết tổng
jq '.data.total | (.done + .doing + .late + .cancel) == .total' /tmp/ewp.json

# (b) 5 cột loại cộng lại = tổng
jq '.data.total | (.meeting + .task + .issue + .trip + .job) == .total' /tmp/ewp.json

# (c) dòng cha <= tổng dòng con (KHÔNG phải ==, xem design-phase4.md §5)
jq '[.data.tree[] | select(.children | length > 0)
     | (.metrics.total <= ([.children[].metrics.total] | add))] | all' /tmp/ewp.json

# (d) cộng các phòng >= dòng TỔNG
jq '([.data.tree[].metrics.total] | add) >= .data.total.total' /tmp/ewp.json
```
Cả 4 lệnh phải in `true`.

- [x] **Bước 5: Kiểm 2 nhánh chặn**

```bash
# thiếu company_id -> 422
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" \
  'http://127.0.0.1:8000/api/v1/assign/report/employee-work-performance?period=year'
# công ty khác -> 403
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" \
  'http://127.0.0.1:8000/api/v1/assign/report/employee-work-performance?company_id=99999&period=year'
```
Kỳ vọng: `422` rồi `403`.

---

### Task 5: `drill` — popup chi tiết gộp theo phiếu

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/EmployeeWorkPerformanceService.php`

**Interfaces:**
- Consumes: `WorkMetrics::groupByDoc()` (Task 2)
- Produces: `EmployeeWorkPerformanceService::getDrillRows(Request $r): array`
- Produces: `EmployeeWorkPerformanceService::isByDoc(string $key): bool`

- [x] **Bước 1: Viết `getDrillRows()` — LỌC TRƯỚC, GỘP SAU**

```php
/**
 * Danh sách chi tiết của 1 node + 1 chỉ tiêu (popup drill-down).
 *
 * `key` = khoá node do getData() trả về (`n/dept:12/emp:345`), hoặc `ALL` cho dòng TỔNG.
 *
 * ⚠️ LỌC TRƯỚC trên từng cặp (phiếu × người) rồi MỚI GỘP theo phiếu. Làm ngược lại thì lọc
 * theo 1 nhân viên vẫn kéo cả những người khác trong phiếu ra (đo trên mockup: 107 dòng phải
 * còn 26, và 0 dòng còn đuôi "+N").
 *
 * Node cấp NHÂN VIÊN (`dim = emp`) KHÔNG gộp — giữ 1 dòng / đầu việc như mockup.
 */
public function getDrillRows(Request $request): array
{
    $this->assertCanView($request);

    $key    = $request->filled('key') ? $request->key : 'ALL';
    $metric = $request->filled('metric') ? $request->metric : 'total';

    $pairs = $this->applyViewFilters(
        (new WorkAssignmentCollector())->collect($request, $this->allowedEmployeeIds($request)),
        $request
    );

    $pairs = $this->filterByNodeKey($pairs, $key);      // từng cặp `<dim>:<id>` trên khoá
    $pairs = $this->filterByMetric($pairs, $metric);    // 1 trong 5 loại, hoặc 1 trong 4 nhóm

    return $this->isByDoc($key) ? WorkMetrics::groupByDoc($pairs) : $pairs;
}

/** Cấp cha (kể cả `ALL`) thì gộp; chỉ cấp nhân viên mới giữ 1 dòng / người. */
public function isByDoc(string $key): bool
{
    return strpos($key, 'emp:') === false;
}
```

- [x] **Bước 2: 2 hàm lọc phụ**

```php
/**
 * Lọc lại từ tập gốc theo từng cặp `<dim>:<id>` trên khoá node, thay vì phải giữ cây trong
 * session. `ALL` = dòng TỔNG, không lọc chiều nào.
 */
private function filterByNodeKey(array $pairs, string $key): array
{
    if ($key === 'ALL') {
        return $pairs;
    }

    $field = ['dept' => 'department_id', 'part' => 'part_id', 'emp' => 'emp_id'];

    foreach (explode('/', $key) as $seg) {
        if (strpos($seg, ':') === false) {
            continue;                                  // bỏ tiền tố 'n'
        }
        [$dim, $id] = explode(':', $seg, 2);
        if (!isset($field[$dim])) {
            continue;
        }
        $col = $field[$dim];
        $pairs = array_values(array_filter($pairs, function ($p) use ($col, $id) {
            // So sánh NGHIÊM NGẶT sau khi quy về string: PHP 7.4 cho 'abc' == 0 là true
            return (string) ($p[$col] ?? '') === (string) $id;
        }));
    }

    return $pairs;
}

/** `total` = tất cả; còn lại là 1 trong 5 LOẠI hoặc 1 trong 4 NHÓM trạng thái. */
private function filterByMetric(array $pairs, string $metric): array
{
    if ($metric === 'total') {
        return $pairs;
    }

    $col = in_array($metric, WorkMetrics::TYPES, true) ? 'type'
        : (in_array($metric, WorkMetrics::BUCKETS, true) ? 'bucket' : null);

    if (!$col) {
        return $pairs;
    }

    return array_values(array_filter($pairs, function ($p) use ($col, $metric) {
        return $p[$col] === $metric;
    }));
}
```

- [x] **Bước 3: Nối controller** — `drill()` trả `['data' => $service->getDrillRows($request)]`.

- [x] **Bước 4: Kiểm số dòng popup KHỚP con số trên cây** (bất biến quan trọng nhất của popup)

```bash
TOKEN=$(jq -r .token ../e2e/.auth/api.json)
BASE='http://127.0.0.1:8000/api/v1/assign/report/employee-work-performance'
Q='company_id=1&period=year'

# lấy 1 node cấp phòng ban + số Tổng của nó
KEY=$(jq -r '.data.tree[0].key' /tmp/ewp.json)
N=$(jq -r '.data.tree[0].metrics.total' /tmp/ewp.json)
M=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/drill?$Q&key=$KEY&metric=total" | jq '.data | length')
echo "cây=$N  popup=$M"
```
Kỳ vọng: **2 số bằng nhau**. Lặp lại với 1 node `emp:` — cũng phải bằng nhau.

- [x] **Bước 5: Kiểm luật gộp**

```bash
# popup cấp cha: số dòng = số mã phiếu KHÁC NHAU
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/drill?$Q&key=$KEY&metric=total" \
  | jq '(.data | length) == ([.data[].doc_key] | unique | length)'
# và có ít nhất 1 dòng nhiều người
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/drill?$Q&key=$KEY&metric=total" \
  | jq '[.data[] | select((.mates | length) > 1)] | length > 0'
```
Cả 2 phải `true`.

- [x] **Bước 6: Kiểm lọc-trước-gộp-sau**

Gọi lại chính popup đó kèm `&employee_id=<1 nhân viên trong phòng>`: số dòng phải giảm, và
`[.data[] | select((.mates|length) > 1)] | length` phải bằng **0**.

---

### Task 6: FE — khung màn, bộ lọc, dải tổng hợp

**Files:**
- Modify: `hrm-client/pages/assign/report/employee-work-performance/index.vue`
- Create: `hrm-client/pages/assign/report/employee-work-performance/components/WorkSummary.vue`
- Create: `hrm-client/pages/assign/report/employee-work-performance/components/InfoTip.vue` (copy nguyên từ `customer-market-development/components/InfoTip.vue`)

**Interfaces:**
- Consumes: `GET assign/report/employee-work-performance` (Task 4)
- Produces: `this.filters` (object dùng chung cho cả `filterFields` lẫn prop `form` của
  `V2BaseCompanyDepartmentFilter`), `this.summary`, `this.total`, `this.tree`

- [x] **Bước 1: Dựng `initialFilters` — `company_id` có giá trị NGAY, không để null**

```js
const initialFilters = {
    period: 'month',
    // Ô lọc gộp: panel ghi vào start_date/end_date, `date_range` là khoá của chính ô
    // — phải khai sẵn, Vue 2 không reactive với property chưa khai.
    date_range: null,
    start_date: null,
    end_date: null,
    // BẮT BUỘC có 1 công ty (user chốt 2026-09-21) -> gán trong created(), không để null
    company_id: null,
    department_id: null,
    part_id: null,
    employee_id: null,
    types: ['meeting', 'task', 'issue', 'trip', 'job'],
    bucket: null,
    host_only: false,
    busy_only: true,
}
```

- [x] **Bước 2: Cờ quyền fail-closed + chốt công ty trong `created()`**

```js
async created() {
    // Fail-closed: KHÔNG bao giờ || true
    this.permissions = {
        is_all_company: false,          // màn này KHÔNG có cấp tổng công ty
        is_company: this.hasAPermission('Xem báo cáo kế hoạch & kết quả làm việc theo công ty'),
        is_department: this.hasAPermission('Xem báo cáo kế hoạch & kết quả làm việc theo phòng ban'),
        is_part: this.hasAPermission('Xem báo cáo kế hoạch & kết quả làm việc theo bộ phận'),
    }

    this.canView = this.permissions.is_company || this.permissions.is_department || this.permissions.is_part
    if (!this.canView) return          // template hiện khối "Bạn không có quyền xem báo cáo này"

    // Công ty đang làm việc — báo cáo LUÔN phải có 1 công ty
    this.filters.company_id = this.$store.state.current_employee_info?.company_role
        ?? this.$store.state.current_employee?.company_id
        ?? null

    this.handleSearch()
}
```

- [x] **Bước 3: Khai ô Công ty RIÊNG, không giao cho `V2BaseCompanyDepartmentFilter`**

```js
{
    key: 'company_id',
    label: 'Công ty',
    type: 'select',
    options: this.companyOptions,
    // Báo cáo luôn phải có 1 công ty -> không cho xoá về rỗng
    allowClear: false,
},
```
⚠️ Lý do (đã đo): `components/V2BaseCompanyDepartmentFilter.vue:8` chỉ render ô Công ty khi
`permissions.is_all_company === true`, mà màn này không có cấp đó → giao cho component là ô
**không bao giờ hiện**. Xem `design-phase4.md` §2.

- [x] **Bước 4: Phòng ban / Bộ phận / Nhân viên vẫn dùng component chung**

```vue
<template #field-org>
    <V2BaseCompanyDepartmentFilter
        :form="filters"
        :permissions="permissions"
        :floating="true"
        wrapper-class="d-contents"
    />
</template>
```
⚠️ Truyền **chính** `this.filters` (component ghi thẳng vào prop `form`, không emit). Nhờ vậy
watcher `form.company_id` tự xoá `department_id / part_id / employee_id` khi đổi công ty.
**KHÔNG bọc thêm `col-*`** quanh component — nó tự khai `.d-contents`, bọc thêm là vỡ lưới và bộ
lọc chết im lặng.

- [x] **Bước 5: Ô "Loại công việc" chọn nhiều**

`type: 'select'`, `multiple: true`, mặc định tick đủ 5, mỗi dòng có chấm màu theo loại. Bỏ tick loại
nào thì **ẩn luôn cột đó** ở Task 7 và trừ khỏi `Tổng`. Chưa chọn loại nào → viền ô đỏ + bảng báo
*"Chưa bật loại công việc nào…"*.

- [x] **Bước 6: `WorkSummary.vue` — 2 khối, ô con xếp ngang**

Copy `DevelopmentSummary.vue` rồi đổi nội dung theo `design.md` mục "Dải tổng hợp":

| Khối | Ô con |
|---|---|
| Khối lượng trong kỳ | Tổng đầu việc · Nhân viên có việc |
| Trạng thái xử lý | Đã hoàn thành · Đang thực hiện · Quá hạn · **Dừng / Huỷ / Từ chối** |

- Meta khối 1 ghi **"Đếm theo phiếu"** (hoặc *"Chỉ việc chủ trì"* khi bật cờ) — dải tổng hợp là số
  cấp công ty.
- Tooltip ô *Tổng đầu việc* ghi thêm `summary.seats` lượt tham gia.
- Không có ô "Bình quân/người" (đã chốt bỏ).

- [x] **Bước 7: Verify Playwright MCP — đo từ DOM**

Mở `http://127.0.0.1:3000/assign/report/employee-work-performance`, đo:
1. `done + doing + late + cancel === total` đọc từ 4 ô của khối 2 và ô *Tổng đầu việc*.
2. Ô **Công ty** có mặt, `allowClear` tắt (không có nút `×`), giá trị ≠ rỗng ngay khi vào màn.
3. Đổi Công ty → 3 ô Phòng ban / Bộ phận / Nhân viên **tự trắng**.
4. Thanh lọc **không vỡ lưới**: đếm số phần tử con trực tiếp của hàng lọc trước/sau khi gắn
   `V2BaseCompanyDepartmentFilter` — phải tăng đúng 3.
5. Console **0 lỗi**.

---

### Task 7: FE — bảng theo dõi 3 cấp

**Files:**
- Create: `hrm-client/pages/assign/report/employee-work-performance/components/WorkTable.vue`
- Create: `hrm-client/pages/assign/report/employee-work-performance/components/DrillCell.vue` (copy nguyên từ `customer-market-development/components/DrillCell.vue`)

**Interfaces:**
- Consumes: `tree` + `total` từ Task 4; `metrics.by_doc` và `metrics.seats` của từng node
- Produces: sự kiện `@drill="{ key, metric }"` cho Task 8

- [x] **Bước 1: Bộ cột động**

`STT · Nội dung theo dõi · <các loại ĐANG BẬT> · Tổng · Đã HT · Tỷ lệ HT`.
Tiêu đề cột **viết hoa chữ đầu** (`text-transform: none`, `12px`, `letter-spacing: 0`) và
`white-space: nowrap`. Mọi số là link mở popup.

- [x] **Bước 2: Tooltip 2 con số ở ô Tổng của dòng cha**

```js
/**
 * Dòng cha đếm theo PHIẾU nên nhỏ hơn tổng các dòng con — ghi thẳng cả 2 con số vào tooltip
 * của ô Tổng để user tự đối chiếu, khỏi phải đẻ thêm cột cho bảng (user chốt 2026-09-21).
 * Dựa vào cờ `by_doc` của BE, KHÔNG tự suy từ `dim`.
 */
seatNote(m) {
    return m.by_doc && m.seats !== m.total
        ? `\n${Number(m.total).toLocaleString('en-US')} phiếu · ${Number(m.seats).toLocaleString('en-US')} lượt tham gia`
        : ''
},
```

- [x] **Bước 3: Select chọn cấp xem** — đặt trong ô tiêu đề cột *Nội dung theo dõi*:
`Chỉ Phòng ban` · `Đến Bộ phận` · `Tất cả cấp (đến Nhân viên)`.
Hiểu theo **TÊN CẤP, không theo độ sâu** (xét `dim` của CON) — phòng không chia bộ phận phải dừng
ở Phòng ban, **không lòi nhân viên ra sớm**. Bấm mũi tên từng dòng không đụng vào lựa chọn của
select. *Xoá lọc* đưa về `Chỉ Phòng ban`.

- [x] **Bước 4: Phân tầng màu theo cấp**

Nền dòng cha tách theo TỪNG cấp `d0 #dceaf4` · `d1 #e9f3f9` · `d2 #f2f8fb`; vạch cấp bên trái ô tên
dựng bằng `::before` tuyệt đối (**KHÔNG** `border-left` của `td` — border nằm ở mép ô, không nằm
đúng chỗ thụt lề); kẻ đậm `2px #b6d8e0` phía trên mỗi dòng cấp 0.

- [x] **Bước 5: Chú thích dưới bảng — đổi chữ theo cờ chủ trì**

Chép nguyên câu đã chốt ở `renderNote()` của mockup: *dòng Nhân viên +1 cho mỗi người tham gia ·
dòng Bộ phận / Phòng ban / TỔNG đếm theo phiếu · dòng cha nhỏ hơn tổng dòng con · cộng các phòng
lớn hơn dòng TỔNG*. Chữ xám `#6b7280`, **không** `.text-muted` (trong hrm-client là màu ĐỎ).

- [x] **Bước 6: Verify Playwright MCP — 6 phép đo từ DOM**

1. **0 dòng cha có `Tổng` > tổng các dòng con trực tiếp** (sai chiều = sai luật).
2. **>= 1 dòng cha có `Tổng` < tổng dòng con** (nếu 0 dòng thì hoặc dữ liệu không có việc làm
   chung, hoặc cờ `by_doc` chưa tới FE — phải kiểm lại, đừng bỏ qua).
3. Cộng mọi dòng cấp 0 **>=** dòng TỔNG.
4. `title` của ô Tổng ở dòng cha khớp mẫu `N phiếu · M lượt tham gia`; dòng nhân viên **không có**
   dòng này.
5. Select cấp ra đúng 3 nấc; ở nấc *Đến Bộ phận* có **0 dòng nhân viên** lọt ra.
6. Bật *Chỉ tính việc chủ trì* → **0 dòng cha lệch** với tổng dòng con (2 cách đếm trùng nhau) và
   tooltip hết phần "lượt tham gia".

---

### Task 8: FE — popup chi tiết + drawer

**Files:**
- Create: `hrm-client/pages/assign/report/employee-work-performance/components/WorkDrillModal.vue`

**Interfaces:**
- Consumes: `GET .../drill` (Task 5), sự kiện `@drill` (Task 7)
- Produces: mở drawer chi tiết 1 đầu việc

- [x] **Bước 1: Copy khung** `DevelopmentDrillModal.vue` (1.050 dòng) — giữ nguyên bộ lọc trong
popup, sort 2 mũi tên, khối tổng hợp mặc định thu gọn, nút In / Xuất Excel của popup.

- [x] **Bước 2: Bộ cột ẩn theo CHIỀU BỊ CỐ ĐỊNH**

```js
/**
 * Chiều nào ĐÃ BỊ CỐ ĐỊNH thì bỏ CẢ CỘT, CẢ Ô LỌC, CẢ CHIP — cột lặp đúng 1 giá trị trên mọi
 * dòng thì không mang thông tin, chỉ đẩy cột có ích ra ngoài khung.
 *
 * 5 nguồn cố định:
 *   1. path của node đã bấm            -> dept / part / emp
 *   2. metric là 1 trong 5 loại        -> type
 *   3. metric là 1 trong 4 trạng thái  -> bucket
 *   4. cờ "Chỉ tính việc chủ trì"      -> role
 *   5. popup GỘP THEO PHIẾU            -> role   (1 dòng mang nhiều vai trò)
 *
 * ⚠️ Chỉ ẩn theo chiều BỊ CỐ ĐỊNH, KHÔNG ẩn theo dữ liệu — cột tình cờ chỉ có 1 giá trị vẫn
 * phải giữ, nếu không cột nhảy ra nhảy vào mỗi lần đổi bộ lọc.
 */
```
Số cột đổi theo từng popup nên `min-width` của bảng phải khai **inline** theo tổng colgroup hiện
tại, KHÔNG để số cứng trong CSS (khuôn gốc khai `min-width: 1740px` cho bảng 14 cột của màn khác —
để nguyên là nới đều mọi cột và đẩy cột cuối ra ngoài khung).

- [x] **Bước 3: Ô Nhân viên / Phòng ban / Bộ phận hiện `+N`**

```js
/** Dòng gộp theo phiếu: hiện người ĐẠI DIỆN + "+N", hover ra đủ tên, đại diện đứng ĐẦU. */
mateExtra(row, field) {
    if (!row.mates || row.mates.length < 2) return ''
    const n = new Set(row.mates.map((m) => m[field])).size
    return n > 1 ? ` +${n - 1}` : ''
},
mateTitle(row) {
    if (!row.mates || row.mates.length < 2) return ''
    const rest = row.mates.filter((m) => m.emp_id !== row.emp_id)
    return `${row.mates.length} người tham gia: ` + [row, ...rest].map((m) => m.emp_name).join(' · ')
},
```

- [x] **Bước 4: 3 KPI — ẩn KPI thứ 3 khi không cố định đơn vị**

```js
/**
 * Ở popup gộp theo phiếu mà KHÔNG cố định đơn vị nào (dòng TỔNG, dải tổng hợp), phiếu nào cũng
 * do một ai đó trong phạm vi chủ trì -> KPI này luôn 100%, mẫu số bằng tử số. Cùng lý do đã bỏ
 * "bình quân/người": chỉ số không đổi thì không mang tin, hiện 100% còn gây hiểu nhầm.
 */
showHostKpi() {
    return !this.byDoc || this.nodePath.length > 0
},
```
Popup gộp đổi nhãn KPI thành **"Tỷ lệ phiếu đơn vị chủ trì"**.

- [x] **Bước 5: Dòng phụ ghi kèm số lượt**

`"107 đầu việc · 158 lượt tham gia · hoàn thành 59 · quá hạn 10 · Kỳ …"` — chỉ ghi phần *lượt tham
gia* khi 2 số khác nhau.

- [x] **Bước 6: Drawer chi tiết 1 đầu việc**

Bấm tên công việc trong popup → mở drawer, **nằm TRÊN popup** (`z-index` drawer > popup), popup giữ
nguyên phía dưới. Nội dung theo `design.md` mục "Gotcha" điểm 5:

- Bảng **thành phần tham gia** (STT · Nhân viên · Vai trò · Phòng ban · Bộ phận) — đây là nơi xem
  đủ danh sách người của dòng đã gộp `+N`.
- 2 ô trạng thái tách bạch: **Trạng thái** (1 trong 4 nhóm theo dõi) và **Trạng thái chứng từ**
  (trạng thái gốc của phiếu) — đặt 2 tên khác nhau để không lẫn.
- `type = meeting` thì ô *Tiến độ* đổi thành **Biên bản họp** (kết quả của meeting là biên bản, nó
  không có % tiến độ), và ô thứ 2 đổi từ *Giờ họp* thành **Kết thúc**.
- Việc gọn trong 1 ngày thì dòng đồng hồ ở header rút gọn: `01/09/2026 15:00 – 17:00`, không viết
  đủ ngày 2 lần.
- Escape đóng **drawer trước**, popup vẫn mở (Escape đóng cả hai là sai).

- [x] **Bước 7: Verify Playwright MCP — 6 phép đo**

1. Bấm số ở dòng **phòng ban**: số dòng popup **=** con số vừa bấm; số mã phiếu khác nhau **=** số
   dòng; **không có** cột *Vai trò*.
2. Bấm số ở dòng **nhân viên**: số dòng **=** con số trên bảng; **vẫn còn** cột *Vai trò*.
3. Lọc 1 nhân viên bên trong popup phòng ban → số dòng giảm, **0 dòng còn `+N`**.
4. Popup dòng TỔNG: đúng **2 KPI**; popup 1 phòng ban: **3 KPI**, KPI thứ 3 < 100%.
5. Tooltip ô Nhân viên: tên đầu tiên **chính là** tên đang hiện trong ô.
6. Mở drawer từ trong popup: `z-index` drawer **>** popup; bảng thành phần có **đúng
   `mates.length` dòng**; Escape lần 1 đóng drawer mà popup **vẫn mở**.

---

### Task 9: In + Xuất Excel

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Report/EmployeeWorkPerformancePrintService.php`
- Create: `hrm-api/Modules/Assign/Export/EmployeeWorkPerformanceExport.php`
- Create: `hrm-api/Modules/Assign/Resources/views/exports/assign/employee_work_performance_report.blade.php`
- Create: `hrm-client/pages/assign/report/employee-work-performance/components/PrintOptionsModal.vue` (copy nguyên từ `customer-market-development/`)
- Modify: `index.vue` — thêm `reportPrintPreviewMixin` + `ReportPrintPreviewModal`

**Interfaces:**
- Consumes: `getData()` · `getDrillRows()` (Task 4, 5) — **không tính lại số ở đây**
- Produces: `EmployeeWorkPerformanceService::getFlatRowsForExport(Request $r): array`

- [x] **Bước 1: `getFlatRowsForExport()` — luôn đủ 3 cấp**

Duyệt cây đã dựng, ra mảng phẳng có STT phân cấp (`1`, `1.1`, `1.1.2`) và thụt lề tên bằng khoảng
trắng. **Không phụ thuộc cấp đang bung trên màn.**

- [x] **Bước 2: Print service — số lấy từ service chính**

Bám `CustomerMarketDevelopmentPrintService`: `use PrintsCompanyLetterhead`, trả HTML thuần.
- Letterhead lấy theo **`company_id` GHI TRÊN BÁO CÁO** (ô lọc Công ty), KHÔNG theo người đăng nhập.
- Meta bản in ghi `N đầu việc (M lượt tham gia)` + câu giải thích cách đếm theo cấp.
- **`number_format()` mặc định** (phẩy ngăn nghìn, chấm thập phân) — cấm tham số kiểu VN.

- [x] **Bước 3: Excel — ô số là SỐ THẬT**

```php
class EmployeeWorkPerformanceExport implements FromView, ShouldAutoSize
```
Blade đổ ô số kèm `data-format="#,##0"`, **KHÔNG** đổ chuỗi đã format sẵn (đổ chuỗi thì Excel báo
*"number stored as text"* và `SUM` ra 0).

- [x] **Bước 4: FE gắn popup xem trước**

```js
mixins: [PageTitleMixin, reportPrintPreviewMixin],
// ...
this.openPrintList('assign/report/employee-work-performance', this.filters, 'Xem trước báo cáo …')
```
⚠️ Endpoint phải đúng tên `print-list-data` và khoá `template` — đổi tên là popup nhận rỗng mà
**không báo lỗi gì**.

- [x] **Bước 5: Verify Playwright MCP**

1. Bấm **In báo cáo** → popup xem trước có nội dung; số dòng bản in **=** số dòng khi bung
   *Tất cả cấp* (bản in luôn đủ cấp dù màn đang thu gọn).
2. Meta bản in ghi đúng `N đầu việc (M lượt tham gia)`; N khớp ô *Tổng đầu việc* trên màn.
3. Letterhead ra đúng công ty đang chọn ở ô lọc (đổi công ty → đổi letterhead).
4. Bấm **Xuất Excel** → tải được file; mở ra ô số **SUM được** (không phải text).

---

### Task 10: E2E + rà chuẩn trước bàn giao

**Files:**
- Create: `hrm-client/../e2e/tests/assign/employee-work-performance.api.spec.ts`
- Create: `hrm-client/../e2e/tests/assign/employee-work-performance.spec.ts`
- Create: `hrm-client/../e2e/utils/ewpFixture.ts`

- [ ] **Bước 1: Fixture cấp quyền — nhớ XOÁ CACHE**

Bám `e2e/utils/cmdFixture.ts`. Gán 3 quyền cho role của tài khoản e2e (`role_has_permissions` cần
`company_id = 1`) **và dựng thêm 1 tài khoản role rỗng** cho ca fail-closed.
⚠️ Cấp quyền bằng SQL xong **bắt buộc `php artisan cache:clear`** — `spatie` cache quyền 24h, chạy
riêng thì xanh mà chạy cả bộ lại 403.

- [ ] **Bước 2: Spec API — assert ĐẲNG THỨC, không so tổng tuyệt đối**

```ts
/**
 * ⚠️ KHÔNG so tổng tuyệt đối: DB test còn fixture của feature khác cũng rơi vào kỳ này.
 * Assert các bất biến luôn đúng kể cả khi DB có thêm dữ liệu:
 *   (a) 4 nhóm trạng thái chia hết tổng, ở MỌI node
 *   (b) 5 cột loại cộng lại = tổng, ở MỌI node
 *   (c) dòng cha <= tổng dòng con  ← KHÁC báo cáo anh em (bên kia là ==)
 *   (d) cộng các dòng cấp 0 >= dòng TỔNG
 *   (e) số dòng popup = con số trên cây, ở CẢ node cha lẫn node nhân viên
 *   (f) popup cấp cha: số dòng = số doc_key khác nhau; popup cấp NV: giữ cột role
 *   (g) bật host_only -> seats == total ở mọi node, và (c) trở thành ==
 *   (h) PHÂN QUYỀN: tài khoản role rỗng -> 403; thiếu company_id -> 422;
 *       company_id lạ -> 403
 */
```
⚠️ Ca (h) là **bắt buộc** — màn này lộ khối lượng việc của toàn phòng ban, thủng gate là lộ dữ
liệu nhân sự.

- [ ] **Bước 3: Spec UI — bám 6 phép đo của Task 7 + 5 phép đo của Task 8**

⚠️ Bộ test chạy `serial`: một ca fail làm mọi ca sau in **"did not run"**, KHÔNG phải "passed" —
phải đọc **dòng tổng kết**. Cấm chờ `networkidle` (app polling nền → hết giờ test).

- [ ] **Bước 4: Chạy đủ bộ, 1 worker**

```bash
cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test assign/employee-work-performance --workers=1
```
⚠️ Luôn `--workers=1` (2 worker tranh 1 Nuxt dev server gây đỏ ngẫu nhiên) và đừng chạy khi có
session khác đang thao tác dữ liệu.

- [ ] **Bước 5: Rà chuẩn — cả 5 lệnh phải RỖNG**

```bash
cd hrm-client
# 1. không HTML thô trong màn mới
grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' \
  pages/assign/report/employee-work-performance/ | grep -v V2Base
# 2. không format số kiểu VN
grep -rnE "(toLocaleString|Intl\.NumberFormat)\(\s*'vi-VN'" \
  pages/assign/report/employee-work-performance/ | grep -v "new Date"
# 3. không cờ quyền hard-code true
grep -rnE "can[A-Za-z]*\s*=\s*true|is_(company|department|part)\s*:\s*true" \
  pages/assign/report/employee-work-performance/
# 4. không .text-muted (trong hrm-client là màu ĐỎ)
grep -rn 'text-muted' pages/assign/report/employee-work-performance/
cd ../hrm-api
# 5. không number_format kiểu VN
grep -rnE "number_format\([^)]+,\s*'.?',\s*'\.'\)" \
  Modules/Assign/Services/Report/EmployeeWorkPerformance* \
  Modules/Assign/Resources/views/exports/assign/employee_work_performance_report.blade.php
```

- [ ] **Bước 6: Giữ nguyên EOL**

```bash
git -C hrm-api diff --numstat && git -C hrm-client diff --numstat
```
File chỉ sửa vài dòng mà báo xoá hàng trăm dòng = đã đổi EOL cả file. Repo **toàn bộ là LF**.

- [ ] **Bước 7: Cập nhật tài liệu**

- `design-phase4.md`: thêm mục *"Đã tự kiểm"* kèm con số đo được thật.
- `.plans/gop-db/STATUS.md`: chuyển feature sang *Hoàn thành Phase 4*.
- Nợ còn lại: cột `tasks.start_time` (giờ bắt đầu Task luôn `00:00`).

---

### Checkpoint — 22/09/2026 (Phase 4: 9/10 task, đã merge `gop_db`)

**Vừa hoàn thành:** Task 1-9 — toàn bộ tính năng. BE (quyền 3 cấp · gom 5 nguồn · cây 3 cấp · popup
gộp theo phiếu · in + Excel) và FE (bộ lọc · dải tổng hợp · bảng 3 cấp · popup + drawer · in/Excel).
**39 unit test xanh (122 assertions).** Đã merge fast-forward vào `gop_db`:
`hrm-api bf0711d6e` · `hrm-client 07a9a6dc4`. **CHƯA PUSH.**

**Đang làm dở:** không có task nào dở giữa chừng.

**Bước tiếp theo:** **Task 10 — e2e + rà chuẩn bàn giao** (7 bước, xem mục Task 10 ở trên). 4 việc
quan trọng nhất trong đó:
1. Xác nhận **đúng role mà bộ e2e dùng** — Task 1 tự suy ra `role_id = 18`, chưa ai xác nhận.
2. Kiểm **index** `assign_requests.from_time` / `meetings.start_date` / `assign_jobs.time_start_request`
   trước khi lên production (§7 yêu cầu, chưa ai làm).
3. Chạy thử **`PermissionsTableSeeder` trọn bộ trên DB nháp** — cả phase chỉ INSERT tay 3 dòng, chưa
   bao giờ chạy seeder thật.
4. Viết 2 spec e2e (`.api.spec.ts` + `.spec.ts`) — lưu ý `HRM/e2e/` **không thuộc repo nào**, worktree
   không cách ly được.

**Blocked:** không có.

**Nợ / lưu ý bàn giao:**
- **Letterhead chỉ kiểm được tới mức URL** ở local (thiếu `ERP_URL` + `erp/public/uploads`) — ảnh thật
  phải nghiệm thu ở môi trường có 2 thứ đó.
- `tasks.start_time` vẫn là nợ backend (giờ bắt đầu Task luôn `00:00`).
- **Bảng `issues` rỗng toàn DB local** → nhánh issue chưa từng chạy với dữ liệu thật.
- 11 **minor đã hoãn** nằm rải trong `.sdd/progress.md`, đáng chú ý nhất:
  `EmployeeWorkPerformancePrintService` **mirror logic cột của FE** → FE đổi `ALL_COLUMNS`/`fixedDims`
  mà quên sửa BE thì bản in lệch với màn, im lặng.

### Checkpoint — Phase 4 (chưa bắt đầu)
**Vừa hoàn thành:** lập plan Phase 4 + `design-phase4.md` (2026-09-21). Đã đối chiếu 5 bảng nguồn
trên DB `hrm_erp` thật và chốt 3 quyết định với user: menu ở 2 phân hệ (CSKH trước bán + Công việc),
phân quyền 3 cấp Công ty/Phòng ban/Bộ phận + bắt buộc chọn 1 công ty, route
`/assign/report/employee-work-performance`.
**Đang làm dở:** chưa viết dòng code nào.
**Bước tiếp theo:** Task 1 (quyền + đường vào màn).
**Blocked:** không có. 2 điểm đã nêu để user duyệt lại khi bắt đầu Task 3: (1) "Tạm dừng" của Task
rơi vào nhóm *Dừng / Huỷ / Từ chối* theo `WorkItemStatusGroup` thay vì *Đang thực hiện* như mockup;
(2) task/issue chưa đặt hạn lấy `created_at` làm mốc thay vì bị loại khỏi báo cáo.
