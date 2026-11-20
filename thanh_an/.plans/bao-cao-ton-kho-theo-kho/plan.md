# Báo cáo tồn kho hàng hóa theo kho — Plan

> Người phụ trách: @khoipv · Bắt đầu: 20/11/2026
> Design: `.plans/bao-cao-ton-kho-theo-kho/design.md` · Spec: `docs/superpowers/specs/2026-11-20-bao-cao-ton-kho-theo-kho-design.md`

## Phase 0 — Thiết kế
- [x] 1. Tạo bộ khung feature (.plans, spec, STATUS.md) @khoipv
- [x] 2. Đọc kỹ demo `bc_ton_kho_theo_kho.html` (bộ lọc, KPI, bảng mã → kho → lô/seri, cảnh báo date, in, xuất Excel) @khoipv
- [x] 3. Khảo sát dữ liệu: `stock_balances`, `stock_serials`, `stock_ledgers`, hàng hóa (nhóm / hãng / nước SX), kho @khoipv
- [ ] 4. Chốt câu hỏi với user (phân quyền theo cấp, nguồn bộ lọc, mốc cận date, tối ưu DB) @khoipv
  - 20/11: user bảo "tiếp tục" chưa trả lời phân quyền → đề xuất mặc định như Cung ứng (có quyền xem = thấy mọi kho, không phân cấp), chờ user sửa
  - 20/11: trình 3 hướng dữ liệu (A đọc thẳng `stock_balances` + nối seri bằng `balance_id` · B thêm bảng tổng hợp · C tính từ `stock_ledgers`), đề xuất A, chờ user chọn
  - 20/11: **user chốt A + phân quyền như Cung ứng** (có quyền xem = mọi kho, không phân cấp). User hỏi "sai khi HSD trống" → giải thích: SQL `NULL = NULL` không khớp → seri không HSD rơi khỏi lô (DB stag: 8/10 dòng tồn, 3/3 seri không HSD); thêm cả lỗi thiếu `hold_contract_id` ở seri → chốt dùng `balance_id`
- [ ] 5. Viết spec chi tiết + design tóm tắt @khoipv
  - 20/11: đã viết spec (DB `balance_id` + index + sửa KH thiếu `customer_id`, quyền, 4 API, luật date, UI V2, Excel, In, edge case) + design tóm tắt; đang chạy reviewer đọc thử spec → gom câu hỏi còn lại cho user
  - 20/11: user bảo push → đã commit + push API (c6ad4ec0), client (f3f568b6), config (af6074f). Spec nằm trong `docs/superpowers/` bị `.gitignore` của config → không lên git
  - 20/11: reviewer hỏi 3 câu, trình user: (1) ĐVT sổ tồn — stag 2/6 dòng PNK nhập khác ĐVT gốc (vd "Chiếc" vs "Hộp"), `writeStock` ghi qty theo ĐVT dòng, không quy đổi → cộng tổng sai; (2) lọc cảnh báo date / tìm nhanh theo mã hay theo lô; (3) mục giữ KH chỉ có tên (không customer_id, không contract_id)

### Ghi chú khảo sát 20/11/2026
- Demo: mỗi mã hàng 1 khối (gộp ô) → mỗi dòng con = 1 kho → bung chi tiết lô / seri (NSX, HSD, cảnh báo, mục đích, SL). Bộ lọc: Kho (chọn nhiều), Nhóm hàng, Hãng SX, Nước SX, Khách hàng (tồn chung / giữ KH), Hàng hóa (tên/mã/lô/seri/KH), Chỉ mã có cảnh báo date. KPI: số mã, tổng tồn, giữ KH, số lô cận date / hết hạn. In 2 chế độ (bảng tồn / chi tiết lô-seri), Xuất Excel từng lô/seri.
- Demo còn "quản lý theo lô / seri / lô+seri" → đã bỏ (chốt 19/11), chi tiết dùng 1 dạng chung.
- DB hàng hóa: Mã nội bộ = `internal_code`, Mã thương mại (NSX) = `product_code`, tên TM = `trade_name`, Nhóm hàng = `product_groups`. **Hãng SX + Nước SX là 1 trường gộp** `producer_country_id` → `producer_countries.name` dạng "Hãng/ Nước" (320 dòng).
- Sổ tồn `stock_balances` (kho×hàng×lô×HSD×KH×HĐ) đủ cho báo cáo; `stock_serials` thiếu liên kết về dòng sổ tồn (chỉ khớp được bằng kho+hàng+lô+HSD+KH, HSD null so sánh lệch, không có HĐ).
- **Bug dữ liệu**: 6/32 mục đích giữ KH ở đơn mua cũ chỉ có tên KH + `contract_id`, không có `customer_id` → duyệt PNK ghi `hold_customer_id = 0` (thành tồn chung). Sửa: suy KH từ `contracts.customer_id`.
- `V2BaseDataTable` có sẵn `cellSpan` (gộp ô) + slot `row-expand` → làm được bảng như demo, không cần sửa base chung.
