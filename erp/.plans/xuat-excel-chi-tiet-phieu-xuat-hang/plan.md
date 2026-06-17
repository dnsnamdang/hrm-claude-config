# Xuất excel chi tiết Phiếu xuất hàng (HĐH) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development hoặc superpowers:executing-plans để chạy plan theo từng task. Các bước dùng checkbox `- [ ]`.

**Goal:** Thêm chức năng xuất Excel chi tiết 1 phiếu xuất hàng loại Xuất bán HĐ hàng hóa (type=14), đúng layout file mẫu, hỗ trợ 2 ca: không xuất thẳng / xuất thẳng.

**Architecture:** Bám pattern `exportList` sẵn có (maatwebsite/excel `FromView` + blade). Controller dùng lại `ProductExport::getDataForShow($id)` để nạp data, build mảng `$data`, đẩy vào 1 Excel class render 1 blade (rẽ nhánh `is_export_direct`). Nút đặt ở màn list (dropdown action) + màn show.

**Tech Stack:** PHP 7.4, Laravel 8, maatwebsite/excel (FromView), Blade.

> **Lưu ý lệch khỏi default skill:** dự án KHÔNG có test tự động cho Excel export và CLAUDE.md cấm commit git → các task dùng **bước verify thủ công** thay cho test tự động, và **không có bước git commit** (chỉ đánh dấu `[x]` trong plan này). Đây là chủ ý theo ràng buộc dự án.

---

## File Structure
| File | Trách nhiệm |
| ---- | ----------- |
| `routes/web.php` (nhóm product_exports ~1292-1307) | Khai báo route `productExport.exportDetail` |
| `app/Http/Controllers/Warehouse/ProductExportsController.php` | method `exportDetail($id)`: nạp data, chặn type, build `$data`, download |
| `app/ExcelExports/ProductExportDetailExcel.php` (mới) | Excel class FromView (copy mẫu `ProductExportExcel`) |
| `resources/views/reports/exports/product_export_detail_export.blade.php` (mới) | Layout Excel; rẽ nhánh `is_export_direct` |
| `app/Http/Controllers/Warehouse/ProductExportsController.php` (searchData ~172-187) | Thêm link action ở màn list (chỉ type=14) |
| `resources/views/warehouse/product_exports/show.blade.php` | Thêm nút download ở màn chi tiết (chỉ type=14) |

Hằng số: `ProductExport::XUAT_BAN_HD_HANG = 14`. Tên file tải: `PXH_{code}.xlsx`.

---

## Task 1: Route

**Files:** Modify `routes/web.php` (trong nhóm `Route::group(['prefix' => 'product_exports'], ...)`, cạnh route `print`).

- [ ] **Step 1:** Thêm route (đặt ngay dưới dòng route `{id}/print`):

```php
Route::get('/{id}/exportDetail', 'ProductExportsController@exportDetail')->name('productExport.exportDetail');
```

- [ ] **Step 2: Verify** chạy `php artisan route:list --name=productExport.exportDetail` (hoặc mở trình duyệt URL `admin/warehouse/product_exports/{id}/exportDetail`) → route tồn tại, trỏ `ProductExportsController@exportDetail`.

---

## Task 2: Excel class

**Files:** Create `app/ExcelExports/ProductExportDetailExcel.php`.

- [ ] **Step 1:** Tạo file (copy đúng pattern `ProductExportExcel`, chỉ đổi tên view):

```php
<?php

namespace App\ExcelExports;

use Illuminate\Contracts\View\View;
use Maatwebsite\Excel\Concerns\FromView;
use Maatwebsite\Excel\Concerns\Exportable;
use Maatwebsite\Excel\Concerns\WithEvents;

class ProductExportDetailExcel implements FromView, WithEvents
{
    use Exportable;

    public $data;

    public function forData($data)
    {
        $this->data = $data;
        return $this;
    }

    public function view(): View
    {
        $data = $this->data;
        return view('reports.exports.product_export_detail_export', compact('data'));
    }

    public function registerEvents(): array
    {
        return [];
    }
}
```

- [ ] **Step 2: Verify** `php -l app/ExcelExports/ProductExportDetailExcel.php` → No syntax errors.

---

## Task 3: Controller method `exportDetail`

**Files:** Modify `app/Http/Controllers/Warehouse/ProductExportsController.php` (thêm method mới, ví dụ ngay sau `exportList`). Ở đầu file đã có `use App\Model\Warehouse\ProductExport` (alias `ThisModel`) và `ExportModel`.

Method nạp data qua `ProductExport::getDataForShow($id)` (đã eager-load: `products.product.model`, `products.acc_warehouses`, `warehouse_export.{warehouse,employee_create,customer,receiver,trips}`, `product_export_request.employee_create`, `firm_contract`, `customer`, `arrange_delivery`, `executors`), build mảng tính sẵn để blade không phải tính.

- [ ] **Step 1:** Thêm method:

```php
public function exportDetail($id)
{
    $object = \App\Model\Warehouse\ProductExport::getDataForShow($id);

    if ($object->type != ExportModel::XUAT_BAN_HD_HANG) {
        abort(404);
    }

    // Bảng kho kế toán: map id => code để hiển thị "Kho kế toán"
    $accWarehouseIds = [];
    foreach ($object->products as $p) {
        foreach ($p->acc_warehouses as $acc) {
            if ($acc->accounting_warehouse_id) $accWarehouseIds[] = $acc->accounting_warehouse_id;
        }
    }
    $accWarehouseMap = \App\Model\Warehouse\AccountingWarehouse::whereIn('id', array_unique($accWarehouseIds))
        ->pluck('code', 'id')->toArray();

    // Hàng hóa: tính sẵn các cột tiền theo công thức (mirror màn show)
    $products = [];
    $sumExportPrice = 0;
    foreach ($object->products as $p) {
        $donGiaBan        = $p->price + $p->extra_price;
        $thanhTienBan     = $donGiaBan * $p->qty;
        $thanhTienSauGiam = $p->allocated_price * $p->qty;
        $soTienVat        = $thanhTienSauGiam * $p->vat_percent / 100;
        $thanhTienSauVat  = $thanhTienSauGiam + $soTienVat;
        $donGiaVon        = $p->export_price * $p->unit_coefficient;
        $thanhTienVon     = $p->export_price * $p->qty * $p->unit_coefficient;
        $sumExportPrice  += $thanhTienVon;

        $accRows = [];
        foreach ($p->acc_warehouses as $acc) {
            $accRows[] = [
                'kho_ke_toan' => $accWarehouseMap[$acc->accounting_warehouse_id] ?? '',
                'sl_xuat'     => $acc->qty,
            ];
        }
        if (empty($accRows)) {
            $accRows[] = ['kho_ke_toan' => '', 'sl_xuat' => $p->qty];
        }

        $products[] = [
            'product_name'       => $p->product_name,
            'model_name'         => $p->model_name,
            'code'               => $p->code,
            'unit_name'          => $p->unit_name,
            'sl_thuc_xuat'       => $p->qty,
            'don_gia_von'        => $donGiaVon,
            'thanh_tien_von'     => $thanhTienVon,
            'gia_niem_yet'       => $p->price,
            'don_gia_ban'        => $donGiaBan,
            'thanh_tien_ban'     => $thanhTienBan,
            'don_gia_sau_giam'   => $p->allocated_price,
            'thanh_tien_sau_giam'=> $thanhTienSauGiam,
            'vat_percent'        => $p->vat_percent,
            'so_tien_vat'        => $soTienVat,
            'thanh_tien_sau_vat' => $thanhTienSauVat,
            'acc_rows'           => $accRows,
        ];
    }

    $company = $object->employee_create->info->company;
    $data = [
        'is_export_direct' => (bool) $object->is_export_direct,
        'object'           => $object,
        'company_name'     => $company->name,
        'company_address'  => $company->address,
        'company_logo'     => $company->logo,
        'products'         => $products,
        // tổng (mirror show)
        'tong_tien_ban'        => $object->sum_amount_after_extra,
        'tong_giam_gia'        => $object->sum_amount_after_extra - $object->sum_amount_allocated,
        'tong_tien_truoc_thue' => $object->sum_amount_allocated,
        'tien_vat'             => $object->sum_amount_allocated_after_vat - $object->sum_amount_allocated,
        'tong_tien_sau_thue'   => $object->sum_amount_allocated_after_vat,
        'tong_tien_von'        => $sumExportPrice,
    ];

    return (new \App\ExcelExports\ProductExportDetailExcel())
        ->forData($data)
        ->download('PXH_' . $object->code . '.xlsx');
}
```

- [ ] **Step 2:** Xác nhận class `AccountingWarehouse` đúng namespace. Chạy:
`grep -rn "class AccountingWarehouse" app/Model/Warehouse/`
Nếu namespace khác → sửa lại `use`/FQN trong Step 1 cho khớp. Expected: `app/Model/Warehouse/AccountingWarehouse.php`.

- [ ] **Step 3: Verify** `php -l` file controller → No syntax errors.

---

## Task 4: Blade layout (phần lõi)

**Files:** Create `resources/views/reports/exports/product_export_detail_export.blade.php`.

Yêu cầu chung: **không dùng `colspan`/`rowspan` ở dòng dữ liệu** (không merge). Mỗi trường thông tin = 1 `<td>` nhãn + 1 `<td>` giá trị. Dòng tiêu đề section = 1 `<td>` text. Bảng hàng hóa: cột chung chỉ ở dòng acc đầu, dòng acc sau để trống.

- [ ] **Step 1:** Tạo khung + header + Section 1 (Thông tin chung, rẽ 2 ca):

```blade
@php
    $o = $data['object'];
    $direct = $data['is_export_direct'];
    $we = $o->warehouse_export;       // null nếu xuất thẳng
    $per = $o->product_export_request; // dùng cho xuất thẳng
@endphp
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head>
<body>
<table>
    <tr><td>{{ $data['company_name'] }}</td></tr>
    <tr><td>{{ $data['company_address'] }}</td></tr>
    <tr><td></td></tr>
    <tr><td style="font-weight:bold;font-size:18px;">PHIẾU XUẤT HÀNG</td></tr>
    <tr><td>No: {{ $o->code }}</td></tr>
    <tr><td>Ngày lập: {{ \Carbon\Carbon::parse($o->created_at)->format('d/m/Y') }}</td></tr>
</table>

<table border="1">
    <tr><td><b>1. Thông tin chung</b></td></tr>
    <tr><td>Loại yêu cầu</td><td>Xuất bán hàng</td><td>Người lập</td><td>{{ optional($o->employee_create)->fullname }}</td></tr>
    <tr><td>Xuất thẳng</td><td>{{ $direct ? 'Có' : 'Không' }}</td><td>Ngày hạch toán</td><td>{{ $o->approved_time ? \Carbon\Carbon::parse($o->approved_time)->format('d/m/Y') : '' }}</td></tr>
    @if(!$direct)
    <tr><td>Phiếu xuất kho</td><td>{{ optional($we)->code }}</td><td>Người yêu cầu</td><td>{{ $o->export_requester ?? '' }}</td></tr>
    <tr><td>Kho xuất</td><td>{{ optional(optional($we)->warehouse)->name }}</td><td>Phòng yêu cầu</td><td>{{ $o->export_request_department ?? '' }}</td></tr>
    <tr><td>Hợp đồng</td><td>{{ optional($o->firm_contract)->code }}</td><td>Thủ kho</td><td>{{ optional(optional($we)->employee_create)->fullname }}</td></tr>
    <tr><td>Khách hàng</td><td>{{ optional($o->customer)->fullname }}</td><td>Người nhận hàng</td><td>{{ optional(optional($we)->receiver)->fullname }}</td></tr>
    <tr><td>Ghi chú</td><td>{{ $o->note }}</td><td></td><td></td></tr>
    @else
    <tr><td>Phiếu YCXH</td><td>{{ optional($per)->code }}</td><td>Người yêu cầu</td><td>{{ $o->export_requester ?? '' }}</td></tr>
    <tr><td>Hợp đồng</td><td>{{ optional($o->firm_contract)->code }}</td><td>Phòng yêu cầu</td><td>{{ $o->export_request_department ?? '' }}</td></tr>
    <tr><td>Khách hàng</td><td>{{ optional($o->customer)->fullname }}</td><td></td><td></td></tr>
    <tr><td>Ghi chú</td><td>{{ $o->note }}</td><td></td><td></td></tr>
    @endif
</table>
```

> Ghi chú: nếu trường "Vận chuyển / Công ty vận chuyển" (ca không xuất thẳng) cần hiển thị ở Section 1 đúng mẫu, lấy từ `$o->vehicle_company`/`$we->trips`. Xác nhận field khi làm Task 6 (vận chuyển).

- [ ] **Step 2: Verify** mở `admin/warehouse/product_exports/{id}/exportDetail` với 1 phiếu type=14 không xuất thẳng → tải được file .xlsx, Section 1 đúng nhãn/giá trị. Lặp với 1 phiếu xuất thẳng (nếu có) → đúng nhánh.

---

## Task 5: Blade — Section 4 Hàng hóa + Tổng + chữ ký

**Files:** Modify `resources/views/reports/exports/product_export_detail_export.blade.php` (thêm sau Section 1; Bốc xếp/Vận chuyển sẽ chèn ở Task 6/7 giữa Section 1 và phần này theo đúng thứ tự mẫu).

- [ ] **Step 1:** Thêm bảng hàng hóa + tổng + chữ ký:

```blade
<table border="1">
    <tr><td><b>Hàng hóa</b></td></tr>
    <tr>
        <td>STT</td><td>Hàng hóa</td><td>Model</td><td>Mã hàng hóa</td><td>Đơn vị tính</td>
        <td>SL thực xuất</td><td>Kho kế toán</td><td>SL xuất</td><td>Đơn giá vốn</td><td>Thành tiền vốn</td>
        <td>Giá niêm yết</td><td>Đơn giá bán</td><td>Thành tiền bán</td><td>Đơn giá Sau giảm</td><td>Thành tiền sau giảm</td>
        <td>% VAT</td><td>Số tiền VAT</td><td>Thành tiền sau VAT</td>
    </tr>
    @foreach($data['products'] as $i => $p)
        @foreach($p['acc_rows'] as $k => $acc)
        <tr>
            {{-- cột chung chỉ ở dòng acc đầu tiên, dòng sau để trống (không merge) --}}
            <td>{{ $k === 0 ? $i + 1 : '' }}</td>
            <td>{{ $k === 0 ? $p['product_name'] : '' }}</td>
            <td>{{ $k === 0 ? $p['model_name'] : '' }}</td>
            <td>{{ $k === 0 ? $p['code'] : '' }}</td>
            <td>{{ $k === 0 ? $p['unit_name'] : '' }}</td>
            <td>{{ $k === 0 ? number_format($p['sl_thuc_xuat']) : '' }}</td>
            <td>{{ $acc['kho_ke_toan'] }}</td>
            <td>{{ number_format($acc['sl_xuat']) }}</td>
            <td>{{ $k === 0 ? number_format($p['don_gia_von']) : '' }}</td>
            <td>{{ $k === 0 ? number_format($p['thanh_tien_von']) : '' }}</td>
            <td>{{ $k === 0 ? number_format($p['gia_niem_yet']) : '' }}</td>
            <td>{{ $k === 0 ? number_format($p['don_gia_ban']) : '' }}</td>
            <td>{{ $k === 0 ? number_format($p['thanh_tien_ban']) : '' }}</td>
            <td>{{ $k === 0 ? number_format($p['don_gia_sau_giam']) : '' }}</td>
            <td>{{ $k === 0 ? number_format($p['thanh_tien_sau_giam']) : '' }}</td>
            <td>{{ $k === 0 ? $p['vat_percent'] : '' }}</td>
            <td>{{ $k === 0 ? number_format($p['so_tien_vat']) : '' }}</td>
            <td>{{ $k === 0 ? number_format($p['thanh_tien_sau_vat']) : '' }}</td>
        </tr>
        @endforeach
    @endforeach
    <tr><td>Thành tiền bán</td><td>{{ number_format($data['tong_tien_ban']) }}</td></tr>
    <tr><td>Tổng giảm giá</td><td>{{ number_format($data['tong_giam_gia']) }}</td></tr>
    <tr><td>Tổng tiền trước thuế</td><td>{{ number_format($data['tong_tien_truoc_thue']) }}</td></tr>
    <tr><td>Tiền VAT</td><td>{{ number_format($data['tien_vat']) }}</td></tr>
    <tr><td>Tổng tiền sau thuế</td><td>{{ number_format($data['tong_tien_sau_thue']) }}</td></tr>
    <tr><td>Tổng tiền vốn</td><td>{{ number_format($data['tong_tien_von']) }}</td></tr>
</table>

<table>
    <tr><td>Người lập phiếu</td><td>Kế toán trưởng</td></tr>
    <tr><td>{{ optional($o->employee_create)->fullname }}</td><td></td></tr>
</table>
</body>
</html>
```

- [ ] **Step 2: Verify** xuất 1 phiếu type=14 có sản phẩm nhiều dòng kho kế toán (LN01/LN02) → đúng: cột chung ở dòng đầu, dòng phụ trống; SL xuất tách theo kho; 6 dòng tổng đúng số (đối chiếu màn `show` của chính phiếu đó).

---

## Task 6: Blade — Section 2 Bốc xếp (điều kiện)

**Files:** Modify blade (chèn giữa Section 1 và Hàng hóa). Dữ liệu: `$o->arrange_delivery` (hasOne, có thể null), `$o->executors` (type=2).
Field arrange_delivery (theo `$fillable`): `rent_type`, `rent_type_name`, `arrange_type`, `arrange_type_name`, `is_weight`, `weight`, `price`, `total_money`, `vat`, `supplier_id`, `account_name`, `cost_debt_name`, `work_name`.

- [ ] **Step 1:** Đọc tab "Bốc xếp" trong `resources/views/warehouse/product_exports/show.blade.php` (tìm `id="boc_xep"`) để xác nhận: cách hiển thị "Loại bốc xếp", tên NCC (`supplier`), và field số tiền executor. Ghi lại binding chính xác.

- [ ] **Step 2:** Thêm block (chỉ render khi có arrange_delivery), rẽ TH1 (thuê công ty) / TH2 (thuê ngoài) theo `rent_type`:

```blade
@if($o->arrange_delivery)
    @php $ad = $o->arrange_delivery; $soSauVat = $ad->total_money + $ad->vat; @endphp
    <table border="1">
        <tr><td><b>Bốc xếp</b></td></tr>
        <tr><td>Cách tính bốc xếp</td><td>{{ $ad->arrange_type_name }}</td></tr>
        <tr><td>Loại hình thuê</td><td>{{ $ad->rent_type_name }}</td></tr>
        <tr><td>{{ $ad->is_weight ? 'Khối lượng hàng' : 'Số giờ' }}</td><td>{{ $ad->weight }}</td></tr>
        <tr><td>Đơn giá bốc xếp</td><td>{{ number_format($ad->price) }}</td></tr>
        <tr><td>Số tiền</td><td>{{ number_format($ad->total_money) }}</td></tr>
        <tr><td>VAT</td><td>{{ number_format($ad->vat) }}</td></tr>
        <tr><td>Số tiền sau VAT</td><td>{{ number_format($soSauVat) }}</td></tr>
        @if($ad->rent_type == 2 || strpos(mb_strtolower($ad->rent_type_name), 'ngoài') !== false)
            {{-- TH2: thuê ngoài --}}
            <tr><td>Nhà cung cấp</td><td>{{ optional($o->arrange_delivery->supplier ?? null)->fullname }}</td></tr>
            <tr><td>Tài khoản nợ</td><td>{{ $ad->account_name }}</td></tr>
            <tr><td>Mã phí</td><td>{{ $ad->cost_debt_name }}</td></tr>
            <tr><td>Vụ việc</td><td>{{ $ad->work_name }}</td></tr>
        @else
            {{-- TH1: thuê công ty → bảng người nhận việc --}}
            <tr><td>STT</td><td>Nhân viên</td><td>Số tiền</td></tr>
            @foreach($o->executors as $idx => $ex)
            <tr><td>{{ $idx + 1 }}</td><td>{{ optional($ex->employee)->fullname }}</td><td>{{ number_format($ex->amount) }}</td></tr>
            @endforeach
        @endif
    </table>
@endif
```

- [ ] **Step 3:** Xác nhận quan hệ `supplier` trên `ProductImportExportArrangeDelivery` và field `employee`/`amount` trên `ProductImportExportArrangeDeliveryExecutor`. Nếu tên khác → sửa cho khớp (đối chiếu show tab boc_xep ở Step 1).
- [ ] **Step 4: Verify** phiếu có bốc xếp thuê công ty → hiện bảng người nhận việc; phiếu thuê ngoài → hiện NCC/TK nợ/mã phí/vụ việc; phiếu không có bốc xếp → không hiện section.

---

## Task 7: Blade — Section 3 Vận chuyển (chỉ không xuất thẳng + có cty vận chuyển)

**Files:** Modify blade (chèn sau Bốc xếp, trước Hàng hóa). Dữ liệu: `$we->trips` (đã eager-load trong getDataForShow) + field KM/phí ở cấp phiếu.

- [ ] **Step 1:** Đọc tab "Vận chuyển" trong `show.blade.php` (tìm `id="van_chuyen"`) để xác nhận chính xác: điều kiện "có công ty vận chuyển" (vd `$o->vehicle_company_id` / cờ `has_delivery`), tên field Số KM dự kiến / Số KM chốt / tổng NV chịu / tổng cty chịu / CP vận chuyển thực tế / thuế, và per-trip: tên chuyến xe + tiền NV chịu + tiền cty chịu. Ghi lại binding.

- [ ] **Step 2:** Thêm block điều kiện theo đúng field xác nhận ở Step 1 (khung mẫu — thay tên field cho khớp sau khi đọc show):

```blade
@if(!$direct && $o->vehicle_company_id)
    <table border="1">
        <tr><td><b>Vận chuyển</b></td></tr>
        <tr><td>Số KM dự kiến</td><td>{{ $o->km_estimate }}</td><td>Chi phí vận chuyển thực tế</td><td>{{ number_format($o->delivery_cost_real) }}</td></tr>
        <tr><td>Số KM chốt</td><td>{{ $o->km_final }}</td><td>Thuế</td><td>{{ number_format($o->delivery_tax) }}</td></tr>
        <tr><td>Nhân viên chịu phí</td><td>{{ number_format($o->employee_delivery_cost) }}</td><td>Công ty chịu phí</td><td>{{ number_format($o->company_delivery_cost) }}</td></tr>
        <tr><td>STT</td><td>Chuyến xe</td><td>Nhân viên chịu phí</td><td>Công ty chịu phí</td></tr>
        @foreach(optional($we)->trips ?? [] as $idx => $trip)
        <tr><td>{{ $idx + 1 }}</td><td>{{ optional($trip->trip)->name }}</td><td>{{ number_format($trip->employee_cost) }}</td><td>{{ number_format($trip->company_cost) }}</td></tr>
        @endforeach
    </table>
@endif
```

> Các field `km_estimate`, `delivery_cost_real`, `delivery_tax`, `employee_delivery_cost`, `company_delivery_cost`, `vehicle_company_id`, và per-trip `employee_cost`/`company_cost`/`trip->name` là **tên dự kiến** — BẮT BUỘC thay bằng tên thật lấy từ show tab van_chuyen (Step 1) trước khi hoàn tất.

- [ ] **Step 3: Verify** phiếu không xuất thẳng có công ty vận chuyển → hiện section + chi tiết chuyến xe đúng số (đối chiếu màn show); phiếu xuất thẳng → KHÔNG có section vận chuyển.

---

## Task 8: Nút ở màn list `all`

**Files:** Modify `app/Http/Controllers/Warehouse/ProductExportsController.php` method `searchData` (khối `addColumn('action', ...)` ~172-187).

- [ ] **Step 1:** Thêm link "Xuất excel chi tiết" ngay sau link "In phiếu" (line 181), chỉ khi type=14:

```php
if ($object->type == ExportModel::XUAT_BAN_HD_HANG) {
    $result = $result . ' <a href="' . route('productExport.exportDetail', $object->id) . '" class="dropdown-item" title="Xuất excel chi tiết"><i class="fa fa-angle-right"></i> Xuất excel chi tiết</a>';
}
```

- [ ] **Step 2: Verify** mở `admin/warehouse/product_exports/all`: phiếu type=14 có item "Xuất excel chi tiết" trong dropdown; phiếu loại khác KHÔNG có. Bấm → tải đúng file.

---

## Task 9: Nút ở màn show

**Files:** Modify `resources/views/warehouse/product_exports/show.blade.php` (khu vực nút đầu trang/cạnh nút In phiếu — tìm link `productExport.print` trong file).

- [ ] **Step 1:** Đọc khu vực nút trong show.blade.php (tìm `productExport.print`) để đặt nút cùng chỗ, đúng style button hiện có.
- [ ] **Step 2:** Thêm nút (chỉ type=14 — dùng `@if($object->type == 14)` ở Blade server-side hoặc `ng-if="form.type == 14"` nếu nằm trong vùng Angular):

```blade
@if($object->type == \App\Model\Warehouse\ExportModel::XUAT_BAN_HD_HANG)
    <a href="{{ route('productExport.exportDetail', $object->id) }}" class="btn btn-success btn-sm" title="Xuất excel chi tiết">
        <i class="fa fa-file-excel-o"></i> Xuất excel chi tiết
    </a>
@endif
```

> Nếu khu vực nút nằm trong DOM do Angular compile, đổi điều kiện sang `ng-if="form.type == 14"` và bỏ `@if` Blade (tránh lỗi compile Angular 1.3.9). Xác nhận biến `$object` có sẵn trong show.blade (controller `show()` truyền gì).

- [ ] **Step 3: Verify** mở màn chi tiết 1 phiếu type=14 → có nút; bấm tải đúng file. Mở phiếu loại khác → không có nút.

---

## Task 10: Đối chiếu tổng thể với file mẫu

- [ ] **Step 1:** Xuất 1 phiếu **không xuất thẳng** (đủ bốc xếp + vận chuyển) → đối chiếu sheet "Xuất bán(khôngXT)" của file mẫu: thứ tự section, nhãn, dữ liệu, "không merge ô".
- [ ] **Step 2:** Xuất 1 phiếu **xuất thẳng** → đối chiếu sheet "Xuất bán (XT)": có Phiếu YCXH, KHÔNG có Kho xuất/Vận chuyển/Thủ kho/Người nhận hàng, KHÔNG có section Vận chuyển.
- [ ] **Step 3:** Báo lại các sai lệch (nếu có) để chỉnh blade.

---

### Checkpoint — 2026-06-09
Vừa hoàn thành: Task 1–9 code xong (route, Excel class, controller exportDetail, blade đủ section, nút list + show). php -l sạch toàn bộ.
Đang làm dở: Task 10 (đối chiếu output với 2 sheet file mẫu) — cần chạy export thật trên trình duyệt với phiếu type=14.
Bước tiếp theo: user chạy thử export + đối chiếu mẫu; xác nhận 2 điểm review (xem dưới).
Blocked:

### Ghi chú implementation (subagent đã điều chỉnh so với plan)
- `vat` bốc xếp là **% (không phải tiền)** → blade tự tính `vatPrice = total_money*vat/100`, `Số tiền sau VAT = total_money + vatPrice`. Hiện đang in dòng "VAT (%)" = giá trị %; **cần đối chiếu mẫu** xem có muốn hiện "Số tiền VAT" (= vatPrice) thay vì %.
- `rent_type`: **1 = Công ty, 2 = Thuê ngoài** (plan ghi ngược → đã sửa). Thuê ngoài hiện NCC/TK nợ/mã phí/vụ việc; Công ty hiện bảng người nhận việc (`executors`: `employee_name`, `employee_price`).
- Vận chuyển: điều kiện hiện block = `!$direct && $we->vehicle_company_id`; field thực tế: `total_km_expected`, `total_km_actual`, `total_cost_transition`, `delivery_tax`, `payer_employee_amount`, `payer_company_amount`; chuyến xe qua `we->trips` (`trip->trip->name`, `payer_employee_amount`, `payer_company_amount`).
- Route controller dùng prefix `Warehouse\ProductExportsController` theo convention web.php.

### Cần user xác nhận khi chạy thử (Task 10)
1. Cột "VAT" bốc xếp: hiện % hay số tiền VAT?
2. Điều kiện hiện block Vận chuyển (`vehicle_company_id`) có đúng nghiệp vụ không?
3. Đối chiếu thứ tự/nhãn/dữ liệu 2 sheet mẫu (không xuất thẳng / xuất thẳng).
