# #12195 [Mua hàng] Cho nhập số lượng có 2 chữ số thập phân (@junfoke)

Repo `TanPhatDev`, nhánh `task_12195` (tách từ `origin/gop_db`), merge `develop_02`.
Phạm vi (user chốt): chỉ cột **SL đặt / SL duyệt**, cho nhập cả số < 1, tối đa 2 số lẻ; hiển thị + bản in + Excel cũng phải hiện đủ phần lẻ; không đụng SL khuyến mãi / bảo hành / chênh lệch. 4 luồng: Nhập khẩu (có Invoice, PLG), Trong nước theo hãng, Trong nước tự do, Mua ngoài.

## Ngày 17/11/2026 (@junfoke)
- [x] 17/11/2026 — Tính năng mới #12195: khảo sát 4 nhóm màn (YC đặt hàng; PO/PI; HĐ mua + phụ lục; Invoice + báo hàng về). Lỗi chính: ô SL dạng chữ gắn setter `Number(value)` trên AngularJS 1.3.9 → gõ "0.05" ghi thành 5. Sửa:
  - ~25 ô nhập đổi sang `type="number" step="0.01" min="0"`, setter `roundNumber(value, 2) || 0` (1.255 → 1.25), giữ các trần sẵn có (SL duyệt ≤ SL đặt…): YC gốc, YC nhập khẩu, PO nhập khẩu + trong nước (kể cả SL đặt bổ sung), PI, HĐ mua nhập khẩu + trong nước, đơn hàng nguyên tắc, PLBS, HĐ + phụ lục mua ngoài, PLG, Invoice, báo hàng về.
  - BE: 7 controller đổi `min:1` → `min:0.01` chỉ cho SL đặt / SL duyệt.
  - Hiển thị: bỏ `number:0`, làm tròn các getter tổng SL (hết 0.9999999999999999), sửa 2 chỗ cộng chuỗi `5 + "2.00"` = "52.00", chỗ có thể nối chuỗi khi sửa Invoice.
  - Bản in + Excel (YC gốc, báo giá PO các mẫu, PI, báo hàng về…): `number_format` / `formatCurrency` trên SL → `formatQuantity(x, 2)`, giữ nguyên ô thành tiền.
- [x] 17/11/2026 — Test full luồng local (theo yêu cầu user trước khi lên dev): nhập khẩu YC gốc PDH-09043 → PDHNK-04202 → PO 1537 → PI 1403 → HĐ 1117 → Invoice 857 → báo hàng về; PLBS 1118 (cả luồng sửa), PLG; trong nước PDH-09044 → PDHTN-06188 → PO 4613 → PI 4381 → HĐ 2538 → báo hàng về 3105; HĐ + phụ lục mua ngoài; sửa YC gốc; tạo YC nhập khẩu trực tiếp. Phát hiện + sửa thêm 3 lỗi:
  - YC trong nước lưu mất phần lẻ: 8 cột SL ở cụm bảng `*_new*` (YC trong nước, HĐ trong nước) là INT → migration `2026_11_17_120000_change_qty_to_decimal_on_inland_order_request_new_and_buy_contract_new.php` đổi sang `decimal(12,2)` (có down).
  - PI chặn lưu sai khi chia đợt giao lẻ (0.06 + 0.57 + 0.37 = 0.9999999999999999 ≠ 1) → làm tròn 2 số khi so sánh, ở PI nhập khẩu + trong nước.
  - Tổng SL hiện số rác → làm tròn getter tổng ở YC, PO, PI, HĐ, Invoice, báo hàng về; ô SL dòng hàng bản in báo hàng về in thô "1.00".
  - Dữ liệu tạm đổi (quản lý phòng, phân công, trạng thái phiếu thử) đã trả lại.
- [x] 17/11/2026 — Commit `d86dd651aa` (85 file, nhánh `task_12195`, đã push) + merge `develop_02` `395f62e027` (đã push; kéo theo 6 commit gop_db chưa có ở develop_02). **Dev cần chạy `php artisan migrate`.**
- [x] 17/11/2026 — Đổi tên nhánh `feat/12195-sl-thap-phan-mua-hang` → `task_12195` đúng quy ước tên nhánh của user.
