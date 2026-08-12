# Plan — Sort cột màn /assign/customers (tham khảo admin/customers ERP)

Phụ trách: @khoipv

Yêu cầu: bật sắp xếp cho 4 cột **Mã KH - Tên khách hàng**, **Loại**, **MST**, **SĐT**.
Tham khảo ERP `sale/customers/index.blade.php` — DataTable ở đó cho sort `code`, `tax_code`,
`fullname`, `customer_type`, `status` (các cột còn lại `orderable: false`).

## Phase 1 — Backend (hrm-api) ✅
- [x] `Modules/Assign/Services/CustomerService::index`: whitelist `sort_by` (map key cột FE → cột thật),
      cột lạ → fallback `id` (trước đây ghép thẳng chuỗi vào `orderBy('customers.' . $sortBy)`)

## Phase 2 — Frontend (hrm-client) ✅
- [x] `pages/assign/customers/index.vue`: thêm `sortable: true` cho `customerInfo`, `customerType`,
      `taxCode`, `mobile` trong `allColumns`
- [x] `handleSort`: bỏ gọi `loadData()` trực tiếp (watcher deep của `filters` đã gọi) → tránh gọi API 2 lần mỗi lần click sort

## Phase 3 — Verify
- [ ] User bấm sort thử 4 cột trên UI (asc/desc), kiểm tra file xuất Excel/CSV vẫn theo đúng thứ tự đang hiển thị
