# Plan: Lập phụ lục bổ sung cho PI trong nước (TanPhatDev)

## Trạng thái
- Bắt đầu: 2026-04-28
- Tiến độ: ✅ Hoàn thành 2026-04-29 (11 task code + 6 case manual test)

## Phase 1: Backend Model

### InlandBuyContractNew.php (model)
- [x] Task 1: Thêm 2 constant sau `const DON_HANG = 3;` (L36):
  ```php
  const PHU_LUC_HANG = 4;
  const PHU_LUC_TU_DO = 5;
  ```
- [x] Task 2: `searchByFilter()` (L860-871) — mở rộng filter theo nhóm firm/free để include phụ lục:
  - `arrived_firm` (L860-861): `whereIn('type', [HOP_DONG_HANG, DON_HANG, PHU_LUC_HANG])` (thêm 4)
  - `arrived_free` (L862-863): `whereIn('type', [HOP_DONG_TU_DO, PHU_LUC_TU_DO])` (đổi `where` → `whereIn` thêm 5)
  - `firm`/`type==2` (L866-867): `whereIn('type', [HOP_DONG_HANG, PHU_LUC_HANG])` (đổi `where` → `whereIn` thêm 4)
  - `free`/`type==1` (L864-865): `whereIn('type', [HOP_DONG_TU_DO, PHU_LUC_TU_DO])` (đổi `where` → `whereIn` thêm 5)

## Phase 2: Backend Controller

### InlandBuyContractNewController.php
- [x] Task 3: Action button "Báo hàng về" L113: đổi `if ($object->type == 2 || $object->type == 3)` → `if (in_array($object->type, [InlandBuyContractNew::HOP_DONG_HANG, InlandBuyContractNew::DON_HANG, InlandBuyContractNew::PHU_LUC_HANG]))` (3 giá trị → 'firm', else type=1/5 → 'free')

- [x] Task 4: `store()` L215 — đổi rule `parent_id` cho cả 2 loại phụ lục + check parent status:
  ```php
  if (in_array($request->type, [InlandBuyContractNew::PHU_LUC_HANG, InlandBuyContractNew::PHU_LUC_TU_DO])) {
      $rule['parent_id'] = 'required';
  }
  ```
  Trước `$validate = Validator::make(...)`. Sau khi validate fails, thêm block (giống BuyContract2Controller L366-371):
  ```php
  if (in_array($request->type, [InlandBuyContractNew::PHU_LUC_HANG, InlandBuyContractNew::PHU_LUC_TU_DO])) {
      $parent = InlandBuyContractNew::find($request->parent_id);
      if ($parent && $parent->status == InlandBuyContractNew::DA_HUY) {
          return $this->responseErrors('Hợp đồng gốc đã hủy. Không thể tạo phụ lục bổ sung!');
      }
  }
  ```

- [x] Task 5: `update()` L483 — áp dụng tương tự Task 4 (rule parent_id required + check parent status DA_HUY)

## Phase 3: Frontend titles

- [x] Task 6: `resources/views/orders/inland_buy_contract_new/create.blade.php` L13-17:
  - Đổi title type=4: "Phụ lục hợp đồng mua hàng theo hãng"
  - Thêm `@elseif (request()->type == 5) Phụ lục hợp đồng mua hàng tự do`

- [x] Task 7: `resources/views/orders/inland_buy_contract_new/edit.blade.php` L15-17 — tương tự (check `$object->type == 4` và thêm `$object->type == 5`)

- [x] Task 8: `resources/views/orders/inland_buy_contract_new/show.blade.php` L26-28 — tương tự

## Phase 4: Frontend form

- [x] Task 9: `resources/views/orders/inland_buy_contract_new/form.blade.php`:
  - L12: `ng-if="form.type == 4"` → `ng-if="form.type == 4 || form.type == 5"` (cột "Hợp đồng")
  - L33: `ng-if="form.type == 4"` → `ng-if="form.type == 4 || form.type == 5"` (label "Số phụ lục")
  - L19: đổi `ng-click="form.buyContract2Search()"` → `ng-click="form.inlandBuyContractSearch()"`

## Phase 5: Frontend JS class

- [x] Task 10: `resources/views/partials/classes/order/InlandBuyContractNew.blade.php`:
  - **Xoá** method `buyContract2Search()` (L723-748)
  - **Xoá** method `addBuyContract2()` (L750-764)
  - **Thêm** sau vị trí cũ:
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
                    d._type = 'all';
                }
            },
            language: i18nDataTable,
            columns: [
                {data: 'DT_RowIndex', orderable: false, title: "STT"},
                {data: 'code', title: "Số hợp đồng"},
                {data: 'created_at', title: "Ngày tạo"},
            ],
            search_columns: [
                {data: 'code', search_type: "text", placeholder: "Số hợp đồng"},
            ]
        }, function(obj) {
            self.addInlandBuyContract(obj);
        }).open();
    }

    addInlandBuyContract = (obj) => {
        let self = this;
        sendRequest({
            type: 'GET',
            url: `/admin/orders/inland_buy_contract_new/${obj.id}/getData`,
            success: function(response) {
                if (response.success) {
                    self.parent_id = response.data.id;
                    self.parent_code = response.data.code;
                    self.code = self.parent_code + '-PL';
                    toastr.success('Thêm thành công');
                }
            }
        }, self.scope);
    }
    ```

## Phase 6: Frontend ofSupplier wire button

- [x] Task 11: `resources/views/orders/inland_purchase_invoice/of_supplier.blade.php`:
  - Xoá comment-out L160-162
  - Thêm button sau "Lập hợp đồng" (giống pattern `purchase_invoice/of_supplier.blade.php` L193-195):
    ```html
    <button ng-click="createAdditionalContract()" class="btn btn-primary" ng-if="form.supplier_id">
        Lập phụ lục bổ sung
    </button>
    ```
  - Thêm function JS sau `$scope.createContract` (~L398):
    ```js
    $scope.createAdditionalContract = function () {
        let annexType = '{{ $type }}' === 'firm' ? 4 : 5;
        let href = `/admin/orders/inland_buy_contract_new/create?` + $scope.stringParams.replace(/^type=[^&]*&?/, '') + `&type=${annexType}`;
        window.location.href = href;
    }
    ```
  - Lưu ý: `$scope.stringParams` đã có `type={{ $type }}&...` (firm/free filter param), cần strip cũ rồi thêm `type=4/5` mới để không conflict.

## Phase 7: Manual test

- [x] Task 12: Test 6 case (báo lại sau khi test xong):
  1. Vào `inland_purchase_invoice/ofSupplier?type=firm` → chọn supplier → click "Lập phụ lục bổ sung" → URL chuyển sang `inland_buy_contract_new/create?type=4&...`. Title hiển thị "Phụ lục hợp đồng mua hàng theo hãng". Field "Hợp đồng" + button search hiện ra.
  2. Click search "Hợp đồng" → modal hiện list HĐ firm + đơn HĐNT của supplier (KHÔNG phải foreign). Chọn 1 → auto fill `parent_code` + `code = parent_code-PL`.
  3. Lưu phụ lục → DB `inland_buy_contract_news.type=4`, `parent_id` = HĐ gốc. Thoát save thành công.
  4. Tương tự với `?type=free` → tạo `type=5` với parent từ list HĐ free.
  5. Tạo phụ lục cho HĐ gốc đã huỷ (`status=DA_HUY`) → reject "Hợp đồng gốc đã hủy. Không thể tạo phụ lục bổ sung!"
  6. Kiểm action button "Báo hàng về" trên list HĐ với phụ lục type=4 → URL có `type=firm`; với phụ lục type=5 → URL có `type=free`.

## Checkpoint
### Checkpoint — 2026-04-28
Vừa hoàn thành: 11/11 task code (5 BE + 6 FE). Tất cả file PHP pass `php -l`.

**Backend (2 file modified):**
- `app/Model/Order/InlandBuyContractNew.php` — constants `PHU_LUC_HANG=4` + `PHU_LUC_TU_DO=5` (rename `PL=4` cũ), searchByFilter mở rộng firm/free filter include phụ lục
- `app/Http/Controllers/Order/InlandBuyContractNewController.php` — searchData L113 báo hàng về include type=4, store/update validate `parent_id required` cho type IN [4,5] + check parent.status != DA_HUY

**Frontend (5 file modified):**
- `resources/views/orders/inland_buy_contract_new/create.blade.php` — title type=4 firm + thêm type=5 free
- `resources/views/orders/inland_buy_contract_new/edit.blade.php` — title type=4 firm + thêm type=5 free
- `resources/views/orders/inland_buy_contract_new/show.blade.php` — title type=4 firm + thêm type=5 free
- `resources/views/orders/inland_buy_contract_new/form.blade.php` — ng-if mở rộng `type==4||type==5`, đổi `buyContract2Search` → `inlandBuyContractSearch`
- `resources/views/partials/classes/order/InlandBuyContractNew.blade.php` — xoá `buyContract2Search`/`addBuyContract2`, thêm `inlandBuyContractSearch`/`addInlandBuyContract` (đúng URL inland)
- `resources/views/orders/inland_purchase_invoice/of_supplier.blade.php` — wire button "Lập phụ lục bổ sung" + thêm `createAdditionalContract()` JS function (annexType = 4 nếu firm, 5 nếu free)

Đang làm dở: chờ user manual test 6 case.
Bước tiếp theo: User test → báo lại.
Blocked: không.

### Checkpoint — 2026-04-29
Vừa hoàn thành: ✅ Toàn bộ 6 case manual test pass. Đóng feature.
Đang làm dở: không
Bước tiếp theo: không
Blocked: không
