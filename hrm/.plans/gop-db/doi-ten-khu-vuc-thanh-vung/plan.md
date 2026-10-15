# Plan — Đổi tên "Khu vực" → "Vùng"

## Phase 1
### FE (hrm-client)
- [x] Menu master-data label
- [x] Màn Vùng `pages/human/areas` (index + AreasModel): tiêu đề, placeholder, popup xác nhận, toast, import (header + alias cũ, sheetName)
- [x] Ô lọc / cột / popup ở Tỉnh/TP, Quận/Huyện, Phường/xã, Đường/phố (index + Model) + alias import Tỉnh/TP
### BE (hrm-api)
- [x] ExportColumnRegistry, CatalogHistoryService (nhãn cột/lịch sử)
- [x] Message Area/Nation/Province entity, CreateAreasRequest, AreaService, ProvinceService, AreaController title
- [x] Comment liên quan + unit test (CatalogImportFixesTest, ProvinceImportValidationTest)
### Verify
- [x] Grep lại còn sót, php -l, compile vue template

### Checkpoint — 2026-10-08
Vừa hoàn thành: đổi chữ Khu vực → Vùng ở 13 file FE + 21 file BE; alias import giữ tên cũ; file export `danh_muc_vung.xlsx`, mẫu import `Mau_import_vung.xlsx`.
Verify: php -l pass; PHPUnit CatalogImportFixesTest + ProvinceImportValidationTest — các case vùng pass, 2 case lỗi sẵn không liên quan (mã bưu chính, biển số xe); compile template/script FE pass.
Bước tiếp theo: user mở trình duyệt kiểm menu + 5 màn Địa lý.
Blocked:

## Phase 2 — rà soát lại (sau khi pull commit "fix bug")
- [x] Cột import Vùng ở Quận/Huyện, Đường/phố, Phường/xã (label, placeholder, hint, alias cũ giữ lại)
- [x] BE ImportsGeoColumns (câu lỗi "Không tìm thấy vùng…", "…không thuộc vùng…"), comment Ward/Hamlet/District Service, Area.php
- [x] Báo cáo phân chia thị trường (division-market): ô lọc Vùng
- [x] Menu sale-hub: tên báo cáo "Từng vùng…", "So sánh theo vùng…"
- [x] Test WardImportValidationTest + GeoImportColumnsTest

### Checkpoint — 2026-10-08 (rà soát lần 2)
Vừa hoàn thành: đổi nốt 5 FE + 8 BE. WardImportValidationTest 5/5, GeoImportColumnsTest 3/3 pass; compile FE pass.
Cố ý giữ: "Khu vực 1/2" báo giá dự án cha, khối KHU VỰC file Excel báo giá, báo cáo theo tỉnh (assign_task_by_province), bảo hiểm, địa chỉ, mockData, migration cũ.
Bước tiếp theo: user kiểm trình duyệt.
Blocked:
