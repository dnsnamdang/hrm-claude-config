# Cập nhật địa điểm chấm công/chọn địa điểm theo địa chỉ mới — Goong API v2 (#10981) — @cuong61n

Nguồn: Redmine #10981 — popup chọn địa điểm ở phiếu giao việc / đi công tác / giao công tác (web + app) chưa ra địa chỉ theo ranh giới hành chính mới. Goong báo muốn có địa chỉ mới phải chuyển sang REST API v2.

## Phase 1 — Web (hrm-client, nhánh develop)
- [x] 13/11/2026 · #10981 · Popup chọn địa điểm (`components/modal/GoogleMap.vue`) chuyển Goong v1 → v2: autocomplete `/v2/place/autocomplete`, chi tiết `/v2/place/detail`, geocode `/v2/geocode`. Cấu trúc kết quả v2 giữ nguyên (predictions / result.geometry.location / results[].formatted_address) nên không đổi logic. Trạng thái: sửa xong ở working tree, CHƯA commit, CHƯA test trên màn thật (key trong .env.sample đã bị Goong vô hiệu, cần key thật trong cấu hình hệ thống).

## Phase 2 — App (TPE_APP, nhánh develop)
- [x] 13/11/2026 · #10981 · `user_api_service.dart` (Geocode), `user_api_service_map_ext.dart` (Place/AutoComplete, Place/Detail) đổi path sang `v2/geocode`, `v2/place/autocomplete`, `v2/place/detail`. Sửa trên nhánh `develop` (qua worktree tạm, không đụng `thanhan`), CHƯA commit, CHƯA chạy thử app. Nhánh khách (thanhan, duclocson) chỉ cherry-pick khi user bảo.

## Ghi chú
- BE `LocationService.php` có URL Goong v1 nhưng đoạn gọi đang bị comment, không ảnh hưởng; có hard-code api key trong file (nên gỡ).

## Phase 3 — Merge, đẩy git, build & phát hành (13/11/2026)
- [x] 13/11/2026 · #10981 · Web: commit Goong v2 (`5db43a00d`) trên develop; merge develop → gop_db (4 file xung đột: BasicSubsystem, V2BaseCompanyDepartmentFilter, TaskListTab, TaskForm — giữ cả hai bên, gỡ khối lọc nhanh trùng ở TaskListTab); build production local OK; đẩy gop_db + develop, hai nhánh cùng `8a35d1611`.
- [x] 13/11/2026 · #10981 · Web prod: chạy `~/build_tpe.sh` trên hrm-prod, client lên `8a35d1611`, bản build có URL Goong v2 (không còn v1), PM2 restart, HTTP 200. CHƯA thử popup trên prod với key Goong thật.
- [x] 13/11/2026 · #10981 · App: commit Goong v2 + bump version trên develop, đồng bộ tpe (cùng `fecca6d`), đã đẩy cả hai. HRM TPE (tpeProd) 2.3.9 build 106: iOS upload TestFlight OK (chờ Apple xử lý + gán nhóm external), Android gửi CH Play production 100% (chờ Google duyệt). Tân Phát ERP-HRM (tpeDev) build 163 chỉ build IPA, chưa upload.
- Nhánh thanhan/duclocson: chưa cherry-pick bản sửa Goong (chờ user bảo).
- [x] 13/11/2026 · #10981 · API (hrm-api): chip mã công ty (TPE) ở header không hiện trên prod vì `AuthNewController` nhánh gop_db thiếu `code` trong `company_roles` (develop có). Nguyên nhân gốc: lần trước chỉ merge hrm-client, bỏ sót hrm-api. Đã merge develop ↔ gop_db cho hrm-api (không xung đột, `php -l` 222 file sạch), hai nhánh cùng `41a6f7f00`, deploy prod bằng `~/build_tpe.sh`: 7 migration chạy OK (3 từ develop: km_actual→DECIMAL, draft_roads, 2 index; 4 từ commit gop_db chưa deploy trước đó), route:cache + permission:catalog-sync OK, FE bỏ qua build (không đổi), web HTTP 200, không có lỗi mới trong log. CHƯA mở prod kiểm chip bằng mắt (cần tải lại trang).
