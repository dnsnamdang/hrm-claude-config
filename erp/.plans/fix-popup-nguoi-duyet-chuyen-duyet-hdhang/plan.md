# Fix: Popup "Người duyệt" (chuyển duyệt) ở duyệt HĐ hãng không hiện dữ liệu

Nhánh: `gop_db` (ERP TanPhatDev)

## Bối cảnh
- Màn: duyệt hợp đồng hãng, thao tác "chuyển duyệt" (gọi ở màn hỗ trợ hạch toán).
- Popup "Người duyệt" có filter "Lọc theo chức vụ" + search "Mã hoặc họ tên", bảng STT/Mã/Họ tên/Chức vụ/Phòng ban → hiện "Không có dữ liệu" (0 mục).
- Nghi ngờ liên quan gộp DB (offset role +100000 / guard) như các ca [[gopdb-signer-role-id-not-offset]], [[gopdb-can-guard-duplicate-permission-first-bug]].

## Task
- [x] T1 — Tìm code: popup `partials/modals/searchEmployee.blade.php` + JS `searchEmployeeJs.blade.php` (route `searchEmployee` → `Common\SearchController@searchEmployee:91`) → `Employee::withPermissionCompany` (Employee.php:2619). Type='Ban giám đốc duyệt hợp đồng', level=2. `$company_id`=công ty người TẠO HĐ (FirmContractController:572).
- [x] T2 — Root cause XÁC NHẬN (read-only DB): `withPermissionCompany` lọc `role_has_permissions.company_id = auth()->user()->info->company_id` (công ty ĐANG CHỌN của kế toán), KHÔNG phải công ty HĐ. `search_company_id` truyền vào nhưng bị comment (SearchController:156-159). Verify: impersonate kế toán cty 1 → popup 8 NV (đúng cty nhà); nhưng HĐ chờ duyệt thuộc cty 1/2/4/8, nếu kế toán chọn cty khác/không grant → RỖNG; nếu khác cty HĐ → SAI người. Fix lọc theo cty HĐ: cty4→3NV, cty2→4NV, cty8→2NV (đúng giám đốc từng cty). KHÔNG phải lỗi guard-duplicate (perm 100847 chỉ 1 bản web).
- [x] T2b — ROOT CAUSE THẬT (từ URL request user cấp): màn phụ lục `firm-contracts-addition-annexes/28331/support-accounting` gửi `type=Duyệt hợp đồng` (KHÔNG phải "Ban giám đốc..."). Permission `Duyệt hợp đồng` bị TRÙNG TÊN 2 guard: id=1141 api (0 role_has_permissions, mồ côi) + id=100041 web (43 grants). `Permission::where(name)->first()` (Employee.php:2622) lấy id=1141 api → `whereIn([])` → RỖNG cho MỌI người/công ty. Đúng họ [[gopdb-can-guard-duplicate-permission-first-bug]]. Verify impersonate Nguyễn Đức Tuân (emp 24, cty 1): first()=api→0 NV; fix guard=web→26 NV.
- [x] T3 — FIX ĐÃ ÁP: thêm `->where('guard_name','web')` vào `Permission::where('name',$permissions)->first()` trong `withPermissionCompany` (Employee.php:2622). `php -l` OK. Chỉ sửa code, KHÔNG đụng DB.
- [x] T4 — Commit + push `gop_db`: commit `e1b59a2d37` → rebase lên `origin/gop_db` (84fbcf74dc) → push `1438bac700`. Cần DEPLOY để ăn thật.

- [x] T5 — AUDIT toàn ERP `Permission::where('name',...)->first()` không guard (user yêu cầu). Kết quả:
  - `hasAnyPermission` (Employee.php:1437) — ĐÃ FIX (session trước)
  - `withPermissionCompany` (Employee.php:2622) — ĐÃ FIX (session này)
  - **`FirmContract::userHasHidePricePermission` (827)** — ĐANG VỠ THẬT: 'Xem hợp đồng ẩn giá' TRÙNG (api 1571 rhp=0 / web 101037 rhp=1), first()=api → luôn trả false → user có quyền vẫn KHÔNG xem được giá ẩn. CẦN FIX.
  - `withPermissionRole` (Employee.php:741) — cùng mẫu, dùng id→role_has_permissions; tên hiện dùng (Duyệt giá hàng hoá/chỉ tiêu/kế hoạch) đều WEB-ONLY → CHƯA vỡ, fix phòng ngừa.
  - `canInCompany` (Employee.php:1476) — cùng mẫu; tên hỏi giá/tính giá đều WEB-ONLY → CHƯA vỡ, fix phòng ngừa.
  - Không còn biến thể khác (grep whereName/Role by name = 0 thật).
- [x] T6 — Áp guard fix cho CẢ 3 chỗ (user chốt "b"). Thêm `->where('guard_name','web')` + comment GOP_DB vào:
  - `FirmContract::userHasHidePricePermission` (827) — chỗ VỠ THẬT ('Xem hợp đồng ẩn giá' api 1571 mồ côi / web 101037).
  - `Employee::withPermissionRole` (741) — phòng ngừa.
  - `Employee::canInCompany` (1476) — phòng ngừa.
  - `php -l` cả `app/Employee.php` + `app/Model/Sale/Firm/Contract/FirmContract.php` → OK. Chỉ sửa code, KHÔNG đụng DB. CHƯA commit (chờ user yêu cầu).

### Checkpoint — 2026-09-25
Vừa hoàn thành: T6 — áp guard fix cả 3 chỗ (FirmContract:827, Employee:741, Employee:1476), lint OK.
Bước tiếp theo: chờ user yêu cầu commit + push gop_db (chưa commit theo quy tắc ERP).
Blocked: —
  - Ghi chú phụ (KHÔNG phải lỗi báo cáo): withPermissionCompany lọc theo cty đăng nhập kế toán thay vì cty HĐ — vấn đề riêng, không gây rỗng ở màn này, chưa đụng.

## Ràng buộc
- Chỉ ĐỌC DB server `hrm_erp_gop`; KHÔNG ghi.
- `submitApprove`/hàm dùng chung → hỏi ý kiến trước khi sửa.
