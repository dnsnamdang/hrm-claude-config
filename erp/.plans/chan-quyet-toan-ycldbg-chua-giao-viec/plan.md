# Plan — Chặn quyết toán khi YCLDBG chưa hoàn thành giao việc

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (feature nhỏ, 1 task) hoặc subagent-driven-development.

**Goal:** Chặn tạo quyết toán HĐ (FirmContract: vật tư/dự án/DHNT) khi HĐ có yêu cầu lắp đặt bàn giao (`AssemblyRequest`) đang trong tiến trình giao việc mà phiếu giao việc (`WrAssignTask`) chưa "Đã hạch toán".

**Architecture:** Thêm 1 khối check vào `FirmSettlementContractService::canCreateSettlementContract()`, cạnh check `need_install` hiện có. Trả `[false, message]` → controller `store()` tự `responseErrors` → FE hiện toastr. Không sửa FE.

**Tech Stack:** PHP 7.4 / Laravel 6, Eloquent. Verify qua `php -l` + tinker trên DB dev/erp_new.

## Global Constraints
- Chỉ sửa `app/Services/Sale/Firm/Settlement/FirmSettlementContractService.php`. KHÔNG đụng FE, KHÔNG đụng logic cũ (need_install/biên bản/công nợ).
- Chặn CHỈ khi TẠO (Phương án B — nhất quán mọi check hiện có; `update()` không re-validate).
- Message chính xác: `"Có yêu cầu lắp đặt bàn giao chưa hoàn thành giao việc"`.
- Query đủ với `WrAssignTask::where('assembly_request_id', ar.id)` (không cần đệ quy parent_id — đã kiểm prod).
- Không commit/push khi chưa được yêu cầu.

---

## ✅ Task 1 (DONE — code + verify tinker/e2e, CHƯA commit):
### Task 1: Thêm check "YCLDBG chưa hoàn thành giao việc" vào canCreateSettlementContract

**Files:**
- Modify: `app/Services/Sale/Firm/Settlement/FirmSettlementContractService.php`

**Interfaces:**
- Consumes: `AssemblyRequest` (const CHO_GIAO_VIEC=1, DA_GIAO_VIEC=2, DANG_GIAO_VIEC=5, CHO_TP_DUYET=6; field `firm_contract_id`), `WrAssignTask` (const KQ_DA_HACH_TOAN=2; field `assembly_request_id`, `status`).
- Produces: `canCreateSettlementContract($contract)` trả thêm `[false, "Có yêu cầu lắp đặt bàn giao chưa hoàn thành giao việc"]` khi có YCLDBG dở.

- [x] **Step 1: Đảm bảo import 2 model**

Kiểm đầu file có `use App\Model\Customers\AssemblyRequest;` và `use App\Model\Customers\WrAssignTask;`. Nếu thiếu → thêm vào khối `use`.

Run: `grep -nE "use App\\\\Model\\\\Customers\\\\(AssemblyRequest|WrAssignTask)" app/Services/Sale/Firm/Settlement/FirmSettlementContractService.php`
Expected: 2 dòng. Nếu thiếu dòng nào → thêm.

- [x] **Step 2: Chèn khối check ngay sau khối `need_install` thứ 2 (dòng ~174), trước `} elseif`**

Tìm anchor: khối
```php
            if ($contract->need_install) {
                $record = HandoverAcceptanceRecord::query()
                    ->where([
                        'contractable_id' => $contract->id,
                        'contractable_type' => FirmContract::class
                    ])
                    ->first();
                if (!$record) {
                    return [false, "Hợp đồng chưa có biên bản bàn giao nghiệm thu"];
                }
            }
```
Chèn NGAY SAU `}` cuối khối trên (vẫn trong nhánh `if (in_array($contract->status, [...]))`):
```php

            // Chặn quyết toán nếu HĐ có yêu cầu lắp đặt bàn giao đang trong tiến trình giao việc
            // (phiếu giao việc WrAssignTask chưa "Đã hạch toán"). Chỉ tính YCLDBG đã vào luồng
            // (loại nháp DANG_TAO=3 và bị từ chối TU_CHOI=4). Chưa có phiếu giao việc nào = chưa hoàn thành.
            $assembly_requests = AssemblyRequest::query()
                ->where('firm_contract_id', $contract->id)
                ->whereIn('status', [
                    AssemblyRequest::CHO_GIAO_VIEC,
                    AssemblyRequest::DA_GIAO_VIEC,
                    AssemblyRequest::DANG_GIAO_VIEC,
                    AssemblyRequest::CHO_TP_DUYET,
                ])
                ->get();
            foreach ($assembly_requests as $assembly_request) {
                $task_statuses = WrAssignTask::query()
                    ->where('assembly_request_id', $assembly_request->id)
                    ->pluck('status');
                $all_accounted = $task_statuses->isNotEmpty()
                    && $task_statuses->every(function ($s) {
                        return (int) $s === WrAssignTask::KQ_DA_HACH_TOAN;
                    });
                if (!$all_accounted) {
                    return [false, "Có yêu cầu lắp đặt bàn giao chưa hoàn thành giao việc"];
                }
            }
```

- [x] **Step 3: `php -l` sạch**

Run: `php -l app/Services/Sale/Firm/Settlement/FirmSettlementContractService.php`
Expected: `No syntax errors detected`

- [x] **Step 4: Verify logic bằng tinker — ca CHẶN (firm_contract=21)**

Run:
```bash
php artisan tinker --execute='
use App\Model\Customers\AssemblyRequest; use App\Model\Customers\WrAssignTask;
$check=function($fcId){
  $ars=AssemblyRequest::where("firm_contract_id",$fcId)->whereIn("status",[1,2,5,6])->get();
  foreach($ars as $ar){
    $st=WrAssignTask::where("assembly_request_id",$ar->id)->pluck("status");
    $ok=$st->isNotEmpty() && $st->every(fn($s)=>(int)$s===2);
    if(!$ok) return "CHAN (ar $ar->id chua xong)";
  }
  return "QUA";
};
echo "fc=21: ".$check(21)."\n";
echo "fc=31: ".$check(31)."\n";
'
```
Expected: `fc=21: CHAN (...)` và `fc=31: QUA`.

- [x] **Step 5: Verify ca không có YCLDBG → QUA**

Run:
```bash
php artisan tinker --execute='
use App\Model\Customers\AssemblyRequest;
$fc=\App\Model\Sale\Firm\Contract\FirmContract::whereDoesntHave("assembly_requests")->value("id")
  ?? \DB::table("firm_contracts as f")->whereNotIn("f.id",function($q){$q->select("firm_contract_id")->from("assembly_requests");})->value("id");
echo "HĐ khong co YCLDBG: id=".$fc." | so ar in-flow=".AssemblyRequest::where("firm_contract_id",$fc)->whereIn("status",[1,2,5,6])->count()." (=0 => QUA)\n";
'
```
Expected: số YCLDBG in-flow = 0 → check này không chặn. (Nếu FirmContract không có relation `assembly_requests`, dùng nhánh whereNotIn.)

- [ ] **Step 6: (nếu muốn E2E) Verify qua browser trên dev**

Mở tạo quyết toán cho HĐ có YCLDBG đang giao việc (như fc=21 nếu ở dev) → phải báo toastr "Có yêu cầu lắp đặt bàn giao chưa hoàn thành giao việc", không tạo được. HĐ đã hạch toán hết (fc=31) → qua check này (có thể vướng check khác — không sao).

- [ ] **Step 7: Commit** (chỉ khi user yêu cầu)

```bash
git add app/Services/Sale/Firm/Settlement/FirmSettlementContractService.php
git commit -m "feat(settlement): chặn quyết toán khi YCLDBG chưa hoàn thành giao việc"
```

---

## Self-Review (đã chạy)
- **Spec coverage:** điều kiện chặn (status YCLDBG {1,2,5,6} + WrAssignTask chưa KQ_DA_HACH_TOAN, gồm "chưa có phiếu") → Step 2 code. Message → Step 2. Chỉ tạo (B) → đặt trong nhánh status tạo. Chỉ FirmContract → hàm firm. ✅
- **Placeholder scan:** không có TBD; code Step 2 đầy đủ.
- **Type consistency:** const `AssemblyRequest::CHO_GIAO_VIEC/...`, `WrAssignTask::KQ_DA_HACH_TOAN` đúng tên đã xác minh; field `firm_contract_id`, `assembly_request_id` đúng.

---

## Bugfix (2026-07-21) — false positive: chặn nhầm HĐ đã hoàn thành

- [x] **Fix:** check gom CẢ phiếu giao việc CHA (PGV, `parent_id=null`) lẫn phiếu duyệt kết quả con (PDKQ, `parent_id!=null`) rồi so status với `KQ_DA_HACH_TOAN=2`. Nhưng PGV dùng bộ enum RIÊNG (DA_DUYET_KET_QUA=3...) khác bộ `KQ_*` → PGV status=3 bị coi là "chưa hạch toán" → chặn nhầm. Yêu cầu gốc chỉ nói "phiếu **duyệt kết quả**" → chỉ được xét PDKQ.
  - Sửa: thêm `->whereNotNull('parent_id')` vào query `$task_statuses` (chỉ lấy PDKQ). Codebase phân biệt PGV/PDKQ bằng `parent_id` (xem `WrSettlementContractService.php:320/326`).
  - File: `app/Services/Sale/Firm/Settlement/FirmSettlementContractService.php` (đoạn foreach $assembly_requests).
- [x] **Verify (erp_new, tinker):** HĐ_TPE_HN_KD3_26_0028_003 (id 11748): trước = BLOCK (PGV 10376/10374 status=3), sau fix = **PASS** (PDKQ 11039/11040 = KQ_DA_HACH_TOAN). Đường chặn vẫn fire: AR chỉ có PGV/PDKQ rỗng (vd AR 16) → BLOCK; AR có PDKQ chưa hạch toán → BLOCK. php -l sạch.
- [ ] **Commit** (chỉ khi user yêu cầu).

### Checkpoint — 2026-07-21 (bugfix)
Vừa hoàn thành: Fix false-positive check quyết toán YCLDBG (chỉ xét PDKQ, bỏ PGV cha). Verify HĐ 11748 PASS + đường chặn còn hoạt động.
Đang làm dở: (không) — sửa 1 dòng (`whereNotNull('parent_id')`) + comment. Chưa commit.
Bước tiếp theo: user duyệt + commit; (tuỳ chọn) E2E browser.
Blocked:
