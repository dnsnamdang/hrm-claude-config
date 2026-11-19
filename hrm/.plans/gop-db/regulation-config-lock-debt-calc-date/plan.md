# Regulation-config — Chặn sửa "Ngày khai báo đầu kỳ" khi đã phát sinh khai đầu kỳ

> Nhánh: `gop_db` (develop). Phụ trách: @dangquang.tom

## Bối cảnh

Màn `/finance/regulation-config` (component dùng chung `RegulationConfigScreen.vue`) tab
**Công nợ & tài chính** (`id: 'congno'`), trường ngày đầu tiên.

Yêu cầu user (nguyên văn):
1. **Sửa text**: "Ngày khai báo công nợ đầu kỳ" → **"Ngày khai báo đầu kỳ"**.
2. **Chặn sửa** giá trị ngày này nếu công ty đã **phát sinh 1 trong các giá trị khai đầu kỳ**:
   công nợ KH, công nợ NCC, tồn hàng, tồn kho.

ERP **không có** ràng buộc này (ConfigsController chỉ `required|date`) → đây là **nghiệp vụ mới** của HRM.

## Mapping 4 nguồn "phát sinh khai đầu kỳ" → bảng (đã xác minh cột trong `erp_hrm_check`)

| Nguồn | Bảng | Scope công ty |
|---|---|---|
| Công nợ KH đầu kỳ | `declare_debt_beginning` (singular) | `company_id` |
| Công nợ NCC đầu kỳ | `declare_debt_supplier_beginnings` | `company_id` |
| Tồn hàng đầu kỳ | `beginning_stocks` | `company_id` |
| Tồn kho (kế toán) đầu kỳ | `beginning_accounting_stocks` | **KHÔNG** có company_id → join `accounting_warehouse_id` → `accounting_warehouses.company_id` |

Company 1 (công ty đang cấu hình trong ảnh user gửi) có data cả 4 nguồn → field bị khóa.

> ⚠️ Mapping là diễn giải của assistant, well-grounded theo các bảng "đầu kỳ/beginning" chuẩn ERP.
> Ghi rõ ở đây để user chỉnh nếu lệch nghiệp vụ.

## Cơ chế chặn

- Field `debt_calculation_date` store=config (bảng `configs`), tab `congno` SCOPE_MIXED, per-company.
- **BE chốt chặn thật** (CLAUDE.md "chặn ở BE không chỉ ẩn FE"):
  - `getTabConfig`: nếu company đã phát sinh đầu kỳ → trả field kèm `locked=true` + `lock_reason`.
  - `saveTabVersions` (điểm vào DUY NHẤT nút "Lưu cấu hình"): nếu `debt_calculation_date` **đổi so với
    giá trị hiện hành** VÀ company đã phát sinh đầu kỳ → `abort(423)` message tiếng Việt. Chỉ chặn khi
    giá trị THỰC SỰ đổi (field khác trong tab vẫn lưu bình thường).
- **FE**: disabled ô ngày khi `f.locked` (giữ hiển thị giá trị, KHÔNG ẩn — field khóa dùng disabled),
  kèm icon Info (ri-information-line + b-popover custom-class="info-popover") giải thích lý do.

## Tasks

- [x] **Task 1: BE — đổi label field + thêm helper `hasOpeningBalances`**
  - `RegulationTabRegistry.php` dòng 47: label 'Ngày khai báo công nợ đầu kỳ' → 'Ngày khai báo đầu kỳ'.
  - `RegulationConfigService.php`: thêm private `hasOpeningBalances(int $companyId): bool` kiểm 4 bảng
    (3 bảng theo company_id + beginning_accounting_stocks join accounting_warehouses.company_id),
    dùng `->exists()`, short-circuit.

- [x] **Task 2: BE — getTabConfig trả `locked`/`lock_reason` cho field debt_calculation_date**
  - Trong vòng dựng `$fields`: nếu `$key==='debt_calculation_date'` và `hasOpeningBalances($companyId)`
    → `$field['locked']=true; $field['lock_reason']='<lý do VN>'`.

- [x] **Task 3: BE — guard saveTabVersions chặn đổi ngày khi đã phát sinh đầu kỳ**
  - Đầu `saveTabVersions`: nếu `$tabKey==='congno'` và `array_key_exists('debt_calculation_date',$values)`
    → cast cả 2 bằng castValue('date'), nếu khác nhau VÀ hasOpeningBalances → abort(423, message VN).

- [x] **Task 4: FE — đồng bộ label + nhận cờ locked + disable + info icon**
  - Dùng lại component chung `components/report/ReportInfoTip.vue` (đúng chuẩn skill info-icon-tooltip)
    cho icon Info — KHÔNG tự dựng b-popover mới.
  - `data.js` dòng 40: dateField helper thêm `locked: false, lockReason: ''` (Vue2 predefine reactive).
  - `data.js` dòng 227: label 'Ngày khai báo công nợ đầu kỳ' → 'Ngày khai báo đầu kỳ' (join theo label!).
  - `RegulationConfigScreen.vue` apiFieldKeys map (dòng ~2219): thêm `locked: f.locked, lockReason: f.lock_reason`.
  - `applyTabToModel` (dòng ~2341): `$set(f,'locked',!!meta.locked)` + `$set(f,'lockReason',meta.lockReason||'')`.
  - Template dòng 282: `:disabled="!!f.fixed || !!f.locked"` + icon Info cạnh label khi `f.locked`
    hiện `f.lockReason` (ri-information-line + b-popover info-popover) — rà pattern có sẵn trước.

- [x] **Task 5: Verify** —
  - BE tinker (DB erp_hrm_check): `getTabConfig(1,'congno')` → label "Ngày khai báo đầu kỳ",
    value '2025-08-01', `locked=true`, `lock_reason` đúng. `saveTabVersions` đổi ngày (2030-12-31)
    → **abort 423** đúng message. Ngày KHÔNG đổi (bọc transaction rollback) → cho qua (lưu field khác OK).
    Cty 1,2,3,4 (có data đầu kỳ) `locked=true`; cty 5,6,7,8 (chưa có) `locked=false`.
  - FE Playwright `/finance/regulation-config` tab Công nợ & tài chính (cty 1): nhãn "Ngày khai báo
    đầu kỳ", ô ngày **disabled** (vẫn hiện 01/08/2025), icon Info hover ra popover `.info-popover` =
    đúng câu lý do. 0 console error.

### Checkpoint — 2026-10-16 (ĐÃ COMMIT + PUSH)
Vừa hoàn thành: Task 1-5 (BE label + hasOpeningBalances + getTabConfig lock + guard 423; FE label +
  cờ locked + disable + ReportInfoTip). Verify BE tinker + FE Playwright PASS.
  **Đã commit + push origin/develop cả 2 repo** (commit riêng YC8, tách hunk khỏi YC7 cùng file):
  - hrm-api: `89e15c0ec` feat(regulation-config): chặn sửa "Ngày khai báo đầu kỳ"...
  - hrm-client: `6ac8a8a8a` feat(regulation-config): khoá ô "Ngày khai báo đầu kỳ"...
Đang làm dở: (không) — feature hoàn tất.
Bước tiếp theo: (không).
Blocked: (không)

**File đã sửa (ĐÃ commit+push):**
- hrm-api: `Modules/MasterData/Support/RegulationTabRegistry.php` (label),
  `Modules/MasterData/Services/RegulationConfigService.php` (hasOpeningBalances + getTabConfig lock + guard).
- hrm-client: `components/regulation-config/data.js` (dateField locked + label),
  `components/regulation-config/RegulationConfigScreen.vue` (import ReportInfoTip, apiFieldKeys map,
  applyTabToModel $set, template disabled + icon).

**Lưu ý nghiệp vụ gửi user xác nhận:** mapping 4 nguồn → bảng (`declare_debt_beginning`,
`declare_debt_supplier_beginnings`, `beginning_stocks`, `beginning_accounting_stocks` join
`accounting_warehouses`) là diễn giải assistant — nếu "tồn kho đầu kỳ" ý user là bảng khác thì báo để chỉnh.
