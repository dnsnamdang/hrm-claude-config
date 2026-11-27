# Import Excel phân quyền: hạ "Tổng công ty" → "Công ty" khi công ty chưa được cấp — plan

Báo 27/11/2026: xuất Excel quyền vai trò Trưởng phòng XNK (TPE, có phạm vi Tổng công ty) → import vào
Trưởng phòng XNK 1 (TPSG, công ty CHƯA được cấp phạm vi Tổng công ty) → dòng hiện "Tổng công ty" +
nhãn "Đang tính như Công ty". User muốn hiện luôn là "Công ty".

Nguyên nhân: `pages/admin/roles/_id/permissions.vue` `applyImport()` gán thẳng `item.scope` từ file, không
giới hạn theo `allowGroupScope` như `setOn()` (tick tay dùng `defaultScope(perm, 3)`).

## Tasks
- [x] `applyImport()`: công ty chưa được cấp (`!allowGroupScope`) mà file ghi Tổng công ty → lấy phạm vi lớn nhất ≤ Công ty
      của quyền; quyền chỉ có cấp Tổng công ty → không tick (giống tick tay), báo số dòng bị bỏ trong toast
- [ ] Kiểm trên màn (import file TPE vào vai trò TPSG) — chưa làm: tài khoản e2e local không có quyền màn vai trò; đã kiểm logic bằng Node
- [x] Commit/push hrm-client develop `6cfc04cba` + gop_db `a7d7217ac` (27/11/2026)

### Checkpoint — 2026-11-27 17:18 (wrap up cuối ngày)
Vừa hoàn thành: Code xong + ✓push hrm-client develop `6cfc04cba` + gop_db `a7d7217ac`; kiểm logic bằng Node.
Đang làm dở: Kiểm trên màn (import file TPE vào vai trò TPSG) — tài khoản e2e local không có quyền màn vai trò.
Bước tiếp theo: QA kiểm trên dev.
Blocked: Không
