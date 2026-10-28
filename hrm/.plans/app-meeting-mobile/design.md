# Design (tóm tắt) — App Meeting trên di động

**Sản phẩm:** bộ thiết kế giao diện cho `TPE_APP` (Flutter) — phân hệ Meeting.
**Không phải task code**: đầu ra là file `.pen` + PDF/PNG bàn giao, không sửa `hrm-api` / `hrm-client`.

| | |
|---|---|
| File thiết kế | `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen` |
| Bàn giao | `~/Documents/demo giao dien/pencil_design/exports/` (v11 · 16/09/2026) |
| Quy mô | **50 artboard**, khung bản đồ 2825 × 24617 |
| Nhánh code đối chiếu | `tpe-develop-assign` (cả 2 repo) |

## Mục tiêu

Đưa toàn bộ nghiệp vụ Meeting của bản web lên điện thoại 393px, **bám 100% logic web** — chỉ đổi
cách trình bày, không đổi luật nghiệp vụ. Mọi chỗ buộc phải khác web đều ghi rõ lý do và đánh dấu
cần chốt lại.

## Các quyết định lớn đã chốt

1. **Điều hướng Hub** — màn chi tiết meeting là bảng điều khiển liệt kê 9 khối, bấm từng khối mở màn con.
   Không bê 4 tab ngang của web sang điện thoại. Kéo theo nhu cầu **API lưu từng phần** (`api-luu-tung-phan.md`).
2. **Phạm vi dữ liệu = của tôi** — app chỉ quản lý meeting mình **chủ trì hoặc tham gia**; bỏ bộ lọc
   Công ty / Phòng ban. Tab cấp 1 tách theo **đúng vai trò**, hai tab rời nhau.
3. **Chọn khách hàng / người liên hệ / dự án TKT** có màn riêng + lối **thêm nhanh**, vì trên điện thoại
   không thể mở modal bảng nhiều cột như web.
4. **Thông báo chỉ một kiểu** — dải nằm trong luồng, 3 loại màu (đỏ lỗi · xám khoá · xanh thông tin).
   Không dùng toast đè. Hộp thoại hỏi ý kiến vẫn là popup.
5. **Dấu `*` bắt buộc theo trạng thái từng màn**, khác với thanh *Mức độ hoàn thiện hồ sơ* (đếm theo
   bộ khối cần cho Hoàn thành).
6. **Không viết chú thích logic vào trong khung điện thoại** — phần giải thích nằm ở caption artboard;
   ghi chú kỹ thuật cho dev nằm ở khối `DEV NOTE` bên ngoài khung máy (4 màn: 01 · 04a · 06 · 21).

## Chốt với khách — 14/10/2026

| # | Câu hỏi | Chốt |
|---|---|---|
| 1 | Màn 06 chọn 1 hay nhiều Giải pháp / Hạng mục | **Meeting chỉ chọn tới cấp DỰ ÁN** → bỏ hẳn phần chọn Giải pháp / Hạng mục khỏi app |
| 2 | Meeting gắn nhiều dự án | Hết vướng sau câu 1: màn 06 chỉ còn danh sách dự án TKT đã gắn (không còn cây giải pháp theo từng dự án) |
| 3 | Màn 42 — địa chỉ xuất hoá đơn | Mặc định **chép từ địa chỉ chính, cho phép sửa** |
| 4 | Màn 44 — liên hệ tạo từ app tự vào Thành phần KH | **Có** (như web) |
| 5 | Màn 18 — xoá dòng NGƯỜI 1 | **Làm theo web** (giữ icon xoá) |
| 6 | Phiếu tổng hợp kết quả meeting #11130 | **Có đưa vào app** — cần vẽ khối trên Hub + màn nhập + màn xem |
| 7 | Nút Xem file (màn 11 · 19 · 36 · 38) | **Chỉ xem PDF + ảnh**; loại khác chỉ có Tải xuống |
| 8 | `customerMeetingHistory()` | **Thay** điều kiện `created_by` bằng "user đang đăng nhập có trong thành phần", không cộng thêm |
| 9 | Biên bản tạo task giao người xử lý | **Bổ sung sau** — bỏ khỏi trạng thái Blocked |

## Khảo sát web — Meeting theo đối tượng (nhánh `gop_db`, 14/10/2026)

Nguồn: `hrm-api` 59537031f + `hrm-client` 3ea829c51 (09/10) · design web `.plans/gop-db/meeting-theo-doi-tuong/design.md`.

- **Cấu hình nằm ở LOẠI MEETING**: `meeting_types.target_type` = 1 Dự án TKT · 2 Hợp đồng · NULL không. Bỏ checkbox "Meeting theo dự án".
- **Bắt buộc ở MỌI lượt lưu, kể cả Lưu nháp** (`ValidatesMeetingTarget` chạy trong `after()`, không xét status):
  loại TKT → `projects` ≥ 1 ("Vui lòng chọn Dự án TKT.") · loại HĐ → `contract_id` ("Vui lòng chọn Hợp đồng.").
  ⇒ App PHẢI có ô đối tượng ngay ở màn 03 Tạo meeting, không thể để sang màn con của Hub.
- **Dự án TKT**: chọn NHIỀU · nguồn `GET assign/prospective-projects/getForMeeting?meeting_id=` · tiến trình 2→10 · phạm vi: mình tạo / làm giải pháp / hỗ trợ · chọn dự án → tự điền KH.
- **Hợp đồng**: chọn MỘT · nguồn `GET assign/contracts/for-meeting?customer_id=&include_id=` · mọi trạng thái trừ Đang tạo, Đã thanh lý · không lọc quyền, KHÔNG trả tiền/SĐT ·
  đã chọn KH → chỉ HĐ của KH đó; chọn HĐ trước → tự điền KH + TÊN người liên hệ (SĐT để trống) · đổi KH khác → bỏ HĐ · đổi loại khỏi HĐ → bỏ HĐ.
  Dòng hiển thị: `Mã HĐ` + tên KH + badge trạng thái (`status_name` / `status_color` do BE trả).
- **Hiện ô** Dự án TKT khi loại = TKT HOẶC meeting đã có dự án HOẶC tạo từ dự án (khi đó dấu `*` chỉ có ở loại TKT). Ô HĐ hiện khi loại = HĐ hoặc meeting đã có HĐ.
- **Đối tượng cũ đã ra khỏi dải trạng thái vẫn giữ** khi sửa meeting (BE chỉ kiểm giá trị mới chọn thêm).
- Màn xem: HĐ = mã (bấm mở HĐ) + tên KH + badge trạng thái. Lịch sử meeting ghi "Hợp đồng: cũ → mới".
- ⚠️ Web VẪN giữ Giải pháp / Hạng mục theo từng dự án (`solution_id`, `solution_module_id`). App bỏ theo chốt #1 → app gửi lại payload `projects` PHẢI giữ nguyên 2 cột này của dự án đã gắn, không được xoá dữ liệu nhập từ web.
- Phát hiện phụ: web có tab **Nhiệm vụ** (#11456, chỉ ở màn chi tiết) — nhiều khả năng là logic "tạo task" của câu 9, để bổ sung sau.

## Đề xuất — tải danh sách Dự án TKT đồng nhất web + app (14/10/2026, ĐÃ DUYỆT — chưa code BE/FE web)

> Triển khai trên nhánh `gop_db` → theo dõi tại `.plans/gop-db/meeting-chon-du-an-tkt/`.

**Hiện trạng web:** `getForMeeting?per_page=10000` tải MỌI dự án trong phạm vi, mỗi dòng kèm toàn bộ resource
(`RESOURCE_EAGER_RELATIONS` + 5 subquery giải pháp) rồi lọc KH / tìm kiếm ở FE. Lý do tải nặng: chọn dự án là
chép nguyên object vào `form.projects` để tab "Dự án tiền khả thi" có đủ trường. App không thể dùng kiểu này.

**Đề xuất — tách 2 việc: CHỌN (nhẹ, phân trang) và LẤY CHI TIẾT (chỉ dự án vừa chọn)**

1. Endpoint mới `GET assign/prospective-projects/meeting-options` — dùng chung web + app.
   - Tham số: `search` (mã / tên) · `customer_id` · `page` · `per_page` (mặc định 20, trần 50).
   - Điều kiện GIỮ NGUYÊN `getForMeeting`: tiến trình 2–10 + (người tạo / người làm giải pháp / người hỗ trợ).
     Tách thành 1 scope dùng chung (vd `scopeSelectableForMeetingBy($userId)`) để 2 endpoint không lệch nhau.
   - Trả gọn: `id, code, name, customer_id, customer_code, customer_name, status, status_name, status_color, is_parent`.
     KHÔNG eager load, KHÔNG subquery giải pháp, KHÔNG ngân sách.
   - Sắp id giảm dần; có `meta` phân trang. Lọc KH và tìm kiếm làm ở BE (thay lọc FE).
   - ⚠️ Tên `meeting-options` đã dùng cho chiều ngược lại (#11142: meeting cho form dự án) → đặt tên khác, vd `options-for-meeting`.
2. Dự án ĐÃ GẮN không cần nằm trong danh sách chọn: lấy từ chi tiết meeting (`form.projects` đã có mã + tên) và
   hiện thành chip đã chọn. Bỏ cơ chế `meeting_id` / include ở danh sách. BE vẫn cho lưu dự án cũ ngoài dải
   (`ValidatesMeetingTarget` chỉ kiểm dự án mới thêm) — không đổi.
3. Chọn thêm 1 dự án → gọi chi tiết đúng dự án đó để điền tab "Dự án tiền khả thi" (web). Dùng endpoint riêng có
   cùng điều kiện phạm vi (vd `GET .../options-for-meeting/{id}`), KHÔNG dùng `show` vì `show` theo quyền xem dự án
   — người hỗ trợ không có quyền xem dự án sẽ bị 403. App không cần bước này (đã bỏ Giải pháp / Hạng mục).
4. FE web: `MultiSearchPicker` hiện chỉ lọc tại chỗ (prop `items`). Cần chế độ tìm phía server: gõ → debounce 300ms
   + huỷ request cũ → gọi endpoint (1); cuộn cuối → trang kế. Đây là component DÙNG CHUNG → hỏi trước khi sửa,
   hoặc tạo component mới riêng. Chưa có component tìm phía server nào trong `components/` để bám.
5. `getForMeeting` cũ: giữ tới khi web chuyển xong, sau đó gỡ (còn chỗ khác gọi thì kiểm trước).

**App (màn Chọn dự án TKT):** ô tìm (mã / tên) + danh sách thẻ phân trang cuộn, mỗi thẻ: mã · tên · KH · badge
tiến trình (màu BE trả). Chọn nhiều, chip đã chọn ở đầu màn. Đã chọn KH ở meeting → truyền `customer_id`.
Có nút Thêm nhanh dự án TKT (màn 47).

## Tài liệu liên quan

| File | Nội dung |
|---|---|
| `plan.md` | 5 phase + **danh sách việc chuyển cho dev** + 6 câu cần chốt với khách |
| `chon-khach-hang-va-lien-he.md` | **Spec chi tiết** — 17 mục, ghi từng vòng sửa kèm căn cứ tra từ source web |
| `api-luu-tung-phan.md` | Đề xuất nhóm endpoint lưu từng phần + danh mục Lý do huỷ |
| `docs/superpowers/specs/2026-09-16-app-meeting-mobile-design.md` | Spec kỹ thuật gom đầu mối |

## Đồng bộ theo web gop_db (19/10/2026) — user: "Cập nhật những thay đổi bản web sang thiết kế app"
Nguồn web: meeting-tab-du-an-nhan-su (14/10) · meeting-chon-du-an-tkt (14–15/10) · meeting-form-redesign D1–D9 (15/10) + vòng 2c (19/10, client 53421e1cb).

| # | Chốt 19/10 | Hệ quả trên app |
|---|---|---|
| W1 | Bỏ tạo dự án từ meeting theo web | Xoá màn 47 + nút "Thêm nhanh dự án" ở 48 |
| W2 | Tab Dự án TKT: bỏ nút "Xem chi tiết" (app chưa có phân hệ Dự án) | 06/34 chỉ thẻ tóm tắt trường chính + phiếu thu thập |
| W3 | Không sắp xếp thứ tự nhân sự trên app | Hiển thị đúng thứ tự đã lưu, thêm mới nối cuối nhóm; sắp xếp làm trên web |
| W4 | Kết luận cuộc họp nằm TRONG Biên bản (user chốt 19/10) | Hub bỏ dòng Kết luận; màn 09 có khối "Kết luận cuộc họp *" cuối biên bản, bấm mở trình soạn 13 (Xong → về 09, Lưu biên bản ghi cả 2); màn 40 gộp vào 37; Mức độ hoàn thiện x/4 → x/3 (4 nếu có Khảo sát); artboard 51 → 50 |
| W5 | Thông tin chung gập/mở từng khối (user chọn phương án A, 19/10) | Chỉ khối đang nhập mở, nhập đủ tự gập thành dòng tóm tắt + mở khối kế; màn sửa mở ra 4 khối gập. Trường chọn = dòng nhãn trái–giá trị phải, trường gõ giữ ô nhập. Lỗi validate: khối có lỗi tự mở, khối gập ghi "n lỗi". Thêm nhanh KH chỉ còn trong màn 41/41b; nút bản đồ thành icon trong dòng Địa điểm. Áp 03 · 05 · 25 · 28; 33 (xem) giữ nguyên. Tài liệu (chuẩn bị / biên bản) vẫn để dòng riêng trên Hub cho dễ xem |
| W6 | Gộp khối như web Phase 4 (19/10) | ① Thông tin cuộc họp = Phân loại · Loại · Tên · Mục tiêu; ② Đối tác (đổi tên từ "Khách hàng & đối tượng"); ③ Thời gian, địa điểm & chủ trì. 03 mở sẵn ①; 05/28 tóm tắt ① gộp; 25 ① mở kèm lỗi Tên; 33 xem 3 khối |
| W7 | Style phân hệ (19/10) | Màn chọn phân hệ 00b (5 phân hệ, mỗi phân hệ 1 màu nhận diện: Chấm công #2E71C3 · Công việc #1E8A63 · Meeting #0E8FA8 · Đào tạo #6B54B8 · Cơm #D9752A) · drawer 00c–00g · C/BottomNav dùng chung (theme `phanhe`) · Tổng quan Meeting 00h. Áp vào bộ màn meeting: cam #E8972C → xanh ngọc #0E8FA8 (nền nhạt #E6F6F9), StatusBar + Header thành dải gradient xanh ngọc chữ trắng, nút chính gradient bo 12, badge "chờ" về hổ phách #D97706 (bảng 9 màu web), màn 01 thay TabBar cũ bằng BottomNav (bỏ FAB trùng). Backup: meeting-mobile.backup-20261019-truoc-style-phan-he.pen |
| W8 | Dashboard + khung phân hệ (19/10) | 00b chọn phân hệ thêm hiệu ứng nền (vòng conic 5 màu, vệt sáng, điểm sáng). Drawer: Chấm công 00c/00c' (852px, đầu+cuối cố định, giữa cuộn + thanh cuộn + mờ mép), Meeting 00d, Công việc 00e, Cơm 00f, Đào tạo 00g. Template C/BottomNav (biến nav-c/nav-c2/nav-tint/nav-glow theo theme `phanhe`; 4 tab + nút giữa). Tổng quan Meeting 00h (thứ tự: Sắp diễn ra → Cần xử lý gấp → Lịch hôm nay → Thống kê tháng dải 4 số → Phòng trống) + 00h' (không có cuộc họp sắp tới → ẩn hẳn khối). Tổng quan Chấm công 00i: khối riêng "Ca làm trong ngày" nhiều ca/phiếu (ca hành chính · phiếu giao việc · phiếu công tác · làm thêm), nhãn hình thức Máy khuôn mặt / App·GPS, nút Chấm công chỉ ở mục allow_app — logic xem khao-sat-tpe-app.md |
| W9 | 20/10 | 00b nền = ảnh nền màn đăng nhập app (TPE_APP assets/images/image.png → pencil_design/images/app-login-bg.png, .pen trỏ đường dẫn tương đối — chia sẻ phải kèm thư mục images/), bỏ hiệu ứng tự vẽ. 00j Thông báo (chuông) dùng chung mọi phân hệ: header navy, gạt Tất cả/Chưa đọc, chip lọc phân hệ, gom theo ngày, dòng tách template [PREFIX] Nhóm hành động: **Tên**. Ghi chú (skill notification-convention), màu nhóm hành động theo nghĩa. Prefix DXN/COM/KH/TBNB chờ chốt. Xuất PNG @3x v12: exports/Meeting-Mobile_Tung-man_v12_2026-10-20/ (60 ảnh, trước khi đổi nền 00b + chưa có 00j; trang 00 Tổng quan luồng chưa cập nhật) |
| W10 | 20/10 | 00i' (bản sao cạnh 00i, frame t41x9): khối "Ca làm trong ngày" v2 — 3 thẻ rời → 1 khối: dải thời gian 08–18h (thanh màu theo loại, vạch cam giờ hiện tại, vùng mờ đã qua, thanh nhạt đã xong, ca chồng giờ xuống làn 2) + mỗi ca/phiếu 1 dòng (tên + giờ ca · địa điểm/đếm ngược; phải chỉ 1 thứ: Vào→Ra + chip Tại máy / Xong / nút Chấm). Mã phiếu, KH, tên máy, chip hình thức, số PGV con dời vào màn chi tiết. Chờ user chọn 00i hay 00i' |
| W11 | 26/10 · Bộ lọc dùng chung (đề xuất, chờ duyệt) | User: bộ lọc hiện tại "to + thô + xấu, hiệu ứng chưa mượt" + "không biết đang lọc theo tiêu chí gì"; không có app tham chiếu → Claude đề xuất. Vẽ 4 trạng thái trên màn Phiếu giao việc (phân hệ Công việc #1E8A63), canvas x=10061…11480 y=-1450: **BL1** danh sách thường (ô tìm xám không viền + nút lọc cùng hàng, hàng chip lọc nhanh có số đếm, dòng kết quả) · **BL2** bảng lọc bottom sheet nấc 1 (chỉ 4 loại trường: chip ≤6 giá trị có ✓ · khoảng ngày 1 dòng + chip nhanh · dòng chọn › · 'Thêm tiêu chí' gập; Công ty/Phòng ban gộp 'Phạm vi'; footer 1 hàng [↺ Đặt lại | Xem 24 phiếu] — user chốt 26/10 đưa Đặt lại xuống cạnh nút chính cho trong tầm ngón cái, BL3 tương tự [✕ Bỏ chọn | Xong · 2 người]) · **BL3** trang con chọn người trượt ngang TRONG bảng, nấc 2 (tìm phía máy chủ, chip đã chọn, tick nhiều, 'Xong · 2 người') · **BL4** danh sách đang lọc (nút lọc tô màu + số, hàng chip tiêu chí có ✕, '24 / 128 phiếu' + 'Xoá lọc'). Số đo/chuyển động là Claude tự chọn: chữ 15/13, dòng 52, chip 32, spring ~350ms, rung selectionClick. Khảo sát hiện trạng: `khao-sat-bo-loc.md` (làm trên code TRƯỚC khi pull develop 331f51b — bản mới đã đổi màu ngăn lọc theo phân hệ, ô tìm cạnh nút lọc). Backup: meeting-mobile.backup-20261026-truoc-bo-loc.pen |

Tự chốt (thuần UI, bám web): thứ tự 5 khối + màu khối (indigo `#4F46E5` · sky `#0284C7` · amber `#D97706` · emerald `#059669` · pink `#DB2777`)
ở màn nhập Thông tin chung; KH chọn trước → ô Dự án TKT/HĐ khoá "Chọn khách hàng trước"; Gợi ý tên; liên hệ 1 ô;
Hub: "Dự án tiền khả thi" → "Dự án TKT" chỉ hiện khi có dự án; "Thành phần tham dự" + "Điểm danh" → 1 dòng "Nhân sự tham gia".
