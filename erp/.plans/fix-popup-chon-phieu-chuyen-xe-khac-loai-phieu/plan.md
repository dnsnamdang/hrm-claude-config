# Fix: Popup chọn phiếu ở Chuyến xe khác không tìm được phiếu xuất kho (PXK)

@junfoke · Repo `TanPhatDev` (bản B) · nhánh `master` · ngày 11/09/2026

## Bối cảnh / Bug

Màn **Tạo chuyến xe khác** (`/admin/other_delivery_trips/create`), tích "Tuyến không có sẵn",
chọn nhân viên (Nguyễn Văn Tế) → bấm nút tìm ở cột "Phiếu nhập/xuất kho" → gõ mã `PXK-30276`
(sau đó `PXK-33355`) → popup báo "Không có dữ liệu". Phải **tự chọn ô "Loại phiếu" = Phiếu xuất
kho** thì mới hiện ra.

## Root cause

`SearchController::searchWarehouseExportAndImport()` chọn bảng theo `$request->type2`:
`type2 == 2` → `WarehouseExport`, **còn lại (kể cả rỗng) → `WarehouseImport`**.

Ô "Loại phiếu" trong popup chính là `type2`. Chưa chọn → `type2` rỗng → backend chỉ tra
**bảng phiếu NHẬP**, nên gõ mã `PXK-...` không bao giờ ra kết quả.

Đã loại trừ nguyên nhân nghiệp vụ bằng data prod: PXK-30276 có `status = 1` (khác 3 nên không bị
nhánh `for_other_delivery_trip` ẩn) và người tạo YC xuất hàng = `755` = Nguyễn Văn Tế (khớp filter
`product_export_requester`) ⇒ phiếu hoàn toàn hợp lệ, chỉ sai ở khâu chọn bảng.

**Lưu ý JS**: `edit.blade.php` / `approve.blade.php` có gán `d.type2 = 2` nhưng gán TRƯỚC
`DATATABLE.mergeSearch(d, context)`; mà `mergeSearch` ghi đè `object[column] = $(this).val()` cho
mọi ô search (rỗng khi chưa chọn) ⇒ dòng gán đó gần như vô tác dụng. Vì vậy phải sửa ở **backend**
mới xử lý triệt để cả 3 màn, không phụ thuộc thứ tự chạy của JS.

## Quyết định

Khi **chưa chọn Loại phiếu** thì gộp cả phiếu nhập + phiếu xuất. Chọn rõ 1 loại thì vẫn lọc riêng
như cũ. Không sửa FE: `chooseRequest` đã tự phân biệt qua `warehouse_export_request_id` /
`warehouse_import_request_id` nên danh sách trộn 2 loại vẫn chọn đúng phiếu.

## Tasks

- [x] BE: `SearchController::searchWarehouseExportAndImport()` — tách 3 nhánh: `type2 == 2` → export,
  `type2 == 1` → import, còn lại → `concat()` cả 2 rồi `sortByDesc('created_at')`.
- [x] Verify an toàn: endpoint chỉ có 4 caller — `other_delivery_trips` create/edit/approve và
  `delivery_arrange/report_detail_employee`. Caller cuối hard-code `d.type2 = 2` nên **không đụng
  tới nhánh mới**. 3 caller còn lại luôn truyền `product_export_requester` /
  `product_import_requester` = employee_id nên `->get()` bị chặn theo nhân viên, không kéo cả bảng.
- [x] Verify: `php -l` sạch; `git diff --stat` = 1 file, +10/−1; CRLF nguyên vẹn (3231 CR / 3231 dòng).
- [x] Commit `e331d53870` trên nhánh `master` (user chốt commit thẳng master). **Chưa push.**
- [ ] User verify browser sau khi deploy: mở popup, **không chọn Loại phiếu**, gõ `PXK-33355` → phải ra.
- [ ] User push + deploy.

## ⚠️ Bài học — lần sửa trước bị mất trắng

Lần đầu xử lý lỗi này chỉ sửa file trong working tree mà **không commit**, sau đó working tree bị
dọn sạch ⇒ mất hẳn, nên QA test lại vẫn thấy lỗi y nguyên.
Kiểm lại ngày 11/09/2026: không nhánh nào (`master`, `develop_01`, `task_10696`, `gop_db`) và cả
bản A `/d/CompanyProject/TanPhatDev` chứa bản sửa; `git stash` rỗng.
⇒ **Sửa xong phải chốt nhánh + commit ngay**, không để thay đổi nằm trong working tree qua nhiều ngày.
