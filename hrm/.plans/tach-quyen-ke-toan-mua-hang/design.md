# Tách quyền `accounting.ke_toan_mua_hang.manage` thành 3 mã theo màn — Design

**Ngày:** 2026-11-27
**Phạm vi:** ERP (TanPhatDev) — không đụng HRM lần này (file Phiếu tính giá bên HRM đang do session khác sửa).
**Mẫu kế thừa:** task chị em `tach-quyen-ke-toan` (`accounting.ke_toan.manage` → 3 mã, đã ✓dev+push). Xem memory `hrm-erp-tach-quyen-ke-toan-3-ma-done`.

---

## 1. Ý đồ & lý do (why)

Quyền `accounting.ke_toan_mua_hang.manage` ("Kế toán mua hàng") là **quyền-cờ vai trò nghiệp vụ** gắn rải trên **3 màn ERP không liên quan nhau**. Admin nhìn tên quyền không biết nó mở màn nào, và muốn cho một người chỉ duyệt Phiếu tính giá thì buộc phải cấp luôn cả quyền trên màn Tờ khai hải quan + YC nhập theo đơn.

**Mục tiêu (user chốt):** tách sao cho **nhìn tên quyền là biết nó tác dụng ở màn nào** — mỗi mã = một màn.

## 2. Hiện trạng — footprint của mã cũ (đã kiểm tới gốc)

`grep -rn "ke_toan_mua_hang" app resources routes` → **14 chỗ**, gom thành 3 nhóm màn + dashboard/menu:

### Nhóm A — Phiếu tính giá (`PriceCalculateRequest`)
Mã cũ làm **người duyệt Phiếu tính giá**: xem + duyệt + từ chối + nhận thông báo.
- `app/Model/Order/PriceCalculateRequest.php:373` — `canShow()` (xem phiếu không phải nháp)
- `:385` — `canApprove()` (`status == CHO_DUYET && can(...)`)
- `:390` — `canReject()` (`status == CHO_DUYET && can(...)`)
- `:405` — `send()` `Notification::sendNotifyWithPermission("...", route('PriceCalculateRequest.show', ...), ...)`
- `app/Model/Order/PriceCalculate.php:300` — `canView()` scope
- `app/Model/Order/PriceCalculateResult.php:150` — trong `canView()` (hàm bắt đầu `return true;` nên dòng này là **dead code**, re-point cho nhất quán)

### Nhóm B — YC nhập theo đơn / Tổng hợp chi phí nhập khẩu (`OrderImportRequest`, route `orderImportRequest`)
Mã cũ **thật sự duyệt** YC nhập theo đơn (người duyệt phụ): xem + duyệt + nhận thông báo + widget dashboard + menu.
- `app/Model/Warehouse/OrderImportRequest.php:698` — `canView()`, là **1 toán hạng OR** cạnh `accounting.ke_toan_kho_yc_nhap_theo_don.manage` và các scope khác → chỉ thay toán hạng mua_hang, **GIỮ toán hạng kho**.
- `:723` — `canApprove()` (`status == 2 && can(...)`)
- `:731` — `send()` `Employee::withPermission('...', Auth::user()->info->company_id)`
- `app/Http/Controllers/HomeController.php:1347` — widget dashboard "Tổng hợp chi phí nhập khẩu chờ duyệt", link `route('orderImportRequest.index').'?type=approve'`
- `resources/views/layouts/topmenubar.blade.php:2243` — menu "Tổng hợp chi phí nhập khẩu cần duyệt" → `orderImportRequest.index?type=approve`
- `resources/views/layouts/topmenubar_old.blade.php:2767` — menu cũ "Duyệt phiếu" → `orderImportRequest.index?type=approve`

> **Đính chính so với đề xuất ban đầu:** dashboard + 2 menu này trỏ `orderImportRequest` (màn nhóm B), KHÔNG phải Phiếu tính giá → thuộc nhóm B.

### Nhóm C — Tờ khai hải quan (`CustomDeclaration`)
Mã cũ ở đây **chỉ cho XEM + nhận thông báo**, **KHÔNG duyệt**.
- `app/Model/Warehouse/CustomDeclaration.php:544` — `canView()`, **1 toán hạng OR** cạnh `accounting.ke_toan_kho_to_khai_hai_quan.manage` → chỉ thay toán hạng mua_hang, **GIỮ toán hạng kho**.
- `:583` — `send()` `Employee::withPermission('...', $this->company_id)`
- ⚠️ `canApprove()` `:575` dùng `purchase.to_khai_hai_quan.approve` — **KHÔNG phải mua_hang, KHÔNG đụng**. Đây là lý do mã #3 đặt tên "Xem", không phải "Duyệt".

### Ngoài phạm vi (không đổi)
- `app/Model/Common/Dashboard.php:9` — `'KE_TOAN_MUA_HANG' => 'Kế toán mua hàng'` là **nhãn nhóm widget** (chuỗi hiển thị), giữ nguyên.
- HRM: module `Modules/MasterData/Services/PriceCalculation/*` dùng "Kế toán mua hàng" chỉ là **chuỗi nhãn bản in**, KHÔNG phải gate quyền → không đụng (và đang do session khác sửa).

## 3. Phương án (approaches)

- **PA-A (chọn): 3 mã riêng từng màn.** Mỗi mã chỉ làm đúng việc mà mã cũ làm trên màn đó. Grant command copy pivot từ mã cũ → cả 3 mã nên **không ai mất quyền**. Mã cũ giữ nguyên tới khi deprecate ở bước cuối. → Đạt mục tiêu "nhìn tên biết màn".
- **PA-B: gộp B/C vào mã `ke_toan_kho_*` sẵn có.** BÁC. `ke_toan_kho_yc_nhap_theo_don`/`ke_toan_kho_to_khai_hai_quan` là quyền **toàn màn kho** (rộng hơn hẳn phần mua_hang làm) → cấp cho holder mua_hang hiện tại sẽ **over-grant** cả màn kho. Không an toàn.
- **PA-C: giữ 1 mã, chỉ đổi tên.** BÁC. Vẫn 1 mã cho 3 màn → không đạt mục tiêu.

**Quyết định: PA-A** (user đã chốt "theo đề xuất").

## 4. 3 mã mới (Catalog `hrm-api/app/Support/Permissions/Catalog/accounting.php`)

Chèn ngay **sau** block `accounting.ke_toan_mua_hang.manage` (sau dòng 541). Tất cả: `subsystem_group='Kinh doanh - Tài chính'`, `subsystem='Kế toán'`, `feature='Kế toán'`, `kind='action'`, `scopes=[]`, `depends_on=[]`, `platforms=['erp']`, `legacy=[]`.

| # | code | name | Màn | mua_hang làm gì ở đó |
|---|------|------|-----|----------------------|
| 1 | `accounting.ke_toan_phieu_tinh_gia.manage` | **Kế toán — Phiếu tính giá** | PriceCalculateRequest | xem + duyệt + từ chối + thông báo |
| 2 | `accounting.ke_toan_duyet_yc_nhap_theo_don.manage` | **Kế toán — Duyệt YC nhập theo đơn** | OrderImportRequest (THCPNK) | xem + duyệt + thông báo + widget + menu |
| 3 | `accounting.ke_toan_xem_to_khai_hai_quan.manage` | **Kế toán — Xem tờ khai hải quan** | CustomDeclaration | xem + thông báo (KHÔNG duyệt) |

## 5. Bản đồ re-point ERP (giữ đúng-giữ đủ, không rộng hơn mã cũ)

| Mã mới | File:dòng | Cách sửa |
|--------|-----------|----------|
| #1 | PriceCalculateRequest.php:373,385,390,405 | thay `ke_toan_mua_hang`→`ke_toan_phieu_tinh_gia` |
| #1 | PriceCalculate.php:300 | thay |
| #1 | PriceCalculateResult.php:150 | thay (dead code, cho nhất quán) |
| #2 | OrderImportRequest.php:698 | thay **toán hạng** mua_hang, giữ `ke_toan_kho_yc_nhap_theo_don` + scope |
| #2 | OrderImportRequest.php:723,731 | thay |
| #2 | HomeController.php:1347 | thay |
| #2 | topmenubar.blade.php:2243 | thay |
| #2 | topmenubar_old.blade.php:2767 | thay |
| #3 | CustomDeclaration.php:544 | thay **toán hạng** mua_hang, giữ `ke_toan_kho_to_khai_hai_quan` |
| #3 | CustomDeclaration.php:583 | thay |

Không đụng: CustomDeclaration.php:575 (`purchase.to_khai_hai_quan.approve`), Dashboard.php:9.

## 6. Fixture RBAC ERP (BẮT BUỘC — bẫy đã biết)

Thêm 3 mã mới vào `tests/Feature/Rbac/Concerns/AccountingCatalog.php` `const MAP` dạng `'<code>' => [[], []],`. Nếu thiếu → suite RBAC ERP ném `UnknownPermissionCode` vì seed bảng `permissions` test từ fixture MAP (mirror tay), không qua `catalog-sync`. Xem memory `erp-rbac-fixture-map-must-seed-new-codes`.

## 7. Lệnh cấp-lại (grant) — không ai mất quyền

Clone `rbac:grant-ke-toan-split` (`hrm-api`):
- `app/Support/Permissions/KeToanMuaHangSplitMap.php` — `OLD_CODE='accounting.ke_toan_mua_hang.manage'`, `newCodes()` = 3 mã trên (đúng thứ tự Catalog).
- `app/Console/Commands/RbacGrantKeToanMuaHangSplitCommand.php` — signature `rbac:grant-ke-toan-mua-hang-split`, report dir `storage/app/rbac-grant-ke-toan-mua-hang-split/...`. Logic y hệt bản mẫu (copy pivot `role_has_permissions` + `employee_has_permissions` từ mã cũ → 3 mã mới, idempotent, `--dry-run/--verify/--report-dir`, tiền kiểm thiếu/deprecate mã → exit 1).

## 8. Test DB-free (mirror `KeToanSplit*`)

Trong `hrm-api/tests/Unit/Permission/`:
- `KeToanMuaHangSplitScan` (helper `erpSource()` đọc file ERP qua đường dẫn tương đối — tái dùng/clone `KeToanSplitScan`).
- `KeToanMuaHangSplitRbacFixtureTest` — assert fixture ERP `AccountingCatalog.php` chứa cả 3 mã mới.
- Test scan từng điểm re-point: PriceCalculate* chứa mã #1 & không còn mua_hang; OrderImportRequest + HomeController + 2 blade chứa mã #2; CustomDeclaration chứa mã #3; và CustomDeclaration vẫn còn `purchase.to_khai_hai_quan.approve` (không bị đụng nhầm).
- Dùng `PHPUnit\Framework\TestCase` (không DB).

## 9. Deprecate mã cũ — BƯỚC CUỐI

Chỉ sau khi: re-point xong + test xanh + `grep -rn "ke_toan_mua_hang" app resources routes tests` chỉ còn chuỗi nhãn `Dashboard.php:9`/`KE_TOAN_MUA_HANG` (không còn gate). Khi đó mới gỡ/deprecate `accounting.ke_toan_mua_hang.manage` khỏi Catalog. **Lần này để lại bước deprecate cho sau cùng** (giống task chị em: giữ mã cũ tới khi rollout prod xong). Quyết định deprecate ngay hay chờ rollout → chốt lúc thực thi.

## 10. Rollout prod (user tự chạy, không trong phạm vi code)

deploy → `permission:catalog-sync` (qua `~/build_tpe.sh`) → `rbac:grant-ke-toan-mua-hang-split --dry-run` → thật → `--verify` → cấp 3 mã ở `/admin/roles` → sau live + grep sạch mới deprecate mã cũ.

## 11. Ràng buộc chung (Global Constraints)

- Không commit/push (chưa có yêu cầu).
- Không chạy lệnh ghi DB prod (user tự chạy catalog-sync/grant/deprecate).
- ERP = Laravel 6, `.env` local trỏ prod DB — **không chạy lệnh ghi DB** khi test local.
- Quyết định nghiệp vụ "duyệt vs xem" bám đúng code gốc (mã #3 chỉ xem).

---

## Quyết định đã chốt
- PA-A (3 mã riêng từng màn), ERP-only. — user "theo đề xuất" 2026-11-27.
- Mã #3 = "**Xem** tờ khai hải quan" (không "Duyệt") vì mua_hang ở CustomDeclaration chỉ xem+thông báo. — phát hiện khi kiểm gốc, chốt trong design.
- Dashboard + 2 menu THCPNK thuộc **mã #2** (không phải #1). — kiểm gốc.
