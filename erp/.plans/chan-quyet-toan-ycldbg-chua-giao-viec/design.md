# Chặn quyết toán HĐ khi có yêu cầu lắp đặt bàn giao chưa hoàn thành giao việc

## Mục tiêu
Bổ sung 1 điều kiện chặn khi **tạo/sửa quyết toán hợp đồng** (vật tư / dự án / DHNT — đều là `FirmContract` khác `type`): nếu HĐ có yêu cầu lắp đặt bàn giao (YCLDBG) đang trong tiến trình giao việc mà **phiếu giao việc chưa "Đã hạch toán"** → chặn + cảnh báo.

Màn: `admin/sale/settlement_contracts` (Quyết toán).

## Logic

### Logic cũ (GIỮ NGUYÊN)
Trong `FirmSettlementContractService::canCreateSettlementContract()` (nhánh `status ∈ {CO_HIEU_LUC, DANG_XUAT_HANG, DA_XUAT_HANG, DA_THANH_LY}`): nếu HĐ tích `need_install` mà chưa có `HandoverAcceptanceRecord` (biên bản bàn giao nghiệm thu) → chặn "Hợp đồng chưa có biên bản bàn giao nghiệm thu" (dòng ~149 và ~164).

### Logic mới (BỔ SUNG)
Thêm 1 khối check ngay sau khối `need_install` (trong cùng nhánh status hợp lệ, cùng hàm firm):

> HĐ có **≥1 yêu cầu lắp đặt bàn giao** (`AssemblyRequest`, `firm_contract_id = contract.id`) thỏa:
> - `status ∈ {CHO_GIAO_VIEC(1), DA_GIAO_VIEC(2), DANG_GIAO_VIEC(5), CHO_TP_DUYET(6)}` — loại trừ `DANG_TAO(3)` (nháp) và `TU_CHOI(4)` (bị từ chối); **VÀ**
> - **chưa hoàn thành hạch toán**: KHÔNG có phiếu giao việc (`WrAssignTask`) nào, HOẶC tồn tại ≥1 phiếu giao việc (gồm cả cấp con) `status ≠ KQ_DA_HACH_TOAN(2)`.
>
> → trả `[false, "Có yêu cầu lắp đặt bàn giao chưa hoàn thành giao việc"]`.

Chỉ cần **1 yêu cầu chưa hoàn thành** là chặn. 2 check (cũ + mới) độc lập, cái nào fail trước báo cái đó.

## Vị trí code
- File: `app/Services/Sale/Firm/Settlement/FirmSettlementContractService.php`, hàm `canCreateSettlementContract($contract)` (dòng ~124), thêm khối sau `need_install`.
- Hàm này được gọi từ `FirmSettlementContractService::getDataForSettlementContract` → controller `SettlementContractsController@store` và `@update` (`if (!$status) return responseErrors($message)`).
- → Chặn **cả tạo lẫn sửa**, và **FE tự hiện toastr** message (không cần sửa FE).

## Thực thể liên quan
| Model | Ý nghĩa | Field/const dùng |
|-------|---------|------------------|
| `App\Model\Customers\AssemblyRequest` | Yêu cầu lắp đặt bàn giao (YCLDBG) | `firm_contract_id`; status: CHO_GIAO_VIEC=1, DA_GIAO_VIEC=2, DANG_TAO=3, TU_CHOI=4, DANG_GIAO_VIEC=5, CHO_TP_DUYET=6 |
| `App\Model\Customers\WrAssignTask` | Phiếu giao việc / kết quả | `assembly_request_id`, `parent_id`; status: KQ_CHO_HACH_TOAN=1, **KQ_DA_HACH_TOAN=2**, KQ_DANG_TAO=3, KQ_CHO_BKS_DUYET=4 |

**Query (ĐÃ CHỐT):** chỉ cần `WrAssignTask::where('assembly_request_id', $ar->id)` — **đủ**. Đã kiểm prod: mọi task thuộc yêu cầu lắp đặt đều mang `assembly_request_id` (54 task con `assembly_request_id=null` có cha CŨNG null → không thuộc yêu cầu nào, là task WR khác). KHÔNG cần đệ quy `parent_id`.

**Thời điểm chặn (ĐÃ CHỐT — Phương án B):** chỉ chặn khi **TẠO** quyết toán, nhất quán với toàn bộ check hiện có (`update()` không re-validate; edit form ở `DANG_QUYET_TOAN` trả `[true]` sớm). Đặt check trong nhánh status tạo (`CO_HIEU_LUC/DANG_XUAT_HANG/DA_XUAT_HANG/DA_THANH_LY`), cạnh `need_install`.

## Pseudo-code
```php
$inFlow = [AssemblyRequest::CHO_GIAO_VIEC, AssemblyRequest::DA_GIAO_VIEC,
           AssemblyRequest::DANG_GIAO_VIEC, AssemblyRequest::CHO_TP_DUYET];
$requests = AssemblyRequest::where('firm_contract_id', $contract->id)
    ->whereIn('status', $inFlow)->get();
foreach ($requests as $ar) {
    $tasks = WrAssignTask::where('assembly_request_id', $ar->id)->get(); // + con qua parent_id (chốt ở plan)
    $done = $tasks->isNotEmpty()
        && $tasks->every(fn($t) => (int)$t->status === WrAssignTask::KQ_DA_HACH_TOAN);
    if (!$done) {
        return [false, "Có yêu cầu lắp đặt bàn giao chưa hoàn thành giao việc"];
    }
}
```

## Edge cases
- HĐ không có YCLDBG → không chặn (qua check này).
- Tất cả YCLDBG đã hạch toán xong → không chặn.
- YCLDBG nháp (DANG_TAO) / bị từ chối (TU_CHOI) → bỏ qua.
- YCLDBG đang trong luồng nhưng chưa tạo phiếu giao việc → chặn.
- Nhiều YCLDBG → chặn nếu bất kỳ cái nào chưa hoàn thành.

## YAGNI / Không làm
- Chỉ áp `FirmContract` (vật tư/dự án/DHNT). KHÔNG đụng quyết toán HĐ dịch vụ (WR) — service riêng, ngoài yêu cầu.
- Không sửa FE (message tự surface qua responseErrors).
- Logic cũ (need_install + biên bản) giữ nguyên.

## Test
- HĐ có YCLDBG đang giao việc (WrAssignTask status ≠ 2) → tạo/sửa quyết toán bị chặn, đúng message.
- HĐ có YCLDBG đã hạch toán hết → cho tạo/sửa.
- HĐ có YCLDBG nháp/từ chối → không chặn.
- HĐ không có YCLDBG → không chặn.
- Verify trên dev (`dev-erp.dnsmedia.vn`) + `php -l` sạch.
