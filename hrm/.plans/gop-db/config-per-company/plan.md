# Plan — Đọc bảng `configs` THEO CÔNG TY (bỏ đọc global)

## Bối cảnh / root cause
DB gộp (`gop_db`) lưu bảng `configs` **1 dòng / 1 công ty** (`configs.company_id`, 9 công ty).
Nhiều hàm port từ ERP (vốn single-tenant) vẫn đọc `configs` **không lọc company_id**
(`->first()` / `->value()` / `->orderBy('id')->value()`) → luôn trả dòng ĐẦU (id nhỏ nhất = công
ty 1). Hệ quả: đổi cấu hình cho công ty khác (vd `debt_calculation_date` của công ty 9 vừa set
2026-10-01) **không có tác dụng** trên các luồng này — khi công ty 9 khai tồn đầu kỳ vẫn chụp ngày
của công ty 1 (2025-08-01).

Phát hiện khi điều tra "công ty 9 khai tồn đầu kỳ áp ngày mới chưa": công ty 9 CHƯA khai dòng nào
(`declare_debt_beginning` / `declare_debt_supplier_beginnings` không có company 9) → chưa hạch toán
sai, nhưng BUG sẽ cắn khi họ bắt đầu khai. Mở rộng: sửa TẤT CẢ chỗ đọc `configs` global.

## Quyết định đã chốt (user 2026-10-06)
- Mặc định: đọc `configs` theo **công ty NGƯỜI ĐĂNG NHẬP** (`auth()->user()->info->company_id`).
- Ngoại lệ **`ContractSupportAccountingService`** (`tndn`): đọc theo **công ty của HỢP ĐỒNG**
  (`$contract->company_id`) — khớp dòng ngay cạnh đã lấy `companies` theo HĐ; kế toán cty A mở HĐ
  cty B mà lấy thuế của A là sai. User đồng ý giữ theo HĐ.
- KHÔNG fallback về dòng đầu khi thiếu công ty (đó chính là bug) → trả `null`/0.
- Đã verify: KHÔNG có cron/console/queue gọi 5 service này → luôn có `auth()` (request HTTP).
- `RegulationConfigService` (MasterData) đã lọc `company_id` sẵn → KHÔNG đụng.
- CRM `MateAuthService::getConfig()` là config tích hợp Mate, KHÔNG phải bảng `configs` → ngoài scope.

## Tasks

### Phase 1 — Helper dùng chung
- [x] 1.1: Tạo `app/Support/CompanyConfig.php`:
      - `currentCompanyId(): ?int` — `auth()->user()->info->company_id`, null-safe (PHP 7.4, không `?->`).
      - `value(string $column, ?int $companyId = null)` — `configs WHERE company_id` (null → công ty
        người đăng nhập; vẫn null → trả `null`).
      - `row(?int $companyId = null)` — đọc cả dòng (null → công ty người đăng nhập; vẫn null → `null`).

### Phase 2 — Áp 7 điểm đọc global
- [x] 2.1: `DeclareDebt/DeclareDebtPostingService:177` `debt_calculation_date` → `CompanyConfig::value(...)` (người đăng nhập).
- [x] 2.2: `BorrowExtendRequestService:301` + `:363` `max_borrow_date` → `CompanyConfig::value(...)` (người đăng nhập).
- [x] 2.3: `PrepickConfigService:30,38` `warning_day` / `max_prepick_date` → `CompanyConfig::value(...)` (người đăng nhập); gỡ import `DB` thừa.
- [x] 2.4: `ProductPrepickRequestService:884` `max_prepick_date(_project_contract)` → `CompanyConfig::row(...)` (người đăng nhập).
- [x] 2.5: `Assign/ContractSupportAccountingService:120` `tndn` → `CompanyConfig::row($contract->company_id)` (công ty HĐ).

### Phase 3 — Kiểm
- [x] 3.1: `php -l` các file sửa — tất cả PASS (6 file: helper + 5 service).
- [x] 3.2: grep lại không còn `table('configs')->first()/->value()` global ngoài RegulationConfig + tests (chỉ còn 5 file test MasterData, out of scope).
- [ ] 3.3: (user) test thực tế: công ty 9 vào khai tồn đầu kỳ → ngày chụp = 2026-10-01.

## Ghi chú
- gop_db: CHƯA commit (chờ yêu cầu). DB trỏ PROD → không ghi DB.
- Liên quan memory: hrm-regconfig-scheduled-not-auto-apply-cron (per-company), gopdb-configs-missing-row-new-company-regconfig-500.
