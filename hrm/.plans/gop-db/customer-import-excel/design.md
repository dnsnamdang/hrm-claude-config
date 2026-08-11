# Import Excel Khách hàng — Tóm tắt

- Nhánh: `gop_db` · Người làm: @khoipv · Bắt đầu: 2026-08-10
- Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-10-customer-import-excel-design.md`

## Mục tiêu

Bổ sung Import Excel cho màn `/assign/customers` (HRM) — chức năng ERP đã có
(`Sale\CustomersController@importExcel`) mà HRM còn thiếu.

Khảo sát đối chiếu 2026-08-10: ERP có ~30 import Excel, phần lớn thuộc nghiệp vụ HRM không có
(kho, tồn đầu kỳ, kiểm kê, hàng hoá, công nợ đầu kỳ). Ba chức năng ERP có mà HRM còn thiếu màn tương
ứng: **Khách hàng**, Quốc gia (`human/nations`), Thôn/xóm (`human/hamlets`).
User chốt chỉ làm **Khách hàng**; 2 cái còn lại để sau.

## Quyết định lớn

| # | Quyết định |
| --- | --- |
| 1 | Bộ cột = 24 cột file mẫu ERP (giữ nguyên thứ tự) + 1 cột Lĩnh vực kinh doanh = **25 cột** → file cũ của ERP dán sang vẫn chạy |
| 2 | Danh mục (nhóm KH, quốc gia, tỉnh, huyện, xã, thôn) **tra theo tên, không tự tạo mới** — vì chung `gop_db`, tự tạo sẽ sinh rác trong danh mục ERP |
| 3 | Nhiều liên hệ / TK ngân hàng: bỏ trống cột Tên = dòng con của KH phía trên (đúng cách ERP) |
| 4 | Trùng MST / CCCD → báo lỗi, bỏ qua. Import **chỉ tạo mới**, không cập nhật đè |
| 5 | UI theo `V2BaseImportModal` 4 bước; **một cột duy nhất** cho Loại hình + Lĩnh vực, dạng cặp `MãLoạiHình:MãLĩnhVực` giống hệt màn `/assign/application` — loại hình suy ra từ vế trái, không có cột riêng |
| 6 | Import gọi lại đúng `CustomerService::save()` — không dựng nhánh ghi thứ hai |

## Ràng buộc kỹ thuật đáng nhớ

- `V2BaseImportModal.handleImport()` chỉ gửi dòng `__isValid` → nếu cha/con lệch cờ thì nhóm bị xé đôi.
  ⇒ **`isValid` đồng bộ theo nhóm**: cả nhóm hợp lệ hoặc cả nhóm bị loại.
- Props `requiredFields` / `validationRules` của `V2BaseImportModal` hiện **khai báo nhưng chưa được gọi**
  → cổng validate thật nằm hoàn toàn ở BE.
- `CustomerService::save()` bắt buộc user có `employee_info_id` + bản ghi `employees` tương ứng
  → chặn sớm bằng 1 lỗi chung thay vì để chết từng dòng.
- Không dùng `mysql2` (quy tắc nhánh `gop_db`).

## Phạm vi

Không migration, không permission mới (dùng lại `erpPermission:Thêm khách hàng`),
không sửa `CustomerService::save()`, không đụng import bên ERP.
