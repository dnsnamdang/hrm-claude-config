# Design tóm tắt — Đổi hàng trong phiếu đề xuất / phiếu xử lý cung ứng

> Phụ trách: @khoipv · Ngày: 2026-09-26 · Trạng thái: **spec xong, chờ user duyệt**
> Spec đầy đủ: [docs/superpowers/specs/2026-09-26-doi-hang-cung-ung-design.md](../../docs/superpowers/specs/2026-09-26-doi-hang-cung-ung-design.md)

## Mục tiêu

HĐ bán ký hàng **A**, khách đổi sang hàng **B**. Phiếu phải ghi được cặp (A danh nghĩa · B giao thật):
xuất hóa đơn / đối trừ HĐ vẫn là **A**, còn mua hàng + giao hàng là **B**.

## Quyết định lớn

- Chọn hàng vẫn chọn **A** từ HĐ, **Đổi** là bước 2 riêng; B chọn **tự do** từ danh mục.
- Mỗi dòng tối đa **1 hàng thay thế**, đổi **toàn bộ dòng**; **nhập SL riêng cho B** (mặc định = SL A).
- Đổi được ở **cả 2 màn**; phiếu xử lý kế thừa lúc lập rồi sửa độc lập — **không ghi ngược** lên đề xuất.
- Số liệu nguồn (tồn kho / đang mua / giá) và **toàn bộ ô phân bổ** của phiếu xử lý chạy theo **B**;
  SL đặt đơn theo HĐ, SL còn lại theo HĐ, validate vượt HĐ giữ theo **A**.
- Hiển thị: **dòng phụ nền vàng ngay dưới dòng A** — "↳ ĐỔI SANG: mã · tên · ĐVT · SL" + badge `ĐỔI` ở dòng chính.

## Dữ liệu

Thêm 8 cột `swap_*` (product_id/code/hh_code/name, unit_id/unit_name, quantity, reason) vào **cả 2 bảng**
`supply_proposal_products` và `supply_handling_products`. `swap_product_id IS NULL` = dòng không đổi.
Không bảng con, không khóa ngoại (chỉ index).

## Điểm cần lưu ý

- `handledQtyByProduct()` đổi khóa gom sang cặp `(product_id, swap_product_id)` — nếu không sẽ cộng nhầm đơn vị.
- Báo cáo **Nhu cầu mua** gom theo `COALESCE(swap_product_id, product_id)` ⇒ **số liệu báo cáo sẽ đổi**.
- Không sửa hóa đơn / kho. (Đơn mua hàng / HĐ mua: bổ sung đổi hàng NCC từ 28/09/2026 — xem mục mở rộng bên dưới.)

## Mở rộng 28/09/2026 — Đổi hàng trên Đơn mua / HĐ mua (làm lại, spec mục 11)

> Bản cũ (popup nhập 2 số / tỷ lệ, spec mục 10) đã hoàn tác — không dùng lại.

- Khách đổi hàng ở khâu mua: **hóa đơn + đối trừ HĐ bán vẫn theo A**, mua + giao theo **C**. Làm cho cả đơn mua lẫn HĐ mua.
- Thao tác như PĐX / PXL: nút **Đổi** (cột Thao tác) → popup chọn 1 hàng từ danh mục → **khối cặp**:
  dòng chính là C có chip `⇄ ĐỔI`, dòng phụ `↳ THAY CHO <A>` có ô **SL gốc nhập theo từng phiếu / HĐ bán**.
- SL gốc chỉ để **cảnh báo** (vượt đề xuất / vượt SL còn lại HĐ của A), không chặn lưu; BE chỉ bắt SL gốc > 0 khi phiếu có SL mua (HĐ nguyên tắc bỏ qua).
- PXL đã đổi A→B rồi đơn mua đổi tiếp → hàng gốc vẫn là **A** (lấy từ `purposes[].swap_for_*`).
- Dữ liệu: 9 cột `swap_from_*` trên `purchase_order_products` + `purchase_contract_products` (chỉ index); `purposes[].swapOrigQty` trong JSON.
- Endpoint `POST supply/purchase-orders|purchase-contracts/swap-info`: quy cách hàng mới + SL còn lại HĐ của hàng gốc.
- HĐ mua dòng đã đổi: đơn giá báo giá là giá của A (không quy đổi ĐVT), chiết khấu = 0.
- Chưa làm: Excel đơn mua / HĐ mua, đối trừ HĐ bán theo `swapOrigQty` ở màn sau.
