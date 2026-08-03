# setting-master-history — Tóm tắt

## Mục tiêu
Bổ sung "Lịch sử thay đổi" cho màn **Cài đặt** (`/timesheet/setting/setting-master`) — audit ai sửa gì, cũ → mới, lúc nào.

## Bối cảnh kỹ thuật
- `master_settings` là kho cấu hình **key-value toàn hệ thống** (mỗi `category` 1 dòng `content`), KHÔNG có `company_id`, không có id thực thể (singleton).
- Endpoint `POST /v1/master-settings` loop `updateOrCreate` theo TỪNG key → **dùng chung**, nhiều màn khác cũng đọc/ghi. Whitelist history chỉ gồm 8 category của màn này.
- Route `master-settings` **không có** `auth:api` (login/forgot/reset đọc logo/title trước khi đăng nhập) → GIỮ NGUYÊN, không thêm middleware.

## Quyết định (đã chốt với user)
1. Track cả **8 trường**: `title, use_erp, use_decision, use_rice, use_crm, is_sub_month_before_date, update_working_sub_month_before_date, logo`. Logo hiển thị `(ảnh cũ) → (ảnh mới)`.
2. **KHÔNG** permission riêng (ai vào màn thì xem được).
3. Nhãn boolean = **Có / Không**.
4. Biến thể **subset-diff** (BE diff sẵn, chỉ ghi trường thay đổi) — mặc định skill entity-history.

## Thiết kế
- **DB**: bảng `master_setting_history` (không `company_id`, không entity_id): `action, old_value, new_value, changed_by, changed_at, timestamps`.
- **BE**: `MasterSettingService::store()` chụp snapshot 8 category trước, updateOrCreate, diff, ghi 1 dòng nếu đổi. `changed_by = auth('api')->id()` (jwt parse token lazy — POST luôn có token). Thêm `histories()` sort cũ→mới.
- **Route**: `GET /v1/master-settings/histories` group riêng `->middleware('auth:api')`.
- **FE**: nút light `ri-history-line` cạnh nút Lưu + `MasterSettingHistoryModal.vue` (theo mẫu GeneralHistoryModal, cũ ĐỎ → mới XANH, bộ lọc Trường/Người/Từ-Đến ngày).
