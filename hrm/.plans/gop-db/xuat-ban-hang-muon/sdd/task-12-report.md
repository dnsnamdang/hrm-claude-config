# Task 12 — Report: FE màn CHI TIẾT + IN + duyệt/từ chối + lịch sử (PYCXBHM)

## Status
DONE

## Files

**Created:**
- `hrm-client/pages/finance/borrow-sell-requests/_id/index.vue` — trang chi tiết: khối thông tin chung (mã/loại/HĐ/trạng thái/người lập/ngày lập/ghi chú/lý do từ chối khi status=4), khối khách hàng, bảng SP (nhóm theo `tabs[].name` khi có, bảng đơn khi không có tabs), thanh nút Từ chối/TP duyệt/Chuyển BGD/BGD duyệt/In/Lịch sử/Quay lại gate theo cờ `is_can_*`, 2 `BaseConfirmModal` (Từ chối có textarea bắt buộc; duyệt/chuyển không cần nhập), mở `BorrowSellRequestHistoryModal`.
- `hrm-client/pages/finance/borrow-sell-requests/_id/print.vue` — trang in `layout: 'print'`, gọi `printData`, render template Vue thường (KHÔNG v-html) từ dữ liệu có cấu trúc: đầu phiếu + khối khách hàng + bảng SP + khối ký tên, nút "In" gọi `this.$printContent(...)` (đồng bộ trong click handler).
- `hrm-client/pages/finance/borrow-sell-requests/components/BorrowSellRequestHistoryModal.vue` — modal lịch sử (`b-modal` theo khuôn modal-popup skill), prop `id`/`code`, gọi `histories(dispatch, id)` ở `mounted`, render bảng khi có dữ liệu, empty-state "Chưa có lịch sử thay đổi" khi mảng rỗng.

**Modified:**
- `hrm-client/pages/finance/borrow-sell-requests/api.js` — CHỈ thêm helper `histories(dispatch, id)` ở cuối file (GET `.../{id}/histories`); không sửa/di chuyển bất kỳ helper nào khác.

## Verify

**Lint:** Dự án không có ESLint cài đặt (`node_modules/.bin/eslint` không tồn tại, `package.json` không khai `eslint` trong devDependencies; `npx eslint` kéo bản 10.9.1 mới nhất không tương thích cấu hình dự án Node14). Theo hướng dẫn task, dùng fallback:
- `vue-template-compiler` (đã có sẵn trong `node_modules`) compile phần `<template>` của cả 3 file `.vue` mới → cả 3 **template OK**, không lỗi/tip.
- `node --check` trên phần `<script>` (extract riêng, giữ nguyên `export`/`import` dạng ESM) của cả 3 file `.vue` mới + `api.js` → **0 lỗi cú pháp** ở cả 4 file.
- Không chạy được kiểm tra semantic đầy đủ như ESLint thật (unused-vars, vue/no-unused-components...) — đã tự rà bằng mắt (xem mục rà tay bên dưới).

**Rà tay theo checklist §8 brief:**

a) Mở chi tiết 1 phiếu mỗi status — nút enable/disable đúng theo cờ: TẤT CẢ 6 nút (Từ chối/TP duyệt/Chuyển BGD/BGD duyệt/In/Lịch sử) dùng `:interactable="!!data.is_can_*"` đọc thẳng từ response, không có nhánh nào gán cứng theo `status`. Chưa test thủ công trên trình duyệt thật (không có BE chạy sẵn trong phiên làm việc này) — xác nhận bằng đọc code: mỗi nút map đúng 1 cờ theo bảng §3.2.

b) Từ chối mở modal comment, gọi đúng endpoint: `askDeny()` chỉ mở modal khi `data.is_can_deny`; `BaseConfirmModal` với `show-input`/`input-type="textarea"` bắt buộc; `handleDenyConfirm()` chặn rỗng (trim) trước khi gọi `deny(dispatch, id, comment)` → khớp §3.2/§4.

c) TP/BGD duyệt gọi đúng helper, reload sau đó: `runAction()` route theo `pendingAction` (manager_approve → `managerApprove`, switch_board → `switchBoardOfManager`, board_approve → `boardOfManagerApprove`); `runRequest()` dùng chung cho cả 4 hành động — toast `response.message` rồi `await this.loadData()` (gọi lại `show`) trong mọi trường hợp thành công; lỗi 403/422 hiện toast từ `error.response.data.message`, KHÔNG đổi state (403 có reload lại để cập nhật cờ mới nhất, đúng khuôn import-requests).

d) Trang in render đủ dữ liệu snapshot khách hàng + bảng SP: `print.vue` bind trực tiếp `data.code/type_name/contract_code/note/created_at/creator_name/customer_*/contact_address/delivery_place` + lặp `data.products[]` (stt/code/product_name/model_name/unit_name/qty) bằng template Vue thường — không có `v-html` nào trong file.

e) Modal Lịch sử hiện empty-state khi `[]`: `histories.length` rỗng (mặc định `[]`, giữ nguyên khi BE trả `[]` hoặc lỗi) → render "Chưa có lịch sử thay đổi"; không có dữ liệu giả nào được dựng.

f) Không có cờ quyền hard-code `=true`: đã `grep -n "is_can"` trên cả 3 file — mọi chỗ dùng đều đọc từ `data.is_can_*` (response BE), không có literal `true`.

g) `histories` helper thêm đúng vào api.js: thêm ở cuối file, sau `printData`, đúng path `${BASE}/${id}/histories`, không đụng thứ tự/nội dung các export khác (đã diff bằng mắt — chỉ thêm block mới).

## Rulings / Assumptions

- **R-T12-1 (đã có sẵn trong brief):** giữ nguyên — modal Lịch sử luôn wiring gọi `histories()`, chỉ hiện empty-state ở Phase 1.
- **Nhóm SP theo `tabs[].name` (brief §4, "tùy chọn"):** đã làm — khi `data.tabs` có phần tử (Firm), bảng SP nhóm theo từng tab (lọc `products` theo `firm_contract_tab_id === tab.id`), kèm nhóm "Khác" fallback cho SP không khớp tab nào (an toàn dữ liệu, không mất dòng). HĐ dịch vụ (`tabs` rỗng) hiển thị 1 bảng chung như bình thường.
- **Modal Từ chối / modal xác nhận duyệt:** dùng lại `BaseConfirmModal` (component dùng chung, đã dùng ở `index.vue` màn danh sách cùng module) thay vì tự dựng modal riêng theo mẫu `product-import-requests` (form/textarea + `BaseConfirmModal` xác nhận riêng) — vì brief §4 chỉ yêu cầu "1 textarea `comment` bắt buộc → gọi `deny`", không yêu cầu giá duyệt/nhiều vai trò như import-requests. Cách này khớp convention `.claude/skills/modal-popup/SKILL.md` và nhất quán với màn danh sách cùng module (`pages/finance/borrow-sell-requests/index.vue`) — không tạo thêm biến thể UI cho cùng 1 hành động trong cùng module.
- **Không dùng `V2Footer`:** theo khuôn `BorrowSellRequestForm.vue` (form tạo mới cùng module) tự dựng thanh nút cố định `position: fixed` — `V2Footer` có bộ menu mặc định không khớp bộ nút đặc thù (TP duyệt/Chuyển BGD/BGD duyệt) của màn này.
- **`is_can_edit`/`is_can_approve` trong DetailResource (brief §3.1) không dùng ở task này** — bảng nút §3.2 của brief chỉ liệt kê 5 hành động (Từ chối/TP duyệt/Chuyển BGD/BGD duyệt/In) + Lịch sử; không có yêu cầu nút Sửa ở màn chi tiết (đã có sẵn ở màn danh sách/route `/edit` riêng theo task khác).
- **Trang in không tái sử dụng mẫu in ERP (report_templates HTML)** như `product-import-requests/_id/print.vue` — vì `printData` BE của module này trả dữ liệu có cấu trúc (brief §3.3, không phải HTML), nên tự dựng bảng bằng template Vue. Layout/CSS in (lề, font Times New Roman, border bảng, `#printContent`) mô phỏng đúng quy ước đã có ở `product-import-requests` để đồng bộ trải nghiệm in giữa các module.

## Concerns

- Chưa chạy được thủ công trên trình duyệt thật với dữ liệu BE thật (không có server/API chạy sẵn trong phiên làm việc) — verify mục (a)-(e) chỉ dừng ở rà code, chưa test tương tác end-to-end (bấm nút, xem toast, xem trang in render đúng bố cục). Đề xuất: chạy `npm run dev` + tạo/xem thử 1 phiếu mỗi status khi có môi trường BE sẵn sàng để xác nhận UI cuối cùng.
- ESLint thật không chạy được trong môi trường này (dự án không cài eslint cục bộ) — chỉ verify bằng `vue-template-compiler` + `node --check`, không bắt được lỗi kiểu `no-unused-vars`/`vue/*` rule. Đã tự rà thủ công nhưng nên chạy ESLint thật (máy có cấu hình Node phù hợp) trước khi merge nếu muốn chắc chắn 100%.
- `BorrowSellRequestHistoryModal.vue` không dùng chung `ProductImportRequestHistoryPanel` (component đó gắn cứng với API/route của `product-import-requests`) — đã tự viết bảng lịch sử tối giản (thời gian/người thực hiện/hành động) vì Phase 1 chưa có dữ liệu thật để biết đúng shape các field BE Phase 2 sẽ trả; các tên field trong template dùng fallback (`item.created_at || item.time`, `item.user_name || item.creator_name`, `item.description || item.action`) để linh hoạt — Phase 2 nên chốt lại tên field chính xác từ BE rồi rà lại template này.
