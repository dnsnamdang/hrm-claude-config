# Danh mục khu vực kinh doanh — design (tóm tắt)

> Người phụ trách: @junfoke · Redmine [#11623](http://quanly.dnsmedia.vn/issues/11623) · Nhánh `gop_db`
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-10-business-areas-design.md`
> Nguồn yêu cầu: file demo `danh-muc-khu-vuc-kinh-doanh.html` đính kèm issue (bản lưu: `C:\Users\Legion\.pw-mcp\out-a\kvkd_demo.html`).

## Mục tiêu

Gom nhiều phường/xã của 1 Tỉnh/TP thành 1 **khu vực kinh doanh**.
- 1 Tỉnh/TP có nhiều khu vực · 1 khu vực gồm nhiều phường/xã (cùng tỉnh) · 1 phường/xã thuộc **tối đa 1** khu vực.
- Cơ cấu chọn: Quốc gia → Vùng (bảng `areas`) → Tỉnh/TP. Khu vực chỉ LƯU `province_id`; Vùng / Quốc gia suy ra từ tỉnh.

## Phạm vi

Màn MỚI `/human/business-areas` (menu Danh mục › Địa lý › Khu vực kinh doanh), BE `Modules/Human`, route `/human/business-areas`.
Danh sách + bộ lọc + popup Tạo/Sửa/Xem (gán phường/xã bằng bảng tick) + Khoá/Mở khoá + Xoá + Lịch sử + Xuất Excel + Import Excel.

## Quyết định đã chốt (10/10/2026, user)

| # | Câu hỏi | Chốt |
| --- | --- | --- |
| 1 | Phân quyền | **Không gate quyền** (giống cả nhóm Địa lý). Không phân quyền theo cấp. |
| 2 | Sửa/Xoá khi đang Khoá (demo cho phép) | **Theo quy tắc project**: đang Khoá → ẩn Sửa/Xoá, BE trả 423; xoá = xoá cứng, phường/xã trở về Chưa gán. |
| 3 | Import Excel (demo chưa đặc tả) | **Làm import cơ bản**: Tên khu vực*, Tỉnh/TP*, Phường/xã (tên cách nhau `;`), Ghi chú. |
| 4 | Nhãn cấp trên Tỉnh/TP | **"Vùng"** (commit `đổi danh mục khu vực->vùng` của khoipv đang ở `develop`, chưa vào `gop_db`). |
| 5 | Lưu gán phường/xã | Bảng nối `business_area_wards` có `UNIQUE(ward_id)` — KHÔNG thêm cột vào bảng ERP `wards`. |
| 6 | Bỏ trường Mã số | Theo demo (khách yêu cầu bỏ). |

## Lệch demo có chủ đích

- Demo cho Sửa/Xoá khi Khoá → làm theo CLAUDE.md (mục 2 ở trên).
- Demo popup Xem có nút "Sửa" ở footer → giữ (khi bản ghi Hoạt động).
