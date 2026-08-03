# decision-date-format-variants — Tóm tắt

**Mục tiêu:** Mỗi biến ngày trong mẫu in module Decision cung cấp 2 định dạng cho người soạn mẫu:
- `_CHU` → `Ngày 13 tháng 07 năm 2026` (HOA, zero-pad)
- `_SO` → `13/07/2026`

**Scope:** Toàn bộ mẫu in module Decision (các loại Quyết định + HĐLĐ + Phụ lục HĐLĐ + HĐ đào tạo + Biên bản sự cố). Không migration, không permission, không git.

**Quyết định lớn:**
1. Giữ biến gốc nguyên trạng (mẫu đã lưu không vỡ) + thêm `{{X_CHU}}` / `{{X_SO}}`.
2. Picker chỉ hiện `_CHU` + `_SO`, ẩn biến gốc (biến gốc vẫn chạy ngầm).
3. Định dạng chữ chuẩn: `Ngày 13 tháng 07 năm 2026`.
4. Biến khoảng (câu "Từ ngày… đến ngày…": `THOI_HAN_HOP_DONG`, `THOI_GIAN_KY_LUAT`) giữ cấu trúc câu, chữ "ngày" thường trong câu.

**Kiến trúc 3 tầng:**
- Tầng 1 — Helper (`Modules/Human/Helper/Helper.php`): `formatDateVICapital`, `formatDateVICapitalInline`, `fillDateVariants(&$result, base, date, legacyFormat)`.
- Tầng 2 — Metadata picker (`PrintTemplateVariable.php`): đánh cờ `is_date` + hàm `expandDateVariables` tự sinh 2 dòng, ẩn gốc.
- Tầng 3 — Value-fill (`DecisionService` + 12 controller): thay ~50 dòng gán ngày (gồm khối lặp) bằng `fillDateVariants`; composite xử lý riêng.

**Spec chi tiết:** `docs/superpowers/specs/2026-07-14-decision-date-format-variants-design.md` (inventory đầy đủ file:line + mapping).
