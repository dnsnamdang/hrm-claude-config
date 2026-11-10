# Phiếu chi — gắn link phiếu đề nghị (@junfoke)

## Ngày 09/11/2026 (@junfoke)
- [x] 09/11/2026 — Xử lý yêu cầu: màn xem + tạo/sửa phiếu chi (vd bill_payments/1516) ô "Số phiếu đề nghị" thành link mở phiếu đề nghị ở tab mới, chỉ hiện link khi người xem có quyền xem phiếu đề nghị (dùng lại đúng hàm kiểm quyền của màn xem phiếu đề nghị: người lập, người đã duyệt, quyền xem theo phạm vi, người duyệt theo trạng thái); chọn lại phiếu qua kính lúp thì link đổi theo. Sửa `BillPayment.php`, `BillPaymentRequestController.php`, `formShow.blade.php`, `form.blade.php`. Kiểm script + ảnh màn xem/sửa local. Commit "fix xem phiếu" `4fed690c63` (gop_db).
