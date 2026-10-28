# Lỗi mở 15/10 — Đợt bổ sung (c) ERP: N120 · N121 — Report

Ngày 15/10/2026. Worktree `wt-erp-2d1`. Nhánh con `feat/cdhh-loi-mo-2-erp` (từ `feat/2d1-erp-khong-loi` @ `f19ef0abca`),
merge `--no-ff` LOCAL về `feat/2d1-erp-khong-loi` = **`7bfe798a9f`**. KHÔNG push. Soát marker xung đột: 0. EOL giữ nguyên (cả 4 file LF, `--numstat` không xoá dòng thừa).

## Commit

| Commit | Mã | Nội dung |
|---|---|---|
| `f1d7a6d035` | N120 | `InlandOrderRequestNewController::searchData` bỏ mục Sửa/Xóa (giữ In; mã phiếu vẫn là link Xem). `inland_order_request_new/show.blade.php`: bọc comment blade popup "Chọn luồng" (nút Duyệt) + 4 hàm `submit` / `updateApproverComment` / `submitDepartment` / `submitCancel` (gọi route approve/departmentApprove/updateApproverComment/cancel — method không tồn tại). `approver_index.blade.php`: comment N97 "(N112)" → "(N120)" |
| `24728cf0ce` | N121 | `customercare/customermanager/show_.blade.php`: vòng `.date-model` lúc tải trang dừng khi đối tượng giữa đường rỗng (`&& object` + `if (!object) return;`) |
| `4f0fd73f00` | test | `tests/Feature/LoiMo1510ErpTest.php` thêm 3 ca |
| `7bfe798a9f` | merge | Merge về nhánh chung |

Ghi chú N120 màn chi tiết: thực tế trang chi tiết KHÔNG có nút Duyệt/Huỷ/Lưu ý kiến hiển thị (report đợt 3 ghi số dòng 253/281/302/342 là các URL route trong JS). Thứ còn "sống" là popup chọn luồng có nút Duyệt + Hủy (ẩn, mở qua `submit`) và 4 hàm JS trỏ route chết ⇒ đã ẩn hết. Chi tiết không có nút In riêng — In nằm ở dropdown danh sách (giữ nguyên).

## Kiểm

- Lint blade (compileString + `php -l`): 3 blade sửa "No syntax errors"; bản compile `show` còn 0 lần `setNotificationModal` / `inlandOrderRequestNew.approve` / `departmentApprove` / `updateApproverComment` / `inlandOrderRequestNew.cancel` / `submitCancel`. `php -l` controller sạch.
- PHPUnit ERP cả bộ: **194 tests, 4351 assertions, 4 skipped, xanh** (mốc 191 + 3 ca mới). 3 ca mới đã xác nhận ĐỎ trên code gốc (tạm chép bản HEAD vào file rồi trả lại):
  - `test_n120_man_tn_moi_chi_dan_route_co_method` — mọi route `inlandOrderRequestNew.*` mà controller + 4 view TN mới còn dẫn tới phải trỏ method có thật; còn show/print/searchData.
  - `test_n120_chi_tiet_tn_moi_khong_con_thao_tac`
  - `test_n121_vong_date_model_bo_qua_doi_tuong_chua_co`
- Playwright (ERP `artisan serve --port=8090` từ worktree, trước đó không có `bootstrap/cache/config.php` + `config:clear`; PID 17213/17221 — đã kill đúng PID). Đăng nhập `e2e_assign@test.local`. Cùng script chạy 2 lượt trước/sau: `scratchpad/loimo-erp/check2.js` → `before2.json` / `after2.json`.

Danh sách TN mới luôn rỗng (xem N126) ⇒ để đo DOM thật, script chặn request `searchData`, bỏ tham số `type` và lọc đúng mã phiếu tạm PDHTN-04990.

| Ca | Trước sửa | Sau sửa |
|---|---|---|
| Danh sách `/inland_order_request_new` — mục Sửa · Xóa · In · link Xem trong bảng | 1 · 1 · 1 · 2 | **0 · 0** · 1 · 2 |
| `/forApprover` — như trên | 1 · 1 · 1 · 1 | **0 · 0** · 1 · 1 |
| `/forDepartmentApprover` — như trên | 1 · 1 · 1 · 1 | **0 · 0** · 1 · 1 |
| Link `…/edit`, `…/delete` trên trang (cả 3 màn) | 2 | **0** |
| `searchData?code=PDHTN-04990` (JSON, cột action) — Sửa · Xóa · In | 1 · 1 · 1 | 0 · 0 · 1 |
| Chi tiết `/4990/show` — phần tử Duyệt/Hủy/Huỷ/Lưu ý kiến/Sửa/Xóa trong DOM (kể cả ẩn) | 2 ("Duyệt", "Hủy" trong popup) | **0** |
| Chi tiết — `ng-click="submit…"` · popup `#setNotificationModal` · hàm scope submit/submitDepartment/submitCancel · URL route chết trong HTML | 1 · có · 3 · 4 | **0 · không · 0 · 0** |
| Chi tiết — trang 200, 5 dòng hàng, mã PDHTN-04990 | có | có (vẫn xem được) |
| In `/4990/print` | HTTP 200 | HTTP 200 |
| KH 1000 (loại 2) — pageerror | `Cannot read properties of undefined (reading 'date_of_birth')` | **0** |
| KH 1000 — mở tab "Thông tin liên hệ" → bấm "Thêm mới" (KHÔNG lưu) → bấm ô Sinh nhật → chọn ngày 15 trên datepicker thật | ô hiện `15/10/2026`, `contactToAdd.date_of_birth = 2026-10-15` | y nguyên: `15/10/2026` / `2026-10-15`, 0 lỗi |
| KH 232387 (loại 1) | 0 lỗi JS; `customer.date_of_birth` hiện `19/09/2025` | 0 lỗi JS; y nguyên |

Lỗi console "Failed to load resource" 404/405 còn lại ở mọi trang (trước và sau) là ảnh tĩnh môi trường local (logo `/uploads/…jpg`, avatar e2e) — như đợt 3, ngoài phạm vi.

## Dữ liệu thử / quyền tạm (đã dọn)

- Role tạm `TMP_E2E_LOIMO_1510_BOSUNG` id **122366** trên `hrm_erp_giacty`: `role_has_permissions` (100057 "Xem khách hàng", 100387 "Tổng hợp đặt hàng trong nước"; company_id=1) + `employee_has_roles` (employee 1180, model_type `App\Employee`, company_id=1).
- Fixture TN mới: phiếu **4990** tạm đổi `status 1→3`, `created_by 68→1180` (để `canEdit()` true ⇒ có mục Sửa/Xóa khi đo; DB không có phiếu status 3 nào). Đổi bằng `DB::table` nên `updated_at` không đổi.
- Làm mới quyền: chỉ `Cache::forget('spatie.permission.cache')` (KHÔNG chạy `cache:clear`).
- Đã dọn: xoá đúng id 122366 (roles 0, rp 0, ehr 0); 1180 còn đúng role 118805; `can('Xem khách hàng')` = false; phiếu 4990 trả `status=1, created_by=68`; phân bố status bảng = 4953 (1) + 37 (0) như trước.
- Không lưu phiếu / KH / người liên hệ nào.

## Lỗi mới ngoài phạm vi (không vá)

- **N126** — Cả 3 màn danh sách TN mới (`index`, `forApprover`, `forDepartmentApprover`) LUÔN rỗng: view gửi `d.type = 'index' | 'approve' | 'department_approve'`, `searchByFilter` lọc `where('type', $request->type)` trên cột int `type` (giá trị thật 1/2) ⇒ MySQL ép chuỗi thành 0 ⇒ 0 dòng. Đo: màn index không chặn request hiện "Không có dữ liệu". Hệ quả: link Xem / mục In ở danh sách thực tế không tới được qua UI (chỉ vào chi tiết qua URL/thông báo). Cỡ S nhưng cần chốt nghiệp vụ: `type` này nghĩa là gì ở TN mới (bỏ lọc, hay map index/approve/department_approve sang điều kiện người tạo/người duyệt như màn TN 2).
- **N127** — Chi tiết TN mới không có nút In (In chỉ ở dropdown danh sách, mà danh sách đang rỗng — N126). Nếu muốn "chỉ xem + in" đúng nghĩa trên trang chi tiết, thêm nút In trỏ `inlandOrderRequestNew.print` (đang HTTP 200). Cỡ S, cần user chốt.
- Ghi chú nhỏ: `$scope.notifications` ở `show.blade.php` giờ không còn dùng (giữ lại cho lúc mở lại luồng duyệt).
