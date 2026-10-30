---
name: app-module-shell
description: Khung phân hệ của TPE_APP — 5 phân hệ (Chấm công, Công việc, Meeting, Đào tạo, Cơm), màu theo phân hệ, header gradient + vân nền, chuông thông báo, tab đáy + nút giữa "Tạo mới" (menu chọn loại), menu trái (drawer), thanh tab con trên header, hiệu ứng chuyển tab. Dùng khi thêm màn vào phân hệ, thêm mục menu / tab / loại tạo mới, khi header sai màu / thiếu vân, khi tab chuyển giật.
---

# Khung phân hệ — TPE_APP

## 1. Màu + header

- 5 phân hệ = `enum AppModule` (`resource/styles/app_module.dart`): `chamCong` xanh dương · `congViec` xanh lá ·
  `meeting` xanh ngọc · `daoTao` tím · `com` cam. Mỗi phân hệ có `color`, `color2`, `heroColors` (3 màu
  gradient header), vân nền (`watermark`). Màu đang dùng = `AppModule.current` (đặt khi vào phân hệ).
- **Không viết mã màu phân hệ trong màn.** Lấy `AppModule.currentColor`, `AppModule.currentButtonGradient`,
  `AppModule.currentTint` (nền nhạt). Màu chữ / viền dùng `AppPalette.*`.
- **Mọi màn dùng `PrimaryAppBar`** → tự có gradient + vân nền (vân tay Chấm công, …) của phân hệ ĐÚNG ở mọi màn
  con (user chốt 28/10/2026: vân hiện ở cả màn khác trong phân hệ, không riêng Tổng quan). Header tự dựng
  (vd màn Thông báo) thì bọc `ModuleHeaderDecor(module:, icon:)` phía sau nội dung.
- **Chuông thông báo có ở MỌI màn** (sẵn trong `PrimaryAppBar`), chỉ tắt ở chính màn Thông báo.
- Header chỉ có: ☰ / ‹ · tiêu đề · (⋮ hành động nếu có) · chuông. Không đặt nút lọc / ➕ trên header màn
  danh sách (lọc nằm ở `ListFilterBar`, tạo mới ở nút giữa).

## 2. Tab đáy + nút giữa "Tạo mới"

- Phân hệ dựng bằng `ModuleShell(module:, tabs: [ModuleTab(label:, icon:, builder:, badge:)], fab: ModuleFab, drawerBuilder:)`
  (`ui/module_shell/module_shell_pages.dart`). Tab dựng lười, giữ trạng thái khi chuyển.
- **Nút giữa = lối tạo mới DUY NHẤT của phân hệ.** Bấm mở bottom sheet chọn loại (khuôn
  `showCongViecCreateMenu` — `ui/my_todo/create_menu_sheet.dart`): mỗi dòng icon màu loại · tên · 1 dòng mô tả.
  - Tên loại = ĐÚNG tên ở bộ lọc / web (vd "Phiếu giao việc (chấm công)", không "Giao việc").
  - Chỉ đưa loại **app đã có màn tạo**; loại chưa có màn → không đưa (ghi rõ trong code là chưa có).
  - Mỗi dòng ẩn theo quyền tạo loại đó (như nút Thêm ở màn danh sách loại đó).
  - Web có menu Tạo mới tương ứng thì 2 bên cùng danh sách loại (sửa 1 bên phải kiểm bên kia).
  - Mở từ tab Lịch → truyền ngày đang chọn để form điền sẵn (thiết kế mytodo D1).

## 3. Menu trái (drawer)

- Khai ở `ui/module_shell/module_menus.dart` (`ModuleMenus`), theo phân hệ. Mục cần quyền → điều kiện trong
  đó (fail-closed: không có quyền thì không hiện).
- Mục đã có tab đáy thì drawer chuyển tab (không push màn mới). Màn báo cáo phụ (Báo cáo tiến độ task) để ở
  drawer, giữ badge.

## 4. Tab con trên header (2–3 lựa chọn)

- Đặt trong `PrimaryAppBar(bottom: PreferredSize(...))`, khuôn `_HeaderTabs` của Việc của tôi
  (`ui/my_todo/my_todo_page.dart`): rãnh kính trắng 12%, ô đang chọn trắng, chữ đậm màu `heroColors[1]`.
- **Chuyển động bắt buộc giống `MeetingSegmented`:** nền trắng là 1 "con trượt" `AnimatedPositioned` 240ms
  `easeOutCubic` chạy sang ô mới; chữ GIỮ độ đậm, chỉ đổi màu (`AnimatedDefaultTextStyle` / `ColorTween`
  200ms). KHÔNG tắt ô cũ – bật ô mới (giật, user báo 29/10/2026), KHÔNG đổi độ đậm chữ (nhảy bề rộng).
- Nội dung các tab con: `IndexedStack` (giữ trạng thái, cuộn), mỗi tab là widget riêng `AutomaticKeepAliveClientMixin`.
- Nút gạt trong nội dung (Đối tác / Nội bộ, Tuần / Tháng) cũng theo đúng chuyển động trên (`MeetingSegmented`).

## 5. Lịch trong màn (tuần / tháng)

- Khuôn tab Lịch của Việc của tôi (`ui/my_todo/my_todo_calendar_view.dart`): thanh kỳ `‹ dd/MM–dd/MM ›` + Hôm nay
  + nút gạt Tuần/Tháng; mỗi ngày tối đa 2 chấm màu loại + "+"; dưới là danh sách theo ngày.
- **Kéo thu nhỏ / mở rộng như lịch iOS:** vuốt lên trên lịch → 1 tuần, kéo xuống → cả tháng, thanh kéo xám dưới
  lịch chạm để đổi; dùng chung hàm đổi với nút Tuần/Tháng, `AnimatedSize` 220ms.

## Checklist

- [ ] Màn mới dùng `PrimaryAppBar` (không tự vẽ header), không mã màu phân hệ trong màn
- [ ] Loại tạo mới mới thêm → có trong menu nút giữa (đúng tên bộ lọc, ẩn theo quyền) + web tương ứng
- [ ] Tab con / nút gạt chuyển bằng con trượt, chữ không đổi độ đậm
- [ ] Đã xem trên simulator: màu, vân, chuông đúng phân hệ ở cả màn con
