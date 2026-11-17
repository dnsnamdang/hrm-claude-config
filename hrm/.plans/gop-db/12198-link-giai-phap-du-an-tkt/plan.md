# #12198 [PL01 - Dự án TKT] Bổ sung link mở chi tiết giải pháp (@junfoke)

Repo `hrm-client`, nhánh `task_12198` (tách từ `origin/gop_db`, worktree `.worktrees/12198-link-giai-phap`). Chỉ FE, id giải pháp đã có sẵn ở 2 chỗ.

## Ngày 17/11/2026 (@junfoke)
- [x] 17/11/2026 — Lỗi #12198: Danh sách dự án TKT — ô "Giải pháp" thành link "Mã - Tên" cùng kiểu ô Mã dự án, mở màn chi tiết giải pháp trong tab hiện tại (`prospective-projects/index.vue`, dự án chưa có giải pháp giữ như cũ); Quản lý dự án TKT › tab Giải pháp — ô "Mã giải pháp" thành link mở tab mới (`SolutionInfoTab.vue`). Kiểm ảnh local: YTG Vina → GP41, dự án 495.
- [x] 17/11/2026 — Đổi tên nhánh `feat/12198-link-giai-phap-du-an-tkt` → `task_12198` đúng quy ước (chưa push nên không ảnh hưởng server).
- [x] 17/11/2026 — Commit `904aa525c`, merge develop `33019e371` (đã push; merge trong thư mục tạm vì worktree develop có file dở của phiên khác). Chưa lên gop_db.
