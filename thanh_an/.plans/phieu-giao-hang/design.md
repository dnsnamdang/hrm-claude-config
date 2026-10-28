# Design (tóm tắt) — Phiếu giao hàng (bản thật, giai đoạn 1)

> @khoipv · 28/10/2026 · Spec đầy đủ: [docs/superpowers/specs/2026-10-28-phieu-giao-hang-design.md](../../docs/superpowers/specs/2026-10-28-phieu-giao-hang-design.md) · Demo nguồn: `demos/demo-phieu-giao-hang.html` (bản 28/10)

## Mục tiêu
Làm thật luồng demo bước 1–3: Đơn mua đã duyệt (mọi hình thức VC) → Cung ứng **Gửi bộ phận giao hàng** → **bất kỳ ai** (không cần quyền) tự **Tiếp nhận** (thành người phụ trách) hoặc **Trả lại** → người phụ trách cập nhật **Tiến độ** (lấy hàng NCC nếu tự lấy · giao / nhận từng điểm) + **Chi phí** → **Hoàn thành**.

## Quyết định lớn
- [User] Hoàn thành chỉ đổi trạng thái phiếu → Hoàn thành, **không ghi về đơn mua** (bước 4 để sau). Nút xác nhận bấm tay trên đơn mua giữ nguyên.
- [User 28/10] **Không có quyền riêng**: menu Phiếu giao hàng ai cũng thấy; ai cũng xem / tiếp nhận / trả lại / xử lý phiếu. Quyền `Giao/nhận hàng hóa` (526) làm ở bản đầu đã **gỡ hẳn**. Chỉ Gửi / Sửa và gửi lại / Hủy phiếu cần quyền `Lập đơn mua hàng` (522). Không phân quyền theo cấp.
- [User] Thông báo khi gửi phiếu → chỉ thành viên **nhóm nghiệp vụ Kho**.
- 4 bảng mới `purchase_delivery_notes` / `_points` / `_items` / `_costs` (chỉ index). File hóa đơn chi phí lưu json trên dòng chi phí.
- Còn phải gửi tính theo cặp (điểm, dòng đơn mua), trừ thực giao của phiếu Hoàn thành + SL yêu cầu của phiếu đang mở.
- Không cần chặn thêm trên đơn mua: đơn đã duyệt vốn không sửa / xóa / hủy được.
- [User] Chống kẹt phiếu: người phụ trách được Trả lại khi đã tiếp nhận nhưng chưa xác nhận gì; Cung ứng được Hủy phiếu Bị trả lại (status 6).
- FE: màn danh sách + chi tiết mới `pages/supply/delivery_notes`, chuẩn V2 Cung ứng; nút gửi + bảng tiến độ ở `DeliveryNoteBlock.vue` trong slot `#notice` màn chi tiết đơn mua (`purchase_orders/_id/index.vue`). Mã phiếu `PGH-<năm>-<####>`.

## Ngoài phạm vi
Ghi kết quả về đơn mua, hủy / dời phiếu, chuyển người phụ trách, hoàn ứng, duyệt chi phí, chứng từ, phương tiện, xuất Excel, phân quyền theo cấp.
