# Danh mục tiền tệ — chuyển từ ERP sang HRM (phân hệ Tài chính)

> Phụ trách: @junfoke · Bắt đầu: 2026-08-03 · Trạng thái: đang brainstorming

## Mục tiêu

Chuyển màn **Danh mục tiền tệ** của ERP (`admin/accounting/currencies`) sang HRM, đặt trong
phân hệ **Tài chính** → menu **Danh mục**, cùng chỗ với Danh mục tài khoản và Danh mục loại tài khoản
(xem [[finance-account-catalog]]).

## Hiện trạng ERP (đã khảo sát 2026-08-03)

| Hạng mục | Chi tiết |
|---|---|
| Route | `admin/accounting/currencies` — `index`, `store`, `update/{id}`, `{id}/delete`, `searchData` |
| Controller | `Accounting\CurrencyController` (108 dòng) |
| Model | `App\Model\Accounting\Currency` — bảng `currencies`, `STATUS_ACTIVE=1`, `STATUS_BLOCK=2` |
| View | 1 file `accounting/currencies/index.blade.php` (319 dòng) — DATATABLE + 2 modal create/edit |
| Bảng | `currencies` — 11 bản ghi, 8 cột: `id, code, name, other_name, status, exchange_rate, created_at, updated_at` |
| Cột DS | STT, Mã, Tên, Tên gọi khác, Tỷ giá, Trạng thái, Hành động |
| Bộ lọc | 2 ô text: Mã (`%kw%`), Tên (`%kw%`) |
| Form | 5 field: `code`(bắt buộc, unique), `name`(bắt buộc), `other_name`, `exchange_rate`(bắt buộc, numeric), `status` |
| Quyền | **Không gate quyền nào** bên ERP |

**KHÔNG có ở ERP** (khác 2 màn trước): không `created_by`/`updated_by`, không version/history,
không Xuất Excel, không Import, không In, không điều kiện chặn xóa.

## Điểm cần lưu ý

1. **Tỷ giá được cron tự cập nhật hằng ngày 03:00** — `currency:update_exchange_rate`
   (`app/Console/Commands/UpdateExchangeRateCurrency.php`) kéo XML tỷ giá bán từ Vietcombank,
   khớp theo `code`, bỏ qua `VNĐ`. Sửa tỷ giá tay ở HRM sẽ bị cron ERP ghi đè vào sáng hôm sau.
2. **Xóa không kiểm tra ràng buộc** — `delete()` gọi thẳng `destroy($id)` trong khi có **20+ model**
   tham chiếu `currency_id` (BillIncome, BillPayment, Invoice2, FirmWarranty, CustomerDept…).
3. `exchange_rate` khai `double(8,2)` → **trần 999.999,99**. Đã có tiền tệ sát trần (CHF 32.827,67 thì
   không sao, nhưng nếu tỷ giá nào vượt 1 triệu sẽ tràn).
4. Bug đã fix ở ERP: sửa tiền tệ báo "Không hợp lệ" do `number_format` trả chuỗi có dấu phẩy —
   xem [[project_datatable_number_format_edit_numeric_fail]]. Sang HRM không dính vì không dùng DATATABLE.

## Quyết định (user chốt 2026-08-03)

| # | Nội dung | Chốt |
|---|---|---|
| 1 | Phạm vi | **Bám sát ERP** — list + modal CRUD + xóa + lọc. Không audit/history/import → không ALTER bảng |
| 2 | Xóa | **Chặn khi đang dùng** (khác ERP, là sửa lỗi) |
| 3 | Cron ghi đè tỷ giá | Ban đầu chốt "không làm gì", sau đó user bổ sung: **chuyển luôn cron sang HRM** |

## Lỗi bản ERP (đã sửa khi port)

1. **Đồng tiền đầu file XML không bao giờ được cập nhật.** `array_search` trả index, phần tử đầu
   trả `0`; bản ERP kiểm tra `if ($searchResultKey)` nên `0` bị coi là "không tìm thấy".
   **Đã kiểm chứng thật**: AUD là dòng đầu của XML Vietcombank, trong DB đứng yên ở 16.356,78 với
   `updated_at = 2025-03-24` (~16 tháng không đổi) trong khi giá bán thực tế là 18.813,43.
   Bản HRM so `!== false`.
2. `$currencies->exchange_rate = ...` gán vào **collection** chứ không phải từng bản ghi — thừa,
   không tác dụng. Đã bỏ.
3. Không xử lý khi curl lỗi / HTTP khác 200 / XML hỏng → chạy tiếp và im lặng. Bản HRM dừng + ghi log.
4. Không chặn giá trị vượt trần cột `double(8,2)`.

## Cách chặn xóa — vì sao không dùng cờ `is_can_delete` như 2 màn trước

Điều kiện phải dò **27 cột trên 23 bảng**; riêng `account_details` ~950k dòng và **không có index**
trên `currency_id` → quét full mất ~0,8s. Tính sẵn cho cả trang danh sách sẽ làm màn chậm hẳn.

→ Tách thành endpoint riêng `GET /currencies/{id}/usage`, FE gọi **đúng lúc bấm nút Xóa**. Nếu đang
dùng thì hiện toast nêu tên tối đa 3 nơi và không mở hộp xác nhận. BE vẫn kiểm tra lại ở `delete()`.

Chỉ tính các cột lưu **ID**. Các cột `currency` kiểu `varchar` lưu **TÊN** tiền tệ (`USD`, `EURO`,
`VNĐ`) — riêng `price_calculates` / `price_calculate_requests` lẫn cả id lẫn mã trong cùng cột — nên
không đưa vào điều kiện chặn.

## Kết quả

BE: `Modules/Finance/{Entities/Currency, Services, Http/Requests/Currency, Http/Controllers/V1,
Transformers/CurrencyResource}` + `app/ExcelExport/CurrencyExport.php` +
`resources/views/exports/currencies.blade.php` + 8 route `/v1/finance/currencies`.

Cron: `app/Console/Commands/UpdateExchangeRateCurrencyCommand.php`, signature
`finance:update-exchange-rate`, lịch `dailyAt('03:00')` trong `app/Console/Kernel.php`.

⚠️ **Cron cùng chức năng bên ERP vẫn đang bật** và ghi cùng bảng `currencies` trên DB gộp. Hai bên
lấy cùng nguồn nên không sai dữ liệu, nhưng thừa — cần chốt tắt một bên khi triển khai thật.

Quyền: id 1113 `Quản lý danh mục tiền tệ`, 1114 `Xem danh mục tiền tệ`, `type = 8`,
`group = 'Danh mục tài chính'`.

FE: `pages/finance/currencies/index.vue`, `components/modal/finance/currency-modal.vue`,
mục menu trong `components/subsystem-menu/finance.js`.
