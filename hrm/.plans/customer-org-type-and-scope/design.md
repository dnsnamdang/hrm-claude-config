# Design — Loại hình tổ chức & Lĩnh vực khách hàng (HRM)

> Ngày: 2026-06-09 · Hệ thống: **HRM** (làm trước) · ERP có spec riêng (làm sau).

## 1. Mục tiêu

Bổ sung/điều chỉnh các trường trên danh mục Khách hàng (`/human/customers/add`, `/human/customers/:id/edit`, và tìm kiếm):

1. Đổi nhãn trường **"Đối tượng" → "Loại hình tổ chức"**, mở rộng từ 2 lên 5 loại.
2. Thêm 2 trường bắt buộc: **"Nhóm lĩnh vực khách hàng"** và **"Lĩnh vực khách hàng"** (searchable dropdown, đồng bộ 2 chiều).
3. **Bỏ "Nhóm khách hàng"** khỏi form + tìm kiếm (chỉ ẩn, giữ nguyên dữ liệu/báo cáo).

## 2. Hiện trạng (đã khảo sát)

- **Catalog đã tồn tại** ở `Modules/Assign`: bảng `customer_scopes`, `customer_scope_groups`, pivot `customer_scope_group_members`; entity `CustomerScope`, `CustomerScopeGroup`; màn `/assign/customer-scopes`, `/assign/customer-scope-groups`. → **Không xây lại catalog.**
- Quan hệ `CustomerScope` ↔ `CustomerScopeGroup` là **nhiều-nhiều** (1 lĩnh vực có thể thuộc nhiều nhóm — đã xác nhận qua seeder, vd "Bệnh viện" thuộc 2 nhóm).
- API list đã có: `GET /assign/customer-scopes`, `GET /assign/customer-scope-groups`.
- `CustomerForm.vue` (`components/human-components/customer/CustomerForm.vue`): `form.customer_type` options `1 Cá nhân` / `2 Tổ chức`; nhiều section điều kiện `v-if="customer_type == 1"` (Cá nhân) và `v-if="customer_type == 2"` (Tổ chức).
- Bảng `customers` (Modules/Human) **chưa có** cột scope/group.
- Form HRM hiện **chưa có** field "Nhóm khách hàng" (field này tồn tại bên ERP). Sẽ rà ở màn danh sách/tìm kiếm và bỏ nếu có.

## 3. Quyết định chốt

| #   | Vấn đề                                               | Quyết định                                                                                               |
| --- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1   | Phạm vi                                              | HRM trước; ERP spec riêng (ERP đọc catalog từ HRM qua remote DB).                                        |
| 2   | Bỏ "Nhóm khách hàng"                                 | Chỉ ẩn khỏi form + tìm kiếm; giữ nguyên cột/dữ liệu/báo cáo.                                             |
| 3   | Bắt buộc 2 trường mới                                | `required` chỉ ở tầng validate khi tạo/sửa; cột DB `nullable`; **không backfill** khách cũ.              |
| 4   | `customer_type`                                      | Giữ kiểu int; `2 Tổ chức` đổi tên thành `2 Doanh nghiệp tư nhân` (**giữ nguyên value=2**); thêm `3,4,5`. |
| 5   | Lưu trữ scope                                        | Lưu **cả hai** `customer_scope_group_id` + `customer_scope_id` trên `customers` (Hướng A).               |
| 6   | Auto-fill nhóm khi chọn lĩnh vực (Bottom-Up) đa nhóm | 1 nhóm → auto-fill; nhiều nhóm → lọc ô Nhóm còn các nhóm hợp lệ, để trống, bắt người dùng chọn.          |
| 7   | Filter danh sách theo Nhóm lĩnh vực/Lĩnh vực         | Chờ xác nhận (mặc định **không thêm** ở phase này).                                                      |

## 4. Loại hình tổ chức (mapping `customer_type`)

| value | Nhãn                                          | Layout form                |
| ----- | --------------------------------------------- | -------------------------- |
| 1     | Cá nhân                                       | Form Cá nhân (giữ nguyên)  |
| 2     | Doanh nghiệp tư nhân _(đổi tên từ 'Tổ chức')_ | Form tổ chức               |
| 3     | Doanh nghiệp nước ngoài                       | Giống Doanh nghiệp tư nhân |
| 4     | Tổ chức phi chính phủ                         | Giống Doanh nghiệp tư nhân |
| 5     | Cơ quan nhà nước                              | Giống Doanh nghiệp tư nhân |

→ FE: thay mọi điều kiện `customer_type == 2` bằng computed **`isOrganization`** = `[2,3,4,5].includes(customer_type)`. Điều kiện `customer_type == 1` (Cá nhân) giữ nguyên.

## 5. Backend — Modules/Human

- **Migration** thêm vào `customers`:
  - `customer_scope_group_id` `unsignedBigInteger nullable` (FK `customer_scope_groups`).
  - `customer_scope_id` `unsignedBigInteger nullable` (FK `customer_scopes`).
- **Entity `Customer`**: thêm 2 cột vào `$fillable`; quan hệ `belongsTo` `scopeGroup` (CustomerScopeGroup), `scope` (CustomerScope).
- **Request** (Create/Update/SaveCustomerRequest):
  - `customer_type` → `required|in:1,2,3,4,5`.
  - `customer_scope_group_id` → `required|exists:customer_scope_groups,id`.
  - `customer_scope_id` → `required|exists:customer_scopes,id` + **rule kiểm tra lĩnh vực thuộc nhóm** (tồn tại bản ghi trong `customer_scope_group_members` với `customer_scope_id` + `customer_scope_group_id` tương ứng).
  - Rethrow `ValidationException` (không catch chung `Exception`) — theo CLAUDE.md.
- **Service** store/update: lưu 2 trường mới.
- **Resource** (`CustomerDetailResource`, `CustomerListResource`): trả `scope_group {id,name}` + `scope {id,name}` để hiển thị và đổ lại khi sửa.

## 6. Backend — Modules/Assign (API cấp dropdown)

- `GET /assign/customer-scopes`: bổ sung filter tham số **`customer_scope_group_id`** → trả các lĩnh vực thuộc nhóm (phục vụ Top-Down). Không truyền → trả tất cả.
- `CustomerScopeResource`: include mảng **`groups [{id,name}]`** của mỗi lĩnh vực → phục vụ Bottom-Up auto-fill.
- `GET /assign/customer-scope-groups`: đã có, cấp danh sách nhóm.
- Quyền: dropdown chỉ yêu cầu đăng nhập (mọi user được tạo/sửa KH đều đọc được danh mục).

## 7. Frontend — Form khách hàng

### 7.1 CustomerForm.vue

- Đổi nhãn **"Đối tượng" → "Loại hình tổ chức"**; options theo bảng mục 4.
- Thêm computed `isOrganization`; thay các `v-if="customer_type == 2"` thành `v-if="isOrganization"`.
- Bỏ "Nhóm khách hàng" khỏi form (nếu tồn tại) — HRM hiện chưa có, chủ yếu rà tìm kiếm/danh sách.
- Nhúng component `CustomerScopeSelect` (mục 7.2), v-model 2 trường `customer_scope_group_id` + `customer_scope_id`.

### 7.2 Component dùng chung `CustomerScopeSelect.vue`

- 2 ô **searchable dropdown** (vue-multiselect): "Nhóm lĩnh vực khách hàng" (_) và "Lĩnh vực khách hàng" (_).
- **Top-Down** (đổi Nhóm): gọi `GET /assign/customer-scopes?customer_scope_group_id=<id>` để nạp lại danh sách Lĩnh vực; nếu Lĩnh vực đang chọn không còn hợp lệ → reset.
- **Bottom-Up** (chọn Lĩnh vực): đọc `groups` của lĩnh vực:
  - 1 nhóm → auto-fill Nhóm.
  - nhiều nhóm → lọc danh sách Nhóm chỉ còn các nhóm hợp lệ, để trống, bắt người dùng chọn 1.
- **Khi edit:** nạp sẵn cả Nhóm + Lĩnh vực từ resource; danh sách Lĩnh vực filter theo Nhóm đã lưu.
- **Validate inline:** viền đỏ `is-invalid` + text `invalid-feedback`; flag `touched` chỉ hiện lỗi sau lần submit đầu (theo CLAUDE.md).
- Thiết kế tách biệt để tái dùng (prospective-projects/ERP sau này).

## 8. Frontend — Danh sách & tìm kiếm khách hàng

- Đổi nhãn filter "Đối tượng" → "Loại hình tổ chức" (5 loại).
- Bỏ filter "Nhóm khách hàng" nếu có.
- _(Chờ xác nhận)_ thêm filter Nhóm lĩnh vực / Lĩnh vực — mặc định không thêm ở phase này.

## 9. Ngoài phạm vi (YAGNI)

- Không sửa CRUD catalog (đã có ở Assign).
- Không backfill/di trú dữ liệu khách cũ.
- Không đụng ERP (spec riêng).
- Không xóa cột/dữ liệu "Nhóm khách hàng".

## 10. Edge cases

- Khách cũ chưa có scope/group: form sửa **bắt** chọn trước khi lưu; bản ghi cũ không bị ép backfill.
- Chọn Lĩnh vực rồi đổi Nhóm sang nhóm không chứa lĩnh vực đó → reset Lĩnh vực.
- Lĩnh vực bị khóa (status inactive) → không hiển thị trong dropdown tạo mới; khi edit bản ghi đang trỏ tới lĩnh vực inactive → vẫn hiển thị giá trị cũ (read-only hint) nhưng yêu cầu chọn lại nếu đổi.
- Submit khi thiếu Nhóm/Lĩnh vực → BE trả `ValidationException`, FE hiện lỗi inline tại từng input.
