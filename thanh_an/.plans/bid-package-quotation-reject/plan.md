# Plan — Từ chối lập gói thầu

> @khoipv — bắt đầu 2026-06-23
> Plan chi tiết: `docs/superpowers/plans/2026-06-23-bid-package-quotation-reject.md`

## Phase 0 — Brainstorming & Spec
- [x] Chốt yêu cầu qua brainstorming
- [x] Viết spec chi tiết
- [x] User review spec
- [x] Viết plan triển khai

## Phase 1 — Backend ✅ (review sạch 2026-06-23)
- [x] Task 1: Thêm const `Quotation::TU_CHOI_LAP_GOI_THAU=20`, `Project::TU_CHOI_LAP_GOI_THAU=19`
- [x] Task 2: Model `Quotation::canRejectBid()`
- [x] Task 3: Service `QuotationService::rejectBid()` (đổi status BG+DT + lịch sử + notification)
- [x] Task 4: Controller `rejectBid` + route `PUT /quotations/{quotation}/reject-bid`
- [x] Task 5: Expose `can_reject_bid` trong `QuotationResource`
- [x] Task 6: Cập nhật statusMap (QuotationController 20 ×3; ProjectController 19 ×3: detailReport/lifecycleReport/lifecycleDetail — plan ghi nhầm exportDetailReport)

## Phase 2 — Frontend ✅ (review sạch 2026-06-23)
- [x] Task 7: Nút + modal "Từ chối lập gói thầu" + status 20 trên `bid_package/quotation/index.vue`
- [x] Task 8: Nhãn trạng thái dự toán 19 trên `sale/project/index.vue`

## Phase 3 — Hoàn thiện nhãn cross-screen ✅ (từ final review, 2026-06-23)
> Final review phát hiện status 20/19 xuất hiện ở nhiều màn list/dashboard nhưng thiếu nhãn → hiển thị rỗng (spec mục 6 đã dự báo). Đã thêm nhãn label-only:
- [x] Báo giá (20): `plan/quotation/index.vue`, `plan/quotation/waiting-approve.vue`, `contractor/quotation/index.vue`, `contract/quotation_render/index.vue`
- [x] Dự toán (19): `plan/project/index.vue`, `bid_package/project/index.vue`
- [x] Filter báo cáo (19): `sale/detail-report/index.vue`, `sale/report-project-contract/index.vue`
- [x] Dashboard BE: `CategoryDashboardService::getAllQuotationStatusMapping()` thêm 20 vào nhóm "Không thực hiện"

## Phase 4 — Follow-up sau khi user verify (2026-06-23)
- [x] `plan/quotation/index.vue`: thêm `{ id: 20 }` vào mảng `statuses` (dropdown lọc trạng thái) — trước chỉ thêm getStatusText/colorMap, sót filter
- [x] `plan/quotation/_id/index.vue`: thêm alert hiển thị `reason_deny` khi `status == 20` (BE đã trả sẵn ở DetailQuotationResource:150)

## Phase 5 — Thêm chức năng từ chối ở màn bid_package/project (2026-06-23, theo yêu cầu user)
> Màn "Danh sách dự toán đã gửi thầu" — thao tác từ chối trên báo giá gắn với dự toán (item.quotation_id).
- [x] BE `ProjectResource`: thêm `can_reject_bid => $quotation->canRejectBid()` (tái dùng $quotation sẵn có dòng 37) — php -l PASS
- [x] FE `bid_package/project/index.vue`: nút "Từ chối lập gói thầu" (v-if can_reject_bid) gọi `showRejectModal(item.quotation_id)` + modal `modal-reject-bid` + data (rejectReason/rejectError/rejectQuotationId) + methods (showRejectModal/handleRejectBid → PUT category/quotations/{quotation_id}/reject-bid)

## Phase 6 — Từ chối lập gói thầu cho dự toán ĐI THẲNG vào thầu (2026-06-23)
> Phát hiện khi user test DT-227/2026: dự toán đi thẳng vào thầu ở **project status 7** (DA_GUI_THAU), KHÔNG có báo giá → nút cũ (gate theo quotation) không hiện.
> User chốt: chỉ thêm luồng cấp dự toán cho loại status 7; lưu lý do vào cột mới `reason_reject_bid` (migration).
- [x] Migration `add_reason_reject_bid_to_projects_table` (cột text nullable, không FK) — đã chạy migrate OK
- [x] `Project::canRejectBid()` = status==DA_GUI_THAU(7) && quyền 'Lập gói thầu'; thêm `reason_reject_bid` vào fillable
- [x] `ProjectController::rejectBid()` (validate reason, 403 nếu !canRejectBid, set status=19 + reason_reject_bid + rejected_by/at, notify người tạo dự toán) — php -l PASS
- [x] Route `PUT category/projects/{project}/reject-bid`
- [x] `ProjectResource`: thêm `can_reject_bid_project => $this->canRejectBid()`
- [x] FE `bid_package/project/index.vue`: nút v-if `can_reject_bid || can_reject_bid_project`; `showRejectModal(item)` chọn endpoint theo loại (project status 7 → projects/{id}/reject-bid; status 10 → quotations/{quotation_id}/reject-bid); dùng `rejectUrl`

## Phase 7 — Hiển thị lý do từ chối ở chi tiết dự toán (2026-06-23)
- [x] BE `DetailProjectResource`: thêm `reason_reject_bid`
- [x] FE `sale/project/_id/index.vue`: thêm alert đỏ khi `status == 19` (lý do + người từ chối + thời gian), mirror block status 17

## Minor findings (chưa sửa — cân nhắc sau)
- (không còn)
- FE `handleRejectBid`: khi API lỗi không `preventDefault()` → modal vẫn đóng (chỉ hiện toast lỗi). Nhất quán với luồng "từ chối phân công" sẵn có. Không bắt buộc.
- Class màu trạng thái mới: màn chính dùng `pj-status-rose`, các màn cross-screen dùng `pj-status-red` (đều đỏ, theo class sẵn có mỗi file). Nhỏ, không đồng nhất tuyệt đối.

## Checkpoint
### Checkpoint — 2026-06-23
Vừa hoàn thành: Toàn bộ BE + FE + nhãn cross-screen, đã review từng phase + final review end-to-end (sạch sau fix)
Đang làm dở: Không — chờ user verify UI thực tế
Bước tiếp theo: User test trên UI (từ chối 1 báo giá status "Đã gửi thầu" → kiểm tra báo giá rời list, dự toán + báo giá hiển thị nhãn "Từ chối lập gói thầu", notification tới người lập)
Blocked:
