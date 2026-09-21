# Hành chính nhân sự: chuyển bước duyệt sang phạm vi phòng ban

**Người phụ trách:** @khoipv · **Ngày:** 18/09/2026
**Spec chi tiết:** `docs/superpowers/specs/2026-09-18-human-duyet-theo-phong-ban-design.md`

## Mục tiêu
Áp dụng cho `Modules/Human` cùng nguyên tắc đã làm ở Chấm công, và rà thêm `Modules/Payroll`.

## Phát hiện then chốt
`Modules/Human` **không có** chỗ nào dùng nhóm nghiệp vụ ở điều kiện duyệt — khác hẳn Chấm công.
Chỉ 1 điểm dùng cơ chế nhóm: thông báo "hồ sơ tự khai cần duyệt".
Các bước duyệt còn lại vốn **không giới hạn phạm vi nhân viên** (chỉ check trạng thái + quyền).

## Scope đã làm
| Luồng | Xử lý |
|---|---|
| Hồ sơ tự khai — thông báo cần duyệt | Đổi từ quản lý **nhóm** → quản lý **phòng ban** |
| Hồ sơ tự khai — `can_approve` / `can_reject` | Thêm ràng buộc phòng ban (trước đây không giới hạn) |
| Dashboard HCNS đếm hồ sơ tự khai chờ duyệt (nằm trong `Modules/Payroll`) | Lọc cùng điều kiện |
| Hợp đồng lao động, Thông báo nội bộ | **Giữ nguyên** — quyền cấp hệ thống, chờ chốt nghiệp vụ |
| Quyền XEM | Giữ nguyên toàn bộ |

## Kết quả rà `Modules/Payroll`
Không có bước duyệt nào theo nhóm nghiệp vụ. Bảng lương / tạm ứng duyệt theo **bảng** (không gắn nhân viên) nên không có phạm vi để lọc. 4 chỗ trong `SalaryService` vốn đã dùng `listManageEmployeeInfoIds()` (đã theo phòng ban) và thuộc quyền xem → giữ nguyên.

## Rủi ro
Giống Chấm công: thiếu dữ liệu `employee_manage_departments` thì người không quản lý phòng ban nào sẽ không duyệt được hồ sơ tự khai (trừ `all_department = 1`).
Staging hiện không còn hồ sơ tự khai nào ở trạng thái chờ duyệt nên không kẹt hồ sơ đang chạy.
