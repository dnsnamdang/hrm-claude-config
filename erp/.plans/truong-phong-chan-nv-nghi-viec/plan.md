# Chặn chọn nhân viên đã nghỉ làm Trưởng phòng (màn Phòng ban ERP)

@junfoke · Repo `TanPhatDev`, nhánh `gop_db`

## Bối cảnh (02/10/2026)
Chị Thúy (KT) báo phòng `MT_KD` Kinh doanh CN Vinh (id 77) bị đổi trưởng phòng từ Nguyễn Đình Đông
(`employees.id` 1056) sang Phạm Sơn Tùng (926, đã nghỉ) → hạch toán sai. Cùng kiểu ở phòng TBCN.

- Nguyên nhân gốc: ô Trưởng phòng dùng `ALL_EMPLOYEES = Employee::getAll(true)` → gồm cả người đã
  nghỉ (1.101 người, chỉ 554 đang làm ở DB local); BE `update/store` chỉ `required`, không kiểm
  trạng thái. Mỗi lần Lưu popup đều ghi lại trưởng phòng.
- Hạch toán thưởng (work 12/13/14) ghi `account_details.employee_id` = trưởng phòng TẠI LÚC hạch
  toán, không đọc lại → sửa phòng ban không tự sửa hạch toán cũ.
- Không do HRM: không có `department_changes` cho phòng 77; số 1056 HRM đọc sai nghĩa ra rỗng.

## Xử lý dữ liệu prod (user chạy 02/10/2026)
- 31 dòng `account_details` (13 HĐ: quyết toán 28517 + xuất kho/bán mượn 28664, 28722–28728,
  28730, 28732, 28763), tất cả hạch toán 01/10 09:06–15:33 (phòng được sửa lại 16:34 bởi Đào Thị
  Thúy) → `UPDATE employee_id 926 → 1056` theo danh sách id.
- Phiếu quyết toán quý (`bill_commission/productivity_settlement_quarter_employees`): không có
  dòng nào của Tùng → không cần lập lại.

## Tasks
- [x] Truy nguyên nhân + SQL sửa hạch toán
- [x] `DepartmentsController@index`: truyền `$lead_employees = Employee::getEmployeeActive()`
- [x] `DepartmentsController::validateDepartmentLead()`: chặn trưởng phòng MỚI đã nghỉ ở store +
      update; giữ nguyên trưởng phòng hiện tại thì cho qua (không chặn sửa trường khác)
- [x] `common/departments/index.blade.php`: ô Trưởng phòng (tạo + sửa) dùng `LEAD_EMPLOYEES`;
      trưởng phòng hiện tại đã nghỉ vẫn hiện đúng tên (`leadOptionsFor`); hiện lỗi dưới ô
- [x] Verify: tinker 4 ca validate; browser :8001 (DB gop_db local) — sửa phòng không có người nghỉ
      trong DS, trưởng phòng đã nghỉ (Lê Tất Long, id 309) vẫn hiện, popup Tạo mới không có người nghỉ
- [ ] Commit + deploy
- [ ] (Đề xuất, chưa làm) Ghi lịch sử đổi trưởng phòng

### Checkpoint — 02/10/2026
Vừa hoàn thành: code 2 file + verify local
Đang làm dở: —
Bước tiếp theo: user chốt commit (nhánh `gop_db`), deploy
Blocked:
