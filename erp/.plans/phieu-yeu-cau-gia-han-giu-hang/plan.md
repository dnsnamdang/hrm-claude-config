# Phiếu yêu cầu gia hạn giữ hàng (ERP) — hỗ trợ vận hành (@junfoke)

## Ngày 11/11/2026 (@junfoke)
- [x] 11/11/2026 — Hỗ trợ check PGHHG-02077 (ERP prod, bước TP duyệt báo không đủ SL dù báo cáo hàng giữ vẫn thấy anh Nguyễn Đức Hiểu giữ 1 TEXA-Z10410:08): không phải lỗi — 10/11 phiếu gia hạn lập 08:38 cho dòng giữ cũ, 10:21 PHHG-04893 hủy chính dòng đó (SL 0), 10:28 PXG-02881 giữ lại 1 bộ hạn 17/11 (dòng giữ mới). Phiếu gia hạn gắn cứng 1 dòng giữ nên báo không đủ là đúng; báo cáo đọc dòng mới. Hướng xử lý: TP từ chối PGHHG-02077, người lập xoá; cần giữ quá 17/11 thì lập phiếu gia hạn mới cho dòng của PXG-02881. Chỉ xem dữ liệu, không sửa.
