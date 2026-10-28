# Plan — YCLĐBG: Cần khảo sát mặt bằng (#11723)

**Người phụ trách:** @junfoke — 2026-10-27
Tóm tắt: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-10-27-ycldbg-khao-sat-mat-bang-design.md`

## Phase 1 — ERP (`TanPhatDev`, nhánh `gop_db`)
- [x] Đọc issue + file BA (sheet "1-Tạo PYC", "2_xemchitiet", "Lịch sử update" dòng 9)
- [x] Migration thêm `need_site_survey` (đã chạy local bằng `--path`)
- [x] Model: fillable + cast integer
- [x] Controller `store()`: nhận `need_site_survey`
- [x] FormRequest: `required|in:0,1` + rule bắt buộc file khi = Có (tính file cũ còn lại khi sửa)
- [x] View: radio Có/Không, `(*)` động cho File đính kèm, dòng lỗi riêng
- [x] Test local: bỏ trống → lỗi chọn; Có + không file → lỗi file; xem chi tiết phiếu cũ → radio trống, khoá
- [x] Test rule khi sửa (tinker, rollback): có file cũ → OK; xoá hết file cũ → lỗi; Không → OK
- [ ] Test trọn luồng tạo phiếu thật có file (chọn KH + HĐ) trên dev-erp
- [x] Commit + push `gop_db` (merge `task_11723`, `30aad08686`, 28/10)
- [ ] Chạy migration trên dev-erp / prod
- [ ] Báo QA trên Redmine #11723

## Phase 2 — HRM (khi port màn Yêu cầu lắp đặt bàn giao)
- [ ] Làm theo checklist spec mục 6 (BE rule + FE radio + show + test đối chiếu). KHÔNG tạo migration lại.

## Checkpoint — 2026-10-27
- **Vừa hoàn thành:** Phase 1 code ERP + test local (validate tạo mới qua UI, validate sửa qua tinker).
- **Đang làm dở:** —
- **Bước tiếp theo:** user review → commit `gop_db` TanPhatDev → migrate dev-erp → QA.
- **Blocked:** —

## Ngày 28/10/2026 (@junfoke)
- [x] 28/10/2026 — Merge `task_11723` vào `gop_db` TanPhatDev (`30aad08686`, đã push). Còn: migrate dev-erp / prod, test trọn luồng có file trên dev-erp, báo QA #11723.
- [x] 28/10/2026 — ERP `develop_02` (worktree `TanPhatDev/.worktrees/develop_02`): sửa lỗi `Trying to get property 'code' of non-object` (AssemblyRequestController.php:114) ở DS phiếu YC lắp đặt bàn giao khi KH/HĐ đã bị xoá → dùng `optional()`. Commit `a323e97c3c`, đã push `develop_02`.
- [ ] Bản sửa trên chưa có ở `gop_db` (cherry-pick nếu cần); hàm xuất DS `AssemblyRequest.php:424-425` còn cùng kiểu lỗi, chưa sửa.
