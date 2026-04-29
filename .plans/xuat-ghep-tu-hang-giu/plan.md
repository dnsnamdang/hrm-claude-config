# Plan: Xuất ghép từ hàng giữ (TanPhatDev)

## Trạng thái
- Bắt đầu: 2026-04-28
- Tiến độ: brainstorming dở dang — đã chốt 7 quyết định, còn 6 câu hỏi (Q6→Q11)

## Phase 0: Brainstorming
- [x] Khám phá context (join_export_requests, prepick_transfer2, product_imports, stockOfProducts API, export_prepick_qty pattern)
- [x] Chốt Q1-Q5: hiển thị, validation, cascade nhập ghép (A), customer per-parent (B), hạn giữ (c), xuất thẳng (a)
- [ ] Q6: customer_id cấp nào (parent/recipe/cả 2) + cascade >1 customer
- [ ] Q7-Q11: validation hạn giữ, approval, pending lock, popup filter, edit/cancel
- [ ] User duyệt design final

## Phase 1: Backend (TBD sau brainstorming)
- [ ] Migration thêm `from_prepick_detail_id` + `customer_id`
- [ ] `JoinExportRequestsController` validation + syncProducts
- [ ] Cascade customer_id sang `warehouse_export_request`
- [ ] `ProductImportsController` xử lý tab phân bổ giữ cho type=8
- [ ] `ProductExport` xuất thẳng tạo prepick_detail mới

## Phase 2: Frontend YCXG (TBD)
- [ ] `join_export_requests/form.blade.php` thêm 3 cột
- [ ] `JoinExportRequest` class — gọi API stockOfProducts
- [ ] Popup chọn prepick_detail + enforce per-parent customer

## Phase 3: Frontend Nhập ghép (TBD)
- [ ] `product_imports/form.blade.php` thêm nhánh `ng-if="form.type == 8"` cho tab phân bổ giữ
- [ ] Editable hạn giữ với default config

## Phase 4: Test & wrap up (TBD)
- [ ] Manual test luồng thường + xuất thẳng
- [ ] Kiểm tra không chạm 3 nhánh tab phân bổ cũ

## Checkpoint
### Checkpoint — 2026-04-28 (paused)
Vừa hoàn thành: chốt Q1-Q5 (hiển thị tồn/giữ qua API, validation `qty ≤ in_stock + prepick_qty`, cascade A, per-parent customer B, hạn giữ default = `today + max_prepick_date`, xuất thẳng a — tái sử dụng pattern `export_prepick_qty/hold_qty/total_qty` + FIFO consume).
Đang làm dở: Q6 — customer_id cấp nào + cascade khi YCXG có >1 customer.
Bước tiếp theo: User trả lời Q6 → tiếp Q7-Q11 → propose 2-3 approaches → present design → viết plan tasks chi tiết.
Blocked: chờ user reply Q6.
