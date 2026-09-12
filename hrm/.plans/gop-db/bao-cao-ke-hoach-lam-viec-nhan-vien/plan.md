# Plan — Báo cáo kế hoạch làm việc của nhân viên (Mockup UI)

**Người phụ trách:** @dnsnamdang
Xem `design.md` cùng thư mục cho spec đã chốt.
File duy nhất: `bao-cao-ke-hoach-lam-viec-nhan-vien.html` (standalone) + `screenshots/`.

## Global Constraints (áp cho MỌI task)

- Mockup HTML tĩnh 1 file, KHÔNG thư viện ngoài; toàn bộ tiếng Việt.
- Port nguyên khối `<style>` của `../bao-cao-phat-trien-thi-truong-khach-hang/`; phần riêng để CUỐI khối style dưới nhãn *"BỔ SUNG RIÊNG MÀN KẾ HOẠCH LÀM VIỆC"*.
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
