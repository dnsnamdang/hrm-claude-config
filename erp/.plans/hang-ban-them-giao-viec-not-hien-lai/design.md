# Hàng bán thêm vẫn hiện lại ở phiếu giao việc nốt — Fix

## Hiện trạng / Triệu chứng
Trên HĐ dịch vụ (luồng Giao việc → Nhập kết quả → Duyệt kết quả), sau khi đã duyệt kết quả
hàng bán thêm với SL bàn giao = SL trên HĐ (giao đủ), khi lập **phiếu giao việc nốt** cho các
mục chưa hoàn thành thì mục **"Hàng bán thêm" vẫn hiện và "SL trên HĐ" vẫn = SL gốc** → cho
giao tiếp (over-assign).

## Nguyên nhân gốc
Cột "SL trên HĐ" của hàng bán thêm tính ở `WrServiceContract::getForAssignTask()`:

```
available_qty = qty (SL hợp đồng) − annex_qty − getAssigningMerchandiseQty()
```

`WrServiceContractMerchandise::getAssigningMerchandiseQty()` cộng cột **`assign_task_qty`** —
SL mà NVKD gõ ở ô "Số lượng giao lần này" **ngay bước lập phiếu giao việc**. Ô này thường bị để
trống = 0 (hàng bán thêm hay được giao & nhập ở bước Nhập kết quả). Khi đó:

- `assign_task_qty = 0` → `available_qty = SL HĐ − 0 = SL HĐ` → phiếu giao việc nốt luôn hiện lại.

SL đã giao thực nằm ở cột **`delivery_qty`** của dòng `assign_task_progress` (type=TYPE_MERCHANDISE):
- Bước lập phiếu giao việc: `delivery_qty = assign_task_qty = SL giao lần này`.
- Bước Nhập kết quả (`WrImportResultsController` ~2309/2314): `delivery_qty = import_result_qty = SL thực giao`.

→ `delivery_qty` là SL "cam kết hiện hành theo bước mới nhất", đúng vai trò cần trừ.

### Bằng chứng (DB erp_new)
- 292/327 dòng merchandise progress có `assign_task_qty = 0`.
- 83 ca `sum(assign_task_qty) ≠ sum(delivery_qty)` (assign=0 nhưng delivery>0).
  VD HĐ 7854 SP 17684: SL HĐ=7, sum assign=0, sum delivery=7.

## Hướng sửa — bám ĐÚNG cách vật tư sửa chữa (user chốt)
Vật tư sửa chữa (`items`) trong cùng `getForAssignTask()` đã làm đúng:
- `getAssigningItemQty()` cộng `qty` của **progress con** (`AssignTaskItemProgress`) — cột này được
  bước Nhập kết quả ghi đè `= import_result_qty` (WrImportResultsController:469-470) → SL thực giao.
- Set pre-fill `qty = available_qty > 0 ? available_qty : 0` (dòng 2706).
- **Lọc bỏ** dòng `available_qty <= 0` (dòng 2710-2712).

Hàng bán thêm là progress phẳng (không có progress con) → cột tương đương = `delivery_qty`.

### 3 sửa đổi
1. `WrServiceContractMerchandise::getAssigningMerchandiseQty()` — nhánh có progress: cộng
   `delivery_qty` thay vì `assign_task_qty`. (Nhánh fallback `WrAssignTaskMerchandise.qty` giữ
   nguyên, tương đương fallback của repair — chỉ chạy khi chưa có progress.)
2. `WrServiceContract::getForAssignTask()` loop merchandise: thêm
   `$merchandise->qty = $merchandise->available_qty > 0 ? $merchandise->available_qty : 0;`
3. Cuối hàm: lọc `$object->merchandises` bỏ `available_qty <= 0`, gán `$result['merchandises']`.

## NGOÀI phạm vi (user chốt)
- KHÔNG thêm validate chặn duyệt kết quả khi "chưa đủ SL bàn giao" (Q2 — không cần nữa).
- KHÔNG đụng lỗi phụ thiếu `->save()` ở `WrApproveResultsController:822-841`.

## Lưu ý
- `getAssigningMerchandiseQty()` là hàm nghiệp vụ dùng chung → đã xin ý kiến, user chốt mirror repair.
- ERP là Laravel 6 / PHP 7.4 — không dùng `?->`, không tính năng L7+.
- Chỉ sửa CODE, KHÔNG vá dữ liệu.
