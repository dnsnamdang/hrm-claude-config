# Plan — Fix lỗi API filter khách hàng ở màn BOM List

## Phase 1 — FE
- [x] Bỏ `assign/customers/search?limit=20000` ở `pages/assign/bom-list/index.vue` (nạp 43k KH → BE PHP fatal "Allowed memory size exhausted")
- [x] Đổi ô lọc Khách hàng sang `V2BaseSelectRemote` + `fetchCustomers(q, limit=30)` theo khuôn `/sale/warranty-repair-requests`
- [x] Giữ label KH khi auto-fill từ dự án TKT / quay lại màn (`customerInitialOption` + localStorage `assign_bom_list_customer_label`)

### Checkpoint — 2026-08-19
Vừa hoàn thành: fix filter KH màn BOM List
Đang làm dở: chưa test trên trình duyệt
Bước tiếp theo: user reload /assign/bom-list kiểm tra ô lọc Khách hàng
Blocked:
