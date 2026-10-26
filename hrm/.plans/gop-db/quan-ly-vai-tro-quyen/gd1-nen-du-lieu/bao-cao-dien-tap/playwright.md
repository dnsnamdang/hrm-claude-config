# Diễn tập Vai trò & Quyền giai đoạn 1 — 26/10/2026

## Môi trường

| | Mốc (chưa chuyển đổi) | Diễn tập |
|---|---|---|
| DB | `hrm_erp_21_10_prod` (bản sao prod 21/10) | `hrm_erp_rbac_rehearsal` = nhân bản `hrm_erp_21_10_prod` (10 phút, 1.911 bảng, số dòng khớp) |
| Code | checkout chính `gop_db` | worktree `wt-rbac/*` nhánh `rbac` (chưa commit) |
| hrm-api / hrm-client | :8000 / :3000 | :8011 / :3011 (`NUXT_BUILD_DIR=.nuxt-rbac`, API trỏ :8011 qua biến môi trường) |
| ERP | :8098 (checkout chính) | :8099 (worktree) |

DB diễn tập chạy theo đúng `runbook-go-live.md`: 6 migration `gop_db` còn chờ (2026_10_22_*, 2026_10_23_*) → 5 migration `2026_11_01_000001…5` (lẻ, `--path`) → `rbac:convert --dry-run` → `artisan down` + `rbac:convert --erp-da-bao-tri`.

## Kết quả chuyển đổi

- Dry-run: mã 0, `chenh-lech-khac` = 0, checksum 32 bảng không đổi (chỉ AUTO_INCREMENT nhảy — InnoDB không trả lại khi rollback).
- Chạy thật: 16 giây. Dữ liệu commit, **DDL sau commit lỗi** `1832 Cannot change column 'company_id': used in a foreign key constraint 'roles_company_id_foreign'`.
  - Sửa `TableRebuilder::finishPlan()` thành 3 bước tự xét trạng thái: gỡ FK → `MODIFY … NOT NULL` → gắn lại FK.
  - `rbac:convert --resume-ddl --erp-da-bao-tri` chạy tiếp xong. Đây là lần đầu đường `--resume-ddl` được dùng thật — hoạt động đúng.
- Sau chuyển đổi: `roles.company_id` NOT NULL + unique `(company_id, base_name)`; rhp/ehr dựng lại có FK mới; `role_has_permissions` không còn `company_id`; `permission:catalog-sync --dry-run` = 0 thay đổi (892 mã, 1.764 tên cũ).
- Số liệu (`chay-that/tom-tat.json`): gán quyền 21.212 → 15.295; 284 cặp vai trò × công ty (145 vai trò mới); chuyển hướng 11.027 dòng trỏ role id + sửa lệch id ERP 2.248 hợp đồng; 304 dòng không tự chuyển được (133 công ty không có trong map, 56 không xác định công ty, 115 bảng không có cột công ty) ⇒ `du-lieu-tro-role-id.csv`.
- Báo cáo mất/thêm: `mat-do-bit-ro` 23.645; `mat-do-cong-ty-qua-vai-tro` 29.856 (dùng được trên giao diện 15.720, 14 NV / 55 cặp); `bo-theo-danh-muc` 9.189; thêm do gộp nền tảng 18.321, cấp cao bao thấp 21.579, Super Admin 29.920, gộp cùng mã 2.436, bổ sung công ty làm việc 289, model_type 0; thiếu quyền xem 106.
- Script khôi phục phụ: `chay-that/rollback.sql` (87 dòng, chỉ in, chưa chạy thử).
- Test sau chuyển đổi: hrm-api Rbac 168 + 13 xanh (trên DB test).

## Tài khoản kiểm

| Mã NV | Người | Đặc điểm |
|---|---|---|
| 987 | Hà Mạnh Cường | 1 công ty (TPE), 11 vai trò |
| 407 | Cao Thị Thùy Linh | 2 công ty (TPE, TPV), 12 vai trò |
| 196 | Nguyễn Thị Ngọc Hà | có vai trò Super Admin (TPE) |

Đăng nhập: JWT HRM / phiên ERP (redis) cấp bằng tinker, không qua màn đăng nhập.

## HRM — quyền trả về từ API profile (`/api/v1/users/auth/user-profile`)

| NV | Mốc | Diễn tập | Mất | Thêm | Đối chiếu báo cáo |
|---|---|---|---|---|---|
| 987 | 232 | 257 | 3 | 28 | mất 3 = `bo-theo-danh-muc`; thêm 16 gộp nền tảng + 12 cấp cao |
| 407 | 11 | 99 | 0 | 88 | 52 gộp nền tảng; 36 còn lại* |
| 196 | 204 | 890 | 3 | 689 | mất 3 = `bo-theo-danh-muc`; 538 Super Admin + 86 gộp nền tảng + 9 cấp cao; 56 còn lại* |

\* 92 quyền "còn lại" đều là tên **trùng y hệt ở cả ERP và HRM** (cùng mã sau gộp). HRM cũ gom quyền theo tên không lọc guard nên ở tầng API (middleware) người dùng đã có các quyền này; chỉ API profile cũ lọc guard api nên menu không hiện. Báo cáo tính theo tầng API nên không ghi là "thêm". Đã kiểm 92/92 cùng nguyên nhân. Hệ quả cho QA: menu HRM của người có quyền ERP trùng tên sẽ hiện thêm mục.

Đổi công ty (NV 407, gọi `update-company-role` trên DB diễn tập rồi đặt lại NULL): TPE 12 quyền, TPV 99 quyền; chỉ-TPE 1, chỉ-TPV 88 — quyền không lọt chéo công ty.
API đổi công ty trả 500 `Unsupported driver []` ở local: model `EmployeeInfo` đồng bộ sang kết nối tenant `mysql_tpe/etek/...` mà `.env` local (cả checkout chính) không khai báo. Không do nhánh `rbac`; trên prod có cấu hình. Giá trị công ty vẫn được lưu.

## HRM — đo DOM (Playwright, chờ 15 giây mỗi màn, viewport 1440)

Cột: số đường dẫn menu khác nhau / số dòng bảng / số nút thao tác. Mọi lượt: 0 request API lỗi (≥ 400).

| NV | Màn | Mốc | Diễn tập | Nút khác nhau |
|---|---|---|---|---|
| 987 | Báo giá `/assign/quotations` | 25 / 1 / 6 | 25 / 1 / 6 | — |
| 987 | Hàng hoá `/master-data/products/company` | 21 / 1 / 4 | 41 / 20 / 4 | thêm quyền xem (gộp nền tảng) |
| 987 | Chấm công `/timesheet/attendance` | 54 / 10 / 3 | 54 / 10 / 3 | — |
| 407 | Báo giá | 25 / 1 / 6 | 25 / 1 / 6 | — |
| 407 | Hàng hoá | 41 / 20 / 7 | 41 / 20 / 7 | — |
| 407 | Chấm công | 44 / 10 / 3 | 44 / 10 / 3 | — |
| 196 | Báo giá | 25 / 1 / 6 | 61 / 20 / 6 | Super Admin đủ mã, phạm vi Tổng công ty |
| 196 | Hàng hoá | 41 / 20 / 4 | 41 / 20 / 7 | + Tạo mới, Xây dựng catalog, Xuất Excel |
| 196 | Chấm công | 55 / 10 / 3 | 69 / 10 / 3 | Super Admin đủ mã |

Lưu ý đo: lượt đầu chờ 7 giây cho ra số 0/1 dòng giả vì Nuxt dev đang biên dịch trang; đo lại chờ 15 giây và xác minh bằng request API thật (`/products/company` trả 20 dòng ở cả 2 bên).

## ERP — so HTML server render (bỏ `<script>`, chuẩn hoá cổng)

| NV | Màn | Đường dẫn trên trang (mốc / diễn tập) | Nút | Khác nhau |
|---|---|---|---|---|
| 987 | `/admin/customers`, `/admin/quotations`, `/admin/products` | 485 / 485 · 481 / 481 · 485 / 485 | giống | không |
| 407 | 3 màn | 521 / 487 · 517 / 483 · 521 / 487 | giống | mất 34 mục menu chờ duyệt/chờ hạch toán (hợp đồng chờ, YC hạch toán dịch vụ, phiếu thu/điều chỉnh công nợ chờ kế toán…) = 76 quyền ERP ở TPV trong `mat-do-bit-ro` (vai trò chỉ được tick ở cột công ty khác — user chốt A, theo đúng ô tick) |
| 196 | 3 màn | 531 / 530 · 527 / 526 · 531 / 530 | giống | mất "Kế hoạch bán hàng phòng chờ duyệt" — gỡ đặc quyền Super Admin (user chốt A 26/10), không thuộc báo cáo mã |

Chênh lệch dung lượng trang ERP (0,5–0,9 MB) là thanh debug PHP (ghi câu truy vấn), không phải nội dung.

## Kết luận

- Chuyển đổi chạy được trên bản sao prod sát nhất; phát hiện và sửa 1 lỗi DDL (FK khi MODIFY), đường `--resume-ddl` đã kiểm thật.
- Mọi chênh lệch đo được trên 3 tài khoản × 2 app đều khớp báo cáo hoặc quyết định đã chốt.
- Việc còn lại trước go-live: xem `runbook-go-live.md` mục A (quản trị viên cấp lại theo danh sách lần chạy này; báo người dùng Super Admin; script e2e/seeder; tenant khác).
