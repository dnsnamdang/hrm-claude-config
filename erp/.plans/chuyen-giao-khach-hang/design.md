# Design — Chức năng chuyển giao khách hàng (YCCGKH)

> Nguồn: `ERP_Chức năng chuyển giao khách hàng_v1.1_26062026.xlsx` (7 sheet: Hợp đồng, Dashboard chờ duyệt, DS phiếu YCCGKH, DS chờ duyệt, Tạo/sửa, Duyệt phiếu, Xem chi tiết + 2 sheet bối cảnh: Quy trình, Luồng ảnh hưởng).

## Mục tiêu
Tạo **phiếu Yêu cầu chuyển giao khách hàng (YCCGKH)** để chuyển KH của 1 hợp đồng (Vật tư / Dự án / Dịch vụ) từ KH cũ sang KH mới. Khi duyệt → cập nhật KH trên HĐ (Phase 1) và lan sang toàn bộ luồng/báo cáo liên quan (các phase sau).

## Phân kỳ (đã chốt)
- **Phase 1 (spec này):** module phiếu YCCGKH (7 màn) + duyệt **ghi đè snapshot KH trên chính HĐ** (FirmContract/WrServiceContract) + hủy duyệt revert. Xem `design-phase1.md`.
- **Phase 2+:** lan thay đổi KH sang 13 luồng + hàng chục báo cáo (báo giá, xuất/nhập hàng, hàng giữ, dịch vụ, thu-chi, công nợ, quyết toán thưởng, bảo hành, SC-BH, giao việc…). Mỗi nhóm double-check data riêng. Tách spec sau.

## Quyết định lớn (đã chốt với user)
1. **Phân kỳ**: làm Phase 1 (module + duyệt đổi KH trên HĐ) trước.
2. **Nhất quán dữ liệu Phase 1**: chấp nhận **lệch tạm thời** — HĐ đổi KH mới, công nợ/phiếu con giữ KH cũ đến phase sau.
3. **Hủy duyệt (Phase 1)**: từ Đã duyệt → **revert snapshot KH cũ về HĐ** (dùng `old_customer_data`), có **guard** (HĐ chưa phát sinh đề nghị xuất hóa đơn sau chuyển giao). Người có quyền "Duyệt phiếu YCCGKH" được hủy duyệt.
4. **Data model**: Hướng A — bảng phiếu polymorphic (`contractable_id/type`) + snapshot JSON `old_customer_data`/`new_customer_data`, thêm 2 cột index `old_customer_id`/`new_customer_id`.

## Loại HĐ áp dụng
- HĐ Vật tư = `FirmContract` type `HOP_DONG(1)`; HĐ Dự án = `HOP_DONG_DU_AN(4)`.
- HĐ Dịch vụ = `WrServiceContract`.
- **Loại trừ**: HĐ nguyên tắc (`HOP_DONG_NGUYEN_TAC(7)`, `DON_HANG_NGUYEN_TAC(8)`).

## Câu hỏi mở (ghi nhận, xử lý sau)
- Model chính xác của "đề nghị xuất hóa đơn" (tiền điều kiện + guard hủy duyệt) — chốt khi implement.
- Xử lý khi HĐ đã có biên bản bàn giao nghiệm thu ký với KH cũ (sheet Quy trình) — Phase sau.
