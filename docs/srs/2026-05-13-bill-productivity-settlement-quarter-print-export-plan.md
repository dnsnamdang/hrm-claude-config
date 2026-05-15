# In/Xuất Excel phiếu quyết toán thưởng năng suất quý — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm chức năng In (HTML) và Xuất Excel cho phiếu quyết toán thưởng năng suất quý, nút đặt ở danh sách + chi tiết.

**Architecture:** Tạo blade template cho Excel export (FromView pattern). Controller build HTML table cho print, dùng view `print.blade.php` chung. Thêm link vào dropdown action trên danh sách (server-side Datatable) và nút trên trang chi tiết.

**Tech Stack:** Laravel 6, Maatwebsite/Excel 3.1, Blade, AngularJS (views), Yajra Datatables

---

### Task 1: Tạo blade template cho Excel export

**Files:**
- Create: `TanPhatDev/resources/views/reports/exports/bill_productivity_settlement_quarter.blade.php`

- [ ] **Step 1: Tạo file blade template**

```html
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
<table>
    <thead>
    <tr>
        <td colspan="16" style="text-align: center">
            <img alt="" width="1460" src="{{ safeImage($data['header']) }}"/>
        </td>
    </tr>
    <tr>
        <td colspan="16" style="text-align: center; font-weight: bold; font-size: 20px">
            QUYẾT TOÁN THƯỞNG NĂNG SUẤT QUÝ
        </td>
    </tr>
    <tr>
        <td colspan="16" style="text-align: center; font-size: 14px">
            Kỳ {{ $data['period'] }} năm {{ $data['year'] }} — Từ ngày {{ $data['date_from'] }} đến ngày {{ $data['date_to'] }}
        </td>
    </tr>
    <tr>
        <td colspan="16" style="text-align: center; font-size: 14px">
            Phòng ban: {{ $data['department_name'] }}
        </td>
    </tr>
    <tr>
        <td rowspan="2" style="border:1px solid black; text-align:center; font-weight:bold; width:50px">STT</td>
        <td rowspan="2" style="border:1px solid black; text-align:center; font-weight:bold; width:200px">Nhân viên</td>
        <td rowspan="2" style="border:1px solid black; text-align:center; font-weight:bold; width:120px">DS tiêu chuẩn</td>
        <td rowspan="2" style="border:1px solid black; text-align:center; font-weight:bold; width:120px">Thưởng TH HĐ</td>
        <td colspan="3" style="border:1px solid black; text-align:center; font-weight:bold">Thưởng năng suất tháng</td>
        <td colspan="3" style="border:1px solid black; text-align:center; font-weight:bold">Thưởng năng suất quý</td>
        <td rowspan="2" style="border:1px solid black; text-align:center; font-weight:bold; width:120px">Tổng TNS lũy tiến</td>
        <td rowspan="2" style="border:1px solid black; text-align:center; font-weight:bold; width:120px">Thưởng thêm</td>
        <td colspan="3" style="border:1px solid black; text-align:center; font-weight:bold">Phân chia thưởng thêm</td>
        <td rowspan="2" style="border:1px solid black; text-align:center; font-weight:bold; width:120px">Tổng thu nhập từ BH quý</td>
    </tr>
    <tr>
        <td style="border:1px solid black; text-align:center; font-weight:bold; width:100px">NV</td>
        <td style="border:1px solid black; text-align:center; font-weight:bold; width:100px">TBP</td>
        <td style="border:1px solid black; text-align:center; font-weight:bold; width:100px">TP</td>
        <td style="border:1px solid black; text-align:center; font-weight:bold; width:100px">NV</td>
        <td style="border:1px solid black; text-align:center; font-weight:bold; width:100px">TBP</td>
        <td style="border:1px solid black; text-align:center; font-weight:bold; width:100px">TP</td>
        <td style="border:1px solid black; text-align:center; font-weight:bold; width:100px">NV</td>
        <td style="border:1px solid black; text-align:center; font-weight:bold; width:100px">TBP</td>
        <td style="border:1px solid black; text-align:center; font-weight:bold; width:100px">TP</td>
    </tr>
    {{-- Dòng tổng --}}
    <tr>
        <td colspan="2" style="border:1px solid black; text-align:center; font-weight:bold">Tổng cộng</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_actual_sale'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_cost'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_month_nv'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_month_tbp'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_month_tp'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_quarter_nv'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_quarter_tbp'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_quarter_tp'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_employee'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_bonus_nv'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_bonus_nv_share'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_bonus_tbp'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_commission_bonus_tp'] }}</td>
        <td style="border:1px solid black; text-align:right; font-weight:bold">{{ $data['total']['sum_income_quarter'] }}</td>
    </tr>
    </thead>
    <tbody>
    @foreach($data['employees'] as $index => $emp)
    <tr>
        <td style="border:1px solid black; text-align:center">{{ $index + 1 }}</td>
        <td style="border:1px solid black; text-align:left">{{ $emp['employee_code'] }} - {{ $emp['employee_name'] }}{{ $emp['role'] == 'part_lead' ? ' (TBP)' : ($emp['role'] == 'dept_lead' ? ' (TP)' : '') }}</td>
        <td style="border:1px solid black; text-align:right">{{ $emp['sum_actual_sale'] }}</td>
        <td style="border:1px solid black; text-align:right">{{ $emp['sum_commission_cost'] }}</td>
        {{-- TNS tháng NV/TBP/TP --}}
        <td style="border:1px solid black; text-align:right">{{ $emp['col_month_nv'] }}</td>
        <td style="border:1px solid black; text-align:right">{{ $emp['col_month_tbp'] }}</td>
        <td style="border:1px solid black; text-align:right">{{ $emp['col_month_tp'] }}</td>
        {{-- TNS quý NV/TBP/TP --}}
        <td style="border:1px solid black; text-align:right">{{ $emp['col_quarter_nv'] }}</td>
        <td style="border:1px solid black; text-align:right">{{ $emp['col_quarter_tbp'] }}</td>
        <td style="border:1px solid black; text-align:right">{{ $emp['col_quarter_tp'] }}</td>
        {{-- Tổng TNS lũy tiến --}}
        <td style="border:1px solid black; text-align:right">{{ $emp['sum_commission_employee'] }}</td>
        {{-- Thưởng thêm --}}
        <td style="border:1px solid black; text-align:right">{{ $emp['base_commission_bonus'] }}</td>
        {{-- Phân chia NV/TBP/TP --}}
        <td style="border:1px solid black; text-align:right">{{ $emp['col_bonus_nv'] }}</td>
        <td style="border:1px solid black; text-align:right">{{ $emp['col_bonus_tbp'] }}</td>
        <td style="border:1px solid black; text-align:right">{{ $emp['col_bonus_tp'] }}</td>
        {{-- Tổng thu nhập --}}
        <td style="border:1px solid black; text-align:right">{{ $emp['sum_income_quarter'] }}</td>
    </tr>
    @endforeach
    </tbody>
</table>

{{-- Chữ ký --}}
<table style="width:100%; margin-top:30px">
    <tr>
        <td style="text-align:center; width:33%"><b>Người lập</b></td>
        <td style="text-align:center; width:33%"><b>Trưởng phòng</b></td>
        <td style="text-align:center; width:33%"><b>Kế toán</b></td>
    </tr>
    <tr>
        <td style="text-align:center; height:60px"></td>
        <td style="text-align:center"></td>
        <td style="text-align:center"></td>
    </tr>
    <tr>
        <td style="text-align:center"><b>{{ $data['creator_name'] }}</b></td>
        <td style="text-align:center"></td>
        <td style="text-align:center"></td>
    </tr>
</table>
</body>
</html>
```

---

### Task 2: Tạo ExcelExport class

**Files:**
- Create: `TanPhatDev/app/ExcelExports/BillProductivitySettlementQuarterExcel.php`

- [ ] **Step 1: Tạo file ExcelExport**

```php
<?php

namespace App\ExcelExports;

use Illuminate\Contracts\View\View;
use Maatwebsite\Excel\Concerns\FromView;
use Maatwebsite\Excel\Concerns\Exportable;
use Maatwebsite\Excel\Concerns\WithEvents;
use Maatwebsite\Excel\Events\AfterSheet;

class BillProductivitySettlementQuarterExcel implements FromView, WithEvents
{
    use Exportable;

    protected $data;
    protected $count;

    public function forData($data, $count)
    {
        $this->data = $data;
        $this->count = $count;

        return $this;
    }

    public function view(): View
    {
        $data = $this->data;
        return view('reports.exports.bill_productivity_settlement_quarter', compact('data'));
    }

    public function registerEvents(): array
    {
        return [
            AfterSheet::class => function (AfterSheet $event) {
                $count = $this->count;
                $headerRange = 'A5:P6';
                $dataRange = 'C8:P' . ($count + 8);

                $event->sheet->getStyle($headerRange)->getAlignment()->setWrapText(true);
                $event->sheet->getStyle($dataRange)->getNumberFormat()->setFormatCode('###,###,###');
            }
        ];
    }
}
```

---

### Task 3: Thêm method print() và export() vào Controller

**Files:**
- Modify: `TanPhatDev/app/Http/Controllers/Accounting/BillProductivitySettlementQuartersController.php`

- [ ] **Step 1: Thêm import ở đầu file**

Thêm sau dòng `use App\Employee;` (dòng 21):

```php
use App\ExcelExports\BillProductivitySettlementQuarterExcel;
```

- [ ] **Step 2: Thêm method `print($id)` vào cuối class**

Thêm trước dấu `}` đóng class:

```php
    public function print($id)
    {
        $bill = BillProductivitySettlementQuarter::getDataForEdit($id);
        $company = $bill->employee_create->info->company ?? null;

        $template = $this->buildPrintHtml($bill, $company);
        return view('print_landscape', compact('template'));
    }

    public function export($id)
    {
        $bill = BillProductivitySettlementQuarter::getDataForEdit($id);
        $company = $bill->employee_create->info->company ?? null;

        $data = $this->buildExportData($bill, $company);
        $count = count($bill->employees);
        $filename = 'QTTNSTQ_' . str_replace(['.', '/'], '_', $bill->code) . '.xlsx';

        return (new BillProductivitySettlementQuarterExcel())
            ->forData($data, $count)
            ->download($filename);
    }

    private function buildExportData($bill, $company)
    {
        $data = [];
        $data['header'] = $company->header ?? '';
        $data['period'] = $bill->period;
        $data['year'] = $bill->year;
        $data['date_from'] = $bill->date_from;
        $data['date_to'] = $bill->date_to;
        $data['department_name'] = $bill->department->name ?? '';
        $data['creator_name'] = $bill->employee_create->info->fullname ?? '';

        $sumMonthNv = 0; $sumMonthTbp = 0; $sumMonthTp = 0;
        $sumQuarterNv = 0; $sumQuarterTbp = 0; $sumQuarterTp = 0;
        $sumBonusNv = 0; $sumBonusTbp = 0; $sumBonusTp = 0;
        $sumBaseBonusNv = 0;

        $employees = [];
        foreach ($bill->employees as $emp) {
            $role = $emp->role ?? 'employee';
            $row = [
                'employee_code' => $emp->employee_code,
                'employee_name' => $emp->employee_name,
                'role' => $role,
                'sum_actual_sale' => $emp->sum_actual_sale,
                'sum_commission_cost' => $emp->sum_commission_cost,
                'sum_commission_employee' => $emp->sum_commission_employee,
                'sum_income_quarter' => $emp->sum_income_quarter,
            ];

            // TNS tháng theo role
            $row['col_month_nv'] = $role == 'employee' ? $emp->sum_commission_month_employee : ($emp->sum_commission_month_part_lead > 0 && $role != 'part_lead' ? $emp->sum_commission_month_part_lead : '');
            $row['col_month_tbp'] = $role == 'part_lead' ? $emp->sum_commission_month_employee : ($role == 'employee' && $emp->sum_commission_month_part_lead > 0 ? $emp->sum_commission_month_part_lead : '');
            $row['col_month_tp'] = $role == 'dept_lead' ? $emp->sum_commission_month_employee : ($role == 'employee' && $emp->sum_commission_month_dept_lead > 0 ? $emp->sum_commission_month_dept_lead : '');

            // TNS quý theo role
            $row['col_quarter_nv'] = $role == 'employee' ? $emp->sum_commission_quarter_employee : '';
            $row['col_quarter_tbp'] = $role == 'part_lead' ? $emp->sum_commission_quarter_employee : ($role == 'employee' && $emp->sum_commission_quarter_part_lead > 0 ? $emp->sum_commission_quarter_part_lead : '');
            $row['col_quarter_tp'] = $role == 'dept_lead' ? $emp->sum_commission_quarter_employee : ($role == 'employee' && $emp->sum_commission_quarter_dept_lead > 0 ? $emp->sum_commission_quarter_dept_lead : '');

            // Thưởng thêm
            $row['base_commission_bonus'] = $role == 'employee' ? $emp->sum_commission_bonus_employee : '';

            // Phân chia thưởng thêm
            $row['col_bonus_nv'] = $role == 'employee' ? $emp->sum_commission_bonus_employee : '';
            $row['col_bonus_tbp'] = $role == 'part_lead' ? $emp->sum_commission_bonus_employee : ($role == 'employee' && $emp->sum_commission_bonus_part_lead > 0 ? $emp->sum_commission_bonus_part_lead : '');
            $row['col_bonus_tp'] = $role == 'dept_lead' ? $emp->sum_commission_bonus_employee : ($role == 'employee' && $emp->sum_commission_bonus_dept_lead > 0 ? $emp->sum_commission_bonus_dept_lead : '');

            // Tính tổng
            if ($role == 'employee') {
                $sumMonthNv += $emp->sum_commission_month_employee;
                $sumQuarterNv += $emp->sum_commission_quarter_employee;
                $sumBonusNv += $emp->sum_commission_bonus_employee;
                $sumBaseBonusNv += $emp->sum_commission_bonus_employee;
            } elseif ($role == 'part_lead') {
                $sumMonthTbp += $emp->sum_commission_month_employee;
                $sumQuarterTbp += $emp->sum_commission_quarter_employee;
                $sumBonusTbp += $emp->sum_commission_bonus_employee;
            } elseif ($role == 'dept_lead') {
                $sumMonthTp += $emp->sum_commission_month_employee;
                $sumQuarterTp += $emp->sum_commission_quarter_employee;
                $sumBonusTp += $emp->sum_commission_bonus_employee;
            }

            $employees[] = $row;
        }

        $data['employees'] = $employees;
        $data['total'] = [
            'sum_actual_sale' => $bill->sum_actual_sale,
            'sum_commission_cost' => $bill->sum_commission_cost,
            'sum_commission_month_nv' => $sumMonthNv,
            'sum_commission_month_tbp' => $sumMonthTbp,
            'sum_commission_month_tp' => $sumMonthTp,
            'sum_commission_quarter_nv' => $sumQuarterNv,
            'sum_commission_quarter_tbp' => $sumQuarterTbp,
            'sum_commission_quarter_tp' => $sumQuarterTp,
            'sum_commission_employee' => $bill->sum_commission_employee,
            'sum_commission_bonus_nv' => $sumBaseBonusNv,
            'sum_commission_bonus_nv_share' => $sumBonusNv,
            'sum_commission_bonus_tbp' => $sumBonusTbp,
            'sum_commission_bonus_tp' => $sumBonusTp,
            'sum_income_quarter' => $bill->sum_income_quarter,
        ];

        return $data;
    }

    private function buildPrintHtml($bill, $company)
    {
        $data = $this->buildExportData($bill, $company);

        $header = '<div style="text-align:center"><img src="' . safeImage($company->header ?? '') . '" width="100%" /></div>';
        $header .= '<h3 style="text-align:center; margin:10px 0">QUYẾT TOÁN THƯỞNG NĂNG SUẤT QUÝ</h3>';
        $header .= '<p style="text-align:center">Kỳ ' . $data['period'] . ' năm ' . $data['year'] . ' — Từ ngày ' . $data['date_from'] . ' đến ngày ' . $data['date_to'] . '</p>';
        $header .= '<p style="text-align:center">Phòng ban: ' . $data['department_name'] . '</p>';

        // Build table
        $s = 'style="border:1px solid black;';
        $table = '<table style="width:100%; border-collapse:collapse; font-size:12px">';

        // Header row 1
        $table .= '<tr>';
        $table .= '<td rowspan="2" ' . $s . ' text-align:center"><b>STT</b></td>';
        $table .= '<td rowspan="2" ' . $s . ' text-align:center"><b>Nhân viên</b></td>';
        $table .= '<td rowspan="2" ' . $s . ' text-align:center"><b>DS tiêu chuẩn</b></td>';
        $table .= '<td rowspan="2" ' . $s . ' text-align:center"><b>Thưởng TH HĐ</b></td>';
        $table .= '<td colspan="3" ' . $s . ' text-align:center"><b>Thưởng NS tháng</b></td>';
        $table .= '<td colspan="3" ' . $s . ' text-align:center"><b>Thưởng NS quý</b></td>';
        $table .= '<td rowspan="2" ' . $s . ' text-align:center"><b>Tổng TNS lũy tiến</b></td>';
        $table .= '<td rowspan="2" ' . $s . ' text-align:center"><b>Thưởng thêm</b></td>';
        $table .= '<td colspan="3" ' . $s . ' text-align:center"><b>Phân chia thưởng thêm</b></td>';
        $table .= '<td rowspan="2" ' . $s . ' text-align:center"><b>Tổng thu nhập từ BH quý</b></td>';
        $table .= '</tr>';

        // Header row 2
        $table .= '<tr>';
        foreach (['NV','TBP','TP','NV','TBP','TP','NV','TBP','TP'] as $sub) {
            $table .= '<td ' . $s . ' text-align:center"><b>' . $sub . '</b></td>';
        }
        $table .= '</tr>';

        // Tổng cộng
        $t = $data['total'];
        $table .= '<tr>';
        $table .= '<td colspan="2" ' . $s . ' text-align:center"><b>Tổng cộng</b></td>';
        foreach ([
            $t['sum_actual_sale'], $t['sum_commission_cost'],
            $t['sum_commission_month_nv'], $t['sum_commission_month_tbp'], $t['sum_commission_month_tp'],
            $t['sum_commission_quarter_nv'], $t['sum_commission_quarter_tbp'], $t['sum_commission_quarter_tp'],
            $t['sum_commission_employee'], $t['sum_commission_bonus_nv'],
            $t['sum_commission_bonus_nv_share'], $t['sum_commission_bonus_tbp'], $t['sum_commission_bonus_tp'],
            $t['sum_income_quarter']
        ] as $val) {
            $table .= '<td ' . $s . ' text-align:right"><b>' . ($val ? formatCurrency($val) : '-') . '</b></td>';
        }
        $table .= '</tr>';

        // Rows
        foreach ($data['employees'] as $idx => $emp) {
            $roleSuffix = $emp['role'] == 'part_lead' ? ' (TBP)' : ($emp['role'] == 'dept_lead' ? ' (TP)' : '');
            $table .= '<tr>';
            $table .= '<td ' . $s . ' text-align:center">' . ($idx + 1) . '</td>';
            $table .= '<td ' . $s . ' text-align:left">' . str_replace('&', '&amp;', $emp['employee_code'] . ' - ' . $emp['employee_name'] . $roleSuffix) . '</td>';
            foreach ([
                $emp['sum_actual_sale'], $emp['sum_commission_cost'],
                $emp['col_month_nv'], $emp['col_month_tbp'], $emp['col_month_tp'],
                $emp['col_quarter_nv'], $emp['col_quarter_tbp'], $emp['col_quarter_tp'],
                $emp['sum_commission_employee'], $emp['base_commission_bonus'],
                $emp['col_bonus_nv'], $emp['col_bonus_tbp'], $emp['col_bonus_tp'],
                $emp['sum_income_quarter']
            ] as $val) {
                $table .= '<td ' . $s . ' text-align:right">' . ($val ? formatCurrency($val) : '-') . '</td>';
            }
            $table .= '</tr>';
        }
        $table .= '</table>';

        // Chữ ký
        $sign = '<table style="width:100%; margin-top:30px"><tr>';
        $sign .= '<td style="text-align:center; width:33%"><b>Người lập</b></td>';
        $sign .= '<td style="text-align:center; width:33%"><b>Trưởng phòng</b></td>';
        $sign .= '<td style="text-align:center; width:33%"><b>Kế toán</b></td>';
        $sign .= '</tr><tr><td style="height:60px"></td><td></td><td></td></tr><tr>';
        $sign .= '<td style="text-align:center"><b>' . ($data['creator_name']) . '</b></td>';
        $sign .= '<td></td><td></td></tr></table>';

        return $header . $table . $sign;
    }
```

---

### Task 4: Thêm routes

**Files:**
- Modify: `TanPhatDev/routes/web.php:4754`

- [ ] **Step 1: Thêm 2 route sau dòng 4754**

Tìm dòng:
```php
Route::post('/{id}/deny', 'Accounting\BillProductivitySettlementQuartersController@deny')->name('bill_productivity_settlement_quarters.deny');
```

Thêm ngay sau:
```php
            Route::get('/{id}/print', 'Accounting\BillProductivitySettlementQuartersController@print')->name('bill_productivity_settlement_quarters.print');
            Route::get('/{id}/export', 'Accounting\BillProductivitySettlementQuartersController@export')->name('bill_productivity_settlement_quarters.export');
```

---

### Task 5: Thêm link In/Xuất Excel vào dropdown action trên danh sách

**Files:**
- Modify: `TanPhatDev/app/Http/Controllers/Accounting/BillProductivitySettlementQuartersController.php:67-83` (method `searchData`, phần `addColumn('action')`)

- [ ] **Step 1: Sửa addColumn action**

Tìm đoạn trong method `searchData()`:

```php
                if ($object->canDelete()) {
                    $html .= '<a href="' . route('bill_productivity_settlement_quarters.delete', $object->id) . '" class="dropdown-item delete" title="Xóa">Xóa</a>';
                }

                $html .= '</div></div>';
```

Thay bằng:

```php
                if ($object->canDelete()) {
                    $html .= '<a href="' . route('bill_productivity_settlement_quarters.delete', $object->id) . '" class="dropdown-item delete" title="Xóa">Xóa</a>';
                }

                $html .= '<a href="' . route('bill_productivity_settlement_quarters.print', $object->id) . '" class="dropdown-item" target="_blank" title="In">In</a>';
                $html .= '<a href="' . route('bill_productivity_settlement_quarters.export', $object->id) . '" class="dropdown-item" title="Xuất Excel">Xuất Excel</a>';

                $html .= '</div></div>';
```

---

### Task 6: Thêm nút In/Xuất Excel vào trang chi tiết

**Files:**
- Modify: `TanPhatDev/resources/views/accounting/bill_productivity_settlement_quarters/show.blade.php:16-39`

- [ ] **Step 1: Thêm nút In + Xuất Excel**

Tìm đoạn:

```blade
    <div class="text-right">
        @if ($data->canEdit())
```

Thay bằng:

```blade
    <div class="text-right">
        <a href="{{ route('bill_productivity_settlement_quarters.print', ['id' => $data->id]) }}"
           class="btn btn-info btn-cons" target="_blank">
            <i class="fa fa-print"></i> In
        </a>
        <a href="{{ route('bill_productivity_settlement_quarters.export', ['id' => $data->id]) }}"
           class="btn btn-success btn-cons">
            <i class="fa fa-file-excel-o"></i> Xuất Excel
        </a>
        @if ($data->canEdit())
```

---

### Task 7: Verify — kiểm tra `print_landscape` view tồn tại

**Files:**
- Read: `TanPhatDev/resources/views/print_landscape.blade.php`

- [ ] **Step 1: Kiểm tra file print_landscape.blade.php**

Chạy:
```bash
head -20 TanPhatDev/resources/views/print_landscape.blade.php
```

Nếu file tồn tại và tương tự `print.blade.php` (nhận biến `$template`) → OK.
Nếu khác cấu trúc hoặc không nhận `$template` → đổi `print()` method sang dùng `view('print', ...)` thay vì `view('print_landscape', ...)`.

- [ ] **Step 2: Test thủ công**

1. Vào danh sách phiếu quyết toán thưởng năng suất quý
2. Ở dropdown hành động → click "In" → mở tab mới hiển thị bản in
3. Click "Xuất Excel" → tải file .xlsx
4. Vào chi tiết 1 phiếu → click nút "In" và "Xuất Excel"
5. Kiểm tra: header, tiêu đề, bảng dữ liệu (16 cột, đúng giá trị), chữ ký
