# Chặn chọn phòng tiếp nhận khác công ty người tạo — YCLDBG / HDDV / PLBS HDDV

Repo `TanPhatDev`. Phụ trách @junfoke.

## Phạm vi

3 màn, đúng ô **Phòng tiếp nhận xử lý**:

| Màn | Route | FormRequest chặn BE |
| --- | --- | --- |
| YCLDBG (Yêu cầu lắp đặt bàn giao) | `assembly_requests` | `AssemblyRequestStoreRequest` + `changeDepartmentApprove` |
| HDDV (Hợp đồng dịch vụ SC-BH) | `warranty_repair_contracts` | `WarrantyRepairServiceContractStoreRequest` |
| PLBS HDDV | `warranty_repair_contract_addition_annexs` | dùng chung request trên |

**PL HDDV (`warranty_repair_contract_annexs`) NGOÀI phạm vi** — dùng request riêng
`WarrantyRepairServiceContractStoreAnnexRequest`, BE không chặn. Chỉ dropdown màn
`choiceReceptionDepartment` của nó đổi theo vì include chung
`warranty_repair_contracts/formJS.blade.php`.

## Cách làm

- `Department::getForSelectByCompany($companyId, $includeIds)` — phòng còn hoạt động của
  `$companyId`, **cộng thêm id đang được chọn trên phiếu** để mở phiếu cũ không mất giá trị.
  `$companyId = null` (màn tạo mới) thì lấy công ty người đang đăng nhập.
- `Department::isOfCompany($id, $companyId)` — dùng trong rule closure của FormRequest.
- Blade dùng biến riêng `$scope.departments_reception`; `$scope.departments` giữ nguyên cho ô
  **Phòng QTC** nên ô đó không bị lọc theo.
- Lỗi trả về đúng key `department_reception_id` → FE hiện inline dưới ô.

## Mốc so sánh — đã đổi 1 lần

| Bản | Mốc | Commit |
| --- | --- | --- |
| Đầu | Công ty người **đang đăng nhập** | (bỏ) |
| 2 | `company_id` **ghi trên phiếu** | `9e62363b5b` (master) |
| **Hiện tại** | **Công ty HIỆN TẠI của người tạo** (`employee_infos.company_id` của `created_by`) | `c1b289c18d` (nhánh `task_11473`) |

Bản 2 bị Redmine **#11473** trả lại: đổi công ty nhân viên sang CN Hải Phòng rồi mở phiếu cũ thì
dropdown vẫn ra phòng công ty cũ, vì `company_id` trên phiếu đóng băng lúc tạo.

Bản hiện tại đọc động qua `Employee::companyIdOf()` + accessor `creator_company_id` trên
`AssemblyRequest` và `WrServiceContract`. Không tra được hồ sơ người tạo thì **lùi về
`company_id` của phiếu**, không trả null (null sẽ nới lỏng ràng buộc).

⚠️ **Đánh đổi đã được user chốt (16/09/2026):** người tạo chuyển công ty thì phiếu cũ đổi danh sách
phòng theo, nên một phiếu công ty A có thể nhận phòng tiếp nhận công ty B. Bất biến "phòng tiếp nhận
luôn cùng công ty với phiếu" **không còn được giữ** — đây là lựa chọn có chủ đích, đừng "sửa lại cho
đúng" ở phiên sau.

## Task

- [x] `Department::getForSelectByCompany` + `isOfCompany`
- [x] 3 blade `formJS` dùng `departments_reception`
- [x] Chặn BE ở `store` / `update` / `reception` / `changeDepartmentApprove`
- [x] Đổi mốc sang công ty hiện tại của người tạo (#11473)
- [ ] Push `task_11473` + merge về `master`
- [ ] Phản hồi Redmine #11473

### Checkpoint — 16/09/2026

Vừa hoàn thành: đổi mốc sang `creator_company_id`, commit `c1b289c18d` trên `task_11473`
(rẽ từ `master`). Verify local **16/16** bằng curl trên `artisan serve :8001`:

- FE — YCLDBG 24 (phiếu công ty 1, người tạo id 47 nay ở công ty 7): dropdown còn **3 option** =
  2 phòng công ty 7 + phòng `HN_KTCN` đang chọn của phiếu (giữ qua `includeIds`).
  YCLDBG 41 (người tạo vẫn công ty 1) và màn tạo mới: 28 phòng, 100% công ty 1.
- BE — phiếu YCLDBG 24: `update` / `changeDepartmentApprove` cho qua phòng công ty 7, chặn phòng
  công ty 1. WrSC 195 (phiếu công ty 4, người tạo nay công ty 1): `update` / `reception` của cả
  HDDV lẫn PLBS cho qua phòng công ty 1, chặn phòng công ty 4. Tạo mới: chặn phòng công ty 7.
  PL HDDV `store` không chặn — đúng thiết kế.

Bước tiếp theo: push nhánh + phản hồi task 11473.

Blocked: chưa tái hiện được trực tiếp trên dev vì hồ sơ Trịnh Thị Lợi (id 787) đã được trả về
công ty 1 — dùng dữ liệu local có sẵn 2 phiếu lệch (YCLDBG 24, WrSC 195) để đối chứng thay thế.

## Bẫy đã trả giá

- `php artisan route:list` ở repo này **chết** (`ProductExportRequest::CHO_DUYET_NHAP` undefined) —
  lấy URL bằng `route('<name>', $id, false)` qua tinker.
- Lỗi validate trả về JSON **escape unicode** (`c\u00f4ng ty`) → `grep` chuỗi tiếng Việt trên
  response curl luôn trượt, phải `json.loads` rồi mới so.
- Màn `edit` / `choiceReceptionDepartment` hay trả "Không có quyền truy cập" tuỳ trạng thái phiếu —
  đừng kết luận "thiếu biến / chưa deploy" khi chưa xem `<title>`.
