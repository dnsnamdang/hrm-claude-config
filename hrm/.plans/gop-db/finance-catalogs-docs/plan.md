# Tài liệu 3 màn danh mục Tài chính — SRS + HDSD + TC

> Nhánh `gop_db` · **@junfoke phụ trách tài liệu** · 17/08/2026
> Nhóm 2 trong yêu cầu 10 màn danh mục của user (nhóm 1 = Địa lý, xem
> `.plans/gop-db/geo-catalogs-docs/plan.md`).

## Phạm vi

| Màn | Đường dẫn | Quyền |
|---|---|---|
| Danh mục vụ việc | `/finance/works` | Quản lý danh mục vụ việc |
| Danh mục mã phí | `/finance/cost-debts` | Quản lý danh mục mã phí |
| Danh mục nguồn vốn | `/finance/source-capitals` | Quản lý danh mục nguồn vốn |

Mỗi màn dùng **đúng một quyền** cho cả xem lẫn sửa — không tách quyền xem riêng, không phân
quyền theo cấp. Không có quyền thì mục menu không hiện và truy cập thẳng đường dẫn bị chặn.
Khác hẳn nhóm Địa lý (không màn nào có quyền).

## Vụ việc và Mã phí là cặp song sinh

Hai màn giống nhau tới từng dòng: cùng khuôn giao diện, cùng 4 tiêu chí lọc, cùng 4 ô nhập,
cùng điều kiện xóa. Chỉ khác nhãn. Ticket áp cho màn này gần như chắc chắn có ticket y hệt cho
màn kia.

## Khác biệt giữa 3 màn (đã đọc code 17/08/2026)

| | Vụ việc | Mã phí | Nguồn vốn |
|---|---|---|---|
| Ô nhập | Mã, Tên, Trạng thái, Ghi chú | Mã, Tên, Trạng thái, Ghi chú | **chỉ Tên** |
| Cột Trạng thái trên lưới | ✅ | ✅ | ❌ |
| Bộ lọc nâng cao | 3 tiêu chí | 3 tiêu chí | **không có** |
| Trường duy nhất | **Mã** (tên được trùng) | **Mã** (tên được trùng) | **Tên** |
| Điều kiện xóa | chưa phát sinh bút toán | chưa phát sinh bút toán | không ràng buộc |
| Bản chất Xóa | xóa thật | xóa thật | **ngừng sử dụng (xóa mềm)** |

## Điểm nghiệp vụ cốt lõi đã xác minh trong code

- **Nút Xóa chỉ hiện khi bản ghi chưa phát sinh bút toán kế toán.** Đã kiểm chứng trên dev: dòng
  đầu có đủ Sửa / Xóa / Lịch sử, hai dòng sau chỉ có Sửa / Lịch sử. Đúng quy ước dự án "nút không
  dùng được thì ẩn hẳn".
- **Không có nút Khóa riêng.** Muốn ngừng dùng một bản ghi đã phát sinh bút toán thì mở cửa sổ
  Sửa rồi đổi ô Trạng thái sang Khóa. Khác nhóm Địa lý (có nút Khóa trong menu ba chấm).
- **Ràng buộc duy nhất áp cho MÃ, không áp cho TÊN** ở màn Vụ việc và Mã phí. Hai bản ghi khác mã
  được phép trùng tên — dễ bị báo lỗi nhầm khi kiểm thử.
- **Cửa sổ nhập liệu chỉ có 2 nút Lưu và Đóng** — không có "Lưu và tiếp tục" như nhóm Địa lý.
- **Trạng thái mặc định của bản ghi mới là Hoạt động.**
- Màn Nguồn vốn: "xóa" thực chất gọi hàm chặn sử dụng ở phía máy chủ, dữ liệu không mất hẳn nên
  chứng từ cũ vẫn hiển thị đúng tên.

## Thông báo lỗi lấy nguyên văn từ code

| Màn | Thông báo |
|---|---|
| Chung | `Bắt buộc phải nhập` |
| Vụ việc | `Mã vụ việc đã tồn tại` |
| Mã phí | `Mã phí đã tồn tại` |
| Nguồn vốn | `Tên nguồn vốn đã tồn tại` |

## Kết quả

- [x] Ảnh: **15** trong `fin_shots/`, chụp trên cổng dev `hrm-crm.eteksofts.com`
- [x] **3 × `SRS - <Tên màn>.docx`** — form 4 phần, mục lục do Word cập nhật thật

      | Màn | Trang | Bảng | Ảnh |
      |---|---|---|---|
      | Vụ việc | 17 | 21 | 10 |
      | Mã phí | 16 | 21 | 9 |
      | Nguồn vốn | 15 | 21 | 8 |

- [x] **3 × `testcase - <Tên màn>.xlsx`** — tổng **147 TC**, P0 83%.
      Vụ việc 53 · Mã phí 53 · Nguồn vốn 41. Có section phân quyền 6 TC mỗi màn
      (khác nhóm Địa lý vì nhóm này có quyền thật).
- [x] **3 × `HDSD_<Tên màn>.docx`** — 10-12 trang, 9 bảng, 5-7 ảnh.

## File sinh tài liệu

```text
python .plans/gop-db/finance-catalogs-docs/gen_srs.py        # + fin_config.py
python .plans/gop-db/finance-catalogs-docs/gen_testcase.py
python .plans/gop-db/finance-catalogs-docs/gen_hdsd.py
```

## Còn lại

Màn cuối trong yêu cầu 10 màn: **Công việc, lỗi thiết bị** (`/customer-care/device-errors`) —
nặng nhất, 9 tiêu chí lọc, ~14 cột, có In và Xuất Excel, form Tạo mới là trang riêng.
