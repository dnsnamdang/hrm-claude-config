# HRM link Mã phiếu duyệt hàng tạm → ERP — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sau khi gửi duyệt hàng tạm sang ERP, banner tab Báo giá hiển thị Mã phiếu yêu cầu duyệt hàng tạm dạng link mở chi tiết phiếu bên ERP.

**Architecture:** HRM lưu `request_id`/`request_code` (ERP trả về) trên `quotations`; `buildTmpSyncSummary` trả thêm `request_code` + `request_url` (full ERP URL, dùng `config('app.erp_url')`); Vue banner render link.

**Tech Stack:** PHP 7.4/Laravel 8 (nwidart modules) — hrm-api; Nuxt 2/Vue 2 — hrm-client.

## Global Constraints

- KHÔNG commit/push khi user chưa yêu cầu.
- KHÔNG đọc/sửa `vendor/`, `node_modules/`.
- Branch: `sync_quotation` (cả hrm-api + hrm-client — đang ở nhánh này).
- `.env` HRM DB = `dev_hrm_2` (local dev) — migrate an toàn. Xác nhận lại `grep DB_DATABASE .env` trước migrate.
- Bảng: `quotations` (Module Assign). ERP base URL: `config('app.erp_url', env('ERP_URL'))`.
- URL ERP: `{erpBase}/admin/sale/tmp_product_requests/{request_id}/show`.
- ERP đã trả sẵn `request_id`+`request_code` trong response `sync-from-hrm` — KHÔNG sửa ERP.

---

## File Structure
- **Create** `hrm-api/Modules/Assign/Database/Migrations/2026_07_01_000001_add_erp_tmp_product_request_to_quotations_table.php`
- **Modify** `hrm-api/Modules/Assign/Services/TmpProductSyncService.php` (`sendApproval` lưu id/code)
- **Modify** `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` (`buildTmpSyncSummary` trả thêm field)
- **Modify** `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue` (banner link)

---

### Task 1: Migration thêm 2 cột vào `quotations`

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_07_01_000001_add_erp_tmp_product_request_to_quotations_table.php`

- [x] **Step 1: Tạo migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddErpTmpProductRequestToQuotationsTable extends Migration
{
    public function up()
    {
        Schema::table('quotations', function (Blueprint $table) {
            $table->unsignedBigInteger('erp_tmp_product_request_id')->nullable();
            $table->string('erp_tmp_product_request_code')->nullable();
        });
    }

    public function down()
    {
        Schema::table('quotations', function (Blueprint $table) {
            $table->dropColumn(['erp_tmp_product_request_id', 'erp_tmp_product_request_code']);
        });
    }
}
```

- [x] **Step 2: Xác nhận DB local rồi migrate** (dev_hrm_2, migrated 349ms)

Run: `cd hrm-api && grep DB_DATABASE .env` → phải là `dev_hrm_2` (không phải prod).
Run: `php artisan module:migrate Assign`
Expected: migrate thành công; `SHOW COLUMNS FROM quotations LIKE 'erp_tmp_product_request%';` thấy 2 cột.

- [ ] **Step 3: Commit** (chỉ khi user yêu cầu)

```bash
git add Modules/Assign/Database/Migrations/2026_07_01_000001_add_erp_tmp_product_request_to_quotations_table.php
git commit -m "feat(assign): thêm cột erp_tmp_product_request_id/code vào quotations"
```

---

### Task 2: BE — lưu id/code + trả link trong banner

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/TmpProductSyncService.php` (~dòng 56-75)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` (`buildTmpSyncSummary`, ~dòng 436-443)

**Interfaces:**
- `$result` từ ERP có keys: `map`, `request_id`, `request_code`.
- Banner array tiêu thụ bởi FE qua `res.tmp_sync` → thêm `request_code`, `request_url`.

- [x] **Step 1: `sendApproval` lưu request_id/code**

Trong `TmpProductSyncService::sendApproval()`, thay đoạn (dòng 65-75):

```php
        DB::transaction(function () use ($map, $quotation, $tempLines) {
            foreach ($map as $m) {
                $line = $tempLines->firstWhere('id', $m['hrm_line_id']);
                if ($line) {
                    $line->erp_tmp_product_id = $m['tmp_product_id'];
                    $line->save();
                }
            }
            $quotation->tmp_sync_status = 'syncing';
            $quotation->save();
        });
```

bằng:

```php
        $requestId = $result['request_id'] ?? null;
        $requestCode = $result['request_code'] ?? null;

        DB::transaction(function () use ($map, $quotation, $tempLines, $requestId, $requestCode) {
            foreach ($map as $m) {
                $line = $tempLines->firstWhere('id', $m['hrm_line_id']);
                if ($line) {
                    $line->erp_tmp_product_id = $m['tmp_product_id'];
                    $line->save();
                }
            }
            $quotation->tmp_sync_status = 'syncing';
            $quotation->erp_tmp_product_request_id = $requestId;
            $quotation->erp_tmp_product_request_code = $requestCode;
            $quotation->save();
        });
```

- [x] **Step 2: `buildTmpSyncSummary` trả thêm request_code + request_url**

Trong `QuotationController::buildTmpSyncSummary()`, thay đoạn return (dòng 436-443):

```php
        return [
            'quotation_id' => $won->id,
            'quotation_code' => $won->code,
            'status' => $won->tmp_sync_status, // null | syncing | synced
            'unsent' => $unsent,
            'sent_total' => $sentTotal,
            'approved' => $approved,
        ];
```

bằng:

```php
        $erpBase = rtrim(config('app.erp_url', env('ERP_URL', '')), '/');

        return [
            'quotation_id' => $won->id,
            'quotation_code' => $won->code,
            'status' => $won->tmp_sync_status, // null | syncing | synced
            'unsent' => $unsent,
            'sent_total' => $sentTotal,
            'approved' => $approved,
            'request_id' => $won->erp_tmp_product_request_id,
            'request_code' => $won->erp_tmp_product_request_code,
            'request_url' => $won->erp_tmp_product_request_id
                ? $erpBase . '/admin/sale/tmp_product_requests/' . $won->erp_tmp_product_request_id . '/show'
                : null,
        ];
```

- [x] **Step 3: Lint**

Run: `cd hrm-api && php -l Modules/Assign/Services/TmpProductSyncService.php && php -l Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`
Expected: `No syntax errors detected` cả 2.

- [ ] **Step 4: Commit** (chỉ khi user yêu cầu)

```bash
git add Modules/Assign/Services/TmpProductSyncService.php Modules/Assign/Http/Controllers/Api/V1/QuotationController.php
git commit -m "feat(assign): lưu + trả link phiếu duyệt hàng tạm ERP trong banner"
```

---

### Task 3: FE — hiển thị link Mã phiếu trong banner

**Files:**
- Modify: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue` (banner, sau dòng 16)

**Interfaces:**
- Consumes: `tmpSync.request_code`, `tmpSync.request_url` (Task 2).

- [x] **Step 1: Thêm dòng link vào banner**

Sau khối badge/progress (dòng 11-16, đóng bằng `</div>` ở dòng 16), thêm ngay trước `</div>` đóng `.tmp-sync-info` (dòng 17):

```html
                    <div v-if="tmpSync.request_code" class="mt-1 small">
                        Mã phiếu:
                        <a :href="tmpSync.request_url" target="_blank" rel="noopener">{{ tmpSync.request_code }}</a>
                    </div>
```

- [ ] **Step 2: Kiểm thử thủ công (dev)**

Trên dev: mở dự án trúng thầu có báo giá hàng tạm → bấm "Gửi duyệt hàng tạm" → banner hiển thị "Mã phiếu: <code>" là link; click mở tab ERP đúng trang `/admin/sale/tmp_product_requests/{id}/show`. Reload trang → link vẫn còn (đọc từ DB).

- [ ] **Step 3: Commit** (chỉ khi user yêu cầu)

```bash
git add pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue
git commit -m "feat(assign): hiển thị link phiếu duyệt hàng tạm ERP trên banner"
```

---

## Self-Review

1. **Spec coverage:**
   - DB 2 cột → Task 1. ✅
   - sendApproval lưu id/code → Task 2 Step 1. ✅
   - buildTmpSyncSummary trả request_code + request_url (config app.erp_url + path show) → Task 2 Step 2. ✅
   - FE banner link → Task 3. ✅
   - Edge ERP không trả request_id → `?? null` (BE) + `v-if` (FE) → không lỗi, không hiện link. ✅
2. **Placeholder scan:** không TBD/TODO; mọi step có code + lệnh + expected. ✅
3. **Type consistency:** field `request_code`/`request_url`/`request_id` nhất quán giữa Task 2 (BE trả) và Task 3 (FE dùng). ✅
