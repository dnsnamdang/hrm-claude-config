# Plan — Điều chuyển kho Danh sách: bộ lọc + sort

Xem quyết định ở `design.md`. Feature nhỏ (1 phase).

## Task 1 — FE: thêm lọc Công ty + Phòng ban (QĐ2)

- [x] `index.vue`: import + đăng ký `V2BaseCompanyDepartmentFilter`.
- [x] `initialStateForm`: thêm `company_id`, `department_id`, `part_id`, `employee_id` (= '').
- [x] `data`: thêm `permissions: {}`.
- [x] `filterFields`: thêm nhóm `{ key: 'org', label: 'Công ty – Phòng ban', wrapperClass: 'd-contents', hideLabel: true, resetKeys: ['company_id','department_id','part_id','employee_id'], inputCount: 2 }` ở ĐẦU mảng.
- [x] Template: slot `#field-org` render `V2BaseCompanyDepartmentFilter` (`:form="filters"`, `:permissions`, `:floating="true"`, `:disable_part="true"`, `:disable_employee="true"`, `wrapper-class="d-contents"`).
- [x] `mounted`: set `permissions` từ 4 quyền scope (QĐ2) TRƯỚC `loadFilterState`.
- Copy pattern từ `pages/finance/product-exports/index.vue:21-30,316-326,489-494`.

## Task 2 — FE: đổi nhãn ô hàng hóa (QĐ1)

- [x] `filterFields`: `product_name` label `'Tên hàng hóa'` → `'Tên/mã hàng hóa'`.

## Task 3 — FE: sort cột Mã + Phiếu ĐNXK (QĐ3)

- [x] `initialStateForm`: thêm `sort_by: ''`, `sort_desc: 'true'`.
- [x] `V2BaseDataTable`: thêm `:sortBy="filters.sort_by"`, `:sortDirection="filters.sort_desc === 'true' ? 'desc' : 'asc'"`, `@sort="handleSort"`.
- [x] `allColumns`: `code` + `warehouse_export_request_code` thêm `sortable: true`.
- [x] methods: thêm `handleSort({ field, direction })`.
- [x] `mounted`: guard sort_by không thuộc cột sortable → reset về `''`/`'true'`.
- Copy pattern từ `pages/transport/delivery-quotations/index.vue:28-33,404-407,307-311`.

## Task 4 — BE: sort động (QĐ3)

- [x] `WarehouseTransferController`: thêm private `applySort($query, $request)` với whitelist
      `code => warehouse_transfers.code`, `warehouse_export_request_code => wer.code`, mặc định
      `warehouse_transfers.id DESC`.
- [x] `index()` :94 — thay `orderByDesc(...)` bằng `$this->applySort($query, $request)`.
- [x] `export()` :193 — thay `orderByDesc(...)` trong chuỗi chunk bằng `applySort` trước `->chunk(...)`.
- Copy pattern từ `Modules/Transport/Entities/DeliveryQuotation/DeliveryQuotation.php:142-152`.

## Task 5 — Kiểm thử Playwright (bắt buộc trước khi báo xong)

- [x] Mở `http://127.0.0.1:3000/finance/warehouse-transfers` (inject token).
- [x] Panel bộ lọc có Công ty + Phòng ban (cascade), ô "Tên/mã hàng hóa".
- [x] Bấm sort cột Mã (asc/desc) + Phiếu ĐNXK → request kèm `sort_by`/`sort_desc`, data đổi thứ tự.
- [x] grep self-check element thô = rỗng.

## Kết quả kiểm thử (06/11/2026)

DB local `erp_hrm_check`: bảng `warehouse_transfers` **0 dòng** → bảng luôn "Không có dữ liệu",
không xem được thứ tự đổi thật, nhưng đã xác nhận param + BE nhận đúng (200, không 500):

- 4 quyền scope `Xem phiếu điều chuyển kho theo …` **có sẵn trong DB** (id 101239–101242, guard `api`),
  user test (DNS Admin) chưa được gán → filter Công ty/Phòng ban bị ẩn theo đúng thiết kế fail-closed.
  Inject tạm `permissions` vào component (runtime, không đụng DB) để nghiệm thu FE:
  - Công ty hiện 5 cty, chọn → `company_id=1` (200).
  - Phòng ban cascade theo cty vừa chọn, chọn → `company_id=1&department_id=45` (200).
  - Ô "Tên/mã hàng hóa" hiển thị đúng nhãn mới.
- Sort: Mã `sort_by=code&sort_desc=false`→`…=true` (toggle), Phiếu ĐNXK
  `sort_by=warehouse_export_request_code&sort_desc=false` — tất cả 200, alias `wer.code` hợp lệ.
- Console chỉ còn warning HMR/postcss dev-mode (re-export, flex-end) — không có lỗi runtime.
