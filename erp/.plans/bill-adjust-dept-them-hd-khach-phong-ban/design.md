# Design — Bill Adjust Dept: thêm chọn HĐ/khách + phòng ban

**Ngày:** 2026-06-23 · **Phạm vi:** ERP (TanPhatDev) · **Màn:** `admin/income-expenditure/bill_adjust_dept/create` (+ edit dùng chung form)

## Mục tiêu
Phiếu kế toán điều chỉnh công nợ (Bill Adjust Dept) — bổ sung lựa chọn dữ liệu khi tạo:
1. **Mã khách**: cho chọn thêm **Phòng ban** (status Hoạt động) làm đối tượng.
2. **Bỏ cột "Số phiếu yc xuất hàng"** (chỉ ẩn FE).
3. **Đơn hàng/Hợp đồng**: cho chọn thêm **HĐ mua dịch vụ** (`BuyServiceContract`) và **Đơn bảo hiểm** (`InsurancePrincipleForm`).

## Hiện trạng (đã khảo sát)
- Route: `bill_adjust_dept.create` → `IncomeExpenditure\BillAdjustDeptController@create` → view `income_expenditure/bill_adjust_depts/{create,form,formJs}.blade.php` + class JS `partials/classes/IncomeExpenditure/BillAdjustDept(Detail).blade.php`.
- **Mã khách (đối tượng):** `form.blade.php:239-251`, nút → `detail.chooseCustomer()` (`BillAdjustDeptDetail.blade.php:247-290`) mở modal gọi route `searchObject` (`Common\SearchController@searchObject:311`). Lưu `objectable_type/objectable_id/objectable_code/objectable_name`.
  - `searchObject` hiện union: customers (Customer/Supplier theo `is_supplier`) + employees, đều `status=1`. **Là endpoint DÙNG CHUNG nhiều màn.**
- **Cột "Số phiếu yc xuất hàng":** `form.blade.php:204` (th) + `311-325` (td), binding `detail.exportable_*`, modal `showModalProductExportRequest()`.
- **Đơn hàng/Hợp đồng:** `form.blade.php:286-310`, nút → `detail.chooseContract()` (`BillAdjustDeptDetail.blade.php:292-342`) mở modal gọi `searchAllContract` với `type='bill_adjust_dept'` → `SearchContractService@searchAllContract`. Nhánh `bill_adjust_dept` (`SearchContractService.php:~302-310`) hiện chỉ trả: FirmContract (type[1,4,7,8]) + WrServiceContract (type[1,2]).
  - `BuyServiceContract` đã có query sẵn trong service (dòng 121-123, đối tượng = `supplier_id`) nhưng **chưa include** vào nhánh `bill_adjust_dept`.

## Quyết định (đã chốt với user)
- Mục 1: phương án **(a)** — Phòng ban là 1 loại đối tượng trong **cùng modal** đối tượng. Phạm vi: **status=1 AND `company_id` = công ty người đăng nhập**.
- Mục 2: **chỉ ẩn FE**, giữ nguyên data + logic `exportable` ở BE.
- Mục 3: HĐ mua dịch vụ = `BuyServiceContract` (đối tượng NCC). Đơn bảo hiểm = `InsurancePrincipleForm` (đối tượng NCC qua `supplier_id`), **chỉ status `DA_DUYET=2`**, hiển thị `code`.

## Thiết kế chi tiết

### Mục 1 — Phòng ban làm đối tượng
**BE — `SearchController@searchObject`:** thêm union nhánh `departments` **CÓ ĐIỀU KIỆN** theo flag request (vd `include_department=1`) để KHÔNG ảnh hưởng các màn khác dùng chung `searchObject`:
```php
if ($request->include_department) {
    $departments = DB::table('departments')
        ->select(['id', 'code', DB::raw('name as fullname'), 'status',
                  DB::raw('"App\\\\Model\\\\Common\\\\Department" as type_object')])
        ->where('status', 1)
        ->where('company_id', auth()->user()->info->company_id);
    // áp filter code/fullname như customers; union vào $results
}
```
**FE — `BillAdjustDeptDetail.blade.php::chooseCustomer()`:** modal `searchObject` truyền thêm `include_department: 1`. Khi chọn row `type_object == Department` → set `objectable_type='App\Model\Common\Department'`, `objectable_id`, `objectable_code`(code), `objectable_name`(name).
**Kiểm tra khi implement:** BE store của BillAdjustDept(Detail) có whitelist/validate `objectable_type` không → nếu có, thêm `Department::class`. Quan hệ polymorphic `objectable()` hiển thị tên phòng ban ở màn show/print.

### Mục 2 — Bỏ cột "Số phiếu yc xuất hàng" (FE)
- Xóa `<th>` `form.blade.php:204` và `<td>` `form.blade.php:311-325`.
- `form.blade.php` dùng chung create + edit → ẩn ở cả hai. Rà thêm `formShow.blade.php` / `approved.blade.php` / export blade `reports/exports/bill_adjust_dept*` nếu có cột tương ứng → ẩn cho đồng bộ.
- **Không** đụng class JS (`detail.exportable_*`, `showModalProductExportRequest`) và **không** đụng BE store/load — chỉ bỏ phần render cột.

### Mục 3 — Thêm 2 loại vào chọn HĐ
**BE — `SearchContractService`:**
- Trong nhánh `type=='bill_adjust_dept'`: `unionAll($buy_service_contract)` (query sẵn có) + nhánh mới `$insurance_principle_form`.
- Query mới `$insurance_principle_form`:
  ```php
  InsurancePrincipleForm::query()->with(['employee_create.info.department','supplier'])
    ->select('id','code','status','supplier_id as objectable_id','created_at','created_by',
             DB::raw('"insurance_principle_form" as type'), DB::raw('0 as payed_cost'), DB::raw('"" as handover_date'))
    ->where('status', InsurancePrincipleForm::DA_DUYET)        // =2
    ->where('company_id', auth()->user()->info->company_id);
  ```
- Cập nhật các hàm phụ trong service xử lý theo `contractable_type` (vùng `extrated`, map objectable_type, dòng ~220-280 / 475-507) để thêm case `'buy_service_contract'` (nếu chưa có cho bill_adjust_dept) và `'insurance_principle_form'` → objectable_type = `Supplier::class`.
**FE — `BillAdjustDeptDetail.blade.php::chooseContract()`:** modal cùng route `searchAllContract` nên tự có thêm 2 loại; bổ sung map `contractable_type` → class khi lưu:
- `buy_service_contract` → `App\Model\Sale\BuyServiceContract`
- `insurance_principle_form` → `App\Model\Insurance\InsurancePrincipleForm`
- Khi chọn → auto đối tượng (Mã khách) = NCC (`Supplier`) tương ứng, như HĐ hiện tại.

## Edge cases
- Phòng ban không có khái niệm "đơn hàng/hợp đồng" → khi đối tượng là Phòng ban, cột HĐ để trống (không bắt buộc).
- 2 loại HĐ mới đối tượng = NCC; đảm bảo set đúng `objectable_type=Supplier`, `objectable_id=supplier_id`.
- Company scope: phòng ban + đơn bảo hiểm lọc theo `company_id` công ty người đăng nhập (đồng bộ cách FirmContract lọc theo `employee_create.info.company_id`).

## Hàm dùng chung — lưu ý
- `searchObject`: thêm Phòng ban **qua flag** `include_department` → không ảnh hưởng màn khác.
- `searchAllContract`: chỉ sửa nhánh `type=='bill_adjust_dept'` + thêm case mapping cho 2 type mới; đảm bảo không phá các `type` khác.
→ Theo CLAUDE.md, đây là sửa hàm dùng chung có kiểm soát; cần review kỹ.

## Ngoài phạm vi
- Không bỏ logic/dữ liệu `exportable` ở BE.
- Không đổi nghiệp vụ hạch toán/validate hiện có của phiếu.
