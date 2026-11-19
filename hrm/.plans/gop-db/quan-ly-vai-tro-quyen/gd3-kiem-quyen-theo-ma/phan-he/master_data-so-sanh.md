# master_data — so mốc trước / sau (GĐ3 Task 8.17)

- Mốc: `master_data-truoc.json` / `master_data-sau.json` — 1.316 ô = 159 route ScopeSnapshot × 7 tài khoản (1.113 ô) + 29 route băm nội dung
  (`bodysnap.py`: JSON cờ / cột giá vốn, HTML trang có khối `@if can(...)`, tập link menu topmenubar) × 7 (203 ô).
- Mốc trước ổn định: chụp 2 lần trên code HEAD ⇒ ScopeSnapshot 0 ô khác; bodysnap 0 ô khác (sau khi bỏ dòng `phpdebugbar` khỏi HTML — debugbar
  in id/thời điểm request mỗi lần).
- So sau (`ScopeSnapshot diff`): **1.309/1.316 khớp, 7 ô khác** — đều là `x.erp.device_errors.searchData` × 7 tài khoản (kể cả `khong_ma`, 0 mã).

## 7 ô khác — không phải đổi hành vi
`admin/sale/device-errors/searchData` chạy yajra Datatables ở chế độ debug: JSON trả kèm khoá `queries` = danh sách MỌI câu SQL của request.
Bản cũ kiểm tên (`can('Sửa danh mục công việc - lỗi thiết bị')`…) ⇒ checker tra `permission_aliases`; bản mới kiểm mã ⇒ không có câu tra alias ⇒
danh sách `queries` khác, băm JSON khác. Dữ liệu dòng (`data`, cột `action` sinh từ canEdit/canDelete/canLockOrUnlock), `recordsFiltered` không đổi
(ô ScopeSnapshot `erp.device_errors.searchData` khớp 7/7). Tương đương cờ canEdit/canDelete/canLockOrUnlock: `MasterDataScopeConversionTest::
test_moi_ten_cu_tuong_duong_ma` (can(tên) === can(mã) cho mọi tên Catalog ở mọi mức). Các route JSON ERP khác không lệch vì không bật debug `queries`.

## Ô U8
Không có (rehearsal: 0 dòng `master_data.yeu_cau_duyet_hang_tam.view` scope NULL; mọi mã master_data khác không phạm vi).

## Ô lỗi sẵn (cả trước lẫn sau)
- `erp.product-infos.searchData2`: 500 cho mọi tài khoản có mã hàng hoá (200/-1 cho dm, khong_ma do bị chặn trước).
- `api.products.catalogs.products`: 422 (thiếu tham số bắt buộc) với pv4/dm.
- Trang ERP sản phẩm (`products`, `product2`, `product_templates` show/edit/create, `groups`, `scopes`, `editPrices`…): 403 cho mọi tài khoản
  (middleware `productMovedToHrm` — màn đã chuyển sang HRM), y nhau trước/sau.
