# Port "Phiếu Yêu cầu đặt hàng" ERP → HRM (chỉ phía KD khởi tạo)

Ngày: 2026-11-20 · @nguyentrancu97 · Nhánh: HRM `develop` (api + client), ERP `develop_02`; gop_db làm sau khi user bảo.
Tiền lệ cùng khuôn (làm cùng ngày, đã push develop): `docs/superpowers/specs/2026-11-20-yc-dat-hang-mua-ngoai-design.md` (YC đặt hàng mua ngoài — api `671fac58e`, client `dd3000b15`, ERP `c97b5a30f7`). Tái dùng: `ProductMovedToHrm` (TARGETS + `buildHrmUrl`), `App\Services\HrmBell` (ERP ghi chuông HRM), khuôn chuông ERP từ HRM của `Modules/Sale/Services/InlandOrderRequest/*`.

## Mục đích
Đưa phần **khởi tạo phiếu của KD** (lập / sửa / lưu nháp / gửi duyệt / xoá nháp) sang HRM. **TP duyệt và toàn bộ phần mua hàng của XNK giữ ở ERP** không đổi: tiếp nhận, tách mã lẻ (recipe), sinh phiếu đặt trong nước / nhập khẩu / nhập tồn đang về, chuyển người nhận, in/xuất. KD theo dõi mọi phiếu của mình trên HRM.

## Hiện trạng ERP (nguồn port)
- Controller `Order\RootOrderRequestController` (1026 dòng), model `App\Model\Order\RootOrderRequest` (+ `RootOrderRequestProduct`, `RootOrderRequestProductDetail`), service `App\Services\RootOrderRequests\RootOrderRequestService`, views `orders/root_order_requests/*` + partial JS `partials/classes/order/RootOrderRequest*.blade.php`. Route prefix `admin/orders/root_order_request` (web.php:2588-2608). Menu "Phiếu Yêu cầu đặt hàng" = `rootOrderRequest.index?_type=all` (topmenubar:322, :1540); "chờ duyệt" = `?_type=for-approved` (:2374).
- Mã `PDH-` + `generateCode(5, id)`; lúc tạo `code = randomString(16)` tạm rồi save lần 2 (Model:562-566, Ctl:241).
- **Trạng thái đầu phiếu:** `1` Đang tạo · `2` Chờ TP duyệt · `3` Chờ tiếp nhận · `4` Đã tiếp nhận · `5` Huỷ (không chỗ nào set).
- Luồng:
  1. KD `store`/`update` với `status` ∈ {1 Lưu, 2 Lưu & gửi}. Gửi ⇒ `department_received_time = now`, mọi detail `status = 1`, `follower_id = approver_id` (luôn null); notify `NotificationHelper::sendNotifyWithPermission('purchase.phieu_yeu_cau_dat_hang_truong_phong.approve', show-url, "Bạn có một yêu cầu đặt hàng cần duyệt từ {tên}", true)` — người có quyền, cùng công ty, quản lý phòng người lập (Ctl:290-295, 391-395).
  2. TP `departmentApprove` 2 → 3 (tiếp) / 2 → 1 (không duyệt, bắt buộc `department_approver_comment`). Notify buyer + người lập.
  3. XNK `approve` 3 → 4 (tiếp nhận: tách dòng, sinh phiếu con theo `type_order_request`) / 3 → 1 (trả lại, bắt buộc `approver_comment`). Notify người lập.
  4. Phiếu về 1 ⇒ người lập sửa và gửi lại.
- **Dữ liệu lập phiếu** (store Ctl:201-300, update Ctl:309-400):
  - Đầu phiếu: `brand_id` bắt buộc (đổi ⇒ xoá hết hàng + hãng), `manufacture_id` bắt buộc (read-only, lấy theo mã đầu tiên thêm vào), `send_company_id` bắt buộc (mặc định công ty người lập), `note` ≤255. Hiển thị Người nhận đơn / Người mua = `getDeputy` của hãng (chỉ hiển thị).
  - Dòng hàng `products[]` ≥1: `product_id`, `unit_id` (exists), `note`, `order_company` (tích "Đặt tồn kho"), `order_company_request_qty`; `details[]`: `customer_id` (exists), `request_qty` 0,01..999.999 (cột double(8,2) — trần 999.999.999 của ERP sẽ tràn cột), `date_needed` (date, **> min_date**), `note`.
  - `min_date` = hôm nay + tổng `since_delivery_time + since_approved_time + since_PO_time + since_PI_time` của `kpi_sales` hãng theo **công ty người đăng nhập** (Ctl:203-209).
  - Nếu `order_company` bật: `order_company_request_qty` bắt buộc ≥1, `details` được rỗng; không bật: `details` ≥1.
  - Gửi (status 2): phải có `AssignHistory` đang hiệu lực (công ty, thương hiệu, hãng) có `buy_employee_id`, không có ⇒ lỗi "Chưa phân công…" (Ctl:251-260).
  - Sau lưu: mọi hàng phải `brand_id` = thương hiệu phiếu (Ctl:276-281).
  - FE: ngày cần > hôm nay; không trùng KH trong 1 mã; không trùng mã; không khác thương hiệu/hãng; chống bấm đúp.
  - `syncProducts` (Model:501-560): xoá hết products + details rồi tạo lại; product `is_root=1`, chụp `product_name`, `code`, `model_id/name`, `manufacture_id/name`, `origin_id/name`, `all_barcodes`, `unit_name`, `price` = giá loại 1 theo ĐVT của công ty phiếu (`Product::getPriceByUnitAndType(p, u, 1, DocumentCompany::ofOrUser)`), `request_qty = root_request_qty = Σ detail.request_qty`, `order_company`, `order_company_request_qty = root_order_company_request_qty`, `order_company_qty`, `qty = adjusted_qty = 0`; detail chụp `customer_name`, `customer_code`, `request_qty = root_request_qty`, `qty = 0`, `parent_id`, `root_order_request_id`.
  - Boot `created`: `company_id`, `department_id`, `part_id` từ người đăng nhập (khi `department_id` trống); BaseModel điền `created_by`/`updated_by`.
- **Lưu không giữ hàng, không ghi lịch sử, không đụng kho.**
- Hỗ trợ form: `stockIncoming` (`ArrivingQtyService::tonFor(company người đăng nhập, product)` — hàng đang về của đơn đặt tồn), `products/{id}/getData` (đơn vị + giá), `warehouseInfo.stockOfProducts` (tồn bán được = `in_stock / hệ số ĐVT`, theo kho/nhóm kho chọn), `manufactures/{id}/getDeputy`.
- Quyền: lập phiếu **không cần quyền**. `canEdit`/`canDelete` = status 1 + chính chủ (Model:614-631). Xoá = xoá cứng phiếu + products + details. `canView` (Model:568-587): buyer được giao, chính chủ, `approver_id`, `department_approver_id`, quản lý phòng có quyền TP, hoặc scope `purchase.phieu_yeu_cau_dat_hang.view`. Danh sách `_type=all` (`searchByFilter` Model:326-471): scope `.view` (Tổng cty = tất cả, Cty = `company_id`, Phòng = phòng quản lý hoặc của mình, không có = buyer/người duyệt/chính chủ); **ẩn status 1 của người khác**. Bộ lọc: mã, luồng (notification), trạng thái, người lập, phòng, công ty, người duyệt, thương hiệu, hàng (tên/mã/model/barcode), KH, công ty nhận đơn, hãng, từ ngày – đến ngày.
- HRM đã ghi vài cột của 2 bảng con từ phía kho (`Modules/Finance/Services/WarehouseImportWriteService.php:1272-1297` — detail `status=8`, product `stock_incoming_warehouse`; `ProductImport.php:888-908` `bumpArrived`). Các cột này chỉ phát sinh sau tiếp nhận.

## Quyết định đã chốt (user, 20/11/2026)
1. **Ranh giới A (như lần trước):** HRM chỉ tạo / sửa / lưu nháp / gửi duyệt / xoá nháp (status 1 → 2). TP duyệt (2 → 3) và mọi bước sau ở ERP.
2. **Cùng khuôn màn YC đặt hàng mua ngoài:** danh sách HRM hiện mọi phiếu KD được xem, đủ mọi status; chi tiết khi status ≠ 1 là chỉ xem + "Mở trên ERP"; ERP chặn tạo/sửa, nút trỏ HRM; chuông 2 chiều.
3. **Port gốc, ghi thẳng bảng ERP sẵn có**, không tạo bảng/cột mới.

## Các cách đã cân nhắc
| Cách | Đánh đổi | Kết luận |
|---|---|---|
| **Port gốc, HRM ghi thẳng bảng ERP** (khuôn màn mua ngoài) | Hai bản logic lập phiếu nhưng ERP bị chặn ghi; tái dùng được middleware/chuông đã có | **Chọn** |
| HRM gọi ERP để lưu | ERP không có API JSON cho màn này, auth session | Loại |
| Nhúng form ERP | Không phải port, vỡ đăng nhập | Loại |
| Ranh giới B (HRM làm cả TP duyệt) | Gọn KD nhưng thêm màn chờ duyệt + quyền + hạn quản lý | User chọn A |

## Thiết kế

### HRM — BE (hrm-api, module Sale, cạnh `InlandOrderRequest`)
- Entity map 3 bảng `root_order_requests`, `root_order_request_products`, `root_order_request_product_details` (đọc thêm tên buyer từ `AssignHistory`, tên TP/người duyệt cho chi tiết).
- Endpoint: danh sách, chi tiết, form-data (thương hiệu, công ty, hãng-deputy), tạo, sửa, xoá, KPI min-date theo hãng, hàng đang về + tồn bán được theo hàng. Không có endpoint duyệt.
- Validate y hệt ERP (mục Hiện trạng), lỗi 422 theo field để FE hiện inline. **Không chép lỗi ERP:** notify chạy sau commit; mismatch thương hiệu kiểm **trước** khi ghi (không ghi rồi rollback dở); hãng không có `kpi_sales` ⇒ min_date = hôm nay (không 500); `request_qty` tổng do BE tính, không tin FE.
- `syncProducts` port 1:1 (cột chụp như Hiện trạng). Giá loại 1 dùng hàm giá-theo-công-ty mà port mua ngoài đã dùng (builder dùng lại).
- Mã `PDH-` + `generateCode(5, id)` như ERP.
- `company_id/department_id/part_id/created_by/updated_by` từ nhân viên đăng nhập (`employees.id` chung HRM↔ERP).
- `canEdit/canDelete/canView` + phạm vi danh sách port y ERP. Thêm `'hrm'` vào `platforms` của `purchase.phieu_yeu_cau_dat_hang.view` trong catalog (giữ `'erp'`); quyền TP giữ chỉ ERP.
- Hàng đang về: HRM chưa có `ArrivingQtyService` ⇒ port riêng phần `tonFor` (chỉ đọc) — bất biến `arriving = max(0, Σprogress − arrived)` (memory erp-arriving-qty-invariant). Tồn bán được: dùng service tồn kho HRM sẵn có nếu ra cùng số; nếu không thì port truy vấn `stockOfProducts`.
- **Chuông khi gửi (1 → 2):** ghi chuông ERP (`notifications`, `notifiable_type = App\Employee`) cho tập người nhận như `sendNotifyWithPermission` (có quyền TP ∩ cùng công ty ∩ quản lý phòng người lập, đang làm), url `/admin/orders/root_order_request/{id}/show`, content y ERP. Lỗi notify chỉ log.

### HRM — FE (hrm-client)
- Trang `pages/sale/order-requests/{index,add,_id/index,_id/edit}.vue`; gắn link cho mục menu sẵn có `'YC đặt hàng'` (`components/subsystem-menu/sale-hub.js:187`, giữ nhãn).
- **Danh sách:** cột theo ERP index, bộ lọc như ERP, hành động Sửa/Xoá khi canEdit/canDelete, "Mở trên ERP" khi status ≠ 1; nút Thêm mới.
- **Form:** đầu phiếu (thương hiệu, hãng read-only, công ty nhận đơn, người nhận đơn/người mua hiển thị, ghi chú); bảng hàng (chọn hàng → ĐVT, giá hiển thị, tồn bán được, hàng đang về, Đặt tồn kho + SL, ghi chú), mỗi hàng N dòng KH / SL / ngày cần / ghi chú; nút "Áp dụng tất cả" KH cho mọi mã; min ngày cần theo KPI hãng. Nút **Lưu** (1) / **Lưu và gửi** (2). Tái dùng picker hàng/KH HRM. Lưu xong về danh sách.
- **Chi tiết:** thông tin phiếu + bảng hàng/KH, ý kiến TP / XNK, người duyệt + thời gian, trạng thái. Status 1 + chính chủ: Sửa/Xoá; còn lại chỉ xem + "Mở trên ERP".

### ERP (TanPhatDev)
- Thêm đích `ProductMovedToHrm::TARGETS`: `root-order-list` → `/sale/order-requests`, `root-order-create` → `/sale/order-requests/add`, `root-order-edit` → `/sale/order-requests/{id}/edit` (fallback danh sách).
- Gắn middleware cho `create`, `store`, `edit`, `update`, `delete`. **Giữ** mọi route khác (index, forApprover, show, departmentApprove, approve, stockIncoming, getListOrderCompany, print, export…).
- Nút "Thêm mới" ở index (và các view danh sách khác nếu có) `create_link` = `buildHrmUrl('root-order-create')`; Sửa/Xoá trong `searchData` trỏ HRM.
- **Chuông về người lập** khi TP duyệt/không duyệt và XNK tiếp nhận/trả lại: thêm `HrmBell::notifyEmployee` (url trang HRM `/sale/order-requests/{id}`), giữ chuông ERP cũ. Lỗi chỉ log, không chặn duyệt.

## Không làm
- Không chuyển TP duyệt, tiếp nhận, tách mã lẻ, phiếu con, chuyển người nhận, in/xuất (phiếu và danh sách) sang HRM — in/xuất vẫn qua ERP.
- Không tạo bảng/cột mới; không đụng các cột kho HRM đang ghi.
- Không đổi quyền TP.

## Để builder tự quyết
- Tên file/route chi tiết, cấu trúc component, tái dùng picker.
- Service tồn bán được HRM tương đương `stockOfProducts`.

## Đã kiểm (builder check 20/11)
- **Phân công khi gửi:** `AssignHistory` where `company_id = send_company_id`, `brand_id`, `manufactures_id`, `employee_date_to IS NULL`, mới nhất theo `created_at`; phải có `buy_employee_id`. Lỗi y câu "Chưa phân công người phụ trách thương hiệu, hãng sản xuất".
- **Công ty lấy giá:** `DocumentCompany::ofOrUser($phiếu)` = `company_id` của phiếu (công ty người lập), fallback công ty người đăng nhập — **không** phải `send_company_id`. `min_date` theo công ty người đăng nhập; thông báo lỗi "Không được nhỏ hơn ngày {hôm nay + tổng + 1, d/m/Y}".
- **Nháp cũ lập trên ERP:** chung bảng ⇒ sửa được trên HRM, không cần bước dữ liệu. ERP `show` vẫn mở được mọi status.
- **Sửa = xoá-tạo-lại dòng con như ERP:** ở status 1 chưa có gì tham chiếu id dòng con (cột kho/phiếu con chỉ sinh sau tiếp nhận) ⇒ an toàn. Xoá nháp = xoá cứng như ERP.
- **Đồng thời:** update/delete/gửi khoá dòng phiếu (`lockForUpdate`) và kiểm lại status 1 + chính chủ **trong transaction**; lệch ⇒ 422 "Phiếu đã được gửi/xử lý, không sửa được".
- **Người nhận chuông TP:** HRM tự viết resolver như port mua ngoài (quyền qua role Spatie + quyền trực tiếp, `guard` đúng, cùng công ty người lập, quản lý phòng người lập qua `employee_manage_departments`, nhân viên đang làm).
- **Quyền `.view` trên HRM:** seed/catalog-sync + kiểm phạm vi (Tổng cty / Cty / Phòng) bằng helper scope HRM như port mua ngoài; thêm bước kiểm trên DB local rằng danh sách không trống với role có quyền (bẫy memory borrow-sell-requests).
- **Tồn bán được:** form có ô chọn kho / nhóm kho như ERP (mặc định nhóm kho mặc định `WarehouseGroup::getGroupDefault`).
- **Chuông ERP → HRM:** thêm chuông HRM, giữ chuông ERP cũ (như port mua ngoài). "Mở trên ERP" trên HRM dùng `erp_url` như màn trước.
- **Ẩn nháp người khác:** port y — ẩn status 1 của người khác ở mọi phạm vi.
- **Nghiệm thu:** feature test API (validate, mã, cột chụp, quyền, phạm vi, chuông) + so cột với phiếu lập trên ERP cùng đầu vào (golden) + e2e Playwright lập → gửi → TP duyệt ERP → chuông HRM.

## Quyết định do Claude đặt (user soát lại)
- Đường dẫn HRM `/sale/order-requests`, gắn menu `'YC đặt hàng'`.
- Đợt này không làm in/xuất Excel trên HRM.
- Thêm `'hrm'` vào `platforms` quyền `.view`; lập phiếu không cần quyền như ERP.
- Sửa 4 lỗi ERP khi port (notify sau commit, kiểm thương hiệu trước khi ghi, null `kpi_sales`, BE tự tính tổng).
