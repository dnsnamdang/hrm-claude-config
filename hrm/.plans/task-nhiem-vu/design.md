# Design — Nhiệm vụ (Task): đổi tên + phân loại Nhiệm vụ chung / cụ thể

Redmine: http://quanly.dnsmedia.vn/issues/11453 — @cuong61n
Nhánh: `tpe` (worktree `HRM/worktrees/tpe-api` :8005 + `HRM/worktrees/tpe-client` :3005)
Spec chi tiết: `docs/superpowers/specs/2026-09-12-task-nhiem-vu-design.md`

## Mục tiêu

1. Đổi toàn bộ NHÃN hiển thị "Task" → "Nhiệm vụ" trên mọi màn của phân hệ Giao việc & Bàn giao
   (danh sách, modal tạo/sửa/chi tiết, tab Task trong Giải pháp / Hạng mục / Dự án TKT / Công việc của tôi,
   báo cáo, bản in, file Excel, thông báo chuông).
2. Thêm trường bắt buộc **"Loại nhiệm vụ"**: `Nhiệm vụ chung` / `Nhiệm vụ cụ thể`.
   Nhiệm vụ chung cho chọn NHIỀU người thực hiện → khi lưu sinh ra N bản ghi nhiệm vụ độc lập
   (mỗi người 1 bản), theo dõi tiến độ/trạng thái riêng.

## Quyết định đã chốt (2026-09-12)

| Vấn đề | Chốt |
|---|---|
| N bản ghi sinh ra có liên kết nhau không | **Có** — thêm cột `batch_id` (UUID) ghi cội nguồn cùng 1 lần giao việc |
| Dữ liệu cũ trong DB | Migration set toàn bộ `task_type = 2` (Nhiệm vụ cụ thể) |
| Màn Sửa của nhiệm vụ sinh từ Nhiệm vụ chung | Chỉ chọn 1 người thực hiện; ô Loại nhiệm vụ hiện nhưng **disabled**, không cho đổi loại sau khi tạo |
| Tên quyền trong DB ("Xem danh sách task theo công ty"…) | **GIỮ NGUYÊN** cả `name` lẫn `display_name` + group `Task` |
| Mã tự sinh `TPE.TASK.NB.26.0001` | **GIỮ** `.TASK.` |
| Phần phụ khi sinh N bản ghi (checklist, tệp, người theo dõi, thẻ, nhiệm vụ con, lặp lại, báo cáo tiến độ) | **Copy nguyên** sang cả N bản ghi |
| Vị trí ô "Loại nhiệm vụ *" | Đầu form, trên "Tên công việc"; mặc định **Nhiệm vụ cụ thể** |
| Cột + bộ lọc "Loại nhiệm vụ" ở màn danh sách | **Có** (ngoài phạm vi task Redmine, bổ sung để phân loại dùng được) |
| Nhiệm vụ chung ở chế độ phức tạp (lặp lại, báo cáo tiến độ) | **Cho phép**, copy nguyên sang từng bản ghi |

## Giải pháp kỹ thuật

- 2 cột mới trên bảng `tasks`: `task_type` (tinyint, 1=chung / 2=cụ thể, default 2) + `batch_id` (varchar 36, nullable, index).
  KHÔNG dùng `parent_id` sẵn có vì cột đó đang gánh logic nhiệm vụ con (trọng số `weight`, cộng dồn tiến độ)
  — nhét nhiệm vụ chung vào sẽ làm sai tiến độ ở các màn báo cáo.
  KHÔNG tạo bảng `task_batches` riêng (YAGNI — chưa có yêu cầu sửa/xoá hàng loạt theo lô).
- `TaskService::store()` tách phần tạo 1 task thành `createSingleTask()`, khi `task_type = 1` thì sinh `batch_id`
  và lặp `assignee_ids` tạo N task đầy đủ. Controller đã bọc sẵn `DB::transaction`.
- Sau khi sinh xong, N bản ghi là nhiệm vụ bình thường → mọi màn danh sách, báo cáo, phân quyền theo cấp,
  thông báo chạy nguyên như cũ, không phải sửa.
- Đổi nhãn: sửa tay theo danh sách khảo sát. GIỮ NGUYÊN route `/assign/tasks`, tên component/biến/class CSS,
  `itemable_type === 'Task'`, tên quyền, mã `.TASK.`.
