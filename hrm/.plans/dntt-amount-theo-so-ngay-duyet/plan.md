# Plan — Sửa lỗi Thành tiền DNTT tính theo số ngày ĐỀ XUẤT thay vì số ngày TP/KT duyệt

Phụ trách: @junfoke
Nguồn: Redmine/QA — DNTT-01022, DNTT-01021 (TP/KT duyệt = 0 nhưng thành tiền vẫn = 0,5 ngày × đơn giá)

## Phase 1 — Fix FE

- [x] Xác định gốc lỗi: `calcNumberDayRequest()` / `calcNumberDayRequestSupport()` phân nhánh theo
      `form.canTpApprove` / `form.canKtApprove` (cờ QUYỀN DUYỆT, chỉ true khi phiếu đang chờ đúng
      người đó duyệt). Phiếu đã duyệt xong (status 3/4) hoặc người xem khác → cả 2 cờ false →
      rơi vào nhánh `else` → tính lại `amount` theo `number_day_request`.
      Commit 22c907f83 (27/03/2026) thêm `watch: form.id` gọi lại 2 hàm này mỗi lần load trang
      → phiếu đã duyệt luôn bị ghi đè thành tiền theo số ngày đề xuất.
- [x] Thêm computed `approveStage` (`kt` | `tp` | `request`) xét cả `status`, theo đúng cách
      `PrintTab.vue` (`canTpApprove || status == 3`, `canKtApprove || status == 4`) đang làm.
- [x] `BusinessTravelExpensesTab.vue` — dùng `approveStage` cho cả bảng A (thực tế) và B (hỗ trợ)
- [x] `StayTab.vue` — cùng lỗi ở `calcNumberNightRequest()` / `...Support()` (tiền lưu trú)
- [x] `MovingCostTabEmployeeDetail.vue` — cùng lỗi ở `calcEmployee()` (chi phí đi đường)
- [ ] Verify trên môi trường dev: mở lại DNTT-01022 → Thành tiền = 0
- [x] Kiểm tra dữ liệu prod 1021/1022: `amount = 0`, `business_cost = 0` → DB ĐÚNG, không phải
      lỗi ghi dữ liệu. BE chỉ lưu số FE gửi; lúc TP/KT bấm Duyệt thì cờ đang `true` nên ghi đúng.
      Sai chỉ xảy ra khi MỞ LẠI phiếu đã duyệt (cả 2 cờ về false).

## Phase 2 — Lỗi thứ hai lộ ra khi rà toàn bộ dữ liệu

Câu rà `amount <> amount_dung` trên prod ra 7 dòng (DNTT-00848, 00664, 00266, 00265 ×2, 00264,
00120). Cả 7 đều có `price_regulation = 0` mà `amount` = đúng SỐ NGÀY.

- [x] Gốc lỗi: fallback `(Number(val.price_regulation) || 1)` — đơn giá 0 thì `0 || 1` ra `1`,
      thành tiền = số ngày × 1 đồng. Không có nghĩa nghiệp vụ nào cho "đơn giá mặc định 1 đồng".
- [x] Đổi `|| 1` → `|| 0` (12 chỗ): `BusinessTravelExpensesTab.vue` (6), `StayTab.vue` (6)
- [ ] Rà bảng `payment_business_request_stays` xem có dòng nào dính cùng lỗi không (SQL đã gửi user)
- [ ] Chuẩn hoá 7 dòng dữ liệu cũ về `amount = 0` + tính lại bảng cha (SQL đã gửi user, KHÔNG bắt buộc
      — lệch 0,5-1 đồng, sau khi deploy FE thì màn hình đã hiển thị đúng 0)

## Ghi nhận thêm (chưa sửa)

- `validateNumber()` ở cả 2 tab cũng phân nhánh theo `canTpApprove/canKtApprove` → phiếu đã duyệt
  vẫn validate theo số liệu đề xuất. Chưa sửa vì ngoài phạm vi bug báo, cần chốt với user.

### Checkpoint — 2026-09-10
Vừa hoàn thành: sửa 3 component FE dùng `approveStage`
Đang làm dở: chờ kết quả SQL dữ liệu prod của DNTT-01021/01022 để biết có phải sửa dữ liệu cũ không
Bước tiếp theo: user chạy SQL kiểm tra `amount` đã lưu
Blocked:

### Checkpoint — 2026-09-10 (Phase 2)
Vừa hoàn thành: sửa fallback `|| 1` → `|| 0` cho đơn giá ở 2 tab (12 chỗ)
Đang làm dở: (không)
Bước tiếp theo: user build + deploy hrm-client, verify DNTT-01022/01021; chạy SQL rà bảng lưu trú
Blocked:
