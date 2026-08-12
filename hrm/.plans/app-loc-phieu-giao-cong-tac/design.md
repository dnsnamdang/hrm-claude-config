# Bộ lọc màn Danh sách phiếu giao công tác (app Flutter)

**Repo**: `TPE_APP` (nhánh **`develop`** — nhánh code mới nhất) — KHÔNG phải hrm-api/hrm-client
**Spec chi tiết**: `docs/superpowers/specs/2026-08-06-app-loc-phieu-giao-cong-tac-design.md`

## Mục tiêu

Màn *Danh sách phiếu giao công tác* trên app (`ui/ds_phieu_giao_cong_tac/`) hiện không có bộ lọc nào —
chỉ gửi `company_id` (hard-code công ty user), `page`, `limit`, `type=all`. Bổ sung bộ lọc **14 trường**
đúng như bản web `/assign/assign_business?type=all`.

## Scope

- **Chỉ sửa app** — BE `AssignBusinessService::searchByFilter` đã nhận đủ 14 tham số, không đụng tới.
- `/api/v1/users/auth/user-profile` đã trả sẵn `companies`, `departments`, `parts`, `list_employee_infos`,
  `permissions` → chỉ cần map thêm vào model app.

## 14 trường (thứ tự như web)

Công ty · Phòng ban · Bộ phận · Phiếu công tác (`code`) · Loại công tác (`business_type`) ·
Phiếu đề xuất công tác (`parent_code`) · Phiếu việc cần giao (`wr_assign_task_code`) ·
Phiếu đề xuất công việc (`job_request_code`) · Số hợp đồng (`contract_code`) · Khách hàng (`customer`) ·
Trạng thái (`status`) · Nhân viên (`employee_info_id`) · Từ ngày (`from_time`) · Đến ngày (`to_time`)

## Các quyết định đã chốt

| Vấn đề | Quyết định |
|---|---|
| Kiểu UI | Tái dùng `FilterView` end-drawer có sẵn (`custom_view/filter_view.dart`), giống màn *Danh sách phiếu giao việc*. Không tạo component mới. Dùng luôn `FilterView.activeCount` để hiện "N bộ lọc đang áp dụng". |
| `company_id` đang hard-code | Giữ mặc định = công ty của user, nhưng cho user đổi. "Làm mới" reset về mặc định này, KHÔNG reset rỗng. |
| Ẩn Công ty/Phòng ban/Bộ phận | Ẩn theo quyền giống hệt web, đọc từ mảng `permissions` của user-profile. |
| Cascade | Phòng ban lọc theo Công ty; Bộ phận lọc theo Phòng ban; Nhân viên KHÔNG cascade (web cũng không). |
| Nguồn Bộ phận | `parts` trong user-profile (BE đã trả, `AuthNewController.php:376`) — chỉ thêm field vào model app. |
| Ô ngày | Dùng `DateInput` có sẵn trên `develop` (chọn ngày, có `skipFilterCheck`/`onClear`) → KHÔNG sửa widget dùng chung. |
| Sửa BE | Không. |

## Bẫy đã biết

- Màn *Danh sách phiếu giao việc* nạp option dropdown bằng `if (!env.isThanhAnGroup) return;` → với flavor
  nhóm TPE (gồm `production`, `erp`) dropdown sẽ RỖNG. Màn mới **không** được copy cái gate này.
- `develop` pin Flutter **3.41.7** qua `.fvmrc`, bắt buộc chạy qua `fvm` (README ghi rõ). Flutter global
  3.22.3 trên máy chỉ dùng được cho nhánh `main`.
- freezed 3.x: mọi class `@freezed` phải khai `abstract class`.
- Repo commit sẵn file generated `.g.dart`/`.freezed.dart` → sửa freezed model phải chạy lại `build_runner`
  và diff sẽ gồm cả file generated.
- Chỉ đưa param vào `queryParameters` khi khác `null` — gửi chuỗi rỗng dễ làm BE hiểu nhầm.
