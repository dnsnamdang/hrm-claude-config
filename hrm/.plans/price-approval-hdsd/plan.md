# Plan — HDSD màn "Cấu hình duyệt giá"

Người phụ trách: @manhcuong
Output: `HDSD_luongchinh/HDSD_CauHinhDuyetGia.docx`
Tài khoản chụp ảnh: namdangit@gmail.com (DNS ADMIN update) — https://dev-hrm.eteksofts.com/assign/settings/price-approval

## Phase 1: Khảo sát & chụp ảnh
- [x] Agent Opus đọc FE index.vue (506 dòng) + BE BomPriceApprovalConfig Controller/Service/Entity/Log/Resource + routes + migration seed + cách QuotationService dùng cấu hình (calculateApprovalLevel, max(levelV, levelM), selfApprove/tpApprove/bgdApprove) + badge cấp duyệt ở quotations/_id/edit.vue
- [x] Chụp 6 ảnh thật → `hdsd_priceapproval_shots/`
  - [x] 01 tổng quan, 02 tooltip mức sàn, 03 tooltip + bảng tỷ suất LN, 04 lịch sử (đã Xem thêm)
  - [x] 05 footer màn Làm giá (BG-2026-00151) — LN đỏ dưới sàn + badge "Cấp duyệt: C3 — TP & BGĐ"
  - [x] 06 cảnh báo validate ngưỡng sai (không lưu DB — validate FE chặn trước API, đã reload khôi phục)
  - [~] Toast "Đã lưu mức sàn" biến mất quá nhanh không chụp được — mô tả bằng chữ (nguyên văn từ code)

## Phase 2: Dựng tài liệu Word
- [x] Generator `scratchpad/gen_priceapproval.py` (dùng hdsd_p5_work/hdsd_lib.py, khung HDSD_VaiTroDuAn)
- [x] TỔNG QUAN: thuật ngữ (C1/C2/C3, V, M, mức sàn, TP, BGĐ), giới thiệu, quyền "Cấu hình phân hệ giao việc/ công tác"
- [x] PHẦN 1: bố cục 4 khối + lưu ý 3 nút Lưu độc lập
- [x] PHẦN 2: mức sàn — bảng trường (0-100, step 0.01), công thức tooltip, toast, không ghi lịch sử
- [x] PHẦN 3: ngưỡng giá trị đơn hàng — bảng cấp + mặc định (1 tỷ/20 tỷ), cascade Từ=Đến cấp trước, mô tả tự sinh, validate lỗi
- [x] PHẦN 4: ngưỡng tỷ suất LN — logic ngược (M cao → cấp thấp), mặc định 20%/10%, ranh giới ≥
- [x] PHẦN 5: lịch sử thay đổi (badge Giá trị ĐH/Tỷ suất LN, cũ đỏ → mới xanh, ∞, Xem thêm, chỉ ghi khi đổi thật)
- [x] PHẦN 6: mapping cấp duyệt → luồng duyệt báo giá (max(levelV, levelM), bảng ví dụ 5 case, badge realtime màn Làm giá, chốt cấp lúc gửi duyệt, hở khoảng → C3)
- [x] Build + verify: 9 Heading 1, 6 hình + 6 caption, 7 bảng, updateFields, broken=0, ~0.7MB

## Phase 3: Hoàn thiện
- [x] Cập nhật plan.md + design.md + STATUS.md

### Checkpoint — 03/07/2026
Vừa hoàn thành: HDSD_CauHinhDuyetGia.docx đầy đủ 6 phần, có phần giải thích nghiệp vụ cấu hình → cấp duyệt báo giá kèm ví dụ số.
Đang làm dở: không
Bước tiếp theo: chờ user review.
Blocked:

## Output
- File: `HDSD_luongchinh/HDSD_CauHinhDuyetGia.docx` (~0.7MB, 9 Heading 1, 6 hình, 7 bảng)
- Ảnh nguồn: `hdsd_priceapproval_shots/` (6 ảnh)
- Generator: scratchpad phiên (`gen_priceapproval.py`) — chạy từ ROOT project HRM/
