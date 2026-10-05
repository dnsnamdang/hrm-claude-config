# Fix: Báo cáo hàng gửi trừ thiếu khi phiếu xuất chia nhiều kho kế toán

@junfoke — Repo `TanPhatDev`, nhánh `master`.

## Hiện tượng (user báo 10/09/2026)
- Phiếu PXH-33614 / PXK-29383 (`/admin/warehouse/product_exports/33614/show`), hàng
  `ENEO-450-V5252`, xuất 18 Thùng 4 Can = **72 Can 5L**, nguồn 100% từ **hàng gửi**.
- Màn chi tiết: cấp **hàng hoá** ghi "Từ SL gửi = 72", nhưng 2 dòng **kho kế toán** chỉ ghi
  V-HG **8** và MT01 **0** ⇒ tổng 8.
- Báo cáo hàng gửi (`warehouse_reports/holdDetail`) đọc theo dòng kho kế toán → ghi nhận
  "SL xuất = 8", còn tồn gửi 64 dù thực tế đã xuất hết.

## Root cause
Sổ hàng gửi (`hold_detail_logs`) được trừ trong `ProductExport::approve` theo **từng dòng kho kế
toán** (`product_export_detail_accounting.export_from_hold`), không dùng số cấp hàng hoá.
Số đó do FE chia, ở `ProductExport.blade.php::calculatePrepickQty()`. Hai lỗi:

1. **Không tính lại khi thêm/bớt dòng kho kế toán.** `calculatePrepickQty()` chỉ được gọi ở
   `ng-change` của ô SL (`form.blade.php:823`) và lúc load phiếu. Dòng kho kế toán thêm mới được
   **tự điền SL trong constructor** (`ProductExportLotAccounting`: `this.qty = this.parent.qty`)
   nên `ng-change` không bắn ⇒ dòng mới giữ `export_from_hold = undefined → 0`.
   Đúng kịch bản PXH-33614: sửa SL dòng V-HG về 2 (bắn ng-change → được 8, còn dư 64), rồi **thêm**
   dòng MT01 16 thùng → không tính lại → 0.
2. **Nhánh `qty >= total` không reset `total`.** Dòng sau vẫn thấy `total` cũ nên được gán lại
   đúng số đó ⇒ trừ **thừa** hàng gửi khi nguồn giữ/gửi nhỏ hơn tổng SL xuất. Nhánh `else` cũng
   quên gán `export_from_stock = 0`.

Cùng lỗi áp cho `export_from_prepick` (SL giữ) của mọi loại phiếu xuất khác, không riêng type 12.

## Tasks
- [x] FE `ProductExport.blade.php::calculatePrepickQty()`: reset `total`/`total_prepick` về 0 ở
      nhánh đủ, gán `export_from_stock = 0` ở nhánh thiếu, `|| 0` chống `undefined → NaN`
- [x] FE `ProductExportLot.blade.php`: gọi `this.parent.calculatePrepickQty()` sau
      `addAccWarehouse()` và `removeAccWarehouse()`
- [x] BE `ProductExportsController`: thêm `splitAccSourceQty()` và **tính lại phân bổ ở server**
      trong cả `store()` và `update()` — tổng `export_from_hold`/`export_from_prepick` của các dòng
      kho kế toán luôn bằng số cấp hàng hoá, không phụ thuộc FE (bỏ qua khi `is_export_direct`)
- [x] `php -l` sạch; CRLF giữ nguyên (2 blade CRLF, controller LF)
- [x] Chạy thử thuật toán chia: ca PXH-33614 ra `8 + 64 = 72`, các ca một phần / không có hàng gửi /
      SL lẻ đều cân đúng `hold + stock = tổng SL xuất`
- [ ] User test browser: tạo phiếu xuất hàng gửi, sửa SL dòng 1 rồi **thêm** dòng kho kế toán 2 →
      màn chi tiết phải hiện đủ 2 dòng có "Từ SL gửi", duyệt xong báo cáo hàng gửi về 0
- [x] Rà dữ liệu prod: toàn hệ thống chỉ **2 bản ghi** lệch — PXH-33614 (hàng gửi, thiếu 64) và
      PXH-00476 (SL giữ, thiếu 48, phiếu 11/08/2025)
- [x] **VÁ XONG PXH-33614 trên prod 10/09/2026** (user chạy, backup `hold_details_bak_20260910`,
      `hold_detail_logs_bak_20260910`, `peda_bak_20260910`): thêm log `hold_detail_logs` id 13669
      (objectable 86175, change −64, 64→0), `hold_details` 464 qty 64→0,
      `product_export_detail_accounting` 86175 `export_from_hold` 0→64. Sổ giờ cân:
      +64 +8 −8 −64 = 0
- [ ] PXH-00476 (phần SL giữ / `prepick_details`, thiếu 48) — **chờ user quyết có vá không**;
      phiếu hơn 1 năm, số giữ nhiều khả năng đã hết hạn/bị reset, phải dò trạng thái sổ giữ trước
- [ ] DROP 3 bảng backup sau vài ngày khi báo cáo đã đúng
- [ ] Commit + deploy

## Ghi chú
- Không đổi cấu trúc sổ `hold_detail_logs` (vẫn gắn `objectable = ProductExportDetailAccounting`)
  để báo cáo giữ nguyên cột Phiếu yêu cầu / Phiếu hạch toán.
- Cách chia giữa các kho kế toán là chia tuần tự theo thứ tự dòng; `hold_details` chỉ theo **kho vật
  lý** nên chia thế nào cũng được, miễn tổng đúng.

## ✅ Trạng thái xác minh (10/09/2026) — ROOT CAUSE ĐÃ XÁC NHẬN BẰNG DATA PROD

SQL nhắm thẳng phiếu 33614 (user chạy trên prod `erp_new`):

| Bảng | Số liệu |
| --- | --- |
| `product_exports` | id 33614, type 12, **status 1** (= đã duyệt, có `approved_time`), `updated_at` = `created_at` ⇒ **không hề sửa lại sau duyệt** |
| `product_export_details` | detail 86489, qty 18 × coef 4 = 72, `export_from_hold` = **72** |
| `product_export_detail_accounting` | acc **86174** (kho 52, qty 2) → hold **8**; acc **86175** (kho 19, qty 16) → hold **0** |
| `hold_detail_logs` | chỉ **1 dòng**: hold_detail 464, objectable 86174, change **-8**, qty_after 64 |

⇒ Đúng kịch bản: dòng kho kế toán **tạo trước** (id nhỏ hơn, 86174) nhận đủ 8 = SL của chính nó;
dòng **thêm sau** (86175) giữ 0 vì `calculatePrepickQty()` không được gọi lại ⇒ sổ hàng gửi thiếu 64.

⚠️ **Câu SQL dò đợt đầu sai điều kiện**: lọc `pe.status = 3` trong khi **status 1 = đã duyệt**,
status 3 = nháp (kiểm chứng local: 724 phiếu status 1 đều có `approved_time`, 3 phiếu status 3 đều
không có) — nên trả về 0 dòng. Dò lại phải dùng `pe.approved_time IS NOT NULL`.

**Lỗi #2 (không reset `total`)** cũng đã chứng minh bằng chạy lại thuật toán cũ: ca "dòng 1 đã đủ
nguồn, còn dòng 2" ⇒ code cũ ra `hold=[64,8]` = 72 trong khi nguồn gửi chỉ có 64 ⇒ **trừ THỪA 8**.

### Checkpoint — 2026-09-10
Vừa hoàn thành: xác nhận root cause bằng data prod; sửa 2 file FE + 1 file BE (lint sạch, CRLF
nguyên vẹn); vá xong dữ liệu PXH-33614 trên prod, sổ hàng gửi về 0.
Đang làm dở: không.
Bước tiếp theo: user commit + deploy 3 file code; quyết định vá PXH-00476; DROP bảng backup.
Blocked: không.
