# Design: Cấu hình chặn luồng quá hạn — Tab 2 chặn TP + Lịch sử chỉnh sửa

## Bối cảnh

Hệ thống đã có Tab 1 "Chặn nhân viên" (middleware `CheckDueConfigs`, bảng `due_configs` + `company_due_configs`). Yêu cầu: thêm Tab 2 "Chặn trưởng phòng duyệt" + lịch sử chỉnh sửa. TP bị chặn duyệt nếu BẤT KỲ NV nào trong phòng do TP quản lý có quá hạn (hàng mượn/giữ/NXT).

## Thay đổi

### Phase 1: DB + Seed + UI config

**Migration:**
- `due_configs`: thêm cột `tab tinyint default 1` (1=chặn NV, 2=chặn TP)
- Bảng mới `due_config_histories`: id, content text, updated_by bigint FK employees, created_at

**Seed:** 30 records `due_configs` tab=2 (danh sách phiếu duyệt theo spec)

**View `due_configs/edit.blade.php`:** Tab 2 checkboxes + bảng lịch sử chỉnh sửa (STT, Thời gian, Nội dung, Người cập nhật)

**Controller `update()`:** So sánh before/after → ghi log vào `due_config_histories`

### Phase 2: Logic chặn TP (ERP)

**Service `DueConfigBlockService`:**
- `isManagerBlocked($userId, $actionName)`: query `employee_manage_departments` → lấy NV trong phòng → check 3 loại quá hạn → check `company_due_configs` tab=2
- Reuse logic detection quá hạn từ middleware `CheckDueConfigs` hiện có

**API cho HRM:** `GET /api/v1/due-configs/check-manager-block?user_id=X&action=Y`

### Phase 3: Hook vào routes

**ERP:** Middleware `checkDueConfigsManager` hoặc gọi service trong controller approve
**HRM (hrm-api):** Gọi HTTP sang ERP API trước khi approve (pattern `ErpApiService`)

## Không thay đổi
- Tab 1 logic hiện tại
- Bảng `company_due_configs` dùng chung
- 3 loại quá hạn detection — reuse
