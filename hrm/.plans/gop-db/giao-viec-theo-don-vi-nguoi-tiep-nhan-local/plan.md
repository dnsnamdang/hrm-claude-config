# Giao việc theo đơn vị — điều tra "Phòng ban này chưa có người tiếp nhận" + cấp quyền local (@cuong61n)

Hỗ trợ cho feature "Giao việc theo đơn vị" (spec gop-db/2026-11-21-giao-viec-theo-don-vi, `WorkAssignScope`). Không sửa code.

## Phase 1 — Điều tra + dữ liệu local (2026-11-25)

- [x] 2026-11-25 Lần code câu báo đỏ ở form Tạo nhiệm vụ (`TaskForm.vue` → `unitReceiversMixin` → API `assign/work-assign/receivers` → `WorkAssignScope::receivers`). Kết luận: chặn nghiệp vụ có chủ đích — người tiếp nhận của phòng D = NV đang làm, có mã `assign.giao_viec_nhan_su_phong_ban.assign` ở công ty của D VÀ quản lý D (`employee_manage_departments` hoặc cờ `all_department`). Mã cấp nào chỉ tính cho đơn vị cấp đó, không lùi lên phòng.
- [x] 2026-11-25 Kiểm DB local `local_hrm_erp` (API :8000 và :8003 cùng DB): phòng HN_KD2 "PHÒNG THIẾT BỊ Ô TÔ 2" (id 5, cty 1) đã có 8 người quản lý (namdangit all_department, Trần Ngọc Duy…), nhưng 2 mã quyền `giao_viec_nhan_su_*` chưa cấp cho vai trò nào → receivers rỗng.
- [x] 2026-11-25 Cấp 2 mã (`..._phong_ban.assign` + `..._bo_phan.assign`, scope NULL như quyền action khác) cho vai trò `TPE_Super admin` (id 18) và `TPE_Giám đốc kinh doanh` (id 100050) bằng SQL `insert ignore role_has_permissions`. Kiểm bằng tinker `WorkAssignScope::receivers(5, null)` → 7 người: 13 DNS Admin, 34, 35 Trần Ngọc Duy, 36, 224, 883, 1084. Chỉ DB local, không đụng dev/prod.
- Ghi nhớ cho dev/prod: mã mới chưa ai có → phải cấp ở `/admin/roles` rồi gắn phòng quản lý ở `/admin/employee-roles`, không thì mọi phòng đều báo "chưa có người tiếp nhận".

## Phase 2 — Dev lệch phiên bản FE/BE + deploy (2026-11-25)

- [x] 2026-11-25 Điều tra lỗi 422 (`assignee_id: Bắt buộc phải nhập`, `status: Không hợp lệ`) khi tạo Nhiệm vụ giao cho phòng Quản trị thông tin trên dev-hrm. Nguyên nhân: client dev (`develop`) đã merge gop_db lúc 14:54 (có form đơn vị), còn API dev (`develop` commit 14:22) chưa có `TaskStoreRequest::isUnitMode` → rule cũ đòi người đích danh, không nhận trạng thái Chờ phân công.
- [x] 2026-11-25 Merge `origin/gop_db` → `develop` hrm-api (worktree tạm, 93 file; 1 conflict `Issue.php` 2 dòng `use` → giữ cả hai; `php -l` sạch). Push `develop` = `17e6df081`.
- [x] 2026-11-25 Deploy dev bằng tay đúng bước backend của `~/build_tpe.sh` (bỏ build FE vì client đã mới): pull · migrate 5 migration (chat_polls ×2, issues.assigned_by, tasks unit_assign, workspaces.allow_outside_assignee) · route:cache · permission:catalog-sync → có mã 105100/105101.
- [x] 2026-11-25 Cấp 2 mã `giao_viec_nhan_su_*` cho vai trò `TPE_Super admin (DNS DÙNG)` (id 18) trên DB dev. Kiểm tinker `receivers(36, null)` phòng HN_QTTT → 6 người (13 namdangit, 34, 144, 224, 493, 883). Chờ user thử lại form tạo Nhiệm vụ trên dev.
