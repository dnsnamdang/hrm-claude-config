# Plan — Báo cáo phát triển thị trường - Khách hàng (Mockup UI)

Xem `design.md` cùng thư mục cho spec đã chốt.
File duy nhất: `bao-cao-phat-trien-thi-truong-khach-hang.html` (standalone).

## Global Constraints (áp cho MỌI task)

- Mockup HTML tĩnh 1 file, KHÔNG thư viện ngoài; toàn bộ tiếng Việt.
- Port nguyên khối `<style>` của `bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`; phần riêng để CUỐI khối style.
- Data demo sinh bằng **LCG có hạt giống** (không `Math.random`) — demo không nhảy số.
- Mọi diễn giải / công thức nằm trong tooltip icon `i`, không viết chữ ra màn.
- **Task đụng giao diện BẮT BUỘC verify Playwright trên trình duyệt thật, ĐO BẰNG SỐ LẤY TỪ DOM** (toạ độ, bề rộng, `getComputedStyle`, `Range.getBoundingClientRect`) — không chỉ nhìn ảnh.
- ⚠️ `scrollWidth` của ô trong bảng `table-layout: fixed` KHÔNG đáng tin (đã 2 lần báo tràn giả). Đo bề rộng nội dung bằng `Range.selectNodeContents()`.

## Phase 1 — Dựng màn (2026-09-06)

### Task 1: Brainstorming + chốt spec
- [x] Đọc mockup mẫu CSKH tiềm năng + báo cáo meeting theo thị trường.
- [x] Chốt: 2 tiêu chí theo dõi · bộ cột "vòng đời meeting + kết quả phát triển" · cấp Bộ phận "có thì hiện" · bấm số ra popup chi tiết.
- [x] Trình bày thiết kế ngắn trong chat → user duyệt.

### Task 2: Dựng file mockup
- [x] Port CSS + dựng markup (topbar · toolbar · dải tổng hợp · bảng · drawer · 2 popup · toast · `#print-area`).
- [x] Mock data: 2 công ty · 10 phòng ban · 9 bộ phận (4 phòng) · 30 NV · 20 tỉnh/TP · 60 KH · 591 meeting.
- [x] **Hàm dựng cây ĐỆ QUY N CẤP** (`buildTree` + `nodeRows`) — thay `groupRows2` cứng 2 cấp của màn CSKH; tự sinh STT phân cấp, indent theo độ sâu, **tự bỏ qua cấp Bộ phận** ở phòng không chia bộ phận.
- [x] Popup drill-down · drawer biên bản · in A4 ngang 2 chế độ · xuất Excel `.xls`.
- [x] Verify Playwright 1440: số liệu khớp tính toán độc lập bằng node (160/119/104/18/22/32 · 375,7 tỷ · 56 KH); **cộng dồn 0 sai lệch / 213 dòng cha × 6 cột**; 25 nhánh có Bộ phận đi 4 cấp / 31 nhánh nhảy 3 cấp / 0 dòng "Chưa phân bộ phận"; popup 104 dòng toàn "Hoàn thành". **0 lỗi console**.

### Task 3: Fix 3 lỗi phát hiện khi đo
- [x] Tooltip `.rsum-info::after` (246px) của 2 cột cuối tràn khung bảng → `scrollWidth 1462 / clientWidth 1354`. Neo tooltip 3 cột cuối về mép PHẢI → 1354/1354.
- [x] Thụt lề theo cấp KHÔNG ăn: `.rsum-tb td` (0,1,1) đè `.rsum-tb__name--dN` (0,1,0) → cả 4 cấp dính 10px. Đổi selector `td.rsum-tb__name--dN`, lề 30/52/74/96px (đủ chỗ caret thò trái 24px).
- [x] Drawer mở TỪ TRONG popup bị backdrop popup che kín (`elementFromPoint` trả `.minutes-modal-backdrop`) vì drawer z-index 1000/1001 < popup 1100/1101. Nâng drawer lên 1200/1201; bỏ 2 rule chết `#project-modal*`.
- [x] Verify lại: drawer nổi trên popup, đóng drawer quay về đúng danh sách 104 dòng.

## Phase 2 — Tinh chỉnh theo phản hồi user (2026-09-06 → 07)

### Task 4: Bỏ chế độ xem "Tất cả" — bắt buộc chọn 1 tiêu chí (2026-09-06)
- [x] Select còn 2 option, mặc định Thị trường; dòng tiêu đề phần I/II gộp thành **1 dòng `TỔNG`**; gỡ hàm `toRoman()` thành code chết.
- [x] Khối lọc riêng theo tiêu chí + **xoá giá trị ô lọc đang bị ẩn** (chống lọc ngầm).
- [x] Verify: 1 dòng TỔNG · 19 vs 56 dòng cấp 0 · bung hết 226 dòng **0 lỗi cộng dồn** · tổng dòng cấp 0 = 160 = dòng TỔNG · bản in 227 dòng.

### Task 5: Fix tiêu đề cột bị che (2026-09-06)
- [x] Đo: 5 nhãn dài hơn ô — Hoàn thành thiếu 19px · Đã thực hiện 18 · Meeting KH 16 · Giá trị dự kiến 14 · Nhu cầu 8; icon `i` lòi qua mép 9–20px.
- [x] Cho hàng tiêu đề xuống dòng + canh đáy (sau này Task 8 đổi lại thành 1 dòng chữ thường).
- [x] Nới cột "Giá trị dự kiến (đ)" popup 130 → 144px; cột STT bảng biên bản drawer 40 → 46px.

### Task 6: Thống kê theo `created_at` — Lập trước kỳ / Lập trong kỳ (2026-09-07)
- [x] Thêm trường `createdAt` = ngày họp − (1..28) ngày, tính theo **số thứ tự phiếu (không gọi `demoRnd`)** để không làm lệch chuỗi ngẫu nhiên → **số liệu cũ giữ nguyên 100%**.
- [x] `metrics()` thêm `pre` / `inp`; cache kỳ đang xem vào `RANGE` để không đọc DOM hàng trăm lần mỗi lần render.
- [x] Popup thêm cột **Ngày tạo meeting**; 2 chỉ tiêu mới bấm được.
- [x] Verify: 72 + 88 = 160 ở mọi kỳ (tháng/quý/năm/tuần); mốc kiểm tra logic **kỳ "Năm nay" → "Lập trước kỳ" = 0**; mọi dòng popup có ngày tạo đúng phía kỳ; ngày tạo ≤ ngày họp trên cả 591 meeting.

### Task 7: Nén dải tổng hợp (2026-09-07)
- [x] ❌ Thử bản **lưới text phẳng** (344 → 159px) — **user chê xấu, revert**.
- [x] Bản chốt: GIỮ khối/hộp, nén bằng (1) 2 khối + cụm KPI về CÙNG 1 HÀNG, (2) ô con xếp ngang thay lưới 2×2, (3) thu padding/cỡ chữ. Phần nén KPI viết trong `.type-summary-bar` nên **không ảnh hưởng hộp KPI của popup**.
- [x] Verify: 344 → **143px** (44% → 16% màn hình); bảng từ y=548 lên y=347; dòng thấy được 4 → 14.

### Task 8: Tiêu đề cột — chữ thường, 1 dòng (2026-09-07)
- [x] Bỏ `text-transform: uppercase`, `white-space: nowrap`. Chữ thường hẹp hơn ~12% nên chỉ phải nới 5 cột đúng phần thiếu (+16/+12/+12/+8/+8), lấy từ phần dư của cột "Nội dung theo dõi".
- [x] Verify: 0 tiêu đề bị cắt (dư 2–25px/cột), 0 cột xuống dòng, hàng tiêu đề 45 → 37px.

### Task 9: Đổi bộ chỉ tiêu dải tổng hợp · BỎ khối KPI (2026-09-07)
- [x] Khối 1 = Tổng meeting · Lập trước kỳ · Lập trong kỳ. Khối 2 = Meeting hoàn thành · Meeting bị huỷ · Nhu cầu thu thập được.
- [x] Bỏ hẳn markup + CSS + hàm `kpiBlock()`; giữ `kpiBox()` vì popup còn dùng. Số tổng xuống ô con nên **header khối bỏ số to** (tránh lặp 160 hai lần).
- [x] Verify: 136px (15% màn hình); 72+88=160; bấm "Meeting bị huỷ" → 18 dòng **toàn trạng thái Huỷ**; popup vẫn đủ 3 hộp KPI.

### Task 10: Chuẩn hoá LOGIC POPUP (2026-09-07)
- [x] `buildTree` ghi lại **`path`** (chuỗi cấp đã đi qua) cho từng node.
- [x] **Luật bộ lọc**: mọi chiều trên `path` → ẩn ô lọc + xoá giá trị; cascade vẫn dùng chiều đã cố định để thu hẹp cấp dưới.
- [x] **Tiêu đề**: *"Đang xem &lt;chỉ tiêu&gt; theo &lt;Cấp&gt;: &lt;Tên&gt;"* + dòng phụ hiện đường dẫn cấp cha.
- [x] **Chip phân bổ** bỏ Loại meeting + Trạng thái.
- [x] Verify 6 kiểu node (thị trường / phòng ban / khách hàng / bộ phận / nhân viên / dòng TỔNG): ô lọc và tiêu đề đúng từng trường hợp; ô Nhân viên khi mở theo Bộ phận chỉ còn 2 người của bộ phận đó.

### Task 11: Popup — chip, filter thị trường, thứ tự cột, giờ họp, sort (2026-09-07)
- [x] Chip phân bổ **chỉ còn Thị trường + Phòng ban** (bỏ Nhân viên / Khách hàng).
- [x] Thêm luật **cố định Khách hàng ⇒ ẩn luôn ô lọc Thị trường** (1 KH chỉ ở 1 thị trường).
- [x] Cột "Ngày họp" hiện **ngày + giờ**; "Ngày tạo phiếu" → **"Ngày tạo meeting"** (nới 128 → 154px vì nhãn + mũi tên sort thiếu 22px).
- [x] **Sắp xếp được ở 4 cột**: Ngày họp · Ngày tạo meeting · Thị trường · Phòng ban (bấm: tăng → giảm; mở popup mới reset). Ngày so theo mốc thời gian thật, tên so bằng `localeCompare('vi')`.
- [x] Verify: sort tăng/giảm đúng ở cả 4 cột; **In + Xuất Excel bám đúng thứ tự đang sắp** (3 dòng đầu bản in trùng khít popup).

### Task 12: Thứ tự cột theo tiêu chí · cấp Bộ phận cho tiêu chí Thị trường · loại meeting mới (2026-09-07)
- [x] ⚠️ Quy tắc "Nhân viên chủ trì LUÔN trước Phòng ban" (Task 11) **bị thay thế** — user chốt xếp đúng thứ tự cấp theo dõi.
- [x] Các chiều theo dõi dồn lên **ngay sau STT**, dùng chung hàm `dimColumnOrder()` cho popup + bản in + Excel.
- [x] Tiêu chí Thị trường thêm cấp **Bộ phận** → 4 cấp như tiêu chí Khách hàng.
- [x] Thêm loại **"Meeting triển khai Dự án"** (mt5) + 3 mẫu tên. Vì `demoPick` vẫn tiêu thụ đúng 1 số ngẫu nhiên nên **số liệu cũ không đổi**.
- [x] Verify: cây Thị trường 4 cấp (19·47·71·33) **0 lỗi cộng dồn**; thứ tự cột đúng cả 2 tiêu chí ở popup lẫn bản in; 0 tiêu đề bị cắt; sort vẫn chạy.

### Task 13: Popup — BỎ CỘT của cấp đã cố định (2026-09-07)
- [x] `drillColumns()` lọc bỏ mọi chiều nằm trên `path` của node (`drillFixedDims`). Popup theo Thị trường bỏ cột Thị trường, theo Khách hàng bỏ cột Khách hàng, theo Bộ phận bỏ cả Phòng ban lẫn Bộ phận; popup từ dòng TỔNG giữ đủ cột.
- [x] Cố ý dùng `drillFixedDims` chứ không `drillHiddenDims` — **cột Thị trường vẫn giữ** ở popup theo Khách hàng (chỉ ô lọc bị ẩn), đúng yêu cầu user.
- [x] Không phải sửa bản in / Excel / `colspan` dòng rỗng: đều đã bám `drillColumns()` và `cols.length`.
- [x] Verify Playwright 1440×900, **13 ca popup** (7 tiêu chí Thị trường + 6 tiêu chí Khách hàng):
  bộ cột đúng kỳ vọng từng ca; ô lọc hiện/ẩn khớp với cột còn lại; **0 tiêu đề bị cắt**
  (đo bằng `Range.selectNodeContents`, không dùng `scrollWidth`); bảng 2065 → 1670px tuỳ số cột.
- [x] Verify **không mất thông tin**: đo trên bản TRƯỚC khi sửa, mọi cột bị bỏ đều có **đúng 1 giá trị phân biệt** trên toàn bộ dòng.
- [x] Verify sắp xếp: popup theo Thị trường mất nút sắp cột Thị trường (còn `dept/date/created`), popup theo Phòng ban còn `date/created`;
  sắp theo Thị trường ở popup ALL rồi mở popup theo Thị trường → **reset đúng về Ngày họp tăng dần** (11/09 → 19/09 → 25/09), không lỗi.
- [x] Verify bản in: header + số ô dòng 1 **trùng khít popup** ở 4 ca. Excel xuất ra header `STT · Phòng ban · Bộ phận · Nhân viên chủ trì · Khách hàng · …` — đã bỏ Thị trường. **0 lỗi console**.
- [x] ⚠️ Phát hiện khi đo: popup theo Khách hàng **mất chip "KH mới"** (chip nằm trong ô Khách hàng). 15/56 node Khách hàng có chip trong danh sách nhiều dòng → ghi vào *Còn treo*, chờ user chốt chỗ gắn chip.

### Task 14: Đổi quy mô data demo (2026-09-07)
- [x] **10 thị trường** (từ 20) · **chỉ 1 phòng có bộ phận** — Kinh doanh dự án × 2 bộ phận (từ 4 phòng / 9 bộ phận) · **65 nhân viên**, mỗi phòng ban / bộ phận **5–7 người** (từ 30 NV, ~3/phòng).
- [x] Số NV mỗi đơn vị đếm **cố định theo chu kỳ 5·6·7** (không gọi `demoRnd`) nên demo vẫn không nhảy số.
- [x] Verify **0 chỉ tiêu bị lệch** so với trước khi đổi: kỳ 09/2026 vẫn 160 · 119 · 104 · 18 · 22 · 32 · 375,7 tỷ · 56 KH · 72+88.
  Lý do: `demoPick` luôn tiêu thụ đúng 1 số ngẫu nhiên bất kể độ dài mảng ⇒ chuỗi LCG không đổi, chỉ phân bổ đổi.
- [x] ⚠️ **Sửa số sai trong tài liệu**: "591 meeting" là sai — đo cả bản TRƯỚC lẫn SAU đều ra **612** (kỳ "Năm nay").
- [x] Verify cây: tiêu chí Thị trường **10 · 43 · 69 · 19** (142 dòng), tiêu chí Khách hàng **56 · 56 · 79 · 19** (211 dòng);
  **0 lỗi cộng dồn / 63 dòng cha × 6 cột = 378 phép kiểm**; tổng dòng cấp 0 = 160 = dòng TỔNG ở cả 2 tiêu chí.
- [x] Verify ràng buộc: ô lọc Thị trường đúng **10** mục; **11 đơn vị** (9 phòng + 2 bộ phận) đều có **5–7 NV**, min 5, tổng 65;
  chỉ **2 tên bộ phận** xuất hiện trong cây (Năng lượng · Môi trường) ⇒ đúng 1 phòng có bộ phận; **0 dòng "Chưa phân bộ phận"**.
- [x] Verify Task 13 vẫn đúng trên data mới: 5 kiểu popup bỏ cột đúng kỳ vọng, **0 tiêu đề bị cắt**, **0 lỗi console**.
- [x] ⚠️ Ghi nhận cách bung cây khi verify: bảng **re-render sau MỖI click** nên phải click **từng caret một** trong vòng lặp;
  click cả loạt trong 1 lượt chỉ ăn click đầu (đã báo nhầm 40 dòng thay vì 142).

### Task 15: Thêm kỳ "Tuần tiếp theo" / "Tháng tiếp theo" (2026-09-07)
- [x] Thêm 2 option vào `#f-period`, đặt ngay sau kỳ cùng loại: `… Tuần này · Tuần tiếp theo · Tháng này · Tháng tiếp theo · Quý này …`
- [x] `periodRange()`: gộp nhánh `week`/`nextweek` bằng biến `shift` (0 / 7 ngày); `nextmonth` = `[new Date(y, m+1, 1), new Date(y, m+2, 0)]`.
- [x] Handler `change` chỉ phân biệt `custom` nên không phải sửa; nút Xoá lọc vẫn về `month`.
- [x] Verify mốc kỳ (TODAY = 26/09/2026): Tuần này **21/09–27/09**, Tuần tiếp theo **28/09–04/10** (vắt đúng sang tháng 10), Tháng tiếp theo **01/10–31/10**.
- [x] Verify số liệu: Tuần tiếp theo **37 meeting** (29 lập trước + 8 lập trong = 37), Tháng tiếp theo **148** (73 + 75 = 148);
  *Đã thực hiện / Hoàn thành / Huỷ / Nhu cầu* = **0** ở cả 2 kỳ — đúng vì chưa tới ngày họp.
- [x] Verify cây + popup ở 2 kỳ mới: **0 lỗi cộng dồn** (40 và 59 dòng cha × 6 cột), tổng dòng cấp 0 = dòng TỔNG = số dòng popup (37 / 148);
  ngày họp trong popup nằm trọn trong kỳ (28/09→04/10 và 01/10→31/10). **0 lỗi console**.
- [x] ⚠️ Phát hiện khi đo: **"Lập trong kỳ" ≠ 0 ở kỳ tương lai** (8 và 75) vì data demo sinh `createdAt` không chặn trần theo TODAY
  → phiếu mang ngày tạo ở tương lai. Đã sửa lại comment trong code cho đúng thực tế và ghi vào *Còn treo*; chờ user chốt có kẹp `createdAt ≤ TODAY` không.

### Task 16: Thay danh mục demo bằng DỮ LIỆU THẬT từ DB HRM (2026-09-07)
- [x] Đọc `hrm_erp`: `companies` ▸ `departments` ▸ `parts` ▸ `employee_infos`; lọc phòng **kinh doanh** `status=1` có **≥ 5 NV** đang hoạt động.
- [x] Chọn **10 phòng**: 6 phòng của *CTCP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT* (THIẾT BỊ Ô TÔ 1/2/3 · KINH DOANH THƯƠNG MẠI · KD VẬT TƯ THIẾT BỊ BÔI TRƠN · KD THIẾT BỊ VÀ VẬT LIỆU CÔNG NGHIỆP) + 4 phòng *TNHH THIẾT BỊ TÂN PHÁT SÀI GÒN* (KD Khu vực 1–4).
- [x] **Phòng có bộ phận = PHÒNG KINH DOANH THƯƠNG MẠI**: DB có 3 bộ phận nhưng bộ phận *Kinh doanh dự án* chỉ 1 NV (< 5) ⇒ lấy 2 bộ phận — khớp luôn lựa chọn "2 bộ phận" user đã chốt ở Task 14.
- [x] **63 nhân viên tên thật**, lấy N người đầu mỗi đơn vị theo chu kỳ 5·6·7 (không gọi `demoRnd`).
- [x] Dọn chuỗi còn sót tên cũ: `'Tại Tân Phát ETEK'` → `'Tại văn phòng Tân Phát'`; comment ví dụ đổi sang phòng hiện có.
- [x] Verify Playwright: **10 phòng · 2 công ty đúng tên DB · 11 đơn vị đều 5–7 NV** (min 5, tổng 63);
  chỉ 2 tên bộ phận trong cây; **0 dòng "Chưa phân bộ phận"**; **0 lỗi cộng dồn / 63 dòng cha × 6 cột**; dòng TỔNG 160 = tổng cấp 0.
- [x] Verify tràn chữ (tên thật dài hơn nhiều): **0 ô bị cắt** ở bảng chính lẫn popup, bảng chính **không tràn ngang khung**.
- [x] ⚠️ Hồi quy mật độ: popup **158/160 dòng (99%) cao 2 dòng** (35 → tới 66px) vì cột *Phòng ban* chỉ 144px mà tên thật dài;
  bảng chính nhẹ hơn, **4/145 dòng (3%)** cao 52px. Chờ user chốt hướng xử lý (nới cột / dùng `code` / giữ nguyên).
- [x] ⚠️ Cách đo sai đã loại: đếm `Range.getClientRects().length` KHÔNG cho biết số dòng — ô có caret/badge cho nhiều rect dù chỉ 1 dòng.
  Đo xuống dòng bằng **chiều cao dòng so với dòng chuẩn**.

### Task 17: Bỏ cột Bộ phận khi popup không có dòng nào thuộc bộ phận (2026-09-07)
- [x] `drillColumns()` thêm: `if (!drillMeetings(key).some(m => m.teamId)) fixed.add('team')`.
  Xét trên toàn bộ meeting của node, KHÔNG theo bộ lọc trong popup → cột không nhấp nháy khi lọc.
- [x] Áp cho MỌI popup (user chốt), không riêng popup theo Phòng ban: popup theo Nhân viên / Khách hàng / Thị trường rơi vào cùng tình huống cũng bỏ.
- [x] Verify **toàn bộ 360 popup** (cả 2 tiêu chí): **325 bỏ cột · 35 giữ**; **0 ca giữ cột mà cột rỗng**.
- [x] Verify chiều nghịch trên bản TRƯỚC khi sửa: 360 popup = **266 có cột nhưng rỗng + 35 có dữ liệu + 59 vốn đã bỏ** (luật Task 13).
  325 = 266 + 59 ⇒ **khớp chính xác, không bỏ thừa cũng không sót**.
- [x] Verify bản in bám đúng cột ở 4 ca (TỔNG · phòng không BP · phòng có BP · nhân viên); **0 tiêu đề bị cắt**; **0 lỗi console**.

### Task 17b: Đính chính kết luận về mật độ dòng popup (2026-09-07)
- [x] Kết luận ở Task 16 (*"popup 99% dòng 2 hàng do đổi data thật, thủ phạm là cột Phòng ban"*) **SAI ở cả 2 vế**. Đo lại bản TRƯỚC khi dùng data thật: đã **156/160 dòng (98%)** cao hơn dòng chuẩn từ trước.
- [x] Đo số ô dài quá bề rộng cột (dựng span `white-space:nowrap` cùng font để lấy bề rộng 1 dòng thật):
  popup TỔNG — **Tên meeting 142/160 · Khách hàng 134/160 · Phòng ban 96/160 · Loại meeting 83/160** · Bộ phận 9 · Nhu cầu 6 · Nhân viên 1.
- [x] Kết luận đúng: dòng 2 hàng là **vốn có**, do *Tên meeting* + *Khách hàng*. Đổi sang data thật chỉ làm cột *Phòng ban* từ **7 → 96** ô quá khổ, kéo dòng cao nhất **52 → 66px** (một số dòng sang 3 hàng).
- [x] ⚠️ Cách đo sai đã loại: đo "quá khổ" bằng `Range.getBoundingClientRect()` trên ô ĐÃ wrap chỉ trả bề rộng dòng dài nhất, luôn ≤ bề rộng ô → không bao giờ báo tràn. Phải dựng span nowrap để lấy bề rộng 1 dòng.

### Task 18: Bỏ cột "Tỷ trọng giá trị" (2026-09-07)
- [x] Gỡ khỏi `COLS`, khỏi ô của `sectionRow` + `nodeRow`, khỏi `TRACK_COLUMNS` và `trackRows` (bản in + Excel).
- [x] Gỡ code chết theo: hàm `shareBar()`, tham số `baseInvest` xuyên `nodeRow`/`nodeRows`/`walk`, CSS `.rsum-sbar*` + `.rsum-tb__share`.
- [x] Verify: bảng còn **10 cột** khớp nhau ở `thead` / `colgroup` / ô dữ liệu; bản in 10 cột; Excel header hết "Tỷ trọng giá trị"; **0 lỗi cộng dồn / 63 dòng cha × 6 cột**.

### Task 19: Thay nút "Ẩn/Hiện chi tiết" bằng bộ CHỌN CẤP XEM (2026-09-07)
- [x] Select đặt đúng chỗ nút cũ (trong ô tiêu đề "Nội dung theo dõi"), 4 mục: `Chỉ <cấp gốc>` · `Đến Phòng ban` · `Đến Bộ phận` · `Tất cả cấp (đến Nhân viên)`.
- [x] Hàm `applyLevel()` xét theo **`dim` của node con**, KHÔNG theo độ sâu — vì cây bỏ qua cấp Bộ phận ở 9/10 phòng, tính theo độ sâu sẽ lẫn bộ phận với nhân viên trên cùng một hàng.
- [x] `state.level` là nguồn sự thật; bấm caret tay chỉ đổi `state.expanded` nên select không bị nhảy giá trị.
- [x] Đổi tiêu chí: render lại để dựng `TREES` mới rồi mới `applyLevel` (thứ tự này bắt buộc, cây cũ không còn key hợp lệ). Nút Xoá lọc đưa `state.level` về 0.
- [x] CSS select bê nguyên khuôn nút cũ (cao 21px, viền `#b6d8e0`, chữ 10.5px, mũi tên SVG nền) → **hàng tiêu đề vẫn 37px**, không cao thêm; select nằm gọn trong ô.
- [x] Verify từng mức (tiêu chí Thị trường): cấp 0 → **10 dòng** · Đến Phòng ban → **51** · Đến Bộ phận → **63** · Tất cả cấp → **145**.
- [x] Verify điểm mấu chốt của luật "theo tên cấp": ở mức *Đến Bộ phận*, **12 dòng cấp 2 đều là "BP ..."**, và **chỉ PHÒNG KINH DOANH THƯƠNG MẠI** đang bung — 40 phòng còn lại đứng yên, không lòi nhân viên.
- [x] Verify đổi tiêu chí giữ nguyên cấp đang chọn + nhãn đổi theo (*Chỉ Khách hàng*); Xoá lọc về cấp 0 (11 dòng); bấm caret tay không đổi giá trị select. **0 lỗi console**.
- [x] ⚠️ Cách đo sai đã loại: đo bề rộng nhãn tiêu đề bằng `th.textContent` **nuốt luôn chữ trong `<option>`** của select → báo nhầm "Nội dung theo dõi" thiếu 46px.
  Phải lấy riêng các text node trực tiếp. Đo lại: 7 cột báo âm 5–13px **giống hệt bản TRƯỚC khi sửa** ⇒ không phải hồi quy,
  và `th` có `white-space: nowrap; overflow: visible` nên chữ tràn ra chứ không bị cắt.

### Task 20: Đưa nút In / Xuất Excel lên góc phải thanh tiêu đề (2026-09-08)
- [x] Chuyển 2 nút từ `.market-toolbar__actions` vào `.topbar` trong `.topbar__actions` (`margin-left:auto` → dính mép phải).
- [x] Khuôn mới `.topbar-btn` (+ biến thể `--excel`): cao 26px, chữ 12px, nền trong suốt + viền trắng mờ hợp nền navy. Gỡ hẳn CSS cũ `.market-outline-btn` / `.market-export-btn` / `.market-toolbar__actions` (không còn chỗ nào dùng).
- [x] Verify vị trí: cụm nút **cách mép phải đúng 0px** sau padding 20px, **cùng hàng với tiêu đề**, **không đè icon info**.
- [x] Verify không phình chiều cao: thanh tiêu đề **vẫn 42px** như trước; toolbar **118 → 68px**; dải tổng hợp từ y=190 lên **y=140**; bảng theo dõi từ y=359 lên **y=309** ⇒ **dôi ra 50px**.
- [x] Verify màn hẹp **1280 và 1024**: nút vẫn cùng hàng tiêu đề, sát mép phải, không đè icon info, **không tràn ngang** (topbar có `flex-wrap` nên đây là điểm dễ vỡ nhất).
- [x] Verify chức năng: bấm *In báo cáo* mở đúng popup chọn kiểu in; *Xuất Excel* tải được file. **0 lỗi console**.

### Task 21: Khối tổng hợp trong popup — mặc định thu gọn, có nút như form báo cáo (2026-09-08)
- [x] Bọc 2 khối (`#drill-kpibox` KPI + `#drill-sumbox` phân bổ) vào `#drill-sumwrap`; thêm dòng đầu `.drill-sumhead` với nút dùng **chung khuôn `.rsum-toggle`** của form báo cáo.
- [x] `state.drillSumCollapsed` mặc định `true`; `openDrill()` đặt lại `true` **mỗi lần mở popup** (không mang trạng thái từ popup trước sang).
- [x] Thu gọn thì **bỏ qua luôn `renderDrillKpis` + `renderDrillSummary`** — khỏi tính khi không hiển thị.
- [x] Ẩn bằng thuộc tính `hidden` trên khối bọc thay vì `style.display`, để không đè logic tự ẩn sẵn có của `renderDrillSummary`.
- [x] Verify 4 trạng thái: mở lần đầu (ẩn · nút "Mở rộng" · bảng y=287 · `scrollHeight` 669) → bấm mở rộng (KPI 64px + chip 69px · nút "Thu gọn" · bảng y=451 · 840) → bấm thu lại (về đúng 287/669) → **mở popup KHÁC sau khi đã mở rộng vẫn thu gọn** (287/669).
- [x] Verify không hỏng thứ khác: In (14 cột) + Xuất Excel chạy được **khi đang thu gọn**; sau khi mở rộng, chip lọc nhanh vẫn lọc (160 → 26 dòng) và KPI cập nhật theo bộ lọc (73,1% — 19/26). **0 lỗi console**.
- [x] ⚠️ Bài đo hỏng đã loại: `state.drillSumCollapsed` ban đầu KHÔNG reset khi mở popup nên các lượt đo nối tiếp nhau thừa hưởng trạng thái của lượt trước → tôi gán nhầm nhãn "thu gọn"/"mở rộng" cho 2 lượt đo và tưởng `scrollHeight` chạy ngược.
  Bài đo trạng thái phải **tải lại trang hoặc ép trạng thái đầu vào**, không tin thứ tự thao tác của ca trước.

### Task 22: 4 chỉnh nhỏ trong popup (2026-09-08)
- [x] **Nhãn nút tổng hợp**: "Mở rộng" → **"Xem tổng hợp"** (giữ "Thu gọn" khi đang mở); `title` đổi theo.
- [x] **Bỏ cột "Mã meeting"** khỏi `drillColumns()` → popup còn **13 cột**; bản in + Excel của popup tự bám theo.
- [x] **Thêm sắp xếp cột "Nhân viên chủ trì"**: chỉ cần thêm `host` vào `DRILL_SORT` (so bằng `localeCompare('vi')`) là tiêu đề tự mọc nút sắp xếp. Popup nay sắp được **5 cột**.
- [x] **Icon sắp xếp → 2 mũi tên ngược chiều**: 1 SVG 2 polyline (`.drill-sort__up` / `.drill-sort__down`), bỏ cách cũ (1 mũi tên + `transform: rotate(180deg)`).
- [x] Verify nhãn nút qua 3 lượt bấm: "Xem tổng hợp" → "Thu gọn" → "Xem tổng hợp".
- [x] Verify sắp xếp theo Nhân viên chủ trì: tăng (Bùi Hải Ninh…) và giảm (Vũ Trí Thức…) **đúng thứ tự trên toàn bộ 160 dòng**; **bản in bám đúng thứ tự đang sắp**.
- [x] Verify icon bằng `opacity` lấy từ `getComputedStyle`: cột chưa sắp `0.30 / 0.30`; sắp tăng `1.00 / 0.30`; sắp giảm `0.30 / 1.00`.
- [x] Verify không hỏng: popup + bản in đều **không còn "Mã meeting"**; **0 tiêu đề bị cắt** (cột Nhân viên chủ trì nay thêm icon sort nhưng vẫn dư chỗ); **0 lỗi console**.
- [x] ⚠️ Ghi nhận lệch còn lại: `detailColumns()` — bản in *"Danh sách chi tiết meeting"* của cả báo cáo — VẪN còn cột Mã meeting vì yêu cầu chỉ nói tới popup. Chờ user chốt có gỡ nốt không.

### Task 23: Phân biệt cấp khi bung hết bảng (2026-09-08)
- [x] **Chẩn đoán bằng số** thay vì đoán: bung hết 145 dòng thì `d0/d1/d2` cha đều nền `rgb(232,242,248)` + đậm 800 (**63/145 dòng chung 1 màu**) vì `.rsum-tb__row--open td` là rule chung đè lên phân tầng `d1/d2/d3`; 2 cấp lá chênh nhau ~1% (`#fafcfe` vs `#fdfefe`).
- [x] Trình bày **3 hướng** kèm mockup → user chốt **"viền trái + kẻ tách khối"**.
- [x] Tách nền dòng cha theo cấp (`#dceaf4` / `#e9f3f9` / `#f2f8fb`), gỡ hẳn rule chung.
- [x] Vạch cấp bằng `::before` tuyệt đối (KHÔNG `border-left`, vì border nằm ở mép ô chứ không đúng chỗ thụt lề): `2 / 24 / 46 / 68px`, đậm → nhạt.
- [x] Kẻ đậm 2px `#b6d8e0` trên mỗi dòng cấp 0.
- [x] Verify tiêu chí Thị trường: **3 nền phân biệt** cho 3 cấp cha (220/233/242) thay vì 1; **4 vị trí vạch phân biệt**.
- [x] Verify tiêu chí Khách hàng (214 dòng): **56/56 khối cấp 0 đều có kẻ đậm 2px**; 4 vị trí vạch đúng.
- [x] Verify `:hover` không bị nền mới nuốt — dump `cssRules`: luật hover **cụ thể hơn (0,2,3 > 0,2,1) VÀ khai báo sau**.
- [x] ⚠️ Bài đo hỏng đã loại: gọi `browser_hover` rồi `evaluate` ở **2 lượt tool riêng** → tới lượt đo thì con trỏ đã rời bảng (`tr:matches(':hover')` đếm được 0 dòng), suýt kết luận nhầm "hover thua".
  Kiểm quyền ưu tiên CSS thì **đọc `document.styleSheets` cssRules**, đừng dựa vào trạng thái hover qua 2 lượt gọi.

### Task 24: Tiêu đề cột popup về chữ thường (2026-09-08)
- [x] `.drill-table thead th`: `text-transform: uppercase` → `none`, bỏ `letter-spacing` — khớp hàng tiêu đề bảng theo dõi (Task 8). Giữ nguyên cỡ chữ 11px và `white-space: nowrap`.
- [x] Verify **0 tiêu đề bị cắt** ở popup TỔNG (14 cột) và popup theo Thị trường; cột chật nhất còn **dư 4px** (STT), các cột chiều dư 15–97px. Hàng tiêu đề **31px**, không xuống dòng.
- [x] Verify phần lan sang: `.drill-table` dùng chung cho **bảng biên bản trong drawer** → tiêu đề drawer cũng thành chữ thường ("Nội dung / Vấn đề trao đổi"…), đúng hướng đồng bộ. **0 lỗi console**.
- [x] Ghi nhận cố ý giữ: nhãn nhóm chip `.drill-sum__label` ("THỊ TRƯỜNG" / "PHÒNG BAN") vẫn chữ hoa vì là nhãn nhóm, không phải tiêu đề cột.

### Task 25: Thêm tiêu chí Phòng ban ▸ Bộ phận ▸ Nhân viên ▸ Thị trường (2026-09-08)
- [x] User chốt **CÓ chèn cấp Bộ phận** (4 cấp) theo đúng luật "phòng nào có bộ phận thì hiện" của 2 tiêu chí cũ.
- [x] Thêm `CRITERIA.dp` (tone `dept` — dùng lại biến thể CSS cam có sẵn nhưng chưa ai dùng) + option trong `#f-criteria`.
- [x] **Gỡ 3 chỗ giả định "chỉ có 2 tiêu chí"**: `dimColumnOrder(isCus)` → đọc `CRITERIA[crit].cols`; `drillColumns` rút tiêu chí từ key bằng regex thay vì `indexOf('|cus')`; `syncCriteriaFilters` suy từ `dims` thay vì 2 nhánh `if` cứng.
- [x] Verify cả **3 tiêu chí**: 0 lỗi cộng dồn (130 / 310 / 55 dòng cha × 6 cột), dòng TỔNG 330 = tổng cấp 0 ở cả 3.
- [x] Verify ô lọc theo tiêu chí: mk → Thị trường · cus → Khách hàng · dp → Thị trường. Nhãn bộ chọn cấp tự đổi: *Chỉ Phòng ban · Đến Bộ phận · Đến Nhân viên · Tất cả cấp (đến Thị trường)*.
- [x] Verify popup tiêu chí mới: thứ tự cột `Phòng ban · Bộ phận · Nhân viên · Thị trường · Khách hàng`; popup theo Phòng ban bỏ đúng cột Phòng ban + Bộ phận; **bản in khớp popup**. **0 lỗi console**.

### Task 26: Data demo — 3-5 NV/đơn vị · mỗi NV 4-5 thị trường (2026-09-08)
- [x] Nhân viên: chu kỳ 5·6·7 → **3·4·5** ⇒ 63 → **43 người**, 11 đơn vị đều 3–5 (verify min 3 / max 5).
- [x] Thêm `EMPLOYEES[].markets` — 4–5 thị trường phụ trách, chia cố định (bước nhảy 3 trên vòng 10 tỉnh), **không gọi `demoRnd`**.
- [x] **Viết lại bộ sinh meeting**: chạy theo *nhân viên ▸ thị trường* thay vì *theo khách hàng*. Cách cũ gán mỗi KH 1 chủ nhà + đồng nghiệp cùng phòng nên một nhân viên chỉ chạm 1–2 thị trường → cấp Thị trường của tiêu chí mới gần như chỉ 1 nhánh.
- [x] Ép **ít nhất 1 meeting rơi vào tháng của `TODAY`** cho mỗi cặp (nhân viên × thị trường) → yêu cầu "4–5 thị trường" nhìn thấy được **ngay ở kỳ mặc định**, không phải đổi kỳ mới thấy.
- [x] `isFirst` chuyển sang tính SAU khi có toàn bộ meeting (meeting sớm nhất của mỗi KH) vì vòng lặp không còn chạy theo khách hàng.
- [x] Verify đúng mục tiêu: **43/43 nhân viên có 4–5 nhánh thị trường** (22 người 4 · 21 người 5), min 4 max 5.
- [x] Verify tính đúng đắn: 0 lỗi cộng dồn ở cả 3 tiêu chí; kỳ "Năm nay" cho **KH mới = 60 = đúng số khách hàng** (mỗi KH đúng 1 meeting đầu tiên).
- [x] ⚠️ Ghi nhận đánh đổi: kỳ mặc định gom **330/661 meeting (~50%)** vì mỗi cặp (NV × thị trường) đều bị ép 1 meeting vào tháng này. Tỷ lệ HT tháng này lên 81,5% (trước 65%).
- [x] ⚠️ Lỗi tự gây khi sửa: gọi `MARKET_NAME` — một biến KHÔNG tồn tại (nhầm với `MARKET_BY` ở khối script sau). Đã thay bằng map dựng tại chỗ từ `MARKETS`.

## Phase 3 — Chốt 5 mục treo + bộ cột popup (2026-09-13)

### Task 27: Đổi nghĩa "KH mới" · BỎ cột "Đã thực hiện" (2026-09-13)
- [x] **"KH mới" = khách hàng được TẠO trong kỳ**, tính cho **NGƯỜI TẠO** KH (user chốt phương án B trong 3 phương án đưa ra), thị trường lấy theo thị trường của KH. Bỏ hẳn mốc cũ "meeting đầu tiên với KH" (`isFirst`).
- [x] Data demo: thêm `CUSTOMERS[].createdAt` + `createdBy` (= `ownerId`), sinh bằng **công thức theo số thứ tự** `ageDays = (i%5===0) ? (i*7)%26 : 30+(i*53)%400` — KHÔNG gọi `demoRnd` nên chuỗi LCG giữ nguyên.
- [x] **Bản ghi giả cho KH mới**: mỗi KH tạo trong kỳ gói thành 1 record mang đủ chiều (`customerId · marketId của KH · hostId = người tạo · departmentId/teamId của người tạo`), chạy qua ĐÚNG bộ `DIM` khi dựng cây ⇒ node tự mọc cho nhân viên/thị trường không có meeting, số vẫn cộng dồn theo cấp.
- [x] `buildTree` tách 2 rổ tại node: `items` (meeting thật) / `news` (KH mới) ⇒ popup · drawer · bản in · Excel **không thấy bản ghi giả**.
- [x] `metrics(list, news)` — bỏ `done`, `newCus` lấy từ rổ `news`.
- [x] Popup "KH mới" thành **danh sách KHÁCH HÀNG**: cột `STT · Khách hàng · Thị trường · Phòng ban · Bộ phận · Người tạo KH · Ngày tạo KH`; ẩn 2 ô lọc Loại meeting / Trạng thái; bỏ 3 hộp KPI; Excel `Danh-sach-khach-hang-moi.xls`.
- [x] KPI "Tỷ lệ phát triển KH mới" → **ô chỉ có SỐ** `kpiNum()` (mẫu số cũ "KH đã tiếp cận" không còn bao được tử số vì KH mới có thể chưa có meeting nào ⇒ chia ra vượt 100%).
- [x] **Bỏ cột "Đã thực hiện"** (user: *sai về ý nghĩa theo dõi*) — bảng còn **9 cột**, gỡ khỏi màn + bản in + Excel + chỉ tiêu popup + CSS `.rsum-tb__done`.
- [x] Verify: KH mới **12 (tháng) · 20 (quý) · 44 (năm)** khớp đúng công thức sinh data tính độc lập; **0 sai lệch / 3018 ô** cộng dồn cha–con ở cả 3 tiêu chí; số liệu meeting cũ **không xê dịch** (330 · 90 nhu cầu · 1177,5 tỷ).
- [x] ⚠️ Đo được **8 dòng** ở tiêu chí Thị trường có *Meeting KH = 0* — đúng ý đồ "đẻ thêm dòng cho người tạo KH không có meeting", tất cả đều có *KH mới > 0*.
- [x] ⚠️ Đính chính tài liệu: bung hết cấp là **331 / 590 / 256 dòng** (Thị trường / Khách hàng / Phòng kinh doanh), con số *145 / 214* ghi ở Task 23 là SAI.

### Task 28: 3 mục treo còn lại — kẹp trần ngày tạo · bỏ Mã meeting · chip KH mới (2026-09-13)
- [x] **Kẹp trần** `createdAt = min(ngày họp − (1..28) ngày, TODAY)` ⇒ kỳ tương lai *Lập trong kỳ* = **0** (đo: Tuần tiếp theo 23/0 · Tháng tiếp theo 64/0; trước khi sửa là 8 và 75).
- [x] Gỡ `'code'` khỏi `detailColumns()` — bản in *"Danh sách chi tiết meeting"* hết cột **Mã meeting**, đồng bộ với popup.
- [x] **Chip "KH mới" nhảy sang cột "Tên meeting"** khi cột Khách hàng bị bỏ — cờ `DRILL_NO_CUS_COL` đặt lại trước mỗi lần dựng bảng / bản in / Excel. Đo ở popup theo Khách hàng: chip nằm ở ô *Tên meeting*.
- [x] Giữ nguyên **CỘT Thị trường ở tiêu chí Khách hàng** (user chốt lại lần 2).
- [x] ⚠️ Ghi nhận: theo nghĩa mới, chip là thuộc tính của KHÁCH HÀNG nên popup cố định 1 KH thì **mọi dòng đều mang chip** (12/12) — bản cũ chỉ 1 dòng. Chưa xử lý, xem *Chờ user chốt*.

### Task 29: Popup Huỷ — Lý do huỷ từ danh mục + ghi chú (2026-09-13)
- [x] **Danh mục lý do huỷ meeting** 8 mục thay 4 câu text cũ; vẫn chọn bằng `demoPick` (tiêu thụ đúng 1 số ngẫu nhiên) nên **không lệch số liệu cũ**.
- [x] **Ghi chú huỷ** `CANCEL_NOTES` chọn theo công thức `seq % 3 === 0` (không gọi `demoRnd`) — đo **11/29** phiếu huỷ có ghi chú.
- [x] Cột `Lý do huỷ` 2 dòng: lý do danh mục (đậm) + ghi chú (11px, `--text-muted`); drawer thêm trường *Ghi chú huỷ*.
- [x] Popup Huỷ: **Ngày tạo meeting đứng trước Ngày họp**; **bỏ cột Trạng thái** (mọi dòng đều "Huỷ"); **bỏ cột Nhu cầu + Giá trị dự kiến** (đo 0/29 dòng có số — nhu cầu chỉ ghi nhận ở meeting Hoàn thành).
- [x] ⚠️ **Lỗi đo ra, không nhìn ra**: đặt cột Lý do huỷ sau "Tên meeting" thì cột bắt đầu ở **1388px trong khung 1368px** → mở popup KHÔNG thấy cột vừa thêm. Vá tạm bằng cách đẩy lên trước "Tên meeting" + bóp còn 225px; Task 30 đảo khối cột xong thì **hoàn tác cả 2 chỗ vá** (trả về sau Tên meeting, rộng 250px).
- [x] ⚠️ `.drill-table { min-width: 1740px }` là số đo cho bảng meeting 13 cột — bảng "KH mới" chỉ 7 cột (984px) bị phình ra ngoài khung, 2 cột cuối khuất. Thêm `.drill-table--fit { min-width: 0 }`.
- [x] ⚠️ HRM thật hiện **chỉ có 1 ô `cancel_reason` nhập tay tự do** (`MeetingForm.vue`), chưa có danh mục → port thật cần 1 bảng danh mục + tách `cancel_reason_id` / `cancel_note`.

### Task 30: Đảo thứ tự cột popup — thông tin meeting lên trước (2026-09-13)
- [x] Bộ cột chia **3 khối**: (1) thông tin meeting — **Tên meeting đứng đầu** · Ngày họp · Ngày tạo meeting · Loại · Trạng thái; (2) các chiều theo dõi theo tiêu chí; (3) 2 cột số ở cuối (Nhu cầu · Giá trị dự kiến — user chọn "cuối bảng" thay vì đi liền khối meeting).
- [x] Áp cho **mọi popup meeting** + **bản in "Danh sách chi tiết meeting"**; popup "KH mới" không áp (không có cột meeting nào).
- [x] Popup Huỷ: `STT · Tên meeting · Ngày tạo meeting · Ngày họp · Lý do huỷ · Loại meeting · <các chiều>`.
- [x] ⚠️ 2 luật cũ **bị thay thế**: "Nhân viên chủ trì LUÔN trước Phòng ban" (T11) và "các chiều theo dõi dồn lên ngay sau STT" (T12/T13).
- [x] Verify: mở popup thấy ngay 6 cột đầu không phải cuộn ngang; popup Huỷ thấy trọn tới cột Lý do huỷ; chip KH mới vẫn nhảy đúng sang *Tên meeting*; bản in khớp thứ tự mới.

## Checkpoint

### Checkpoint — 2026-09-08 (WRAP UP — Task 1 → 26)

**Vừa hoàn thành**: toàn bộ Phase 1 + Phase 2, Task 1 → 26. File mockup chạy được, 1 file standalone.

Phiên 2026-09-08 làm: bỏ cột Tỷ trọng (T18) · bộ chọn cấp xem thay nút Ẩn/Hiện (T19) ·
nút In / Xuất Excel lên góc phải thanh tiêu đề (T20) · khối tổng hợp popup mặc định thu gọn (T21) ·
4 chỉnh nhỏ popup: nhãn "Xem tổng hợp", bỏ cột Mã meeting, sort cột Nhân viên, icon 2 mũi tên (T22) ·
phân biệt cấp khi bung hết bảng: vạch cấp + kẻ tách khối (T23) · tiêu đề cột popup về chữ thường (T24) ·
tiêu chí thứ 3 Phòng ban ▸ Bộ phận ▸ Nhân viên ▸ Thị trường (T25) ·
data 3-5 NV/đơn vị + mỗi NV 4-5 thị trường, viết lại bộ sinh meeting (T26).

**Quy mô data hiện tại**: 2 công ty · 10 phòng kinh doanh (lấy từ DB `hrm_erp` thật) ·
1 phòng có 2 bộ phận · 43 nhân viên (3-5/đơn vị, mỗi người 4-5 thị trường) ·
10 tỉnh/TP · 60 khách hàng · 661 meeting. Kỳ mặc định 09/2026: **330 meeting · 58 KH · 90 nhu cầu · 1177,5 tỷ**.

**Trạng thái verify**: Playwright 1440×900 (và 1280 / 1024 cho thanh tiêu đề) —
0 lỗi console · 0 tiêu đề cột bị cắt (bảng chính + popup + drawer) · không tràn ngang ·
cộng dồn cha–con đúng ở **cả 3 tiêu chí** · in / Excel khớp bộ lọc và thứ tự đang xem.

**Đang làm dở**: không có.

**Chờ user chốt** (không cái nào chặn việc khác):
1. **"KH mới" đếm cả meeting đầu tiên bị huỷ / chưa tới ngày họp**. Nếu chỉ tính khi đã thực sự gặp khách → đổi mốc sang meeting *hoàn thành* đầu tiên.
2. Ở tiêu chí Khách hàng, **CỘT** Thị trường vẫn hiện dù lặp 1 giá trị (chỉ ô LỌC đã bỏ) — có ẩn luôn cột không?
3. **Chip "KH mới" mất ở popup theo Khách hàng** (T13) vì chip nằm trong ô Khách hàng mà cột đó bị bỏ. Gắn sang cột Tên meeting, hay chấp nhận bỏ?
4. **`createdAt` ở kỳ tương lai** (T15): có kẹp `createdAt = min(createdAt, TODAY)` để "Lập trong kỳ" = 0 ở kỳ tương lai không?
5. **Bản in "Danh sách chi tiết meeting" của cả báo cáo vẫn còn cột Mã meeting** (T22) — chỉ popup đã bỏ. Gỡ nốt cho đồng bộ?
6. **Tiêu đề bảng biên bản trong drawer cũng thành chữ thường** (T24) do dùng chung `.drill-table` — giữ hay tách riêng?
7. **Kỳ mặc định gom 330/661 meeting (~50%)** vì mỗi cặp (NV × thị trường) bị ép 1 meeting vào tháng này (T26). Nếu chỉ cần "4-5 thị trường" đúng trên toàn bộ dữ liệu thì giãn ra được.
8. **Dòng popup cao 2 hàng ở ~99% dòng** — do cột *Tên meeting* + *Khách hàng*, KHÔNG phải do đổi data thật (T17b). Muốn gọn thì nới 2 cột đó.
9. Nguồn dữ liệu THẬT cho `created_at` của phiếu meeting và cờ "KH mới phát triển".
10. RESPONSIVE (chưa làm) → port Vue thật sang `hrm-client`.

### Checkpoint — 2026-09-13 (WRAP UP — Task 27 → 30)

**Vừa hoàn thành**: Phase 3, Task 27 → 30. **Mockup ĐÃ ĐƯỢC USER DUYỆT** (13/09/2026).

Phiên 13/09 làm: chốt 5 mục treo từ checkpoint 08/09 + 4 yêu cầu mới phát sinh trong lúc duyệt.
- Mục treo 1 → **đổi nghĩa "KH mới"** thành *KH được tạo trong kỳ, tính cho người tạo* (T27)
- Mục treo 2 → giữ cột Thị trường ở tiêu chí Khách hàng (T28)
- Mục treo 3 → chip "KH mới" nhảy sang cột Tên meeting (T28)
- Mục treo 4 → kẹp trần `createdAt`, kỳ tương lai *Lập trong kỳ* = 0 (T28)
- Mục treo 5 → bỏ Mã meeting khỏi bản in chi tiết (T28)
- Mới: **bỏ cột "Đã thực hiện"** (T27) · popup Huỷ đổi thứ tự ngày + **cột Lý do huỷ danh mục + ghi chú** (T29) · **đảo khối cột popup**, Tên meeting đứng đầu (T30)

**Quy mô data**: không đổi — 661 meeting; kỳ mặc định 09/2026 **330 meeting · 58 KH · 90 nhu cầu · 1177,5 tỷ**,
thêm **12 KH mới**. Bảng theo dõi còn **9 cột**.

**Trạng thái verify** (Playwright, đo bằng số lấy từ DOM): 0 lỗi console ·
cộng dồn cha–con **0 sai lệch / 3018 ô** ở cả 3 tiêu chí · KH mới 12/20/44 khớp công thức data ·
kỳ tương lai *Lập trong kỳ* = 0 · popup Huỷ 29/29 dòng có lý do, 11 dòng có ghi chú, cột nằm trọn trong khung ·
popup KH mới 7 cột vừa khung không cuộn ngang · bản in 3 chế độ đúng bộ cột mới.

**Đang làm dở**: **lên plan triển khai code THẬT** — mới khảo sát xong codebase, CHƯA viết file plan.

Đã khảo sát được (dùng lại khi quay lại):
- Khuôn màn anh em gần nhất: `Modules/Assign/Services/Report/MeetingByMarketService.php` (988 dòng) +
  `MeetingByMarketReportController.php` + `Modules/Assign/Export/MeetingByMarketExport.php`;
  route ở `Modules/Assign/Routes/api.php` (~dòng 1015); FE `pages/assign/report/meeting-by-market/`.
- **"KH mới" ĐÃ CÓ SẴN** ở `MeetingByMarketService::getSummary()` — dùng `customers.created_at` bên ERP,
  gán vào meeting qua `attachProvinceInfo()` (trường `customer_created_at`), KHÔNG mở thêm query.
- **Người tạo KH**: ERP `customers.created_by` → ERP `employees.id` (auth model ERP = `App\Employee`) →
  nối sang HRM qua **`employee_info_id`** (`TpEmployee2` ↔ HRM `employees`). Chưa đo độ phủ của mapping này.
- Thị trường của KH **không join xuyên DB được** trên nhánh `tpe` → batch query sang `mysql2` như
  `resolveCustomerProvinces()`; KH không resolve được gom nhóm *"Chưa xác định thị trường"*.
- Nhu cầu đầu tư: bảng **`meeting_investment_demands`** (`expected_amount`, `scope_name`).
- `meetings` đã có `host_employee_id` (nhân viên chủ trì), `cancel_reason` (**text tự do**, chưa có danh mục),
  `company_id / department_id / part_id / customer_id / meeting_type_id / start_date / status` (0-4).
- Phân quyền: 3 quyền/cấp như màn anh em, check bằng `isCurrentEmployeeHasPermission(...)`;
  seeder `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, **id lớn nhất đang dùng = 1186**.
- Xuất Excel: FE gọi thẳng URL server kèm `?token=` (KHÔNG dùng blob — lỗi Safari), xem
  `meeting-by-market/index.vue:428`.
- Menu: `hrm-client/components/menu-sidebar.js` (cụm báo cáo, ~dòng 240).
- E2E: `HRM/e2e/tests/assign/` có cả `*.spec.ts` (UI) lẫn `*.api.spec.ts`.

**Bước tiếp theo**: viết `plan.md` phần triển khai code (BE + FE + e2e) cho nhánh `tpe`.

**Blocked — 2 câu hỏi đang chờ user**:
1. **Danh mục lý do huỷ meeting có nằm trong đợt này không?** Nếu có → Phase 0: bảng `meeting_cancel_reasons`
   + seeder 8 mục, thêm `cancel_reason_id` / `cancel_note` vào `meetings`, sửa chỗ huỷ meeting trong
   `MeetingForm.vue`. Nếu không → cột "Lý do huỷ" tạm đọc `meetings.cancel_reason` (text tự do), không có ghi chú riêng.
2. **Chỗ để tài liệu**: giữ ở `.plans/gop-db/` (nằm cạnh cụm mockup anh em, giống tiền lệ
   `bao-cao-ket-qua-du-an-tkt`) hay chuyển ra `.plans/bao-cao-phat-trien-thi-truong-khach-hang/` cho đúng
   quy ước nhánh `tpe`?

**Chờ user chốt** (không chặn việc khác) — cập nhật lại từ checkpoint 08/09:
1. ~~"KH mới" đếm cả meeting đầu bị huỷ~~ → **đã giải quyết bằng T27** (đổi hẳn định nghĩa).
2. ~~Cột Thị trường ở tiêu chí Khách hàng~~ → **user chốt GIỮ**.
3. ~~Chip "KH mới" mất ở popup theo Khách hàng~~ → **đã gắn sang cột Tên meeting (T28)**. Phát sinh mới:
   chip nay **lặp ở mọi dòng** của popup cố định 1 KH (12/12) — gọn hơn thì đưa chip lên **tiêu đề popup**.
4. ~~Kẹp `createdAt`~~ → **đã kẹp (T28)**.
5. ~~Bản in còn cột Mã meeting~~ → **đã gỡ (T28)**.
6. Tiêu đề bảng biên bản trong drawer cũng thành chữ thường (T24) do dùng chung `.drill-table` — giữ hay tách?
7. Kỳ mặc định gom 330/661 meeting (~50%) vì mỗi cặp (NV × thị trường) bị ép 1 meeting vào tháng này.
8. Dòng popup cao 2 hàng ở ~99% dòng — do cột *Tên meeting* + *Khách hàng*.
9. RESPONSIVE (chưa làm) → sẽ xử lý khi port Vue thật.

---

# Phase 4 — TRIỂN KHAI CODE THẬT (bắt đầu 14/09/2026)

> Mockup đã duyệt 13/09. Phần dưới là plan code, KHÔNG còn đụng file mockup.
> Spec giao diện: `design.md` cùng thư mục + file mockup `bao-cao-phat-trien-thi-truong-khach-hang.html`.

**Mục tiêu**: dựng màn `/assign/report/customer-market-development` — theo dõi kế hoạch và kết quả
phát triển thị trường / khách hàng của Phòng ban - Nhân viên qua các cuộc meeting với khách hàng.

**Kiến trúc**: bám khuôn màn anh em `meeting-by-market` (service + controller + export + trang Nuxt),
nhưng **bỏ phần resolve thị trường sang ERP theo từng lần chạy** — thị trường được **snapshot xuống
`meetings` lúc lưu phiếu**. Cây N cấp dựng trong PHP từ tập meeting đã lọc, cộng thêm tập "khách hàng
mới" lấy bằng **đúng 1 query gộp** sang ERP.

**Nhánh**: `tpe-bao-cao-phat-trien-thi-truong-kh`, tách từ `tpe` ở **CẢ 2 repo** (`hrm-api`, `hrm-client`).

## Global Constraints (áp cho MỌI task Phase 4)

- Nhánh `tpe` → **được** dùng connection `mysql2` (ràng buộc cấm `mysql2` chỉ áp cho nhánh `gop_db`).
  Nhưng **chỉ cho phép ĐÚNG 1 query gộp** sang ERP mỗi lần chạy báo cáo (lấy KH mới). Mọi thứ khác
  phải nằm trong DB HRM. Tuyệt đối không query trong vòng lặp.
- **Màn `report/meeting-by-market` GIỮ NGUYÊN**, không sửa, không refactor dùng chung.
- Mọi task đụng giao diện **BẮT BUỘC verify Playwright trên trình duyệt thật, ĐO BẰNG SỐ LẤY TỪ DOM**.
- E2E chạy **`--workers=1`** (2 worker tranh 1 Nuxt dev server gây đỏ ngẫu nhiên); đọc dòng tổng kết,
  bộ test chạy `serial` nên 1 ca fail làm các ca sau in "did not run" chứ không phải "passed".
- Giữ nguyên **CRLF** của file đang sửa.
- Không `git stash` ở repo dùng chung; cần cách ly thì dùng worktree (và **không symlink `vendor`**).

## Quyết định đã chốt (13-14/09/2026)

| # | Quyết định |
|---|---|
| 1 | **"KH mới" = khách hàng được TẠO trong kỳ**, tính cho **NGƯỜI TẠO** KH; thị trường lấy theo thị trường của KH. Không cần có meeting trong kỳ vẫn được đếm. |
| 2 | Bảng theo dõi **9 cột**, KHÔNG có "Đã thực hiện". |
| 3 | **Thị trường snapshot xuống `meetings`** (`province_id` + `province_name`), ghi **lúc lưu lần đầu**, **KHÔNG đồng bộ lại** khi KH đổi tỉnh. Meeting cũ → seeder backfill. |
| 4 | **"KH mới" đọc ERP bằng đúng 1 query gộp** theo kỳ — không snapshot được vì HRM không có bảng khách hàng riêng (màn danh mục KH của HRM ghi thẳng sang ERP qua `TpCustomer`). |
| 5 | **Danh mục lý do huỷ ĐÃ MERGE vào `tpe`** — dùng lại, không làm mới. Lý do = `cancel_reason_ref->name`, **ghi chú huỷ = `meetings.cancel_reason`** (cột text cũ). KHÔNG có cột `cancel_note`. |
| 6 | Tài liệu ở `.plans/bao-cao-phat-trien-thi-truong-khach-hang/` (đã chuyển khỏi `.plans/gop-db/` ngày 14/09). |

## Hiện trạng codebase (đã khảo sát 13-14/09, dùng lại khỏi tra lại)

- Khuôn tham chiếu: `Modules/Assign/Services/Report/MeetingByMarketService.php` (988 dòng) ·
  `Http/Controllers/Api/V1/MeetingByMarketReportController.php` · `Modules/Assign/Export/MeetingByMarketExport.php` ·
  route `Modules/Assign/Routes/api.php` (~dòng 1015) · FE `pages/assign/report/meeting-by-market/`.
- `meetings` đã có: `start_date` · `status` (0-4, hằng số `Meeting::DANG_TAO/LEN_LICH/CHOT_LICH/HOAN_THANH/HUY`) ·
  `customer_id` · **snapshot `customer_name` / `customer_code`** · `host_employee_id` (nhân viên chủ trì) ·
  `company_id` / `department_id` / `part_id` (của **người TẠO** phiếu) · `meeting_type_id` ·
  `cancel_reason` (text) · `cancel_reason_id` + `cancelled_at` (mới merge) · `created_at`.
- Nhu cầu đầu tư: bảng **`meeting_investment_demands`** (`meeting_id`, `scope_name`, `expected_amount`).
- ERP: `customers.province_id` → `provinces.name`; `customers.created_at`, `customers.created_by`.
- ⚠️ **`customers.created_by` KHÔNG đồng nhất**: KH tạo bên ERP → ERP `employees.id`; KH tạo từ HRM
  (`Modules/Assign/Services/CustomerService::writeErpCreate`, ~dòng 1393) → ghi **`employee_info_id`**.
- Nối ERP employee ↔ HRM employee qua **`employee_info_id`** (`TpEmployee2` ↔ HRM `employees`).
- Phân quyền: `isCurrentEmployeeHasPermission(...)`; seeder `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`;
  **id lớn nhất đang dùng = 1186** → quyền mới **1187-1189**. ⚠️ Seeder `truncate` cả bảng; `role_has_permissions` cần `company_id = 1`.
- Xuất Excel: FE gọi thẳng URL server kèm `?token=` (KHÔNG dùng blob — lỗi Safari), mẫu
  `meeting-by-market/index.vue:428`.
- Menu: `hrm-client/components/menu-sidebar.js` (cụm báo cáo, ~dòng 240).
- E2E: `HRM/e2e/tests/assign/` có cả `*.spec.ts` (UI) lẫn `*.api.spec.ts`.

---

## Phase 4A — Nền dữ liệu: snapshot thị trường xuống `meetings`

### Task 31: Migration 2 cột thị trường trên `meetings`
**File**: tạo `hrm-api/database/migrations/2026_09_14_000001_add_province_columns_to_meetings_table.php`

- [x] Tạo nhánh **`tpe-bao-cao-phat-trien-thi-truong-kh`** tách từ `tpe` ở **cả 2 repo** (cây sạch, 0 file thay đổi).
- [x] Tạo migration thêm `province_id` (unsignedBigInteger, nullable, after `customer_code`) và
      `province_name` (string 255, nullable, after `province_id`), kèm index `meetings_province_id_index`.
      `Schema::hasColumn` bao ngoài + index tách riêng có `hasIndex()` đọc `information_schema` → chạy lại được.
      **KHÔNG đặt foreign key** — `provinces` nằm ở DB ERP.
- [x] Comment nêu rõ: snapshot tại thời điểm lưu phiếu, KHÔNG đồng bộ khi KH đổi tỉnh; gắn mốc **`@TODO-GOPDB`**.
- [x] Chạy `php artisan migrate` (php@7.4) → **đo bằng query, không đoán**:
      `province_id | bigint unsigned | null=YES` · `province_name | varchar(255) | null=YES` ·
      index `meetings_province_id_index` = 1 dòng · vị trí cột **19 customer_code → 20 province_id → 21 province_name**.
      ⚠️ Lượt migrate này chạy kèm 1 migration của feature khác đang treo sẵn trên `tpe`
      (`2026_09_13_000001_fix_backfill_prospective_project_status_logs`) — không phải của task này.
- [x] Commit `a3a454326` (hrm-api, 1 file mới).

### Task 32: Ghi snapshot khi lưu meeting
**File**: sửa `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingController.php` (hàm `store`, ~dòng 200-240
và hàm `update`) · tạo `hrm-api/Modules/Assign/Services/MeetingMarketSnapshotService.php`

- [ ] Viết service với 1 hàm tĩnh:
```php
/**
 * Resolve tỉnh/TP của khách hàng từ ERP (1 query) để SNAPSHOT xuống meetings.
 * Chỉ gọi lúc LƯU PHIẾU — báo cáo đọc thẳng cột đã snapshot, không resolve lại.
 * Trả ['province_id' => ?int, 'province_name' => ?string]; KH không có tỉnh -> cả 2 null.
 */
public static function resolveForCustomer($customerId): array
{
    if (!$customerId) {
        return ['province_id' => null, 'province_name' => null];
    }

    $erpDb = env('DB_DATABASE_SECOND');

    $row = \App\Models\TpCustomer::query()
        ->leftJoin($erpDb . '.provinces as p', 'p.id', '=', 'customers.province_id')
        ->where('customers.id', $customerId)
        ->select(['customers.province_id', 'p.name as province_name'])
        ->first();

    if (!$row || !$row->province_id || !$row->province_name) {
        return ['province_id' => null, 'province_name' => null];
    }

    return ['province_id' => $row->province_id, 'province_name' => $row->province_name];
}
```
- [x] Viết `Modules/Assign/Services/MeetingMarketSnapshotService.php`; **nuốt exception + ghi log** khi
      ERP lỗi → không làm hỏng việc lưu meeting (seeder vá sau).
- [x] ⚠️ **ĐỔI SO VỚI PLAN**: móc vào **sự kiện `saving` của model `Meeting`** (`booted()`, không đụng
      `boot()` của `BaseModel`) thay vì sửa `store()` / `update()` của controller. Lý do: phủ MỌI đường
      ghi (tạo, sửa, đổi trạng thái, import sau này) trong 1 chỗ; gán thẳng thuộc tính nên không phụ
      thuộc `$fillable`, FE **không chèn được** giá trị giả.
- [x] Điều kiện resolve: `province_id` còn trống **HOẶC** `isDirty('customer_id')` → đúng luật "chỉ ghi
      lần đầu, KH đổi tỉnh thì không sửa số cũ".
- [x] **Verify bằng tinker trong transaction rồi rollback** (không để lại dấu vết trên DB), 3 ca:
      (1) cột trống → save tự điền `province_id=2 · "Thành phố Hà Nội"`;
      (2) đã có giá trị → save lại **KHÔNG bị ghi đè** (giữ nguyên giá trị giả 999999 cố tình đặt);
      (3) đổi sang khách hàng khác → **resolve lại đúng** `41 · "Tỉnh Ninh Bình"`.
- [x] Commit `f164e5edb`.

### Task 33: Seeder backfill thị trường cho meeting cũ
**File**: tạo `hrm-api/database/seeds/BackfillMeetingProvinceSeeder.php` (hoặc `Modules/Assign/Database/Seeders/`)

- [x] `Modules/Assign/Database/Seeders/BackfillMeetingProvinceSeeder.php`: gom `customer_id` **distinct**
      của meeting còn thiếu → hỏi ERP theo **lô 1000** → **gom tiếp theo TỈNH** để mỗi tỉnh chỉ tốn 1 câu
      `UPDATE ... whereIn('customer_id', ...)`. Không lặp từng meeting.
- [x] Chạy lại nhiều lần vẫn an toàn (chỉ đụng dòng `province_id IS NULL`).
- [x] In ra số meeting đã vá / số KH resolve được / số còn lại kèm lý do.
- [x] Chạy `php artisan db:seed --class="Modules\Assign\Database\Seeders\BackfillMeetingProvinceSeeder"`.
- [x] **Đo kết quả trên DB local**: 73 meeting có khách hàng · **73/73 đã có thị trường** ·
      63/63 khách hàng resolve được · **0 meeting còn thiếu** · **24 tỉnh** khác nhau.
- [x] **Đối chứng độc lập**: so từng dòng `meetings.province_id/province_name` với tỉnh hiện tại của KH
      bên ERP → **0 dòng lệch**.
- [x] Commit `847918fd9`.

---

## Phase 4B — Backend báo cáo

### Task 34: Service — lọc + phân quyền + tập meeting của kỳ
**File**: tạo `hrm-api/Modules/Assign/Services/Report/CustomerMarketDevelopmentService.php`

- [x] `getFilteredQuery(Request)`: `Meeting::whereNotNull('customer_id')` + `whereIn('status', [LEN_LICH,
      CHOT_LICH, HOAN_THANH, HUY])` + lọc `company_id / department_id / part_id / host_employee_id /
      meeting_type_id / status / province_id / customer_id`.
      ⚠️ Lọc nhân viên bám **`host_employee_id`** (nhân viên **chủ trì**) chứ không phải `created_by` —
      khác `MeetingByMarketService`, vì cây của màn này đi theo người chủ trì.
- [x] `resolvePeriodRange(Request)`: 8 kỳ của mockup — `today · week · nextweek · month · nextmonth ·
      quarter · year · custom`. **2 kỳ tương lai là MỚI**, `MeetingByMarketService` không có.
      Lọc meeting theo `start_date` (ngày họp).
- [x] `applyPermissionFilter($query)`: 3 cấp, copy khuôn `MeetingByMarketService:167-190`, đổi tên quyền:
      `Xem báo cáo phát triển thị trường - khách hàng theo tổng công ty / theo công ty / theo phòng ban`;
      không có quyền nào → chỉ meeting mình chủ trì hoặc mình tạo.
- [x] ⚠️ **KHÔNG resolve tỉnh** — đọc thẳng `meetings.province_id / province_name`; NULL → gom nhóm
      **"Chưa xác định thị trường"**, đẩy xuống cuối.
- [x] Verify tinker: đếm meeting trả về khớp query thủ công trên DB ở 3 kỳ khác nhau.
- [x] Commit.

### Task 35: Service — tập "khách hàng mới" (1 query gộp sang ERP)
**File**: sửa `CustomerMarketDevelopmentService.php`

- [x] `getNewCustomers(Request)`: **đúng 1 query** sang ERP lấy KH có `created_at` trong kỳ:
```php
$erpDb = env('DB_DATABASE_SECOND');

$rows = \App\Models\TpCustomer::query()
    ->leftJoin($erpDb . '.provinces as p', 'p.id', '=', 'customers.province_id')
    ->whereBetween('customers.created_at', [$from, $to])
    ->select([
        'customers.id', 'customers.fullname', 'customers.code',
        'customers.province_id', 'p.name as province_name',
        'customers.created_by', 'customers.created_at',
    ])
    ->get();
```
- [x] **Map người tạo → nhân viên HRM**, xử lý CẢ 2 kiểu `created_by` (bẫy đã đo):
      (a) coi là `employee_info_id` → tra HRM `employees` theo `employee_info_id`;
      (b) không khớp thì coi là **ERP `employees.id`** → tra `TpEmployee2` lấy `employee_info_id` → tra tiếp HRM.
      Cả 2 bước đều **query gộp theo mảng id**, không lặp.
      Không map được → gom nhóm **"Không xác định người tạo"**, vẫn hiện trên báo cáo (không nuốt số).
- [x] Mỗi KH mới dựng thành **bản ghi giả** mang đủ chiều để chạy qua cùng bộ dựng cây:
      `['is_new_customer' => true, 'customer_id', 'customer_name', 'province_id', 'province_name',
      'host_employee_id' => <người tạo>, 'department_id', 'part_id', 'created_at']`
      (phòng ban / bộ phận lấy theo **hồ sơ người tạo**, không lấy của meeting).
- [x] **ĐO NGAY độ phủ mapping** trên dữ liệu thật: `% KH mới map được sang nhân viên HRM` theo từng
      kiểu (a)/(b). Ghi số vào checkpoint. Dưới ~80% thì báo user trước khi đi tiếp.
- [x] Verify tinker: tổng KH mới của kỳ = `SELECT COUNT(*) FROM <erp>.customers WHERE created_at BETWEEN ...`.
- [x] Commit.

### Task 36: Service — cây N cấp + bộ chỉ tiêu
**File**: sửa `CustomerMarketDevelopmentService.php`

- [x] 3 tiêu chí (`CRITERIA`) đúng như mockup:
      `mk` = thị trường ▸ phòng ban ▸ bộ phận ▸ nhân viên ·
      `cus` = khách hàng ▸ phòng ban ▸ bộ phận ▸ nhân viên ·
      `dp` = phòng ban ▸ bộ phận ▸ nhân viên ▸ thị trường.
- [x] `buildTree($rows, $dims)` đệ quy: gom theo chiều đầu, **bỏ qua cấp bộ phận khi cả nhánh không ai
      có `part_id`** (không đẻ dòng "Chưa phân bộ phận" rỗng), STT phân cấp `1 ▸ 1.1 ▸ 1.1.1`.
- [x] Mỗi node tách **2 rổ**: `items` (meeting thật) và `news` (bản ghi KH mới) — đúng như mockup,
      để popup / bản in / Excel không nhìn thấy bản ghi giả.
- [x] `metrics($items, $news)` trả **9 cột**: `plan` (tổng meeting) · `comp` (Hoàn thành) · `cancel` (Huỷ) ·
      `rate` = comp/plan · `new_customers` = `count($news)` · `demand` (số meeting có ≥1 dòng
      `meeting_investment_demands`) · `invest` = `SUM(expected_amount)` · `pre` / `inp` (bổ dọc theo
      `meetings.created_at` so với đầu kỳ — dùng cho dải tổng hợp).
      **KHÔNG có `done`** (cột "Đã thực hiện" đã bỏ).
- [x] Nhu cầu + giá trị lấy bằng **1 query gộp** `meeting_investment_demands` theo `whereIn('meeting_id', ...)`,
      không lặp theo meeting.
- [x] **Verify bằng script đối chứng** (không chỉ nhìn): với 1 kỳ cụ thể, so `tổng dòng cấp 0 == dòng TỔNG`
      và `mỗi dòng cha == tổng dòng con` trên **cả 6 cột số × cả 3 tiêu chí**, kỳ vọng **0 sai lệch**.
- [x] Commit.

### Task 37: Controller + route + quyền + Excel
**File**: tạo `hrm-api/Modules/Assign/Http/Controllers/Api/V1/CustomerMarketDevelopmentReportController.php` ·
tạo `hrm-api/Modules/Assign/Export/CustomerMarketDevelopmentExport.php` ·
sửa `hrm-api/Modules/Assign/Routes/api.php` ·
sửa `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- [x] Controller 3 action bám khuôn `MeetingByMarketReportController`: `index` (data + meta.summary) ·
      `export` (Excel bảng theo dõi) · `drill` (danh sách chi tiết của 1 node + 1 chỉ tiêu).
- [x] Route trong group `assign/report`:
```php
// Báo cáo phát triển thị trường - khách hàng
Route::get('/customer-market-development', [CustomerMarketDevelopmentReportController::class, 'index']);
Route::get('/customer-market-development/drill', [CustomerMarketDevelopmentReportController::class, 'drill']);
Route::get('/customer-market-development/export', [CustomerMarketDevelopmentReportController::class, 'export']);
```
- [x] 3 quyền mới **id 1187-1189**, `group` = `'Báo cáo phát triển thị trường - khách hàng'`, `type` = 4.
      ⚠️ Seeder `truncate` cả bảng → chạy xong phải gán lại `role_has_permissions` (nhớ `company_id = 1`).
- [x] Export: dùng `maatwebsite/excel` như `MeetingByMarketExport`; **đọc skill `export-excel`** trước khi viết
      (logo, bề rộng cột, định dạng số tiền).
- [x] Verify: gọi 3 endpoint bằng token thật, đối chiếu số với script ở Task 36; test **cả có quyền lẫn
      không quyền** (chống fail-open lộ giá trị hợp đồng).
- [x] Commit.


### Kết quả đo Phase 4B (14/09/2026)

| Hạng mục | Số đo |
|---|---|
| Lọc + kỳ (T34) | Số meeting service trả về **khớp query thủ công** ở 3 kỳ: tháng 7 · quý 39 · năm 69. 0 dòng thiếu thị trường / phòng ban / người chủ trì. |
| Kỳ tương lai | `nextweek` = 21-27/09/2026 · `nextmonth` = 01-31/10/2026 (hôm nay 14/09/2026). |
| KH mới (T35) | Kỳ năm nay **3208 KH**, khớp đúng số đếm thẳng trên ERP. Map người tạo **3208/3208 = 100%**. 31 KH (1%) chưa có thị trường. |
| `created_by` 2 nghĩa | Đo trên KH tạo năm 2026: **179/179 khớp ERP `employees.id`**; 136 giá trị khớp CẢ HAI kiểu; **0 giá trị không khớp kiểu nào** ⇒ chốt ưu tiên hiểu là ERP `employees.id`. |
| Phân quyền | Tài khoản quyền tổng công ty: 69 meeting / 3208 KH mới. Tài khoản **không có quyền nào**: **0 / 0** — không fail-open. |
| Cộng dồn (T36) | **0 sai lệch / 7488 ô** (Thị trường 1302 · Khách hàng 5160 · Phòng kinh doanh 1026); tổng dòng cấp 0 = dòng TỔNG ở cả 3 tiêu chí. |
| Dải tổng hợp | Lập trước kỳ 2 + lập trong kỳ 37 = 39 tổng meeting (chia hết). |
| Endpoint (T37) | `index` 200; popup khớp cây ở dòng TỔNG, node cấp 0 và node sâu 4 cấp; `export` trả xlsx 26KB đúng định dạng Excel 2007+. |

⚠️ **Phát hiện ngoài lề**: `PermissionsTableSeeder` đang có **id trùng** — 1184/1185 dùng cho cả
"Danh mục lý do hủy cuộc họp" (dòng 942-943) lẫn "Báo cáo kết quả dự án TKT" (dòng 1070-1072),
ngoài ra còn 161 · 394 · 411. Không phải do task này; đã tránh bằng cách lấy **1187-1189**.

---

## Phase 4C — Frontend

### Task 38: Trang + bộ lọc + dải tổng hợp
**File**: tạo `hrm-client/pages/assign/report/customer-market-development/index.vue` ·
`components/CustomerMarketDevelopmentSummary.vue`

- [x] Bộ lọc: Kỳ (8 lựa chọn, mặc định **Tháng này**) · **Tiêu chí theo dõi (bắt buộc, mặc định Thị trường)** ·
      Tỉnh/TP · Khách hàng · Công ty ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên (cascade) · Loại meeting · Trạng thái · nút Xoá lọc.
      ⚠️ Ô lọc Thị trường / Khách hàng **hiện theo tiêu chí** (`dims`), ô đang ẩn phải **xoá giá trị** để không lọc ngầm.
      ⚠️ Dùng `V2BaseCompanyDepartmentFilter` thì **bind thẳng vào prop form**, KHÔNG bọc thêm `col-*`.
- [x] Dải tổng hợp: 2 khối cùng 1 hàng, mỗi khối 3 ô ngang — *Kế hoạch meeting trong kỳ* (Tổng · Lập trước kỳ ·
      Lập trong kỳ) và *Kết quả phát triển trong kỳ* (Hoàn thành · Bị huỷ · Nhu cầu). **KHÔNG có khối KPI.**
- [x] 2 nút **In báo cáo · Xuất Excel** ở góc phải thanh tiêu đề.
- [x] **Verify Playwright, đo từ DOM**: chiều cao dải tổng hợp, toạ độ bảng, đổi tiêu chí thì ô lọc ẩn/hiện
      đúng và giá trị bị xoá.
- [x] Commit.

### Task 39: Bảng theo dõi N cấp
**File**: tạo `components/CustomerMarketDevelopmentTable.vue`

- [x] **9 cột**: `STT · Nội dung theo dõi · Meeting KH · Hoàn thành · Huỷ · Tỷ lệ HT · KH mới · Nhu cầu · Giá trị dự kiến`.
- [x] 1 dòng `TỔNG` + cây N cấp, bung/thu từng dòng, **select chọn cấp xem** nằm trong ô tiêu đề cột
      "Nội dung theo dõi" (`Chỉ <cấp gốc>` · `Đến Phòng ban` · `Đến Bộ phận` · `Tất cả cấp`).
- [x] Phân biệt cấp khi bung hết: nền dòng cha **theo từng cấp** (`d0 #dceaf4 · d1 #e9f3f9 · d2 #f2f8fb`),
      vạch cấp bên trái ô tên dựng bằng `::before` (KHÔNG dùng `border-left` của `td`), kẻ đậm 2px trên mỗi dòng cấp 0.
- [x] Tiêu đề cột **viết hoa chữ đầu, không xuống dòng**; mọi diễn giải nằm trong tooltip icon `i`
      (đọc skill `info-icon-tooltip`).
- [x] Ô số bằng 0 làm mờ, khác 0 thì bấm được → mở popup.
- [x] **Verify Playwright**: 0 tiêu đề bị cắt, không tràn ngang, và **cộng dồn cha = tổng con trên 6 cột số
      × 3 tiêu chí = 0 sai lệch** (đo lại trên DOM thật, không tin số BE).
- [x] Commit.

### Task 40: Popup chi tiết (3 biến thể) + drawer
**File**: tạo `components/DrillModal.vue` · dùng lại drawer chi tiết meeting sẵn có

- [x] Bộ cột **3 khối** (luật số 4 trong `design.md`): (1) thông tin meeting — **Tên meeting đứng đầu** ·
      Ngày họp · Ngày tạo meeting · Loại meeting · Trạng thái; (2) các chiều theo dõi theo tiêu chí;
      (3) 2 cột số cuối bảng — Nhu cầu · Giá trị dự kiến.
- [x] **Bỏ cột của cấp đã cố định** (mọi dòng cùng 1 giá trị) + bỏ cột Bộ phận khi popup không có dòng nào
      thuộc bộ phận; chip "KH mới" **nhảy sang cột Tên meeting** khi cột Khách hàng bị bỏ.
- [x] Biến thể **Huỷ**: `STT · Tên meeting · Ngày tạo meeting · Ngày họp · Lý do huỷ · Loại meeting · <các chiều>`.
      Ô *Lý do huỷ* 2 dòng: **`cancel_reason_ref->name`** (đậm) + **`cancel_reason`** (ghi chú, 11px xám).
      Bỏ cột Trạng thái / Nhu cầu / Giá trị dự kiến.
- [x] Biến thể **KH mới**: danh sách KHÁCH HÀNG — `STT · Khách hàng · Thị trường · Phòng ban · Bộ phận ·
      Người tạo KH · Ngày tạo KH`; ẩn 2 ô lọc Loại meeting / Trạng thái; bỏ 3 hộp KPI; bảng **vừa khung**
      (không để `min-width` của bảng meeting làm khuất 2 cột cuối).
- [x] Khối tổng hợp trong popup **mặc định THU GỌN**, nút "Xem tổng hợp" / "Thu gọn".
- [x] Sắp xếp được ở các cột ngày / thị trường / phòng ban / nhân viên; in + Excel của popup **bám đúng thứ tự đang sắp**.
- [x] **Verify Playwright, đo từ DOM**: với popup Huỷ phải đo `getBoundingClientRect()` của cột *Lý do huỷ*
      nằm **trọn trong khung** ngay khi mở (bẫy đã dính 1 lần ở mockup: cột mới thêm bị đẩy ra ngoài 1388px/1368px).
- [x] Commit.

### Task 41: Bản in · Xuất Excel · Menu · Phân quyền FE
**File**: tạo `print.vue` (hoặc dùng `ReportPrintPreviewModal` theo skill `print-page`) ·
sửa `hrm-client/components/menu-sidebar.js`

- [x] Bản in 2 chế độ: *Bảng theo dõi* (luôn xuất **đủ mọi cấp**, không phụ thuộc cấp đang xem trên màn) và
      *Danh sách chi tiết meeting* (**KHÔNG có cột Mã meeting**).
- [x] Xuất Excel: gọi **thẳng URL server kèm `?token=`**, KHÔNG dùng `blob` + `<a download>` (lỗi Safari/webview
      ra file UUID không đuôi).
- [x] Menu "Phát triển thị trường - Khách hàng" vào cụm báo cáo, cạnh "Kết quả meeting theo thị trường".
- [x] Gate màn bằng 3 quyền mới; **không có quyền nào thì không hiện menu và chặn cả route**.
- [x] **Verify**: vào bằng tài khoản KHÔNG quyền → đo DOM đảm bảo **không render dữ liệu** (vào được trang
      ≠ gate còn sống); tài khoản có quyền cấp phòng ban → chỉ thấy dữ liệu phòng mình.
- [x] Commit.

---

## Phase 4D — Kiểm thử + tài liệu

### Task 42: E2E
**File**: tạo `HRM/e2e/tests/assign/customer-market-development.api.spec.ts` và `customer-market-development.spec.ts`

- [x] `api.spec`: cộng dồn cha = tổng con trên 6 cột số × 3 tiêu chí · kỳ tương lai *Lập trong kỳ* = 0 ·
      KH mới của kỳ khớp `COUNT(*)` trên `customers` · **ca không quyền trả 403 / rỗng**.
- [x] `spec` (UI): đổi tiêu chí → cột và ô lọc đổi đúng · bung "Tất cả cấp" không vỡ · popup Huỷ có cột
      Lý do huỷ 2 dòng · popup KH mới đúng 7 cột · bản in không còn Mã meeting.
- [x] Chạy **toàn bộ** bộ test của màn: `npx playwright test tests/assign/customer-market-development --workers=1`,
      đọc **dòng tổng kết** (bộ test chạy `serial`, 1 ca fail làm các ca sau in "did not run").
- [x] Commit.

### Task 43: Tài liệu + wrap up
- [x] Cập nhật `design.md`: thêm mục *Hiện thực* (tên bảng/cột mới, endpoint, tên 3 quyền, chỗ snapshot).
- [x] Ghi checkpoint vào `plan.md` + cập nhật `.plans/STATUS.md`.
- [x] SRS + testcase: **chỉ làm khi user yêu cầu** (theo skill `srs-documenter` / `testcase-documenter`).

---


### Kết quả đo Phase 4C + 4D (14/09/2026)

| Hạng mục | Số đo |
|---|---|
| Bảng theo dõi | **9 cột**, không còn "Đã thực hiện". Bung *Tất cả cấp* ở kỳ quý này: **461 dòng · 217 dòng cha · 0 sai lệch / 1302 ô**; tổng dòng cấp 0 = dòng TỔNG ở cả 6 cột; **không tràn ngang**. |
| Định dạng | Tỷ lệ hiển thị chuẩn VN (`51,3%`) — bản đầu ra `51.3%`, đã sửa. |
| Popup meeting | 13 cột, 6 cột đầu đúng thứ tự `STT · Tên meeting · Ngày họp · Ngày tạo · Loại · Trạng thái`, 2 cột số ở cuối. 39 dòng khớp cây. |
| Popup KH mới | **7 cột** đúng spec, không còn cột nào của meeting. 344 dòng. |
| Popup theo node | Node *Thành phố Hà Nội*: **bỏ đúng cột Thị trường** còn 12 cột, 15 dòng khớp cây, tiêu đề nêu đúng đối tượng. |
| Popup Huỷ | Ngày tạo trước Ngày họp · cột **Lý do huỷ 2 dòng** (`Hủy do khách không gặp` + ghi chú) · bỏ cột Trạng thái/Nhu cầu/Giá trị · cột nằm **trọn trong khung** ngay khi mở (left 593 / khung 1108). |
| E2E | **18/18 xanh** (`--workers=1`): 3 setup · **10 API** · **5 UI**. |

### ⚠️ Lỗi hiệu năng phát hiện khi chạy e2e (đã sửa)

Ca "Dải tổng hợp" đỏ vì **request kỳ Năm nay quá 30 giây**. Đo lại bằng `curl`:

| Kỳ | Trước | Sau |
|---|---|---|
| Tháng này | 3,926s | **0,203s** |
| Quý này | 2,250s | **0,134s** |
| Năm nay | **25,906s** | **0,175s** |

Nguyên nhân: `isCurrentEmployeeHasPermission()` chạy **1 query mỗi lần gọi**, mà gate quyền của
cột "KH mới" hỏi theo **TỪNG DÒNG khách hàng** — kỳ Năm nay có 3208 khách hàng ⇒ ~10.000 query.
Sửa bằng memo cấp quyền + danh sách phòng ban/bộ phận quản lý vào thuộc tính service.
Đây đúng là **rủi ro #3** đã ghi trước khi code, nhưng nguyên nhân thật khác dự đoán (không phải
do dựng cây trong PHP mà do gate quyền).

## Rủi ro đã biết (đọc trước khi code)

1. **Độ phủ mapping người tạo KH** (Task 35) — `customers.created_by` có 2 nghĩa. Chưa đo trên dữ liệu thật.
   Nếu thấp, cột "KH mới" sẽ dồn nhiều vào nhóm "Không xác định người tạo" → phải báo user trước khi đi tiếp.
2. **Độ phủ backfill thị trường** (Task 33) — KH không có `province_id` bên ERP sẽ rơi vào "Chưa xác định thị trường".
   Đo và báo con số, đừng để user tưởng là lỗi.
3. **Khối lượng meeting** — báo cáo phải load **toàn bộ** meeting của kỳ để dựng cây (không phân trang được).
   Đo thời gian chạy ở kỳ "Năm nay" trên dữ liệu thật; chậm thì gom chỉ tiêu bằng SQL thay vì PHP.
4. **`meetings.department_id / part_id` là của NGƯỜI TẠO phiếu**, không phải người chủ trì. Màn CSKH tiềm năng
   đã từng phải đổi sang lấy theo **hồ sơ người chủ trì** (`employee_infos`). Cây của màn này đi theo
   **người chủ trì** ⇒ phải lấy phòng ban/bộ phận theo hồ sơ `host_employee_id`, KHÔNG dùng 2 cột trên `meetings`.

---

## ⚠️ NỢ KỸ THUẬT — PHẢI ĐỔI KHI MERGE SANG NHÁNH GỘP DB

**Đọc mục này TRƯỚC KHI merge feature vào `gop_db`** (hoặc bất kỳ nhánh nào đã gộp DB ERP + HRM).

Lý do: trên nhánh `tpe`, `customers` / `provinces` nằm Ở **DB ERP khác** nên phải đi vòng
(`mysql2` + snapshot). Khi gộp DB thì khách hàng **nằm cùng 1 database** ⇒ cả 2 chỗ vòng này
thành thừa, và phải đổi lại nếu không số liệu sẽ **sai âm thầm** (`mysql2` trỏ DB ERP CŨ, id lệch).

| Chỗ phải đổi | Hiện tại (nhánh `tpe`) | Sau khi gộp DB |
|---|---|---|
| Cột **KH mới** (Task 35) | 1 query gộp sang `mysql2` lấy `customers` tạo trong kỳ | **Join thẳng** `customers` trong cùng DB, bỏ `env('DB_DATABASE_SECOND')` và bỏ `TpCustomer` |
| **Người tạo KH** (Task 35) | map 2 kiểu `created_by` (ERP `employees.id` **hoặc** `employee_info_id`) qua `TpEmployee2` | Join thẳng sang bảng nhân viên đã gộp — nhưng **vẫn phải giữ nhánh xử lý 2 kiểu `created_by`**, vì dữ liệu cũ đã lỡ ghi lẫn 2 nghĩa |
| **Snapshot thị trường** (Task 31-33) | 2 cột `meetings.province_id` / `province_name` ghi lúc lưu phiếu | **Giữ nguyên 2 cột** (báo cáo phản ánh thị trường TẠI THỜI ĐIỂM họp — đã chốt 14/09). Chỉ đổi `MeetingMarketSnapshotService::resolveForCustomer()` sang join thẳng, bỏ `mysql2` |

**Cách tìm lại các chỗ này trong code**: mọi đoạn đụng ERP của feature này phải gắn sẵn
comment mốc `@TODO-GOPDB` ngay trên dòng query — khi merge chỉ cần:

```bash
grep -rn "@TODO-GOPDB" hrm-api/Modules/Assign
```

Đây là **bước bắt buộc của Task 32 / 35 / 33** — code không có mốc `@TODO-GOPDB` thì coi như task chưa xong.

### Task 44: Sửa bộ chọn cấp xem vỡ trong ô tiêu đề (14/09/2026)
- [x] User báo "lỗi UI ở select chọn cấp xem". **Tái hiện + đo TRƯỚC khi sửa**, ra **3 lỗi**:
      (1) ô cao **32px** trong khi vùng nội dung ô tiêu đề chỉ **26px** → hộp trắng đè lên viền ô;
      (2) ô rộng **356px / cột 480px = 74%** → nuốt gần hết cột "Nội dung theo dõi";
      (3) **dropdown bị cắt**: render bên trong `.market-table-wrap` mà `overflow-x: auto` cắt cả
      trục dọc → dropdown thò quá đáy khung **24px**, 2 lựa chọn cuối không bấm được.
- [x] Nguyên nhân gốc: mockup đặt select trong `<th>` được vì dùng **`<select>` HTML thuần**
      (dropdown do trình duyệt vẽ, không dính khung cuộn); màn thật bắt buộc dùng **V2BaseSelect
      (select2)** nên không đặt trong `<th>` của bảng có khung cuộn được.
- [x] Sửa: đưa bộ chọn ra **thanh nhỏ ngay TRÊN bảng**, canh phải, nhãn "Cấp xem", rộng 240px.
- [x] ⚠️ **Ca e2e đầu tiên XANH OAN**: viết theo kỳ "Quý này" (bảng 33 dòng) nên dropdown lọt vừa,
      không tái hiện được. Phải viết lại theo **kỳ mặc định** (bảng 4 dòng) mới đỏ đúng chỗ.
- [x] Thêm 2 ca e2e cho bộ chọn cấp; chạy lại **TOÀN BỘ** bộ test của màn: **20/20 xanh**.
- [x] Commit `8a9359327` (hrm-client).

### Task 45: Dòng hiện "—" thay vì tên (14/09/2026)
- [x] User hỏi "tại sao có phòng hiện -". **Đo trước khi sửa**, ra **2 lỗi cùng loại**:
      (1) **Phòng ban**: 1 dòng cấp 0 mang `department_id = 1`, mà bảng `departments` chỉ có
      **id 5-126** (84 dòng, không có id 1) → tra tên không ra → fallback `'—'`. 5 hồ sơ nhân viên
      **fixture e2e** đang trỏ tới phòng ban ma này, kéo theo **10 meeting**.
      (2) **Khách hàng**: **44 dòng không tên** ở tiêu chí Khách hàng — cột snapshot
      `meetings.customer_name` có thể NULL dù `customer_id` trỏ tới KH thật; đo **47/73 meeting
      (64%)** bỏ trống, thuộc **42 khách hàng mà cả 42 đều còn bên ERP**.
- [x] Sửa (1): id trỏ tới danh mục đã mất → đưa về null để **GOM vào nhóm "Chưa xác định …"**,
      không đẻ dòng riêng mang nhãn vô nghĩa. Cùng luật đã áp cho thị trường.
- [x] Sửa (2): **snapshot tên/mã KH lúc lưu phiếu** (`resolveForCustomer` trả thêm `fullname`/`code`,
      model bù khi 2 cột trống) + **mở rộng seeder backfill** vá dữ liệu cũ → vá **47/47 meeting**.
- [x] Nhãn thay thế nói rõ vấn đề: *Khách hàng không xác định* · *Nhân viên không xác định* ·
      *Chưa có người chủ trì*.
- [x] ⚠️ Lỗi (2) **do chính ca e2e mới viết cho lỗi (1) phát hiện ra** — nếu chỉ sửa đúng chỗ user
      hỏi thì 44 dòng không tên vẫn còn.
- [x] Đo lại: **0 dòng "—"** ở cả 3 tiêu chí · 10 meeting kia nằm trong "Chưa xác định phòng ban" ·
      tổng KHÔNG đổi (69 meeting · 3208 KH mới). Toàn bộ bộ test của màn: **21/21 xanh**.
- [x] Commit `7d48cf802` (hrm-api).

### Task 46: Soát UI theo mockup + màn dự án TKT (14/09/2026)
- [x] ⚠️ **Tự phê**: 5 ca e2e UI ban đầu chỉ kiểm **dữ liệu và bộ cột**, KHÔNG kiểm chất lượng giao
      diện — nên "đã chạy Playwright" không chứng minh được UI đạt. User phải nhắc mới soát.
- [x] Mở **mockup đã duyệt song song màn thật**, đo bằng DOM. Ra 3 lỗi màn chính:
      **0/7 icon ⓘ ở tiêu đề cột · 0/9 icon ⓘ ở dải tổng hợp** (mockup có đủ) ·
      tỷ lệ lẫn lộn `14,3%` / `0%` / `100%` · tiền lẫn lộn `1,3 tỷ` / `0` (mất đơn vị).
      Sửa: thêm component `InfoTip` dùng chung đúng chuẩn skill `info-icon-tooltip`
      (`ri-information-line` 14px `#94a3b8`, `font-weight: normal`, `b-popover` `info-popover`);
      ép cả % lẫn tiền LUÔN 1 chữ số thập phân kiểu VN.
- [x] Thử mở sẵn bộ lọc cho giống mockup rồi **TRẢ LẠI thu gọn**: cụm lọc mockup cao 68px (nhãn cạnh
      ô) còn `V2BaseFilterPanel` cao 254px (nhãn trên ô) → mở sẵn thì bảng tụt y=378 → y=632, số
      dòng thấy được **18 → 10**. ⚠️ Project đang có 2 kiểu (7 màn thu gọn / 3 màn mở sẵn) — **chờ user chốt**.
- [x] **POPUP dựng lại theo khuôn chuẩn** (user chỉ tham khảo `/assign/report/prospective-project-results`).
      Popup cũ tự khai `b-modal` tay, trái skill `modal-popup` mục 0. Đo ra 5 lỗi:
      không có footer (nút Excel bị nhét lên toolbar, chữ xuống 2 dòng; không có nút Đóng) ·
      bảng 2047px trong khung 1108px mà **chỉ có thanh cuộn dưới** ·
      dialog 1140px trong màn 1680px (thừa 540px) · header tự chế, không icon tròn · dòng cao 45px.
      Sửa: dựng trên **`V2BaseModal`** + bọc bảng bằng **`V2BaseTableScroll`** + cắt 2 dòng cột chữ dài.
- [x] Đo lại popup: dialog **1400px** · footer `Xuất Excel danh sách · Đóng` **luôn trong tầm nhìn** ·
      **đúng 1** khối cuộn dọc · **có** thanh cuộn ngang phía trên · số dòng thấy được **12 → 20**.
- [x] ⚠️ **Lỗi tự gây khi sửa**: script thay `<template>` cắt nhầm vào thẻ `<template v-if>` lồng bên
      trong → file còn 68 dòng markup mồ côi, popup **không mở được** mà console KHÔNG báo lỗi
      (`$refs` rỗng là dấu hiệu duy nhất). Đã xoá và kiểm lại bằng DOM.
- [x] Thêm 3 ca e2e (icon ⓘ + định dạng số · tooltip đúng chuẩn icon · cấu trúc popup).
      Toàn bộ bộ test của màn: **24/24 xanh**.
- [x] Commit `f1b97bb6d` + `3c4d1a16b` (hrm-client).

### Task 47: Bộ lọc riêng trong popup (14/09/2026)
- [x] ⚠️ **Tự phê**: mockup có đủ bộ lọc trong popup, tôi **tự cắt cho nhanh** rồi chỉ ghi "chưa làm"
      vào `design.md` — KHÔNG hỏi user trước khi thu hẹp phạm vi. User phải hỏi mới làm.
- [x] Thêm **7 ô lọc** (Thị trường · Khách hàng · Phòng ban · Bộ phận · Nhân viên · Loại meeting ·
      Trạng thái) + ô tìm kiếm + nút *Xoá lọc*; select dùng **`V2BaseSelectInModal`** để dropdown
      không bị popup cắt (skill `modal-popup` mục 2).
- [x] 3 luật ẩn: chiều trên `path` đã cố định → bỏ ô của chính nó · cố định Khách hàng → ẩn Thị
      trường · popup "KH mới" → bỏ Loại meeting / Trạng thái. Ô bị ẩn **xoá giá trị** (chống lọc ngầm).
      Ô Bộ phận chỉ hiện khi có dòng thuộc bộ phận.
- [x] Tuỳ chọn lấy **distinct từ chính tập dòng đang xem**, không gọi danh mục đầy đủ.
- [x] Đo: TỔNG đủ **7 ô** · theo Thị trường còn **6** (bỏ đúng Thị trường) · KH mới còn **5** ·
      lọc phòng ban **39 → 1 khớp đếm tay** · xoá lọc về 39 · mở popup khác **0 giá trị còn sót**.
- [x] ⚠️ **Ca e2e cấu trúc popup (Task 46) bắt hồi quy ngay**: hàng lọc làm body cao thêm 40px →
      **2 thanh cuộn dọc lồng nhau** (bẫy skill `modal-popup` mục 3b). Hạ trần bảng còn
      `calc(70vh - 120px)`. Đây là lần ca test tự viết cứu được lỗi mình vừa tạo.
- [x] Thêm 1 ca e2e cho bộ lọc popup. Toàn bộ bộ test của màn: **25/25 xanh**.
- [x] Commit `6d6b6fec9` (hrm-client).

### Task 48: Bản in cho màn và cho popup (14/09/2026)
- [x] Theo **skill `print-page` mục 0**: nút In mở **POPUP XEM TRƯỚC** ngay tại chỗ, KHÔNG dựng
      trang `/print` (mở tab mới làm mất ngữ cảnh + bộ lọc). Màn báo cáo Vue tuy thuộc nhóm ngoại
      lệ được phép dựng `/print`, nhưng **màn anh em `prospective-project-results` đã đi đường
      popup** nên bám theo để cả họ báo cáo cùng 1 kiểu.
- [x] **BE**: endpoint `print-list-data` + `CustomerMarketDevelopmentPrintService` + 2 blade
      (`customer_market_development_summary` / `_detail`), khuôn copy `ProspectiveProjectResultPrintService`.
      Contract bắt buộc: tên endpoint `print-list-data`, khoá `template` — đổi tên là popup nhận
      rỗng mà **không báo lỗi gì**.
- [x] Số liệu **không tính lại**: gọi thẳng `getFlatRowsForExport()` / `getDrillRows()` /
      `getMeetingRows()` nên bản in – màn hình – Excel không bao giờ lệch.
- [x] Theo skill: `number_format()` **mặc định** (phẩy ngăn nghìn, chấm thập phân — mục 2d) ·
      ô lọc trống ghi **"Tất cả"** (mục 4e) · cột ngày họp trong bảng danh sách **có GIỜ** ·
      letterhead theo **công ty đang lọc**, không lọc thì theo công ty người đăng nhập (mục 4b).
- [x] **FE**: nút *In báo cáo* → `PrintOptionsModal` (2 chế độ) → `ReportPrintPreviewModal` qua
      `reportPrintPreviewMixin`. Popup chi tiết thêm nút **In danh sách** ở footer, gửi kèm node +
      chỉ tiêu + **bộ lọc riêng của popup** (đổi về đúng tên tham số của màn chính) nên bản in ra
      **đúng tập đang nhìn thấy**.
- [x] Đo trên trình duyệt: 2 chế độ hiện đúng · khổ **ngang** · có letterhead công ty · dòng mô tả
      bộ lọc có "Tất cả" · **đúng 9 cột** như màn · in **đủ mọi cấp** (463 dòng so với 33 dòng cấp 0
      đang hiện) · **chỉ 2 cỡ chữ 13px/10px** (tự kiểm của skill mục 8b) · in từ popup ra **đúng số
      dòng và đúng tên** với tập đang lọc.
- [x] ⚠️ Phép đo hụt 1 dòng lúc đầu là do **đếm cả bảng "Ngày in"** cuối bản in, không phải lỗi code.
- [x] Ca e2e cấu trúc popup lại bắt hồi quy: thêm nút *In danh sách* làm footer đổi → cập nhật kỳ vọng.
- [x] Thêm 2 ca e2e cho bản in. Toàn bộ bộ test của màn: **27/27 xanh**.
- [x] Commit `912937b32` (hrm-api) + `9c474bf9b` (hrm-client).

### Task 49: Dứt điểm nhóm "Chưa xác định phòng ban" (14/09/2026)
- [x] User hỏi vì sao vẫn còn nhóm đó. **Truy tới cùng**: cả **10/39 meeting** của kỳ rơi vào nhóm
      này đều do **đúng 1 người chủ trì** — tài khoản `E2E Assign`, hồ sơ trỏ `department_id = 1`
      mà bảng `departments` **bắt đầu từ id 5**.
- [x] Nguồn rác: **`e2e_provision.php` hard-code `department_id => 1`** cho MỌI tài khoản E2E (5 hồ sơ).
      Task 45 mới gom chúng vào nhóm "Chưa xác định phòng ban" (thay nhãn "—" vô nghĩa) chứ **chưa
      sửa nguồn** — vì là fixture dùng chung của feature khác.
- [x] ⚠️ Không phải lỗi riêng của báo cáo này: `e2e/utils/work-calendar-fixtures.ts:211` **đã phải cố ý
      loại trừ `department_id=1`** để né đúng dữ liệu bẩn đó.
- [x] Kiểm trước khi sửa: **không spec nào phụ thuộc con số 1** (các spec đọc department từ fixture).
- [x] Sửa: fixture lấy **phòng ban THẬT nhỏ nhất của công ty E2E**; nhánh "employee đã tồn tại" vá
      luôn hồ sơ cũ đang trỏ phòng ban không còn trong danh mục. Vá dữ liệu local: 5 hồ sơ → phòng
      `PHÒNG THIẾT BỊ Ô TÔ 2`.
- [x] Đo lại: **0** hồ sơ trỏ phòng ban treo · **0/39** meeting thiếu phòng ban ·
      **0 dòng "Chưa xác định phòng ban"** ở cả 3 tiêu chí.
- [x] ⚠️ Nhóm **"Chưa xác định thị trường" vẫn còn và ĐÚNG**: 0/69 meeting thiếu thị trường, nhưng
      **31/3208 KH mới** là khách nước ngoài (`MEXMON TECHNOLOGIES`, `SHENZHEN MINGWEI…`) thật sự
      không có tỉnh/TP bên ERP. Đây là dữ liệu đúng, không phải lỗi.
- [x] ⚠️ Ca `potential-customer-care.spec.ts:1005` đỏ — **kiểm A/B** bằng cách trả dữ liệu về `dept=1`
      thì VẪN đỏ y hệt (36 vs 20) ⇒ **đỏ sẵn từ trước**, không phải do thay đổi này.
- [x] Bộ test của màn: **27/27 xanh**. Commit `151b42a4e` (hrm-api).

---

### Checkpoint — 2026-09-14 (WRAP UP — Phase 4 XONG, Task 31 → 43)

**Vừa hoàn thành**: toàn bộ Phase 4 — màn báo cáo chạy được thật, có e2e.

**Nhánh**: `tpe-bao-cao-phat-trien-thi-truong-kh` tách từ `tpe` ở CẢ 2 repo. **Chưa push, chưa merge.**

**hrm-api** — 7 commit:
`a3a454326` migration 2 cột thị trường · `f164e5edb` ghi snapshot khi lưu meeting ·
`847918fd9` seeder vá thị trường meeting cũ · `285f78c89` service nền (lọc/kỳ/quyền) ·
`9e19c9567` tập khách hàng mới · `6d89b7cea` cây N cấp + chỉ tiêu ·
`f51bd3c72` controller/route/popup/Excel · `e8925b6cd` sửa hiệu năng 25,9s → 0,17s ·
`b38ae8fd9` dọn file tạm.

**hrm-client** — 1 commit: `ef3369ec3` toàn bộ FE + menu.

**e2e** — 2 spec + 1 util (⚠️ `HRM/e2e/` KHÔNG thuộc repo nào → **chỉ có trên máy này**):
`tests/assign/customer-market-development.api.spec.ts` · `.spec.ts` · `utils/cmdFixture.ts`.
Fixture PHP thì nằm trong hrm-api (`database/e2e_customer_market_dev_seed.php`) nên đã được commit.

**Đang làm dở**: không có.

**Việc người khác phải làm trước khi deploy**:
1. Chạy `php artisan migrate` (thêm 2 cột `meetings.province_id` / `province_name`).
2. Chạy `php artisan db:seed --class="Modules\Assign\Database\Seeders\BackfillMeetingProvinceSeeder"`.
3. Cấp 3 quyền **1187-1189** cho các role cần xem (seeder `PermissionsTableSeeder` đã có, nhưng
   seeder này **truncate cả bảng** nên môi trường thật thường gán tay).

**Blocked**: không có.

---

### Checkpoint — 2026-09-14 chiều (WRAP UP — Task 44 → 49)

**Vừa hoàn thành**: 6 đợt bổ sung sau khi user soát UI. Màn coi như **đủ tính năng so với mockup**,
chỉ còn 1 mục chưa làm (khối tổng hợp thu gọn trong popup).

| Task | Nội dung | Commit |
|---|---|---|
| 44 | Bộ chọn cấp xem vỡ trong ô tiêu đề → đưa ra thanh trên bảng | `8a9359327` |
| 45 | Dòng hiện "—" (phòng ban treo + 44 dòng KH không tên) | `7d48cf802` |
| 46 | Soát UI theo mockup: thiếu 16 icon ⓘ · định dạng số lệch · popup dựng lại trên `V2BaseModal` | `f1b97bb6d` · `3c4d1a16b` |
| 47 | Bộ lọc riêng trong popup (7 ô + 3 luật ẩn) | `6d6b6fec9` |
| 48 | Bản in cho màn chính + popup (popup xem trước, 2 chế độ) | `912937b32` · `9c474bf9b` |
| 49 | Dứt điểm "Chưa xác định phòng ban" — sửa `e2e_provision.php` | `151b42a4e` |

**Tổng cộng nhánh `tpe-bao-cao-phat-trien-thi-truong-kh`**: `hrm-api` **12 commit** ·
`hrm-client` **6 commit** so với `tpe`. Cây sạch ở cả 2 repo. **Chưa push, chưa merge.**

**E2E**: **27/27 xanh** (`--workers=1`) — 3 setup · 11 API · 13 UI.
⚠️ `HRM/e2e/` không thuộc repo git nào → 2 spec + `utils/cmdFixture.ts` **chỉ có trên máy này**;
fixture PHP thì đã nằm trong `hrm-api`.

**3 bài học rút ra trong ngày** (đã ghi chi tiết ở từng task):
1. **Bộ e2e UI ban đầu chỉ kiểm dữ liệu và bộ cột** → UI hỏng mà test vẫn xanh. Phải mở mockup song
   song + so với màn anh em mới lòi ra. Nay đã có ca chặn hồi quy cho khuôn popup, icon ⓘ, định dạng số.
2. **Ca test viết sai trạng thái là xanh oan**: ca đầu cho bộ chọn cấp viết theo kỳ "Quý này" (bảng
   dài) nên dropdown lọt vừa; phải viết theo **kỳ mặc định** (bảng ngắn) mới đỏ đúng chỗ.
3. **Tự cắt phạm vi mà không hỏi**: bộ lọc trong popup có trong mockup nhưng bị bỏ, chỉ ghi "chưa
   làm" vào design. Lần sau thu hẹp phạm vi phải hỏi trước.

**Đang làm dở**: không có.

**Còn thiếu so với mockup**: **khối tổng hợp thu gọn trong popup** (3 hộp KPI + dải chip phân bổ
Thị trường / Phòng ban, mặc định thu gọn — luật 0 và luật 3 của mục *Luật POPUP chi tiết*).

**Chờ user chốt**:
1. Bộ lọc màn chính **mở sẵn hay thu gọn** — project đang có 2 kiểu (7 màn thu gọn / 3 màn mở sẵn).
   Hiện để **thu gọn** vì đo được mở sẵn làm số dòng thấy được rơi 18 → 10.
2. Nhóm **"Chưa xác định thị trường"** giữ nguyên hay đổi tên — nó là **31/3208 khách hàng nước
   ngoài** thật sự không có tỉnh/TP bên ERP (dữ liệu đúng, không phải lỗi).

**Việc người khác phải làm trước khi deploy** (không đổi so với checkpoint trước):
1. `php artisan migrate` — 2 cột `meetings.province_id` / `province_name`.
2. `php artisan db:seed --class="Modules\Assign\Database\Seeders\BackfillMeetingProvinceSeeder"`
   — nay vá cả thị trường lẫn tên/mã khách hàng còn trống.
3. Cấp 3 quyền **1187-1189** cho các role cần xem.

**Blocked**: không có.

⚠️ Ca `potential-customer-care.spec.ts:1005` (phân trang popup màn CSKH) **đỏ sẵn từ trước**, đã
kiểm A/B — không phải do đợt này, chưa sửa vì ngoài phạm vi.

---

### Checkpoint — 2026-09-14 tối (ĐÃ MERGE VÀO `tpe`)

**Vừa hoàn thành**: user merge nhánh `tpe-bao-cao-phat-trien-thi-truong-kh` vào `tpe` ở CẢ 2 repo.
Kiểm chứng sau merge (không tin lời báo, đo bằng lệnh):

| Kiểm | Kết quả |
| --- | --- |
| `git branch --show-current` (2 repo) | `tpe` · `tpe` |
| `git status --porcelain` (2 repo) | rỗng — cây sạch |
| `git log tpe..tpe-bao-cao-phat-trien-thi-truong-kh` | **0 commit** ở cả 2 repo → merge đủ, không sót |
| Commit của feature nay nằm trong `tpe` | `hrm-api` 12 (`a3a454326` … `151b42a4e`) · `hrm-client` 6 (`ef3369ec3` … `9c474bf9b`) |
| Chạy lại **toàn bộ** bộ test của màn trên `tpe` | **27/27 XANH** (1.9 phút, `--workers=1`) |

**Đang làm dở**: không có.

**Bước tiếp theo — 2 việc của user, KHÔNG tự làm** (đụng remote + xoá nhánh):
1. **Push `tpe`** — local đang trước `origin/tpe`: `hrm-api` **98 commit**, `hrm-client` **86 commit**
   (phần lớn là việc của người khác đã merge từ trước, không riêng feature này).
2. **Xoá nhánh feature** `tpe-bao-cao-phat-trien-thi-truong-kh` (còn ở cả 2 repo) — chỉ nên xoá
   SAU khi đã push `tpe`, vì lúc này `tpe` chưa có ở remote nên nhánh feature là bản sao duy nhất
   ngoài máy local nếu nó đã từng được push.

**3 việc deploy** (không đổi): `migrate` → `BackfillMeetingProvinceSeeder` → cấp quyền 1187-1189.

⚠️ Nhắc lại: `HRM/e2e/` không thuộc repo git nào — 2 spec + `utils/cmdFixture.ts` **chỉ có trên máy
này**, push `tpe` KHÔNG mang chúng đi. Fixture PHP thì đã nằm trong `hrm-api`.

**Blocked**: không có.

---

## Phase 5 — Bù nốt phần còn thiếu so với mockup (14/09/2026, sau khi đã merge `tpe`)

**3 quyết định user chốt khi mở đợt này:**
1. Code **thẳng trên `tpe`** (không tách nhánh riêng).
2. Bộ lọc màn chính **GIỮ THU GỌN** — không chạy theo mockup (mockup hiện cụm lọc vì nhãn nằm
   CẠNH ô, cao 68px; `V2BaseFilterPanel` dựng nhãn TRÊN ô nên cao 254px, mở sẵn thì số dòng thấy
   được rơi 18 → 10). ⇒ **hết treo**, không còn việc phải làm.
3. Nhóm **"Chưa xác định thị trường" GIỮ NGUYÊN TÊN** — 31/3208 khách nước ngoài thật sự không có
   tỉnh/TP bên ERP, dữ liệu đúng. ⇒ **hết treo**, không còn việc phải làm.

⇒ Phạm vi Phase 5 rút lại còn ĐÚNG 1 phần thiếu thật: **khối tổng hợp thu gọn trong popup**
(luật 0 + luật 3 của mục *Luật POPUP chi tiết*), cộng 1 lỗi chuẩn số tự phát hiện.

- [x] **Task 50** — `index.vue`: tìm node đang mở popup trên cây, truyền `node-metrics` xuống
      `DevelopmentDrillModal` (cần `new_customers` của nhánh; dòng TỔNG thì lấy `total`).
      Số KH mới **KHÔNG đổi theo bộ lọc trong popup** vì KH mới không gắn với meeting nào.
- [x] **Task 51** — Modal: dòng đầu `.cmd-drill-sumhead` ("Tổng hợp danh sách đang xem" + nút
      `.rsum-toggle` dùng chung khuôn với khối tổng hợp màn chính). **MẶC ĐỊNH THU GỌN**, reset về
      thu gọn MỖI lần mở popup. Nhãn nút: *Xem tổng hợp* ↔ *Thu gọn*.
- [x] **Task 52** — 3 hộp KPI (port `.rsum-kpi` của mockup): *Tỷ lệ hoàn thành meeting* (main) ·
      *KH mới tạo trong kỳ* (good, chỉ số, không có tỷ lệ) · *Tỷ lệ meeting huỷ* (bad).
      Tính trên **tập ĐANG LỌC** trong popup. Popup "KH mới" **bỏ hẳn 3 hộp** (đều tính trên meeting).
- [x] **Task 53** — Dải chip "Phân bổ meeting theo cơ cấu": **chỉ Thị trường + Phòng ban**, chip
      `tên · số · %`, bấm chip = bật/tắt ô lọc tương ứng. Ẩn chiều đã cố định (cùng luật với ô lọc:
      cố định Khách hàng ⇒ ẩn cả Thị trường). Không còn chiều nào thì ẩn cả khối.
- [x] **Task 54** — Sửa **định dạng số** cho đúng chuẩn quốc tế của CLAUDE.md (`1,234.5`):
      5 chỗ còn `toLocaleString('vi-VN')` ở `DevelopmentTable.vue` (2) · `DevelopmentSummary.vue` (2) ·
      `DevelopmentDrillModal.vue` (1). Tự kiểm bằng lệnh grep trong CLAUDE.md phải RỖNG cho màn này.
- [x] **Task 55** — e2e: thêm ca đo DOM cho khối tổng hợp popup (mặc định thu gọn · bấm mới dựng ·
      3 KPI · chip lọc thật sự · ẩn chiều cố định · KHÔNG đẻ thanh cuộn dọc thứ 2), cập nhật 2
      assertion định dạng số, chạy lại **TOÀN BỘ** bộ test của màn.
- [x] **Task 56** — Cập nhật `design.md` (3 quyết định vừa chốt) + `STATUS.md`.

### Checkpoint — 2026-09-14 tối muộn (Phase 5 XONG, Task 50 → 56)

**Vừa hoàn thành**: khối tổng hợp trong popup + sửa định dạng số. Chỉ đụng **4 file FE**
(`hrm-client`), **KHÔNG** đụng backend, không migration, không quyền mới.

| Kiểm bằng số đo từ DOM (Playwright MCP, 1920×1080 + 1366×768) | Kết quả |
| --- | --- |
| Mở popup → khối tổng hợp thu gọn, chưa dựng nội dung | ✅ mọi popup, kể cả mở popup khác khi đang mở |
| Thân popup tràn dọc (trước khi sửa: 9px thu gọn / 21px mở rộng) | **0px** ở cả 2 trạng thái |
| Số khối cuộn dọc trong popup | **1** (danh sách ngắn thì 0) |
| Trần bảng tự co giãn | 627 ↔ 467px (1920) · 584 / 593 / 530px tuỳ popup · 248–263px (1366) |
| 3 hộp KPI, mỗi hộp 1 icon ⓘ | ✅ `53.7%` (22/41) · `344` KH · `0.0%` (0/41) |
| Chip: số trên chip = số dòng lọc ra | ✅ Hà Nội 15 → bảng còn 15 dòng, cột Thị trường đồng nhất 1 giá trị |
| Chip ẩn theo luật ẩn của ô lọc | TỔNG: 2 dải · theo Thị trường: còn *Phòng ban* · theo Thị trường›Phòng ban: ẩn cả khối |
| Popup *KH mới* | 0 hộp KPI, còn 2 dải chip, tiêu đề *Phân bổ khách hàng theo cơ cấu* |
| Dải chip dài | tự cuộn ngang trong chính nó (2601px trong khung 1295px), không nới rộng popup |

**2 lỗi tự phát hiện khi đo, đã sửa:**
1. **Thân popup tràn → 2 thanh cuộn dọc lồng nhau.** Hằng số `calc(70vh - 120px)` không còn đúng khi
   có thêm khối tổng hợp. Thay bằng `syncTableHeight()` đo thật ngân sách chiều cao.
2. **Watcher đo nhầm trạng thái CŨ**: `$nextTick` trong watcher chạy TRƯỚC lượt vẽ lại (bấm *Thu gọn*
   lại ra đúng trần của lúc đang mở). Phải `$nextTick` + `requestAnimationFrame`.
3. **Mở popup khác khi popup đang mở thì không reset** (watcher chỉ bám `visible`) → gom thành
   `resetState()` và bắt thêm watcher `nodeKey` / `metric`.

**Test**: thêm 2 ca e2e (đo DOM, không nhìn ảnh) + sửa 3 chỗ assertion định dạng số (kể cả hàm
`parse()` của ca cộng dồn — nó đang bóc số theo kiểu VN). Chạy lại **TOÀN BỘ bộ test của màn**:
**29/29 xanh** (3.1 phút, `--workers=1`); 1 ca *flaky* ("Execution context was destroyed" lúc
`openReport`, xanh ở lượt retry và xanh khi chạy lẻ — lỗi thời điểm điều hướng của Nuxt, không liên
quan thay đổi này).

**Ảnh chụp**: `.plans/bao-cao-phat-trien-thi-truong-khach-hang/screenshots/2026-09-14-popup-khoi-tong-hop.png`
(ca e2e tự chụp).

**Đang làm dở**: không có. **Blocked**: không có.

**Bước tiếp theo**: user push `tpe` (hrm-api 98 / hrm-client 86+1 commit trước origin) và xoá nhánh
`tpe-bao-cao-phat-trien-thi-truong-kh` nếu không cần nữa.

---

### Checkpoint — 2026-09-14, sau khi user push lên VPS

**Vừa hoàn thành**: soạn `deploy.md` — mọi việc phải làm khi lên production, dựa trên số đo thật
trên máy dev chứ không phải phỏng đoán.

**4 điều đo được khi rà deploy (chưa ai nêu trước đó):**

1. 🔴 **Hiệu năng tiêu chí "Khách hàng" + kỳ dài** — API nhanh (0.25s) nhưng **trình duyệt** phải
   dựng 3.264 dòng (bung hết cấp: 9.046 dòng ≈ 20.000 component). Đo trên bản DEV:
   **46s** nạp · **73s** khi bung hết cấp. Mạng + `JSON.parse` 4.3MB chỉ 1.1s ⇒ nghẽn ở RENDER.
   Thử `Object.freeze` cả cây (bỏ reactivity) **không ăn thua** (75s) ⇒ muốn chữa phải phân trang
   hoặc ảo hoá bảng. Bản in *Tổng hợp* của cùng trường hợp ra **6.5MB HTML**.
   Mặc định màn là *Tháng này · Thị trường* (4 dòng) nên mở màn vẫn nhẹ.
2. 🔴 **`company_id` khi cấp quyền không phải lúc nào cũng là 1** — đo trên DB: quyền đang cấp theo
   **5 công ty** (1, 2, 3, 4, 8). Cấp thiếu công ty là người thuộc công ty đó không thấy gì mà cũng
   không báo lỗi. Cách an toàn: nhân bản grant của quyền 1179-1181 (báo cáo CSKH tiềm năng, trùng
   khớp 3 cấp) sang 1187-1189.
3. 🟠 **Menu KHÔNG bị ẩn theo quyền** (`filterMenuItems()` trả nguyên danh sách) ⇒ ai cũng thấy mục
   menu, chưa cấp quyền thì vào là báo cáo trống. Cấp quyền TRƯỚC khi thông báo cho người dùng.
4. 🟠 **`env('DB_DATABASE_SECOND')` gọi ngoài file config** (115 file trong `hrm-api`, không riêng
   màn này) ⇒ **không được bật `php artisan config:cache`** trên VPS, bật là chết kết nối ERP.

**Kiểm lại seeder backfill**: chạy lần 2 trên DB local — vá đúng 2 dòng mới sinh, không ghi đè dòng
cũ, in ra dòng tổng kết "Còn lại 0 meeting chưa có thị trường" ⇒ **chạy lại nhiều lần an toàn**.

**Bước tiếp theo**: sau khi deploy, đo lại 2 ô đỏ ở bảng hiệu năng bằng **bản build prod**; nếu vẫn
hàng chục giây thì mở task chặn (phân trang / ảo hoá bảng / bắt buộc lọc thêm khi tiêu chí = Khách
hàng và kỳ > 1 tháng).

**Blocked**: không có.

---

## Phase 6 — Phân trang (14/09/2026)

Lý do: đo được ở Phase 5 — tiêu chí *Khách hàng* + kỳ Năm nay ra **3.264 dòng** (bung hết cấp
**9.046**), trình duyệt dựng mất hàng chục giây. Popup cũng đổ hết danh sách 1 lần.

Khuôn copy từ **báo cáo anh em đã có phân trang popup**: `potential-customer-care/components/
DemandListModal.vue` (client-side `V2BasePagination`, `safePage` kẹp trang, STT chạy tiếp qua trang).
Bảng theo dõi dạng CÂY thì **chưa màn nào trong project làm** → tự thiết kế, ghi lại vào design.md.

- [x] **Task 57** — Popup chi tiết: phân trang client-side trên tập ĐÃ LỌC + ĐÃ SẮP.
      STT chạy tiếp qua trang. Đổi bộ lọc / bấm chip / đổi sắp xếp / mở popup mới → về trang 1.
      **In danh sách + Xuất Excel vẫn lấy TOÀN BỘ tập đã lọc**, không phải mỗi trang đang xem.
      Khối KPI + dải chip vẫn tính trên toàn tập (không đổi theo trang).
- [x] **Task 58** — Bảng theo dõi: phân trang theo **DÒNG CẤP 1**, mỗi dòng cấp 1 mang NGUYÊN nhánh
      con của nó sang cùng trang (không cắt cha lìa con). Dòng **TỔNG luôn hiện**, không thuộc trang
      nào (nó là tổng cả kỳ). **STT giữ số thật** (trang 2 bắt đầu từ 51), không đánh lại từ 1.
- [x] **Task 59** — Đo lại trường hợp nặng nhất bằng Playwright, chốt bộ `page-size-options` theo
      số đo (không đoán).
- [x] **Task 60** — e2e: thêm ca phân trang cho cả 2 chỗ; **rà lại ca "Bung tất cả cấp"** (nó so
      tổng các dòng cấp 1 với dòng TỔNG — phân trang làm số dòng cấp 1 hiển thị ít đi).
      Chạy lại TOÀN BỘ bộ test của màn.
- [x] **Task 61** — Cập nhật `deploy.md` (mục rủi ro hiệu năng), `design.md`, `STATUS.md`.

### Checkpoint — 2026-09-14 khuya (Phase 6 XONG, Task 57 → 61)

**Vừa hoàn thành**: phân trang cho cả bảng theo dõi và popup. Chỉ **2 file FE**
(`DevelopmentTable.vue`, `DevelopmentDrillModal.vue`), KHÔNG đụng backend.

| Đo bằng Playwright (số lấy từ DOM) | Trước | Sau |
| --- | --- | --- |
| *Năm nay · Khách hàng* — tải + vẽ xong | **46,3s** | **1,08s** |
| …bung hết cấp | **73,4s** (9.046 dòng) | **0,19s** (148 dòng trong trang) |
| Số dòng bảng vẽ 1 lúc | 3.264 | 51 |
| Sang trang / đổi số dòng/trang | — | 0,28s / 0,01s |

Kiểm thêm: STT giữ số thật (trang 2 → 51, trang cuối → 3251, con là `3263.1.1`), dòng TỔNG có ở
mọi trang, popup STT 1-20 → 21-40, KPI ở trang 2 vẫn là `51 / 71` (toàn tập), bấm chip → về trang 1.

**2 lỗi tự phát hiện khi đo, đã sửa:**
1. **Khổ 1280×720 (khổ e2e dùng) mở khối tổng hợp → 2 thanh cuộn dọc lồng nhau.** Thêm thanh phân
   trang làm ngân sách chiều cao chỉ còn **137px** cho bảng, mà sàn cứng là 180px nên ép trần kiểu gì
   cũng tràn. Sửa: dưới ngưỡng thì **BỎ trần** (`0`) → `V2BaseTableScroll` bỏ `overflow-y`, cả thân
   popup thành 1 vùng cuộn duy nhất. Luật kiểm đổi thành "**đúng 1 khối cuộn dọc**", không bắt buộc
   là khối nào.
2. `syncTableHeight()` đo 1 lượt vẫn hụt → thêm **vòng tự sửa** `trimTableOverflow()`: đo lại, còn
   tràn bao nhiêu trừ tiếp bấy nhiêu, tối đa 2 lượt.

Ca e2e cũng được sửa để **in ra danh sách khối đang cuộn** khi fail — lần đầu nó chỉ báo
"Expected 1, Received 2", không biết khối nào, phải mò.

**Test**: thêm 2 ca phân trang; **31/31 xanh** (2.1 phút, `--workers=1`), không có ca flaky.
**Ảnh**: `screenshots/2026-09-14-phan-trang-bang-theo-doi.png`.

**Đang làm dở**: không có. **Blocked**: không có.

**Còn lại (đã ghi trong `deploy.md`)**: bản in *Tổng hợp* tiêu chí Khách hàng + Năm nay vẫn 6,5 MB
HTML (bản in phải in đủ mọi dòng nên không phân trang được) và payload API 4,3 MB — muốn giảm nữa
phải phân trang ở backend, chưa làm.

---

## Phase 7 — Chuyển phân trang sang BACKEND (14/09/2026)

User chốt: **"luôn phân trang phía BE, đó là nguyên tắc"** — đúng với `CLAUDE.md` mục hiệu năng
("Luôn phân trang, không trả cả bảng"). Bản Phase 6 cắt lát ở FE là **làm sai nguyên tắc**, phải sửa.

Ràng buộc phải giữ nguyên khi chuyển:
- Dòng **TỔNG** và **dải tổng hợp** vẫn tính trên TOÀN kỳ (không theo trang).
- **Excel + bản in vẫn xuất/in ĐỦ mọi dòng** — `getFlatRowsForExport()` gọi chung `getData()` nên
  phải có cờ tắt phân trang, nếu không file xuất ra chỉ còn 1 trang.
- Popup: **KPI + dải chip + ô lọc + cột Bộ phận** phải tính trên toàn tập, không phải trang đang xem.
  ⇒ BE trả kèm các số đó, FE không tự tính từ mảng dòng nữa.
- Ô lọc trong popup phải lấy tuỳ chọn từ tập **TRƯỚC** bộ lọc riêng của popup, nếu không chọn 1 phòng
  ban xong là dropdown còn đúng 1 mục.

- [x] **Task 62** — BE `getData()`: thêm `page` / `per_page`, cắt ở **cấp 1** ngay trong `buildTree()`
      (chỉ dựng nhánh con cho các node thuộc trang → đỡ cả CPU lẫn payload), trả `pagination`.
      Thêm cờ `$paginate` để Excel/bản in gọi bản KHÔNG phân trang.
- [x] **Task 63** — BE: bộ lọc riêng của popup đổi sang tiền tố `p_*` + `q`, tách khỏi bộ lọc báo cáo
      (để còn tính được tuỳ chọn ô lọc trên tập gốc). Thêm sắp xếp `sort` / `sort_dir` ở BE.
- [x] **Task 64** — BE `getDrillPage()`: trả `rows` (1 trang) + `pagination` + `summary` (KPI) +
      `allocations` (chip) + `filter_options` + `has_part`, tất cả tính trên TOÀN tập.
      Thêm cờ `customer_is_new` cho từng dòng meeting (chip "KH mới" hiện đang chết vì FE chỉ có
      danh sách KH mới sau khi người dùng mở popup "KH mới").
- [x] **Task 65** — FE: bảng theo dõi + popup bỏ cắt lát client, gọi API theo trang; popup đọc
      KPI/chip/ô lọc/cột từ BE. Bản in gửi đúng bộ `p_*` + `q` để in khớp tập đang xem.
- [x] **Task 66** — e2e: sửa 2 ca phân trang (nay là server-side), thêm ca kiểm **Excel/bản in vẫn đủ
      dòng** khi bảng đang ở trang 1. Chạy lại TOÀN BỘ.
- [x] **Task 67** — Cập nhật `design.md`, `deploy.md`, `STATUS.md`.

### Checkpoint — 2026-09-14 (Phase 7 XONG, Task 62 → 67)

**Vừa hoàn thành**: chuyển phân trang sang BACKEND cho cả bảng theo dõi và popup.

| Đo *Năm nay · Khách hàng* | Trước | FE cắt lát (bị bác) | **BE phân trang** |
| --- | --- | --- | --- |
| Payload API | 4,3 MB | 4,3 MB | **67 KB** |
| Tải + vẽ xong | 46,3s | 1,08s | **0,87s** |
| Số dòng vẽ 1 lúc | 3.264 | 51 | **51** |

**BE** (`hrm-api`): `buildTree()` nhận cửa sổ `offset/limit` và cắt **ngay tại cấp 1, sau sort,
TRƯỚC khi dựng nhánh con**; `getData($request, $paginate)` trả thêm `pagination`;
`getDrillPage()` trả `rows` + `pagination` + `summary` + `allocations` + `filter_options` +
`has_part`; bộ lọc popup đổi sang tiền tố `p_*` + `q`; `sortDrillRows()` (5 mốc, hoà thì so `code`
cho thứ tự ổn định giữa các trang); cờ `customer_is_new` cho từng dòng; **endpoint mới
`drill/export`** + 1 export class + 1 blade; memo hoá `getNewCustomerRows()` (1 query gộp ERP).

**FE** (`hrm-client`): bảng + popup bỏ hết phần cắt lát / lọc / sắp ở client; popup đọc KPI, chip,
tuỳ chọn ô lọc, cột Bộ phận từ BE; ô tìm nhanh **debounce 300ms**; nút Xuất Excel của popup chuyển
sang tải thẳng từ server.

**3 cái bẫy đã chặn bằng test:**
1. **Excel / bản in dùng chung `getData()`** → quên tắt phân trang là file chỉ còn 1 trang mà KHÔNG
   báo lỗi. Có ca riêng "Bản in + Excel vẫn ĐỦ MỌI DÒNG dù màn hình đang phân trang".
2. **Tuỳ chọn ô lọc popup** nếu tính trên tập đã lọc thì chọn 1 phòng ban xong dropdown còn đúng 1
   mục → BE tính `filter_options` trên tập TRƯỚC bộ lọc popup, có ca kiểm.
3. **Ca cộng dồn của API** (tổng dòng cấp 1 = dòng TỔNG) đỏ ngay lần chạy đầu vì chỉ lấy 1 trang →
   sửa thành gom đủ mọi trang. Đây đúng là thứ ca test sinh ra để bắt.

**Test**: **35/35 xanh** (2,5 phút, `--workers=1`) — thêm 4 ca (2 API về tính đầy đủ của Excel/bản in
+ ô lọc, 1 UI kiểm nút Xuất Excel tải từ server, và 2 ca phân trang cũ viết lại cho chế độ BE).

**Đang làm dở**: không có. **Blocked**: không có.

---

### Checkpoint — 2026-09-16 (WRAP UP — toàn bộ Phase 1 → 7 đã xong)

**Trạng thái**: màn hoàn thiện, không còn task mở. Tổng kết cả hành trình:

| Phase | Nội dung | Kết quả |
| --- | --- | --- |
| 1→3 | Mockup + design + plan | Mockup đã duyệt |
| 4 | Code thật (Task 31→43) + 6 đợt bổ sung | 27/27 e2e, đã merge `tpe` |
| 5 | Khối tổng hợp thu gọn trong popup + chuẩn định dạng số | 29/29 e2e |
| 6 | Phân trang (làm ở FE) | 31/31 e2e — **bị bác vì sai nguyên tắc** |
| 7 | Phân trang **Ở BACKEND** | **35/35 e2e** |

**Lần chạy test cuối**: 35/35 xanh (2,5 phút, `--workers=1`) — chạy khi 2 repo còn đứng ở nhánh
`tpe`. ⚠️ **Hiện cả 2 repo đã được checkout sang `gop_db`** (việc của phần gộp DB), nên code của màn
này KHÔNG nằm trong cây làm việc lúc này; muốn chạy lại test phải `git checkout tpe` ở cả 2 repo.

**Git — còn 2 commit CHƯA PUSH ở mỗi repo** (nằm trên nhánh `tpe`):
- `hrm-api`: `a8e5a4cc2` (phân trang BE) + `b536c343f` (merge `origin/tpe`)
- `hrm-client`: `3dfd28d5b` (FE theo phân trang BE) + `723362788` (merge `origin/tpe`)
- Đã push từ trước: `26130f5b1` (khối tổng hợp popup) · `656cfd5bc` (phân trang bản FE, nay đã bị
  bản BE thay thế) và toàn bộ Phase 1→4.

**Đang làm dở**: không có. **Blocked**: không có.

**Bước tiếp theo (việc của user)**:
1. `git checkout tpe` ở cả 2 repo rồi **push** (mỗi repo 2 commit).
2. Deploy theo `deploy.md` — lần này **BE có đổi** (service + controller + route + 1 export class +
   1 blade), không có migration mới.
3. Xoá nhánh `tpe-bao-cao-phat-trien-thi-truong-kh` nếu không cần nữa (vẫn còn ở cả 2 repo).
