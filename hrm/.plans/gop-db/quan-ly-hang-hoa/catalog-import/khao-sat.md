# Import cây catalog kinh doanh từ Excel — khảo sát (16/10/2026)

**Trạng thái: TẠM DỪNG** — user xử lý trước file quan hệ Nhóm hàng hoá (cũ) → Loại hàng hoá (mới).
Chưa viết code, chưa chạy gì vào DB.

## File nguồn
`Cây danh mục catalogue.xlsx` (Zalo, 5,7 MB) — bản chép đọc thử nằm ở scratchpad phiên 16/10, KHÔNG nằm trong repo.

| Sheet | Lĩnh vực ghi trong file | Chương | Mục | Tiểu mục | Ghi chú |
|---|---|---|---|---|---|
| Dữ liệu cũ | Dịch vụ ô tô | 12 | 80 | 474 | + cột "Sản phẩm (Cấp 5)" 1.037 dòng — bản cũ, đề xuất BỎ |
| Cây Lĩnh vực-Chương | 7 lĩnh vực | — | — | — | sheet tổng quan; cột Chương là ghi chú phụ trách ("Power, Green", "Phòng dự án") — đề xuất BỎ |
| Cây danh mục Dịch vụ ô tô | Dịch vụ ô tô | 15 | 118 | 578 | |
| Cây danh mục năng lượng PW | Năng lượng | 11 | 135 | 767 | bộ Chương gần trùng "công nghiệp PW" |
| Cây danh mục giáo dục DA1 | Giáo dục - Đào tạo | 6 | 48 | 1.018 | có Chương rác "…." |
| Cây danh mục công nghiệp PW | Công nghiệp | 10 | 20 | 120 | |
| Cây danh mục công nghiệp | (trống) | 4 | 8 | 7 | nhà máy ô tô / xe máy / xe tải |
| Cây danh mục môi trường | Môi trường | 7 | 5 | 0 | có Mục, chưa có Tiểu mục |

Ô gộp kiểu "chỉ ghi ở dòng đầu" ⇒ cấp cha để trống ở các dòng sau, phải mang giá trị xuống.

## DB (`hrm_erp_giacty`, 16/10)
- Lĩnh vực = `internal_business_scopes` (8 dòng: Khác, Công nghiệp, Môi trường, Giáo dục đào tạo, Tiện ích công cộng,
  Năng lượng và hạ tầng, Dịch vụ ô tô, Giải pháp quản trị số). Được `hrm_scopes` (35), `meeting_investment_demands` (153),
  `meeting_investment_scopes` (146) dùng ⇒ KHÔNG đụng, chỉ ánh xạ theo tên.
- `chapters` 66 (65 chưa gắn lĩnh vực — dữ liệu ERP cũ), `job_groups` 107, `job_clusters` 3.
- FK trỏ vào: `product_group_classifies` (1.019 dòng — Nhóm hàng cũ ↔ catalog, FK chapter/job_group/job_cluster),
  `product_business_catalogs` (21 dòng — Hàng hoá ↔ Tiểu mục).

## Đã chốt
1. **Không truncate** — giữ dữ liệu cũ (user 16/10). ⇒ seeder kiểu tìm-hoặc-tạo theo (tên, cha), chạy lại không nhân bản.
2. Nhóm hàng sẽ đổi sang Loại hàng hoá — user cung cấp file mapping Nhóm hàng (cũ) → Loại hàng hoá (mới), xử lý TRƯỚC.

## Còn hỏi (lần lượt)
2. Sheet nào nhập (đề xuất 6 sheet cây; xử lý "năng lượng PW" vs "công nghiệp PW"; sheet "công nghiệp" thiếu Lĩnh vực).
3. Ánh xạ tên Lĩnh vực file → DB: "Giáo dục - Đào tạo" → "Giáo dục đào tạo"? "Năng lượng" → "Năng lượng và hạ tầng"?
4. Chuẩn hoá tên: giữ số thứ tự "1. …" trong tên Chương? cắt khoảng trắng; bỏ dòng rác "…."; so trùng không phân biệt hoa thường?
5. Phạm vi code: repo/nhánh (hrm-api `feat/chuyen-doi-hang-hoa`), seeder đọc file từ đâu (đặt file vào repo hay truyền đường dẫn),
   chạy vào DB nào.
