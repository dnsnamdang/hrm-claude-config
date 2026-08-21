# PL8 — Phân vùng "Lịch sử" ở màn Xem chi tiết

Redmine: [#10814](http://quanly.dnsmedia.vn/issues/10814) · Nhánh: `tpe-develop-assign` (cả hrm-api + hrm-client)
Spec chi tiết: `docs/superpowers/specs/2026-08-06-pl8-thong-tin-he-thong-design.md`

## Mục tiêu

Thống nhất 9 màn Xem chi tiết của phân hệ Giao việc / QLDA TKT:

1. Số phiếu (mã) hiển thị nổi bật trên tiêu đề màn chi tiết.
2. Cuối màn có phân vùng **Lịch sử** — lịch sử phiếu (người tạo/sửa/duyệt/hủy duyệt + thời gian + phòng ban + ghi chú), **mặc định thu gọn**, bấm nút mới hiện.
3. Màn chi tiết có đủ action như ngoài màn danh sách.

9 đối tượng: Dự án TKT · Yêu cầu giải pháp · Hạng mục dự án · BOM Giải pháp · Báo giá · Lịch meeting · Task · Issue · Phiếu bàn giao.

## Quyết định chốt

| # | Quyết định |
| --- | --- |
| 1 | UI lịch sử theo **timeline** giống `TaskHistoryModal` (chấm màu theo hành động, diff cũ đỏ → mới xanh), bổ sung Tài khoản (mã NV – tên) · Phòng ban · Ghi chú |
| 2 | 1 component FE dùng chung `components/assign/SystemInfoSection.vue`, dùng được cho cả trang chi tiết lẫn modal |
| 3 | 1 endpoint BE chuẩn hoá `GET assign/system-logs/{type}/{id}`, adapter đọc **log sẵn có** của từng entity — không migrate dữ liệu cũ |
| 4 | 3 entity chưa có log (Lịch meeting, Hạng mục dự án, Yêu cầu giải pháp) → **không tạo bảng mới**, dựng log từ cột audit sẵn có (created_by/updated_by/closed_by + lý do hủy) |
| 5 | Phòng ban lấy theo phòng ban **hiện tại** của nhân viên (log cũ không snapshot) |
| 6 | Không thêm quyền mới: vào được màn chi tiết là xem được lịch sử |
| 7 | Lazy load: chỉ gọi API khi người dùng bấm mở phân vùng lần đầu |
| 8 | Màn mẫu = **Báo giá** (đúng màn trong ảnh Redmine), duyệt UI xong mới nhân bản |

## Nguồn log theo entity

| Đối tượng | Bảng log | Ghi chú |
| --- | --- | --- |
| Báo giá | `quotation_histories` | đã có endpoint `histories`, đủ action + note |
| BOM Giải pháp | `bom_list_logs` | action/content/actor_id/meta |
| Phiếu bàn giao | `handover_logs` | cùng shape BOM |
| Task | `task_history` | old/new JSON — có diff trường |
| Issue | `issue_history` | old/new JSON |
| Dự án TKT | `prospective_project_status_logs` | chỉ log đổi trạng thái |
| Lịch meeting · Hạng mục dự án · Yêu cầu giải pháp | *(chưa có)* | dựng từ cột audit của chính bản ghi |

## Phân đợt

- **Phase 1 (mẫu)** — màn Báo giá: endpoint chuẩn hoá + component + tiêu đề mã phiếu + rà action.
- **Phase 2 (xong)** — Dự án TKT, Yêu cầu giải pháp, BOM, Lịch meeting, Phiếu bàn giao (5 trang chi tiết).
- **Phase 3 (xong)** — Task, Issue, Hạng mục dự án (nhúng vào modal xem chi tiết).

> Tiêu đề phân vùng hiển thị là **"Lịch sử"** (chốt ngày 06/08/2026); nút "Lịch sử" ở footer màn chi tiết đã bỏ vì trùng chức năng.
