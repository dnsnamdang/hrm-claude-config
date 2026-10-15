# Design — Cột hành động màn "Danh sách đề nghị nhập kho"

> Nhánh: `gop_db` · Phụ trách: @namdangit · Ngày: 19/09/2026
> Màn: `hrm-client/pages/finance/warehouse-import-requests/index.vue` (PDNNK, module Finance)

## Nguồn yêu cầu (Redmine, ảnh chụp có 2 chú thích)

Ticket **[ERP => HRM] Phiếu đề nghị nhập kho - Danh sách**. Ảnh chú thích:
1. "Đổi thành cột hành động" — trên header cột "Thao tác".
2. "Cột hành động gồm đầy đủ các nút như duyệt nhanh… như các cột hành động tại màn khác."

## 3 quyết định đã CHỐT với user

1. **Chỉ BỔ SUNG nút vào cột hành động, GIỮ header "Thao tác"** — không đổi tên header.
   (Cả 4 màn finance đều dùng "Thao tác"; user xác nhận "1 đúng là bổ sung".)
2. **"Duyệt nhanh" = Option A: deep-link ERP** — surface nút "Tạo phiếu nhập kho" đã có sẵn
   (mở tab ERP `warehouse_imports/create?warehouse_import_request_id=`). HRM KHÔNG có route duyệt
   (đúng thiết kế: duyệt xảy ra ở tầng ERP trên bản ghi DB gộp chung id).
3. **Đưa ra ĐỦ nút nhưng GOM vào menu ⋮** khi nhiều — theo màn chuẩn (`V2BaseRowActions`), không dàn
   hết nút inline.

## Giải pháp

- **FE-only.** BE `WarehouseImportRequestResource` (dùng chung list + detail) đã trả đủ 5 cờ:
  `is_can_edit`, `is_can_create_warehouse_import`, `is_can_deny`, `is_can_cancel` (+ luôn cho In).
- Cột hành động dùng component chuẩn **`V2BaseRowActions`** (khuôn `/assign/customers`, `bill-incomes`):
  tối đa 3 nút inline (`maxInline=3`), dư thì gom vào menu ⋮ (`ri-more-2-fill`) append `<body>`.
- Cột **Mã phiếu** đổi thành `nuxt-link` (`class="v2-cell-link field-line"`) trỏ chi tiết — theo quy ước
  `V2BaseRowActions` KHÔNG có nút "Xem", click mã → chi tiết.
- Tập nút (thứ tự, cờ hiện): **Sửa** (`is_can_edit`) · **Tạo phiếu nhập kho** (`is_can_create_warehouse_import`)
  · **Từ chối** (danger, `is_can_deny`) · **In** (luôn) · **Hủy** (danger, `is_can_cancel`).
- Từ chối/Hủy dùng `base-confirm-modal` (Từ chối có ô lý do textarea bắt buộc); In dùng
  `reportPrintPreviewMixin` + `ReportPrintPreviewModal` (endpoint `.../{id}/print-data` đã có).

## Đồng bộ với màn CHI TIẾT

Tập nút + điều kiện hiện lấy y hệt `_id/index.vue` (nguồn pattern) → danh sách và chi tiết khớp nhau
(list-page skill mục 7.2).

## Verify (Playwright, 19/09/2026)

Danh sách trống với emp 48 (thiếu quyền xem) → bơm 4 mock row client-side (KHÔNG đụng DB) đủ tổ hợp cờ:
- A (edit+cancel): Sửa · In · Hủy = 3 inline, không menu ✓
- B (create_import+deny): Tạo phiếu nhập kho · Từ chối · In = 3 inline ✓
- C (đủ 5 cờ): Sửa · Tạo phiếu nhập kho · ⋮ (2 inline + menu) → menu chứa Từ chối/In/Hủy ✓
- D (chỉ In): 1 inline ✓
- Mã phiếu đều là link chi tiết ✓ · nút danger (Từ chối/Hủy) có class `is-danger` ✓
