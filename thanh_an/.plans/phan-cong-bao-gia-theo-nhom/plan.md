# Phân công báo giá: giới hạn theo nhóm nghiệp vụ mình quản lý

**Người phụ trách:** @khoipv
**Ngày tạo:** 18/09/2026

## Yêu cầu
Người có quyền `Phân công báo giá` chỉ được phân công những **dự toán do nhân viên trong nhóm nghiệp vụ mình quản lý tạo ra**.
Nếu không quản lý nhóm nào → chỉ phân công được **dự toán do chính mình tạo**.

## Hiện trạng
- `Project::canAssign()` (`Modules/Category/Entities/Project/Project.php:146`) — logic đúng **đã có sẵn nhưng bị comment** (dòng 148), đang chạy dòng 149: ai có quyền là phân công được mọi dự toán.
- `ProjectController::assignEmployee()` (`:78`) — **không check quyền gì cả**, gọi thẳng API là phân công được.
- `ProjectService::store/update` (`:219`, `:267`) — thông báo "cần phân công" gửi cho **tất cả** ai có quyền (dòng theo nhóm cũng đang bị comment ở `:218`, `:266`).
- `CategoryDashboardService` (`:130`, `:355`, `:1515`) — đếm "dự toán cần phân bổ" theo phạm vi XEM, không theo phạm vi phân công.
- `app/Console/Commands/NotifyProjectAssignmentDue.php:40` — nhắc quá hạn gửi cho tất cả ai có quyền.

## Quy tắc áp dụng
`created_by ∈ listManageEmployeeIdsByGroup()` **HOẶC** `created_by == auth()->user()->id`
(không quản lý ai → mảng rỗng → chỉ còn dự toán của chính mình)

## Task
- [x] `Project::canAssign()` — bật lại ràng buộc nhóm nghiệp vụ
- [x] `Project::canRejectAssignment()` — áp cùng phạm vi (từ chối phân công là hành động của chính người phân công)
- [x] `ProjectController::assignEmployee()` — chặn server-side bằng `canAssign()`
- [x] `ProjectService::store()` / `update()` — thông báo gửi cho quản lý nhóm của người tạo; không có quản lý → gửi chính người tạo nếu họ có quyền
- [x] `CategoryDashboardService` 3 chỗ đếm "dự toán cần phân bổ" — lọc cùng điều kiện
- [x] `NotifyProjectAssignmentDue` — gửi theo từng dự toán cho quản lý nhóm của người tạo
- [x] `php -l` + đối chiếu bằng tinker

## Không đụng
- Quyền XEM danh sách dự toán / báo giá (`Xem danh sách dự toán theo tổng công ty / công ty / nhóm nghiệp vụ`)
- Các luồng duyệt khác của báo giá (TP duyệt, BGĐ duyệt, Duyệt bàn giao báo giá)

## Checkpoint — 18/09/2026
Vừa hoàn thành: toàn bộ task, `php -l` sạch 5 file.

**File đã sửa**
1. `Modules/Category/Entities/Project/Project.php:146` — `canAssign()` + `canRejectAssignment()` viết inline `(in_array($this->created_by, listManageEmployeeIdsByGroup()) || $this->created_by == auth()->user()->id)`, đúng style sẵn có của `Quotation::canApprove()` (đã bỏ helper + cache tách riêng theo góp ý của @khoipv)
2. `Modules/Category/Http/Controllers/Api/V1/ProjectController.php:80` — chặn `assign-employee` bằng `canAssign()` (trước đây API không kiểm tra gì)
3. `Modules/Category/Services/ProjectService.php` (store + update) — thông báo "cần phân công" gửi cho quản lý nhóm của người tạo, fallback về chính người tạo nếu họ có quyền
4. `Modules/Category/Services/CategoryDashboardService.php:131,361,1526` — đếm "dự toán cần phân bổ" theo cùng điều kiện
5. `app/Console/Commands/NotifyProjectAssignmentDue.php` — nhắc quá hạn gửi theo từng dự toán cho quản lý nhóm của người tạo

**Kết quả test (tinker, dữ liệu staging — 2 dự toán chờ phân công: #467 do emp 161 tạo, #549 do emp 70 tạo)**

| Người dùng | Quyền | Quản lý | DT#467 | DT#549 |
|---|---|---|---|---|
| emp 14 (QL nhóm Kinh doanh) | có | 70 NV | ✗ | ✓ |
| emp 66 (QL nhóm Dự án_HCM) | có | 22 NV | ✓ | ✗ |
| emp 44 | có | 6 NV | ✗ | ✗ |
| emp 70 (tự tạo, không QL ai) | có | 0 NV | ✗ | ✓ |
| emp 161 | không | 0 NV | ✗ | ✗ |

Thông báo "cần phân công": trước gửi cho **21 người** có quyền → nay gửi cho **2-3 quản lý nhóm** của người tạo.

Đang làm dở: (không)
Bước tiếp theo: test trên giao diện màn Dự toán (nút Phân công / Từ chối phân công) + dashboard Kế hoạch/Sale.
Blocked: (không)

### Checkpoint — 18/09/2026 (wrap up)
Vừa hoàn thành: viết tài liệu wrap up lần đầu của feature — `.plans/phan-cong-bao-gia-theo-nhom/design.md` (tóm tắt) và `docs/superpowers/specs/2026-09-18-phan-cong-bao-gia-theo-nhom-design.md` (spec đầy đủ: bối cảnh, quy tắc nghiệp vụ, từng file/dòng đã sửa kèm snippet, kết quả test, phần giữ nguyên có chủ đích). Đã bổ sung link design + spec vào `STATUS.md`.
Đang làm dở: (không)
Bước tiếp theo: Test UI màn Dự toán (nút Phân công / Từ chối phân công) + dashboard Kế hoạch/Sale.
Blocked: (không)
