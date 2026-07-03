# Design — HDSD màn "Cấu hình duyệt giá" (/assign/settings/price-approval)

## Mục tiêu
Tài liệu HDSD Word cho quản trị viên phân hệ Giao việc: màn thiết lập ngưỡng xác định cấp duyệt báo giá (C1/C2/C3) + mức sàn tỷ suất lợi nhuận + lịch sử thay đổi.

## Hiện trạng màn (khảo sát 03/07/2026)
- FE: `hrm-client/pages/assign/settings/price-approval/index.vue` (1 trang, 4 khối, 3 nút Lưu độc lập). Menu "Cấu hình duyệt giá", quyền FE `isShow: ['Cấu hình phân hệ giao việc/ công tác']`.
- BE: `Modules/Assign` — GET/PUT `assign/bom-price-approval-configs` + GET `/logs`; mức sàn lưu riêng qua `general-regulations.profit_margin_threshold` (không ghi log timeline). Route KHÔNG gắn checkPermission (chặn chủ yếu ở FE menu).
- Bảng `bom_price_approval_configs`: 6 dòng (2 type × 3 level). Seed mặc định: order_value 0–1 tỷ / 1–20 tỷ / >20 tỷ; profit_margin ≥20% / 10–20% / <10%. Log ở `bom_price_approval_config_logs` (chỉ khi giá trị đổi thật, old/new json, changed_by).
- FE cascade: sửa "Đến" (order_value) → "Từ" cấp sau tự theo; sửa "Từ" (profit_margin) → "Đến" cấp sau tự theo. Validate CHỈ Ở FE (BE không validate ngưỡng). Mô tả tự sinh.
- Nghiệp vụ: `BomPriceApprovalConfigService::calculateApprovalLevel(totalSale, marginPercent)` = max(levelV, levelM); không khớp dòng nào → C3. QuotationService chốt `price_approval_level` LÚC GỬI DUYỆT (đổi cấu hình không tính lại BG đã gửi; reject → null → gửi lại áp ngưỡng mới). C1 selfApprove; C2 tpApprove (quyền "Trưởng phòng duyệt giá Bom giải pháp"); C3 TP duyệt → Chờ BGĐ → bgdApprove (quyền "Ban giám đốc duyệt giá Bom giải pháp"). Badge realtime "Cấp duyệt: C1/C2/C3" + LN đỏ/xanh theo mức sàn ở footer `quotations/_id/edit.vue`.
- Ranh giới: min dùng ≥, max dùng < (V đúng bằng "Đến" thuộc cấp đó vì mô tả V ≤ max; M đúng bằng "Từ" thuộc cấp đó).

## Cách dựng
- 1 agent Opus đọc FE+BE+luồng quotation. Playwright chụp 6 ảnh dev-hrm (namdangit): tổng quan, 2 tooltip, lịch sử, footer Làm giá BG-2026-00151 (C3 + LN 0% đỏ), cảnh báo validate (nhập sai rồi reload, không lưu).
- Generator `gen_priceapproval.py` + `hdsd_p5_work/hdsd_lib.py`, khung HDSD_VaiTroDuAn, bìa "(Màn hình: Cấu hình duyệt giá)".

## Output
- `HDSD_luongchinh/HDSD_CauHinhDuyetGia.docx` — 9 Heading 1 (TỔNG QUAN + PHẦN 1..6), 6 hình, 7 bảng, ~0.7MB, broken=0.
- Ảnh: `hdsd_priceapproval_shots/`.
