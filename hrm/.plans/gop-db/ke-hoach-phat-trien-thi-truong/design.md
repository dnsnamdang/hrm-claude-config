# Kế hoạch phát triển thị trường (Kinh doanh) — Mockup UI

**Nhánh:** `update_sidebar_menu` (client) / `menu_phan_he_2026` (api) — đều con `gop_db` · **Phụ trách:** @namdangit · 2026-08-08
**Ảnh tham khảo:** mẫu Excel "Theo dõi thị trường & khách hàng" (phòng Kinh doanh)
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-08-08-ke-hoach-phat-trien-thi-truong-design.md`

## Mục tiêu
Mockup HTML tĩnh (sân thử UI) màn "Kế hoạch phát triển thị trường" cho phòng Kinh doanh — chốt UI trước khi port Vue thật. Style navy+teal đồng bộ menu Bán hàng, self-contained (inline CSS+SVG), verify Playwright.

## ⚠️ PIVOT v2 (2026-08-08) — 1 màn lịch phiếu công việc
Bỏ tab "Theo thị trường", gộp về **1 màn lịch duy nhất** (Tháng/Tuần) trung tâm là **phiếu công việc**:
- **4 loại phiếu** (thẻ màu): Phiếu công tác (teal) · Meeting (xanh dương) · Phiếu giao việc (tím) · Task (cam). Mỗi thẻ: màu loại + thời gian + badge trạng thái.
- **Trạng thái chung 4**: Chờ duyệt (xám) · Đang thực hiện (xanh dương) · Hoàn thành (xanh lá) · Từ chối/Hủy (đỏ).
- **Toolbar**: giữ bộ lọc cũ (Tháng/Năm, Phòng ban, NV, Người theo dõi, Thị trường, Tìm kiếm) + thêm **Loại phiếu** + **Trạng thái** — TẤT CẢ lọc thật, re-render lịch + cập nhật thống kê.
- **4 box** = đếm số phiếu MỖI LOẠI trong kỳ lọc (thay KPI trạng thái KH cũ).
- **Click thẻ** → popover + link "Xem chi tiết" mở drawer (tái dùng drawer v1 cho chi tiết phiếu).
- Bản v1 (accordion theo thị trường + drawer KH) giữ làm phụ lục, không còn là hướng chính.

## ⚠️ PIVOT v3 (2026-08-10) — màn "Quản lý lịch làm việc cá nhân" (3 tab)
Bản meeting (`...-mockup-meeting.html`, copy `quan_ly_cong_viec_ca_nhan.html`) mở rộng thành **màn quản lý lịch làm việc cá nhân**, đổi tên topbar + `<title>` → **"Quản lý lịch làm việc cá nhân"**. Cấu trúc **3 tab**:
1. **Công việc của tôi** (My To Do — tab ĐẦU, mặc định): gộp thống nhất **Task / Issue / Cá nhân** (bỏ Cuộc họp/Phiếu duyệt), nhóm theo thời gian **thu gọn/mở rộng** ĐÚNG màn thật (đối chiếu `pages/assign/my-todo/components/TodoGroupHeader.vue` + `TodoMainList.vue`): thứ tự Hôm nay→Ngày mai→Tuần này→Tuần sau→Sau đó→Không hạn→**Quá hạn (cuối)**; mỗi nhóm 1 card có icon+màu riêng+badge, mặc định chỉ "Hôm nay" mở, today/tomorrow/this-week/overdue luôn hiện dù rỗng. Kèm stats (Quá hạn/Hôm nay/Tuần này/Cần duyệt), filter (Loại/Vai trò/Trạng thái), mini lịch + danh sách cá nhân. Data mock độc lập (chưa nối TICKETS).
2. **Lịch meeting**: calendar Tháng/Tuần — **màu nền thẻ theo trạng thái** (Lên lịch xám/Đã chốt xanh dương/Hoàn thành xanh lá/Huỷ đỏ); nút "Thêm meeting" quick-add; drawer nút theo trạng thái.
3. **Kết quả meeting theo thị trường** (đổi tên từ "Meeting theo thị trường"): bảng meeting-centric header 1 cấp + bộ lọc Thị trường/Trạng thái/Loại meeting + **Kỳ** (Hôm nay/Tuần/Tháng/Quý/Năm/Tuỳ chọn) + **Xuất Excel**; đánh dấu **KH mới phát triển** (badge + highlight, đưa lên đầu); cột **Dự án TKT** + **Phiếu công tác/Lịch sử chấm công GPS** (CHỈ meeting Hoàn thành); summary **lưới text** + nhóm Tổng hợp (dự án/KH mới/tỷ lệ hoàn thành).

## ⚠️ PIVOT v4 (2026-08-19) — tách BÁO CÁO thành màn/file RIÊNG

Tab 3 tách hẳn thành file độc lập **`bao-cao-ket-qua-meeting-theo-thi-truong.html`** (topbar "Báo cáo kết quả meeting theo thị trường", không còn dải tab). File `...-mockup-meeting.html` chỉ còn **2 tab**: Công việc của tôi · Lịch meeting.

**Cấu trúc bảng (Task 44→59):**
- **Outline 3 cấp** thay ô gộp rowspan: STT phân cấp `I` (thị trường) → `1` (khách hàng) → `1.1` (meeting) + 1 cột gộp tên "Thị trường / Khách hàng / Meeting".
- **2 chế độ cột**: **TỔNG HỢP** (mặc định, chỉ hiện tới cấp Khách hàng) = mỗi phòng ban 1 cột đếm + cột Tổng, ẩn toàn bộ cột chi tiết; dòng meeting hiện **dấu tick**, dòng nhóm hiện **số**. **CHI TIẾT** = 13 cột đầy đủ. Chuyển bằng nút "Ẩn/Hiện chi tiết"; caret trên từng dòng nhóm thu/bung riêng lẻ.
- **Cột "Phòng ban"** = phòng ban của **người chủ trì**; bộ lọc **cascade Công ty ▸ Phòng ban ▸ Người chủ trì**. Lọc phòng/công ty → **chỉ hiện cột phòng tương ứng** (đồng bộ bảng · dải tổng hợp · Excel · bản in).
- **Sắp xếp** mọi cột dữ liệu (từ "Thời gian" sang phải): asc → desc → mặc định; giữ nguyên cấu trúc nhóm (chi tiết: sắp meeting trong KH; tổng hợp: sắp KH trong thị trường + sắp thị trường).
- **Sticky** hàng tiêu đề + dòng **TỔNG CỘNG** (đã dời từ cuối bảng lên ngay dưới tiêu đề); khung bảng tự tính chiều cao theo cửa sổ.
- **Drill-down**: click con số ở dòng TỔNG CỘNG → **popup danh sách meeting** tương ứng (theo phòng ban hoặc tất cả) kèm nút **In danh sách** + **Xuất Excel** riêng.
- **Chi tiết meeting**: click bất kỳ đâu trên dòng meeting → panel overlay dùng lại **drawer của màn Lịch meeting**.
- **In**: nút "In báo cáo" → popup chọn **In tổng hợp / In chi tiết**; bản in A4 ngang, bám bộ lọc đang áp.

**Dải tổng hợp (thiết kế lại):** 4 ô KPI (Tổng meeting · Hoàn thành + % · Khách hàng · Dự án TKT) + 3 khối phân bổ (thanh xếp chồng theo trạng thái · thanh ngang theo phòng ban · thanh ngang theo thị trường, chỉ liệt kê nơi có meeting). **Bộ lọc nằm TRÊN dải tổng hợp**, có nút **Ẩn/Hiện tổng hợp**.

**Bỏ khỏi bản này:** nhận dạng "KH mới phát triển" (badge/highlight/ưu tiên sắp xếp) — thay bằng chỉ số "Khách hàng" trong KPI.

**Data demo:** 30 meeting / 11 khách hàng / **3 thị trường** (Hà Nội 14 · TP.HCM 8 · Đà Nẵng 8); phòng ban cân đối Kinh doanh 1 = 11 · Kinh doanh 2 = 11 · Kinh doanh dự án = 8; 2 công ty demo (tạm `Tân Phát ETEK` gồm KD1+KD2, `Tân Phát Sài Gòn` gồm KD dự án — **chờ user chốt tên thật**).

> Ngoài scope (giữ nguyên): code Vue thật, DB/API, phân quyền, responsive (đang HOÃN). Câu hỏi mở: có tách hẳn "Công việc của tôi" thành file/màn riêng không.

## ⚠️ PIVOT v5 (2026-08-20) — thêm màn/file BÁO CÁO THỨ 2: "Báo cáo tổng hợp nhu cầu khách hàng"

File độc lập **`bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`** (cùng folder). Layout bám **ảnh Excel** user gửi; style tái dùng NGUYÊN bộ design token + component của `bao-cao-ket-qua-meeting-theo-thi-truong.html` (navy+teal, `.market-table` outline, `.market-toolbar`/`.calendar-filter-*`, `.rsum-*`, `.minutes-modal`, `.ticket-drawer`).

**Khác biệt cốt lõi so với báo cáo meeting:** đơn vị dòng là **NHU CẦU của khách hàng** (thu thập từ 1 meeting), không phải meeting.

- **Outline 3 cấp**: `I` Lĩnh vực KD (Gara · Năng lượng · Môi trường · Đào tạo - Dạy nghề) → `1` Thị trường → `1.1` Khách hàng. Giữ đủ 4 lĩnh vực kể cả rỗng; trong lĩnh vực chỉ liệt kê thị trường có dữ liệu.
- **10 cột**: STT · Lĩnh vực KD/TT/KH · Tổng giá trị đầu tư dự kiến · Thời gian dự kiến triển khai · Nhu cầu dịch vụ sửa chữa · Meeting thu thập nhu cầu · Kinh doanh chủ trì · Phòng · Trạng thái · Dự án TKT. Tiêu đề cột **không xuống dòng** (bảng chi tiết cuộn ngang, `table-layout: fixed` + colgroup).
- **2 chế độ cột**: CHI TIẾT (10 cột) ↔ **TỔNG HỢP** (4 cột: STT · Lĩnh vực KD/TT · Tổng giá trị đầu tư · Số nhu cầu — ẩn hẳn cột chi tiết rỗng, không cuộn ngang). Excel và bản in bám đúng chế độ đang xem.
- **Trạng thái = trạng thái NHU CẦU KH** (không phải meeting/dự án): Mới ghi nhận · Đang theo dõi · **Đã lập dự án TKT** · Không tiếp tục.
- **Dự án TKT**: chưa có → nút **`+ TẠO MỚI`** mở popup tạo dự án (gợi ý mã `TKT.YYYY.<viết tắt KH>`); tạo xong gán mã, chuyển trạng thái "Đã lập dự án TKT", cập nhật KPI + TỔNG CỘNG. Nhu cầu "Không tiếp tục" không hiện nút.
- **Click tên meeting → drawer chi tiết meeting** (dùng lại `.ticket-drawer`): 4 khối — Thông tin cuộc họp · Mục tiêu/Nội dung · Thành phần tham dự · **Nhu cầu thu thập được**; footer có nút Tạo dự án TKT (popup đè lên drawer, tạo xong drawer tự làm mới).
- **Bộ lọc (7)**: Kỳ xem (bám **thời gian bắt đầu họp**) · Lĩnh vực KD · Khách hàng · cascade **Công ty ▸ Phòng ban ▸ Bộ phận ▸ Kinh doanh chủ trì** · Xoá lọc. Tất cả dùng `<select class="calendar-filter-select">` chuẩn như file mẫu.
- **Dải KPI**: Tổng nhu cầu · Tổng giá trị đầu tư dự kiến · Khách hàng · Chưa có dự án TKT (+%) + 3 khối phân bổ (thanh xếp chồng trạng thái, thanh ngang lĩnh vực KD, thanh ngang thị trường); có nút Ẩn/Hiện tổng hợp.
- **Quyết định UI khác ảnh Excel**: BỎ tô nền vàng dòng chưa có dự án (mọi dòng nhu cầu cùng nền trắng — dấu hiệu chỉ còn nút "+ TẠO MỚI").
- **Data demo**: 26 nhu cầu / 18 khách hàng / 4 lĩnh vực / 3 thị trường; nhân sự – phòng ban – công ty đồng bộ file báo cáo meeting. Thông tin cuộc họp cho drawer sinh 1 lần bằng `enrichMeetings()` (cố định, không random).

> Câu hỏi mở: Lĩnh vực KD có cần **chọn nhiều** không (ảnh Excel ghi "select chọn nhiều", hiện đang select đơn theo yêu cầu dùng đúng select của file mẫu).

## ⚠️ PIVOT v6 (2026-08-23) — đổi định vị màn: "Báo cáo kết quả chăm sóc khách hàng tiềm năng" · **UI ĐÃ DUYỆT**

Vẫn file `bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`, nhưng **đổi tên báo cáo + đổi hẳn phần summary** theo spec user gửi.

- **Tên báo cáo** (title · topbar · bản in · tên file Excel): **Báo cáo kết quả chăm sóc khách hàng tiềm năng**.
- **Mục tiêu** (hiện thành 1 dòng đầu dải tổng hợp + trong bản in): *Theo dõi kết quả chăm sóc các khách hàng có nhu cầu đầu tư dự án trong kỳ*.
- **Dữ liệu lấy vào báo cáo** (thay luật lọc cũ "meeting họp trong kỳ"):
  1. Nhu cầu **phát sinh trong kỳ** = meeting họp trong kỳ có biên bản khách trả lời **CÓ** ở câu "anh/chị có nhu cầu đầu tư không?".
  2. Nhu cầu phát sinh **kỳ trước** nhưng tới ngày đầu kỳ vẫn **chưa lập dự án TKT** và **chưa hết hạn theo dõi** (dòng bảng gắn nhãn `Kỳ trước`).
- **Hạn theo dõi 1 nhu cầu** = hết tháng (**tháng dự kiến triển khai + N tháng cấu hình**). N chọn ngay trên toolbar (bộ lọc **Hạn theo dõi**: +3 / +6 / +9 / +12, mặc định **+3**) — đổi N là toàn bộ số liệu I/II/III đổi theo. Cột "Thời gian dự kiến triển khai" hiện thêm dòng *Hạn TD dd/mm/yyyy*; drawer meeting thêm trường "Hạn theo dõi nhu cầu".
- **Kỳ xem**: BỎ lựa chọn "Tất cả" (báo cáo luôn tính theo kỳ), mặc định **Tháng này**.
- **Summary (chốt lần cuối 2026-08-23)** — **1 BẢNG CHUNG 4 phần** + cột hộp KPI bên phải, **bỏ hẳn khối "Phân bổ theo trạng thái nhu cầu"**:
  - Bảng chung 5 cột `STT · Nội dung tổng hợp · Số nhu cầu · Giá trị đầu tư · Tỷ trọng giá trị` (thanh bar + %), chia 4 phần: **I.** Tổng nhu cầu trong kỳ (1 còn hiệu lực · 2 PS trong kỳ) → **II.** Tổng nhu cầu bị đóng trong kỳ (1 chuyển đổi thành dự án · 2 hết hạn không thành dự án) → **III.** Theo lĩnh vực kinh doanh → **IV.** Theo thị trường. Mỗi dòng tiêu đề phần có màu riêng (I teal · II xám · III xanh lá · IV tím).
  - Tỷ trọng tính theo **giá trị đầu tư**: phần I/III/IV so với tổng kỳ, phần II so với tổng giá trị nhu cầu đã đóng.
  - **Kết quả KPI hiện dạng summary box** — 3 hộp xếp dọc bên phải bảng (viền trái teal/xanh lá/cam): % lớn + số thô `10 / 35` + thanh bar + công thức `= II.1 / I`.
  - **Mọi diễn giải nằm trong icon `i`, hover mới hiện tooltip** (mục tiêu báo cáo + 4 tiêu đề phần + 4 dòng chỉ tiêu + 3 KPI). Dòng meta 1 hàng phía trên: kỳ đang xem · hạn theo dõi · tổng giá trị đầu tư.
  - **I. Tổng nhu cầu trong kỳ** = I.1 *Tổng nhu cầu còn hiệu lực theo dõi* (PS giai đoạn trước, chưa hết hạn tính tới ngày đầu kỳ) + I.2 *Tổng các nhu cầu PS trong kỳ này*.
  - **II. Tổng nhu cầu bị đóng trong kỳ** = II.1 *chuyển đổi thành dự án* (lập dự án TKT trong kỳ) + II.2 *hết hạn mà không chuyển thành dự án được*.
  - **III. Kết quả KPI**: Tỷ lệ chuyển đổi thành công `= II.1 / I` · Tỷ lệ thành công / tổng nhu cầu đóng `= II.1 / II` · Tỷ lệ thất bại / tổng nhu cầu đóng `= II.2 / II`.
- **Trạng thái nhu cầu**: thêm **Hết hạn theo dõi** (cam) và **suy ra theo kỳ đang xem** (`effStatus`) thay vì đọc cứng `d.status` — nhờ vậy khối "Phân bổ theo trạng thái" khớp đúng với mục II.
- **Data demo**: thêm **11 nhu cầu kỳ trước** (meeting 04–07/2026) + `projectDate` (ngày lập dự án TKT) cho nhu cầu đã có dự án. Kỳ 08/2026 với N=3: I = 35 (9 + 26) · II = 13 (10 + 3) · KPI 28,6% / 76,9% / 23,1%.
- **Giả định đang áp** (chưa có trong spec): nhu cầu "Không tiếp tục" (dừng thủ công) KHÔNG tính vào II và không mang sang kỳ sau.
- **Fix lỗi hiển thị**: dòng TỔNG CỘNG dính bị hở ~2px dưới hàng tiêu đề (nội dung cuộn lòi qua khe) → ghim `top: 34px` cho luồn xuống dưới tiêu đề. `box-shadow` KHÔNG dùng được vì bảng `border-collapse: collapse` (Chrome bỏ qua shadow của ô bảng).

> **Nợ UI (user đã biết, chưa xử lý):** bảng chi tiết rộng 1660px > vùng hiển thị ~1426px (màn 1512) nên cuộn ngang, cột "Dự án TKT" bị khuất — muốn hết cuộn ngang phải rút ngắn tên vài tiêu đề cột, mà tiêu đề cột đã chốt là KHÔNG xuống dòng.

## ⚠️ PIVOT v7 (2026-08-23) — bảng theo dõi là MÀN CHÍNH, bỏ bảng chi tiết; số bấm được → popup

Cấu trúc màn rút còn 3 tầng: **bộ lọc → khối KPI → bảng theo dõi**.

- **BỎ hẳn bảng chi tiết outline 3 cấp khỏi màn** (và 2 nút "Ẩn tổng hợp" / "Ẩn chi tiết" — không còn ý nghĩa). Dữ liệu chi tiết vẫn còn, chỉ đổi chỗ hiển thị (popup + bản in).
- **Bảng tổng hợp I → IV trở thành BẢNG THEO DÕI CHÍNH**, chiếm 100% chiều rộng, nằm trong `.calendar-panel`; bỏ khoá chiều cao (`max-height`) để không cuộn lồng trong cuộn.
- **Khối KPI lên đầu màn**, 100% chiều rộng, **3 box trên 1 hàng** (trước đó xếp dọc bên phải bảng).
- **Bấm con số (số nhu cầu hoặc giá trị đầu tư) trong bảng → popup danh sách nhu cầu chi tiết** (`#drill-modal`, rộng 1400px): 13 cột dựng theo bảng chi tiết cũ + thêm Lĩnh vực KD / Thị trường / Hạn theo dõi (vì popup không có outline để suy ra). Popup có: nút **Xuất Excel danh sách** riêng · bấm tên meeting → đóng popup, mở drawer chi tiết meeting · nút **+ TẠO MỚI** tạo dự án TKT ngay trong popup (popup tạo dự án z-index cao hơn, tạo xong bảng + popup tự làm mới).
  - Key drill: `all` (I & tiêu đề III/IV) · `carried` (I.1) · `arisen` (I.2) · `closed` (II) · `converted` (II.1) · `expired` (II.2) · `field:<id>` (III.x) · `market:<id>` (IV.x).
- **Xuất Excel** (nút toolbar) = đúng bảng theo dõi đang xem. **In báo cáo** giữ 2 lựa chọn: *In bảng theo dõi* (4 phần I→IV + dòng KPI) hoặc *In danh sách chi tiết* (outline 3 cấp 10 cột như cũ).

## ⚠️ PIVOT v8 (2026-08-23) — bỏ "Hạn theo dõi" khỏi màn · bảng theo dõi 5 phần I → V

- **Bỏ bộ lọc "Hạn theo dõi"** và mọi chỗ hiển thị hạn (dòng meta · cột trong popup chi tiết · trường trong drawer · dòng mô tả bản in). Số tháng thành **hằng cấu hình hệ thống** `TRACK_MONTHS = 3` — logic II.2 (hết hạn theo dõi) giữ nguyên, chỉ không lộ ra UI.
- **Hộp KPI bỏ dòng công thức** dưới thanh %; công thức + số thô + diễn giải dồn hết vào **icon `i`** trên nhãn.
- **III đổi tên → "Theo lĩnh vực kinh doanh nội bộ"** (kéo theo nhãn bộ lọc, cột popup, trường drawer) và **thêm cấp con NHÓM NGÀNH**: mỗi lĩnh vực 2–3 nhóm ngành (11 nhóm cho 4 lĩnh vực), **mặc định ẩn**, bung bằng caret ngay trên dòng lĩnh vực.
- **Thêm phần V — Theo phòng ban**: 2 cấp **Phòng ban ▸ Nhân viên (kinh doanh chủ trì)**, nhân viên **mặc định ẩn**, bung bằng caret trên dòng phòng.
- Dòng cấp con: STT dạng `2.1`, thụt lề, **tỷ trọng tính trong nội bộ nhóm cha**; số vẫn bấm được → popup danh sách (key `sector:<id>` · `dept:<id>` · `emp:<id>`).
- Popup chi tiết đổi cột: bỏ *Hạn theo dõi*, thêm *Nhóm ngành* (13 cột, vẫn vừa 1 màn không cuộn ngang).

> Chưa động tới: **Xuất Excel / In báo cáo** vẫn theo bố cục cũ (chưa có phần V và nhóm ngành) — user yêu cầu sửa layout trước.

## ⚠️ PIVOT v9 (2026-08-23) — I & II tách thành 2 khối trên KPI · bảng còn 3 phần I → III

- **I. Tổng nhu cầu trong kỳ** và **II. Tổng nhu cầu bị đóng trong kỳ** rời khỏi bảng, thành **2 khối nằm TRÊN dải 3 hộp KPI** (mỗi khối: badge số La Mã · tên · tổng số nhu cầu + giá trị · 2 ô chỉ tiêu con). **Mọi con số vẫn bấm được → popup danh sách chi tiết** như cũ.
- **Bảng theo dõi đánh số lại liên tục**: **I.** Theo lĩnh vực KD nội bộ / Nhóm ngành (2 cấp) → **II.** Theo thị trường → **III.** Theo phòng ban / Nhân viên (2 cấp).
- Tiêu đề popup bỏ số La Mã (tránh trùng giữa khối trên và bảng): "Tổng nhu cầu trong kỳ", "Nhóm ngành: …", "Phòng ban: …"…
- Thứ tự đọc màn: bộ lọc → **2 khối I/II** → **3 hộp KPI** → **bảng theo dõi 3 phần**.

## ⚠️ PIVOT v10 (2026-08-23) — bộ lọc xoay quanh "Tiêu chí theo dõi"; bảng chỉ hiện 1 tiêu chí

- **2 khối tổng hợp đầu màn bỏ hết số thứ tự** (I / II và 1 / 2) — số La Mã đứng cạnh số lượng gây hiểu nhầm là số liệu.
- **Bộ lọc chuẩn**: `Kỳ` · **`Tiêu chí theo dõi`** · (khối lọc riêng của tiêu chí) · `Công ty` · `Phòng ban` · `Bộ phận` · `Kinh doanh chủ trì` · nút xoá lọc. **Bỏ bộ lọc "Khách hàng"**.
- **Tiêu chí theo dõi** (mặc định **Tất cả**) quyết định bảng dựng thế nào **và** khối lọc nào hiện. Mỗi tiêu chí CHỈ hiện khối lọc của riêng nó — không hiện lẫn khối của tiêu chí khác:
  - `Tất cả` → bảng đủ 3 phần **I / II / III**; khối lọc: **Công ty ▸ Phòng ban ▸ Nhân viên**.
  - `Lĩnh vực KD nội bộ / Nhóm ngành` → bảng chỉ phần lĩnh vực; khối lọc: **Lĩnh vực KD nội bộ ▸ Nhóm ngành** (KHÔNG hiện Công ty/Phòng ban).
  - `Thị trường` → bảng chỉ phần thị trường; khối lọc: **Thị trường**.
  - `Phòng ban / Nhân viên` → bảng chỉ phần phòng ban; khối lọc: **Công ty ▸ Phòng ban ▸ Nhân viên**.
- **Bỏ hẳn bộ lọc "Bộ phận"** (cascade tổ chức rút còn Công ty ▸ Phòng ban ▸ Nhân viên). Đổi tiêu chí thì **xoá giá trị của khối lọc không còn hiện** để không lọc ngầm.
- **Ghi chú trong icon `i` viết bằng lời** (không còn số La Mã vì khối tổng hợp đã bỏ số thứ tự), kèm số thực: vd *"Công thức: Nhu cầu chuyển đổi thành dự án ÷ Tổng nhu cầu bị đóng trong kỳ = 10 / 13 = 76,9%"*.
- Đổi tiêu chí thì **thu gọn lại toàn bộ cấp con** đang bung; nút Xoá lọc trả về tiêu chí mặc định + xoá cả nhóm ngành / thị trường.
- 2 khối tổng hợp + 3 hộp KPI vẫn tính trên danh sách đã lọc; mọi con số vẫn bấm ra popup chi tiết.

## ⚠️ PIVOT v11 (2026-08-23) — thị trường có cấp Phường/xã · dày data · chuẩn hoá bold + tooltip

- **Thị trường thành 2 cấp**: `Tỉnh / Thành phố ▸ Phường / xã` (cha–con giống Phòng ban ▸ Nhân viên), phường/xã mặc định ẩn, bung bằng caret. Khối lọc của tiêu chí Thị trường đổi thành **cascade Tỉnh/TP ▸ Phường/xã** (phường/xã nạp theo tỉnh đang chọn) thay cho select thị trường đơn.
- **Dày data demo**: 6 thị trường (thêm Hải Phòng · Bình Dương · Cần Thơ) · 14 phường/xã · 26 khách hàng · 5 phòng ban (thêm KD 03 · KD miền Tây) · 12 nhân viên · **50 nhu cầu**.
- **Font-weight đồng bộ** (chốt cuối 2026-08-23): TẤT CẢ cột số liệu (`Số nhu cầu · Chuyển đổi thành công · Tỷ lệ thành công · Hết hạn theo dõi · Giá trị dự kiến`) để **chữ thường ở mọi dòng**; dòng tổng / dòng cha phân biệt bằng nền + tên phần in đậm.
- **Tên cột chốt**: `Chuyển đổi thành công` (trước là Thành công) · `Hết hạn theo dõi` (trước là Thất bại) · `Giá trị dự kiến` (trước là Giá trị đầu tư).
- **Hover dòng** dùng nền teal rõ (#d9eff7) cho cả bảng chính lẫn bảng trong popup, có transition.
- **Bảng theo dõi thêm 2 cột kết quả**: **Thành công** (số nhu cầu lập được dự án TKT trong kỳ, chữ xanh lá) và **Thất bại** (số nhu cầu hết hạn theo dõi trong kỳ, chữ cam) — có ở mọi cấp (dòng tổng · dòng cha · dòng con). Bấm số mở popup danh sách tương ứng qua key ghép `<nhóm>@won` / `<nhóm>@lost` (vd `field:nangluong@won`); số 0 không bấm được.
- **Tooltip icon `i` viết theo gạch đầu dòng** (`white-space: pre-line`): dòng đầu là tiêu đề in hoa, các dòng sau là `•` — gồm cả công thức KPI tách rõ tử số / mẫu số / kết quả.

## ⚠️ PIVOT v12 (2026-08-23) — popup chi tiết: có bộ lọc riêng, tóm tắt lên thanh tiêu đề

- **Thông tin tóm tắt chuyển lên thanh tiêu đề popup** (dòng phụ dưới tên chỉ tiêu): `<số nhu cầu> · <tổng giá trị> đ · Kỳ dd/mm – dd/mm`, thêm đuôi "đang lọc trong N nhu cầu" khi bộ lọc popup đang áp.
- **Popup có bộ lọc riêng** (đặt TĨNH trong thân popup nên gõ tìm kiếm không mất con trỏ): ô **tìm kiếm** (khách hàng · meeting · người chủ trì · thị trường · phường/xã · nhóm ngành · mã dự án) · select **Trạng thái nhu cầu** · select **Dự án TKT** (tất cả / đã có / chưa có) · nút **Xoá lọc** · bộ đếm `x / y nhu cầu` bên phải. Mở popup mới thì bộ lọc tự reset; nút Xuất Excel bám đúng danh sách đang lọc.
- **Bảng trong popup cuộn ngang, tiêu đề cột KHÔNG xuống dòng**: bề rộng 13 cột nới lên tổng ~1774px (khung 1366px) nên header luôn nằm 1 dòng.

## ⚠️ PIVOT v13 (2026-08-23) — popup có đủ ô lọc theo cột · khối tổng hợp thu gọn được

- **Popup thêm 6 ô lọc tương ứng các cột**, dạng cascade như màn chính: `Lĩnh vực KD ▸ Nhóm ngành` · `Tỉnh/TP ▸ Phường xã` · `Phòng ban ▸ Nhân viên` (cộng với tìm kiếm · Trạng thái · Dự án TKT đã có).
- **Ẩn ô lọc đã bị CỐ ĐỊNH bởi chính chỉ tiêu đang mở** (rà soát cho mọi popup):
  - popup **Thành công / Thất bại** (và `converted` / `expired`) → bỏ ô **Trạng thái** + **Dự án TKT** (mọi dòng đều cùng kết quả);
  - popup theo **lĩnh vực** → bỏ ô Lĩnh vực; theo **nhóm ngành** → bỏ cả Lĩnh vực + Nhóm ngành;
  - theo **thị trường** → bỏ Tỉnh/TP; theo **phường/xã** → bỏ Tỉnh/TP + Phường/xã;
  - theo **phòng ban** → bỏ Phòng ban; theo **nhân viên** → bỏ Phòng ban + Nhân viên.
  Ô đang ẩn cũng KHÔNG tham gia lọc (giá trị cũ không lọc ngầm).
- **Khối tổng hợp có nút Thu gọn / Mở rộng** ở góc trên bên phải: thu gọn thì chỉ còn dòng meta 1 hàng (kỳ · số nhu cầu · tổng giá trị), giấu 2 khối + 3 hộp KPI.
- Bỏ các dòng "Là tử số…" / "Tử số — …" / "Mẫu số — …" trong tooltip; công thức KPI viết gọn `A ÷ B` + dòng kết quả.
- Fix badge cột **Trạng thái** trong popup tràn ra ngoài ô (nới cột 130 → 158px, badge `max-width: 100%`).

## ⚠️ PIVOT v14 (2026-08-23) — thêm cột Tỷ lệ thành công · fix tooltip hàng tiêu đề

- **Bảng thêm cột "Tỷ lệ thành công"** ngay sau cột Thành công = `Thành công ÷ Số nhu cầu` của CHÍNH dòng đó (dòng tổng = tỷ lệ chuyển đổi chung của kỳ). Bảng thành 8 cột.
- **Fix tooltip icon `i` ở hàng tiêu đề bảng bị ẩn**: tooltip vốn đổ LÊN nên bị khung `.market-table-wrap` (overflow:auto) cắt mất → thêm biến thể `.rsum-info--down` đổ XUỐNG (mũi tên lật) dùng cho icon trong `thead`.
- **Nút xoá lọc trong popup** đổi thành **icon refresh tròn** dùng chung `.calendar-filter-clear-btn` với nút xoá lọc trên toolbar báo cáo.

## ⚠️ PIVOT v15 (2026-08-23) — nút Ẩn/Hiện chi tiết ở ô tiêu đề + làm nổi dòng cha đang bung

- **Nút "Ẩn chi tiết / Hiện chi tiết" nằm ngay trong ô tiêu đề cột "Nội dung theo dõi"** — bấm 1 phát bung (hoặc thu) TOÀN BỘ cấp con cuối của tiêu chí đang xem (nhóm ngành · phường/xã · nhân viên; tiêu chí "Tất cả" thì cả 3 phần). Caret trên từng dòng cha vẫn dùng độc lập.
- **Dòng cha đang bung** được tô nền (#e8f2f8) và **in đậm toàn bộ số liệu** để khoanh vùng cha–con; dòng cha đang đóng và dòng con vẫn chữ thường như quy tắc đã chốt.

## Quyết định lớn v1 (đã chốt qua brainstorming — 1 phần đã pivot)
- **Sản phẩm:** mockup HTML tĩnh trước (chưa code Vue thật, chưa định DB/API).
- **2 chế độ (tab):**
  - **Theo lịch:** toggle Tháng + Tuần; lịch gộp 3 loại sự kiện (🟣 Kế hoạch tiếp theo · 🟢 Lịch sử làm việc · 🔵 Meeting/công tác), có filter bật-tắt; click chip → popover chi tiết.
  - **Theo thị trường:** accordion nhóm theo thị trường (header đếm KH theo trạng thái); click dòng KH → **drawer trượt phải** hiện đầy đủ thông tin + timeline lịch sử + kế hoạch tiếp theo.
- **Dải KPI 4 trạng thái** trên đỉnh (Tiềm năng/Đang chăm sóc/Đã chốt/Hủy) + **Đánh giá chung / Ghi chú chung** cuối trang.
- **Người theo dõi** (header ảnh mẫu) → filter ở toolbar.
- Mock data bịa hợp lý (~4-5 thị trường, ~10-15 KH, 2-3 NV) — thay sau nếu user có list thật.

## Ngoài scope
Code Vue thật, DB/migration, API contract, phân quyền — để phase sau.

## ⚠️ PIVOT v12 (2026-08-24) — đổi tên file · thứ tự cột · mục đích báo cáo vào icon topbar

- **Tên file mockup** đổi cho khớp tên báo cáo: `bao-cao-tong-hop-nhu-cau-khach-hang.html` → **`bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`**.
- **Thứ tự cột bảng theo dõi** (chốt): `STT · Nội dung theo dõi · Số nhu cầu · **Giá trị dự kiến** · Chuyển đổi thành công · Tỷ lệ thành công · Hết hạn theo dõi · Tỷ trọng giá trị` — 2 cột quy mô (số lượng + giá trị) đứng cạnh nhau, rồi mới tới nhóm cột kết quả. Cột *Tỷ trọng giá trị* vẫn ở cuối.
- **Topbar bỏ tên người dùng**, thay bằng **icon `i` mục đích báo cáo** (hover mới hiện, tooltip 420px):
  - Tổng hợp được các nhu cầu KH mà nhân viên thu thập trong kỳ, gồm: nhu cầu mới PS trong kỳ này · nhu cầu thu thập từ kỳ trước nhưng chưa đóng.
  - Theo dõi được tỷ lệ **chuyển đổi thành công** NHU CẦU thành dự án TKT.
  - Theo dõi tỷ lệ **thất bại của NHÂN VIÊN** khi nhu cầu bị đóng → chi tiết theo thị trường / lĩnh vực kinh doanh.

## ⚠️ PIVOT v13 (2026-08-24) — chuẩn hoá popup báo cáo: thống kê chéo + cột theo cơ cấu

Mọi popup drill-down đều theo cùng 1 khuôn: **bộ lọc → khối thống kê chéo → bảng chi tiết**.

- **Cơ cấu của popup** suy từ key drill; popup thống kê theo 2 cơ cấu CÒN LẠI:
  | Popup mở theo | Thống kê chéo |
  |---|---|
  | Lĩnh vực KD nội bộ (`field:` · `sector:`) | Thị trường · Phòng ban |
  | Thị trường (`market:` · `ward:`) | Lĩnh vực KD · Phòng ban |
  | Phòng ban (`dept:` · `emp:`) | Thị trường · Lĩnh vực KD |
  | Popup tổng (`all` `carried` `arisen` `closed` `converted` `expired`, kể cả `@won` / `@lost`) | đủ 3 cơ cấu |
- **Khối thống kê** nằm dưới bộ lọc, thiết kế PHẲNG (không khung nền, chỉ 1 đường kẻ dưới): mỗi cơ cấu 1 hàng chip `tên · số nhu cầu · %`, giá trị đầu tư nằm trong tooltip chip. Tính trên danh sách ĐANG LỌC trong popup, 0 dòng thì ẩn. **Bấm chip = lọc nhanh** theo mục đó (bấm lại = bỏ lọc).
- **Thứ tự cột bảng chi tiết bám ĐÚNG THỨ TỰ CÁC HÀNG TRONG KHỐI THỐNG KÊ** (chốt 24/08): summary xếp cơ cấu nào trước thì cột của cơ cấu đó đứng trước — **ngay sau STT, TRƯỚC cả cột Khách hàng** — áp cho cả popup tổng. Cột của chính cơ cấu đang xem xếp ngay sau, phần còn lại giữ thứ tự mặc định.
- **Khối thống kê: mỗi cơ cấu đúng 1 HÀNG, không xuống dòng** — dài thì cuộn ngang cả khối, nhãn cơ cấu ghim bên trái.
- Cột popup khai báo 1 lần trong `DRILL_COLDEFS` (`label · width · td() · val()`) → bảng · tiêu đề · Excel danh sách luôn khớp thứ tự.
- **Luật bộ lọc trong popup** (chốt 24/08): cơ cấu đang xem → bỏ ô lọc của chính nó, chỉ còn ô cấp con **giới hạn trong mục đang xem**; mở ngay ở cấp con (nhóm ngành / phường xã / nhân viên) → bỏ cả cặp. 2 cơ cấu chéo **chỉ lọc tới cấp cha** (Lĩnh vực · Tỉnh/TP · Phòng ban), không có cấp con. Popup tổng giữ đủ 2 cấp cả 3 cơ cấu. **Bỏ hẳn ô lọc "Dự án TKT"** ở mọi popup; ô "Trạng thái" vẫn ẩn khi chỉ tiêu đang mở đã cố định kết quả.

## ⚠️ DATA DEMO v2 (2026-08-24) — quy mô 20 thị trường / 10 phòng ban

- **20 tỉnh/TP theo bộ đơn vị hành chính sau sáp nhập 2025** (bỏ Bình Dương — nay thuộc TP.HCM), mô hình 2 cấp **Tỉnh/TP ▸ Phường/xã** (45 phường/xã, không còn quận/huyện) — khớp đúng cấu trúc 2 cấp của màn.
- **10 phòng ban / 26 nhân viên / 60 khách hàng / 200 nhu cầu · ~2.065 tỷ**.
- Khách hàng + nhu cầu **sinh cố định bằng LCG có hạt giống** (không dùng `Math.random`) → demo không "nhảy số" giữa các lần mở. Phân bổ chủ ý để kỳ 08/2026 có đủ 3 nhóm chỉ tiêu: ~22% chuyển đổi thành dự án · ~8% hết hạn theo dõi · ~4% dừng theo dõi · 65% meeting trong kỳ / 35% kỳ trước.
- **Chuẩn popup (chốt 24/08)**: tiêu đề *"Bạn đang xem kết quả CSKH tiềm năng theo: <cơ cấu> — <mục>"* · khối **"Kết quả KPI"** (3 hộp dùng lại component KPI của màn chính, bản thu nhỏ) đặt TRÊN khối **"Phân bổ nhu cầu theo cơ cấu"** · header có **nút phóng to toàn màn hình** · footer có **In danh sách** (bản in bám đúng cột + bộ lọc của popup) và **Xuất Excel danh sách**.
- **Tên khách hàng demo là tên pháp nhân đầy đủ** (Công ty CP / TNHH / Trường Cao đẳng nghề …), không dùng tên thương hiệu trần.
- **Popup nhu cầu HẾT HẠN THEO DÕI** (`expired` · hậu tố `@lost`): bỏ cả khối KPI lẫn khối phân bổ theo cơ cấu — chỉ còn bộ lọc + bảng chi tiết (KPI của nhóm này luôn 0% / 0% / 100%).
- **Đổi tên (24/08)**: *Lĩnh vực KD nội bộ* → **Lĩnh vực công ty kinh doanh** (áp ở mọi nơi: bộ lọc · tiêu chí theo dõi · bảng theo dõi · popup · drawer · bản in).
