# Check: Ô Số lượng bảng hàng hóa Báo giá / Gói thầu / Hợp đồng không lưu được số < 1

> @khoipv — 04/11/2026

## Câu hỏi
Màn Báo giá (`plan/quotation`), bảng hàng hóa, ô Số lượng có đang chặn nhập số nhỏ hơn 1 không?

## Kết luận
- **FE KHÔNG chặn.** Ô SL dùng `components/common/CurrencyInput.vue` vẫn gõ được thập phân (`0,5`, `1,25`). Đã chạy thử bằng Vue thật (jsdom, có cả `changeProduct` làm cha vẽ lại) → đúng.
  - ⚠️ Lần đầu đọc code tôi kết luận sai "gõ `0,` bị mất dấu phẩy". Thực tế gõ `0,` thì emit `0` trùng giá trị cũ → Vue không vẽ lại → ô giữ nguyên `0,`. Bài học: với input kiểu này phải chạy thử, không suy từ code.
- **BE chặn:** rule `qty` `min:1` (Báo giá có `numeric`, nên < 1 bị 422). Gói thầu / HĐ thiếu `numeric` → `min:1` thành so độ dài chuỗi → thập phân lọt nhưng số âm cũng lọt.
- DB `qty` kiểu `float` → không chặn.

## Quyết định (user chốt 04/11/2026)
- Cho SL thập phân, kể cả < 1; SL phải **> 0**.
- Chỉ sửa BE, FE giữ nguyên `currency-input`.

## Task
- [x] BE `StoreQuotationRequest`: `groups.*.products.*.qty` `min:1` → `gt:0` (giữ nhánh `project_type == 6`) + message "Số lượng phải lớn hơn 0".
- [x] BE `StoreBidPackageRequest`: `groups.*.products.*.qty` `required|min:1` → `required|numeric|gt:0` + message.
- [x] BE `StoreContractRequest`: `groups.*.products.*.qty` (nhánh ≠ type 5) → `required_with:groups.*.products|numeric|gt:0`; `group_kpis.*.product_kpis.*.qty` → `required|numeric|gt:0` + message.
- [x] Hoàn tác FE: xoá `components/common/DecimalInput.vue`, trả ô SL ở 4 file (`plan/quotation`, `bid_package/bid_package`, `contract/contract` ProductComponent + ProductKpiComponent) về `<currency-input>`.

## Chưa làm (chờ user)
- Phụ lục HĐ (`contract_annex_*`, `discount_appendix`) và Biên bản thương thảo (`StoreNegotiationMinuteRequest:29` `required|min:1` thiếu `numeric`).

### Checkpoint — 04/11/2026
Vừa hoàn thành: BE `gt:0` cho SL Báo giá / Gói thầu / HĐ; hoàn tác FE
Đang làm dở:
Bước tiếp theo: user test lưu SL 0,5 / 0 / số âm ở 3 màn
Blocked:
