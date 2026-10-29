# Plan — Điều khoản thanh toán fallback về công ty mẹ (G1 per-company)

**Nhánh:** `gop_db` · **Người phụ trách:** @namdangit

## Bối cảnh / Bug

- Màn ERP `admin/sale/principle-contracts/create?firm-quotation=59364` (lập HĐ nguyên tắc từ báo
  giá hãng) báo "điều khoản thanh toán không được áp dụng".
- Báo giá 59364 thuộc **công ty 3 (CN Vinh)**. Trên prod gộp `hrm_erp_gop`, công ty 3 **chưa khai**
  điều khoản nào; toàn bộ điều khoản chỉ khai cho **công ty mẹ id=1** (11 thanh toán + 8 báo giá).
- Root cause (bug code, KHÔNG phải data): khi làm G1 per-company (commit `f29c241955` + `ed9d026105`),
  fallback về công ty mẹ id=1 khi công ty chưa khai **chỉ được thêm vào `QuotationTerm::getForSelect()`**,
  **bỏ sót `PaymentMethodTerm::getForSelect()`**. Nên công ty ≠ 1: điều khoản báo giá hiện (qua
  fallback) nhưng điều khoản thanh toán rỗng → không áp dụng được.

## Tasks

- [x] **T1 — Điều tra root cause** (systematic-debugging): xác nhận đầu-cuối trên prod —
  firm_quotation 59364 → company_id=3; `payment_method_terms`/`quotation_terms` của cty 3 = 0;
  toàn bộ điều khoản ở cty 1; so sánh 2 model → `PaymentMethodTerm` thiếu fallback.
- [x] **T2 — Fix code:** `PaymentMethodTerm::getForSelect()` thêm fallback về `PARENT_COMPANY_ID=1`
  khi công ty hiện tại rỗng (mirror y hệt `QuotationTerm`): thêm hằng `PARENT_COMPANY_ID=1` + tách
  `queryForSelect($companyId, $type)` private + nhánh `if ($terms->isEmpty() && $companyId &&
  $companyId != PARENT_COMPANY_ID) → lấy cty 1`. Giữ nguyên nhánh `type` (bug cũ cột không tồn tại,
  ngoài phạm vi). `php -l` sạch. Verify tinker trên prod: cty 3 rỗng → fallback trả 11 điều khoản cty 1.
- [x] **T3 — Commit + push `gop_db`** (commit `ce3389a24a`): `app/Model/Common/PaymentMethodTerm.php`.

### Checkpoint — 2026-10-05
Vừa hoàn thành: T1 (điều tra) + T2 (fix fallback, verify prod).
Đang làm dở: (không có)
Bước tiếp theo: user deploy + mở lại `principle-contracts/create?firm-quotation=59364` (hoặc bất kỳ
HĐ nguyên tắc của công ty ≠ 1) → dropdown "Điều khoản thanh toán" phải hiện 11 điều khoản công ty mẹ.
Blocked:
