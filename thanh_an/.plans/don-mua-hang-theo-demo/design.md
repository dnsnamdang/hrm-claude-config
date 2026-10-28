# Design — Đơn mua hàng sửa theo demo `demo-lap-don-mua-hang.html`

> Người phụ trách: @khoipv · Bắt đầu: 21/10/2026
> Spec chi tiết: `docs/superpowers/specs/2026-10-21-don-mua-hang-theo-demo-design.md`
> Demo: `demos/demo-lap-don-mua-hang.html` · Spec demo: `docs/superpowers/specs/2026-10-06-demo-don-giao-hang-design.md`

## Mục tiêu

Màn Đơn mua hàng (`supply/purchase_orders`) chạy như demo:

- Có thể **theo HĐ mua** hoặc là **đơn mua lẻ**.
- Công ty mua chọn ở header.
- Thêm tab **Giao nhận & vận chuyển**.
- Sau duyệt: **xác nhận đã nhận / đã giao** → **Hoàn thành**.

## Scope

- **4 tab:** Thông tin chung · Hàng hóa · Giao nhận & vận chuyển · Điều khoản thanh toán.
- **Popup chọn hàng có 2 chế độ:**
  - HĐ mua: dòng HĐ × mục đích + hàng HĐ bán chưa đề xuất.
  - Đơn lẻ: nhu cầu mua + hàng HĐ bán chưa đề xuất.
- **Hàng hóa:**
  - Chặn mua vượt SL còn lại (HĐ TM theo còn lại HĐ; đơn lẻ theo còn cần mua; HĐ NT không giới hạn).
  - Dòng theo HĐ khoá giá, CK, ĐVT và đổi hàng.
- **Giao nhận:** 3 phương thức `ncc_kho` / `ncc_kh` / `tu_lay` (con: kho / kh).
  - Về kho: kho* + ngày giờ nhận*.
  - Giao KH: điểm giao tự nhóm theo khách.
  - Tự lấy: người đi nhận*.
  - Chi phí VC: NCC chịu / Công ty chịu (bảng khoản chi trả NCC hoặc trả đơn vị VC); chi phí tự vận chuyển.
- **Thanh toán:**
  - Nạp điều khoản từ HĐ.
  - Thêm khối chi phí VC trả đơn vị VC.
  - Tổng thanh toán NCC = tiền hàng + phí VC NCC thu.
- **Màn chi tiết:** nút xác nhận đã nhận hàng (kho) / đã giao từng điểm (KH); trạng thái 6 Hoàn thành.

**Không làm:** sinh phiếu nhập kho / ĐNTT, quyền mới.

## Quyết định lớn

| # | Quyết định |
|---|---|
| 1 | DB: thêm cột vào `purchase_orders` (`purchase_contract_id`, `buyer_company_id`, giao nhận, phí, xác nhận) và `purchase_order_products.purchase_contract_product_id`. Thêm 2 bảng `purchase_delivery_points`, `purchase_delivery_costs`. Chỉ index, không FK |
| 2 | `purposes[].pc_key` liên kết mục đích với HĐ mua. Đã mua = Σ `buyQty` của DMH sống khác (trừ Từ chối / Hủy) |
| 3 | DMH theo HĐ TM không ghi `purchase_demand_allocations`, vì HĐ đã trừ nhu cầu |
| 4 | Thêm STATUS 6 Hoàn thành; báo cáo nhu cầu coi 6 = đã mua |
| 5 | Xác nhận giao/nhận dùng quyền "Lập đơn mua hàng" |
| 6 | Bỏ khỏi form: Loại đơn, Diễn giải, Địa chỉ giao, Cty mua theo dòng (giữ cột DB) |
| 7 | `total_amount` = tiền hàng sau VAT; `ncc_fee`, `carrier_fee`, `self_cost` lưu riêng, BE tự tính lại |
