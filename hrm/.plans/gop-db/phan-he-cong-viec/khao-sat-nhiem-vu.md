# Khảo sát Nhiệm vụ hiện có (03/11/2026, nhánh `gop_db`)

Nguồn: `hrm-api/Modules/Assign/Entities/Task/*`, `TaskResource`, `DetailTaskResource`; `hrm-client/pages/assign/tasks/index.vue`,
`components/CreateTaskModal.vue` (3.479 dòng), `components/ImportResultModal.vue` (2.335 dòng), `components/comments/*`.

## 1. Trường dữ liệu (`tasks`)
| Nhóm | Trường | Ghi chú |
|---|---|---|
| Định danh | `code` | `{công ty}.TASK.{KH\|NB}.{yy}.{nnnn}` |
| | `task_type` | 1 Nhiệm vụ chung · 2 Nhiệm vụ cụ thể (bắt buộc) |
| | `title`, `description` | Tên công việc * |
| Ngữ cảnh | `project_id` (Dự án/Nhóm), `solution_id` + `solution_version_*`, `solution_module_id` + `module_version_*` (Hạng mục), `meeting_id` / `meeting_report_id` | |
| Người | `assignee_id` (Người thực hiện *), `approver_id` (Người duyệt kết quả), `created_by`, watchers (`task_watchers`) | |
| Thời gian | `start_date` *, `due_date` *, `due_time` (Giờ hạn) *, `estimated_hours` (Số giờ được giao *) | |
| Trạng thái | `status` (10 trạng thái), `priority` (Bình thường / Cao / Khẩn cấp, BE trả màu) | |
| Kết quả | `result_text`, `actual_hours`, `progress_percent` / `progress_pct`, `performance_percent`, `submitted_at`, `approved_at`, `approved_by`, `reject_reason`, `completed_at` | |
| Khác | `weight` (trọng số KPI), `mode` (1 đơn giản / 2 nâng cao), `parent_id`, `recurring_parent_id`, `batch_id`, `sort_order` | |
| Con | `task_checklists` (content, is_done, result_note) · `task_children` (title, assignee, due, status) · `task_attachments` · `task_tags` · `task_links` (FS / SS / FF / SF / RL) · `task_recurring_rules` (lặp ngày / tuần / tháng / năm, kết thúc: không / đến ngày / sau n lần) · `task_progress_report_rules` (báo cáo theo ngày / tuần / tháng + giờ gửi) · `task_result_progress_logs` (report_date, hours, progress_pct, note) · `task_result_attachments` · `task_histories` · comments | |

## 2. Quyền (code thật)
- `canEdit` = **người tạo** và không có nhiệm vụ con. `canDelete` = người tạo **và trạng thái Nháp**.
- `canImportResult` = **người làm** và trạng thái Chờ bắt đầu / Đang thực hiện / Từ chối kết quả.
- `canApprove` = duyệt triển khai (quyền `assign.trien_khai_task.approve` + quản lý phòng ban người làm) hoặc duyệt kết quả (đúng `approver_id`).
- Đổi trạng thái: `getAllowedNextStatuses()` (đã mô phỏng trong mockup).
- `deadline_state_text`: "Quá hạn" khi qua `due_date + due_time` với mọi trạng thái **trừ** Nháp / Hoàn thành / Huỷ — tức **Hoàn thành - Chờ duyệt vẫn bị tính quá hạn**.

## 3. Popup hiện tại
- **2 popup khác nhau tuỳ trạng thái**: Nháp / Chờ phê duyệt / Chờ bắt đầu / Từ chối triển khai → `CreateTaskModal` (xem / sửa); Đang thực hiện → Huỷ → `ImportResultModal` (Kết quả). Cùng 1 nhiệm vụ, đổi trạng thái là đổi giao diện.
- `CreateTaskModal` cỡ XL, toàn màn: đầu popup có mã + tiêu đề + trạng thái + nhãn "Đơn giản / Nâng cao", nút **Chế độ nâng cao**, **Xoá trắng**, Đóng.
  - Cột trái: Loại nhiệm vụ *, Tên công việc *, Giải pháp, Dự án/Nhóm, Hạng mục, Meeting, Người thực hiện *, Trạng thái, Mức độ ưu tiên, Ngày bắt đầu *, Hạn hoàn thành *, Giờ hạn *, Mô tả, Số giờ được giao *; nâng cao thêm Checklist, Nhiệm vụ con, Tệp đính kèm (bảng: tên, loại, file, dung lượng), Bình luận.
  - Cột phải (nâng cao), 2 tab: **Thiết lập** (Người duyệt kết quả, Người theo dõi, Thẻ, Lặp lại, Yêu cầu báo cáo tiến độ) · **Liên kết & KPI** (Liên kết nhiệm vụ).
  - Cuối: Lịch sử (thu gọn), Lưu / Lưu & Tiếp tục.
- `ImportResultModal`: thông tin nhiệm vụ + **Kết quả thực hiện** (Số giờ được giao, Số giờ làm thực tế *, Tiến độ (%) *, Hiệu suất, Kết quả thực hiện *) hoặc **Nhật ký tiến độ theo ngày / tuần / tháng** khi có quy tắc báo cáo; Checklist, Nhiệm vụ con, Tệp.
- Danh sách: bấm mã mở popup xem; hàng nút Sửa · Xoá · ⋮ (Nhập kết quả, Duyệt, Lịch sử). Đổi trạng thái = chọn trong ô Trạng thái của form rồi Lưu.

## 4. Điểm chưa tốt (cơ sở cho đề xuất)
1. Hai popup theo trạng thái → người dùng mất phương hướng; nút "Nhập kết quả" và "Xem" dẫn tới 2 nơi.
2. Xem = form khoá (ô input xám) → khó đọc, mỗi lần sửa 1 trường phải vào chế độ Sửa cả form.
3. Công tắc Đơn giản / Nâng cao giấu Checklist, Người duyệt, Tệp… → người xem không biết nhiệm vụ có hay không.
4. Đổi trạng thái qua ô chọn + Lưu, không có nút hành động theo vai trò.
5. Popup che toàn màn, mất ngữ cảnh danh sách.
6. Người làm không có đường đề nghị đổi hạn (chỉ người tạo sửa được hạn).
