# Kiểm kê xuất vượt lớp hàng giữ → tồn bán âm

## Bối cảnh / sự cố

Sản phẩm **34686** (Model `MN-HB-BN0306`, mã `SG-MN-HB-BN0306`, "Bàn nguội 1800x600x700mm inox màu xám"),
công ty **4 (TPSG)**, kho Sài Gòn. Màn danh mục hiện **"tồn có thể bán = −2"** trong khi **vẫn còn 2 phiếu
giữ sống**. User khẳng định: có giữ thì PHẢI khóa hàng, chắc chắn có bug cho xuất vượt lớp giữ.

### Kết luận điều tra (đã xác minh)

- **Công thức "tồn có thể bán"** (`SearchController.php:533`, nhánh non-self): `in_stock = accounting_qty −
  prepick_qty − hold_qty − werd_qty`. Số thật: `0 − 2 − 0 − 0 = −2`.
- **Tồn vật lý = tồn kế toán = 0** (khớp hoàn toàn). Lệch duy nhất là **lớp giữ = 2 treo trên tồn 0**.
- **Nguyên nhân gốc:** 02/08/2026 phiếu xuất điều chỉnh kiểm kê **PXHĐCKK-00066** (`inventory_exports` id=66,
  `warehouse_inventory_export_id`=81) kéo tồn kế toán kho 7 từ 4→0, **tách SP 34686 thành 4 dòng qty=1**.
  Guard chống xuất vượt giữ **kiểm từng dòng** (`1 < in_stock(=2)` → false) nên 4 dòng qua hết; tổng xuất 4 >
  khả dụng 2. → **Lỗ hổng guard per-row, không cộng tổng theo sản phẩm.**
- **2 phiếu giữ sống** (`prepick_details` qty>0):
  - Hold A — `pd64272` qty=1, NV **298** (Nguyễn Thế Hiền), KH **34023** (CN Gò Vấp – Thăng Long), cty 4,
    expire 22/10. Gốc PXG-02038.
  - Hold B — `pd69600` qty=1, NV **744** (Hồ Ngọc Tiến), KH **39155** (Kiên Nga Đức Cơ), cty 4, expire 15/11.
    Gốc PXG-02182. Vừa gia hạn 16/10.
  - SP có 1 đơn vị: `unit_id=41` "Cái.", `unit_coefficient=1`, is_base.
  - Không còn phiếu gia hạn treo (status≠1) → không tự tái sinh sau khi xử lý.
- **Lệnh "hủy giữ hết" trước đây KHÔNG trúng 2 phiếu này** — phiếu hủy giữ cuối của SP là 14/05/2026
  (PHHG-02518/PYCHHG-02553); 2 hold tạo 08/07 + 27/07 nên chưa từng nằm trong phiếu hủy nào.

## Hướng xử lý (user chốt B + C + E, 2026-10-16)

### B — Fix data: giải phóng đúng 2 phiếu giữ (chốt: lập phiếu hủy giữ CHUẨN)
Lập phiếu hủy giữ đi đúng luồng nghiệp vụ PYCHHG (`PrepickCancelRequest`) → PHHG (`PrepickCancel`), dùng
chính các method model đã có (`validateProducts`/`syncProducts`/`updateWarehouse`) để trừ `prepick_details`
+ ghi `prepick_logs` chuẩn. **Chỉ 2 phiếu của SP 34686, KHÔNG backfill systemic.** Vì mỗi hold khác
employee+customer → **2 bộ PYCHHG+PHHG riêng**.

- Né `Auth`: `PrepickCancelRequest::boot()` chỉ gọi `Auth` khi `company_id` rỗng → set `company_id=4` tường
  minh. `approve()`/notification/Redis gọi `Auth::user()` → **set trạng thái duyệt thủ công** (status=1,
  approver_id, approved_time), bỏ notification (backfill không cần). Ledger lại.

### C — Fix code: vá lỗ hổng guard per-row (chốt: CHẶN CỨNG, cả 2 controller)
Cộng **tổng qty theo sản phẩm** trước khi so `in_stock`:
- `InventoryExportsController::validateAccountingWarehouse` — gom theo `(product_id, accounting_warehouse_id,
  unit_id)`.
- `WarehouseInventoryExportsController::validateAccountingStock` — gom theo `(product_id, company_id,
  unit_id)`.
Vượt → **chặn, không cho lưu/duyệt** (giữ nguyên thông báo cũ).

### E — Fix code: bịt kẽ hở ở bước DUYỆT kiểm kê (chốt: CHẶN CỨNG tại approve, không ai bỏ qua)
`WarehouseInventoryExportsController::approve()` (dòng 286) hiện **không có guard** trước
`updateWarehouse()`. Thêm: khi duyệt (`status==1`), nếu tồn mới < tổng đang giữ thì **chặn duyệt**, buộc
hủy giữ trước. Dùng lại `validateAccountingStock` trên chi tiết phiếu đang duyệt.

## Phạm vi KHÔNG làm
- Không backfill các SP khác (user chốt).
- Không đụng luồng gia hạn giữ (hướng D user không chọn).
- Không sửa `getAccountingStockDetail` / `SearchController` (công thức đúng).
