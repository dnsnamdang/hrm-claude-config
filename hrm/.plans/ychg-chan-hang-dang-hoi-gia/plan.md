# YCHG — chặn hàng đang được hỏi giá ở phiếu khác (QA 18/11/2026)

## Yêu cầu (tài liệu QA, dòng đỏ mục "Hàng được chọn")
- Hiện tại chỉ hiện cảnh báo "Đang được hỏi giá ở …" trong từng dòng, chưa chặn.
- Sửa: **1 hàng chỉ nằm trong 1 YCHG đang trong tiến trình** ⇒ chặn + báo "Hàng đang được hỏi giá ở <mã phiếu>".

## Nguyên nhân
`PriceAskingProductReader::blockReason()` trả `null` cho hàng trạng thái 1 Đang nhập thông tin / 3 Đang KD
trước khi xét `$askingIn` (YCHG khác đang Chờ PTKD / Đang hỏi giá, nhóm chưa đóng) ⇒ chỉ cảnh báo.

## Task
- [x] BE `blockReason`: hàng 1/3 có `asking_in` ⇒ `Hàng đang được hỏi giá ở <mã>` (gom message vào `askingMessage()`).
      Writer `validateInput` đã chặn theo `block_reason` ⇒ Lưu nháp lẫn Gửi đều 422 theo dòng `product_ids.i`.
- [x] FE `PriceAskingRequestForm.vue`: popup chọn hàng dùng chung (scope `price_asking`) vẫn liệt kê hàng này;
      chọn xong `onPickerSelect` lọc qua `dropBlocked()` (tách từ `prefill`) ⇒ bỏ hàng + toast kèm mã phiếu.
      Phiếu đang sửa vẫn nạp `keepBlocked` để thấy dòng, lưu sẽ bị BE báo lỗi dòng.
- [x] Test: `PriceAskingRequestApiTest::chon_hang_chan_dang_hoi_gia_va_loc_trang_thai` (block_reason + 422 nháp/gửi).
- [x] Playwright: nạp từ màn hàng hoá (?product_ids=) và popup Chọn hàng hoá → CH-PRO-8125 bị bỏ, toast "… (Hàng đang được hỏi giá ở PYCHG-03583)".

## Không đổi
- `applySelectableScope` (scope picker dùng chung) giữ nguyên — hàng vẫn hiện trong popup kèm dòng "Đang được hỏi giá ở …" để user biết vì sao bị bỏ.
- Phiếu Nháp không tính là "đang trong tiến trình" với hàng thường (như cũ `askingIn` không lấy Nháp).
