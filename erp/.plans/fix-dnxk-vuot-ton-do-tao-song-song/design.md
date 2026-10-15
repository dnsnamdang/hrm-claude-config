# Fix: ĐNXK cho phép vượt tồn khi 2 phiếu tạo gần nhau (race condition)

## Vấn đề
Sự cố thật (prod `erp_new`, 17/08/2026): mã hàng KOWA-KL-4-4 (product_id 4121), kho Phan Trọng Tuệ – Hàng bán (acc wh 3), cty 1, tồn = **9**. Nhưng 2 đề nghị xuất kho **PDNXK-32706** (qty 6) và **PDNXK-32708** (qty 5), cùng type 14 (XUAT_BAN_HD_HANG) / cùng kho 1 / cty 1 / khách 43536, do cùng NV 209 tạo cách nhau ~8–10 giây, **cả 2 đều qua** kiểm tra tồn → tổng giữ 11 > 9.

## Nguyên nhân gốc (đã xác minh)
**Check‑then‑reserve KHÔNG nguyên tử** dưới snapshot isolation của InnoDB:
- `WarehouseExportRequestsController::store()` bọc toàn bộ luồng trong **1 transaction** (`DB::beginTransaction()` dòng 249). Read đầu tiên (`ProductExportRequest::firstOrFail()` dòng 257) ghim **read snapshot** (REPEATABLE READ).
- `WarehouseExportRequest::validateProducts()` → `Product::getAccountingStockDetail()` đọc tồn/pending **trong snapshot đó**, **không có** `lockForUpdate`/`FOR UPDATE` (đã grep cả controller, model, Product.php).
- "Giữ chỗ" (`warehouse_export_request_details.export_total_qty`) chỉ ghi **sau** validate (`updateWarehouse()` dòng 365).

→ Nếu transaction của phiếu B mở snapshot **trước khi** phiếu A commit, reservation của A **vô hình** với B dù validate của B chạy sau vài giây. B đọc tồn cũ (9) → qua. Đã chứng minh phép JOIN trừ pending có khả năng thấy phiếu anh em (không phải lỗi filter); vấn đề thuần là **isolation/không khóa**.

Điểm yếu kèm theo (không sửa trong phase này, chỉ ghi nhận):
- `available_qty` (toàn công ty, Product.php dòng 2609) **không** trừ pending ĐNXK — toàn bộ chặn liên‑phiếu chỉ dựa vào phép trừ `in_warehouse`.
- Không có ràng buộc DB `SUM(export_total_qty) ≤ tồn`.

## Hướng fix (đã chốt với user)
**Advisory named lock của MySQL (`GET_LOCK`) theo (kho, công ty)**, mở khóa **TRƯỚC** khi transaction đọc lần đầu, nhả trong `finally` (cả commit lẫn rollback/exception).

```php
$lockName = "we_reserve_{$warehouseId}_{$companyId}";
DB::select('SELECT GET_LOCK(?, 10)', [$lockName]);   // chờ tối đa 10s
try {
    DB::beginTransaction();                            // snapshot mở SAU khi cầm khóa
    // validateProducts (thấy reservation phiếu trước) → syncProducts → updateWarehouse → commit
    DB::commit();
} finally {
    DB::select('SELECT RELEASE_LOCK(?)', [$lockName]);
}
```

**Vì sao đúng:** phiếu B chặn ở `GET_LOCK` tới khi A nhả (sau commit A). Lúc đó B **chưa** đọc → snapshot của B mở *sau* commit A → validate B thấy đủ giữ chỗ của A → chặn đúng. Không dính phantom, không phụ thuộc isolation level.

**Chốt granularity:** khóa theo **(kho, công ty)** — 1 khóa/phiếu → không deadlock, `finally` chỉ nhả 1 khóa, đúng ngay và khó viết sai. (Đã cân nhắc khóa theo mã hàng: mịn hơn nhưng nhiều khóa → phải sort thứ tự tránh deadlock + dọn dẹp partial‑acquire, dễ sai; tần suất ĐNXK thấp nên không đáng.)

## Phạm vi
- Áp cho CẢ `store()` **và** `update()` (gửi từ nháp cũng là điểm reserve) trong `WarehouseExportRequestsController`.
- Nếu quá 10s không lấy được khóa → trả thông báo thân thiện "Hệ thống đang xử lý phiếu khác trên kho này, vui lòng thử lại".
- **Không** đụng `validateProducts`/`getAccountingStockDetail` (hàm dùng chung) trong phase này — chỉ bọc khóa quanh critical section ở controller.

## Lưu ý
- ERP prod `erp_new` — chỉ đọc khi điều tra; **không** chạy fix trực tiếp lên prod.
- Đang ở nhánh `master` → nên tạo nhánh riêng trước khi code + PR (chưa commit/push khi chưa được yêu cầu).
