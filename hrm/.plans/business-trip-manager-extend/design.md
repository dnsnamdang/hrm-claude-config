# Manager gia hạn / kết thúc sớm phiếu công tác theo quyền — Tóm tắt

**Mục tiêu:** User có quyền `315 - "Gia hạn, kết thúc sớm phiếu công tác"` được tạo phiếu gia hạn/kết thúc sớm
cho phiếu giao công tác của nhân sự thuộc phòng ban/bộ phận/công ty mình quản lý. Logic giống self-flow.

**Quyết định chính:**
- Target: chọn **từng nhân sự cụ thể** trong phiếu (per-employee).
- Luồng duyệt: **vẫn chờ duyệt** (status=1) — y hệt self-flow.
- UI: màn **Quản lý phiếu đi công tác** (`index.vue`) — nút row + modal manager riêng.
- Phạm vi quản lý: tái dùng `listManageEmployeeInfoIds(false, null, true)`.
- Gate quyền: kiểm tra trong **controller** (`isCurrentEmployeeHasPermission('Gia hạn, kết thúc sớm phiếu công tác')`),
  KHÔNG dùng middleware vì tên quyền có dấu phẩy.
- Self-flow + middleware dùng chung: **giữ nguyên**.

**Spec chi tiết:** `docs/superpowers/specs/2026-06-24-business-trip-manager-extend-design.md`

**Phụ trách:** @manhcuong
