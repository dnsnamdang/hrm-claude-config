# Auto-fill chỉ khi còn đúng 1 option — Dự án tiền khả thi

**Người phụ trách:** @namdang · **Module:** Assign · **Ngày:** 2026-06-04

## Mục tiêu
Màn `/assign/prospective-projects/add`, ở cả 2 luồng "Chọn theo Nhóm ngành" và "Chọn theo Lĩnh vực KH": khi chọn 1 dropdown, các dropdown còn lại **chỉ tự điền nếu chỉ còn đúng 1 option**; nhiều option thì để trống cho người dùng tự chọn (thay vì luôn lấy giá trị đầu tiên `[0]` như hiện tại).

## Quyết định chính
- Áp dụng cho **tất cả** điểm auto-fill (chọn Ứng dụng / Nhóm giải pháp / Nhóm LVKH / Lĩnh vực KH).
- Auto-fill **lan truyền đến khi ổn định**: fill 1 field xong, nếu field khác nhờ đó còn 1 option thì fill tiếp.
- Chỉ fill field **đang trống**, không ghi đè lựa chọn người dùng đã chọn tay.
- Gom về 1 method chung `autoFillSingleOptions()`, tận dụng các computed options sẵn có.
- Giữ nguyên `pruneInvalidCascade()`, backend, UI.

## Phạm vi
- **Chỉ FE**, 1 file: `hrm-client/pages/assign/prospective-projects/components/ProjectInfoSection.vue`.
- Backend không đổi.

## Spec chi tiết
`docs/superpowers/specs/2026-06-04-prospective-project-autofill-single-option-design.md`
