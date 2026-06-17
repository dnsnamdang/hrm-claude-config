# Mở rộng Hàng hoá (DM-08+DM-01) — Plan

> **Checkpoint 2026-06-05: HOÀN THÀNH** (BE+FE, chạy main chưa commit). BE smoke-test pass (classification + supplier_name + conversion_rate 1/24 + default_bom_name). FE: ProductForm thêm phân loại + NCC/BOM mặc định (ẩn/hiện) + cột Tỷ lệ quy đổi; index thêm filter phân loại. KHÔNG phá logic giá/ảnh/units cũ (đã review). Còn: user test UI.

> Subagent-driven. KHÔNG commit. Sửa product catalog đang có (đọc kỹ file hiện tại trước khi sửa).
**Spec:** `docs/superpowers/specs/2026-06-05-product-catalog-extend-design.md`

## Phase 1 — BE
- [ ] 2 migration (conversion_rate vào product_units; classification/supplier_id/default_bom_id vào products)
- [ ] ProductUnit + Product entity (fillable, relations supplier/defaultBom, accessor, classification const)
- [ ] ProductRequest (3 rule mới + units.*.conversion_rate)
- [ ] ProductService (lưu field mới + conversion_rate)
- [ ] Transformers (classification_name, supplier_name, default_bom_name, conversion_rate)
- [ ] ProductController show load supplier+defaultBom

## Phase 2 — FE
- [ ] ProductForm: phân loại + NCC/BOM mặc định (ẩn/hiện) + cột Tỷ lệ quy đổi
- [ ] index.vue: filter Phân loại + hiển thị classification_name

## Phase 3 — Test
- [ ] mua sẵn+NCC; SX+BOM mặc định; conversion_rate; ĐVT cơ bản=1

---

## Phase 4 — Chỉnh quy tắc giá + conversion_rate số nguyên (2026-06-05)
> Checkpoint HOÀN THÀNH (FE+BE, chạy main chưa commit).
> User: "P3/P5/P7/P10 đang giảm % → đổi thành TĂNG %; Tỷ lệ quy đổi để số nguyên."
- [x] ProductForm onPriceP0Change: P3=+3%, P5=+5%, P7=+7%, P10=+10% (×1.03/1.05/1.07/1.10) thay cho giảm
- [x] conversion_rate: migration product_units `decimal`→`integer` + ALTER bảng; ProductRequest rule `integer` + message VN; input thêm step="1"
- [x] Test: conversion_rate decimal → 422 "Tỷ lệ quy đổi phải là số nguyên"

---

## Phase 5 — Trạng thái "Nháp" + nút Lưu nháp/Lưu (hàng hoá & BOM) (2026-06-05)
> Checkpoint HOÀN THÀNH (FE+BE). User: bỏ "Lưu & tiếp tục", thay bằng "Lưu nháp" + "Lưu"; thêm trạng thái Nháp.
- [x] BE: Product + Bom thêm `STATUS_DRAFT=3`; isCanEdit cho phép ACTIVE+DRAFT; ProductService/BomService guard updateOrCreate+update cho phép sửa bản Nháp; ProductRequest status in:1,2,3
- [x] FE ProductForm: bỏ select Trạng thái (chỉ hiện badge ở view), footer dùng `submit_and_draft`(→status 3) + `submit_form`(→status 1), bỏ "Lưu & tiếp tục"; submitForm(saveStatus) luôn về list
- [x] FE AddBomModal: bỏ select Trạng thái, nút "Lưu nháp"(3)/"Lưu"(1) thay "Lưu & Tiếp tục"; submitForm(saveStatus)
- [x] FE list products + boms: thêm filter + badge "Nháp" (vàng), ẩn nút khoá cho bản Nháp; thêm css tpl-status-draft
- [x] Test BE: tạo Nháp(status=3), sửa Nháp→Lưu(1), BOM Nháp→Lưu(1) đều 200

---

## Phase 6 — Chuẩn hoá hiển thị Trạng thái (text+màu từ BE, FE dùng V2BaseBadge) (2026-06-05)
> Checkpoint HOÀN THÀNH. Quy tắc đã ghi vào CLAUDE.md.
- [x] BE: trait `Modules\Category\Entities\Concerns\HasStatusBadge` (accessor status_name/status_color, mặc định Hoạt động/Khoá); gắn vào 10 entity category; Product+Bom khai báo `const STATUSES` (thêm Nháp #D97706)
- [x] BE: 10 list resource + DetailProduct/DetailBom resource trả status_name + status_color
- [x] FE: 10 màn /category/*/index.vue thay renderStatus HTML → `<V2BaseBadge :color="item.status_color">{{ item.status_name }}</V2BaseBadge>`, xoá renderStatus
- [x] FE: ProductForm + AddBomModal view-badge dùng V2BaseBadge (status_name/color từ detail), bỏ computed map cũ
- [x] CLAUDE.md: thêm mục "Convention hiển thị Trạng thái (status)"
- [x] Test: 5 endpoint list trả status_name/status_color đúng; accessor Product/Manufacturer/Warehouse OK
