# Design: Lập phụ lục bổ sung cho PI trong nước (TanPhatDev)

## Bối cảnh

PI nhập khẩu (`purchase_invoice/ofSupplier`) có button "Lập phụ lục bổ sung" → redirect `buy_contract2/create?type=2&...`. PI trong nước theo hãng + tự do (`inland_purchase_invoice/ofSupplier?type=firm`/`type=free`) hiện chưa có button này — đoạn code đã được comment-out vì sai endpoint.

`InlandBuyContractNew` đã có code stub cho `type=4` (phụ lục) từ commit `b71ac091fb` (2022-12-19) nhưng **chưa wire UI**, chưa từng dùng thực tế. JS class `InlandBuyContractNew.blade.php` có method `buyContract2Search()` đang search nhầm sang `BuyContract2` (foreign).

## Quy tắc

### Schema
Mở rộng giá trị `inland_buy_contract_news.type`:
- `1`: HĐ tự do (free) — đã có
- `2`: HĐ theo hãng (firm) — đã có
- `3`: Đơn đặt hàng theo HĐNT — đã có
- **`4`: Phụ lục theo hãng (firm annex)** — tận dụng code stub có sẵn
- **`5`: Phụ lục tự do (free annex)** — mới thêm

KHÔNG cần migration — không thêm cột mới. `parent_id` đã có sẵn nullable.

### Logic phụ lục
- Phụ lục là **HĐ độc lập**, có flow báo hàng về riêng
- Form tạo phụ lục y hệt HĐ chính (form trống, user lập từ đầu), khác duy nhất:
  - Lưu `parent_id` + `type=4/5`
  - Auto-fill `code = parent_code + '-PL'` (user vẫn sửa được)
- Validate parent contract chưa huỷ trước khi tạo phụ lục (giống `BuyContract2Controller::store` L366-371)
- Mapping firm/free khắp hệ thống:
  - `in_array(type, [2, 3, 4]) → 'firm'`
  - `in_array(type, [1, 5]) → 'free'` (default else)

## Thay đổi

### Backend

`app/Http/Controllers/Order/InlandBuyContractNewController.php`:
- L113 `searchData` action button "Báo hàng về": đổi `if ($object->type == 2 || $object->type == 3)` → `if (in_array($object->type, [2, 3, 4]))`
- L215 `store`: đổi `if ($request->type == 4)` → `if (in_array($request->type, [4, 5]))` cho `parent_id required` rule
- L215 thêm check parent status: nếu `parent.status == DA_HUY` → `responseErrors('Hợp đồng gốc đã hủy. Không thể tạo phụ lục bổ sung!')`
- L483 `update`: tương tự cho cả parent_id required + status check
- L286-291 không cần đổi — nhánh `else $object->type = $request->type` đã handle 4 và 5 (truyền số nguyên trực tiếp)

`app/Model/Order/InlandBuyContractNew.php`:
- `searchByFilter()`: nếu request `type=firm` → filter `whereIn type [2, 3, 4]`; `type=free` → filter `whereIn type [1, 5]`. (Verify cụ thể vị trí khi code.)

### Frontend — PI ofSupplier

`resources/views/orders/inland_purchase_invoice/of_supplier.blade.php`:
- Xoá comment-out L160-162
- Thêm button "Lập phụ lục bổ sung" `ng-click="createAdditionalContract()"` cạnh button "Lập hợp đồng" (giống pattern của `purchase_invoice/of_supplier.blade.php` L193-195)
- Thêm function JS (sau `createContract`):
  ```js
  $scope.createAdditionalContract = function () {
      $scope.stringParams = 'type={{ $type }}&' + Object.keys($scope.form)...
      let annexType = '{{ $type }}' === 'firm' ? 4 : 5;
      window.location.href = `/admin/orders/inland_buy_contract_new/create?type=${annexType}&` + $scope.stringParams;
  }
  ```

### Frontend — InlandBuyContractNew form

`resources/views/orders/inland_buy_contract_new/create.blade.php`:
- L13 sửa title cho type=4: "Phụ lục hợp đồng mua hàng theo hãng" (rõ hơn)
- Thêm nhánh `@elseif (request()->type == 5) Phụ lục hợp đồng mua hàng tự do`

`resources/views/orders/inland_buy_contract_new/edit.blade.php` + `show.blade.php`:
- Tương tự, thêm nhánh title cho `$object->type == 5`

`resources/views/orders/inland_buy_contract_new/form.blade.php`:
- L12: `ng-if="form.type == 4"` → `ng-if="form.type == 4 || form.type == 5"`
- L33: `ng-if="form.type == 4"` → `ng-if="form.type == 4 || form.type == 5"` cho label "Số phụ lục"
- L19: đổi `ng-click="form.buyContract2Search()"` → `ng-click="form.inlandBuyContractSearch()"`

### Frontend — JS class

`resources/views/partials/classes/order/InlandBuyContractNew.blade.php`:
- **Xoá** `buyContract2Search()` (L723-748) + `addBuyContract2()` (L750-764) — dead code, sai endpoint
- **Thêm** `inlandBuyContractSearch()`:
  ```js
  inlandBuyContractSearch = () => {
      let self = this;
      new BaseSearchModal({
          title: "Hợp đồng mua hàng",
          ajax: {
              url: "{!! route('inlandBuyContractNew.searchData') !!}",
              data: function (d, context) {
                  DATATABLE.mergeSearch(d, context);
                  d.supplier_id = self.supplier_id;
                  d.type = self.type == 4 ? 'firm' : 'free';
              }
          },
          ...
      }, function(obj) { self.addInlandBuyContract(obj); }).open();
  }
  ```
- **Thêm** `addInlandBuyContract(obj)`:
  ```js
  addInlandBuyContract = (obj) => {
      sendRequest({
          url: `/admin/orders/inland_buy_contract_new/${obj.id}/getData`,
          success: function(response) {
              if (response.success) {
                  self.parent_id = response.data.id;
                  self.parent_code = response.data.code;
                  self.code = self.parent_code + '-PL';
              }
          }
      }, self.scope);
  }
  ```
- Verify endpoint `/admin/orders/inland_buy_contract_new/${id}/getData` tồn tại (xem `routes/web.php`). Nếu không có → tạo method `getData` trong controller giống pattern BuyContract2.

## Không thay đổi

- BuyContract2 (PI nhập khẩu) — không động
- type=1, 2, 3 ở InlandBuyContractNew — không đổi semantic
- Bảng `inland_buy_contract_news` — không thêm cột (chỉ mở rộng giá trị enum)
- `getDataAnnexAdditionForInvoice()` (model L378+) — đã hoạt động dựa trên `parent_id`, không cần đổi
- Báo hàng về (`inlandProductArrivedNew`) — không động, chỉ cần URL từ index trỏ đúng `type=firm/free`
