# #12135 — Import ĐM công đi lại (HRM) + Xuất Excel DM tuyến đường (ERP)

Người phụ trách: @junfoke · Redmine http://quanly.dnsmedia.vn/issues/12135 · file nghiệp vụ QA: `Import_DM_Cong_Di_Lai.xlsx` (bản 11/11/2026, đã bỏ cột Số km)

## Phạm vi
1. HRM `/assign/moving_norms`: nút **Import Excel** (V2BaseImportModal 4 bước) — ghi định mức cho **công ty người đang thao tác** (`current_company_role`), quyền `assign.danh_muc_dinh_muc_cong_di_lai.manage`.
2. ERP `/admin/roads`: nút **Xuất Excel** theo đúng bộ lọc đang chọn — STT · Tên · Km · Trạng thái · Người tạo · Ngày tạo · Người sửa gần nhất · Ngày sửa.

## Quyết định đã chốt (12/11/2026)
- Nhánh HRM: `feat/12135-import-dm-cong-di-lai` tách từ `origin/gop_db` (cả api + client). ERP: thẳng `gop_db`.
- **File mẫu giữ y khuôn QA (ngoại lệ khuôn chung `buildImportTemplate`)**: tiêu đề 2 tầng (ô "Chi tiết" gộp trên Phương tiện / Giờ định mức / Giá vé), dòng mô tả nền vàng, sheet ẩn "Hành động" làm ô chọn. Bỏ dòng 1 "Mô tả nghiệp vụ" của file QA (chỉ để user hiểu). Sinh bằng code (`movingNormImport.js`), không thêm file tĩnh.
- Popup chung `V2BaseImportModal` thêm prop tuỳ chọn `parser` (user duyệt) để màn này dùng trình đọc riêng; không truyền thì như cũ.
- Số km: file không có — lấy km của tuyến trong DM tuyến đường ERP (`roads.km`) khi tuyến mới vào định mức; tuyến đã có trong định mức giữ km cũ.
- Tuyến / phương tiện bị khoá: **luôn chặn** (kể cả thêm mới cặp chưa có).
- Giá vé để trống: phương tiện tính theo km → đơn giá × km tuyến (như màn nhập tay); còn lại lấy giá DM phương tiện, không có thì 0.

## Thông báo lỗi (theo spec)
TH1 đã tồn tại → "…đã tồn tại trong công ty <mã>, vui lòng chọn cập nhật" / CẬP NHẬT chưa có → "…chưa tồn tại…, vui lòng Thêm mới" ·
TH2 khoá → "Tuyến đường / Kiểu phương tiện đã bị khóa trong công ty <mã>" · TH3 → "Chưa có tuyến đường / kiểu phương tiện trong công ty <mã>" ·
trùng trong file (tuyến + phương tiện + hành động) → báo mọi dòng trùng.

## File chính
- BE: `Modules/Assign/Services/MovingNormImportService.php`, `MovingNormController@validateImport|import`, route `assign/moving_norms/import[/validate]`
- FE: `components/assign-components/moving-norm/movingNormImport.js`, `pages/assign/moving_norms/index.vue`, `components/V2BaseImportModal.vue` (prop `parser`)
- ERP: `RoadController@export`, `app/ExcelExports/RoadListExport.php`, `reports/exports/list_road.blade.php`, `Road::scopeSearchByFilter` (+ lọc created_by/updated_by — ô lọc có sẵn trên màn nhưng trước đây máy chủ bỏ qua)
