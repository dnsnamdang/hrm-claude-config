---
name: app-new-screen
description: Dựng màn mới cho TPE_APP — chọn kiểu (BLoC cho màn nhiều trạng thái / luồng lưu như Hub Meeting; StatefulWidget + ApiService cho danh sách / form gọn như Việc của tôi; KHÔNG Riverpod), cấu trúc thư mục, @RoutePage + đăng ký AutoRoute, DI, make gen, rồi dựng UI theo app-components + skill loại màn. Dùng khi "tạo màn hình mới", "thêm screen", "scaffold a feature", "new page", hoặc user đưa tên thư mục màn mới.
---

# Tạo màn hình mới — TPE_APP

> Rà lại 29/10/2026 (skill gốc của TuJobs, 06/2026): mẫu cũ dùng `@freezed class` (freezed 2) và `AutoRoute<dynamic>(page: XPage)`
> (auto_route cũ) — **không còn biên dịch** với freezed ^3.2 / auto_route ^11 hiện tại; màu `AppColors.current` và
> `CommonText`/`Dimen` không còn là chuẩn màn mới (Meeting / Việc của tôi dùng `AppPalette`, `Text`, số đo thiết kế).
> Đã sửa các mẫu dưới cho khớp code thật.

## 0. Chọn kiểu màn TRƯỚC

| Kiểu | Khi nào | Ví dụ tham khảo cách code |
|---|---|---|
| **A. BLoC** (`BasePageState` + `BaseBloc`, event/state freezed) | Màn nhiều trạng thái, nhiều bước lưu, nhiều màn con dùng chung 1 bản ghi | Hub Meeting `ui/meeting/meeting_hub/` |
| **B. StatefulWidget + ApiService** (`getIt<XxxApiService>()`, `setState`, `ValueNotifier` báo đổi) | Danh sách, form, chi tiết gọn; picker; sheet | Việc của tôi `ui/my_todo/` |
| ~~Riverpod `BasePage` + hooks~~ | KHÔNG dùng cho màn mới (còn ở ~90 màn cũ — để nguyên tới khi sửa) | — |

Sau khi có khung: dựng UI theo `app-components` + skill đúng loại màn (`app-list-page` / `app-form` /
`app-detail-page`), header/màu theo `app-module-shell`, test theo `app-simulator-test`.

**Kiểu B — khung tối thiểu** (đầy đủ xem `ui/my_todo/personal_todo_form_page.dart`):
```dart
@RoutePage()
class XxxPage extends StatefulWidget {
  const XxxPage({this.item, super.key});
  final Xxx? item;
  @override
  State<XxxPage> createState() => _XxxPageState();
}

class _XxxPageState extends State<XxxPage> {
  final _api = getIt<XxxApiService>();
  // _load() trong initState, setState khi có dữ liệu, lỗi qua MeetingSaveError.from(e)
  @override
  Widget build(BuildContext context) => CommonScaffold(
        backgroundColor: AppPalette.pageBg,
        appBar: PrimaryAppBar(text: 'Tiêu đề'),
        body: …,
        bottomBar: BottomActionBar(children: [ … ]),
      );
}
```

## Kiểu A — BLoC (chi tiết bên dưới)

## Thông tin cần hỏi trước khi tạo (nếu user chưa cung cấp)
1. **Tên màn hình** (PascalCase, thường tiếng Việt không dấu, VD: `QuanLyPhieuMuon`) → suy ra `snake_case` folder/file (`quan_ly_phieu_muon`).
2. **Tiêu đề AppBar** hiển thị (tiếng Việt có dấu, VD: `'Quản lý phiếu mượn'`).
3. **Có gọi API/use case khi mở màn hình không?** (để biết có cần `InitLoad` + repository hay không).
4. **Route trả về kiểu gì?** (`dynamic` mặc định, hoặc `bool`/model cụ thể).

Nếu user chỉ đưa tên — dùng mặc định: có `InitLoad`, route `dynamic`, hỏi lại tiêu đề nếu không rõ.

## Quy ước bắt buộc (đã xác minh trong codebase)
- Folder: `app/lib/ui/<snake_case>/` với `bloc/` con bên trong.
- Event **không** dùng một `@freezed` union — mỗi event là 1 class riêng `@freezed abstract class X extends <Name>Event with _$X` (freezed 3 BẮT BUỘC `abstract`), base là `abstract class <Name>Event extends BaseBlocEvent`.
- State: `@freezed abstract class <Name>State extends BaseBlocState with _$<Name>State`.
- Bloc: `@Injectable()` + `extends BaseBloc<<Name>Event, <Name>State>`. Đăng ký handler bằng `on<Event>(_handler, transformer: log())`; với action gửi/submit dùng `transformer: throttleTime(duration: const Duration(seconds: 2))`.
- Gọi nghiệp vụ qua `launchFutureUseCase(...)` / `launchSyncUseCase(...)` của `BaseBloc` (không gọi repository trực tiếp trừ khi đã có tiền lệ).
- Page: `StatefulWidget` + `_<Name>PageState extends BasePageState<<Name>Page, <Name>Bloc>`. Trigger load trong `initState` bằng `bloc.add(const InitLoad())`.
- UI: `CommonScaffold` + `PrimaryAppBar` + component trong `app-components` (nút, thẻ, ô nhập, lọc…). `Text` / `Column` / `Row` gốc dùng bình thường như Meeting / Việc của tôi; `CommonText`/`CommonContainer` không bắt buộc.
- Kích thước: component chung giữ kích thước của nó (nút `kAppButtonHeight` 44 — user chốt không nhân hệ số màn hình, dù thiết kế ghi 48); phần riêng của màn lấy theo số đo thiết kế `.pen` (pt). Thiết kế khác quy tắc / component chung → hỏi user (`app-ui-convention` mục Thứ tự ưu tiên). `Dimen.current` còn ở màn cũ / Meeting, màn mới không bắt buộc.
- Điều hướng giữa màn: `navigator.push(<Name>Route())`, `navigator.pop(result: ...)`. `Navigator.of(ctx).pop(...)` chỉ để đóng bottom sheet / hộp thoại vừa mở.
- Màu: `AppPalette.*` / `AppModule.currentColor` (KHÔNG `AppColors.current` ở màn mới, KHÔNG mã hex rải trong màn); KHÔNG `Color.withOpacity()` → `.withValues(alpha: ...)`.
- Haptic: chỉ `HapticFeedback.selectionClick()` / `HapticFeedback.lightImpact()` — KHÔNG `vibrate()`.

## Các file phải tạo

### 1. `bloc/<snake>_event.dart`
```dart
import 'package:freezed_annotation/freezed_annotation.dart';

import '../../../base/bloc/base_bloc_event.dart';

part '<snake>_event.freezed.dart';

abstract class <Name>Event extends BaseBlocEvent {
  const <Name>Event();
}

@freezed
abstract class InitLoad extends <Name>Event with _$InitLoad {
  const factory InitLoad() = _InitLoad;
}

@freezed
abstract class PageRefreshed extends <Name>Event with _$PageRefreshed {
  const factory PageRefreshed() = _PageRefreshed;
}
```

### 2. `bloc/<snake>_state.dart`
```dart
import 'package:freezed_annotation/freezed_annotation.dart';

import '../../../base/bloc/base_bloc_state.dart';

part '<snake>_state.freezed.dart';

@freezed
abstract class <Name>State extends BaseBlocState with _$<Name>State {
  const factory <Name>State({
    @Default(false) bool isLoading,
    @Default([]) List<dynamic> items,
    String? errorMessage,
  }) = _<Name>State;
}
```

### 3. `bloc/<snake>_bloc.dart`
```dart
import 'dart:async';

import 'package:injectable/injectable.dart';

import '../../../app.dart';
import '<snake>_event.dart';
import '<snake>_state.dart';

@Injectable()
class <Name>Bloc extends BaseBloc<<Name>Event, <Name>State> {
  <Name>Bloc(/* inject use cases / repository ở đây */) : super(const <Name>State()) {
    on<InitLoad>(_onInitLoad, transformer: log());
    on<PageRefreshed>(_onPageRefreshed, transformer: log());
  }

  FutureOr<void> _onInitLoad(InitLoad event, Emitter<<Name>State> emit) async {
    // launchFutureUseCase(useCase: ..., input: ..., doOnSuccess: (data) => emit(state.copyWith(items: data)));
  }

  FutureOr<void> _onPageRefreshed(PageRefreshed event, Emitter<<Name>State> emit) async {
    add(const InitLoad());
  }
}
```

### 4. `bloc/<snake>.dart` (barrel — bắt buộc, page import file này)
```dart
export '<snake>_bloc.dart';
export '<snake>_event.dart';
export '<snake>_state.dart';
```

### 5. `<snake>_page.dart`
```dart
import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../base/base_page_state.dart';
import '../../common_view/common_view.dart';
import '../../custom_view/custom_view.dart'; // PrimaryAppBar nằm ở đây, không phải common_view
import '../../resource/resource.dart';
import 'bloc/<snake>.dart';

@RoutePage()
class <Name>Page extends StatefulWidget {
  const <Name>Page({Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _<Name>PageState();
}

class _<Name>PageState extends BasePageState<<Name>Page, <Name>Bloc> {
  @override
  void initState() {
    super.initState();
    bloc.add(const InitLoad());
  }

  @override
  Widget buildPage(BuildContext context) {
    return CommonScaffold(
      appBar: PrimaryAppBar(text: '<AppBar title>'),
      backgroundColor: AppPalette.pageBg,
      body: BlocBuilder<<Name>Bloc, <Name>State>(
        bloc: bloc,
        builder: (context, state) {
          return SingleChildScrollView(
            padding: EdgeInsets.symmetric(horizontal: Dimen.current.w(16)),
            child: Column(
              children: const [
                // TODO: build UI với CommonText / CommonContainer ...
              ],
            ),
          );
        },
      ),
    );
  }
}
```

### 6. Đăng ký route trong `app/lib/navigation/routes/app_router.dart`
- Thêm `import 'package:app/ui/<snake>/<snake>_page.dart';` cùng nhóm import.
- Thêm dòng vào `routes` của `@AutoRouterConfig` (auto_route 11 — route class sinh từ `@RoutePage()`, tên `<Name>Route`):
  ```dart
  AutoRoute(page: <Name>Route.page),
  ```

## Bước cuối — BẮT BUỘC
Sau khi tạo xong, chạy code generation để sinh `.freezed.dart`, đăng ký DI (`di.config.dart`) và route (`app_router.gr.dart`):
```bash
make gen        # từ gốc repo TPE_APP (= build_runner build --delete-conflicting-outputs)
```
Rồi `cd app && fvm dart analyze lib/ui/<snake>/` (không thêm lỗi so với mức chuẩn). KHÔNG `dart format` lên file đang
sửa dở (chỉ file mới tạo) — diff phình hàng nghìn dòng. Agent chạy nền không chạy `make gen`.

## Lưu ý
- Thay `<Name>` = PascalCase, `<snake>` = snake_case xuyên suốt.
- Nếu cần use case mới: tạo trong `app/lib/domain/lib/src/usecase/...` extends `OldBaseFutureUseCase<Input, Output>` với `@Injectable()`, input `extends BaseInput`. Method API nằm ở `Repository` (interface trong `domain`, impl trong `data`).
- Nếu màn cần pull-to-refresh: bọc body trong `RefreshIndicator` và bắn `PageRefreshed`.
- Đối chiếu cách code với ví dụ kiểu A `ui/meeting/meeting_hub/` / kiểu B `ui/my_todo/` nếu nghi ngờ pattern (`check_in_out/` là màn cũ).
