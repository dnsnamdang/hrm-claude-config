# N128 — Đo chứng từ dở dang của Hải Phòng có hàng không do HP làm chủ

Đo ngày 15/10/2026. Chỉ đọc (SELECT), không sửa code và không ghi DB.

- DB `hrm_erp` là dữ liệu gốc, chưa backfill, tức là tình trạng "hôm nay". Bản chụp dữ liệu mới nhất ngày **15/09/2026**.
- DB `hrm_erp_giacty` đã backfill, nhưng chạy theo **luật CŨ** (cụm 1-2-3-4). Xem mục "Việc treo" ở `ngoai-luong/soat-bang-c.md`.
- Chủ hàng = `products.company_id`, theo design P2c. Hàng "không do HP làm chủ" là hàng có chủ thuộc 1/3/4. Hiện HP chỉ làm chủ 3 mã.
- Luật mới: `config/price.php` (hrm-api `5ab7ab2ac`). Nhóm chia sẻ là `shared_price_company_ids` [1,3,4], nhóm tự quản là `self_managed_company_ids` [2,7].
- Code ERP đọc ở `wt-erp-2d1` (`af4780843f`), code hrm-api đọc ở `wt-chuyen-doi-hang-hoa/hrm-api` (`35d101453`).

## 1. Định nghĩa "dở" theo hằng số model

| Loại | Bảng (dòng hàng) | Trạng thái tính là "dở" |
|---|---|---|
| Báo giá đại lý/dự án ERP | `firm_quotations` (+ tab/group/combo/combo_group_option/promotions) | 1 Đang tạo, 2 Đã duyệt (chưa lập HĐ). Đã xong: 3 Đã lập HĐ, 4 Không hiệu lực |
| Hợp đồng/đơn ERP | `firm_contracts` (+ tab/group/combo/combo_group_option/promotions) | **Sửa được:** 1 Đang tạo, 2 Chờ duyệt, 4 Từ chối, 11 Gia hạn chờ duyệt. **Đang thực hiện:** 3 Có hiệu lực, 6 Đang xuất hàng, 9 Đang quyết toán. Đã xong: 5/7/8/10/12/13 |
| YC xuất hàng | `product_export_requests` + `product_export_request_details` | Các trạng thái trong `STATUS_PROCESING` (1,2,3,4,7,8,9,10,11,14–19) |
| YC mượn chuyển bán | `borrow_sell_requests` + `borrow_sell_request_products` | 1 Đã duyệt (chưa quyết toán), 10, 11, 12 |
| YC hỏi giá | `price_asking_requests` + `_products` | 2, 3, 5, 6, 7 (chưa tính giá / chưa kết thúc) |
| YC tính giá | `price_calculate_requests` | 2, 3 |
| Báo giá HRM `quotations`, báo giá/HĐ dịch vụ CSKH `wr_service_quotations`/`wr_service_contracts`, `service_quotations` | — | **HP có 0 phiếu** ở mọi trạng thái nên không đo tiếp |

## 2. Số liệu (`hrm_erp`, công ty 2)

| Loại chứng từ | Phiếu dở | Phiếu có hàng chủ 1/3/4 | Dòng hàng chủ 1/3/4 | Mã khác nhau | Mã có hệ số riêng HP (`pcc` cty 2) | trong đó hệ số ≠ 1 | Phiếu mới nhất | Phiếu tạo từ 15/06 |
|---|---|---|---|---|---|---|---|---|
| Báo giá ERP (`firm_quotations`) | 122 (đang tạo 105, đã duyệt 17) | 122 | 1.747 | 310 | 93 | 50 | 10/09/2026 | 40 |
| HĐ/đơn ERP, nhóm **sửa được** (1/2/4/11) | 56 | 56 | 1.570 | 94 | 75 | 43 | 14/09/2026 | 15 |
| HĐ/đơn ERP, nhóm **đang thực hiện** (3/6/9) | 465 | 465 | 13.245 | 218 | 122 | 77 | 15/09/2026 | 273 |
| YC xuất hàng (`product_export_requests`) | 14 | 14 | 26 | 20 | 14 | 11 | 14/09/2026 | 6 |
| YC mượn chuyển bán | 13 | 13 | 39 | 21 | 5 | 4 | 22/04/2026 | 0 |
| YC hỏi giá | 2 | 2 | 3 | 3 | 0 | 0 | 15/04/2026 | 0 |
| YC tính giá | 0 | — | — | — | — | — | — | — |
| **Tổng (gộp mã)** | **668** | **668** | **16.630** | **408** | **148** | **90** | 15/09/2026 | 334 |

Ghi chú:

- **Không chứng từ dở nào của HP có dòng hàng của chính HP** (0 dòng hàng chủ 2). Nghĩa là 100% chứng từ dở của HP dính hàng 1/3/4.
- Trong 408 mã có 7 mã đã xoá (`status=0`), còn 401 mã đang bán.
- HĐ/đơn tách theo loại (dòng = số phiếu / số mã):

  | Loại | Nhóm sửa được | Nhóm đang thực hiện |
  |---|---|---|
  | HĐ thường (1) | 36 / 67 mã | 100 / 135 mã |
  | **HĐ nguyên tắc (7)** | 5 / 41 mã | **160 / 151 mã** |
  | Đơn hàng nguyên tắc (8) | 10 / 28 mã | 145 / 93 mã |
  | Phụ lục bổ sung HĐNT (9) | 5 / 26 mã | 57 / 89 mã |
  | Khác (3, 10) | — | 3 |

- YCXH tách theo loại: 12 phiếu loại 14 (Xuất bán HĐ hàng), 4 phiếu loại 15 (KM HĐ hàng), 1 phiếu loại 99 (Khác). Các phiếu này đang tạo, đang lập đề nghị hoặc đang xuất kho.
- Báo giá tách theo loại: 111 phiếu BG hàng (loại 1), 11 phiếu BG HĐ nguyên tắc (loại 3).

## 3. Giá riêng HP và giá cụm

- **Hôm nay:** `product_unit_prices.company_id` đều NULL (một bộ giá chung). ERP tính giá HP bằng giá cụm × `pcc(HP)`; mã không có dòng `pcc` cty 2 thì hệ số là 1.
- Trong 408 mã: **148 mã có dòng hệ số riêng HP**, trong đó 90 mã có hệ số ≠ 1. 260 mã còn lại dùng giá cụm. 148 mã này nằm trong số 398 mã mà report đã nêu.

## 4. Sau backfill: HP còn đọc được giá không

| | Mã có dòng `product_unit_prices` cty 2 | `pcc` cty 2 status 3 |
|---|---|---|
| `hrm_erp` (hôm nay) | 0/408 (giá nằm ở dòng NULL, đủ 408/408) | — |
| `hrm_erp_giacty` (đã backfill **luật cũ**) | **401/408** (7 mã đã xoá) | 401 |
| **Luật mới 15/10** (`CompanyPriceBackfill`: HP không nhận B5) | **0/408**. HP chỉ còn giá của 3 mã HP làm chủ | 0 |

Kết luận: `giacty` hiện **không phản ánh** luật mới. Trên DB này HP vẫn có 173.082 dòng giá của 28.371 mã. Khi backfill theo luật mới, mọi đường đọc giá theo công ty chứng từ (= 2) sẽ trả rỗng cho cả 408 mã.

## 5. Code: mở/sửa phiếu dở đọc giá từ đâu (ERP `wt-erp-2d1`)

Mọi đường đều đọc theo **công ty chứng từ**, không lùi về công ty chủ hàng (G3). Khi thiếu dòng giá thì có 2 kiểu hỏng:

**(a) Im lặng ra giá 0**

- **Sửa báo giá ERP:**
  - Chuỗi gọi: `FirmQuotationController.php:250` → `FirmQuotationService::getDataForEdit` (`:545`) → `BaseQuotationProduct.php:127-129` `$product->dataFor($this->priceCompanyId())` → `app/Product.php:1371` → `:1142` `prices where company_id = HP`.
  - Ở FE, `partials/classes/sale/firm/quotation/FirmQuotationTabProduct.blade.php:66-72`: chế độ edit **không dùng giá đã lưu** (`_price` chỉ dùng khi `mode==='show'`) mà lấy `unit.prices` theo loại giá. Thiếu giá thì ra **0**.
  - Khi lưu, `:180` gửi `price: this.price`, tức **ghi đè 0 vào phiếu**.
  - **Hệ quả: cả 122 báo giá dở mở ra đều có đơn giá 0.**
- **YCXH loại 99 / loại đọc giá sống:** `ProductExportRequestDetail.php:169` `dataFor(công ty phiếu)`. JS `partials/classes/warehouse/ProductExportRequestDetail.blade.php:147-156` chỉ giữ `_price` cho loại 1,2,7,11,13–17. Các loại khác (ở đây là 1 phiếu loại 99) ra **0**.
- **hrm-api:** `ProductPriceReader::unitPrice/pricesByUnit` (`Modules/MasterData/Services/ProductPrice/ProductPriceReader.php:159-184`) trả 0 hoặc rỗng khi thiếu giá. Đường này dùng ở YCXH (`Modules/Assign/Services/ProductExportRequestService.php:498`, `ProductExportRequestPickerService.php:296`) và HĐ HRM (`ContractService.php:746-748`, `sale_max_percent`).

**(b) Ném lỗi, lưu thất bại**

`ProductPriceService::priceOf` (`app/Services/Product/ProductPriceService.php:112-125`) ném `PriceNotFoundForCompany`. Chỗ gọi `Product::getPriceByUnitAndType(...)->x` không bọc try:

- **Lập/sửa HĐ từ báo giá ERP:** `FirmContractService.php:848-853` (tab) và `:961-966` (nhóm) lấy `sale_max_percent`. Đường gọi: `saveFirmContractData` `:506` → `syncDataFromQuotation` `:616-632`. Riêng HĐ nguồn HRM (`syncTabsFromHrm` `:703-711`) có try/catch nên ra 0.
  - **Hệ quả: không lập được HĐ từ 17 báo giá đã duyệt, và không lưu lại được 56 HĐ đang tạo/chờ duyệt/từ chối.**
- **Tạo/sửa đơn hàng nguyên tắc:** `PrincipleOrderService.php:287-292` (`sale_max_percent`) và `:400` `validateDifferenceListPrice` (so với giá niêm yết của công ty HĐ).
  - **Hệ quả: 160 HĐ nguyên tắc đang hiệu lực (151 mã) không ra được đơn mới.** Đây là rủi ro lớn nhất vì việc bán hằng ngày đi qua đường này.
- **YCXH từ đơn nguyên tắc, gửi duyệt:** `ProductExportRequestsController.php:2188` `checkDiffPrice` (`->price ?? 0` không bắt được exception).
- **Mượn chuyển bán:** `BorrowSellRequestsController.php:676` (cùng kiểu).
- **Lập HĐ từ báo giá:** `FirmQuotationService::getDataForContract` `:720-722` join `pp.company_id = HP`, ra `sale_max_percent` NULL (im lặng). Sau đó lưu thì vấp lỗi ở `:848`.

**Không vỡ:** màn Xem/In (dùng `_price`), và HĐ đã có hiệu lực khi chỉ xem. Xuất hàng loại 14/15 (YCXH bán HĐ hàng) dùng giá lưu trên phiếu (`ProductExportRequestDetail.blade.php:148`). Ngoại lệ là xuất ghép/tách (`ProductExportsController.php:771`, ném lỗi).

## 6. Kết luận rủi ro

Bật luật mới mà không xử lý gì thì HP **gãy ngay ngày go-live**:

- 122 báo giá dở mở ra đơn giá 0, lưu là ghi đè 0.
- 56 HĐ chưa duyệt và 17 BG đã duyệt không lưu hoặc lập HĐ được.
- 160 HĐ nguyên tắc đang hiệu lực không ra được đơn hàng mới.

Tổng cộng 668 phiếu và 408 mã. Đây là các lỗi cứng hoặc im lặng, không có cảnh báo cho người dùng. Phiếu đang thực hiện (465) chỉ xem hoặc xuất theo giá đã lưu thì vẫn chạy.

## 7. Phương án

**PA1 — "Lấy về" trước go-live cho các mã HP đang dùng** (đường 2-C2, chạy một lần trong backfill)

- Cách làm: chép cho HP giá hôm nay (giá cụm × `pcc(HP)`, giống luật cũ) của **408 mã** đang có trên chứng từ dở. Có thể thu hẹp: mã trên HĐ nguyên tắc/HĐ hiệu lực cộng BG 3 tháng gần nhất.
- Hệ quả tốt: chứng từ dở và HĐNT chạy y như hôm nay, giá không đổi, không phải sửa code.
- Hệ quả xấu:
  - HP phải tự bảo trì giá ~400 mã. Khi chủ đổi giá, HP không tự cập nhật, đúng tinh thần "tự quản".
  - Danh sách cần user chốt.
  - Lệnh so khớp (`product-price:compare`) phải coi những cặp này là hợp lệ.

**PA2 — Đóng sổ chứng từ HP trước go-live, giữ luật thuần**

- Cách làm: HP hoàn tất hoặc huỷ 122 BG và 56 HĐ chưa duyệt. HĐNT hiệu lực phải lập lại sau go-live bằng hàng HP "lấy về" theo nhu cầu.
- Hệ quả tốt: dữ liệu sạch, đúng design P2c.
- Hệ quả xấu:
  - Phụ thuộc vận hành, vì 334 phiếu tạo trong 3 tháng gần nhất.
  - 160 HĐNT đang dùng sẽ ngừng ra đơn cho tới khi HP lấy về từng mã. Gián đoạn bán hàng là chắc chắn.

**PA3 — Giá đã lưu trên phiếu là chuẩn (sửa code) + PA1 thu hẹp**

- Cách làm:
  - Sửa 3 điểm: FQ edit dùng `_price` cho dòng đã có (`FirmQuotationTabProduct.blade.php:66`), bọc `sale_max_percent` thiếu giá là 0 (`FirmContractService.php:848, :961`, `PrincipleOrderService.php:287`), và `checkDiffPrice` dùng `priceOrNull`.
  - Chỉ "lấy về" các mã trên **HĐNT đang hiệu lực** (151 mã), vì đơn mới bắt buộc so giá niêm yết.
- Hệ quả tốt: phiếu dở không vỡ và không ghi đè 0; số mã HP phải tự quản ít hơn.
- Hệ quả xấu:
  - Phải sửa code ERP: thêm phạm vi, cần user cho phép.
  - Đổi hành vi "mở sửa BG thì lấy giá mới" thành giữ giá cũ.
  - Dòng thêm mới vẫn trống giá (đúng luật).

Khuyến nghị: PA1, hoặc PA3 nếu muốn giảm số mã HP tự quản. Cả hai đều cần user chốt danh sách mã và thời điểm chép. Dù chọn phương án nào, nên sửa phần (b) ném lỗi thành thông báo rõ ràng, vì 5/6/8 và HP sau này cũng sẽ gặp khi thêm hàng chưa lấy về.
