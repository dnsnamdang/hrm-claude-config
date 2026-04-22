# Kế toán Module — Scaffold codebase

## Mục tiêu
Tạo khung module `Accounting` (phân hệ Kế toán) ở BE + FE, nhất quán với module hiện có. Không có entity/CRUD nghiệp vụ trong lần scaffold này.

## Quyết định chính
- **BE namespace:** `Modules\Accounting` (copy structure từ `Modules/Decision`).
- **FE route prefix:** `/accounting` (tile trong grid + sidebar menu file + dashboard + index page).
- **DB connection:** default `mysql`, không migration nghiệp vụ.
- **Flag bật/tắt:** Vuex `is_use_accounting` (mirror pattern `is_use_decision`, đọc từ master-setting `use_accounting`).
- **Icon:** copy `icon_quyet_dinh.svg` → `icon_ke_toan.svg` làm placeholder.
- **Sample endpoint:** `GET /api/v1/accounting/dashboard` trả `{ module: 'accounting' }` để verify.

## Không làm (YAGNI)
- Không tạo Entity / migration / seeder nghiệp vụ.
- Không permission seed.
- Không Resource/Transformer/Request mẫu.
- Không Job/Mail/Export.
- Không menu sidebar thật (file rỗng/placeholder).

## Link
Spec chi tiết: [`docs/superpowers/specs/2026-04-21-ke-toan-module-scaffold-design.md`](../../docs/superpowers/specs/2026-04-21-ke-toan-module-scaffold-design.md)
