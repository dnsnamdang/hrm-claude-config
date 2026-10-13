# Khảo sát BE ERP — luồng Tính giá (Hỏi giá → YC tính giá → Phiếu tính giá → Kết quả)

> Khảo sát CHỈ ĐỌC, ngày 10/10/2026.
> Nguồn: worktree `wt-erp-2d1` nhánh `feat/2d1-erp-khong-loi` (HEAD `027fb570a2`, đã có G3 + G6).
> DB: `hrm_erp_giacty` (local, dữ liệu chụp tới khoảng 15/09/2026). Đếm bằng `SELECT COUNT(*)`, không ghi gì.
> Mọi đường dẫn bên dưới tính từ gốc repo ERP, trừ khi ghi rõ.

---

## 0. Tóm tắt nhanh

| Chứng từ | Bảng chính | Mã phiếu | Số dòng (DB) | Controller | Model |
|---|---|---|---|---|---|
| Yêu cầu hỏi giá (YCHG) | `price_asking_requests` | `PYCHG-xxxxx` | 4.029 | `app/Http/Controllers/Order/PriceAskingRequestController.php` | `app/Model/Order/PriceAskingRequest.php` |
| Yêu cầu tính giá (YCTG) | `price_calculate_requests` | `PYCTG-xxxxx` | 3.147 | `.../PriceCalculateRequestController.php` | `app/Model/Order/PriceCalculateRequest.php` |
| Phiếu tính giá (PTG) | `price_calculates` | `PTG-xxxxx` | 3.120 | `.../PriceCalculateController.php` | `app/Model/Order/PriceCalculate.php` |
| Kết quả tính giá (KQ) | `price_calculate_results` | (không có mã, không có cột `code`) | 3.119 | `.../PriceCalculateResultController.php` | `app/Model/Order/PriceCalculateResult.php` |

- Quan hệ thực tế đều là **1–1–1–1**: không YCHG nào có quá 1 YCTG, không YCTG nào có quá 1 PTG (đã đếm, đều bằng 0).
- Khối lượng: 38 YCHG trong 30 ngày gần nhất. Dữ liệu sống bắt đầu từ 01/2026 (có 73 YCHG cũ từ 2024).
- **Không có service, job, observer, event hay queue riêng** cho luồng này. Toàn bộ logic nằm trong 4 model + 4 controller. Công thức tính giá nằm ở **FE (AngularJS class trong Blade)**. BE chỉ lưu con số FE gửi lên, không tính lại.
- Các phần phụ thuộc bên ngoài: `DocumentCompany` (G3), `ProductUnitPrice`, `ProductExpectedPrice`, `ProductCompanyUnit` (G3), `ProductVersion`/`ProductHistory`, `ProductApprove`/`ProductApprovePrice`, `AssignHistory` (phân công mua hàng), `Notification`/`NotificationHelper`, `ReportTemplate` (in).

---

## 1. Danh sách route

Cả 4 nhóm nằm trong `routes/web.php`, thuộc group `prefix=admin`, middleware `['sso.check','userLogin','PreventDuplicateSubmission']` (`routes/web.php:64`), và group con `prefix=orders` (`routes/web.php:2114`). URL đầy đủ có dạng `/admin/orders/...`.

**Gần như không route nào gắn `checkPermission`.** Quyền được kiểm trong model (`canXxx()`), chỉ 2 route có middleware riêng. **Chưa route nào gắn `productMovedToHrm`** (G6 mới chặn màn giá ở `products.*`).

### 1.1 YCHG — `price_asking_requests` (`routes/web.php:2246-2262`)

| Method | URL | Action | Kiểm quyền thực tế (trong code) |
|---|---|---|---|
| GET | `/` | `index` (`?type=index\|approve\|xnk_approve\|calculate`) | lọc ở `searchByFilter` |
| GET | `/create` | `create` | **không kiểm** |
| GET | `/{id}/edit` | `edit` | `canEdit()`: trạng thái 3/6/8/9 và là người tạo |
| GET | `/{id}/delete` | `delete` | `canDelete()` (giống canEdit) |
| GET | `/{id}/show` | `show` | `canView()` → **luôn `true`** (`PriceAskingRequest.php:457-484`, đoạn kiểm đã bị comment) |
| GET | `/{id}/print` | `print` | `canView()` → luôn true |
| POST | `/{id}/update` | `update` | `canEdit()` |
| POST | `/store` | `store` | **không kiểm quyền** |
| POST | `/{id}/approve` | `approve` (PTKD duyệt) | `canApprove()`: st=2 + `canInCompany('PTKD duyệt yêu cầu hỏi giá')` + trong phạm vi xem |
| POST | `/{id}/reject` | `reject` (PTKD không duyệt) | `canReject()` (giống trên) |
| POST | `/{id}/approveXNK` | `approveXNK` | `canXNKApprove()`: st=5 + là người mua được phân công (`isAssignedBuyer`) + `canInCompany('XNK duyệt yêu cầu hỏi giá')` |
| POST | `/{id}/rejectXNK` | `rejectXNK` | `canXNKReject()` (giống trên) |
| POST | `/{id}/cancelApprove` | `cancelApprove` | `canCancelApprove()`: st=1 + quyền XNK + là người mua được phân công + chưa có YCTG |
| GET | `/searchData` | `searchData` (DataTables) | xem 1.5 |
| GET | `/{id}/getDataForPriceCalculate` | `getDataForPriceCalculate` | `canCalculate()`: st=1 + chưa có YCTG + `canInCompany('Lập yêu cầu tính giá')` |

Route phụ trợ ngoài nhóm: `GET /admin/products/{id}/getDataForPriceAsking` → `ProductsController@getDataForPriceAsking` (`routes/web.php:600`, `ProductsController.php:3371-3376`). Route này dùng khi thêm hàng vào YCHG, trả `dataFor(công ty)` và cảnh báo "Hàng này đã có người hỏi giá".

### 1.2 YCTG — `price_calculate_requests` (`routes/web.php:2264-2276`)

| Method | URL | Action | Kiểm quyền |
|---|---|---|---|
| GET | `/` | `index` (`?type=index\|approve\|calculate`) | lọc ở `searchByFilter` |
| GET | `/create` | `create` | middleware `checkPermission:Lập yêu cầu tính giá` |
| GET | `/{id}/edit` | `edit` | middleware `checkPermission:Lập yêu cầu tính giá` + `canEdit()` (st=3, người tạo) |
| GET | `/{id}/delete` | `delete` | `canDelete()` (st=3, người tạo, có quyền lập). Xoá xong **trả YCHG về st=1** (`PriceCalculateRequest.php:318-330`) |
| GET | `/{id}/show` | `show` | `canView()` theo 4 cấp phạm vi, hoặc quyền `Kế toán mua hàng` |
| GET | `/{id}/print` | `print` | `canView()` |
| POST | `/{id}/update` | `update` | `canEdit()` |
| POST | `/store` | `store` | YCHG `canCalculate()` + `can('Lập yêu cầu tính giá')` |
| POST | `/{id}/reject` | `reject` | `canReject()`: st=2 + `Kế toán mua hàng` |
| GET | `/searchData` | `searchData` | |
| GET | `/{id}/getDataForPriceCalculate` | `getDataForPriceCalculate` | `canApprove()`: st=2 + chưa có PTG + `Kế toán mua hàng` |

YCTG **không có route approve riêng**. Lập PTG sẽ gọi `$req->approve()` (xem 3.2).

### 1.3 PTG — `price_calculates` (`routes/web.php:2278-2288`)

| Method | URL | Action | Kiểm quyền |
|---|---|---|---|
| GET | `/` | `index` (`?type=all` hoặc của tôi) | |
| GET | `/create` | `create` | **không kiểm** (kiểm lúc chọn YCTG) |
| GET | `/{id}/edit` | `edit` | `canEdit()`: st=3 + người tạo |
| GET | `/{id}/delete` | `delete` | ⚠️ **KHÔNG kiểm gì**: `PriceCalculateController.php:250-254` gọi thẳng `removeFromDB()`. `canDelete()` trả `false` nhưng không được gọi. Bất kỳ ai đăng nhập cũng xoá được PTG đã duyệt bằng một lệnh GET |
| GET | `/{id}/show` | `show` | `canView()`: Super Admin / người tạo / `Kế toán mua hàng` / 4 cấp phạm vi "Xem DS tính giá bán theo …" |
| GET | `/{id}/print` | `print` | `canView()`. ⚠️ In **hỏng**: template id 100 (`ReportTemplate::TINH_GIA`) **không có trong DB**, nên `firstOrFail` trả 404. Accessor `result_table` cũng không tồn tại (`PriceCalculate.php:824`). Nút In trên list đã bị comment |
| POST | `/{id}/update` | `update` | `canEdit()` |
| POST | `/store` | `store` | YCTG `canApprove()` (cần quyền `Kế toán mua hàng`) |
| GET | `/searchData` | `searchData` | |

### 1.4 KQ — `price_calculate_results` (`routes/web.php:2290-2295`)

| Method | URL | Action | Kiểm quyền |
|---|---|---|---|
| GET | `/` | `index` | |
| GET | `/{id}/show` | `show` | `canView()` → **luôn `true`** (`PriceCalculateResult.php:147-152`) |
| GET | `/{id}/print` | `print` | ⚠️ **Controller không có method `print`** nên lỗi 500. `ReportTemplate::KET_QUA_TINH_GIA` cũng không được khai báo |
| GET | `/searchData` | `searchData` | `type=all` thì **không lọc gì**, thấy toàn bộ KQ của mọi công ty (`PriceCalculateResult.php:54-58`) |

### 1.5 Quyền dùng trong luồng (đều có trong bảng `permissions` của DB gộp)

- YCHG: `PTKD duyệt yêu cầu hỏi giá`, `XNK duyệt yêu cầu hỏi giá`, `Lập yêu cầu tính giá`, `Tính giá bán`. Phạm vi xem (`VIEW_SCOPE_PERMISSIONS`, `PriceAskingRequest.php:88-93`): `Xem danh sách yêu cầu hỏi giá theo tổng công ty` / `Xem DS yêu cầu hỏi giá theo công ty` / `… theo phòng ban` / `… theo bộ phận`. Phạm vi tính (`CALCULATE_SCOPE_PERMISSIONS`, `:96-101`): `Xem DS tính giá bán theo tổng công ty/công ty/phòng ban/bộ phận`. Kiểm bằng `canInCompany` (theo công ty đang đăng nhập).
- YCTG: `Lập yêu cầu tính giá`, `Kế toán mua hàng` (duyệt/tính), `Xem DS yêu cầu tính giá bán theo tổng công ty/công ty/phòng ban/bộ phận`. Kiểm bằng `can()` (không theo công ty), không thống nhất với YCHG.
- PTG: `Kế toán mua hàng`, `Xem DS tính giá bán theo …`.
- Sau khi duyệt PTG (nhánh cần duyệt): thông báo tới người có `Duyệt giá hàng hoá` của công ty bộ giá.
- ⚠️ Có bypass Super Admin ở nhiều chỗ: `Employee::canInCompany` (`app/Employee.php:1473`), `isAssignedBuyer` (`PriceAskingRequest.php:515`), `PriceCalculateRequest::canView` (`:341`), `PriceCalculate::canView` (`:293`). Port sang HRM phải bỏ, theo quy tắc "Super admin không mặc định có quyền".
- Phạm vi "phòng ban" của YCHG dùng `EmployeeManageDepartment` (các phòng NV quản lý, `PriceAskingRequest.php:145-152`). YCTG và PTG lại dùng `department_id` của chính NV. Hai cách khác nhau.

---

## 2. Bảng DB, cột chính, quan hệ, số dòng

> Đã `SHOW TABLES LIKE '%price_ca%' / '%price_ask%' / '%expected%' / 'product_approve%'`. Toàn bộ tên bảng đều ở dạng số nhiều.

### 2.1 Bảng của luồng (15 bảng)

| Bảng | Số dòng | Cột chính | Quan hệ |
|---|---|---|---|
| `price_asking_requests` | 4.029 | code, note, comment (ghi chú PTKD), approver_comment (ghi chú XNK), cancel_reason, approver_id, approved_time, xnk_approver_id, xnk_approved_time, received_time, status, **company_id/department_id/part_id** (của người lập, gán ở `boot::creating` `:154-162`), brand_id, manufacture_id, **send_company_id** (công ty nhận hỏi giá = `manufactures.company_id`, FE gán), created_by | 1-n `price_asking_request_products.parent_id`; 1-n `price_asking_request_approve_histories` |
| `price_asking_request_products` | 6.729 | parent_id, product_id, product_name, code, unit_id, unit_name | (không có SL, không có giá) |
| `price_asking_request_approve_histories` | 19.304 | price_asking_request_id, created_by, type (chuỗi tiếng Việt, 8 loại), note | log tiến trình (xem 3.1) |
| `price_calculate_requests` | 3.147 | code, currency (**id của `currencies`**, không phải chữ), exchange_rate, note, comment, price_asking_request_id, approver_id, approved_time, status, company_id/department_id/part_id (**chép từ YCHG**, không lấy của người lập YCTG, `Controller:143-145`), brand_id, manufacture_id | n-1 YCHG; 1-n `price_calculate_request_products` |
| `price_calculate_request_products` | 5.342 | parent_id, product_id, unit_id, supplier_price, supplier_price_exchange, import_tax, amount_exchange_after_tax, chosen | 1-n `price_calculate_request_product_costs.parent_id` |
| `price_calculate_request_product_costs` | 5.077 | parent_id, price_calculate_request_id, cost_id (→`costs`), cost_name, rate (%), value (ngoại tệ), value_exchange (VNĐ) | |
| `price_calculates` | 3.120 | code, currency, exchange_rate, note, price_calculate_request_id, status, company_id/department_id/part_id (**chép từ YCTG, tức từ YCHG**), brand_id, manufacture_id | n-1 YCTG; 1-n `price_calculate_products` |
| `price_calculate_products` | 4.908 | parent_id, product_id, unit_id, supplier_price, import_tax, supplier_price_exchange, amount_exchange_after_tax, other_cost, **cost_price** (giá nhập kho, FE tính), chosen, note | 1-n costs, 1-n prices |
| `price_calculate_product_costs` | 4.789 | parent_id, price_calculate_id, cost_id, cost_name, rate, value, value_exchange | |
| `price_calculate_product_prices` | 27.874 | parent_id, price_calculate_id, price_type_id (1–6), price, coefficient decimal(5,2), sale_max_percent, price_calculate_request_product_id, price_asking_request_product_id | 1-n expected_prices |
| `price_calculate_product_expected_prices` | 4.192 | parent_id, price_calculate_id, price, coefficient, sale_max_percent, effect_date | |
| `price_calculate_results` | 3.119 | price_asking_request_id, price_calculate_request_id, price_calculate_id, requester_id (= người lập YCHG), created_by | 1-n result_products |
| `price_calculate_result_products` | 4.906 | parent_id, product_id, product_name, code, unit_id, unit_name | 1-n result_product_prices |
| `price_calculate_result_product_prices` | 27.863 | parent_id, price_type_id, price, coefficient, sale_max_percent | 1-n result_product_expected_prices |
| `price_calculate_result_product_expected_prices` | 4.191 | parent_id, price, coefficient, sale_max_percent, effect_date | |

**Nhận xét:** KQ là **bản chép đơn giản** của phần giá bán trong PTG (chỉ các dòng `chosen`, không có giá vốn hay chi phí). Không bảng nào trong luồng có `deleted_at` (xoá cứng).

### 2.2 Bảng ngoài luồng bị đọc/ghi

| Bảng | Số dòng | Vai trò |
|---|---|---|
| `product_unit_prices` | 789.765 (cty1: 270.095, cty2: 173.082, cty3: 173.082, cty4: 173.506) | **PTG ghi** giá bán 6 loại. Có `company_id` (G3) |
| `product_expected_prices` | 101.290 | **PTG ghi** giá hiệu lực tương lai. ⚠️ **KHÔNG có cột `company_id`**: công ty suy ra qua `unit_price_id → product_unit_prices.company_id`. status: 2 = chờ hiệu lực, 1 = đã áp dụng (cron `product:update_price` 01:00, `app/Console/Commands/UpdateProductPrice.php`). flag=1 = chờ duyệt (cron bỏ qua) |
| `product_company_units` | 133.101 | **PTG ghi** giá vốn `cost_price` (G3, thay 13 cột cũ ở `product_units`) |
| `product_versions` / `product_histories` | 113.768 / … | **PTG ghi** phiên bản + lịch sử. `product_versions` không có `company_id` |
| `products` | — | **PTG ghi `products.note`** (`PriceCalculate.php:364-370`) |
| `product_approves` / `product_approve_prices` | **0 / 0** | PTG ghi khi công ty bật "quy chế giá công ty". Hiện **không công ty nào bật** (`companies.is_company_price = 0` cả 8 công ty), nên nhánh duyệt chưa từng chạy trên dữ liệu này |
| `costs` (type=8 `GIA_HANG_HOA`) | 616 (tổng) | danh mục chi phí |
| `manufacture_costs` | **0** | chi phí mặc định theo hãng (YCTG tự nạp). Rỗng nên tính năng này đang chết |
| `currencies` | 11 | currency + exchange_rate mặc định (FE nạp tỉ giá khi chọn tiền tệ) |
| `assign_histories` (model `AssignHistory`) | — | phân công mua hàng (hãng × thương hiệu × công ty → `buy_employee_id`). Quyết định ai là "XNK duyệt" |
| `report_templates` | id 98 (YC hỏi giá), 99 (YC tính giá) có. **100 (Tính giá) không có** | in ấn |
| `notifications` | — | thông báo chuông (adapter `app/Model/Common/Notification.php` ghi xuống schema Laravel của DB gộp). Không có thông báo cũ nào trỏ tới URL luồng này |

### 2.3 Phân bố dữ liệu đáng chú ý

- `price_asking_requests.company_id × send_company_id`: (1,1)=2.839, (4,1)=931, (3,1)=184, (4,4)=20, (8,1)=12, (1,2)=11, (2,1)=4, … và **18 dòng `send_company_id` NULL**. Phần lớn là các công ty hỏi công ty 1 (Tân Phát HN).
- PTG theo công ty phiếu: cty1=2.286, cty4=674, cty3=147, cty8=11, cty2=2.
- **Công ty phiếu PTG khác công ty quản lý hàng** (`products.company_id`) trên các dòng chosen: (phiếu 4, hàng 1)=1.186, (3,1)=158, (8,1)=14, (2,1)=2, (1,4)=4, (3,4)=1. Tổng khoảng **1.365 dòng (~28%)**. Với các dòng này, câu hỏi "PTG ghi giá vào công ty nào" (P9) sẽ cho kết quả khác nhau tuỳ cách chốt.
- PTG `currency` (id): 1 (VNĐ)=1.219, 2 (USD)=1.100, 3 (EUR)=708, 4 (JPY)=90, 6/8/9 mỗi loại 1.

---

## 3. Vòng đời trạng thái

### 3.1 YCHG — `PriceAskingRequest::STATUSES` (`PriceAskingRequest.php:29-85`)

| Giá trị | Hằng | Nhãn hiển thị | Số dòng |
|---|---|---|---|
| 3 | DANG_TAO | Đang tạo | 376 |
| 2 | CHO_DUYET | Chờ PTKD duyệt | 1 |
| 5 | CHO_XNK_DUYET | Chờ XNK duyệt | 41 |
| 1 | DA_DUYET | **"Chờ XNK hỏi giá"** (tên hằng là "đã duyệt" nhưng nhãn khác) | 73 |
| 7 | CHO_TINH_GIA | Chờ tính giá | 22 |
| 4 | DA_TINH_GIA | Đã tính giá | 3.119 |
| 8 | KHONG_DUYET | Không duyệt (PTKD từ chối) | 171 |
| 9 | KHONG_CO_GIA | Không có giá (XNK từ chối) | 71 |
| 6 | HUY_DUYET | Huỷ duyệt | 155 |

Chuyển trạng thái:

```
store/update(status=3) ─► 3 Đang tạo
store/update(status=2) ─► 2 Chờ PTKD duyệt        [send(): received_time=now, TB → mọi người có quyền "PTKD duyệt…", log "Lập phiếu"]
2 ──PTKD approve()──────► 5 Chờ XNK duyệt          [approver_id, approved_time, comment; TB → buy_employee_id của AssignHistory; log "PTKD duyệt"]
2 ──PTKD reject()───────► 8 Không duyệt            [comment bắt buộc; TB → người lập; log]
5 ──XNK approveXNK()────► 1 "Chờ XNK hỏi giá"      [xnk_approver_id, xnk_approved_time, approver_comment; TB → người lập; log "XNK duyệt"]
5 ──XNK rejectXNK()─────► 9 Không có giá           [comment bắt buộc; TB → người lập; log]
1 ──XNK cancelApprove()─► 6 Huỷ duyệt              [cancel_reason bắt buộc; chỉ khi chưa có YCTG; TB → người lập; log]
1 ──lập YCTG status=2───► 7 Chờ tính giá           (PriceCalculateRequestController:155-160 / 207-212)
1 ──lập YCTG status=3───► giữ 1                     (YCTG nháp không đổi YCHG)
7/1 ──duyệt PTG─────────► 4 Đã tính giá            [calculated(): TB → người lập YCHG, link KQ; log "Duyệt tính giá"]
xoá YCTG (st=3) ────────► về 1
3/6/8/9 ──người lập sửa/gửi lại──► 3 hoặc 2
```

- Người được sửa/xoá: chỉ người lập, ở trạng thái 3/6/8/9 (`:530-538`).
- Danh sách mặc định ẩn các trạng thái 3/8/9 của người khác (`:338-341`).
- ⚠️ Lỗi tiềm ẩn ở `approve()` (`:589-605`): lưu `status=5` trước rồi mới kiểm phân công. Nếu chưa phân công người mua thì gọi `$this->responseErrors(...)`, nhưng method này **không tồn tại trên model** (chỉ có trong `ResponseTrait` của controller), nên ném `BadMethodCallException`. Controller `catch (Exception $e)` không bắt được vì chưa `use Exception` (tên bị hiểu là `App\Http\Controllers\Order\Exception`). Kết quả: lỗi 500, transaction không commit nên không lưu gì. Người dùng chỉ thấy "Đã có lỗi".

### 3.2 YCTG — `PriceCalculateRequest::STATUSES` (`PriceCalculateRequest.php:25-51`)

| Giá trị | Hằng | Nhãn | Số dòng |
|---|---|---|---|
| 3 | DANG_TAO | Đang tạo | 27 |
| 2 | CHO_DUYET | Chờ duyệt | 0 |
| 1 | DA_DUYET | Đã duyệt | 1 |
| 4 | DA_TINH_GIA | Đã tính giá | 3.119 |

```
store/update(status=3) ─► 3
store/update(status=2) ─► 2   [YCHG → 7; send(): TB → mọi người có quyền "Kế toán mua hàng" (toàn hệ thống, không lọc công ty)]
2 ──KT reject()─────────► 3   [comment; TB → người lập. YCHG VẪN ở 7, không trả về]
2 ──KT lập PTG (store)──► 1   [$req->approve() gọi VÔ ĐIỀU KIỆN, kể cả PTG lưu nháp]
1 ──PTG được duyệt──────► 4   [calculated(): TB → người lập YCTG, link KQ]
```

- ⚠️ YCTG bị KT từ chối thì quay về 3, nhưng YCHG **vẫn kẹt ở 7 "Chờ tính giá"**. Cập nhật YCTG và gửi lại thì YCHG được đặt lại 7. Không sai dữ liệu nhưng nhãn YCHG gây hiểu nhầm.
- Có đúng 1 cặp YCTG st=1 kèm PTG st=3 (nháp từ 28/02/2026). Đây là ca "lưu nháp PTG làm YCTG thành Đã duyệt".

### 3.3 PTG — `PriceCalculate::STATUSES` (`PriceCalculate.php:37-51`)

| Giá trị | Hằng | Số dòng |
|---|---|---|
| 3 | DANG_TAO | 1 |
| 1 | DA_DUYET | 3.119 |

- `store`/`update` nhận `status ∈ {1,3}` (`Controller:125, 207`). status=1 thì gọi `approve()` **ngay trong cùng request** (không có bước duyệt riêng: KT lập và "duyệt" là một thao tác). Nếu `approve()` trả `success=false` (có giá đang chờ duyệt) thì rollback.
- Chỉ người lập sửa được, khi st=3. Không có hủy duyệt PTG.

### 3.4 KQ

Không có trạng thái. Được tạo tự động trong `PriceCalculate::sendNotify()` (`PriceCalculate.php:783-799`), mỗi lần duyệt PTG tạo 1 KQ. Danh sách mặc định lọc `created_by = tôi` (tức người KT), còn `type=all` thì thấy tất cả.

---

## 4. Duyệt PTG ghi gì, ghi vào đâu (sau G3)

Chuỗi gọi: `PriceCalculateController@store/update` (`:160-166`, `:226-231`) → `PriceCalculate::approve()` (`:333-375`) → `updatePriceWithApproval()` (`:377-776`) + `sendNotify()` (`:783-799`).

### 4.1 Bước chặn trước khi ghi (`approve()`, `:336-362`)

Với mỗi dòng `chosen`, nếu tồn tại `product_approves` (theo product_id + product_unit_id + unit_id, `approved_id IS NULL`) thì trả lỗi "Cần xử lý giá đang chờ duyệt của sản phẩm: …". ⚠️ Truy vấn này **không lọc `company_id`**, trong khi đường ghi bên dưới (BB6) đã tách 1 yêu cầu cho mỗi (hàng × ĐVT × công ty). Hiện `product_approves` = 0 dòng nên chưa lộ.

### 4.2 Ghi `products.note` (`:364-370`)

`$product->note = $pro->note; $product->save();` ghi vào bảng **`products`**, mà thông tin hàng hoá nay do HRM quản lý (đợt 2-D1). Observer audit không log vì route `PriceCalculate.*` nằm trong danh sách trắng (`app/Observers/ProductWriteAuditObserver.php:31`).

### 4.3 Chọn công ty bộ giá: **`products.company_id`**, không phải công ty phiếu

```php
// PriceCalculate.php:385-388
// G3 (sửa tối thiểu, user chốt 10/10): PTG ghi BỘ GIÁ của công ty QUẢN LÝ hàng (products.company_id) như hôm nay,
// ... @TODO-PHASE7: luật chính thức (công ty của phiếu?) chốt ở Phase 7 (P9).
$company_id = $product->company_id ?? Auth::user()->info->company_id;
```

- Đọc `companies.is_company_price / is_all_brand / brand_ids` của công ty đó để quyết định `$is_approve` (`:389-404`). Hiện mọi công ty đều `is_company_price=0`, nên **luôn ghi thẳng, không qua duyệt**.
- ⚠️ **Lệch đọc/ghi:** form PTG nạp giá hiện hành theo **công ty của YCTG** (`PriceCalculateRequest::getDataForPriceCalculate`, `PriceCalculateRequest.php:135-151`, `DocumentCompany::of($object)` = `price_calculate_requests.company_id` = công ty người hỏi giá). Còn đường ghi lại ghi vào **công ty quản lý hàng**. Với khoảng 28% dòng lịch sử (phiếu cty 4/3/8 hỏi hàng cty 1), KT nhìn giá của cty 4 rồi ghi đè giá cty 1. `PriceCalculate::getDataForEdit/getDataForShow` đọc `prices` của chính phiếu nên không bị ảnh hưởng.

### 4.4 Ghi cho từng dòng chosen (`updatePriceWithApproval`, `:379-775`)

| # | Ghi vào | Chi tiết | company_id |
|---|---|---|---|
| a | `product_versions` (create) | `product_data = Product::getDataForVersion($product->id, $company_id)` (`:406-413`). Xoá lại nếu cuối cùng không có dòng history nào (`:581-584`) | không có cột; snapshot theo `$company_id` |
| b | `product_unit_prices` (firstOrNew theo price_type_id + product_unit_id + **company_id**) | Không duyệt: ghi `price, coefficient, sale_max_percent`, xoá 0 hết các cột `*_wait_approve` và `flag_*`. Có duyệt: ghi vào `*_wait_approve` + `flag_*` (`:429-487`). **Không ghi `is_manual_*_online`** (FE có gửi nhưng BE bỏ qua) | `$company_id` (G3) |
| c | `product_expected_prices` | **Xoá mọi dòng `effect_date > hôm nay`** của unit_price đó (`:490-492`), xoá `product_approve_prices` gắn expected (`:493-498`), rồi tạo mới từ PTG (status=2, nếu có duyệt thì kèm flag=1) (`:500-549`) | không có cột; theo `unit_price_id` |
| d | `product_company_units` (firstOrNew theo product_unit_id + company_id) | Không duyệt: `cost_price = $pro->cost_price` (giá nhập kho từ FE). Có duyệt: `price_wait_approve` + `flag_price_wait_approve` (`:420-424`, `:552-570`) | `$company_id` (G3) |
| e | `product_histories` | so `units_for_history` trước/sau rồi `createHistoryRecord('units', …)` + `saveHistory()` (`:572-579`) | — |
| f | `product_approves` + `product_approve_prices` (chỉ nhánh có duyệt) | tạo mới hoặc cập nhật 1 yêu cầu cho mỗi (hàng × ĐVT × company_id) (`:587-774`). TB "Duyệt giá hàng hoá" tới người có quyền ở `$company_id`, link `ProductMovedToHrm::buildHrmUrl('price-approve')` = `/finance/product-price-approvals` của HRM (G6, `:725-729`) | `$company_id` |

Lỗi phụ trong đường ghi:
- `getUnitsForHistoryAttribute` (`app/Product.php:2000-2018`) đọc `prices` của **mọi công ty** và `cost_price/buy_price` từ **13 cột cũ của `product_units`** (G3 đã ngừng ghi). Hệ quả: lịch sử "units" không phản ánh thay đổi giá vốn, và lẫn giá của nhiều công ty.
- Ghi chú `note` được lưu trước khi tạo version, nên `saveHistory()` không ghi lại thay đổi ghi chú.
- Nhánh có duyệt (`:520-532`): `$oldExpectedPrice` được truy vấn **sau khi** đã xoá dòng cũ và lưu dòng mới, nên luôn so với chính nó và gần như luôn đặt flag=1. Nhánh này hiện chưa chạy.
- `approve_expected_prices` không mang `company_id`, nhưng `ProductApprovePrice` cũng không có cột này nên không ảnh hưởng.

### 4.5 `sendNotify()` (`:783-799`) — tạo KQ + chốt trạng thái

1. Tạo `price_calculate_results` (asking_id, calc_request_id, calc_id, requester_id = người lập YCHG) và `syncProducts` (chỉ các dòng chosen, chép prices + expected_prices) (`PriceCalculateResult.php:131-145`).
2. `PriceCalculateRequest::calculated()`: st=4, TB → người lập YCTG, link `PriceCalculateResult.show`.
3. `PriceAskingRequest::calculated()`: st=4, TB → người lập YCHG, link KQ, log "Duyệt tính giá".

### 4.6 Hàng tạm (`tmp_products`)

**Luồng tính giá không liên quan hàng tạm**: không có tham chiếu nào tới `tmp_products`. YCHG chỉ chọn hàng thật (`products,id`, validate `exists:products,id`). Hàng tạm có đường ghi giá riêng (`tmpProductApprove`, xem G3).

---

## 5. Liên kết với chứng từ và chức năng khác

| Loại | Nơi | Chi tiết |
|---|---|---|
| Báo giá / hợp đồng / đơn hàng | — | **Không có liên kết.** Không bảng hay model bán hàng nào tham chiếu bảng tính giá. Báo giá chỉ dùng gián tiếp giá mà PTG đã ghi vào `product_unit_prices` |
| Hàng hoá (popup thêm hàng) | `Product::checkPriceAsked()` (`app/Product.php:7725-7731`), bản sao ở `ProductInfo.php:4016`, `ProductTemplate.php:6958` | cảnh báo "Hàng này đã có người hỏi giá" (YCHG st=1). Gọi từ `getDataForPriceAsking` của 4 controller: `ProductsController.php:3374`, `Product2Controller.php:1980`, `ProductInfoController.php:1708`, `ProductTemplatesController.php:2260` |
| Phân công mua hàng | `AssignHistory` (`app/Model/Order/AssignDepartmentBallot/AssignHistory.php`) | (manufactures_id, brand_id, company_id = send_company_id, `employee_date_to IS NULL`) → `buy_employee_id` = người XNK duyệt / huỷ duyệt; cột "Người mua" ở list |
| Thông báo | `Notification::sendNotify / sendNotifyWithPermission`, `NotificationHelper::sendNotify` | 9 điểm gửi (mục 3). URL là **đường dẫn tương đối của ERP** (`route(..., false)`). Riêng TB duyệt giá đã trỏ HRM (G6). `sendNotifyWithPermission('Kế toán mua hàng')` và `('PTKD duyệt…')` gửi **toàn hệ thống, không lọc công ty** |
| Dashboard "việc chờ" | `HomeController.php:1394-1443` | 3 thẻ: "Yêu cầu hỏi giá chờ duyệt" (st=2, theo phạm vi), "Yêu cầu hỏi giá cần XNK duyệt" (st=5, theo phân công), "Yêu cầu tính giá chờ duyệt" (`PriceCalculateRequest::where('status',2)->count()`, **không lọc công ty**) |
| Approval inbox / registry | — | **ERP nhánh này không có** approval inbox (không có bảng `*approval*` trừ `bom_price_approval_*`) |
| Menu | `resources/views/layouts/topmenubar.blade.php:327, 931, 1534, 1536, 2383` | 5 link menu |
| In ấn | `getPrintTemplateAttribute` + `ReportTemplate` id 98 (YCHG), 99 (YCTG), 100 (PTG, **thiếu trong DB**), `KET_QUA_TINH_GIA` (**chưa khai báo hằng**) | Bản in YCHG có cột "Giá bán" = giá bán lẻ hiện hành của **công ty YCHG** (`DocumentCompany::ofOrUser`, `PriceAskingRequest.php:722`), làm tròn nghìn. Bản in YCTG gồm bảng hàng và bảng chi phí |
| Export Excel | — | **Không có** (import `FastExcel`/`PDF` nhưng không dùng) |
| Lịch sử duyệt | `price_asking_request_approve_histories` | hiển thị ở màn show YCHG (`log_approves`) |
| Seeder backfill | `database/seeds/UpdateDB.php:763-960` (`updatePricesFromApprovedPriceCalculate`, `updateCostPriceFromApprovedPriceCalculate`) | đọc lại PTG đã duyệt để ghi lại giá / giá vốn. Chạy tay một lần |
| **HRM đã tham chiếu** | `hrm-api/Modules/MasterData/Services/Product/ProductUsageGuard.php:56-57` (4 bảng `*_products` để chặn xoá hàng); `hrm-api/Modules/CustomerCare/Entities/Cost/Cost.php:106-107` (2 bảng `*_costs` để chặn xoá chi phí) | HRM đã biết các bảng này nhưng chưa có màn |

---

## 6. Chặn luồng ở ERP thì cái gì vỡ

Đã grep `price_asking_request|PriceAskingRequest|price_calculate|PriceCalculate` toàn bộ `app/`, `resources/views/`, `routes/`, `config/`, `database/seeds/` (trừ 4 controller, 15 model, view `orders/price_*` và class JS `partials/classes/order/Price*`).

| Nơi đọc | Nếu chặn route / bỏ màn ERP |
|---|---|
| `HomeController.php:1394-1443` (3 thẻ dashboard, gọi `route('PriceAskingRequest.index')`, `route('PriceCalculateRequest.index')`) | Nếu **xoá route** thì `route()` ném lỗi, **trang chủ ERP vỡ** với user có quyền. Nếu chỉ gắn middleware chặn (giữ tên route) thì thẻ vẫn hiện nhưng bấm vào ra trang "đã chuyển HRM". Nên bỏ thẻ hoặc trỏ HRM |
| `topmenubar.blade.php` (5 link `route(...)`) | Tương tự: xoá route là vỡ **mọi trang** ERP. Phải sửa menu cùng lúc |
| `Product::checkPriceAsked()` + 4 controller `getDataForPriceAsking` | Chỉ **đọc** bảng, không vỡ khi chặn màn. Nếu bỏ luôn route `product.getDataForPriceAsking` thì form YCHG ERP chết theo (vốn đã chặn) |
| `ProductWriteAuditObserver::WHITELIST_ROUTES` `'PriceCalculate.*'` | Không vỡ. Sau khi chuyển nên gỡ để audit bắt đường ghi còn sót |
| `UpdateDB.php` seeder | Không ảnh hưởng runtime |
| Thông báo cũ trỏ URL ERP | Hiện không có dòng nào trong `notifications` local. Trên production có thể có, bấm vào sẽ ra trang chặn |
| Cron `product:update_price` (01:00) | **Phải giữ**: áp giá hiệu lực mà PTG đã ghi vào `product_expected_prices` (status 2). Không phụ thuộc bảng tính giá nhưng phụ thuộc dữ liệu PTG tạo ra. Nếu HRM có cron riêng thì phải tránh chạy cả 2 nơi |
| Báo giá / bán hàng / kho / mua hàng | **Không đọc** bảng tính giá, nên không vỡ |

Kết luận: chặn bằng middleware kiểu `productMovedToHrm` (giữ nguyên tên route) là an toàn. **Không được xoá route** khi chưa sửa menu và dashboard.

---

## 7. Công thức tính giá (để port)

> BE không tính gì, chỉ lưu số FE gửi. Công thức nằm ở `resources/views/partials/classes/order/PriceCalculate*.blade.php` và `resources/views/partials/classes/sale/ProductPrice.blade.php`, `ProductExpectedPrice.blade.php`. Port sang HRM thì nên tính lại hoặc kiểm lại ở BE.

### 7.1 Đầu vào

- Tiền tệ `currency` = id bảng `currencies`. Chọn tiền tệ thì FE nạp `exchange_rate` mặc định của `currencies` (`price_calculate_requests/formJs.blade.php:7-12`), người dùng sửa được.
- YCTG (XNK/mua hàng nhập): mỗi dòng có `supplier_price` (giá NCC, ngoại tệ), `import_tax` (% thuế NK, mặc định = `products.import_tax`), danh sách chi phí `costs[]` (`cost_id`, `rate` %, `value`). Chi phí mặc định lấy từ `manufacture_costs` (đang rỗng). Cờ `chosen` để chọn dòng đưa sang tính giá.
- PTG (KT nhập): chép từ YCTG các dòng `chosen=1` (`getDataForPriceCalculate`), cho sửa `supplier_price`, `import_tax`, `costs`, thêm `other_cost` (VNĐ), `note`, và bảng giá bán 6 loại (`coefficient`, `price`, `sale_max_percent`) + tối đa 1 giá hiệu lực tương lai cho mỗi loại (`expected_prices`: `coefficient`, `price`, `sale_max_percent`, `effect_date > hôm nay`).

### 7.2 Giá vốn / giá nhập kho (FE: `PriceCalculateProduct.blade.php`, `PriceCalculateProductCost.blade.php`)

```
supplier_price_exchange   = supplier_price × exchange_rate                         (VNĐ)
amount_exchange_after_tax = supplier_price_exchange × (1 + import_tax/100)
cost.value (ngoại tệ)     = rate% × supplier_price  (hoặc nhập value thì rate = value/supplier_price×100, value ≤ supplier_price)
cost.value_exchange (VNĐ) = cost.value × exchange_rate
sum_cost                  = Σ cost.value_exchange
cost_price (giá nhập kho) = amount_exchange_after_tax + sum_cost + other_cost       ← lưu price_calculate_products.cost_price
                                                                                      và ghi product_company_units.cost_price khi duyệt
```

- Ghi chú #11334 trong code: giá vốn cộng **sau thuế NK**.
- BE có công thức dự phòng **khác** (`PriceCalculateProduct.php:77-100`): `exchanged_price = floor(supplier_price × rate)`, `cost_value = floor(exchanged_price × value/100)` (coi `value` là %), `cost_price = exchanged + Σcost_value + other_cost` (**không thuế NK**). Chỉ dùng khi cột `cost_price` NULL (dữ liệu cũ). Bản in PTG dùng `cost_value`.
- `is_foreign` ở BE = `currency != 'VNĐ'` (`PriceCalculate.php:904-907`). Vì currency lưu dạng id nên điều kiện này **luôn đúng**, do đó luôn lấy exchange_rate từ request. Hiện vô hại vì FE gửi 1 cho VNĐ.

### 7.3 Giá bán (FE: `ProductPrice.blade.php`)

- 6 loại giá (`price_types`): 1 Bán lẻ, 2 ĐL cấp 1, 3 ĐL cấp 2, 4 ĐL cấp 3, 5 Giá bán theo lô, 6 TMĐT (online).
- **Hệ số → giá:** `price = round(coefficient × cost_price / 100) × 100`, tức giá = hệ số × giá vốn, làm tròn tới trăm đồng (`:197-204`). Hệ số là **bội số** (ví dụ 1.35), validate `0 ≤ coef < 100` (`not_in:100`), cột decimal(5,2). Hệ số giá hiệu lực tối đa 99.
- **Sửa loại 1 (Bán lẻ) thì lan sang mọi loại khác:** set `price`/`coefficient`/`sale_max_percent` của loại 1 sẽ gọi `parent.updatePrices(field, value)`, gán cùng giá trị cho **mọi loại trừ TMĐT** (`PriceCalculateProduct.blade.php:97-113`). Muốn khác thì sửa từng loại sau.
- **TMĐT (loại 6):** `price = round(retail.price × CONFIG.coefficient_ecommerce_price)`, `coefficient = retail.coefficient × CONFIG.coefficient_ecommerce_price`, `sale_max_percent = 0`. Đây là **cấu hình chung** (`configs.coefficient_ecommerce_price`, `ConfigsController.php:60`). Trong ngữ cảnh PTG luôn dùng công thức (`is_price_calculate_context = true`), không dùng giá DB. Riêng phiếu đã lưu thì hiển thị đúng giá đã lưu (`is_saved_record`). Giá hiệu lực TMĐT suy từ giá hiệu lực bán lẻ cùng `effect_date`, không có thì dùng giá bán lẻ hiện hành.
- `recipe_price` ("giá công thức", hiển thị) = `cost_price × coefficient`, loại 6 làm tròn nghìn.
- Khi mở PTG mới: giá và hệ số hiện hành được nạp theo **công ty YCTG** (xem 4.3). `recalcAllPrices()` tính lại giá bán lẻ = hệ số hiện hành × giá vốn mới, rồi lan sang các loại (`PriceCalculateProduct.blade.php:30-37`).
- `sale_max_percent` = định mức giảm giá tối đa (%) 0–100, không tham gia công thức.

### 7.4 Không có trong luồng

- **Không dùng** `product_company_coefficients.coefficient` (hệ số giá công ty, sẽ bỏ) và `tech_coefficient` (hệ số công nghệ/lắp đặt).
- Không có SL, chiết khấu NCC, phí vận chuyển riêng (vận chuyển là luồng `delivery_cost_asking_requests` riêng).

---

## 8. Rủi ro và câu hỏi nghiệp vụ cần chốt

### 8.1 Câu hỏi cần user chốt

1. **(P9, đang ⏸)** PTG ghi bộ giá vào công ty nào: công ty quản lý hàng (`products.company_id`, như code hiện tại), công ty lập YCHG (`price_asking_requests.company_id`), hay `send_company_id` (công ty nhận hỏi giá)? Khoảng 28% dòng lịch sử có 2 giá trị này khác nhau. Cũng cần chốt **form PTG nạp giá hiện hành theo công ty nào** (hiện là công ty YCTG, đang lệch với đường ghi).
2. Một PTG có ghi được cho **nhiều công ty** cùng lúc không (ví dụ cty 1 tính rồi áp cho cả 4 công ty)? Hay mỗi công ty tự tính?
3. Nhánh "quy chế giá công ty" (`is_company_price`, cần duyệt) hiện tắt ở cả 8 công ty và `product_approves` = 0. HRM có giữ nhánh này không, hay đẩy sang luồng "Duyệt giá bán HRM" (G6)?
4. PTG có tiếp tục **ghi `products.note`** (thông tin hàng do HRM quản lý) không?
5. Phạm vi xem: giữ 3 bộ quyền lệch nhau (YCHG theo `canInCompany` + phòng quản lý; YCTG/PTG theo `can` + phòng của NV) hay thống nhất? KQ hiện **ai cũng xem hết** (`canView` = true, `type=all` không lọc). YCHG `canView` cũng luôn true, và màn show YCHG đã tính giá **nhúng nguyên dữ liệu PTG vào HTML (giá NCC, chi phí, giá vốn `cost_price`)** qua `@json($data)` (`price_asking_requests/show.blade.php:361`, `PriceAskingRequest.php:248-252`). Đây là lộ giá vốn cho NV kinh doanh. Port có chặn không?
6. Thông báo "gửi YCTG" (`Kế toán mua hàng`) và "gửi YCHG" (`PTKD duyệt…`) đang gửi **mọi công ty**. HRM có lọc theo công ty không?
7. Tách bước "KT lập PTG" và "duyệt PTG" thành 2 người, hay giữ một thao tác như hiện tại?
8. Dữ liệu lịch sử: HRM đọc thẳng 15 bảng hiện có (DB gộp, không migrate), hay đổi cấu trúc? Lưu ý `currency` là id, KQ không có mã phiếu.
9. Cron áp giá hiệu lực (`product:update_price` 01:00) giữ ở ERP hay chuyển HRM? Không được chạy cả 2 nơi.

### 8.2 Lỗi sẵn có (ghi nhận, không vá trong đợt này)

- `GET /admin/orders/price_calculates/{id}/delete` **xoá PTG không kiểm quyền** (`PriceCalculateController.php:250-254`).
- In PTG 404 (thiếu template 100). In KQ 500 (thiếu method + hằng).
- PTKD duyệt khi chưa phân công người mua → 500 (`responseErrors` không tồn tại trên model, `catch (Exception)` thiếu `use`). Controller YCHG và PTG đều thiếu `use Exception`.
- YCTG bị từ chối nhưng YCHG vẫn "Chờ tính giá". Lưu nháp PTG đẩy YCTG thành "Đã duyệt".
- Kiểm "giá đang chờ duyệt" không lọc company_id. Lịch sử "units" đọc mọi công ty và cột giá vốn cũ.
- 18 YCHG có `send_company_id` NULL (dữ liệu cũ). Ca này nếu được duyệt XNK thì không tìm được phân công.

### 8.3 Khi port sang HRM phải nhớ

- Bỏ bypass Super Admin (4 chỗ ở mục 1.5).
- Gắn chặn ERP bằng middleware, **giữ tên route** cho tới khi sửa xong menu (`topmenubar`) và dashboard (`HomeController`). Gỡ `'PriceCalculate.*'` khỏi whitelist audit sau khi chuyển.
- Đường ghi giá phải đi qua lớp ghi giá theo công ty của HRM (G-series), ghi đủ `product_unit_prices.company_id` + `product_company_units`. `product_expected_prices` không có `company_id`, chỉ đi theo `unit_price_id`.
- URL thông báo đổi sang đường dẫn HRM FE.
- Công thức ở mục 7 phải chuyển sang FE Vue của HRM (và nên kiểm lại ở BE). Đặc biệt quy tắc "sửa bán lẻ thì lan sang mọi loại", TMĐT theo `configs.coefficient_ecommerce_price`, làm tròn trăm đồng.
