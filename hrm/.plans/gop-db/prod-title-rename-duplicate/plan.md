# Điều tra lỗi sửa chức danh trên PROD (TPV_Giám đốc chi nhánh Vinh) — @cuong61n

- [x] 05/11/2026 — Điều tra: user đổi tên chức danh id 368 `TPV_Giám đốc chi nhánh Vinh` → `Giám đốc chi nhánh Vinh` ở màn Chức danh (prod) bị lỗi.
  - Nghiệp vụ: tên mới đã có ở chức danh khác — id 92 `Giám đốc chi nhánh Vinh` (mã `GĐCN_CNV`, công ty 1, 0 nhân viên đang dùng); id 368 có 2 nhân viên đang dùng.
  - Kỹ thuật: log `laravel.log` 05/11 08:39–10:16 (user 408, 867) `1062 Duplicate entry ... titles_name_unique`. Bản ghi 92 lưu Unicode tổ hợp (NFD, `a`+dấu rời) nên tìm theo chữ không thấy, nhưng collation `utf8mb3_unicode_ci` coi là trùng. BE không validate `unique` → nổ 500 thay vì báo "Đã tồn tại trên hệ thống".
  - Trạng thái: đã báo user → user chốt: **cho phép trùng tên chức danh, chỉ mã không được trùng**.
- [x] 05/11/2026 — Bỏ ràng buộc trùng tên chức danh (hrm-api, nhánh `fix/title-allow-duplicate-name` tách từ `origin/gop_db`).
  - Nghiệp vụ: 2 chức danh được đặt cùng tên (vd "Giám đốc chi nhánh Vinh" ở công ty 1 và công ty 3), mã vẫn phải duy nhất.
  - Kỹ thuật: migration `2026_11_05_100000_drop_unique_name_on_titles_table` bỏ `titles_name_unique`, thêm index thường `titles_name_index` (các luồng import tra theo tên). `CreateTitleRequest` vốn chỉ kiểm `unique` ở `code` nên không phải sửa.
  - Đã kiểm trên DB local `local_hrm_erp`: chạy migration OK; tạo trùng tên → lưu được; trùng mã → vẫn bị chặn 1062 (dữ liệu thử đã rollback).
  - Rủi ro đã báo user: import Excel (EmployeeImport, DecisionSalaryChangeImport, DecisionLaborContractNoManpowerImport) tra chức danh theo tên `->first()` → khi trùng tên sẽ lấy bản id nhỏ nhất.
  - Trạng thái: đã push `gop_db` commit `66f442ebd`, **đã deploy prod 05/11/2026**.
- [x] 05/11/2026 — Deploy prod: `~/build_tpe.sh` kéo code OK nhưng dừng ở `php artisan migrate` (prod hỏi xác nhận yes/no, chạy qua ssh không trả lời được → tự huỷ, các bước route:cache/seeder/FE không chạy — lần này không cần vì không đổi route/quyền/FE). Đã chạy tay `php artisan migrate --force` → index `titles` còn `titles_code_unique` + `titles_name_index`. Thử đổi tên id 368 → "Giám đốc chi nhánh Vinh" trong transaction (đã rollback) → update OK.
  - Lưu ý cho lần sau: chạy `build_tpe.sh` qua ssh không có TTY thì migrate bị huỷ → script nên dùng `migrate --force`.
