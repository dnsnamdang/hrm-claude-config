# Phiếu chờ duyệt tập trung — ERP + HRM (hộp duyệt chung)

Khởi động 22/10/2026. Trạng thái: **TẠM DỪNG 22/10 — spec + danh mục + mockup đã duyệt; plan đợt 1a CHƯA viết**, chưa đụng source/DB.

## Đã chốt với user

| Ngày | Nội dung |
|---|---|
| 22/10 | Hướng dài hạn: mọi chức năng ERP sẽ chuyển sang HRM; giai đoạn gần chạy song song ⇒ làm trên **cả 2 nền tảng**. |
| 22/10 | **1 hộp duyệt chung**, xem được ở cả ERP và HRM; bấm phiếu mở đúng hệ thống sở hữu phiếu. |
| 22/10 | Chưa cập nhật ngay ⇒ làm trên **worktree riêng** (không làm thẳng `gop_db`). |
| 22/10 | **Bỏ ngoại lệ Super Admin** ở registry (Super Admin xét quyền như mọi người). |
| 22/10 | Phạm vi: kiểm kê lại đủ cả ERP + HRM rồi mới chốt (2 file kiểm kê bên dưới). |
| 22/10 | "Chờ duyệt" = duyệt/không duyệt **+ tiếp nhận + lập chứng từ kế tiếp** (hộp là danh sách việc đang chờ mình xử lý: KT lập phiếu chi/phiếu xuất, chờ làm báo giá…). |
| 22/10 | Đợt 1 = **nghiệp vụ**: toàn bộ luồng ERP + HRM Assign/Finance/CSKH/MasterData/Meeting. Đợt 2 = nhân sự (Timesheet/Decision/Training/Payroll/Human). Assign legacy (AS16–AS20, AS22) để riêng. |
| 22/10 | Tồn đọng: **hiện hết, không sửa dữ liệu nguồn**; phiếu gửi quá N ngày tách nhóm "Quá hạn", badge chỉ đếm phiếu trong hạn. |
| 22/10 | Luồng làm được ở 2 nơi: mỗi loại phiếu × cấp khai **1 nơi xử lý** = nơi làm được trọn bước đó (HRM nếu đủ, còn lại ERP); HRM bổ sung xong chỉ đổi khai báo. Không khoá phía ERP. |
| 22/10 | Công ty: **chỉ phiếu của công ty đang làm** (+ phiếu không gắn công ty), giữ như registry ERP cũ; đổi công ty mới thấy phiếu công ty khác. |
| 22/10 | Người duyệt: theo **gate thật của màn gốc** (kể cả duyệt theo vai trò TĐ/GĐ, approver_id, quản lý phòng); luồng gate gốc cho "mọi người" duyệt (KH PTTT/KH bán hàng NV cấp 2) **chưa đưa vào**, ghi danh sách chờ nghiệp vụ. |
| 22/10 | Kiến trúc: **A — cả 2 hệ thống cùng đẩy vào registry** `approval_inbox` dùng chung (không chọn quét định kỳ C, không đọc trực tiếp B). |
| 22/10 | Màn HRM gate qua spatie guard api (khe `App\Employee`, 7 dòng ⚠ flows-dot1 §7): **sửa gate sang trait CEP trong feature này**, rồi khai handler = HRM. |
| 22/10 | Thiết kế 4 phần đã duyệt trong chat → spec [design.md](design.md) + danh mục [flows-dot1.md](flows-dot1.md) chờ user duyệt. |
| 22/10 | User nghi số C3 "chờ làm báo giá" → khảo sát lại: điều kiện thật = status 2 **và có thiết bị sửa chữa/bảo dưỡng** (`WrServiceQuotationService` scope `waiting_create_quotation`) ⇒ **188 phiếu** (175 quá 30 ngày), không phải 4.686. 4.520 phiếu thuần bảo hành không cần báo giá. Tổng danh mục đợt 1: 2.166. |
| 22/10 | Rà lại toàn bộ 155 dòng theo điều kiện màn gốc (recheck-A/B/C.md): đổi số C5 243→428, HĐ bán 11→14, hạch toán bổ sung 39→38; ~11 dòng chặt điều kiện, ~10 gate sửa, ~14 nhóm nghi rác chờ nghiệp vụ. **Tổng đợt 1: 2.353** (ERP 1.390 · HRM 963). Tổng hợp: flows-dot1.md §8. |
| 22/10 | **Loại nhóm "chờ giao việc" khỏi hộp duyệt** (tính chất khác — hàng đợi điều phối theo số lượng còn lại): HĐ dịch vụ C5 (428), PL bổ sung (24), HĐ bảo hành, YC lắp đặt / YC khác chờ giao việc. **Tổng đợt 1: 1.925** (ERP 962 · HRM 963). |
| 22/10 | Mockup HRM [mockup.html](mockup.html) (4 khung: Phiếu chờ duyệt + tab Quá hạn, Báo cáo phê duyệt, my-job › Chờ duyệt, badge topbar) — token đo từ app thật, **chờ user duyệt**. |
| 22/10 | **User duyệt spec + danh mục + mockup.** Thứ tự: **màn Chờ duyệt (danh sách) ở CẢ HRM và ERP làm trước** (kèm toàn bộ nền: registry, sync, bộ giải quyền, khai báo luồng); các màn khác (my-job tab, badge topbar) + báo cáo làm sau. (Chưa phải lệnh code — hỏi riêng kèm phạm vi.) |

## Hiện trạng nền

- Registry `approval_inbox` (ERP, 49 loại, live-hook + `backfill --prune`) chỉ có trên `develop_01`
  (merge `6134e90` + `46ab7152`); **`gop_db` và prod chưa có**. Ghi chú port: `ERP/.plans/phieu-cho-duyet-tap-trung/port-gop-db.md`.
- HRM chưa đọc/ghi `approval_inbox`; tab `my-job › Chờ duyệt` là chỗ giữ chỗ (badge gán cứng '4').

## Kiểm kê (22/10, DB `hrm_erp_21_10_prod`)

- [inventory-erp.md](inventory-erp.md) — 99 luồng thật (49 đã có trong registry, 50 chưa) · 46 luồng có phiếu chờ · 1.424 phiếu.
- [inventory-hrm.md](inventory-hrm.md) — 100 luồng ứng viên · 55 luồng có phiếu chờ · 12.147 phiếu; **34 luồng làm trên bảng ERP** (F1–F25, C1–C5, M1/M2/M4/M5).

### Gộp

| Nhóm | Luồng | Ghi chú |
|---|---:|---|
| Chỉ ERP | ~65 | 99 luồng ERP trừ phần trùng với HRM |
| Trùng (bảng ERP, duyệt được ở 2 nơi hoặc đã chuyển hẳn sang HRM) | 34 | MasterData đã khoá phía ERP (`productMovedToHrm`); Finance/CSKH còn route duyệt ở cả 2 |
| Chỉ HRM | ~66 | Timesheet 11, Human 2, Payroll 2, Meeting 1, Training 8, Decision 21, Assign 21 |
| **Tổng luồng duy nhất** | **~165** | |

Phiếu đang chờ (kiểm kê thô, trước khi rà): C3 "chờ làm báo giá" ghi 4.686 — **sai, thật là 188** (xem dòng 22/10 ở trên); H22 điểm danh 3.631 (đợt 2, chưa rà); Assign legacy 1.581 (ngoài đợt 1).
Bỏ 3 khối này: ERP ~1.424 + HRM riêng ~1.000 (Timesheet 1.273 gồm ~370 phiếu làm thêm/đi muộn đã quá hạn).

## Câu hỏi nghiệp vụ chặn thiết kế (hỏi lần lượt)

1. Định nghĩa "chờ duyệt": chỉ bước duyệt/không duyệt, hay gồm cả **tiếp nhận** (AS6, AS7, C5, bàn giao ERP)
   và **lập chứng từ kế tiếp** (F1, F6, F7, F11, F16, F19, F22, ĐNTT status 6/7, C3)?
2. Đợt đầu gồm nhóm nào: nghiệp vụ (ERP + Assign/Finance/CSKH/MasterData/Meeting), nhân sự (Timesheet/Decision/
   Training/Payroll/Human), Assign legacy?
3. Tồn đọng: dọn/đóng hàng loạt trước go-live hay hiển thị và tách nhóm "quá hạn"?
4. 34 luồng duyệt được ở 2 nơi: ai push vào registry (cả 2 phía hook, hay model-event dùng chung), có khoá phía ERP không?
5. Quy tắc quyền: quyền cấp ở công ty A có áp phiếu công ty B không; registry xét quyền guard nào (web/api) khi
   cùng tên quyền tồn tại 2 bản; khe `model_type = App\Employee` (1.355 role) làm spatie bên HRM không thấy quyền.
6. Luồng chưa rõ người duyệt (H8 phiếu giao việc, H9 công tác, H14 P3, H22 điểm danh, H13 thông báo nội bộ;
   ERP: KH PTTT/KH bán hàng NV cấp 2, báo giá dự án duyệt theo vai trò).

## Lỗi phát hiện ngoài phạm vi (ghi lại, không vá trong đợt này)

Xem mục "Lỗi và rủi ro" cuối `inventory-hrm.md` và mục 8–9 `inventory-erp.md`. Nặng nhất:
- Nhóm route job-assignment HRM thiếu `auth:api` (`Modules/Timesheet/Routes/api.php:176`, khai `' middleware'`).
- `BusinessTripAssignService::approve()` lộ toàn bộ phiếu công tác.
- ~20 luồng HRM chỉ ẩn nút ở FE, BE không kiểm quyền.
- CustomerCare HRM khoá với mọi người do khe `model_type`.


## Tạm dừng 22/10 — việc tiếp theo

1. **Viết plan đợt 1a** (`plan-dot1a.md`, skill writing-plans): nền (registry, `sync()`, bộ giải quyền, khai báo luồng, hook) +
   màn Chờ duyệt (danh sách) ở **cả HRM và ERP**. Các màn khác (my-job tab, badge topbar) + báo cáo làm sau.
2. Duyệt plan → **hỏi riêng cho phép code** (repo · nhánh `gop_db-phieu-cho-duyet-tap-trung` · worktree
   `websites/wt-phieu-cho-duyet/` · migration nào chạy vào DB nào).

### Ghi chú kỹ thuật đã soát cho plan (chưa có trong spec)

- **Công ty đang làm khác nhau 2 bên**: HRM = `auth()->user()->current_company_role` (`PermissionService`), ERP =
  `auth()->user()->info->company_id`.
- **Laravel 6 (ERP, PHP 7.4) vs Laravel 8 (HRM)**: không có `DB::afterCommit` ở L6 ⇒ tự viết hàng đợi chạy sau commit
  (nghe `TransactionCommitted`/`TransactionRolledBack`, flush khi `transactionLevel()==0`). Code chung phải chạy PHP 7.4.
- **Dùng chung code y hệt 2 repo**: cả 2 namespace gốc `App\` ⇒ lõi + định nghĩa luồng đặt ở `app/Services/ApprovalInbox/`
  giống từng byte, chỉ dùng `DB::table` (không Eloquent) — test so khớp = so hash file. Phần riêng mỗi bên: lấy
  employee/công ty, gắn trait vào model, controller/màn.
- **Định nghĩa luồng bằng closure SQL** (không để trong config vì config:cache không chứa closure): mỗi cấp = điều kiện
  `when(Builder)`; `currentLevel(id)` = cấp đầu tiên khớp; backfill liệt kê bằng chính các điều kiện đó.
- **Gate phức tạp → bảng `approval_inbox_assignees`** (inbox_id, employee_id) cho approver/người lập gốc/NV mua hàng phân
  công; cột `gate_type`, `required_permission`, `required_guard`, `scope`, `required_role`, `gate_department_id`,
  `gate_ref_id` (phòng họp / kho) thay cho `gate_params` JSON. Cron 30' **sync lại toàn bộ phiếu chờ** (không chỉ prune)
  để cập nhật người duyệt khi phân công đổi. ⇒ cập nhật design.md §2.1 khi viết plan.
- **Bộ giải quyền**: quyền = `employee_has_roles` (mọi model_type) ⋈ `role_has_permissions.company_id = công ty đang làm`
  + `employee_has_permissions` (đang rỗng); phòng/bộ phận quản lý theo `manageDepartmentIdsOf`/`managePartIdsOf`
  (`app/Helper/PermissionHelper.php`, có cờ `all_department`); phòng họp `meeting_room_managers.meeting_room_id`;
  thủ kho `warehouse_stockers.stocker_id`. MySQL 8.0.43.
- **Gate HRM ⚠ (flows §7)** sửa sang hàm kiểm quyền SQL có công ty (không dùng CEP vì CEP bỏ qua công ty, không dùng
  `PermissionService` vì `$employee->roles` lọc model_type).
- **ERP**: không cherry-pick nguyên `6134e90`/`46ab7152` (66 file hook controller sẽ bị thay bằng model event); chỉ lấy
  view `approval_inbox/index.blade.php`, `ApprovalInboxExcel`, phần list của `ApprovalInboxController` làm gốc. Đường
  dẫn ERP trong định nghĩa phải là path literal (HRM không gọi được `route()` của ERP) — tra `route:list --name=`.
- **HRM màn**: khuôn `pages/finance/bill-payment-requests/index.vue` (V2BaseSmartFilterPanel + V2BaseDataTable,
  `apiGetMethod`, ép Number phân trang); layout mặc định `default` (Topbar, không sidebar) = trang rộng; link ERP qua
  `utils/erp-link.js` `erpUrl()`. Route API đặt ở `routes/api.php` nhóm `v1` + `auth:api`, kiểm quyền xem trong controller
  (middleware `checkPermission` dính khe model_type).
- Test: HRM `tests/Feature` (DatabaseTransactions, chạy trên DB .env — để lại rác, xem memory phpunit); ERP có `tests/Feature`.
