# Plan — Bôi đỏ tab có lỗi validate (màn HĐ add/edit)

**Người phụ trách:** @khoipv
**File chính:** `hrm-thanhan-client/pages/contract/contract/components/GeneralComponent.vue` (dùng chung add + edit)

## Bối cảnh
Màn `contract/contract/add` khi submit thiếu trường bắt buộc → BE trả 422, field bôi đỏ trong tab nhưng **đầu tab (title) không bôi đỏ** → user không biết tab nào đang lỗi. Tab "Hàng hóa" đã có sẵn `hasErrorInProductTab` (nhưng thiếu `group_kpis`). Các tab khác chưa có.

## Map formError → tab (theo StoreContractRequest)
- **Thông tin chung**: objectable_id, quotation_id, code, number, name, type, has_kpi, contract_sign_time, contract_end_time, delivery_method, delivery_cost, receive_address, customer_id, condition, main_company_id, array_product_id
- **Hàng hóa**: groups.*, group_kpis.*
- **Tiến độ thực hiện**: contract_progress.*, reason
- **Bảo lãnh**: guarantees.*
- **Điều khoản thanh toán**: payment_terms.*

## Phase 1 — FE (GeneralComponent.vue)
- [x] Thêm computed `hasErrorInGeneralTab`
- [x] Bổ sung `group_kpis` vào `hasErrorInProductTab`
- [x] Thêm computed `hasErrorInProgressTab` (contract_progress.* + reason)
- [x] Thêm computed `hasErrorInGuaranteeTab` (guarantees.*)
- [x] Thêm computed `hasErrorInPaymentTab` (payment_terms.*)
- [x] Đổi title 4 tab sang slot `#title` + `<span :class="{ 'text-danger': ... }">`

## Phase 2 — Verify
- [ ] User submit thiếu trường ở từng tab → đúng tab đó bôi đỏ tiêu đề
- [ ] Áp dụng cho cả màn edit (dùng chung component)

## Checkpoint

### Checkpoint — 2026-06-30
Vừa hoàn thành: code FE Phase 1 (5 computed + 4 title slot)
Đang làm dở: không
Bước tiếp theo: user verify trên app (add + edit), submit thiếu field từng tab
Blocked:
