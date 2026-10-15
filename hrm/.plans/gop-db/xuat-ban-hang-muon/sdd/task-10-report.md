# Task 10 — Report: FE API layer + list page + menu (Yêu cầu xuất bán hàng mượn)

## File tạo/sửa
1. **Create** `hrm-client/pages/finance/borrow-sell-requests/api.js` — copy verbatim từ brief (11 hàm bọc endpoint Task 8).
2. **Create** `hrm-client/pages/finance/borrow-sell-requests/index.vue` — màn danh sách, adapt từ khuôn `pages/finance/product-import-requests/index.vue`.
3. **Modify** `hrm-client/components/subsystem-menu/finance.js` dòng 169 — thêm `link: '/finance/borrow-sell-requests'`.

Nhánh làm việc: `gop_db` (đã kiểm `git branch --show-current` = `gop_db` trước khi code).

## Điểm lệch brief + cách resolve

1. **Ô lọc "Khách hàng" (param `customer` = customer_id) — KHÔNG đưa vào filter UI.**
   Brief liệt kê `customer` trong bảng filter params nhưng 11 endpoint Task 8 không có endpoint tìm khách hàng theo tên (khuôn `product-import-requests` có sẵn `/partners` riêng để nạp `V2BaseSelectRemote`, feature này thì không). Dựng ô lọc gõ tay ID sẽ sai UX và không thuộc phạm vi 11 endpoint đã cho → bỏ field này khỏi `filterFields`, giữ cột "Khách hàng" hiển thị `customer_name` trong bảng. Xin xác nhận nếu cần bổ sung ở Task 11/12 khi có nguồn select phù hợp.

2. **Bỏ sort (`sortable` cột + `@sort`) so với khuôn.**
   Response/param contract trong brief không nhắc `sort_by`/`sort_desc`, chỉ có `order` là 1 trong các param "tuỳ chọn, không bắt buộc". Vì không rõ định dạng `order` BE nhận, tôi không thêm sort để tránh gửi sai param → cột bảng không có `sortable: true`, không có `handleSort`.

3. **Bỏ `Xuất Excel`, `V2BaseSelectRemote` (NCC/KH), `V2BaseCompanyDepartmentFilter`, warehouse/partners fetch** so với khuôn — không có endpoint tương ứng trong 11 endpoint Task 8, và brief không yêu cầu (Phase 1 chỉ list + filter + action theo cờ quyền).

4. **Không lưu `scopeMeta` (canViewAllCompany/canViewCompany/canViewDepartment/isKeToanKho/isTP/isBGD) vào `data`.** Brief liệt kê các cờ này trong response shape nhưng không chỉ định UI nào tiêu thụ chúng ở Phase 1 (không có filter công ty/phòng ban, row actions dùng thẳng `is_can_*` của từng dòng) → bỏ qua để tránh code chết. Nếu Task 11/12 cần, sẽ đọc lại từ response khi đó.

5. **Badge trạng thái: dùng đúng 3 class có sẵn trong `v2-styles.scss`** (`tpl-status-active` xanh cho status=1, `tpl-status-lock` đỏ cho status=4, `tpl-status-draft` xám cho các status còn lại 2/3/10/11) — đúng theo hướng dẫn giải quyết mâu thuẫn của chính brief ở dòng 124 ("class badge tự map theo status số theo quy ước khuôn: success→active, danger→lock, còn lại→draft"), dù bảng status map phía trên ghi 2/10/11 là "vàng" (không có class vàng dùng chung trong `v2-styles.scss`).

6. **Modal "Từ chối" dùng component dùng chung `components/modal/base-confirm-modal.vue`** (`showInput` textarea) thay vì tạo file `components/DenyModal.vue`/`RejectModal.vue` riêng — brief chỉ cho phép tạo/sửa đúng 3 file. Validate `comment` không rỗng ở FE trước khi gọi `api.deny` (BE vẫn là nguồn validate thật, 422 được bắt và toast lại).

7. **Nút "TP duyệt" / "Chuyển BGD" cùng đọc `is_can_manager_approve`** đúng như brief mô tả (dòng 137: "TP có quyền duyệt thì cũng có quyền chuyển lên BGD") — không tự thêm cờ mới.

## Verify

1. **Lint**: repo không có `eslint` cài trong `node_modules/.bin` và `package.json` không có script `lint` → KHÔNG chạy được eslint thật. Đã kiểm cú pháp bằng `node --check`:
   - `node --check pages/finance/borrow-sell-requests/api.js` fail vì `node --check` mặc định coi file là CommonJS (báo lỗi `Unexpected token 'export'`) — đây là hạn chế của `node --check`/CJS, không phải lỗi cú pháp thật (file dùng ESM `export const` như mọi module khác trong `pages/*`). Đã copy sang `.mjs` trong scratchpad và chạy lại: **`node --check api_check.mjs` → PASS** (cú pháp ESM hợp lệ).
   - `index.vue`: trích khối `<script>...</script>` ra file `.mjs` tạm rồi `node --check` → **PASS**.
   - Không build được Nuxt thật (không cài node_modules đầy đủ / không có script build nhanh trong thời gian task) → KHÔNG có kết quả runtime PASS, chỉ có kết quả kiểm cú pháp tĩnh nêu trên.
2. **Import/component tồn tại** (grep):
   - `index.vue` có `import * as api from './api'` — OK.
   - `components/V2BaseButton.vue`, `V2BaseRowActions.vue`, `V2BaseSmartFilterPanel.vue`, `V2BaseDataTable.vue`, `components/modal/base-confirm-modal.vue` đều tồn tại trên đĩa — OK.
   - `ColumnCustomizationModal` không import trực tiếp, do mixin `columnCustomizationMixin.js` tự đăng ký component (đúng pattern khuôn) — đã đọc mixin xác nhận `components: { ColumnCustomizationModal }` có sẵn.
3. **Menu dòng 169**: `{ label: 'Yêu cầu xuất bán hàng mượn', link: '/finance/borrow-sell-requests' }` — đã có `link`, đúng brief.
4. **Cân bằng thẻ template**: đếm thủ công (python) số thẻ mở/đóng cho `div`, `template`, và các component chính (`V2BaseSmartFilterPanel`, `V2BaseDataTable`, `V2BaseButton`, `V2BaseRowActions`, `BaseConfirmModal`, `ColumnCustomizationModal`) — tất cả khớp (self-closing tính riêng).
5. **Không chạy dev server** — không build được trong môi trường task này (không có `node_modules` eslint, chưa xác nhận toàn bộ deps Nuxt đã cài) → không bịa kết quả runtime.

## STATUS
**DONE_WITH_CONCERNS**

## Concerns
- Ô lọc "Khách hàng" (param `customer`) bị bỏ khỏi UI Phase 1 do thiếu endpoint search — cần xác nhận nếu phải bổ sung sớm hơn Task 11/12.
- Chưa build/chạy dev server thật để xác nhận runtime (route `/finance/borrow-sell-requests/{id}` và `/create` chưa tồn tại là bình thường theo brief, nhưng chưa verify màn list tự nó render đúng qua Nuxt dev).
- Sort cột và Excel export bị lược bỏ so với khuôn — nếu nghiệp vụ cần, phải bổ sung ở task sau khi có contract rõ ràng cho `order`.
