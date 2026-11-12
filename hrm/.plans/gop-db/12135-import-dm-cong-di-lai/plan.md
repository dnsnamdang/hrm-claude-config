# Plan — #12135 Import ĐM công đi lại + Xuất Excel DM tuyến đường

## Phase 1
### BE (hrm-api)
- [x] `MovingNormImportService` validate (TH1/TH2/TH3, trùng file, khoá, giờ/giá) + ghi
- [x] `MovingNormController@validateImport` / `@import`, route + `importRowLimit`
### FE (hrm-client)
- [x] `V2BaseImportModal` prop `parser`
- [x] `movingNormImport.js`: cột, trình đọc khuôn 2 tầng, sinh file mẫu y khuôn QA
- [x] Nút Import Excel + popup ở `pages/assign/moving_norms/index.vue`
### ERP (TanPhatDev)
- [x] `RoadController@export` + `RoadListExport` + blade, nút Xuất Excel theo bộ lọc
- [x] Lọc Người tạo / Người sửa gần nhất ở `Road::scopeSearchByFilter`
### Kiểm
- [x] Tinker: 9 ca validate + ghi (rollback)
- [x] Playwright HRM: tải file mẫu → điền → Load → Validate (2 hợp lệ / 5 lỗi) → Import → danh sách nạp lại; đã trả DB local về như cũ
- [x] Playwright ERP: lọc "Phan Trọng" → Xuất Excel 927 dòng = số dòng bảng

### Checkpoint — 12/11/2026
Vừa hoàn thành: code + test cả 3 repo; commit ở nhánh chức năng (api/client `feat/12135-import-dm-cong-di-lai`,
ERP `feat/12135-xuat-excel-tuyen-duong`, chỉ local); merge --no-ff + push lên dev: api develop 8f3dfff89,
client develop 1e11ea955, ERP develop_02 9c587685ac
Đang làm dở: —
Bước tiếp theo: QA test trên dev-hrm / dev-erp; lên gop_db khi user bảo
Blocked:
