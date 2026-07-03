# Fix: ycldbg (yêu cầu lắp đặt bàn giao) vượt SL hợp đồng

## Mục tiêu

Chặn việc tạo **yêu cầu lắp đặt bàn giao (ycldbg)** vượt quá số lượng đã xuất kho của 1 mã hàng trên 1 hợp đồng hãng (firm contract). Hiện tại có thể tạo nhiều ycldbg cho cùng HĐ + mã hàng dù SL chỉ có 1 → dẫn tới nhiều phiếu giao việc (PGV) cùng giao 1 cái.

## Ca lỗi gốc (production)

- HĐ `9816` (HĐ_TPE_HN_KD1_25_0487_DepotMinhKhai), mã `GYSCN-MONOGYS250-4CS` (product_id `32799`): SL HĐ = 1, `warehouse_exported_qty` = 1.
- Đã tạo **3 ycldbg** (554, 1080, 1111) mỗi cái xin 1.
- 2 PGV cùng giao 1 cái: `11082` (từ ycldbg 1111, success **0%**) và `11319` (từ ycldbg 1080, serial 539410, **100%**).
- Lần giao thật duy nhất = 100% (PGV 11319, nhập KQ 15/06) → đã tiêu đúng SL = 1. PGV/ycldbg 1111 là **thừa**.

## Quy tắc nghiệp vụ (chủ dự án chốt)

1. SL ycldbg cho 1 mã trên 1 HĐ **không được vượt** `warehouse_exported_qty`.
2. Trường hợp **duy nhất** được tạo ycldbg thứ 2 cho cùng HĐ + mã: khi nhập kết quả phiếu trước có **tỉ lệ hoàn thành < 100%** → phần dở dang mới được tạo phiếu mới.

## Hiện trạng code (2 "cổng" tính SL khả dụng)

Cùng 1 logic bị **lặp ở 2 nơi** (nguồn của lỗi lệch nhau):

| Cổng | File | Vai trò |
|------|------|---------|
| FE form data | `app/Http/Controllers/Sale/Firm/FirmContractController.php` → `getDataForFirmContractAssemblyProduct()` (dòng 1281–1338) | Lọc mã + SL hiện ra ở form tạo ycldbg |
| Server validate | `app/Http/Requests/AssemblyRequestStoreRequest.php` → `validateProductQuantities()` / `getUsedQty()` / `buildAssemblyRequestQuery()` (dòng 75–239) | Chặn khi `store`/`update` ycldbg |

Công thức chung hiện tại:
```
usedQty   = hasAnyProgress ? SUM(assign_task_progress.can_request_qty) : SUM(SL ycldbg chưa từ chối)
available = warehouse_exported_qty − usedQty        // > 0 thì cho tạo
```

## 2 khiếm khuyết (root cause)

- **D1 — dòng "ma":** khi tạo PGV, hệ thống sinh `assign_task_progress` cho **toàn bộ mã trên HĐ**, kể cả mã không thuộc phiếu đó (`assign_task_qty = 0`, `can_request_qty = 0`). Các dòng này khiến `hasProgress = exists() = true` → nhánh đếm SL ycldbg đang chờ **bị bỏ qua**, chuyển sang `SUM(can_request_qty) = 0`.
- **D2 — mất SL đang chờ:** khi đã vào nhánh `SUM(can_request_qty)`, các ycldbg **đã yêu cầu nhưng chưa nhập kết quả** không được tính → quỹ bị "nhả" sai → cho tạo phiếu 2.

> Lưu ý: trường `can_request_qty` (gán = SL giao khi 100%, = 0 khi <100% — xem `WrApproveResultsController`) **về ngữ nghĩa đã đúng** với quy tắc 2. Lỗi nằm ở (a) dòng "ma" và (b) không giữ quỹ cho ycldbg đang chờ — KHÔNG phải ở cách ghi `can_request_qty`.

Tại 08/05 (lúc tạo ycldbg 1111): có dòng "ma" của PGV 10900/10993 (product 32799, qty 0) → `hasProgress=true`, `SUM(can_request_qty)=0` → `available = 1 − 0 = 1 ≥ 1` → **lọt**. Trước đó chưa hề có lần nhập KQ <100% nào ⇒ không phải TH hợp lệ.

## Phương án sửa (khuyến nghị)

**Mô hình quỹ theo từng ycldbg (khớp đúng quy tắc):**

```
Với mỗi ycldbg chưa từ chối (loại trừ ycldbg đang sửa), có detail mã này, need=1:
    reqQty = detail.qty
    Nếu ycldbg ĐÃ nhập kết quả (qua PGV của nó):
        consumption = SL hoàn thành 100% (tham chiếu can_request_qty của progress thật, assign_task_qty>0)
                      → 100%: = reqQty (giữ quỹ);  <100%: nhả phần thiếu
    Ngược lại (đang chờ, chưa có kết quả):
        consumption = reqQty            // GIỮ trọn quỹ
usedQty   = SUM(consumption)
available = warehouse_exported_qty − usedQty
```

Đặc tính:
- **Sửa D1:** điều khiển từ **bảng ycldbg** (`assembly_request_details`), KHÔNG dựa vào `exists()` của progress → dòng "ma" vô hại. Khi cần đọc kết quả, chỉ lấy progress **thật** (`assign_task_qty > 0`).
- **Sửa D2:** ycldbg đang chờ luôn giữ trọn `reqQty`.
- Giữ nguyên hành vi đúng: 100% → chặn; <100% → cho tạo phiếu cho đúng phần thiếu.

**Gộp 2 cổng về 1 nguồn chân lý (DRY):** tách 1 helper dùng chung (đề xuất: `FirmContract::getInstallableAvailableQty($productId, $unitId, $exclYcldbgId)` hoặc 1 service) để `FirmContractController` và `AssemblyRequestStoreRequest` gọi chung — tránh tái diễn lệch logic.

**Các điểm lệch cần thống nhất khi gộp** (đang khác nhau giữa 2 cổng):
- `unit_id`: `FirmContractController` group theo `product_id,unit_id`; `AssemblyRequestStoreRequest` bỏ qua unit (comment out). → chọn 1 chuẩn.
- Bộ lọc `warehouse_exported_qty`: `FirmContractController` có thêm điều kiện `need_repair=1 OR created_at < '2025-11-16'`; `StoreRequest` không có. → rà lại ý nghĩa, thống nhất.

## Phạm vi ảnh hưởng (đã verify)

- Chỉ 2 hàm trên + 1 view `assembly_requests/AssemblyRequest.blade.php`.
- **Không** đụng: luồng PGV (`WrAssignTasksController`), xuất kho (chỉ đọc `warehouse_exported_qty`), bảo hành dịch vụ (bảng `assign_task_service_progress` / `WrServiceContract*`), cách **ghi** `can_request_qty`.

## Rủi ro

- Siết quỹ có thể **chặn nhầm** ca tái lắp/sửa nếu mô hình "nhả khi <100%" tính sai → cần test kỹ 4 ca: (1) chưa giao, (2) giao 100%, (3) giao <100%, (4) nhiều ycldbg trộn lẫn.
- Logic do dev khác (`thanhtrung123`) viết → cần review chéo trước merge.

## QUYẾT ĐỊNH CUỐI (2026-06-26) — công thức chốt + 3 điểm Phase 0

Đã tự kiểm tra & verify trên dữ liệu production. Chốt:

### Công thức `getInstallableAvailableQty($contractId, $productId, $exclYcldbgId)`

```
exported = SUM(warehouse_exported_qty) các row firm_contract_tab_products
           (firm_contract_id=C OR root_firm_contract_id=C), product_id=P,
           lọc (need_repair=1 OR created_at < '2025-11-16 23:59:59')     # Q2: GIỮ lọc

used = 0
foreach ycldbg (assembly_requests ar JOIN assembly_request_details ard
                WHERE ar.firm_contract_id=C, ard.product_id=P, ard.need=1,
                      ar.status != TU_CHOI(4), ar.id != exclYcldbg
                GROUP BY ar.id):
    reqQty = SUM(ard.qty)
    real   = assign_task_progress WHERE contract_id=C, product_id=P, request_id=ar.id,
                 request_type=LAP_DAT(4), contract_type='firm', status=DA_DUYET(1),
                 assign_task_qty > 0                                      # loại dòng "ma" (D1)
    if real có row current_stage >= IMPORT_RESULT(4):       # đã nhập KQ
        used += SUM(real.can_request_qty)                   # = giao 100%; <100% tự nhả phần thiếu
    elif real không rỗng:                                   # đã giao việc, đang chờ KQ (in-flight)
        used += SUM(real.assign_task_qty)                   # giữ phần đang làm
    elif ar.status in [DANG_TAO(3), CHO_GIAO_VIEC(1), CHO_TP_DUYET(6)]:  # ycldbg chờ, chưa giao việc
        used += reqQty                                      # GIỮ trọn (D2)
    else:                                                   # đã giao việc nhưng mã bị bỏ khỏi PGV
        used += 0                                           # nhả (không còn nhu cầu thực)

available = exported − used
```

**Verify trên ca gốc (HĐ 9816 / 32799):** used = 0(554) + 1(1080,100%) + 0(1111,0%) = 1 → available = 1−1 = **0** → chặn. ✓

### 3 điểm Phase 0 đã chốt
- **Q1 — unit_id:** KHÔNG lọc theo unit, tính per `product_id` (gộp mọi unit). Theo đúng hành vi server hiện tại (`AssemblyRequestStoreRequest` đã comment-out unit), đơn giản, đúng vật lý (cùng 1 mã). 1 mã trên HĐ gần như luôn 1 unit. (Bỏ qua `unit_coefficient` — ngoài scope.)
- **Q2 — bộ lọc exported:** GIỮ `need_repair=1 OR created_at < '2025-11-16'` (lấy theo bản `FirmContractController`, vì đây là điều kiện xác định mã "được lắp đặt"). Áp **cho cả 2 cổng** để đồng bộ — hiện `AssemblyRequestStoreRequest` đang thiếu, sẽ thêm.
- **Q3 — phân biệt đã-nhập-KQ vs đang-chờ:** dùng `current_stage` (`>= IMPORT_RESULT(4)` = đã có KQ) + bắt buộc `assign_task_qty > 0` để loại dòng "ma".

### Hạn chế đã biết (chấp nhận)
- ycldbg ở trạng thái chờ (status 1/3/6) yêu cầu 1 mã nhưng bị "bỏ quên" (không reject, không giao) sẽ **giữ quỹ** tới khi reject. Cách đóng đúng là REJECT ycldbg (đã loại TU_CHOI). Không false-block ca thường.

## Dữ liệu cũ

Theo yêu cầu: **để nguyên** (ycldbg 1111 / PGV 11082 thừa) — chưa vá ở phase này.
