# Design (tóm tắt) — Bỏ validate khi hợp đồng "Không thực hiện"

**Người phụ trách:** @khoipv
**Spec chi tiết:** `docs/superpowers/specs/2026-06-10-contract-not-executed-skip-validate-design.md`

## Mục tiêu
Khi tạo/sửa hợp đồng (từ gói thầu/báo giá) và chọn `result = 2` (Không thực hiện) → bỏ TẤT CẢ validate, chỉ bắt buộc `reason` (Lý do).

## Quyết định lớn
- Áp dụng cả **tạo mới + cập nhật**, cả **FE + BE**.
- `result = 1` (Thực hiện) hoặc **để trống** → validate đầy đủ như cũ.
- Lưu hết dữ liệu user nhập (không xóa), vẫn gửi duyệt, vẫn cập nhật downstream như bình thường.
- 3 cột NOT NULL (`type`, `customer_id`, `main_company_id`) auto-fill từ nguồn ⇒ **không cần migration**.

## Điểm chạm
- BE: `Modules/Category/Http/Requests/StoreContractRequest.php` — `rules()` rẽ nhánh theo `result`.
- FE: `pages/contract/contract/add.vue` + `GeneralComponent.vue` — validate trước submit rẽ nhánh theo `formSubmit.result`.
