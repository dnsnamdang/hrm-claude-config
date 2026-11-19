# Phiếu xuất điều chỉnh sai số liệu (ERP → HRM) — Design

**Người phụ trách:** @khoipv — 2026-10-27 · Nhánh `develop` (cả 2 repo, nhánh con của `gop_db`)
Plan: `.plans/gop-db/phieu-xuat-dieu-chinh-sai-so-lieu/plan.md` ·
Spec: `docs/superpowers/specs/gop-db/2026-10-27-phieu-xuat-dieu-chinh-sai-so-lieu-design.md`

## Mục tiêu

Port màn ERP `Kho › Xuất kho › Phiếu xuất điều chỉnh sai số liệu` (`warehouseReExport.all`, bảng `warehouse_reexports`,
mã `PXL-xxxxx`) sang HRM `/finance/warehouse-reexports`, phân hệ Kho.

## Luồng nghiệp vụ (giữ y ERP)

PNK bị Kế toán kho "Không duyệt" (4) → người tạo PNK "Tạo phiếu xuất lại" (trừ tồn đúng lô/vị trí, PNK → 5, phiếu xuất lại
"Chờ nhập lại" 2) → "Tạo phiếu nhập lại" (PNK mới) → phiếu xuất lại "Đã nhập lại" 1, PNK cũ → 6.
Luồng tạo đã có từ #11693 (Tri Lee 16/10): `/finance/warehouse-imports/{id}/re-export`. Đợt này KHÔNG đổi logic ghi tồn.

## Quyết định (user chốt 27/10/2026)

1. **4 quyền xem MỚI** (type 21 Kho): "Xem phiếu xuất lại theo tổng công ty / công ty / phòng ban / bộ phận"; không quyền
   ⇒ chỉ phiếu mình tạo (y ERP fallback). Không middleware ở route — phạm vi ở `WarehouseReExportService::scopedQuery()`.
2. **Chuẩn hoá màn chi tiết** đã có theo khuôn nhóm kho (V2BaseFormCard, CreatorInfoLine, V2Footer, 404 không toast).
3. **Làm thêm**: Lịch sử (popup danh sách + khối chi tiết), In phiếu (mẫu blade HRM — ERP In lỗi do hằng
   `PHIEU_XUAT_LAI` không tồn tại), màu "Chờ nhập lại" đỏ → vàng.

## Phạm vi màn

- Danh sách: cột STT · Mã phiếu · Phiếu nhập kho · Ngày tạo · Người tạo · Trạng thái · Hành động; lọc Mã phiếu · Phiếu nhập
  kho · Người tạo · Trạng thái · Ngày tạo · Công ty–Phòng ban; tìm nhanh mã phiếu / mã PNK; sort Mã + Ngày tạo; Xuất Excel;
  Cấu hình cột. Không có Tạo mới / In danh sách (ERP không có).
- Hành động: Tạo phiếu nhập lại (PNK gốc `canReImport`) · In · Lịch sử — dùng chung danh sách + chi tiết.
- Menu: Kho › Xuất kho (chỉ 1 vị trí trong ERP).

Chi tiết API / bảng / edge case: xem spec.
