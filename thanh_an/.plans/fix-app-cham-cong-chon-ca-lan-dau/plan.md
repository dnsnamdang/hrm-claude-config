# Fix App: Chấm công — chọn ca/phiếu lần đầu không hiện ca — @khoipv

App mobile `TPE_APP`, nhánh `thanhan` — màn **Chấm công** → ô "Ca/phiếu chấm công".

## Hiện tượng (user báo 13/11/2026)
Vào Chấm công, bấm chọn ca/phiếu lần đầu → sheet trống, không có ca; đóng lại bấm lần 2 mới hiện ca để chọn.

## Task
- [x] Đọc code mở sheet: `app/lib/ui/check_in_out/check_in_out_page.dart` (PrimaryContainer "Ca/phiếu chấm công" → `showMaterialModalBottomSheet`)
- [x] Đọc bloc tải ca: `check_in_out_bloc.dart` `_onInitLoad` (dòng 88–93)
- [x] Đo thời gian 2 API trên BE local: `POST v1/timekeeper/checkTimesheet` ~0.7s, `GET v1/timekeeper/listTimesheetTypes?only_app=true` ~0.7s
- [x] Sửa: sheet lắng nghe bloc thay vì đọc 1 lần
- [x] `flutter analyze` file sửa — No issues; hot reload OK
- [ ] Test tay trên app với tài khoản **có ca hôm nay** (tài khoản đang đăng nhập local không có ca → `checkTimesheet` trả 422 "Chưa có ca làm việc hoặc đăng ký tăng ca", màn tự đóng nên chưa mở được sheet)

## Nguyên nhân
- `_onInitLoad` gọi **tuần tự** `checkTimesheet` rồi `getListTimesheetTypes`, xong mới `emit(types, enabled: true)` → mất ~1.5s (local), server thật có thể lâu hơn.
- Ô chọn ca luôn bấm được (`enabled: true` cứng); trong `builder` của sheet đọc `final types = bloc.state.types;` **một lần lúc mở** → bấm trước khi tải xong thì `types = []`, sheet không rebuild khi bloc emit → trống. Lần bấm thứ 2 dữ liệu đã có nên hiện.

## Sửa (commit `dd69132`, đã push `origin/thanhan` 13/11/2026)
- Bỏ `final types = bloc.state.types;` trong builder sheet.
- Bọc danh sách bằng `BlocBuilder<CheckInOutBloc, CheckInOutState>(bloc: bloc, buildWhen: types/enabled đổi)`:
  - `!enabled` (chưa tải xong) → `CommonProgressIndicator`
  - tải xong mà rỗng → "Không có ca/phiếu chấm công"
  - có dữ liệu → `ListView` như cũ
- Không `dart format` cả file để diff gọn (+25/−3); phần thân `ListView` bên trong lệch thụt lề 4 dấu cách.

## Ghi chú môi trường (13/11/2026)
- Popup "Lỗi kết nối — Kết nối không ổn định" ở màn Tổng quan khi chạy local: do `php artisan serve` trên Windows xử lý **từng request một**, Tổng quan bắn 10–20 request song song → request cuối chờ > 30s (timeout app `ServerConstantsTimeout` = 30s). Đã chuyển BE local sang nginx + 4 worker PHP 8.1 — xem Phase 0 ở [cham-cong-chon-phuong-tien/plan.md](../cham-cong-chon-phuong-tien/plan.md).

## Nhật ký
### 13/11/2026
- Mở lại máy ảo + BE local + app Thành An
- Xử lý "Lỗi kết nối" khi chạy local: thay `artisan serve` bằng nginx (cổng 8001) + 4 php-cgi 8.1 → 10 request song song ~3.5s, Tổng quan không còn timeout
- Fix sheet chọn ca lần đầu trống → commit `dd69132`, rebase lên `564baff` (build 173) rồi push `origin/thanhan`

### Checkpoint — 13/11/2026
Vừa hoàn thành: fix + push
Đang làm dở: —
Bước tiếp theo: user test với tài khoản có ca hôm nay (mở Chấm công, bấm chọn ca ngay → thấy loading rồi hiện ca)
Blocked: tài khoản local hiện không có ca hôm nay
