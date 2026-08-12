# Plan — Bộ lọc màn Danh sách phiếu giao công tác (app)

Repo: `TPE_APP` nhánh `main`. Không sửa BE.

## Phase 1 — Data layer

- [x] `ApiValueData`: thêm `company_id`, `department_id` (nullable)
- [x] `ApiUserProfileData`: thêm `parts`, `permissions`
- [x] Thêm model `ApiPermissionData` (chỉ field `name`)
- [x] `UserApiService.fetchDanhSachPhieuGiaoCongTac`: nhận 14 param optional, bỏ entry null khỏi query
- [x] `FetchDanhSachGiaoCongTacInput`: thêm 14 field nullable
- [x] `FetchDanhSachGiaoCongTacUseCase`: truyền input xuống repository
- [x] `Repository.fetchDanhSachGiaoCongTac` + `UserRepositoryImpl`: đổi chữ ký, bỏ hard-code `company_id`
- [x] Chạy `build_runner build --delete-conflicting-outputs`

## Phase 2 — Bloc

- [x] Thêm field filter vào `DsPhieuGiaoCongTacBloc`
- [x] Thêm event `FilterApplied`
- [x] Nạp options qua `getUserProfile()` khi init (KHÔNG gate `isThanhAnGroup`)
- [x] Set mặc định `company` = công ty user
- [x] Xoá event `TextChanged` + `state.word` (code chết)
- [x] Bổ sung state chứa options + permissions

## Phase 3 — UI

- [x] `Scaffold` + `GlobalKey` + `endDrawer` thay `CommonScaffold`
- [x] Icon lọc trên `PrimaryAppBar` + chấm badge khi có filter
- [x] `FilterView` 14 trường theo bảng trong spec
- [x] Ẩn Công ty/Phòng ban/Bộ phận theo quyền
- [x] Cascade: đổi Công ty xoá PB+BP; đổi PB xoá BP
- [x] `onApply` / `onReset` đúng business rule (Làm mới về công ty user)

## Phase 4 — Kiểm chứng

- [x] `flutter analyze` sạch phần code mới
- [x] Build lại app, mở màn, thử lọc trên emulator (tài khoản DNS Admin, flavor production)

### Checkpoint — 2026-08-06 10:26
Vừa hoàn thành: code đủ 3 phase + verify trên Android emulator (flavor `production`, tài khoản DNS Admin).
Đã kiểm chứng thực tế: bộ lọc mở từ icon appbar · Công ty điền sẵn công ty user · "Làm mới" xoá hết
nhưng giữ Công ty · lọc `code=PCT-13493` trả đúng 1 bản ghi · badge cam hiện khi có filter ·
cascade Phòng ban → Bộ phận (chọn PHÒNG QUẢN TRỊ THÔNG TIN thì Bộ phận chỉ còn 2 mục thuộc phòng đó).
Chưa kiểm: 8 ô text còn lại, Loại công tác, Trạng thái, Nhân viên, Từ/Đến ngày, ẩn ô theo quyền
(tài khoản admin có đủ quyền nên không thấy nhánh ẩn).
Bước tiếp: user review + test các trường còn lại.
Blocked:

### Checkpoint — 2026-08-06 10:30 (iOS)
Vừa hoàn thành: build lại iOS Simulator (iPhone 15) với code bộ lọc — Xcode build done 31.8s,
không lỗi compile, app khởi động sạch (`Flavor.production`), log chỉ còn cảnh báo locale `vi` có sẵn từ trước.
Đang làm dở: CHƯA verify được luồng lọc trên iOS — không bấm được lên Simulator
(`osascript` bị chặn assistive access -1719; chưa có `cliclick`/`idb`).
Rủi ro còn treo: 2 ô Từ ngày/Đến ngày dùng `DatePicker.showDatePicker` (đoạn vừa sửa trong
`DateTimeInput`), iOS render khác Android nên không suy ra từ kết quả Android được.
Bước tiếp: user cấp quyền Accessibility cho Visual Studio Code → chạy lại kịch bản đã test bên Android.
Blocked: quyền Accessibility

### Checkpoint — 2026-08-06 11:05 (iOS — đã verify render)
Vừa hoàn thành: verify bộ lọc trên iOS Simulator bằng cách chèn code tạm tự mở drawer + tự bật
date picker, chụp màn hình, rồi GỠ SẠCH code tạm (git diff không còn `user_role_menu_page.dart`).
Kết quả: drawer render đúng trên iOS (Công ty điền sẵn công ty user, Phòng ban/Bộ phận/Phiếu công tác/
Loại công tác đúng thứ tự, không vỡ layout); date picker chạy đúng chế độ `dateOnly` —
3 cột Năm/Tháng/Ngày, KHÔNG có cột giờ:phút, nút Hủy bỏ/Xong tiếng Việt.
Chưa kiểm trên iOS: hành vi khi BẤM (không có cách bơm touch — xem ghi chú công cụ bên dưới),
tức là onApply/onReset/cascade trên iOS suy từ Android chứ chưa chứng minh trực tiếp.

Ghi chú công cụ (để lần sau khỏi mò lại): KHÔNG bơm được touch vào iOS Simulator trên máy này.
- `osascript` System Events `click at` → lỗi -25204
- `cliclick` (kể cả sau khi cấp quyền Accessibility, cửa sổ AXFocused=true) → chuột hover đúng chỗ
  nhưng click không được nhận; kiểm chứng bằng nút Quay lại cũng không ăn
- `idb-companion` → đòi Xcode 26.3, máy có Xcode 15.4 (KHÔNG nên nâng: dự án khoá Flutter 3.22.3)
→ Cách dùng được: chèn code tạm tự điều khiển + `xcrun simctl io booted screenshot`.
Toạ độ cửa sổ Simulator lấy động từ AXGroup: script `scratchpad/tap.sh` (chỉ dùng để hover/định vị).

## Phase 5 — Làm lại trên nhánh `develop` (2026-08-06)

Lý do: user báo nhánh code mới nhất là `develop`, không phải `main`. `origin/develop` đi trước `main`
64 commit và các file liên quan lệch rất nhiều (`user_api_service.dart` 2.777 dòng) → patch cũ không áp
được, phải viết lại theo code `develop`.

- [x] Backup code bản `main`: 2 patch + 19 file trong scratchpad, thêm `git stash` trên `main`
- [x] `git fetch` → checkout `develop` (origin/develop)
- [x] Cài `fvm` (qua `dart pub global activate`) + Flutter **3.41.7** theo `.fvmrc`
- [x] Port model `ApiUserProfileData` (+`parts`,`permissions`,`ApiPermissionData`) — freezed 3 `abstract class`
- [x] Port API service → `user_api_service_cong_tac_ext.dart` (14 param optional)
- [x] Port repository + usecase input
- [x] Port bloc (đổi `hasActiveFilter` → `activeFilterCount` cho `FilterView.activeCount`)
- [x] Port UI — dùng `DateInput` có sẵn thay vì sửa `DateTimeInput`; thêm `onClear` cho các ô text
- [x] `build_runner` (1.084 output, 53s) + `flutter analyze` sạch
- [x] Build & test lại trên Android (đã verify bằng log request + danh sách đổi đúng)
- [ ] Build & test lại trên iOS (chưa rõ Xcode 15.4 có đủ cho Flutter 3.41.7 không)

### Khác biệt so với bản làm trên `main` (bản develop sạch hơn)
- KHÔNG còn sửa widget dùng chung `DateTimeInput` — `develop` đã có `DateInput` chọn-ngày sẵn
- KHÔNG còn phải ghim `wakelock_plus` — `develop` đã dùng plugins DSL mới trong settings.gradle
- Badge lọc dùng `FilterView.activeCount` có sẵn thay vì tự vẽ

### Checkpoint — 2026-08-06 12:00 (develop / Android)
Vừa hoàn thành: verify bộ lọc trên nhánh `develop`, Android emulator, flavor production.
Bằng chứng (app tự log URL request):
- Mở màn:   `assign_business?page=1&limit=10&type=all&company_id=1` → company_id mặc định = công ty user,
  không gửi param rỗng.
- Lọc mã:   `...&code=P` → param gắn đúng (kết quả không đổi là ĐÚNG vì `P` khớp mọi mã `PCT-*`).
- Lọc loại: `...&business_type=2` → danh sách đổi hẳn sang PCT-13390/13301/13198, cả 3 đều
  "Loại công tác: Phiếu công tác khác". Chấm cam trên icon lọc + header "1 bộ lọc đang áp dụng" đúng.
- Nút ✕ trong ô text xoá đúng giá trị (onClear nối vào bloc).
Đường vào màn: menu trái → Giao việc/Công tác → Phiếu giao công tác (phải CUỘN mới thấy).

BẪY MÔI TRƯỜNG (nhánh develop, ghi để lần sau khỏi mò):
- Flutter 3.41.7 bật Impeller mặc định trên Android → AVD `Pixel_4_API_29` treo ANR kèm
  `EGL Error ... impeller/toolkit/egl`. Phải chạy `--no-enable-impeller` (hoặc dùng AVD mới hơn).
- Tắt Impeller thì rơi về software rendering, emulator giật nặng → `adb shell input text` rớt ký tự,
  gõ 9 ký tự chỉ vào 1-4 ký tự và đến rất chậm. Verify bằng LOG REQUEST đáng tin hơn nhìn UI.
- Bàn phím Gboard che nút Áp dụng; `keyevent 111` không đóng được, phải `keyevent 4`.

Chưa kiểm trên develop: iOS (chưa build lại sau khi port), các ô text còn lại, cascade, Làm mới,
nhánh ẩn theo quyền (tài khoản admin đủ quyền).
Bước tiếp: build iOS trên develop; user review code.

### Checkpoint — 2026-08-06 (develop / iOS) — BLOCKED bởi môi trường
iOS trên `develop` KHÔNG build được trên máy này. Không liên quan tới code bộ lọc.
Chuỗi sự việc + cách xử lý (ghi lại để lần sau khỏi mò):
1. `pod install` fail: "specs repository is too out-of-date" → chạy `pod repo update` (vài phút).
2. Vẫn fail: `Podfile.lock` cũ (sinh khi build nhánh `main`) ghim `MapboxMaps 11.11.0`, còn `develop`
   dùng `mapbox_maps_flutter 2.22.0` cần `MapboxMaps 11.22.0`. `Podfile.lock` KHÔNG được git track
   → xoá `Podfile.lock` + `Pods/` rồi `pod install` lại là qua. (Bẫy khi nhảy nhánh main ↔ develop.)
3. Pods cài xong nhưng Xcode build fail — lỗi nằm trong SOURCE CỦA POD, không phải code app:
   `Pods/MapboxMaps/Sources/MapboxMaps/Style/StyleManager.swift:1803`
   `Swift Compiler Error: Reference to captured var 'cancelable' in concurrently-executing code`
   Máy: Xcode 15.4 / Apple Swift 5.10. MapboxMaps 11.22.0 cần toolchain Swift mới hơn (Xcode 16+).
→ Muốn build iOS trên `develop` phải NÂNG XCODE. Không tự nâng vì đây là quyết định môi trường của user
   và ảnh hưởng mọi project khác trên máy.
Trạng thái iOS: code đã port xong + `flutter analyze` sạch, nhưng CHƯA chạy được trên iOS ở nhánh này.

### Checkpoint — 2026-08-06 (iOS trên develop — đã truy ra tận gốc)
KẾT LUẬN: build iOS nhánh `develop` cần **Xcode 26** (Swift 6.2), và Xcode 26.0.1–26.3 cần
**macOS Sequoia 15.6** (Apple: developer.apple.com/support/xcode). Máy đang macOS 15.3.2 → chỉ cần
cập nhật vặt trong dòng Sequoia, KHÔNG phải lên macOS 26 Tahoe.

Đường đã thử và LOẠI (ghi để khỏi thử lại):
- Xcode 16.4 / Swift 6.1.2 → VẪN LỖI y nguyên. Nâng từ 15.4 lên 16.4 không giải quyết gì.
- Ép `SWIFT_VERSION = 5.0` cho riêng pod MapboxMaps trong `Podfile` post_install → VẪN LỖI.
  Đã kiểm chứng setting thực sự áp dụng (Debug config của target MapboxMaps = 5.0 trong Pods.pbxproj).
  Kết luận: lỗi này không phụ thuộc language mode, chỉ compiler Swift 6.2 mới chấp nhận. Đã revert Podfile.

Nguồn gốc lỗi (không phải bug của app):
`Pods/MapboxMaps/Sources/MapboxMaps/Style/StyleManager.swift:1803` — bắt và ghi biến `var cancelable`
bên trong `Task { }`. `pubspec.yaml` ghim CỨNG `mapbox_maps_flutter: 2.22.0` → `MapboxMaps 11.22.0`,
và `pubspec.lock` CÓ được git track ⇒ team cố ý dùng bản này ⇒ team đang build bằng Xcode 26.

Việc cần user làm: System Settings → Software Update → lên macOS Sequoia 15.6+ → cài Xcode 26.3
(`xcodes install 26.3`) → rồi build lại. Xcode 16.4 vừa cài trở thành thừa.

## Phase 6 — iOS chạy được + sửa placeholder select (2026-08-06)

### Môi trường: đã gỡ xong nút thắt iOS
Chuỗi bắt buộc để build iOS nhánh `develop`: **macOS Sequoia 15.7.8 → Xcode 26.3 → Swift 6.2.4 →
tải runtime iOS (`xcodebuild -downloadPlatform iOS`)**. Thiếu bất kỳ mắt nào đều gãy.
- Xcode 16.4 KHÔNG đủ (Swift 6.1.2 vẫn từ chối `MapboxMaps/StyleManager.swift`) — đã thử, đã loại.
- Ép `SWIFT_VERSION=5.0` cho pod MapboxMaps: KHÔNG khỏi — đã thử, đã loại, Podfile đã revert.
- `Runner.xcodeproj` ghim `EXCLUDED_ARCHS[sdk=iphonesimulator*] = arm64` (di sản Mapbox) ⇒ app chỉ
  build được cho simulator **x86_64** ⇒ KHÔNG chạy được trên simulator iOS 26 (chỉ có arm64).
  Cách đi: dùng simulator **iOS 17.5** (iPhone 15) — vẫn nằm trong danh sách destination hợp lệ.
  Nếu sau này cần iOS 26: `xcodebuild -downloadPlatform iOS -architectureVariant universal`.
- `Podfile.lock` KHÔNG git track → nhảy nhánh main ↔ develop phải xoá `Podfile.lock` + `Pods/` rồi
  `pod install` lại, nếu không sẽ kẹt version Mapbox cũ.
- Simulator của Xcode 26 NHẬN được click tổng hợp (`cliclick`) — bản Xcode 15.4 thì không.
  Nhưng **drag/scroll tổng hợp vẫn không ăn** → muốn tới màn nằm sâu trong menu cuộn thì
  vẫn phải chèn code tạm tự điều hướng.

### Sửa: SelectInput nuốt mất hintText (user phát hiện)
- [x] `custom_view/filter_view.dart` — `SelectInput` khai `hintText` là tham số BẮT BUỘC nhưng không
      nối vào `dropdownSearchDecoration` ⇒ mọi ô select toàn app rỗng khi chưa chọn, lệch hẳn với
      `TextInput` bên cạnh. Đã thêm `hintText` + `hintStyle`. **Ảnh hưởng 53 chỗ gọi ở 14 màn** —
      user đã duyệt sửa toàn app.
- [x] Đổi hint 6 select của màn này: "Công ty" → "Chọn công ty"… (hint giờ hiện thật, để nguyên sẽ
      lặp y hệt nhãn phía trên; "Chọn X" khớp convention `ds_khoa_hoc`).
- [x] `flutter analyze` sạch (No issues found)
- [x] Verify trên iOS: placeholder hiện đúng, cùng màu/cỡ với TextInput

### Còn lại
- [ ] Verify các trường còn lại (8 ô text, Trạng thái, Nhân viên, Từ/Đến ngày) + cascade + Làm mới trên iOS
- [ ] Nhánh ẩn theo quyền (cần tài khoản quyền thấp; tài khoản test là admin đủ quyền)
- [ ] Dọn máy: xoá `Xcode.app` 15.4 + `Xcode-16.4.0.app`, gỡ tap `facebook/fb` + `cliclick`,
      thu hồi quyền Accessibility của VS Code

### Checkpoint — 2026-08-06 (VERIFY ĐẦY ĐỦ trên develop)
Đã build lại CẢ HAI bằng code sạch (sau khi áp review theo skill `flutter-review`) rồi chạy trọn kịch bản.

ANDROID — verify bằng log request thật, từng bước:
| Bước | Request | KQ |
|---|---|---|
| Mở màn | `?page=1&limit=10&type=all&company_id=1` | ✅ mặc định công ty user, không param rỗng |
| Cascade PB→BP | chọn PHÒNG QUẢN TRỊ THÔNG TIN → Bộ phận rút còn đúng 2 mục thuộc phòng | ✅ |
| Áp dụng PB+BP | `...&company_id=1&department_id=36&part_id=25` | ✅ |
| Từ ngày | picker 3 cột Năm/Tháng/Ngày, KHÔNG có giờ | ✅ |
| Áp dụng ngày | `...&department_id=36&part_id=25&from_time=2026-08-06` | ✅ đúng `yyyy-MM-dd` |
| Làm mới | `?page=1&limit=10&type=all&company_id=1` | ✅ xoá hết, GIỮ Công ty, badge tắt, list đầy lại |
| Placeholder | 14 trường đều có placeholder ("Chọn phòng ban", "Số hợp đồng"…) | ✅ |
| activeCount | "1 bộ lọc đang áp dụng" → "2 bộ lọc đang áp dụng" đúng số | ✅ |

iOS — verify được: build+chạy, mở màn (`company_id=1`), drawer render đủ trường, placeholder đúng,
nút lọc mở drawer bình thường (trước đó tôi tưởng hỏng — thực ra do bấm 2 lần: mở rồi đóng ngay).
CHƯA verify trên iOS: mở dropdown option (click tổng hợp không bung được popup DropdownSearch trên
Simulator; Android thì bình thường) ⇒ apply/cascade/Làm mới trên iOS suy từ Android chứ chưa chứng minh trực tiếp.

Sửa theo `flutter-review` (skill của project):
- `Scaffold` → `CommonScaffold` (nó CÓ hỗ trợ `endDrawer` + `scaffoldKey`, tôi đã nhầm)
- `Text` → `CommonText` trong option dropdown
- **Lỗi thật**: `SelectInput` chỉ dùng `value` + `itemAsString`, KHÔNG render `child` của DropdownMenuItem
  ⇒ fallback `name→text` trong `_itemsOf` vô tác dụng. Đã tách `_labelOf` + truyền `itemAsString` cho cả 5 select.

Còn lại: nhánh ẩn theo quyền (cần tài khoản quyền thấp), dọn máy (Xcode 15.4 + 16.4 thừa,
tap facebook/fb, cliclick, quyền Accessibility của VS Code).
