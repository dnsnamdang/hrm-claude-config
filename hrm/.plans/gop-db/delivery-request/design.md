# Phiếu yêu cầu vận chuyển, bốc xếp — design (tóm tắt)

> Người phụ trách: @khoipv · Nhánh: `develop` (checkout từ `gop_db`) cả 2 repo · Trạng thái 08/10: code xong, chờ kiểm trên trình duyệt
> Spec chi tiết: [`docs/superpowers/specs/gop-db/2026-10-08-delivery-request-design.md`](../../../docs/superpowers/specs/gop-db/2026-10-08-delivery-request-design.md)

## Mục tiêu

Chuyển màn ERP `delivery_requests` (Khởi tạo → Hàng hóa → Vận chuyển - bốc xếp → "Phiếu yêu cầu vận
chuyển, bốc xếp") sang HRM. Dùng CHUNG bảng ERP `delivery_requests` + `delivery_request_details`
(không đổi schema, không migration).

## Nghiệp vụ (giữ ERP)

- Người lập chọn **Đơn hàng/Hợp đồng** → chọn **phiếu YCXH** → khách hàng, người liên hệ, SĐT, địa
  điểm giao + danh sách hàng (qty > 0) chép từ YCXH. Nhập thêm thời gian vận chuyển, ghi chú, file
  đính kèm, tab Bốc xếp (tổng số kiện, phương thức, địa điểm, thời gian) và **Số kiện** từng dòng.
- Trạng thái: 1 Đang tạo · 2 Chờ duyệt · 3 Đã duyệt · 4 Từ chối. Mã `{mã cty}.YCVC{mmyy}.{5 số}`.
- **Thủ kho** của kho trên phiếu YCXH duyệt / từ chối (bắt buộc lý do). Duyệt → YCXH
  `transition_type = 2`.

## Quyết định đã chốt với user (08/10/2026)

| # | Điểm | Chốt |
|---|---|---|
| 1 | Phạm vi xem | **Có phân quyền theo cấp** — 4 quyền mới (tổng cty / cty / phòng ban / bộ phận), tên giữ nguyên ERP, `type = 23` (Bán hàng). Không quyền: phiếu mình tạo + phiếu mình là thủ kho. Nháp chỉ người tạo thấy |
| 2 | Người duyệt | **Mọi thủ kho** (`warehouse_stockers`) của kho trên YCXH. ERP đọc `warehouses.stocker_id` (rỗng cả 23 kho → ERP không gửi duyệt được, bảng 0 phiếu) |
| 3 | Sửa / Xóa | Người tạo + trạng thái Đang tạo / Từ chối. Xóa hẳn (kèm dòng hàng) |
| 4 | Popup chọn YCXH | **Giữ như ERP chạy thật**: mọi YCXH trạng thái 1/2/3/10/11, không lọc theo HĐ |

## Quyết định HRM tự đặt (theo skill / tiền lệ)

- Nguồn hợp đồng: `hrm_contracts` (status 6 Có hiệu lực, thay `firm_contracts`) + `wr_service_contracts`
  (status 3), lọc công ty người lập HĐ = công ty người đăng nhập — bám nhánh `delivery_request` ERP.
- Lịch sử: bảng chung `catalog_histories` (khoá ảo `details_rows`, `attachment_rows`), đủ 2 nơi.
- File đính kèm: khối `AttachmentSection` dùng chung, cột `attachments` ERP (URL nối `', '`), S3 `delivery_request/`.
- Xuất Excel: popup chọn trường + `exportListFile` (BE `export-rows` + `ExportColumnRegistry`).
- ERP không có In → không làm. Thông báo chuông `[YCVC]` cho thủ kho khi gửi duyệt, cho người tạo khi duyệt/từ chối.
- Menu: `sale-hub.js` mục có sẵn `'YC vận chuyển, bốc xếp'` → đổi thành link (giữ nguyên nhãn).

## Sửa lỗi ERP

1. `canEdit/canDelete` sai thứ tự toán tử (ai cũng sửa/xóa nháp người khác).
2. `reject()` validate lý do nhưng không lưu `approver_comment`.
3. `approve()` lưu trạng thái trước rồi mới kiểm YCXH → phiếu kẹt "Đã duyệt" khi YCXH không hợp lệ. HRM kiểm trong transaction + `lockForUpdate`, 409 khi trạng thái đã đổi.
4. `store/update` catch chung `Exception` nuốt lỗi validate.
