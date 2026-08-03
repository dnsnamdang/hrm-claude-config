# Task 3 — FormRequest + Service (Hợp đồng mua) — Report

**Người làm:** @khoipv · **Ngày:** 2026-07-20 · **Trạng thái:** DONE

## File tạo/sửa

| Loại | File |
|---|---|
| Sửa | `hrm-thanhan-api/Modules/Supply/Entities/PurchaseContract.php` — XÓA `getNextCode()` count-based, thay bằng comment trỏ sang Service |
| Tạo | `hrm-thanhan-api/Modules/Supply/Http/Requests/StorePurchaseContractRequest.php` |
| Tạo | `hrm-thanhan-api/Modules/Supply/Services/PurchaseContractService.php` |

> Lưu ý path Request: đặt tại `Http/Requests/StorePurchaseContractRequest.php` (đúng path task/plan yêu cầu), KHÔNG theo subfolder như `SupplyHandling/`, `SupplyProposal/`. Đã xóa bản subfolder tạo nhầm.

## StorePurchaseContractRequest (extends Training\BaseRequest)
- required: `number`, `name`, `type`, `main_company_id`, `supplier_id`.
- `products` required|array|min:1; `products.*.price` & `products.*.order_qty` nullable|numeric|min:0.
- `payment_terms` nullable|array; `payment_terms.*.term_code` nullable|in (4 mã lấy động từ `PurchaseContractPaymentTerm::TERMS`).
- `progress` nullable|array. Messages tiếng Việt cho field required + term_code.

## PurchaseContractService (extends Training\BaseService)
- **generateCode() / previewNextCode()** — copy pattern SupplyHandlingService: base `HDM-<year>-`, max-sequence + `withTrashed()` + vòng while chống trùng.
- **getList($request)** — QUERY BUILDER (không paginate). Filter: `number`(like), `name`(like), `supplier_id`, `type`, `status`, `sign_time_from`/`sign_time_to` (whereDate). `checkPermissionList($query, [self::PERM_VIEW, null, null, null, null], 'purchase_contracts')` (không phân cấp: có quyền Xem → thấy tất cả) + orderBy id desc.
- **store($request)** — DB::transaction: new + fill(header, đã loại mảng con/code/total_amount) + `code=generateCode()` + `total_amount=calcTotalAmount()` + save → syncProducts/syncPaymentTerms/syncProgress → nếu status=2 set `sent_at`+`sendNotification`.
- **update($request,$contract)** — như store nhưng fill vào contract sẵn có; chỉ gửi thông báo khi status=2 VÀ trước đó `sent_at` null (chưa gửi).
- **syncProducts** — xóa hết → bulk insert (chunk 1000), set created_at/updated_at thủ công. Lưu snapshot đầy đủ + `order_qty`/`price`/`vat_percent`/`amount`(=price×order_qty)/`proposed_qty`/`purposes`(json_encode thủ công vì insert thô)/`note`/`sort_order`. Nguyên tắc → order_qty/amount = 0.
- **syncPaymentTerms** — copy logic ContractService: 100PCT enabled → ép tắt loại khác; `updateOrCreate` theo (purchase_contract_id, term_code); payload rỗng & chưa có dòng → tạo `getDefaultTerms()`.
- **syncProgress** — xóa hết → bulk insert (label/pct/time/sort_order).
- **calcTotalAmount** (private) — Σ price×order_qty; type≠Thương mại → 0.
- **approve** — status=APPROVED + approved_by + approved_at.
- **rejectApprove** — status=REJECTED + reason_deny.
- **sendNotification** — xem pattern dưới.

## Pattern sendNotification đã dùng
Theo đúng `SupplyProposalService::notifyHandlers()` / `notifyApprovers()`:
1. `listEmployeeInfoHasPermission(self::PERM_APPROVE)` (helper global tại `app/Helper/PermissionHelper.php`) → mảng employee_info id.
2. `EmployeeInfoService::sendToAllNotification($employeeInfoIds, $data)` (`Modules/Timesheet/Services/EmployeeInfoService.php`) → ghi bảng `notifications` (polymorphic, có receiver_id).
- Quyền dùng: hằng `const PERM_APPROVE = 'Duyệt hợp đồng mua';` khai báo trong Service.
- `$data`: url `/supply/purchase_contracts/{id}`, title "Có hợp đồng mua {code} cần duyệt", type `purchaseContractApprove`, employeeInfo = người tạo.
- Bọc `try/catch` + Log::error để lỗi gửi thông báo không rollback transaction lưu HĐ (giống Supply gốc).

## Kết quả php -l
`No syntax errors detected` cho cả 3 file (Service, Request, Entity).

## Concerns
1. **checkPermissionList — ĐÃ CHỐT & SỬA.** Coordinator xác nhận "không phân cấp = ai có quyền Xem thấy tất cả". Đã đổi thành `checkPermissionList($query, [self::PERM_VIEW, null, null, null, null], 'purchase_contracts')` với hằng `const PERM_VIEW = 'Xem hợp đồng mua'` (nhất quán với `PERM_APPROVE`). Quyền Xem đặt ở index[0] = cấp tổng → có quyền xem thì thấy toàn bộ (gồm cả người duyệt); không có quyền → không thấy. Đã bỏ hẳn `true` ở index[4].
2. **fill header** — dùng `$request->except(['id','code','total_amount','products','payment_terms','progress'])` thay cho `fill($request->all())` để tránh Eloquent insert nhầm cột mảng con (products/payment_terms/progress không phải cột bảng → SQL error). Đây là điều chỉnh nhỏ so với mô tả "fill($request->all())" nhưng bắt buộc để chạy đúng.
3. Chưa chạy `php artisan` (không kiểm tra autoload/DB); chỉ verify tĩnh php -l theo yêu cầu task.
