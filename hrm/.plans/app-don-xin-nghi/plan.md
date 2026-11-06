# Thiết kế lại màn Đơn xin nghỉ trên app (TPE_APP) — @cuong61n

Người phụ trách: @cuong61n · Nhánh: app `tpe` · hrm-api `develop` · hrm-client `develop` (đều chứa gop_db)
Logic bám web `/timesheet/attendance` (`add.vue`, `_id/index.vue`, `_id/approve.vue`) + BE `AttendanceController`
Thiết kế: `~/Downloads/meeting-mobile_v2.pen` → khung **"DXN · Đơn xin nghỉ (Chấm công) — thiết kế lại"** (bên phải nhóm BL1–BL4)

## Phase 1 — Thiết kế (pen.dev)

- [x] 06/11/2026 Đọc logic web + app hiện tại: web có Người bàn giao công việc, cảnh báo đơn trùng thời gian (duplicate_attendance_code), hỏi hủy cơm trùng giờ (423), duyệt 2 cấp TP → NSHC; app đang thiếu 3 thứ này, màn tên "Giấy báo vắng mặt" lệch tên web
- [x] 06/11/2026 Vẽ 7 màn: DXN-01 Danh sách · DXN-02 Tạo đơn · DXN-03 Chi tiết người duyệt · DXN-04 Chi tiết bị từ chối · DXN-05 Chọn loại nghỉ · DXN-06 Cảnh báo trùng thời gian · DXN-07 Hỏi hủy cơm
- [x] 06/11/2026 User chốt: BỎ dải phép năm đầu danh sách, BỎ tiến trình duyệt; màu trạng thái do BE trả, đồng bộ web ↔ app; "Đang tạo" màu xám chuẩn #64748B
- [x] 06/11/2026 Đồng bộ lại bản vẽ theo code: hộp hủy cơm 2 nút [Hủy cơm][Có ăn cơm] như web, 1 icon loại nghỉ chung, ghi chú DXN-05 (> 8 loại → trang chọn có ô tìm)

## Phase 2 — Sửa lỗi user báo 06/11/2026

- [x] 06/11/2026 Màn duyệt / chi tiết không hiện **Loại nghỉ** — gốc: app tra tên loại nghỉ theo danh sách loại nghỉ tải riêng (không khớp → trống, kéo theo tỷ lệ lương 0, leaveTypeId = 0). Sửa: đọc `leave_type_name` / `leave_type_salary_ratio` / `leave_type_usable_leave_days` từ API chi tiết. Đã bấm thử: hiện "Nghỉ phép" + 100%
- [x] 06/11/2026 Màn chi tiết không hiện **Lý do từ chối** — có dữ liệu `reason_of_approver` nhưng màn chưa vẽ. Thêm khối Lý do từ chối ở chi tiết + thẻ danh sách. Đã bấm thử Từ chối → hiện đúng ở cả 2 nơi
- [x] 06/11/2026 Trường bắt buộc thiếu dấu `*` — Loại nghỉ, Từ ngày, Đến ngày, Lý do nghỉ có `*` đỏ (dùng MeetingSelectRow / MeetingTextField `required`)

## Phase 3 — Code theo thiết kế + vá lệch logic so với web

### BE (hrm-api, develop — chưa commit)
- [x] 06/11/2026 `Attendance::ATTENDANCE_STATUS` thêm `color` (9 mã chuẩn) + accessor `status_color`
- [x] 06/11/2026 `AttendanceListResource`: thêm `status_color`, `attendance_reason`, `employee_code`, `department_code`; `leave_type_name` dùng quan hệ (hết query lặp + hết lỗi null khi loại nghỉ bị xoá)
- [x] 06/11/2026 `AttendanceDetailResource`: thêm `status_color`, `leave_type_code`, `leave_type_is_calc_holiday`, `canEdit`, `canDelete`, `substituter_code`, `employee_code`, `department_code`
- [x] 06/11/2026 `AttendanceService` index + approve: eager load `employeeInfo, department, leave_type, updated_by_employee.employeeInfo, attendances_extend_requests` (trước N+1). Đã curl kiểm danh sách + chi tiết + approve list

### Web (hrm-client, develop — chưa commit)
- [x] 06/11/2026 `pages/timesheet/attendance/index.vue` + `approve.vue`: badge trạng thái → `V2BaseBadge :color="item.status_color"` (bỏ class `badge-<type>`). Kiểm Playwright: Đã duyệt #16A34A, Gửi TP duyệt #D97706

### App (TPE_APP, tpe — chưa commit)
- [x] 06/11/2026 Danh sách: thẻ mới (loại nghỉ + badge BE, khoảng nghỉ có thứ, số ngày, "Tên - Mã phòng - Mã NV", lý do, lý do từ chối); menu ⋮ theo cờ BE `can_approve`/`can_reject`/`canEdit`/`canDelete` (trước Sửa/Xóa theo status = 0, không kiểm người tạo)
- [x] 06/11/2026 Form tạo / sửa: tiêu đề "Tạo / Sửa đơn xin nghỉ", người nộp dạng dòng xem, Từ/Đến cạnh nhau (showAppDateTimePicker thay DatePicker cũ), dải Số ngày + Tỷ lệ lương, khối số phép chỉ hiện khi đã chọn loại (trước hiện số của loại thứ 3 khi chưa chọn), chọn loại qua pickWorkOption
- [x] 06/11/2026 Thêm **Người bàn giao công việc** (pickEmployee) — trước app gán cứng `substituter_id` = chính người nộp
- [x] 06/11/2026 Đọc `is_calc_holiday` của loại nghỉ (mapper cũ bỏ sót → luôn 0) → số ngày nghỉ dự kiến tính đúng như web; tính ngay khi đủ 2 ngày (web), không chờ chọn loại
- [x] 06/11/2026 Form tạo chỉ liệt kê loại nghỉ `status = 1` (web); sửa đơn giữ loại đang dùng dù đã khoá; bỏ lọc theo flavor tpeProd ở repository
- [x] 06/11/2026 Chi tiết / duyệt: thẻ đầu (người nộp + badge, Loại nghỉ + số ngày, Từ → Đến, tỷ lệ lương), Nội dung đơn, khối số phép của người nộp; nút [Từ chối][Duyệt] theo cờ BE, Duyệt có hỏi xác nhận; menu ⋮ Sửa / Xóa theo `canEdit`/`canDelete` (khớp danh sách)
- [x] 06/11/2026 Duyệt NSHC: chỉ có quyền NSHC → gọi `POST {id}/nshc-approve` như web (trước gọi `bgd-approve` — route không tồn tại); đọc `can_nshc_approve` của API chi tiết
- [x] 06/11/2026 Cảnh báo đơn trùng thời gian (AppDialog liệt kê mã đơn + khoảng thời gian) — trước bộ đọc lỗi chung ép `as String` với danh sách đơn trùng → văng lỗi; sửa `json_object_error_response_mapper` bỏ qua phần tử không phải câu lỗi
- [x] 06/11/2026 Hỏi hủy cơm (423) theo web: [Hủy cơm] hủy đúng NV trên đơn (`employees: [{employee_info_id}]`) rồi tự gửi lại; [Có ăn cơm] gửi lại kèm `is_confirm_reject_rice`. Viết lại bloc: trước gọi `emit` sau khi handler kết thúc + pop 2 lần (đóng nhầm màn)
- [x] 06/11/2026 Toast theo web: Tạo / Sửa đơn xin nghỉ thành công, Duyệt / Từ chối / Xóa thành công, Hủy cơm thường thành công
- [x] 06/11/2026 `make gen` + `fvm dart analyze lib`: 0 lỗi, 0 cảnh báo, 171 info (chuẩn 173)

### Đã test trên simulator iOS (iPhone 15 Pro, tpeLocal, TK namdangit) — 57 bước step.sh, 0 lỗi Flutter ở màn đơn xin nghỉ
- Danh sách hiển thị · chi tiết đơn quá hạn duyệt chỉ còn Từ chối (đúng cờ BE) · Từ chối → thẻ + chi tiết hiện lý do
- Tạo: Lưu nháp trống → Loại nghỉ đỏ "Bắt buộc chọn" (BE dừng ở lỗi này, web cũng vậy) · chọn loại → hết đỏ, số phép 13/5/8 khớp API web · tính số ngày gửi `is_calc_holiday=1` · Lý do + người bàn giao · ‹ khi chưa lưu → hỏi · Gửi duyệt → DB đúng `substituter_id` người chọn
- Đơn trùng 17/11 → hộp cảnh báo liệt kê mã đơn + ô Lý do đỏ · đơn 18/11 có suất cơm [TEST] → 423 → Hủy cơm → suất cơm chuyển hủy, đơn tự gửi, về danh sách 1 lần
- Sửa từ chi tiết và từ danh sách · Xóa (hỏi xác nhận) · Duyệt TP → Chờ NSHC duyệt (loại cần NSHC) → Duyệt → Đã duyệt · curl `nshc-approve` OK
- Dữ liệu test đã xoá (đơn 13375/13376, suất cơm 223776); đơn 12997 đã trả status 1 nhưng `updated_by/updated_at` đổi theo lần thử Từ chối (DB local)
- CHƯA thử: Android, TK chỉ có quyền NSHC (nhánh gọi nshc-approve từ app), TK không quyền, mất mạng
- Lỗi có sẵn ngoài phạm vi: cuộn menu trái báo "PrimaryScrollController is attached to more than one ScrollPosition" (module_drawer)

## Phase 4 — Build lại bản local + làm đẹp thẻ danh sách (06/11/2026)

- [x] 06/11/2026 User hỏi đang test API nào: app chạy flavor `tpeLocal` → `127.0.0.1:8000` = `HRM/hrm-api` (develop, DB `local_hrm_erp`). Dừng tiến trình flutter cũ (chỉ hot reload từ 03/11), build sạch lại tpeLocal trên iPhone 15 Pro (Xcode 185s); mọi request trong log đều tới 127.0.0.1:8000
- [x] 06/11/2026 Test lại trên bản build mới: Tạo đơn Nghỉ phép 25/11 10:52 → 26/11 23:59 + người bàn giao Nguyễn Tài Trung → Gửi duyệt → DB: status 1, total_days 2, substituter_id 1511 đúng; số ngày (2) + số phép (13/5/8) khớp curl API local; chi tiết hiện Loại nghỉ + người bàn giao; Từ chối có lý do → toast + thẻ danh sách hiện "Từ chối" + lý do. 0 lỗi Flutter. Đã xoá đơn test 13377
- [x] 06/11/2026 User thấy thẻ danh sách xấu → làm lại thẻ: bỏ ô icon loại nghỉ lặp lại ở mọi thẻ, khoảng nghỉ theo khuôn thẻ đầu màn chi tiết (Từ → Đến | số ngày, ngày đậm + giờ dòng dưới), nghỉ trong 1 ngày ghi ngày 1 lần + "08:30 – 17:30", người nộp có avatar chữ tắt + tên đậm "- Mã phòng - Mã NV" xám, lý do thụt theo tên, lý do từ chối gọn 1 khối "Lý do từ chối: …". Thẻ thấp hơn (~3,5 → ~4 thẻ/màn). Analyze sạch, bấm thử ⋮ + kéo tải lại OK
- [x] 06/11/2026 User thấy khoảng giữa dòng "13,043 đơn" và thẻ đầu rộng hơn màn Nhiệm vụ → gốc: dòng tổng của `ListFilterBar` đã có lề dưới 10 mà danh sách còn khai thêm lề trên (12 / 8 / 16 → hở 22 / 18 / 26; Nhiệm vụ + Phiếu giao việc… = 10). Đồng bộ lề trên = 0 ở 18 màn danh sách có dòng tổng: Đơn xin nghỉ, Đi muộn về sớm, Đăng ký làm thêm, Đề nghị tra soát công, Lịch sử chấm công, Yêu cầu điểm danh, Khoá học (DS / đã / đang tham gia / đăng ký / thông báo), Kỳ đánh giá (cần / đã tham gia, thông báo), Lịch thi, Lịch thi của bạn, Kết quả thi, Bài thi kết quả. Ghi quy tắc vào skill `app-list-page`. Analyze 0 lỗi; xem simulator Đơn xin nghỉ + Đi muộn về sớm cách đều 10
- [x] 06/11/2026 Dòng tổng chỉ "13,042 đơn" (chữ xám 12) nhìn trơ → user chọn phương án dùng chung: sửa `ListResultLine` (custom_view/list_filter_bar.dart, user duyệt đổi widget chung) → "Tổng **13,042** đơn", đang lọc "**24** / 13,042 đơn"; chữ "Xoá lọc" → "Xóa lọc" theo bảng chữ chuẩn. Áp tự động ~27 màn danh sách, không sửa từng màn (màn nào truyền chuỗi khác dạng thì hiện nguyên văn). Ghi vào skill `app-list-page`. Analyze sạch; simulator: Đơn xin nghỉ chưa lọc + tìm ra 0 dòng OK
- [x] 06/11/2026 Thẻ danh sách: dòng lý do nghỉ không biết là gì → thêm icon bong bóng lời nhắn (`chat_bubble_outline_rounded` 14, xám) nằm thẳng cột avatar người nộp. Analyze sạch; chưa chụp được trên simulator vì user đang thao tác trên máy
- [x] 06/11/2026 User thấy icon ô chat chưa đẹp → thử dấu ngoặc kép (`format_quote_rounded`) user vẫn chưa ưng → user chọn icon ✎≡ `edit_note_rounded` 18 xám #94A3B8. Đã chụp trên simulator iOS: ổn
- [x] 06/11/2026 User thấy khối khoảng nghỉ 2 dòng tốn chỗ → gom 1 hàng: icon lịch · ngày đậm + giờ xám (1 ngày: "Th 3, 28/07  08:30 – 17:30"; nhiều ngày: "Th 2, 27/07 07:00 → Th 3, 28/07 19:00", co chữ nếu thiếu chỗ) · số ngày "1 ngày" cùng hàng bên phải. Bỏ helper `_rangeEnd`. Analyze sạch; chụp iOS + Android: vừa 1 hàng, thẻ thấp hơn
- [x] 06/11/2026 User thấy danh sách vẫn chưa đẹp → vẽ board "DN · Danh sách Đơn xin nghỉ — 3 phương án thẻ" (`meeting-mobile_v2.pen`): A ô lịch bên trái · B người nộp lên đầu + viền màu trạng thái · C phẳng gom theo tháng (+ C2 bản chỉnh). User chọn B (không gom tháng → không phải sửa sắp xếp BE)
- [x] 06/11/2026 Code thẻ theo B (`_buildItem`): viền trái 4px màu trạng thái BE (`statusTextColor`), đầu thẻ avatar 34 + tên đậm + "Mã phòng - Mã NV" + badge + ⋮; ô xám loại nghỉ đậm + ngày giờ 1 dòng (co chữ khi thiếu chỗ) | số ngày; lý do (icon ✎≡); lý do từ chối chữ xám (bỏ khối nền đỏ — đỏ chỉ cho lỗi). Analyze sạch. Test Android: danh sách Duyệt + Đơn xin nghỉ hiện đúng, ⋮ mở menu Từ chối, tạm gắn lý do từ chối vào đơn 12997 → dòng hiện đúng → đã trả NULL. iOS chưa chụp vì user đang dùng simulator
- [x] 06/11/2026 User muốn icon lý do giống y bản vẽ → dùng đúng Lucide `notebook-pen` (app không có bộ Lucide → nhúng SVG gốc qua flutter_svg) 13×13 #94A3B8, cách 6, chữ 12.5 #475569 (số đọc từ pen). Analyze sạch, chụp Android khớp bản vẽ
- [x] 06/11/2026 User: màn chọn chưa có quy tắc chung (chọn người bàn giao khác chọn loại nghỉ). Rà 5 kiểu đang có: `pickWorkOption` (danh sách phẳng + ✓, ‹), `pickEmployee` (✕, khối gom nhóm "KẾT QUẢ", avatar, ›), `CustomerPickerPage` (‹, ›, nút Hủy đáy), picker dự án / hợp đồng Meeting (mỗi dòng 1 AppCard), `MeetingEmployeePickerPage` (chọn nhiều). User chốt: **danh sách phẳng + ✓**, ≤ 8 mục → bảng trượt. Đã vẽ board "PK · Màn chọn — khuôn chung" trong `meeting-mobile_v2.pen` (PK-01 trang chọn danh mục · PK-02 trang chọn tìm máy chủ có Bỏ chọn · PK-03 bảng trượt · PK-04 chọn nhiều [Hủy | Xác nhận (n)])
- [x] 06/11/2026 User duyệt bản vẽ PK → code: widget chung mới `custom_view/app_pick_tile.dart` (`AppPickTile` dòng chọn 1 / chọn nhiều, `AppPickClearTile` "Bỏ chọn", `showAppPickSheet` bảng trượt PK-03); `MeetingSearchList(flat: true)` (không lề / thẻ / "KẾT QUẢ"). Áp cho: `pickWorkOption` (bảng + trang), `pickEmployee` (‹, không chuông, có `selectedId` / `allowClear` → Người bàn giao bỏ chọn được — trước không có cách bỏ), `CustomerPickerPage` + `MeetingCustomerPickerPage` (bỏ thẻ / › / nút Hủy đáy; KH khoá mờ + lý do), `MeetingProjectPickerPage` (chọn nhiều vòng tròn), `MeetingContractPickerPage`, `MeetingEmployeePickerPage`, bảng Người liên hệ, trang con chọn nhiều của bảng lọc (ô vuông → vòng tròn). Bảng chọn tự dựng chuyển sang `showAppPickSheet`: Loại meeting, Lý do hủy meeting, Sắp xếp (Danh sách meeting + Việc của tôi), Danh sách (việc cá nhân), Trạng thái (Kết quả nhiệm vụ). Giữ nguyên: `showWorkStatusSheet` (form có ô lý do), chọn phòng (lưới tình trạng phòng). Ghi quy tắc vào skill `app-list-page` mục 5 + `app-components` + `app-form` mục 4. Analyze 0 lỗi / 0 cảnh báo / 171 info
- [x] 06/11/2026 Simulator (tpeLocal): Chọn loại nghỉ (trang PK-01, đang chọn ✓) · Chọn người bàn giao (PK-02, chọn → mở lại có ✓ + Bỏ chọn → bỏ được) · Loại meeting (bảng PK-03) · Chọn khách hàng (phẳng, còn nút Thêm nhanh KH) · Người liên hệ (đang chọn ✓). 0 lỗi Flutter mới (lỗi cuộn menu trái có sẵn vẫn còn). CHƯA bấm thử: chọn dự án TKT / hợp đồng / thành phần tham gia (chọn nhiều), bảng Sắp xếp, Lý do hủy, Danh sách việc cá nhân, Trạng thái kết quả nhiệm vụ, bảng lọc chọn nhiều; Android

### Checkpoint — 06/11/2026 10:58
Vừa hoàn thành: build lại bản tpeLocal + test lại luồng trên API local; làm lại thẻ danh sách đơn xin nghỉ; dòng tổng + khoảng cách danh sách đồng bộ; khuôn màn chọn chung PK (vẽ + code)
Đang làm dở: —
Bước tiếp theo: user xem trên simulator / duyệt; commit 3 repo khi user cho; thử Android + TK chỉ quyền NSHC
Blocked:
