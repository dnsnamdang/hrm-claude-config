# #10195 — [App] Báo trùng thời gian Phiếu giao việc / Phiếu đi công tác — @cuong61n

Yêu cầu: tạo phiếu trùng thời gian với phiếu ĐÃ DUYỆT → "Đã có phiếu <> trong khoảng thời gian này" (ảnh lỗi cũ: tiêu đề "Lỗi tạo đơn xin nghỉ", nội dung "fails").

## Hiện trạng (kiểm 19/10/2026 bằng API thật trên local)
- [x] PGV: BE đã sửa (Trí 15–23/04) → 422 "Đã có << PGV-TEST-02 >> trong khoảng thời gian này"; phiếu chờ duyệt KHÔNG chặn (tạo được PGV-29274). App đã đổi tiêu đề (Tú 22/04) → "Lỗi tạo phiếu giao việc" + câu từ BE
- [x] Phiếu đi công tác: chặn đúng, chỉ xét Đã duyệt (phiếu chờ duyệt không chặn; phiếu đã kết thúc sớm không chặn — đúng)
- [x] Sửa BE: số phiếu trong câu báo là id trần ("<< 10392 >>") → đổi sang "PCT10392" như web/app (`BusinessTripAssignService::listBusinessTripAssignEmployee`)
- [x] App gửi `customer_name`, `timekeeping_begin_day` = null mà BE bắt buộc → user chốt hướng 1 (19/10/2026): thêm ô "Khách hàng *" (nhập tay như web) + "Giờ chấm công ngày đầu *" (chọn giờ) vào màn tạo/sửa phiếu đi công tác; nạp lại khi sửa; bỏ snackbar "fails" (lỗi đã hiện dưới ô)
- [x] App test: BE trả đúng "Đã có << PCT10392 >>…" nhưng app không hiện gì — `JsonObjectErrorResponseMapper` (dùng chung) ép `errors.*.first as String`, gặp `duplicate_business_trip_assign_code` là list object → văng lỗi. User chọn sửa ở BE: `BusinessTripAssignRequest` trả danh sách phiếu trùng ở khoá `duplicate_business_trip_assign_code` NGANG HÀNG `errors`; web `business_trip_assigns/add/_id.vue` đọc theo khoá mới. Test app (sửa phiếu nháp PCT10394 trùng PCT10392): snackbar "Đã có << PCT10392 >> trong khoảng thời gian này" ✓
- [x] ~~Mở nút Tạo phiếu công tác cho Tân Phát~~ → ĐÃ HOÀN LẠI (user chốt 19/10/2026): form app thiếu nhiều trường so với web và ghi cứng Địa điểm đến/Địa điểm chấm công = "Hà Nội" (BE dùng tọa độ này làm vị trí chấm công ngày đầu) → Tân Phát vẫn tạo phiếu trên web. Giữ getter `Flavor.isTanPhatGroup` (dùng cho quyền Lưu và duyệt)
- [ ] (TÁCH TASK RIÊNG, chưa làm) Nút "Chỉnh sửa" phiếu nháp trên app gửi lại cả phiếu với place/timekeeping = "Hà Nội", hợp đồng + ca = null → theo code sẽ ghi đè dữ liệu phiếu tạo từ web (chưa chạy thử)
- [x] Đường DUYỆT (`storeApprove`) báo trùng câu khác ("Trùng thời gian… (ID: 10392)") → đổi về "Đã có << PCT10392 >> trong khoảng thời gian này" ✓ (test API)
- [x] Nút "Lưu và duyệt" app lệch giữa các lối vào + khớp lỏng chữ "giao công tác" (cả quyền XEM cũng tự duyệt). User chốt: Tân Phát theo web = đúng quyền "Quản lý phiếu đi công tác"; bản khác giữ nguyên. Hàm `_canDuyetPhieuCongTac` (dashboard_nhan_vien_page) dùng cho ô dashboard, tab Công tác, menu trái
- [x] Test app: admin (có quyền) → "Lưu và duyệt"; NV 305 (chỉ quyền Xem DS phiếu giao công tác theo phòng ban) → ô dashboard + nút "+" danh sách đều "Lưu và Gửi duyệt" ✓ (mật khẩu 305 đã trả lại)
- [x] Web (Playwright): sửa phiếu PCT10394 bấm Lưu → popup "Cảnh báo: các phiếu công tác sau đây trùng thời gian" có dòng Phạm Trung Đức / 10392 ✓

Dữ liệu local đã đổi để test: PGV-TEST-02 (29273) dời sang 21/10/2026 13–17h; phiếu CT 10392 dời sang 22/10/2026 8–17h; tạo thêm PGV-29274 + 1 phiếu CT nháp (test 10195)

### Checkpoint — 19/10/2026 14:05
Vừa hoàn thành: 2 ô bắt buộc + báo trùng (tạo & duyệt) + quyền Lưu và duyệt theo web
Đang làm dở: —
Bước tiếp theo: commit/push cùng các task khác; báo user lỗi Chỉnh sửa ghi đè địa điểm (task riêng)
Blocked:
