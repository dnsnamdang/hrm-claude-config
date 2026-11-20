# Port "Phiếu Yêu cầu hỏi giá vận chuyển" ERP → HRM (chỉ phía lập phiếu)

Ngày: 2026-11-20 · @nguyentrancu97 · Nhánh: HRM `develop` (api + client), ERP `develop_02`; gop_db làm sau khi user bảo.

## Mục đích
Đưa việc **lập phiếu** YC hỏi giá vận chuyển (người kinh doanh) về HRM. **Phần sau giữ ở ERP**: Mua hàng (quyền ERP `purchase.mua_hang.manage`) nhận phiếu, nhập chi phí VC từng khách hàng, Duyệt / Không duyệt. Không đổi cách Mua hàng đang làm.

## Hiện trạng ERP (nguồn port)
- `Order\DeliveryCostAskingRequestController`, model `App\Model\Order\DeliveryCostAskingRequest` (+ `…Customer`, `…CustomerProduct`), views `orders/delivery_cost_asking_requests/*`, route `delivery_cost_asking_requests/*` (web.php ~2242).
- Phiếu: 1 hãng SX (`manufacture_id`) + ghi chú; N khách hàng (`customer_id`, `shipping_method` 1 Hàng không / 2 Đường biển / 3 Đường bộ, `cost` do Mua hàng nhập); mỗi KH N hàng (`product_id`, `unit_id`, `qty`≥1). Chọn hàng lọc theo hãng.
- Mã `PYCHGVC-xxxxx`. Trạng thái: 3 Đang tạo, 2 Chờ duyệt, 1 Đã duyệt, 4 Không duyệt. Lưu nháp (3) / Lưu và gửi (2); gửi set `received_time` + notify mọi người có `purchase.mua_hang.manage`.
- Sửa/xoá: chính chủ khi trạng thái 3 hoặc 4. Xem: chính chủ, hoặc Mua hàng khi ≠ 3; trong phạm vi công ty. Lập không cần quyền.
- Trả lời (Mua hàng): nhập `cost` từng KH, status 1/4 (4 bắt buộc `comment`), set `approver_id`/`approved_time`, notify người lập.
- In: `ReportTemplate::YC_HOI_GIA_VC`. Dashboard ERP đếm phiếu status 2 (HomeController ~1375).
- Không phiếu nào khác dùng kết quả phiếu này → luồng kết thúc ở bước duyệt.

## Quyết định đã chốt (user)
1. Chỉ chuyển phía lập phiếu; trả lời/duyệt vẫn ở ERP.
2. **Kết quả xem trên HRM (A):** chi tiết HRM hiện chi phí VC từng KH, người duyệt, ngày duyệt, lý do không duyệt; thông báo kết quả trỏ về trang HRM.
3. Hướng làm: màn HRM mới **ghi thẳng 3 bảng ERP sẵn có** (DB chung), KHÔNG tạo bảng mới, KHÔNG gọi API ERP để tạo phiếu.

## Các cách đã cân nhắc
| Cách | Đánh đổi | Kết luận |
|---|---|---|
| **Màn HRM ghi thẳng bảng ERP** | Không đồng bộ, Mua hàng thấy phiếu ngay | **Chọn** |
| HRM gọi API ERP để tạo | Thêm điểm hỏng, thừa khi đã chung DB | Loại |
| Nhúng/mở màn ERP từ HRM | Không thật sự port | Loại |

## Thiết kế
### HRM (port trung thành ERP)
- Bám cấu trúc màn đã port **YC vận chuyển, bốc xếp** (`/finance/delivery-requests`): trang `pages/finance/delivery-cost-asking-requests/{index,create,_id/index,_id/edit}.vue` + api.js; BE module Finance (entity map `delivery_cost_asking_requests`, `delivery_cost_asking_request_customers`, `delivery_cost_asking_request_customer_products`).
- Danh sách: chỉ phiếu của mình (ERP route trần). Cột: STT, Số yêu cầu, Hãng SX, Người lập, Ngày lập, Ngày nhận, Người duyệt, Ngày duyệt, Trạng thái, Hành động (In / Sửa / Xoá theo canEdit/canDelete). Bộ lọc như ERP `searchByFilter` (mã, trạng thái, hãng, hàng hoá, KH, ngày lập).
- Form lập/sửa: Hãng SX, Ghi chú, bảng KH → hàng (cột như ERP: Tên, Mã, Model, Thương hiệu, ĐVT, Trọng lượng, Kích thước, SL, Phương thức VC). Nút Lưu nháp / Lưu và gửi. Validate y hệt ERP store/update. Sửa: không đổi hãng (ERP update không nhận manufacture_id).
- Chi tiết: thông tin phiếu + bảng KH/hàng + **chi phí VC từng KH** + người duyệt/ngày duyệt/ghi chú duyệt. Không có nút trả lời.
- In: dùng mẫu `YC_HOI_GIA_VC` (bảng `report_templates` chung), cùng bộ biến ERP.
- Gửi (status 2): set `received_time`, sinh notify **trong ERP** cho người có `purchase.mua_hang.manage` (ghi bảng `notifications` ERP, url = route show ERP) — để Mua hàng vẫn nhận như cũ.
- `company_id`/`department_id` lấy từ nhân viên đăng nhập (như ERP boot creating); `created_by` = id user ERP tương ứng (theo mapping id chung).
- Menu: gắn link cho mục có sẵn `'YC hỏi giá vận chuyển'` ở `components/subsystem-menu/sale-hub.js:183` (giữ nhãn — nhãn là menuKey). Không gắn quyền (ERP lập không cần quyền).

### ERP
- Route `create`, `store`, `edit`, `update`, `delete` gắn middleware "đã chuyển sang HRM" (cùng cơ chế `productMovedToHrm` của hàng tạm) → link HRM `/finance/delivery-cost-asking-requests`. Giữ `index`, `searchData`, `show`, `print`, `reply`.
- Nút Sửa/Xoá trong danh sách ERP và nút "Thêm mới" ở index: ẩn hoặc trỏ HRM.
- `reply()`: thông báo kết quả (Đã duyệt / Không duyệt) gửi người lập **trên HRM**, link trang chi tiết HRM — theo tiền lệ `notifyHrmImportResult` (POST HRM BE endpoint notify, HRM tạo thông báo). Lỗi gọi HRM chỉ log, không chặn duyệt.
- Dashboard đếm phiếu chờ duyệt giữ nguyên.

## Không làm
- Không chuyển bước trả lời/duyệt sang HRM; không tạo bảng/cột mới; không sửa phiếu cũ.

## Để builder tự quyết
- Tên file/route chi tiết, cấu trúc component, cách tái dùng popup chọn KH/hàng đã có ở HRM.
- Cách ghi notify ERP từ HRM (model map bảng `notifications` hay service sẵn có) — miễn Mua hàng thấy như ERP cũ.
