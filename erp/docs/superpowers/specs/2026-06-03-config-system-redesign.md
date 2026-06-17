# Cấu hình hệ thống — Redesign Spec

## Tổng quan

Chỉnh sửa trang Cấu hình hệ thống (`admin/configs/edit`) từ form đơn lẻ thành giao diện 7 tabs, mỗi tab lưu độc lập. Thêm tính năng lịch sử chỉnh sửa và "Loại hàng hóa không hiển thị trên các phiếu". Bỏ các field không dùng nữa.

## Scope

### Bỏ khỏi UI (giữ column trong DB, không xóa)
- Hoa hồng âm tối đa (`min_commission`)
- Thuế TNCN tạm tính (`tndn`)
- Thuế TNCN (`tncn`)
- Thuế Doanh số vượt trội (`vat_extra_cost`)
- Hệ số tính giá vốn dịch vụ (`coefficient_cost_price_service`)
- Hàng cập nhật giá (`is_company_price`, `is_all_brand`, `brand_ids`, `is_new_company`, `is_new_brand`, `new_brand_ids`)
- Điều khoản báo giá mặc định (`quotation_footer`)
- Điều khoản báo giá dịch vụ mặc định (`service_quotation_footer`)

### Tính năng mới
1. UI tabs (7 tabs), mỗi tab lưu độc lập
2. Loại hàng hóa không hiển thị trên các phiếu (Tab 2)
3. Lịch sử chỉnh sửa cấu hình (modal per tab)

---

## Database

### Bảng mới: `config_hidden_product_types`

| Column | Type | Mô tả |
|---|---|---|
| id | bigint, PK, AI | |
| config_id | bigint unsigned, FK → configs.id | |
| product_types | text | JSON array — mảng ID loại hàng hóa đã chọn |
| ticket_types | text | JSON array — mảng key loại phiếu đã chọn |
| created_at | timestamp | |
| updated_at | timestamp | |

### Bảng mới: `config_histories`

| Column | Type | Mô tả |
|---|---|---|
| id | bigint, PK, AI | |
| config_id | bigint unsigned, FK → configs.id | |
| tab | varchar(50) | `general`, `category`, `business`, `warehouse`, `xnk`, `accounting`, `cskh` |
| field_name | varchar(255) | Tên trường hiển thị tiếng Việt |
| old_value | text, nullable | Giá trị trước khi sửa |
| new_value | text, nullable | Giá trị sau khi sửa |
| updated_by | bigint unsigned, FK → users.id | Người cập nhật |
| created_at | timestamp | |
| updated_at | timestamp | |

### Bảng `configs` — không thay đổi schema

---

## Backend

### Routes

Trong group `configs` hiện tại (middleware `checkPermission:Cấu hình hệ thống`):

```
GET  /admin/configs/edit                  → ConfigsController@edit        (sửa lại)
POST /admin/configs/update/{tab}          → ConfigsController@updateTab   (mới)
GET  /admin/configs/histories/{tab}       → ConfigsController@histories   (mới)
```

Route `POST /admin/configs` cũ (`ConfigsController@update`) — giữ lại tạm hoặc xóa sau khi chuyển xong.

### Controller: `ConfigsController`

#### Constants

```php
const TAB_FIELDS = [
    'general'    => ['logo', 'title', 'description'],
    'category'   => ['product_types'],
    'business'   => [
        'max_borrow_date', 'max_prepick_date', 'consignment_holding_time',
        'max_prepick_date_project_contract', 'warning_day',
        'customer_is_following', 'customer_taken_care',
        'quotation_valid_days', 'project_quotation_valid_days',
        'customer_register_expiry', 'customer_groups', 'department_groups',
        'is_equipment', 'is_repair', 'is_project', 'is_principle', 'is_dental_principle',
    ],
    'warehouse'  => ['vat_delivery_trip_percent'],
    'xnk'       => ['environment_tax'],
    'accounting' => ['coefficient_ecommerce_price', 'debt_calculation_date'],
    'cskh'      => ['serial_product_types'],
];

const TICKET_TYPES = [
    'yeu_cau_hoi_gia'        => 'Phiếu Yêu cầu hỏi giá',
    'yeu_cau_dat_hang_ngoai' => 'Phiếu Yêu cầu đặt hàng mua ngoài',
    'yeu_cau_dat_hang'       => 'Phiếu Yêu cầu đặt hàng',
    'bao_gia_vt_hh_tb'      => 'Báo giá vật tư- hàng hóa - thiết bị',
    'bao_gia_dv_sc_bd_bt'   => 'Báo giá dịch vụ sửa chữa - bảo dưỡng - bảo trì',
    'bao_gia_hd_nguyen_tac' => 'Báo giá hợp đồng nguyên tắc',
    'bao_gia_du_an'         => 'Báo giá dự án',
    'yeu_cau_sc_bd'         => 'Phiếu yêu cầu sửa chữa - bảo dưỡng',
];

const FIELD_LABELS = [
    'logo' => 'Logo',
    'title' => 'Tiêu đề',
    'description' => 'Mô tả',
    'product_types' => 'Tính chất hàng hóa',
    'max_borrow_date' => 'Số ngày mượn tối đa',
    'max_prepick_date' => 'Số ngày giữ tối đa',
    'consignment_holding_time' => 'Số ngày giữ tối đa của hàng gửi',
    'max_prepick_date_project_contract' => 'Số ngày giữ tối đa - HĐDA',
    'warning_day' => 'Số ngày cảnh báo (mượn/giữ hàng)',
    'customer_is_following' => 'Khách hàng đang theo dõi',
    'customer_taken_care' => 'Khách hàng được chăm sóc',
    'quotation_valid_days' => 'Số ngày hiệu lực báo giá',
    'project_quotation_valid_days' => 'Số ngày hiệu lực báo giá dự án',
    'customer_register_expiry' => 'Thời gian đăng ký khách hàng',
    'customer_groups' => 'Nhóm khách hàng không ràng buộc HĐ thị trường',
    'department_groups' => 'Phòng ban không ràng buộc thị trường',
    'is_equipment' => 'Ràng buộc HĐ bán hàng',
    'is_repair' => 'Ràng buộc HĐ dịch vụ',
    'is_project' => 'Ràng buộc HĐ dự án',
    'is_principle' => 'Ràng buộc HĐ nguyên tắc',
    'is_dental_principle' => 'Ràng buộc HĐ nguyên tắc nha khoa',
    'vat_delivery_trip_percent' => 'Thuế vận tải',
    'environment_tax' => 'Hệ số thuế bảo vệ môi trường',
    'coefficient_ecommerce_price' => 'Hệ số giá thương mại điện tử',
    'debt_calculation_date' => 'Ngày khai báo công nợ đầu kỳ',
    'serial_product_types' => 'Hàng không bắt buộc Serial',
];
```

#### Method `edit()`

Load data cho view:
- `$config` — `Config::with('contractRows', 'hiddenProductTypes')->first()`
- `$hiddenProductTypes` — từ relation
- `$ticketTypes` — constant `TICKET_TYPES`
- `$productCategories` — `Product\Category::all()` (DM loại hàng hóa, dùng cho Tab 2 bảng ẩn HH)
- `$provinces`, `$customerGroups`, `$departmentGroups`, `$groups`, `$productTypes` (giữ nguyên như hiện tại)

#### Method `updateTab(Request $request, string $tab)`

1. Validate `$tab` nằm trong danh sách hợp lệ
2. Lấy danh sách field từ `TAB_FIELDS[$tab]`
3. Build validation rules chỉ cho field của tab đó
4. Load config hiện tại, so sánh old vs new cho từng field
5. Ghi `config_histories` cho mỗi field có thay đổi
6. Save config (chỉ các field của tab)
7. Xử lý đặc biệt:
   - Tab `category`: CRUD `config_hidden_product_types` (xóa cũ, tạo mới), ghi history cho thay đổi
   - Tab `cskh`: CRUD `contract_rows` (xóa cũ, tạo mới), ghi history cho thay đổi

#### Method `histories(string $tab)`

```php
$histories = ConfigHistory::where('tab', $tab)
    ->with('updater.info')
    ->orderBy('created_at', 'desc')
    ->get()
    ->map(function($h) {
        return [
            'updater' => $h->updater->info->code . '_' . $h->updater->fullname,
            'field_name' => $h->field_name,
            'old_value' => $h->old_value,
            'new_value' => $h->new_value,
            'created_at' => $h->created_at->format('d/m/Y H:i'),
        ];
    });
return $this->responseSuccess($histories);
```

### Models mới

#### `ConfigHiddenProductType`

```php
class ConfigHiddenProductType extends Model {
    protected $fillable = ['config_id', 'product_types', 'ticket_types'];
    protected $casts = ['product_types' => 'array', 'ticket_types' => 'array'];
    public function config() { return $this->belongsTo(Config::class); }
}
```

#### `ConfigHistory`

```php
class ConfigHistory extends Model {
    protected $fillable = ['config_id', 'tab', 'field_name', 'old_value', 'new_value', 'updated_by'];
    public function updater() { return $this->belongsTo(User::class, 'updated_by'); }
}
```

#### `Config` — thêm relations

```php
public function hiddenProductTypes() { return $this->hasMany(ConfigHiddenProductType::class); }
public function histories() { return $this->hasMany(ConfigHistory::class); }
```

---

## Frontend

### Cấu trúc files

```
resources/views/common/configs/
├── edit.blade.php                  ← Khung chính: nav-tabs + @include partials
├── tabs/
│   ├── general.blade.php           ← Tab 1: Logo, Tiêu đề, Mô tả
│   ├── category.blade.php          ← Tab 2: Tính chất HH + Bảng loại HH ẩn phiếu
│   ├── business.blade.php          ← Tab 3: 13 field kinh doanh
│   ├── warehouse.blade.php         ← Tab 4: Thuế vận tải
│   ├── xnk.blade.php              ← Tab 5: Hệ số thuế BVMT
│   ├── accounting.blade.php        ← Tab 6: Hệ số giá TMĐT + Ngày khai báo CN
│   └── cskh.blade.php             ← Tab 7: Serial + Bảng tính công khoán
└── partials/
    ├── tab_buttons.blade.php       ← Cụm Lưu + Lịch sử + Hủy (nhận param $tab)
    └── history_modal.blade.php     ← Modal lịch sử dùng chung
```

### `edit.blade.php`

- `ng-controller="ConfigController"` bao toàn bộ page
- Bootstrap 4 nav-tabs: 7 tab items
- `tab-content` chứa 7 `tab-pane`, mỗi pane include partial tương ứng
- `@section('script')`: chứa class Config (sửa lại bỏ field không dùng), controller Angular

### Angular Controller

```js
app.controller('ConfigController', function($scope) {
    $scope.config = new Config(@json($config));
    $scope.hiddenProductTypes = @json($hiddenProductTypes);
    $scope.ticketTypes = @json($ticketTypes);
    $scope.loading = {};
    $scope.errors = {};

    // Submit theo tab
    $scope.submitTab = function(tab) {
        $scope.loading[tab] = true;
        let data = $scope.getTabData(tab);
        $.ajax({
            type: 'POST',
            url: '/admin/configs/update/' + tab,
            headers: { 'X-CSRF-TOKEN': CSRF_TOKEN },
            data: data,
            success: function(response) {
                if (response.success) {
                    toastr.success(response.message);
                } else {
                    $scope.errors = response.errors;
                    toastr.warning(response.message);
                }
            },
            error: function() { toastr.error('Đã có lỗi xảy ra'); },
            complete: function() {
                $scope.loading[tab] = false;
                $scope.$applyAsync();
            }
        });
    };

    // getTabData — trả object chỉ chứa field của tab tương ứng
    $scope.getTabData = function(tab) { /* switch theo tab */ };

    // Modal lịch sử
    $scope.showHistory = function(tab) {
        $.get('/admin/configs/histories/' + tab, function(response) {
            $scope.histories = response.data;
            $scope.$applyAsync();
            $('#historyModal').modal('show');
        });
    };

    // Tab 2: Thêm/xóa dòng loại HH ẩn
    $scope.addHiddenRow = function() {
        $scope.hiddenProductTypes.push({ product_types: [], ticket_types: [] });
    };
    $scope.removeHiddenRow = function(index) {
        $scope.hiddenProductTypes.splice(index, 1);
    };

    // Tab 7: Thêm/xóa dòng công khoán (giữ nguyên logic hiện tại)
    $scope.addNewRow = function() { /* giữ nguyên */ };
    $scope.removeRow = function(index) { /* giữ nguyên */ };
});
```

### Tab 2 — Bảng loại HH ẩn phiếu

```html
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Loại hàng hóa (*)</th>
            <th>Loại phiếu (*)</th>
            <th><a ng-click="addHiddenRow()"><i class="fa fa-plus"></i></a></th>
        </tr>
    </thead>
    <tbody>
        <tr ng-repeat="row in hiddenProductTypes track by $index">
            <td>
                <select class="select2 form-control" ng-model="row.product_types" multiple>
                    <option ng-repeat="cat in productCategories" ng-value="cat.id">
                        <% cat.name %>
                    </option>
                </select>
            </td>
            <td>
                <select class="select2 form-control" ng-model="row.ticket_types" multiple>
                    <option ng-repeat="(key, label) in ticketTypes" ng-value="key">
                        <% label %>
                    </option>
                </select>
            </td>
            <td>
                <button ng-click="removeHiddenRow($index)" class="btn btn-link text-danger">
                    <i class="fa fa-minus"></i>
                </button>
            </td>
        </tr>
    </tbody>
</table>
```

### Modal Lịch sử (dùng chung)

```html
<div class="modal" id="historyModal">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5>Lịch sử chỉnh sửa</h5>
                <button data-dismiss="modal">&times;</button>
            </div>
            <div class="modal-body">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Người cập nhật</th>
                            <th>Tên trường sửa</th>
                            <th>Nội dung cũ</th>
                            <th>Nội dung mới</th>
                            <th>Ngày cập nhật</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr ng-repeat="h in histories">
                            <td><% h.updater %></td>
                            <td><% h.field_name %></td>
                            <td><% h.old_value %></td>
                            <td><% h.new_value %></td>
                            <td><% h.created_at %></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" data-dismiss="modal">Đóng</button>
            </div>
        </div>
    </div>
</div>
```

### Cụm button mỗi tab (partial)

```html
<!-- @include('common.configs.partials.tab_buttons', ['tab' => 'general']) -->
<div class="text-right mt-3">
    <button class="btn btn-success" ng-click="submitTab('{{ $tab }}')" ng-disabled="loading.{{ $tab }}">
        <i class="fa fa-save" ng-if="!loading.{{ $tab }}"></i>
        <i class="fa fa-spin fa-spinner" ng-if="loading.{{ $tab }}"></i> Lưu
    </button>
    <button class="btn btn-info" ng-click="showHistory('{{ $tab }}')">
        <i class="fa fa-history"></i> Lịch sử chỉnh sửa
    </button>
    <a href="/" class="btn btn-danger"><i class="fa fa-remove"></i> Hủy</a>
</div>
```
