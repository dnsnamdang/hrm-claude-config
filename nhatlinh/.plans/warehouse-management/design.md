# Quản lý kho (Warehouse Management) — Tóm tắt

**Ngày:** 2026-06-28 · @manhcuong · Spec đầy đủ: `docs/superpowers/specs/2026-06-28-warehouse-management-design.md`
Module mới `Modules/Warehouse` + `pages/warehouse`.

## Mục tiêu
Phân hệ quản lý kho greenfield: Nhập / Xuất / Chuyển / Kiểm kê + Báo cáo Tồn kho & Thẻ kho. Nền danh mục Kho, Hàng hoá (đa ĐVT), NCC, Hợp đồng bán đã có.

## Quyết định lớn
- **Engine hướng A**: sổ cái `stock_movements` (nguồn sự thật) + cache `inventories` (tồn hiện tại). `StockService.postMovement` ghi tồn trong transaction + `lockForUpdate`.
- **Chỉ số lượng** (không giá vốn). Tồn theo (kho, hàng hoá, ĐVT cơ bản); không lô/hạn/vị trí.
- **Workflow** Nháp→Chờ duyệt→Đã duyệt/Từ chối; **tồn chỉ đổi khi DUYỆT**. Đã duyệt = khóa, **không hoàn tác** (muốn sửa → phiếu điều chỉnh).
- Phiếu chọn **ĐVT bất kỳ** → quy đổi `quantity_base = quantity * conversion_rate`.
- **Xuất**: gắn HĐ (load dòng còn thiếu, chặn vượt HĐ) hoặc tự do; "SL đã xuất" trên HĐ tính động.
- **Chặn cứng tồn âm** khi xuất/chuyển vượt tồn.
- Phiếu nhập có **chọn NCC** (danh mục `suppliers`).
- **Không scope theo cấp** (có quyền xem = thấy hết); vẫn lưu company/department/part_id.
- Permission nhóm mới, ID từ **1124**, type riêng "Phân hệ Quản lý kho".

## Phân chia phase
- **P1** Engine + Nhập kho
- **P2** Xuất kho (+ HĐ, cập nhật SL đã xuất)
- **P3** Chuyển kho
- **P4** Kiểm kê
- **P5** Báo cáo Tồn kho + Thẻ kho + Excel

→ Mỗi phase có design-phase{N}.md + tasks trong plan.md.
