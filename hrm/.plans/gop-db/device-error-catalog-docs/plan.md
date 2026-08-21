# Tài liệu màn Danh mục công việc, lỗi thiết bị — SRS + HDSD + TC

> Nhánh `gop_db` · **@junfoke phụ trách tài liệu** · 18/08/2026
> Nhóm 3 (cuối) trong yêu cầu 10 màn danh mục của user.
> Nhóm 1 = Địa lý (`geo-catalogs-docs`) · Nhóm 2 = Tài chính (`finance-catalogs-docs`).

## Phạm vi

| | |
|---|---|
| Màn | Danh mục công việc, lỗi thiết bị |
| Đường dẫn | `/customer-care/device-errors` |
| Quyền | Quản lý danh mục công việc - lỗi thiết bị (một quyền duy nhất) |
| Quy mô | FE ~2.700 dòng (form 1.180, danh sách 834) — nặng nhất trong 10 màn |

Đây là danh mục nền của nghiệp vụ sửa chữa: dữ liệu được chọn khi lập báo giá dịch vụ và phiếu
sửa chữa.

## Điểm nghiệp vụ cốt lõi đã xác minh trong code

**Trùng tên xét theo TỪNG LOẠI, không phải toàn danh mục.** Sáu loại: Lỗi đã xác định, Lỗi chưa
xác định, Lắp đặt bàn giao, Thiết kế nền móng, Tư vấn, khảo sát, Giám sát thi công. Hai loại khác
nhau được phép có hạng mục trùng tên. Hệ quả ít ai để ý: **đổi ô Loại khi sửa sẽ kiểm tra lại
trùng tên trong loại mới**.

**Cột Hành động chỉ hiện thẳng HAI nút đầu còn dùng được**, phần còn lại tự dồn vào nút ba chấm.
Đã kiểm chứng trên dev — ba dòng cho ra ba tập nút khác nhau:

| Trạng thái dòng | Hiện thẳng | Trong nút ba chấm |
|---|---|---|
| Hoạt động, chưa phát sinh chứng từ | Sửa, Xóa | Khóa, In, Lịch sử |
| Hoạt động, đã phát sinh chứng từ | Sửa, Khóa | In, Lịch sử |
| Đã Khóa | Mở khóa, In | Lịch sử |

**Nút Xóa cần thỏa CẢ HAI điều kiện**: đang Hoạt động VÀ chưa phát sinh chứng từ. Thiếu một trong
hai thì ẩn hẳn.

**Bốn ô để trống thì hệ thống tự điền**: Công kỹ thuật (tính từ Định mức công), Đơn giá bán (tính
theo công thức), Hệ số giá bán dịch vụ và Đơn giá công kỹ thuật (lấy theo cấu hình công ty). Hai ô
cuối khiến **hai người ở hai công ty khác nhau ra kết quả tính khác nhau** — đúng thiết kế.

**Ba bảng con**: Áp dụng cho thiết bị (bắt buộc ≥1 dòng) · Vật tư thay thế (không bắt buộc) ·
Dịch vụ sửa chữa kèm theo (không bắt buộc, **nhưng dòng đã thêm thì bắt buộc đủ Giá vốn và Giá
dịch vụ** — nếu không sẽ nổ lỗi ở tầng dữ liệu, nên đã chặn sẵn ở tầng kiểm tra).

**Bảy cột mặc định ẩn**: Loại, Áp dụng cho thiết bị, Định mức công, Công kỹ thuật, Đơn giá bán,
Người cập nhật, Ngày cập nhật.

**Chức năng thêm mới mở TRANG RIÊNG** (`/create`), không phải cửa sổ — khác 9 màn danh mục kia.

## Thông báo lỗi lấy nguyên văn từ code

| Ô | Thông báo |
|---|---|
| Các ô bắt buộc | `Bắt buộc phải nhập` |
| Hệ số công nghệ = 0 | `Nhập hệ số lớn hơn 0` |
| VAT > 100 | `Tối đa 100` |
| Ô số nhập chữ | `Phải là số` |
| Ô số âm | `Không được nhỏ hơn 0` |
| Giá vốn / Giá dịch vụ trong bảng | `Bắt buộc phải nhập` — gắn đúng ô trong bảng, không phải thông báo chung |

## Kết quả

- [x] Ảnh: **8** trong `de_shots/`, chụp trên cổng dev `hrm-crm.eteksofts.com`
- [x] `SRS - Danh mục công việc, lỗi thiết bị.docx` — **27 trang**, 30 bảng, 13 ảnh,
      9 chức năng FR-01…FR-09, 7 quy tắc BR-01…BR-07
- [x] `testcase - Danh mục công việc, lỗi thiết bị.xlsx` — **113 TC**, P0 71%,
      9 TC phân quyền + 10 section La Mã
- [x] `HDSD_Danh mục công việc, lỗi thiết bị.docx` — **20 trang**, 11 bảng, 9 ảnh

## File sinh tài liệu

```text
python .plans/gop-db/device-error-catalog-docs/gen_srs.py        # + de_config.py
python .plans/gop-db/device-error-catalog-docs/gen_testcase.py
python .plans/gop-db/device-error-catalog-docs/gen_hdsd.py
```

## Tổng kết cả 10 màn

| Nhóm | Màn | SRS | TC | HDSD |
|---|---|---|---|---|
| Địa lý | 6 | 6 | 327 | 6 |
| Tài chính | 3 | 3 | 147 | 3 |
| Lỗi thiết bị | 1 | 1 | 113 | 1 |
| **Tổng** | **10** | **10** | **587** | **10** |
