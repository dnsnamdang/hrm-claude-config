# Plan — Nhóm khách hàng trên form KH

Nhánh `gop_db` · @khoipv · Spec: `docs/superpowers/specs/gop-db/2026-08-10-customer-form-group-design.md`

## Phase 1 — Khảo sát

- [x] Đọc field Nhóm KH bên ERP (`partials/customers/customerForm.blade.php:107-130`) → multi-select, không bắt buộc
- [x] Rà hiện trạng HRM: pivot `customer_has_groups`, API `customer-groups`, `syncGroups()`, `show()->group_ids` đều ĐÃ CÓ — chỉ thiếu field trên form
- [x] Phát hiện lỗi có sẵn: form không gửi `groups` mà `syncGroups()` chạy vô điều kiện → mỗi lần sửa KH là xoá sạch nhóm

## Phase 2 — Code

- [x] FE `CustomerForm.vue`: khối "Nhóm khách hàng" (`V2BaseSelectInModal`, multiple, không bắt buộc, `:disabled="readonly"`)
- [x] FE: `form.groups` + `listCustomerGroups` + `loadCustomerGroups()` + thêm vào `Promise.all` của `mounted()`
- [x] FE: `loadCustomer()` map `data.group_ids` → `form.groups`
- [x] FE: `buildPayload()` LUÔN gửi `groups` (chống xoá mất nhóm khi sửa)
- [x] BE: `SaveCustomerRequest` + `UpdateCustomerRequest` thêm `groups` nullable array + `exists:customer_groups,id`

## Phase 3 — Verify

- [x] `php -l` 2 request · SFC parse + template compile `CustomerForm.vue` — PASS
- [x] `GET assign/customers/customer-groups` → 378 nhóm
- [x] Tạo KH `groups=[1,4]` → pivot `[1,4]`, `show()->group_ids=[1,4]`, Resource trả `[1,4]`
- [x] Sửa `groups=[4]` → pivot `[4]`; sửa `groups=[]` → pivot rỗng
- [x] Tái hiện lỗi cũ: lưu không gửi key `groups` → pivot bị xoá sạch
- [x] Rollback sạch, không để lại KH test
- [x] Rà 5 màn dùng chung `CustomerForm.vue` — field hiện nhất quán, màn xem chi tiết ở chế độ readonly
- [ ] User test trình duyệt: `/assign/customers/add` chọn nhóm → lưu → mở lại màn sửa thấy đúng nhóm

## Phase 4 — Cột "Nhóm KH" trên màn danh sách

- [x] Tìm nguyên nhân cột trống: `CustomerListResource` hardcode `'group_names' => '—'` (placeholder do việc `customer-column-config` để lại)
- [x] Tách subquery `groupNamesSql()` trong `CustomerService` (song song `vehicleManufactNamesSql()`)
- [x] `index()`: `selectRaw(groupNamesSql())` **không gate** sau `with_extra_columns` — cột này hiện mặc định
- [x] `exportQuery()`: dùng lại helper thay cho SQL viết tay (phải khai lại vì `select()` đã thay sạch select list của `index()`)
- [x] `CustomerListResource`: trả `group_names` thật, `null` khi không có nhóm (FE tự hiện `—`)
- [x] Verify: KH #42151 ghép đúng 7 nhóm khớp DB · KH không nhóm → `null` · COUNT phân trang 17.544 KH vẫn 308 ms (subquery nằm ở SELECT, không đụng COUNT) · lấy 20 dòng 9 ms · `exportQuery()` chạy, không trùng alias

---

### Checkpoint — 2026-08-10
Vừa hoàn thành: thêm trường **Nhóm khách hàng** (chọn nhiều, không bắt buộc) vào form KH, giống ERP.
Chỉ phải sửa FE + 2 dòng validate — pivot, API danh mục, hàm sync và resource đọc đều đã có sẵn.
Kèm theo sửa một lỗi mất dữ liệu có sẵn: form không gửi `groups` trong khi `syncGroups()` xoá-rồi-ghi
vô điều kiện, nên mỗi lần sửa KH trên HRM là xoá sạch nhóm KH do ERP gán.
Đang làm dở: (không)
Bước tiếp theo: user build FE + test trình duyệt.
Blocked: (không)

### Checkpoint — 2026-08-10 (cột Nhóm KH màn danh sách)
Vừa hoàn thành: user hỏi sao màn `/assign/customers` không có dữ liệu nhóm khách hàng — đúng, cột
"Nhóm KH" đang hardcode `'—'` trong `CustomerListResource` từ việc `customer-column-config`.
Đã nối dữ liệu thật bằng subquery tương quan `group_concat` (không nhân dòng, không đụng COUNT).
Verify: khớp DB 100%, COUNT 17.544 KH vẫn 308 ms, 20 dòng 9 ms, export không trùng alias.
Bước tiếp theo: user build FE + test trình duyệt.

### Checkpoint — 2026-08-11 (HOÀN THÀNH)
Vừa hoàn thành: user test trình duyệt xong (trường Nhóm KH trên 5 màn dùng `CustomerForm.vue` +
cột "Nhóm KH" màn danh sách) → **feature HOÀN THÀNH**.
Đang làm dở: không có.
Bước tiếp theo: không có (đã chuyển sang mục "Hoàn thành" ở `.plans/gop-db/STATUS.md`).
Blocked: không có.
