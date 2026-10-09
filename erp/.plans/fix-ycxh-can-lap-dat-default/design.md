# Fix: "Cần lắp đặt" (YCXH) mặc định rỗng + cảnh báo inline

> Issue: http://quanly.dnsmedia.vn/issues/9661
> Màn: YCXH tạo mới — `/admin/warehouse/product_export_requests/create`

## Bug
Field **"Cần lắp đặt"** (radio Có/Không, chỉ hiện khi `type == 14` = XUAT_BAN_HD_HANG) đang **mặc định tích "KHÔNG"**. Người dùng hay quên đổi sang "Có" khi thực tế cần lắp đặt → tạo sai (không tạo được YC lắp đặt bàn giao → không quyết toán được HĐ).

## Yêu cầu sửa
- "Cần lắp đặt" **mặc định hiển thị RỖNG** (không radio nào được chọn).
- **Cảnh báo inline** (viền/hiển thị lỗi) + chặn submit nếu người dùng **không tích** khi type==14.

## Root cause
- Field thực = `form.need_repair` (label "Cần lắp đặt"; radio value 1=Có / 0=Không).
- `resources/views/partials/classes/warehouse/ProductExportRequest.blade.php:44`:
  `if (form.need_repair == null) this.need_repair = false;` → form tạo mới (`new ProductExportRequest({})`) mặc định `false` → radio "Không" tự tích (`ng-checked="need_repair == 0"`, `false == 0` → true).
- `create.blade.php $scope.submit`: chỉ có confirm khi type==14 && status==2 && need_repair đã set (`shouldConfirmNeedRepair`); KHÔNG chặn khi để trống.
- BE `store()` (`ProductExportRequestsController`) validate qua `Validator::make($request->all(), $rule, $translate)` trả `{success:false, errors}` (HTTP 200); block type==14 tại dòng ~409 — chưa require need_repair.

## Giải pháp
1. **FE default rỗng**: `ProductExportRequest.blade.php:44` — form mới để `need_repair = null` (không set false). Với null: `null == 0` và `null == 1` đều false → cả 2 radio bỏ chọn. Edit không ảnh hưởng (load giá trị thật, không rơi nhánh null).
2. **FE chặn + inline**: `create.blade.php $scope.submit` — đầu hàm, nếu `type == 14` và need_repair chưa ∈ ['0','1',0,1,true,false] → `errors['need_repair'] = ['Vui lòng chọn "Cần lắp đặt".']` + `toastr.warning` + `return` (không submit). Inline đã có sẵn tại `form.blade.php:53-55`.
3. **FE clear lỗi khi chọn**: 2 radio thêm `ng-change` xóa `errors['need_repair']`.
4. **BE defense**: `store()` block type==14 thêm `'need_repair' => 'required'` + message "Vui lòng chọn Cần lắp đặt". (dùng `required`, KHÔNG `in:0,1` để tránh phá giá trị boolean khi serialize).

## Phạm vi / rủi ro
- Chỉ ảnh hưởng `type == 14` (XUAT_BAN_HD_HANG). Loại khác không hiện field, không đổi hành vi (need_repair null → BE `filter_var`→false như cũ).
- Màn Sửa (edit): dùng chung form class nhưng luôn load need_repair có giá trị → không rơi default rỗng.
- Không đọc/sửa vendor. Verify: `php -l` + `view:clear` + test browser (tạo type 14 không chọn → chặn + inline; chọn Có/Không → submit OK; edit hiển thị đúng).
