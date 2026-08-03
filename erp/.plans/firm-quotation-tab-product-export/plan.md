# Xuất Excel danh sách hàng hóa từ báo giá đã duyệt — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development hoặc superpowers:executing-plans để thực thi. Steps dùng checkbox (`- [ ]`).

**Goal:** Xuất 1 file Excel gộp danh sách hàng hóa (theo mã hàng) từ các báo giá `firm-quotations` đã duyệt của Tân Phát, lấy từ `firm_quotation_tab_products`.

**Architecture:** Ad-hoc qua tinker — 1 method trong `database/seeds/UpdateDB.php` query + gộp dữ liệu, 1 class `app/ExcelExports/FirmQuotationProductListExcel.php` (maatwebsite FromArray) xuất file ra `storage/app/exports/`.

**Tech Stack:** Laravel 6 / PHP 7.4, Eloquent query builder, maatwebsite/excel ^3.1.

**Design:** `.plans/firm-quotation-tab-product-export/design.md`

> **Lưu ý dự án:** KHÔNG commit/push git khi chưa được yêu cầu. Đây là báo cáo đọc dữ liệu (SELECT) + ghi file — không sửa DB. Tinker local trỏ DB production `erp_new`.

> **Lưu ý không dùng TDD tự động:** Dự án không có test-suite cho luồng tinker/Excel; "test" = chạy method + đối chiếu số liệu thủ công (Task 3).

---

### Task 1: Tạo class Excel export

**Files:**
- Create: `app/ExcelExports/FirmQuotationProductListExcel.php`

- [ ] **Step 1: Tạo file class**

```php
<?php

namespace App\ExcelExports;

use Maatwebsite\Excel\Concerns\FromArray;
use Maatwebsite\Excel\Concerns\WithHeadings;
use Maatwebsite\Excel\Concerns\ShouldAutoSize;

class FirmQuotationProductListExcel implements FromArray, WithHeadings, ShouldAutoSize
{
    /** @var array */
    protected $data;

    public function __construct(array $data)
    {
        $this->data = $data;
    }

    public function array(): array
    {
        return $this->data;
    }

    public function headings(): array
    {
        return ['Mã hàng', 'Tên hàng', 'Model', 'ĐVT', 'SL'];
    }
}
```

- [ ] **Step 2: Kiểm cú pháp**

Run: `php -l app/ExcelExports/FirmQuotationProductListExcel.php`
Expected: `No syntax errors detected`
(Nếu php local lỗi `libaspell` → bỏ qua, intelephense/IDE không báo lỗi là được.)

---

### Task 2: Thêm method export vào UpdateDB

**Files:**
- Modify: `database/seeds/UpdateDB.php` — thêm 1 method `exportQuotationProductsList()` vào trong class `UpdateDB` (đặt cuối class, trước dấu `}` đóng class). `FirmQuotation` đã được import sẵn (dòng 85).

- [ ] **Step 1: Thêm method**

```php
    /**
     * Xuất Excel danh sách hàng hóa (gộp theo mã hàng) từ báo giá đã duyệt.
     * Nguồn: firm_quotation_tab_products. Lọc: company_id=1, status=Đã duyệt,
     * type IN (báo giá hãng, dự án), created_at >= 1/3/2026.
     * Chạy: (new \UpdateDB)->exportQuotationProductsList()
     */
    public function exportQuotationProductsList()
    {
        $rows = \App\Model\Sale\Firm\Quotation\FirmQuotationTabProduct::query()
            ->from('firm_quotation_tab_products as tp')
            ->join('firm_quotations as q', 'q.id', '=', 'tp.firm_quotation_id')
            ->where('q.company_id', 1)
            ->where('q.status', FirmQuotation::DA_DUYET)
            ->whereIn('q.type', [FirmQuotation::BG_HANG, FirmQuotation::BG_DU_AN])
            ->where('q.created_at', '>=', '2026-03-01 00:00:00')
            ->selectRaw('tp.code,
                MAX(tp.product_name) as product_name,
                MAX(tp.model_name) as model_name,
                MAX(tp.unit_name) as unit_name,
                SUM(tp.quantity) as qty')
            ->groupBy('tp.code')
            ->orderBy('tp.code')
            ->get();

        $data = [];
        foreach ($rows as $r) {
            $data[] = [
                $r->code,
                $r->product_name,
                $r->model_name,
                $r->unit_name,
                (float) $r->qty,
            ];
        }

        $relativePath = 'exports/firm_quotation_products_' . date('Ymd_His') . '.xlsx';

        \Maatwebsite\Excel\Facades\Excel::store(
            new \App\ExcelExports\FirmQuotationProductListExcel($data),
            $relativePath,
            'local'
        );

        $fullPath = storage_path('app/' . $relativePath);
        echo 'Đã xuất ' . count($data) . ' mã hàng → ' . $fullPath . PHP_EOL;

        return $fullPath;
    }
```

- [ ] **Step 2: Kiểm cú pháp**

Run: `php -l database/seeds/UpdateDB.php`
Expected: `No syntax errors detected`

---

### Task 3: Chạy thử + đối chiếu số liệu

- [ ] **Step 1: Chạy method qua tinker**

```bash
php artisan tinker
>>> (new \UpdateDB)->exportQuotationProductsList()
```
Expected: in ra `Đã xuất <N> mã hàng → /.../storage/app/exports/firm_quotation_products_<timestamp>.xlsx`
(Nếu tinker báo không tìm thấy class, thử `(new UpdateDB)->exportQuotationProductsList()`.)

- [ ] **Step 2: Đối chiếu nhanh tổng số mã hàng**

```bash
php artisan tinker
>>> DB::table('firm_quotation_tab_products as tp')->join('firm_quotations as q','q.id','=','tp.firm_quotation_id')->where('q.company_id',1)->where('q.status',2)->whereIn('q.type',[1,2])->where('q.created_at','>=','2026-03-01 00:00:00')->distinct()->count('tp.code')
```
Expected: số này khớp số dòng (N) trong file Excel.

- [ ] **Step 3: Mở file Excel kiểm cột + dữ liệu**

Mở `storage/app/exports/firm_quotation_products_<timestamp>.xlsx`:
- 5 cột: Mã hàng | Tên hàng | Model | ĐVT | SL
- Mỗi mã hàng 1 dòng, sắp xếp mã A→Z, SL = tổng cộng dồn.
- Chọn 1-2 mã, cộng tay quantity trên các báo giá thỏa lọc → khớp cột SL.

---

### Bổ sung (2026-06-17): tải qua web URL
- [x] Tách query ra `FirmQuotationProductListExcel::fetchData()` (dùng chung tinker + web), thêm `Exportable` trait.
- [x] `UpdateDB::exportQuotationProductsList()` rút gọn dùng `fetchData()` + `->store()`.
- [x] `FirmQuotationController@exportProductList` → `->download('danh_sach_hang_hoa_bao_gia.xlsx')`.
- [x] Route `GET /admin/sale/firm-quotations/exportProductList` (name `firmQuotation.exportProductList`), đặt trước `/{id}/show`, chưa gắn checkPermission.
- URL: `https://erp.eteksofts.com/admin/sale/firm-quotations/exportProductList`
- [ ] User mở URL trên prod → tải file, đối chiếu số liệu.

### Checkpoint — 2026-06-17
Vừa hoàn thành: Task 1 (class `FirmQuotationProductListExcel`) + Task 2 (method `exportQuotationProductsList()` trong `UpdateDB.php`) — code DONE, spec+quality review PASS. CHƯA commit (chờ user yêu cầu).
Đang làm dở: (không)
Bước tiếp theo: Task 3 — user chạy `(new \UpdateDB)->exportQuotationProductsList()` qua tinker **trên server** (php local lỗi libaspell), đối chiếu số mã hàng + mở file Excel.
Blocked: bước chạy thử cần môi trường php hoạt động + DB.

## Self-review (đã rà soát theo spec)
- ✔ Bộ lọc khớp design: company_id=1, status DA_DUYET, type [BG_HANG, BG_DU_AN], created_at ≥ 2026-03-01.
- ✔ Nguồn chỉ `firm_quotation_tab_products`.
- ✔ Gộp theo `code`, SUM(quantity), 5 cột đúng thứ tự, sort code ASC.
- ✔ Output xlsx ra `storage/app/exports/`, in path.
- ✔ Không placeholder; code đầy đủ; tên class/method nhất quán giữa Task 1–3.
- ⚠ MySQL strict `only_full_group_by`: đã dùng `MAX()` cho các cột mô tả nên không lỗi.
