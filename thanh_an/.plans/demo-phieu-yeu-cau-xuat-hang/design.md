# Demo — Phiếu đề nghị xuất kho (Thành An)

> Người phụ trách: @khoipv · Bắt đầu: 21/11/2026
> Spec đầy đủ: `docs/superpowers/specs/2026-11-21-demo-phieu-yeu-cau-xuat-hang-design.md`
> Demo: `demos/demo-phieu-de-nghi-xuat-kho.html`

## Mục tiêu
Dựng demo màn **Phiếu đề nghị xuất kho (ĐNXK)** cho Thành An, tham khảo màn ĐNXK loại "Xuất bán hợp đồng" bên hrm. Demo phải bám luồng thật của Thành An: **HĐ bán → PĐX → PXL (nguồn × phương án, có đổi hàng) → ĐNXK → Phiếu xuất kho → Phiếu giao hàng**. Giao diện theo chuẩn V2Base và các skill (list-page, button-convention, modal-popup, form-validate, select-and-input-state).

## Scope demo
- 3 màn: Danh sách · Tạo/Sửa · Chi tiết, cùng các popup chọn chứng từ nguồn, xác nhận, nhập lý do, xuất kho (lô/serial/FEFO), cấu hình cột, cài đặt bộ lọc, xuất Excel, lịch sử.
- Thanh DEMO để đổi người đăng nhập (2 Cung ứng · 2 thủ kho · BGĐ) và kịch bản công nợ (trong hạn mức · sát hạn mức · nợ quá hạn).

## Quyết định lớn (chờ user chốt)
1. Hàng lấy từ **các ô xuất kho của PXL**, không lấy thẳng từ HĐ. Chứng từ nguồn là HĐ bán (gom mọi PXL của HĐ). Riêng xuất nội bộ chọn PXL nội bộ.
2. **Mỗi phiếu có 1 loại xuất**, quy định phương án nào được lấy:

   | Loại xuất | Phương án được lấy |
   |---|---|
   | Xuất bán | Kho sẵn + Mua về (chỉ phần đã về kho) |
   | Xuất trả hàng KH gửi | KH gửi |
   | Xuất cho KH vay | Cho KH vay |
   | Xuất kho nội bộ | Kho sẵn |

   NCC giao thẳng không lên phiếu.
3. **Đổi hàng**:
   - Dòng chính là hàng thay thế (chip ĐỔI). SL đề nghị, tồn và xuất kho đều tính theo hàng này.
   - Ô "Thay cho hàng gốc" nhập SL hàng gốc. Thành tiền = SL gốc × đơn giá gốc. Hóa đơn và đối trừ HĐ tính theo hàng gốc.
   - Lần đề nghị cuối phải thay hết SL gốc còn lại.
4. **Đã đề nghị** tính mọi phiếu chưa hủy (kể cả nháp). Phiếu đã đóng tính theo SL thực xuất.
5. **Tồn xuất được** = tồn giữ cho HĐ này + tồn chung − đã đề nghị chờ xuất − phần HĐ khác vượt tồn giữ − dòng cùng mã phía trên. Ô hiện số tổng đậm + 2 dòng nhỏ **Giữ cho HĐ: x** · **Tồn chung: y** (phần còn xuất được, x + y = số tổng; chờ xuất trừ tồn giữ trước).
   - Vượt Còn lại → chặn cả lưu nháp lẫn gửi.
   - Vượt tồn → được lưu nháp, chặn gửi.
6. **1 phiếu chỉ xuất từ 1 kho**.
7. **Kiểm công nợ** khi Gửi kho (chỉ áp dụng xuất bán):
   - Trong hạn mức → Chờ xuất kho.
   - Vượt hạn mức → Chờ BGĐ duyệt.
   - Có nợ quá hạn → chặn gửi, chỉ cho lưu nháp.
8. Thủ kho tiếp nhận bằng một trong hai cách: **Xuất kho** (nhiều lần, theo lô/serial, FEFO) hoặc **Trả lại** (kèm lý do). Xuất thiếu thì **Đóng phần còn lại**.
9. Xuất xong và vận chuyển khác "KH tự lấy" → nút **Gửi bộ phận giao hàng** (tạo PGH).

10. **Phiếu không hiện thông tin PXL** (user chốt 21/11/2026):
    - Bỏ các cột Phiếu xử lý, SL theo PXL, Nguồn (cả bảng hàng, màn chi tiết, danh sách, popup chọn HĐ). Cùng mã hàng từ nhiều nguồn gộp 1 dòng; hàng ĐỔI vẫn dòng riêng.
    - Bảng hàng chỉ hiện: **SL còn lại HĐ** (= SL theo HĐ − SL đã thực hiện, tức đã đề nghị trên phiếu khác) · **Tồn xuất được** · SL đề nghị (không cần cột SL theo HĐ / Đã xuất / Chờ xuất / Còn lại).
    - Không chặn theo phần mua đã về nữa; giới hạn = Còn lại theo HĐ + Tồn xuất được tại kho. NCC giao thẳng không hiện.

11. **Demo chỉ làm loại Xuất bán** (user chốt 21/11/2026): chọn loại khác → toast "chưa phát triển", giữ Xuất bán; phiếu mẫu đều là Xuất bán.
12. **Tạm bỏ kiểm công nợ** (user 21/11/2026): ẩn box công nợ + kịch bản trên thanh DEMO, Gửi kho → Chờ xuất kho; giữ code sau cờ `DEBT_ON = false`.

## Trạng thái
1 Nháp · 2 Chờ BGĐ duyệt · 3 Chờ xuất kho · 4 Đang xuất kho · 5 Đã xuất kho · 6 Bị trả lại · 7 Đã hủy

## Câu hỏi mở
1. **Q1.** Ai lập ĐNXK?
2. **Q2.** Vượt tồn thì chặn gửi hay chỉ cảnh báo?
3. **Q3.** Có cần bước duyệt riêng trước khi thủ kho xuất không?
4. **Q4.** Cho sửa SL hàng gốc hay khóa theo tỷ lệ PXL?
5. **Q5.** Có cần "Xuất thẳng" không?
6. **Q6.** Dùng mẫu in nào?

Chi tiết xem mục 8 trong spec.
