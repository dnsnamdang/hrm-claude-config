# Màn Tạo phiếu gia hạn hàng giữ — "Không có hàng hóa" dù đang giữ hàng

@junfoke · Repo `TanPhatDev` · nhánh `master` · 17/09/2026

## Hiện tượng

QA báo: Nguyễn Thị Hải (SG, `employee_id = 828`) đang giữ hàng, ở màn **Hủy giữ hàng** vẫn
chọn được hàng, nhưng mở **Tạo phiếu gia hạn hàng giữ** thì bảng Chi tiết ra "Không có hàng hóa".

## Root cause (đã đối chiếu dữ liệu prod)

`PrepickExtendRequest::getDataToCreate()` lọc 4 điều kiện cộng dồn. Đếm trên prod ngày 17/09/2026:

| Bước lọc | Số dòng còn lại |
| --- | --- |
| Tổng dòng `prepick_details` của nhân viên 828 | 773 |
| `qty > 0` | 36 |
| `+ company_id = công ty đang chọn (4)` | 25 |
| `+ expire_date <= hôm nay + warning_day (7) = 24/09` | **0** |

Hạn giữ gần nhất của chị Hải là **25/09**, lệch đúng 1 ngày so với ngưỡng ⇒ màn rỗng.

Màn **Hủy giữ hàng** không có điều kiện hạn (`PrepickCancelRequestsController::searchProduct`,
FE không gửi `company_id`) nên vẫn hiện đủ hàng — đó là lý do 2 màn lệch nhau.

## Quyết định đã chốt (17/09/2026, user chốt)

1. **Bỏ hẳn điều kiện `expire_date <= hôm nay + warning_day`** ở màn Tạo phiếu gia hạn.
   Hiện mọi hàng đang giữ (`qty > 0`), user tự chọn dòng cần gia hạn; cột "Hạn giữ hiện tại"
   trong bảng đã đủ cho user biết dòng nào sắp hết hạn.
2. **Giữ nguyên điều kiện `company_id`.** `EmployeeInfo::getCompanyIdAttribute()` trả về
   `session('current_company')` khi nhân viên thuộc nhiều công ty, nên đây là công ty user
   ĐANG CHỌN chứ không phải giá trị cứng trong DB. Chị Hải được gán cả công ty 1 (HN) và 4 (SG)
   trong `company_employees` ⇒ đổi công ty trên thanh chọn là thấy 11 dòng hàng HN.
   Không sửa query, không nới điều kiện.
3. Giữ nguyên `employee_id` (chỉ gia hạn hàng đứng tên mình) và `qty > 0`.

## Phạm vi KHÔNG đụng tới

`warning_day` còn dùng ở cảnh báo dashboard (`HomeController`), lệnh cron `PrepickWarning` /
`BorrowWarning`, báo cáo tồn/mượn (`WarehouseInfosController`, `PrepickDetail::searchByFilter`,
`BorrowIndexReportService`) — đó là chức năng cảnh báo sắp hết hạn, đúng thiết kế, giữ nguyên.
