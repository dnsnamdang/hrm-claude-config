# Plan — Đổi toàn bộ UI app TPE_APP theo thiết kế

## Phase 1 — Nền tảng UI chung

### FE
- [x] Màu nhận diện 5 phân hệ + navy + bảng slate (`app_module.dart`)
- [x] Header `PrimaryAppBar`: gradient theo phân hệ, nút kính quay lại / menu / trang chủ
- [x] Bottom menu: nền trắng bo 24, tab viên thuốc, chấm đỏ badge
- [x] `PrimaryButton` gradient + `SecondaryButton` viền xám
- [x] `PrimaryTextField` nhãn 12, ô 44, lỗi viền đỏ
- [x] `StatusBadge` bo 4, chữ 11, viền mảnh
- [x] Màn chọn phân hệ theo khuôn 00b
- [x] Header màn chính Đào tạo chuyển sang `PrimaryAppBar`
- [x] Chạy simulator kiểm tra (tpeLocal, iPhone 15)

## Phase 2 — Khung phân hệ (drawer + tab)

### FE
- [x] Màn chọn phân hệ 4 mục (tách Chấm công / Công việc)
- [x] Drawer mới `ModuleDrawer` (giữ `LeftMenuView` cũ cho màn vào thẳng không qua khung) theo 00c: hồ sơ + thẻ phân hệ + nút Đổi, nút CTA, nhóm không gập, ô icon, badge, Cài đặt / Đăng xuất / phiên bản
- [x] Khung tab phân hệ dùng chung (4 tab + nút giữa, giữ trạng thái, nút ☰ ở tab gốc mở drawer)
- [x] Chấm công: tab Tổng quan · Lịch sử · [Chấm công] · Bảng công · Đơn từ + drawer 00c
- [x] Công việc: tab Tasks · Tiến độ · [Giao việc] · Phiếu · Phê duyệt + drawer 00e
- [x] Quản lý cơm: tab Lịch cơm · Thông báo · [Ăn dài ngày] · Phiếu · Cài đặt + drawer 00f
- [x] Đào tạo: tab Tổng quan · Khoá học · [Đăng ký] · Lịch thi · Năng lực + drawer 00g

## Phase 3 — Header toàn app

### FE
- [x] Màn tự dựng `AppBar` navy → `PrimaryAppBar` (còn giữ có chủ đích: 2 trình xem ảnh toàn màn nền đen ở task)
- [x] Nút hành động trên header (lọc, thêm, chuông) theo khuôn ô kính, nút lọc có chấm đỏ khi đang lọc

## Phase 4 — Thân màn

### FE
- [x] Khối dựng sẵn `AppCard` / `SectionTitle` / `InfoLine` / `BottomActionBar` / `DangerButton` + 19 widget dùng chung (FilterView, ReasonInputDialog, AppEmptyWidget, container…) theo khuôn
- [x] Màn danh sách: thẻ phiếu AppCard + InfoLine + StatusBadge, bộ lọc FilterView, trống dữ liệu (Chấm công 24 file · Công việc 30 thư mục · Đào tạo 25 màn · Cơm + Thông báo)
- [x] Màn form / chi tiết: BottomActionBar Huỷ + Lưu, DangerButton Từ chối/Xoá, ô nhập, chip

## Phase 5 — Tổng quan Chấm công (00i)

### BE (hrm-api)
- [x] listTimesheetTypes trả allow_app / allow_conn / machines theo từng ca-phiếu (hrm-api `develop`, đã kiểm bằng tinker 3 kiểu ca)
- [x] timekeeper/employee trả job_type_key + job_id + job_assign_id thô
- [x] Ca làm việc dashboard: chưa có bảng công trong ngày thì lấy ca được phân (getWorkshiftForAttendance)

### FE
- [x] Màn Tổng quan Chấm công theo 00i (ca trong ngày ghép lượt chấm theo job_type_key/job_id, tạo phiếu nhanh, công tháng, phép, đi muộn, nhân sự hôm nay)

## Phase 6 — Thông báo (00j)

### FE
- [x] Màn Thông báo: nút gạt Tất cả / Chưa đọc, chip lọc phân hệ, gom theo ngày, dòng theo template, vuốt Đã đọc (lọc ở app vì API chỉ có page/limit; chưa có Xoá vì thiếu API)
- [x] Sửa đường dẫn "Đọc tất cả" `mark_all_as_seen` (404) → `mark_all_as_read`

## Phase 6b — Sửa lỗi sau restyle

### FE
- [x] `BottomActionBar` giãn chiếm cả màn (CommonContainer mặc định căn giữa) → form trắng, chỉ thấy 2 nút
- [x] Giấy báo vắng mặt mất `buildPageListeners` (form không điền dữ liệu) → khôi phục
- [x] Rà ngữ nghĩa 169 file đã sửa (5 nhóm): thêm 1 chỗ mất kéo-làm-mới khi lỗi tải trang đầu ở Thông báo → khôi phục; còn lại không mất logic
- [x] Theo ý user: trả tiêu đề cũ 4 màn Cơm, cuối tuần lịch cơm về đỏ; nút đáy form giữ ghim như thiết kế
- [x] Khôi phục bản mới Tổng quan Chấm công + Thông báo + 3 file hrm-api (user duyệt giữ)
- [x] ~~Trả về chữ cũ~~ → hoàn tác theo ý user (giữ bản design) — (nhãn ':', nhãn mã/trạng thái, dấu *, không cắt '…', bỏ tiêu đề khối mới) ở các màn đã restyle
- [x] ~~Trả về hành vi cũ~~ → hoàn tác theo ý user — hộp lý do, hộp chi phí, ô nhập chung, rung AppCard, đổi mật khẩu, bài thi, báo cáo tiến độ, nút Home cơm, FAB thiết bị; 3 màu nghĩa
- [x] ~~Trả thêm~~ → hoàn tác: nút bộ lọc mờ khi chưa có hàm xử lý, chi tiết thông báo chỉ có nút quay lại khi còn màn sau, SafeArea form công tác
- [x] Dựng lại bản design từ diff rà soát + đảo ngược thao tác (analyze 0 error/warning)
- [ ] Chờ user duyệt các thay đổi BE / dữ liệu hiển thị (Tổng quan Chấm công, Thông báo)
- [x] Sửa màn đỏ khi chạm ô nhập (SystemContextMenu → AdaptiveTextSelectionToolbar ở CommonTextField)

### Thông báo — BE trả trường phân hệ + lọc + số đếm (21/10/2026)
- [x] BE: helper NotificationMeta (module theo type, tách template, dựng nội dung chuẩn cho thông báo mới)
- [x] BE: index nhận module + unread, mỗi dòng thêm module/prefix/action/object_name/note/object_id, trả counts
- [x] BE: mark_all_as_read nhận module, update 1 câu thay vì vòng lặp
- [x] App: model + repo đọc trường mới và counts, chip + nút gạt lọc ở BE
- [x] App: nối nhóm 1 (cơm, điểm danh, gia hạn/kết thúc sớm, báo cáo tiến độ, bảng lương); nhóm 2 báo "xem trên web"
- [x] Test simulator (lọc chip, Chưa đọc, Đọc tất cả theo phân hệ, mở cơm, báo xem trên web) + API local
- [x] Sửa kèm: trang cuối danh sách thông báo (luôn hiện "Xem cũ hơn"), bấm chip khi trang đầu chưa tải xong
- [x] BE: quy đổi câu cũ về template lúc trả API (NotificationLegacyFormat) — 128/128 câu mẫu PROD + local ra đủ mã + nhóm hành động
- [x] BE: cắt hồ sơ người gửi trong API (chỉ id/mã/tên/ảnh); Meeting lên/chốt lịch gửi kèm nhóm hành động
- [x] App: thiếu mã → tag tên phân hệ; chuông Tổng quan làm mới khi quay về từ màn Thông báo
- [x] App: ghi chú thông báo dài cắt 2 dòng + "Xem thêm / Thu gọn" (widget dùng chung custom_view/expandable_text.dart)
- [x] Tổng quan mọi phân hệ dùng chung header: NotificationBellButton (chuông + số, tự làm mới) + OverviewHeaderBand (ngày · lời chào · tóm tắt) — Chấm công, Đào tạo
- [x] Push màn khoá cùng khuôn: tiêu đề "Hành động · Phân hệ", thân "Tên. Ghi chú" (NotificationMeta::push)
- [x] Cơm › Thông báo cùng khuôn dòng với màn Thông báo chung (widget ui/notification/notification_tile.dart dùng chung) + gom theo ngày; sửa kèm type 8 "Admin huỷ cơm" chưa có trong enum làm vỡ cả danh sách
- [x] Web: chuông topbar (BasicSubsystem) + màn /timesheet/notifications cùng khuôn app — components/notification/NotificationItem.vue + utils/notificationDisplay.js; màn danh sách có Tất cả/Chưa đọc + chip phân hệ kèm số + Đánh dấu đã đọc theo phân hệ
- [x] BE: NotificationMeta::present/display/stripSender dùng chung cho API danh sách, user-profile (chuông web) và payload socket — cắt hồ sơ người gửi ở cả 3 nơi
- [x] Fix: web bấm "Đánh dấu tất cả đã đọc" ra trang 404 — gán read_at thẳng vào object trong Vuex (strict) → dựng danh sách mới rồi commit (BasicSubsystem::setNotificationsRead)
- [x] Loading B1: CommonProgressIndicator (BLoC + Riverpod dùng chung) → thẻ trắng bo góc, vòng xoay màu phân hệ (iOS Cupertino / Android Material), chờ 300ms mới hiện; PageLoadingBar 3px cho tải lại; BasePageState thêm showLoadingOverlay + buildLoadingBar; loading stream → BehaviorSubject
- [x] Loading B2: custom_view/skeleton.dart (Skeleton/SkeletonBox/SkeletonLine/SkeletonCard/NotificationSkeletonList) — áp Thông báo (+ báo lỗi trang đầu thay skeleton mãi), Cơm › Thông báo, Tổng quan Chấm công (state.dashLoaded), Tổng quan Đào tạo; OverviewHeaderBand summary null = vạch giữ chỗ
- [x] Loading B3: 1 kiểu cho mọi màn — bỏ hết CircularProgressIndicator tự đặt (Lịch cơm, Task, Phiếu giao việc/công tác, Khoá học cần tham gia, báo cáo tiến độ, chân danh sách tải thêm…): vùng → CommonProgressIndicator, nhỏ/trong nút → AppSpinner; hộp thoại "Đang tải file" + EasyLoading (showLoading) → AppLoadingCard. Còn lại 5 thanh/vòng có value = biểu đồ số liệu, giữ
- [x] Loading mẫu E toàn app: PrimaryAppBar vẽ thanh chạy (PageLoadingScope + GlobalLoading), 3 lớp nền bỏ lớp phủ vòng xoay, showLoading() bỏ EasyLoading; vùng/chân danh sách → skeleton; AppSpinner chỉ trong nút
- [x] Nút cao 44 cố định (kAppButtonHeight) — Primary/Secondary/DangerButton + 3 nút hành động dùng CommonButton h(48)/h(44)
- [ ] Test API nhiều tài khoản khác quyền

## Phase 8 — Meeting (thiết kế meeting-mobile.pen · xem design-meeting.md)

**Việc BE cần duyệt**
- [x] B1 (đã duyệt) `GET assign/meeting/mine?role=host|member` — danh sách meeting của tôi (MeetingCalendarCriteria + tách vai trò), tìm kiếm, 8 bộ lọc, phân trang, đếm 3 chip; dòng trả thêm số có mặt/tổng, có biên bản, chưa gửi lịch
- [x] B2 (chốt) Lưu: giai đoạn đầu dùng `POST assign/meeting/{id}` gửi cả form (không sửa BE); API lưu từng phần (app-meeting-mobile/api-luu-tung-phan.md) làm sau nếu cần
- [ ] B3 `customer-history` lọc sai người (đang so created_by) + trả thêm host_name, end_date
- [ ] B4 `getListEmployee` trả thêm company_code (mã công ty trên dòng nhân sự)
- [ ] B5 `GET assign/meeting/{id}` id không tồn tại trả 404 thay vì 500
- [x] B6 API Tổng quan Meeting (sắp diễn ra, cần xử lý gấp, lịch hôm nay, thống kê tháng)

**M1 — Khung phân hệ + tìm cuộc họp**
- [x] Khung Meeting: bottom menu (Tổng quan · Lịch · Tạo · Danh sách · Phòng họp), drawer 00d, mục Meeting trên màn chọn phân hệ (00b); mở thẳng tab Lịch, Tổng quan/Phòng họp tạm "đang hoàn thiện" (M5)
- [x] 01 Lịch meeting: 2 tab vai trò, 3 chip lọc nhanh (bấm lại để bỏ), tìm theo mã/tên (debounce 400ms), thẻ meeting, skeleton/lỗi/trống, tải thêm khi cuộn; tab Danh sách = API index web (phạm vi quyền), cùng thẻ
- [x] 02 Bộ lọc 8 tiêu chí (FilterView); KH / Dự án TKT tìm trên server (thêm tham số tuỳ chọn `asyncItems` cho SelectInput dùng chung); mở bằng `showFilterPanel` (route gốc) để không bị thanh menu khung phân hệ che nút

### Checkpoint — 22/10/2026 09:20
Vừa hoàn thành: merge origin/develop + origin/gop_db vào develop (hrm-api, hrm-client, 0 conflict, migrate local xong); M1 Meeting (API mine + khung phân hệ + 01 + 02), đã xem trên simulator
Đang làm dở: —
Bước tiếp theo: M2 — 03 Tạo meeting + Hub 04a/b/c + Thông tin chung + Nhân sự + chọn KH/liên hệ/dự án/hợp đồng
Blocked:

**M2 — Tạo + Hub + hồ sơ**
- [x] 03 Tạo meeting (3 khối gập/mở, gợi ý tên, Nội bộ ẩn khối Đối tác + đánh số lại ②), chủ trì mặc định người đăng nhập
- [x] 04a/b/c Hub theo trạng thái + thanh mức độ hoàn thiện + dấu * theo trạng thái; 24 Hub có lỗi; 26 Đã huỷ; 27 Chỉ xem
- [x] 05/25/28 Thông tin chung (lỗi validate, họp Online) + chế độ chỉ xem 33 (khối mở/gập được, chặn ô nhập)
- [x] 07/31 Nhân sự tham gia + 14/17/18 chọn nhân sự công ty / phía KH
- [ ] 41/41b/43/44 Chọn khách hàng, người liên hệ + thêm nhanh liên hệ; 48 Chọn dự án TKT; 49 Chọn hợp đồng
- [ ] 19 Tài liệu chuẩn bị (upload files/upload temporary)
- [x] 45 Cảnh báo chưa lưu khi Quay lại

**M3 — Chốt lịch, họp, biên bản, hoàn thành**
- [x] Lên lịch hẹn / chốt lịch; 23 Xác nhận đổi thời gian; 22 Menu ⋮; 16 Huỷ (lý do bắt buộc); Xoá nháp
- [x] 08 Điểm danh (3 mức + lý do)  · [x] xác nhận tham dự của khách mời nội bộ (khối trên Hub, dùng API attendance-confirm có sẵn)
- [x] 09/10/13 Biên bản: nội dung trao đổi (người đề xuất/thực hiện nhiều người + phía KH, hạn) + kết luận; 11 Tài liệu biên bản
- [x] 29/30/46 Chặn Hoàn thành (biên bản / điểm danh / thiếu khối) ; Hoàn thành
- [x] 15 Xem trước biên bản (mẫu in BIEN_BAN_CUOC_HOP của BE) — chưa có Tải PDF / Chia sẻ (cần thêm package)
- [x] Bộ màn chỉ xem 32/33/36/37/38 (34/39 đi cùng M4)

- [x] Validate theo quy tắc FE: app chỉ kiểm định dạng, bắt buộc/nghiệp vụ hiện lỗi BE theo ô/khối (Thông tin chung, Hub Lên lịch/Hoàn thành, Biên bản, Nội dung trao đổi, Nhân sự KH, Thêm liên hệ, Huỷ)
- [x] BE: Hoàn thành kiểm `reports` (≥1 nội dung) + `attendance` (điểm danh đủ) trong MeetingUpdateApiRequest, lỗi gắn trường
- [x] App: dio_exception_mapper giữ rootException để đọc lỗi theo trường từ body
- [x] 15 Tải PDF / Chia sẻ: BE `GET meeting/{id}/print-pdf` (dompdf, DejaVu Serif) + app share_plus; xem trước dựng khổ A4 thu nhỏ

### Checkpoint — 22/10/2026 11:35
Vừa hoàn thành: chuyển validate meeting app sang BE; Tải PDF / Chia sẻ biên bản
Đang làm dở: —
Bước tiếp theo: M4 — 06/06b Dự án TKT + phiếu, 12 Khảo sát, 21/42/20; test Tài liệu (upload) + luồng họp Đối tác
Blocked:

### Checkpoint — 22/10/2026 10:40
Vừa hoàn thành: M2 + M3 — Hub, Tạo meeting, Thông tin chung, Nhân sự/điểm danh, Tài liệu, Biên bản (09/10/13/29/37), Xem biên bản 15, Huỷ/Xoá; test trên simulator trọn vòng Nháp → Chốt lịch → Biên bản → Điểm danh → Hoàn thành, Huỷ, Xoá
Đang làm dở: —
Bước tiếp theo: M4 — 06/06b Dự án TKT + phiếu, 12 Khảo sát, 21/42/20; còn test Tài liệu (upload ảnh/tệp) và luồng họp Đối tác (chọn KH/liên hệ/dự án)
Blocked:

**M4 — Dự án TKT, khảo sát, khách hàng**
- [x] 06/06b/34 Dự án TKT + phiếu thu thập thông tin (mẫu động theo snapshot / mẫu gắn / Nhóm ngành+Ứng dụng, luật hiện câu như web, Lưu phiếu riêng) — câu kiểu tệp chỉ hiện số tệp (đính kèm trên web)
- [x] 12/39 Khảo sát nhu cầu KH (lĩnh vực → nhóm ngành, mức đầu tư `,` hàng nghìn, ngày)
- [x] 21 Lịch sử meeting khách hàng (BE: lọc theo người xem + host_name, status_color)  · [x] 42 Thêm nhanh KH (thêm MST + Người đại diện theo BE; 41b nút Thêm nhanh khi tìm không ra)  · [x] 20 Chọn địa điểm: dùng lại MapPage có sẵn

**M5 — Tổng quan & Phòng họp**
- [x] 00h/00h' Tổng quan Meeting — BE `GET assign/meeting/overview` (B6)
- [x] Tab Phòng họp: tình trạng phòng (status-board)  · Đặt phòng: để trên web (user chốt 22/10)

### Checkpoint — 22/10/2026 12:25
Vừa hoàn thành: lỗi lưu → snackbar tự ẩn (bỏ dải đỏ); M4 (06/06b, 12, 21, 20) + M5 (00h Tổng quan, tab Phòng họp); test trên simulator thứ 2 (iPhone 15)
Đang làm dở: —
Bước tiếp theo: (đã xử lý ở checkpoint 13:00)
Blocked:

### Checkpoint — 22/10/2026 13:00
Vừa hoàn thành: 42 Thêm nhanh KH; BE chặn Hoàn thành khi phiếu thu thập còn câu bắt buộc (MeetingProjectFormChecker, lỗi `projects.N.answers`); app tìm mẫu phiếu theo application_id
Đang làm dở: —
Bước tiếp theo: xác nhận tham dự của khách mời nội bộ (3.8 attendance self-confirm); test luồng họp Đối tác đầy đủ + upload tài liệu trên máy thật; rà nhiều tài khoản quyền khác nhau
Blocked:

- [x] Fix: cảnh báo "Thông tin chưa được lưu" báo nhầm ở Tạo meeting khi chưa sửa gì (sameAs coi khoá thiếu / null / chuỗi rỗng như nhau)

### Checkpoint — 22/10/2026 13:50
Vừa hoàn thành: khối "Xác nhận tham dự" trên Hub (Có mặt / Vắng có lý do / Sửa lý do; hết hạn thì hiện lý do khoá BE trả)
Đang làm dở: —
Bước tiếp theo: test luồng họp Đối tác đầy đủ + upload tài liệu trên máy thật; rà nhiều tài khoản quyền khác nhau
Blocked:

- [x] Ô Người chủ trì cùng nguồn web: BE `getListEmployee?scope=host` (cùng công ty, đang làm, có tài khoản, xếp theo tên); đổi chủ trì không gỡ người tạo khỏi thành phần
- [x] Fix tải tài liệu: PHP local giới hạn 2 MB bỏ file im lặng (BE trả 200 + []) → chạy PHP local với giới hạn như PROD; app báo lỗi khi BE trả thiếu đường dẫn
- [x] Mục tiêu / Nội dung + Kết luận soạn thảo giàu định dạng như CKEditor web (flutter_quill + chuyển HTML ↔ Quill, MeetingRichEditor)

- [x] Tài liệu: mỗi dòng Xem · Tải xuống · Xoá như thiết kế 11/19 (ảnh xem toàn màn trong app, tệp khác mở bằng trình xem của máy; Tải xuống = bảng chia sẻ); ảnh thu nhỏ; nhấn giữ để đổi tên; bỏ nút chọn màu ở ô soạn thảo
### Checkpoint — 22/10/2026 14:40
Vừa hoàn thành: chủ trì theo nguồn web, fix tải tài liệu, ô soạn thảo giàu định dạng (note + conclusion)
Đang làm dở: —
Bước tiếp theo: user thử trên simulator; chốt có ẩn khối Xác nhận tham dự với chủ trì / người tạo không
Blocked:

- [x] Header (PrimaryAppBar) gọn lại 22/10: thanh 48 cố định (trước h(56) ≈ 59pt), nút kính 36 bo 10 icon 20; nút viên trên header (chọn tháng Cơm, Đào tạo, Đọc tất cả) cao 36. MỌI màn dùng PrimaryAppBar tự có chuông thông báo (cả màn push như Đơn xin nghỉ), tắt bằng showNotificationBell: false ở màn thông báo / chi tiết thông báo. Lịch cơm: nút tháng rút "T10"
- [x] Màn danh sách: nút lọc chuyển từ header xuống hàng tìm kiếm + lọc dưới header (widget chung custom_view/list_filter_bar.dart, khuôn Danh sách meeting) — 29 màn + Meeting; ô từ khoá trong FilterView đưa ra ô tìm ngoài (debounce 400ms) ở ~20 màn; dao_tao (làm bài thi) không phải danh sách nên giữ
- [x] Tổng quan Meeting: link mở danh sách tab Tôi tham gia + đúng meeting đang đếm (BE overview trả meeting_ids, mine nhận ids / exclude_draft); tab Tôi tham gia gồm cả meeting chủ trì

### Checkpoint — 22/10/2026 14:55 (TẠM DỪNG Meeting — user chuyển sang phần Thông báo)
Vừa hoàn thành: chủ trì theo nguồn web, fix tải tài liệu, ô soạn thảo giàu định dạng, Xem/Tải xuống tài liệu; so sánh logic app ↔ web
Đang làm dở: —
Bước tiếp theo (khi quay lại): (1) tự thêm KH cá nhân vào thành phần phía KH (dòng cố định) như web; (2) đổi sang loại không có KH thì giữ dự án nếu loại gắn đối tượng / đã có dự án; (3) nút Thêm nhanh KH kiểm quyền `customers/my-permissions`; (4) chờ user chốt: thêm bước Lên lịch (1) như web? ẩn khối Xác nhận tham dự với chủ trì/người tạo?
Blocked: chờ user quyết 2 câu ở mục (4)

### Checkpoint — 23/10/2026 14:20
Vừa hoàn thành: logic Tạo/sửa meeting theo web — nháp 3 nút Lưu nháp · Lên lịch · Chốt lịch; Giải pháp / Hạng mục từng dự án TKT; Thêm nhanh KH theo quyền `my-permissions.create`; Hub lưu xong tải lại chi tiết (fix 400 projects.N.prospective_project_id khi lưu 2 lần liên tiếp); fix ô MST/SĐT bị bẹp ở Chọn khách hàng; fix badge trạng thái tràn ở Chọn dự án TKT (StatusBadge thêm ellipsis). Test simulator: meeting 66 (TPE.MET.KH.26.0079) lưu/bỏ chọn GP-HM, 0→1 đúng, Chốt lịch BE báo thiếu Địa điểm đúng luật
Đang làm dở: —
Bước tiếp theo: (1) KH cá nhân tự vào thành phần phía KH; (2) đổi loại giữ dự án; (3) chưa test tài khoản KHÔNG có quyền "Thêm khách hàng"
Blocked:

## Phase 7 — Bàn giao

- [ ] Chạy simulator từng phân hệ, nhiều tài khoản quyền khác nhau
- [ ] Đưa sang nhánh `tpe`

### Checkpoint — 20/10/2026 12:10
Vừa hoàn thành: Phase 2–6 (khung phân hệ, header + thân toàn bộ màn cũ, Tổng quan Chấm công 00i FE+BE, Thông báo 00j); analyze toàn app 0 error 0 warning; đã xem trên simulator tpeLocal
Đang làm dở: —
Bước tiếp theo: Phase 7 — test từng phân hệ với nhiều tài khoản khác quyền (cần tài khoản có ca hôm nay để xem thẻ ca 00i), chốt các điểm mở trong báo cáo, rồi đưa sang nhánh `tpe` (TPE_APP) — hrm-api sửa trên `develop`
Blocked:

### Dữ liệu test màn Tạo meeting (DB local, 23/10/2026)
- [x] Tài khoản (mật khẩu `Test@123`): `cannt.kd1@tanphat.com` (id 25, KHÔNG quyền "Thêm khách hàng") · `manhnv.kd1@tanphat.com` (id 30, CÓ quyền) · admin namdangit giữ nguyên
- [x] Loại meeting: 17 `[TEST] Họp đối tác theo dự án TKT` (KH + target 1) · 18 `[TEST] Họp đối tác theo hợp đồng` (KH + target 2) · 19 `[TEST] Họp nội bộ theo dự án TKT` (nội bộ + target 1) · 15 đang khoá (không hiện) · 1/2 thường
- [x] Dự án TKT gán 2 TK làm người hỗ trợ (support_departments id 94–97): 130 ĐH Quy Nhơn (1 GP + 2 HM) · 7 CĐ Việt–Hàn QN (2 GP, 0 HM) · 4 KH cá nhân MR TÂN 0906236723 (không GP) · 149 CYS (1 GP + 2 HM)
- [x] Hợp đồng: 9 `HD-TEST-0001` ĐH Quy Nhơn (Có hiệu lực → chọn được) · 8 `HD-TEST-0002` CĐ Việt–Hàn (Đang tạo → bị loại)
- [x] Test TK Cần: không có nút thêm nhanh KH (header + trạng thái rỗng) · chọn dự án 130 → GP → HM · Lưu nháp thiếu tên → BE 400 tô đỏ khối
- [x] Sửa: cache loại meeting giữ cả phiên → loại mới không hiện; form mở là tải lại, `MeetingTypeCache.find` không thấy thì tải lại 1 lần

### Chuẩn web áp cho app (23/10/2026)
- [x] Skill mới `TPE_APP/.claude/skills/app-ui-convention/SKILL.md` — đối chiếu button-convention / modal-popup / form-validate / unsaved-changes / list-page / select-and-input-state / notification sang widget Flutter; flutter-review trỏ sang
- [x] User chốt: màu nút theo bảng skill (Lưu nháp trắng, bước tiến cùng màu chính) · hộp thoại chung = khuôn meeting · phạm vi = Meeting + màn mới (màn cũ để nguyên)
- [x] Widget chung `custom_view/app_dialog.dart`: `AppDialog` · `showAppConfirm` · `showUnsavedChangesDialog` (thay MeetingDialog / showMeetingUnsavedDialog)
- [x] Meeting: Lên lịch → PrimaryButton, Lưu (trạng thái 1/2) → PrimaryButton; hỏi xác nhận Lên lịch / Chốt lịch (nêu mã + tên + hệ quả); Hoàn thành / Xóa dùng showAppConfirm
- [x] Meeting: chữ nút chuẩn (Hủy/Xóa/Khóa, "Không"→"Hủy", "Xong"/"Lưu nội dung"→"Xác nhận", "Thêm"/"Cập nhật"→"Lưu", "Lưu & chọn"→"Lưu và chọn", menu ⋮ "Sửa" / "Xóa", đổi giờ "Gửi lịch mới")
- [x] Meeting: bỏ chữ "Đang lưu…", lớp tải GlobalLoading ở `_saver` của Hub + `save` lúc tạo + 3 màn tự gọi API
- [ ] Màn cũ: ~40 file tự dựng AlertDialog/CupertinoAlertDialog, chữ Huỷ/Đồng ý/Chỉnh sửa/Không duyệt, 2 chỗ NumberFormat locale vi — sửa khi đụng tới màn
- [x] Bỏ dải "Chế độ chỉ xem" (người chỉ tham dự) ở Hub / Nhân sự / Biên bản / Khảo sát; dải hạn biên bản chỉ cho người sửa được (23/10/2026, chưa build)
- [x] Đổi phân hệ: nút "Đổi" trong drawer mở bảng "Chuyển phân hệ" tại chỗ, chọn là sang thẳng (pushAndPopUntil, không lộ màn chọn phân hệ); danh sách phân hệ dùng chung custom_view/module_switcher.dart với UserRoleMenu (23/10/2026, chưa build)

### Test kỹ luồng Meeting app ↔ web (23/10/2026, local, 3 TK admin / Mạnh / Cần)
- [x] Đã chạy: tạo (TKT đối tác, hợp đồng, nội bộ TKT), thêm nhanh người liên hệ, GP/HM, lưu nháp lỗi BE, nhân sự + cảnh báo chưa lưu, Lên lịch, xác nhận tham dự (có mặt / vắng có lý do), Chốt lịch (thiếu địa điểm → sửa → chốt), điểm danh, biên bản + kết luận, Hoàn thành (bị chặn → thành công), Hủy có lý do, Xóa nháp, tài liệu chuẩn bị (tải / xem / lưu), quyền thành viên chỉ xem + chủ trì không phải người tạo, thông báo + deep-link; đối chiếu web meeting 69
- [x] Sửa: báo ẩn lỗi khi gõ (Thêm nhanh người liên hệ) · bỏ gợi ý ở chọn chủ trì · "Công ty: n · Khách hàng: n" · lỗi BE mang vào màn con + tự mở khối lỗi · Địa điểm Enter không xuống dòng · khối đỏ không xoá sau lưu (hồi quy của lần đổi "tải lại chi tiết") · ẩn Hoàn thành khi can_complete=false + dòng lý do (BottomActionBar.note) · chữ Hủy/Sửa/Xóa/Đóng · nội dung biên bản trống làm app văng lỗi · lỗi dòng biên bản ghi rõ trường · chip hạn chỉ đỏ khi quá hạn · bỏ "· -" SĐT ẩn · bấm thông báo / push meeting mở meeting (trước báo "xem trên web") · họp Nội bộ theo dự án TKT không chọn được dự án · cuộn tới khối lỗi đầu
- [ ] Chưa làm (cần user quyết): G1 nút "Giao" việc từ dòng biên bản · G2 tab Nhiệm vụ · G3 "Tạo phiếu công tác khác" · G4 nút Có mặt/Vắng ngay trên dòng thông báo · "Hủy bỏ" của thư viện chọn giờ (13 màn)
- [ ] Chưa test: Họp tìm hiểu & giới thiệu SP (khảo sát + phiếu thu thập theo dự án), đổi giờ sau khi chốt, KH cá nhân, tài liệu biên bản, auto-hủy quá hạn biên bản
- Dữ liệu test để lại: meeting 69 (hoàn thành), 70 (hủy), 71 (chốt lịch, nội bộ TKT); người liên hệ "Tran Van E2E" của KH 27125; admin thêm làm người hỗ trợ dự án 7, 130
- [x] Tình trạng phòng họp (24/10/2026): thêm 9 phòng [TEST] + 11 phiếu đặt (đang họp / sắp họp / trống / chờ duyệt / từ chối / đã hủy / họp xong / qua đêm / phòng khóa / phòng CN Hải Phòng riêng + dùng chéo); sửa giờ lệch 7 tiếng (ISO +07:00 không toLocal) + "Trống đến hết ngày"; web: chip đếm ở chế độ Ngày tính sai phiếu chờ duyệt + phiếu qua đêm
- [x] Phòng họp 3 trạng thái như thẻ phòng web (user chốt 24/10/2026): tab chia Đang họp (đỏ "Đang họp đến …") · Sắp họp (cam "Sắp họp lúc …") · Trống (xanh "Không còn lịch nào"); khối Tổng quan giữ "trống ngay bây giờ" nhưng phòng sắp họp nhãn cam, thẻ nhỏ đưa sức chứa xuống dòng phụ (hết tràn)
- [x] "Thông báo nội bộ" chỉ còn ở drawer Chấm công (bỏ khỏi Công việc / Cơm / Đào tạo; menu trái cũ LeftMenuView thêm cờ showInternalNotice, chỉ Tổng quan chấm công bật) — 24/10/2026

- [x] Màn Đăng nhập theo UI mới: dùng chung nền màn chọn phân hệ (ảnh cover + phủ #0B254F 35%), lời chào, thẻ trắng bo 20 chứa logo flavor + form, phiên bản ở đáy (24/10/2026)
- [x] Ô mật khẩu PrimaryTextField mặc định che ký tự; version tpeLocal đồng bộ 2.2.6 (152) iOS + Android (24/10/2026)
- [x] Nền màn Đăng nhập + Chọn phân hệ: EntryBackground dùng đúng gradient navy + 4 vệt màu nhóm của web (layouts/system.vue); logo TPE đổi sang SVG vẽ lại từ JPG (tanphat_logo_2026_vector.svg) (24/10/2026)
- [x] Upload TestFlight Tân Phát ERP-HRM 2.2.6 (152) — Delivery 1eb93c70 (24/10/2026)
- [x] Bản đồ chọn địa điểm: chạm 1 điểm → cắm ghim + tự lấy tên địa chỉ (Goong / Nominatim reverse); sửa ghim Mapbox không bao giờ hiện (ảnh ic_map_marker.png không tồn tại → vẽ ghim bằng code); gợi ý "Chạm vào bản đồ để chọn vị trí" (24/10/2026)
- [x] Bản đồ: nút chuyển Bản đồ / Vệ tinh (Mapbox STANDARD ↔ STANDARD_SATELLITE, nhớ lựa chọn qua SharedPreferences, ẩn ở free mode OSM) (24/10/2026)
- [x] Rà & sửa màn cũ toàn app (4 agent: Chấm công / Công việc / Đào tạo / Cơm+chung) + review hồi quy; trả 3 chỗ về hành vi cũ; nút Đóng báo cáo tiến độ đi qua cảnh báo chưa lưu (24/10/2026)
- [x] Số hiển thị theo chuẩn quốc tế ở NumberFormatUtils (en_US) + unit test; 4 form đơn từ: "Lưu" → "Lưu nháp" (đã xác nhận lưu status 0 = Đang tạo), hỏi xác nhận trước gửi duyệt, cảnh báo thoát khi chưa lưu (FormDirtyMixin + UnsavedChangesGuard); bài thi: điền khuyết gửi đủ ô theo thứ tự ô, hỏi trước khi thoát bài đang làm (24/10/2026)
- [x] Thanh điều hướng dưới: nút giữa 66 → 54pt, icon 22, nhãn thẳng hàng các tab (24/10/2026)
- [x] Thanh điều hướng dưới: bỏ khoảng trống thừa (đệm đáy = vùng an toàn - 10, hàng tab 58) (24/10/2026)
- [x] Upload TestFlight Tân Phát ERP-HRM 2.2.6 (153) — Delivery 24e2f530 (24/10/2026)
- [x] Header Tổng quan theo design: lớp trang trí ModuleHeaderDecor (vệt sáng + vòng cung + icon phân hệ cỡ lớn mờ: vân tay / mũ tốt nghiệp) ghép liền header flat + OverviewHeaderBand (26/10/2026)
- [x] Sửa đường nối header ↔ dải lời chào: lớp trang trí lấy status bar thật (View) thay MediaQuery (Scaffold body đã trừ top) (26/10/2026)
- [x] Tổng quan Meeting: header flat + lớp trang trí (icon lịch) ghép liền dải lời chào như Chấm công / Đào tạo (26/10/2026)
- [x] Thẻ "Sắp diễn ra" (Tổng quan Meeting) theo design: nhãn có chấm + giờ bắt đầu cam, tên đậm, dòng thông tin có icon, đường kẻ, nút "Vào cuộc họp →"; lớp tối đáy dải kéo hết chiều cao dải. Avatar người tham dự chờ duyệt BE bổ sung tên (26/10/2026)
- [x] Tăng tốc dashboard Chấm công: BE dashboad/hcns nạp sẵn quan hệ (2623 → 72 câu SQL, web giữ nguyên phản hồi từng byte), lọc ngày dùng index, tham số compact=1 cho app (472KB → 81KB); app gọi song song, chỉ gọi hcns khi có quyền Dashboad quản lý, bỏ gọi trùng user-profile (26/10/2026)
- [x] Meeting: nút ⋮ hiện khi có mục dùng được (người chỉ xem vẫn vào được "Xem / In biên bản"); thêm nút in trên màn Biên bản cuộc họp; bỏ dải "Meeting đã hoàn thành — chỉ xem" ở Chi tiết + 4 màn con (26/10/2026)
- [x] Xem trước biên bản: sửa viền bảng bị đôi (HtmlWidget không gộp border-collapse) — ô vẽ cạnh phải+dưới, bảng vẽ trên+trái, border-spacing 0 (26/10/2026)
- [x] Đổi "Xem / In biên bản" → "Xem biên bản" (menu ⋮, icon màn Biên bản, tiêu đề popup, nút Xem, "Chỉ hiện người có mặt") — điện thoại không in

### Theo design meeting-mobile_v2.pen (26/10/2026)
- [x] Menu trái: đầu drawer gradient + vệt sáng + 2 vòng + icon chìm theo từng phân hệ; mục 46/ô icon 32; CTA 46; chân có viền + bóng; mờ cuối danh sách; sửa viên số bị kéo cao
- [x] Thông tin chung: khối ①②③ (màu/viền/đầu khối/✓ viền/"Chưa nhập"/"n lỗi"), dòng chọn phẳng, segmented iOS, chip Gợi ý tên, thẻ thông tin KH + nút Lịch sử meeting, tóm tắt "T2 14/09 · 08:30 – 10:00"
- [x] Thông tin chung chế độ xem (33): nhãn–giá trị + khối Thông tin bản ghi
- [x] Lịch meeting (01): tab ôm chữ, 3 ô số có chấm, thẻ meeting (tên thường 13, tag viền)
- [x] Hub (04a/b/c): Hero/Mức độ hoàn thiện/danh sách khối tràn viền, màu ô icon theo trạng thái, bảng Hành động (22), hộp đổi thời gian (23), hộp Hủy (16)
- [x] Nhân sự (07/08/32): thẻ nhóm đầu xám + Thêm nhanh, dải điểm danh + Tất cả có mặt, nút gạt điểm danh, chip kết quả khi xem
- [x] Biên bản (09/10/13/37): dải tóm tắt, thẻ nội dung, chip hạn theo màu, Thêm nội dung viền xám, Kết luận nhãn ngoài thẻ, "Chốt bởi"
- [x] Tài liệu (11/19), Khảo sát (12), Chọn nhân sự (14), Chọn khách hàng (41: ô MST/SĐT hiện sẵn, nút Thêm nhanh KH)
- [x] Tổng quan Meeting (00h/00h') + tiêu đề "Meeting"; Tổng quan Chấm công tiêu đề "Chấm công"
- [x] AppDialog dùng chung + hộp "chưa lưu" (45)
- [x] (agent) Tổng quan Chấm công v2 — Ca làm trong ngày dạng dải thời gian
- [x] (agent) Thanh lọc dùng chung BL1/BL4 + bảng lọc BL2/BL3 + màn Phiếu giao việc
- [ ] Còn rà: 06/06b/34 Dự án TKT, 20 bản đồ, 21 lịch sử KH, 42/43/44/48/49, 00b, 00j, trạng thái Hub 24/26/27/29/30/46, 02 bộ lọc meeting

### Sửa bảng lọc Phiếu giao việc (26/10/2026 chiều)
- [x] App: trang con Phạm vi tràn dưới tai thỏ + nút ‹ không ăn (lấy vùng an toàn từ màn gọi, PopScope về bảng chính)
- [x] App: ô tìm lệch chữ (ListFilterBar + trang con) — dựng lại hàng icon · ô collapsed · ✕
- [x] App: chọn 1 = không ô tick, bấm là chọn + quay lại, không footer
- [x] App: Phạm vi theo quyền + lọc tầng Công ty → Phòng ban → Bộ phận; Người thực hiện theo phòng ban
- [x] App: tiêu chí theo cột web (Khách hàng, Nội dung công việc, Người đề nghị/duyệt/cập nhật, Ngày tạo/cập nhật)
- [x] (agent) BE: GET timesheet/job-assignment/filter-options + tham số lọc mới (web jobassignment giữ UI cũ theo user, đã trả file)
- [x] App: dòng chọn đã có giá trị có nút ✕ xoá nhanh tại bảng lọc
- [x] App: rút bảng lọc Phiếu giao việc về đúng bộ lọc web (Phạm vi/phòng ban, Trạng thái, Người thực hiện, Thời gian bắt đầu, Ngày tạo)

### Bảng lọc mới cho mọi màn danh sách app (26/10/2026)
- [x] (agent) Chấm công: lịch sử chấm công, đi muộn về sớm, làm thêm, tra soát công, đơn xin nghỉ, yêu cầu điểm danh
- [x] (agent) Công tác/phiếu: gia hạn/kết thúc công tác, phiếu công tác, kết thúc sớm, phiếu giao công tác, nhập kết quả, thanh toán, Task
- [x] (agent) Đào tạo: bài thi/kết quả thi, đăng ký khoá học, khoá học, thông báo khoá học, khoá học cần/đang/đã tham gia
- [x] (agent) Đánh giá + Cơm: kỳ đánh giá cần/đã tham gia, lịch thi, lịch thi của bạn, thông báo kỳ đánh giá, thông báo cơm, cơm dài hạn
- [x] (agent) Lịch meeting (thay ngăn kéo design 02)
- [x] Kiểm runtime mẫu: Danh sách meeting, Đơn xin nghỉ, Task, Phiếu công tác, Danh sách khoá học
- [x] Sửa lỗi static-data trả `permissions` dạng object làm rỗng Trạng thái/Loại phép (ApiUserProfileData.fromJson)
- [x] filter_sheet: trường 1 ngày (single), searchWith(draft), keyboardType; mapper đọc meta.total
- [x] (agent) BE my-job/task-list lọc Hạn hoàn thành + Tag; app Task thêm lại 2 tiêu chí (user chốt 26/10)
- [x] (agent) Trạng thái Danh sách khoá học: sửa chỗ hợp lý (BE/web) + thêm vào app; đổi chữ "Chưa tham gia" → "Tham gia" như web
- Không làm: lọc phạm vi/người tạo cho Lịch meeting của tôi; Nhóm nghiệp vụ Thành An để nguyên
- [x] MeetingSegmented: nền trắng trượt + chữ không đổi độ đậm; MeetingSection/khối Đối tác co giãn mượt khi đổi Đối tác ↔ Nội bộ
- [x] Bảng lọc: dòng chọn có nhãn dài → giá trị xuống dòng 2 (không bị cắt); màn chọn phân hệ làm mới hồ sơ (menu trái đủ Phòng ban · Mã NV)
- [x] Thẻ phòng họp: số chỗ dồn sát phải (bỏ Flexible+Spacer chia đôi)
- [x] Nút dùng chung tự quay khi chờ API (chỉ khi màn ở trên cùng — không quay lúc hộp xác nhận đang mở); câu lỗi tải PDF đọc đúng lỗi BE
- [x] (agent) Chọn khách hàng dùng chung UI picker Meeting (CustomerPickerPage) — thay hộp thoại chon_diem_di ở Tạo phiếu giao việc (chỗ chọn khách duy nhất ngoài Meeting)
- [x] Bảng lọc: ô nhập tiêu chí (FilterTextField) nền trắng + viền, focus viền màu phân hệ (ô tìm giữ nền xám)

### Header theo bộ màu design + nền header Thông báo (28/10/2026) — @cuong61n
- [x] (28/10) Header mọi màn trong phân hệ dùng đúng gradient 3 màu của design (meeting-mobile_v2.pen) thay cho màu tự pha: Chấm công #2763B5→#17457F→#0B254F, Meeting, Công việc, Đào tạo, Cơm; kèm vệt sáng + vòng cung + icon phân hệ chìm (vân tay…) ở MỌI màn, Tổng quan ghép liền header + dải lời chào. Kiểm trên simulator 3 màn Chấm công (Tổng quan, Lịch sử, Bảng công). Đã push develop `771bbbe`.
- [x] (28/10) Header màn Thông báo: nền navy + vệt sáng + chuông nét viền chìm. Đã push cùng `771bbbe`.

### Mytodo app — rà design mytodo.pen + biên bản review 16/09 (28/10/2026) — @cuong61n
- [x] (28/10) Đọc 15 màn design mytodo.pen + biên bản "REVIEW APP – MYTODO 16/09/2026": design chưa áp góp ý nào; tổng hợp đề xuất cho user.
- [x] (28/10) Ghi ý kiến DNS vào cột "Nội dung thống nhất" (15 dòng + tiêu đề cột) trên Google Doc họp, đối chiếu web hrm-client /assign/my-todo + skill; sự cố ghi lẫn 6 ô "Nội dung đề xuất" đã gỡ, kiểm bằng bản xuất HTML: cột đề xuất 20/20 dòng y nguyên.
- [x] (28/10) Sửa theo user: giữ nút refresh (xoá điều kiện lọc) ở A1/A3/B1; A3 đổi thành khuôn rỗng chung mọi màn danh sách.
- [x] (28/10) Tạo dữ liệu thử nhắc việc cá nhân cho namdangit (id 13) trên DB local_hrm_erp (cổng 3002): 7 việc [TEST] đủ nhóm Hôm nay/Ngày mai/Tuần này/Quá hạn/Không hạn, 2 việc có bước con; hướng dẫn user chỗ tick xác nhận, tạo nhắc việc, tạo meeting từ tab Lịch.

### Đồng bộ thứ tự nút hộp thoại app với web (28/10/2026) — @cuong61n
- [x] (28/10) Hộp thoại app: nút hành động trước, Hủy/Đóng cuối (như web): showAppConfirm, ReasonInputDialog + 13 hộp thoại tự dựng (meeting, duyệt phiếu công tác, gia hạn, điểm danh…); sửa skill app-ui-convention mục 1c. Analyze sạch (173 info). Chưa commit.
- [ ] Thanh nút đáy (57 chỗ) còn khác web — chờ user chốt.

### Khuôn rỗng chung mọi màn danh sách app (29/10/2026) — @cuong61n
- [x] (29/10) AppEmptyWidget thêm cờ `filtered`: không lọc → "Không có dữ liệu.", đang lọc/tìm mà không ra → "Không có dữ liệu phù hợp."; không còn nút "Xóa bộ lọc"/"Tải lại" ở màn rỗng (xoá lọc dùng nút trên thanh lọc, tải lại = kéo xuống). Theo chốt ô A3 biên bản review Mytodo.
- [x] (29/10) Bỏ câu/icon/dòng phụ tự đặt ở 39 màn danh sách: 30 màn có thanh lọc (Chấm công, Công tác/phiếu, Đào tạo, Đánh giá, Cơm, Lịch meeting, Task, Thông báo, Phiếu yêu cầu…) truyền `filtered`; 11 màn không lọc (bảng công, bảng lương, thiết bị, trưởng nhóm, lịch học/lịch thi…) về câu mặc định. Lịch sử chấm công bỏ ảnh + 2 dòng chữ riêng. Task: bỏ nút "Tải lại", màn rỗng kéo xuống được. Giữ câu riêng cho lỗi tải / không tìm thấy bản ghi / trạng thái đăng ký.
- [x] (29/10) Ghi quy tắc vào skill app-ui-convention mục 4 + "Quyết định đã chốt".
- [x] (29/10) Kiểm: analyze 0 error/warning (173 info như cũ); simulator Lịch sử chấm công gõ từ khoá không khớp → "Không có dữ liệu phù hợp." + "0 / 22 lượt". Chưa commit TPE_APP.

### Sửa file design mytodo.pen theo biên bản review 16/09 + Nội dung thống nhất (29/10/2026) — @cuong61n
- [x] (29/10) Chuẩn chung: đổi bộ màu file sang phân hệ Công việc (accent #1E8A63, nền #F2F4F7, chữ slate); header gradient #23A06F→#136B4C→#083A2A + vệt sáng + vòng cung + icon chìm task_alt cho MỌI màn (C/HeaderList có tab Công việc của tôi/Lịch làm việc, C/HeaderDetail); thanh dưới phân hệ Công việc: Việc của tôi · Tasks · [Tạo mới] · Phiếu · Phê duyệt; bỏ nút + cam từng màn; nút chính gradient xanh, ô nhập bo 12; nhãn "Chờ duyệt" về màu chuẩn #D97706; bỏ 3 component cũ (StatusBar navy, TopTabs, Header trắng).
- [x] (29/10) A1/A2: Quá hạn lên đầu; tên loại theo web (Nhiệm vụ, Vấn đề, Phiếu giao công tác…) + 2 loại chấm công; thẻ Meeting có Xác nhận tham gia; Nhiệm vụ/Vấn đề nhãn vai trò + trạng thái thật; Nhắc việc bỏ 2 nhãn, tick bước ngay trên thẻ; giữ nút ↻.
- [x] (29/10) A3 khuôn rỗng chung "Không có dữ liệu phù hợp.", bỏ nút Xoá bộ lọc; A4 popup xác nhận hoàn thành (Hoàn thành trước, Hủy cuối).
- [x] (29/10) B1–B4: chấm ngày tối đa 2 + "+"; bảng lọc lịch đủ loại, "Làm mới", Áp dụng xanh.
- [x] (29/10) C1–C6: bỏ dải chỉ xem/banner vàng; C2 thêm Meeting liên quan; C3 thêm Hạn hoàn thành + công khoán; C4 "Chi tiết nhiệm vụ", bỏ ô trùng, thêm người giao/duyệt + liên kết, checklist ✓/chấm, tệp 2 nhóm + xem/tải/chia sẻ; C5 gộp dòng đầu, Mô tả lên trên, nút Sửa; C6 "Chi tiết vấn đề", hạn đỏ ⚠, chưa phân công màu cam.
- [x] (29/10) D1 nút giữa mở sheet Tạo mới (Nhắc việc cá nhân · Meeting · Giao việc); thêm D2 màn Tạo/Sửa nhắc việc cá nhân (đủ trường form web). Cập nhật chú thích, ghi chú tư vấn, dàn lại vị trí các nhóm. Kiểm bằng ảnh xuất từng màn.
- [x] (29/10) Bổ sung chi tiết: A1 đủ 7 nhóm như web (thêm Tuần sau · Sau đó · Không hạn); thẻ nhắc việc có "Xem bước / Thu gọn"; pill đang lọc có ✕; A3c "Không có dữ liệu."; A4b sheet Sửa bước (Lưu · Xóa bước), A4c xác nhận xoá bước (Xóa · Hủy); B1 thẻ meeting "Đã xác nhận tham gia"; D2c hộp "Thông tin chưa được lưu"; nới khung + dàn lại vị trí.
- [ ] Chờ user chốt: thứ tự thanh nút đáy app (Hủy/Lưu) so với web.

### Code Mytodo trên app — tab "Việc của tôi" phân hệ Công việc (29/10/2026) — @cuong61n
Theo design mytodo.pen (đã sửa 29/10) + Nội dung thống nhất biên bản review 16/09. API có sẵn: GET v1/assign/my-todo, /calendar, CRUD /todos, PATCH /todos/{id}/toggle.
- [x] (29/10) BE hrm-api develop: GET my-todo trả `attendance_confirm` (can_confirm, my_status…) cho meeting, nạp sẵn điểm danh của user 1 query (preloadMyCompanyMember) — kiểm curl: 6 meeting đều có trường. Chưa commit.
- [x] (29/10) Web hrm-client develop: nhóm Quá hạn lên đầu (TodoMainList groupOrder). Chưa commit.
- [x] (29/10) App data: MyTodoApiService (my-todo, calendar, lists, CRUD/toggle todo) + model WorkItem/WorkSubItem/TodoListOption. Bẫy: API trả MẢNG ở `data` phải dùng mapper jsonObject + đọc json['data'] (dataResponse chỉ nhận object → ra 0 dòng).
- [x] (29/10) Khung phân hệ Công việc: tab đầu "Việc của tôi"; "Tiến độ" chuyển vào menu trái (mở màn riêng); nút giữa "Tạo mới" → sheet Nhắc việc cá nhân · Meeting · Giao việc.
- [x] (29/10) Tab Công việc của tôi (my_todo_list_view.dart): tìm + ↻ xoá lọc, 2 pill Loại/Trạng thái (✕ bỏ điều kiện, tự xuống dòng), 7 nhóm Quá hạn đầu, chỉ Hôm nay mở; thẻ WorkItemCard dùng chung; khuôn rỗng chung.
- [x] (29/10) Tab Lịch (my_todo_calendar_view.dart): Tuần/Tháng, chấm tối đa 2 + "+", agenda theo ngày (việc nhiều ngày ghi "ngày 2/3"), Bộ lọc loại + nhóm trạng thái, ↻.
- [x] (29/10) Chi tiết nhắc việc (PersonalTodoDetailPage, C5) + form Tạo/Sửa (PersonalTodoFormPage, D2, cảnh báo chưa lưu, lỗi BE tô đỏ đúng ô, sửa thì ẩn lỗi); sheet sửa/thêm/xoá bước; bấm thẻ loại khác mở màn có sẵn (Meeting Hub, Task, phiếu giao việc, phiếu giao công tác; Vấn đề chưa có màn app → báo xem trên web). Bảng lọc chung đổi "Đặt lại" → "Làm mới".
- [x] (29/10) Kiểm: analyze 0 error/warning (173 info như cũ); simulator: danh sách 30 việc + nhóm; lọc Loại; tick hoàn thành (popup Hoàn thành/Hủy, DB is_completed=1); tick bước cuối → việc cha tự Hoàn thành; tạo nhắc việc + bước (DB id 28/29), bấm Lưu khi trống → ô Tiêu đề đỏ "Tiêu đề là bắt buộc"; sửa bước (DB id 6, 7); form Sửa điền sẵn. Sửa lỗi màn đỏ `_dependents.isEmpty` (controller ô sửa bước huỷ khi sheet còn trượt → tách _StepSheet).
- [x] (29/10) Thêm 2 loại phiếu phân hệ Chấm công vào "Việc của tôi" (chốt A2 — user bảo làm luôn, không chờ):
  - BE hrm-api: `Modules/Assign/Services/MyTodo/TimesheetWorkItems.php` — `ts_job` = Phiếu giao việc (chấm công) (job_assignment_notes, ngày = MIN/MAX details.intend_*), `ts_business` = Phiếu đi công tác (chấm công) (business_trip_assigns, from/to_time). Của tôi = có tên trong nhân viên thực hiện; Chưa xong = Đã duyệt + chưa nhập kết quả, kết thúc trong 30 ngày gần đây trở đi; Đã xong = đã nhập kết quả; Lịch = mọi trạng thái trừ Đang tạo. Nối vào MyTodoService::getAll + WorkCalendarService + validate types[]. Migration index (employee_id, …) cho job_assignment_employees / business_trip_employees, đã chạy local.
  - Kiểm curl với 4 phiếu [TEST] cho namdangit (job 29275 chưa KQ, 29276 đã KQ, business 10396/10397): pending 3, done 1, all 4, calendar 4 đúng nhóm trạng thái; my-todo ~0,31s.
  - Web hrm-client: work-item-types.js thêm 2 loại (nhãn/màu/icon + trạng thái lọc lịch), TodoFilterBar thêm 2 lựa chọn, bấm thẻ → $router.push(url) màn xem có sẵn (/timesheet/self-jobassignment/{id}, /timesheet/business_trip_assigns/add/{id}?view=true). Chưa mở thử trên trình duyệt (client develop chưa chạy).
  - App: WorkType thêm 2 loại (tên/màu khớp web), bấm → PhieuGiaoViecDetailRoute / PhieuCongTacDetailRoute. Simulator: thẻ hiện đúng nhóm Hôm nay, lịch tháng chấm tím 30–31/10, thẻ "ngày 1/3 · 30/10 → 01/11", mở đúng 2 màn chi tiết.
- [x] (29/10) Tab Công việc của tôi: bỏ nút ↻ và 2 pill riêng, chuyển sang thanh lọc chung ListFilterBar + showFilterSheet như mọi màn danh sách (Loại việc chọn 1 · Trạng thái chọn 1, trống = Chưa xong); tiêu chí đang bật hiện chip ✕ + badge số trên nút lọc. Kiểm simulator: chọn Meeting + Tất cả → chip + badge 2, danh sách lọc đúng.
- [x] (29/10) Bỏ hàng chip lọc nhanh (quickChips) ở 17 màn danh sách (Phiếu giao việc, Phiếu công tác, Phiếu giao công tác, Nhập kết quả, Thanh toán, Đơn xin nghỉ, Đi muộn về sớm, Làm thêm, Tra soát công, Gia hạn/kết thúc công tác, Yêu cầu điểm danh, Lịch thi, Lịch thi của bạn, Kết quả thi, Bài thi, Kỳ đánh giá cần tham gia, Đăng ký khóa học) — chip chỉ chọn Trạng thái, Trạng thái đã có trong bảng lọc nên không mất điều kiện. Ghi quy tắc vào skill app-ui-convention.
  - Sự cố: chạy `dart format` (Dart 3.11) lên 54 file đang sửa → diff phình ~10.000 dòng do đổi kiểu thụt dòng. Gỡ bằng script so token (bỏ khoảng trắng + dấu phẩy cuối), ghép đúng phần sửa thật vào bản HEAD; kiểm chứng từng file: format(bản gỡ) == bản đã format → 54/54 đạt. Diff về 91+/280−. Analyze 173 info như cũ; simulator màn Phiếu giao việc không còn hàng chip.
- [ ] Chưa kiểm được nút "Xác nhận tham gia" trên thẻ meeting (dữ liệu local không có meeting sắp diễn ra mà user chưa xác nhận). Chưa commit TPE_APP / hrm-api / hrm-client.
