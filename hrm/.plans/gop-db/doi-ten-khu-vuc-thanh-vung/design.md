# Đổi tên danh mục "Khu vực" → "Vùng"

Người phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo)

## Mục tiêu
Đổi toàn bộ chữ hiển thị của danh mục `areas` từ "Khu vực" thành "Vùng" (menu, màn danh sách, popup, bộ lọc, cột, import/export Excel, lịch sử, câu lỗi BE).

## Quyết định
- CHỈ đổi chữ (label/message/comment). KHÔNG đổi tên bảng `areas`, cột `area_id`, route, key `area_name` → không migration, không ảnh hưởng dữ liệu.
- Import Excel: header mới "Tên vùng"; GIỮ alias cũ "Tên khu vực"/"Khu vực" để file mẫu cũ vẫn import được.
- KHÔNG đụng các chữ "khu vực" không thuộc danh mục: "Khu vực 1/2" của báo giá dự án cha, khối "KHU VỰC ... " trong file Excel báo giá, tên báo cáo bán hàng ở sale-hub, bảo hiểm, địa chỉ, migration cũ.
