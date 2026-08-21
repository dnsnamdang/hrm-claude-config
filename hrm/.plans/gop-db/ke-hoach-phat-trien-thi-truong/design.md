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

File độc lập **`bao-cao-tong-hop-nhu-cau-khach-hang.html`** (cùng folder). Layout bám **ảnh Excel** user gửi; style tái dùng NGUYÊN bộ design token + component của `bao-cao-ket-qua-meeting-theo-thi-truong.html` (navy+teal, `.market-table` outline, `.market-toolbar`/`.calendar-filter-*`, `.rsum-*`, `.minutes-modal`, `.ticket-drawer`).

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
