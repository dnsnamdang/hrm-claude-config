# Plan — Fix màn Danh sách Phiếu nhập kết quả (app + BE)

Repo: `hrm-api` nhánh **`tpe`** · `TPE_APP` nhánh **`develop`**. Nguồn chuẩn nghiệp vụ: ERP (`TanPhatDev`).

## Nguyên nhân đã trace được

**Bug 1 — trạng thái không khớp ERP**
`WrImportResultListResource.php:33` dùng `TpWrAssignTask::getStatus()` (vòng đời *Phiếu giao việc*:
Chờ giao / Đang giao / Đang đề nghị thanh toán / **Đã thanh toán**) để hiển thị cho *Phiếu nhập kết quả*.
`TpWrImportResult` đã có sẵn `STATUSES` đúng nhưng **thiếu trạng thái thứ 6 `KHONG_DUYET`** so với ERP.
Ngoài ra `TpWrImportResultService::searchByFilter` lọc trên `wr_assign_tasks.status` — KHÁC cột đang hiển thị
(`wr_import_results.status`). Hiển thị một cột, lọc một cột.

**Bug 2 — sửa/xoá sau khi duyệt**
App hiện nút "Chỉnh sửa"/"Xoá" vô điều kiện; list resource không trả cờ quyền nào.
ERP có rule: `canEdit = created_by == me && (DANG_TAO || KHONG_DUYET)`.
Phát hiện thêm: `_onDeletePhieu` trong bloc **rỗng**, hrm-api **không có route DELETE** → nút Xoá là nút chết.

**Bug 3 — thiếu bộ lọc**: app không có bộ lọc; ERP có 7 trường.

## Quyết định đã chốt với user
- Trạng thái + rule sửa/xoá: **lấy y nguyên ERP**; BE trả cờ `can_edit`/`can_delete`, FE chỉ hiển thị theo cờ
  (không hard-code điều kiện ở FE).
- Bộ lọc: **đủ 7 trường như ERP**.
- Nút Xoá: user xác nhận "chỉ thấy nút hiện, bấm không ăn" → không làm chức năng xoá mới.

## Bẫy kỹ thuật
`wr_import_results` nằm ở **DB ERP** (`mysql2`), `created_by` là id `employees` **bên ERP**, KHÔNG phải id HRM.
Khoá quy đổi dùng chung là `employee_info_id` (ERP `storeApp` map bằng chính khoá này).
⇒ tính `can_edit` phải resolve qua `TpEmployee::where('employee_info_id', auth()->user()->employee_info_id)`.

## Phase 1 — BE (hrm-api, nhánh `tpe`)

- [x] `TpWrImportResult`: thêm `const KHONG_DUYET = 6` + entry STATUSES ('Không duyệt kết quả', danger), đúng thứ tự ERP
- [x] `TpWrImportResult`: thêm helper `canEditBy($erpEmployeeId)` theo rule ERP
- [x] `WrImportResultListResource`: đổi `TpWrAssignTask::getStatus` → `TpWrImportResult::getStatus`
- [x] `WrImportResultListResource`: trả thêm `can_edit`, `can_delete`
- [x] `TpWrImportResultService::searchByFilter`: sửa lọc status sang `wr_import_results.status`
- [x] `searchByFilter`: bổ sung param ERP — `customer_id`, `created_by`, `approved_by`, `startDate`, `endDate`
- [x] ~~Trả kèm danh sách trạng thái cho FE~~ → CHỐT: FE hard-code 6 trạng thái theo ERP
      (khớp cách app đã làm ở các màn khác; danh sách này ổn định, không đổi theo công ty)

## Phase 2 — App (TPE_APP, nhánh `develop`)

- [x] Model `PhieuKetQuaData` + entity `DanhSachKetQua`: map `can_edit`, `can_delete`
- [x] Màn danh sách: ẩn "Chỉnh sửa"/"Xoá" theo cờ BE
- [x] Xử lý nút Xoá chết (chờ user chốt: ẩn hẳn hay giữ)
- [x] Thêm `FilterView` 7 trường theo ERP (tái dùng pattern màn Phiếu giao công tác)
- [x] API service + repository + usecase: truyền tham số lọc
- [x] `build_runner` + `flutter analyze`

## Phase 3 — Kiểm chứng
- [x] Đối chiếu nhãn trạng thái app ↔ ERP
- [x] Phiếu đã duyệt: không còn nút Sửa/Xoá
- [x] Lọc từng trường, đối chiếu log request

### Checkpoint — 2026-08-06 (code xong, chưa chạy thử)
BE (hrm-api, nhánh `tpe`) — 3 file, `php -l` sạch:
- `TpWrImportResult`: +`KHONG_DUYET=6` (khớp đủ 6 trạng thái ERP) + `canEditBy($erpEmployeeId)`
- `WrImportResultListResource`: `TpWrAssignTask::getStatus` → `TpWrImportResult::getStatus`; +`can_edit`
  (CỐ Ý không trả `can_delete` — hệ thống chưa có đường xoá, trả cờ sẽ ngụ ý khả năng không tồn tại)
- `TpWrImportResultService`: lọc status đổi sang `wr_import_results.status`;
  +`customer` (LIKE tên/mã), `customer_id`, `created_by`, `approved_by`, `startDate`, `endDate`

App (TPE_APP, nhánh `develop`) — `build_runner` 455 output, `flutter analyze` No issues:
- model/entity/mapper: +`can_edit` (entity mặc định `false` — fail-closed)
- màn danh sách: ẩn CẢ cụm menu thao tác khi `!canEdit`; GỠ HẲN nút Xoá (30 dòng) + event `DeletePhieu`
  chết + handler rỗng
- bloc: 7 field lọc, `FilterApplied`, `activeFilterCount`, 6 trạng thái copy từ ERP
- FilterView 7 trường + badge

Chủ ý làm KHÁC ERP (đã báo user):
- Khách hàng dùng ô nhập chữ (BE lọc LIKE `customer_name`/`customer_code`) thay vì dropdown `customer_id`
  — danh sách khách hàng quá lớn cho dropdown mobile, project đã có tiền lệ query không LIMIT gây fatal.
- `created_by`/`approved_by` app gửi `employee_info_id`, BE quy đổi qua `TpEmployee` (bảng `employees`
  BÊN ERP). Trong service có sẵn đoạn comment so thẳng id HRM với cột này — bỏ comment ra dùng là lọc sai âm thầm.

CHƯA làm: build + chạy thử trên máy ảo; chưa đối chiếu nhãn trạng thái thực tế với ERP.

### Checkpoint — 2026-08-06 (ĐÃ VERIFY END-TO-END trên BE local + app)
Cách test: `php -S 127.0.0.1:8000` đang chạy CHÍNH checkout `HRM/hrm-api` nhánh `tpe`; DB local
(`hrm_prod_local` + `dev_erp`). App build flavor `erp` với `build_config.dart` sửa TẠM sang
`http://10.0.2.2:8000/api/` (đường máy ảo Android → host), test xong ĐÃ TRẢ LẠI nguyên trạng.

Bảng trước–sau (nguồn: `TpWrAssignTask::STATUSES` cũ vs `TpWrImportResult::STATUSES` mới):
| status | Nhãn CŨ (sai) | Nhãn MỚI | Số phiếu trong DB |
|---|---|---|---|
| 1 | Đang giao | Đang tạo | 4 |
| 2 | Đã nhập kết quả | Chờ duyệt kết quả | 214 |
| 3 | Đã duyệt kết quả | Đã duyệt kết quả | 6.967 |
| 4 | Chờ BKS duyệt kết quả | Chờ BKS duyệt kết quả | 3 |
| 5 | Đang đề nghị thanh toán | Đang duyệt kết quả | 3 |
| 6 | **Đã thanh toán** | **Không duyệt kết quả** | 58 |

Kiểm chứng API (curl trực tiếp, đối chiếu count DB):
- list: status trả "Đã duyệt kết quả"/"Chờ duyệt kết quả", hết "Đã thanh toán"
- `?status=6` → 58 dòng toàn "Không duyệt kết quả" (khớp count DB)
- `?status=1` → 4 dòng "Đang tạo" (khớp)
- `?created_by=6` (employee_info_id) → 1 dòng (khớp) ⇒ quy đổi employee_info_id→ERP id chạy đúng
- `?startDate/endDate` → 154 dòng tháng 8
- `can_edit` = false toàn bộ: ĐÚNG nghiệp vụ (user sở hữu 1 phiếu, 0 phiếu ở status 1/6),
  KHÔNG phải do quy đổi id null — đã xác minh `employee_info_id=6` → ERP employee `13`

Kiểm chứng app: bộ lọc 7 trường hiện đủ + placeholder; dropdown trạng thái đúng 6 mục ERP
(không còn "Đã thanh toán"); lọc `status=6` → list toàn "Không duyệt kết quả"; badge cam đúng;
KHÔNG dòng nào còn nút ⋯ (can_edit=false ẩn menu).

CHƯA chứng minh trực tiếp: nhánh `can_edit = true` — tài khoản test không sở hữu phiếu nào ở
trạng thái Đang tạo/Không duyệt, và tôi không sửa dữ liệu thật để tạo tình huống.

### Checkpoint — 2026-08-06 (sửa UI badge trạng thái)
User báo "Không duyệt kết quả" bị xuống dòng. Vào xem thì badge có 2 lỗi:
- `width: 115` CỨNG → nhãn dài ("Không duyệt kết quả", "Chờ BKS duyệt kết quả") bị ngắt 2 dòng
- `color: Color(0xFF489760)` CỨNG → badge LUÔN màu xanh lá bất kể trạng thái;
  "Không duyệt kết quả" (từ chối) hiện màu thành công — sai nghĩa nặng hơn cả việc xuống dòng

Sửa:
- Bỏ width cứng, badge ôm nội dung (padding 10x6), `maxLines: 1` + `overflow: ellipsis`
- Lấy `type` (danger/warning/success) BE đã trả sẵn trong `ApiStatusData` (mapper trước đây vứt đi):
  entity `DanhSachKetQua` thêm `statusType` + getter `statusColor`/`statusTextColor`,
  dùng ĐÚNG bảng màu sẵn có của app (xem `Assignment.statusColor`): nền pastel + chữ cùng tông
  · success D4FCE5/489760 · warning FFEFC3/CEA03C · danger FEEFED/E95151

Verify trên emulator (flavor `erp` trỏ BE local, đã trả lại `build_config.dart` sau khi test):
lọc status=6 → badge 1 dòng, nền đỏ nhạt chữ đỏ, không tràn không ngắt dòng.
`build_runner` 448 output, `flutter analyze` No issues.

### Checkpoint — 2026-08-06 (TẠM DỪNG, mai làm tiếp)
Vừa hoàn thành: cả 3 lỗi + sửa UI badge, verify end-to-end trên BE local.
Trạng thái repo: CHƯA COMMIT — `hrm-api` nhánh `tpe` 3 file, `TPE_APP` nhánh `develop`.
Máy đã dọn: `build_config.dart` trả về `dev-hrm.eteksofts.com`; app trên emulator chạy lại
flavor `production` (đã xác nhận log `Flavor.production`), không còn trỏ API local.

Bước tiếp theo khi quay lại:
1. User review code 2 repo → commit (tôi không tự commit theo quy ước dự án)
2. Chứng minh nhánh `can_edit = true`: cần tài khoản sở hữu phiếu ở trạng thái Đang tạo/Không duyệt
3. Deploy: BE TRƯỚC, app SAU (app mới + BE cũ ⇒ mất nút Sửa mọi dòng)
4. Việc còn treo từ feature trước (app-loc-phieu-giao-cong-tac): nhánh ẩn ô lọc theo quyền — user tự test
5. Dọn máy còn lại: `sudo xcode-select -s /Applications/Xcode-26.3.0.app/Contents/Developer &&
   sudo rm -rf /Applications/Xcode.app` (Xcode 15.4 còn 5,7GB, xcode-select vẫn trỏ vào nó)

### Checkpoint — 2026-08-07 (đóng nốt việc tồn)
1. ĐÃ chứng minh nhánh `can_edit = true` — thứ hôm qua còn treo. Không cần tài khoản khác, kiểm thẳng
   `canEditBy()` trên bản ghi thật qua tinker, đủ 4 nhánh:
   - `TPE.PNKQ.2025000083` (status=1, created_by=347): canEditBy(347)=**true**
   - canEditBy(99999)=false · canEditBy(null)=false (fail-closed)
   - `TPE.PNKQ.2025000001` (status=3 đã duyệt), canEditBy(chính người tạo)=**false** ← đúng bug đã fix
2. Chạy `flutter-review` (skill dự án) cho phần code màn KQ:
   - Sửa: `Text('Chỉnh sửa')` → `CommonText` (nằm trong code đã đụng)
   - CHẤP NHẬN có lý do: `width/height: 8` của chấm badge và padding badge để px cứng thay vì `Dimen` —
     copy đúng convention 4 màn lọc sẵn có; đổi riêng màn này sẽ lệch với phần còn lại
   - Cân nhắc chưa làm: `transformer: throttleTime` cho `FilterApplied` chống double-tap nút Áp dụng
     (các màn khác cũng dùng `log()`, chưa màn nào throttle → để nguyên cho đồng bộ)
   - `flutter analyze`: No issues found

CÒN LẠI (đều là việc của user): review + commit 2 repo · deploy BE trước app ·
dọn Xcode 15.4 bằng lệnh sudo · test nhánh ẩn ô lọc theo quyền của feature trước.

### Checkpoint — 2026-08-07 (đã test CẢ Android + iOS với code mới nhất)
Trước đó màn này CHƯA từng chạy trên iOS. Nay đã test cả hai, cùng trỏ API local nên đối chiếu được:
- Cùng dữ liệu (`TPE.PNKQ.2026007378/7377/7376`), hai bên hiển thị giống hệt
- Badge: 1 dòng, ôm nội dung, màu đúng theo `type` (xanh "Đã duyệt kết quả" / vàng "Chờ duyệt kết quả")
- Không dòng nào còn nút ⋯ (can_edit=false)

QUY TRÌNH MỚI — hot reload thay vì build lại (tiết kiệm rất nhiều thời gian):
Chạy `flutter run ... < /tmp/flutter_run.fifo` rồi `printf 'r\n' > fifo` để hot reload, `R` để hot restart.
Gỡ code tạm + đổi URL chỉ mất ~4s thay vì 2 lượt build.
2 bẫy đã vấp:
- Mở named pipe để ĐỌC sẽ TREO tới khi có tiến trình giữ đầu GHI
  → phải chạy kèm `nohup sh -c 'sleep 100000 > /tmp/flutter_run.fifo' &`
- `cliclick t:` KHÔNG gõ được chữ ("cannot handle your keyboard layout")
  → dùng `osascript -e 'tell application "System Events" to keystroke "..."'`
- Cả iOS Simulator lẫn Android emulator dùng chung `http://127.0.0.1:8000` được,
  nhờ `adb reverse tcp:8000 tcp:8000` (phải chạy lại mỗi lần emulator khởi động lại)
- Log `flutter run` trên iOS gộp cả app khác đang chạy nền → thấy URL production dễ báo động nhầm;
  xác minh bằng dòng `flutter: Flavor.xxx` + bundle id

Môi trường: `xcode-select` ĐÃ trỏ Xcode 26.3 (user tự chạy). `/Applications/Xcode.app` (15.4) VẪN CÒN
5,7GB — lệnh `sudo A && sudo B` hỏi mật khẩu 2 lần nên vế `rm` không chạy; cần `sudo rm -rf` riêng.
`cliclick` giữ lại theo ý user (kèm quyền Accessibility cho VS Code).

## Phase 3 — Redmine 10959 ý 2.2 + 3 lỗi màn tạo/sửa Phiếu nhập KQ

### FE (TPE_APP, nhánh develop)
- [x] 2.2 Tốc độ load: bỏ `await _loadFilterOptions` khỏi lúc vào màn, chuyển sang sự kiện `FilterOpened` (bắn khi bấm nút lọc) — áp cho cả `DsPhieuNhapKetQuaCongViecBloc` lẫn `DsPhieuGiaoCongTacBloc`
- [x] Request danh sách đầu tiên của Phiếu giao công tác lấy công ty mặc định từ `AppPreferences` thay vì chờ `user-profile`
- [x] Lỗi 1 — hộp thoại xác nhận đổi serial nhảy theo từng ký tự: `bao_hanh_tab_view.dart` + `bao_duong_tab_view.dart` gọi `showWarning` ngay trong `TextField.onChanged` → chuyển sang `Focus.onFocusChange` (chỉ hỏi khi nhập xong)
- [x] Lỗi 1b — 2 ô serial đó chỉ cảnh báo mà KHÔNG lưu giá trị → bổ sung `UpdateGroup1Serial`
- [x] Lỗi 1c — chốt chống lặp hỏng: `putIfAbsent(type, () => {index:true})` không ghi được index thứ 2, và `finally` lại xoá chốt ngay → đổi sang map lưu giá trị serial đã hỏi, bỏ `finally`
- [x] Lỗi 2 — ảnh đính kèm bấm không xem được: `AppLocalFileView` chưa hề có `onTap` → thêm xem full màn hình bằng `PhotoView` (dùng chung cho ảnh server và file vừa chọn)
- [x] Lỗi 3 — SL bàn giao sai: `api_nhap_ket_qua_data.dart::extendedAssembly` tách dòng vô điều kiện theo `qty` và nhân bản nguyên object (mỗi dòng vẫn SL=N) → chỉ tách khi `is_serial == true`, mỗi dòng `copyWith(qtyValue: 1)`
- [x] Bổ sung field `is_serial` vào `ApiProductRepairData` (ERP đã trả sẵn, app chưa đọc)
- [ ] Test thực tế trên Android + iOS (chưa chạy)

### Ghi chú điều tra
- Số đo tốc độ (dev): danh sách 0,13s/3KB · `user-profile` 0,39s/950KB · chi tiết phiếu 1,5–2,8s
- Chi tiết phiếu chậm do `TpWrImportResultService::show()` proxy HTTP sang ERP (`ERP_URL`) — nút thắt CÓ SẴN, chưa động vào
- Trang tạo/sửa đang chạy là `nhap_ket_qua_cong_viec_main_page.dart`; `nhap_ket_qua_cong_viec_page.dart` là code chết (không route nào trỏ tới)
- ERP chỉ gắn cờ `is_serial` (theo `Config.serial_product_types`) chứ KHÔNG tách dòng ở `getForDataImportResult` — việc tách là của client

### Lỗi "Lưu và Gửi duyệt" — vì sao vá rồi vẫn nổ
- [x] Nguyên nhân 1: app đang chạy BUILD CŨ. Stack trỏ `user_api_service.dart:1325:26` trong khi dòng 1325 của source hiện tại chỉ là `}` → lần hot reload cuối diễn ra TRƯỚC khi file được sửa
- [x] Nguyên nhân 2 (nặng hơn, do chính bản vá gây ra): helper `_setFirstSerial` bị chèn CHEN GIỮA `@LazySingleton()` và `class UserApiService` → annotation gắn nhầm vào hàm, `build_runner` bỏ luôn dòng `gh.lazySingleton<UserApiService>()` trong `di.config.dart` → app chết ngay khi khởi động ("UserApiService is not registered inside GetIt"). Đã chuyển annotation về đúng trên class
- [x] Vá tận gốc: thêm `toJson: _serialsToJson` cho field `serials` trong `ApiProductRepairData`. Trước đây chỉ khai `fromJson:` nên json_serializable ghi thẳng `instance.serials` — `toJson()` trả về `EqualUnmodifiableListView<SerialData>` nằm lẫn trong Map JSON, nơi gọi tưởng JSON thuần rồi ghi `list[0] = {...}` là nổ
- [x] Đã chạy lại phiên iOS bằng build mới, khởi động sạch (không còn lỗi GetIt)
- [ ] User đăng nhập và bấm lại "Lưu và Gửi duyệt" để xác nhận

BÀI HỌC: chèn code vào file phải nhìn xem có annotation nào đang treo ngay trên vị trí đó không.
Dart cho annotation đứng cách khai báo bởi comment, nhưng KHÔNG cho cách bởi một khai báo khác.

### Chuyển lỗi 3 (SL bàn giao) từ FE sang BE — theo yêu cầu "sửa BE dễ hơn thì sửa BE"
- [x] BE: `TpWrAssignTaskService::show()` (endpoint `wr_assign_tasks/{id}` — proxy thuần sang ERP, CHỈ app dùng) thêm `splitRowsRequiringSerial()`: thiết bị `is_serial` + SL>1 → tách N dòng SL=1; còn lại giữ nguyên. Không sửa `apiShow` bên ERP vì ERP web dùng chung
- [x] `filter_var(..., FILTER_VALIDATE_BOOLEAN)` để nuốt được cả `true` lẫn `1`
- [x] FE: gỡ field `is_serial` khỏi `ApiProductRepairData`, `extendedAssembly` trả thẳng list của BE (không tự nhân dòng)
- [x] Đã thử logic PHP với 5 case: true/1/0/SL=1/thiếu field — đúng hết

BẪY ĐÃ VẤP (tự gây, mất 1 vòng build): khai `@JsonKey(name:'is_serial') bool? isSerial` trong khi BE trả `0`
→ `json[...] as bool?` ném TypeError → HỎNG TOÀN BỘ parse thiết bị → màn tạo/sửa trắng "Không có dữ liệu để hiển thị".
Model của dự án này luôn phải parse phòng thủ (`_intFromJson`, `_doubleFromJson`...), KHÔNG khai kiểu trần.

### Môi trường test local (07/08/2026)
- App iOS trỏ `http://127.0.0.1:8000/api/` (flavor erp — `build_config.dart` ĐANG SỬA TẠM, phải trả lại trước khi commit)
- Đăng nhập: `tientt.cnsg@tanphat.com` / `123456@` — mật khẩu do tôi đặt trên DB LOCAL để test.
  Hash cũ + lệnh trả lại nằm ở scratchpad `restore_password.sql`
- Đã sửa 1 dòng DB LOCAL để tái hiện: `wr_assign_task_assembles` của task 14881, product 44973 → qty=2
  (lệnh trả về qty=1 cũng nằm trong `restore_password.sql`)
- Kiểm chứng BE qua HTTP thật: `GET /api/v1/assign/wr_assign_tasks/14881` trả 3 dòng,
  product 44973 thành 2 dòng qty=1, product 38204 (không serial) giữ 1 dòng
- Bẫy khi lái UI Simulator bằng cliclick: cửa sổ ở (232,38), VÙNG MÀN HÌNH thiết bị ở (261,120) size 379x821.
  Quy đổi: screen_x = 261 + px*0.3215 ; screen_y = 120 + py*0.3212 (ảnh chụp 1179x2556).
  Phải `activate` Simulator trước khi gõ, và TẮT bộ gõ tiếng Việt (Ctrl+Space) nếu không "tientt" thành "tiếng".

### Lỗi phát sinh: trạng thái "Unknown" ở Danh sách phiếu giao công tác
- [x] `domain/lib/src/entity/giao_cong_tac.dart::statusText` chỉ ánh xạ 6/11 trạng thái → 4, 8, 9, 10, 11 đều hiện "Unknown". Bổ sung đủ 11, copy nguyên nhãn của web `pages/assign/assign_business/index.vue::getStatusText`; fallback đổi "Unknown" → "Không rõ" cho khớp web
- [x] `statusColor`/`statusTextColor`: giữ NGUYÊN màu các trạng thái vốn có (0,1,2,3,5), chỉ thêm màu cho 4/7/8/9/10/11 vì trước đây chúng rơi vào `default` nên hiện màu đỏ (đọc thành "bị từ chối")
- Ảnh hưởng thực tế trên DB local: status 11 có 860 phiếu, 9 có 451, 4 có 100, 8 và 10 mỗi loại 1 → 1.413 phiếu đang hiện sai

### Lỗi 2 (ảnh đính kèm) — hoá ra có HAI nguyên nhân, lần đầu mới sửa được một
- [x] Nguyên nhân 1 (đã sửa trước): `AppLocalFileView` không hề có `onTap` → thêm xem full màn hình bằng `PhotoView`
- [x] Nguyên nhân 2 (thật sự làm "không view được"): ảnh KHÔNG TẢI ĐƯỢC.
      BE trả đường dẫn tương đối `/uploads/wrImportResult/...` (thuộc host ERP) rồi để APP TỰ ĐOÁN host
      bằng cách thay đuôi `.eteksofts.com` → `.dnsmedia.vn`. Trên production thành `hrm.dnsmedia.vn`
      — host KHÔNG TỒN TẠI (curl trả 000, không phân giải) → mọi ảnh server đều hỏng.
      Dev may mắn đúng vì có case riêng `dev-hrm` → `dev-erp.dnsmedia.vn`.
- [x] BE: `TpWrImportResultService::show()` ghép sẵn URL đầy đủ cho `galleries_construction`/`galleries_handover`
      qua `toAbsoluteErpUrl()`, dùng `ERP_PUBLIC_URL` (fallback `ERP_URL`). App không phải đoán nữa
- [x] FE: giữ nhánh đoán host làm dự phòng cho BE bản cũ, nhưng sửa quy tắc — đổi `hrm.` đầu tên miền
      thành `erp.` và GIỮ NGUYÊN đuôi (`hrm.eteksofts.com` → `erp.eteksofts.com`, đã kiểm tra host này sống)
- [ ] CẦN OPS XÁC NHẬN: `ERP_URL` trên production có phải địa chỉ công khai không. Nếu là địa chỉ nội bộ
      thì phải set thêm `ERP_PUBLIC_URL` = host ERP công khai, nếu không app vẫn không tải được ảnh

### Lỗi 3 — kiểm tra lại sau khi user hỏi "chắc chắn chưa": THIẾU 1 CỘT
- [x] Bản tách dòng đầu chỉ hạ `qty`, BỎ SÓT `delivery_qty` — mà `delivery_qty` MỚI là cột
      "SL bàn giao" hiển thị bên ERP. Tách xong ERP vẫn hiện SL=2, đúng triệu chứng phiếu
      tpe.pnkq.2026000440. Trên DB dev có 1.550 dòng `wr_assign_task_assembles` có delivery_qty > 1
- [x] `splitRowsRequiringSerial()` nay hạ cả `delivery_qty` về 1, chỉ khi cột đó có giá trị
      (không biến NULL thành 1). Đã thử với dòng 19058 set delivery_qty=2 → API trả 2 dòng qty=1/delivery_qty=1
- [x] Đã kiểm luồng LƯU: `assemblyWithSerials` = `state.data.extendedAssembly` (nay là list BE trả),
      payload `Map.from(e.toJson())` giữ nguyên qty/delivery_qty → gửi lên 2 dòng SL=1, không còn nhân đôi
- [ ] Phiếu tpe.pnkq.2026000440 ĐÃ LƯU DỮ LIỆU SAI TỪ TRƯỚC — bản vá không tự sửa dữ liệu cũ,
      phải xoá/tạo lại phiếu hoặc sửa tay `wr_import_result_products`

### Lỗi "Lưu và Gửi duyệt" — đã chốt bằng test hồi quy
- [x] Thêm `test/serials_payload_test.dart` (3 case): toJson trả JSON thuần / ghi đè serial đầu không ném lỗi / serials rỗng-null an toàn
- [x] ĐÃ CHỨNG MINH test bắt được lỗi: gỡ `toJson: _serialsToJson` ra → test ĐỎ đúng kiểu lỗi cũ
      (`_SerialDataa is not a subtype of Map`); gắn lại → XANH 3/3
- [x] Quét toàn bộ lib: không còn chỗ nào ghi thẳng vào list `serials` theo chỉ số

### Lỗi 4: mở cả 2 nhóm ảnh thì không thấy ô Số seri đang nhập
- [x] Nguyên nhân: khối "File/ảnh đính kèm" là một dòng CỐ ĐỊNH của `Column` ngoài cùng trong
      `nhap_ket_qua_cong_viec_main_page.dart`, nằm NGOÀI vùng cuộn. Mở cả ảnh công trình lẫn ảnh
      biên bản là nó chiếm gần hết màn; bật bàn phím thì phần `Expanded` còn lại co lại, ô serial
      bị đẩy khuất mà không cuộn tới được
- [x] Sửa: chuyển khối ảnh vào `NestedScrollView.headerSliverBuilder` (SliverToBoxAdapter) —
      vuốt lên là khối ảnh trôi đi, nhường toàn bộ chiều cao cho form. Tab con vốn đã là
      `SingleChildScrollView` nên phối hợp được ngay
- [x] Tiện tay sửa tràn layout ngay trên màn đó: `bao_hanh_tab_view.dart` Row "% Hoàn thành /
      SL bàn giao / Định mức công" dùng bề rộng cứng 90+80+85 + khoảng cách → vượt màn hẹp,
      hiện vạch "RIGHT OVERFLOWED BY 6.0 PIXELS" (thấy rõ trong ảnh user gửi). Đổi sang
      `Expanded(flex: 18/16/17)` giữ đúng tỷ lệ cũ
- [x] Đã hot reload và chụp màn xác minh: khối ảnh cuộn được, vạch tràn biến mất, log 0 lỗi layout

### Lỗi 5: không thêm được công khoán phụ khi PGV chưa có công phụ nào
- [x] Nguyên nhân: `_getVisibleMainTabs()` trong `nhap_ket_qua_cong_viec_main_page.dart` chỉ hiện tab
      `MainTab.congPhu` khi `work_p3` ĐÃ CÓ dữ liệu → PGV chưa có công phụ thì tab biến mất,
      không còn đường nào để thêm (web thì bấm dấu "+" thêm được)
- [x] Sửa 1 dòng: `work_p3.isNotNullNorEmpty == true || !_isReadOnly` — tạo/sửa thì LUÔN hiện tab,
      xem/duyệt vẫn ẩn khi rỗng vì không có gì để xem
- [x] Không phải viết thêm UI: `CongPhuTabView` vốn đã có sẵn nút "Thêm công phụ" cho cả nhánh rỗng,
      và `_onAddWorkP3` trong bloc đã xử lý được trường hợp `object` null / list rỗng
      (`ApiObjectData(workP3: [...])` + nới `congViecPhuChecked`)
- [x] Đã hot reload + chụp màn xác minh: tab hiện ra, vuốt sang thấy đúng nút "Thêm công phụ"

### Lỗi 3 — SỬA SAI CHIỀU, đã đảo lại (bằng chứng từ tester)
- [x] BẪY LỚN: `is_serial` TÊN NGƯỢC NGHĨA. ERP tính `in_array(product_type, Config::serial_product_types)`,
      mà ô cấu hình đó trên UI tên là **"Hàng KHÔNG bắt buộc Serial"** (Cấu hình hệ thống > CSKH,
      cổng dev chỉ có Dầu nhờn + Hoá chất làm sạch). Nên `is_serial = true` nghĩa là MIỄN serial.
- [x] Vì đọc theo tên biến, bản vá đầu tách ĐÚNG TẬP NGƯỢC LẠI. Đã đảo: `if (!$mienSerial && $qty > 1)`
- [x] Với cách hiểu đúng thì code ERP `if (!pro.is_serial) { tách }` KHỚP HOÀN TOÀN mô tả task —
      trước đó tôi tưởng hai bên mâu thuẫn và đã hỏi user, thực ra là do tôi đọc sai cờ
- [x] Bằng chứng tester: PGV TPE.PGV.2026000531 (2 dòng, SL bàn giao 2) → PNKQ TPE.PNKQ.2026000432
      hiện 4 dòng, SL bàn giao mỗi dòng = 1
- [x] Thử lại trên dữ liệu thật: 44973 (miễn serial, SL2) giữ 1 dòng SL2; 38204 (bắt buộc serial, SL2)
      tách 2 dòng SL1
- [ ] CẦN ĐẨY LẠI hrm-api: bản user vừa deploy đang chạy ĐÚNG CHIỀU NGƯỢC
