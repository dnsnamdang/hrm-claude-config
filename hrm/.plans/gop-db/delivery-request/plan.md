# Phiếu yêu cầu vận chuyển, bốc xếp — plan

Thiết kế: [`./design.md`](./design.md) · Người phụ trách: @khoipv · Nhánh `develop` (từ `gop_db`)

Khuôn bám: BE `BillAdjustDeptRequest*` + `AdditionAccountingRequestWriteService` (lịch sử + đính kèm);
FE `bill-adjust-dept-requests` (form/chi tiết/footer) + `borrow-extend-requests` (danh sách) +
`wr-information-requests` (xuất Excel `exportListFile`).

## Phase 0 — Khảo sát & chốt hướng ✅ (2026-10-08)

- [x] Đọc ERP: controller, model, StoreRequest, 9 blade, 2 class JS, SearchContractService, SearchRequest
- [x] Menu ERP: 1 chỗ duy nhất (Khởi tạo → Hàng hóa → Vận chuyển - bốc xếp), link trần
- [x] Đo dữ liệu `gop_db`: `delivery_requests` 0 phiếu; `warehouses.stocker_id` rỗng 23/23 kho
- [x] Chốt 4 điểm với user (design.md)

## Phase 1 — BE ✅ (2026-10-08)

- [x] Seeder quyền: 4 quyền xem theo cấp id 1695-1698, type 23
- [x] Entity `DeliveryRequest` + `DeliveryRequestDetail` (scope, canView/Edit/Delete/Approve, generateCode)
- [x] `DeliveryRequestService` (đọc: list, show, meta, popup HĐ, popup YCXH, nạp YCXH, KH, export-rows)
- [x] `DeliveryRequestWriteService` (store/update/destroy/approve/reject/deleteFile + lịch sử)
- [x] `DeliveryRequestAttachmentService` + `DeliveryRequestNotifyService`
- [x] FormRequest store/reject, Resource list/detail, Controller, routes
- [x] Đăng ký `catalog_histories` (`CatalogHistoryService::TABLES`) + `ExportColumnRegistry`
- [x] Smoke test API bằng tinker (HTTP kernel, bọc transaction rollback, chặn notify): nháp → gửi duyệt → từ chối (bắt buộc lý do) → gửi lại → duyệt; 409 khi trạng thái đổi; YCXH `transition_type = 2`; người ngoài không thấy; lịch sử ghi đúng dòng hàng sửa
- [x] Sửa lỗi phát hiện khi test: super admin không thấy phiếu (closure `where` rỗng bị Laravel bỏ)

## Phase 2 — FE ✅ (2026-10-08, chưa mở trình duyệt)

- [x] `pages/finance/delivery-requests/index.vue` (danh sách, lọc, cấu hình cột, xuất Excel, lịch sử)
- [x] `components/DeliveryRequestForm.vue` + `RecordPickerModal` (dùng cho cả popup Hợp đồng lẫn YCXH) + `RejectModal`
- [x] `create.vue` · `_id/edit.vue` · `_id/index.vue`
- [x] Menu `sale-hub.js` → link
- [x] Compile kiểm tra (vue-template-compiler + babel)

## Phase 3 — Tự kiểm

- [x] Grep checklist skill `erp-to-hrm-screen`
- [x] Cập nhật spec + STATUS
- [x] Test Playwright (user yêu cầu 08/10, tài khoản DNS Admin — Super admin): danh sách, validate trống, 2 popup chọn (tìm + chọn), điền từ YCXH (18 dòng), ô số chặn chữ, datepicker gõ tay, Lưu nháp, cảnh báo chưa lưu, Gửi duyệt, Từ chối (bắt buộc lý do), sửa lại + gửi lại, Duyệt (xác nhận), tìm nhanh, lọc Trạng thái, Làm mới, Xuất Excel (logo + 8 cột + khối ký), Lịch sử 2 nơi, Lưu và tiếp tục, Xóa — đều đạt. Đã dọn sạch dữ liệu test (phiếu, lịch sử, thông báo, trả YCXH 35667 về transition_type 3)
- [x] Sửa sau test: ô trống ở màn Chi tiết bỏ placeholder; câu lỗi popup từ chối theo khuôn "Tên trường – Nội dung"
- [x] (user yêu cầu 08/10) Ô chọn Đơn hàng/Hợp đồng + Phiếu YCXH theo khuôn ô "Phiếu xác nhận bảo hành" của `addition-accounting-requests`: ô readonly nền trắng, bấm vào ô mở popup, bỏ nút "Chọn"; popup `size="xl"`. Compile OK — chưa xem được trên trình duyệt (watcher Nuxt dev ngừng nạp file, cần khởi động lại `npm run dev`)
- [ ] Chưa test bằng tài khoản THƯỜNG (thủ kho không phải Super admin, người không quyền) trên giao diện — phần này mới kiểm bằng API
- [ ] Chạy `PermissionsTableSeeder` trên môi trường deploy (local `gop_db` chưa có quyền 1695-1698) rồi admin gán quyền

## Fix bug

- [x] (user yêu cầu 12/10) Khoảng cách giữa các dòng thông tin: `mb-3` → `mb-2` ở các ô trong `DeliveryRequestForm.vue` (khối Thông tin vận chuyển + Bốc xếp)
- [x] (user yêu cầu 12/10) Bố cục khối Thông tin vận chuyển: Người liên hệ - SĐT - Địa điểm giao hàng 1 hàng (4/4/4); Thời gian vận chuyển - Ghi chú 1 hàng (4/8); hàng đầu có Mã phiếu (sửa/chi tiết) thì chia 1/4 (`topColClass`) để các hàng dưới không lệch
- [x] (user yêu cầu 12/10) Màn Chi tiết (`readonly`): mọi ô `col-md-4` (cả hàng đầu lẫn khối Bốc xếp — `topColClass`/`carryColClass`), riêng Ghi chú `col-12`; màn Tạo/Sửa giữ bố cục trên → (user yêu cầu tiếp) màn Sửa cũng y màn Chi tiết (điều kiện `isEdit`, bỏ `topColClass`); chỉ màn Tạo giữ Ghi chú `col-md-8` + Bốc xếp `col-md-3`
- [x] (user báo 12/10) ERP `/admin/delivery_requests` không vào được: phiếu HRM lưu `contractable_type = Modules\Assign\Entities\Contract\Contract` → datatable ERP nổ "Class not found" ở `$record->contractable->link`, 1 phiếu làm hỏng cả danh sách. Sửa ở repo ERP (`D:\laragon\www\erp`, user chọn hướng 1): thêm model `App\Model\Assign\HrmContract` (bảng `hrm_contracts`, `customer()`, `link` → `HRM_URL_FE/assign/contracts/{id}`) + `Relation::morphMap` trong `AppServiceProvider::boot()`. Verify: searchData trả 200, phiếu id 9 ra link HĐ-TEST-DNTT-37
- [x] (user yêu cầu 12/10 "sửa giống bên ERP") Popup chọn Đơn hàng/Hợp đồng: ERP ra 12.640 dòng (10 nguồn — nhánh `type=delivery_request` của `SearchContractService` không có `return` riêng, rơi xuống union mặc định), HRM chỉ 1.390 (hrm_contracts + BH-SC). Sửa HRM ra đủ 10 nguồn ERP + giữ hrm_contracts, lọc y ERP (HĐ bán ERP/BH-SC: hiệu lực + cùng công ty; xử lý hàng thiếu status 5; XN BH hãng 3/5/6; còn lại không lọc; 4 loại HĐ mua khớp thêm mã qua account_details TK 99). Đồng bộ whitelist `contractable_type` (FormRequest) + `contractCode()` (WriteService). Verify: so ERP từng mã tìm (trống/HĐ/TEST/2024/MH/PO) → HRM trừ 6 HĐ bán HRM khớp tuyệt đối (12.640/6.222/16/111/64/217); contractCode ra mã đủ 11 loại, loại lạ bị chặn
- [x] (user yêu cầu 14/10) Popup chọn Phiếu YCXH không cho chọn phiếu trạng thái "Đang tạo" (3) — khác ERP (ERP `[1,2,3,10,11]`): bỏ 3 khỏi `DeliveryRequest::EXPORT_REQUEST_STATUSES` → áp cho cả popup, lấy dữ liệu, lưu, duyệt. Verify tinker: popup 141 phiếu, 0 phiếu Đang tạo (DB có 326); `exportRequestData` phiếu Đang tạo bị chặn; 0 phiếu VC chưa duyệt đang gắn YCXH Đang tạo (không vỡ dữ liệu cũ)
- [x] (Redmine #11696, 15/10) Popup chọn Phiếu YCXH: mã phiếu thành link mở tab mới (`/finance/product-export-requests/{id}`), bấm link không chọn dòng
- [x] (Redmine #11696) Danh sách: Số hợp đồng/đơn hàng có link cả loại HĐ mở sang ERP (`href` của `contractLink`) — trước chỉ dựng link HRM (`to`) nên HĐ ERP ra chữ trơn
- [x] (Redmine #11696) Danh sách thêm cột Ngày cập nhật, Người cập nhật (BE resource `updated_at`/`updater_name`, sort `updatedAt`, xuất Excel)
- [x] (Redmine #11696) Popup Từ chối: nút Hủy thêm icon
- [x] (Redmine #11696) Sửa phiếu + bấm Gửi duyệt: trạng thái tách sang mốc "Thay đổi trạng thái" riêng, không nằm trong "Thay đổi thông tin" (khuôn `AdditionAccountingRequestWriteService::update`)
- [x] (Redmine #11696 phản hồi 16/10) Popup "Chọn đơn hàng/hợp đồng": số HĐ thành link mở tab mới (theo `contractLink` — HĐ HRM mở màn HRM, HĐ ERP mở ERP), bấm link không chọn dòng
- [x] (Redmine #11696 phản hồi 16/10) Form chi tiết: ô Đơn hàng/Hợp đồng có link cả HĐ ERP (`href`) — trước chỉ dựng `to` nên HĐ ERP ra chữ trơn
- [x] (Redmine #11696 phản hồi 16/10) "Vẫn đổi trạng thái trong Thay đổi thông tin": ảnh tester là log 13/10 16:18 — ghi TRƯỚC bản sửa 15/10 (`c603ad3e2`), log cũ giữ nguyên; code hiện tại đã tách mốc

- [x] (Redmine #11852, 26/10) Popup "Chọn đơn hàng/hợp đồng" thêm ô lọc **Loại hợp đồng** (`V2BaseSelectInModal`); BE nhận `contractable_type` (chỉ khoá trong `CONTRACT_SOURCES`), trả kèm `sources`. Verify: tất cả 12.646, lọc HĐ mua dịch vụ 72, loại lạ 0
- [x] (Redmine #11852) Bấm mã PYCXH báo "không có quyền": màn chi tiết YCXH lọc theo 4 quyền "Xem yêu cầu xuất hàng theo …" (`ProductExportRequestController::scopedQuery`), popup thì liệt kê mọi phiếu. Thêm `DeliveryRequest::viewableExportRequestIds()` (chép đúng scopedQuery) → mã YCXH chỉ là link khi mở được, còn lại chữ trơn — áp ở popup (`can_view`), danh sách + form chi tiết (`objectable_can_view`). Verify: DNS Admin local chỉ xem được 1/100 phiếu ở trang đầu popup
- [x] (Redmine #11852) ERP 501 phiếu vs HRM 101: do bỏ trạng thái "Đang tạo" (3) hôm 14/10 → user chốt 26/10 trả lại giống ERP, `EXPORT_REQUEST_STATUSES = [1, 2, 3, 10, 11]` (popup, nạp dữ liệu, lưu, duyệt). Verify local: popup 141 → 467; YCXH Đang tạo 33680 nạp được
- [x] (Redmine #11852) Phiếu YCXH chưa gắn khách hàng: chặn NGAY lúc chọn (`exportRequestData` 422) → báo dưới ô Phiếu YCXH + toast, không điền form. Verify: YCXH 410 bị chặn, 35546 vẫn nạp được
- [x] (Redmine #11852) Khối Bốc xếp màn Sửa 4 ô 1 hàng như màn Tạo (`carryColClass` theo `readonly`); màn Chi tiết giữ 1/3
- [x] (Redmine #11852 phản hồi 26/10) Popup chọn phiếu YCXH ẩn luôn phiếu chưa gắn khách hàng (`searchExportRequests` thêm `customer_id > 0`); chặn ở `exportRequestData` giữ làm lưới an toàn. Verify local: 467 → 249 (218 phiếu không KH), YCXH 410 không còn trong popup
- [x] (Redmine #11852 phản hồi 27/10) "Gắn link tất cả các phiếu": user chốt 29/10 link hết + nới quyền xem màn chi tiết YCXH theo ERP `ProductExportRequest::canView()` (Kế toán kho cùng `company_id` / người tạo / quyền TP hoặc BGĐ duyệt vượt hạn mức công nợ), cộng dồn với 4 quyền theo cấp. Áp cho show + in + xuất DS hàng + biên bản bàn giao. FE popup/danh sách/form luôn là link; bỏ `viewableExportRequestIds`/`can_view`/`objectable_can_view`. Helper `ProductExportRequestController::findViewable()` + `ProductExportRequest::canViewLikeErp()` (bỏ nhánh "TP duyệt hàng mượn" — chưa có trong seeder). Verify local (giả lập quyền qua RequestCache): 0 quyền → 404; Kế toán kho cùng cty 200 / khác cty 404; BGĐ vượt HM 200 cả 2; compile FE OK

- [x] (Redmine #11854, 26/10) Tiêu đề màn Chi tiết + Sửa có tag trạng thái (`buildStatusTitle`, khuôn `product-export-requests/_id`); BE `STATUSES` thêm `color` (hex theo `statusBadgeVariant.js`), detail trả `status_color`. Verify: phiếu Chờ duyệt → `#D97706`
- [x] (Redmine #11854) Tên chuẩn "Chi tiết/Sửa phiếu yêu cầu vận chuyển, bốc xếp: {mã}" — top-menu + tab trình duyệt (`plainTitle`, tab không dính HTML badge)
- [x] (Redmine #11854) Câu lỗi validate theo skill form-validate: bỏ tiền tố tên trường, câu nguyên văn `locales/vi.json` (Bắt buộc phải nhập / Vui lòng nhập tối đa N ký tự. / Vui lòng nhập số nguyên. / Không hợp lệ / Định dạng file không hợp lệ / File quá lớn) — FE form + popup Từ chối, BE StoreRequest/RejectRequest/upload/Service/WriteService. Toast lỗi validate đổi thành câu nhắc chung "Vui lòng kiểm tra lại thông tin đã nhập". Verify: Validator payload rỗng ra đúng câu

### Checkpoint — 2026-10-08
Vừa hoàn thành: BE + FE màn Phiếu yêu cầu vận chuyển, bốc xếp (`/finance/delivery-requests`), smoke test API pass, compile FE pass.
Đang làm dở: không.
Bước tiếp theo: test UI bằng tài khoản thủ kho thường ; chạy seeder quyền 1695-1698 ; review code.
Blocked:
