# Khách hàng sử dụng cuối cùng — chọn nhiều (tóm tắt)

- **Người phụ trách:** @khoipv
- **Ngày:** 2026-07-07
- **Spec chi tiết:** [`docs/superpowers/specs/2026-07-07-khach-hang-cuoi-cung-chon-nhieu-design.md`](../../docs/superpowers/specs/2026-07-07-khach-hang-cuoi-cung-chon-nhieu-design.md)

## Mục tiêu
Trường "Khách hàng sử dụng cuối cùng" từ chọn 1 → **chọn nhiều**. Tạo chứng từ từ dự toán có khách hàng → **auto** đưa khách hàng chính vào danh sách. Vẫn thêm/xóa được (kể cả dòng auto).

## Phạm vi
3 module: Báo giá (`quotations`), Hợp đồng (`contracts`), Gói thầu (`bid_packages`) — mỗi module: `add` + `edit` + `GeneralComponent`.

## Quyết định lớn
- **Lưu JSON:** thêm cột `customer_last_used` (json, mảng `[{id, name}]`) làm nguồn chính.
- **Giữ cột cũ** `customer_last_used_name` = tên nối `", "` (list/report/export không phải sửa), `customer_last_used_id` = id phần tử đầu.
- **UI chip/tag**, tái dùng `CustomerModal` single-pick → append + chống trùng theo id.
- **Auto từ dự toán:** trong `addProject` đẩy `customer_id/customer_name` vào mảng (dedupe), xóa được.
- Không đụng report/list/export.

## Không làm
- Không cho nhập tên tự do (chỉ chọn từ danh sách khách hàng).
- Không sửa màn report/list.
