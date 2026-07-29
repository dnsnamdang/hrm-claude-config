# Plan — Đổi tên cột KPI không cần "Đặt lại mặc định" (một nguồn tên)

**Phụ trách:** @namdangit
**Ngày:** 2026-07-28

## Bối cảnh
- User đổi tên `<b-th>` "Đơn giá bán (đã bao gồm VAT)" ở tab hàng hóa áp KPI, phải vào "Tuỳ chỉnh cột → Đặt lại mặc định" mới thấy tên mới → mất công người dùng.
- File thực sự: `pages/contract/discount_appendix/components/ProductKpiComponent.vue` (dòng 49). (File `contract/contract/components/ProductKpiComponent.vue` là cột "Đơn giá trao tặng", khác.)

## Điều tra (root cause)
- Tab KPI KHÔNG lưu cấu hình cột theo user ở bất cứ đâu: không localStorage, không API `column-customizations`, không mixin, không `mergeSavedColumns`. `updateColumns()` chỉ set `this.columns` trong RAM (mất khi reload). Modal `column-customization-product-modal.vue` cũng không persist (chỉ `$emit`).
- Header 'price' (dòng 48-50) là `<b-th>` cứng, KHÔNG `v-if` → luôn render; đổi text hiện ngay sau build. **End user vốn KHÔNG cần "Đặt lại mặc định".**
- Nguyên nhân gây hiểu nhầm: tên cột bị **lặp ở 2 nơi tách rời** — header cứng (dòng 49) và `columns[].text` (dòng 651, đang là "Đơn giá bán (Gồm VAT)"). Sửa 1 chỗ → chỗ kia lệch → popup "Tuỳ chỉnh cột" vẫn tên cũ → cảm giác phải reset.

## Giải pháp (chốt): một nguồn tên duy nhất
Header đọc thẳng từ mảng `columns` → đổi tên ở `columns[].text` là cả header bảng lẫn popup đổi theo, không bao giờ cần reset.

- [x] Thêm method `colText(key)` trả `columns.find(k).text`
- [x] Header 'price' (dòng 48-50) → `{{ colText('price') }}`
- [x] Đồng bộ `columns[].text` cột 'price' = "Đơn giá bán (đã bao gồm VAT)"
- [ ] User build lại client + kiểm tra: header + popup "Tuỳ chỉnh cột" cùng hiện tên mới, không cần Đặt lại mặc định

## Đã áp cho CẢ 2 tab KPI (2026-07-28)
User test trên màn hợp đồng chính → header vẫn "Đơn giá trao tặng (đã bao gồm VAT)" (file `contract/contract`, khác file discount_appendix). Áp cùng fix một-nguồn cho file này:
- [x] `contract/contract/components/ProductKpiComponent.vue`: header 'price' → `{{ colText('price') }}`; `columns[].text` price = "Đơn giá bán (đã bao gồm VAT)"; thêm `colText(key)`
- [x] `discount_appendix/components/ProductKpiComponent.vue`: đã sửa trước (như trên)

## Ghi chú
- Tên cột 'price' giờ đặt DUY NHẤT tại `columns[].text` (dòng ~651 mỗi file). Muốn đổi lại (vd giữ "trao tặng") chỉ sửa 1 dòng đó.
- Các cột khác vẫn header cứng — pattern `colText` sẵn sàng tái dùng nếu muốn mở rộng.
