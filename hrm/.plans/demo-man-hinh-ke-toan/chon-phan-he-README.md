# Demo màn Chọn phân hệ (2 cấp)

File: `demo/chon-phan-he.html` — nằm chung folder bộ demo kế toán, dùng chung `assets/style.css` + Remix Icon.
Nguồn dữ liệu: infographic `erp_14.png` (PHẦN MỀM ERP).

## Logic điều hướng
- **Cấp 0**: lõi hệ thống (3 phân hệ core: Thông tin nhân sự / Danh mục chung / Quản trị hệ thống)
  nằm giữa dạng 3 múi; **4 nhóm** nằm trên circle.
- Click 1 nhóm → **Cấp 1**: tên nhóm vào giữa (hub gradient màu nhóm), các phân hệ của nhóm nằm
  trên circle; có breadcrumb "← Quay lại / <tên nhóm>".

## Nhóm & phân hệ (theo ảnh mẫu)
| Nhóm | Màu | Phân hệ |
|---|---|---|
| 1. Nhân sự - Tiền lương | xanh dương | Chấm công, Quản lý cơm, Tính lương, Bảo hiểm xã hội, Thuế TNCN, Tuyển dụng |
| 2. Hành chính | xanh lá | Văn phòng số, Quyết định, Quản lý tài sản, Đánh giá KPI, Đào tạo |
| 3. Sản xuất – Cung ứng | cam | Quản lý sản xuất, Mua hàng, Kho, Vận chuyển |
| 4. Hoạt động kinh doanh | tím | Bán hàng, CSKH, Quản lý công việc, Tài chính |

## Hiệu ứng
- Hover node vòng ngoài: phóng to + đổ nền màu + hiện chip.
- Hover 3 múi lõi: múi bung ra + sáng, 2 múi còn lại mờ.
- Auto-fit: luôn gọn 1 màn hình, không scroll.

Ảnh: `preview-chon-phan-he-lv0.png`, `preview-chon-phan-he-lv1.png`.
