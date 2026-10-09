# Task P2-13 Report — Màn CHI TIẾT (tab Hạch toán) + IN phiếu xuất bán hàng mượn

## Status: DONE

## File tạo (2 file)
- `hrm-client/pages/finance/borrow-sells/_id/index.vue` — chi tiết, bọc 2 tab.
- `hrm-client/pages/finance/borrow-sells/_id/print.vue` — trang in.

## Chi tiết implementation

### `_id/index.vue`
- Mirror khuôn `pages/finance/borrow-sell-requests/_id/index.vue`: card "Thông tin chung", subpanel
  "Khách hàng", bảng hàng hoá, box tổng, `.export-actionbar` (giữ nguyên style/mixin `PageTitleMixin`,
  `buildStatusTitle`).
- Nạp dữ liệu qua `show(this.$store.dispatch, id)` import từ `../api` (api.js T10b của phiếu bán, KHÔNG
  dùng api Phase 1). Lỗi 403/404 → toast rồi `goBack()`.
- **Component tab dùng: `b-tabs`/`b-tab` (Bootstrap-Vue)** — không tìm thấy component tab kiểu V2Base
  trong `components/` (chỉ có `V2BaseTabNavigation.vue`, dùng cho pattern router-link khác, không hợp
  cho 2 tab nội bộ 1 trang). `bootstrap-vue/nuxt` đã đăng ký global trong `nuxt.config.js:169` nên
  `b-tabs`/`b-tab` dùng trực tiếp không cần import. `activeTab` mặc định 0 (tab đầu active).
- Tab 1 "Thông tin phiếu": card thông tin chung (mã phiếu, loại phiếu, trạng thái, số HĐ, loại HĐ,
  phiếu YC xuất bán, người lập, ngày lập, chịu phí ship), khách hàng, bảng hàng hoá (`data.products`,
  cột Mã/Tên/Model/Hãng, ĐVT, SL bán=qty, đơn giá niêm yết=price, phụ thu=extra_price, đơn giá bán=
  export_price, chiết khấu=rebate_price, đơn giá phân bổ=allocated_price, VAT%, thành tiền=qty×export_price
  tính ở FE cho dòng — KHÔNG đụng box tổng), box tổng đọc trực tiếp `sum_amount_after_extra*`,
  `sum_amount_allocated*`, `vat_cost_allocated` qua `formatMoney`, không tính lại.
- Tab 2 "Hạch toán": theo đúng brief A4 — nếu `data.accounting_error` (khác null/rỗng) → banner
  `alert alert-warning`, không render bảng; ngược lại render bảng STT/Tài khoản/Nợ/Có/TK đối ứng/Ghi chú
  từ `data.accounting[]` (`type===1`→Nợ, `type===2`→Có, `ref` join bằng ', '), dòng tổng cuối dùng
  computed `sumDebit`/`sumCredit` (copy verbatim công thức trong brief); rỗng & không lỗi → text
  "Chưa có dữ liệu hạch toán.".
- Actionbar chỉ 2 nút đúng brief A5: "Quay lại" (`light`, icon `fas fa-arrow-left`, luôn hiện) và "In"
  (`light`, icon `ri-printer-line`, gate `v-if="data.is_can_view"` — KHÔNG hard-code).
- **Cách mở trang in: `this.$router.push(...)`** (theo đúng brief A5 gợi ý ưu tiên router push khớp
  pattern phiếu). Lưu ý: khuôn Phase 1 (`borrow-sell-requests/_id/index.vue`) thực ra dùng
  `window.open(..., '_blank')` cho `printRequest()`. Task này đã chọn `router.push` theo pattern đã có
  sẵn trong khuôn PHẦN B (print.vue Phase 1 tự chứa nút "In" riêng để `$printContent`), giữ trang chi
  tiết điều hướng nội bộ sang `/finance/borrow-sells/{id}/print` thay vì mở tab mới — ghi rõ ở đây làm
  concern nếu team muốn khớp 100% hành vi tab-mới của Phase 1.

### `_id/print.vue`
- Mirror khuôn `borrow-sell-requests/_id/print.vue`: `layout: 'print'`, `#content`, render template Vue
  thường (KHÔNG v-html), `mounted()` gọi `printData` rồi nút "In" gọi `this.$printContent({ styles,
  pageMargin: '15mm 10mm 15mm 20mm' })` — copy nguyên khối `styles` từ khuôn.
- Import `printData` từ `../api` (api.js phiếu bán T10b).
- Tiêu đề "PHIẾU XUẤT BÁN HÀNG MƯỢN". Khối thông tin phiếu (`code, contract_code, created_at,
  creator_name, note`), khối khách hàng (`customer_name, customer_address, customer_mobile,
  customer_contact_name, customer_contact_phone, contact_address, delivery_place`), bảng hàng hoá
  (`products[]`: stt/code/product_name/model_name/unit_name/qty/export_price/thanh_tien, cột "Đơn giá"
  và "Thành tiền" dùng `formatMoney`), dòng tổng "Tổng thành tiền" = Σ `thanh_tien`, khối chữ ký 3 cột
  giống Phase 1. `formatMoney` trả `'—'` khi giá trị null/undefined/rỗng theo yêu cầu brief.

## Kiểm tra tự thực hiện
- `grep -nE "can[A-Za-z]*\s*=\s*true"` trên cả 2 file mới → **0 match** (đúng yêu cầu fail-closed).
- Kiểm cân bằng thẻ template bằng script Node stack-based (đọc nội dung trong `<template>...</template>`,
  bỏ qua thẻ tự đóng/void) → **cả 2 file OK, stack rỗng cuối cùng**.
- eslint: **không chạy được** — repo không có `node_modules/.bin/eslint` local (Node 14, môi trường
  agent chưa cài deps đầy đủ) → bỏ qua, đã bù bằng grep + kiểm tag balance ở trên như brief cho phép.
- Không `nuxt build`, không git commit, không `git add -A`. Chưa `git add` — để nguyên uncommitted theo
  yêu cầu (2 file mới, `git status` sẽ hiện untracked).

## Concerns
1. **Cách mở trang in**: dùng `router.push` thay vì `window.open(..., '_blank')` như Phase 1 thực tế
   làm — brief A5 diễn đạt "theo đúng cách Phase 1 làm" nhưng cũng liệt kê router.push là 1 lựa chọn.
   Nếu muốn khớp tuyệt đối hành vi Phase 1 (mở tab mới, giữ trang chi tiết ở tab cũ), cần đổi
   `printPage()` sang `window.open(`/finance/borrow-sells/${this.requestId}/print`, '_blank')`. Dễ sửa 1
   dòng nếu team muốn đổi.
2. Trường `details[]` của `products[]` không có field `code`/tên phiếu mượn nguồn theo đúng shape verbatim
   trong brief (chỉ có `product_export_request_id`), nên FE hiển thị dạng text "Nguồn phiếu mượn #<id>"
   thay vì link có mã phiếu đẹp như Phase 1 (Phase 1 có field `product_export_request_code` — Phase 2
   Resource không liệt kê field này trong brief). Nếu BE thực tế có trả thêm field code, có thể nâng cấp
   thành link như Phase 1.
3. Không có mapping màu cho `status_name`/pill trạng thái (brief không đưa danh sách status của BorrowSell)
   nên tab 1 hiển thị `status_name` dạng text thường, không dùng pill màu như Phase 1.
