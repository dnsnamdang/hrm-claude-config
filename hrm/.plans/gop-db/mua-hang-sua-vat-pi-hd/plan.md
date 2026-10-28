# Plan — mua-hang-sua-vat-pi-hd (#11833)

Spec: [2026-10-22-mua-hang-sua-vat-pi-hd-design.md](../../../docs/superpowers/specs/gop-db/2026-10-22-mua-hang-sua-vat-pi-hd-design.md)
Repo ERP `TanPhatDev`, nhánh `gop_db`. Chưa commit.

## Phase 1 — Khảo sát + chốt phạm vi
- [x] Đọc issue + 2 ảnh; khảo sát 3 luồng (form, JS tính tiền, store/update, cột DB, PI → HĐ, downstream)
- [x] Phát hiện luồng nhập khẩu không có %VAT theo dòng → user chốt làm trong nước trước, nhập khẩu hỏi BA
- [x] Kiểm cột DB: `double(8,2)` / `double(16,2)` → bỏ migration `decimal(5,2)` đã định

## Phase 2 — PI trong nước
- [x] `public/js/app.js`: hàm mới `parsePercentInput(value, maxDecimals)`
- [x] `InlandPurchaseInvoiceProductDelivery`: getter/setter `vat_percent` (số) + `vat_percent_input` (ô nhập);
      chỉ lấy %VAT theo DM khi dòng chưa có giá trị (hết ghi đè ở màn sửa)
- [x] `InlandPurchaseInvoicePromotion`: như trên + sửa `amounta_after_vat` → `amount_after_vat`
- [x] `inland_purchase_invoice/form.blade.php`: ô nhập %VAT dòng hàng (khóa khi có rule contract) + khuyến mại, hiện lỗi
- [x] `PIStoreRequest`: rule `vat_percent` (dòng hàng + khuyến mại) + thông báo tiếng Việt

## Phase 3 — HĐ mua trong nước
- [x] `InlandBuyContractNewProductDetail`: getter/setter `vat_percent` + `vat_percent_input`
- [x] `inland_buy_contract_new/form.blade.php`: cột %VAT sau "Thành tiền" ở tab "Hàng hóa theo hợp đồng",
      `colspan` dòng sản phẩm 4 → 5, `ng-change` tính lại bảng tổng hợp
- [x] `InlandBuyContractNewController` store + update: rule `products.*.details.*.vat_percent` + thông báo

## Phase 4 — Hiển thị số lẻ
- [x] `PrintPurchaseInvoiceDetailService`: `formatCurrency(vat_percent, 2)` cho dòng hàng / khuyến mại / chi phí
- [x] Trang xem HĐ (khuyến mại) + PI (chi phí): `| number:0` → `| number`

## Phase 5 — Verify
- [x] `php -l` các file PHP sạch
- [x] Browser local, màn sửa PI 1495: mở lên giữ 8 (đã lưu); gõ "8,5" → 8.5, VAT 382,500, tổng 4,882,500;
      gõ "7.255" → 7.25; `submit_data` gửi đúng; không lỗi JS
- [x] Browser màn tạo / sửa HĐ mua: ô %VAT, tab tổng hợp + tổng VAT / giá trị HĐ cập nhật
- [x] Lưu thật PI + HĐ (server lưu đúng, mở lại giữ giá trị, nhập > 100 báo đỏ)
- [ ] Dev-erp: QA test lại theo issue

## Phase 6 — Test trọn luồng thật trên local (22/10/2026)
Chạy qua giao diện local (Playwright), mỗi bước đối chiếu DB:

| Bước | Kết quả |
|---|---|
| Sửa PI 1495: %VAT 150 → Lưu | Server chặn, chữ đỏ "%VAT tối đa 100" dưới ô |
| %VAT 8,5 → Lưu | DB 8.5 (DM 8.00), VAT 382,500; mở lại màn sửa vẫn 8.5; trang xem 8.5 |
| Thêm khuyến mại PI, %VAT 6,5 → Lưu | DB 6.5, VAT 13,000, **tiền sau VAT 213,000** (trước lỗi gõ nhầm luôn 0) |
| Gửi duyệt → Duyệt PI | Trạng thái 1, %VAT dòng / khuyến mại giữ 8.5 / 6.5 |
| Lập HĐ từ PI đã duyệt | Dòng HĐ mặc định 8.5, khuyến mại 6.5, tổng VAT 395,500, giá trị 5,095,500 = PI → lưu, DB khớp |
| Lập HĐ từ PI 2194 (%VAT 8), sửa 5,25 → Lưu | DB 5.25, tổng VAT 614,775, giá trị 12,324,775 |
| Sửa HĐ: mở lại giữ 5.25; 150 → báo đỏ; 10 → Lưu | DB 10, tổng VAT 1,171,000, giá trị 12,881,000; trang xem khớp |
| Bản in PI | In 8.5 / 6.5 (trước làm tròn) |

Sửa thêm phát hiện khi test:
- [x] `InlandBuyContractNew.caculatePromotions`: chép khuyến mại PI bằng `...promotion` → `vat_percent` (giờ là getter
      trên prototype) không được chép → khuyến mại HĐ mất %VAT. Gán rõ `vat_percent: promotion.vat_percent`.
- [x] `InlandPurchaseInvoiceController@update` không ghi `total_pay` (chỉ store ghi) → tổng PI trong DB cũ. Thêm ghi khi có.
- Dữ liệu test (2 HĐ, sửa PI 1495, dòng phân công người mua tạm id 2624) đã trả lại như cũ.
- Popup tìm hàng (thêm khuyến mại) gọi API HRM, local không kết nối → test bằng `addProduct({id})` (bỏ qua mỗi popup).

## Phase 7 — Khuyến mại HĐ cho sửa %VAT + chỉnh cỡ ô (23/10/2026, user yêu cầu)
- [x] PI: ô %VAT dòng hàng + khuyến mại cố định cột 90px / ô 80px (trước hẹp — "7.25" hiện ".25"; rồi bảng khuyến mại
      giãn làm ô quá to)
- [x] `InlandBuyContractNewPromotion`: getter/setter %VAT (xét cả `_vat_percent` khi đầu vào là object đã spread)
- [x] Form HĐ: ô %VAT khuyến mại; controller store + update: rule + thông báo `promotions.*.vat_percent`
- [x] Test thật local (nhánh `task_11833`): lập HĐ từ PI 2194, thêm khuyến mại → mặc định 8 (DM); sửa 7,5 → VAT 45,000,
      tổng VAT 981,800, giá trị 13,291,800 → lưu, DB 7.5. Sửa HĐ: mở giữ 7.5; 150 → đỏ "%VAT tối đa 100"; 9,25 → lưu,
      DB 9.25 / 55,500, tổng 992,300 / 13,302,300; trang xem khớp. Đã xoá HĐ test + phân công tạm 2625.
- Ảnh: `C:\Users\Legion\.pw-mcp\out-a\vat-11833-hd-khuyen-mai*.png`, `vat-11833-pi-o-vat.png`

## Checkpoint — 2026-10-22
- Vừa hoàn thành: Phase 1-6, test trọn luồng PI → duyệt → HĐ trên local.
- Đang làm dở: không.
- Bước tiếp theo: user commit; QA test trên dev-erp; hỏi BA phạm vi luồng nhập khẩu.
- Blocked: không.
