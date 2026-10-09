# Điều tra PXK-29097 / PXK-30040 + lỗ hổng logic tạo giữ (prepick)

## Bối cảnh (2026-07-27, prod erp_new)
User báo 2 phiếu xuất kho bị lỗi khi ra phiếu xuất hàng.

## PXK-29097 (WE 29097, cty 4)
- Mã GC-GC-40PRO-A:04 (pid 29407): tồn thực kho 4 = 5, nhưng ĐANG GIỮ (prepick qty>0) = 6 (giữ cho 3 khách khác). Tồn "bán được" = 0.
- Ban đầu lỗi 1427 "xuất nhiều hơn prepick" do `export_prepick_qty=1` stale (giữ khách 25777 đã reset 0 từ 05/07). Đã sửa export_prepick_qty→0 rồi REVERT về 1 theo yêu cầu user (xuất từ giữ).
- KẾT LUẬN: thiếu hàng thật cho khách 25777 (6 tồn đã giữ hết cho khách khác) — quyết định nghiệp vụ, KHÔNG tự sửa.

## PXK-30040 (WE 30040, cty 4)
- Mã SG-MN-HB-SST0101:01 (pid 16136): lỗi "SL xuất không vượt quá SL được xuất" (ProductExportsController:1708).
- Tồn thực=0, tồn kế toán=2, bán được=1 (đã trừ 1 giữ khách 40994), muốn xuất 2 → chặn.

## LỖ HỔNG GỐC phát hiện (logic tạo giữ prepick)
- `Product::getAccountingStockDetail` tính pending (bảng warehouse_export_request_details) LOẠI TRỪ đề nghị xuất kho status=3 "Đang tạo" (dòng 2452) + status=5 Hủy.
- `export_total_qty` (field khóa hàng) CHỈ set ở `WarehouseExportRequest::updateWarehouse()` — chỉ chạy khi đề nghị gửi duyệt (status=2). → Khi đề nghị "Đang tạo", HÀNG CHƯA BỊ KHÓA.
- Phiếu xuất kho tạo được khi đề nghị status=2 (`canApprove()`).
- → Khe hở: khách A soạn yêu cầu xuất (status 3, chưa khóa hàng) → khách B tạo GIỮ chồng lên đúng hàng đó (validate thấy còn trống) → khách A gửi duyệt + xuất trước → giữ của B thành GIỮ ẢO (giữ 1 cái đã bán).
- Đây là race + thiếu khóa cứng, KHÔNG phải "luồng tạo giữ thiếu validate" (cả 2 luồng đều validate tại snapshot).
- Giữ ảo #51346 (khách 40994, pid 16136) hợp lệ (WPR #2078 status=1 còn hạn 08/08) → gỡ = tước suất khách 40994. Chưa xử lý.

## Trạng thái
- KHÔNG có code fix (2 phiếu = thiếu hàng thật / xung đột nghiệp vụ). Chỉ sửa+revert data PXK-29097.
- Lỗ hổng tạo giữ: đề xuất fix triệt để (khóa hàng sớm hơn khi đề nghị đã đặt hàng, hoặc giải phóng giữ ảo ở bước cuối) — CẦN bàn team, chưa làm.

### Checkpoint — 2026-07-27
Vừa hoàn thành: điều tra sâu 2 PXK + xác định lỗ hổng logic tạo giữ (race + thiếu khóa cứng).
Bước tiếp: user quyết xử lý giữ ảo #51346 + nhập hàng cho 2 phiếu; cân nhắc fix triệt để lỗ hổng tạo giữ (bàn team).
Blocked: quyết định nghiệp vụ (ưu tiên khách / nhập hàng).
