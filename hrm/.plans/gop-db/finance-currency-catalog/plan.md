# Plan — Danh mục tiền tệ (phân hệ Tài chính)

> Phụ trách: @junfoke · Tạo 2026-08-03
> Design: `.plans/gop-db/finance-currency-catalog/design.md`

## Phase 0 — Khảo sát ERP

- [x] Đọc route `admin/accounting/currencies`, `CurrencyController`, model `Currency`,
      `CurrencyStoreRequest` / `CurrencyUpdateRequest`, view `accounting/currencies/index.blade.php`
- [x] Soi bảng `currencies` trên `gop_db`: 11 bản ghi, 8 cột, không có audit/version/history
- [x] Phát hiện cron `currency:update_exchange_rate` chạy 03:00 hằng ngày ghi đè `exchange_rate`
- [x] Phát hiện `delete()` không chặn khi tiền tệ đang được dùng

## Phase 1 — Chốt phạm vi (user chốt 2026-08-03)

- [x] **Bám sát ERP**: danh sách + modal thêm/sửa + xóa + lọc. KHÔNG thêm `created_by`/`updated_by`,
      KHÔNG version/history, KHÔNG Import → không ALTER bảng `currencies`
- [x] **Chặn xóa khi đang dùng** (khác ERP — sửa lỗi)
- [x] **Chuyển luôn cron cập nhật tỷ giá sang HRM** (user bổ sung giữa chừng)

## Phase 2 — BE: Entity + Service + Controller

- [x] `Entities/Currency/Currency.php` — extends `Model` thuần (bảng KHÔNG có `created_by` nên
      `BaseModel` sẽ nổ lỗi cột không tồn tại), `STATUS_ACTIVE=1` / `STATUS_BLOCK=2`,
      hằng `USED_BY` 27 cột / 23 bảng + `usedIn()` (dừng sớm khi đủ 3 nhãn, bảng lớn xếp cuối)
- [x] `Transformers/CurrencyResource/CurrencyResource.php` — **không** trả `is_can_delete` (xem design)
- [x] `Services/CurrencyService.php` — index (keyword/code/name/status + sort), getAll, store,
      update, destroy; `normalizeNumber()` bỏ dấu phẩy ngăn cách nghìn
- [x] `Http/Requests/Currency/CurrencyRequest.php` — `prepareForValidation` chuẩn hóa mã hoa + bỏ
      dấu phẩy tỷ giá; `exchange_rate` required|numeric|gt:0|max:999999.99 (trần cột `double(8,2)`)
- [x] `Http/Controllers/V1/CurrencyController.php` — thêm action `usage()`
- [x] `app/ExcelExport/CurrencyExport.php` + `resources/views/exports/currencies.blade.php`
- [x] 8 route `/v1/finance/currencies` (index, getAll, export, store, update, delete, usage, show)

## Phase 3 — BE: cron cập nhật tỷ giá

- [x] `app/Console/Commands/UpdateExchangeRateCurrencyCommand.php` — `finance:update-exchange-rate`
- [x] Đăng ký `dailyAt('03:00')` + `withoutOverlapping()` trong `app/Console/Kernel.php`
- [x] Sửa 4 lỗi của bản ERP (chi tiết trong design.md)

## Phase 4 — Quyền

- [x] 2 quyền vào seeder: id **1113** `Quản lý danh mục tiền tệ`, **1114** `Xem danh mục tiền tệ`,
      `type = 8`, `group = 'Danh mục tài chính'`. (1111/1112 đã bị Danh mục vụ việc chiếm)
- [x] Insert tay vào DB local + cấp cho cùng bộ vai trò/công ty đang có quyền 1107 (5 dòng mỗi quyền).
      KHÔNG chạy seeder vì `run()` truncate cả bảng

## Phase 5 — FE

- [x] Mục "Danh mục tiền tệ" trong `components/subsystem-menu/finance.js` (bỏ trạng thái xám mờ)
- [x] `pages/finance/currencies/index.vue` — V2Base list, lọc Mã/Tên/Trạng thái, Xuất Excel,
      tỷ giá format `vi-VN` 2 chữ số thập phân
- [x] `components/modal/finance/currency-modal.vue` — thêm/sửa/xem

## Phase 6 — Verify

- [x] Cron chạy thật: cập nhật 8, bỏ qua 2, VNĐ được loại đúng. **Đã khôi phục lại tỷ giá cũ**
      để không để lại thay đổi ngoài ý muốn
- [x] Kiểm chứng lỗi index-0 của ERP: AUD đứng đầu XML, DB đứng yên 16.356,78 từ 2025-03-24
- [x] `usedIn()` trên dữ liệu thật: USD → 3 nơi, KWR → "Chi phí tờ khai hải quan", đều chặn xóa đúng
- [x] Service: lọc keyword/code, sort theo tỷ giá, getAll = 11
- [x] CRUD round-trip: tạo (tỷ giá "12,345.67" → 12345.67), sửa, xóa → DB về đúng 11 bản ghi
- [x] Validate 6 case biên: rỗng / âm / 0 / vượt trần / chữ / hợp lệ + trùng mã USD
- [x] Excel export: 11 dòng, file 80KB
- [x] 8 route đăng ký đúng; gọi không token → 401
- [x] `php -l` 10 file PHP, `vue-template-compiler` 2 file Vue, Nuxt build không lỗi,
      `/finance/currencies` trả 200
- [ ] ⏳ **Chưa verify bằng mắt trên browser** — không đăng nhập được vào phiên Playwright
      (tự sinh JWT bị chặn quyền). Cần user mở `/finance/currencies` xem lại

## Phase 7 — Fix sort (user báo 2026-08-03)

- [x] 🐛 **Sort Tỷ giá không chạy**: `key` cột đặt camelCase `exchangeRate` trong khi
      `CurrencyService::$allowedSortFields` chỉ nhận `exchange_rate`. `V2BaseDataTable` emit thẳng
      `column.key` lên `sort_by` → BE không nhận ra, âm thầm rơi về `orderBy('id')`; mũi tên header
      vẫn đổi chiều nên nhìn như đang sort. Đổi key thành `exchange_rate` + `updated_at`
      (kèm tên slot `#cell-*`)
- [x] Bật `sortable` cho cả `updated_at` và `status` (BE vốn đã hỗ trợ, trước đó bỏ sót)
- [x] Chốt chặn `sort_by` cũ trong localStorage không khớp cột sortable nào → xóa khi mounted
- [x] Rà 2 màn Tài chính đã làm trước: `type-accounts` chỉ sort `code`/`name` (trùng tên BE),
      `accounts` không có cột sortable → **không dính lỗi này**
- [x] Verify: 5 trường sort đều trả đúng thứ tự; gửi `exchangeRate` (tên cũ) đúng là bị bỏ qua

**Bài học chung**: `key` của cột sortable **phải trùng tên trường BE nhận**, vì V2BaseDataTable
emit `column.key` chứ không có lớp map nào ở giữa.

## Phase 8 — Tắt cron bên ERP (user chốt 2026-08-03)

- [x] Comment lịch `currency:update_exchange_rate` trong `TanPhatDev/app/Console/Kernel.php`
      (nhánh **gop_db**) kèm ghi chú lý do + trỏ sang command HRM. **Giữ nguyên class command**
      để còn chạy tay khi cần, chỉ bỏ lịch tự động
- [x] Verify `php artisan schedule:list` bên ERP: không còn dòng nào về tỷ giá (12 lịch còn lại);
      bên HRM vẫn có `finance:update-exchange-rate` — lần chạy kế 2026-08-04 03:00 +07:00
- [x] Cập nhật lại ghi chú trong `hrm-api/app/Console/Kernel.php`: đây là nơi DUY NHẤT còn chạy
- [x] Thêm `->emailOutputTo(env('ADMIN_EMAIL', 'namdangit@gmail.com'))` cho lịch HRM — user chốt
      giữ y như ERP
- [ ] ⚠️ **Cần cấu hình mail HRM trước khi lên thật**: `hrm-api/.env` đang để
      `MAIL_HOST=mailhog`, `MAIL_USERNAME=null`, `MAIL_FROM_ADDRESS=null` và **không có
      `ADMIN_EMAIL`** (đang rơi về mặc định hardcode giống ERP). ERP thì dùng
      `MAIL_HOST=smtp.gmail.com`. Không sửa .env thì mail kết quả không gửi được

## Việc còn lại

- [ ] Chạy seeder quyền trên môi trường thật (local đã insert tay)
- [ ] User verify bằng mắt màn `/finance/currencies`

## Phase — Tai lieu ban giao (2026-08-13)

- [x] `testcase.xlsx` — 117 TC (P0 49%), form 17 cot 2 khoi DNS/TP; generator `gen_testcase.py`
- [x] `HDSD_Danh muc tien te.docx` — 17 trang, 11 Heading 1, 8 bang, 6 anh chup that;
      generator `gen_hdsd.py`, anh nguon `hdsd_shots/` (CHI LOCAL, khong commit)
