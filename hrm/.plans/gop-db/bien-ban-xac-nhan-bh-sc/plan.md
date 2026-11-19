# Biên bản xác nhận BH - SC (ERP `warrantyReport`) — KHÔNG PORT (@khoipv)

## Khảo sát — 2026-11-05

- [x] Khảo sát màn ERP `warrantyReport.index` (Bán hàng › Lắp đặt - BH - SC, link không tham số) — kết luận: **luồng chết, user chốt bỏ, không port**

Căn cứ:
- `warranty_reports` + chuỗi nguồn `warranty_requests` → `warranty_works` = **0 bản ghi** ở mọi DB local (gop_db, erp_new_11032026, erp_10022026, tp_219); bảng con `warranty_report_costs/descriptions/external_products`, `warranty_payment_requests` cũng 0.
- Không còn lối tạo: `create` bắt buộc `warranty_work_id`, mà Phiếu công việc BH (`warrantyWork`) không có mục menu và màn chi tiết của nó không có nút tạo biên bản.
- Code ERP hỏng: `update` ghi `description`, `cause_analysis`, `how_to_fix`… — các cột không có trong bảng `warranty_reports` → lỗi SQL; `searchByFilter` nhánh `type=all` gọi `whereHas('employees')` không tồn tại trên model.
- Luồng BH-SC đang chạy thật: Phiếu YC SC-BH (`warranty_repair_requests` 5.485) → Phiếu giao việc (`wr_assign_tasks` 14.661) → Phiếu nhập kết quả (`wr_import_results` 6.808).
- Menu HRM: `components/subsystem-menu/sale-hub.js:228` đã khai `'BB xác nhận BH - SC'` dạng chuỗi trần (bấm báo "đang phát triển") — giữ nguyên, không sửa.

### Checkpoint — 2026-11-05
Vừa hoàn thành: khảo sát + chốt không port
Đang làm dở:
Bước tiếp theo: không có (muốn gỡ hẳn mục menu thì xoá dòng `sale-hub.js:228` — chờ user yêu cầu)
Blocked:
