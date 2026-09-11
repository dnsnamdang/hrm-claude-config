# Tiến trình nội bộ dự án TKT — 12 bước theo 2 luồng (Redmine #11426)

Người phụ trách: @cuong61n · Nhánh `tpe` (worktree `HRM/worktrees/tpe-api` :8005 + `tpe-client` :3005)

## Mục tiêu
Cập nhật trường "Tiến trình nội bộ" (`prospective_projects.status`, 12 bước) theo bảng
"Tiến trình dự án con / dự án độc lập nội bộ - QTTT - 10/09". Áp cho dự án con + dự án độc lập, dự án cha giữ nguyên.

## Hiện trạng (đã rà 2026-09-11)
- 12 bước đã có ở `ProspectiveProject::STATUS`, nhảy bước tự động 1→8 và 11 đã đúng spec.
- 2 luồng có/không giải pháp đã tách bằng cờ `has_solution` (không có GP thì không tạo được Solution → đi thẳng 2→6).
- Tên bước bị hard-code 6 nơi (BE entity, blade export, FE constants.js, progressOptions ×4, manager.vue, ChildrenTab).
- Chốt giải pháp / Chốt báo giá chưa bắt buộc file. "Yêu cầu bổ sung thông tin" chưa kéo dự án về bước 2.
- Bước 9, 10, 12 chưa có code set.

## Quyết định đã chốt
- Gom tên bước về BE (`status_name` + `status_color`), FE bỏ hard-code. Sửa kèm lỗi dự án cha sai tên ở filter/export.
- TH2 + TH3 đã gộp → không thêm ô chọn trường hợp, dùng checkbox "Có giải pháp" lúc tạo dự án.
- File chốt: bắt buộc, nhiều file, lưu bảng `files` chung, hiện lại ở chi tiết dự án (khối Giải pháp / tab Báo giá).
- Lịch sử tiến trình: giữ NGUYÊN bảng `prospective_project_status_logs` (user chốt 2026-09-11 không thêm cột text). Mọi chỗ đổi bước phải qua model (`changeStatusById`) để hook ghi log — cấm query builder `->update(['status'])`.
- Bước 9, 10, 12, 11b (HĐ hủy → tự đóng dự án): NGOÀI phạm vi, để task sau.

## Tài liệu
- Mô tả dễ hiểu từng bước + thao tác chuyển: `mo-ta-tien-trinh-noi-bo.md`
- Spec chi tiết: `docs/superpowers/specs/2026-09-11-prospective-project-status-12-steps-design.md`
