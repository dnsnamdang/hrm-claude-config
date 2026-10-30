---
name: app-simulator-test
description: Cách test TPE_APP trên iOS simulator TRƯỚC khi báo xong — chạy app (fvm, flavor tpeLocal), hot reload / hot restart, chụp màn + tỉ lệ toạ độ chạm, mobile-mcp, bàn phím ảo (ngắt bàn phím Mac), kịch bản test bắt buộc theo loại màn (form, danh sách, chi tiết, thông báo), thử push, không chen tay khi user đang dùng simulator, dữ liệu thử. Dùng khi vừa sửa app xong, khi user nói "test kỹ", "chạy thử", "xem trên simulator", "sao bấm không được".
---

# Test trên simulator — TPE_APP

**User chốt 29/10/2026: "test thật kỹ, đừng để những lỗi cơ bản".** Lỗi đã lọt vì test hời hợt: bàn phím che nút Lưu
(test bằng bàn phím Mac nên không thấy), "Làm mới" bộ lọc không xoá, chọn nhân sự kiểu cũ, nút thiếu icon. Báo xong
= đã BẤM THẬT đúng luồng user sẽ làm, trên đúng loại màn, không chỉ `analyze` sạch.

## 1. Chạy app

- Luôn `fvm` (Flutter 3.41.7). Chạy nền 1 lần, giữ suốt phiên:
  `cd app && ~/fvm/versions/3.41.7/bin/flutter run --debug -t lib/main.dart --flavor tpeLocal --dart-define=FLAVOR=tpeLocal -d <UDID> > run.log 2>&1`
- `tpeLocal` trỏ `127.0.0.1:8000` (`HRM/hrm-api` develop). Muốn xem dữ liệu dev → bản TestFlight tpeDev.
- Sửa code: hot reload `kill -USR1 $(pgrep -f "flutter_tools.snapshot run"|head -1)`; đổi `main`/`my_app`/khởi tạo
  → hot restart `-USR2` (về màn chọn phân hệ). Thêm route / `@LazySingleton` / freezed → `make gen` rồi chạy lại.
- Lỗi link `SAMKeychain` khi build simulator: `make fix_pod_dev` + `pod install` (ngoài sandbox), xong
  `git checkout app/ios/Podfile`. Build release xong cũng trả `Podfile` về như cũ.
- Agent chạy nền KHÔNG build / bật simulator / `build_runner` (đụng nhau).

## 2. Thao tác

- Chụp: `xcrun simctl io <UDID> screenshot s.png` rồi `sips -Z 800` để xem. **Toạ độ chạm = toạ độ trên ảnh 800px × 1,065**.
- Chạm / vuốt / gõ: mobile-mcp (`mobile_click_on_screen_at_coordinates`, `mobile_swipe_on_screen`, `mobile_type_keys`).
  Cần toạ độ chắc chắn → `mobile_list_elements_on_screen`.
- **Bàn phím ảo:** simulator nối bàn phím Mac thì KHÔNG hiện bàn phím ảo → test form phải ngắt: ⇧⌘K (I/O →
  Keyboard → Connect Hardware Keyboard bỏ ✓). Trả lại cho user gõ phím Mac: ⇧⌘K lần nữa.
- Màn chuyển trang iOS để màn trước lệch x = −130 trong cây phần tử — bình thường, không phải lỗi.
- **User đang dùng simulator** (màn đổi giữa 2 lần chụp, có chữ mình không gõ) → DỪNG thao tác, chỉ báo cách xem;
  lỡ chạm vào form của user → chọn "Ở lại màn này", không để mất dữ liệu user đang nhập.
- Test xong để nguyên simulator + app (memory "Giữ simulator sau test").

## 3. Kịch bản bắt buộc theo loại màn

**Form** (`app-form`), bàn phím ảo BẬT:
1. Gõ ô 1 dòng → Enter sang ô sau. 2. Gõ ô nhiều dòng → chạm vùng trống → bàn phím đóng, thấy nút Lưu.
3. Vuốt form khi bàn phím mở → đóng. 4. Chạm ô chỉ đọc khi đang gõ → đóng. 5. Danh sách gõ nhanh: Enter và ➕
đều thêm, bàn phím giữ. 6. Để trống bắt buộc → Lưu → lỗi đỏ đúng ô (BE). 7. Sửa → ‹ → hỏi chưa lưu.
8. Lưu thật → về màn trước, kiểm DB (`mysql -uroot local_hrm_erp`).

**Danh sách** (`app-list-page`): mở lọc → chọn → Xem N → chip + badge đúng; bấm ✕ chip; **Làm mới → Xem kết quả →
hết lọc**; tìm ra 0 → "Không có dữ liệu phù hợp."; kéo tải lại; đổi dữ liệu ở màn con → danh sách tự cập nhật.

**Chi tiết** (`app-detail-page`): đủ trạng thái (nháp / đang chạy / đã xong / không quyền) → đúng nút; thao tác
ghi có hỏi; lưu ở màn con → quay lại thấy mới.

**Khung / chung:** đổi tab con (con trượt, không giật); màu + vân + chuông đúng phân hệ ở màn con; nút có icon;
thanh 3 nút không cắt chữ (màn 393pt).

**Thông báo** (`app-notification`): bấm từng loại → đúng màn; push trên màn hình khoá (`simctl push`).

## 4. Dữ liệu thử

- Tạo dữ liệu đủ trạng thái trước khi test (SQL / tinker trên `local_hrm_erp`, tiền tố `[TEST-…]`), tài khoản
  namdangit@gmail.com / 2025Dns@2 (user 13, employee_info 6). Dev ghi được, prod phải hỏi.
- Lệnh chạy nền / thông báo theo giờ: chạy command với `--at` đúng mốc thay vì chờ.

## 5. Báo kết quả

Bảng "thao tác → kết quả" thật đã bấm; ghi rõ cái CHƯA thử (vd chưa thử Android, chưa thử màn X). Không viết
"đã test" khi chỉ analyze. Ghi vào plan.md.
