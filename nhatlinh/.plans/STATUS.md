# STATUS.md

## Đang làm

- product-bom-inline → @manhcuong → .plans/product-bom-inline/plan.md
  Spec: docs/superpowers/specs/2026-06-06-product-bom-inline-design.md
  Đổi BOM thành inline trong tab hàng hoá (lưu nested), bỏ hẳn danh mục BOM riêng + permission BOM. Mỗi SP ≤1 BOM = bảng NVL; bỏ Mã/Tên BOM; status theo hàng hoá.
  Checkpoint 2026-06-06: **CODE HOÀN THÀNH** (BE+FE, subagent-driven, chạy main chưa commit). BE smoke-test 5 kịch bản PASS; FE compile sạch; đã xoá trang/menu/route/permission BOM. Còn: user test trình duyệt.

- MODULE 1 — Danh mục & Cấu hình: **CODE HOÀN THÀNH TOÀN BỘ** (2026-06-05, chạy main chưa commit).
  Tất cả BE smoke-test pass + FE reviewed. Còn lại: user test UI trên app + tạo file mẫu import .xlsx + commit.
  - DM-03 product-type-hierarchy (nhóm hàng cha-con, list đã đổi về phẳng theo yêu cầu)
  - DM-04 supplier-category (NCC + nhóm NCC + liên hệ)
  - DM-05 customer-category (KH mới `category_customers` + loại trường + liên hệ)
  - DM-06 warehouse-category (Kho + loại kho + thủ kho)
  - DM-02 product-bom (BOM nhiều/sp + default + dòng NVL + lịch sử)
  - DM-08+DM-01 product-catalog-extend (quy đổi ĐVT + phân loại mua sẵn/SX + NCC/BOM mặc định)
  Permission đã thêm: NCC 1097-98, nhóm NCC 1099-1100, KH 1101-02, Kho 1103-04, BOM 1105-06 (gán Super admin).

- supplier-category → @manhcuong → .plans/supplier-category/plan.md
  DM-04 — Nhà cung cấp + Nhóm NCC (2 entity + supplier_contacts).
  Checkpoint 2026-06-05: CODE HOÀN THÀNH (BE+FE, chạy main chưa commit). BE smoke-test pass. Còn: user test UI + tạo file mẫu import. Tiếp theo: #3 unit-conversion (DM-08) hoặc #4 customer-category (DM-05).

- product-type-hierarchy → @manhcuong → .plans/product-type-hierarchy/plan.md
  Spec: docs/superpowers/specs/2026-06-04-product-type-hierarchy-design.md
  DM-03 — đổi tên "Loại hàng hoá" → "Nhóm hàng hoá" + phân cấp cha-con (tree-table).
  Checkpoint 2026-06-04: CODE HOÀN THÀNH (BE+FE, chạy trên main chưa commit). BE đã smoke-test pass (tinker). Còn lại: user test UI trên app + tạo file mẫu import .xlsx. Tiếp theo: feature #2 supplier-category (DM-04).

- product-catalog → @manhcuong → .plans/product-catalog/plan.md
  Spec: docs/superpowers/specs/2026-06-03-product-catalog-design.md

## MODULE 1 — Danh mục & Cấu hình (overview)

- Bản đồ phân rã 7 feature: docs/superpowers/specs/2026-06-04-module-1-danh-muc-overview.md
- Thứ tự: (1) product-type-hierarchy DM-03 ← đang làm, (2) supplier-category DM-04, (3) unit-conversion DM-08, (4) customer-category DM-05 (entity KH MỚI trong Category, KH chính thức ERP), (5) warehouse-category DM-06, (6) product-bom DM-02, (7) product-catalog mở rộng DM-01.

## Chờ

- claude-config-repo → @manhcuong → .plans/claude-config-repo/plan.md
  Spec: docs/superpowers/specs/2026-05-16-claude-config-repo-design.md

## Đã làm

- manufacturer-category → @manhcuong → .plans/manufacturer-category/plan.md
  Hoàn thành: 2026-06-01 — CRUD + Import/Export + Lock/Unlock, code HSX.XXXX

- country-of-origin-category → @manhcuong → .plans/country-of-origin-category/plan.md
  Hoàn thành: 2026-06-01 — CRUD + Import/Export + Lock/Unlock, code NSX.XXXX

- product-type-category → @manhcuong → .plans/product-type-category/plan.md
  Hoàn thành: 2026-06-01 — CRUD + Import/Export + Lock/Unlock, code LHH.XXXX

- unit-category → @manhcuong → .plans/unit-category/plan.md
  Hoàn thành: 2026-06-01 — CRUD + Import/Export + Lock/Unlock, code DVT.XXXX

- ke-toan-module-scaffold → @manhcuong → .plans/ke-toan-module-scaffold/plan.md
  Hoàn thành: 2026-04-21 — Giữ làm mẫu chuẩn cho task scaffold module mới.
