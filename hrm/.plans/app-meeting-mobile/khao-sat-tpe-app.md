# Khảo sát app thật TPE_APP (19/10/2026)

Nguồn: đọc mã `TPE_APP/app/lib` (nhánh `develop`) + chạy flavor `erp` trên máy ảo iPhone 18 Pro (bản 2.2.4).
Mục đích: user muốn sắp xếp lại một số màn của app hiện tại.

## Kết luận chính
- App **CHƯA có Meeting / Lịch họp / MyTodo** — `meeting-mobile.pen`, `mytodo.pen` là thiết kế màn MỚI.
- "Công việc" hiện có: **Task** (danh sách + chi tiết + bình luận, CHỈ XEM — không tạo/sửa trên mobile), **Báo cáo tiến độ task**, **Phiếu giao việc / Phiếu công tác**.
- 93 màn `@RoutePage`, khai phẳng ở `lib/navigation/routes/app_router.dart:66-166` (auto_route 11, không nested/tab router, không guard).
- Không có deep link thật (`my_app.dart:79` bỏ qua link) — chỉ vào thẳng màn qua push notification (`app_bloc.dart:164-244`).

## Điều hướng (nhóm TPE)
Đăng nhập → **Chọn phân hệ** (`user_role_menu_page.dart`): Chấm công & Giao việc · Đào tạo & Năng lực · Quản lý cơm (ẩn với Kasaco); 8 ô khác đang comment (Tính lương, HCNS, Quản lý công việc…).

**Tổng quan Chấm công** (`dashboard_nhan_vien_page.dart`, class `TongQuanChamCongPage`):
- Body: Ca làm việc → Tạo phiếu (Xin nghỉ · Giao việc · Tra soát công; Công tác chỉ Thành An) → Báo cáo tổng quan → biểu đồ → Danh sách nhân sự (quyền "Dashboad quản lý").
- Bottom bar KHÔNG phải tab (currentIndex -1), chỉ là phím tắt push (dòng 767-813): Chấm công · Lịch sử · Bảng công · Công tác · Giao việc.
- Drawer (dòng 136-274): [Thông báo nội bộ — nhóm TPE] · Công việc của tôi (Tasks) · Chấm công · Quản lý đơn · Phê duyệt (theo quyền PD-*) · Giao việc/Công tác · Bảng công tổng hợp · Bảng lương · Cài đặt · nút Chọn phân hệ.

**Đào tạo & Năng lực** (`menu_khoa_hoc_page.dart`): drawer 5 mục; body Lộ trình · Khoá học (5 ô) · Năng lực (4 ô KHÔNG bấm được; "Kết quả thi" onTap bị comment); bottom bar 4 nút.
**Quản lý cơm** (`quan_ly_dk_com/normal_page.dart`): lịch cơm theo tháng; drawer Thông báo · Đăng ký ăn dài ngày · Cài đặt.

## Điểm cần biết khi sắp xếp lại
- Đổi thứ tự / ẩn hiện phải sửa **3 nơi**: drawer + bottom bar (`dashboard_nhan_vien_page.dart`), ô phân hệ (`user_role_menu_page.dart:58-136`) + bản sao trong bottom sheet `left_menu.dart:215-260`.
- 7 route không có đường vào: SearchFilter, ChonNv, GiaHanKetThucCongTac, KhungNangLuc, XemLichHoc, XemLichThi (TaskDetail mở bằng `pushWidget`, không qua route).
- Cờ flavor (`build_config.dart:31-56`): `isTPEGroup` (erp, production, staging, tanphat, wetek, zitec, ori, kasaco, toyotasonglam) · `isThanhAnGroup` · `isDLSGroup` · `isWhatTheFuckToDoThis` (erp, production, staging, zitec, ori, kasaco, toyotasonglam — bật Phiếu giao công tác / Quản lý phiếu giao việc / Phiếu nhập kết quả).
- Flavor: `erp` = bản dev TPE ("Tân Phát ERP-HRM", API dev-hrm.eteksofts.com) · `production` = live "HRM TPE" · `tanphat` thực ra là ETEK POWER.

## Danh sách màn theo nhóm (tóm tắt)
- Khởi động/chung: Login, ChangePassword, UserRoleMenu, TongQuanChamCong, Setting, SaveThietBi, DangKyThietBi, Map, Notification, NewNotification (Thành An), SelfNotification, InternalNotification(+Detail), SearchFilter*, DsTruongNhom, ChonNv*.
- Chấm công: CheckInOut(+Success), CheckInHistory, BangCong, DanhSachBangCong, BangCongDetail, DanhSachBangLuong, BangLuongDetail.
- Đơn/Phê duyệt (1 màn dùng chung `isApprove`): đơn xin nghỉ, đi muộn về sớm, làm thêm, tra soát công (danh sách + form mỗi loại).
- Giao việc/Công tác: phiếu giao việc (DS, tạo, chi tiết), phiếu công tác (DS, tạo, chi tiết, duyệt giao), gia hạn/kết thúc sớm, phiếu giao công tác, quản lý phiếu giao việc, nhập kết quả công việc (tab dịch vụ), phiếu thanh toán CTP (Thành An).
- Task: TaskList (chip Tôi làm / Tôi giao / Tôi theo dõi / Tôi duyệt + bộ lọc), TaskDetail (chỉ đọc), TaskComments, BaoCaoTienDoTask.
- Đào tạo: MyCourse, khoá học (DS, chi tiết 4 tab, đăng ký, cần/đã/đang tham gia), lịch học/thi, kết quả thi, làm bài (DaoTao), thông báo khoá học, điểm danh, kỳ đánh giá năng lực (5 màn).
- Cơm: QuanLyDkCom, thông báo cơm (+chi tiết), ăn dài ngày (DS, thêm, chi tiết), cài đặt cơm.
(* = không có đường vào)

## Chạy để khảo sát
`cd TPE_APP/app && fvm flutter run --debug -t lib/main.dart --flavor erp --dart-define=FLAVOR=erp -d D0C0E274-8590-4D39-9196-CD5D535338DD`
(Podfile dòng Mapbox đã comment sẵn.) Chỉ xem, KHÔNG lưu/gửi phiếu — flavor erp ghi vào server dev.
