# Design — filter-panel-inline-buttons

Người phụ trách: @khoipv

## Mục tiêu

Mọi màn dùng `hrm-client/components/V2BaseFilterPanel.vue` (73 file) hiển thị 2 nút **Tìm kiếm** / **Làm mới** cùng dòng với ô input tìm kiếm nhanh, thay vì xuống hàng riêng bên dưới. Layout tham khảo: popup "Thêm hàng hoá" màn BOM (`pages/assign/bom-list/components/BomBuilderAddProductModal.vue`) — input và nút cùng 1 hàng, nút căn phải.

## Quyết định

- Component đã có sẵn prop `inlineSearchButtons` (opt-in, chỉ `QuotationProductSearchModal` bật) → **đổi mặc định thành `true`**, không sửa từng màn.
- 10 màn report dùng `:show-quick-search="false"` không có hàng input → fallback: nút giữ nguyên hàng riêng bên dưới khi mở panel lọc (hành vi cũ, không mất nút).
- Nút "Làm mới" đổi `secondary` → `tertiary` theo skill button-convention (nhóm Reset/Phụ trợ) — khớp luôn với nút Làm mới ở popup bom-list tham khảo.
- Giữ prop `inlineSearchButtons` để màn nào cần vẫn opt-out được (`:inline-search-buttons="false"`).

## Phạm vi ảnh hưởng

Chỉ 1 file FE: `hrm-client/components/V2BaseFilterPanel.vue`. Không BE, không migration, không permission.
