## Global Constraints

Mọi task đều ngầm bao gồm phần này. Giá trị lấy nguyên văn từ spec + dữ kiện đã kiểm chứng (2026-09-12):

- **Nhánh:** `gop_db` (cả hrm-api + hrm-client). KHÔNG dùng `DB_CONNECTION_SECOND`/`mysql2` — mọi truy vấn đi connection mặc định (DB gộp).
- **KHÔNG commit/push git** trừ khi người dùng yêu cầu rõ. Giữ nguyên line-ending (LF/CRLF) từng file.
- **Mọi model mới PHẢI `extends App\Models\BaseModel`** (tự set created_by/updated_by/company_id... qua `boot()`, guard bằng `Schema::hasColumn`).
- **7 cột Công nợ trên `companies` đã tồn tại sẵn trên DB gộp (do ERP tạo), hrm-api KHÔNG quản lý bằng migration → tuyệt đối KHÔNG viết migration tạo/sửa 7 cột này.** Danh sách 7 cột + metadata (thứ tự cố định dùng xuyên suốt payload/diff/validation):

  | # | key (cột `companies`) | label (nhãn tiếng Việt) | unit | kiểu | validation |
  |---|---|---|---|---|---|
  | 1 | `limit_export_debt_employee` | Hạn mức công nợ xuất hàng NV | đồng | integer | `required\|integer\|min:0` |
  | 2 | `adjust_odd_balance` | Số dư lẻ tối đa cho phép điều chỉnh | đồng | integer | `required\|integer\|min:0` |
  | 3 | `overdue_date_max_customer` | Số ngày quá hạn tính lãi (Bán lẻ) | ngày | integer | `required\|integer\|min:0` |
  | 4 | `overdue_date_max_agency` | Số ngày quá hạn tính lãi (Đại lý) | ngày | integer | `required\|integer\|min:0` |
  | 5 | `overdue_date_max_service` | Số ngày quá hạn tính lãi (Dịch vụ) | ngày | integer | `required\|integer\|min:0` |
  | 6 | `warning_due_date` | Thời gian cảnh báo thu nợ đến hạn | ngày | integer | `nullable\|integer\|min:0` |
  | 7 | `interest_rate` | Lãi suất | % | decimal | `required\|numeric\|min:0` |

  (Validation port từ ERP `CompanyRegulationRequest`: các số quá hạn/hạn mức/số dư = `integer`; `interest_rate` = `min:0`; `warning_due_date` ERP không có rule → `nullable`.)
- **NGOÀI phạm vi Slice 1:** field mock `Thuế vận tải` và `Ngày khai báo công nợ đầu kỳ` (dateField `fixed=true`) — chưa xác minh cột `companies` tương ứng và không phải giá trị versioning; giữ hiển thị mock/read-only, KHÔNG version hoá trong slice này.
- **History = Cách A:** khi áp, ghi vào `company_regulation_histories` (schema ERP: `id, company_id, created_by, field_name, name, value_before decimal(16), value_after decimal(16), timestamps`), **mỗi field đổi giá trị = 1 dòng**. `created_by` = **người tạo phiên bản** (`regulation_scheduled_versions.created_by`), KHÔNG phải `auth()` (cron chạy không có auth). `diff_snapshot` chỉ để hiển thị hàng đợi, không thay history.
- **Không có bước duyệt** (spec §10, giai đoạn 1). Gate quyền = tái dùng quyền sẵn có, KHÔNG đẻ quyền mới (xem Task 6 để xác định tên quyền).
- **Response API:** dùng `App\Http\Controllers\Api\Traits\ResponseTrait` — `responseSuccessJson($message, $code, $data)`, `responseJson($message, $code, $data)`, `responseValidationErrorJson`. Gate quyền bằng `isCurrentEmployeeHasPermission($perm)`.
- **`tab_key` = `'congno'`, `scope_type` = `'company'`, `scope_id` = `company_id`** cho toàn Slice 1. Thiết kế đủ tổng quát để tab Form khác tái dùng bảng/service.
- **Test chạy DB gộp thật (dev), KHÔNG `RefreshDatabase`.** Vì 7 cột `companies` không nằm trong migration hrm-api, một test DB dựng-từ-migration sẽ thiếu cột. Dùng trait `Illuminate\Foundation\Testing\DatabaseTransactions` để rollback sau mỗi test. Trước khi chạy test đọc `grep DB_ hrm-api/.env` xác nhận trỏ DB gộp có sẵn 7 cột + bảng `company_regulation_histories`.

---

