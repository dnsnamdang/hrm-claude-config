# Chặn tab lệch công ty đang làm — design (tóm tắt)

> 27/10/2026 · @namdangit · hrm-api `bf24b5f5b` + hrm-client `4eb26ea7d` (đã push `gop_db`)
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-27-chan-tab-lech-cong-ty-design.md`

## Mục tiêu

Bịt lỗ hổng: công ty đang làm (`employee_infos.company_role`) dùng chung mọi tab/thiết bị ⇒ đổi công ty ở tab khác thì tab
cũ vẫn hiện công ty cũ nhưng đọc/ghi vào công ty mới. Lộ ra ở Cập nhật giá bán: TPE sửa giá mã TPE bị chặn bởi sàn giá
"của TPE" (BE tưởng là công ty lấy về); giá ≥ sàn thì ghi nhầm sang công ty kia không báo gì.

## Quyết định đã chốt

- 1 tài khoản = 1 công ty tại 1 thời điểm. Tab lệch là lỗ hổng, **không** làm "mỗi tab 1 công ty" (user 27/10).
- Chặn ở BE cho **mọi** request (cả đọc), không riêng màn giá — middleware `EnsureSameCompany` trả 409.
- Request không header (app mobile, client cũ) cho qua để không vỡ client chưa cập nhật.
- Popup không đóng được, chỉ "Tải lại trang"; mất dữ liệu đang gõ dở chấp nhận được (an toàn hơn ghi nhầm công ty).
- Có thêm tín hiệu `storage` giữa các tab để báo sớm — chỉ là lớp trải nghiệm, chốt chặn thật là BE.
- Popup đang hiện ⇒ tắt toast toàn cục (tránh màn tự toast câu 409 đè popup).
- Luật sàn giá giữ chiều cũ: giá công ty lấy về **không được thấp hơn** giá công ty quản lý — không đổi gì ở `OwnerPriceFloor`.

## Phạm vi code

- BE: `app/Http/Middleware/EnsureSameCompany.php` + `app/Http/Kernel.php` (nhóm `api`) + `tests/Feature/EnsureSameCompanyTest.php`
- FE: `plugins/company-guard.js` (mới, khai trong `nuxt.config.js`), `utils/companyGuard.js`,
  `components/modal/CompanyChangedModal.vue`, `components/BasicSubsystem.vue`, `plugins/api-error-guard.js`
- Không migration / seeder / quyền.

## Deploy

2 repo cùng lúc + restart Nuxt (đổi `nuxt.config.js`).

## Còn treo

- `update-company-role` không kiểm chủ hồ sơ / quyền ở công ty chọn (xem plan.md mục Ngoài luồng) — chờ user quyết làm.
