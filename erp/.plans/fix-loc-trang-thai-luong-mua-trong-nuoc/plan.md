# Fix bộ lọc Trạng thái — Luồng mua trong nước Tự do

Phụ trách: @junfoke
Màn: `/admin/orders/inland_order_notification_new?type=1&_type=all`

## Vấn đề

Cột Trạng thái hiển thị nhãn **"Không có yêu cầu"** nhưng dropdown bộ lọc Trạng thái không có
option nào tương ứng để lọc.

Nguyên nhân: cột `status` trong DB chỉ có 3 giá trị (1=Đã đóng, 2=Đang mở, 3=Khóa). View suy ra
5 nhãn bằng cách ghép thêm `expired_date` + số phiếu yêu cầu, còn bộ lọc chỉ map theo `status` +
`expired_date` → thiếu 1 nhánh.

Hệ quả phụ: filter `Đã hết hạn (5)` hiện đang bao gồm CẢ bản ghi hiển thị "Không có yêu cầu"
(vì cả hai đều là `status=2` + quá hạn) → 2 nhóm chồng nhau.

## Phương án (user chốt: phương án 1)

Thêm mã lọc mới `6` = "Không có yêu cầu", đồng thời siết mã `5` = "Đã hết hạn" thành
"quá hạn VÀ CÓ phiếu yêu cầu" để 2 nhóm tách bạch, khớp đúng nhãn ở cột Trạng thái.

Mapping sau khi sửa:

| Mã lọc | Nhãn | Điều kiện query |
|---|---|---|
| 4 | Tất cả | (không lọc) |
| 1 | Đã đóng | `status = 1` |
| 2 | Đang tổng hợp | `status = 2` AND `expired_date >= today` |
| 5 | Đã hết hạn | `status = 2` AND `expired_date < today` AND **has** requests |
| 6 | Không có yêu cầu | `status = 2` AND `expired_date < today` AND **doesntHave** requests |
| 3 | Khóa | `status = 3` |

Quan hệ `requests` là `hasMany` không lọc `status` → dùng `has()` / `doesntHave()` khớp chính xác
với `count($object->requests)` mà view đang đếm.

## Tasks

- [x] BE: `InlandOrderNotificationNew::searchByFilter` — thêm nhánh `status == 6`
      (`doesntHave('requests')`), siết nhánh `status == 5` thêm `has('requests')`
- [x] FE: `inland_order_notification_new/index.blade.php` — thêm option `{id: 6, name: "Không có yêu cầu"}`
- [x] FE: `inland_order_notification_new/creator_index.blade.php` — sửa "Đã hết hạn" từ `id: 3`
      (đang trỏ nhầm sang Khóa) thành `id: 5`, thêm option `id: 6`
- [x] Áp cùng fix cho màn **Luồng nhập khẩu** (`OrderNotification2` + `order_notification2/index` +
      `creator_index`) — logic giống hệt 100% (5 nhãn, filter 4/5/2/else, `requests` hasMany không lọc status)
- [x] Verify cú pháp: `php -l` sạch cả 6 file; `git diff --stat` = 14 insert / 6 delete → CRLF không bị phá
- [x] Verify bằng query (tinker, read-only, DB local `erp_dev_30_01_26`): đếm theo nhãn hiển thị vs đếm
      theo query từng mã lọc → khớp 5/5 nhãn ở cả 2 màn; tổng quá hạn = "Đã hết hạn" + "Không có yêu cầu"
      (15 = 8+7 inland, 25 = 23+2 nhập khẩu) → 2 nhóm rời nhau, không sót
- [x] Verify trên trình duyệt (127.0.0.1:8001): dropdown render đủ 6 option kể cả "Không có yêu cầu";
      gọi `searchData` với từng mã lọc → nhãn cột Trạng thái trả về đồng nhất 100% với option đã chọn
      (inland: 5→2 "Đã hết hạn", 6→3 "Không có yêu cầu", 1→53, 3→5; nhập khẩu: 5→23, 6→2, 1→98, 3→1)

### Checkpoint — 2026-09-07
Vừa hoàn thành: fix + verify đầy đủ (query + browser) cho 2 màn Luồng trong nước Tự do và Luồng nhập khẩu.
Đang làm dở: không.
Bước tiếp theo: user test lại trên dev/prod rồi commit (nhánh `develop_01`, chưa commit).
Blocked: chờ user quyết 2 màn `OrderNotifications` / `InlandOrderNotification2` (xem mục dưới).

## Hai màn KHÔNG áp (logic khác hẳn) — chờ user quyết riêng

`OrderNotifications` (luồng nhập khẩu cũ) và `InlandOrderNotification2`: cột Trạng thái cũng render
"Không có yêu cầu", nhưng **bộ lọc của 2 màn này cấu trúc hoàn toàn khác**:

- Model chỉ có `where('status', $request->status)` — không có nhánh nào ghép `expired_date`.
- Blade chỉ khai đúng **2 option**: `{id:1, "Đã tổng hợp"}` và `{id:2, "Đang tổng hợp"}` — nhãn cũng
  khác (`Đã tổng hợp` vs `Đã đóng`), và **không hề có** "Đã hết hạn" lẫn "Khóa".

Nghĩa là ở 2 màn này, lọc "Đang tổng hợp" (id 2) đang gom cả bản ghi quá hạn lẫn chưa quá hạn — lệch
rộng hơn nhiều, không phải chỉ thiếu 1 option. Sửa cho khớp = thiết kế lại bộ lọc (thêm 3 option +
3 nhánh query), đổi cả nhãn hiện có → cần user chốt nghiệp vụ trước, không áp máy móc.
