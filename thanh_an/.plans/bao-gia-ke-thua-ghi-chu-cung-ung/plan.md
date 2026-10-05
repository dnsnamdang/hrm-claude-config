# Plan — Báo giá kế thừa "Ghi chú cung ứng" của lần trước

Phụ trách: @khoipv
Màn: `plan/quotation` (add/edit) · Nguồn dữ liệu: `Modules/Supply`
Spec: [docs/superpowers/specs/2026-09-25-bao-gia-ke-thua-ghi-chu-cung-ung-design.md](../../docs/superpowers/specs/2026-09-25-bao-gia-ke-thua-ghi-chu-cung-ung-design.md)

## Yêu cầu (user 25/09/2026)
Ghi chú ở Đơn mua hàng đã đẩy ngược về `quotation_tab_products.note_supply` (feature `don-mua-ghi-chu-ve-bao-gia`) — GIỮ NGUYÊN.
MỚI: lập báo giá tiếp theo cho **cùng khách hàng + cùng hàng hóa** thì ô "Ghi chú cung ứng" tự ăn theo ghi chú của **lần mua gần nhất**;
báo giá đó đến giai đoạn mua hàng, có ghi chú mới thì lại ghi đè ngược về chính nó (luồng cũ).

## Quyết định đã chốt với user
1. **Thời điểm**: đổ ngay khi chọn hàng / đổi khách hàng (pattern cột "Giá bán HĐ trước"), bấm Lưu thì ghi vào DB báo giá mới.
2. **Nguồn**: chứng từ mua **gần nhất** — tính **cả Đơn mua hàng lẫn HĐ mua**.
3. **Khách hàng**: đúng `customer_id`, **không** nới theo tỉnh.
4. **Không có chứng từ mua** → để trống, không đoán.
5. **Ô "Ghi chú cung ứng"** ở báo giá vẫn **chỉ đọc**.

## BE
- [x] `Modules/Supply/Services/SupplyNoteLookupService.php` — `latestNotesByCustomer($customerId, $productIds)`; 2 truy vấn `JSON_TABLE` (MySQL 8.0.30) bóc `purposes` của `purchase_order_products` + `purchase_contract_products`, join `contracts` lọc theo khách; loại chứng từ xóa mềm; bỏ ghi chú trắng; gom 2 nguồn lấy `updated_at` mới nhất
- [x] `ProductController::getPreviousSupplyNote()` + route `POST category/products/previous-supply-note` (đặt cạnh `previous-contract-price`)
- [x] `QuotationService::syncGroups()` — **không đổi logic** (fill payload trước, map DB đè sau đã đúng thứ tự ưu tiên), chỉ bổ sung comment
- [x] `php -l` 4 file sạch · `route:list` thấy route mới

## FE
- [x] `utils/previousSupplyNote.js` — helper dùng chung (tránh lặp như bài học 6 bản copy của `previousContractPrice`)
- [x] `pages/plan/quotation/components/ProductComponent.vue` — import helper + method `fetchPreviousSupplyNotes()`, gọi ở 2 điểm (chọn hàng xong, import excel)
- [x] `pages/plan/quotation/components/GeneralComponent.vue` — gọi qua `$refs.product` ở 2 điểm (chọn dự án, đổi khách hàng)
- [x] Chỉ điền ô trống hoặc ô do chính helper điền (cờ tạm `note_supply_inherited`) → ghi chú thật không bị đè, đổi khách thì kế thừa được thay/xóa
- [x] Ô vẫn chỉ đọc, không đụng template; không phải sửa payload submit (add/edit gửi nguyên `groups`)
- [x] Compile sạch (vue-template-compiler + @babel/parser)

## Verify tự động (transaction + rollback, DB `thanhan_stag_07052026`)
- [x] `SupplyNoteLookupService` **14/14 PASS** (xem mục 8 của spec)
- [x] `QuotationService::syncGroups()` **4/4 PASS**: nhận kế thừa · ghi chú thật không bị đè · FE không gửi thì giữ nguyên · tra không ra → trống
- [x] DB sau kiểm thử nguyên vẹn

## Còn lại — user test UI
- [ ] Lập báo giá mới cho khách đã từng mua hàng → chọn hàng → cột "Ghi chú cung ứng" hiện ghi chú của lần mua gần nhất
- [ ] Đổi sang khách khác → ghi chú kế thừa đổi theo / xóa trắng
- [ ] Lưu báo giá → mở lại vẫn còn ghi chú
- [ ] Nhập ghi chú mới ở Đơn mua hàng cho báo giá đó → lưu → báo giá nhận ghi chú mới (ghi đè kế thừa)
- [ ] Mở sửa báo giá đã có ghi chú thật, chọn thêm hàng → ghi chú cũ không bị đè

### Checkpoint — 2026-09-25
Vừa hoàn thành: Toàn bộ BE (1 file mới + controller + route + comment) và FE (1 helper mới + 2 component). Verify tự động 18/18 PASS, DB đã rollback sạch.
Đang làm dở: (không)
Bước tiếp theo: ⚠️ Sửa cả BE lẫn FE → **build lại client + hard refresh**, rồi user test 5 luồng UI ở trên.
Blocked:
