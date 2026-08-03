# Mở tab mới khi click "Chứng từ nghiệp vụ" — tab Dữ liệu liên quan (4 màn)

@khoipv — 2026-07-06

## Mục tiêu
Ở tab "Dữ liệu liên quan" của 4 màn chi tiết (Dự toán / Báo giá / Thầu / Hợp đồng),
cột "Chứng từ nghiệp vụ" khi click phải mở màn chi tiết chứng từ ở **tab trình duyệt mới**
thay vì điều hướng SPA trong cùng tab.

## Cách làm
Thêm `target="_blank" rel="noopener"` vào `<nuxt-link>` cột mã chứng từ.
Chỉ FE, không đụng BE. Không đổi logic `getDetailRoute`.

## Task
- [x] Rà soát 4 component tab dữ liệu liên quan (cấu trúc giống hệt nhau)
- [x] `sale/project/components/RelationDataComponent.vue` (Dự toán)
- [x] `plan/quotation/components/QuotationRelatedDataComponent.vue` (Báo giá)
- [x] `bid_package/bid_package/components/BidRelatedDataComponent.vue` (Thầu)
- [x] `contract/contract/components/ContractRelatedDataComponent.vue` (Hợp đồng)
- [ ] Verify UI: click mã chứng từ ở mỗi màn → mở tab mới đúng chi tiết

## Ghi chú
- nuxt-link có `target="_blank"` → vue-router bỏ qua click handler, để browser mở tab mới native.
