# Plan — Chuẩn hoá button trong popup các màn Quản lý dự án TKT

Phụ trách: @namdangit

## Phase 1 — Rà soát (DONE)

- [x] FE: Rà 36 file popup của 8 màn QLDA (prospective-projects, request-solution, solutions, solution-modules, product-project, bom-list, pricing-requests, quotations) đối chiếu button-convention + modal-popup

## Phase 2 — Sửa vi phạm

### FE — prospective-projects
- [x] FormAnswerHistoryModal.vue: nút X →V2BaseIconButton; nút Đóng footer →tertiary size sm + #prefix fas fa-arrow-left
- [x] SolutionListModal.vue: nút Xem chi tiết trong bảng →V2BaseIconButton
- [x] formTabInput.vue: nút In (size + #prefix), nút Đóng (light→tertiary, icon fas fa-arrow-left, size, #prefix)
- [x] ProspectiveProjectQuotationsTab.vue: nút Hủy chốt thêm status=danger
- [x] SolutionAdjustmentTab.vue: bỏ no-close-on-backdrop (2 modal); nút Đóng light→tertiary (3 nút); thêm size các nút; icon Từ chối ri-close-circle-line

### FE — request-solution
- [x] FormTab.vue: nút In (size + #prefix); nút Đóng light→tertiary + fas fa-arrow-left + size + #prefix

### FE — solutions/manager + core
- [x] ModulesTab.vue: đổi thứ tự footer Lưu trước → Đóng cuối
- [x] HumanResourceTab.vue (solutions): hide-footer + tự viết modal-footer 2 V2BaseButton (Thêm nhân sự primary ri-user-add-line, Huỷ tertiary fas fa-arrow-left)
- [x] DetailListModal.vue: thêm modal-footer nút Đóng tertiary
- [x] TaskUpcomingModal.vue: nút bảng →V2BaseIconButton; thêm footer nút Đóng
- [x] PendingApprovalModal.vue: nút bảng →V2BaseIconButton; thêm footer nút Đóng
- [x] ModuleApprovalModal.vue: bỏ no-close-on-backdrop; Từ chối secondary→primary; sửa thứ tự 2 nhánh footer; icon Duyệt ri-check-line, Gửi ri-send-plane-line
- [x] SolutionApprovalModal.vue: bỏ no-close-on-backdrop; Từ chối thêm primary; sửa thứ tự 2 nhánh footer; icon Duyệt ri-check-line, Gửi ri-send-plane-line
- [x] IssueUpcomingModal.vue: nút Làm mới secondary→tertiary; nút bảng →V2BaseIconButton
- [x] CategoryLateTasksModal.vue: nút bảng →V2BaseIconButton
- [x] MeetingUpcomingModal.vue: nút Làm mới secondary→tertiary; nút bảng →V2BaseIconButton

### FE — solution-modules
- [x] HumanResourceTab.vue: hide-footer + tự viết modal-footer 2 V2BaseButton
- [x] PeopleLateTasksModal.vue: thêm footer nút Đóng tertiary
- [x] PendingApprovalModal.vue: nút bảng →V2BaseIconButton (icon Duyệt ri-check-line); thêm footer nút Đóng
- [x] TaskUpcomingModal.vue: nút bảng →V2BaseIconButton; thêm footer nút Đóng

### FE — bom-list
- [x] BomBuilderEditModal.vue: nút Đóng/Huỷ + fas fa-arrow-left; nút Lưu cập nhật + ri-save-3-line; đổi thứ tự footer
- [x] BomBuilderColumnModal.vue: nút Đóng + fas fa-arrow-left
- [x] BomBuilderSubBomModal.vue: nút Đóng + fas fa-arrow-left; nút Gộp + ri-merge-cells-horizontal
- [x] BomListLogModal.vue: nút Đóng light→tertiary + size
- [x] BomExportModal.vue: b-button→V2BaseButton (Huỷ tertiary + fas fa-arrow-left, Xuất Excel secondary + ri-download-line); đổi thứ tự
- [x] BomBuilderEditor.vue: nút Huỷ + fas fa-arrow-left; nút Lưu icon ri-save-line→ri-save-3-line; đổi thứ tự footer

### FE — quotations
- [x] _id/edit.vue: nút Thêm bind icon ri-add-line khi mode thêm (nhẹ)

## Phase 3 — Kiểm tra
- [x] Rà lại toàn bộ nút đã sửa, đảm bảo không lỗi cú pháp template

### Checkpoint — 2026-07-02
Vừa hoàn thành: Sửa toàn bộ vi phạm button trong ~23 file popup của 8 màn QLDA (7 fix-agent Opus song song). Verify: hết no-close-on-backdrop, hết light footer, hết btn-light bảng, hết b-button bom-list, hết type="primary"; thẻ V2BaseButton/IconButton cân bằng.
Đang làm dở: (không)
Bước tiếp theo: Test UI thực tế trên trình duyệt (Playwright) nếu cần trước khi merge.
Blocked:
