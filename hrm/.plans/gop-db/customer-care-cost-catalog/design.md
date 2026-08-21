# Danh mục dịch vụ sửa chữa và chi phí khác — chuyển ERP sang HRM

> Nhánh: `gop_db` · Phụ trách: @junfoke · Bắt đầu 2026-08-03 · **Đang khảo sát, chờ chốt phạm vi**
> Nền tảng bắt buộc đọc trước: `.plans/gop-db/design.md`

## Mục tiêu

Chuyển màn ERP `admin/accounting/costs?kind_of=2` sang HRM, phân hệ **CSKH** → nhóm
**"Danh mục - Dịch vụ"** (cùng chỗ 2 màn bảo dưỡng vừa chuyển, xem
`components/subsystem-menu/customer-care.js`).

## Hiện trạng ERP

| | |
|---|---|
| Route | `admin/accounting/costs` — `index`, `store`, `update/{id}`, `{id}/delete`, `searchData`, `{id}/getData` |
| Controller | `Accounting\CostsController` (297 dòng) |
| Model | `App\Model\Accounting\Cost` — bảng `costs`, extends **`BaseModel`** |
| View | 1 file `accounting/costs/index.blade.php` |
| Bảng | `costs` — **587 dòng**: `kind_of=2` **524**, `kind_of=1` 57, `kind_of=0` 6 |
| Quyền ERP | **CÓ gate**: `checkPermission:Quản lý chi phí` (khác 3 màn đã chuyển — đều không gate) |

### Cột & trường

`id, name, en_name, type, status, created_by, updated_by, kind_of, rate_value_capital,
revenue_calculation, vat_percent`

Trường phụ thuộc `kind_of`:

| Trường | kind_of = 1 (chi phí phải trả) | kind_of = 2 (dịch vụ SC & chi phí khác) |
|---|---|---|
| `type` | bắt buộc, 8 loại (Quốc tế / Nội địa / NCC quốc tế / Báo giá DV / Lắp đặt / Dự án / Bán hàng / Giá hàng hóa) | luôn `null` |
| `en_name` (Tên tiếng Anh) | có nhập (ERP hiện field + cột + ô tìm) | **KHÔNG dùng** — ERP `ng-if="kind_of==1"`, màn này không hiện. Giữ `null`. |
| `rate_value_capital` | `null` | **bắt buộc**, số ≥ 0 (tỷ lệ giá vốn %) |
| `revenue_calculation` | `null` | 1 = Dịch vụ có tính doanh thu / 0 = Chi phí khác |
| `vat_percent` | bắt buộc ≤ 100 | bắt buộc ≤ 100 |

## ⚠️ 4 điểm khiến màn này KHÁC HẲN 3 màn đã chuyển

### 1. Một màn ERP phục vụ 3 mục menu

`cost.index` được gọi từ 3 chỗ với query khác nhau:

- `?kind_of=2` → **"Danh mục dịch vụ sửa chữa và chi phí khác"** ← màn user yêu cầu
- `?kind_of=1` → "Danh mục chi phí phải trả" (menu Kế toán)
- `?kind_of=1` → "Danh mục chi phí bán hàng" (menu Kinh doanh) — **trùng y hệt mục trên**

Blade bật/tắt cột và trường form bằng `ng-if="editing.kind_of == 1"`. Chuyển riêng `kind_of=2`
thì phần `kind_of=1` vẫn nằm bên ERP → 1 bảng dữ liệu bị quản lý ở 2 cổng.

### 2. `discount` là dữ liệu THEO CÔNG TY, nằm ở bảng khác

Cột "Chiết khấu" trên danh sách **không thuộc `costs`** mà lấy từ `company_costs`
(`company_id`, `cost_id`, `discount`) qua accessor:

```php
CompanyCost::where(['company_id' => Auth::user()->info->company_id, 'cost_id' => $this->id])
```

→ **cùng 1 dịch vụ, mỗi công ty thấy một mức chiết khấu khác nhau**. Bảng đang có 424 dòng,
trải trên 2 công ty (company_id 1: 305 dòng, company_id 4: 119 dòng).
Đây là màn đầu tiên trong nhóm port có dữ liệu phân theo công ty → phải chốt lấy `company_id`
từ đâu ở HRM (JWT có claim `current_company`).

### 3. Model `Cost` có ĐỒNG BỘ CRM ở tầng save

`Cost::save()` và hook `updating` đẩy dữ liệu sang CRM ngoài (`product.template` qua
`CRMProductTemplateService`) và ghi bảng `module_mappings`, bật/tắt bằng
`config('services.mate.use_crm')` = `env('MATE_API_USE_CRM')`.

- Local đang **`false`** → không chạy.
- Nếu production bật `true` mà HRM ghi thẳng `costs` bằng model riêng (như 3 màn trước) thì
  **CRM sẽ không được đồng bộ** → lệch dữ liệu âm thầm.

Ghi chú: hook này còn có bug sẵn — dùng `$this->` bên trong closure `static::updating(function ($cost)…)`
(dòng `categ_id => $this->getCompareId(...)`), gọi trúng nhánh đó là fatal error.

### 4. Trùng việc với feature `erp-cost-catalog` của @dnsnamdang

`.plans/erp-cost-catalog/` (nhánh **`tpe-develop-assign`**, trạng thái CODE DONE) đang **đọc và
ghi thẳng bảng `costs`** cho luồng BOM / Báo giá: lọc `status=1 AND kind_of=2`, quick-create ghi
mới, và `syncServiceCostRatesToErp()` ghi ngược `rate_value_capital`. Feature đó đi qua
connection **`mysql2`** (DB ERP cũ) — trái ràng buộc của nhánh `gop_db`.

→ **Cần thống nhất với @dnsnamdang trước khi làm**, nếu không sẽ có 2 đường ghi vào cùng 1 bảng
bằng 2 connection khác nhau.

## Nghiệp vụ khác cần giữ

- `canEdit()` / `canDelete()`: **chặn cứng theo TÊN** — `['Chi phí đi lại', 'Chi phí vận chuyển']`
  không cho sửa/xóa. `canDelete()` còn đòi `status == 1`.
- `delete()` thực chất là **"khóa hoặc xóa"**: nếu `cost_id` đã dùng ở `firm_quotation_costs`
  hoặc `firm_contract_costs` → chỉ set `status = 0` (Khóa); nếu chưa → xóa hẳn + dọn `company_costs`.
- Bộ lọc: `name`, `updated_by` (gộp cả created_by khi updated_by null),
  `status`, `revenue_calculation`. (KHÔNG lọc `en_name` — chỉ thuộc kind_of=1.)
- Sắp xếp theo cột `discount` phải join động `company_costs` theo company của user (ERP làm bằng
  raw subquery + addBinding).

## Quyết định (user chốt 2026-08-03)

| # | Nội dung | Chốt |
|---|---|---|
| 1 | Phạm vi | **Làm cả 2 loại** — 1 component dùng chung, bật/tắt cột + trường theo `kind_of` như ERP |
| 2 | Đồng bộ CRM | **Bỏ qua** — user cho biết phần CRM đã bỏ, HRM chỉ ghi DB |
| 3 | Chiết khấu | Theo **công ty đang chọn trên HRM** (claim `current_company` trong JWT) |

## 2 hệ quả phải xử lý (phát sinh từ quyết định 1)

### A. Mỗi link chỉ được thuộc ĐÚNG 1 phân hệ → phải tách 2 đường dẫn

`resolveSubsystem()` bỏ query string khi so khớp (`normalizePath`), nên **không thể** dùng chung
`/finance/costs?kind_of=1` và `?kind_of=2` cho 2 phân hệ khác nhau — sẽ khớp sai phân hệ
(xem [[project_subsystem_registry_fe]]).

→ Tách 2 route, **dùng chung 1 component**, khác nhau ở prop `kindOf`:

| Đường dẫn | `kind_of` | Phân hệ / menu |
|---|---|---|
| `/customer-care/costs` | 2 | CSKH → Danh mục - Dịch vụ → "Danh mục dịch vụ sửa chữa và chi phí khác" |
| `/finance/payable-costs` | 1 | Tài chính → Danh mục → "Danh mục chi phí phải trả" |

### B. 2 trong 3 mục menu ERP KHÔNG có trong sheet gộp

Rà `components/subsystem-menu/*.js`: chỉ có **"Danh mục dịch vụ sửa chữa và chi phí khác"**
(customer-care.js). Hai mục **"Danh mục chi phí phải trả"** (ERP menu Kế toán) và
**"Danh mục chi phí bán hàng"** (ERP menu Kinh doanh) không được sheet đưa sang.

Xử lý theo tiền lệ Phase 7 của `bo-sung-menu-phan-he` (màn ERP nằm ở menu Kế toán thì về phân hệ
Tài chính): thêm mục **"Danh mục chi phí phải trả"** vào menu Tài chính.

⚠️ Mục **"Danh mục chi phí bán hàng"** bên ERP trỏ **cùng `kind_of=1`, cùng dữ liệu** với mục trên
— chỉ là 2 lối vào 1 màn. Không tạo màn thứ 3; để nguyên mục xám mờ ở menu Bán hàng.
**Cần user xác nhận** có muốn bỏ hẳn mục trùng này khỏi menu Bán hàng không.

## Còn nợ — phối hợp với `erp-cost-catalog` (@dnsnamdang)

Feature đó (nhánh `tpe-develop-assign`) đọc/ghi cùng bảng `costs` qua `mysql2`. Không chặn việc
port màn danh mục này, nhưng khi 2 nhánh gặp nhau sẽ có 2 đường ghi bằng 2 connection khác nhau —
**cần thống nhất trước khi merge**.
