# Lịch sử thay đổi — phân hệ Kho (tóm tắt)

> @khoipv · 26/11/2026 · Spec đầy đủ: [docs/superpowers/specs/2026-11-26-lich-su-thay-doi-kho-design.md](../../docs/superpowers/specs/2026-11-26-lich-su-thay-doi-kho-design.md)

## Mục tiêu
Thêm lịch sử thay đổi chuẩn hrm (`entity-history`) cho 4 màn Kho: Phiếu nhập kho, Phiếu đề nghị xuất kho,
danh mục Kho vật lý, danh mục Kho kế toán — ai sửa trường nào, cũ → mới, lúc nào, kèm ghi chú / lý do.

## Quyết định lớn
- Engine BE dùng chung mới `App\CommonServices\EntityHistoryService` (port lõi `CatalogHistoryService` hrm, bỏ bảng nhãn cứng — snapshot khóa nhãn tiếng Việt).
- PNK / ĐNXK: thêm `old_value`/`new_value` vào bảng log sẵn có (log cũ vẫn hiện). Danh mục: bảng mới `catalog_histories`.
- 1 endpoint: `GET warehouse/histories/{type}/{id}` (+ `/filter-options`), không thêm quyền — xem được màn là xem được lịch sử.
- FE: component mới `components/history/` (SystemInfoSection, SystemInfoValue, EntityHistoryModal) port từ hrm; thay timeline cũ ở PNK / ĐNXK; ⋮ "Lịch sử" ở 4 danh sách; khối Lịch sử trong popup Xem danh mục.
- Bảng con ghi theo khóa bảng (thêm / xóa / sửa từng dòng): hàng hóa, chi tiết lô/HSD/seri, file đính kèm.
- Lưu không đổi gì → không ghi dòng "Thay đổi thông tin". Xóa bản ghi → không ghi.
