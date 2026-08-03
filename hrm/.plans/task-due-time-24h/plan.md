# Plan — Chuyển trường "Giờ hạn" Task sang định dạng 24h (HH:mm)

@khoipv — Module Giao việc (Assign) / màn Task

## Bối cảnh

Trường "Giờ hạn" (`due_time`) trên màn Task đang dùng `<input type="time">` native (qua `V2BaseInput`).
Native time input hiển thị theo locale trình duyệt → nhiều máy hiện AM/PM (04:30 PM) thay vì 24h.
Cột `due_time` là MySQL `time` → BE trả về "HH:mm:ss" (vd "20:15:00"), list hiển thị thô kèm giây.

Giải pháp (giống feature `my-todo-form-enhance`): đổi sang `V2BaseDatePicker type="time" format="HH:mm" value-type="HH:mm"`
→ ép hiển thị 24h, giá trị lưu "HH:mm"; strip giây khi load & khi hiển thị list.

## Phạm vi: CHỈ FE. Không đụng BE/migration/route/permission/git.

## Tasks

### FE — CreateTaskModal.vue (Tạo mới / Cập nhật / Chi tiết readonly)
- [x] T1. Đổi Giờ hạn task chính (form.due_time): `V2BaseInput type=time` → `V2BaseDatePicker type=time format=HH:mm value-type=HH:mm`
- [x] T2. Đổi Giờ hạn task con dòng thêm nhanh (input.child_due_time) tương tự
- [x] T3. Đổi Giờ hạn task con trong danh sách con (task.due_time) tương tự
- [x] T4. Chuẩn hoá default '17:00:00' → '17:00' (data form + input + reset fallback)
- [x] T5. Strip giây khi load task chi tiết: `(task.due_time || '17:00').slice(0,5)`
- [x] T6. Strip giây khi load children: map due_time về "HH:mm"

### FE — index.vue (Danh sách Task)
- [x] T7. Cột "Giờ hạn" (item.due_time) strip giây → hiển thị "20:15"

### FE — daily-report.vue (hiển thị Giờ hạn — đồng nhất)
- [x] T8. "Giờ hạn: {{ task.due_time }}" strip giây

### Verify
- [x] T9. Parse-check vue-template-compiler + @babel/parser 3 file → OK cả 3
- [x] T10. Browser Playwright PASS toàn bộ (tài khoản DNS ADMIN update):
  - AC1: picker Tạo mới hiện 24h (cột giờ 17,18,19,20,21,22,23 — không AM/PM) ✓
  - AC2: tạo Task "Test giờ hạn 24h 20:15" giờ hạn 20:15 → "Đã lưu task thành công" ✓
  - AC3: danh sách hiện cột "17/07/2026 . 20:15" (24h, không giây); chi tiết/sửa prefill "20:15" ✓
  - AC4: màn Cập nhật picker 24h + prefill 20:15 đúng, mở picker highlight 20:15 ✓
  - Đã xóa task test (Tổng 27→26), không để lại data rác.

## Ghi chú kỹ thuật
- Cột DB `due_time` = MySQL `time` → lưu "HH:mm:ss"; BE Request `due_time` = nullable (chấp nhận "HH:mm"); TaskResource trả thô "HH:mm:ss". Round-trip: FE gửi "HH:mm" → DB "HH:mm:ss" → FE strip về "HH:mm". **KHÔNG đụng BE.**
- Dùng `V2BaseDatePicker` (wrapper vue2-datepicker) cho đồng nhất với các date picker khác trong file; `:clearable="false"` vì Giờ hạn luôn có giá trị (native input cũ cũng vậy).
- Đồng nhất với feature [[my-todo-form-enhance]] (đã đổi cùng cách).

## Điều kiện nghiệm thu
- AC1: Màn Tạo mới → picker Giờ hạn theo 24h (16:30, không 04:30 PM)
- AC2: Tạo Task giờ hạn 20:15 → Lưu thành công
- AC3: Danh sách + chi tiết hiện đúng "20:15"
- AC4: Màn Cập nhật → picker Giờ hạn 24h, hoạt động bình thường
