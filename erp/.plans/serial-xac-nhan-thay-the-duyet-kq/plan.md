# Plan — Xác nhận thay thế serial khi Nhập/Duyệt kết quả

Owner: @junfoke — Bắt đầu 2026-09-23
Nhánh: `task_serial_xac_nhan_thay_the` (rẽ từ `master`, repo `hrm-cursor/TanPhatDev`)
Commit: `5a4eb6d0b8` (đợt 1) + `07b89f808b` (bảng Bảo dưỡng) — đã merge `develop_01`

## Phase 1 — BE: cấp dữ liệu serial cho màn duyệt
- [x] Thêm `WrAssignTask::attachCustomerSerials()` — gắn `serials` (serial đang sử dụng) + `product_stock_qty` cho dòng sửa chữa / bảo hành, dùng chung 1 lần `getListProductOfCustomer`
- [x] Gọi ở `getForShowImportResult()` (màn tạo phiếu duyệt KQ) và `WrApproveResultsController@edit` (màn sửa)
- [x] Không cần sửa `checkValidateSerial` / `syncProduct`: FE gắn `serial_id` = serial cần ngừng thì 2 chỗ này đã xử lý đúng sẵn

## Phase 2 — FE màn Duyệt kết quả
- [x] `WrApproveResultProduct.blade.php`: `chooseSerial()` + `used_serial_count` + `findSerialByNumber()`
- [x] `WrApproveResult.blade.php`: `changeSerial()`, `needChangeSerial()`
- [x] `wr_approve_results/form.blade.php`: popup `#chooseSerialChange`

## Phase 3 — FE màn Nhập kết quả
- [x] `WrImportResultProduct.blade.php`: bật lại `chooseSerial()` (bị comment ở `54b14cb8b8`, 23/04/2025), bỏ điều kiện bắt buộc có sẵn `serial_id`
- [x] `WrImportResult.blade.php`: `needChangeSerial()` gắn thẳng cho dòng đang mở popup (dòng bảo hành trước đây không được gắn)

## Phase 4 — Kiểm chứng
- [x] `php -l` sạch 2 file PHP; `node --check` sạch 4 file blade JS
- [x] Giữ CRLF, `git diff --stat` gọn: 7 file, 210+/29-
- [x] Chạy `attachCustomerSerials` trên dữ liệu thật (PNKQ 332 / PGV 368): trả `product_stock_qty=1`, `serials=[16918/65678977897]`, khớp `serial_old`
- [x] Test 7 nhánh logic `chooseSerial()` bằng harness Node: TH1.1 / 1.2 / 2.1 / 2.2 / 3.1 + 2 ca không hỏi đều đúng
- [ ] QA test trên môi trường thật theo 5 TH của file Excel
- [ ] Merge về `master` sau khi QA xác nhận

### Checkpoint — 2026-09-23
Vừa hoàn thành: toàn bộ Phase 1-4 (phần tự kiểm), commit `5a4eb6d0b8` trên nhánh `task_serial_xac_nhan_thay_the`.
Đang làm dở: (không)
Bước tiếp theo: QA test 5 TH trên môi trường thật, rồi merge về `master`.
Blocked: Không vào được màn trên ERP local (DB snapshot 30/01/26 thiếu phân quyền CSKH) → phần UI chưa chụp được ảnh thật, phải nhờ QA.

## Phase 5 — Bảng Bảo dưỡng (QA báo tiếp 23/09/2026)
- [x] Tách hộp thoại xác nhận ra partial dùng chung `partials/classes/base/SerialReplaceConfirm.blade.php`, include ở `layouts/app.blade.php`; 4 lớp dòng thiết bị chỉ còn gọi `confirmReplaceSerialFromContract()`
- [x] `attachCustomerSerials()` phủ thêm `extend_products` + cache danh sách thiết bị của khách theo `customer_id` trong 1 request
- [x] `WrApproveResultsController@create` gắn lại serial cho dòng bảo dưỡng (chúng lấy từ phiếu nhập kết quả, không phải phiếu giao việc)
- [x] `WrApproveResultExtendProduct` / `WrImportResultExtendProduct`: `has_completed_service` + `chooseSerial()`
- [x] Markup 2 màn: ô Serial bảo dưỡng thêm `ng-change`/`ng-blur`, ô tích hoàn thành của gói dịch vụ gọi `product.chooseSerial()`
- [x] Verify: `php -l` + `node --check` sạch; 8 nhánh logic test bằng harness Node; chạy thật trên PNKQ 2 — 4 dòng bảo dưỡng đều có `serials` + `product_stock_qty` và ra tới `toArray()`
- [ ] QA test lại trên dev-erp sau khi deploy `develop_01`

### Checkpoint — 2026-09-23 (lần 2)
Vừa hoàn thành: Phase 5 — bảng Bảo dưỡng + gom logic về 1 partial dùng chung. Commit `07b89f808b`, đã merge vào `develop_01` (chưa push).
Đang làm dở: (không)
Bước tiếp theo: push `develop_01` để dev-erp có bản mới, QA test lại 5 TH ở cả 3 bảng.
Blocked: (không)

## Việc còn lại (đề xuất, chưa làm)
- [ ] `syncProduct()` chỉ ngừng serial cũ khi `!$exist_serial` (serial mới chưa tồn tại "đang sử dụng" ở BẤT KỲ khách nào). Nếu số serial mới trùng một serial đang dùng chỗ khác thì serial cũ KHÔNG bị ngừng dù người duyệt đã đồng ý → thiết bị dư serial. Nên siết phạm vi kiểm tra về cùng khách + cùng hàng hoá — cần chốt nghiệp vụ trước khi sửa.
