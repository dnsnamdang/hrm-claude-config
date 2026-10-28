# Design — Trả lại / thu hồi HĐ đã kết xuất sang cung ứng

> @khoipv — Bắt đầu 26/10/2026 · Spec chi tiết: [docs/superpowers/specs/2026-10-26-tra-lai-thu-hoi-hd-da-ket-xuat-design.md](../../docs/superpowers/specs/2026-10-26-tra-lai-thu-hoi-hd-da-ket-xuat-design.md)

## Mục tiêu
HĐ **Đã kết xuất (9)** chưa có phiếu đề xuất cung ứng còn sống → đưa về **Đã duyệt (3)** bằng 2 đường:
- **Cung ứng trả lại** (màn HĐ đã kết xuất + màn chi tiết HĐ) — bắt buộc lý do, ai vào màn cũng bấm được, báo người lập HĐ kèm lý do, banner đỏ ở màn kết xuất.
- **Người lập HĐ thu hồi** (màn DS hợp đồng, nút fa-undo) — không lý do, báo người đã tiếp nhận (nếu có).

Kèm popup **Lịch sử kết xuất** ở cả 2 màn danh sách (gửi duyệt / duyệt / từ chối / thu hồi / trả lại / thu hồi sau kết xuất).

## Quyết định lớn
- "Phiếu còn sống" = cùng định nghĩa cột Phiếu đề xuất (bỏ phiếu xóa mềm + phiếu 7/8). HĐ đã tiếp nhận vẫn trả lại được.
- Về 3: reset `supply_rendered_*`, `supply_render_requested_*`, `supply_received_*`; giữ điều khoản TT / kết quả / bảo lãnh; kết xuất lại đi qua duyệt `3 → 10 → 9`.
- 1 migration 3 cột `contracts.supply_returned_at/_by/_return_reason` (index, không FK).
- Lịch sử dùng bảng `history_approved_contracts` có sẵn, lọc theo 6 hằng action.
- Siết 2 hàm dùng chung (user đồng ý): `assertContractHasRemaining()` khóa dòng HĐ (bỏ ý suy HĐ từ dòng hàng — chặn nhầm phiếu tay, xem spec §5.6); `receive()` xét status 9.
- Không thêm quyền, không migration dữ liệu.
