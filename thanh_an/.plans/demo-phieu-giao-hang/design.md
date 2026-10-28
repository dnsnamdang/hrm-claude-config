# Design (tóm tắt) — Phiếu giao hàng

> @khoipv · 27/10/2026 · bản 2: 28/10/2026 · Spec đầy đủ: [docs/superpowers/specs/2026-10-27-demo-phieu-giao-hang-design.md](../../docs/superpowers/specs/2026-10-27-demo-phieu-giao-hang-design.md) · Demo: `demos/demo-phieu-giao-hang.html`

## Mục tiêu
Áp dụng cho đơn mua đã duyệt, **mọi hình thức vận chuyển** (NCC giao về kho · NCC giao thẳng KH · Cty tự lấy về kho / giao KH). Luồng:
1. Cung ứng bấm **Gửi bộ phận giao hàng**.
2. Ai trong bộ phận phụ trách thì vào **Tiếp nhận** và trở thành **người phụ trách**.
3. Người phụ trách cập nhật **tiến độ**, **chi phí**, rồi bấm **Hoàn thành**.
   - Cty tự lấy: lấy hàng tại NCC → giao từng điểm.
   - NCC giao: không có bước lấy hàng → có mặt nhận / bàn giao, xác nhận **SL thực nhận** từng điểm (≤ yêu cầu, thiếu → lý do).
4. Kết quả tự ghi về đơn mua, thay cho các nút xác nhận bấm tay. *(Demo tạm bỏ màn Kết quả — hoàn thành xong ở lại phiếu.)*

## Phạm vi
- Có: mọi `ship_method` (`ncc_kho`, `ncc_kh`, `tu_lay` về kho / giao KH).
- Không:
  - giao từ kho tới KH
  - GPS
  - in biên bản giao nhận

## Quyết định lớn (đề xuất, chờ chốt)
1. **Gửi đơn giản**: modal gồm ngày lấy hàng, ưu tiên, ghi chú. Phiếu tự kèm toàn bộ SL còn phải gửi + điểm giao của đơn. Không duyệt, không chọn người.
2. **Tự tiếp nhận**: cả bộ phận được thông báo, ai bấm Tiếp nhận trước là người phụ trách. Có thể **Trả lại** (bắt buộc lý do).
3. Trạng thái:
   - Chờ tiếp nhận → Đang xử lý → Hoàn thành (cờ Có chênh lệch)
   - Chờ tiếp nhận → Bị trả lại → Sửa & gửi lại
4. Chỉ người phụ trách được cập nhật. Màn cập nhật **1 trang đơn giản**: Tiến độ giao hàng → Chi phí → Hoàn thành (không tab, không phương tiện, không chứng từ, không panel người phụ trách / điều kiện hoàn thành / lịch sử / lộ trình).
5. **Chi phí**: mỗi khoản có loại, số tiền, trả cho (tự chi / đơn vị VC / NCC) và hóa đơn. Tổng được so với dự kiến của đơn mua (tự lấy: chi phí tự lấy · NCC giao: cước NCC thu thêm, mặc định trả NCC). Không có khoản nào thì tick "không phát sinh".
6. **Chứng từ**: bỏ (28/10) — chỉ còn file hóa đơn theo từng khoản chi phí.
7. **Hoàn thành**: cần đã lấy hàng (chỉ tự lấy) + giao / nhận hết điểm + chi phí hợp lệ. Khi hoàn thành:
   - điểm giao và đơn mua tự cập nhật
   - chi phí ghi vào Chi phí VC của đơn mua; khoản tự chi chuyển Kế toán hoàn ứng
   - về kho → báo thủ kho
   - NCC giao thiếu → quay lại "Còn phải gửi"
8. DB mới gồm `purchase_delivery_notes` và các bảng `_points`, `_items`, `_costs` (chỉ index, không khóa ngoại).

## Câu hỏi mở
- Tự tiếp nhận hay trưởng bộ phận giao người? Có phân quyền theo cấp không?
- Chỉ 1 người phụ trách mỗi phiếu?
- Có cần lưu chứng từ / thông tin xe ở đâu khác không? Có cần chuyển người phụ trách không?
- Khoản tự chi có lập đề nghị hoàn ứng không? Chi phí vượt dự kiến có cần duyệt không?
- NCC giao: cước NCC thu thêm có hóa đơn riêng không? NCC giao bù thì gửi phiếu mới hay mở lại phiếu cũ?
- Danh mục xe dùng gì?
- Có cần hủy / dời phiếu sau khi đã tiếp nhận không?

Chi tiết: spec §9.
