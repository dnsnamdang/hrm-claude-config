# Design — Xác nhận thay thế serial khi Nhập/Duyệt kết quả giao việc

**Owner:** @junfoke · **Ngày:** 2026-09-23 · **Module:** CustomerCare (ERP)
**Nhánh:** `task_serial_xac_nhan_thay_the` ← `master` · **Commit:** `5a4eb6d0b8` + `07b89f808b` (đã merge `develop_01`)

## Bối cảnh
QA báo (23/09/2026, kèm bảng quy tắc Excel + ảnh phiếu TPE.PNKQ.2026008285): SL thiết bị = 1,
serial trên hợp đồng được chọn từ danh sách serial của thiết bị; tới bước **Duyệt kết quả** người
duyệt nhập serial khác thì **chỉ hiện cảnh báo "số serial đang sử dụng đã đủ…" chứ không có hộp
thoại hỏi** để người dùng xác nhận ngừng serial cũ trên HĐ và thay bằng serial mới (TH 1.1).

## Nguyên nhân
1. Popup xác nhận (`chooseSerial()`) **bị comment toàn bộ** ở `WrImportResultProduct` — commit
   `54b14cb8b8` (23/04/2025, message chỉ ghi "fix"). Bản còn sống là `WrImportResultProductApprove`
   nhưng lớp đó chỉ dùng cho bảng **lắp đặt** ở màn Kết quả giao việc.
2. Màn **Duyệt kết quả chưa bao giờ có** luồng này: `form.blade.php` gọi `p.chooseSerial(p)` và
   `form.changeSerial(p)` nhưng `WrApproveResultProduct` / `WrApproveResult` không định nghĩa, cũng
   không có popup "Chọn serial cần ngưng".
3. Dữ liệu thiếu: `getForShowImportResult()` (nguồn của màn duyệt) không gắn `serials` +
   `product_stock_qty` cho dòng thiết bị, nên kể cả có popup cũng không biết thiết bị còn chỗ hay không.
4. Điều kiện cũ của popup bắt buộc dòng phải có sẵn `serial_id`; dòng không còn `serial_id` (đúng
   phiếu QA chụp) thì không hỏi gì mà bị `checkValidateSerial` chặn thẳng.

## Giải pháp
- **BE** — `WrAssignTask::attachCustomerSerials($wrAssignTask)`: gắn `serials` (serial đang sử dụng
  của khách) + `product_stock_qty` (SL thiết bị) cho `product_repairs` / `product_warrantys`; gọi 1
  lần `Customer::getListProductOfCustomer`, không query theo dòng. Dùng ở `getForShowImportResult()`
  và `WrApproveResultsController@edit`.
- **FE** — `chooseSerial()` trên cả 2 màn, nổ khi dòng đã tích hoàn thành + serial nhập khác
  `serial_old` + `serial_old` nằm trong danh sách serial của thiết bị:
  | Tình huống | Hành vi |
  |---|---|
  | **TH1.1 / 2.1** Đồng ý | `serial_id` = serial từ HĐ → BE ngừng serial cũ, bổ sung serial mới |
  | **TH2.2** Không đồng ý, thiết bị còn chỗ | `serial_id = null` → serial cũ giữ "Đang sử dụng", serial mới được bổ sung |
  | **TH1.2** Không đồng ý, thiết bị đã đủ | mở popup "Chọn serial cần ngưng" để chọn serial khác; không chọn thì `checkValidateSerial` vẫn chặn kèm hướng dẫn vào Danh mục serial |
  | **TH3.1** serial HĐ là serial tạm (không có trong DS serial) | không hỏi, serial mới được bổ sung như thường |
- **Không sửa** `checkValidateSerial` và `syncProduct`: khi FE gắn đúng `serial_id` (serial cần
  ngừng) thì chốt BE tự bỏ qua dòng đó và `syncProduct` đã có sẵn nhánh ngừng serial cũ + thêm mới.

## Quyết định đã chốt
- TH1.2 dùng **popup chọn serial khác để ngừng** (giống khuôn có sẵn ở màn Nhập KQ), không bắt user
  thoát phiếu vào Danh mục serial như chữ trong file Excel của QA — user chốt 23/09/2026.
- Bật lại popup ở **cả màn Nhập kết quả**, không chỉ màn Duyệt — user chốt 23/09/2026.
- Bảng **Bảo dưỡng** (`extend_products`) ban đầu để đợt sau, nhưng QA báo tiếp ngay trong ngày nên đã làm nốt 23/09/2026; nhân đó tách hộp thoại xác nhận ra partial dùng chung `partials/classes/base/SerialReplaceConfirm.blade.php` cho cả 4 lớp dòng thiết bị.

## File thay đổi
| File | Nội dung |
|---|---|
| `app/Model/Customers/WrAssignTask.php` | thêm `attachCustomerSerials()`, gọi trong `getForShowImportResult()` |
| `app/Http/Controllers/Customercare/WrApproveResultsController.php` | gọi `attachCustomerSerials()` ở `edit()` |
| `resources/views/customercare/wr_approve_results/WrApproveResultProduct.blade.php` | `chooseSerial()`, `used_serial_count`, `findSerialByNumber()` |
| `resources/views/customercare/wr_approve_results/WrApproveResult.blade.php` | `changeSerial()`, `needChangeSerial()` |
| `resources/views/customercare/wr_approve_results/form.blade.php` | popup `#chooseSerialChange` |
| `resources/views/customercare/warranty_repair_import_results/WrImportResultProduct.blade.php` | bật lại `chooseSerial()` |
| `resources/views/customercare/warranty_repair_import_results/WrImportResult.blade.php` | `needChangeSerial()` gắn cho cả dòng bảo hành |

## Rủi ro đã biết
`syncProduct()` chỉ ngừng serial cũ khi số serial mới **chưa tồn tại "đang sử dụng" ở bất kỳ khách
nào** (`$exist_serial`). Trùng số serial với khách khác thì serial cũ không bị ngừng dù người duyệt
đã đồng ý → thiết bị dư serial. Chưa sửa vì cần chốt nghiệp vụ (xem mục "Việc còn lại" ở `plan.md`).

Liên quan: `.plans/fix-serial-du-vuot-so-luong-thiet-bi/` (đợt bật lại chốt `checkValidateSerial`).
