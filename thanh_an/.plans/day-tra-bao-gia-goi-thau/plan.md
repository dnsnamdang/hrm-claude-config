# Đẩy trả báo giá / gói thầu — Plan

**Người phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-07-09-day-tra-bao-gia-goi-thau-design.md`

## Phase 1 — Backend

- [x] Migration: thêm `return_reason` (text null) + `returned_by` (unsignedBigInteger null) + `returned_at` (timestamp null) vào `quotations` + `bid_packages`; thêm vào `$fillable` 2 entity
- [x] `Quotation::canReturnRender()` + `BidPackage::canReturnRender()`
- [x] Route `PUT quotations/{id}/return-render` + `PUT bid_packages/{id}/return-render`
- [x] `QuotationController::returnRender` + `QuotationService::returnRender` (BG 9→1 group null; project →6 'Kế hoạch'; history; notification người tạo)
- [x] `BidPackageController::returnRender` + `BidPackageService::returnRender` (GT 4→2 group null; project →11 'Thầu'; quotation nguồn 18→8 'Thầu' khi project_type==1; TODO multi-quotation; history; notification NV thực hiện)
- [x] Clear 3 cột return khi gửi lại: `QuotationService::update()` (status→CHO_DUYET) + `BidPackageService::update()` (status→CHO_DUYET_KET_QUA)
- [x] Resources: `can_return_render` vào QuotationResource + BidPackageResource (list); `return_reason/returned_at/returned_by_name` vào 2 DetailResource

## Phase 2 — Frontend

- [x] `contract/quotation_render/index.vue`: nút Đẩy trả + modal lý do + handler
- [x] `contract/bid_package_render/index.vue`: nút Đẩy trả + modal lý do + handler
- [x] Banner lý do đẩy trả: `plan/quotation/_id/index.vue` + `bid_package/bid_package/_id/index.vue`
- [x] Banner lý do đẩy trả trên màn SỬA: `plan/quotation/_id/edit.vue` + `bid_package/bid_package/_id/edit.vue` (bổ sung theo yêu cầu sau wrap up; verify UI bằng dữ liệu tạm rồi revert — không side effect)
- [x] Dấu `*` đỏ trong modal đẩy trả (2 màn render): thay `label="Lý do đẩy trả *"` bằng slot label + `<Required />` — verify UI sao đỏ rgb(255,0,0); quy tắc đã ghi vào `docs/conventions.md` mục Quy tắc Frontend

## Phase 3 — Verify

- [x] Chạy migration (6 cột OK trên `quotations` + `bid_packages`)
- [x] Verify UI: đẩy trả BG-331 (banner ✅, notification chuông ✅, dự toán 268 về 6 'Kế hoạch' ✅, gửi duyệt lại clear banner + project về 3 ✅, `contract_manager_id` giữ nguyên ✅)
- [x] Verify UI: đẩy trả GT-336 (banner ✅, notification ✅, group_process NULL ✅, dự toán 245 về 11 'Thầu' ✅, BG nguồn 312 về 8 'Thầu' ✅, gửi duyệt KQ status 3 clear ✅ — bước gửi duyệt qua API vì record test thiếu field bắt buộc có sẵn, 422 không liên quan feature)
- [x] Edge: status đã đổi → 400 (cả 2) ✅; user không quyền → 400 ✅; lý do trống → FE chặn + API 422 ✅; log Laravel 09/07 không có lỗi ✅

## Checkpoint

### Checkpoint — 2026-07-09 12:20
Vừa hoàn thành: Toàn bộ 7 task (BE + FE + E2E verify) qua subagent-driven, mỗi task có review; 1 lỗi Critical (group_process không fillable ở BidPackage → mass-assign bị drop) đã sửa bằng gán trực tiếp + save().
Đang làm dở: (không) — feature hoàn thành, chờ user review + tự commit.
Bước tiếp theo: User review diff 2 repo (đã stage sẵn `git add -A`, CHƯA commit) rồi tự commit. Lưu ý minor tồn đọng: reason chưa escape trong title HTML notification (pattern giống rejectBid), 3 cột return client-writable qua PUT update chung (fillable), modal đóng trước khi API trả về (mất lý do nếu lỗi).
Blocked: (không)

**Side effects dữ liệu staging do test E2E:** BG-331: 9→2 (chờ duyệt), project 268: 12→3, GT-336: 4→3 (+bổ sung bid_opening_time/bid_closing_time/execution_time do record thiếu), project 245: 12→11, BG-312: 18→8. Lịch sử duyệt 2 chứng từ có thêm dòng "Đẩy trả về phòng trước"; 2 notification mới cho DNS Admin.
