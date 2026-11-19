# Design — Icon Info + diễn giải cho ô "Chính sách kinh doanh" (màn Thêm/Sửa hàng hoá)

## Bối cảnh
Màn chi tiết hàng hoá `master-data/products/{id}`, tab **Quản trị hàng hoá**, ô **Chính sách kinh doanh**.
Yêu cầu: ở màn **Thêm** và **Sửa** hàng hoá, khi mở ô chọn thì **mỗi option kèm icon Info (ⓘ)** chứa
**diễn giải** của chính sách đó. Hình thức UI **làm theo màn meeting** (`assign/meeting/create` — ô "Loại meeting").

## Hiện trạng (code)
- Ô render tại `hrm-client/components/product/form/ProductFormAdmin.vue:26-39` bằng `V2BaseSelect` phẳng
  (`:options="options.business_policies"`), KHÔNG có icon mô tả.
- `ProductFormAdmin.vue` được dùng bởi `components/product/form/ProductForm.vue` → cho cả
  `pages/master-data/products/create.vue` (Thêm) và `pages/master-data/products/_id/edit.vue` (Sửa).
  ⇒ Sửa 1 file này là phủ cả 2 màn.
- Màn **xem chi tiết** dùng `ProductTabAdmin.vue` (ô `V2BaseInput disabled` hiện tên) — NGOÀI phạm vi (chỉ thêm/sửa).

## Pattern chuẩn đã có (SKILL THẮNG SPEC)
- Component ruột: `components/DescriptionInfoSelect.vue` — select có icon ⓘ ở cuối mỗi option + tooltip mô tả,
  tự gắn 🔒 cho option đã khoá (tự khai `templateResult` nên phải tự `LOCKED_OPTION_PREFIX`). Mỗi option cần `{ id, name, description, is_locked }`.
- Tiền lệ wrapper mỏng: `components/MeetingTypeSelect.vue`, `components/ProjectPhaseSelect.vue` — chỉ đặt tên/placeholder/`infoLabel`.
- Nguồn tooltip: `utils/meetingTypeInfoTooltip.js` (icon `ri-information-line` 14px xám `#94a3b8` + popover). Khớp
  quy ước `.claude/skills/info-icon-tooltip` và CLAUDE.md.

## Quyết định đã chốt
1. **Tạo wrapper mỏng `components/BusinessPolicySelect.vue`** bọc `DescriptionInfoSelect` (giống `MeetingTypeSelect`),
   `infoLabel="Mô tả chính sách kinh doanh"`, placeholder "Chọn chính sách kinh doanh". KHÔNG dùng `DescriptionInfoSelect` thẳng (đúng docblock của nó).
2. **Thay `V2BaseSelect` bằng `BusinessPolicySelect`** trong `ProductFormAdmin.vue`, giữ nguyên `:invalid`,
   `keep-locked-options`, `@change` (chảy qua `$attrs`/`$listeners` của wrapper → không đổi hành vi khoá/validate).
3. **BE bổ sung `description` vào option** `business_policies`: `ProductOptionService::options()` đã hỗ trợ
   `extraCols` (echo thẳng vào output) ⇒ chỉ thêm `'description'` vào lời gọi, KHÔNG sửa hàm chung.
   Cột `business_policies.description` (varchar 500, nullable) đã có sẵn trong DB. Sửa 2 call site:
   `formOptions()` (dòng 81) + `optionsForIds()` (dòng 123, dùng cho nhân bản hàng hoá).
4. Option không có diễn giải ⇒ KHÔNG hiện icon (DescriptionInfoSelect bỏ qua mô tả rỗng) — giống meeting.

## Phạm vi file
- MỚI: `hrm-client/components/BusinessPolicySelect.vue`
- SỬA: `hrm-client/components/product/form/ProductFormAdmin.vue`
- SỬA: `hrm-api/Modules/MasterData/Services/Product/ProductOptionService.php` (2 dòng)

## Hiệu năng
Không thêm request: `description` đi kèm trong endpoint `form-options` sẵn có (1 cột text/option, không N+1).
