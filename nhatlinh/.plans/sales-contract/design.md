# Sales Contract (Module 2 — Hợp đồng bán hàng) — Design (tóm tắt)

**Phụ trách:** @manhcuong · **Phạm vi đợt này:** HD-01 (Danh sách) + HD-02 (Tạo/sửa). Hoãn HD-03/04/05.
**Spec chi tiết:** `docs/superpowers/specs/2026-06-08-sales-contract-design.md`

## Mục tiêu
Module mới `Modules/Sale` quản lý hợp đồng bán hàng: danh sách (lọc/tìm/xuất Excel) + tạo/sửa HĐ (thông tin chung + hạng mục hàng hoá + đợt thanh toán + bảo hành/ghi chú/file), luồng duyệt **Nháp → Chờ duyệt → Đã duyệt (+ Huỷ)**.

## Quyết định lớn
- **Module mới** `Modules/Sale`, route `/api/v1/sale/contracts`, FE `pages/sale/contracts/`. Khung giống `Category`.
- **4 bảng:** `sale_contracts`, `sale_contract_items`, `sale_contract_payment_terms`, + bảng `files` chung (table='sale_contracts').
- **Mã HĐ** tự sinh `HĐ.NNNNN` (5 số, chạy liên tục) qua `getNextCode()` + lockForUpdate.
- **Hạng mục:** chọn SP từ danh mục hàng hoá → auto-fill ĐVT/đơn giá gợi ý/VAT/loại, cho sửa đơn giá + SL.
- **VAT theo dòng** (auto từ SP). Tổng HĐ = tiền hàng trước thuế + thuế. BE tính lại, không tin FE.
- **Đợt thanh toán:** bảng đợt tự do (tên + % + số tiền auto + ngày), validate tổng % = 100%.
- **Phân quyền cấp:** list lọc theo company/department/part; HĐ Nháp chỉ người tạo thấy.
- **Xoá:** chỉ khi Nháp + là người tạo. Khác thì dùng Huỷ.
- **Quyền (id 1105-1107):** Quản lý / Duyệt / Xem hợp đồng bán hàng (seeder + DB + Super admin + menu).
- **Status badge:** entity `const STATUSES` + trait `HasStatusBadge`; FE chỉ `V2BaseBadge`. Nháp `#D97706`, Chờ duyệt `#2563EB`, Đã duyệt `#059669`, Huỷ `#6B7280`.

## Không làm đợt này
Timeline tiến độ (HD-03), phụ lục (HD-04), báo cáo doanh số (HD-05), liên kết PO/LSX/giao/thu.
