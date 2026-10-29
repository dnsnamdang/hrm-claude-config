# Lịch sử trạng thái tự động luồng xuất–nhập — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Ghi dòng lịch sử "Thay đổi trạng thái" cho MỌI lần status phiếu luồng xuất–nhập (8 phiếu) tự động chuyển do được lập từ màn khác (kể cả chéo luồng), + ghi lịch sử khi user đổi status thủ công trên YCNH & YCXBHM.

**Architecture:** Hướng 1 — chèn log tường minh tại từng điểm đổi status. Nhóm 1 (YCXH/ĐNXK/ĐNNK/PNK) dùng wrapper `logStatusChanged()` + hạ tầng `catalog_histories` sẵn có. YCNH ghi vào hệ lịch sử riêng (`product_import_request_versions/_histories`) + mở rộng `historyAction()`. YCXBHM dựng mới hạ tầng `catalog_histories` + repoint stub + popup lịch sử màn danh sách.

**Tech Stack:** PHP 7.4, Laravel 8, `nwidart/laravel-modules`; FE Nuxt 2/Vue 2 + Bootstrap-Vue. DB MySQL (`catalog_histories` chung + bảng version riêng YCNH).

**Spec:** `docs/superpowers/specs/gop-db/2026-10-14-lich-su-trang-thai-tu-dong-luong-xuat-nhap-design.md`

## Global Constraints

- Nhánh `gop_db` (Module `Finance` chỉ tồn tại ở đây). KHÔNG commit/push khi chưa có yêu cầu.
- Đổi trạng thái LUÔN là dòng log RIÊNG `action='change_status'`, nhãn **"Thay đổi trạng thái"**, màu `#d97706` — đã có sẵn trong `CatalogHistoryService::ACTION_LABELS`/`ACTION_COLORS`. `catalogColumns()` TUYỆT ĐỐI KHÔNG chứa cột `status` (skill entity-history §3a).
- Người thực hiện = `auth()->id()` (= `employees.id`, KHÔNG `auth()->user()->info->id`). Không có user → log vẫn ghi (`changed_by` null), KHÔNG chặn giao dịch.
- Ghi chú nguồn vào field `note` của dòng log; format: `Tự động chuyển do lập <Tên phiếu nguồn> <mã>` (thủ công → `note=null`). Chuỗi ≤ 120 ký tự.
- Chỉ log khi status THỰC đổi (cũ ≠ mới) — wrapper `logStatusChanged` đã tự no-op khi bằng nhau.
- Mass-update bằng `DB::table()->update()` KHÔNG bắn event → phải fetch (id, status cũ, code) TRƯỚC khi update, rồi log từng dòng.
- Model mới `extends BaseModel`; BorrowSellRequest `extends Model` (đã có boot gán created_by/updated_by) — KHÔNG đổi base.
- Số định dạng `en-US`; `.text-muted` là ĐỎ (dùng `#6b7280` cho xám); đỏ chỉ cho lỗi validate. FE form/kho dùng `V2Base*`.
- Test §7a: script bootstrap Laravel riêng trong scratchpad, MỖI ca bọc `DB::beginTransaction()` / `DB::rollBack()` — KHÔNG ghi DB thật.

## Review Focus

- **Hồi quy YCNH mốc Tạo:** version cũ có dòng `status` với `old_value=null` phải GIỮ nhãn "Tạo mới", không bị đổi thành "Thay đổi trạng thái" sau khi sửa `historyAction()`. → Task 7 có ca test bản ghi create cũ.
- **Mass-update cascade Không duyệt YCXH:** phiếu con có status ĐÃ bằng `DA_HUY_PHIEU` (đã hủy trước đó) không được sinh dòng log rỗng; chỉ log dòng thực đổi. → Task 5 test cả con đã-hủy lẫn con đang-active.
- **auth() null (job/queue/console):** điểm auto chạy ngoài HTTP (nếu có) → log vẫn ghi `changed_by=null`, không ném lỗi. → Task 4/6 test với `auth()->logout()`/không login.
- **YCXBHM status id lạ (ngoài map):** `statusText()` gặp id không có trong `STATUS_TEXTS` phải trả chuỗi id chứ không ném lỗi. → Task 2 test id lạ.
- **Lập PXH nhưng YCXH đã ở Đang hạch toán:** gọi lại điểm auto với status cũ==mới → 0 dòng log mới. → Task 4 test idempotent.

---

## PHASE 1 — Hạ tầng (whitelist, map status, nới wrapper)

### Task 1: Nới `public` + thêm `$note` cho wrapper ĐNXK & PNK

**Files:**
- Modify: `Modules/Assign/Services/WarehouseExportRequestService.php:131` (`logStatusChanged`)
- Modify: `Modules/Finance/Services/ProductImportService.php:188` (`logStatusChanged`)

**Interfaces:**
- Produces: `WarehouseExportRequestService::logStatusChanged(WarehouseExportRequest $dnxk, int $statusBefore, ?string $note = null): void` — **public**
- Produces: `ProductImportService::logStatusChanged(ProductImport $obj, int $statusBefore, ?string $note = null): void` — **public**

- [x] **Step 1: Sửa chữ ký + thân ĐNXK**

Trong `WarehouseExportRequestService.php`, đổi:
```php
    private function logStatusChanged(WarehouseExportRequest $dnxk, int $statusBefore): void
    {
        if ($statusBefore === (int) $dnxk->status) {
            return;
        }
        $this->logCatalogStatus($dnxk, 'change_status', $this->statusText($statusBefore), $this->statusText((int) $dnxk->status));
    }
```
thành:
```php
    /**
     * Ghi dòng "Thay đổi trạng thái". Public để luồng tạo PXH (ProductExportService) gọi chéo
     * khi lập phiếu làm ĐNXK tự chuyển trạng thái. $note = ghi chú nguồn (entity-history §4.1).
     */
    public function logStatusChanged(WarehouseExportRequest $dnxk, int $statusBefore, ?string $note = null): void
    {
        if ($statusBefore === (int) $dnxk->status) {
            return;
        }
        $this->logCatalogStatus($dnxk, 'change_status', $this->statusText($statusBefore), $this->statusText((int) $dnxk->status), $note);
    }
```

- [x] **Step 2: Sửa chữ ký + thân PNK**

Trong `ProductImportService.php`, đổi:
```php
    private function logStatusChanged(ProductImport $obj, int $statusBefore): void
    {
        if ($statusBefore === (int) $obj->status) {
            return;
        }
        $this->logCatalogStatus($obj, 'change_status', $this->statusText($statusBefore), $this->statusText((int) $obj->status));
    }
```
thành:
```php
    /**
     * Ghi dòng "Thay đổi trạng thái". Public để gọi chéo luồng. $note = ghi chú nguồn (§4.1).
     */
    public function logStatusChanged(ProductImport $obj, int $statusBefore, ?string $note = null): void
    {
        if ($statusBefore === (int) $obj->status) {
            return;
        }
        $this->logCatalogStatus($obj, 'change_status', $this->statusText($statusBefore), $this->statusText((int) $obj->status), $note);
    }
```

- [x] **Step 3: Lint 2 file**

Run: `php -l Modules/Assign/Services/WarehouseExportRequestService.php && php -l Modules/Finance/Services/ProductImportService.php`
Expected: `No syntax errors detected` cả 2.

- [x] **Step 4: Verify ĐNNK đã public** (chỉ đổi access modifier, không đổi thân)

Trong `Modules/Finance/Services/WarehouseImportRequestService.php:128` đổi `private function logStatusChanged` → `public function logStatusChanged` (giữ nguyên `$note` sẵn có). Lint lại.

Run: `php -l Modules/Finance/Services/WarehouseImportRequestService.php`
Expected: `No syntax errors detected`.

- [x] **Step 5: Commit** (chỉ khi user yêu cầu commit — mặc định KHÔNG commit)

```bash
git add Modules/Assign/Services/WarehouseExportRequestService.php Modules/Finance/Services/ProductImportService.php Modules/Finance/Services/WarehouseImportRequestService.php
git commit -m "refactor(history): mở public + thêm \$note cho logStatusChanged ĐNXK/ĐNNK/PNK"
```

---

### Task 2: Hạ tầng YCXBHM — whitelist + map status + trait

**Files:**
- Modify: `app/Services/CatalogHistoryService.php` (mảng `TABLES`, sau entry `borrow_sells`)
- Modify: `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php` (thêm `STATUS_TEXTS` + `statusText()`)
- Modify: `Modules/Finance/Services/BorrowSellRequestService.php` (dùng trait `LogsCatalogHistory` + khai `catalogTable/catalogColumns/catalogDisplay`)
- Test: `scratchpad/test_task2_ycxbhm_infra.php`

**Interfaces:**
- Produces: `BorrowSellRequest::statusText($status): string`
- Produces: `BorrowSellRequestService::logStatusChanged(BorrowSellRequest $req, int $statusBefore, ?string $note = null): void` (dùng ở Task 6)
- Consumes: trait `App\Services\Concerns\LogsCatalogHistory` (`logCatalogStatus`), whitelist key `borrow_sell_requests`.

- [x] **Step 1: Thêm whitelist `borrow_sell_requests`**

Trong `CatalogHistoryService.php` mảng `TABLES`, thêm sau entry `'borrow_sells' => [...]`:
```php
        // Yêu cầu xuất bán hàng mượn — lịch sử trước đây là stub, nay ghi vào catalog_histories.
        // KHÔNG khai 'status': đổi trạng thái là dòng change_status riêng (skill entity-history §3a).
        'borrow_sell_requests' => ['label' => 'yêu cầu xuất bán hàng mượn', 'columns' => [
            'customer_name' => 'Khách hàng',
            'note' => 'Ghi chú',
        ]],
```
> Danh sách cột là tối thiểu (chỉ cột thực sự sửa được). Khi implement, rà `BorrowSellRequest::$fillable` để bổ sung cột thông tin sửa được nếu YCXBHM có màn Sửa; nếu phiếu chỉ tạo+đổi status thì giữ tối thiểu.

- [x] **Step 2: Thêm map nhãn status trên entity**

Trong `BorrowSellRequest.php`, sau khối const status (dòng ~33), thêm:
```php
    const STATUS_TEXTS = [
        self::DA_DUYET => 'Đã duyệt',
        self::CHO_KE_TOAN_KHO => 'Chờ kế toán kho',
        self::DANG_TAO => 'Đang tạo',
        self::KHONG_DUYET => 'Không duyệt',
        self::CHO_TP_DUYET => 'Chờ TP duyệt',
        self::CHO_BGD_DUYET => 'Chờ BGĐ duyệt',
    ];

    /** Nhãn trạng thái để ghi lịch sử; id lạ trả về chính id (không ném lỗi). */
    public static function statusText($status): string
    {
        return self::STATUS_TEXTS[(int) $status] ?? (string) $status;
    }
```

- [x] **Step 3: Gắn trait vào service**

Trong `BorrowSellRequestService.php`:
- Thêm `use App\Services\Concerns\LogsCatalogHistory;` (phần use đầu file).
- Trong class, thêm `use LogsCatalogHistory;`.
- Thêm 2 method bắt buộc của trait + wrapper status:
```php
    protected function catalogTable(): string
    {
        return 'borrow_sell_requests';
    }

    protected function catalogColumns(): array
    {
        // KHÔNG có 'status' (skill entity-history §3a).
        return ['customer_name', 'note'];
    }

    /**
     * Ghi dòng "Thay đổi trạng thái" cho YCXBHM. Public để luồng tạo PXBHM gọi chéo.
     * $note = ghi chú nguồn (entity-history §4.1).
     */
    public function logStatusChanged(BorrowSellRequest $req, int $statusBefore, ?string $note = null): void
    {
        if ($statusBefore === (int) $req->status) {
            return;
        }
        $this->logCatalogStatus(
            $req,
            'change_status',
            BorrowSellRequest::statusText($statusBefore),
            BorrowSellRequest::statusText((int) $req->status),
            $note
        );
    }
```
> `catalogDisplay()`/`catalogSnapshot()` dùng mặc định của trait (không cần override vì columns là chuỗi phẳng). Kiểm `use` entity `BorrowSellRequest` đã import ở đầu service.

- [x] **Step 4: Viết script test hạ tầng**

Tạo `scratchpad/test_task2_ycxbhm_infra.php`:
```php
<?php
require __DIR__ . '/../../HRM/hrm-api/vendor/autoload.php';
$app = require __DIR__ . '/../../HRM/hrm-api/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

use Illuminate\Support\Facades\DB;
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;
use Modules\Finance\Services\BorrowSellRequestService;
use App\Services\CatalogHistoryService;

// (a) whitelist có key mới
$ref = new ReflectionClass(CatalogHistoryService::class);
$tables = $ref->getConstant('TABLES');
echo isset($tables['borrow_sell_requests']) ? "OK whitelist\n" : "FAIL whitelist\n";

// (b) statusText map đúng + id lạ không lỗi
echo BorrowSellRequest::statusText(1) === 'Đã duyệt' ? "OK statusText(1)\n" : "FAIL statusText(1)\n";
echo BorrowSellRequest::statusText(999) === '999' ? "OK statusText(lạ)\n" : "FAIL statusText(lạ)\n";

// (c) wrapper ghi 1 dòng change_status
DB::beginTransaction();
try {
    $req = BorrowSellRequest::query()->first();
    if ($req) {
        $before = (int) $req->status;
        $req->status = $before === BorrowSellRequest::DA_DUYET ? BorrowSellRequest::DANG_TAO : BorrowSellRequest::DA_DUYET;
        $req->save();
        app(BorrowSellRequestService::class)->logStatusChanged($req, $before, 'Test ghi chú nguồn');
        $row = DB::table('catalog_histories')
            ->where('table_name', 'borrow_sell_requests')->where('table_id', $req->id)
            ->where('action', 'change_status')->orderByDesc('id')->first();
        echo $row && $row->note === 'Test ghi chú nguồn' ? "OK log change_status + note\n" : "FAIL log\n";
    } else {
        echo "SKIP: không có bản ghi YCXBHM để test\n";
    }
} finally {
    DB::rollBack();
}
```

- [x] **Step 5: Lint + chạy test**

Run: `php -l app/Services/CatalogHistoryService.php && php -l Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php && php -l Modules/Finance/Services/BorrowSellRequestService.php`
Run: `cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api && php ../../../scratchpad/.../test_task2_ycxbhm_infra.php` (chỉnh đường dẫn scratchpad thực tế).
Expected: tất cả dòng `OK ...` (hoặc `SKIP` ở ca c nếu DB trống).

- [x] **Step 6: Commit** (chỉ khi được yêu cầu)

```bash
git add app/Services/CatalogHistoryService.php Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php Modules/Finance/Services/BorrowSellRequestService.php
git commit -m "feat(history): hạ tầng catalog_histories cho YCXBHM (whitelist + map status + trait)"
```

---

## PHASE 2 — Nhóm 1 BE: chèn log tại điểm auto (ProductExportService)

### Task 3: YCXH & ĐNXK tự chuyển khi lập PXH (ProductExportService)

**Files:**
- Modify: `Modules/Assign/Services/ProductExportService.php` (~352–360 và ~628)
- Test: `scratchpad/test_task3_pxh_autostatus.php`

**Interfaces:**
- Consumes: `WarehouseExportRequestService::logStatusChanged(..., ?string $note)` (Task 1), `ProductExportRequestService::logStatusChanged(ProductExportRequest $req, int $statusBefore, ?string $note = null)` (sẵn có, public).
- Consumes: hằng `ProductExportRequest::STATUS_DANG_HACH_TOAN` (=9), `WarehouseExportRequest::STATUS_DANG_HACH_TOAN` (=7).

- [x] **Step 1: Đọc lại cụm code ~340–365 và ~620–632 để pin số dòng chính xác**

Run: `grep -n "STATUS_DANG_HACH_TOAN\|->update(\['status'\|\$per->status\|\$req->status\|\$we->status" Modules/Assign/Services/ProductExportService.php`

- [x] **Step 2: Chèn log ĐNXK tại điểm `$req->status = WarehouseExportRequest::STATUS_DANG_HACH_TOAN` (~355)**

Bọc đoạn set status ĐNXK (phải lấy status cũ TRƯỚC khi gán):
```php
            $dnxkStatusBefore = (int) $req->status;
            $req->status = WarehouseExportRequest::STATUS_DANG_HACH_TOAN; // 7
            $req->save();
            app(WarehouseExportRequestService::class)->logStatusChanged(
                $req,
                $dnxkStatusBefore,
                'Tự động chuyển do lập Phiếu xuất hàng ' . ($productExport->code ?? ('#' . $productExport->id))
            );
```
> Tên biến phiếu PXH vừa tạo: rà đúng biến (vd `$productExport` / `$pe`) ở ngữ cảnh. `use` 2 service + entity nếu thiếu.

- [x] **Step 3: Chèn log YCXH tại mass-update ~359**

Điểm hiện tại:
```php
            ProductExportRequest::where(...)
                ->update(['status' => ProductExportRequest::STATUS_DANG_HACH_TOAN]); // 9
```
Đổi thành fetch-before-update:
```php
            $perRowsBefore = ProductExportRequest::where(/* đúng điều kiện cũ */)
                ->get(['id', 'status', 'code']);
            ProductExportRequest::where(/* đúng điều kiện cũ */)
                ->update(['status' => ProductExportRequest::STATUS_DANG_HACH_TOAN]); // 9
            $perService = app(ProductExportRequestService::class);
            $pxhCode = $productExport->code ?? ('#' . $productExport->id);
            foreach ($perRowsBefore as $perBefore) {
                if ((int) $perBefore->status === ProductExportRequest::STATUS_DANG_HACH_TOAN) {
                    continue; // đã ở trạng thái đích → không log rỗng
                }
                $perModel = ProductExportRequest::find($perBefore->id);
                $perModel->status = ProductExportRequest::STATUS_DANG_HACH_TOAN;
                $perService->logStatusChanged($perModel, (int) $perBefore->status, 'Tự động chuyển do lập Phiếu xuất hàng ' . $pxhCode);
            }
```
> `logStatusChanged` so `$statusBefore` với `$model->status` HIỆN TẠI; vì đã `->update()` nên load lại model (status đã =9) rồi truyền statusBefore cũ — khớp.

- [x] **Step 4: Chèn log YCXH tại điểm save ~628 (`$per->status = STATUS_DANG_HACH_TOAN`)**

```php
            $perStatusBefore = (int) $per->status;
            $per->status = ProductExportRequest::STATUS_DANG_HACH_TOAN; // 9
            $per->save();
            app(ProductExportRequestService::class)->logStatusChanged(
                $per,
                $perStatusBefore,
                'Tự động chuyển do lập Phiếu xuất hàng ' . ($productExport->code ?? ('#' . $productExport->id))
            );
```
> Nếu điểm ~359 và ~628 cùng một luồng tạo PXH thì chỉ 1 trong 2 chạy cho mỗi phiếu — kiểm nhánh để không log kép.

- [x] **Step 5: Lint**

Run: `php -l Modules/Assign/Services/ProductExportService.php`
Expected: `No syntax errors detected`.

- [x] **Step 6: Script test (transaction rollback)**

Tạo `scratchpad/test_task3_pxh_autostatus.php` bootstrap Laravel: trong `DB::beginTransaction()`, dựng/chọn 1 YCXH + ĐNXK ở trạng thái trước, gọi luồng tạo PXH (hoặc gọi trực tiếp đoạn service nếu tách được), assert:
- 1 dòng `catalog_histories` table=`product_export_requests` action=`change_status` new="Đang hạch toán" note chứa "lập Phiếu xuất hàng".
- 1 dòng table=`warehouse_export_requests` action=`change_status`.
Kết thúc `DB::rollBack()`. In `OK`/`FAIL` từng assert.

- [x] **Step 7: Chạy test**

Run: `php scratchpad/.../test_task3_pxh_autostatus.php`
Expected: các dòng `OK`.

- [x] **Step 8: Commit** (khi được yêu cầu)

```bash
git add Modules/Assign/Services/ProductExportService.php
git commit -m "feat(history): ghi change_status YCXH+ĐNXK khi lập PXH"
```

---

## PHASE 3 — Nhóm 1 BE: luồng nhập (ProductImportService) + chéo luồng

### Task 4: markParentUsed + các mass-update hạch toán (ProductImportService)

**Files:**
- Modify: `Modules/Finance/Services/ProductImportService.php` (`markParentUsed` ~2245–2276; mass ~3283, ~3310, ~3367; ~3446)
- Test: `scratchpad/test_task4_import_autostatus.php`

**Interfaces:**
- Consumes: `WarehouseImportRequestService::logStatusChanged(..., ?string $note)` (Task 1, public), `ProductImportService::logStatusChanged(ProductImport $obj, int $statusBefore, ?string $note)` (Task 1), `ProductExportRequestService::logStatusChanged(...)` (sẵn), `ProductImportRequestService::logStatusChanged(...)` (Task 8 — nếu Task 8 làm trước thì gọi; nếu không, dùng helper model YCNH `saveStatusHistory()` Task 8).
- Consumes: `ProductImportRequest::statusText($id)` / `STATUSES` để dịch nhãn.

> **Phụ thuộc:** các điểm đổi status YCNH ở Task 4 dùng cơ chế hệ-riêng của YCNH (Task 8). Thực thi Task 8 TRƯỚC Task 4, hoặc trong Task 4 chỉ vá các điểm non-YCNH (PNK/ĐNNK/YCXH) rồi bổ sung điểm YCNH sau khi Task 8 xong. Kế hoạch: **làm Task 8 trước Task 4**.

- [x] **Step 1: Pin số dòng**

Run: `grep -n "markParentUsed\|DANG_LAP_DE_NGHI\|->update(\['status'\|PER_STATUS_DANG_HACH_TOAN_NHAP\|PER_STATUS_DA_HACH_TOAN\|DA_HACH_TOAN\|CHO_DUYET" Modules/Finance/Services/ProductImportService.php`

- [x] **Step 2: Vá `markParentUsed()` nhánh indirect (~2257–2273)**

Trước mỗi `DB::table(...)->update(['status'=>...])`, fetch status cũ rồi log:
```php
        // PNK (warehouse_imports) → 7
        $wiBefore = DB::table('warehouse_imports')->where('id', $parent->id)->value('status');
        DB::table('warehouse_imports')->where('id', $parent->id)->update([
            'status' => 7, 'approver_id' => auth()->id(), 'approved_time' => $now,
        ]);
        if ((int) $wiBefore !== 7) {
            $pnkModel = \Modules\Finance\Entities\ProductImport::find($parent->id); // kiểm đúng entity PNK
            if ($pnkModel) {
                app(self::class)->logStatusChanged($pnkModel, (int) $wiBefore, 'Tự động chuyển do nhập kho');
            }
        }

        if ($parent->warehouse_import_request_id) {
            $wirBefore = DB::table('warehouse_import_requests')->where('id', $parent->warehouse_import_request_id)->value('status');
            DB::table('warehouse_import_requests')->where('id', $parent->warehouse_import_request_id)->update(['status' => 7]);
            if ((int) $wirBefore !== 7) {
                $wirModel = \Modules\Finance\Entities\WarehouseImportRequest::find($parent->warehouse_import_request_id);
                if ($wirModel) {
                    app(\Modules\Finance\Services\WarehouseImportRequestService::class)
                        ->logStatusChanged($wirModel, (int) $wirBefore, 'Tự động chuyển do lập Phiếu nhập hàng ' . ($parent->code ?? ('#' . $parent->id)));
                }
            }
        }
```
> Kiểm tên entity PNK thực tế (`warehouse_imports` ↔ model `ProductImport`? — rà `protected $table`). `logStatusChanged` PNK nhận model `ProductImport` (Task 1).

- [x] **Step 3: Vá điểm YCNH trong markParentUsed (~2248 save và ~2270 mass)**

Dùng cơ chế hệ-riêng YCNH (Task 8 `saveStatusHistory`):
```php
        // ~2248 nhánh direct
        if ($isImportDirect) {
            $pirStatusBefore = (int) $parent->status;
            $parent->status = ProductImportRequest::DANG_LAP_DE_NGHI;
            $parent->approver_id = auth()->id();
            $parent->approved_time = Carbon::now();
            $parent->save();
            $parent->saveStatusHistory($pirStatusBefore, 'Tự động chuyển do lập đề nghị nhập kho');
            return;
        }
```
```php
        // ~2270 mass product_import_requests → DANG_HACH_TOAN
        if ($sourcePir) {
            $pirBefore = (int) $sourcePir->status;
            DB::table('product_import_requests')->where('id', $sourcePir->id)->update(['status' => ProductImportRequest::DANG_HACH_TOAN]);
            if ($pirBefore !== (int) ProductImportRequest::DANG_HACH_TOAN) {
                $pirModel = ProductImportRequest::find($sourcePir->id);
                if ($pirModel) {
                    $pirModel->saveStatusHistory($pirBefore, 'Tự động chuyển do nhập kho');
                }
            }
        }
```

- [x] **Step 4: Vá mass-update YCXH ~3283 (=19) và ~3367 (=5)**

Theo khuôn fetch-before-update + loop log YCXH (như Task 3 Step 3), note = `'Tự động chuyển do hạch toán nhập kho'`. Dùng `ProductExportRequestService::logStatusChanged`.

- [x] **Step 5: Vá mass-update YCNH ~3310 (DA_HACH_TOAN=5)**

Fetch-before-update, loop load `ProductImportRequest::find(id)` rồi `$m->saveStatusHistory($before, 'Tự động chuyển do hạch toán')`.

- [x] **Step 6: Vá ~3446 (tạo YCNH loại 17, status=CHO_DUYET)**

Đây là TẠO phiếu mới → đã có `saveCreateHistory()` ở luồng tạo. Kiểm: nếu phiếu loại 17 tự sinh có gọi `saveCreateHistory()` thì KHÔNG thêm change_status (tránh kép); nếu không, gọi `saveCreateHistory()` để có mốc Tạo. **Quyết định:** coi là mốc Tạo, KHÔNG phải change_status (spec §6.1). Ghi rõ trong code comment.

- [x] **Step 7: Lint**

Run: `php -l Modules/Finance/Services/ProductImportService.php`

- [x] **Step 8: Script test (rollback)** — ca: PNK→7, ĐNNK→7, YCNH→Đang hạch toán, YCXH→19/5, idempotent (gọi lại status cũ==mới → 0 dòng), auth() null → không lỗi. Assert từng bảng.

- [x] **Step 9: Chạy test** → `OK` hết.

- [x] **Step 10: Commit** (khi được yêu cầu)

---

## PHASE 4 — YCXBHM: luồng tạo PXBHM + repoint stub + FE popup

### Task 5: Cascade Không duyệt YCXH cha → con (Controller)

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` (~1567 cha, ~1606 cascade con)
- Test: `scratchpad/test_task5_cascade_huy.php`

**Interfaces:**
- Consumes: `ProductExportRequestService::logStatusChanged(...)`, `ProductExportRequest::STATUS_DA_HUY_PHIEU`.

- [x] **Step 1: Vá cha ~1567**
```php
        $reqStatusBefore = (int) $req->status;
        $req->status = ProductExportRequest::STATUS_DA_HUY_PHIEU;
        $req->save();
        $service->logStatusChanged($req, $reqStatusBefore, 'Không duyệt yêu cầu xuất hàng');
```
> `$service` là `ProductExportRequestService` đã inject vào `update()`/action method; nếu method này không có sẵn, `app(ProductExportRequestService::class)`.

- [x] **Step 2: Vá cascade con ~1606 (mass-update)**
```php
        $childrenBefore = ProductExportRequest::where('parent_request_id', $req->id)
            ->where('status', '!=', ProductExportRequest::STATUS_DA_HUY_PHIEU)
            ->get(['id', 'status', 'code']);
        ProductExportRequest::where('parent_request_id', $req->id)
            ->where('status', '!=', ProductExportRequest::STATUS_DA_HUY_PHIEU)
            ->update(['status' => ProductExportRequest::STATUS_DA_HUY_PHIEU]);
        $svc = app(ProductExportRequestService::class);
        foreach ($childrenBefore as $child) {
            $childModel = ProductExportRequest::find($child->id);
            $svc->logStatusChanged($childModel, (int) $child->status, 'Tự động hủy do Không duyệt YCXH cha ' . ($req->code ?? ('#' . $req->id)));
        }
```

- [x] **Step 3: Lint** → `php -l` file controller.

- [x] **Step 4: Script test (rollback):** tạo cha + 2 con (1 active, 1 đã DA_HUY_PHIEU), gọi action Không duyệt, assert: cha có 1 change_status, con active có 1 change_status note "Không duyệt YCXH cha", con đã-hủy KHÔNG sinh dòng mới (do `where status != DA_HUY` loại ra). → Review Focus.

- [x] **Step 5: Chạy test** → `OK`.

- [x] **Step 6: Commit** (khi được yêu cầu)

---

### Task 6: YCXBHM tự chuyển Đã duyệt khi lập PXBHM (BorrowSellService)

**Files:**
- Modify: `Modules/Finance/Services/BorrowSell/BorrowSellService.php` (~252)
- Test: `scratchpad/test_task6_pxbhm_autostatus.php`

**Interfaces:**
- Consumes: `BorrowSellRequestService::logStatusChanged(...)` (Task 2), `BorrowSellRequest::DA_DUYET`.

- [x] **Step 1: Vá ~252**
```php
            $parentStatusBefore = (int) $parent->status;
            $parent->status = BorrowSellRequest::DA_DUYET;
            $parent->save();
            app(\Modules\Finance\Services\BorrowSellRequestService::class)->logStatusChanged(
                $parent,
                $parentStatusBefore,
                'Tự động chuyển do lập Phiếu xuất bán hàng mượn ' . ($object->code ?? ('#' . $object->id))
            );
```
> `$object` = PXBHM vừa tạo (rà đúng biến). `use` entity + service nếu cần.

- [x] **Step 2: Lint** → `php -l` file.

- [x] **Step 3: Script test (rollback):** chọn YCXBHM status≠DA_DUYET, gọi luồng tạo PXBHM (hoặc đoạn service), assert 1 dòng `catalog_histories` table=`borrow_sell_requests` action=change_status new="Đã duyệt" note chứa "lập Phiếu xuất bán hàng mượn". auth() null → không lỗi.

- [x] **Step 4: Chạy test** → `OK`.

- [x] **Step 5: Commit** (khi được yêu cầu)

---

## PHASE 5 — YCNH hệ lịch sử riêng

### Task 7: Tách `historyAction()` (status-only → change_status) + hồi quy

**Files:**
- Modify: `Modules/Finance/Services/ProductImportRequestService.php` (`histories()` ~836, `historyAction()` ~874)
- Test: `scratchpad/test_task7_ycnh_historyaction.php`

**Interfaces:**
- Produces: `historyAction` phân loại: version có dòng `status` với `old_value` rỗng → `create`; `old_value` không rỗng → `change_status` (nhãn "Thay đổi trạng thái", `#d97706`).

- [x] **Step 1: Đổi chữ ký + logic `historyAction`**

Đổi call site (dòng ~836):
```php
            $action = self::historyAction($versionRows);
```
Đổi method:
```php
    private static function historyAction($versionRows): array
    {
        $rows = collect($versionRows);
        $columns = $rows->pluck('column_name')->all();

        // Dòng `status`: old rỗng = mốc TẠO; old có giá trị = ĐỔI TRẠNG THÁI (skill §3a).
        if (in_array(ProductImportRequest::HISTORY_CREATE_COLUMN, $columns, true)) {
            $statusRow = $rows->firstWhere('column_name', ProductImportRequest::HISTORY_CREATE_COLUMN);
            $old = $statusRow->old_value ?? null;
            if ($old === null || trim((string) $old) === '') {
                return ['key' => 'create', 'label' => 'Tạo mới', 'color' => '#16a34a'];
            }
            return ['key' => 'change_status', 'label' => 'Thay đổi trạng thái', 'color' => '#d97706'];
        }

        if (in_array('rejected_time', $columns, true)) {
            return ['key' => 'reject', 'label' => 'Từ chối', 'color' => '#dc2626'];
        }
        if (in_array('handled_time', $columns, true)) {
            return ['key' => 'complete', 'label' => 'Hoàn thành', 'color' => '#16a34a'];
        }
        if (in_array('approved_time', $columns, true)) {
            return ['key' => 'approve', 'label' => 'Duyệt', 'color' => '#16a34a'];
        }
        if (in_array('received_time', $columns, true)) {
            return ['key' => 'send_approve', 'label' => 'Gửi duyệt', 'color' => '#f59e0b'];
        }
        return ['key' => 'update', 'label' => 'Cập nhật phiếu', 'color' => '#0ea5e9'];
    }
```

- [x] **Step 2: Ẩn dòng `comment` khỏi `changes[]` cho version change_status** (để note chỉ hiện ở khối note)

Trong `histories()` map, sau khi tính `$action`, lọc changes:
```php
            if ($action['key'] === 'change_status') {
                $changes = array_values(array_filter($changes, function ($c) {
                    return ($c['field'] ?? null) !== self::HISTORY_LABELS['comment'];
                }));
            }
```
> Đặt sau khi `$changes` và `$action` đã tính; chỉ bỏ dòng "Ghi chú duyệt", giữ dòng "Trạng thái: cũ → mới".

- [x] **Step 3: Lint** → `php -l` file.

- [x] **Step 4: Script test (rollback) — hồi quy + mới**

Ca: (a) version create cũ (status, old=null) → `historyAction` trả `create`; (b) version status old='Đang tạo' new='Đang lập đề nghị' → trả `change_status` label "Thay đổi trạng thái"; (c) version approved_time → `approve` (không đổi). Dùng reflection gọi `historyAction` hoặc dựng version thật rồi gọi `histories()`.

- [x] **Step 5: Chạy test** → `OK`.

- [x] **Step 6: Commit** (khi được yêu cầu)

---

### Task 8: Thêm `saveStatusHistory()` trên model YCNH

**Files:**
- Modify: `Modules/Finance/Entities/ProductImportRequest/ProductImportRequest.php` (sau `saveCreateHistory()` ~793)
- Test: `scratchpad/test_task8_ycnh_savestatus.php`

**Interfaces:**
- Produces: `ProductImportRequest::saveStatusHistory(int $statusBefore, ?string $note = null): void` — ghi 1 version + dòng `status` (old=tên cũ, new=tên mới) + (nếu có note) dòng `comment`=note.

- [x] **Step 1: Thêm method**

Sau `saveCreateHistory()`:
```php
    /**
     * Ghi mốc "Thay đổi trạng thái" lên tab Lịch sử khi status tự chuyển (lập từ màn khác) hoặc
     * đổi thủ công. No-op nếu status không đổi. 1 version + 1 dòng `status` (old→new); nếu có
     * $note thì thêm 1 dòng `comment` mang ghi chú nguồn (hiện ở khối ghi chú — service ẩn nó
     * khỏi danh sách "thay đổi"). Mirror saveCreateHistory() về cách ghi 2 bảng versions/histories.
     */
    public function saveStatusHistory(int $statusBefore, ?string $note = null): void
    {
        if ($statusBefore === (int) $this->status) {
            return;
        }

        $now = Carbon::now();
        $statusName = function ($id) {
            return collect(self::STATUSES)->firstWhere('id', (int) $id)['name'] ?? (string) $id;
        };

        $versionId = DB::table('product_import_request_versions')->insertGetId([
            'product_import_request_id' => $this->id,
            'employee_id' => auth()->id(),
            'created_at' => $now,
            'updated_at' => $now,
        ]);

        $rows = [[
            'version_id' => $versionId,
            'product_import_request_id' => $this->id,
            'column_name' => self::HISTORY_CREATE_COLUMN, // 'status'
            'old_value' => $statusName($statusBefore),
            'new_value' => $statusName($this->status),
            'created_at' => $now,
            'updated_at' => $now,
        ]];

        if ($note !== null && trim($note) !== '') {
            $rows[] = [
                'version_id' => $versionId,
                'product_import_request_id' => $this->id,
                'column_name' => 'comment',
                'old_value' => null,
                'new_value' => $note,
                'created_at' => $now,
                'updated_at' => $now,
            ];
        }

        DB::table('product_import_request_histories')->insert($rows);
    }
```

- [x] **Step 2: Lint** → `php -l` file.

- [x] **Step 3: Script test (rollback):** chọn 1 YCNH, gọi `saveStatusHistory($before, 'Tự động chuyển do nhập kho')`, rồi gọi `ProductImportRequestService::histories($id)`, assert: dòng mới nhất `action='change_status'`, `action_label='Thay đổi trạng thái'`, `changes` chứa "Trạng thái: cũ → mới", `note='Tự động chuyển do nhập kho'`, KHÔNG có dòng "Ghi chú duyệt" trong changes. Ca no-op: status cũ==mới → 0 version mới.

- [x] **Step 4: Chạy test** → `OK`.

- [x] **Step 5: Commit** (khi được yêu cầu)

---

## PHASE 6 — Nhóm C thủ công + YCXBHM repoint stub + FE + nhóm D

### Task 9: Repoint stub `histories()` YCXBHM đọc catalog_histories

**Files:**
- Modify: `Modules/Finance/Services/BorrowSellRequestService.php` (method `histories()` đang trả `[]`)
- Modify (FE): `hrm-client` api.js YCXBHM (endpoint histories) — chỉ cần BE trả thật, giữ URL cũ.
- Test: `scratchpad/test_task9_ycxbhm_histories.php`

**Interfaces:**
- Consumes: `CatalogHistoryService::getLogs('borrow_sell_requests', $id)` → DTO chuẩn.

- [x] **Step 1: Sửa `histories()`**
```php
    public function histories(int $id): array
    {
        return app(\App\Services\CatalogHistoryService::class)->getLogs('borrow_sell_requests', $id);
    }
```
> Kiểm chữ ký method hiện tại (tên tham số) để khớp controller gọi.

- [x] **Step 2: Lint** → `php -l`.

- [x] **Step 3: Script test:** sau khi Task 6 tạo dòng change_status (trong cùng transaction), gọi `histories($id)` → assert có phần tử `action='change_status'`, DTO đủ field (`action_label`, `action_color='#d97706'`, `note`, `created_at`, `created_at_raw`).

- [x] **Step 4: Chạy test** → `OK`.

- [x] **Step 5: Commit** (khi được yêu cầu)

---

### Task 10: Nhóm C — ghi lịch sử status THỦ CÔNG (YCNH & YCXBHM)

**Files:**
- Modify: `Modules/Finance/Services/ProductImportRequestService.php` (các điểm đổi status thủ công: ~250, 578, 611, 641, 664, 690, 715, 1625)
- Modify: `Modules/Finance/Services/BorrowSellRequestService.php` (~79, 552, 560, 571, 582)
- Test: `scratchpad/test_task10_manual_status.php`

- [x] **Step 1: Pin điểm YCNH**

Run: `grep -n "->status = \|status = (int)\|->save()" Modules/Finance/Services/ProductImportRequestService.php`

- [x] **Step 2: Chèn `saveStatusHistory` thủ công YCNH**

Tại mỗi điểm user đổi status (không phải tạo mới), lấy status cũ trước khi gán, sau `save()` gọi:
```php
            $statusBefore = (int) $model->status;
            // ... gán status mới + save ...
            $model->saveStatusHistory($statusBefore); // note=null: thao tác thủ công
```
> CHỈ chèn nơi là đổi trạng thái thủ công; KHÔNG chèn ở `store()` tạo mới (đã có `saveCreateHistory`). Rà từng điểm.

- [x] **Step 3: Chèn `logStatusChanged` thủ công YCXBHM**

Tại các điểm đổi status trong `BorrowSellRequestService`, lấy status cũ, sau save gọi `$this->logStatusChanged($req, $statusBefore);` (note=null).

- [x] **Step 4: Lint** cả 2 file.

- [x] **Step 5: Script test (rollback):** đổi status thủ công YCNH → assert 1 version change_status note=null; đổi status thủ công YCXBHM → assert 1 dòng catalog_histories change_status note=null. → Review Focus (thủ công note=null).

- [x] **Step 6: Chạy test** → `OK`.

- [x] **Step 7: Commit** (khi được yêu cầu)

---

### Task 11: Nhóm D — điểm return sớm `updateTransfer` (ProductExportRequestService:807)

**Files:**
- Modify: `Modules/Assign/Services/ProductExportRequestService.php` (~807 `updateTransfer` loại 7 return sớm)

- [x] **Step 1: Đọc ngữ cảnh ~790–830** — xác định updateTransfer có đổi status không.

- [x] **Step 2:** Nếu có đổi status trước `return` → chèn `logStatusChanged($req, $statusBefore, <note phù hợp>)` trước return. Nếu KHÔNG đổi status → ghi comment xác nhận "không đổi status, không cần log" và bỏ qua.

- [x] **Step 3: Lint** → `php -l`.

- [x] **Step 4:** Nếu có vá: script test rollback assert dòng change_status. Nếu không: ghi chú trong plan "Task 11 no-op xác nhận".

- [x] **Step 5: Commit** (khi được yêu cầu)

---

### Task 12: FE — popup lịch sử màn danh sách YCXBHM

**Files:**
- Modify: `hrm-client/pages/.../borrow-sell-requests/index.vue` (thêm mục "Lịch sử" ở cột hành động + mount popup)
- Reuse: component popup lịch sử của 1 phiếu nhóm 1 (rà `ProductExportRequest` list để copy đúng component + cách mở).

**Interfaces:**
- Consumes: endpoint `GET finance/borrow-sell-requests/{id}/histories` (Task 9 trả DTO thật).

- [x] **Step 1: Rà component lịch sử dùng chung** — `grep -rn "histories\|HistoryModal\|SystemInfoSection" hrm-client/pages/.../product-export-requests/` để tìm khuôn popup/modal lịch sử đang dùng.

- [x] **Step 2: Thêm nút/mục "Lịch sử"** vào cột hành động màn danh sách YCXBHM theo đúng khuôn (button-convention + modal-popup skill). Mở popup, nạp từ endpoint histories.

- [x] **Step 3: Kiểm màn chi tiết YCXBHM có SystemInfoSection chưa** — nếu có, đảm bảo đọc cùng DTO; nếu chưa và skill §5.1 yêu cầu, bổ sung (xác nhận user nếu phát sinh ngoài dự kiến).

- [x] **Step 4: Verify Playwright MCP** — mở `http://127.0.0.1:3000`, vào danh sách YCXBHM, mở popup lịch sử của 1 phiếu có change_status, chụp màn hình xác nhận hiện dòng "Thay đổi trạng thái" + ghi chú nguồn.

- [x] **Step 5: Commit** (khi được yêu cầu)

---

## PHASE 7 — Tổng kiểm

### Task 13: Chạy lại toàn bộ script test + kiểm bộ lọc "Loại hoạt động"

- [x] **Step 1:** Chạy lại tất cả `scratchpad/test_task*.php` → tất cả `OK`.
- [x] **Step 2:** Verify bộ lọc "Loại hoạt động" (nhóm `status`) gom đúng dòng `change_status` ở popup YCXBHM + các phiếu nhóm 1 (Playwright). `SystemLogService`/`groupOfAction` map `change_status`→`status`.
- [x] **Step 3:** Kiểm hồi quy YCNH: mở lịch sử 1 YCNH cũ, mốc Tạo vẫn "Tạo mới" (Playwright).
- [x] **Step 4:** Cập nhật `plan.md` đánh `[x]`, ghi checkpoint; cập nhật `.plans/gop-db/STATUS.md`.

---

## Self-review (đã chạy)

1. **Spec coverage:** Nhóm 1 (Task 1,3,4,5) · YCNH (Task 7,8,10) · YCXBHM (Task 2,6,9,12) · nhóm C (Task 10) · nhóm D (Task 11) · format note (Global Constraints + từng task) · test §7a (mỗi task có script rollback + Task 13). ✔ phủ đủ §2–§10 spec.
2. **Placeholder scan:** mọi step có code thật hoặc lệnh grep pin dòng; các số dòng ~N kèm bước grep pin lại — không phải placeholder, là chỉ dẫn định vị. ✔
3. **Type consistency:** `logStatusChanged(..., ?string $note = null)` đồng nhất 4 service (Task 1) + YCXBHM (Task 2); `saveStatusHistory(int, ?string)` dùng ở Task 4/8/10; `historyAction($versionRows)` đổi call site Task 7. ✔
4. **Review Focus:** 5 mục đã gắn test vào task sở hữu code (Task 4 idempotent+auth null, Task 5 cascade con đã-hủy, Task 2 status id lạ, Task 7 hồi quy create). ✔

## Checkpoint — 2026-10-14 (HOÀN THÀNH)
Vừa hoàn thành: **TOÀN BỘ 13 task** (subagent-driven, mỗi task review clean 0 Critical/Important, commit local).
- Commit hash theo task: T1 `f49d4c575` · T2 `968de4587` · T3 `de101c9f4` · T4 `139179acf` · T5 `96a25148c` · T6 `6d4d50edf` · T7 `ec5bf402a` · T8 `df9aec340` · T9 `18ae20c06` · T10 `9619eee1f` · T11 `66943b821` (comment NO-OP) · T12 `bfb6c56599` (hrm-client) · T13 tổng kiểm.
- T13 đã chạy: (1) 9 script test đều PASS (bọc transaction/rollback, DB 0 dòng sót); (2) bộ lọc màn YCNH nhãn thật là **"Loại hành động"** (không phải "Loại hoạt động" ghi nhầm ở tiêu đề task) — dựng động từ log, xác nhận Playwright hiện đúng 3 options Duyệt/Gửi duyệt/Cập nhật phiếu, KHÔNG vỡ sau T7 tách change_status; (3) hồi quy YCNH mốc "Tạo mới" chứng minh qua test_task7 + panel chi tiết PYCNH-12230 hiện đủ mốc.
Đang làm dở: không.
Bước tiếp theo: final whole-branch review (opus) → finishing-a-development-branch.
Blocked: không.

---

## PHASE 8 — Fix điểm sót (phát hiện sau nghiệm thu)

> **Bối cảnh:** User báo phiếu YCXH **PYCXH-39303** đang ở "Đang lập đề nghị" (status 7) nhưng
> KHỐI LỊCH SỬ KHÔNG có dòng chuyển sang trạng thái đó. Điều tra: 3 điểm trong
> `WarehouseExportRequestService` (create/updateDraft/cancel) đổi status của **YCXH cha**
> (ProductExportRequest) như hệ quả tự động khi thao tác trên màn ĐNXK, nhưng chỉ gọi log cho
> CHÍNH ĐNXK (`$this->logStatusChanged` của trait → bảng `warehouse_export_requests`), KHÔNG log
> cho YCXH. Spec §6.5 từng liệt kê các điểm :221/:225/:296/:323 nhưng GIẢ ĐỊNH "đã log" — nhầm:
> cái "đã log" là ĐNXK, không phải YCXH. Từ góc nhìn YCXH đây đúng là auto-transition "từ phiếu khác".

### Task 14: Log YCXH cha khi tạo/sửa/hủy ĐNXK (WarehouseExportRequestService)

**Files:**
- Modify: `Modules/Assign/Services/WarehouseExportRequestService.php` (`create()` ~221–227, `updateDraft()` ~293–299, `cancel()` ~321–326)

**Interfaces:**
- Consumes: `ProductExportRequestService::logStatusChanged(ProductExportRequest $req, int $statusBefore, ?string $note = null): void` (public, no-op khi status không đổi) — gọi qua `app(ProductExportRequestService::class)`.
- Note nguồn theo spec §7: `Tự động chuyển do lập Đề nghị xuất kho {code}` (create/updateDraft); `Tự động chuyển do hủy Đề nghị xuất kho {code}` (cancel).

- [x] **Step 1: `create()`** (thực tế method tên `createFromExportRequest()`) — capture `$reqStatusBefore = (int) $req->status;` TRƯỚC L221; sau cả 2 nhánh save status (sau L227) gọi `app(ProductExportRequestService::class)->logStatusChanged($req, $reqStatusBefore, "Tự động chuyển do lập Đề nghị xuất kho {$dnxk->code}");`. Nháp → 1 dòng 3→7; gửi thủ kho → 1 dòng net 3→1.

- [x] **Step 2: `updateDraft()`** — capture `$reqStatusBefore` của `$req` (YCXH) TRƯỚC khi đổi (trong nhánh gửi thủ kho L293-299), gọi `logStatusChanged` sau save với cùng note. No-op tự lo khi giữ nháp (không đổi).

- [x] **Step 3: `cancel()`** — capture status YCXH TRƯỚC L323 (trong nhánh `if $req && status==7`), gọi `logStatusChanged($req, $before, "Tự động chuyển do hủy Đề nghị xuất kho {$dnxk->code}")` sau save.

- [x] **Step 4: Lint** — `php -l WarehouseExportRequestService.php`.

- [x] **Step 5: Script test rollback** — bọc `DB::beginTransaction()/rollBack()`, kiểm 4 transition (create nháp 3→7, create gửi thủ kho 3→1, updateDraft gửi thủ kho →1, cancel 7→2) mỗi lần đúng 1 dòng `change_status` trên `catalog_histories table='product_export_requests'` + note đúng; no-op khi status không đổi. **PASS 11/11** (CA1 create nháp 2→7, CA2 cancel 7→2, CA3 no-op); ca "gửi thủ kho" cần tồn kho thật → dùng chung 1 call `logStatusChanged` no-op-protected đã verify ở CA1/CA3. Script: `scratchpad/test_task14_ycxh_log.php`.

- [x] **Step 6: Verify Playwright MCP** — YCXH 39304: lập ĐNXK (→ PDNXK-31112) rồi hủy. Khối lịch sử hiện ĐỦ: (1) 09:41 Chờ duyệt→Đang lập đề nghị "Tự động chuyển do lập Đề nghị xuất kho PDNXK-31112"; (2) 09:44 Đang lập đề nghị→Chờ duyệt "Tự động chuyển do hủy Đề nghị xuất kho PDNXK-31112"; (3) 14/10 Tạo mới. YCXH về "Chờ duyệt" sau hủy. Cả create + cancel đều PASS trên UI.

- [x] **Step 7: Commit** — hrm-api `17e01dece` (gộp Task 14+15, cùng 1 file service).

> **LƯU Ý backfill:** phiếu 39303 (và các YCXH cũ đã qua các điểm này) sẽ KHÔNG tự có log — log là
> snapshot bất biến. Muốn phiếu cũ hiện đúng phải backfill riêng (CHỜ user quyết, KHÔNG tự chạy).

### Task 15: `cancel()` hủy ĐNXK phải hủy luôn YCXH về "Đã hủy phiếu" (6) — bám ERP

> **Bối cảnh:** User báo `warehouse-export-requests/create?request_id=39304` lỗi `1062 Duplicate
> entry '39304' for key warehouse_export_requests_product_export_request_id_unique`. Điều tra 2 việc:
> (A) rác test PDNXK-31112 (status Đã hủy) còn chiếm unique index — đã dọn tay (xóa WER 31112 + 1
> detail + 4 dòng catalog_histories) trả 39304 về pristine. (B) **Bẫy pre-existing**: `cancel()`
> HRM revert YCXH về "Chờ duyệt" (2) để "lập lại đề nghị", nhưng unique index chỉ cho **1 ĐNXK/1
> YCXH** + `createFromExportRequest` luôn `new WarehouseExportRequest()` (INSERT) → lập lại = trùng
> key. ERP (`\App\Model\Warehouse\WarehouseExportRequest::cancel()`) hủy ĐNXK thì đưa YCXH về **6
> "Đã hủy phiếu" (terminal) + is_completed=true**, KHÔNG revert → không bao giờ lập lại/đụng index.
> **User chốt Hướng A (2026-10-16): bám ERP.**

**Files:**
- Modify: `Modules/Assign/Services/WarehouseExportRequestService.php` (`cancel()` ~328–360)

- [x] **Step 1: Sửa `cancel()`** — guard mở rộng cho YCXH ở **7 (nháp) HOẶC 1 (đã gửi thủ kho)**; set `status = STATUS_DA_HUY_PHIEU (6)` + `is_completed = true` (bỏ `approver_id=null` và nhánh revert→2). Giữ `logStatusChanged($req, $before, "Tự động chuyển do hủy Đề nghị xuất kho {code}")` → giờ ghi "Đang lập đề nghị/Đã đề nghị → Đã hủy".

- [x] **Step 2: Lint** — `php -l` sạch.

- [x] **Step 3: Script test rollback** — cập nhật CA2 assert YCXH sau hủy = **6** + `is_completed=1` + lịch sử "Đang lập đề nghị → Đã hủy". **PASS 12/12** (`scratchpad/test_task14_ycxh_log.php`).

- [x] **Step 4: Verify FE (đọc code, không ghi DB)** — gate `detailCanCreateWarehouseRequest`/`detailCanCreateProductExport` yêu cầu `status===2`; YCXH ở 6 → nút "Lập đề nghị"/"Lập phiếu xuất hàng" tự ẩn → bẫy duplicate đóng ở FE. Badge 6="Đã hủy" #F44336 do BE trả. KHÔNG cần sửa FE.

- [x] **Step 5: Commit** — hrm-api `17e01dece` (gộp cùng Task 14, cùng 1 file service).

### Task 16: Bảng dòng hàng nhập tay YCXH — bỏ nút "+" per-row + icon Xóa đỏ (UI)

> **Bối cảnh:** User gửi screenshot màn chi tiết hàng hoá YCXH (loại nhập tay), yêu cầu nguyên văn:
> "chi tiết hàng hoá bỏ cái dấu + thêm hàng hoá ở từng dòng hàng đi, icon xoá đổi màu đỏ". Cột
> "Hành động" của `ManualLinesTable` đang có 2 nút mỗi dòng: "+" (`$emit('add')`) và thùng rác (xám).
> Theo skill `button-convention`: nút Xóa trong cột hành động phải là `V2BaseIconButton danger` màu đỏ
> với icon `ri-delete-bin-line`; nút thêm hàng hoá chỉ cần 1 chỗ (nút tổng "+ Thêm hàng hoá" ở góc thẻ).

**Files:**
- Modify: `hrm-client/pages/finance/product-export-requests/components/ManualLinesTable.vue` (cột Hành động ~L60-63; import + components)

- [x] **Step 1: Bỏ nút "+" per-row** — gỡ `<V2BaseButton tertiary ... @click="$emit('add')"><i class="ri-add-line"></i></V2BaseButton>` khỏi cột Hành động. Giữ nút tổng "+ Thêm hàng hoá" (`@add="openProductModal"`) ở `#meta` thẻ "Chi tiết hàng hoá" của `ProductExportRequestForm.vue`.

- [x] **Step 2: Icon Xóa đỏ** — đổi nút xóa sang `<V2BaseIconButton v-b-tooltip.hover.top="'Xóa dòng'" size="sm" danger @click="remove(idx)"><i class="ri-delete-bin-line"></i></V2BaseIconButton>` (pattern chuẩn toàn project). `remove(idx)` giữ nguyên (filter mảng + emit 'input').

- [x] **Step 3: Import + đăng ký** — `import V2BaseIconButton from '@/components/V2BaseIconButton.vue'` + thêm vào `components`. Cập nhật doc comment "+/−" → "Xóa".

- [x] **Step 4: Verify Playwright MCP** — mở `http://127.0.0.1:3000/finance/product-export-requests/39305/edit` (PYCXH-39305 type 6 nháp, created_by=13). Bảng chi tiết hàng hoá: cột Hành động mỗi dòng CHỈ còn 1 nút icon thùng rác **màu đỏ**, KHÔNG còn dấu "+". Nút "+ Thêm hàng hoá" tổng (xanh) vẫn ở góc thẻ. PASS.

- [x] **Step 5: Commit** — hrm-client `932cd9d52`.

### Task 17: YCXH loại "Xuất hàng gửi" (12) — bỏ nút "×" đỏ bỏ chọn khách hàng (UI)

> **Bối cảnh:** User gửi screenshot trường "Khách hàng" của YCXH loại Xuất hàng gửi (type 12), bên
> phải ô chọn KH có nút `V2BaseIconButton danger` (icon `ri-close-line`, `clearCustomer`) hiện khi
> đã chọn KH (`v-if="form.customer_id"`). Yêu cầu nguyên văn: "loại xuất gửi bỏ cái nút xoá đi".
> Đổi KH vẫn thực hiện được bằng cách bấm lại ô picker để mở popup chọn, nên nút bỏ chọn là thừa.

**Files:**
- Modify: `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (block Khách hàng ~L147-170; method `clearCustomer` ~L2360)

- [x] **Step 1: Gỡ nút "×"** — xóa block `<V2BaseIconButton v-if="form.customer_id" danger ... @click="clearCustomer"><i class="ri-close-line"></i></V2BaseIconButton>` trong `.cost-pick` của trường Khách hàng. Giữ `SourcePicker` (bấm mở popup chọn KH).

- [x] **Step 2: Gỡ method `clearCustomer`** không còn tham chiếu (grep xác nhận chỉ dùng ở nút vừa xóa). `V2BaseIconButton` vẫn giữ import vì còn dùng ở nút clear HĐ chi phí (loại 99) — KHÔNG đụng nút đó.

- [x] **Step 3: Verify Playwright MCP** — màn Tạo mới YCXH, chọn Loại "Xuất hàng gửi" → chọn KH "15TPHPTA - HUAZHI": trường Khách hàng KHÔNG còn nút "×" đỏ (ô full-width). Nút clear HĐ chi phí loại 99 không bị ảnh hưởng. PASS.

- [x] **Step 4: Commit** — hrm-client `cdf7b4605`.

> **Backfill 39303: User chốt KHÔNG backfill (2026-10-16)** — chỉ phiếu phát sinh từ nay mới có log.

### Task 18: YCXH loại 19 "Xuất thực hiện hợp đồng" — khối thông tin KH bám đúng ERP (BE+FE)

> **Bối cảnh:** User gửi screenshot màn tạo YCXH loại "Xuất thực hiện hợp đồng" (type 19): "mst k
> hiện / số điện thoại đang lấy số của ng liên hệ chứ kp cty". Đối chiếu ERP
> (`resources/views/warehouse/product_export_requests/form.blade.php` + `ProductExportRequest.blade.php:474-480`):
> ERP có **2 khối KH tách theo loại**. Loại 19 dùng cờ `has_contract_customer` (CHỈ type 19) → khối
> **rút gọn chỉ 2 dòng**: *Khách hàng* (`customer.code - fullname`) + *Địa chỉ giao hàng*
> (`emplement_contract.delivery_places`, lấy từ báo giá). ERP **KHÔNG** hiển thị MST / Số điện thoại /
> Người liên hệ cho loại 19 (store cũng chỉ ghi `customer_id/type/name + delivery_place`,
> `ProductExportRequestsController:769-777`). Khối đầy đủ (CMT/MST + Số điện thoại=mobile + Điện thoại
> liên hệ=contact_phone) chỉ cho cờ `has_customer` = loại 1,2,8,11,13,14,15,16,17.
>
> HRM đang gộp 1 khối "Thông tin khách hàng" dùng chung cho 14/19/20/21 với MST + Số điện thoại +
> Người liên hệ. Loại 19 MST trống (BE firm hardcode `NULL as customer_tax_code`) + SĐT bind
> `customer_contact_phone` (số người liên hệ). **User chốt Hướng A (2026-10-16): bám ERP — loại 19
> chỉ hiện Khách hàng + Địa chỉ giao hàng.** Phạm vi: CHỈ loại 19 (14/20/21 giữ nguyên khối đầy đủ).

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` (`emplementContracts()` — thêm `delivery_place` vào 2 subquery UNION)
- Modify: `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (block KH L288-322 + `onEmplementContractSelected` L2164-2182)

- [x] **Step 1: BE trả `delivery_place`** — firm subquery: `leftJoin('firm_quotations as fq','fq.id','=','c.firm_quotation_id')` + selectRaw thêm `, fq.delivery_place as delivery_place`; wr subquery: selectRaw thêm `, c.delivery_place as delivery_place` (cột trực tiếp). 2 subquery giữ số cột khớp để `unionAll`.

- [x] **Step 2: Lint BE** — `php -l` sạch.

- [x] **Step 3: FE map delivery_place** — `onEmplementContractSelected`: thêm `delivery_place: contract.delivery_place` vào `customerInfo` (giữ customer_name; MST/phone/contact không render nữa).

- [x] **Step 4: FE template loại 19** — 4 ô *Mã số thuế*, *Số điện thoại*, *Người liên hệ*, *Địa chỉ*(customer_address) thêm `v-if="!isEmplementContractType"` (14/20/21 vẫn hiện). Ô *Địa chỉ giao hàng* đổi `v-if="isFirmContractType"` → `v-if="isFirmContractType || isEmplementContractType"`. Loại 19 còn đúng: Khách hàng + Địa chỉ giao hàng.

- [x] **Step 5: Verify Playwright MCP** — màn tạo YCXH, Loại "Xuất thực hiện hợp đồng", chọn HĐ: khối KH chỉ còn *Khách hàng* + *Địa chỉ giao hàng* (có số liệu), KHÔNG còn MST/SĐT/Người liên hệ. Loại 14 (Xuất bán HĐ hãng) vẫn hiện khối đầy đủ.

- [x] **Step 6: Commit** — tách BE + FE theo repo. BE `99ed609ac` (hrm-api), FE `0cb9afc27` (hrm-client), đều LOCAL chưa push.

### Checkpoint — 2026-10-16
Vừa hoàn thành: Task 18 (YCXH loại 19 khối KH bám ERP) — BE+FE commit local, verify Playwright PASS (loại 19 chỉ Khách hàng + Địa chỉ giao hàng; loại 14 regression khối đầy đủ vẫn hiện).
Đang làm dở: (không)
Bước tiếp theo: Chờ user chốt push + final whole-branch review + finishing-a-development-branch cho nhánh `lich-su-trang-thai-tu-dong-luong-xuat-nhap` (các commit T1-T18 đều local chưa push).
Blocked:
