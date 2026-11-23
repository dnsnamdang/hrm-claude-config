# Demo — Phiếu xuất kho (Thành An)

> Người phụ trách: @khoipv · Bắt đầu: 23/11/2026
> Spec đầy đủ: `docs/superpowers/specs/2026-11-23-demo-phieu-xuat-kho-design.md`
> Demo: `demos/demo-phieu-xuat-kho.html` · Tiếp luồng `demos/demo-phieu-de-nghi-xuat-kho.html`

## Mục tiêu
Demo màn Phiếu xuất kho nối tiếp Phiếu đề nghị xuất kho: thủ kho nhận ĐNXK → chọn lô / serial → duyệt xuất (trừ tồn, ghi thẻ kho) → gửi bộ phận giao hàng.

## Quyết định lớn
- PXK **chỉ lập từ ĐNXK** (Chờ xuất kho / Đang xuất kho), do **thủ kho của kho đó** lập (như hrm). 1 ĐNXK nhiều PXK, tối đa 1 nháp.
- **2 trạng thái** như Phiếu nhập kho: Nháp (giữ tạm tồn lô) → Đã xuất kho (trừ `stock_balances` / `stock_serials`, ghi `stock_ledgers` PXK, khóa).
- Lô được chọn: tồn chung + lô giữ cho đúng HĐ (hàng KH gửi tạm bỏ, chờ chốt logic); sắp **lô giữ HĐ trước rồi FEFO**; gợi ý lô tự động.
- Hết hạn chặn cứng, cận date ≤ 90 ngày cảnh báo mềm; xuất thiếu cảnh báo mềm → ĐNXK sang Đang xuất kho.
- Chặn vượt tồn khả dụng lô, vượt SL còn phải xuất, SL số nguyên; ngày xuất ≥ ngày tạo ĐNXK, ≤ hôm nay.
- Tạo mới vào thẳng form, **chọn ĐNXK trong form** (select bắt buộc; đổi khi đã nhập SL thì xác nhận; Sửa nháp khóa ĐNXK).
- Thông tin vận chuyển (hình thức, người nhận, SĐT, địa chỉ) copy từ ĐNXK nhưng **sửa được trên PXK**, lưu riêng PXK, không ghi ngược ĐNXK; PGH / in phiếu dùng thông tin PXK.
- PXK không mang giá; bản in mẫu 02-VT để trống Đơn giá / Thành tiền.
- Danh sách: chỉ Phiếu xuất kho (list V2 đủ bộ lọc). Bỏ tab Đề nghị chờ xuất kho — ĐNXK chờ xuất chọn trong form Tạo mới.

## Câu hỏi mở
Q1 phân quyền theo cấp · Q2 `is_can_delete` · Q3 bỏ duyệt / nhập lại · Q4 giá trên PXK · Q5 PGH theo PXK hay ĐNXK · Q6 bỏ popup Xuất kho ở ĐNXK · Q7 lùi ngày xuất.

## Việc kéo theo
Đồng bộ demo ĐNXK: bỏ popup Xuất kho, thống nhất mã PXK (`PXK-YYYY-####`), PGH theo PXK.
