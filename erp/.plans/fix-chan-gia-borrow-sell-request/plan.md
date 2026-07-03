# Fix: lỗ hổng chặn thay đổi giá - Yêu cầu xuất bán hàng mượn

## Bug
`BorrowSellRequestsController::checkDiffPrice` chỉ chạy khi `status == CHO_TP_DUYET(10)`. Phiếu tạo/duyệt thẳng status khác (vd 1=Đã duyệt) → bỏ qua check giá → xuất lọt dù giá đổi. Ca lỗi: req PYCXBHM-00149 (status=1) / borrow_sell 142 / HĐ 1102 (đơn hàng nguyên tắc type=8) / mã ENEO-800-V5079:03.

## Quyết định (user chốt)
1. BỎ điều kiện `status == CHO_TP_DUYET`, thay bằng LOẠI TRỪ status Đang tạo(3) + Không duyệt(4) → mọi status còn lại đều check.
2. Giữ nguyên 2 điều kiện kia: chỉ áp cho FirmContract + DON_HANG_NGUYEN_TAC (đơn hàng nguyên tắc).

## Tasks
- [ ] Sửa điều kiện trong checkDiffPrice (BorrowSellRequestsController) — master
- [ ] php -l
- [ ] User test: tạo yc xuất bán hàng mượn (status Đã duyệt) với mã đã đổi giá → bị chặn

### Checkpoint — 2026-06-30
Vừa hoàn thành: Sửa lỗ hổng `checkDiffPrice` (BorrowSellRequestsController) — bỏ điều kiện `status == CHO_TP_DUYET`, thay bằng `!in_array($request->status, [3,4])` (loại trừ Đang tạo/Không duyệt); giữ chỉ đơn hàng nguyên tắc. php -l sạch.
Đang làm dở: không.
Bước tiếp theo: USER test browser (tạo YC xuất bán hàng mượn status Đã duyệt với mã đã đổi giá → phải bị chặn) → rồi commit.
Blocked:
