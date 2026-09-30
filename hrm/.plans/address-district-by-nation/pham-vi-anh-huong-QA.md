# Phạm vi ảnh hưởng — gửi tester

Tính năng: **Khôi phục cấp Quận/Huyện cho địa chỉ nước ngoài**
Người làm: @junfoke · Ngày: 09/09/2026 · Nhánh `tpe` (cả `hrm-api` và `hrm-client`)

---

## 1. Quy tắc nghiệp vụ cần nắm trước khi test

Việt Nam đã bỏ cấp huyện, nhưng địa chỉ các nước khác vẫn còn. Nên ô Quận/Huyện **không bị bỏ**, mà **ẩn/hiện theo quốc gia**:

| Quốc gia đang chọn | Luồng chọn địa chỉ |
| --- | --- |
| **Việt Nam** | Quốc gia → Tỉnh/TP → **Phường/Xã** → Đường/Thôn — KHÔNG có ô Quận/Huyện |
| **Nước khác** | Quốc gia → Tỉnh/TP → **Quận/Huyện** → **Phường/Xã** → Đường/Thôn |

Quy tắc phụ áp dụng cho **mọi màn** ở mục 3:

- Ô Quận/Huyện **ẩn hẳn** khi là Việt Nam (không phải hiện rồi làm mờ).
- Đổi Quốc gia → xoá sạch Tỉnh/Quận/Xã/Thôn đang chọn.
- Đổi Tỉnh → xoá Quận/Xã/Thôn. Đổi Quận → xoá Xã/Thôn.
- Nước ngoài: **chưa chọn Quận/Huyện thì chưa chọn được Phường/Xã**.
- Mở lại bản ghi cũ (màn Sửa/Xem) phải hiện đúng Quận/Huyện đã lưu, không được để trống.

---

## 2. Điều kiện tiền đề — làm trước khi test, không có thì test sẽ fail oan

1. **Chạy `php artisan migrate`** trên môi trường test.
   Migration `2026_09_08_000000_add_status_and_audit_to_districts_table` thêm `created_by` / `updated_by` (và `status` nếu chưa có) vào bảng `districts`. Chưa chạy thì màn Danh mục Quận/Huyện và API lấy quận/huyện **lỗi 500**.

2. **Kiểm dữ liệu bảng `nations`.**
   Trên máy dev của tôi, `nations` bên HRM chỉ có **3** bản ghi trong khi bên ERP có **30** — dẫn tới **không lưu được khách hàng nước ngoài** (báo lỗi ở ô Quốc gia: *"Không tồn tại"*). Đây là **lỗi dữ liệu có sẵn, không phải của tính năng này**, nhưng nó chặn luôn phần test địa chỉ nước ngoài.
   Câu lệnh kiểm nhanh:
   ```sql
   SELECT (SELECT COUNT(*) FROM hrm.nations)  AS nations_hrm,
          (SELECT COUNT(*) FROM erp.nations)  AS nations_erp;
   ```
   Lệch nhau → báo lại dev trước khi test, đừng ghi bug "không lưu được khách hàng".

3. Cần **ít nhất 1 tỉnh/thành thuộc quốc gia khác Việt Nam** có sẵn quận/huyện + phường/xã để thử (ví dụ trên máy dev: Indonesia → Jakarta → Jakarta Selatan → Kec. Setiabudi).

---

## 3. Danh sách màn bị ảnh hưởng

### Nhóm A — Màn MỚI

| Màn | Đường dẫn |
| --- | --- |
| Danh mục Quận/Huyện | `/human/districts` (menu **Danh mục → Danh mục quận/huyện**, nằm giữa Tỉnh/TP và Phường/xã) |

Test đầy đủ: danh sách, bộ lọc (Quốc gia / Tỉnh-TP / Tên / Trạng thái), Tạo mới, Sửa, Xoá, Khoá, Mở khoá, phân trang, cột Người cập nhật + Ngày cập nhật.
Lưu ý riêng: bản ghi **đã khoá** thì menu hành động chỉ còn **Mở khóa** (Sửa/Xoá phải biến mất).

### Nhóm B — Màn ĐÃ SỬA, phải test kỹ phần địa chỉ

| # | Màn | Đường dẫn | Khối địa chỉ cần test |
| --- | --- | --- | --- |
| B1 | Khách hàng (Dự án & Giao việc) — Thêm mới | `/assign/customers/add` | Địa chỉ khách hàng, ở **cả 2 dạng**: chọn Loại hình = *Cá nhân* và = *Doanh nghiệp tư nhân* (2 khối khác nhau trong code) |
| B2 | Khách hàng (Dự án & Giao việc) — Sửa | `/assign/customers/{id}/edit` | Như B1 **+ khối "Địa chỉ giao hàng"** — mỗi dòng có Quốc gia riêng, phải ẩn/hiện Quận/Huyện **độc lập theo từng dòng** |
| B3 | Khách hàng (Dự án & Giao việc) — Chi tiết | `/assign/customers/{id}` | Hiển thị đúng địa chỉ đã lưu |
| B4 | Khách hàng (HCNS) — Thêm mới | `/human/customers/add` | Khối "Địa chỉ công ty"; test cả KH cá nhân lẫn KH tổ chức |
| B5 | Khách hàng (HCNS) — Sửa / Chi tiết | `/human/customers/{id}` | Mở KH nước ngoài cũ phải hiện đúng Quận/Huyện đã lưu |
| B6 | Hồ sơ nhân sự — Thêm mới | `/human/employee_info/add` | **2 khối**: Hộ khẩu thường trú **và** Nơi ở hiện tại |
| B7 | Hồ sơ nhân sự — Chi tiết / Sửa | `/human/employee_info/{id}` | Như B6 |
| B8 | Hồ sơ nhân sự — Yêu cầu cập nhật thông tin | `/human/employee_info/{id}/update_request` | Như B6 |
| B9 | Thông tin của tôi | `/human/employee_info/my_info` | Chuỗi địa chỉ hiển thị phải có tên Quận/Huyện (nếu bản ghi có) |
| B10 | Yêu cầu cập nhật thông tin của tôi — chi tiết | `/human/employee_info/my-info-request/{id}` | Như B6 |
| B11 | Duyệt yêu cầu cập nhật thông tin | `/human/employee_info/request-update` và `/human/employee_info/request-update/{id}` | Như B6 |
| B12 | Lý do từ chối (người duyệt) | `/human/employee_info/my-info-request/{id}/reason_deny_approver` | Như B6 |

> **Lưu ý cho Hồ sơ nhân sự (B6–B12)**: màn này **không có ô Quốc gia riêng** cho địa chỉ. Quốc gia được **suy ra từ Tỉnh/TP đang chọn**. Nên:
> - Chưa chọn Tỉnh/TP → **chưa hiện** ô Quận/Huyện (đúng, không phải bug).
> - Chọn tỉnh của Việt Nam → không có ô Quận/Huyện.
> - Chọn tỉnh nước ngoài → hiện ô Quận/Huyện.
> - Hai khối Hộ khẩu và Nơi ở hiện tại **độc lập nhau**: một khối chọn tỉnh nước ngoài, khối kia chọn tỉnh Việt Nam → chỉ khối đầu có ô Quận/Huyện.

### Nhóm C — Màn KHÔNG sửa nhưng **dùng chung API địa chỉ** → test hồi quy (smoke test)

API `/api/v1/addresses` bị sửa (thêm lại cấp quận/huyện, danh sách tỉnh trả kèm mã quốc gia). Các màn dưới đây gọi chung API đó nhưng **không đổi giao diện** — chỉ cần mở lên xem danh sách Tỉnh/TP, Phường/Xã còn chạy bình thường:

| # | Màn | Đường dẫn | Kiểm gì |
| --- | --- | --- | --- |
| C1 | Công ty — Thêm mới / Sửa | `/human/company/add`, `/human/company/{id}` | Chọn Tỉnh/TP → Phường/Xã còn nạp đúng. **Màn này KHÔNG có ô Quận/Huyện — đúng thiết kế, ngoài phạm vi đợt này** |
| C2 | Danh mục Ngân hàng — chi nhánh | `/human/banks` (popup Chi nhánh) | Dropdown Tỉnh/TP còn đủ dữ liệu |
| C3 | Danh mục Phường/Xã | `/human/wards` | Không đổi, mở kiểm cho chắc |
| C4 | Danh mục Tỉnh/TP | `/human/provinces` | Không đổi, mở kiểm cho chắc |

### Nhóm D — Ảnh hưởng gián tiếp

| # | Chỗ cần để ý | Mô tả |
| --- | --- | --- |
| D1 | **Lịch sử thay đổi hồ sơ nhân sự** | Quận/Huyện nay được lưu lại → khi sửa trường này, popup Lịch sử thay đổi phải ghi nhận dòng "Quận/Huyện/Thị xã" (giá trị cũ → giá trị mới) |
| D2 | **Đồng bộ sang ERP** | Tạo/Sửa/Xoá/Khoá ở Danh mục Quận/Huyện được đồng bộ sang bảng `districts` của ERP (cùng id). Sửa hồ sơ nhân sự cũng đồng bộ `district_id` sang ERP |
| D3 | **Danh sách khách hàng** | Cột/bộ lọc liên quan địa chỉ — kiểm không vỡ hiển thị |

---

## 4. Bộ ca test tối thiểu cho mỗi màn ở nhóm B

1. **Việt Nam** → không thấy ô Quận/Huyện; chọn Tỉnh → Phường/Xã nạp thẳng theo tỉnh.
2. **Đổi sang nước khác** → ô Quận/Huyện xuất hiện, nằm **giữa** Tỉnh/TP và Phường/Xã.
3. **Cascade nước ngoài**: chọn Tỉnh → danh sách Quận/Huyện nạp đúng; chọn Quận → Phường/Xã chỉ còn các xã thuộc quận đó.
4. **Chưa chọn Quận/Huyện** → ô Phường/Xã bị khoá (nước ngoài).
5. **Đổi Quốc gia ngược về Việt Nam** → ô Quận/Huyện biến mất, Tỉnh/Quận/Xã đã chọn bị xoá sạch.
6. **Lưu** bản ghi nước ngoài → mở lại màn Sửa: Tỉnh / Quận/Huyện / Phường/Xã hiện **đúng như lúc lưu** (đây là ca dễ lỗi nhất).
7. **Mở bản ghi Việt Nam cũ** (dữ liệu có sẵn từ trước) → không thấy ô Quận/Huyện, Tỉnh và Phường/Xã vẫn hiện đúng.
8. Riêng B2: thêm 2 dòng Địa chỉ giao hàng, **1 dòng Việt Nam + 1 dòng nước ngoài** → chỉ dòng nước ngoài có ô Quận/Huyện, hai dòng không ảnh hưởng nhau.

---

## 5. Ngoài phạm vi — không cần test

- Màn **Công ty** (`/human/company/*`): cố ý không bổ sung ô Quận/Huyện đợt này (chỉ smoke test như C1).
- Dữ liệu danh mục địa chỉ (tỉnh/quận/xã): dùng dữ liệu có sẵn, không nhập mới.
- File `components/human-components/employee_info/request-update/EmployeeInfoShow.vue` có trong danh sách sửa nhưng **hiện không màn nào dùng** — không cần tìm để test.

---

## 6. Đã dev tự kiểm (PASS) — tester vẫn nên kiểm lại

- Danh mục Quận/Huyện: Tạo / Sửa / Khoá / Mở khoá / Xoá + đồng bộ ERP 2 chiều + cột Người cập nhật.
- KH (HCNS): ẩn/hiện theo quốc gia, cascade, reset, mở lại bản ghi nước ngoài cũ giữ đúng giá trị.
- KH (Giao việc): ẩn/hiện + cascade + reset ở cả KH cá nhân và KH tổ chức; danh sách Tỉnh/TP lọc đúng theo quốc gia.
- Hồ sơ nhân sự (màn Thêm mới): 2 khối địa chỉ độc lập, suy quốc gia từ tỉnh.

**Dev CHƯA kiểm được** (bị chặn bởi mục 2.2 và thiếu quyền), tester lưu ý test kỹ:

- Vòng **Lưu** khách hàng nước ngoài ở màn Giao việc.
- Khối **Địa chỉ giao hàng** (B2).
- Các màn B8–B12 (nhánh yêu cầu cập nhật thông tin / duyệt).
