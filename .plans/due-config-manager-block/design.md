# Design: Cấu hình chặn luồng quá hạn — Tab 2 chặn TP + Lịch sử chỉnh sửa

## Bối cảnh

Tab 2 "Chặn trưởng phòng duyệt" đã triển khai xong (middleware, service, UI config, hook routes). Yêu cầu mới: **sửa cách hiển thị thông báo chặn** từ text/toast → popup (modal) hiển thị danh sách NV quá hạn + xuất Excel.

Spec chi tiết: `docs/superpowers/specs/2026-05-05-due-config-manager-block-popup-design.md`

## Phase đã hoàn thành (trước đó)

- Phase 1: DB + Seed + UI config ✅
- Phase 2: Logic chặn TP (ERP) ✅
- Phase 3: Hook vào routes ✅

## Phase 4: Popup thông báo + Xuất Excel (mới)

**API mới:** `GET /api/v1/due-configs/overdue-employees` — trả danh sách NV quá hạn (JSON) hoặc file Excel (export=1)

**ERP frontend:** Modal Bootstrap hiển thị bảng NV quá hạn khi AJAX approve bị chặn + nút xuất Excel

**HRM frontend:** Sửa axios interceptor nhận diện 403 quá hạn → hiển thị global modal (BootstrapVue) + nút xuất Excel

**HRM API:** Proxy endpoint gọi ERP API

## Không thay đổi
- Logic chặn 3 loại quá hạn, middleware, Tab 1, Tab 2 config UI
