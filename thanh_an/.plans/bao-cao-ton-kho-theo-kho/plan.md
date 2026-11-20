# Báo cáo tồn kho hàng hóa theo kho — Plan

> Người phụ trách: @khoipv · Bắt đầu: 20/11/2026
> Design: `.plans/bao-cao-ton-kho-theo-kho/design.md` · Spec: `docs/superpowers/specs/2026-11-20-bao-cao-ton-kho-theo-kho-design.md`

## Phase 0 — Thiết kế
- [x] 1. Tạo bộ khung feature (.plans, spec, STATUS.md) @khoipv
- [x] 2. Đọc kỹ demo `bc_ton_kho_theo_kho.html` (bộ lọc, KPI, bảng mã → kho → lô/seri, cảnh báo date, in, xuất Excel) @khoipv
- [x] 3. Khảo sát dữ liệu: `stock_balances`, `stock_serials`, `stock_ledgers`, hàng hóa (nhóm / hãng / nước SX), kho @khoipv
- [ ] 4. Chốt câu hỏi với user (phân quyền theo cấp, nguồn bộ lọc, mốc cận date, tối ưu DB) @khoipv
- [ ] 5. Viết spec chi tiết + design tóm tắt @khoipv

### Ghi chú khảo sát 20/11/2026
- Demo: mỗi mã hàng 1 khối (gộp ô) → mỗi dòng con = 1 kho → bung chi tiết lô / seri (NSX, HSD, cảnh báo, mục đích, SL). Bộ lọc: Kho (chọn nhiều), Nhóm hàng, Hãng SX, Nước SX, Khách hàng (tồn chung / giữ KH), Hàng hóa (tên/mã/lô/seri/KH), Chỉ mã có cảnh báo date. KPI: số mã, tổng tồn, giữ KH, số lô cận date / hết hạn. In 2 chế độ (bảng tồn / chi tiết lô-seri), Xuất Excel từng lô/seri.
- Demo còn "quản lý theo lô / seri / lô+seri" → đã bỏ (chốt 19/11), chi tiết dùng 1 dạng chung.
- DB hàng hóa: Mã nội bộ = `internal_code`, Mã thương mại (NSX) = `product_code`, tên TM = `trade_name`, Nhóm hàng = `product_groups`. **Hãng SX + Nước SX là 1 trường gộp** `producer_country_id` → `producer_countries.name` dạng "Hãng/ Nước" (320 dòng).
- Sổ tồn `stock_balances` (kho×hàng×lô×HSD×KH×HĐ) đủ cho báo cáo; `stock_serials` thiếu liên kết về dòng sổ tồn (chỉ khớp được bằng kho+hàng+lô+HSD+KH, HSD null so sánh lệch, không có HĐ).
- **Bug dữ liệu**: 6/32 mục đích giữ KH ở đơn mua cũ chỉ có tên KH + `contract_id`, không có `customer_id` → duyệt PNK ghi `hold_customer_id = 0` (thành tồn chung). Sửa: suy KH từ `contracts.customer_id`.
- `V2BaseDataTable` có sẵn `cellSpan` (gộp ô) + slot `row-expand` → làm được bảng như demo, không cần sửa base chung.
