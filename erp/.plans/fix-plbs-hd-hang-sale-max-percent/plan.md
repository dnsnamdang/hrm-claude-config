# Fix: Phụ lục bổ sung HĐ hãng cảnh báo "chưa có giá (loại giá N)" chặn lưu

## Bối cảnh
Màn **Tạo phụ lục bổ sung HĐ hãng** (`FirmContractAdditionAnnexesController@store` → `FirmContractService::store`) hiện lên toast cảnh báo
`Hàng hoá #5371 chưa có giá (loại giá 1) tại công ty #4` và **không lưu được** khi báo giá có hàng chưa khai giá ở công ty của phụ lục.

## Root cause (systematic-debugging Phase 1-3, đã xác nhận bằng tinker)
`FirmContractService` đọc `Product::getPriceByUnitAndType(...)->sale_max_percent` ở 3 chỗ:
- Dòng **709** (`syncProducts`, nhánh products trực tiếp): **đã** bọc try/catch → `sale_max_percent = 0`. ✓
- Dòng **849** (`syncProductsFromQuotation`): **CHƯA** bọc → ném `PriceNotFoundForCompany`. ✗
- Dòng **962** (`syncGroupsFromQuotation`): **CHƯA** bọc → ném `PriceNotFoundForCompany`. ✗

`getPriceByUnitAndType` → `ProductPriceService::priceOf` ném `PriceNotFoundForCompany` khi không có dòng
`product_unit_prices` cho (ĐVT × công ty × loại giá). SP 5371 chỉ có giá ở cty 1 (đủ 6 loại), không có dòng nào ở cty 4
→ phụ lục lập cho cty 4 ném lỗi, bubble lên Handler → toast, chặn cả lưu.

`sale_max_percent` chỉ là **% giảm giá tối đa** (trần chiết khấu dùng tính `net_price`); giá bán thật lấy từ báo giá.
Thiếu nó phải mặc định 0 (không có trần), KHÔNG được chặn lưu — đúng như dòng 709 đã làm. Hai nhánh từ báo giá bị bỏ sót.

Tiền lệ cùng loại: memory `erp-dhnt-validate-gia-chi-sl-lon-hon-0` (ĐHNT) — validate giá không được chặn thao tác lưu.

## Tasks
- [x] Phase 1: Reproduce + xác định root cause (tinker: `getPriceByUnitAndType(5371,41,1,4)` ném đúng câu báo)
- [x] Phase 4: Bọc try/catch → `sale_max_percent = 0` cho `syncProductsFromQuotation` (FirmContractService ~849), mirror dòng 709
- [x] Phase 4: Bọc try/catch → `sale_max_percent = 0` cho `syncGroupsFromQuotation` (FirmContractService ~967), mirror dòng 709
- [x] Verify: tinker xác nhận guard nuốt lỗi → `sale_max_percent = 0`, luồng lưu không còn ném; `php -l` sạch
- [x] Rà biến thể nha khoa: `ZTFirmContractService` có cùng lỗi ở 2 chỗ (~662, ~745) → đã bọc try/catch luôn

## Kết quả
5 điểm đọc `getPriceByUnitAndType(...)->sale_max_percent` nay đều guard (3 ở FirmContractService: 709 cũ + 849 + 967; 2 ở ZTFirmContractService: 662 + 750). Thiếu dòng giá ⇒ trần chiết khấu 0, phụ lục bổ sung lưu bình thường. CHƯA commit/push (chờ user).

## Không làm (tránh mở rộng scope)
- KHÔNG đổi ngữ nghĩa `sale_max_percent` hay cách tính `net_price`/`standard_price`.
- KHÔNG backfill dữ liệu giá cty 4 (đó là việc nghiệp vụ của user, không phải bug code).
