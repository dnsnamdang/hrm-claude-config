# Plan — Kết chuyển chi phí phải trả

Spec: `design.md` cùng thư mục. Thực thi inline.

## BE (hrm-api worktree hrm-api-kccppt)
- [x] T1 Seeder 3 quyền type 8
- [x] T2 Entity ClosingEntry + ClosingEntryDetail (quyền, searchByFilter, generateCode)
- [x] T3 ClosingEntryService (paginate, meta, formOptions, detail, sumMoney, export)
- [x] T4 ClosingEntryAccountingService (gom số liệu + ghi sổ) + WriteService.store (transaction)
- [x] T5 StoreRequest + Controller + routes
- [x] T6 Feature test: list scope, show 403, sum-money, store validate, store posting khớp ERP (7/7 OK)
- [x] T6b Lịch sử: `ClosingEntryHistoryService` (ghi `catalog_histories`, action create); WriteService gọi `logCreate`.
  Thêm mục registry `closing_entries` vào `app/Services/CatalogHistoryService.php` (file DÙNG CHUNG — chỉ thêm 1 mục, không sửa logic).
- [x] T6c Nhãn cột xuất Excel đổi theo nhãn màn: "Mã phiếu", "Tính đến ngày".

## FE (hrm-client worktree hrm-client-kccppt)
- [x] T7 pages/finance/closing-entries/index.vue
- [x] T8 components/ClosingEntryForm.vue + add.vue + _id/index.vue
  - Validate bắt buộc ở FE (`requiredErrors()`): Năm, Tính đến ngày, Phòng ban, Vụ việc từng dòng, ≥1 dòng → mọi ô đỏ cùng lúc + toast, không bật popup xác nhận.
  - Màn tạo: dòng trống mặc định hiện ngay, không chờ form-options.
  - Chi tiết: form readonly + `SystemInfoSection entity-type="closing_entries"` + `V2Footer` chỉ "Quay lại" (ERP không có Sửa/Xoá/In).
- [x] T9 menu finance.js link + isShow 3 quyền
- [x] T10 verify trình duyệt (05/11/2026) — xem dưới

## Kết quả verify T10
Server riêng của worktree: API `:8001`, Nuxt `:3001` (không đụng `:8000/:3000` của main-tree). Server dev rất chậm (API ~7–8s/request) — chờ đủ lâu trước khi kết luận màn trống.
- Danh sách: 162 phiếu, sort ngày tạo giảm dần; vào màn 3 request (list 1 lần + export-columns + form-options); đổi trang 1 request; tìm theo mã 1 request, về trang 1, ra đúng 1 dòng.
- Thêm mới: trống bấm "Lưu và duyệt" → 3 ô đỏ + toast; nhập đủ → số tiền 83,454 khớp curl sum-money → lưu, về danh sách. DB: `closing_entries` id 168 `TPE.KCCPPT2026.00056`, `catalog_histories` id 8410 action create.
- Chi tiết `/finance/closing-entries/168`: tiêu đề có mã, đủ trường, bảng chi tiết + tổng, khối Lịch sử có dòng "Tạo mới", footer chỉ "Quay lại".
- Modal Lịch sử từ cột Hành động ở danh sách: tiêu đề "Lịch sử thay đổi: <mã>", dòng "Tạo mới".

## Dữ liệu test để lại trên DB local `erp_hrm_check`
- Phiếu 168 `TPE.KCCPPT2026.00056` (đã ghi sổ) + `catalog_histories` 8410.
- Gán quyền tạm: `role_has_permissions` (102372,31), (102373,31) — 3 quyền api id 102372–102374.
