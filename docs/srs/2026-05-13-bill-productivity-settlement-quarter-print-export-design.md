# In/Xuất Excel phiếu quyết toán thưởng năng suất quý

## Mục tiêu

Thêm chức năng In (HTML print) và Xuất Excel cho phiếu quyết toán thưởng năng suất quý (`bill_productivity_settlement_quarters`). Nút đặt ở dropdown hành động trên danh sách và trong trang chi tiết mỗi phiếu.

## Scope

- BE: `TanPhatDev` — Controller, Route, ExcelExport, Blade view
- FE: Blade views (AngularJS) — thêm nút vào `index.blade.php` và `show.blade.php`

## Dữ liệu

Lấy từ phiếu đã lưu trong DB:
- `bill_productivity_settlement_quarters` — thông tin chung (code, date_from, date_to, department_id, period, year, sum_*)
- `bill_productivity_settlement_quarter_employees` — chi tiết theo nhân viên (employee_id, role, sum_commission_*, sum_commission_bonus_*, sum_income_quarter)
- `employees` + `employee_infos` — mã NV, tên NV
- `departments` — tên phòng ban
- `companies` — tên công ty, header (logo)

Method load data: `BillProductivitySettlementQuarter::getDataForEdit($id)` — đã có sẵn, dùng lại.

## Cấu trúc bản in/export

### Header
- Logo + tên công ty (lấy từ `$bill->employee_create->info->company`)
- Tiêu đề: **QUYẾT TOÁN THƯỞNG NĂNG SUẤT QUÝ**
- Dòng phụ: `Kỳ [period] năm [year] — Từ ngày [date_from] đến ngày [date_to]`
- Phòng ban: `[department.name]`

### Bảng dữ liệu (16 cột, 2 dòng header)

Dòng header 1:

| STT | Nhân viên | DS tiêu chuẩn | Thưởng TH HĐ | Thưởng NS tháng (colspan=3) | Thưởng NS quý (colspan=3) | Tổng TNS lũy tiến | Thưởng thêm | Phân chia thưởng thêm (colspan=3) | Tổng thu nhập từ BH quý |

Dòng header 2 (sub-columns):

| | | | | NV | TBP | TP | NV | TBP | TP | | | NV | TBP | TP | |

Dòng Tổng cộng: hiển thị ngay sau header, sum tất cả nhân viên.

Dòng nhân viên: mỗi nhân viên 1 dòng. Logic hiển thị theo role giống form.blade.php:
- `employee`: hiển thị cột NV, ẩn TBP/TP (trừ khi có `sum_commission_month_part_lead` / `sum_commission_month_dept_lead`)
- `part_lead`: hiển thị cột TBP
- `dept_lead`: hiển thị cột TP

### Chữ ký (cuối trang)

3 cột: Người lập | Trưởng phòng | Người lập (kế toán)

Hiển thị tên người tạo phiếu ở cột "Người lập".

## Files ảnh hưởng

| File | Thay đổi |
|------|----------|
| `app/Http/Controllers/Accounting/BillProductivitySettlementQuartersController.php` | Thêm `print($id)` + `export($id)` |
| `routes/web.php` | Thêm 2 route trong group `bill_productivity_settlement_quarters` |
| `app/ExcelExports/BillProductivitySettlementQuarterExcel.php` | **Tạo mới** — implements FromView, WithEvents |
| `resources/views/reports/exports/bill_productivity_settlement_quarter.blade.php` | **Tạo mới** — blade template cho Excel |
| `resources/views/accounting/bill_productivity_settlement_quarters/index.blade.php` | Thêm link In + Xuất Excel vào dropdown action |
| `resources/views/accounting/bill_productivity_settlement_quarters/show.blade.php` | Thêm nút In + Xuất Excel |

## Chi tiết kỹ thuật

### Route
```php
Route::get('/{id}/print', '...Controller@print')->name('bill_productivity_settlement_quarters.print');
Route::get('/{id}/export', '...Controller@export')->name('bill_productivity_settlement_quarters.export');
```

### Controller — print()
- Load data bằng `getDataForEdit($id)`
- Build HTML table (giống pattern `CommissionSettlementQuarterPrint::getTable()`)
- Return `view('print', compact('template'))`

### Controller — export()
- Load data bằng `getDataForEdit($id)`
- Dùng `BillProductivitySettlementQuarterExcel` (FromView)
- Return download Excel file, tên: `QTTNST_QUY_{code}.xlsx`

### ExcelExport class
- Implements `FromView`, `WithEvents`
- `forData($data)` — nhận data đã load
- `view()` — render blade template
- `registerEvents()` — format số, wrap text header

### Template Excel (blade)
- Header: logo, tiêu đề, kỳ, phòng ban
- Bảng HTML table với border + style
- Chữ ký cuối

### Nút trên danh sách (index.blade.php)
Thêm vào dropdown action (cột `action` trong searchData Datatable):
```html
<a href="route('...print', $id)" class="dropdown-item" target="_blank">In</a>
<a href="route('...export', $id)" class="dropdown-item">Xuất Excel</a>
```

### Nút trên chi tiết (show.blade.php)
Thêm nút ở header card hoặc toolbar:
```html
<a href="route('...print', $id)" class="btn btn-info" target="_blank"><i class="fa fa-print"></i> In</a>
<a href="route('...export', $id)" class="btn btn-success"><i class="fa fa-file-excel-o"></i> Xuất Excel</a>
```
