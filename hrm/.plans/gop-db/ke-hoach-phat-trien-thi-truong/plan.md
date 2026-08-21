# Plan — Kế hoạch phát triển thị trường (Mockup UI)

> **Cho worker:** đây là mockup HTML tĩnh 1 file. Không có unit test — mỗi task kết thúc bằng **verify Playwright** (chạy qua `python3 -m http.server`, chụp screenshot + kiểm phần tử). Bám spec: `docs/superpowers/specs/gop-db/2026-08-08-ke-hoach-phat-trien-thi-truong-design.md`.

**Goal:** Dựng file HTML tĩnh self-contained mô phỏng màn "Kế hoạch phát triển thị trường" (2 tab: Theo lịch + Theo thị trường), style navy+teal đồng bộ menu Bán hàng.

**Architecture:** 1 file `ke-hoach-phat-trien-thi-truong-mockup.html` — inline CSS + inline SVG + vanilla JS render từ mock data. Không CDN, không thư viện ngoài. Verify từng phase bằng Playwright.

**Tech Stack:** HTML5 + CSS3 (fl/grid) + vanilla JS. Playwright (qua MCP) để verify.

## Global Constraints (copy từ spec — áp cho MỌI task)

- File tại: `.plans/gop-db/ke-hoach-phat-trien-thi-truong/ke-hoach-phat-trien-thi-truong-mockup.html`
- Self-contained: inline CSS + inline SVG, **KHÔNG CDN / thư viện ngoài**.
- Bảng màu: navy `#0a1c3d→#1e57a0`, primary `#2E71C3`, teal `#0a99a7` / header `#20d9ea`.
- 4 trạng thái: Tiềm năng 🟢`#2ecc71` · Đang chăm sóc 🔵`#3498db` · Đã chốt 🟠`#f39c12` · Hủy/Không phù hợp ⚪`#95a5a6`.
- Verify Playwright: chặn `file://` → chạy `python3 -m http.server <port>` trong folder feature, mở `http://127.0.0.1:<port>/ke-hoach-phat-trien-thi-truong-mockup.html`.
- Không commit/push khi chưa có yêu cầu.

---

## Phase 1 — Scaffold + tokens + khung layout

### Task 1: Khung trang + design tokens + topbar/toolbar/KPI/tabs (rỗng)

**Files:**
- Create: `.plans/gop-db/ke-hoach-phat-trien-thi-truong/ke-hoach-phat-trien-thi-truong-mockup.html`

- [x] **Step 1:** Tạo file HTML với `<head>` chứa `<style>` khai báo CSS variables (màu theo Global Constraints), reset cơ bản, font system-ui.
- [x] **Step 2:** Dựng TOPBAR navy gradient + tiêu đề "Kế hoạch phát triển thị trường".
- [x] **Step 3:** Dựng TOOLBAR filter (Tháng/Năm, Phòng ban=Kinh doanh, NV kinh doanh, Người theo dõi, Thị trường, ô Tìm kiếm, nút [+ Thêm KH]) — dạng static, chưa cần hoạt động.
- [x] **Step 4:** Dựng DẢI KPI 4 thẻ trạng thái (icon màu + nhãn + số 0 tạm).
- [x] **Step 5:** Dựng hàng TABS [📅 Theo lịch] [🗂 Theo thị trường] + 2 vùng nội dung rỗng (`#tab-calendar`, `#tab-market`), mặc định hiện tab Theo thị trường.
- [x] **Step 6:** Dựng FOOTER 2 cột (Đánh giá chung + Ghi chú chung) với text mock.
- [x] **Step 7 (verify):** Chạy http.server, mở bằng Playwright, chụp screenshot. Kiểm: topbar/toolbar/KPI/tabs/footer hiển thị, không lỗi console, không tràn ngang.

---

## Phase 2 — Mock data + Tab "Theo thị trường"

### Task 2: Khai báo mock data JS

**Files:**
- Modify: file mockup (thêm `<script>` mock data cuối `<body>`)

**Interfaces (Produces):** các biến global dùng ở task sau:
- `MARKETS = [{id, name}]`
- `EMPLOYEES = [{id, name}]`
- `CUSTOMERS = [{id, marketId, employeeId, name, contact, phone, email, industry, need, source, status, result, cancelReason, nextPlan:{date,content}, history:[{date,content,result,doneBy}]}]`
- `status` ∈ `'potential'|'caring'|'closed'|'cancelled'`
- `EVENTS = [{date, time, type, title, customerId, employeeId}]`, `type` ∈ `'plan'|'history'|'meeting'`

- [x] **Step 1:** Khai báo `MARKETS` (~5: Miền Bắc, Miền Trung, Miền Nam, Hà Nội, TP.HCM), `EMPLOYEES` (~3: NV1/NV2/NV3).
- [x] **Step 2:** Khai báo `CUSTOMERS` (~12-15) rải trên các thị trường, đủ 4 trạng thái, mỗi KH có 1-3 `history` + 1 `nextPlan` (ngày nằm trong tháng hiện tại — hardcode tháng 8/2026 để khớp mock, tránh dùng `Date.now()`).
- [x] **Step 3:** Sinh `EVENTS` từ CUSTOMERS (plan từ `nextPlan`, history từ `history`) + thêm ~4-5 meeting/công tác hardcode.
- [x] **Step 4 (verify):** Reload, đọc console (`EVENTS.length`, `CUSTOMERS.length` > 0), không lỗi JS.

### Task 3: Render accordion "Theo thị trường" + cập nhật KPI

**Files:**
- Modify: file mockup

**Interfaces (Consumes):** `MARKETS`, `CUSTOMERS`, `EMPLOYEES` từ Task 2.

- [x] **Step 1:** Viết `renderMarketTab()`: group CUSTOMERS theo `marketId`, mỗi thị trường 1 accordion (header: tên + tổng KH + badge đếm theo 4 trạng thái + chevron).
- [x] **Step 2:** Body accordion = danh sách dòng KH (chấm trạng thái · tên KH · người liên hệ · NV phụ trách · kết quả Chốt/Hủy · ngày kế hoạch tiếp theo, rỗng → "—"). Tên/nội dung dài → ellipsis + `title`.
- [x] **Step 3:** Toggle thu/mở accordion khi click header (mặc định mở hết).
- [x] **Step 4:** Viết `updateKpi()`: đếm CUSTOMERS theo status, đổ vào 4 thẻ KPI.
- [x] **Step 5 (verify):** Playwright: thấy đủ các nhóm thị trường, badge đếm đúng, KPI khớp tổng; click header → thu/mở; chụp screenshot.

### Task 4: Drawer chi tiết KH (trượt phải)

**Files:**
- Modify: file mockup

**Interfaces (Consumes):** dòng KH từ Task 3 (`data-cid`).

- [x] **Step 1:** Dựng markup drawer (ẩn mặc định, `transform: translateX(100%)`) + backdrop mờ.
- [x] **Step 2:** Viết `openDrawer(cid)`: đổ đầy đủ — khối thông tin KH (contact, phone/email, industry, need, source), khối trạng thái (chip + result + cancelReason), timeline "Lịch sử làm việc" (sort ngày giảm dần), khối "Kế hoạch tiếp theo". Thêm nút UI [Sửa] [Thêm hoạt động] (chưa cần hoạt động).
- [x] **Step 3:** Gắn click dòng KH → `openDrawer`; ESC / click backdrop → đóng (`closeDrawer`).
- [x] **Step 4 (verify):** Playwright: click 1 KH → drawer trượt ra đủ thông tin + timeline; ESC đóng; danh sách vẫn thấy phía sau. Screenshot.

---

## Phase 3 — Tab "Theo lịch"

### Task 5: View Tháng + filter loại sự kiện

**Files:**
- Modify: file mockup

**Interfaces (Consumes):** `EVENTS` từ Task 2.

- [x] **Step 1:** Dựng header tab lịch: toggle [Tháng][Tuần] + ◀ ▶ + nhãn kỳ + 3 chip filter loại (🟣 Kế hoạch · 🟢 Lịch sử · 🔵 Meeting/công tác), mặc định bật cả 3. State kỳ hardcode start = tháng 8/2026.
- [x] **Step 2:** Viết `renderMonth()`: lưới 7 cột × 6 hàng, số ngày góc ô, ngày ngoài tháng mờ, ngày 8/8/2026 highlight "hôm nay".
- [x] **Step 3:** Đổ EVENTS (đã lọc theo filter) vào đúng ô ngày; mỗi ô tối đa 3 chip màu theo type, dư → "+N khác".
- [x] **Step 4:** ◀ ▶ đổi tháng (re-render); toggle filter chip → ẩn/hiện loại; filter tắt hết → "Không có sự kiện".
- [x] **Step 5 (verify):** Playwright: chuyển sang tab Theo lịch, thấy lưới tháng + chip sự kiện đúng màu; tắt 1 filter → loại đó biến mất; ◀▶ đổi tháng. Screenshot.

### Task 6: View Tuần + popover chi tiết sự kiện

**Files:**
- Modify: file mockup

- [x] **Step 1:** Viết `renderWeek()`: cột = 7 ngày, hàng = khung giờ 7:00–18:00; sự kiện có `time` (meeting/công tác) đặt đúng khung; sự kiện cả ngày (plan/history) nằm dải "cả ngày" trên cùng.
- [x] **Step 2:** Toggle [Tháng][Tuần] chuyển view; ◀▶ ở view Tuần đổi tuần.
- [x] **Step 3:** Click chip sự kiện (cả 2 view) → popover nhỏ: KH liên quan · nội dung · người thực hiện · giờ (nếu có). Click ngoài → đóng.
- [x] **Step 4 (verify):** Playwright: chuyển Tuần → thấy khung giờ + meeting đúng chỗ; click chip → popover đúng nội dung. Screenshot.

---

## Phase 4 — Hoàn thiện

### Task 7: Responsive + polish + verify tổng

**Files:**
- Modify: file mockup

- [~] **Step 1:** Responsive: drawer full-width < 768px; toolbar wrap; lưới lịch scroll ngang trong container riêng nếu chật (body không tràn ngang). — CODE ĐÃ VIẾT nhưng CHƯA verify (user yêu cầu để sau khi chốt UI desktop).
- [x] **Step 2:** Tìm kiếm toolbar: lọc KH theo tên (tab Theo thị trường) — ẩn dòng/nhóm không khớp.
- [x] **Step 3:** Polish: hover states, transition drawer/accordion/tab, chú thích màu trạng thái, icon SVG cho KPI & loại sự kiện.
- [x] **Step 4 (verify tổng):** Playwright ở **1440px** (desktop): 2 tab + drawer + view Tháng/Tuần + popover + "+N khác" + tìm kiếm — sạch. (375px hoãn theo yêu cầu user.)
- [x] **Step 5:** Báo user review mockup trên app thật (URL http.server).

---

## Phase 5 — PIVOT v2: 1 màn lịch phiếu công việc (2026-08-08)

> Đổi hướng theo yêu cầu user: bỏ tab, gộp 1 màn lịch của 4 loại phiếu (công tác/meeting/giao việc/task) + filter thật + KPI đếm theo loại. Spec v2 đã cập nhật.

### Task 8: Data model phiếu + bỏ tab + layout 1 màn lịch + KPI theo loại
- [x] **Step 1:** Thay mock: `DEPARTMENTS`, `EMPLOYEES{departmentId}`, `MARKETS`, `TICKETS` (25-35 phiếu, 4 loại, 4 trạng thái, đủ NV/phòng/thị trường; ≥1 ngày ≥4 phiếu; meeting/công tác có giờ).
- [x] **Step 2:** Bỏ 2 tab + tab switcher; vùng nội dung = **chỉ lịch** (giữ header lịch Tháng/Tuần + ◀▶). Ẩn/xóa accordion tab thị trường (giữ code drawer để tái dùng).
- [x] **Step 3:** Thẻ phiếu trên ô ngày/tuần: màu theo LOẠI (viền trái + tint) + thời gian (nếu có) + tiêu đề ellipsis + **badge trạng thái** (chấm + nhãn). Chú thích màu 4 loại (legend tĩnh).
- [x] **Step 4:** Đổi 4 box thành **đếm số phiếu theo loại** (Phiếu công tác/Meeting/Phiếu giao việc/Task) trong tập đang hiển thị.
- [x] **Step 5 (verify):** Playwright 1440: 1 màn lịch, thẻ đủ màu loại + giờ + badge trạng thái, 4 box đếm đúng theo loại. Screenshot.

### Task 9: Bộ lọc chạy thật + popover→drawer chi tiết phiếu
- [x] **Step 1:** Toolbar: giữ Tháng/Năm, Phòng ban, Nhân viên, Người theo dõi, Thị trường, Tìm kiếm + thêm **Loại phiếu** + **Trạng thái** (đổ option từ mock). Nút "Xóa lọc".
- [x] **Step 2:** `applyFilters()`: tính `filteredTickets` (AND) → re-render lịch (view đang mở) + cập nhật 4 box. Đổi filter nào cũng chạy. Rỗng → lịch trống + box 0 + thông báo.
- [x] **Step 3:** Click thẻ → popover (loại/tiêu đề/giờ/trạng thái/người thực hiện/địa điểm) + link "Xem chi tiết".
- [x] **Step 4:** "Xem chi tiết" → drawer phải (tái dùng) đổ đầy đủ trường phiếu. ESC/backdrop/✕ đóng.
- [x] **Step 5:** BỎ footer 2 khối Đánh giá chung / Ghi chú chung (user yêu cầu).
- [x] **Step 6 (verify):** Playwright 1440: đổi từng filter → lịch + box đổi đúng; tìm kiếm; popover→drawer; xóa lọc; không còn footer. Screenshot.

> Responsive: HOÃN tới khi chốt UI desktop (yêu cầu user).

---

## Phase 6 — Bám style THẬT phân hệ Bán hàng + nâng cấp visual (2026-08-08)

> Khảo sát UI thật (`sale-theme.scss` + `V2BaseFilterPanel` + ảnh app `/sale/quotations`). Bộ lọc hiện xấu + chưa đúng → dựng lại theo pattern thật; 4 box gọn hơn; calendar ấn tượng + phân biệt T7/CN/hôm nay.

### Task 10: Dựng lại filter bar theo pattern V2BaseFilterPanel + lọc chạy đúng
- [x] **Step 1:** Bọc filter trong card trắng `.tp-card` (radius 8-12px, viền `#e5e7eb`, shadow nhẹ). Header: icon tròn teal (ri-filter, nền `rgba(10,153,167,.12)` màu `#0a99a7`) + tiêu đề gạch teal trái + nút "Tìm kiếm nâng cao" (toggle) bên phải.
- [x] **Step 2:** Hàng quick-search: ô input (icon kính lúp trái, radius 8px, h30-32px, viền `#d1d5db`) chiếm flex + nút **[Tìm kiếm]** primary teal `#1abc9c` (radius 8px h32) + **[Làm mới]** trắng viền. Tìm theo tiêu đề phiếu.
- [x] **Step 3:** Khối "nâng cao" (ẩn/hiện bằng toggle): lưới 4 cột (Phòng ban · Nhân viên · Người theo dõi · Thị trường · Loại phiếu · Trạng thái · Tháng/Năm), mỗi field = **label trên** (12px, 600, `#0f172a`) + select dưới (h32, viền `#cbd5e1`, radius 5px, focus teal `#0a99a7`). Giao diện gọn, canh lưới đều.
- [x] **Step 4:** Lọc chạy đúng: mọi filter (kể cả quick search + nâng cao) đều AND, đổi là re-render lịch + 4 box; nút [Làm mới] reset toàn bộ. Kiểm từng filter + tổ hợp 2 filter.
- [x] **Step 5 (verify):** Playwright 1440: filter bar đẹp đúng style thật; test Loại phiếu, Trạng thái, Nhân viên, Thị trường, tổ hợp 2 filter, quick search, Làm mới. Screenshot.

### Task 11: 4 box summary gọn + calendar ấn tượng (T7/CN/hôm nay)
- [x] **Step 1:** 4 box summary nhỏ gọn: 1 hàng, chiều cao thấp (~56-64px), icon nhỏ + nhãn + số trên 1 dòng ngang, nền `.tp-card`, viền trái màu theo loại. Bỏ khoảng trống thừa.
- [x] **Step 2:** Header lịch (T2..CN): style dải teal `#20d9ea` gradient nhạt như header bảng thật; **CN** chữ đỏ/cam, **T7** nhấn nhẹ.
- [x] **Step 3:** Ô ngày: cột **T7 + CN nền tint** (xám/xanh nhạt) phân biệt ngày thường; **hôm nay (08/08)** nền nổi bật + viền accent + số trong vòng tròn filled teal/navy. Ngày ngoài tháng mờ.
- [x] **Step 4:** Polish lịch: bo góc lưới, hover ô, thẻ phiếu gọn nét, khoảng cách đều — trông hiện đại/ấn tượng.
- [x] **Step 5 (verify):** Playwright 1440: 4 box gọn; calendar phân biệt rõ T7/CN/hôm nay; view Tuần cũng phân biệt cuối tuần. Screenshot.

> Responsive vẫn HOÃN tới khi chốt UI desktop.

---

## Phase 7 — Tinh chỉnh visual + chip lọc nhanh + summary ngữ cảnh (2026-08-08, user feedback)

### Task 12: Chip lọc nhanh theo loại + summary ngữ cảnh
- [x] **Step 1:** 4 chip góc phải lịch (Phiếu công tác/Meeting/Phiếu giao việc/Task) → **click lọc nhanh theo loại**: click chip = chọn loại đó (đồng bộ select "Loại phiếu" + applyFilters), chip active nổi bật, click lại chip đang active → về "Tất cả". Các chip khác mờ khi 1 chip active.
- [x] **Step 2:** Summary ngữ cảnh: nếu Loại phiếu = Tất cả → hiện **4 box** như hiện tại. Nếu lọc 1 loại → **ẩn 4 box**, hiện **dải tổng hợp 1 hàng**: "Từ ngày [đầu kỳ] – [cuối kỳ] · Số [tên loại]: N · Chờ duyệt X · Đang thực hiện Y · Hoàn thành Z · Từ chối/Hủy W" (đếm trên tập đã lọc; khoảng ngày = kỳ lịch đang xem Tháng/Tuần).
- [x] **Step 3:** Đồng bộ 2 chiều: đổi select Loại phiếu ↔ chip active ↔ dạng summary luôn khớp. [Làm mới] về Tất cả + 4 box.
- [x] **Step 4 (verify):** Playwright 1440: click chip Meeting → chỉ meeting, chip active, summary đổi sang dải tổng hợp đúng số; click lại → về 4 box; đổi qua select cũng vậy. Screenshot.

### Task 13: De-bold ô ngày + thiết kế lại hôm nay/T7/CN
- [x] **Step 1:** Thẻ phiếu trong ô ngày: BỎ bold tràn lan — phân cấp chữ: tiêu đề weight ~500 màu đậm vừa; giờ nhỏ + màu loại (không bold nặng); badge trạng thái nhỏ, chữ thường. Chỉ 1 điểm nhấn/thẻ. Giảm rối trong không gian hẹp.
- [x] **Step 2:** Thiết kế lại **hôm nay**: tinh tế — nền ô phớt teal rất nhẹ, số ngày trong **vòng tròn filled** gọn (teal), bỏ/thu nhãn "HÔM NAY" cồng kềnh (thay bằng dấu chấm/label rất nhỏ hoặc chỉ vòng tròn), có thể thêm thanh accent mảnh trên đỉnh ô. Không viền dày lòe.
- [x] **Step 3:** Thiết kế lại **T7/CN**: tint cuối tuần nhẹ nhàng hơn (không xám nặng), phân biệt bằng màu chữ tiêu đề (CN đỏ dịu, T7 tông khác nhẹ) + nền phớt tinh tế; hài hòa tổng thể.
- [x] **Step 4 (verify):** Playwright 1440: ô ngày dễ đọc, không rối bold; hôm nay/T7/CN đẹp tinh tế (Tháng + Tuần). Screenshot.

> Responsive vẫn HOÃN.

---

## Phase 8 — Bám dữ liệu THẬT 3 loại (2026-08-08, sau khảo sát app)

> Khảo sát `/assign/assign_business`, `/assign/meeting/42/show`, `/assign/tasks`. Bỏ Phiếu giao việc (còn 3 loại). Mỗi loại dùng trường + trạng thái THẬT (spec mục 3B/5B/9B).

### Task 14: Data model v3 (3 loại, trường + trạng thái thật) + card/popover/drawer theo loại
- [x] **Step 1:** Bỏ loại `giao_viec` khỏi mọi nơi (data, legend/chip, filter, summary, màu). Còn 3 loại: cong_tac/meeting/task.
- [x] **Step 2:** Viết lại `TICKETS` theo data model v3 (mục 5B): mỗi loại đủ trường thật + trạng thái đúng bộ của loại (mục 3B). ~24-30 phiếu, đủ các trạng thái mỗi loại, có Task Quá hạn, meeting Online có link, công tác có địa điểm/trưởng nhóm/nhân sự.
- [x] **Step 3:** Badge trạng thái dùng hàm màu semantic theo từ khóa (mục 3B). Thẻ lịch: giờ + tiêu đề + badge trạng thái loại.
- [x] **Step 4:** Popover theo loại (loại+code+tiêu đề+thời gian+trạng thái+người chính+link). Drawer đổ ĐÚNG bộ trường của loại (công tác/meeting/task khác nhau).
- [x] **Step 5 (verify):** Playwright 1440: 3 loại hiển thị đúng; click từng loại → drawer đúng trường; badge trạng thái đúng màu/nhãn. Screenshot.

### Task 15: Filter Trạng thái động theo loại + summary theo trạng thái thật + 3 chip
- [x] **Step 1:** Chip góc phải còn 3 (bỏ giao việc). Filter "Loại phiếu" còn 3 option.
- [x] **Step 2:** Filter "Trạng thái" ĐỘNG: Loại cụ thể → options = bộ trạng thái loại đó; Loại=Tất cả → chỉ "Tất cả". Đổi Loại thì reset/nạp lại options Trạng thái.
- [x] **Step 3:** Summary ngữ cảnh 1 loại: breakdown theo bộ trạng thái THẬT của loại (công tác 6 tt / meeting 4 / task 4). Loại=Tất cả → 3 box đếm theo loại.
- [x] **Step 4 (verify):** Playwright 1440: chọn Loại=Công tác → Trạng thái có 6 option + summary 6 trạng thái; Meeting→4; Task→4; chip đồng bộ; Làm mới. Screenshot.

> Responsive vẫn HOÃN.

---

## Phase 9 — Single-user + gọn filter vào header calendar (2026-08-08)

### Task 16: Bỏ card filter trên; đưa Trạng thái + Thị trường vào header card calendar
- [x] **Step 1:** XÓA hẳn card "Bộ lọc phiếu" trên cùng (search, tìm kiếm nâng cao, và mọi filter: Tháng/Năm, Phòng ban, Nhân viên, Người theo dõi, Loại phiếu, quick search). Giữ logic applyFilters nhưng chỉ còn 2 input.
- [x] **Step 2:** Thêm vào **header card calendar** (hàng chứa Tháng/Tuần + ◀▶ + chip loại): 2 dropdown **Thị trường** + **Trạng thái** (style select nhỏ gọn đồng bộ). Trạng thái vẫn ĐỘNG theo loại (chip): Tất cả loại→chỉ "Tất cả"; chọn loại→bộ trạng thái loại đó. Bố trí gọn, wrap đẹp nếu chật.
- [x] **Step 3:** Single-user: topbar/subtitle thể hiện tên 1 user (vd "Lịch công việc — Nguyễn Văn A"); dữ liệu mock coi như của user đó. Bỏ mọi dấu vết filter nhân viên/phòng ban.
- [x] **Step 4:** applyFilters chỉ theo Thị trường + Trạng thái + loại(chip); nút làm mới nhỏ (tùy chọn) đưa về Tất cả. Summary + calendar cập nhật đúng.
- [x] **Step 5 (verify):** Playwright 1440: không còn card filter trên; header calendar có Thị trường + Trạng thái chạy đúng; chip loại + Trạng thái động vẫn ok; summary đúng. Screenshot.

> Responsive vẫn HOÃN.

---

## Phase 10 — Màu tương phản + card có icon loại + data theo thời gian + task-market (2026-08-08)

### Task 17: Đổi màu 3 loại + card layout icon+time + data demo chuẩn + task bỏ lọc thị trường
- [x] **Step 1:** Đổi màu 3 loại tương phản mạnh: công tác teal-green `#0d9488`, meeting indigo `#4f46e5`, task orange `#ea580c` (đè mọi nơi: chip, legend, thẻ, box, drawer, popover).
- [x] **Step 2:** Thẻ item: dòng 1 = **icon tròn theo loại** (SVG trắng nền màu loại: công tác=briefcase, meeting=nhóm người, task=checklist) + tiêu đề (ellipsis); dòng 2 = **thời gian "Từ - Đến"** (HH:mm - HH:mm; không giờ → "Cả ngày") + **badge trạng thái**. Bỏ giờ ở đầu dòng 1.
- [x] **Step 3:** Data demo theo thời gian (hôm nay 08/08/2026): ngày > hôm nay KHÔNG "Hoàn thành"/"Hoàn thành - Chờ duyệt"/"Đã duyệt kết quả"/overdue; chỉ trạng thái chờ/đang. Hoàn thành/Quá hạn/Không duyệt chỉ ngày ≤ hôm nay. Rà lại toàn bộ TICKETS cho hợp lý.
- [x] **Step 4:** Task không lọc theo Thị trường: khi loại=Task (chip) → Thị trường disable + reset "Tất cả"; loại khác → enable lại.
- [x] **Step 5 (verify):** Playwright 1440: 3 màu tương phản rõ; thẻ có icon tròn + time Từ-Đến dòng 2 trước badge; ngày tương lai không Hoàn thành/Quá hạn; chọn Task → Thị trường mờ/disable. Screenshot.

### Task 18: Summary khi chọn loại — thiết kế ấn tượng
- [x] **Step 1:** Loại=1 loại → dải summary dạng **thẻ/pill trạng thái** (mỗi trạng thái: chấm/viền màu semantic + nhãn + số lớn), **tổng nổi bật** (Số [loại]: N cỡ lớn) + khoảng ngày kỳ. Bố cục thoáng, có nền/viền tinh tế đồng bộ tông. (Loại=Tất cả giữ 3 box.)
- [x] **Step 2:** Cập nhật realtime theo filter/kỳ/chip; wrap đẹp khi nhiều trạng thái (công tác 6).
- [x] **Step 3 (verify):** Playwright 1440: chọn công tác/meeting/task → summary pills đẹp, số đúng. Screenshot.

> Responsive vẫn HOÃN.

---

## Phase 11 — Bỏ popover + drawer chi tiết ấn tượng (2026-08-08)

### Task 19: Click thẻ mở thẳng drawer (bỏ popover) + redesign drawer
- [x] **Step 1:** Bỏ popover chi tiết sự kiện: click thẻ phiếu → gọi thẳng `openTicketDrawer(id)` (không hiện popover trung gian). Popup "+N khác" của ngày giữ; click 1 mục trong đó → mở thẳng drawer. Dọn code popover không dùng (nếu chỉ dùng cho chi tiết).
- [x] **Step 2:** Redesign drawer ấn tượng: **header banner** gradient màu theo loại + icon tròn loại + tiêu đề lớn (trắng) + badge trạng thái + dòng phụ (mã/thời gian). Thân: các **khối có tiêu đề + icon** (Thông tin chính / Liên quan / Mô tả…), nhãn–giá trị thoáng, trường quan trọng nhấn. Nút Sửa/Duyệt đẹp dưới chân. Vẫn đúng bộ trường theo loại (công tác/meeting/task).
- [x] **Step 3 (verify):** Playwright 1440: click thẻ từng loại → drawer mở thẳng (không popover), header màu theo loại đẹp, đúng trường; ESC/backdrop đóng; "+N khác" → click mục → drawer. Screenshot 3 loại.

> Responsive vẫn HOÃN.

### Task 20: Thu nhỏ font + nén gọn drawer chi tiết
- [x] **Step 1:** Giảm cỡ chữ trong drawer (tiêu đề header, nhãn, giá trị, tiêu đề khối, badge) 1-2px; giảm padding/margin/gap các khối, header banner mỏng hơn, khoảng cách nhãn–giá trị chặt hơn — bố cục nhỏ gọn, tối ưu không gian, vẫn dễ đọc & giữ phân cấp.
- [x] **Step 2 (verify):** Playwright 1440: drawer 3 loại gọn hơn, font nhỏ hơn, không vỡ layout, vẫn đủ trường. Screenshot.

> Responsive vẫn HOÃN.

### Task 21: Filter "Loại meeting" (chỉ hiện khi chọn Meeting)
- [x] **Step 1:** Thêm dropdown "Loại meeting" trong header calendar, CHỈ hiện khi loại đang chọn = Meeting (chip/state); loại khác → ẩn. Options = "Tất cả" + các `loaiMeeting` distinct từ TICKETS (type=meeting).
- [x] **Step 2:** Lọc: khi Meeting + chọn 1 Loại meeting → chỉ meeting có loaiMeeting đó; đồng bộ applyFilters + summary. Đổi loại khác/Làm mới → ẩn + reset.
- [x] **Step 3 (verify):** Playwright 1440: chọn chip Meeting → hiện "Loại meeting" đủ option; chọn 1 loại → lịch/summary lọc đúng; đổi sang Công tác/Task → ẩn. Screenshot.

> Responsive vẫn HOÃN.

## Phase 12 — Phiếu kéo dài nhiều ngày (2026-08-08)

### Task 22: Multi-day tickets (data + render Tháng thanh trải + Tuần dải cả ngày)
- [x] **Step 1:** Data: thêm `endDate` cho TICKETS; thêm vài phiếu nhiều ngày mỗi loại (công tác đi công tác 2-4 ngày, meeting workshop 2 ngày, task kéo dài nhiều ngày), có ≥1 phiếu **vắt qua ranh giới tuần** (CN→T2). Tuân rule thời gian (tương lai không Hoàn thành/Quá hạn — xét theo endDate).
- [x] **Step 2:** View Tháng: render phiếu nhiều ngày thành **thanh trải** qua các ô, cắt theo tuần, dùng **lane** cố định + spacer để thẳng hàng liền mạch; bo trái ngày đầu / bo phải ngày cuối; icon+tiêu đề(+badge) ở ô đầu đoạn. Sự kiện 1 ngày giữ dưới lane.
- [x] **Step 3:** View Tuần: phiếu nhiều ngày = thanh span cột trong dải "Cả ngày".
- [x] **Step 4:** Drawer/summary/popup ngày: khoảng "Từ dd/MM – dd/MM"; đếm 1 lần/phiếu; "+N khác" và filter vẫn đúng với phiếu nhiều ngày.
- [x] **Step 5 (verify):** Playwright 1440: thanh nhiều ngày liền mạch (kể cả vắt tuần) ở Tháng; Tuần span cột; click mở drawer đúng khoảng ngày; filter/summary ổn. Screenshot Tháng + Tuần.

> Responsive vẫn HOÃN.

### Task 23: Sửa multi-day (dưới số ngày) + ngưỡng "+N khác" >3 + nền transparent
- [x] **Step 1:** View Tháng: đưa lane multi-day XUỐNG DƯỚI hàng số ngày (số ngày ở đỉnh ô; lane + single-day nằm dưới). Vẫn thẳng hàng liền mạch qua ô.
- [x] **Step 2:** "+N khác" chỉ hiện khi tổng đối tượng của ngày (multi-day phủ ngày + single-day) **> 3**; ≤3 hiện hết. Sửa đếm để multi-day 1-2 thanh không làm gộp sớm.
- [x] **Step 3:** Nền thẻ/thanh để **trong suốt hoặc tint rất nhạt** (alpha thấp), giữ nhận diện bằng viền trái màu loại + icon tròn + màu chữ — tránh nền đặc gây chói. Áp cho thẻ 1 ngày + thanh multi-day (Tháng + Tuần).
- [x] **Step 4 (verify):** Playwright 1440: multi-day nằm dưới số ngày; ô ≤3 không có "+N khác"; ô >3 mới gộp; nền dịu không chói. Screenshot Tháng + Tuần.

> Responsive vẫn HOÃN.

### Task 24: Rõ border chia ngày trong lịch
- [x] **Step 1:** Tăng độ rõ đường kẻ chia ô ngày (dọc giữa các ngày + ngang giữa các tuần) view Tháng: màu đậm hơn (vd `#dfe4ea`/`#d6dde6`), đủ tương phản, đều. Đảm bảo nhất quán qua 3 lớp (số ngày/lane/single-day) để MỖI CỘT NGÀY là 1 khối viền liền từ trên xuống (không đứt đoạn giữa các lớp). Viền ngoài lưới gọn.
- [x] **Step 2:** View Tuần: đường chia cột ngày + dòng giờ cũng rõ tương ứng.
- [x] **Step 3 (verify):** Playwright 1440: ô ngày phân tách rõ ràng, cột liền mạch qua 3 lớp, không lệch. Screenshot Tháng + Tuần.

> Responsive vẫn HOÃN.

## Phase 13 — Bản biến thể CHỈ-MEETING (2026-08-08)

> File riêng: `ke-hoach-phat-trien-thi-truong-mockup-meeting.html` (clone từ bản gốc). Bản gốc 3 loại GIỮ NGUYÊN.

### Task 25: Rút gọn bản clone về chỉ-Meeting
- [x] **Step 1:** Data: chỉ giữ TICKETS type='meeting' (bỏ công tác + task). Giữ meeting multi-day (workshop).
- [x] **Step 2:** Bỏ 3 chip loại + legend loại + filter "Loại phiếu"/logic type (mặc định luôn meeting). Tiêu đề/subtitle phản ánh Meeting.
- [x] **Step 3:** Filter header luôn hiện: **Thị trường + Loại meeting + Trạng thái** (Trạng thái = bộ meeting: Lên lịch/Đã chốt/Hoàn thành/Huỷ, cố định). Lọc thật.
- [x] **Step 4:** Summary: luôn là **stat-card Meeting** (Số Meeting + pills 4 trạng thái), bỏ chế độ 3 box. Màu indigo, icon meeting.
- [x] **Step 5 (verify):** Playwright 1440 trên file -meeting.html: chỉ meeting, filter chạy, summary meeting, drawer meeting, multi-day workshop ok. Screenshot.

> Responsive vẫn HOÃN.

### Task 26: Hiện Tên Khách hàng trên thẻ lịch (cả 2 file)
- [x] **Step 1:** Thẻ single-day (Tháng + Tuần): thêm dòng **Tên khách hàng** (nhỏ, muted, ellipsis) cho phiếu có `khachHang` (Meeting + Phiếu công tác); Task không có → bỏ qua. Vị trí: dưới tiêu đề, trước dòng thời gian+badge. Giữ de-bold/gọn.
- [x] **Step 2:** Thanh multi-day: hiện tên KH nối sau tiêu đề nếu còn chỗ (hoặc bỏ qua nếu chật) — ưu tiên không tràn.
- [x] **Step 3:** Áp cho CẢ 2 file: `...-mockup.html` và `...-mockup-meeting.html`.
- [x] **Step 4 (verify):** Playwright 1440 cả 2 file: thẻ meeting/công tác hiện tên KH; task không có; không tràn/không vỡ. Screenshot.

> Responsive vẫn HOÃN.

### Task 27: Đổi màu Meeting tím → xanh ngọc — CHỈ bản chỉ-Meeting (bản gốc GIỮ tím)
- [x] **Step 1:** Bản `-meeting.html`: Meeting `#4f46e5`/`#3730a3` (tím) → **xanh ngọc `#06b6d4`/`#0e7490`** (+ rgba tint) ở mọi nơi (thẻ/multi-day/icon/summary/drawer/link).
- [x] **Step 2:** BẢN GỐC `...-mockup.html` GIỮ NGUYÊN TÍM — subagent lỡ đổi cả 2, đã revert file gốc về indigo bằng đảo hex; công tác teal-green + task cam không đổi.
- [x] **Step 3 (verify):** Playwright 1440: bản gốc meeting=tím; bản meeting=xanh ngọc. Screenshot cả 2.

> Responsive vẫn HOÃN.

### Task 28: Border ngày hôm nay nổi bật (chỉ file meeting) — ĐÃ REVERT (user thấy xấu)
- [x] ~~Viền cam `#f97316` bao quanh cột hôm nay~~ → user thấy XẤU → **đã revert toàn bộ** về thiết kế gốc (nền phớt teal + vạch accent teal 2px đỉnh + vòng tròn số gradient). grep sạch `#f97316`, số dòng khớp trước Task 28. Verify Playwright: ô hôm nay như cũ, không còn cam. Bản gốc không đụng.

> Responsive vẫn HOÃN.

## Phase 14 — Bản meeting: 2 tab (Lịch + Theo thị trường) (2026-08-08)

### Task 29: Thêm 2 tab cho bản chỉ-Meeting
- [x] **Step 1:** Thêm tab switcher [📅 Lịch meeting] [🗂 Meeting theo thị trường] (dưới summary stat-card). Tab 1 = toàn bộ calendar hiện tại (bọc vào container tab-1). Summary stat-card giữ chung trên đỉnh.
- [x] **Step 2:** Data: thêm field `ketQua` cho các meeting (kết quả thực tế theo trạng thái); thêm vài meeting để cây có chiều sâu (1 thị trường ≥2 KH, 1 KH ≥2 meeting).
- [x] **Step 3:** Tab 2 "Meeting theo thị trường" — accordion phân cấp: **Thị trường** (L1, header + đếm) ▸ **Khách hàng** (L2, header + đếm) ▸ **các cuộc meeting** (L3 row: ngày + tiêu đề + badge trạng thái, click → drawer) ▸ **Kết quả** (L4 leaf: dòng "Kết quả: ..." dưới mỗi meeting). Style đồng bộ xanh ngọc, thụt cấp rõ.
- [x] **Step 4:** Chuyển tab mượt; tab 2 render từ tập meeting (có thể theo filter hiện hành hoặc toàn bộ — ưu tiên đơn giản, đúng số).
- [x] **Step 5 (verify):** Playwright 1440 file -meeting: 2 tab chuyển được; tab 2 cây Thị trường▸KH▸meeting▸kết quả đúng, click meeting → drawer. Screenshot 2 tab.

> Responsive vẫn HOÃN.

### Task 30: Tab 2 "Meeting theo thị trường" → dạng BẢNG (theo mẫu Excel)
- [x] **Step 1:** Thay cây accordion tab 2 bằng BẢNG có **header 2 tầng gộp nhóm** như ảnh mẫu; header navy chữ trắng + sub-header nhạt. Bảng scroll ngang trong container riêng (body không tràn).
- [x] **Step 2:** Mỗi **cuộc meeting = 1 dòng**. Ô GỘP (rowspan): **Thị trường** (gộp theo thị trường), **Khách hàng + Người liên hệ + SĐT/Email** (gộp theo khách hàng). Cột theo meeting: **Ngày · Nội dung (tiêu đề + loại meeting) · Trạng thái (chấm màu + nhãn) · Kết quả/Ghi chú (ketQua) · Người thực hiện**. STT chạy theo dòng.
- [x] **Step 3:** Nhóm cột: "THÔNG TIN KHÁCH HÀNG" (KH/Liên hệ/SĐT) + "LỊCH SỬ LÀM VIỆC / HOẠT ĐỘNG" (Ngày/Nội dung/Người thực hiện) + Trạng thái + Kết quả. Màu chấm trạng thái theo statusColor. Click dòng → drawer.
- [x] **Step 4 (verify):** Playwright 1440 file -meeting tab 2: bảng gộp ô đúng (thị trường/KH merge), header 2 tầng, chấm trạng thái, click dòng → drawer; không tràn ngang. Screenshot.

> Responsive vẫn HOÃN.

### Task 31: Bảng tab 2 — đổi cột theo mẫu mới (meeting-centric)
- [x] **Step 1:** Đổi cột bảng tab 2 theo ảnh mẫu mới. Header 2 tầng gộp nhóm: `Thị trường` (rowspan) · **Meeting**(Tên meeting/Loại meeting/Thời gian/Địa điểm) · `Người chủ trì` · **Thành phần tham gia**(Khách hàng/Thành phần công ty/Thành phần bên KH) · **Kết quả meeting**(Trạng thái/Biên bản họp - Lý do huỷ). BỎ STT, Người liên hệ, SĐT/Email, Lịch sử làm việc, Người thực hiện.
- [x] **Step 2:** Mỗi meeting = 1 dòng; CHỈ gộp rowspan cột Thị trường (theo thị trường). Data: Thời gian=ngày(+giờ, multi-day→khoảng); Địa điểm=diaDiem / "Trực tuyến"+link nếu online; Người chủ trì (thêm field `nguoiChuTri`, mặc định Nguyễn Văn A); Thành phần công ty=thanhPhanCty, Thành phần bên KH=thanhPhanKH; Trạng thái=chấm màu+nhãn; Biên bản họp/Lý do huỷ=ketQua. Giữ nhóm "Khác/Nội bộ".
- [x] **Step 3:** Click dòng → drawer. Giữ header navy 2 tầng + viền ô + scroll ngang.
- [x] **Step 4 (verify):** Playwright 1440: cột đúng mẫu mới, gộp Thị trường, thành phần tham gia + biên bản/lý do huỷ hiển thị; click → drawer. Screenshot.

> Responsive vẫn HOÃN.

### Task 32: Bảng tab 2 — 6 chỉnh sửa (chỉ file meeting)
- [x] **1. Header đồng nhất màu:** 2 hàng header bảng cùng màu navy (hiện hàng trên sai màu).
- [x] **2. Thị trường = tỉnh/thành phố:** đổi MARKETS thành tỉnh/thành (Hà Nội, TP.HCM, Phú Thọ, Đà Nẵng, Hải Phòng...), bỏ vùng miền (Miền Bắc/Trung/Nam); reassign marketId các meeting. Tab 2 KHÔNG hiển thị meeting nội bộ (marketId null) + bỏ nhóm "Khác/Nội bộ".
- [x] **3. Click:** ở tab 2 chỉ click **Tên meeting** (link) mới mở drawer (bỏ click cả dòng).
- [x] **4. Biên bản họp:** meeting "Hoàn thành" → nút **"Xem biên bản"** → popup biên bản theo mẫu thật (bảng: STT/Nội dung-Vấn đề trao đổi/Phương án xử lý/Người đề xuất/Người thực hiện/Hạn dự kiến + Kết luận cuộc họp; nút In/Excel tĩnh). Huỷ → lý do huỷ; khác → "Chưa lập biên bản"/"—". Thêm mock `bienBan{rows[],ketLuan}` cho meeting hoàn thành.
- [x] **5. Trạng thái = badge:** cột trạng thái dạng badge/pill (nền tint + chữ màu + chấm), kiểu app thật.
- [x] **6. Summary thêm thống kê theo thị trường:** dải summary trên thêm breakdown số meeting theo tỉnh/thành.
- [x] **7 (verify):** Playwright 1440: header đồng màu; thị trường là tỉnh/thành, không nội bộ; click tên→drawer; Hoàn thành có "Xem biên bản"→popup đúng mẫu; trạng thái badge; summary có thống kê theo thị trường. Screenshot.

> Responsive vẫn HOÃN.

### Task 33: 5 tinh chỉnh bản meeting
- [x] **1. Summary 2 nhóm cùng row:** chia rõ "Theo trạng thái" + "Theo thị trường" (2 nhóm có nhãn), đặt CÙNG 1 HÀNG (cạnh hero) để tiết kiệm chiều cao.
- [x] **2. Header bảng tab2 = màu header calendar:** đổi header bảng tab 2 dùng cùng màu/style header lịch (teal/cyan gradient) cho đồng bộ (bỏ navy).
- [x] **3. Thêm demo meeting Hoàn thành:** thêm 2-3 meeting quá khứ (≤08/08/2026) trạng thái Hoàn thành + có thị trường (tỉnh/thành) + `bienBan` → nhiều nút "Xem biên bản".
- [x] **4. Thành phần Cty/KH hiển thị tốt hơn:** danh sách người tham gia dạng chip avatar (initials tròn + tên), wrap, dư → "+N".
- [x] **5. Drawer chi tiết: font nhỏ hơn, hạn chế bold, label KHÔNG uppercase** (đổi tiêu đề khối uppercase→thường, giảm weight, giảm cỡ chữ).
- [x] **6 (verify):** Playwright 1440: summary 2 nhóm 1 hàng; header bảng đồng màu lịch; nhiều "Xem biên bản"; chip avatar thành phần; drawer chữ nhỏ/không bold/không uppercase. Screenshot.

> Responsive vẫn HOÃN.

### Task 34: Thành phần (avatar/chức vụ) + Xem lịch sử meeting (bản meeting)
- [x] **1.** Thành phần công ty: chip **avatar** (initials tròn) + tên.
- [x] **2.** Thành phần khách hàng: hiển thị **chức vụ** đi kèm tên (thêm data chức vụ cho thanhPhanKH).
- [x] **3.** Cột Khách hàng: thêm nút **"Xem lịch sử meeting"** → popup liệt kê tất cả meeting với KH đó (Ngày · Tên meeting · Loại · Trạng thái badge · Kết quả).
- [x] **4 (verify):** Playwright 1440 tab2: công ty có avatar; KH có chức vụ; nút Xem lịch sử → popup đúng KH. Screenshot.

> Responsive vẫn HOÃN.

## Phase 15 — Bản meeting: hoàn thiện tab Thị trường + tab "Công việc của tôi" + đổi định vị màn (2026-08-10)

> Chỉ tác động file `ke-hoach-phat-trien-thi-truong-mockup-meeting.html`. Verify Playwright qua `python3 -m http.server 8777`. Có bản copy `quan_ly_cong_viec_ca_nhan.html` (đồng nội dung, tên khớp màn mới).

### Task 35: Popup "Xem lịch sử meeting" — sort + nhân sự + header + biên bản
- [x] Xếp lịch sử **mới → cũ** (sort giảm dần theo ngày).
- [x] Bổ sung cột nhân sự tham gia: **Người chủ trì / Thành phần công ty / Thành phần bên KH** (tái dùng chip avatar).
- [x] Header bảng popup dùng **background teal dùng chung** (giống `.market-table thead th`), bỏ nền navy.
- [x] Thêm nút **"Xem biên bản"** cột cuối (mở popup biên bản chồng lên, z-index cao hơn, ESC/scroll xử lý đúng).

### Task 36: Bảng tab Thị trường — header 1 cấp + cột Phiếu công tác/Chấm công
- [x] Bỏ group header 2 tầng → **header 1 cấp**.
- [x] Thêm cột **"Phiếu công tác / Lịch sử chấm công"** (1 cột gộp, ở cuối): chip mã phiếu + nút mở popup chấm công GPS (thời gian + vị trí + link Google Maps). Popup **tab theo từng người**; bỏ cột "Loại chấm công"; bỏ card thông tin đầu popup.
- [x] Tăng tương phản màu **hover row**.

### Task 37: Bộ lọc + Xuất Excel + Lọc thời gian (tab Thị trường)
- [x] Bộ lọc **Thị trường / Trạng thái / Loại meeting** + Xóa lọc (độc lập tab Lịch).
- [x] Nút **Xuất Excel** (kết xuất tập đã lọc ra `.xls`, UTF-8, header + mã dự án).
- [x] Bộ lọc **Kỳ**: Hôm nay / Tuần / Tháng / Quý / Năm / **Tuỳ chọn (Từ–Đến)** — mốc hôm nay 08/08/2026; summary phản ánh khoảng ngày. Loại meeting nội bộ (marketId null) khỏi tập lọc để khớp bảng.

### Task 38: Nút "Thêm nhanh meeting" + panel chi tiết theo trạng thái
- [x] Nút **"Thêm meeting"** nhỏ gọn cuối phải header lịch → popup form quick-add (validate required, thêm vào TICKETS, re-render lịch + bảng).
- [x] Drawer chi tiết **nút theo trạng thái**: Lên lịch → [Sửa][Duyệt]; Đã chốt → [Sửa]; Hoàn thành → [Xem biên bản]; Huỷ → ẩn footer.

### Task 39: KH mới phát triển + cột Dự án TKT
- [x] Đánh dấu **KH mới phát triển** (badge "KH mới" + highlight ô, đồng bộ bảng/drawer/popup lịch sử).
- [x] **Đưa KH mới lên đầu** (nhóm thị trường có KH mới lên trước + trong nhóm KH mới lên trên; áp cả Excel).
- [x] Cột **"Dự án TKT"** — chỉ meeting **Hoàn thành** (chip mã dự án); export có cột này.

### Task 40: Summary tab Thị trường — tổng hợp + dạng lưới text
- [x] Summary thêm nhóm **Tổng hợp**: Số dự án / Số KH mới / Tỷ lệ hoàn thành (chỉ tab Thị trường, qua param `extraStats`).
- [x] Thiết kế lại summary (cả 2 tab meeting) sang **lưới text** (bỏ chip): nhóm cột có tiêu đề + "Nhãn — Giá trị", zero mờ.
- [x] **Chỉ meeting Hoàn thành** mới có phiếu công tác/lịch sử chấm công.
- [x] Đổi tên tab 2 → **"Kết quả meeting theo thị trường"**.

### Task 41: Tab "Công việc của tôi" (My To Do) + đổi định vị màn
- [x] Đổi tên màn → **"Quản lý lịch làm việc cá nhân"** (title + topbar), **topbar nhỏ gọn 1 hàng**.
- [x] Thêm **tab "Công việc của tôi"** làm **tab đầu tiên** (mặc định), `switchTab` nâng 3 tab. Gộp Task/Issue/Cá nhân (mock), stats (Quá hạn/Hôm nay/Tuần này/Cần duyệt), filter (Loại/Vai trò/Trạng thái), mini lịch + danh sách cá nhân.
- [x] **Group + thu gọn/mở rộng đúng màn My To Do thật** (đối chiếu `TodoGroupHeader.vue`/`TodoMainList.vue`): thứ tự Hôm nay→Ngày mai→Tuần này→Tuần sau→Sau đó→Không hạn→**Quá hạn (cuối)**; icon + màu riêng; badge nền màu; mặc định chỉ "Hôm nay" mở; nhóm today/tomorrow/this-week/overdue luôn hiện dù rỗng.
- [x] Tab này **chỉ Task / Issue / Cá nhân** (bỏ Cuộc họp/Phiếu duyệt).

### Task 42: Lịch meeting — màu nền thẻ theo trạng thái
- [x] Thẻ meeting (view Tháng/Tuần + thanh nhiều ngày) đổi **màu nền theo trạng thái**: Lên lịch xám · Đã chốt xanh dương · Hoàn thành xanh lá · Huỷ đỏ (helper `cardStatusStyle` gán `--card-color/--card-bg/--card-border`).

### Task 43: Bảng tab "Kết quả meeting theo thị trường" → 3 cấp Thị trường ▸ Khách hàng ▸ Meeting
- [x] Nâng cột **Khách hàng** thành cấp nhóm (ô gộp `rowspan`), đặt ngay sau cột Thị trường; **bỏ** cột Khách hàng khỏi từng dòng meeting.
- [x] Nhóm meeting **theo khách hàng** trong mỗi thị trường; ô Khách hàng gộp giữ nguyên badge "KH mới" + nút "Xem lịch sử meeting".
- [x] Meeting trong 1 khách hàng sắp xếp **cũ → mới** (ngày tăng dần); KH mới vẫn nổi lên đầu (thị trường + khách hàng có KH mới lên trước).
- [x] Đồng bộ thứ tự nhóm/sort cho **Xuất Excel** (nhóm theo KH, cũ→mới).
- [x] Verify Playwright 1440: header 13 cột (Khách hàng ở vị trí 2), rowspan Thị trường = tổng meeting, rowspan Khách hàng gộp đúng; meeting trong KH cũ→mới (Thành Đạt 01/08→14/08, Thăng Long 08/08→21/08); KH mới nổi đầu; nút "Xem lịch sử meeting" trong ô gộp vẫn mở popup đúng KH.

### Task 44: Cột "Phòng ban" (của người chủ trì) + bộ lọc cascade Công ty ▸ Phòng ban ▸ Người chủ trì
- [x] **Mock data**: thêm `COMPANIES` (2 công ty) + `companyId` cho `DEPARTMENTS`; helper tra cứu người chủ trì → phòng ban → công ty (`getEmployeeByName`/`getHostEmployee`/`getHostDepartment`/`getHostCompanyId`), resolve theo TÊN nên meeting thêm mới từ quick-add vẫn chạy đúng.
- [x] **Bảng**: thêm cột **Phòng ban** ngay SAU cột "Người chủ trì" (header 13 → **14 cột**), giá trị = phòng ban của người chủ trì, `—` nếu không tra được.
- [x] **Bộ lọc cascade** trong toolbar tab: **Công ty → Phòng ban → Người chủ trì** (đặt trước Thị trường). Chọn cấp trên → cấp dưới lọc lại danh sách + reset về "Tất cả"; "Tất cả" ở cấp trên → cấp dưới hiện đủ.
- [x] **Logic lọc**: AND vào `getMarketTabFilteredTickets()` theo người chủ trì (công ty/phòng ban/chính người đó).
- [x] **Xuất Excel**: thêm cột "Phòng ban" đúng vị trí; nút "Xóa lọc" reset cả 3 select mới + dựng lại cascade.
- [x] Verify Playwright 1440: header **14 cột** đúng thứ tự (Phòng ban ngay sau Người chủ trì) · Phòng ban khớp chủ trì (Đỗ Thị F → Kinh doanh dự án, Phạm Thị D → Kinh doanh 2) · cascade: Tất cả 11 dòng → Cty ETEK 9 dòng (còn 2 phòng, 4 NV) → Kinh doanh 2 còn 2 dòng (2 NV) → chủ trì Lê Văn C 0 dòng (empty state) · Xóa lọc trả lại 11 dòng + full option · không lỗi console.
- [x] CSS: `.market-export-btn { margin-left:auto }` — toolbar 7 select xuống 2 hàng, nút "Xuất Excel" vẫn nằm sát phải.
- [ ] **Chờ user chốt**: tên 2 công ty demo (đang tạm `Công ty CP Tân Phát ETEK` = KD1+KD2, `Công ty TNHH Tân Phát Sài Gòn` = KD dự án).

### Task 45: Đổi cấu trúc bảng → dạng OUTLINE (dòng nhóm + STT phân cấp + ẩn/hiện chi tiết)
Theo mẫu ảnh user gửi (2026-08-19): bỏ ô gộp `rowspan`, chuyển sang **dòng nhóm kiểu Excel outline**.
- [x] **Cột**: bỏ 2 cột Thị trường + Khách hàng, thay bằng **STT** (I / 1 / 1.1) + **"Thị trường / KH / Meeting"** (1 cột chung 3 cấp, thụt lề theo cấp). Các cột còn lại giữ nguyên: Thời gian · Địa điểm · Người chủ trì · Phòng ban · Thành phần công ty · Thành phần bên KH · Trạng thái · Loại meeting · Biên bản/Lý do huỷ · Dự án TKT · Phiếu công tác/Chấm công.
- [x] **3 loại dòng**: cấp I = thị trường `Hà Nội (6 meeting)` · cấp 1 = khách hàng `Toyota Hà Đông (2)` · cấp 1.1 = meeting (đổ đủ dữ liệu các cột). Dòng nhóm để trống các cột dữ liệu (giữ lưới ô như mẫu).
- [x] Badge "KH mới" + nút "Xem lịch sử meeting" chuyển lên **dòng nhóm khách hàng**.
- [x] **Ẩn / hiện chi tiết**: nút tổng ở góc phải trên bảng (thu/bung toàn bộ dòng meeting) + **caret trên từng dòng nhóm** (thu/bung riêng 1 thị trường hoặc 1 khách hàng); trạng thái thu/bung giữ nguyên khi đổi bộ lọc.
- [x] **Xuất Excel** bám đúng cấu trúc mới (có STT phân cấp + cột gộp tên, dòng nhóm kèm số đếm).
- [x] Verify Playwright 1440: **13 cột** · 24 dòng = 4 TT + 9 KH + 11 meeting, STT `I,1,1.1,2,2.1,II,…` đúng · thu 1 thị trường (Hà Nội) → 14 dòng, bung lại 24 · thu 1 KH → 23 · nút tổng: 13 dòng (0 meeting) + nhãn đổi "Hiện chi tiết" ↔ 24 dòng · lọc Công ty/Phòng ban/Trạng thái vẫn đúng và đánh lại STT/số đếm · **0 lỗi console**.
- [x] Nhỏ: caret đặt inline trong span tên nhóm (tên KH dài không đẩy caret đứng lẻ dòng); cụm nút "Ẩn chi tiết" + "Xuất Excel" giữ sát phải.
- [x] **User chốt (2026-08-19)**: "Các cột còn lại" trong ảnh mẫu = đúng các cột đang có của báo cáo (không thêm cột mới); thứ tự cột hiện tại (Loại meeting nằm sau Trạng thái) **giữ tạm như vậy**.

### Task 46: Tách báo cáo thành FILE RIÊNG + mặc định chỉ hiện tới cấp Khách hàng
- [x] File mới **`bao-cao-ket-qua-meeting-theo-thi-truong.html`** (self-contained): tiêu đề/topbar = "Báo cáo kết quả meeting theo thị trường", KHÔNG còn dải tab. Bỏ DOM + script của 2 tab kia (My To Do, Lịch meeting), bỏ popup "Thêm nhanh meeting" và `renderFilterOptions()` của toolbar lịch; giữ mock data, drawer chi tiết, 3 popup (Biên bản / Lịch sử meeting / Chấm công GPS). Bảng render ngay khi mở trang.
- [x] **Mặc định thu tới cấp Khách hàng**: mở màn chỉ thấy dòng Thị trường + Khách hàng, nút góc phải để "Hiện chi tiết" mới bung dòng meeting. Cơ chế: `marketDetailHidden` = mặc định chung (khởi tạo `true`) + `MARKET_OUTLINE.customerState[key]` chỉ lưu nhóm user tự bấm caret (ghi đè mặc định); bấm nút tổng = reset ghi đè, đổi mặc định + đổi nhãn nút.
- [x] File cũ `...-mockup-meeting.html` gỡ hẳn tab 3: bỏ nút tab + section `#tab-by-market` + JS bộ lọc/xuất Excel/outline của tab đó → còn **2 tab** (Công việc của tôi · Lịch meeting).
- [x] Verify Playwright 1440 — **file báo cáo**: mở lên 13 dòng (4 TT + 9 KH, 0 meeting) + nhãn "Hiện chi tiết" · caret 1 KH → 14 dòng rồi thu lại 13 · nút tổng → 24 dòng/11 meeting, nhãn "Ẩn chi tiết" · thu 1 thị trường khi đang bung → 20 dòng · drawer + popup Biên bản/Lịch sử/Chấm công mở đúng · **0 lỗi console**.
- [x] Verify Playwright — **file cũ**: chỉ còn 2 tab, lịch (14 thẻ) + My To Do (7 nhóm) chạy bình thường, **0 lỗi console**.
- [ ] Lưu ý: bản copy cũ `quan_ly_cong_viec_ca_nhan.html` (2026-08-10) vẫn còn tab 3 bản cũ — đã LỆCH, chỉ giữ để tham chiếu.

### Task 47: Bỏ "KH mới" · chữ tên meeting · tương phản cấp · data 3 thị trường · summary theo phòng ban
Chỉ sửa file báo cáo `bao-cao-ket-qua-meeting-theo-thi-truong.html`.
- [x] **Bỏ nhận dạng "KH mới phát triển"**: xoá `NEW_CUSTOMERS`/`isNewCustomer()`/`buildKhNewBadgeHtml()` + badge ở dòng khách hàng, drawer, popup lịch sử; bỏ highlight xanh lá; bỏ ưu tiên sắp xếp (KH mới lên đầu, thị trường có KH mới lên đầu) → thị trường theo thứ tự `MARKETS`, khách hàng theo ngày meeting sớm nhất. Chỉ số summary "KH mới" đổi thành **"Khách hàng"** (đếm KH distinct). Dọn hàm chết `buildTableCustomerCellHtml()`, `sortTicketsNewFirst()`.
- [x] **Tên meeting** `font-weight: 400` (bỏ đậm).
- [x] **Tăng tương phản 3 cấp**: Thị trường nền teal đậm `#0e7490` chữ trắng (caret trắng) · Khách hàng nền `#d7f2f7` + viền trái đậm ở cột tên · Meeting nền trắng (hover `#f1fbfd`).
- [x] **Data demo gom về 3 thị trường** (thêm m15–m25, chuyển m01 Phú Thọ → Hà Nội): Hà Nội 5 KH/10 meeting · TP.HCM 3 KH/6 · Đà Nẵng 3 KH/6 = **22 meeting/11 KH**; 2 KH mới trong data (Dược phẩm Nam Việt, Cơ điện Miền Trung); chủ trì trải đều 6 NV của 3 phòng ban.
- [x] **Summary thêm nhóm "Theo phòng ban"** (đếm theo phòng ban của người chủ trì, có mục "Không xác định" khi cần), đặt giữa "Theo trạng thái" và "Theo thị trường".
- [x] Verify Playwright: 36 dòng khi bung (3 TT + 11 KH + 22 meeting) · 0 badge KH mới · `font-weight=400` · nền 3 cấp `rgb(14,116,144)` / `rgb(215,242,247)` / `rgb(255,255,255)` · summary 22 phiếu — Trạng thái 5/8/8/1, Phòng ban KD1=10 KD2=7 KDDA=5, Thị trường HN=10 HCM=6 ĐN=6 · lọc Phòng ban=Kinh doanh 2 → 7 meeting và summary khớp · drawer/lịch sử/biên bản/chấm công mở đúng · **0 lỗi console**.

### Task 48: Xem chi tiết meeting = panel overlay theo mẫu Lịch meeting
- [x] Xác nhận panel chi tiết trong báo cáo **đang dùng đúng drawer của màn Lịch meeting** (`window.openTicketDrawer` — header gradient theo trạng thái + khối Thông tin cuộc họp / Khách hàng & người liên hệ / Mục tiêu / Thành phần tham dự + nút theo trạng thái Sửa·Duyệt·Xem biên bản). Đã giữ nguyên khi tách file ở Task 46.
- [x] Bổ sung cho giống thao tác bên Lịch meeting: **click bất kỳ đâu trên dòng meeting** → mở panel (trước chỉ click đúng tên meeting mới mở); `cursor: pointer` trên dòng meeting.
- [x] Không đụng các nút/link trong dòng: click "Xem biên bản" / "Xem lịch sử meeting" / link họp / dự án vẫn ra popup riêng, KHÔNG mở panel.
- [x] Verify Playwright: click ô "Người chủ trì" của 1 dòng meeting → panel mở đúng meeting · click nút biên bản → popup biên bản mở, panel vẫn đóng · click "Xem lịch sử meeting" → popup lịch sử mở, panel vẫn đóng · **0 lỗi console**.

### Task 49: Chế độ TỔNG HỢP — ẩn cột chi tiết + cột đếm meeting theo phòng ban
- [x] Bảng có **2 bộ cột theo chế độ**: TỔNG HỢP (đang "Ẩn chi tiết") = `STT · Thị trường/Khách hàng/Meeting · <1 cột cho mỗi phòng ban> · Tổng` — **ẩn hết cột chi tiết**; CHI TIẾT = giữ nguyên 13 cột.
- [x] Ô đếm = số meeting của nhóm đó do **người chủ trì thuộc phòng ban ấy** (`countTicketsByDepartment`), tính cho cả dòng Thị trường (rollup) lẫn dòng Khách hàng; ô 0 hiện `—` mờ; cột Tổng tô nền đậm hơn.
- [x] Bung lẻ 1 nhóm bằng caret khi đang ở chế độ tổng hợp → dòng meeting cũng theo bộ cột tổng hợp (1 tại phòng ban của chủ trì, Tổng = 1), không để trống trơn.
- [x] Bảng chế độ tổng hợp bỏ `min-width: 1560px` → không cuộn ngang thừa. Panel chi tiết vẫn mở được từ dòng meeting.
- [x] **Xuất Excel bám chế độ đang xem**: tổng hợp → cột phòng ban + Tổng, chỉ tới cấp khách hàng; chi tiết → như cũ.
- [x] Verify Playwright: header tổng hợp 6 cột / chi tiết 13 cột · Hà Nội `KD1=10, Tổng 10` · TP.HCM `KD2=2, KDDA=4, Tổng 6` · Đà Nẵng `KD2=5, KDDA=1, Tổng 6` (∑ = 22, khớp summary) · dòng meeting bung lẻ = `1.1 | tên | 1 | — | — | 1` · click dòng meeting vẫn mở panel · lọc Phòng ban=Kinh doanh 2 → chỉ còn TP.HCM 2 + Đà Nẵng 5 · **0 lỗi console**.

### Task 50: Fix hover dòng nhóm · dòng TỔNG CỘNG theo phòng ban · nút In (2 chế độ)
- [x] **Fix bug hover**: rule `.market-table__row:hover td` áp cho MỌI dòng → hover dòng Thị trường (nền teal đậm, chữ trắng) bị phủ nền sáng ⇒ chữ trắng trên nền trắng. Đổi thành chỉ áp cho `.market-table__row--meeting`; dòng nhóm hover chỉ đậm/nhạt nhẹ trong đúng tông cấp (thị trường `#0b5f77`, khách hàng `#c9edf4`).
- [x] **Dòng TỔNG CỘNG** (`<tfoot>`) ở chế độ tổng hợp: tổng số meeting của toàn tập đang lọc theo TỪNG phòng ban + cột Tổng (10 · 7 · 5 · 22).
- [x] **Nút "In báo cáo"** cạnh Xuất Excel → popup chọn **In tổng hợp** (tới cấp Khách hàng + số theo phòng ban + dòng Tổng cộng) hoặc **In chi tiết** (đủ 3 cấp + toàn bộ cột). Bản in bám **bộ lọc đang áp dụng** và độc lập với chế độ đang xem trên màn hình.
- [x] Bản in dựng vào `#print-area` (tiêu đề + dòng meta: loại bản in · bộ lọc · ngày in) + `@media print` (A4 ngang, chỉ in `#print-area`, ẩn topbar/bộ lọc/modal/drawer).
- [x] Verify Playwright: hover dòng thị trường giữ `rgb(14,116,144)` + chữ trắng · tfoot `TỔNG CỘNG | 10 | 7 | 5 | 22` · popup in mở/đóng, 2 lựa chọn · bản tổng hợp = 15 dòng (3 TT + 11 KH + tổng cộng), header 6 cột · bản chi tiết = 36 dòng, header 13 cột, dòng meeting đủ dữ liệu (mã dự án/phiếu công tác) · meta in "Bản TỔNG HỢP · Kỳ: tất cả · Ngày in: 08/08/2026" · **0 lỗi console**.

### Task 51: Tổng meeting trên tiêu đề cột phòng ban · hover rõ hơn · gom cụm nút · icon cho mọi button
- [x] **Tiêu đề cột phòng ban kèm TỔNG**: `Kinh doanh 1 / 10 · Kinh doanh 2 / 7 · Kinh doanh dự án / 5 · Tổng / 22` (số đổi theo bộ lọc, khớp dòng TỔNG CỘNG cuối bảng).
- [x] **Hover rõ + đẹp hơn**: dòng meeting nền `#ddf4fa` + vệt accent trái ở ô STT + gạch chân tên meeting; dòng nhóm hover đậm thêm 1 bậc đúng tông cấp (thị trường `#095a70`, khách hàng `#bce7f0`), chữ luôn đọc được.
- [x] **Gom cụm nút**: bọc 3 nút vào `.market-toolbar__actions` (`margin-left:auto` cho cả cụm) → "Ẩn/Hiện chi tiết · In báo cáo · Xuất Excel" nằm cạnh nhau sát phải; trước đây mỗi nút tự `margin-left:auto` nên nút đầu bị đẩy ra giữa hàng.
- [x] **Mọi button đều có icon**: rà toàn file, bổ sung icon cho 4 nút còn thiếu — drawer "Sửa" (bút), drawer "Duyệt" (tick), popup in "Huỷ" (X), popup in "In" (máy in). Các nút còn lại đã có sẵn icon.
- [x] Verify Playwright: header 6 cột kèm số 10/7/5/22 · hover dòng thị trường giữ nền teal + chữ trắng, hover dòng meeting hiện nền nhạt + accent + gạch chân · 3 nút cùng hàng (top=210) sát phải · 8/8 button kiểm tra đều có `<svg>` · **0 lỗi console**.

### Task 52: Bỏ số ở tiêu đề · dời dòng TỔNG CỘNG lên đầu · sticky tiêu đề + dòng tổng
- [x] Bỏ số tổng khỏi tiêu đề cột phòng ban (Task 51) — tiêu đề chỉ còn tên phòng.
- [x] Dòng **TỔNG CỘNG** chuyển từ `<tfoot>` cuối bảng lên **ngay dưới hàng tiêu đề** (đặt trong `<thead>`).
- [x] **Sticky khi cuộn**: `.market-table-wrap` có `max-height: calc(100vh - 230px)` + `overflow:auto` (sticky cần vùng cuộn thật); hàng tiêu đề `position:sticky; top:0`; dòng TỔNG CỘNG sticky với `top` gán ĐỘNG bằng JS = chiều cao thật của hàng tiêu đề (đo lại mỗi lần render vì đổi theo chế độ/độ rộng).
- [x] Verify Playwright: tiêu đề không còn số · dòng tổng nằm trong `<thead>`, `top: 37.5px`, không còn `<tfoot>` · chế độ CHI TIẾT cuộn 400px → tiêu đề dính (thTop 279 ≈ wrapTop 278) · chế độ TỔNG HỢP bung hết (16 dòng) cuộn → tiêu đề dính 279 + dòng tổng dính 316 (`TỔNG CỘNG 10 · 7 · 5 · 22`) · **0 lỗi console**.

### Task 53: Thiết kế lại dải TỔNG HỢP cho dễ đọc
Trước: 1 hàng ngang ~16 con số text (Tổng hợp / Trạng thái / Phòng ban / Thị trường) — dày, khó quét.
- [x] **Tầng 1 — 4 ô KPI** có icon + số lớn + dòng phụ: `Tổng meeting 22 phiếu (kỳ đang lọc)` · `Hoàn thành 8 (36% tổng số)` · `Khách hàng 11` · `Dự án TKT 8`.
- [x] **Tầng 2 — 3 khối phân bổ**: *Trạng thái* = thanh xếp chồng (khe 2px, màu semantic của trạng thái) + chú giải 2 cột (nhãn · số · %); *Phòng ban (người chủ trì)* và *Thị trường* = thanh ngang so sánh, **cùng 1 tông teal** (độ lớn, không phải danh tính), sắp xếp giảm dần.
- [x] Thị trường **chỉ liệt kê nơi có meeting**, phần 0 gom 1 dòng ghi chú "Chưa phát sinh: …" (trước hiện 3 mục số 0 gây nhiễu).
- [x] Nguyên tắc trình bày: mọi mục đều có **nhãn + số** (không mã hoá bằng màu đơn thuần), chữ dùng màu ink, màu chỉ ở chấm/thanh; hover thanh/mảnh có tooltip `nhãn: số (…%)`.
- [x] `countTicketsByDepartment()` chuyển lên phạm vi **global** (cả dải tổng hợp lẫn bảng/bản in dùng chung) — sửa lỗi `ReferenceError` khi render summary.
- [x] Chiều cao khung bảng chuyển sang tính **động** (`fitMarketTableHeight()` + bind `resize`) thay cho `calc()` cứng, vì dải tổng hợp cao thấp tuỳ nội dung → sticky tiêu đề/dòng tổng vẫn đúng.
- [x] Fix `.rsum-bar__track/__fill` là `<span>` inline nên `width %` không ăn (thanh dài 0px) → `display: block`.
- [x] Verify Playwright: tỷ lệ thanh đúng (KD1 100% · KD2 70% · KDDA 50%; HN 100% · HCM 60% · ĐN 60%) · mảnh trạng thái 22.7/36.4/36.4/4.5% · lọc Phòng ban = Kinh doanh dự án → KPI 5/2/3/2, thị trường còn TP.HCM 4 · Đà Nẵng 1, ghi chú "Chưa phát sinh: Hà Nội · Phú Thọ · Hải Phòng · Bắc Ninh" · **0 lỗi console**.

### Task 54: Bộ lọc lên trên dải tổng hợp + nút ẩn/hiện tổng hợp
- [x] Đảo thứ tự trong `#tab-by-market`: **toolbar (bộ lọc + cụm nút) → dải tổng hợp → bảng**.
- [x] Thêm nút **"Ẩn tổng hợp / Hiện tổng hợp"** (icon mắt ↔ mắt-gạch) ở đầu cụm nút; ẩn xong gọi `fitMarketTableHeight()` để bảng ăn hết chỗ trống.
- [x] Verify Playwright: thứ tự DOM `market-toolbar → type-summary-bar-market → market-tree-panel` · ẩn → `display:none`, nhãn "Hiện tổng hợp", khung bảng nới từ **332px → 587px**; hiện lại → về 332px, nhãn "Ẩn tổng hợp" · **0 lỗi console**.

### Task 55: Cân bằng data demo theo phòng ban
Trước: meeting dồn gần hết vào 1 phòng ở mỗi thị trường (Hà Nội 10/10 = Kinh doanh 1).
- [x] Thêm **8 meeting** (m26–m33): Hà Nội +4 (2 Kinh doanh 2, 2 Kinh doanh dự án) · TP.HCM +2 (Kinh doanh 1) · Đà Nẵng +2 (Kinh doanh 1).
- [x] Đổi chủ trì 3 meeting Hà Nội cũ để trải đều: m12 → Lê Văn C (KD2) · m10 → Hoàng Văn E (KD dự án) · m17 → Phạm Thị D (KD2); đồng bộ `createdBy` + thêm người chủ trì vào Thành phần công ty.
- [x] Kết quả: **30 meeting / 11 khách hàng**, phòng ban **Kinh doanh 1 = 11 · Kinh doanh 2 = 11 · Kinh doanh dự án = 8**; mỗi thị trường đều có đủ 3 phòng — Hà Nội 14 (7/4/3) · TP.HCM 8 (2/2/4) · Đà Nẵng 8 (2/5/1); nhiều khách hàng có meeting của 2–3 phòng khác nhau (vd Thành Đạt 1/1/1).
- [x] Verify Playwright: dòng TỔNG CỘNG `11 | 11 | 8 | 30` khớp KPI + thanh phân bổ · chế độ chi tiết 44 dòng (3 TT + 11 KH + 30 meeting) · **0 lỗi console**.

### Task 56: Chế độ tổng hợp — ô phòng ban bằng 1 hiển thị dấu tick
- [x] Ô cột phòng ban ở chế độ tổng hợp: `0` → `—` mờ · **`1` → dấu tick** · `>1` → số. Tick đổi màu theo cấp dòng (thị trường: trắng · khách hàng/meeting: teal đậm); mọi ô có `title="<Phòng ban>: N meeting"` để tra số chính xác khi hover.
- [x] Dòng **TỔNG CỘNG** và cột **Tổng** vẫn giữ SỐ (là dòng/cột thống kê).
- [x] Xuất Excel + bản in không đổi (vẫn xuất số để tính toán được).
- [x] Verify Playwright: dòng KH "Nội thất Hoàng Gia" = `✓ · ✓ · — · 2` · dòng meeting bung lẻ = `✓ · — · — · 1` · dòng thị trường Hà Nội giữ số `7 · 4 · 3 · 14` · TỔNG CỘNG `11 · 11 · 8 · 30` · tooltip "Kinh doanh 1: 1 meeting" · **0 lỗi console**.

### Task 57: Sắp xếp theo cột (từ cột "Thời gian" sang phải)
- [x] Mọi cột DỮ LIỆU đều sắp xếp được — chi tiết: 11 cột (Thời gian → Phiếu công tác); tổng hợp: các cột phòng ban + Tổng. Hai cột STT và "Thị trường/Khách hàng/Meeting" không sắp.
- [x] Bảng là outline 3 cấp nên **sắp xếp giữ nguyên cấu trúc nhóm**: chế độ CHI TIẾT sắp các meeting trong từng khách hàng; chế độ TỔNG HỢP (cột là số đếm của cả nhóm) sắp các khách hàng trong từng thị trường **và** sắp luôn thứ tự thị trường.
- [x] Bấm lần 1 tăng dần → lần 2 giảm dần → lần 3 trả về mặc định; tiêu đề cột đang sắp được tô đậm + mũi tên chỉ chiều; hover hiện mũi tên mờ.
- [x] Cột "Thời gian" so sánh theo mốc thật (`date + timeStart`), các cột còn lại so sánh text tiếng Việt (`localeCompare('vi')`), cột số so sánh số.
- [x] Đổi chế độ tổng hợp/chi tiết → bỏ sắp xếp đang áp (2 chế độ khác bộ cột). Xuất Excel bám đúng thứ tự đang xem.
- [x] Verify Playwright: tổng hợp sắp theo "Tổng" tăng → TP.HCM(8)·Đà Nẵng(8)·Hà Nội(14), giảm → ngược lại, lần 3 về mặc định · chi tiết sắp "Thời gian" giảm → 05/08 lên trước 29/07 · cột "Trạng thái" nhận class `is-sorted` · **0 lỗi console**.

### Task 58: Tick nhỏ + chỉ ở dòng meeting · lọc phòng ban thì chỉ hiện cột phòng đó
- [x] Icon tick nhỏ lại 15px → **12px**.
- [x] Tick **chỉ hiện ở dòng MEETING** (đánh dấu phòng của người chủ trì); dòng Khách hàng / Thị trường / TỔNG CỘNG luôn hiện **số lượng** meeting.
- [x] **Cột phòng ban bám bộ lọc** (`getVisibleDepartments()`, để ở phạm vi global): lọc 1 Phòng ban → chỉ cột của phòng đó · lọc 1 Công ty → chỉ các phòng thuộc công ty · không lọc → đủ 3 cột. Áp dụng đồng bộ cho **bảng · dải tổng hợp · Xuất Excel · bản in**; việc đếm vẫn chạy trên toàn bộ phòng ban, chỉ phần hiển thị thu hẹp.
- [x] Đổi bộ lọc Công ty/Phòng ban → bỏ sắp xếp đang áp (bộ cột đổi theo), chỉ số cột sắp xếp tính lại theo danh sách phòng đang hiển thị.
- [x] Verify Playwright: dòng KH "Nội thất Hoàng Gia" = `1 · 1 · — · 2` (số), dòng meeting = `✓ · — · — · 1`, icon đo được 12×12 · lọc Phòng ban = Kinh doanh 2 → header còn `Kinh doanh 2 · Tổng`, Hà Nội 4 meeting, TỔNG CỘNG `11 · 11`, dải tổng hợp cũng chỉ còn 1 phòng · lọc Công ty = Tân Phát ETEK → 2 cột phòng · Xóa lọc → về 3 cột · **0 lỗi console**.

### Task 59: Drill-down từ dòng TỔNG CỘNG → popup danh sách meeting (có In / Xuất Excel)
- [x] Mỗi con số ở dòng **TỔNG CỘNG** thành nút bấm (gạch chân chấm + hover): cột phòng ban → danh sách meeting **do phòng đó chủ trì**; cột **Tổng** → toàn bộ meeting. Danh sách bám **bộ lọc đang áp dụng**.
- [x] Popup rộng (`min(1100px, 94vw)`) — bảng 8 cột: STT · Thị trường · Khách hàng · Tên meeting · Thời gian · Người chủ trì · Phòng ban · Trạng thái; sắp theo Thị trường → Khách hàng → ngày; header dính khi cuộn trong popup.
- [x] Popup có **2 nút riêng**: "In danh sách" (dựng `#print-area` + `window.print()`, tiêu đề + số lượng + bộ lọc + ngày in) và "Xuất Excel" (file `Danh-sach-meeting-<phòng>.xls`).
- [x] Tách `downloadXls(headers, rows, filename)` thành hàm dùng chung cho export báo cáo chính và export popup.
- [x] Verify Playwright: ô drill = `dep1=11 · dep2=11 · dep3=8 · __all__=30` · bấm Tổng → popup "Tất cả phòng ban (30)", 30 dòng, width 1100px · In danh sách → `#print-area` 30 dòng, meta "30 meeting · Kỳ: tất cả · Ngày in: 08/08/2026" · bấm Kinh doanh dự án → 8 dòng, dòng đầu đúng meeting của Hoàng Văn E · **0 lỗi console**.

> Responsive vẫn HOÃN.

## Phase 16 — File MỚI: "Báo cáo tổng hợp nhu cầu khách hàng" (2026-08-20)

> File độc lập `bao-cao-tong-hop-nhu-cau-khach-hang.html` (cùng folder). **Layout** bám ảnh Excel user gửi (`Báo cáo tổng hợp nhu cầu khách hàng`), **style** tái dùng nguyên bộ token + component của `bao-cao-ket-qua-meeting-theo-thi-truong.html` (navy+teal, `.market-table` outline, `.market-toolbar`, `.rsum-*`, `.minutes-modal`). Self-contained, verify Playwright.
>
> **Chốt với user (2026-08-20):** cột Trạng thái = **trạng thái NHU CẦU KH** · ô "TẠO MỚI" = **nút bấm** mở popup tạo dự án TKT · có KPI + thu/bung outline + TỔNG CỘNG + Xuất Excel + In báo cáo · **KHÔNG** làm drawer chi tiết (tên meeting chỉ là link tĩnh).

### Task 60: Scaffold + topbar + toolbar 7 bộ lọc
- [x] Tạo file, copy design tokens + reset + topbar + `.page-body` từ file báo cáo meeting; `<title>`/topbar = "Báo cáo tổng hợp nhu cầu khách hàng".
- [x] Mock data: 4 lĩnh vực KD (Gara · Năng lượng · Môi trường · Đào tạo - Dạy nghề) × 3 thị trường (Hà Nội · TP.HCM · Đà Nẵng) × ~16 nhu cầu / ~11 KH; nhân sự/phòng ban/công ty đồng bộ file báo cáo meeting (Kinh doanh 1 · Kinh doanh 2 · Kinh doanh dự án; Tân Phát ETEK · Tân Phát Sài Gòn). Giữ nhóm rỗng cho giống ảnh.
- [x] Toolbar: **Kỳ xem** (Tất cả/Hôm nay/Tuần/Tháng/Quý/Năm/Tuỳ chọn → Từ–Đến; lọc theo thời gian bắt đầu họp) · **Lĩnh vực KD** (chọn NHIỀU, dropdown checkbox) · **Khách hàng** · cascade **Công ty ▸ Phòng ban ▸ Bộ phận ▸ Kinh doanh chủ trì** · nút Xoá lọc; cụm nút phải: Ẩn tổng hợp · Hiện/Ẩn chi tiết · In báo cáo · Xuất Excel.

### Task 61: Dải KPI tổng hợp
- [x] 4 ô KPI: Tổng nhu cầu · Tổng giá trị đầu tư dự kiến · Số khách hàng · Chưa có dự án TKT (kèm %).
- [x] 2 khối phân bổ thanh ngang: theo **Lĩnh vực KD** và theo **Thị trường** (chỉ liệt kê nơi có dữ liệu).
- [x] Nút "Ẩn/Hiện tổng hợp" hoạt động; KPI cập nhật theo bộ lọc.

### Task 62: Bảng chính — outline 3 cấp + TỔNG CỘNG + trạng thái
- [x] 10 cột đúng ảnh: STT · Lĩnh vực KD/TT/KH · Tổng giá trị đầu tư dự kiến · Thời gian dự kiến triển khai · Nhu cầu dịch vụ sửa chữa · Meeting thu thập nhu cầu · Kinh doanh chủ trì · Phòng · Trạng thái · Dự án TKT.
- [x] Outline `I` Lĩnh vực KD → `1` Thị trường → `1.1` Khách hàng; caret thu/bung từng nhóm + nút "Hiện/Ẩn chi tiết" toàn bảng.
- [x] Sticky header + dòng **TỔNG CỘNG** ngay dưới header (tổng giá trị đầu tư + đếm nhu cầu).
- [x] Badge trạng thái nhu cầu: Mới ghi nhận (xám) · Đang theo dõi (xanh dương) · Đã chốt (xanh lá) · Không tiếp tục (đỏ).
- [x] Dòng **chưa có dự án TKT → tô vàng** như Excel; tên meeting hiển thị link gạch chân (tĩnh).

### Task 63: Nút "+ TẠO MỚI" → popup tạo dự án TKT
- [x] Ô Dự án TKT: chưa có → nút `+ TẠO MỚI`; đã có → mã `TKT.2026.XXXX` dạng link.
- [x] Popup xác nhận (dùng `.minutes-modal`): hiện tên KH / lĩnh vực / giá trị đầu tư; bấm Tạo → gán mã, bỏ highlight vàng, cập nhật KPI + TỔNG CỘNG.

### Task 64: Xuất Excel + In báo cáo + verify tổng thể
- [x] Xuất Excel đúng bảng đang lọc (tái dùng pattern `downloadXls`).
- [x] "In báo cáo" → popup chọn In tổng hợp / In chi tiết; bản in A4 ngang bám bộ lọc + meta (số nhu cầu, kỳ, ngày in).
- [x] Verify Playwright 1440: lọc · thu/bung · tạo dự án · Excel · In · **0 lỗi console**.


### Task 65: Chỉnh theo phản hồi user (2026-08-20)
- [x] **Lĩnh vực KD**: bỏ dropdown checkbox tự chế → dùng `<select class="calendar-filter-select">` chuẩn **giống hệt file mockup mẫu** (chọn 1 lĩnh vực / Tất cả).
- [x] Đổi tên trạng thái **"Đã chốt" → "Đã lập dự án TKT"**; tạo dự án từ popup → trạng thái chuyển thẳng sang "Đã lập dự án TKT".
- [x] **Tiêu đề cột KHÔNG xuống dòng** (`white-space: nowrap`), nới `COL_WIDTHS` (tổng ~1660px) → bảng chi tiết cuộn ngang như file mẫu.
- [x] **Bỏ tô nền vàng** dòng chưa có dự án TKT — mọi dòng nhu cầu cùng nền trắng, dấu hiệu chỉ còn nút "+ TẠO MỚI".
- [x] **Chế độ xem tổng hợp** ("Ẩn chi tiết"): ẩn hẳn 6 cột chi tiết rỗng, chỉ còn 4 cột STT · Lĩnh vực KD/TT · Tổng giá trị đầu tư · **Số nhu cầu**; bỏ luôn cuộn ngang. Excel + bản in bám đúng chế độ đang xem (`pickCells`).
- [x] **Dày data demo**: 16 → **26 nhu cầu** / 18 khách hàng — Gara 8 · Năng lượng 7 · Môi trường 5 · Đào tạo 6.
- [x] Verify Playwright 1440: tổng hợp 4 cột/16 dòng in · Excel tổng hợp 6.5KB · lọc Đào tạo = 6 nhu cầu · tạo dự án → badge "Đã lập dự án TKT" · 0 dòng nền vàng · **0 lỗi console**.

### Task 66: Click tên meeting → drawer chi tiết meeting (2026-08-20)
- [x] Port nguyên khung `.ticket-drawer` / `.drawer-backdrop` / `.drawer-block*` từ `bao-cao-ket-qua-meeting-theo-thi-truong.html` (trượt từ phải 460px, header gradient teal theo loại Meeting, thân khối card, footer).
- [x] Làm dày data meeting bằng `enrichMeetings()` (sinh 1 lần, không random): mã `MEET.2026.NN`, giờ họp, hình thức Trực tiếp/Trực tuyến + link, địa điểm, mục tiêu, thành phần công ty (chủ trì + 1 người cùng phòng), thành phần KH (tên + chức vụ), người liên hệ, **trạng thái meeting** (Hoàn thành / Lên lịch / Huỷ — khác trạng thái nhu cầu).
- [x] Drawer 4 khối: Thông tin cuộc họp · Mục tiêu/Nội dung · Thành phần tham dự · **Nhu cầu thu thập được** (lĩnh vực, trạng thái nhu cầu, giá trị đầu tư, mốc triển khai, dịch vụ sửa chữa, dự án TKT).
- [x] Footer: nút **Tạo dự án TKT** (chỉ khi chưa có dự án & nhu cầu chưa dừng) mở popup đè lên drawer → tạo xong drawer tự làm mới; nút Đóng.
- [x] Đóng bằng ✕ / click backdrop / ESC (ESC ưu tiên đóng popup trước); khoá cuộn trang nền khi drawer mở.
- [x] Verify Playwright 1440: mở drawer từ tên meeting (4 khối/16 trường, header "Hoàn thành · MEET.2026.04") · tạo dự án từ drawer → ô Dự án TKT đổi thành `TKT.2026.FTX`, nút ẩn, drawer vẫn mở · nhu cầu "Không tiếp tục" (nc07) → badge "Huỷ", ẩn nút tạo dự án · ESC/backdrop đóng đúng, trả lại cuộn trang · **0 lỗi console**.

## Checkpoint

### Checkpoint — 2026-08-08 (khởi tạo plan)
Vừa hoàn thành: brainstorming + spec đầy đủ + plan (đã duyệt design & spec).
Đang làm dở: chưa bắt đầu code — chờ chọn cách thực thi (subagent-driven / inline).
Bước tiếp theo: Task 1 (scaffold khung + tokens).
Blocked:

### Checkpoint — 2026-08-08 (mockup DONE, subagent-driven)
Vừa hoàn thành: TẤT CẢ Phase 1–4 (subagent-driven, 4 implementer tuần tự + verify Playwright mỗi phase).
File: `ke-hoach-phat-trien-thi-truong-mockup.html` — 2 tab (Theo lịch Tháng/Tuần + Theo thị trường accordion), drawer chi tiết KH, KPI, popover sự kiện, filter loại, "+N khác", tìm kiếm KH. Verify desktop 1440 sạch.
Đang làm dở: RESPONSIVE đã code nhưng chưa verify — HOÃN theo yêu cầu user (làm sau khi chốt UI desktop).
Bước tiếp theo: user review mockup (`http://127.0.0.1:8912/ke-hoach-phat-trien-thi-truong-mockup.html`) → chỉnh UI desktop theo phản hồi → chốt → mới làm responsive.
Blocked:

### Checkpoint — 2026-08-09 (wrap up — bản gốc pivot + bản meeting hoàn thiện)
Vừa hoàn thành: 2 file mockup ở `.plans/gop-db/ke-hoach-phat-trien-thi-truong/`:
  - `...-mockup.html` (bản GỐC 3 loại: Phiếu công tác/Meeting/Task, meeting = tím) — qua Phase 1–12 (pivot lịch phiếu công việc, filter thật, drawer, multi-day thanh trải, border ngày rõ, tên KH trên thẻ).
  - `...-mockup-meeting.html` (bản CHỈ-MEETING, màu xanh ngọc) — Phase 13–14 + Task 25→34: 2 tab (Lịch meeting + Meeting theo thị trường dạng BẢNG kiểu Excel), header đồng bộ, thị trường=tỉnh/thành, badge trạng thái, popup "Xem biên bản" (mẫu app thật), popup "Xem lịch sử meeting", chip avatar công ty / chức vụ KH, summary 2 nhóm 1 hàng, drawer chữ thường-nhỏ-ít bold.
Đã verify Playwright 1440 mọi task. Tất cả CHƯA commit (mockup nằm trong .plans, không commit theo rule).
Đang làm dở: không có việc dở; đang ở nhịp user review từng phần bản meeting.
Bước tiếp theo: chờ yêu cầu chỉnh tiếp bản meeting; khi chốt UI desktop → làm RESPONSIVE (đang HOÃN cả 2 file); sau đó mới bàn port sang Vue thật.
Blocked:

### Checkpoint — 2026-08-10 (wrap up — Phase 15: tab Thị trường hoàn thiện + tab "Công việc của tôi" + đổi định vị màn)
Vừa hoàn thành: Phase 15 (Task 35→42) trên `ke-hoach-phat-trien-thi-truong-mockup-meeting.html` (có bản copy `quan_ly_cong_viec_ca_nhan.html`):
  - **Tab "Kết quả meeting theo thị trường"** (đổi tên từ "Meeting theo thị trường"): header 1 cấp; cột "Phiếu công tác / Lịch sử chấm công" (popup chấm công GPS, tab theo người) — CHỈ meeting Hoàn thành; cột "Dự án TKT" (chỉ Hoàn thành); bộ lọc Thị trường/Trạng thái/Loại meeting + **Kỳ** (Hôm nay/Tuần/Tháng/Quý/Năm/Tuỳ chọn) + **Xuất Excel**; đánh dấu **KH mới phát triển** (badge + highlight, đưa lên đầu danh sách); summary **lưới text** (bỏ chip) + nhóm Tổng hợp (dự án/KH mới/tỷ lệ hoàn thành).
  - **Tab "Công việc của tôi" (My To Do)** = tab ĐẦU TIÊN mặc định: gộp Task/Issue/Cá nhân, nhóm theo thời gian có **thu gọn/mở rộng** đúng màn thật (`TodoGroupHeader.vue`/`TodoMainList.vue` — Quá hạn ở cuối, chỉ Hôm nay mở sẵn), stats + filter + mini lịch + danh sách cá nhân.
  - **Tab "Lịch meeting"**: nút "Thêm meeting" quick-add (form + validate); drawer nút theo trạng thái (Sửa/Duyệt/Xem biên bản); **màu nền thẻ theo trạng thái**.
  - Đổi tên màn → **"Quản lý lịch làm việc cá nhân"**, topbar nhỏ gọn.
Đã verify Playwright (server `python3 -m http.server 8777`, giữ chạy theo yêu cầu user) mọi task. CHƯA commit (mockup trong .plans).
Đang làm dở: không có việc dở.
Bước tiếp theo: chờ user review/chỉnh tiếp; chốt xem có tách hẳn màn "Công việc của tôi" thành file riêng không (hiện `quan_ly_cong_viec_ca_nhan.html` là bản copy); RESPONSIVE vẫn HOÃN; sau đó mới bàn port Vue thật + đồng bộ My To Do với data meeting thật.
Blocked:

### Checkpoint — 2026-08-11 (wrap up — Task 43: bảng tab Thị trường → 3 cấp)
Vừa hoàn thành: Task 43 trên `ke-hoach-phat-trien-thi-truong-mockup-meeting.html` — bảng tab "Kết quả meeting theo thị trường" đổi từ 2 cấp (Thị trường rowspan + meeting) sang **3 cấp Thị trường ▸ Khách hàng ▸ Meeting**:
  - Cột **Khách hàng** nâng thành ô gộp `rowspan`, đặt sau Thị trường; BỎ khỏi từng dòng meeting (header vẫn 13 cột). Ô gộp giữ badge "KH mới" + nút "Xem lịch sử meeting".
  - Meeting **nhóm theo khách hàng**; trong 1 KH sắp xếp **cũ → mới** (ngày tăng dần). KH mới vẫn nổi đầu (thị trường + khách hàng có KH mới lên trước).
  - Xuất Excel đồng bộ thứ tự (nhóm theo KH, cũ→mới) + đưa cột Khách hàng lên vị trí 2.
  - Code: thêm helper `groupTicketsByCustomer()` + `buildCustomerGroupCellHtml()` (tái dùng `buildTableCustomerCellHtml()`), viết lại `buildMarketTableBodyHtml()` (2 vòng lồng market→customer), bỏ td Khách hàng khỏi `buildTableMeetingCellsHtml()`, sửa header trong `renderMarketTable()`, cập nhật `exportRowValues()`/`exportMarketTableToExcel()`, thêm CSS `.market-table__cell--customer`.
Đã verify Playwright 1440 (server 8777 giữ chạy): rowspan đúng (Hà Nội=6/TP.HCM=2/Đà Nẵng=2/Phú Thọ=1); cũ→mới đúng (Thành Đạt 01/08→14/08, Thăng Long 08/08→21/08); nút "Xem lịch sử meeting" trong ô gộp vẫn mở đúng KH. CHƯA commit (mockup trong .plans).
Chỉ sửa `...-mockup-meeting.html` (bản copy `quan_ly_cong_viec_ca_nhan.html` giữ nguyên — nay đã LỆCH bản chính).
Đang làm dở: không có việc dở.
Bước tiếp theo: user review tab 3 (3 cấp) → chỉnh tiếp nếu cần (thứ tự khách hàng / style ô gộp / tô nền phân tầng); chốt xem có đồng bộ đổi sang `quan_ly_cong_viec_ca_nhan.html` không; RESPONSIVE vẫn HOÃN; sau đó port Vue thật.
Blocked:

### Checkpoint — 2026-08-11 (wrap up — session vận hành, KHÔNG sửa code feature)
Vừa hoàn thành: mở lại bản mockup mới nhất `ke-hoach-phat-trien-thi-truong-mockup-meeting.html` (sửa lần cuối 2026-08-10 21:48) + khởi động lại môi trường dev cả 2 repo (đang ở nhánh `gop_db`).
  - **hrm-client** chạy tại http://localhost:3000 (node v12.22.12 — node 14.21.3 project yêu cầu CHƯA cài trong nvm). Script `dev` gốc thiếu heap → **crash JS heap OOM**; phải chạy `NODE_OPTIONS=--max-old-space-size=8192 nuxt`.
  - **hrm-api** chạy `php artisan serve --port=8000` tại http://127.0.0.1:8000 (PHP 7.4.33 tại `/opt/homebrew/opt/php@7.4/bin/php` — `php` không có trong PATH). FE trỏ `BASE_API_URL=http://127.0.0.1:8000` (`.env`) → khớp.
Đang làm dở: không có (không đụng code feature). Mockup giữ nguyên như Task 43.
Bước tiếp theo: như checkpoint Task 43 (user review tab 3 cấp). Chi tiết cách chạy dev environment đã lưu vào memory.
Blocked:

### Checkpoint — 2026-08-19 (wrap up — Task 44→59: TÁCH FILE BÁO CÁO + hoàn thiện)
Vừa hoàn thành: 16 task (44→59) trên **file báo cáo ĐỘC LẬP mới** `bao-cao-ket-qua-meeting-theo-thi-truong.html`
(tách khỏi `...-mockup-meeting.html` ở Task 46; file cũ nay chỉ còn 2 tab Công việc của tôi + Lịch meeting):
  - **Cấu trúc**: bảng OUTLINE 3 cấp `I / 1 / 1.1` (Thị trường ▸ Khách hàng ▸ Meeting) thay ô gộp rowspan; 1 cột gộp tên + cột STT phân cấp.
  - **2 chế độ cột**: TỔNG HỢP (mặc định, chỉ tới cấp Khách hàng) = 1 cột/phòng ban + Tổng, ẩn hết cột chi tiết · CHI TIẾT = 13 cột đầy đủ. Nút "Ẩn/Hiện chi tiết" + caret thu/bung từng nhóm.
  - **Cột & lọc theo tổ chức**: cột "Phòng ban" (của người chủ trì) + bộ lọc cascade **Công ty ▸ Phòng ban ▸ Người chủ trì**; lọc phòng/công ty → chỉ hiện cột phòng tương ứng (bảng · summary · Excel · bản in).
  - **Tương tác**: sắp xếp mọi cột dữ liệu (từ "Thời gian" sang phải, 3 trạng thái asc/desc/mặc định) · sticky hàng tiêu đề + dòng TỔNG CỘNG (dời từ tfoot lên đầu) · click cả dòng meeting mở panel chi tiết (drawer của Lịch meeting) · click số ở dòng TỔNG CỘNG → popup danh sách meeting kèm nút In + Xuất Excel riêng.
  - **Dải tổng hợp thiết kế lại**: 4 ô KPI + 3 khối phân bổ (thanh xếp chồng trạng thái, thanh ngang phòng ban/thị trường), bộ lọc chuyển LÊN TRÊN dải này + nút "Ẩn/Hiện tổng hợp".
  - **In**: nút "In báo cáo" → popup chọn In tổng hợp / In chi tiết, bản in A4 ngang bám bộ lọc.
  - **Data demo**: 30 meeting / 11 khách hàng / 3 thị trường (Hà Nội 14 · TP.HCM 8 · Đà Nẵng 8), phòng ban cân đối 11/11/8; bỏ hẳn nhận dạng "KH mới".
Đã verify Playwright sau MỖI task (0 lỗi console ở lần verify cuối).
Đang làm dở: không có việc dở.
Bước tiếp theo: user review tổng thể file báo cáo (`http://127.0.0.1:8931/bao-cao-ket-qua-meeting-theo-thi-truong.html`) → chốt UI desktop; sau đó mới bàn RESPONSIVE (vẫn hoãn) và port sang Vue thật.
Blocked: chờ user chốt tên 2 công ty demo (đang tạm Tân Phát ETEK / Tân Phát Sài Gòn) và quyết định xử lý bản copy lệch `quan_ly_cong_viec_ca_nhan.html`.

### Checkpoint — 2026-08-20 (wrap up — Phase 16: file BÁO CÁO TỔNG HỢP NHU CẦU KHÁCH HÀNG)
Vừa hoàn thành: Task 60→66 — **file mockup ĐỘC LẬP mới** `bao-cao-tong-hop-nhu-cau-khach-hang.html`
(layout bám ảnh Excel user gửi, style tái dùng nguyên bộ token + component của `bao-cao-ket-qua-meeting-theo-thi-truong.html`):
  - **Toolbar 7 bộ lọc**: Kỳ xem (Tất cả/Hôm nay/Tuần/Tháng/Quý/Năm/Tuỳ chọn — bám thời gian BẮT ĐẦU HỌP) · Lĩnh vực KD · Khách hàng · cascade **Công ty ▸ Phòng ban ▸ Bộ phận ▸ Kinh doanh chủ trì** · Xoá lọc. Cụm nút phải: Ẩn tổng hợp · Ẩn/Hiện chi tiết · In báo cáo · Xuất Excel.
  - **Dải KPI**: Tổng nhu cầu · Tổng giá trị đầu tư · Khách hàng · Chưa có dự án TKT (+%) + 3 khối phân bổ (thanh xếp chồng trạng thái · thanh ngang lĩnh vực KD · thanh ngang thị trường).
  - **Bảng outline 3 cấp** `I` Lĩnh vực KD → `1` Thị trường → `1.1` Khách hàng, 10 cột đúng ảnh; sticky header + dòng TỔNG CỘNG; caret thu/bung từng nhóm.
  - **2 chế độ cột**: CHI TIẾT 10 cột (cuộn ngang, tiêu đề không wrap) ↔ **TỔNG HỢP** 4 cột (STT · Lĩnh vực KD/TT · Tổng giá trị đầu tư · Số nhu cầu, ẩn hết cột chi tiết rỗng, không cuộn ngang). Excel + bản in bám đúng chế độ đang xem.
  - **Nút "+ TẠO MỚI"** ở cột Dự án TKT → popup tạo dự án (gợi ý mã `TKT.YYYY.<viết tắt KH>`), tạo xong gán mã + chuyển trạng thái **"Đã lập dự án TKT"** + cập nhật KPI/TỔNG CỘNG + toast.
  - **Drawer chi tiết meeting** (Task 66): click TÊN MEETING → panel trượt phải dùng lại khung `.ticket-drawer` của file báo cáo meeting; 4 khối (Thông tin cuộc họp · Mục tiêu/Nội dung · Thành phần tham dự · Nhu cầu thu thập được); footer có nút "Tạo dự án TKT" (popup đè lên drawer, tạo xong drawer tự làm mới); đóng bằng ✕/backdrop/ESC.
  - **Chỉnh theo phản hồi user (Task 65)**: select Lĩnh vực KD dùng `<select>` chuẩn giống file mẫu (bỏ dropdown checkbox) · "Đã chốt" → "Đã lập dự án TKT" · tiêu đề cột không xuống dòng · BỎ tô nền vàng dòng chưa có dự án · chế độ tổng hợp ẩn cột rỗng · data 16 → **26 nhu cầu / 18 KH** (Gara 8 · Năng lượng 7 · Môi trường 5 · Đào tạo 6).
Đã verify Playwright 1440 sau mỗi nhóm thay đổi — **0 lỗi console**; Excel tải thật (chi tiết 25KB / tổng hợp 6.5KB); bản in tổng hợp 4 cột/16 dòng, chi tiết 10 cột/30 dòng.
Đang làm dở: không có việc dở.
Bước tiếp: user review tổng thể `http://127.0.0.1:8952/bao-cao-tong-hop-nhu-cau-khach-hang.html` → chỉnh tiếp nếu cần; sau đó mới bàn RESPONSIVE (vẫn hoãn) và port Vue thật.
Blocked: chờ user chốt (a) Lĩnh vực KD có cần **chọn nhiều** không (hiện là select đơn theo yêu cầu "dùng đúng select như file mẫu", trong khi ảnh Excel ghi "select chọn nhiều"); (b) tên 2 công ty demo (tạm Tân Phát ETEK / Tân Phát Sài Gòn).
