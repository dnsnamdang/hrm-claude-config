# Sửa báo cáo chi tiết báo giá — Mỗi báo giá 1 dòng

**Tóm tắt:** Sửa `plan/detail-report` từ hiển thị mỗi hàng hóa 1 dòng (27 cột) sang mỗi báo giá 1 dòng (19 cột). Bấm vào "Số mặt hàng" → popup chi tiết hàng hóa.

**Scope:**
- BE: Tạo API mới `quotations/summary-report` (GROUP BY quotation)
- FE: Sửa bảng + thêm popup + sửa export Excel
- Backup bản cũ

**Quyết định lớn:**
- Tạo API mới thay vì group ở FE → phân trang chính xác, ít băng thông
- Popup dùng API có sẵn `quotations/{id}` → không cần thêm endpoint
- Style popup giống GT/HĐ detail của `sale/report-project-contract`

**Spec chi tiết:** `docs/superpowers/specs/2026-05-28-detail-report-quotation-summary-design.md`
