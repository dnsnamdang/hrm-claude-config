# Phủ hết màn duyệt — nhóm Công việc (tổng hợp A+B+C) — @cuong61n

Chi tiết: phu-het-cong-viec-A.md (assign_request, task), -B.md (solution, issue), -C.md (kiểm kê + bàn giao/giảm giá/điều chỉnh GP).

## Loại mới đợt 2 (8) — đều verify 0 chênh lệch, đột biến bị bắt
assign_request (đề xuất công tác, BE không chốt quyền → theo giao diện) · task_start_approval · task_result_approval · solution (cấp 1 PM, cấp 2 Leader) · issue · solution_adjustment_request (BE không chốt quyền) · handover_item · discount_type.

## Bỏ (kèm bằng chứng)
solution_module (không có trạng thái chờ riêng; Leader duyệt hạng mục = cấp 2 solution; hồ sơ hạng mục đã có) · yêu cầu lắp đặt bàn giao (HRM chỉ tab hàng đợi + in: Routes/api.php:1320-1327; menu-sidebar.js:266 không link) · biên bản bàn giao nghiệm thu, BOM list, yêu cầu XD giá (chỉ send, api.php:587-596), duyệt bình luận task, my-todo/my-job (xem -C.md) · job_request status 3 (chỉ lập chứng từ kế tiếp) · các màn "Phiếu duyệt KQ…" (assign_job_approve_result/index.vue:428 status 6; assign_approve_result/index.vue:461 status 7) chỉ là danh sách đã duyệt.

## Chuyển nhóm khác
CSKH: handover-records (approve), assign-other-requests (reject), reject-reception. Tài chính/Kho: YC xuất hàng reject/manager-approve (Routes/api.php:794-801), đề nghị xuất kho cancel (846), phiếu xuất hàng deny (886-887) — chưa có Definition.
