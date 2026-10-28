# Cho phép sửa %VAT trên PI và Hợp đồng mua (#11833) — Tóm tắt

**Người phụ trách:** @junfoke — 2026-10-22 · Repo ERP `TanPhatDev`, nhánh `gop_db`
Spec đầy đủ: [docs/superpowers/specs/gop-db/2026-10-22-mua-hang-sua-vat-pi-hd-design.md](../../../docs/superpowers/specs/gop-db/2026-10-22-mua-hang-sua-vat-pi-hd-design.md)

## Mục tiêu
%VAT từng dòng hàng trên PI và HĐ mua: mặc định theo DM hàng hóa, **cho sửa** (tối đa 2 số lẻ),
sửa xong tính lại tiền VAT dòng, tổng thuế, tổng giá trị.

## Scope
- **Làm:** luồng mua trong nước (theo hãng + tự do — chung 1 form PI) và HĐ `inland_buy_contract_new`.
- **Chưa làm:** luồng nhập khẩu (`purchase_invoice` / `buy_contract2`) — hiện không có %VAT theo dòng, phải làm mới
  hoàn toàn → chờ BA xác nhận.

## Quyết định chính (user chốt 22/10/2026)
- Không migration: cột `vat_percent` là `double(8,2)` / `double(16,2)`, đã đủ 2 số lẻ.
- Ô %VAT của HĐ đặt ở tab "Hàng hóa theo hợp đồng" (cạnh Đơn giá HĐ); tab "Hàng hóa - Chi phí" vẫn chỉ đọc.
- Vượt 100 → server báo đỏ, không tự kéo về 100.
- Dòng mới lấy %VAT theo DM; dòng đã lưu giữ %VAT đã nhập (trước đây màn sửa PI ghi đè lại theo DM).

## Sửa kèm
- Khuyến mại PI gửi `amount_after_vat` gõ nhầm (`amounta_after_vat`) → luôn lưu 0.
- Bản in PI / trang xem làm tròn %VAT (8.5 → 9).
