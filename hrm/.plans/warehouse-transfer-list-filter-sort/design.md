# Điều chuyển kho — Danh sách: bổ sung bộ lọc + sort (Ticket "[ERP => HRM] Điều chuyển kho - Danh sách")

Màn: Danh sách phiếu điều chuyển kho (PDCK — loại 5).
FE: `hrm-client/pages/finance/warehouse-transfers/index.vue`.
BE: `hrm-api/Modules/Finance/Http/Controllers/V1/WarehouseTransferController.php`.

## Yêu cầu (Redmine, assignee Trần Cư)

1. **Bộ lọc:** thiếu lọc theo **công ty**, **phòng ban**, **mã hàng hóa**.
2. **Thêm sort** vào cột **mã** và cột **phiếu ĐNXK**.

## Hiện trạng rà được

- **BE `applyFilters`** ĐÃ đọc sẵn `company_id`, `department_id`, `part_id` (controller:126–134) và
  `product_name` (whereHas products: `product_name LIKE` **hoặc** `code LIKE`, controller:150–155).
  → Không cần đụng BE cho Task 1, chỉ cần FE gửi params.
- **BE sort CỐ ĐỊNH** `orderByDesc(warehouse_transfers.id)` ở `index()` (:94) và `export()` (:193),
  KHÔNG đọc param → cần sửa cho Task 2.
- **FE** chưa có ô lọc Công ty/Phòng ban, nhãn ô hàng hóa là "Tên hàng hóa", cột không có `sortable`,
  `buildParams` chưa truyền sort.
- **ERP gốc** (`WarehouseTransfer::searchByFilter`): màn `index` KHÔNG có lọc Công ty/Phòng ban
  (`search_by_info:false`), lọc hàng hóa là 1 ô `product` khớp `WarehouseTransferLot.product_name LIKE`
  hoặc `code`. Sort động: `code`, `created_at`, `status`, `approved_time`; **Phiếu ĐNXK `orderable:false`**.
  Màn biến thể `all` mới có Công ty/Phòng ban (`Company::getForSelect` + `Department::getForSelectAll`,
  lọc qua `FilterDepartmentHelper`). → Ticket yêu cầu khách THÊM, vượt parity màn `index`.

## Quyết định đã chốt

### QĐ1 — "Mã hàng hóa" = ĐỔI NHÃN ô sẵn có, KHÔNG thêm ô mới

Ô `product_name` hiện tại đổi nhãn **"Tên hàng hóa" → "Tên/mã hàng hóa"**. Lý do:
- BE đã khớp **cả tên lẫn mã** trong cùng 1 điều kiện (`product_name LIKE` OR `code LIKE`).
- Đúng nhãn ERP gốc ("Tên, mã hàng hóa") và đúng màn chị em `product-exports/index.vue:330`
  (`{ key: 'product_name', label: 'Tên/mã hàng hóa' }`) — bám pattern có sẵn, KHÔNG tự chế.
- Thêm ô "Mã hàng hóa" riêng sẽ trỏ cùng 1 param BE → trùng lặp vô nghĩa.

### QĐ2 — Công ty + Phòng ban dùng component chung `V2BaseCompanyDepartmentFilter`

Bám đúng `product-exports/index.vue` (cùng nhóm kho): nhóm filter `key: 'org'` + slot `#field-org`
render `V2BaseCompanyDepartmentFilter` với `:disable_part` + `:disable_employee` (đúng 2 ô Công ty +
Phòng ban). Component **tự nạp options từ store** (`companies`/`departments` nạp 1 lần lúc đăng nhập)
và **tự cascade** (đổi Công ty → reset Phòng ban). Ghi thẳng `company_id`/`department_id` vào `filters`
→ `watch filters` bắt được, gọi lại API.

`permissions` map từ 4 quyền scope của màn (đã có trong `scopedQuery()`):
- `is_all_company` ← `Xem phiếu điều chuyển kho theo tổng công ty`
- `is_company` ← `Xem phiếu điều chuyển kho theo công ty`
- `is_department` ← `Xem phiếu điều chuyển kho theo phòng ban`
- `is_part` ← `Xem phiếu điều chuyển kho theo bộ phận`

Giữ `part_id` + `employee_id` trong `initialStateForm` cho cascade (Vue 2 reactivity) dù 2 ô bị ẩn —
đúng khuôn `product-exports`. BE bỏ qua `employee_id` (không đọc), vô hại.

### QĐ3 — Sort: thêm cho CẢ cột Mã và Phiếu ĐNXK (theo ticket)

ERP để Phiếu ĐNXK `orderable:false`, nhưng ticket yêu cầu rõ sort cho cột này → **thêm**.
- FE: bám pattern `delivery-quotations/index.vue` — `sort_by`/`sort_desc` (chuỗi `'true'`/`'false'`),
  `:sortBy`/`:sortDirection`/`@sort` trên `V2BaseDataTable`, `sortable: true` ở 2 cột, `handleSort`,
  guard trong `mounted` (sort_by không hợp lệ → reset). `buildParams` đã spread `...rest` nên 2 param
  tự đi theo.
- BE: bám pattern `DeliveryQuotation::searchByFilter` — whitelist cột, mặc định `id DESC`:
  - `code` → `warehouse_transfers.code`
  - `warehouse_export_request_code` → `wer.code` (cột join alias — PHẢI qualify alias, không BE báo
    "ambiguous"/sai cột). Dùng chung 1 helper `applySort()` cho cả `index()` lẫn `export()`.

## Phạm vi KHÔNG làm

- Không sửa luồng nghiệp vụ, không thêm quyền mới, không đổi Resource.
- Không thêm ô lọc Bộ phận/Nhân viên (ticket chỉ xin Công ty + Phòng ban).
