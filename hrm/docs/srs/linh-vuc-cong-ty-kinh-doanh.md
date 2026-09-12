# SRS: Danh mục Lĩnh vực Công ty kinh doanh

| Thông tin | Chi tiết |
|-----------|----------|
| Module | Assign (Dự án & Giao việc) |
| Phiên bản | 1.2 |
| Ngày tạo | 2026-08-22 |
| Cập nhật | 2026-08-27 (đổi tên hiển thị + tên quyền) |
| Người tạo | @dnsnamdang |
| Trạng thái | Implemented — chờ nghiệm thu |
| Route FE | `/assign/internal-business-scopes` |
| Bảng DB | `internal_business_scopes` |
| Nhánh | `linh-vuc-noi-bo` (đã gộp vào `tpe`) |

> **Lưu ý về tên gọi.** Danh mục ban đầu tên là *"Lĩnh vực kinh doanh nội bộ"*, đổi tên hiển thị
> thành **"Lĩnh vực Công ty kinh doanh"** ngày 27/08/2026. Các định danh kỹ thuật **giữ nguyên**
> tên cũ: URL `internal-business-scopes`, bảng `internal_business_scopes`, cột
> `internal_business_scope_id`, tiền tố mã `LVKDNB.`, tên file mẫu import
> `Mau_import_LinhVucKinhDoanhNoiBo.xlsx`.

---

## 1. Giới thiệu

### 1.1. Mục đích

Cung cấp danh mục **Lĩnh vực Công ty kinh doanh** — tập hợp các lĩnh vực kinh doanh mà công ty đang
hoạt động, dùng làm **cấp phân loại cha của Nhóm ngành** trong phân hệ Dự án & Giao việc.

Đặc điểm:
- Danh mục **dùng chung toàn công ty**, không phân theo công ty con / phòng ban / bộ phận
- Chỉ 2 trường nghiệp vụ: **Mã** + **Tên** (kèm Trạng thái). Không có Mô tả
- Mã theo định dạng cố định `LVKDNB.XXXX`, **không được trùng**; Tên cũng **không được trùng**
- Metadata (người/ngày tạo, người/ngày cập nhật) **hệ thống tự ghi**, không có ô nhập
- Phân quyền **phẳng 2 quyền**: Quản lý / Xem

### 1.2. Phạm vi

**Trong scope:**
- Màn danh sách 9 cột + bộ lọc nhanh & lọc nâng cao + phân trang + sắp xếp
- Modal Tạo mới / Sửa / Xem chi tiết
- Khoá / Mở khoá bản ghi; Xoá bản ghi
- Xuất Excel theo đúng bộ lọc đang áp
- Import Excel (tải file mẫu → nạp → validate → import)
- Liên kết 1-n xuống **Nhóm ngành** (`scopes.internal_business_scope_id`)
- Phân quyền 2 quyền phẳng, fail-closed ở FE, enforce 403 ở BE

**Ngoài scope:**
- Gắn trực tiếp vào Khách hàng / Dự án / Giải pháp (chỉ gắn gián tiếp qua Nhóm ngành)
- Lịch sử thay đổi bản ghi (`catalog_histories` — hạ tầng dùng chung chưa tồn tại ở nhánh này)
- Popup Cấu hình cột hiển thị, popup Chọn trường xuất file, `V2BaseSmartFilterPanel`, `V2BaseModal`
  (5 thành phần chuẩn `list-page` còn nợ — xem §12)
- Sinh file mẫu Import bằng endpoint API (hiện dùng file tĩnh)
- Phân quyền theo công ty con / phòng ban

### 1.3. Thuật ngữ

| Thuật ngữ | Giải thích |
|-----------|-----------|
| LVCTKD | Lĩnh vực Công ty kinh doanh — đối tượng của tài liệu này |
| LVKDNB | Tiền tố mã (`LVKDNB.`) — viết tắt tên cũ, **giữ nguyên** không đổi |
| Nhóm ngành | Bảng `scopes` — cấp phân loại con, mỗi Nhóm ngành **bắt buộc** thuộc 1 LVCTKD |
| Khoá (Lock) | Trạng thái = 2 — bản ghi bị đóng băng, chặn mọi đường ghi |
| Hậu tố mã | Phần sau `LVKDNB.` — 1–4 ký tự `[A-Za-z0-9_]` |
| Fail-closed | Cờ quyền FE mặc định `false`, chỉ bật khi quyền thật có trong store |
| Sắp theo độ khớp | Kết quả tìm kiếm xếp bản ghi khớp sát từ khoá lên trước (§5.4) |

---

## 2. Actors & Permissions

| Actor | Mô tả | Quyền |
|-------|-------|-------|
| Người quản lý danh mục | Admin / cán bộ phụ trách danh mục | `Quản lý danh mục lĩnh vực Công ty kinh doanh` |
| Người xem danh mục | Nhân viên cần tra cứu | `Xem danh mục lĩnh vực Công ty kinh doanh` |
| Người không có quyền | Nhân viên khác | Không thấy menu, mọi API trả 403 |

### 2.1. Bảng quyền chi tiết

| Chức năng | Quản lý | Xem | Không quyền |
|-----------|:-------:|:---:|:-----------:|
| Thấy mục menu "Lĩnh vực Công ty kinh doanh" | ✅ | ✅ | ❌ |
| Xem danh sách + lọc + sắp xếp + phân trang | ✅ | ✅ | ❌ 403 |
| Xem chi tiết (bấm vào Mã) | ✅ | ✅ | ❌ 403 |
| Xuất Excel | ✅ | ✅ | ❌ 403 |
| Nút "Tạo mới" | ✅ | ❌ ẩn | ❌ |
| Nút "Import Excel" | ✅ | ❌ ẩn | ❌ |
| Sửa | ✅ | ❌ ẩn | ❌ 403 |
| Khoá / Mở khoá | ✅ | ❌ ẩn | ❌ 403 |
| Xoá | ✅ | ❌ ẩn | ❌ 403 |

**Quy tắc:** nút không dùng được thì **ẩn hẳn**, không hiển thị dạng disable.
Cờ quyền FE `canManage` fail-closed — mặc định `false`, cấm gán literal `true`.

### 2.2. Định nghĩa quyền trong hệ thống

| id | name / display_name | group | type |
|----|---------------------|-------|------|
| 1177 | Quản lý danh mục lĩnh vực Công ty kinh doanh | Danh mục | 4 |
| 1178 | Xem danh mục lĩnh vực Công ty kinh doanh | Danh mục | 4 |

Khai báo tại `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:1053-1054`.

---

## 3. Use Cases

### UC-01: Xem danh sách Lĩnh vực Công ty kinh doanh

**Actor:** Người quản lý / Người xem
**Tiền điều kiện:** đăng nhập, có 1 trong 2 quyền

**Luồng chính:**
1. User vào menu **Danh mục › Lĩnh vực Công ty kinh doanh**
2. Hệ thống điều hướng tới `/assign/internal-business-scopes`
3. Bảng hiện spinner **ngay lập tức**, request danh sách bắn đầu tiên (không chờ request quyền)
4. Hệ thống gọi `GET /api/v1/assign/internal-business-scopes?page=1&per_page=10&sort_desc=true`
5. Bảng hiển thị 9 cột, mặc định sắp `id DESC` (bản ghi mới nhất lên đầu), 10 dòng/trang

**Luồng phụ:**
- 4a. Không có bản ghi nào khớp → hiện `Không có dữ liệu phù hợp bộ lọc.`
- 4b. Lỗi mạng / 500 → toast `Lỗi khi tải dữ liệu`, bảng rỗng
- 4c. 403 → **không** hiện toast (tránh nhiễu), bảng rỗng

---

### UC-02: Tìm kiếm & lọc

**Actor:** Người quản lý / Người xem

**Luồng chính:**
1. User gõ vào ô tìm nhanh (placeholder: *Tìm theo mã, tên lĩnh vực Công ty kinh doanh, người tạo*)
2. Bấm **Tìm kiếm** (hoặc Enter) → về trang 1, gọi lại API với `keyword`
3. BE tìm trên: `code` LIKE, `name` LIKE, **hoặc** tên người tạo (`employee_infos.fullname`) qua `EXISTS`
4. Kết quả sắp theo **độ khớp** (§5.4) khi từ khoá ≥ 2 ký tự và chưa bấm sort cột

**Luồng lọc nâng cao:**
1. User bấm mở panel lọc nâng cao (mặc định thu gọn)
2. Nhập/chọn 6 ô: Mã · Tên · Trạng thái · Người tạo · Người cập nhật · Cập nhật từ · Cập nhật đến
3. **Auto-search:** mọi ô nâng cao đổi giá trị là tự gọi API (deep watcher), reset về trang 1.
   Riêng ô tìm nhanh (`keyword`) **không** auto-search, phải bấm Tìm kiếm
4. Bấm **Làm mới** → xoá toàn bộ điều kiện, về trang 1, nạp lại danh sách đúng 1 lần

---

### UC-03: Tạo mới Lĩnh vực Công ty kinh doanh

**Actor:** Người quản lý
**Tiền điều kiện:** có quyền Quản lý

**Luồng chính:**
1. User bấm **Tạo mới** → mở modal *Tạo mới lĩnh vực Công ty kinh doanh*
2. Form 1 hàng 3 ô: **Mã** (3 cột) · **Tên** (6 cột) · **Trạng thái** (3 cột)
   - Ô Mã: tiền tố `LVKDNB.` cố định (không xoá được), user chỉ gõ hậu tố, `maxlength=4`
   - Trạng thái mặc định **Hoạt động**
3. User nhập Mã + Tên → bấm **Lưu**
4. FE chạy `validateAll()` — **mọi ô sai báo lỗi đồng thời**
5. Hợp lệ → `POST /api/v1/assign/internal-business-scopes`
6. BE chuẩn hoá (`strtoupper` + trim) → validate → ghi bản ghi, tự ghi `created_by`/`updated_by`
7. Toast `Thêm mới thành công`, đóng modal, nạp lại danh sách

**Luồng phụ:**
- 4a. Có lỗi FE → hiện `V2BaseError` dưới ô sai + viền đỏ `is-invalid`, **focus ô lỗi đầu tiên**
  (Mã → Tên), không gọi API
- 6a. Mã trùng → 422 `Mã lĩnh vực Công ty kinh doanh đã tồn tại`, modal **không đóng**
- 6b. Tên trùng → 422 `Tên lĩnh vực Công ty kinh doanh đã tồn tại`, modal **không đóng**
- 6c. Lỗi 422 hiện dưới đúng ô; user sửa lại ô nào thì lỗi BE của ô đó **tự biến mất**
- 3a. User bấm **Lưu & Tiếp tục** → lưu xong giữ modal mở, reset form để nhập bản ghi kế tiếp
  (nút này chỉ có ở chế độ Tạo mới)

---

### UC-04: Sửa Lĩnh vực Công ty kinh doanh

**Actor:** Người quản lý

**Luồng chính:**
1. User bấm biểu tượng **Sửa** trên dòng → FE gọi `GET /{id}` nạp dữ liệu mới nhất
2. Mở modal *Sửa lĩnh vực Công ty kinh doanh*, header hiện chip **người/ngày cập nhật gần nhất**,
   cuối body hiện block **Người tạo / Ngày tạo**
3. User sửa Mã và/hoặc Tên → **Lưu** → `PUT /{id}`
4. Toast `Cập nhật thành công`, đóng modal, nạp lại danh sách; cột Người/Ngày cập nhật đổi theo

**Luồng phụ:**
- 1a. Bản ghi đã bị người khác xoá → 404 `Dữ liệu đã thay đổi, vui lòng tải lại`, đóng modal
- 3a. Bản ghi đã bị người khác **khoá** → 423 `Bản ghi đang bị khoá, vui lòng mở khoá trước khi cập nhật.`
- Bản ghi đang Khoá thì **nút Sửa bị ẩn** ở danh sách (`is_can_edit = false`)
- Ô Trạng thái bị **disable** khi bản ghi đang ở trạng thái Khoá

---

### UC-05: Xem chi tiết

**Actor:** Người quản lý / Người xem

**Luồng chính:**
1. User bấm vào **Mã** ở cột thứ 2 (Mã là link, kiểu `v2-cell-link`)
2. FE gọi `GET /{id}` → mở modal *Xem chi tiết lĩnh vực Công ty kinh doanh*
3. Toàn bộ ô ở chế độ **chỉ đọc**; footer chỉ còn nút **Đóng**

> Màn danh mục **không có** nút "Xem" riêng ở cột Hành động — xem bằng cách bấm vào Mã.

---

### UC-06: Khoá / Mở khoá

**Actor:** Người quản lý

**Luồng Khoá:**
1. Dòng đang Hoạt động → bấm biểu tượng **Khoá**
2. Modal xác nhận: *Bạn có chắc muốn khoá lĩnh vực Công ty kinh doanh '<tên>'?*
3. Xác nhận → `GET /{id}/lock` → `status = 2`, `updated_by` được ghi lại
4. Toast `Khoá thành công`, nạp lại danh sách; badge đổi sang **Khoá** (variant `required`)
5. Dòng đã khoá **chỉ còn nút Mở khoá** (Sửa và Xoá bị ẩn)

**Luồng phụ:**
- 3a. Còn Nhóm ngành **đang Hoạt động** trỏ tới lĩnh vực này → BE trả 400
  `Dữ liệu đang được sử dụng, vui lòng tải lại`. FE cũng **ẩn sẵn nút Khoá** khi
  `is_can_lock_update = false`

**Luồng Mở khoá:** bấm **Mở khoá** → xác nhận → `GET /{id}/unlock` → `status = 1`.
Mở khoá **luôn được phép**, không có điều kiện chặn.

---

### UC-07: Xoá

**Actor:** Người quản lý

**Luồng chính:**
1. Dòng đang Hoạt động **và không có Nhóm ngành nào** trỏ tới → hiện nút **Xoá**
2. Bấm Xoá → modal xác nhận *Bạn có chắc muốn xóa lĩnh vực Công ty kinh doanh '<tên>'?*
3. Xác nhận → `DELETE /{id}` → xoá cứng bản ghi
4. Toast `Xoá thành công`, nạp lại danh sách

**Luồng phụ:**
- 3a. Vừa bị Nhóm ngành gắn vào (race) → 400 `Dữ liệu đang được sử dụng, vui lòng tải lại`
- 3b. Vừa bị người khác khoá → 423 `Bản ghi đang bị khoá, vui lòng mở khoá trước khi xoá.`
  → FE nạp lại danh sách cho khớp trạng thái thật
- 3c. Bản ghi đã bị xoá → 404 `Dữ liệu đã thay đổi, vui lòng tải lại`

---

### UC-08: Xuất Excel

**Actor:** Người quản lý / Người xem

**Luồng chính:**
1. User bấm **Xuất Excel**
2. FE mở trực tiếp URL `GET /export?token=<JWT>&<bộ lọc hiện tại>` (**không** dùng fetch + blob)
3. Server trả file kèm `Content-Disposition` → trình duyệt lưu `danh_sach_linh_vuc_cong_ty_kinh_doanh.xls`
4. File chứa **đúng tập bản ghi đang lọc** (không phân trang), 8 cột (§7.3)

> Bắt buộc tải trực tiếp theo `?token=`: cách blob + `<a download>` sinh file UUID không đuôi
> trên Safari/webview.

---

### UC-09: Import Excel

**Actor:** Người quản lý

**Luồng chính:**
1. User bấm **Import Excel** → mở `V2BaseImportModal` (*Import Lĩnh vực Công ty kinh doanh*)
2. Bấm **Tải file mẫu** → tải `Mau_import_LinhVucKinhDoanhNoiBo.xlsx` từ `hrm-client/static/`
   - Dòng 1: header · Dòng 2: hướng dẫn (`skipRows = 1`) · Dòng 3–4: 2 dòng mẫu **import được thật**
3. User điền dữ liệu → chọn file → bấm **Load lên bảng**
4. FE khớp header theo `label` hoặc `aliases`, map về 2 khoá `Code` / `Name`
5. Bấm **Validate** → `POST /import/validate` → BE chấm từng dòng, trả `rows[] / total / validCount / invalidCount`
6. Bảng đánh dấu dòng hợp lệ (khoá lại) / dòng lỗi (hiện danh sách lỗi, cho sửa tại chỗ)
7. Nút **Import** chỉ bật khi **không còn dòng lỗi** → `POST /import` → BE ghi các dòng hợp lệ
8. Toast kết quả, đóng modal, nạp lại danh sách

**Luồng phụ:**
- 7a. Vừa hợp lệ vừa lỗi → HTTP **207**, toast cảnh báo
  `Import thành công X/Y lĩnh vực Công ty kinh doanh. Z lĩnh vực thất bại.`
- 7b. Không dòng nào hợp lệ → 400 `Không có dữ liệu hợp lệ để import`
- Bản ghi import vào luôn có `status = Hoạt động`

---

## 4. Business Rules

| # | Quy tắc |
|---|---------|
| BR-01 | **Mã** bắt buộc, định dạng `LVKDNB.` + hậu tố **1–4 ký tự** thuộc `[A-Za-z0-9_]` |
| BR-02 | Mã tự **viết HOA** khi lưu; khoảng trắng ngay sau dấu chấm bị loại bỏ |
| BR-03 | Mã **không được trùng** (unique toàn bảng, không phân biệt hoa/thường vì đã upper) |
| BR-04 | Chỉ gõ mỗi tiền tố `LVKDNB.` → coi như **bỏ trống**, báo `Bắt buộc phải nhập` |
| BR-05 | **Tên** bắt buộc, tối đa **255 ký tự** |
| BR-06 | Tên **không được chứa** dấu phẩy `,` và dấu hai chấm `:` |
| BR-07 | Tên **không được trùng** (unique toàn bảng) |
| BR-08 | **Trạng thái** chỉ nhận 1 (Hoạt động) hoặc 2 (Khoá); mặc định 1 khi tạo mới |
| BR-09 | Bản ghi **đang Khoá** thì chặn mọi đường ghi (Sửa / Xoá) → HTTP **423** |
| BR-10 | Chỉ **Xoá** được khi bản ghi đang Hoạt động **và** không còn Nhóm ngành nào trỏ tới |
| BR-11 | Chỉ **Khoá** được khi không còn Nhóm ngành **đang Hoạt động** nào trỏ tới |
| BR-12 | **Mở khoá** luôn được phép, không điều kiện |
| BR-13 | `created_by` / `updated_by` do `BaseModel` tự ghi theo `auth()->id()` (= `employees.id`) |
| BR-14 | Khoá / Mở khoá dùng `$model->save()` để hook audit chạy → `updated_by` được cập nhật |
| BR-15 | Validate phải báo **đồng thời** lỗi của mọi ô — 1 lần bấm Lưu hiện hết lỗi |
| BR-16 | Ngày giờ hiển thị `d/m/Y H:i` (**không giây**); Người tạo/cập nhật chỉ hiện **tên** |
| BR-17 | Import tối đa **1000 dòng**/lần |
| BR-18 | Trong file import, Mã và Tên còn phải **không trùng nhau giữa các dòng** |

---

## 5. Data Model

### 5.1. Quan hệ

```
internal_business_scopes (LVCTKD)
        │ 1
        │
        │ n
     scopes (Nhóm ngành)  ← scopes.internal_business_scope_id (BẮT BUỘC)
        │ n
        │
   … Khách hàng / Dự án / Giải pháp (gắn qua Nhóm ngành)
```

### 5.2. Bảng `internal_business_scopes`

| Cột | Kiểu | Null | Mặc định | Ghi chú |
|-----|------|:----:|----------|---------|
| `id` | bigint unsigned AI | ❌ | | PK |
| `code` | varchar(50) | ❌ | | **UNIQUE**. Dạng `LVKDNB.XXXX` |
| `name` | varchar(255) | ❌ | | **INDEX**. Unique kiểm ở tầng validate |
| `status` | tinyint | ❌ | `1` | 1 = Hoạt động · 2 = Khoá |
| `created_by` | bigint unsigned | ✅ | `NULL` | `employees.id` — hook tự ghi |
| `updated_by` | bigint unsigned | ✅ | `NULL` | `employees.id` — hook tự ghi |
| `created_at` | timestamp | ✅ | | |
| `updated_at` | timestamp | ✅ | | |

**Không có** `company_id` / `department_id` / `part_id` — danh mục dùng chung, phân quyền phẳng.

Migration: `hrm-api/database/migrations/2026_08_22_000001_create_internal_business_scopes_table.php`

### 5.3. Cột liên kết ở bảng `scopes`

| Cột | Kiểu | Null | Ghi chú |
|-----|------|:----:|---------|
| `internal_business_scope_id` | bigint unsigned | ✅ (DB) | Nghiệp vụ **bắt buộc** — `ScopeRequest` chặn |

Migration: `2026_08_22_000002_add_internal_business_scope_id_to_scopes_table.php`

### 5.4. Enum & hằng

| Hằng | Giá trị | Ghi chú |
|------|---------|---------|
| `STATUS_ACTIVE` | 1 | `status_text = 'Hoạt động'`, badge variant `brand` |
| `STATUS_INACTIVE` | 2 | `status_text = 'Khoá'`, badge variant `required` |
| `CODE_PREFIX` | `LVKDNB.` | Tiền tố cố định |
| `CODE_SUFFIX_MAX` | 4 | Độ dài tối đa hậu tố |

### 5.5. Thuật toán sắp theo độ khớp

Chỉ chạy khi **chưa bấm sort cột** và từ khoá ≥ **2 ký tự** (lấy từ `keyword`, hoặc `name`, hoặc `code`).

Thứ tự sắp:
1. **Điểm khớp** = `LEAST(điểm_theo_Mã, điểm_theo_Tên)`, càng nhỏ càng lên trên

   | Chất lượng khớp | Điểm ở cột Mã | Điểm ở cột Tên |
   |-----------------|:-------------:|:--------------:|
   | Trùng khít | 0 | 1 |
   | Bắt đầu bằng | 10 | 11 |
   | Khớp đầu một từ | 20 | 21 |
   | Chỉ chứa | 30 | 31 |
   | Không khớp | 99 | 99 |

2. **Khớp đúng dấu** trước khớp bỏ dấu (`COLLATE utf8mb4_0900_as_ci`)
3. **Vị trí xuất hiện** trong Tên (`LOCATE`; không tìm thấy → quy về 9999)
4. **Độ dài Tên** tăng dần
5. `id DESC`

---

## 6. API Specification

**Base URL:** `/api/v1/assign/internal-business-scopes`
**Xác thực:** JWT Bearer token
**Ký hiệu quyền:** `Q` = Quản lý danh mục lĩnh vực Công ty kinh doanh · `X` = Xem danh mục lĩnh vực Công ty kinh doanh

| # | Method | Path | Quyền | Mô tả |
|---|--------|------|-------|-------|
| 1 | GET | `/` | Q hoặc X | Danh sách (lọc + sắp xếp + phân trang) |
| 2 | GET | `/getAll` | *(không gắn)* | Options cho select — bản ghi Hoạt động |
| 3 | GET | `/export` | Q hoặc X | Xuất Excel theo bộ lọc |
| 4 | POST | `/import/validate` | Q | Chấm điểm từng dòng import |
| 5 | POST | `/import` | Q | Ghi các dòng hợp lệ |
| 6 | POST | `/` | Q | Tạo mới, hoặc cập nhật nếu body có `id` |
| 7 | PUT | `/{id}` | Q | Cập nhật |
| 8 | GET | `/{id}` | Q hoặc X | Chi tiết |
| 9 | DELETE | `/{id}` | Q | Xoá |
| 10 | GET | `/{id}/lock` | Q | Khoá |
| 11 | GET | `/{id}/unlock` | Q | Mở khoá |

### 6.1. `GET /` — Query params

| Param | Kiểu | Mô tả |
|-------|------|-------|
| `page` | int | Trang, mặc định 1 |
| `per_page` | int | Số dòng/trang, mặc định 10 |
| `keyword` | string | Tìm nhanh: Mã · Tên · **tên người tạo** |
| `code` | string | Lọc Mã (LIKE `%…%`) |
| `name` | string | Lọc Tên (LIKE `%…%`) |
| `status` | int | 1 hoặc 2 |
| `created_by` | int | `employees.id` |
| `updated_by` | int | `employees.id` |
| `updated_from` | date `Y-m-d` | Ngày cập nhật từ (so theo ngày) |
| `updated_to` | date `Y-m-d` | Ngày cập nhật đến |
| `sort_by` | enum | `code` · `name` · `createdAt` · `updatedAt`. Ngoài whitelist → bỏ qua |
| `sort_desc` | bool | `true` = giảm dần |

### 6.2. Resource trả về

```json
{
  "id": 12,
  "code": "LVKDNB.OTO",
  "name": "Ô tô",
  "status": 1,
  "status_text": "Hoạt động",
  "created_by_name": "Nguyễn Văn A",
  "created_at": "22/08/2026 14:30",
  "updated_by_name": "Nguyễn Văn A",
  "updated_at": "22/08/2026 15:02",
  "is_can_edit": true,
  "is_can_delete": true,
  "is_can_lock_update": true,
  "scopes_count": 0
}
```

| Field | Ý nghĩa |
|-------|---------|
| `is_can_edit` | Đang Hoạt động → cho Sửa |
| `is_can_delete` | Đang Hoạt động **và** `scopes_count = 0` |
| `is_can_lock_update` | Không còn Nhóm ngành **đang Hoạt động** trỏ tới → cho Khoá |
| `scopes_count` | Số Nhóm ngành đang dùng lĩnh vực này |

### 6.3. `POST /` · `PUT /{id}` — Body

```json
{ "id": 12, "code": "LVKDNB.OTO", "name": "Ô tô", "status": 1 }
```
`id` chỉ có ở luồng `POST` khi muốn cập nhật. `status` bỏ trống → mặc định 1 (tạo mới) /
giữ nguyên (cập nhật).

### 6.4. Mã lỗi

| HTTP | Khi nào | Message |
|------|---------|---------|
| 200 | Thành công | `success` |
| 207 | Import một phần | `Import thành công X/Y lĩnh vực Công ty kinh doanh. Z lĩnh vực thất bại` |
| 400 | Đang được sử dụng | `Dữ liệu đang được sử dụng, vui lòng tải lại` |
| 400 | Import 0 dòng hợp lệ | `Không có dữ liệu hợp lệ để import` |
| 403 | Thiếu quyền | *(middleware `checkPermission`)* |
| 404 | Bản ghi không tồn tại | `Dữ liệu đã thay đổi, vui lòng tải lại` |
| 422 | Validate sai | Xem §6.5 |
| 423 | Bản ghi đang khoá | `Bản ghi đang bị khoá, vui lòng mở khoá trước khi cập nhật.` / `… trước khi xoá.` |
| 500 | Lỗi server khi import | `Lỗi server khi import` |

### 6.5. Câu lỗi validate (422)

| Field | Rule | Message |
|-------|------|---------|
| `code` | required / chỉ có tiền tố | `Bắt buộc phải nhập` |
| `code` | không bắt đầu bằng tiền tố | `Mã phải bắt đầu bằng LVKDNB.` |
| `code` | regex | `Hậu tố tối đa 4 ký tự, chỉ gồm chữ không dấu (A-Z), số (0-9) và dấu gạch dưới (_)` |
| `code` | unique | `Mã lĩnh vực Công ty kinh doanh đã tồn tại` |
| `name` | required | `Bắt buộc phải nhập` |
| `name` | max:255 | `Tên lĩnh vực Công ty kinh doanh tối đa 255 ký tự` |
| `name` | not_regex `[,:]` | `Tên không được chứa ký tự dấu phẩy (,) và dấu hai chấm (:)` |
| `name` | unique | `Tên lĩnh vực Công ty kinh doanh đã tồn tại` |
| `status` | in:1,2 | `Trạng thái không hợp lệ` |

> Rule của `code` xếp closure **trước** `regex` vì `BaseRequest` chỉ trả lỗi **đầu tiên** của mỗi field.

### 6.6. Import — cấu trúc payload & lỗi từng dòng

**Request:**
```json
{ "internal_business_scopes": [ { "code": "LVKDNB.OTO", "name": "Ô tô" } ] }
```
Ràng buộc: `required|array|min:1|max:1000`, mỗi phần tử có `code` và `name` là string.

**Response `validate`:**
```json
{ "rows": [ { "index": 0, "code": "LVKDNB.OTO", "name": "Ô tô", "isValid": true, "errors": [] } ],
  "total": 1, "validCount": 1, "invalidCount": 0 }
```

**Lỗi từng dòng** (kiểm theo thứ tự, dừng ở lỗi đầu của mỗi trường):

| Trường | Điều kiện | Lỗi |
|--------|-----------|-----|
| Mã | rỗng hoặc chỉ có tiền tố | `Mã bắt buộc phải nhập` |
| Mã | sai định dạng | `Mã phải có dạng LVKDNB. + tối đa 4 ký tự (A-Z, 0-9, _)` |
| Mã | đã có trong DB | `Mã đã tồn tại trong hệ thống` |
| Mã | trùng dòng trước trong file | `Mã bị trùng với dòng N trong file` |
| Tên | rỗng | `Tên bắt buộc phải nhập` |
| Tên | > 255 ký tự | `Tên tối đa 255 ký tự` |
| Tên | chứa `,` hoặc `:` | `Tên không được chứa dấu phẩy (,) và dấu hai chấm (:)` |
| Tên | đã có trong DB (so **không phân biệt hoa/thường**) | `Tên đã tồn tại trong hệ thống` |
| Tên | trùng dòng trước trong file | `Tên bị trùng với dòng N trong file` |

---

## 7. UI Specification

### 7.1. Menu

**Danh mục › Lĩnh vực Công ty kinh doanh** — đặt **ngay trước** mục *Nhóm ngành*
(`hrm-client/components/menu-sidebar.js:322-329`).

### 7.2. Bảng danh sách — 9 cột

| # | Cột | Căn | Width | Sort | Ghi chú |
|---|-----|-----|-------|:----:|---------|
| 1 | STT | center | 60px | ❌ | sticky, số thứ tự theo trang |
| 2 | Mã | left | 150px | ✅ | sticky, **là link** mở modal Xem |
| 3 | Tên lĩnh vực Công ty kinh doanh | left | min 260px | ✅ | wrap, chữ thường không in đậm |
| 4 | Người tạo | left | 170px | ❌ | chỉ hiện **tên** |
| 5 | Ngày tạo | left | 140px | ✅ | `d/m/Y H:i` |
| 6 | Người cập nhật | left | 170px | ❌ | chỉ hiện **tên** |
| 7 | Ngày cập nhật | left | 140px | ✅ | `d/m/Y H:i` |
| 8 | Trạng thái | center | 130px | ❌ | `V2BaseBadge` + `status_text` |
| 9 | Hành động | center | 140px | ❌ | **luôn ở cuối** |

Ô trống hiển thị `—`.

**Nút trên đầu bảng:** Tạo mới *(chỉ Quản lý)* · Xuất Excel *(mọi quyền)* · Import Excel *(chỉ Quản lý)*

**Cột Hành động** (ẩn hẳn nút không dùng được):

| Nút | Điều kiện hiện |
|-----|----------------|
| Sửa | `canManage && is_can_edit` |
| Khoá | `canManage && status = 1 && is_can_lock_update ≠ false` |
| Mở khoá | `canManage && status = 2` |
| Xoá | `canManage && is_can_delete` |

### 7.3. Modal Tạo / Sửa / Xem

| Chế độ | Tiêu đề | Footer |
|--------|---------|--------|
| Tạo mới | Tạo mới lĩnh vực Công ty kinh doanh | Lưu · Lưu & Tiếp tục · Đóng |
| Sửa | Sửa lĩnh vực Công ty kinh doanh | Lưu · Đóng |
| Xem | Xem chi tiết lĩnh vực Công ty kinh doanh | Đóng |

Bố cục: 1 hàng lấp đầy 12 cột — **Mã** (3) · **Tên** (6) · **Trạng thái** (3).

- Header: chip `V2BaseMetaInfo` hiện người/ngày cập nhật (khi Sửa/Xem)
- Cuối body: block `V2BaseMetaInfo` hiện Người tạo / Ngày tạo (khi Sửa/Xem)
- Lỗi hiển thị bằng `V2BaseError` + viền đỏ `is-invalid`; ưu tiên `errors.first(x) || formError[x]`

### 7.4. File Excel xuất ra

Tên file `danh_sach_linh_vuc_cong_ty_kinh_doanh.xls`, tiêu đề *Danh sách lĩnh vực Công ty kinh doanh*,
8 cột: STT · Mã · Tên lĩnh vực Công ty kinh doanh · Trạng thái · Người tạo · Ngày tạo ·
Người cập nhật · Ngày cập nhật.

### 7.5. File mẫu Import

`hrm-client/static/Mau_import_LinhVucKinhDoanhNoiBo.xlsx`

| Dòng | Nội dung |
|------|----------|
| 1 | Header: STT · Mã lĩnh vực Công ty kinh doanh · Tên lĩnh vực Công ty kinh doanh |
| 2 | Hướng dẫn (bị bỏ qua nhờ `skipRows = 1`) |
| 3–4 | 2 dòng mẫu **import được thật** |

Header cũ (*"Mã/Tên lĩnh vực kinh doanh nội bộ"*) vẫn được nhận qua `aliases` → file mẫu người dùng
đang giữ không bị hỏng.

---

## 8. Non-functional Requirements

| # | Yêu cầu |
|---|---------|
| NFR-01 | Vào màn: bảng hiện spinner ngay, request danh sách bắn **đầu tiên**, không chờ request quyền |
| NFR-02 | `loadSeq` chống race — response của lượt gọi cũ bị bỏ qua |
| NFR-03 | Options Người tạo / Người cập nhật chỉ nạp khi mở panel lọc nâng cao |
| NFR-04 | Tìm theo người tạo dùng `EXISTS` để không phình câu `COUNT` khi phân trang |
| NFR-05 | Export không phân trang — trả toàn bộ tập đang lọc |
| NFR-06 | Import tối đa 1000 dòng, ghi trong 1 transaction |
| NFR-07 | Tương thích PHP 7.4 / Laravel 8 / Nuxt 2 / Vue 2 / Bootstrap-Vue 2.15 |
| NFR-08 | Đỏ chỉ dùng cho lỗi validate |

---

## 9. Danh sách file

**hrm-api**
```
database/migrations/2026_08_22_000001_create_internal_business_scopes_table.php
database/migrations/2026_08_22_000002_add_internal_business_scope_id_to_scopes_table.php
database/e2e_internal_scope_fixture.php
Modules/Assign/Entities/InternalBusinessScope/InternalBusinessScope.php
Modules/Assign/Services/InternalBusinessScopeService.php
Modules/Assign/Http/Controllers/Api/V1/InternalBusinessScopeController.php
Modules/Assign/Http/Requests/InternalBusinessScope/InternalBusinessScopeRequest.php
Modules/Assign/Transformers/InternalBusinessScopeResource/InternalBusinessScopeResource.php
Modules/Assign/Transformers/InternalBusinessScopeResource/DetailInternalBusinessScopeResource.php
Modules/Assign/Exceptions/LockedRecordException.php
Modules/Assign/Routes/api.php                                   (sửa)
Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php   (sửa)
app/ExcelExport/InternalBusinessScopeExport.php
resources/views/exports/internal_business_scopes.blade.php
```

**hrm-client**
```
pages/assign/internal-business-scopes/index.vue
pages/assign/internal-business-scopes/AddScopeModal.vue
static/Mau_import_LinhVucKinhDoanhNoiBo.xlsx
components/menu-sidebar.js                                      (sửa)
```

**e2e**
```
pages/InternalBusinessScopePage.ts
tests/assign/internal-business-scope.spec.ts
tests/assign/internal-business-scope.api.spec.ts
tests/assign/industry-group-internal-scope.api.spec.ts
```

---

## 10. Deploy

### 10.1. Thứ tự

1. Chạy migration `2026_08_22_000001` (+ `2026_08_22_000002` nếu chưa có)
2. Tạo 2 quyền id **1177 / 1178** — **insert thủ công**, KHÔNG chạy `PermissionsTableSeeder`
   (seeder `truncate` cả bảng `permissions`)
3. Gán quyền cho role: `role_has_permissions` cần cột `company_id = 1` như các quyền khác
4. Deploy `hrm-api` → deploy `hrm-client`
5. `php artisan cache:clear`

### 10.2. Nếu môi trường đã có bản cũ (tên "Lĩnh vực kinh doanh nội bộ")

Phải chạy **cùng lúc** với deploy code, nếu không sẽ mất menu + 403 toàn màn:

```sql
UPDATE permissions SET name='Quản lý danh mục lĩnh vực Công ty kinh doanh',
       display_name='Quản lý danh mục lĩnh vực Công ty kinh doanh' WHERE id=1177;
UPDATE permissions SET name='Xem danh mục lĩnh vực Công ty kinh doanh',
       display_name='Xem danh mục lĩnh vực Công ty kinh doanh' WHERE id=1178;
```

Sau đó `php artisan cache:clear`.

---

## 11. Edge cases

| # | Tình huống | Xử lý |
|---|-----------|-------|
| EC-01 | Gõ mỗi tiền tố `LVKDNB.` rồi Lưu | Báo `Bắt buộc phải nhập` (không phải lỗi định dạng) |
| EC-02 | Hậu tố 5 ký tự | Ô nhập chặn sẵn `maxlength=4`; BE vẫn chặn bằng regex |
| EC-03 | Hậu tố chữ thường `oto` | Tự viết HOA thành `LVKDNB.OTO` khi lưu |
| EC-04 | Hậu tố có dấu / ký tự đặc biệt | 422 lỗi định dạng |
| EC-05 | Tên chỉ gồm khoảng trắng | `trim` → rỗng → `Bắt buộc phải nhập` |
| EC-06 | Tên trùng nhưng khác hoa/thường | Unique của MySQL `_ci` → vẫn báo trùng |
| EC-07 | Bấm Lưu khi form trống | Hiện **2 lỗi đồng thời**, 2 ô viền đỏ, focus ô Mã |
| EC-08 | Lỗi 422 rồi user sửa lại ô đó | Lỗi BE của ô đó tự mất, nhường validate realtime |
| EC-09 | 2 tab: tab A khoá, tab B bấm Sửa | 423, FE nạp lại danh sách |
| EC-10 | 2 tab: tab A xoá, tab B bấm Sửa | 404 `Dữ liệu đã thay đổi, vui lòng tải lại` |
| EC-11 | Xoá lĩnh vực đang có Nhóm ngành | Nút Xoá **ẩn**; gọi thẳng API → 400 |
| EC-12 | Khoá lĩnh vực có Nhóm ngành đang Hoạt động | Nút Khoá **ẩn**; gọi thẳng API → 400 |
| EC-13 | Khoá lĩnh vực chỉ còn Nhóm ngành đã Khoá | **Cho phép** khoá |
| EC-14 | Tìm kiếm gõ thiếu dấu (`o to`) | Vẫn khớp (collation `_ci`) nhưng xếp **sau** bản khớp đúng dấu |
| EC-15 | Import file có 2 dòng cùng Mã | Dòng sau báo `Mã bị trùng với dòng N trong file` |
| EC-16 | Import file thiếu cột | `V2BaseImportModal` báo không khớp header |
| EC-17 | Import file mẫu cũ (header tên cũ) | Vẫn nhận nhờ `aliases` |
| EC-18 | Sort theo tham số lạ (`sort_by=abc`) | Bỏ qua, rơi về `id DESC` |
| EC-19 | Xuất Excel khi bộ lọc không ra dòng nào | File chỉ có header |
| EC-20 | User bị thu hồi quyền giữa chừng | API trả 403, FE **không** hiện toast |

---

## 12. Nợ kỹ thuật

Skill `list-page` mô tả 6 thành phần dùng chung **không tồn tại trong repo này**:

| Thành phần | Trạng thái |
|-----------|-----------|
| `V2BaseSmartFilterPanel` | Chưa có — dùng `V2BaseFilterPanel` |
| Popup Cấu hình cột (`columnCustomizationMixin`) | Chưa có |
| Popup Chọn trường xuất file (`ExportColumnRegistry` + `DynamicExport`) | Chưa có — export cố định 8 cột |
| Bộ Lịch sử danh mục (`catalog_histories` + `CatalogHistoryModal`) | Chưa có — **không có** hành động Lịch sử |
| `V2BaseModal` | Chưa có — dùng `b-modal` |
| File mẫu Import sinh bằng API | Chưa có — dùng file tĩnh trong `static/` |

Kế hoạch: xử lý **sau khi gộp DB**, theo quyết định của user.

---

## 13. Phụ lục — Tham chiếu

- Spec gốc: `docs/superpowers/specs/2026-08-22-linh-vuc-kinh-doanh-noi-bo-design.md`
- Plan thực thi: `.plans/linh-vuc-kinh-doanh-noi-bo/plan.md`
- Design tóm tắt: `.plans/linh-vuc-kinh-doanh-noi-bo/design.md`
- Ảnh chụp màn hình: `.plans/linh-vuc-kinh-doanh-noi-bo/screenshots/`
- Testcase: `docs/srs/linh-vuc-cong-ty-kinh-doanh-testcases.xlsx`
