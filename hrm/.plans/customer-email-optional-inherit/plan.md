# Plan — Email KH: bỏ bắt buộc + kế thừa vào báo giá + cho sửa tay

## Phase 1 — BE bỏ required Email KH
- [x] `ProspectiveProjectRequest.php:44`: `required|email` → `nullable|email`
- [x] `MeetingCreateApiRequest.php:94`: `required|email` → `nullable|email`
- [x] `MeetingUpdateApiRequest.php:118`: `required|email` → `nullable|email`
- [x] php -l 3 file (sạch)

## Phase 2 — FE dự án TKT bỏ dấu * Email
- [x] `CustomerBlock.vue:107`: label Email bỏ `:required` (bỏ dấu *)

## Phase 3 — Báo giá: email editable + payload
- [x] `quotations/_id/edit.vue`: ô Email → V2BaseInput bound `item.customer_email`, disable khi !canEdit
- [x] `quotations/_id/edit.vue`: `customer_email` vào payload (dùng chung create + update)
- [x] Kế thừa: đã có (`selectProject` gán customer_email)

## Phase 4 — BE báo giá nhận customer_email
- [x] `QuotationService::create` (dòng 92): `array_key_exists('customer_email',$data) ? $data[...] : $project->customer_email`
- [x] `QuotationService::update` `$updatable`: thêm `customer_email`
- [x] `QuotationStoreRequest` + `QuotationUpdateRequest`: thêm rule `customer_email`
- [x] **FIX task note trước**: thêm `products.*.note` vào 2 request (validated() đang loại note → note không lưu qua save FE; BOM dùng input() nên OK)
- [x] php -l (sạch)

## Phase 5 — Verify
- [x] BE: dự án TKT validate email rỗng → PASS (nullable)
- [x] BE: QuotationUpdateRequest validated() giữ customer_email + products.*.note (tinker)
- [x] UI: form dự án TKT label "Email khách hàng" KHÔNG còn dấu * (Playwright)
- [x] UI: form báo giá — Email là input editable (không disable), kế thừa sẵn từ dự án; đổi tay + Lưu nháp → DB lưu `kh2-edited@tanphat.com`
- [x] E2E note (fix task trước): QuotationService::update giữ note qua saveDirectProduct → DB (tinker)
- [x] Dọn artifact test (quotation 2 note=NULL, email về kh2@gmail.com)

---
### Checkpoint — 2026-07-06
Vừa hoàn thành: Toàn bộ Phase 1-5. Email KH không bắt buộc (dự án TKT + báo giá + meeting), báo giá kế thừa + cho sửa tay. Kèm FIX gap validation note của task product-project-note-sync.
Đang làm dở: (không)
Bước tiếp theo: User verify browser + test tạo báo giá mới (chọn dự án → email tự điền → sửa/để trống → lưu).
Blocked:
