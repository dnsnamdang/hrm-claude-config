# Seed `configs` cho công ty mới + backfill công ty thiếu

## Bối cảnh / sự cố
Màn HRM `finance/regulation-config` tab **Công nợ & tài chính** (`congno`) lưu cho công ty 9
(CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN) → API trả `500 {"message":"configs công ty 9 không tồn tại"}`.

## Root cause
- `congno` là `SCOPE_MIXED`: field `debt_calculation_date` có `store='config'` (ghi bảng `configs`
  theo `company_id`), các field còn lại `store='company'` (ghi bảng `companies`).
- Khi lưu, `RegulationConfigService::applyVersion` nhánh config-store làm:
  `$configId = configs.where(company_id=$scopeId)->value('id'); abort_if(!$configId, 500, 'configs công ty '.$scopeId.' không tồn tại')`.
- Công ty 9 **không có dòng nào trong `configs`** → abort.
- Vì sao thiếu: migration `hrm-api/.../2026_09_24_000001_add_company_id_to_configs_and_clone_per_company`
  clone dòng `configs` (singleton company_id=1) cho mọi công ty **tại thời điểm chạy**. Công ty 9
  được tạo **SAU** migration → bị sót. Luồng tạo công ty (`CompaniesController@store`) trước đây
  KHÔNG tạo dòng `configs` → lỗ hổng hệ thống, mọi công ty tạo mới sẽ lặp lại.

## Hướng xử lý (user chốt "sửa luôn" 2026-10-01)
- **A — Backfill dữ liệu (ĐÃ CHẠY THẬT prod `hrm_erp_gop`):** clone `configs` id=1 → `company_id=9`
  + 1 `contract_rows`. Kết quả: tạo `configs.id=9`, tổng công ty có configs = 9/9.
- **B — Chặn tận gốc:** `CompaniesController@store` sau `$company->save()` gọi
  `seedDefaultConfig($company->id)` — clone template company_id=1 (+ contract_rows), idempotent,
  bọc try/catch report (lỗi seed không làm hỏng tạo công ty).

## Lưu ý
- Clone kéo theo `title`/`logo`/`description` = "Tân Phát" (giống 8 công ty kia khi migration chạy —
  trạng thái đúng thiết kế). Cần riêng thì chỉnh sau ở màn cấu hình.
- KHÔNG sửa `RegulationConfigService` (hàm dùng chung HRM) — giữ nguyên hành vi.
