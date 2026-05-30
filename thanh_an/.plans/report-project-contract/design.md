# BC Tổng hợp Vòng đời Dự toán → Hợp đồng — Tóm tắt

## Mục tiêu
Xây dựng trang báo cáo tổng hợp theo dõi vòng đời 4 giai đoạn: **Dự toán → Báo giá → Gói thầu → Hợp đồng**. Mỗi dòng = 1 Dự toán, hiển thị aggregate data qua các giai đoạn.

## Scope
- 1 trang BC Tổng hợp (không tab)
- KPI cards: Số DT, Tổng BG, Tổng HĐ, % BG→HĐ
- Bảng grouped headers 2 tầng + toggle chi tiết
- Popup drill-down: DT (chỉ SL), GT (đầy đủ), HĐ (đầy đủ)
- Bộ lọc đầy đủ + phân quyền 3 cấp
- Export Excel (ExcelJS)

## Quyết định lớn
- **Bỏ Tên DT + Giá trị DT** → DT chỉ là entity grouping, không có giá trị riêng
- **Base so sánh = BG** (không phải DT): Chênh lệch = HĐ - BG, % Chuyển đổi = HĐ/BG
- **Single endpoint aggregate** (Phương án A) → 1 API call cho main table
- **Popup DT không có đơn giá/thành tiền** (vì project_products không lưu giá)
- **Giữ nhóm header "Dự toán" riêng** (chỉ chứa 2 cột detail: NV, Ngày lập)

## Enhancement: Gom hàng hóa 4 phân hệ + Quy đổi ĐVT (2026-05-29)

Nâng cấp popup chi tiết DT: hiển thị tất cả hàng hóa từ 4 phân hệ (DT/BG/Thầu/HĐ), thêm 3 cột SL (BG/Thầu/HĐ) đã quy đổi về ĐVT chính.

- Sửa BE `lifecycleDetail`: UNION product_id từ 4 bảng, quy đổi bằng `ConversionHelper`
- Sửa FE popup `dt-detail`: thêm 3 cột SL
- Spec: `docs/superpowers/specs/2026-05-29-lifecycle-detail-aggregate-products-design.md`

## Spec chi tiết (feature gốc)
→ `docs/superpowers/specs/2026-05-25-report-project-contract-design.md`
