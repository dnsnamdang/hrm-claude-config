# Khai tử chuỗi chức năng Chi phí lắp đặt gắn với `App\Contract` (ERP)

**Ngày:** 2026-11-28 · **Trạng thái:** đã chốt scope, đang thực thi · **Không commit/push.**

## Ý định (why)
User (chủ nghiệp vụ) xác nhận chuỗi chức năng lắp đặt gắn với `App\Contract` **không còn dùng từ lâu**:
InstallRequest → InstallPlan → InstallSummary → InstallEstimate / InstallAdvance.
Yêu cầu: **khai tử hết nếu gắn với Contract**. Ràng buộc nguyên văn:
- "có thể không cần xoá url" → **KHÔNG xoá route/URL**.
- "tôi không muốn thấy quyền liên quan xuất hiện trong việc chọn quyền" → **HARD REQ**: 4 mã quyền của chuỗi phải biến khỏi picker `/admin/roles`.
- Phạm vi mã: user chọn **"Cả 4 mã"** (AskUserQuestion).

Thẩm quyền: user biết tình hình dùng thật ở prod mà code không thể hiện; đã chấp nhận quyền quyết định của user, không tranh luận màn còn sống hay không.

## Goals
1. 4 mã quyền của chuỗi KHÔNG còn xuất hiện trong UI chọn quyền.
2. Các màn của chuỗi không còn lối vào từ thao tác bình thường ("khai tử").
3. Không vỡ luồng lắp đặt đang sống (`assemblyRequest`/`AssemblyRequest`).
4. Không làm đỏ bộ test RBAC.

## Non-goals / Anti-goals
- KHÔNG xoá route/URL (user cho phép giữ).
- KHÔNG xoá các lời gọi `can()` trong model InstallEstimate/Advance/Plan/Summary (fail-closed tự nhiên — xem dưới).
- KHÔNG sửa `Contract.php` (gate `canInstallEstimate()` tự fail-closed; file lớn, tránh rủi ro).
- KHÔNG đổi `code` mã đã lên prod; gỡ quyền = gỡ khỏi Catalog để sync đặt `deprecated_at`, KHÔNG xoá dòng DB.
- KHÔNG gộp DB / không rollout trong task này.

## 4 mã quyền (đều ĐỘC QUYỀN cho chuỗi chết — đã grep tới gốc, không caller khác)
| Mã | Tên | Chỉ dùng ở |
|---|---|---|
| `accounting.de_nghi_tam_ung_chi_phi_lap_dat.approve` | Duyệt đề nghị tạm ứng chi phí lắp đặt | InstallAdvance |
| `accounting.chi_phi_lap_dat.approve` | Kiểm soát chi phí lắp đặt | InstallEstimate |
| `customer_care.du_toan_chi_phi_lap_dat.create` | Dự toán chi phí lắp đặt | Contract (canInstallEstimate) |
| `customer_care.lap_dat.manage` | Quản lý lắp đặt | InstallPlan + InstallSummary (+ middleware route summary) |

## Cách làm (the how)
### A. Picker (HARD REQ) — sửa chéo repo hrm-api (file Catalog DÙNG CHUNG)
Gỡ 4 entry khỏi `hrm-api/app/Support/Permissions/Catalog/{accounting,customer_care}.php`.
Sau `php artisan permission:catalog-sync`, 4 mã bị đặt `deprecated_at` → `validCodes()` loại → picker không hiện. (Dòng DB giữ nguyên, không xoá.)

### B. Khai tử lối vào — sửa ERP (`TanPhatDev`)
Gỡ 3 nút thao tác (datatable/controller action-column):
- `app/Datatables/Sale/ContractDatatable.php` — nút "Dự toán chi phí lắp đặt".
- `app/Http/Controllers/Tech/InstallSummaryController.php` — nút "Đề nghị tạm ứng chi phí" (→ InstallAdvance.create).
- `app/Http/Controllers/Tech/InstallRequestController.php` — nút "Giao lịch" (→ InstallPlan.create).

### C. An toàn prod — đã kiểm tới gốc (`PermissionCode.php`)
- `validCodes()` = regex AND `permissions.code` với `deprecated_at IS NULL`. Mã deprecate ⇒ "không hợp lệ".
- `ensure()` ở **production chỉ log + trả `false` (fail-closed), KHÔNG 500**; chỉ `local`/`testing` mới ném `UnknownPermissionCode`.
- `Auth::user()->can()` đi qua `PermissionChecker::has()/allows()` = **"thuần dữ liệu, không kiểm mã hợp lệ"** → KHÔNG ném kể cả env testing; mã deprecate không có trong `grants` (join `whereNull(deprecated_at)`) → trả `false`.
- ⇒ Giữ route + giữ `can()` trong màn chết = **tự fail-closed an toàn** ở prod. install_summaries có middleware `checkPermission:customer_care.lap_dat.manage` → sau deprecate là **403 toàn màn** (cascade khai tử thêm). install_requests/plans/estimates/advances không middleware → vào URL được nhưng mọi action fail-closed.

### D. Test — đã kiểm tới gốc, KHÔNG động fixture
Fixture MAP ERP (`tests/Feature/Rbac/Concerns/{Accounting,CustomerCare}Catalog.php`) là **seed test DB** để code ERP còn tham chiếu 4 mã không bị `ensure()` ném; nó mirror "mã code còn tham chiếu", **không phải** "mã còn trong picker", và **không đọc file Catalog hrm-api**. Code ERP vẫn tham chiếu 4 mã (route/model giữ nguyên) ⇒ **phải GIỮ NGUYÊN 4 dòng fixture**, nếu gỡ sẽ làm đỏ `CustomerCareScopeConversionTest`/`AccountingScopeConversionTest`. hrm-api không có test nào tham chiếu 4 mã này.

## Approaches đã cân nhắc
1. **(Chọn)** Gỡ 4 entry Catalog + gỡ 3 nút lối vào; giữ route/model/fixture. Ít rủi ro nhất, đạt đủ 2 goal, test xanh.
2. Gỡ cả route + `can()` trong model + fixture. Bị loại: user bảo "không cần xoá url"; đụng nhiều file lớn; dễ làm đỏ test; không thêm lợi ích (đã fail-closed).
3. Chỉ gỡ Catalog, không gỡ nút. Bị loại: nút `canAdvance()`/`canApprove()` không gate theo quyền (chỉ theo trạng thái) vẫn có thể hiện → chưa "khai tử hết".

## Kiểm chứng (deletion task, không RED-GREEN)
Đây là task GỠ BỎ, không sinh hành vi mới → không TDD RED-GREEN. Xác minh:
- `php -l` 3 file ERP sửa.
- grep: 4 mã KHÔNG còn trong 2 file Catalog; 3 chuỗi nút KHÔNG còn trong 3 file ERP.
- grep: fixture MAP vẫn còn đủ 4 mã (không bị động).
- (nếu chạy được) suite RBAC ERP + catalog test hrm-api xanh.
