# Tách quyền "Kế toán" (`accounting.ke_toan.manage`) thành 3 quyền theo màn — Design

> Phạm vi: **ERP + HRM** (quyền dùng chung qua Catalog). Chốt để lập plan.
> Ngày: 2026-11-27. Anh em cùng loạt: `.plans/tach-quyen-ke-toan-kho/` (36 mã, đã xong).

## 1. Ý định & lý do (why)

Hiện có **một** quyền `accounting.ke_toan.manage` (nhãn "Kế toán") đóng vai "người kế toán hỗ trợ / lập chứng từ". Nó gác ~3 chức năng khác hẳn nhau. Admin tích "Kế toán" là cấp cả cụm — không cấp lẻ được từng chứng từ. Giống lý do đã tách "Kế toán kho": tên quá chung → all-or-nothing.

**Mục tiêu:** tách thành **3 quyền tên rõ, mỗi màn/chứng từ = 1 quyền**, cấp đúng từng chỗ; không ai mất quyền sau khi tách; deprecate quyền cũ.

## 2. Goals / Non-goals / Anti-goals

**Goals**
- 3 quyền mới, nhãn tiếng Việt rõ, mỗi quyền gác đúng 1 màn/chứng từ.
- **Không ai mất quyền:** mọi vai trò/NV đang có `accounting.ke_toan.manage` được cấp tự động cả 3 mã mới (lệnh cấp-lại 1→3, mượn nguyên cơ chế `rbac:grant-ke-toan-kho-split`).
- Mọi gate/thông báo hiện trỏ về mã cũ phải trỏ lại đúng mã mới tương ứng; không còn gate nào dùng `accounting.ke_toan.manage`.

**Non-goals**
- Không đổi nghiệp vụ (ai duyệt/thấy gì vẫn như cũ — chỉ đổi "khoá" kiểm).
- Không port thêm màn HRM mới.
- Không đụng hằng `PERMISSION_NOTIFY_TARGET` (`:242`) — nó đã trỏ mã **kế toán kho #36** từ đợt trước, KHÔNG phải `accounting.ke_toan.manage`.
- Không đụng `accounting.ke_toan_mua_hang.manage` (quyền khác, ngoài phạm vi).

**Anti-goals (thất bại dù code chạy)**
- Sau deploy, một người đang lập phiếu/duyệt bị chặn ở chức năng họ vốn làm được.
- Sót một chỗ gate khiến mã cũ vẫn tác dụng (khoá "ma").
- Nhầm mã mới `ke_toan_yc_hach_toan_bo_sung` với mã có sẵn `ke_toan_kho_yc_hach_toan_bo_sung` (gần giống tên).

## 3. Constraints

- Catalog là nguồn sự thật: `hrm-api/app/Support/Permissions/Catalog/accounting.php`; đồng bộ DB bằng `php artisan permission:catalog-sync` (thêm/deprecate, không xoá cứng). **KHÔNG seeder, KHÔNG migration** cho quyền (đã gỡ 06/11/2026).
- DB **dùng chung** ERP+HRM (gộp). Spatie pivot `role_has_permissions`, `employee_has_permissions`. Prod chạy `catalog-sync` qua `~/build_tpe.sh` trên VPS HRM.
- ERP = Laravel 6 (`develop_02`), check `->can('<code>')` / `NotificationHelper::sendNotify…Permission`. HRM = Laravel 8 (`develop`), check qua hằng + `currentEmployeeHasPermission` + Approval Center Definition.
- Không đổi `code` đã lên prod; không bypass Super Admin (HRM).
- Client Nuxt KHÔNG gate trực tiếp bằng mã này (chỉ đọc cờ BE `is_support_accountant`, `is_can_create_accounting_bill`) → **không sửa hrm-client**.

## 4. Approaches

- **(A) Mịn — 3 mã (1 mã/chức năng). ✅ CHỌN** (user chốt). Khớp đúng "cấp đúng từng chứng từ". Giá: sửa 6 chỗ ERP + 1 hằng HRM (+ lan tự động) + Catalog + lệnh cấp-lại + deprecate. Nhỏ hơn kế toán kho nhiều.
- **(B) Gộp — 2 mã** (gộp Phiếu thưởng KD + Phiếu lợi nhuận). Loại: không cấp lẻ được 2 phiếu.
- **(C) Giữ 1 quyền, đổi tên rõ.** Loại: vẫn all-or-nothing.

## 5. 3 quyền mới (how — phần quyết định)

**Quy ước:** code `accounting.ke_toan_<slug>.manage`, `subsystem_group='Kinh doanh - Tài chính'`, `subsystem='Kế toán'`, `kind='action'`.

| # | Code | Nhãn | platforms | Màn/chức năng |
|---|---|---|---|---|
| 1 | `accounting.ke_toan_phieu_thuong_kd.manage` | Kế toán — Phiếu thưởng kinh doanh | `['erp']` | Lập Phiếu thưởng kinh doanh |
| 2 | `accounting.ke_toan_phieu_loi_nhuan.manage` | Kế toán — Phiếu lợi nhuận | `['erp']` | Lập Phiếu lợi nhuận |
| 3 | `accounting.ke_toan_yc_hach_toan_bo_sung.manage` | Kế toán — Yêu cầu hạch toán bổ sung (phối hợp) | `['erp','hrm']` | Xem DS chờ duyệt + duyệt/lập phiếu loại 7 + thông báo + định tuyến ApprovalCenter |

> ⚠️ Nhãn #3 có hậu tố **"(phối hợp)"** để phân biệt với mã sẵn có `accounting.ke_toan_kho_yc_hach_toan_bo_sung.manage` (vai kế toán **kho**, đích thông báo — đợt tách trước). Hai mã, hai vai khác nhau trên cùng chứng từ.

## 6. Bản đồ gate (file:dòng — đã verify tới gốc 2026-11-27)

### ERP (`ERP/TanPhatDev/app`) — 6 điểm
| Điểm | File:dòng | Hiện tại | Sửa thành |
|---|---|---|---|
| Lập Phiếu thưởng KD | `Http/Controllers/Accounting/BillBonusBusinessController.php:112` | `can('accounting.ke_toan.manage')` | `...ke_toan_phieu_thuong_kd.manage` |
| Lập Phiếu lợi nhuận | `Http/Controllers/IncomeExpenditure/BillProfitsController.php:132` | `can('accounting.ke_toan.manage')` | `...ke_toan_phieu_loi_nhuan.manage` |
| DS YC HTBS chờ duyệt (scope) | `Model/IncomeExpenditure/AdditionAccountingRequest.php:276` | `can('finance.ke_toan_thanh_toan.manage') \|\| can('accounting.ke_toan.manage')` | đổi operand 2 → `...ke_toan_yc_hach_toan_bo_sung.manage` (**giữ OR** với ke_toan_thanh_toan) |
| Duyệt YC HTBS loại 7 | `Model/IncomeExpenditure/AdditionAccountingRequest.php:520` (`canApproveSupport`) | `can('accounting.ke_toan.manage')` | `...ke_toan_yc_hach_toan_bo_sung.manage` |
| Thông báo YC HTBS cần duyệt | `Services/Sale/Firm/Settlement/SettlemenHandleAdditionalAccountingService.php:244` | `sendNotifyWithToDiffrentCompanyPermission('accounting.ke_toan.manage', …)` | `...ke_toan_yc_hach_toan_bo_sung.manage` (giữ nguyên người nhận hiện tại nhờ lệnh cấp-lại) |
| Dashboard "Đề nghị thu tiền chờ duyệt" | `Http/Controllers/HomeController.php:1422` | `can('finance.ke_toan_thanh_toan.manage') \|\| can('accounting.ke_toan.manage')` | **BỎ HẲN** operand 2 → chỉ còn `finance.ke_toan_thanh_toan.manage` (quyết định đã chốt: mục thu tiền không thuộc 3 chứng từ trên) |

### HRM (`HRM/hrm-api`) — 1 sửa, phần còn lại lan tự động
| Điểm | File:dòng | Sửa |
|---|---|---|
| Hằng quyền DUYỆT loại 7 | `Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequest.php:239` | `const PERMISSION_ACCOUNTANT_SUPPORT = 'accounting.ke_toan_yc_hach_toan_bo_sung.manage';` |
| (lan tự động — đọc hằng theo tên, KHÔNG sửa) | `:343` scope pending · `:716` `canCreateAccountingBill` · `:749` `isSupportAccountant` · `Services/AdditionAccountingRequestService.php:146` · `ApprovalCenter/Definitions/Finance/AdditionAccountingRequestDefinition.php:59,141` | — |
| GIỮ NGUYÊN (ngoài phạm vi) | `:242 PERMISSION_NOTIFY_TARGET` (đã là `ke_toan_kho_yc_hach_toan_bo_sung`) | không đụng |

> Divergence đã biết (không phải lỗi ta tạo): sau tách, **ERP** thông báo YC HTBS theo mã mới `ke_toan_yc_hach_toan_bo_sung` (giữ đúng người nhận hiện tại), còn **HRM** thông báo theo mã `ke_toan_kho_yc_hach_toan_bo_sung` (do đợt kế toán kho đã đổi `:242`). Ghi nhận, không sửa ở feature này.

### Catalog + cấp lại + deprecate
- `hrm-api/app/Support/Permissions/Catalog/accounting.php`: **thêm 3 mã** (#1 `['erp']`, #2 `['erp']`, #3 `['erp','hrm']`), mỗi mã có `legacy` phù hợp (kế thừa tên cũ nếu cần để không 403 trước khi cấp).
- **Lệnh cấp-lại** `rbac:grant-ke-toan-split` (clone `rbac:grant-ke-toan-kho-split`): 1→3, idempotent (md5 chữ ký), `--dry-run/--verify/--report-dir`; copy pivot `role_has_permissions` + `employee_has_permissions` của `accounting.ke_toan.manage` sang 3 mã mới (giữ scope/company).
- **Deprecate** `accounting.ke_toan.manage`: **BƯỚC CUỐI** — sau khi cả ERP + HRM live và `grep` xác nhận 0 gate còn dùng mã cũ → gỡ khỏi Catalog, `catalog-sync` đặt `deprecated_at`.

## 7. Thứ tự rollout (prod — user tự chạy, không chạy hộ)
1. Deploy code (ERP + HRM) → `~/build_tpe.sh` tự `catalog-sync` (3 mã mới vào DB).
2. `php artisan rbac:grant-ke-toan-split --dry-run` (soát số) → chạy thật → `--verify`.
3. Sau khi xác nhận live + grep sạch → gỡ mã cũ khỏi Catalog, deploy lại để `catalog-sync` deprecate.

## 8. Còn lại cho builder
- Slug/nhãn chính xác có thể tinh chỉnh khi lập plan (giữ nguyên quy ước §5).
- Test DB-free soi source cho từng điểm re-point (mẫu `HrmKeToanKho*` của đợt trước); lệnh cấp-lại có test idempotent.
- Playwright/kiểm tay là bước nghiệm thu của user, không bắt buộc trong plan.
