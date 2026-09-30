# Design — Báo giá kế thừa "Ghi chú cung ứng" của lần trước

Phụ trách: @khoipv — 25/09/2026
Spec đầy đủ: [docs/superpowers/specs/2026-09-25-bao-gia-ke-thua-ghi-chu-cung-ung-design.md](../../docs/superpowers/specs/2026-09-25-bao-gia-ke-thua-ghi-chu-cung-ung-design.md)

## Mục tiêu
Khép kín vòng ghi chú cung ứng giữa Báo giá và chứng từ mua:
- **Chiều xuôi (đã có)**: Đơn mua hàng / HĐ mua nhập ghi chú theo từng HĐ bán → ghi đè `quotation_tab_products.note_supply` của báo giá gốc.
- **Chiều ngược (feature này)**: lập báo giá MỚI cho cùng khách + cùng hàng → ô "Ghi chú cung ứng" tự ăn theo ghi chú của **chứng từ mua gần nhất**.

## Scope
| Trong phạm vi | Ngoài phạm vi |
|---|---|
| Màn Báo giá `plan/quotation` (lập mới + sửa) | Màn Hợp đồng bán, Gói thầu |
| Nguồn: Đơn mua hàng **và** HĐ mua | Backfill dữ liệu báo giá cũ |
| Khớp đúng `customer_id` + `product_id` | Hiển thị nguồn ghi chú (mã đơn mua) trên lưới |

## Quyết định lớn
1. Đổ ghi chú **ngay khi chọn hàng / đổi khách hàng** (không chờ lúc lưu) — đúng pattern cột "Giá bán HĐ trước".
2. "Gần nhất" tính theo **chứng từ mua**, không phải theo báo giá; Đơn mua hàng và HĐ mua cạnh tranh nhau, cái lưu sau thắng.
3. Khớp khách hàng **chặt** (`customer_id`), không fallback theo tỉnh.
4. Ô "Ghi chú cung ứng" vẫn **chỉ đọc**; ghi chú thật của báo giá không bao giờ bị giá trị kế thừa đè.
5. Không thêm bảng, không migration — tra thẳng mảng JSON `purposes` bằng `JSON_TABLE` (MySQL 8).

## Đụng vào
- BE: `Modules/Supply/Services/SupplyNoteLookupService.php` (mới), `ProductController` + `Routes/api.php` (Category), comment ở `QuotationService::syncGroups()`.
- FE: `utils/previousSupplyNote.js` (mới), `pages/plan/quotation/components/ProductComponent.vue`, `GeneralComponent.vue`.
- ⚠️ Sửa cả BE lẫn FE → build lại client + hard refresh. Không migration.
