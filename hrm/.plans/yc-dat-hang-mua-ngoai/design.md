# Port "Phiếu Yêu cầu đặt hàng mua ngoài" ERP → HRM (chỉ phía KD khởi tạo)

Ngày: 2026-11-20 · @nguyentrancu97 · Nhánh: HRM `develop` (api + client), ERP `develop_02`; gop_db làm sau khi user bảo.
Tiền lệ cùng khuôn (làm cùng ngày): `docs/superpowers/specs/2026-11-20-yc-hoi-gia-van-chuyen-design.md` (YC hỏi giá vận chuyển — HRM lập, ERP Mua hàng trả lời; api `f0ec354ae`, `fb60ea508`).

## Mục đích
Đưa phần **khởi tạo phiếu của KD** (lập / sửa / lưu nháp / gửi duyệt / xoá nháp) sang HRM. **Phần mua hàng của XNK giữ ở ERP** không đổi: TP duyệt, Kiểm soát duyệt giá NCC + giao buyer, buyer lập HĐ mua ngoài / phụ lục, huỷ, yêu cầu duyệt lại giá, báo cáo duyệt giá. KD theo dõi toàn bộ phiếu của mình trên HRM, không phải nhớ phiếu đang nằm bên nào.

## Hiện trạng ERP (nguồn port)
- Controller `Order\InlandOrderRequestsController` (1381 dòng), model `App\Model\Order\InlandOrderRequest` (+ `InlandOrderRequestProduct`, `InlandOrderRequestProductDetail`, `InlandOrderRequestProductBuyerGroup`, `InlandOrderRequestProductBuyer`), views `orders/inland_order_requests/*`, route `admin/orders/inland_order_requests/*` (web.php ~2452). Menu ERP "Phiếu Yêu cầu đặt hàng mua ngoài" = `inlandOrderRequest.index?type=all` (topmenubar.blade.php:321).
- Mã `PDHTN-xxxxx` (`generateCode`, sau khi save có id; lúc tạo `code = randomString(16)` tạm).
- Trạng thái: `3` Đang tạo · `6` Chờ TP duyệt · `2` Chờ duyệt (Kiểm soát) · `1` Đã duyệt · `4` Đang lập HĐ · `5` Đã lập HĐ · `0` Đã huỷ.
- Luồng:
  1. KD `store`/`update` với `status` ∈ {3 lưu nháp, 6 gửi}. Gửi ⇒ notify người có `purchase.yeu_cau_dat_hang_ngoai.approve` **và** quản lý phòng (`employee_manage_departments.department_id` = phòng người lập) hoặc bộ phận (`employee_manage_parts.part_id`) của người lập; url = ERP `inlandOrderRequest.show`.
  2. TP `departmentApprove` (6 → 2 duyệt / 6 → 3 không duyệt, bắt buộc `department_approver_comment`) — quyền `.approve`. Notify người lập; khi 2 notify người có `.confirm` (url `preApprove`).
  3. Kiểm soát `approve` (2 → 1): nhập `supplier_price`, `supplier_id`, giao `buyers` từng dòng — quyền `.confirm`, cùng công ty người lập. `reject` ⇒ 3 + notify người lập.
  4. Buyer (`forBuyer`) lập HĐ mua ngoài (`inland_buy_contracts`) ⇒ 4/5.
- Dữ liệu lập phiếu (validate store/update giống nhau, trừ `attachments` bắt buộc khi tạo, tuỳ chọn khi sửa):
  - Đầu phiếu: `note` bắt buộc ≤255; `vat_percent`, `cost_after_vat`, `vat_cost`, `total_cost` (FE tính, BE lưu nguyên); `attachments` (file ppt/pptx/doc/docx/pdf/xls/xlsx/pg/jpeg/png/zip ≤15MB, S3 thư mục `inland_order_requests`, cột lưu chuỗi nối `, `; khi sửa thêm file mới **nối** vào chuỗi cũ; xoá từng file qua `deleteFile`).
  - Dòng hàng `products[]`: `product_id`, `unit_id`, `suggest_price` (1..999.999.999.999), `vat_percent`, `note` ≤255; `details[]` ≥1: `customer_id`, `date_needed` (> hôm nay), `qty` (0,01..999.999.999), `note` ≤255.
  - `syncProducts`: xoá hết dòng con (detail, buyer, buyer group, product) rồi tạo lại; mỗi dòng chụp `product_name`, `code`, `model_id/name`, `manufacture_id/name`, `unit_name`, `supplier_price = suggest_price`, `price` = giá loại 1 theo ĐVT của công ty phiếu (`Product::getPriceByUnitAndType(..., 1, DocumentCompany::ofOrUser)`), `qty` = Σ detail.qty; detail chụp `customer_name`, `allocated_qty = 0`.
  - Boot `created`: `company_id`, `department_id`, `part_id` lấy từ người đăng nhập.
  - Hỗ trợ form: `latestApprovedPrices` / `batchLatestApprovedPrices` (giá NCC đã duyệt gần nhất của hàng).
- Quyền (catalog HRM `app/Support/Permissions/Catalog/purchase.php`, hiện `platforms => ['erp']`): `.view` (scope 2 Phòng / 3 Công ty / 4 Tổng công ty), `.approve`, `.confirm`. **Lập phiếu không cần quyền** (ERP `create/store` không gắn checkPermission).
- Xem (`canView`): trong phạm vi công ty theo `.view`; chính chủ; hoặc theo status + quyền duyệt; hoặc buyer được giao; hoặc theo scope `.view`. Danh sách `type=all` (`searchByFilter`): lọc theo scope `.view` (Tổng cty = không lọc, Cty = thành viên cty, Phòng = thành viên phòng, không có = của mình) và **ẩn nháp (3) của người khác**. Bộ lọc: mã, trạng thái, người lập, phòng, công ty, người duyệt, hàng (tên/mã), khách hàng, từ ngày – đến ngày.
- Sửa/xoá: `status == 3 && created_by == mình`. Xoá = xoá cứng phiếu + products + details.
- In: `ReportTemplate::YCDH_TRONG_NUOC` + `print_data` / `product_table` (giá NCC chỉ in khi status ∈ {1,4,5}, ngược lại "Chưa duyệt"; `KS_KY` khi 1, `TBP_KY` khi 1|2). Xuất Excel danh sách: `InlandOrderRequestsExcel`.

## Quyết định đã chốt (user, 20/11/2026)
1. **Ranh giới A:** HRM chỉ làm tạo / sửa / lưu nháp / gửi duyệt / xoá nháp (status 3 → 6). Mọi bước từ TP duyệt trở đi ở ERP.
2. **Theo dõi trên HRM (cách 1):** danh sách HRM hiện mọi phiếu KD được xem, đủ mọi status; chi tiết sau khi gửi là **chỉ xem** (trạng thái, ý kiến TP, người duyệt, buyer, HĐ đã lập) + nút **"Mở trên ERP"** cho các thao tác sau duyệt (Huỷ, YC duyệt lại giá, Tạo phụ lục).
3. **Giá NCC hiện trên HRM** theo đúng quy tắc ERP: status ∈ {1,4,5} hiện giá, còn lại "Chưa duyệt".
4. **Hướng làm:** port gốc — API hrm-api + màn Nuxt, logic bám ERP 1:1, **ghi thẳng các bảng ERP sẵn có** (DB chung), không tạo bảng/cột mới, không gọi API ERP để lưu.

## Các cách đã cân nhắc
| Cách | Đánh đổi | Kết luận |
|---|---|---|
| **Port gốc, HRM ghi thẳng bảng ERP** | Hai bản logic lập phiếu, nhưng ERP bị chặn ghi nên thực tế chỉ còn bản HRM; khớp mọi đợt port trước | **Chọn** |
| HRM làm UI, gọi API ERP để lưu | Ít code; nhưng ERP auth session/SSO chưa có API, lỗi ERP kéo theo HRM, ngược hướng chuyển nghiệp vụ KD sang HRM | Loại |
| Nhúng màn ERP vào HRM (iframe) | Không thật sự port, vỡ đăng nhập | Loại |
| Ranh giới B (HRM làm cả TP duyệt) | Gọn khâu nội bộ KD, nhưng quyền `.approve` thuộc nhóm Mua hàng/ERP | User chọn A |

## Thiết kế

### HRM — BE (hrm-api)
- Entity map các bảng `inland_order_requests`, `inland_order_request_products`, `inland_order_request_product_details` (đọc thêm `…_buyer_groups`, `…_buyers`, `inland_buy_contracts` cho màn chi tiết). Module: Sale (cùng chỗ YCHG) — builder chốt nếu có lý do khác.
- Endpoint: danh sách (+ xuất Excel), chi tiết, tạo, sửa, xoá, xoá file đính kèm, in, giá duyệt gần nhất (đơn + hàng loạt). Không có endpoint duyệt.
- Validate y hệt ERP store/update (mục Hiện trạng), lỗi trả 422 theo field để FE hiện inline. `syncProducts` port 1:1 (chụp tên/mã/model/hãng/ĐVT, `supplier_price = suggest_price`, `price` = giá loại 1 theo ĐVT của công ty phiếu — dùng hàm giá-theo-công-ty HRM đang dùng cho YCHG/hàng hoá).
- Mã `PDHTN-xxxxx` sinh cùng công thức ERP `generateCode(5, id)` để không trùng/lệch dãy với phiếu cũ.
- `company_id` / `department_id` / `part_id` từ nhân viên đăng nhập (như boot ERP); `created_by` = `employees.id` (id chung HRM↔ERP).
- Quyền: `canEdit`/`canDelete` = status 3 + chính chủ; `canView` + phạm vi danh sách port y `canView`/`searchByFilter type=all`. Thêm `'hrm'` vào `platforms` của `purchase.yeu_cau_dat_hang_ngoai.view` trong catalog (giữ `'erp'`); `.approve`/`.confirm` giữ chỉ ERP.
- File đính kèm: S3 cùng thư mục `inland_order_requests`, cùng định dạng cột (chuỗi nối `, `) để ERP đọc được — lưu ý memory "HRM local upload đi S3 thật".
- **Thông báo khi gửi (3 → 6):** ghi chuông **ERP** cho đúng tập người nhận ERP (có `.approve` ∩ quản lý phòng/bộ phận người lập, nhân viên đang làm), url = `/admin/orders/inland_order_requests/{id}/show`, content y câu ERP — theo khuôn `Modules/Finance/Services/DeliveryCostAskingNotifier.php` (bảng `notifications` chung, `notifiable_type = App\Employee`, `data = {url, content, created_by, sender_name, sender_avatar}`). Lỗi notify chỉ log, không chặn gửi.
- In: mẫu `YCDH_TRONG_NUOC` (bảng `report_templates` chung), cùng bộ biến ERP `print_data`/`product_table`.

### HRM — FE (hrm-client)
- Trang `pages/sale/inland-order-requests/{index,add,_id/index,_id/edit}.vue` (đặt tên theo quy ước màn sale hiện có, như `price-asking-requests`). Gắn link cho mục menu có sẵn `'YC đặt hàng mua ngoài'` (`components/subsystem-menu/sale-hub.js:183`, giữ nhãn vì nhãn là menuKey).
- **Danh sách:** cột theo ERP index (STT, Số YC, Người lập, Phòng, Ngày lập, Ngày nhận, Người duyệt TP, Người duyệt, Ngày duyệt, Buyer/HĐ, Trạng thái, Hành động). Bộ lọc như ERP. Hành động: In; Sửa/Xoá khi canEdit/canDelete; "Mở trên ERP" khi status ≠ 3. Nút "Thêm mới" + "Xuất Excel".
- **Form lập/sửa:** đầu phiếu (ghi chú, đính kèm), bảng hàng (chọn hàng → ĐVT, giá đề xuất, %VAT, ghi chú, giá duyệt gần nhất), mỗi hàng N dòng KH / ngày cần / SL / ghi chú; tổng tiền trước/sau VAT tính như ERP formJs. Nút **Lưu nháp** (3) / **Lưu và gửi** (6). Tái dùng picker hàng / KH sẵn có của HRM.
- **Chi tiết:** thông tin phiếu + bảng hàng/KH, ý kiến TP (`department_approver_comment`), người duyệt + thời gian, buyer được giao + HĐ đã lập, giá NCC theo quyết định 3. Status 3 + chính chủ: nút Sửa/Xoá; status ≠ 3: chỉ xem + "Mở trên ERP" (`erp_url` + `/admin/orders/inland_order_requests/{id}/show`).

### ERP (TanPhatDev)
- Thêm đích vào `ProductMovedToHrm::TARGETS`: `inland-order-list` → `/sale/inland-order-requests`, `inland-order-create` → `/sale/inland-order-requests/add`, `inland-order-edit` → `/sale/inland-order-requests/{id}/edit` (fallback danh sách) + câu mô tả trung tính trên trang báo.
- Gắn middleware cho route `create`, `store`, `edit`, `update`, `delete`, `deleteFile`. **Giữ** `index`, `forDepartmentApprover`, `forApprover`, `forBuyer`, `searchData`, `show`, `preApprove`, `approve`, `reject`, `departmentApprove`, `backApprove*`, `cancel`, `print`, `export`, báo cáo, `latestApprovedPrices`.
- Ẩn nút "Thêm mới" ở index và Sửa/Xoá trong `searchData` (hoặc trỏ HRM); nút Sửa trên show nếu có.
- **Thông báo về người lập** (TP duyệt/không duyệt, Kiểm soát không duyệt ⇒ phiếu về 3, và thông báo duyệt xong nếu có): trỏ **trang HRM** `/sale/inland-order-requests/{id}` — theo tiền lệ `notifyHrmImportResult` (ERP gọi HRM tạo thông báo) như YC hỏi giá VC. Lỗi gọi HRM chỉ log, không chặn duyệt. Thông báo gửi người duyệt (url `preApprove`) giữ nguyên ERP.

## Không làm
- Không chuyển TP duyệt / Kiểm soát / buyer / HĐ mua / huỷ / duyệt lại giá / báo cáo sang HRM.
- Không tạo bảng/cột mới, không sửa phiếu cũ (phiếu nháp cũ lập trên ERP vẫn sửa được ở HRM vì chung bảng).
- Không đổi quyền `.approve`/`.confirm`.

## Để builder tự quyết
- Module hrm-api, tên file/route chi tiết, cấu trúc component, tái dùng picker hàng/KH.
- Hàm giá-theo-công-ty HRM tương đương `getPriceByUnitAndType(…,1,…)`.
- Cách ERP báo HRM (endpoint notify sẵn có của tiền lệ hay service tương đương). Lưu ý: `notifyHrmImportResult` dùng `jwt_token` của người duyệt ERP — thiếu token thì thông báo bị bỏ (chỉ log). Nên chọn cách không phụ thuộc token (vd ERP ghi thẳng dòng `notifications` dạng HRM với url HRM).

## Quyết định do Claude đặt (user soát lại)
- Đường dẫn HRM `/sale/inland-order-requests`, gắn mục menu sẵn có `'YC đặt hàng mua ngoài'` (sale-hub).
- Thông báo người duyệt khi gửi = chuông ERP (người duyệt thao tác trên ERP).
- Thông báo về người lập (TP duyệt/không duyệt, Kiểm soát không duyệt, duyệt giá xong 2→1) đổi url sang trang chi tiết HRM.
- Thêm `'hrm'` vào `platforms` của quyền `.view`; lập phiếu không cần quyền như ERP.
- Có Xuất Excel danh sách trên HRM (bám ERP).

## Đã kiểm (builder check 20/11)
- `backApproveSm` chỉ đưa phiếu về 1 hoặc 2, không về 3 ⇒ phiếu đã có buyer/HĐ không bao giờ quay lại sửa được, `syncProducts` không xoá mất buyer/HĐ.
- HRM có `App\Helper\CmcS3Helper` cùng S3 với ERP ⇒ đính kèm cùng định dạng được.
