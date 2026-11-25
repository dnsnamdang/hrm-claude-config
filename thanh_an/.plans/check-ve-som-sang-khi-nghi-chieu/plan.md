# Check: Đã xin nghỉ chiều, sáng về trước 30' có bị trừ công không? Có cần làm đơn "về sớm giữa ca" 30'?

@khoipv — Bắt đầu 25/11/2026 — Nguồn: tin nhắn hỏi (Screenshot_64.png)

## Câu hỏi
NV đã có đơn nghỉ buổi chiều (đã duyệt). Buổi sáng về sớm 30' (vd ra 11:30 thay vì 12:00) → có bị trừ công nhiều không? Làm đơn "Về sớm giữa ca 30 phút" là được phải không?

## Task
- [x] Trace logic tính công `TimesheetSummaryService::calcTimesheetEmployee()`
- [x] Trace đơn đi muộn/về sớm (`late_early_outs`) dùng trường nào khi tính công
- [x] Đối chiếu cấu hình ca + dữ liệu đơn nghỉ chiều (DB local `thanhan_stag_07052026`)
- [x] Trả lời user

## Kết luận
**Không bị trừ công, kể cả không làm đơn về sớm.** Ngày đó vẫn đủ 1 công (0,5 làm + 0,5 nghỉ).

1. Đơn nghỉ chiều lưu tới hết ca (vd 13:30–17:30) → phủ giờ ra chuẩn `checkout_accept` (17:30 − 15' cho phép = 17:15).
   - Nghỉ có lương (Nghỉ phép, Nghỉ bù… `salary_ratio > 0`): `TimesheetSummaryService.php:430-436` gán `checkout = checkout_accept` → có vào + có ra → `labour_day` = đủ ca; cộng `subDay` 0,5 rồi chặn trần = 1 (`:505-510`); `minutes_early = 0` vì checkout không sớm hơn checkout_accept (`:531`).
   - Nghỉ không lương (`LT_NKL`, `salary_ratio = 0`): không gán checkout; giờ ra 11:30 không nằm khung chấm ra (16:00–19:00) → coi như chỉ có chấm vào → phạt quên chấm ra 0,5 (`:483-490`), `nghi_khong_luong = 0,5` → công = 0,5 (đúng phần làm buổi sáng). Không có trừ thêm cho 30'.
2. Giờ ra lúc 11:30 chỉ được ghi vào `checkin_out_center` (`:390-396, :423-425`) — cột này chỉ lưu để hiển thị, **không tham gia tính công/đi muộn về sớm**. Hệ thống hiện không kiểm tra giờ ra giữa ca.
3. Trường "Về sớm giữa ca (phút)" của đơn đi muộn/về sớm (`early_leaving_middle_shift`, FE `pages/timesheet/late-in-early-out/add.vue:106`) **không được dùng ở bất kỳ chỗ tính công nào** — chỉ `late_coming_shift_start` / `early_leaving_shift_end` được dùng (`:337-371, :592, :634`). ⇒ Làm đơn về sớm giữa ca 30' là được về mặt thủ tục (quản lý duyệt, lưu vết) nhưng không làm thay đổi công.

Lưu ý: hệ quả ngược lại — NV đã nghỉ chiều có lương thì sáng về lúc nào (9h, 10h…) công vẫn đủ, hệ thống không bắt. Nếu công ty muốn kiểm soát về sớm buổi sáng khi nghỉ chiều thì cần bổ sung logic (chưa làm, chờ user quyết).

### Checkpoint — 25/11/2026
Vừa hoàn thành: trace logic + trả lời
Đang làm dở: —
Bước tiếp theo: chờ user có muốn bổ sung kiểm tra về sớm giữa ca khi nghỉ nửa ngày không
Blocked:

## Hỏi thêm 25/11/2026: Không cần tạo đơn về sớm vẫn được đúng không?
Đúng (xét về tính công): có hay không có đơn về sớm thì công vẫn như nhau. Điều kiện: đơn nghỉ chiều phải được **duyệt**. Nếu duyệt sau khi đã chạy tính công thì phải tính công lại ngày đó.

## Hỏi thêm 25/11/2026: Lúc về (11:30) có cần chấm công không?
- **Không cần chấm ra.** Lượt chấm 11:30 nằm ngoài khung chấm ra (vd 16:00–19:00) → không được lấy làm giờ ra, chỉ lưu `checkin_out_center` (`TimesheetSummaryService.php:382-396`). Chấm hay không thì kết quả như nhau:
  - Chiều nghỉ có lương: giờ ra tự gán = giờ ra chuẩn (`:434-436`) → 1 công.
  - Chiều nghỉ không lương: luôn bị coi là thiếu chấm ra → 0,5 công (đúng phần sáng).
- **Chấm vào buổi sáng vẫn phải có:**
  - Chiều nghỉ không lương mà thiếu cả chấm vào → không có vào/ra → 0 công.
  - Chiều nghỉ có lương mà thiếu chấm vào: code hiện tại chỉ có giờ ra (tự gán) → phạt quên chấm vào 0,5 (hoặc 0,25 tùy ca) rồi cộng 0,5 nghỉ → vẫn **đủ 1 công** (`:491-510`). Đây là lỗ hổng: NV nghỉ chiều có lương thì sáng không đi làm cũng không bị trừ. Chưa sửa, chờ user quyết.
