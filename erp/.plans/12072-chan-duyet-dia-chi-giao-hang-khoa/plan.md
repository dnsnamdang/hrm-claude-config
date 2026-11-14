# Plan — #12072 Chặn duyệt báo giá / HĐ khi địa chỉ giao hàng thuộc tỉnh/thành, xã/phường đã khoá (@junfoke)

Redmine: http://quanly.dnsmedia.vn/issues/12072 — "[Bán hàng] Báo giá và hợp đồng: chặn duyệt báo giá và HĐ (tất cả các loại) nếu địa chỉ giao hàng là tỉnh/thành, xã/phường cũ (đã bị khóa)". QA đã bỏ PLBS/PLG khỏi phạm vi.

## Ngày 13/11/2026 (@junfoke)
- [x] 13/11/2026 — Hỗ trợ check hiện trạng: Redmine còn "Mới" 0%; đã có commit `9863e36d27` của nguyentrancu97 (07/11) chặn theo phường/xã khoá cho báo giá vật tư + HĐ vật tư + HĐNT (7 controller), thiếu báo giá/HĐ dự án, Đơn hàng nguyên tắc, HĐ SC-BD-BT, và chưa chặn tỉnh/thành khoá.
- [x] 13/11/2026 — Lỗi #12072: làm đủ phạm vi trên nhánh `task_12072` (tách từ `gop_db`), logic gom ở `app/Services/Sale/Firm/FirmLockedDeliveryWard.php`, 11 controller gọi vào:
  - Chặn thêm **tỉnh/thành bị khoá** (trước chỉ phường/xã).
  - **Đơn hàng nguyên tắc** (thường + nha khoa): chặn khi gửi duyệt theo địa chỉ giao hàng trên báo giá của HĐNT cha, báo sale lập HĐNT mới (local 22 HĐNT hiệu lực bị ảnh hưởng).
  - Người duyệt bấm **Duyệt / Chuyển duyệt** HĐ đang chờ duyệt cũng bị chặn (kể cả HĐ gửi trước khi phường bị khoá); **Từ chối** vẫn được.
  - **Báo giá + HĐ sửa chữa – bảo dưỡng – bảo trì**: chặn khi duyệt báo giá, gửi duyệt HĐ, duyệt HĐ.
  - Lưu nháp, PLBS, PLG không bị chặn.
- [x] 13/11/2026 — Kiểm: 40/40 test pass trên `task_12072` và `develop_02` sau merge; gọi trên DB local với phiếu thật ra đúng câu báo ("phường/xã đã khóa (Yên Bình, nay là Yên Thắng)…"). Chưa bấm thử giao diện.
- [x] 13/11/2026 — Commit `ab40c62a70` → merge `develop_02` (`4bd5da4d67`), push cả 2 nhánh. Merge kéo theo 10 commit `gop_db` chưa có ở `develop_02` (gồm middleware `record.company`); conflict 1 dòng chú thích `Road.php` giữ bản `develop_02`.

### Checkpoint — 13/11/2026 14:04
Vừa hoàn thành: code + test, đã lên `origin/develop_02`.
Đang làm dở: —
Bước tiếp theo: chuyển Redmine sang "Code xong chờ test"; QA đạt thì merge `task_12072` vào `gop_db` (hỏi user).
Blocked:
