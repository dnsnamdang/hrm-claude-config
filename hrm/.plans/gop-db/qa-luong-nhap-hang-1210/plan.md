# Đợt QA luồng nhập hàng 12/10/2026 — Redmine #11635 #11634 #11633 #11631 #11511 #11506

> Phụ trách: @junfoke (user nhận thay Trần Cư, sửa trên `develop` — chốt 12/10/2026)
> Ảnh QA đã tải: scratchpad phiên 12/10 (prnt.sc). Mọi bug "đồng bộ" bám màn mẫu QA chỉ:
> `finance/prepick-transfer-requests/create`, `finance/borrow-export-requests/create`, `finance/bill-income-requests/{id}`.

## Quyết định đã chốt

- #11635 B3/B5: **port luôn** loại "Nhập điều chuyển kho nội bộ" (và các loại tự sinh khác đi qua "Chọn phiếu nhập kho")
  cho màn Phiếu nhập hàng — đủ tab/cột như ERP + hạch toán BE.
- Tiêu đề khối: bỏ in hoa ngay trong `components/V2BaseFormCard.vue` (18 màn luồng xuất nhập cùng đổi), cỡ 14px như màn mẫu.
- Super Admin role ERP (100002): **giữ vá cục bộ** ở Đề nghị nhập kho, KHÔNG sửa trait `ChecksEmployeePermission`.
- Hoàn thành phiếu nhập hàng → đóng YC nhập nguồn (status 5, is_complete, imported_qty) cho **MỌI loại** như ERP.
- Loại 6 cho thành tiền dòng = 0 (FormRequest `minLotTotal()`), loại khác giữ min:1.
- #11634 B7: **giữ** nút "Tạo phiếu nhập kho" mở màn ERP; lỗi là do server dev thiếu biến `TP_URL` → nhờ người quản
  server khai, không sửa code. Port màn Phiếu nhập kho là task riêng.

## Phiếu nhập hàng `/finance/product-imports` (#11635, #11506 B1)

- [x] #11635 B1 toolbar danh sách: nút cách đều (`mr-2 mb-2`)
- [x] #11635 B2 Tạo mới vào thẳng form, ô "Chọn phiếu nhập kho" nằm trong form (như ERP), bỏ bước "Chọn phiếu nguồn"
- [x] #11635 B3 lập từ PNK loại điều chuyển nội bộ không có nút Lưu nháp/Lưu/Lưu và duyệt
- [x] #11635 B3 có quyền vẫn báo "Không tải được danh mục kho kế toán"
- [x] #11635 B4 tiêu đề khối bỏ icon, chữ thường; dòng người tạo - ngày theo khuôn chung
- [x] #11635 B5 đủ tab/cột như ERP cho loại điều chuyển nội bộ (BE + FE)
- [x] #11635 B6 validate Số lượng: lỗi dưới ô + viền đỏ
- [x] #11635 B7 nút "x" xoá dòng kho kế toán đổi thành icon
- [x] #11506 B1 nút Duyệt ở màn thêm phiếu nhập hàng không hoạt động

## Đề nghị nhập kho `/finance/warehouse-import-requests` (#11634, #11506 B2)

- [x] B1 khối Thông tin chung / File đính kèm / Danh sách hàng hoá theo khuôn chung (mẫu borrow-export-requests/create)
- [x] B2 Tạo mới vào thẳng form (không bật popup chọn phiếu YCNH trước)
- [x] B3 chữ lỗi SL nhập kho to bằng các màn khác
- [x] B4 thêm nút "Lưu và tiếp tục"
- [x] B5/B11 cột Mã YCNH: màu + kiểu link như Mã phiếu
- [x] B6 phân trang mặc định 10
- [x] B8 nút In màu trắng
- [x] B9 bỏ khoảng trắng thừa dưới bảng hàng hoá
- [x] B10 lưu nháp xong sửa tiếp + lưu và gửi duyệt được
- [x] #11506 B2 lập ĐNNK từ YCNH thiếu dữ liệu (so ERP `warehouse_import_requests/create?product_import_request_id=14041`)

## Phiếu yêu cầu nhập hàng `/finance/product-import-requests` (#11631, #11633, #11511, #11506 B3)

- [x] #11631 B1 / #11511 B1 tiêu đề khối bỏ icon, chữ thường
- [x] #11631 B2 / #11633 B2 file đính kèm theo khuôn chung (validate dung lượng, cột dung lượng, đổi file ghi lịch sử)
- [x] #11631 B3 / #11511 B2 ô Nhập thẳng thẳng hàng ô Loại yêu cầu
- [x] #11631 B4 danh sách ô rỗng để trống (không "—")
- [x] #11631 B5 placeholder "Nhập lý do từ chối"
- [x] #11631 B6 / #11506 B3 Từ chối / Duyệt xong về danh sách
- [x] #11633 B1 lỗi validate hiện tại đúng ô (viền đỏ + chữ dưới ô), không chỉ toast chung
- [x] #11633 B3 Số lượng: > 0, không âm, không chữ, không vượt mức cho phép — lỗi dưới ô

### Checkpoint — 12/10/2026 16:50
Vừa hoàn thành: code + nghiệm thu ảnh local cả 3 màn; mở loại 6 (BE ProductImportService + importTypeConfig).
Đang làm dở: #11635 B4 — màn Phiếu nhập hàng vẫn dùng V2BaseFormCard (tiêu đề IN HOA) trong khi 2 màn kia đã chữ thường.
Bước tiếp theo: chờ user quyết V2BaseFormCard + quyền Super Admin dùng chung; deploy dev cần composer dump-autoload + biến TP_URL.
Blocked: các quyết định ở trên.

### Checkpoint — 12/10/2026 17:10
Vừa hoàn thành: 4 quyết định trên đã code + kiểm (tinker rollback, ảnh local).
Bước tiếp theo: user review diff rồi commit; deploy dev nhớ `composer dump-autoload` (hrm-api) + khai `TP_URL` (hrm-client).
Blocked:
