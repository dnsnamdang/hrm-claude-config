# Đưa style menu của nhánh `gop_db` sang `tpe-develop-assign`

**Người phụ trách:** @dnsnamdang · **Nhánh:** `feature/menu-style-hub` (checkout từ `tpe-develop-assign`, chỉ repo `hrm-client`)
**Spec chi tiết:** `docs/superpowers/specs/2026-08-17-menu-style-hub-design.md`

## Mục tiêu

Bê **giao diện** menu của nhánh `gop_db` sang `tpe-develop-assign`. **Nội dung menu và danh sách
phân hệ giữ nguyên 100%** — không thêm phân hệ mới, không thêm/bớt/đổi tên mục menu nào.

## Phạm vi (3 phần)

| # | Phần | Trước | Sau |
| - | ---- | ----- | --- |
| A | Màn chọn phân hệ `/` | lưới card trắng 3 cột | bố cục "bông hoa" nền navy gradient (`layouts/system.vue` + `pages/index.vue`) |
| B | Sidebar trái phân hệ Dự án & giao việc, Đào tạo | cây tree UBold | rail navy + panel menu con bay ra (kiểu MISA) |
| C | Popup chuyển phân hệ ở topbar (icon lưới) | lưới 3 cột phẳng | chia nhóm, huy hiệu tròn màu nhóm, tô sáng phân hệ đang mở |

## Quyết định chính

1. **Registry `components/subsystems.js`** (mới, rút gọn từ `gop_db`) — gom 7 phân hệ HRM + ERP về
   một chỗ để 3 phần A/B/C dùng chung tên, icon, nhóm, link. Field `menu` trỏ thẳng vào mảng menu
   cũ (`menu.js`, `menu-sidebar.js`, `default-menu/*`) — **không chép lại nội dung menu**.
2. **Chia nhóm** (dùng cho bông hoa + popup): LÕI HỆ THỐNG = HCNS, ERP · 1. NHÂN SỰ = Chấm công,
   Tính lương, Quản lý cơm · 2. VĂN PHÒNG SỐ = Dự án & giao việc, Đào tạo, Quyết định.
   Chỉ có 2 nhóm nghiệp vụ nên bông hoa chạy biến thể `stage--duo`: 2 cánh trái/phải thay vì 4 góc.
3. **Sidebar hub chỉ bật cho `assign` + `training`** (`HUB_SUBSYSTEMS` trong `subsystem-menu/hub.js`).
   5 phân hệ còn lại vốn dùng topbar ngang — kéo chúng sang sidebar là đổi cấu trúc điều hướng,
   không còn là "đổi style".
4. **Menu của rail suy thẳng từ cây menu cũ** (`deriveHubGroups`) → 1 phân hệ vẫn chỉ có 1 nguồn menu.
5. **`sale-theme.scss` port RÚT GỌN**: chỉ lấy phần rail sidebar + topbar + panel menu. Bỏ hẳn phần
   `gop_db` đổi header bảng / tiêu đề card / `.info-table` / chip — nằm ngoài phạm vi "style menu".

## Điểm cần biết

- Badge đỏ số lượng ở mục "Báo cáo tiến độ task" (phân hệ Dự án & giao việc) **không có** trên
  sidebar hub — bản `gop_db` cũng vậy. Cần thì phải làm thêm.
- 2 mục menu Đào tạo gate theo **vai trò** (`isShow` là chuỗi) đã được xử lý riêng để rail hiện
  giống hệt sidebar cũ.
