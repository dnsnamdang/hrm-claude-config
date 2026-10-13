# Plan — Đảo thứ tự cột "Số phụ lục" / "Số hợp đồng" ở các DS phụ lục

Yêu cầu (2026-09-11, theo ảnh chụp màn "DS phụ lục bổ sung HĐ trong nước theo hãng"):
đưa **Số phụ lục lên cột đầu (ngay sau STT)**, **Số hợp đồng xuống cột 2**. Áp cho cả 3 DS phụ lục:
phụ lục HĐ nhập khẩu, phụ lục trong nước theo hãng, phụ lục trong nước tự do.
Chỉ đổi thứ tự hiển thị + ô lọc; không đụng data/BE/nghiệp vụ. Liên quan [[pl-nhap-khau-cot-so-hd-goc]] (đã thêm 2 cột này trước đó).

## Tasks — ĐÃ XONG
- [x] 1. `resources/views/orders/buy_contract2/index.blade.php` (type `annex_addition` = phụ lục HĐ nhập khẩu):
  - `columns`: đổi `code`(Số phụ lục) trước, `parent_code`(Số hợp đồng) sau.
  - `search_columns`: đổi tương ứng (giữ khớp thứ tự với columns).
- [x] 2. `resources/views/orders/inland_buy_contract_new/index.blade.php` (type 4 = theo hãng, type 5 = tự do):
  - `columns`: đổi `code`(Số phụ lục) trước, `parent_code`(Số hợp đồng) sau.
  - `search_columns`: đổi tương ứng.

## Tasks bổ sung (2026-09-11) — màn xem chi tiết phụ lục thiếu Số hợp đồng gốc
- [x] 3. `resources/views/orders/buy_contract2/show.blade.php` — thêm ô "Số hợp đồng" (`form.parent_code`, disabled), `ng-if="form.parent_code"`, ngay sau ô Số phụ lục.
- [x] 4. `resources/views/orders/inland_buy_contract_new/show.blade.php` — block code/phụ lục đang bị comment; thêm ô "Số hợp đồng" (`form.parent_code`, disabled), `ng-if="form.parent_code"` ở đầu hàng thông tin chung.
- Ghi chú: `parent_code` là cột thật trên cả 2 bảng (buy_contract2, inland_buy_contract_news) → có sẵn trong `@json($object/$data)` truyền vào form show; chỉ phụ lục mới có giá trị nên `ng-if` tự ẩn ở HĐ gốc.

## Kiểm chứng
- Chỉ swap 2 dòng trong mỗi khối `@if`; nhánh type khác (HĐ, không phải phụ lục) giữ nguyên.
- Không file nào set `order:` cứng theo chỉ số cột → default sort cột 0 (STT) không ảnh hưởng.
- `search_columns` đảo khớp `columns` nên ô lọc vẫn nằm đúng dưới cột.
