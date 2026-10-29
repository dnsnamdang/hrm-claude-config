# Regulation-config tab "Tổ chức bán hàng & thị trường" — field "Phân thị trường theo"

> Nhánh: `gop_db` (develop). Phụ trách: @dangquang.tom

## Bối cảnh

Màn `/sale/regulation-config` tab **Tổ chức bán hàng & thị trường** (`id: 'thitruong'`), field
**"Phân thị trường theo"** (`companies.market_division_type`, string, store=company, single select).

Yêu cầu user (nguyên văn, kèm ảnh prnt.sc/ILALjLcoPBVV):
1. **Chọn-1 (không chọn-nhiều)** — user báo "Hiện tại đang cho chọn nhiều >> Sai".
2. **Đổi nhãn** option "Theo quận / huyện" → **"Theo Phường/Xã"**.
3. **Thêm option** "Theo khu vực kinh doanh".

## Hiện trạng đã xác minh (2026-10-16)

- **Yêu cầu #1 — ĐÃ ĐÚNG SẴN trong code develop.** Kiểm live DOM `/sale/regulation-config` tab thị
  trường: `<select>` `multiple=false`, container `select2-selection--single`, đúng 2 option. Registry
  (`input:'select'`), data.js (`csel` = coded SINGLE), Screen.vue (`t==='select'` → V2BaseSelect
  single) đều single. Ảnh user chụp là bản build/prod CŨ. → **KHÔNG sửa gì cho #1.**

- **Yêu cầu #2 — bug nhãn HRM port sai.** ERP (nguồn chân lý) `regulation.blade.php:318-330` nhãn
  value `ward` vốn là **"Phường/Xã"**; HRM port nhầm thành "Theo quận / huyện". Value `ward` ĐÚNG,
  chỉ sai NHÃN → đổi nhãn là khớp. 3 điểm:
  - BE inline options: `RegulationConfigService.php:551`.
  - BE history: dùng `formatOptionValue`→`resolveOptions` (cùng nguồn 551) nên tự đúng; chỉ sửa
    comment `:1896` cho khớp.
  - FE fallback: `data.js:190` (opts fallback lúc loading; options thật do BE trả).

- **Yêu cầu #3 — ERP KHÔNG hỗ trợ "khu vực kinh doanh" ở `market_division_type`.** Agent rà ERP:
  enum khóa cứng `in:province,ward` (CompanyRegulationRequest:65); 2 controller DivisionMarket* chỉ
  phân nhánh `ward→type2 / else→type1`; `FirmSupportAccountingService` khớp HĐ **chỉ theo
  `province_id`**, không đọc `market_division_type`. Khái niệm "khu vực" (bảng `areas`,
  `provinces.area_id`, model `Area`) CÓ nhưng chỉ dùng cho chỉ tiêu KD + lọc báo cáo, KHÔNG gắn
  market_division_type, không có value code `'area'`. Cột `market_division_type` nằm trong DB dùng
  chung (erp_hrm_check) — HRM ghi `'area'` → ERP đọc coi như province (type 1) → **option chết**,
  HĐ không ràng buộc đúng thị trường. → **CHẶN: báo user, không tự thêm option trống** (CLAUDE.md
  "chặn ở BE không chỉ ẩn FE" + "hỏi trước khi làm điều ảnh hưởng nghiệp vụ"). Thêm đúng nghĩa đòi
  sửa cả ERP (enum + 2 controller + FirmSupportAccountingService) = ngoài scope session HRM gop_db.

## Tasks

- [x] **Task 1: Xác minh #1 single** — live DOM confirm single. Không sửa code.

- [x] **Task 2: BE — đổi nhãn `ward` → "Theo Phường/Xã"**
  - `RegulationConfigService.php:551`: `'name' => 'Theo quận / huyện'` → `'Theo Phường/Xã'`. ✔
  - `RegulationConfigService.php:1896`: sửa comment cho khớp ("ward" → "Theo Phường/Xã"). ✔

- [x] **Task 3: FE — đổi nhãn fallback `ward`**
  - `data.js:190`: `['ward', 'Theo quận / huyện']` → `['ward', 'Theo Phường/Xã']`. ✔

- [x] **Task 4: Verify Playwright** — live DOM: option `ward` = "Theo Phường/Xã", `province` =
  "Theo tỉnh / thành phố", `multiple=false`, `select2-selection--single`, rendered "Theo Phường/Xã".
  0 console error. PASS.

- [x] **Task 5 — yêu cầu #3 "Theo khu vực kinh doanh": USER CHỐT DỪNG (2026-10-16).**
  - User chọn Hướng 1: KHÔNG thêm option vì ERP không hỗ trợ value mới ở `market_division_type`
    (enum khóa `in:province,ward`, tầng khớp HĐ chỉ theo province_id → option sẽ chết nghiệp vụ).
    Làm đúng phải mở rộng cả ERP = ngoài scope. → Không sửa code cho #3.

### Checkpoint — 2026-10-16
Vừa hoàn thành: Task 1 (xác minh #1 đã single, không sửa) + Task 2 (BE nhãn ward) + Task 3 (FE nhãn
  ward fallback) + Task 4 (verify Playwright PASS). CHƯA commit (chờ gộp cùng quyết định #3 / chờ
  user yêu cầu commit).
Đang làm dở: (không).
Bước tiếp theo: chờ user yêu cầu commit (#1 không sửa; #2 đã sửa+verify; #3 user chốt dừng).
Blocked: (không).

**File đã sửa (CHƯA commit):**
- hrm-api: `Modules/MasterData/Services/RegulationConfigService.php` (nhãn ward + comment).
- hrm-client: `components/regulation-config/data.js` (nhãn ward fallback).
