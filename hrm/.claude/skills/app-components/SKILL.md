---
name: app-components
description: Danh mục component dùng chung của TPE_APP (app Flutter của HRM) — tra TRƯỚC khi dựng bất kỳ khối UI nào để các màn dùng đúng 1 widget cho 1 việc (khung màn, header, nút, hộp thoại, thẻ, dòng xem, ô nhập, ô chọn, nút gạt, bảng lọc, màn chọn nhân sự / khách hàng, rỗng / đang tải, badge, màu). Dùng khi định dựng widget mới, khi hỏi "cái này dùng widget nào", khi review thấy màn tự dựng AlertDialog / ElevatedButton / TextField trần / Container làm thẻ.
---

# Component dùng chung — TPE_APP

**Luật:** 1 việc = 1 widget. Tra bảng dưới trước khi viết UI. Không có → tạo trong `lib/custom_view/` (export
`custom_view.dart`) rồi **thêm 1 dòng vào bảng này**. Đừng dựng lại trong màn (dù "chỉ 1 chỗ").

Widget họ `Meeting*` (`ui/meeting/widget/`, `ui/meeting/picker/`) **là component chung của app** dù mang tên
Meeting — dựng cho Meeting trước, Việc của tôi đã dùng lại. Màn mới cứ import dùng. (Đổi tên / chuyển sang
`custom_view/` là việc riêng, hỏi user trước khi làm vì đụng nhiều file.)

## 1. Khung màn + phân hệ → chi tiết ở `app-module-shell`

| Việc | Dùng | File |
|---|---|---|
| Khung màn | `CommonScaffold(appBar:, body:, bottomBar:, backgroundColor: AppPalette.pageBg)` | `common_view/common_scaffold.dart` |
| Header mọi màn | `PrimaryAppBar(text:, actions:, bottom:, leadingIcon:)` — gradient + vân phân hệ + chuông tự có | `custom_view/primary_app_bar.dart` |
| Nút kính trên header (⋮, ✕) | `AppBarGlassButton(icon:, onTap:)` | `custom_view/primary_app_bar.dart` |
| Khung phân hệ (tab đáy + nút giữa + menu trái) | `ModuleShell(module:, tabs: [ModuleTab], fab: ModuleFab, drawerBuilder:)` | `custom_view/module_shell.dart` |
| Nền gradient + vân phân hệ cho header tự dựng | `ModuleHeaderDecor(module:, icon:)` | `custom_view/module_header_decor.dart` |
| Màu theo phân hệ | `AppModule.current` · `.color` · `.heroColors` · `AppModule.currentColor` · `AppModule.currentButtonGradient` | `resource/styles/app_module.dart` |
| Màu chữ / viền / nền | `AppPalette.textStrong · text · textBody · textSub · textLabel · textMuted · textHint · iconMuted · border · borderSoft · borderStrong · divider · fieldFill · pageBg · danger` | `resource/styles/app_module.dart` |

## 2. Nút + hộp thoại → quy tắc ở `app-ui-convention` mục 1–2

| Việc | Dùng |
|---|---|
| Hành động chính / phụ / nguy hiểm | `PrimaryButton` · `SecondaryButton` · `DangerButton` (`custom_view/primary_button.dart`) — icon TỰ có theo chữ (`appButtonIcon`), trả `Future` thì tự hiện vòng xoay + chặn bấm lặp |
| Thanh nút đáy màn | `BottomActionBar(children: [...], note:)` (`custom_view/app_card.dart`) — `note` = dòng xám lý do không làm được |
| Hỏi Có / Không | `showAppConfirm(context, title:, message:, acceptText:, danger:, icon:)` → `bool` (`custom_view/app_dialog.dart`) |
| Hộp thoại nội dung riêng | `AppDialog(content:, actions:)` |
| Nhập lý do (Từ chối, Hủy…) | `ReasonInputDialog` |
| Thoát form chưa lưu | `UnsavedChangesGuard(isDirty:, screenName:, onSave:, child:)` → tự hỏi bằng `showUnsavedChangesDialog` |
| Lớp tải chặn chạm | `GlobalLoading.show()` / `hide()` (`custom_view/page_loading_bar.dart`) — nút trả Future đã tự quay, thường không cần |
| Vòng xoay | `AppSpinner(color:, size:)` |

## 3. Danh sách → quy tắc ở `app-list-page`

| Việc | Dùng |
|---|---|
| Hàng tìm + nút lọc dưới header | `ListFilterBar(searchController:, searchHint:, onSearchChanged:, activeCount:, onFilter:, activeChips:, onClearFilter:)` |
| Bảng lọc (bottom sheet 2 nấc) | `showFilterSheet(context, fields:, initial:, onCount:, unit:, openField:)` → `FilterValues?` (`custom_view/filter_sheet.dart`) |
| Loại trường lọc | `FilterChipsField` (chip, `multi`) · `FilterDateRangeField` · `FilterPickerField(sections: [FilterPickerSection(parentKey:)])` · `FilterTextField` · `advanced: true` |
| Chip tiêu chí đang bật | `filterActiveChips(fields:, values:, onOpen:, onRemove:)` |
| Nhóm Công ty – Phòng ban – Bộ phận theo quyền xem | `buildOrgScopeField(profile, OrgScopePermissions.of('<meeting/task/issue>'))` + `orgScopeQuery(values)` (`custom_view/filter_org_scope.dart`) — profile = `UserApiService.getUserProfile()` |
| Thẻ Nhiệm vụ / Vấn đề (ưu tiên · trạng thái · 💬 / tên / ngữ cảnh / meta) | `WorkRecordCard` + `WorkTotalLine` (Tổng · Quá hạn) (`ui/work/widget/work_widgets.dart`) |
| Rỗng | `AppEmptyWidget(filtered: <đang lọc/tìm>)` — KHÔNG tự đặt title cho trạng thái rỗng |
| Đang tải | `ContentSkeleton(cards: n)` · `SkeletonCard` · `ListFooterSkeleton` (`custom_view/skeleton.dart`) |
| Thẻ trắng chung | `AppCard(child:, onTap:, padding:, margin:)` |
| Thẻ việc (Việc của tôi / lịch) | `WorkItemCard` (`ui/my_todo/widget/work_item_card.dart`) |
| Thẻ meeting | `MeetingCard` (`ui/meeting/widget/meeting_card.dart`) |
| Badge trạng thái | `StatusBadge(text:, color:, textColor:)` — chữ + màu do BE trả (`common_view/status_badge.dart`) |
| Danh sách tìm phía máy chủ có phân trang (màn chọn) | `MeetingSearchList<T>(fetch: (kw, page, filters) => SearchPage(...), itemBuilder:, hint:, grouped:)` |
| Thẻ gom nhiều dòng | `meetingGroupedCard([...])` |

## 4. Form → quy tắc ở `app-form`

| Việc | Dùng |
|---|---|
| Ô gõ (khuôn thiết kế C/Field) | `MeetingTextField(controller:, hint:, label:, required:, maxLines:, error:)` |
| Ô chọn (bấm mở màn / sheet chọn) | `MeetingSelectRow(label:, placeholder:, value:, required:, error:, onTap:)` |
| Nhãn + lỗi dưới ô (khi tự dựng ô) | `MeetingFieldLabel` · `MeetingFieldError` |
| Nút gạt 2–3 lựa chọn | `MeetingSegmented(options: [(value, label, icon)], value:, onChanged:)` — nền trắng TRƯỢT ngang |
| Khối gập đánh số ①②③ | `MeetingSection` |
| Chọn 1 nhân sự (toàn trang, tìm máy chủ) | `pickEmployee()` → `ApiNvData?` (`ui/chon_nv/employee_picker.dart`) |
| Chọn nhân sự (Meeting, nhiều người, gợi ý) | `MeetingEmployeePickerPage` |
| Chọn khách hàng | `CustomerPickerPage<T>(fetch:, describe: → CustomerPickInfo)` (`ui/customer_picker/`) — vd `pickJobAssignCustomer()` |
| Soạn văn bản có định dạng (HTML như web) | `MeetingRichEditor` |
| Tệp đính kèm: xem / tải | `MeetingFileActions` |

## 5. Chi tiết → quy tắc ở `app-detail-page`

| Việc | Dùng |
|---|---|
| Dòng nhãn – giá trị (chế độ xem) | `MeetingViewRow(label, value:)` (xếp dọc) · `WorkInfoRow(label, value)` (nhãn trái – giá trị phải, tự ẩn khi trống — màn chi tiết Nhiệm vụ / Vấn đề) |
| Đầu màn chi tiết (chip loại · mã, tên, pill trạng thái ▾ / ưu tiên / hạn, tiến độ) | `WorkHero` + `WorkPill` (`ui/work/widget/work_widgets.dart`) |
| Khối gập ở màn chi tiết (icon · tiêu đề · số đếm · ▴▾) | `WorkFoldCard` — khối FORM đánh số dùng `MeetingSection` |
| Dòng "Lịch sử thay đổi ›" · nút 💬 có số trên header | `WorkLinkRow` · `WorkCommentHeaderButton` |
| Menu ⋮ "Hành động" | `showActionMenuSheet(context, subtitle:, items: [ActionMenuItem(icon:, label:, danger:, onTap:)])` (`custom_view/action_menu_sheet.dart`) |
| Sheet đổi trạng thái (allowed_next_statuses, lý do từ chối, bước sang màn khác) | `showWorkStatusSheet(...)` (`ui/work/widget/work_status_sheet.dart`) |
| Lịch sử thay đổi (system-logs) | `WorkHistoryRoute(type: 'task'/'issue', id:, recordTitle:)` |
| Chọn 1 mục trong danh mục đã tải (giải pháp, hạng mục…) | `pickWorkOption(context, title:, options: [WorkPickOption])` — ≤ 8 mục bottom sheet, nhiều hơn trang chọn có ô tìm |
| Khối trên màn Hub (icon · tên · gợi ý · giá trị · ›) | `MeetingHubRow(icon:, title:, hint:, value:, error:, onTap:)` |
| Dòng người (avatar chữ tắt) | `MeetingPersonRow(name:, subtitle:, tag:, badge:, trailing:)` |
| Thẻ nhóm người có "Thêm nhanh" | `MeetingGroupCard` |
| Dải thông báo đỏ / xám dưới header, thẻ xanh hướng dẫn | `MeetingBanner` |
| Lỗi tải / trống của màn chi tiết | `MeetingLoadError` |
| Chữ dài có "Xem thêm" | `ExpandableText` |

## 6. Khác

| Việc | Dùng |
|---|---|
| Điều hướng | `navigator.push(XxxRoute(...))` (extension trên `Object`); trong hàm top-level dùng `getIt<AppNavigator>()` |
| Rung khi chạm | `HapticFeedback.selectionClick()` / `lightImpact()` — KHÔNG `vibrate()` |
| Báo kết quả thao tác (thành công / lỗi) | `navigator.showSuccessSnackBar('…')` / `showErrorSnackBar('…')` → hiện `AppToast` (`custom_view/app_toast.dart`): đầu màn, nền màu + icon ✓ / ✕, tự ẩn, không mất khi `pop()`. Quy tắc câu chữ: `app-ui-convention` mục 6a |
| Lỗi lưu từ BE (422 theo trường) | `MeetingSaveError.from(e)` → `.summary` + `.fields` (`ui/meeting/model/meeting_errors.dart`) |
| Báo màn khác tải lại sau khi đổi dữ liệu | `ValueNotifier` dùng chung (vd `myTodoChanged`) — màn nghe tự `_load()` |

## KHÔNG dùng ở màn mới

`AlertDialog` / `CupertinoAlertDialog` / `showDialog` + Column nút tự dựng · `ElevatedButton` / `TextButton` /
`OutlinedButton` / `CommonButton` tự tô màu làm nút hành động · `TextField` trần không khuôn · `Container` tự
vẽ thẻ / badge / màu hex rải rác (dùng `AppCard`, `StatusBadge`, `AppPalette`) · `FilterView` / `showFilterPanel`
(bảng lọc kiểu cũ) · `ListFilterBar(quickChips:)` · `ChonNvPage` (hộp chọn nhân sự cũ — dùng `pickEmployee`) ·
`ScaffoldMessenger.showSnackBar(SnackBar(...))` / `Fluttertoast` / `ViewUtils.showAppSnackBar` (dùng `AppToast` qua navigator).
