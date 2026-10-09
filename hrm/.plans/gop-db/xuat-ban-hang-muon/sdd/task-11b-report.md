# Task 11b — Report: FE màn TẠO phiếu Yêu cầu xuất bán hàng mượn (PYCXBHM)

## Status
DONE_WITH_CONCERNS

## Files created

| File | Mục đích |
|---|---|
| `hrm-client/pages/finance/borrow-sell-requests/create.vue` | Page wrapper mỏng — render `BorrowSellRequestForm`, guard unsaved-changes qua `unsavedChildFormMixin` (form thật nằm ở component con). |
| `hrm-client/pages/finance/borrow-sell-requests/components/ContractPickerModal.vue` | Modal chọn 1 hợp đồng (Firm/WrService), search theo mã/tên KH + lọc loại HĐ bằng nút bấm (không dùng select để tránh phải kéo `V2BaseSelectInModal`). |
| `hrm-client/pages/finance/borrow-sell-requests/components/ExportRequestPickerModal.vue` | Modal chọn nhiều phiếu xuất mượn nguồn (checkbox multi-select), lọc bỏ phiếu đã chọn ở form cha qua prop `excludeIds`. |
| `hrm-client/pages/finance/borrow-sell-requests/components/BorrowSellRequestForm.vue` | Form chính: chọn HĐ → nạp `contractProducts`/`firmTabIds`, chọn phiếu nguồn → nạp breakdown, lắp grid (giao SP-HĐ × phiếu nguồn), nhập SL bán có chặn cận trên, build payload, gọi `store`, xử lý lỗi 422 (kể cả `change_price`). Tự gắn `unsavedChangesMixin` + `formValidateMixin` (cùng khuôn `BillIncomeForm.vue`). |

Không sửa `api.js`, không sửa file nào ngoài `pages/finance/borrow-sell-requests/`.

## Verify

- **ESLint**: `npx eslint` không chạy được trong môi trường này — repo `hrm-client` **không có `.eslintrc*` / eslint trong `node_modules`**, và `npx` kéo ESLint 10 (yêu cầu Node mới) trong khi Node hiện tại là 14.21.3 → lỗi `SUPPORTED_VERSIONS.at is not a function` (không phải lỗi của code). Đã thử fallback:
  - `vue-template-compiler` (đã có sẵn trong `node_modules`) parse + compile block `<template>` của cả 4 file → **0 lỗi** (`template OK` cho cả 4).
  - `node --input-type=module --check` cho block `<script>` của cả 4 file (tách bằng `vue-template-compiler`) → **0 lỗi cú pháp**.
  - Đọc tay lại toàn bộ để soát import thừa/biến chưa dùng — không thấy.
- **Build**: không chạy `nuxt build` (build repo Nuxt cỡ lớn, rủi ro timeout cao so với giá trị xác nhận thêm được) — bỏ qua theo cho phép của brief §7.
- **Checklist tay (brief §7)**:
  - (a) Chọn HĐ Firm → `loadContractProducts()` gọi `getBorrowSellData` với `contractable_type` verbatim, set `contractProducts` + `firmTabIds`; grid có cột "SL khả dụng" (= `availableCap()`, ép `Math.floor` khi `unit_coefficient != 1`). ✅ (đọc code, chưa chạy trình duyệt thật — xem Concerns).
  - (b) `buildPayload()`: Firm → thêm `firm_tab_ids`, không có `wr_service_contract_item_id`/`rebate_price`; WrService → ngược lại (thêm `wr_service_contract_item_id` + `rebate_price`, không có `firm_tab_ids`). ✅ đọc code xác nhận nhánh `if (this.isFirm)`.
  - (c) 422 `change_price`: `handleSaveError()` parse JSON `errors.change_price` → `markPriceErrors()` gắn `_priceError` đúng `product_id+unit_id` → viền đỏ (`row-error`/`is-invalid`) + toast `errors.products?.[0]`; không có luồng confirm/resubmit. ✅ đọc code.
  - (d) Success → `this.$router.push('/finance/borrow-sell-requests/' + data.id)`. ✅.
  - (e) Không hard-code cờ quyền `= true` — màn này không có cờ quyền riêng (đọc/nhập liệu thuần), không phát sinh cờ nào. ✅.
  - (f) `markFormSaved()` gọi ngay trước `$router.push` trong nhánh thành công của `save()`. ✅.

## Rulings (điểm brief không nói rõ — đã tự quyết, ghi lại để review)

1. **`type` trong payload = `contract.type` (từ `getContracts`), KHÔNG hard-code `1`.** Brief §5 gợi ý "mặc định 1 nếu spec không phân biệt", nhưng `getContracts` (§3.1) trả sẵn `type(1|2)` verbatim cho từng HĐ, và giá trị này khớp domain đã dùng ở `index.vue` (`EXPORT_TYPE_OPTIONS`). Dùng nguồn có sẵn thay vì hard-code để `type` phản ánh đúng loại HĐ đã chọn (Firm=1/WrService=2) — tránh lệch giữa `type` và `contractable_type` gửi lên cùng payload.
2. **`net_price` — KHÔNG gửi key này trong `products[]`.** Spec §5 liệt kê `net_price` trong template payload nhưng không có công thức/nguồn dữ liệu nào ở §3/§4 để tính nó; §5 cũng ghi rõ "trường tổng... nullable... có thể bỏ qua, nếu bỏ đừng gửi key". Vì không có nguồn tin cậy để tính đúng, chọn omit hẳn thay vì gửi giá trị suy đoán sai.
3. **`rebate_price` — chỉ gửi cho WrService** (lấy từ `contractProduct.rebate_price`, đúng field liệt kê ở §3.2 cho WrService). Firm không có field này trong danh mục SP trả về (§3.2 liệt kê field Firm không có `rebate_price`) nên omit hẳn key cho Firm thay vì gửi `0` giả định.
4. **Grid KHÔNG hiển thị cột giá/thành tiền** — chỉ hiện mã/tên/model/ĐVT/SL khả dụng/SL bán. Brief §4 mục 3 nói "giá lấy từ contractProduct" nhưng đọc theo mạch câu là nguồn dữ liệu cho **payload**, không phải yêu cầu hiển thị cột giá trên UI; §0 cũng nói rõ Phase 1 "KHÔNG hạch toán". Giữ bảng gọn, đúng phạm vi chứng từ yêu cầu.
5. **Không dùng `V2Footer`** cho nút Lưu — component này không có cơ chế disable nút theo điều kiện (không có prop `disabled`/`interactable` truyền vào từng menu item), trong khi brief §6 yêu cầu cứng "Nút Lưu disable tới khi đủ [điều kiện]". Tự dựng 2 nút `V2BaseButton` (Lưu dùng `:interactable="canSubmit && !saving"`, Quay lại) — cùng khuôn nút footer 2 modal picker.
6. **Đổi hợp đồng đã chọn (mở lại `ContractPickerModal` sau khi đã có dữ liệu) → reset sạch** `selectedExportRequests`/`exportRequestBreakdowns`/`gridRows`/`contractProducts`/`firmTabIds`. Brief không nói rõ hành vi này; chọn reset vì SP/giá của phiếu nguồn cũ có thể không khớp HĐ mới (đúng thuật toán khớp §4), giữ lại sẽ gây nhầm.
7. **Khớp `product_id`(+`unit_id`)** nới lỏng: nếu 1 trong 2 phía thiếu `unit_id` thì chỉ so `product_id`. Spec ghi "(+ `unit_id`)" có dấu ngoặc gợi ý là điều kiện phụ, không phải luôn bắt buộc — xử lý phòng hờ trường hợp 1 trong 2 API không trả `unit_id`.
8. **`ExportRequestPickerModal` dùng prop `excludeIds`** (lọc phiếu đã chọn khỏi danh sách hiển thị) thay vì `selectedIds` (giữ tick) như khuôn `TransferRequestSearchModal.vue` — khuôn gốc khai `selectedIds` nhưng thực ra KHÔNG dùng trong code (nhìn code thực tế, `checked` luôn reset rỗng khi mở modal, prop `selectedIds` chết). Chọn cách rõ ràng hơn (loại hẳn khỏi list) để tránh double-select cùng 1 phiếu.

## Concerns

- **Chưa test trên trình duyệt thật** (Playwright không được yêu cầu trong task này, và brief cấm dispatch subagent) — mọi xác nhận ở checklist §7 là đọc code tĩnh, không phải chạy thực tế. Rủi ro lớn nhất nằm ở **response shape thật của 3 endpoint** (`getBorrowSellData`, `getExportRequests`, `getExportRequestData`) — code giả định `res.data` chứa payload (khớp mọi ví dụ khác trong repo), nhưng nếu BE trả shape khác (vd không bọc `data`, hoặc `getExportRequestData` không có `data.code`) thì cần chỉnh nhỏ ở 2-3 chỗ `res?.data || res || {}`.
- **Không có ESLint chạy được** trong môi trường (xem mục Verify) — chỉ xác nhận bằng parser template + syntax check script, không bắt được các lỗi style/best-practice mà ESLint config thật của dự án (nếu tồn tại ở máy khác) có thể bắt.
- **`type` filter trong `ContractPickerModal`** dùng nút bấm thay vì tự nhớ lựa chọn — mỗi lần mở lại modal reset về "Tất cả" (giống hành vi reset `keyword`), chấp nhận được vì đây chỉ là bộ lọc phụ.
- Chưa có màn chi tiết (`/finance/borrow-sell-requests/:id` — Task 12) nên nhánh push sau khi lưu thành công **chưa test được thực tế** (route đích hiện chưa tồn tại, đúng như brief §6 đã lường trước — "có thể chưa tồn tại, cứ push").
