# Fix popup Người duyệt lỗi Ajax ở Hỗ trợ hạch toán HĐ hãng

Ngày 07/11/2026, nhánh `gop_db`.

## Lỗi

- Màn `admin/sale/firm-contracts/{id}/support-accounting`, popup Người duyệt báo DataTables Ajax error.
- Log: `Call to undefined method Spatie\Permission\Models\Role::baseNameSql()`.

## Nguyên nhân

- Commit RBAC `5101a750a9` thêm `Role::baseNameSql()` vào nhánh `level == 2` của `SearchController::searchEmployee`.
- File này import `Spatie\Permission\Models\Role`; hàm chỉ có ở `App\Model\Common\Role`.
- Mọi popup gọi `searchEmployee` với `level=2` đều dính.

## Task

- [x] Gọi hàm qua `\App\Model\Common\Role`, như `AnalyticController` đang làm.
- [x] Rà 38 file import Role của Spatie: không còn chỗ nào gọi hàm riêng của model app.
- [x] Đối chiếu DB `hrm_erp_gop` chỉ đọc: có cột `base_name`, 6 vai trò Giám đốc, 14 nhân viên.
- [x] Commit và push `gop_db`.
- [ ] Kiểm lại popup trên production sau khi deploy.

## Lưu ý

DB local `erp_hrm_check` chưa có `roles.base_name`, nên không tái hiện trọn popup ở local.
