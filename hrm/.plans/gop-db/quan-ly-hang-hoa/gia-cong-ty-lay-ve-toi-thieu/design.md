# Giá công ty lấy về ≥ giá công ty tạo — thiết kế

> 21/10/2026 · nhánh `gop_db`. Yêu cầu user: "Khi công ty B lấy hàng hoá của Công ty A về kinh doanh thì validate Giá của
> Công ty B phải >= giá Công ty A". Khảo sát: chưa có quy tắc so giá giữa công ty nào (các chốt cũ: mỗi công ty tự quản giá,
> chính sách nội bộ chỉ gợi ý — quy tắc này là RÀNG BUỘC MỚI, không đổi các chốt đó).

## Chốt với user (21/10)

| # | Câu | Chốt |
|---|---|---|
| Q1 | Chặn ở đâu | **Mọi đường ghi giá của B**: Phiếu tính giá (lưu và duyệt / gửi duyệt) · màn Cập nhật giá bán · Duyệt giá (người duyệt sửa giá) |
| Q2 | Loại giá | **Cả 6 loại** (Bán lẻ, ĐL1/2/3, Giá bán theo lô, TMĐT) — so CÙNG loại, CÙNG ĐVT (`product_unit_id`) |
| Q3 | A chưa có giá | Giá A = 0 hoặc 1 đ ("chưa có giá" theo quy ước) ⇒ **bỏ qua** loại giá đó |
| Q4 | Mốc so | **Giá A đang áp dụng** (`upp.price` của A, không tính giá A chờ duyệt). Áp cho cả giá hiện hành lẫn **giá hiệu lực** B khai. A đổi giá sau ⇒ không tự sửa B, chỉ chặn lần B lưu tiếp; **cron áp giá hiệu lực không chặn** |
| Q5 | Mức chặn | **Chặn cứng** 422, báo dưới ô giá: "Không được thấp hơn giá <Loại giá> của <mã công ty A> (<giá>)"; mọi ô sai báo cùng lúc |

## Phạm vi áp
- "Công ty A" = công ty tạo hàng (`products.company_id`). Chỉ áp khi công ty ghi giá (B) ≠ A. A tự sửa giá của mình: không áp.
- So giá ĐƯỢC LƯU / ĐỀ NGHỊ: giá trị B gửi lên (giá hiện hành + từng dòng giá hiệu lực). TMĐT do BE tự tính từ Bán lẻ ⇒ so
  sau khi BE tính.

## Thiết kế (dự kiến)
- BE: 1 lớp dùng chung `OwnerPriceFloor` (MasterData/Services/ProductPrice): `floors(productId, companyId)` ⇒
  `[product_unit_id][price_type_id] => giá A` (bỏ 0 / 1 đ, null khi B = A) + `violations(rows)` ⇒ lỗi theo khoá ô của từng
  màn. Gọi ở: `ProductPriceUpdateService::validate`, `ProductPriceApprovalService::validateEdits` (+ giá đề nghị khi duyệt),
  `ProductPriceApprovalSubmitter` (gửi duyệt), `PriceCalculateWriter::submit` (lưu và duyệt / gửi duyệt). Một nguồn để 3 màn
  báo cùng câu.
- FE: 3 màn đã hiện lỗi 422 theo khoá ô — kiểm map khoá lỗi mới về đúng ô; không tự tính trước ở FE (skill form-validate:
  FE chỉ định dạng, nghiệp vụ để BE).
- Test: PHPUnit mỗi đường (B thấp hơn ⇒ 422 đúng ô · bằng ⇒ OK · A = 0/1 đ ⇒ OK · A tự sửa ⇒ OK · giá hiệu lực) + Playwright 3 màn.

## Đã làm (21/10 — ĐÃ PUSH gop_db: api `fe099fb5b` + merge `7fa0b01ff`)
- BE: `ProductPrice/OwnerPriceFloor.php` + gắn ở `ProductPriceUpdateService` (khoá `prices.{i}.price` / `.expected_prices.{j}.price`),
  `ProductPriceApprovalService::validateEdits` (khoá `{paId}.{papId}.price` — mọi dòng sẽ ghi, kể cả đề nghị không sửa),
  `PriceCalculateWriter::submit` (khoá `rows.{i}.prices.{loại}.price`, cùng lượt với C15; Lưu nháp không chặn).
  Giá hiệu lực TMĐT (suy từ Bán lẻ) báo ở ô giá hiệu lực Bán lẻ. Khai `tests/fixtures/price-readers.txt`.
- PHPUnit: `OwnerPriceFloorApiTest` 6/6 + ca mới `PriceCalculateApiTest::gia_cong_ty_lay_ve_…`; các bộ giá liên quan xanh
  (trừ `ExpectedPriceApplyTest::chot_chan_…` — cần dữ liệu "giá quá hạn chưa dọn" mà DB local đã dọn lúc go-live, không liên quan).
- FE: không sửa (3 màn đã map lỗi 422 theo khoá ô). Chưa mở được màn trên local: menu Tài chính › Cập nhật giá bị ẩn ở Cài đặt phân hệ.
