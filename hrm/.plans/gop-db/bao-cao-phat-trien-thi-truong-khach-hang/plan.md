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
