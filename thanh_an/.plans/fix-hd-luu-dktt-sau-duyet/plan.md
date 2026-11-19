# Plan — Fix: HĐ đã duyệt, sửa Điều khoản thanh toán bấm Lưu nhưng mở lại vẫn thấy dữ liệu cũ

> @khoipv — Bắt đầu 30/10/2026
> Màn: `hrm-thanhan-client/pages/contract/contract/components/GeneralComponent.vue` (tab Điều khoản thanh toán, nút Lưu sau duyệt)
> BE: `ContractService::updatePaymentTermsAfterApprove` · `ContractDetailResource`

## Nguyên nhân (đã trace code)
- Lưu sau duyệt (`POST category/contracts/{id}/updatePaymentTermsAfterApprove`) ghi vào **bảng thật**:
  `contract_payment_terms`, `contract_payment_installments`, `contracts.payment_mode_main/kpi`, `contracts.payment_terms_note` → **lưu được**.
- Nhưng màn chi tiết đọc `ContractDetailResource`, mà 5 trường ĐKTT (`payment_terms`, `payment_terms_note`,
  `payment_mode_main`, `payment_mode_kpi`, `payment_installments`) **ưu tiên lấy từ snapshot version 0**
  (`ContractDetailResource.php:245-283`) — cố ý làm vậy để HĐ gốc hiện điều khoản gốc khi có PL thay đổi ĐKTT.
- Snapshot v0 không được cập nhật khi lưu sau duyệt → F5 / mở lại vẫn hiện bản v0 cũ → user thấy như "không lưu".
- Cùng lỗi ở luồng Kết xuất cung ứng (`renderSupply` gọi lại `updatePaymentTermsAfterApprove`).
- Rủi ro thêm: HĐ đã có PL thay đổi ĐKTT được duyệt → tab hiện bản v0 (gốc), bấm Lưu sẽ ghi đè bảng thật
  bằng bản gốc đã sửa → **mất điều khoản của phụ lục** (cùng dạng lỗi PL gia hạn thời gian).

## Quyết định (user chốt 30/10/2026)
- Lưu sau duyệt → đồng bộ 5 trường ĐKTT vào **mọi** `contract_versions` (giống số HĐ / tên HĐ)
- HĐ có PL `change_payment_terms` đã duyệt → **khoá tab** ở màn HĐ, BE chặn (đổi điều khoản qua phụ lục)

## Phase 1 — BE
- [x] `ContractService::updatePaymentTermsAfterApprove`: sau khi sync bảng thật → đọc lại (đã chuẩn hoá 100% / dọn theo mode) → ghi `payment_terms`, `payment_installments`, `payment_mode_main`, `payment_mode_kpi`, `payment_terms_note` vào mọi version
- [x] Thêm `ContractService::hasApprovedPaymentTermsAnnex()`; HĐ có PL ĐKTT đã duyệt → hàm lưu bỏ qua (cả luồng `renderSupply` — trước đây kết xuất cũng đè bản v0 vào bảng thật)
- [x] `ContractController::updatePaymentTermsAfterApprove`: có PL ĐKTT đã duyệt → trả 400 kèm thông báo

## Phase 2 — FE (`GeneralComponent.vue`)
- [x] Computed `hasApprovedPaymentTermsAnnex` (từ `formSubmit.annexes`, `annex_type = change_payment_terms`, status 3)
- [x] `canEditPayment` thêm `&& !hasApprovedPaymentTermsAnnex` → khoá bảng điều khoản + ghi chú (cả lúc kết xuất)
- [x] Ẩn nút Lưu + hiện dòng ghi chú "HĐ đã có phụ lục thay đổi điều khoản thanh toán được duyệt — thay đổi điều khoản qua phụ lục."

## Phase 2b — Loading nút Lưu (30/10/2026, user yêu cầu)
- [x] `submitPaymentTermsAfterApprove`: cờ `isSavingPaymentTerms` chặn bấm lặp + `$nuxt?.$loading?.start?.()` trước lệnh gọi, `finish` trong `finally` (theo skill button-convention A6b)
- [x] Nút Lưu `:disabled` thêm `|| isSavingPaymentTerms`

## Phase 3 — Test
- [x] Tinker trên DB local (bọc transaction, rollback): HĐ-194/2026 (#222) trước `terms=[]` → lưu TIME 45 ngày + ghi chú → `ContractDetailResource` trả đúng dữ liệu mới, 0 version chưa đồng bộ; rollback về như cũ
- [x] `hasApprovedPaymentTermsAnnex` đúng với HĐ #154 (có PL ĐKTT đã duyệt)
- [ ] User test UI: HĐ đã duyệt → sửa ĐKTT → Lưu → F5 thấy dữ liệu mới; HĐ #154 tab bị khoá; kết xuất cung ứng giữ điều khoản vừa sửa

### Checkpoint — 30/10/2026
Vừa hoàn thành: Phase 1 + 2 + 2b, test BE qua tinker; đã commit + push `master` (API 366a5571, Client 8e13db52)
Đang làm dở:
Bước tiếp theo: user test UI (build client) — HĐ đã duyệt sửa ĐKTT → Lưu → F5 thấy dữ liệu mới; HĐ #154 tab bị khoá. Còn treo: HĐ đã lưu ĐKTT trước bản sửa vẫn hiện bản v0 cũ tới khi lưu lại (chưa viết script đồng bộ)
Blocked:
