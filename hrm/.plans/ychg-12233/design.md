# #12233 — YCHG: Tạo phiếu / chọn hàng & kho hàng tạm (QA UI + quyền giá nhập)

## Bug & cách sửa (chỉ FE `hrm-client`)
1. **Bỏ ô "Số phiếu"** (và ô "Trạng thái" trùng badge) ở khối Thông tin chung — `components/sale/price-asking/PriceAskingRequestForm.vue`; Công ty + Người tạo chuyển `col-md-6`.
2. **Badge trạng thái cạnh tiêu đề** — dùng `buildStatusTitle()` (`utils/page-title-status.js`) ở `pages/sale/price-asking-requests/add.vue` (badge "Đang tạo" `#64748B`), `_id/edit.vue`, `_id/index.vue` (status_text/status_color BE trả). `head()` giữ tiêu đề chữ thuần.
3. **Giãn cách nút + icon Xoá đỏ** — `V2BaseIconButton danger`; `.row-actions` gap 8px.
   - Bẫy: rule global `.v2-styles .row-actions { gap: 0 }` cùng specificity với rule scoped và nạp sau ⇒ đè mất. Selector scoped phải là `.v2-styles .row-actions`.
4. **Không quyền "Xem giá vốn hàng hoá" thì không có cột Giá nhập** ở tab kho hàng tạm (`pages/assign/quotations/components/QuotationProductSearchModal.vue`): `<th>/<td>` gate `isYchg && reuseCanViewCost`, colspan 13/14. `reuseCanViewCost` fail-closed, set từ `res.can_view_cost_price === true`.
   - BE `ProductProjectController` (scope=ychg) đã đúng sẵn: trả `can_view_cost_price`, null `estimated_price` khi thiếu quyền, lọc dự án theo `ProspectiveProject::visibleIdsQuery()` ⇒ không sửa BE.
   - Picker chọn hàng (`ProductPickerPanel.vue`) đã gate `canSeeCost` sẵn.

## Kiểm Playwright (127.0.0.1:3000, 19/11/2026)
- Add: tiêu đề có badge "Đang tạo", không còn Số phiếu/Trạng thái.
- Chi tiết 3568: tiêu đề "Chi tiết yêu cầu hỏi giá: PYCHG-03568" + badge "Đang hỏi giá".
- Dòng hàng: icon xoá `rgb(220,38,38)`, khoảng cách 2 nút 8px.
- Tab kho hàng tạm: không quyền → 13 cột, không có Giá nhập; có quyền → hiện "Giá nhập (Mã tiền tệ)".
