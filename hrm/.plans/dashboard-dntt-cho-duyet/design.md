# Dashboard — Box "Đề nghị thanh toán chờ duyệt" (@khoipv)

## Mục tiêu
Thêm 2 dòng vào card **"Công việc chờ duyệt"** trên Dashboard Giao việc (`/assign/dashboard`),
hiển thị số Đề nghị thanh toán (DNTT = `PaymentBusinessRequest`) đang chờ duyệt, lọc theo quyền + phạm vi TK quản lý.

## Scope
- **DNTT chờ TP duyệt** — hiện khi TK có quyền `TP Duyệt đề nghị thanh toán` (id 975).
  Đếm phiếu `status = CHO_TP_DUYET (2)` trong phạm vi Xem của TK.
- **DNTT chờ KT duyệt** — hiện khi TK có quyền `KT Duyệt đề nghị thanh toán` (id 980).
  Đếm phiếu `status = CHO_KT_DUYET (3)` trong phạm vi Xem của TK.
- Có cả 2 quyền → hiện cả 2 dòng (cơ chế `isShow` + `getAllCurrentPermission()` sẵn có).
- Vị trí: ngay **dưới** dòng "Hồ sơ thanh toán chi phí công tác chờ duyệt".

## Quyết định chốt (cập nhật 2026-07-17)
- **Phạm vi = dùng lại scope màn danh sách** (user chốt lại sau khi thấy scope cũ không thấy công ty khác).
  Nhân bản đúng logic phân cấp của `PaymentBusinessRequestCriteria` vào private helper
  `WaitingApproveService::applyPaymentBusinessRequestScope()` theo các quyền **Xem**:
  - `Xem ... theo tổng công ty` (976) → **không lọc** (thấy TẤT CẢ công ty)
  - `Xem ... theo công ty` (977) → `company_id = current_company_role`
  - `Xem ... theo phòng ban` (978) → `department_id ∈ listManageDepartmentIds()` OR mình tạo OR mình là NV
  - `Xem ... theo bộ phận` (1022) → mình tạo OR mình là NV
  - (không quyền) → chỉ phiếu của mình
- **KHÔNG sửa `PaymentBusinessRequestCriteria`/màn danh sách** (hàm dùng chung) — chỉ nhân bản để tránh
  regression. Nếu Criteria đổi scope → cập nhật đồng bộ helper.
- Số đếm giờ **khớp** tổng dòng màn danh sách khi lọc đúng status (2/3).
- Cấp **bộ phận** vẫn không lọc theo `part_id` (bảng thiếu cột) — đồng nhất Criteria (đã comment part_id).
- Box vẫn gate bằng quyền **duyệt** (975/980); phạm vi đếm theo quyền **xem**. TK có quyền duyệt nhưng
  không có quyền xem tương ứng → đếm hẹp (chỉ phiếu của mình) — giống hành vi màn danh sách.

## File thay đổi
| Layer | File | Thay đổi |
| --- | --- | --- |
| BE | `Modules/Assign/Services/Dashboard/WaitingApproveService.php` | +2 method đếm + import model |
| BE | `Modules/Assign/Services/Dashboard/DashboardService.php` | +2 count call + 2 item mảng |
| FE | `pages/assign/payment_business_request/index.vue` | `mounted()` đọc `$route.query.status` → `formFilter.status` |

FE card **không cần sửa** — `CardSimpleTotal` type 1 tự render dòng mới.

## Không đụng
Không migration, không permission mới (dùng quyền 975/980 có sẵn), không git.

Spec đầy đủ: `docs/superpowers/specs/2026-07-17-dashboard-dntt-cho-duyet-design.md`
