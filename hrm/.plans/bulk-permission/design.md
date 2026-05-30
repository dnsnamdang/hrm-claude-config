# Design — Phân quyền hàng loạt (tóm tắt)

**Spec đầy đủ**: [docs/superpowers/specs/2026-05-27-bulk-permission-design.md](../../docs/superpowers/specs/2026-05-27-bulk-permission-design.md)

## Mục tiêu
Cho phép admin **cấp** hoặc **thu hồi** một tập permission cho nhiều NV cùng lúc, lọc theo Khối / Phòng ban / Bộ phận / Chức vụ / Chức danh + NV bổ sung + NV loại trừ.

## Scope
- Popup mở từ `/timesheet/setting/roles` (button "Phân quyền hàng loạt").
- Cấp/thu hồi permission trực tiếp NV qua `model_has_permissions` (spatie), scope `current_company`.
- KHÔNG đụng Role hiện có. Role + RBAC giữ nguyên.

## Quyết định cốt lõi
1. Song song với Role, không thay thế.
2. Cộng dồn: quyền NV = Role ∪ permission trực tiếp.
3. Hai action: grant / revoke (radio button trên popup).
4. State checkbox lưu **excluded list** (Set), không lưu "đã chọn".
5. Filter đổi → giữ excluded, hiện banner "Đang loại trừ N — [Xóa loại trừ]".
6. Tick-all header chỉ phạm vi trang hiện tại.
7. UI dùng V2Base.
8. **Defer lịch sử** (#10455) — phase sau.

## Out of scope phase này
- Lịch sử phân quyền.
- Queue async cho bulk lớn.
- Bulk-remove role.
