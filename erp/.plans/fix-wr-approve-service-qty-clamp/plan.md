# Fix: SL bàn giao dịch vụ = 0 dù đã hoàn thành (màn duyệt kết quả sửa chữa)

## Bối cảnh
Màn `/admin/customer-care/wr_approve_results/{id}/show` → "A - Dịch vụ sửa chữa" → "Danh sách dịch vụ" (vd "Vật tư lắp đặt"): tích Đã hoàn thành 100% nhưng **SL bàn giao = 0**.

## Root cause (đã verify bằng DB)
- DB `wr_import_result_product_services`: `qty=1`, `available_qty=0`, completed=1. → DB đúng.
- Class dùng chung `WrAssignTaskProductService` (`warranty_repair_assign_tasks/WrAssignTaskProductService.blade.php`) có `set qty` **clamp về available_qty**: `if (value > available_qty) value = available_qty`. FE gán available_qty(0) trước rồi qty(1) → qty bị ép 0.
- Dịch vụ có `available_qty=0` mặc định (không quản tồn) → clamp ép qty về 0 oan. Vật tư mới cần clamp.

## Fix (Cách A — chỉ màn approve, không đụng class dùng chung)
File: `resources/views/customercare/wr_approve_results/WrApproveResultProductService.blade.php`
Override `get qty` + `set qty` để KHÔNG clamp (cột SL bàn giao trên màn approve chỉ hiển thị, không nhập):
```js
set qty(value) {
    this._qty = Number(value);
    this.parent.parent.calculateAllServices();
}
get qty() {
    return this._qty || 0;
}
```
(Giữ `calculateAllServices()` như base để không đổi luồng tính tiền; chỉ bỏ phép clamp.)

## Tasks
- [x] Thêm override `get/set qty` (không clamp) vào `WrApproveResultProductService` (chặn phát sinh mới)
- [x] Data fix `fixWrApproveServiceQtyZero()` trong UpdateDB.php — set qty 0→1 cho 28 service phiếu duyệt completed (đã chạy trên prod)
- [x] Verify browser: record 2023 SL bàn giao = 1 ✅ (user xác nhận)

## ĐÍNH CHÍNH root cause (quan trọng)
- Chẩn đoán đầu SAI: query nhầm `wr_import_result_product_services` (qty=1). Nguồn THẬT màn show = `wr_assign_task_product_services.qty` (getForShow), lưu **0**.
- Root cause đúng: clamp (`set qty: value>available_qty→available_qty`) chạy lúc **LẬP phiếu duyệt** → service qty (1, từ phiếu nhập KQ) bị ép 0 (available_qty=0) → lưu qty=0 vào `wr_assign_task_product_services`.
- Bằng chứng: 2673 service phiếu duyệt → qty>0: 2617, completed&qty=0: 28, và 28/28 có available_qty=0.
- Fix 2 phần: (1) FE bỏ clamp ở `WrApproveResultProductService` chặn tương lai; (2) data fix 28 record cũ.

## Test (repro thủ công — không có JS test framework)
1. Mở `/admin/customer-care/wr_approve_results/2023/show` → dòng "Vật tư lắp đặt" → **SL bàn giao = 1** (đúng DB), không còn 0.
2. Dòng "Công tháo lắp" vẫn = 1 (không hồi quy).
3. Màn giao việc (assign task) — dịch vụ vẫn clamp theo available_qty như cũ (không đụng class cha).

## Điều tra upstream (vì sao available_qty=0)

Chuỗi nguyên nhân đầy đủ (verify bằng DB):
1. Gốc: `wr_assign_task_product_services.available_qty` = **NULL** (ATPS#120). Phân bố: 4006 dòng → **NULL=201, =0:59, >0:3746**. (available_qty được tính ở form tạo assign task = `quantity − annex − getAssigningQty()`, submit qua submit_data; ~201 dòng NULL = tạo qua path không lưu available_qty / data cũ.)
2. Tạo phiếu nhập kết quả: sync `available_qty = $atService['available_qty'] ?? 0` → **NULL → 0** (WrImportResult).
3. Màn duyệt `getForShow`: đọc `available_qty ?? 0` = 0.
4. Class FE `WrAssignTaskProductService.set qty`: clamp `qty(1) > available_qty(0)` → **0**. = triệu chứng.

→ 2 điểm khuếch đại: (a) coalesce NULL/unknown → 0, (b) dùng available_qty làm trần cứng cho SL **đã bàn giao** trên màn KẾT QUẢ. SL đã làm (=1, từ phiếu nhập KQ) không nên bị giới hạn bởi "available" cũ/unknown.

**Không hỏng tiền/DB:** DB qty luôn=1 (sync hardcode), payed_price không nhân qty. Fix Cách A xử lý đúng triệu chứng (bỏ clamp khi hiển thị kết quả).

### Checkpoint — 2026-06-15 (DONE — verify PASS trên prod)
Vừa hoàn thành: FE bỏ clamp (`WrApproveResultProductService`) + data fix 28 record (`fixWrApproveServiceQtyZero`, đã chạy trên DB prod erp_new). User xác nhận record 2023 hiển thị SL bàn giao = 1.
Đang làm dở: —
Bước tiếp theo: FE fix cần đảm bảo đã deploy server (user đã deploy). Data fix là one-off, không cần lặp.
Blocked: —
Lưu ý: `.env` ERP local trỏ DB production (erp.eteksofts.com/erp_new) → artisan/tinker chạy thẳng prod.
