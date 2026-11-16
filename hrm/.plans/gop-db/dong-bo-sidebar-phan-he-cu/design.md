# Đồng bộ sidebar 4 phân hệ cũ về chuẩn hub — @khoipv

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-11-16-dong-bo-sidebar-phan-he-cu-design.md`
Trạng thái: CODE XONG + ĐÃ PUSH develop hrm-client `e876d0237` (16/11/2026). hrm-api không đổi.

## Mục tiêu
4 phân hệ cũ **Thông tin nhân sự (`human`), Chấm công (`timesheet`), Quản lý cơm (`rice`), Tính lương (`payroll`)**
dùng menu ngang trên topbar (`layouts/default.vue`) — lệch với ~22 phân hệ mới dùng sidebar hub (kiểu MISA: rail icon,
mặc định thu gọn, rê chuột bung, ☰ ghim). Đưa 4 phân hệ về cùng chuẩn để toàn hệ thống một kiểu menu.

## Scope (user chốt 16/11)
- Phase 1 — chỉ đổi KHUNG menu: giữ nguyên nhóm / mục / nhãn / quyền của menu cũ. Không gom nhóm, không đổi tên.
- Phase 2 — tên màn trên topbar (hướng "từng page", user chọn thay vì fallback chung) + BỎ cụm tiêu đề + breadcrumb
  trong màn (`<PageHeader>` / `page-title-box`), giống màn phân hệ mới.
- Kèm: fix lỗi có sẵn `mixins` khai 2 lần ở 2 báo cáo Cơm (user yêu cầu).

## Quyết định chính
- Thêm 4 key vào `HUB_SUBSYSTEMS`; menu 2 cấp → `deriveHubGroups()` tự suy, mục lẻ cấp 1 thành link trên rail.
  Không sửa hàm dùng chung nào của hub.
- Page dùng `layout: 'subsystem'` (nạp bộ scss topbar mà màn cũ dựa vào), KHÔNG dùng `default-sidebar`.
  `layouts/subsystem.vue` được bổ sung cơ chế thu gọn/ghim hub (bản sao `default-sidebar.vue` — sửa 1 bên phải đối chiếu bên kia).
- Thêm `icon` (Remix) cho mục cấp 1 của 4 menu.
- Bỏ sidebar con `SettingSlidebar` ở Cấu hình chấm công (mục đã có trong nhóm "Cấu hình").
- Tên màn: danh sách = nhãn menu; Thêm/Sửa/Chi tiết/Duyệt + `: <mã>` khi có mã; bảng lương/kỳ công không có mã → nối tên
  bảng (heading cũ chỉ hiện tên này); màn duyệt danh sách đặt "… chờ duyệt".
- KHÔNG sửa `components/Page-header.vue` (dùng chung ~300 page phân hệ khác) — gỡ thẻ khỏi từng page cũ.

## Còn mở
- User test trình duyệt; chốt đuôi "… chờ duyệt"; 9 màn human chép nguyên từ màn Công ty (lỗi có sẵn).
- Nhóm "Cấu hình" Chấm công ẩn trên local vì mã `timesheet.thong_so.configure` chưa gán vai trò (gate giống topbar cũ).
