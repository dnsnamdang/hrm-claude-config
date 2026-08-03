# Design — Xuất / Nhập phục vụ sản xuất (production-stock-io)

- Người phụ trách: @manhcuong
- Spec chi tiết: `docs/superpowers/specs/2026-07-02-production-stock-io-design.md`
- Phân hệ: Quản lý kho — `Modules/Warehouse` + `pages/warehouse`

## Mục tiêu

Quản lý luồng kho của sản xuất: **Lệnh sản xuất** (nhiều thành phẩm + SL kế hoạch, bung NVL gộp từ BOM, sửa được) → xuất NVL / nhập thành phẩm bằng **phiếu kho hiện có mở rộng loại mới**, lập nhiều đợt, chặn cứng vượt SL lệnh.

## Quyết định lớn

1. **Kiến trúc**: KHÔNG tạo phiếu riêng — `WhIssue` thêm loại 3 "Xuất phục vụ sản xuất", `WhReceipt` thêm loại 4 "Nhập từ sản xuất", cả 2 thêm `production_order_id`. Entity mới chỉ có Lệnh sản xuất (3 bảng: `production_orders` + `production_order_products` + `production_order_materials`).
2. **Workflow lệnh**: Nháp → Chờ duyệt → Đã duyệt / Từ chối → Hoàn thành (bấm tay, confirm cảnh báo nếu chưa đủ; sau hoàn thành khoá tạo/duyệt phiếu gắn lệnh).
3. **NVL**: bung từ BOM (định mức × SL × (1+hao hụt%), gộp trùng NVL, snapshot) — cho sửa/thêm/xóa; thành phẩm không BOM chỉ cảnh báo.
4. **Chặn vượt**: tại bước Duyệt phiếu, theo `quantity_base`, tổng đã duyệt + phiếu hiện tại ≤ SL lệnh (từng product); vẫn assertEnough tồn như cũ.
5. **Không đơn giá** trên phiếu loại sản xuất; kho chọn trên từng phiếu; không scope cấp.
6. **Permission** 1139 Xem / 1140 Thêm sửa / 1141 Duyệt lệnh sản xuất (type=10, Duyệt gồm Từ chối + Hoàn thành).
7. **Sửa/xóa lệnh**: sửa Nháp/Từ chối, xóa chỉ Nháp (như phiếu kho).

Chi tiết schema, API, validation, edge cases, downstream impact: xem spec.

## Mở rộng sau bàn giao core (2026-07-03, Phase 5-8)

1. **Phase 5 — form/list**: auto bung NVL theo BOM khi bảng thành phẩm đổi (bỏ nút, debounce + confirm khi NVL sửa tay); icon popup xem BOM công thức từng thành phẩm (endpoint `product-bom/{id}`); trường Người phụ trách SX (`manager_id`, migration 2026_07_03_000001); 4 button workflow trên cột Thao tác của list.
2. **Phase 6 — dashboard kho**: key `production_orders` (KPI chờ duyệt/đang thực hiện/hoàn thành trong kỳ + 10 lệnh đang chạy kèm % tiến độ, quá hạn); FE card KPI + khối bảng, gate quyền Xem lệnh sản xuất.
3. **Phase 7 — liên kết HĐ bán**: `contract_id` nullable (null = SX tồn kho; chỉ gắn HĐ Đã duyệt — migration 2026_07_03_000002); form chọn mục đích SX + đổ dòng hàng HĐ vào bảng TP; detail HĐ bán hiện 2 cột SL đặt SX/SL SX đã nhập (loại lệnh Từ chối khỏi SL đặt) + khối lệnh SX. Kèm fix bug BOM trong form hàng hoá: ĐVT dòng NVL theo product_units của NVL.
4. **Phase 8 — BomDemoSeeder**: 10 TP SXTP.0001-0010 + BOM ≥3 NVL/công thức, idempotent.

E2E: core 11/11 + Phase 5-7 16/16 PASS. Deploy: tổng 9 migration + 3 permission 1139-1141 insert tay.
