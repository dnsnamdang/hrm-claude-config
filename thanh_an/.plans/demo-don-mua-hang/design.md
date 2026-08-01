# Demo "Tạo mới Đơn mua hàng" (prototype)

- Người phụ trách: @namdangit · Ngày: 2026-07-23
- Nguồn: sheet "Đề xuất mua" (Google Sheet cung ứng) từ dòng 65, phần Đơn mua hàng (~618–712)
- Spec chi tiết: `docs/superpowers/specs/2026-07-23-demo-don-mua-hang-design.md`

## Tóm tắt quyết định

- Demo HTML standalone `demos/demo-tao-don-mua-hang.html`, style giống `demo-lap-hop-dong-mua.html` (Bootstrap 4, tab).
- **2 loại đơn**: Lập từ nhu cầu mua hàng (mặc định, popup nhặt **theo từng dòng phiếu đề xuất** PDNMH — 1 mã nhiều dòng thì rowspan gộp ô thông tin hàng) · Lập mới (chọn hàng từ danh mục, dropdown phân loại Dự trù NK / Dự trù PPL / Mua khác).
- **2 tab**: Thông tin chung (loại đơn + thông tin đơn + NCC kèm khối dư nợ theo công ty, địa chỉ NCC sửa được) / Hàng hóa (bảng đúng cột sheet: SL đặt, đơn giá, thành tiền, %VAT, KH sử dụng, loại đề xuất, mục đích mua, HĐ mua, cty ký kết, ngày cần, đơn giá kế hoạch).
- Chọn HĐ mua tham chiếu → auto điều khoản thanh toán + NCC. Cảnh báo vàng (không chặn) khi SL đặt > còn lại. Tổng tiền trước VAT/VAT/tổng thanh toán realtime.
- Vị trí luồng: DXCU → PXL → BC nhu cầu mua → HĐ mua → **Đơn mua hàng** → (sau) Phiếu giao hàng + Đề nghị thanh toán.
