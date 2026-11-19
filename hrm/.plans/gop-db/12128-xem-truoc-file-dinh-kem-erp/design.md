# #12128 — Xem trước file đính kèm trên mọi phiếu (ERP)

**Người phụ trách:** @junfoke — 2026-11-12
**Redmine:** http://quanly.dnsmedia.vn/issues/12128 (Quản trị · Web App, không có ảnh)
**Repo / nhánh:** `TanPhatDev` — `task_12128` tách từ `gop_db`, merge vào `develop_02` (dev test) để QA trước.
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-11-12-12128-xem-truoc-file-dinh-kem-erp-design.md`

## Mục tiêu

Cạnh mọi file đính kèm trên phiếu ERP có nút **Xem trước** → mở popup xem file ngay trên phần mềm, không tải về.
Định dạng không xem được ⇒ "Định dạng file chưa hỗ trợ xem trước" + nút Tải xuống. Giữ nguyên chức năng tải.

## Quyết định đã chốt (user, 12/11/2026)

| # | Quyết định |
| --- | --- |
| Q1 | Làm **toàn bộ màn**, không chỉ vài màn |
| Q2 | "Cửa sổ mới" trong issue = **popup** trên trang (mở tab mới bất tiện) |
| Q3 | Quyền: **coi như đạt** — chỉ ai vào được phiếu mới thấy nút. File S3 vẫn public như cũ |
| Q4 | Cơ chế xem **giống HRM** (`FilePreviewModal.vue`), **không thêm backend** |
| Q5 | (12/11 chiều, theo ảnh mẫu user gửi) Ô file thành **thẻ**: icon màu theo loại + tên + "Xem trước", nút tải góc phải trên. **Bấm bất kỳ đâu = xem trước, CHỈ icon tải về mới tải.** Link lẻ: bấm link = xem trước, icon tải đứng sau. Icon dùng **Material Symbols Outlined** (Google Fonts, chỉ nạp các icon cần) — ERP chỉ có FA4 không có icon giống mẫu |

## Cách làm (1 partial, 0 sửa từng màn)

- `resources/views/partials/common-js/file-preview.blade.php`, include 1 lần trong `layouts/app`.
- Directive AngularJS tên `a` (`ng-app` ở `<body>`) tự gắn 👁 vào mọi `<a>` trỏ tới file đính kèm (host S3 hoặc `/uploads/`, `/storage/` cùng domain):
  góc trái `.document-item` (~210 màn), góc `.gallery-file`, hoặc ngay sau link lẻ (~70 link ở ~33 màn). Cùng URL trong 1 khối chỉ 1 nút.
- Ô chọn file mới trong `.document-item` → 👁 xem file chưa lưu (blob).
- Xem: ảnh `<img>`; PDF/txt/csv Google Docs Viewer; Word/Excel/PowerPoint Office Online; khác → báo chưa hỗ trợ.

## Giới hạn (giống HRM)

- Google Viewer chậm (~10s PDF), thỉnh thoảng trắng → nút Tải lại / Tải xuống. Office Online ≤ ~10 MB, cần URL public.
- File Office chưa lưu không xem được (báo "chỉ xem được sau khi lưu phiếu").
- Danh sách DataTables (jQuery render, không qua Angular compile) không có nút — ngoài phạm vi "phiếu".
