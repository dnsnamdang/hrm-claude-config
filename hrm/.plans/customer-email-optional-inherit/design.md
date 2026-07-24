# Email KH: bỏ bắt buộc + kế thừa vào báo giá + cho sửa tay

**Phụ trách:** @manhcuong · **Loại:** Feature nhỏ (2 màn) · 2026-07-06

## Mục tiêu
1. Bỏ bắt buộc trường "Email khách hàng" ở form tạo/sửa **Dự án TKT** và **Báo giá** (cho phép lưu khi để trống).
2. Form **Báo giá**: chọn Dự án TKT → tự điền (kế thừa) email KH của dự án vào trường email; trường này vẫn cho sửa tay (không disable/readonly).

## Quyết định (chốt với user)
- Chỉ trường **Email KH** trên báo giá thành editable; các trường KH khác (tên/MST/địa chỉ/liên hệ) giữ read-only snapshot.
- Bỏ required email luôn ở form **Meeting** (cũng tạo dự án TKT).

## Thay đổi
**BE bỏ required:** `ProspectiveProjectRequest`, `MeetingCreateApiRequest`, `MeetingUpdateApiRequest` (`required|email` → `nullable|email`).

**FE dự án TKT:** `CustomerBlock.vue` — label email bỏ `:required` (bỏ dấu *). Validate FE vốn dựa vào lỗi BE trả về.

**Báo giá kế thừa:** đã có sẵn — `quotations/_id/edit.vue::selectProject` gán `customer_email` từ dự án.

**Báo giá editable + lưu:**
- FE `edit.vue`: ô email đổi text read-only → `V2BaseInput` bound `item.customer_email`, `:disabled="!canEdit"`; gửi `customer_email` trong payload (dùng chung create + update).
- BE `QuotationService::create`: `array_key_exists('customer_email',$data) ? $data[...] : $project->customer_email`.
- BE `QuotationService::update`: thêm `customer_email` vào whitelist `$updatable`.
- BE `QuotationStoreRequest` + `QuotationUpdateRequest`: thêm rule `customer_email` (vì store/update dùng `$request->validated()`).

**Fix kèm (liên quan [[product-project-note-sync]]):** 2 request báo giá thiếu `products.*.note` → `validated()` loại note ở luồng save báo giá thật (khiến ghi chú hàng tạm báo giá không lưu qua form). Đã thêm rule `products.*.note`. BOM save dùng `$request->input()` nên không bị ảnh hưởng.

## Verify
- BE tinker: email rỗng PASS; validated() giữ customer_email + products.*.note.
- Playwright: form dự án TKT không dấu *; form báo giá email input editable, sửa tay + Lưu nháp → DB lưu.
- tinker: note lưu qua `QuotationService::update`.

## Ngoài scope
- Các trường KH khác trên báo giá vẫn read-only snapshot.
