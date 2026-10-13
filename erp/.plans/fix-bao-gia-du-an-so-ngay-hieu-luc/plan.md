# Fix: Màn báo giá dự án (firm-quotations type=2) chưa áp "Số ngày hiệu lực báo giá dự án"

**Nhánh:** `gop_db` (ERP TanPhatDev)
**Màn:** Báo giá dự án — `admin/sale/firm-quotations?type=all&quotation_type=2`
**File sửa:** `resources/views/partials/classes/sale/firm/quotation/FirmQuotation.blade.php`

## Vấn đề

Getter `date_of_entering` (số ngày hiệu lực báo giá, dùng để tính ngày HẾT HẠN hiển thị) luôn lấy
`config.quotation_valid_days` (= "Số ngày hiệu lực báo giá" thường, mặc định 10) cho MỌI loại báo
giá — kể cả báo giá DỰ ÁN (`quotation_type = BG_DU_AN = 2`), vốn phải dùng cấu hình riêng
`config.project_quotation_valid_days` (= "Số ngày hiệu lực báo giá dự án", vd 60).

Cấu hình "Số ngày hiệu lực báo giá dự án" nay khai ở HRM regulation-config (màn "Báo giá – Hợp
đồng"), ghi về bảng `configs`. ERP đã có sẵn giá trị này trong `config` nhưng màn firm-quotation
không rẽ nhánh theo loại nên không dùng tới.

Đối chiếu: màn `ProjectQuotation.blade.php:78-89` (một luồng báo giá dự án khác) đã dùng đúng
`project_quotation_valid_days` — firm-quotation type=2 thì chưa.

## Yêu cầu bổ sung của user: "phải sửa đúng theo công ty"

`this.config = @json(App\Model\Common\Config::getConfig())` (constructor dòng 28). `getConfig()`
đã scope THEO CÔNG TY người đăng nhập:
- `resolveCompanyId()` → `auth()->user()->info->company_id` (fallback cty 1 nếu công ty tạo sau
  chưa backfill dòng `configs`).
- `where('company_id', $companyId)->first()`.

→ `this.config` chính là dòng `configs` của công ty người lập, nên cả `quotation_valid_days` lẫn
`project_quotation_valid_days` đọc ra ĐÃ đúng theo công ty. Getter chỉ cần rẽ nhánh đúng key —
không cần thêm plumbing per-company nào khác. (Liên quan memory gộp-DB: helper đọc `configs` global
hay trả dòng công ty 1; ở đây Config::getConfig đã per-company nên không dính bẫy đó.)

## Thay đổi

Getter `date_of_entering` (dòng ~419-431): thêm biến `valid_days` chọn key theo loại báo giá,
dùng ở cả so sánh lẫn giá trị mặc định.

```js
let valid_days = this.quotation_type == 2        // BG_DU_AN
    ? this.config.project_quotation_valid_days
    : this.config.quotation_valid_days;
```

- `this.quotation_type` có sẵn trên instance: `create.blade.php:40` khởi tạo
  `new FirmQuotation({quotation_type: {{ $quotation_type ?: 1 }}}, ...)`.
- Nhánh `mode == 'show'` giữ nguyên (trả `_date_of_entering` đã lưu) — không đụng chi tiết/sửa.
- BE `store()` vẫn chỉ lưu `date_of_entering` FE gửi lên → fix thuần FE là đủ.

## Tasks

- [x] Xác minh `Config::getConfig()` per-company (resolveCompanyId → auth company_id)
- [x] Xác minh `this.quotation_type` tới được class (create.blade.php:40)
- [x] Sửa getter `date_of_entering` rẽ nhánh theo `quotation_type == 2`
- [ ] Verify trình duyệt: tạo báo giá dự án (quotation_type=2), kiểm ngày hết hạn = ngày lập +
  `project_quotation_valid_days` của ĐÚNG công ty người lập; báo giá hàng (type=1) vẫn dùng
  `quotation_valid_days`
- [ ] Commit + push khi user yêu cầu

## Ghi chú

- Chỉ sửa FE getter, không đụng BE, không đụng `Config::getConfig()` (hàm dùng chung).
- Chưa commit/push — chờ user yêu cầu (CLAUDE.md ERP cấm tự commit).
