# baogia-warning-zero-price — Plan

**Spec:** docs/superpowers/specs/2026-07-20-baogia-warning-zero-price-design.md
**Màn:** `/assign/quotations` — Gửi duyệt báo giá.

---

## Phase 1 — Backend: nới ràng buộc giá 0 + định tuyến auto/phân cấp

### BE (✅ implement + review Approved)
- [x] Rà `ensureAllPricesPositive()` + floor asserts: floor chỉ so cha≥con, KHÔNG chặn giá 0 → giữ nguyên
- [x] Nới `ensureAllPricesPositive()`: bỏ ném lỗi `quoted_price <= 0` (hàng hoá + dịch vụ)
- [x] Nới: bỏ ném lỗi hàng tạm `estimated_price <= 0`; GIỮ chặn "giảm giá vượt đơn giá bán"
- [x] Floor asserts: xác nhận không chặn ngầm giá 0 (giữ nguyên)
- [x] Thêm `isClean(Quotation)`: mọi hàng ERP + không dịch vụ + discount_method NULL + mọi quoted_price>0
- [x] Tách `doSelfApprove(Quotation)` dùng chung (selfApprove không đổi hành vi)
- [x] Sửa `submit()`: isClean → doSelfApprove `auto_approved=true`; ngược lại ngưỡng cũ `auto_approved=false` (mọi payload có auto_approved)
- [x] Thêm `submitCheck(Quotation)`: `{zero_price_items:[{code,name}], zero_price_count, is_clean}`
- [x] Controller `submitCheck()` + route `POST /{id}/submit-check` (không permission mới)

## Phase 2 — Frontend: cảnh báo 0đ + highlight cam + định tuyến

### FE (✅ implement + 2 vòng fix + review Approved)
- [x] Component `QuotationZeroPriceModal.vue` (b-modal, header/body/bảng SKU+Tên, nút cam, cờ `confirmed` chống back lạc)
- [x] `edit.vue` state `zeroPriceHighlight` + class `row-zero-price` (parent/child/service, `<=0`) + CSS cam
- [x] `edit.vue` store call `submit-check`
- [x] `edit.vue` `openSubmit()`: save → submit-check → popup nếu 0đ (back=dừng giữ màn / continue=đi tiếp) + cờ `submitInFlight` chống double-POST
- [x] `edit.vue` định tuyến `auto_approved` (auto: toast+redirect / not-clean: QuotationSubmitModal cũ)
- [x] **[Fix final-review]** Nới `save(strict)` (`validatePrices`+`badTotal`+viền đỏ inline): bỏ chặn giá 0 để popup mở được (AC2/3/4)

## Verify (khi user yêu cầu)
- [ ] AC1 báo giá sạch → auto-duyệt, không popup
- [ ] AC2 có dòng 0đ → highlight cam + popup danh sách đúng SKU/tên
- [ ] AC3 "Quay lại chỉnh sửa" → đóng popup giữ màn
- [ ] AC4 "Tiếp tục trình duyệt" → đi bước duyệt
- [ ] AC5 có hàng tạm/dịch vụ/GG → phân cấp (không auto)

---

## Checkpoint
### Checkpoint — 2026-07-20 (CODE DONE + REVIEW SẠCH)
Vừa hoàn thành: Toàn bộ Phase 1 BE + Phase 2 FE (subagent-driven Opus). Mỗi phase qua implementer→reviewer→fix→re-review + 1 vòng review tổng whole-branch. Review tổng bắt 1 CRITICAL (FE save(strict) vẫn chặn giá 0 → popup không mở) đã fix + re-review Approved.
File sửa (CHƯA COMMIT, branch tpe-develop-assign):
- hrm-api: QuotationService.php (nới ensureAllPricesPositive + isClean + doSelfApprove + submit routing + submitCheck), QuotationController.php (submitCheck), Routes/api.php (POST /{id}/submit-check)
- hrm-client: QuotationZeroPriceModal.vue (mới), edit.vue (openSubmit + submit-check + highlight cam + submitInFlight + nới save(strict) validate giá 0)
Đang làm dở: —
Bước tiếp theo: (1) User chốt M3 (combo BOM con giá 0 → luôn không sạch + đổ popup — có loại trừ con-combo-ERP không?); (2) verify browser khi user yêu cầu; (3) commit + không cần migration.
Blocked:
