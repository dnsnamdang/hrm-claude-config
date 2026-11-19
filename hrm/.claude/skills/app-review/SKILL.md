---
name: app-review
description: Review code Flutter / git diff của TPE_APP theo quy chuẩn app (app-ui-convention, app-components, skill loại màn, app-hrm-api, app-notification) — freezed 3 / route / make gen, mapper API, ép kiểu, quyền, component dùng chung, nút / hộp thoại / lọc / form / bàn phím. Use when the user asks to "review code", "check màn hình này", "kiểm tra theo chuẩn dự án", or before committing a feature.
---

# Code Review theo chuẩn TPE_APP

Review file/đoạn code được chỉ định, hoặc diff hiện tại (`git diff`), theo đúng convention dự án. Nếu user không chỉ rõ phạm vi → mặc định review `git diff` của các file Dart đang thay đổi.

## Cách làm
1. Xác định phạm vi: file user đưa ra, hoặc chạy `git diff --name-only` lọc `*.dart` (bỏ `*.g.dart`, `*.freezed.dart`, `*.gr.dart`, `*.gen.dart`).
2. Đọc code, đối chiếu checklist dưới.
3. Báo cáo theo 3 mức ưu tiên, mỗi finding kèm `file:line` (markdown link clickable) và đề xuất fix cụ thể.
4. Chạy `cd app && fvm dart analyze <path>` để bắt lỗi tĩnh bổ sung (so với mức chuẩn, không chạy `dart format`).

## Checklist

> Rà lại 29/10/2026 (skill gốc của TuJobs, 06/2026): bỏ các mục không còn là chuẩn ở màn mới (bắt buộc `CommonText` /
> `CommonContainer` / `Dimen`, mọi logic phải qua BLoC + use case) — Meeting / Việc của tôi đã chốt khác. Màn CŨ chưa
> đụng tới thì không bắt sửa theo checklist này (phạm vi `app-ui-convention`).

### 🔴 Nghiêm trọng — phải sửa
- [ ] Freezed 3: `@freezed` thiếu `abstract` / `sealed` → không biên dịch. Sửa model / event / state / route / `@LazySingleton` mà CHƯA `make gen`.
- [ ] Route mới thiếu `@RoutePage()` hoặc chưa thêm `AutoRoute(page: XRoute.page)` vào `app_router.dart`.
- [ ] API trả MẢNG đọc bằng mapper `dataResponse` → luôn 0 dòng (`app-hrm-api` mục 1).
- [ ] Ép kiểu cứng dữ liệu BE / `FilterValues` (`as List`, `as Set`, `as int`) → crash khi BE / bộ lọc đổi kiểu; đọc phòng thủ.
- [ ] Map số trạng thái → chữ / màu ở app (phải lấy `status_text` / `status_color` BE); tự ghép câu thông báo ở app.
- [ ] Thông báo `type` mới ở BE mà `notification_bloc._redirect()` chưa có `case`; mượn `type` của luồng khác.
- [ ] Cờ quyền mặc định `true` / hiện nút rồi disable thay vì ẩn; danh sách và chi tiết lệch điều kiện hành động.
- [ ] Tự dựng `AlertDialog` / `CupertinoAlertDialog` / nút `ElevatedButton`… ở màn mới (`app-components` mục KHÔNG dùng).
- [ ] Form: tự chặn "bắt buộc" ở app thay vì để BE trả lỗi; lỗi không tô đúng ô; thiếu `UnsavedChangesGuard`; lưu xong không quay về.
- [ ] `HapticFeedback.vibrate()`.

### 🟡 Cảnh báo — nên sửa
- [ ] Không dùng component có sẵn (`ListFilterBar`, `showFilterSheet`, `AppEmptyWidget(filtered:)`, `MeetingTextField`, `pickEmployee`…) mà dựng lại.
- [ ] Màu hex / mã màu phân hệ trong màn (dùng `AppPalette` / `AppModule.currentColor`); `withOpacity` → `withValues(alpha:)`.
- [ ] Chữ nút sai bảng (Huỷ / Xoá / Đồng ý / Cập nhật / `&`); nút chính không nằm bên phải; truyền `icon:` trùng icon tự động.
- [ ] Màn danh sách có `quickChips`, nút ↻ / pill lọc riêng, tiêu chí lọc khác web; rỗng tự đặt title.
- [ ] Đổi tab / nút gạt không dùng con trượt (`MeetingSegmented` / `_HeaderTabs`), chữ đổi độ đậm khi chọn.
- [ ] Ô nhiều dòng / form dài thiếu `keyboardDismissBehavior: onDrag`; ô 1 dòng thiếu `textInputAction: next`.
- [ ] Gọi API trong vòng lặp / mỗi dòng 1 request; tải lại cả màn khi chỉ đổi 1 dòng (cập nhật tại chỗ rồi đồng bộ ngầm).
- [ ] `Navigator.of(context).push` giữa các màn (dùng `navigator.push(XRoute())`; `Navigator.of(ctx).pop` chỉ để đóng sheet / hộp thoại).

### 🟢 Best practice
- [ ] Màn mới đúng 1 trong 2 kiểu của `app-new-screen` (BLoC hoặc StatefulWidget + ApiService), không Riverpod mới.
- [ ] BLoC: `buildWhen` / `BlocSelector`; handler gửi form có `throttleTime`.
- [ ] Màn con đổi dữ liệu báo màn danh sách qua `ValueNotifier` chung / `then(reload)`.
- [ ] Code theo flavor dùng `env.isThanhAnGroup` / `BuildConfig.flavor`, không so chuỗi rời rạc.
- [ ] `fvm dart analyze` không thêm lỗi so với mức chuẩn; đã test theo `app-simulator-test` (ghi rõ phần chưa thử).

## Định dạng output
Với mỗi nhóm, liệt kê:
> 🔴 [`path/to/file.dart:42`](path/to/file.dart#L42) — Mô tả vấn đề. **Fix:** đề xuất cụ thể.

Kết thúc bằng tổng kết ngắn (số lượng mỗi mức + có nên chạy `build_runner`/`analyze` lại không).
