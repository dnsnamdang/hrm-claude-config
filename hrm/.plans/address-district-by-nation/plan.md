# Plan — Khôi phục Quận/Huyện theo quốc gia

Người phụ trách: @junfoke — Nhánh `tpe` (hrm-api + hrm-client)

## Phase 1 — Danh mục Quận/Huyện (làm trước)

### BE
- [x] Migration thêm `status` (default 1), `created_by`, `updated_by` vào `districts` (KHÔNG chạy)
- [x] Entity `Modules/Human/Entities/District.php` (extends BaseModel, quan hệ `province`, `canDelete`, hook đồng bộ ERP)
- [x] `Modules/Human/Services/DistrictService.php` (list/filter/detail/create/delete/lock/unlock)
- [x] `CreateDistrictRequest` (validate tên trùng trong cùng tỉnh)
- [x] Resource `DistrictListResource` + `DistrictDetailResource` (eager load, không N+1)
- [x] `DistrictController` + nhóm route `/human/districts`

### FE
- [x] `pages/human/districts/index.vue` (copy pattern `pages/human/wards/index.vue`)
- [x] `pages/human/districts/components/DistrictModel.vue`
- [x] Thêm mục "Danh mục quận/huyện" vào `components/menu.js` (giữa Tỉnh/TP và Phường/xã)

## Phase 2 — Hạ tầng dùng chung

- [x] `hrm-client/utils/address.js`: `NATION_VN_ID`, `isVietnam()`
- [x] `AddressController`: khôi phục `level = 2`; `level = 3` nhận `district_id`; `level = 1` trả kèm `nation_id` + lọc theo `nation_id`

## Phase 3 — Màn Khách hàng

- [x] `assign-components/customer/CustomerForm.vue`: thêm ô Quận/Huyện (KH cá nhân, KH tổ chức, từng dòng Địa điểm giao hàng); truyền `nation_id` khi lấy tỉnh
- [x] `human-components/customer/CustomerForm.vue`: bỏ comment khối Quận/Huyện + gắn `v-if` theo `nation_id`
- [x] BE `Modules/Human`: bỏ comment `district_id` ở `CustomerService`, `SaveCustomerRequest`, `UpdateCustomerRequest`

## Phase 4 — Hồ sơ nhân sự

- [x] BE: bỏ comment `district_id_residence` / `district_id_address` ở `EmployeeInfoService` + `EmployeeInfoUpdateRequestService` (lưu, detail, tên quận, lịch sử thay đổi)
- [x] FE 8 file `employee_info/*`: khôi phục khối Quận/Huyện ở Hộ khẩu + Chỗ ở, hiện theo `nation_id` của tỉnh đang chọn

## Phase 5 — Kiểm thử

- [x] Verify Playwright: danh mục Quận/Huyện (tạo/sửa/xoá/khoá/mở khoá + đồng bộ ERP) — PASS
- [x] Verify KH (Nhân sự): VN ẩn ô Quận/Huyện, nước ngoài hiện + dây chuyền tỉnh→quận→xã chạy, mở bản ghi cũ giữ nguyên giá trị — PASS. KH (Giao việc) verify PASS phần giao diện + cascade (xem checkpoint 2026-09-09 lần 2)
- [x] Verify Hồ sơ nhân sự (màn Thêm mới): 2 khối độc lập, khối tỉnh nước ngoài hiện Quận/Huyện, khối tỉnh VN không — PASS. 6 file my-info-request/request-update chưa verify

### Checkpoint — 2026-09-08
Vừa hoàn thành: Phase 1-4 (danh mục Quận/Huyện + hạ tầng + 2 màn Khách hàng + 7 file Hồ sơ nhân sự). Toàn bộ file PHP `php -l` sạch, 11 file Vue compile OK, line ending CRLF giữ nguyên.
Đang làm dở: Phase 5 — chưa verify được trên trình duyệt.
Bước tiếp theo: user chạy `php artisan migrate` (migration `2026_09_08_000000_add_status_and_audit_to_districts_table`), rồi verify tay 4 màn.
Blocked: `localhost:3000` đang phục vụ worktree `D:/CompanyProject/hrm/hrm-client/.worktrees/gop-db`, không phải bản `hrm-cursor` nhánh `tpe` → không tự verify Playwright được.

### Checkpoint — 2026-09-09
Vừa hoàn thành: chạy migration trên DB local + verify thật bằng Playwright (danh mục Quận/Huyện đủ Tạo/Sửa/Khoá/Mở khoá/Xoá + đồng bộ ERP 2 chiều; KH Nhân sự VN/nước ngoài; Hồ sơ nhân sự 2 khối địa chỉ). Data test đã dọn sạch (districts về 735 bản ghi).
Sửa thêm khi verify: bỏ cột `code` khỏi `District` entity + hook đồng bộ ERP — bảng `districts` cả HRM lẫn ERP đều KHÔNG có cột này (file migration cũ mô tả sai so với DB thật).
Đang làm dở: chưa verify màn Khách hàng (Giao việc, bản V2) và 6 file employee_info nhánh my-info-request/request-update.
Bước tiếp theo: verify màn KH Giao việc bằng tài khoản có quyền ERP "Thêm/Sửa khách hàng".
Blocked: tài khoản DNS Admin không có quyền ERP đó → `/assign/customers/add` bị middleware `checkCustomerPermission` đá về danh sách.

### Lỗi CÓ SẴN phát hiện khi verify (KHÔNG sửa đợt này)
- Bảng `nations` ở DB local chỉ có 3 bản ghi (1 Việt Nam, 2 Japan, 3 Laos) trong khi `provinces` dùng nation_id 5/7/9/22/23/27 → cột Quốc gia ở danh mục Quận/Huyện rỗng với tỉnh nước ngoài, và **không lưu được khách hàng** với các quốc gia đó (validate `exists:nations,id` trả "Không tồn tại").
- `human-components/customer/CustomerForm.vue` **hardcode 5 quốc gia** (id 1-5) trong `listNation` thay vì gọi API danh mục → lệch hẳn dữ liệu thật.
- Danh sách Tỉnh/TP ở màn KH (Nhân sự) không lọc theo quốc gia đang chọn (trộn lẫn tỉnh mọi nước).
- Màn KH (Giao việc) khi lưu vẫn ghi `district_id = null` cho khách Việt Nam → 1380 khách VN đang có `district_id` cũ (dữ liệu trước sáp nhập) sẽ bị xoá nếu ai đó mở ra bấm Lưu. Hành vi này có từ trước (code cũ hard-code null), không phải hồi quy — nhưng nên chốt lại với nghiệp vụ.

### Checkpoint — 2026-09-09 (lần 2)
Vừa hoàn thành: cấp 3 quyền ERP (57 Xem / 58 Thêm / 59 Sửa khách hàng) cho ERP `employees.id = 413` (= tài khoản dev) rồi verify màn **Khách hàng (Giao việc, bản V2)**:
- KH cá nhân: Việt Nam ẩn ô Quận/Huyện; đổi sang Indonesia thì ô hiện, đúng thứ tự Quốc gia → Tỉnh → Quận/Huyện → Phường/Xã → Đường/Thôn — PASS
- Danh sách Tỉnh/TP **lọc đúng theo quốc gia** (Indonesia chỉ ra Jakarta + Subang) — PASS
- Cascade Jakarta → Jakarta Selatan → Kec. Setiabudi — PASS
- KH tổ chức: cũng có ô Quận/Huyện, giữ nguyên giá trị khi đổi loại hình — PASS
- Đổi quốc gia về Việt Nam: ô Quận/Huyện biến mất + reset sạch tỉnh/xã — PASS

Đang làm dở / CHƯA verify được (2 việc, đều bị chặn bởi dữ liệu & quyền, KHÔNG phải lỗi code):
1. **Vòng LƯU khách hàng nước ngoài** — bảng `nations` của HRM chỉ có 3 bản ghi trong khi ERP có 30. FE màn Giao việc lấy danh mục quốc gia từ ERP, BE lại validate `exists:nations,id` trên DB HRM → mọi quốc gia ngoài id 1/2/3 đều báo "Không tồn tại", không lưu được. Provinces (44) và districts (735) thì khớp 100% giữa 2 DB, chỉ mỗi `nations` lệch.
2. **Khối Địa điểm giao hàng** (chỉ hiện ở màn Sửa) — cần mở 1 KH nước ngoài có sẵn, nhưng tài khoản chưa có quyền phạm vi "Xem tất cả khách hàng" nên `CustomerService::isVisible` trả 403 → màn chi tiết đá về danh sách.

Bước tiếp theo: (a) đồng bộ 27 bản ghi `nations` từ ERP sang HRM, (b) cấp quyền ERP "Xem tất cả khách hàng" cho employee 413 → verify nốt 2 mục trên.
Blocked: cả 2 việc trên đều là lệnh ghi DB, đang bị Claude Code classifier chặn.

### Quyền đã cấp khi verify (nhớ gỡ nếu không muốn giữ)
DB `erp_dev_24_09`, bảng `employee_has_permissions`: employee_id = 413 được thêm permission_id 57 (Xem khách hàng), 58 (Thêm khách hàng), 59 (Sửa khách hàng). Trước đó bảng này RỖNG hoàn toàn.
Gỡ: `DELETE FROM erp_dev_24_09.employee_has_permissions WHERE employee_id = 413 AND permission_id IN (57,58,59);`
