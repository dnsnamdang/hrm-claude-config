# Test Cases: BOM List

## BE API Test Results (Auto)

| # | Test | Kết quả |
|---|------|---------|
| 1 | INDEX — danh sách + count | PASS |
| 2 | SHOW — detail + products + name + relationships | PASS |
| 3 | FILTER — status, keyword | PASS |
| 4 | STORE — tạo nháp + products cha/con + không tạo product_projects | PASS |
| 5 | UPDATE — đổi status + products | PASS |
| 6 | UPDATE BLOCKED — status=3 không cho sửa | PASS |
| 7 | DESTROY — xoá BOM Đang tạo | PASS |
| 8 | DESTROY BLOCKED — status=2 không cho xoá | PASS |
| 9 | VALIDATE IMPORT — valid/invalid + lookup check | PASS |
| 10 | IMPORT PRODUCTS — cha/con + auto-gen code + resolve lookup | PASS |

---

## UI Test Cases (Manual)

### TC-01: Màn danh sách
**URL:** `/assign/bom-list`

| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Truy cập URL | Hiện bảng danh sách BOM, có data |
| 2 | Gõ "PLC" vào ô tìm kiếm nhanh | Chỉ hiện BOM có mã/tên chứa "PLC" |
| 3 | Xoá keyword, mở bộ lọc nâng cao | Hiện các filter: Công ty, Phòng ban, Bộ phận, Dự án, Giải pháp, Hạng mục, KH, Người tạo, Trạng thái, Loại BOM, Ngày tạo |
| 4 | Chọn 1 Dự án TKT | Giải pháp tự fill (readonly), Hạng mục enable |
| 5 | Chọn Hạng mục | Danh sách lọc theo hạng mục |
| 6 | Click "Làm mới" | Reset tất cả filter, hiện lại toàn bộ |
| 7 | Click header cột "Ngày tạo" | Sort tăng/giảm |
| 8 | Đổi trang (pagination) | Chuyển trang đúng |
| 9 | Click icon tuỳ chỉnh cột | Modal hiện, ẩn/hiện cột, save |

### TC-02: Tạo BOM Thành phần — Lưu nháp
**URL:** `/assign/bom-list/add`

| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Chọn Dự án TKT | Giải pháp tự fill, Khách hàng tự fill |
| 2 | Nhập Tên BOM | OK |
| 3 | Chọn loại: Thành phần | Button "Chọn hàng hoá" enable |
| 4 | Click "Thêm nhanh hàng hoá" | Popup thêm nhanh, nhập tên + model + brand + origin + ĐVT + SL |
| 5 | Lưu → thêm lần 2 | Không lỗi trùng code |
| 6 | Click "Thêm nhanh con" trên hàng cha | Popup thêm con, lưu thành công |
| 7 | Click "Lưu nháp" | Toast "thành công", redirect danh sách |
| 8 | Kiểm tra DB | `bom_lists.status = 1`, `product_projects` KHÔNG có record mới |

### TC-03: Tạo BOM Thành phần — Lưu
| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Tạo BOM + thêm SP | Tương tự TC-02 step 1-6 |
| 2 | Click "Lưu BOM" | Toast "thành công", redirect danh sách |
| 3 | Kiểm tra DB | `bom_lists.status = 2` |

### TC-04: Tạo BOM — Chọn từ danh mục
| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Click "Chọn hàng hoá" | Popup danh mục, hiện SP từ product_projects |
| 2 | Tick chọn SP cha + con | Highlight |
| 3 | Click "Áp dụng" | SP thêm vào bảng BOM với đầy đủ thông tin |
| 4 | Lưu BOM | Thành công |
| 5 | Kiểm tra DB | `bom_list_products` có `name`, `code`, `product_project_id` (nguồn gốc) |

### TC-05: Sửa BOM
| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Mở edit BOM Đang tạo | Hiện cả "Lưu nháp" + "Lưu BOM" |
| 2 | Mở edit BOM Hoàn thành | Chỉ hiện "Lưu BOM" (ẩn Lưu nháp) |
| 3 | Sửa tên, thêm/xoá SP | OK |
| 4 | Sửa tên SP trong BOM | Lưu → kiểm tra `product_projects` KHÔNG thay đổi |
| 5 | Lưu → mở lại | Data đúng (name, code, qty, price) |

### TC-06: Xoá BOM
| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Tại danh sách, BOM Đang tạo + do mình tạo | Hiện icon xoá |
| 2 | Click xoá | Modal confirm hiện mã + tên BOM |
| 3 | Confirm | Toast "thành công", BOM biến mất khỏi danh sách |
| 4 | BOM Hoàn thành | KHÔNG hiện icon xoá |
| 5 | BOM của người khác | KHÔNG hiện icon xoá |

### TC-07: Xuất Excel
| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Tại danh sách, click icon Excel trên 1 BOM | Popup chọn cột + checkbox cấp con |
| 2 | Bỏ chọn vài cột, click "Xuất Excel" | Download file .xlsx, popup đóng |
| 3 | Mở file Excel | Font Times New Roman, auto-fit cột |
| 4 | Header: Tên BOM, Mã, Dự án, GP, HM, KH | Đúng thông tin |
| 5 | Bảng: chỉ hiện cột đã chọn | Đúng |
| 6 | Hàng cha: bold, nền xanh | Đúng |
| 7 | Tắt checkbox cấp con → xuất | File chỉ có hàng cha |
| 8 | Cột tiền: dùng được hàm SUM trong Excel | Số không phải text |
| 9 | Dòng tổng cộng | Đúng tổng thành tiền |

### TC-08: Import Excel
| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Mở edit BOM → click "Import Excel" | Modal 4 bước |
| 2 | Click "Download template" | File mở được, có header + mẫu cha/con |
| 3 | Điền data vào template, upload | Preview hiện đúng số dòng |
| 4 | Click "Validate" | Hiện kết quả: X hợp lệ, Y lỗi |
| 5 | Dòng thiếu tên → lỗi "Tên hàng hoá là bắt buộc" | Đúng |
| 6 | Model không tồn tại → lỗi "không tồn tại trong danh mục" | Đúng |
| 7 | Hàng cha thành tiền ≠ tổng con → cảnh báo | Đúng |
| 8 | Click "Import" | Toast thành công, SP thêm vào BOM |
| 9 | Mã hàng không nhập | Tự sinh HH-XXXXX |
| 10 | STT 1=cha, 1.1=con | parent_id mapping đúng |
| 11 | BOM Tổng hợp | Không hiện nút Import |

### TC-09: Trang chi tiết
**URL:** `/assign/bom-list/{id}`

| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Truy cập URL | Hiện readonly, không có input/textarea |
| 2 | Không có cột Thao tác | Layout không lệch |
| 3 | Không có buttons: Chọn HH, Import, Thêm nhanh, Sửa, Xoá | Đúng |
| 4 | STT cấp con | Lùi đầu dòng, font normal |
| 5 | Header card | Hiện người tạo + thời gian |
| 6 | Footer bar | Button "Sửa" → navigate edit |
| 7 | Footer bar | Button "Xuất Excel" → popup chọn cột → download |
| 8 | Tất cả form fields | Disabled |

### TC-10: BOM Tổng hợp
| Step | Thao tác | Kết quả mong đợi |
|------|----------|-------------------|
| 1 | Tạo BOM, chọn loại "Tổng hợp" | "Chọn hàng hoá" disabled |
| 2 | Click "Chọn BL con" | Popup hiện danh sách BOM Thành phần |
| 3 | Chọn BL con → lưu | Chip hiện mã + tên BOM con |
| 4 | Không có nút Import | Đúng |
| 5 | Lưu BOM | DB: bom_list_type=2, bom_list_relations có record |
| 6 | Edit → BL con hiện đúng | Thêm/bỏ BL con → save |
| 7 | Trang chi tiết | BL con hiện readonly, không có "Chọn BL con" |
| 8 | Đổi Thành phần → Tổng hợp | Hàng hoá clear, BL con enable |
| 9 | Đổi Tổng hợp → Thành phần | BL con clear, hàng hoá enable |
