# Bypass duyệt kết quả lắp cho PNKQ 5598 (HĐ 125)

## Yêu cầu nghiệp vụ
Cho phép **duyệt kết quả lắp** của `wr_import_result_id = 5598` (HĐ 125, product MUTR-FP-VRC:130 / 38333) dù validation "không đủ SL để bàn giao".
- Lý do bế tắc: hàng đã xuất bán (PXH-26791) rồi **bị KD nhập trả lại** (PNH-09934, đã hạch toán) → `warehouse_exported_qty=0`; nhưng KT đã lắp thực tế.
- User quyết: **HĐ 125 sẽ KHÔNG quyết toán nữa** → chấp nhận lệch dữ liệu (xuất kho/kế toán), chỉ cần duyệt được kết quả lắp.

## Thay đổi (FIX TẠM — chủ ý, có rủi ro lệch dữ liệu)
File: `app/Http/Controllers/Customercare/WrApproveResultsController.php`
- [x] `store()` (~dòng 231): thêm điều kiện bỏ qua `hasProductExport` khi `wr_import_result_id == 5598` (đứng cạnh tiền lệ sẵn có `wr_assign_task_id != 1941`).
- [x] `update()` (~dòng 1083): thêm cùng điều kiện `wr_import_result_id != 5598`.
- Khóa hẹp đúng phiếu 5598 → không ảnh hưởng phiếu khác. Nếu field null thì check vẫn chạy (an toàn mặc định).
- [x] `php -l` sạch.

## Tác động đã biết & được chấp nhận
- Hệ thống ghi sản phẩm "đã lắp/bàn giao" cho HĐ 125 dù sổ sách đang là "đã trả hàng" (doanh thu/giá vốn đã đảo, tồn kho đã về). Lệch giữa thực tế lắp ↔ kế toán.
- Downstream (quyết toán công KT / hoa hồng KD / tồn kho / contract-done) sẽ lệch — **chấp nhận** vì HĐ 125 không quyết toán.

## Lưu ý kỹ thuật / nợ kỹ thuật
- Đây là hardcode id (giống tiền lệ `1941`). Tích lũy id hardcode là nợ kỹ thuật; nếu sau này cần bypass lâu dài nên thay bằng cờ/cấu hình.
- Có thể gỡ bypass này sau khi phiếu 5598 đã duyệt xong (không còn cần).
- Gốc rễ chưa xử lý: chưa có chức năng hủy phiếu nhập đã hạch toán + chưa có guard chặn nhập trả lại khi đã có lắp đặt (đề xuất phòng ngừa, chưa làm).

## Kiểm thử (user)
- [ ] Vào `admin/customer-care/wr_approve_results/create?wr_import_result_id=5598` → duyệt → KHÔNG còn cảnh báo "không đủ SL bàn giao", duyệt thành công.
- [ ] Phiếu kết quả khác (import_result khác) vẫn bị check bình thường.

### Checkpoint — 2026-06-10
Vừa hoàn thành: bypass check hasProductExport cho wr_import_result_id=5598 (store + update); php -l sạch
Bước tiếp theo: user duyệt thử phiếu 5598
Blocked:
