# Plan: Chọn trường & loại giá khi xuất Excel — màn Quản lý giá hàng hóa

**@khoipv · 2026-06-29**

> Chi tiết code: `docs/superpowers/plans/2026-06-29-product-unit-price-export-fields.md`
> Verify bằng demo HTML (`demos/`) + thủ công trên màn thật. KHÔNG auto-commit.

## Phase 1 — Demo kiểm chứng logic
- [x] Tạo `demos/demo-xuat-excel-gia-hang-hoa.html` (2 nhóm checkbox + ExcelJS export + validate)
- [ ] Thử 4 kịch bản trên trình duyệt (mặc định / bỏ trường / bỏ loại giá / chọn lọc) — user verify
- [x] Cập nhật `demos/README.md`

## Phase 2 — Component modal
- [x] Tạo `components/modal/export-product-price-modal.vue` (2 Select2 multiple + "Chọn tất cả" + validate ≥1/mục, mặc định tích hết, emit `{ fields, priceTypes }`)

## Phase 3 — Trang index.vue (wiring)
- [x] Thêm `EXPORT_FIELDS` (module scope)
- [x] Đăng ký component + computed `exportFieldOptions` + data `exportPriceTypeOptions`
- [x] Đổi nút "Xuất excel" → `openExportModal`, nhúng modal
- [x] Thêm method `openExportModal` (fetch price types → dựng options → show modal)

## Phase 4 — Xuất động
- [x] Sửa `handleExport(selection)` (bỏ fetch price types, nhận selection)
- [x] Sửa `generateWorkbook` dựng cột thông tin + cột giá theo selection (bỏ chỉ số cột cứng, align theo meta)

## Phase 6 — Bổ sung cột "Thông số kỹ thuật" (chỉ ở Excel)
- [x] BE: `ProductUnitPriceResource` trả thêm `content` (Thông số kỹ thuật, HTML) — additive, không ảnh hưởng bảng
- [x] FE: thêm `{ key:'content', label:'Thông số kỹ thuật', width:40 }` vào `EXPORT_FIELDS` (sau Quy cách)
- [x] FE: helper `stripHtml` + strip HTML cho cột `content` trong `generateWorkbook` (CKEditor → text thuần)
- [x] Demo: thêm cột content + dữ liệu HTML mẫu + stripHtml
- [x] Đổi `stripHtml` → `stripHtmlForExport` (copy từ màn category/product — giữ xuống dòng, decode entity)
- [x] Thêm cột `owner_country` "Hãng, nước chủ sở hữu" (đã có sẵn trong resource, không đổi BE)
- [ ] User verify: cột "Thông số kỹ thuật" ra text thuần + cột "Hãng, nước chủ sở hữu" có dữ liệu

## Phase 5 — Verify (chờ user chạy app thật)
- [ ] Kịch bản mặc định (tích hết → file đủ cột)
- [ ] Kịch bản chọn lọc cột
- [ ] Kịch bản validate (chặn + báo đỏ)
- [ ] Kịch bản tôn trọng bộ lọc màn
- [ ] Báo user verify cuối

---
### Checkpoint — 2026-06-29
Vừa hoàn thành: code xong toàn bộ (Phase 1-4) qua subagent-driven, review file-by-file sạch.
  - Demo: `demos/demo-xuat-excel-gia-hang-hoa.html` + README
  - Component: `components/modal/export-product-price-modal.vue`
  - Sửa `pages/category/product_unit_price/index.vue` (EXPORT_FIELDS, openExportModal, handleExport(selection), generateWorkbook động)
Đang làm dở: không
Bước tiếp theo: user verify trên app thật (Phase 5) — mở demo HTML thử 4 kịch bản + chạy màn thật
Blocked: không
