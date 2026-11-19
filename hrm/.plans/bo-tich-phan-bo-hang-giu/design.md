# #12041 — Phiếu nhập kho: cho bỏ tích "Cần giữ" ở tab Phân bổ hàng giữ

Phạm vi HRM: màn PNK tạo/sửa, loại 2 và 15 (tab chỉ hiện ở 2 loại này).
Nghiệp vụ: bỏ tích dòng/tất cả phải hỏi xác nhận; đồng ý thì không giữ, hàng về tồn kho, ô Hạn giữ khoá.
BE đã xử lý sẵn `allocation = 0` (không tạo giữ) nên chỉ sửa FE.

## Quyết định đã chốt

- 10/11/2026 — Chữ nút popup bỏ tích: ticket ghi "Đồng ý / Không", skill button-convention quy định
  popup xác nhận là "Xác nhận / Hủy". User chốt **theo chuẩn HRM: Xác nhận / Hủy**. Câu hỏi giữ nguyên văn ticket.
  (ERP giữ "Đồng ý / Không" như ticket.)
