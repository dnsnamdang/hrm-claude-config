# Task 2 — Entities — Báo cáo

**STATUS:** DONE

## File đã tạo (4)
- `hrm-thanhan-api/Modules/Supply/Entities/PurchaseContract.php`
- `hrm-thanhan-api/Modules/Supply/Entities/PurchaseContractPaymentTerm.php`
- `hrm-thanhan-api/Modules/Supply/Entities/PurchaseContractProduct.php`
- `hrm-thanhan-api/Modules/Supply/Entities/PurchaseContractProgress.php`

## Xác nhận nội dung

### PurchaseContract
- extends `App\Models\BaseModel`, `use SoftDeletes`, `$table='purchase_contracts'`, `$guarded=[]`.
- Constants trạng thái: `STATUS_DRAFT=1, STATUS_PENDING=2, STATUS_APPROVED=3, STATUS_REJECTED=4, STATUS_CANCELED=5`.
- Constants loại: `TYPE_NGUYEN_TAC=1, TYPE_THUONG_MAI=2`.
- `STATUSES` = 5 phần tử [id/name/text_type]: Nháp=secondary, Chờ duyệt=warning, Đã duyệt=success, Từ chối=danger, Hủy=dark. (theo Global Constraints plan dòng 14 — dùng `text_type`, không phải `color` như SupplyHandling).
- Thêm `TYPES` (tiện dùng FE/transformer).
- Quan hệ: `products()` hasMany, `paymentTerms()` hasMany, `progress()` hasMany (orderBy sort_order).
- Accessors: `getIsCanEditAttribute` (status ∈ {DRAFT,REJECTED}); `getIsCanDeleteAttribute` (status ∈ {DRAFT,REJECTED} AND created_by == auth id, dùng `optional(auth()->user())->id` an toàn null); `getIsCanApproveAttribute` (status == PENDING).
- `getNextCode(): string` → `HDM-<năm>-<####>` (4 chữ số), đếm bản ghi năm hiện tại của bảng này bằng `self::whereYear('created_at',$year)->count()`.

### PurchaseContractPaymentTerm
- extends BaseModel, `$table='purchase_contract_payment_terms'`, `$guarded=[]`.
- Const `TERM_100PCT/TERM_TIME/TERM_VALUE/TERM_ROLLING` + mảng `TERMS` (name/exclusive/field) copy y nguyên từ ContractPaymentTerm (100PCT exclusive=true field=null; TIME→max_days; VALUE→max_value; ROLLING→max_orders).
- `getDefaultTerms(): array` → 4 dòng enabled=false.
- `purchaseContract()` belongsTo.

### PurchaseContractProduct
- extends BaseModel, `$table='purchase_contract_products'`, `$guarded=[]`, `$casts=['purposes'=>'array']`.
- `purchaseContract()` belongsTo.

### PurchaseContractProgress
- extends BaseModel, `$table='purchase_contract_progress'`, `$guarded=[]`.
- `purchaseContract()` belongsTo.

## php -l
No syntax errors detected — cả 4 file.

## Concerns / lưu ý
- `STATUSES` dùng key `text_type` (theo yêu cầu Task + Global Constraints) — KHÁC SupplyHandling dùng key `color` (mã hex). Transformer Task 4 (map `status_color`) cần map lại từ `text_type` hoặc bổ sung `color`; cần thống nhất khi làm Task 4.
- `getIsCanApproveAttribute` chỉ kiểm `status == PENDING` (theo mô tả entity của Task). Spec §5.8 ghi "is_can_approve = status=2 AND có quyền duyệt" — phần kiểm quyền để Service/Transformer xử lý, không đặt trong accessor entity.
- Không tạo service/controller/migration (đúng scope Task 2).
