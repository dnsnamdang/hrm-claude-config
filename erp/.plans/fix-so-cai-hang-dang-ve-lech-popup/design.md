# Fix: Báo cáo luân chuyển — cột "Hàng đang về / Tồn kho" lệch với popup Chi tiết

## Hiện tượng
Màn `admin/stock-transfer/report`. Mã `GC-GC-40PRO-A:06`: cột **Hàng đang về / Tồn kho = 18**,
bấm vào popup Chi tiết cộng ra **56** (2 + 24 + 2 + 28). User báo lỗi lặp lại nhiều lần, nhiều mã hàng.

## Hai nguồn số khác nhau (đáng lẽ phải luôn bằng nhau)

| | Nguồn | Vị trí |
|---|---|---|
| Cột | `arriving_qty` trên dòng hàng của YC đặt hàng / PO | `StockTransferReportService.php:1347, 1468, 1669, 1737` |
| Popup | Sổ cái `order_stock_progress` — mỗi dòng = SL đang nằm ở 1 chứng từ (PI → HĐ → Invoice → Tờ khai → Phiếu nhập) | `StockTransferReportService.php:4242+` (`getStockTranfer`) |

Thiết kế của hệ thống: hàng đi sang bước sau thì **trừ dòng sổ cái bước trước + cộng dòng bước sau**;
khi tách sang khách hàng hoặc nhập kho thì trừ **cả** `arriving_qty` **lẫn** dòng sổ cái.
⇒ Bất biến: `arriving_qty` == SUM(`order_stock_progress.qty`) của cùng dòng hàng.
Kiểm trên DB local (snapshot 30/01/26): 152/153 dòng khớp tuyệt đối ⇒ bất biến là đúng, không phải 2 khái niệm khác nhau.
**Số đúng là cột (18); popup thừa vì có dòng sổ cái bước cũ không được trừ.**

## Root cause — 2 lỗi cùng một pattern "tra hụt rồi bỏ qua im lặng"

Pattern chung: `arriving_qty` **luôn** bị trừ, còn dòng sổ cái chỉ trừ khi `->first()` tra trúng;
không trúng thì `if ($row)` bỏ qua, **không lỗi, không log** → lệch âm thầm, tích luỹ dần.

### Lỗi 1 — Hợp đồng gốc vs PHỤ LỤC lệch id (luồng nhập khẩu)
`OrderRequest2.php:546-556` (tách hàng tồn kho sang khách hàng) tra sổ cái theo **đúng 1 id**
`$detail->buy_contract2_id`. Dòng sổ cái có thể nằm ở phụ lục còn dòng tách gắn hợp đồng gốc (hoặc ngược lại) → trượt.

Bằng chứng prod (mã GC-GC-40PRO-A:06, `order_request_product2` id 5798, `arriving_qty = 18`, sổ cái 56):

| Dòng sổ cái | HĐ | qty | updated_at | Dòng tách sang khách |
|---|---|---|---|---|
| 877 | 0526.01 HP-ANNEX 01 (phụ lục của 700) | 24 | 10/08 10:27:35 | detail 5843 gắn HĐ **877** → trúng → có trừ |
| 878 | 0526 HP LCL-ANNEX (phụ lục của 701) | 2 | 11/08 09:04:14 | detail 5850 gắn HĐ **878** → trúng → có trừ |
| 879 | 0526.02 HP-ANNEX (phụ lục của 699) | 28 | **chưa từng update** | detail 5842 gắn HĐ **699 = gốc** → trượt → KHÔNG trừ |

### Lỗi 2 — Sai tên trường (luồng trong nước) — nặng hơn
`InlandOrderRequestNew.php:500` dùng `$detail->buy_contract2_id`, nhưng `$detail` là
`InlandBuyContractNewProductDetail`; bảng `inland_buy_contract_new_product_details` **không có cột đó**
(chỉ có `inland_buy_contract_new_id`) → luôn `null` → **không bao giờ khớp** → dòng sổ cái tồn kho
của hàng trong nước chưa từng được trừ ở luồng tách.

## Quy mô trên prod (SQL đối chiếu toàn hệ thống, 10/09/2026)

| Nguồn | Số dòng lệch | Tổng cột | Tổng popup |
|---|---|---|---|
| YC đặt hàng (nhập khẩu) | 5 | 86 | 141 |
| YC đặt hàng trong nước | 19 | 186 | 355 |
| PO nhập khẩu / PO trong nước | 0 | — | — |

## Các điểm code cùng pattern cần rà (phía tồn kho)
`OrderRequest2.php:547, 567` · `InlandOrderRequestNew.php:500, 520` ·
`Invoice2.php:497, 519, 663, 698` · `Invoice2Controller.php:576, 598` ·
`InlandBuyContractNewController.php:786, 820, 1161, 1193`

## Hướng fix
1. Helper lấy **cả họ hợp đồng** (bản gốc + toàn bộ phụ lục — model đã có `annex_additions()` ở cả
   `BuyContract2` và `InlandBuyContractNew`), tra `whereIn` rồi trừ lần lượt qua các dòng của họ đó.
2. Sửa lỗi sai tên trường ở `InlandOrderRequestNew.php:500`.
3. Không tìm thấy dòng sổ cái để trừ → **ghi log** thay vì bỏ qua im lặng.
4. Dọn dữ liệu prod: kéo tổng sổ cái về khớp `arriving_qty` (backup `order_stock_progress` trước).
5. Hàng rào ở báo cáo: cột và popup lấy chung một nguồn để không đá nhau nếu sổ cái còn lệch.
