# BOM List — Xuất Excel & In (tham chiếu màn Báo giá)

**Người phụ trách:** @namdangit
**Ngày tạo:** 2026-08-27

## Mục tiêu

Bổ sung chức năng **IN** cho bản ghi BOM List theo đúng khuôn đang chạy ở màn Báo giá
(`/assign/quotations`): nút In ở dòng danh sách → popup cấu hình cột → popup xem trước → in.
Xuất Excel của BOM List **giữ nguyên** (đã có sẵn).

## Hiện trạng trước khi làm

| | Báo giá | BOM List |
| --- | --- | --- |
| In 1 bản ghi | Nút 🖨 ở dòng danh sách → `QuotationPrintConfigModal` → `QuotationPrintPreview` | **Chưa có** |
| Xuất Excel 1 bản ghi | Màn chi tiết + màn sửa (`/export-quotation-data`) | Màn chi tiết + màn sửa (`BomExportModal` → `/export`) |
| Xuất Excel danh sách | Không có | Có (toolbar → `/export-list`) |

## Quyết định đã chốt (2026-08-27)

1. **Vị trí nút In**: dòng ở màn danh sách `/assign/bom-list` **và** footer màn chi tiết
   `/assign/bom-list/{id}`. KHÔNG thêm ở màn sửa (`/edit`).
2. **Bản in KHÔNG có cột giá.** BOM List đã bỏ quản lý giá (`BomBuilderEditor.vue` —
   `visibleColumns.estimatedPrice/salePrice/amount/profitMargin = false`, giá nằm ở Báo giá).
   In cột giá sẽ ra toàn số 0 → bỏ hẳn, không cần gate quyền "Xem giá vốn hàng hoá" ở bản in.
   Cột chọn được: STT, Mã hàng, Tên hàng, Model, Thương hiệu, Xuất xứ, ĐVT, Thông số kỹ thuật,
   Ghi chú, Số lượng + tuỳ chọn "Hiện hàng hoá cấp con".
3. **Khối đầu bản in là tài liệu NỘI BỘ**, không copy khuôn "Kính gửi / Hiệu lực / Đại diện
   kinh doanh" của báo giá: letterhead công ty + tiêu đề `DANH MỤC VẬT TƯ (BOM LIST)` + Mã BOM,
   Tên BOM, Dự án, Giải pháp, Hạng mục, Khách hàng, Loại BOM, Trạng thái, Người tạo, Ngày tạo, Ghi chú.
4. **KHÔNG thêm Xuất Excel theo dòng** ở màn danh sách — giữ chốt cũ: xuất 1 BOM làm ở màn
   Chi tiết / Sửa (giống báo giá).
5. **In bằng IFRAME ẨN**, không `window.open` — theo `.claude/skills/print-page/SKILL.md` mục 4a
   (window.open làm select2 ở màn danh sách chết focus trên Windows). Báo giá đang còn dùng
   `window.open`, màn BOM làm đúng ngay từ đầu.
6. **Một nguồn CSS** cho cả xem trước và bản in (`printCss(root)`), theo skill mục 8a.

## Ảnh hưởng

- BE: `DetailBomListResource` trả thêm tên hiển thị (dự án / giải pháp / phân hệ / loại BOM /
  phòng người tạo) để bản in ở màn chi tiết không phải gọi thêm API. `loadDetail()` eager load
  kèm để không sinh N+1.
- FE: 2 component mới + 1 mixin dùng chung cho 2 màn (danh sách + chi tiết).

Spec chi tiết: `docs/superpowers/specs/2026-08-27-bom-list-print-design.md`
