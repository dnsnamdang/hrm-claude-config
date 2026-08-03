# Plan — Sửa chính tả Nhóm giải pháp "Huyndai" → "Hyundai" (NGP.0179)

Người phụ trách: @khoipv

## Bối cảnh / Kết quả điều tra

- Master table: `industries` (Danh mục Nhóm giải pháp, prefix `NGP.`, màn `/assign/solution-groups`).
- Record lỗi: **id=179, code=NGP.0179, name="Huyndai"** — duy nhất 1 dòng bị typo (đã verify DB local).
- **Không có cột snapshot tên** ở bảng con. Tất cả tham chiếu qua FK `industry_id`, resolve tên qua relation `industry->name`:
  - `request_solutions.industry_id` (Yêu cầu làm giải pháp) — 1 bản ghi trỏ 179 (TPE.YCP.TC.26.0016)
  - `solutions.industry_id` (Giải pháp) — 1 bản ghi trỏ 179 (GP27)
  - `prospective_projects.industry_id` (Dự án TKT) — 0
  - `application_industries.industry_id` (Ứng dụng N-N) — 1
- ➡️ Chỉ cần UPDATE 1 dòng master → toàn bộ màn liên đới tự đúng (thỏa AC1–AC4).

## Phương án

Data-fix bằng **migration** (chạy `php artisan migrate` được cả local + product). Dùng query builder (không dùng Eloquent save). Idempotent + guard theo `code` + `name` cũ. Có `down()` rollback.

## Tasks

- [x] Điều tra data model (FK vs snapshot) — xác nhận chỉ đổi master row
- [x] Verify DB: đúng 1 record NGP.0179 = "Huyndai", đếm bản ghi liên đới
- [x] Viết migration data-fix `2026_07_18_000001_fix_industry_name_hyundai_typo`
- [x] Quét toàn DB literal "Huyndai": xác nhận tên chỉ ở `industries.name` (1 dòng); các bảng con lưu `industry_id` không lưu tên → chỉ cần sửa master
- [x] Quyết định user (a): BỎ QUA các chuỗi "Huyndai" text tự do ở bảng khác (chấm công/tăng ca/thanh toán/biên bản...) — ngoài phạm vi
- [x] Chạy migration local + verify AC1–AC4 PASS (2026-07-18): AC1 NGP.0179=Hyundai; AC2 request_solution id=16 industry_name=Hyundai; AC3 solution id=27 industry_name=Hyundai; AC4 search Hyundai=1, Huyndai còn sót=0
- [ ] User chạy trên product: `php artisan migrate --path=Modules/Assign/Database/Migrations/2026_07_18_000001_fix_industry_name_hyundai_typo.php --force`

## Acceptance Criteria

- AC1: Danh mục Nhóm giải pháp tìm NGP.0179 → tên "Hyundai".
- AC2: Chi tiết Yêu cầu làm giải pháp TPE.YCP.TC.26.0016 → Nhóm giải pháp = "Hyundai".
- AC3: Chi tiết Giải pháp GP27 (HN_KD2.UD.0100.2026.DA026_GP27) → Nhóm giải pháp = "Hyundai".
- AC4: Search/lọc theo "Hyundai" → ra các bản ghi cũ của "Huyndai" (vì trỏ cùng industry_id=179).
