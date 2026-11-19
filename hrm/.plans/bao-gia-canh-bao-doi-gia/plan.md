# PLAN — #10791 Cảnh báo đơn giá thay đổi khi sửa báo giá (điều tra phản hồi tester)

Phản hồi tester (Redmine #10791, 5 ngày trước): "Thay đổi giá hàng hóa trên ERP → vào lại báo giá
không thấy cảnh báo".

## Kết quả điều tra (2026-08-18) — TÁI HIỆN ĐƯỢC, không phải lỗi logic HRM
- HRM so đơn giá đang lưu với `dev_erp.product_unit_prices.price` (giá ĐANG hiệu lực):
  `edit.vue::repriceErpRows` → `POST assign/quotations/erp-reprice` → `QuotationService::repriceErpItems`
  → `TpProductUnitPrice::getUnitOptions`.
- ERP sửa giá KHÔNG ghi thẳng bảng đó: `TanPhatDev/app/Http/Controllers/ProductApprovesController.php:221`
  ép `effect_date >= ngày mai`, ghi vào `product_expected_prices`; cron
  `product:update_price` (`app/Console/Commands/UpdateProductPrice.php`) mới copy sang `product_unit_prices`
  đúng ngày hiệu lực.
- ⇒ Đổi giá hôm nay → mở lại báo giá hôm nay: giá hiệu lực chưa đổi → không cảnh báo.

## Test đã chạy (BG-2026-00240, Đang tạo, DNS Admin, AUD, bảng giá Bán lẻ)
- [x] Baseline: 0 dòng lệch → không popup
- [x] Mô phỏng đổi giá trên ERP hôm nay (`product_expected_prices` = 32.713.560, hiệu lực ngày mai,
      status=2): mở màn Sửa → **KHÔNG có popup** ⇒ tái hiện đúng phản hồi.
      Chi tiết: FE vẫn NHẬN biết giá dự kiến — ô "Hiệu lực báo giá" tự rút về 19/08/2026 — nhưng
      logic cảnh báo chỉ so giá hiện hành.
- [x] Mô phỏng tới ngày hiệu lực (ghi thẳng `product_unit_prices` = 32.713.560): mở lại → **popup hiện**
      "Đơn giá hàng hoá đã thay đổi … 0 → 2.000 VNĐ"; bấm Đồng ý → giá bán lưới + tổng = 2.000 AUD
      (~32.713.560 VND) ⇒ AC3/AC4 chạy đúng.
- [x] Dọn dữ liệu test: trả `product_unit_prices` 250815 về 1.00, 157810 về 119.000.000, xoá 2 dòng
      `product_expected_prices` thêm tay. Báo giá 240 KHÔNG bấm Lưu → DB nguyên vẹn (quoted_price 0.00).

## Thao tác THẬT trên ERP :8001 (Cập nhật nhanh giá hàng hoá, mã CH-BOMAYTINH:05)
ERP có 2 cách đổi giá trên cùng 1 màn — kết quả khác hẳn nhau:

| Cách làm | ERP ghi vào đâu | HRM mở lại báo giá |
|---|---|---|
| Sửa ô **"Giá mới"** ở dòng *Đang áp dụng* rồi bấm lưu | `product_unit_prices.price` đổi **NGAY** (công ty 1 có `is_company_price = 0` ⇒ không cần duyệt) | **CÓ popup** "Đơn giá hàng hoá đã thay đổi" ✅ |
| Bấm **"Thêm giá hiệu lực"**, nhập giá + ngày (bắt buộc ngày tương lai) | Chỉ tạo `product_expected_prices` (40.000.000, hiệu lực 19/08); `product_unit_prices.price` GIỮ NGUYÊN | **KHÔNG popup** — chỉ hiện icon ⚠ cạnh mã hàng + "Hiệu lực báo giá" rút về 19/08/2026 |

⇒ Chức năng #10791 CHẠY ĐÚNG với cách 1. Tester không thấy cảnh báo nhiều khả năng vì dùng cách 2
(giá dự kiến), hoặc môi trường test bật duyệt giá (`companies.is_company_price = 1` ⇒ giá vào
`price_wait_approve`, phải TP duyệt mới đổi), hoặc sửa loại giá khác bảng giá của báo giá.

## Lỗi phụ phát hiện
- [ ] Popup ghi sai đơn vị tiền: "0 → 2.000 **VNĐ**" trong khi báo giá đang là **AUD**
      (`edit.vue` ~dòng 3177 hardcode "VNĐ") → phải lấy mã tiền tệ của báo giá.
- [ ] `canEdit` (edit.vue:1563) yêu cầu người đăng nhập là NGƯỜI TẠO báo giá → mở báo giá người khác
      tạo cũng không có popup. Cần hỏi tester test trên phiếu nào để loại trừ.

## Hướng xử lý ĐÃ CHỐT (user chốt 2026-08-18): GIỮ NGUYÊN
- KHÔNG so với `product_expected_prices`. Chỉ cảnh báo khi giá ĐÃ có hiệu lực
  (`product_unit_prices.price` đổi) — vì bấm Đồng ý trên giá chưa hiệu lực sẽ chốt sai giá bán tại
  thời điểm ký hợp đồng.
- Việc cần làm: trả lời tester trên Redmine #10791 (nội dung đã soạn, xem mục dưới), KHÔNG sửa logic.
- Giá dự kiến vẫn đang được thể hiện ở màn Sửa: icon ⚠ cạnh mã hàng (tooltip "Giá bán thay đổi
  ngày dd/mm") + tự rút "Hiệu lực báo giá" về ngày đổi giá gần nhất.

## Phản hồi #12 Redmine #10791 (2026-10-16, nhánh develop) — link mã hàng sang ERP
User chốt: chỉ làm ý "gắn hyperlink vào mã sản phẩm", link sang màn chi tiết hàng hoá bên ERP (`/admin/products/{id}/show`). Ý F/PE (TC_2.1022, TC_2.1026) tạm để.
- [x] `utils/erp-link.js`: thêm `erpProductUrl(erpProductId)` + khai `ERP_PATHS.productShow`
- [x] Màn Xem chi tiết báo giá (`quotations/_id/index.vue`) + Làm giá (`quotations/_id/edit.vue`): mã hàng ERP (dòng cha + dòng con) thành link `v2-cell-link`, mở tab mới; hàng tạm giữ chữ thường
- [x] Test 16/10: hàm `erpProductUrl` đúng với ERP_URL có/không có `/` cuối, thiếu ERP_URL → '' (hiện chữ thường); BG-2026-00093 màn Chi tiết + Làm giá: 2 hàng ERP có link (navy, gạch chân đứt, chữ thường), 4 hàng tạm HHBG chữ thường; bấm link mở tab mới, màn Làm giá giữ nguyên; route `/admin/products/{id}/show` tồn tại trên dev-erp + erp prod (302 sang SSO). Chưa có dữ liệu hàng con là hàng ERP để thử (cùng khuôn với dòng cha). Ảnh: test-phan-hoi-12/
- Ghi nhận: local `ERP_URL` comment, nuxt.config fallback `TP_URL` = qttt.tanphat.com (domain cũ) → link local 404; dev/prod cấu hình đúng
