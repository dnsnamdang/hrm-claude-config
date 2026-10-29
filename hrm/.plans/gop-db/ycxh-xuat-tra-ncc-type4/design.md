# YCXH loại 4 — Xuất trả nhà cung cấp (XUAT_TRA_NCC) — Design (tóm tắt)

> Trạng thái: SPEC XONG, chờ user review. Loại thứ 2/3 đợt này (15 ✅ → 4 → 17).
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-17-ycxh-xuat-tra-ncc-type4-design.md`

## Mục tiêu
Port loại xuất 4 (XUAT_TRA_NCC) từ ERP sang HRM, trọn chuỗi, **cả 2 kiểu** direct + non-direct.

## Chốt quan trọng
- **Nguồn phiếu = YCNH** (`Modules/Finance` ProductImportRequest), KHÔNG phải ĐNNK (giả định cũ đã SAI).
- Hạch toán: **Nợ 3311 / Có 156 / Có 33311** (công nợ NCC; không doanh thu/632). Giá vốn bình quân dùng `WarehouseExportAccountingService` sẵn có (không ép giá 0).
- Khóa dòng = product_id + unit_id + {order_import_detail_id, inland_notify_detail_id, rule_inland_notify_detail_id}. Cả 3 cột đã có sẵn trên 3 bảng chi tiết → **không migration**.
- Side-effect finalize: `returned_qty +=`; loại 12 trừ arrived+allocated; loại 13 trừ allocated; `exported_qty +=`; YCXH status 5.

## Quyết định đã chốt (2026-10-17)
1. **Phạm vi = parity đầy đủ (option A)**: mọi loại mua hàng `canSupplierReturn` cho phép {1,2,12,13,15}, giữ mọi side-effect, hạch toán theo loại.
2. **Cả 2 chuỗi** direct + non-direct ("2 kiểu").
3. **LÀM ĐÚNG ERP, KHÔNG TỰ BỔ SUNG** — mirror 1:1, kể cả chỗ ERP lệch: show chỉ 2/12, map HĐ hạch toán chỉ 2/15, side-effect chỉ 12/13; KHÔNG lấp khoảng trống, KHÔNG thêm nhánh.
