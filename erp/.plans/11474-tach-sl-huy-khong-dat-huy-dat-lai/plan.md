# #11474 — Tách "SL hủy mua" thành Hủy không đặt / Hủy đặt lại, sửa SL chờ lập HĐ âm

**Người phụ trách:** @junfoke
**Repo:** `TanPhatDev` · **Nhánh:** `master` · **Commit:** `947107bcfc` [1/2 migration] + `a775520034` [2/2 code] — **ĐÃ PUSH `master` 16/09/2026**
**Issue:** http://quanly.dnsmedia.vn/issues/11474 — Nguyễn Huyền báo 16/09/2026
Liên quan: `../fix-bao-cao-bo-sot-phieu-lay-ton-kho/plan.md`, `../fix-ton-kho-dang-ve-gop-nham-dong-ton-kho/plan.md`

## Yêu cầu trong issue

1. **Báo cáo tiến độ đặt hàng theo nhân viên**: tách cột "SL hủy mua" thành **SL hủy không đặt** +
   **SL hủy đặt lại** (cả form xuất Excel). Công thức mới:
   `SL chờ lập HĐ = SL duyệt − SL lập HĐ − SL hủy không đặt`.
2. **HĐ mua / PLBS mua, tất cả luồng mua**: hủy không đặt và hủy đặt lại đều hiện "Đã hủy" nên
   không tra soát được → đổi text trạng thái theo lựa chọn thật. Hủy hết mục hàng thì trạng thái
   HĐ/PLBS **vẫn là "Đã hủy"**.

## Nguyên nhân số âm

`reOrder()` nhận tham số `type` (1 = hủy không đặt, 2 = hủy đặt lại) nhưng **chỉ set `status = 0`,
vứt `type` đi** — không cột nào lưu. Báo cáo vì thế coi mọi dòng hủy là "hủy mua" rồi trừ vào cột
chờ; trong khi SL hủy **đặt lại** sau đó được lập lại bằng HĐ/PLBS khác nên đã nằm trong
"SL đã lập HĐ" → trừ hai lần → âm.

## Đã làm

- **Migration** `2026_09_16_160000_add_cancel_type_to_contract_product_details.php`: thêm cột
  `cancel_type` TINYINT NULL vào `inland_buy_contract_new_product_details` và
  `buy_contract_product_detail2`. NULL = dữ liệu cũ, báo cáo tính như "hủy không đặt".
- **Hằng số** `HUY_KHONG_DAT = 1` / `HUY_DAT_LAI = 2` trên 2 model chi tiết.
- **`reOrder()` cả 2 luồng** ghi `cancel_type`. Luồng nhập khẩu bổ sung luôn guard chặn bấm hủy
  lần 2 (luồng trong nước đã có ở commit `00ff575208`).
- **Báo cáo**: `getDataTNHD` + `getDataNKHD` tách `deny_no_reorder_qty` / `deny_reorder_qty`;
  `getData` đổi công thức cột chờ.
- **Hiển thị**: blade màn hình, `OrderReportController` (in/Excel), `OrderReportProcessMailJob`
  (mail tự động) — thêm 2 cột.
- **Badge dòng hủy**: `inland_buy_contract_new/show.blade.php` + `buy_contract2/show.blade.php`.
  Dòng cũ chưa xác định vẫn hiện "Đã hủy".
- **Backfill** `backfill.sql` (user chốt hướng suy luận 16/09/2026): dòng đã hủy mà **cùng dòng nhu
  cầu** còn chi tiết HĐ/PLBS khác đang hiệu lực ⇒ `cancel_type = 2`; còn lại ⇒ `1`. Dòng tồn kho
  (không có dòng nhu cầu) đối chiếu theo phiếu đặt hàng + hàng hoá.

## ⚠️ THỨ TỰ TRIỂN KHAI BẮT BUỘC

Code mới `SELECT cancel_type` — **chạy migration TRƯỚC, deploy code SAU**. Deploy code trước khi có
cột sẽ làm báo cáo và màn HĐ/PLBS lỗi ngay.

Tách làm **2 commit riêng** đúng để đẩy/deploy theo 2 nhịp:

1. Push + deploy `947107bcfc` (**chỉ có migration**, không đụng code) → `php artisan migrate`
2. Chạy `backfill.sql`
3. Push + deploy `a775520034` (code)

## Kiểm chứng (DB `erp_prod_09_26`, tinker, rollback sau mỗi phép đo)

| Phép đo | Kết quả |
|---|---|
| `reOrder(type=1)` / `reOrder(type=2)` | `cancel_type` = 1 / 2 ✓ |
| Mã SND-EVB4S22NC0M **trước** backfill | Hủy không đặt 2/6, chờ lập HĐ **−2 / −6** |
| Mã SND-EVB4S22NC0M **sau** backfill | Hủy không đặt 0, hủy đặt lại 2/6, chờ lập HĐ **0 / 0** ✓ |
| Hồi quy 40 sản phẩm / 196 dòng, `cancel_type` còn NULL | **0 dòng lệch** — code an toàn khi chưa backfill |

`php -l` sạch 8 file, CRLF nguyên vẹn, diff +72/−16 trên 10 file + 1 migration mới.

## Tasks

- [x] Đọc issue + 2 ảnh đính kèm
- [x] Migration `cancel_type` cho 2 luồng
- [x] `reOrder()` ghi loại hủy (+ guard bấm lần 2 cho luồng nhập khẩu)
- [x] Báo cáo tách 2 cột + đổi công thức
- [x] Màn hình + bản in/Excel + mail tự động
- [x] Badge trạng thái dòng ở HĐ/PLBS cả 2 luồng
- [x] SQL backfill dữ liệu cũ
- [x] Verify + hồi quy
- [x] Chạy migration + backfill trên prod
- [x] Push cả 2 commit đúng thứ tự
- [ ] QA nghiệm thu, cập nhật issue Redmine

## Checkpoint — 16/09/2026

Vừa hoàn thành: toàn bộ code + backfill, tách **2 commit** trên `master` (`947107bcfc` migration, `a775520034` code), **chưa push**.
Đang làm dở: không có.
Bước tiếp theo: chạy migration + backfill trên prod rồi mới push code.
Blocked: chờ user chạy migration (không tự đụng DB prod).

## Checkpoint — 16/09/2026 (đã lên prod)

Đã chạy đúng 3 nhịp: push `947107bcfc` → migrate → `backfill.sql` → push `a775520034`.

Kết quả backfill trên prod, **189 dòng đã hủy** được phân loại, không còn dòng NULL:

| Luồng | Hủy đặt lại (2) | Hủy không đặt (1) |
|---|---|---|
| Trong nước | 13 | 5 |
| Nhập khẩu | 84 | 87 |

Bước tiếp theo: QA nghiệm thu trên màn báo cáo + màn HĐ/PLBS, cập nhật issue #11474.
Cần xem lại sau khi QA xác nhận: 13 + 84 = 97 dòng chuyển sang "hủy đặt lại" ⇒ cột
"SL chờ lập HĐ" của những mã liên quan sẽ **tăng lên** (hết âm) — báo trước cho người dùng.
