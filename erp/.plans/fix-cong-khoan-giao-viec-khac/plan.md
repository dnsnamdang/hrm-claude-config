# Fix: Công khoán đề xuất duyệt về 0 với "yêu cầu giao việc khác" (KQ bảo hành)

## Bối cảnh
Phiếu nhập KQ bảo hành (wr_import_results). Với nguồn giao việc = assign_other_request ("giao việc khác"), mục "Tính công dịch vụ đính kèm → Dịch vụ đính kèm" (revenue_costs) có "Công khoán đề xuất duyệt" = 0 (sai). Verify phiếu 7138: wr_assign_task_revenue_costs.rate_effort_approve = NULL, wr_import_result_costs.rate_effort_approve = 0.

## Nguyên nhân
1. Giao việc "khác" không lưu rate_effort_approve cho revenue_costs (form không có ô; WrAssignTaskRevenueCost.submit_data bỏ sót) → NULL.
2. KQ class WrImportResultCost: getter cố ý mặc định rate_effort_approve = rate_effort khi null, NHƯNG setter ép NULL→0 nên fallback không chạy → hiển thị/lưu 0.
(Chỉ assign_other_request dùng revenue_costs/WrImportResultCost nên chỉ nó dính.)

## Fix (WrImportResultCost.blade.php)
- Setter rate_effort_approve: value rỗng/null → giữ null (không ép 0).
- Getter: check null||undefined → fallback rate_effort.
- submit_data: rate_effort_approve chưa nhập → gửi rate_effort (ĐM công).

## Tasks
- [ ] Sửa 3 chỗ WrImportResultCost.blade.php
- [ ] User test tạo/nhập KQ giao việc khác: công khoán đề xuất = ĐM công
- [ ] (tuỳ) data-fix phiếu 7138 đã lưu 0
