# Chấm công theo phiếu công tác — chọn phương tiện (BE + App mobile) — Plan

> Người phụ trách: @khoipv · Bắt đầu: 12/11/2026
> Nối tiếp: [Danh mục phương tiện](../danh-muc-phuong-tien/plan.md)
> Code: BE `hrm-thanhan-api` (Modules/Timesheet) · App `C:\dev\TPE_APP` nhánh `thanhan` (Flutter)

## Mục tiêu
- Lượt **chấm vào** (lượt đầu trong ngày) theo **phiếu công tác** → nhân viên bắt buộc chọn phương tiện: xe do phòng ban mình phụ trách (đang dùng) hoặc "Không đi xe công ty".
- Lưu vào `timesheets` và hiện "Phương tiện sử dụng" ở chi tiết phiếu công tác.
- Danh mục phương tiện: chỉ xóa được xe chưa được chọn ở lượt chấm nào.

## Phase 0 — Dựng môi trường code app (máy @khoipv, 12/11/2026)
> Chỉ dùng trên máy local — các thay đổi cấu hình dưới đây KHÔNG commit/push.

- [x] Flutter qua FVM: SDK ở `C:\dev\TPE_APP\.fvm\flutter_sdk` (Flutter 3.41.7 stable). `fvm` không có trên PATH → gọi thẳng `C:\dev\TPE_APP\.fvm\flutter_sdk\bin\flutter.bat`
  - `.gitignore`: gom ignore FVM thành `.fvm/` (đưa xuống cuối file)
- [x] Máy ảo Android: AVD `Pixel_API_35` (system image android-35, x86_64)
  - Chạy bằng `emulator.exe -avd Pixel_API_35 -gpu host` — để mặc định `auto` sẽ chọn lavapipe (render bằng CPU) → ngốn CPU, app "isn't responding", Android tự khởi động lại
  - Cửa sổ máy ảo mở lệch lên trên màn hình (1536x824) → sau khi mở phải dời/đổi cỡ (SetWindowPos ~x=1150, y=5, 365x800)
- [x] `app/android/app/build.gradle`: chuyển `abiFilters` xuống `buildTypes` — release giữ `arm64-v8a`, debug thêm `x86_64` để cài được lên máy ảo trên PC
- [x] Backend local: `D:\laragon\www\dns\hrm-thanhan-api` (Laravel 8, nhánh `thanhan-dev`, DB `thanhan_stag_07052026` trên MySQL Laragon) — KHÔNG phải `D:\laragon\www\hrm\hrm-api`
  - ~~Chạy: `D:\laragon\bin\php\php-8.1.10-Win32-vs16-x64\php.exe artisan serve --host=0.0.0.0 --port=8001`~~ — **bỏ từ 13/11/2026**: `artisan serve` trên Windows chạy từng request một → màn Tổng quan (10–20 request song song) bị timeout 30s, app báo "Lỗi kết nối"
  - [x] (13/11/2026) Chạy bằng nginx Laragon + 4 worker PHP 8.1: file `D:\laragon\etc\nginx\sites-enabled\thanhan-api-8001.conf` (listen 8001, root `.../hrm-thanhan-api/public`, upstream `127.0.0.1:9101–9104`)
    - Mỗi lần khởi động lại máy phải bật lại worker (PowerShell): `$env:PHP_FCGI_MAX_REQUESTS='0'; 9101..9104 | % { Start-Process D:\laragon\bin\php\php-8.1.10-Win32-vs16-x64\php-cgi.exe -ArgumentList '-b',"127.0.0.1:$_" -WindowStyle Hidden }`
    - nginx Laragon phải đang chạy; nạp lại cấu hình: `nginx.exe -s reload` trong `D:\laragon\bin\nginx\nginx-1.22.0`
    - Kết quả: 10 request song song ~3.5s (trước xếp hàng > 30s)
  - Kiểm tra: POST `http://127.0.0.1:8001/api/v1/users/auth/login` → 422 "Bắt buộc phải nhập" là OK
- [x] Trỏ app vào BE local: `BuildConfig` đọc `--dart-define=API_DOMAIN=...` (không truyền thì dùng domain theo flavor như cũ); máy ảo gọi máy tính qua `10.0.2.2`
- [x] Lệnh chạy app Thành An (trong `app/`):
  `flutter.bat run --flavor thanhan --dart-define FLAVOR=thanhan --dart-define API_DOMAIN=http://10.0.2.2:8001/api/ -t lib/main.dart`
- [x] Hot reload thay vì build lại mỗi lần sửa: chạy `flutter run --machine` qua pipe (`tail -f cmd.txt | flutter.bat run --machine -d emulator-5554 ... > run.log`), gửi lệnh `app.restart` (`fullRestart:false` = hot reload, `true` = hot restart) vào `cmd.txt`
  - Chỉ build lại khi đổi native/pubspec hoặc app/máy ảo chết; sửa PHP ở BE thì app không cần làm gì
  - Máy ít RAM: build xong tắt Gradle/Kotlin daemon (~2GB)

## Phase 1 — BE (`hrm-thanhan-api/Modules/Timesheet`)
- [x] Migration `2026_11_12_100000_add_vehicle_to_timesheets_table`: `timesheets.vehicle_id` (nullable, index, không FK) + `no_company_vehicle` tinyint
- [x] `Timesheet`: fillable `vehicle_id`, `no_company_vehicle` + quan hệ `vehicle()` (withTrashed)
- [x] `Vehicle::isUsed()` → `Timesheet::where('vehicle_id', id)->exists()`
- [x] `TimekeeperService::isBusinessTripCheckIn()` (chưa có lượt chấm nào trong ngày của phiếu) + `vehiclesForEmployee()` (xe active thuộc phòng ban NV)
- [x] API `GET v1/timekeeper/vehicles` (`TimekeeperController::vehicles`)
- [x] Danh sách loại chấm công trả `require_vehicle` cho phiếu công tác
- [x] Lưu chấm công: `resolveVehicle()` — chỉ áp lượt chấm vào theo phiếu công tác; 422 khi chưa chọn / xe không hợp lệ hoặc đã khóa
- [x] `BusinessTripAssignDetailResource`: trả `vehicle_text` theo từng lượt trong `timesheet_info`
- [ ] Chạy migrate local + test API (chấm vào có/không xe, xe phòng khác, xe đã khóa, lượt chấm thứ 2 không bắt chọn)

## Phase 2 — App (`TPE_APP`, nhánh `thanhan`)
- [x] Model `TimekeeperVehicleData` (id, brand, license_plate, `displayName`) + build_runner
- [x] `TimesheetTypeData.requireVehicle` (`require_vehicle`, parse bool/0/1/"1")
- [x] API service `getTimekeeperVehicles()`; chấm công gửi `vehicle_id` / `no_company_vehicle`
- [x] `UserRepository` + impl: thêm tham số `vehicleId`, `noCompanyVehicle`
- [x] `CheckInOutBloc`: event `ChonPhuongTien`, chọn loại chấm có `requireVehicle` → tải danh sách xe; reset khi đổi loại; chặn chấm khi chưa chọn ("Chưa chọn phương tiện sử dụng")
- [x] `CheckInOutPage`: UI chọn phương tiện (danh sách xe + "Không đi xe công ty")
- [x] `RemoteDanhSachCongTacData.vehicleUsages` (parse `timesheet_info`) + `PhieuCongTacDetailPage` hiện "Phương tiện sử dụng"
- [x] `BuildConfig`: `--dart-define=API_DOMAIN=...` để chạy với BE local (chỉ local, không commit)
- [ ] Chạy app trên emulator với BE local, test luồng chấm vào / chấm ra / chi tiết phiếu công tác

## Phase 2b — Web: hiện "Phương tiện sử dụng" ở bảng Lịch sử chấm công (12/11/2026)
- [x] BE: chuyển `vehicleText()` thành `Timesheet::vehicleText(array)` (static, dùng chung 3 resource)
- [x] BE `BusinessTripAssignListResource` (API danh sách phiếu CT — popup chọn phiếu ở màn đề nghị TT công tác phí): join `vehicles`, trả `vehicle_text`
- [x] BE `DetailRequestPaymentWorkingFeeResource` (chi tiết/sửa phiếu đề nghị TT công tác phí): join `vehicles`, trả `vehicle_text` (chỉ phiếu công tác, không làm ngoài giờ)
- [x] FE chi tiết phiếu công tác `business_trip_assigns/add/_id.vue` + `_id/approve.vue`: thêm cột "Phương tiện sử dụng"
- [x] FE phiếu đề nghị TT công tác phí `RequestPaymentWorkingFeeForm.vue`: thêm cột "Phương tiện sử dụng"
- [x] ~~User test trên web~~ → user đổi yêu cầu (Phase 2c)

## Phase 2c — Web: chuyển "Phương tiện sử dụng" lên phần thông tin phiếu (12/11/2026)
> User: không để ở bảng Lịch sử chấm công, cho lên phần thông tin phiếu công tác.
- [x] Helper FE `utils/businessTripVehicle.js` → `vehicleUsageText(timesheet_info)`: gom `vehicle_text` các lượt chấm (bỏ trống, bỏ trùng), nối ", " (timesheet_info có thể là mảng hoặc object)
- [x] Bỏ cột "Phương tiện sử dụng" ở 3 bảng Lịch sử chấm công (`add/_id.vue`, `_id/approve.vue`, `RequestPaymentWorkingFeeForm.vue`)
- [x] Chi tiết phiếu công tác (`add/_id.vue`, `_id/approve.vue`): ô chỉ xem "Phương tiện sử dụng" cạnh "Ngày giờ xuất phát", hiện khi phiếu đã duyệt (cùng điều kiện bảng Lịch sử chấm công)
- [x] Phiếu đề nghị TT công tác phí: ô "Phương tiện sử dụng" trong khối thông tin từng phiếu công tác (sau "Đến ngày"), chỉ phiếu PCT
- [x] Fix: phiếu 5913 không hiện phương tiện ở `add/_id.vue` — `timesheet_info` chỉ khai báo trong `form` nhưng mounted gán `this.timesheet_info` (cấp ngoài, không reactive) → computed tính lúc render đầu (form.status null → ô đã hiện) ra rỗng rồi cache mãi. Khai báo `timesheet_info: []` ở cấp ngoài data(). `approve.vue` đã khai báo đúng, không bị
- [ ] User test trên web

## Phase 3 — Bàn giao
- [ ] User test tay
- [x] Commit + push (12/11/2026, theo yêu cầu user): API `master` 41bb1dfa · Client `master` c30a07d1 · App `thanhan` đã có sẵn trên remote (4ed1a4a feature + 36e3d09 cấu hình chạy máy ảo/API local)
- [ ] Môi trường khác: `php artisan module:migrate Timesheet`

## Nhật ký
### 12/11/2026
- Dựng môi trường code app: FVM Flutter 3.41.7, máy ảo Pixel_API_35 (`-gpu host`), sửa `abiFilters` cho debug x86_64, chạy BE `hrm-thanhan-api` ở cổng 8001, thêm override `API_DOMAIN`, quy trình hot reload qua pipe
- Code BE: lưu phương tiện khi chấm vào theo phiếu công tác, API danh sách xe, `require_vehicle`, `vehicle_text` ở chi tiết phiếu
- Code App: chọn phương tiện ở màn Chấm công, hiện "Phương tiện sử dụng" ở chi tiết phiếu công tác
- Web (Phase 2c): user đổi ý — bỏ cột ở bảng Lịch sử chấm công, chuyển thành ô "Phương tiện sử dụng" ở phần thông tin phiếu (gom xe các lượt chấm, bỏ trùng). BE giữ `vehicle_text` từng lượt làm nguồn dữ liệu. Helper chạy thử OK với timesheet_info dạng mảng + object
- Web (Phase 2b): thêm cột "Phương tiện sử dụng" vào bảng Lịch sử chấm công ở chi tiết phiếu công tác + phiếu đề nghị TT công tác phí. Kiểm bằng tinker trên DB local: lượt 407809 (phiếu CT 5911) ra "29A-00435 (Lexus)" ở cả Detail / List / DetailRequestPaymentWorkingFee resource

### 13/11/2026
- BE local chuyển từ `artisan serve` sang nginx + 4 php-cgi 8.1 (cổng 8001 giữ nguyên) để hết "Lỗi kết nối" ở Tổng quan — chi tiết Phase 0
- Fix app: sheet chọn ca lần đầu trống → plan riêng [fix-app-cham-cong-chon-ca-lan-dau](../fix-app-cham-cong-chon-ca-lan-dau/plan.md)

### Checkpoint — 12/11/2026
Vừa hoàn thành: dựng môi trường + code BE + App (chưa commit)
Đang làm dở: test API + test trên app
Bước tiếp theo: migrate local → chạy app với `API_DOMAIN=http://10.0.2.2:8001/api/` → test luồng chọn phương tiện
Blocked:
