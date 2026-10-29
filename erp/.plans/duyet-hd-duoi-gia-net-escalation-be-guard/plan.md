# Plan — Chặn duyệt HĐ "bán dưới giá net" ở BE (escalation guard)

## Bối cảnh
HĐ hãng 29072 (-2% dưới net) có quy chế #723 `change_approver=1` (phải chuyển duyệt BGD) nhưng
TP KD (emp 256) vẫn duyệt được. Điều tra (read-only, DB gộp hrm_erp_gop) kết luận:

1. **Trực tiếp**: emp 256 mang thêm role **Super Admin** → `Employee::hasRole()` (dòng 1382) short-circuit
   Super Admin = true cho MỌI role → `isRole('Giám đốc')`=true → `isBigBoss=true` ở FE → nút Duyệt hiện
   dù `change_approver=1`.
2. **Gốc/hệ thống**: điều kiện escalation CHỈ chặn ở FE (ẩn nút). `FirmContractController@approve()`
   KHÔNG kiểm `change_approver` → bất kỳ người quản lý phòng nào cũng duyệt được bất kể quy chế.

User chốt **Hướng A**: thêm chốt chặn THẬT ở BE trong `approve()`.

## Điều tra (xong)
- [x] Xác nhận quy chế đã lưu #723 `change_approver=1` ở `firm_support_accounting_departments` (is_main, phòng 36).
- [x] Xác nhận BE `approve()` không có guard `change_approver` (chỉ có guard "Doanh số vượt trội" dòng 670-672).
- [x] Xác nhận emp 256 có Super Admin (cty 1) → isBigBoss short-circuit.
- [x] Xác nhận guard mới sẽ CHẶN HĐ 29072 (requiresBgd=CÓ, 256 không phải BGD thật).
- [x] Cty 1 có 10 Giám đốc thật → chặn không làm kẹt hệ thống.

## Fix BE (code)
- [x] Thêm private helper `requiresBgdEscalation(FirmContract $c): bool` — mirror cổng FE:
      `switch_approve` HOẶC `support_accounting->department_main->regulation->change_approver`.
- [x] Thêm private helper `approverIsRealBigBoss($user, $companyId): bool` — kiểm role
      'Giám đốc'/'Ban Giám đốc' trực tiếp trên `employee_has_roles` theo cty HĐ, **KHÔNG** dùng
      `isRole()` (tránh short-circuit Super Admin).
- [x] Trong `approve()` nhánh duyệt hiệu lực (mode 2, `!$request->approver_id`, status→CO_HIEU_LUC):
      nếu `requiresBgdEscalation` && !`approverIsRealBigBoss` → `DB::rollBack()` + trả lỗi
      "Hợp đồng bán dưới giá net phải chuyển duyệt Ban giám đốc.".
- [x] `php -l` sạch.

## Quyết định đã chốt
- BGD thật = chỉ 2 role **'Giám đốc' / 'Ban Giám đốc'** (đúng 2 role cổng FE đang dùng), KHÔNG tính
  Super Admin / Quản trị hệ thống. Nếu user muốn thêm vai khác được vượt quy chế → chỉnh danh sách role.
- Phạm vi cty = **company_id của HĐ** (role gán theo cty trong `employee_has_roles`).
- Chỉ sửa controller `approve()` — KHÔNG đụng hàm dùng chung `hasRole()`.

## Chưa làm (chờ user)
- [ ] Siết FE `isBigBoss` (Hướng B) — chưa làm, chờ user yêu cầu thêm.
- [ ] Xử lý nghiệp vụ phiếu 29072 đã trót duyệt (thu hồi/duyệt lại) — chờ user.
- [ ] Deploy: code sửa trên repo, CHƯA test chạy thật (DB .env đang trỏ PROD gộp, chỉ SELECT).

## Checkpoint — 2026-10-07
Vừa hoàn thành: Hướng A xong — thêm guard escalation vào `FirmContractController@approve()`
(nhánh duyệt hiệu lực) + 2 helper `requiresBgdEscalation()` / `approverIsRealBigBoss()`; `php -l` sạch.
Guard: HĐ có quy chế `change_approver` (hoặc `switch_approve`) + người duyệt KHÔNG phải BGD thật
(role 'Giám đốc'/'Ban Giám đốc' trên `employee_has_roles` theo cty HĐ) → rollBack + trả lỗi.
Đang làm dở: để trống (code hoàn tất trên repo).
Bước tiếp theo (chờ user): deploy + test trên DB test (KHÔNG test trên .env prod gộp SELECT-only);
xử lý nghiệp vụ phiếu 29072 đã trót duyệt; cân nhắc Hướng B siết FE isBigBoss.
Blocked: để trống.
