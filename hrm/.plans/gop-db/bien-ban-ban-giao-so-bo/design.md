# Biên bản bàn giao sơ bộ (ERP → HRM) — @khoipv

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-11-04-bien-ban-ban-giao-so-bo-design.md`

## Mục tiêu
Port màn ERP `handoverRecords.index?type=all` (CSKH › Hồ sơ công việc › Biên bản bàn giao sơ bộ; cùng link ở
CSKH › Chăm sóc khách hàng › Phiếu CSKH) sang HRM trọn bộ: Danh sách · Tạo · Sửa · Chi tiết · Duyệt / Từ chối · Xoá.
Biên bản gom 1..n phiếu xuất kho cùng khách hàng, chụp lại dòng hàng từ lô phiếu xuất.

## Quyết định (user chốt 04/11/2026)
- Quyền **y ERP: không có quyền nào** — ai đăng nhập cũng xem / tạo / sửa / xoá / duyệt; cờ hành động theo trạng thái.
- Sửa 3 lỗi ERP ở **cả HRM lẫn ERP**: Xoá chạy được (xoá cứng Đang tạo | Từ chối) · Duyệt / Từ chối chỉ khi Chờ duyệt ·
  popup phiếu xuất kho chỉ công ty người tạo.
- Menu **cả 2 chỗ như ERP** (Hồ sơ công việc + "Phiếu CSKH").
- Bộ bắt buộc HRM (Xuất Excel, Cấu hình cột, Lịch sử 2 nơi, Lưu và tiếp tục) + **In danh sách + In biên bản** (mẫu HRM).
- "Đang tạo" đổi màu xám (ERP xanh dương).

## Phạm vi code
- BE `Modules/CustomerCare`: entity `HandoverRecord(+Product)`, `HandoverRecordService` (list/chi tiết/xoá/duyệt/lịch sử/
  nguồn phiếu xuất), `HandoverRecordStoreService` + `HandoverRecordRequest`, `HandoverRecordPrintService`,
  `HandoverRecordNotifier`, controller + route `/v1/customer-care/handover-records`; đăng ký `ExportColumnRegistry`,
  `CatalogHistoryService::TABLES`, prefix `BBBGSB` ở `NotificationMeta`.
- FE `pages/customer-care/handover-records/` (index, create, `_id/index`, `_id/edit`) + `HandoverRecordForm.vue`
  + `WarehouseExportPickerModal.vue` + `handoverRecordActions.js`; menu `subsystem-menu/customer-care.js`.
- ERP (`D:\laragon\www\erp`, nhánh gop_db, chưa commit): `HandoverRecordsController`, `WarehouseExport`, `show.blade.php`.

## Rủi ro / còn lại
- Chưa bấm thử trình duyệt (user tự test); chưa upload S3 thật.
- Local 0 biên bản → chưa đối chiếu dữ liệu ERP cũ trên prod.
