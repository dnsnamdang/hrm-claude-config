# Phiếu phân chia thị trường theo phòng ban — design (tóm tắt)

> @junfoke · Redmine [#11694](http://quanly.dnsmedia.vn/issues/11694) (phụ thuộc #11623 Danh mục khu vực kinh doanh) · nhánh `gop_db`
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-14-division-market-department-design.md`
> Nguồn: demo `phieu-phan-chia-thi-truong-theo-phong-ban (3).html` (bản lưu `C:\Users\Legion\.pw-mcp\out-b\pptt_demo.html`) + màn ERP `Division/DivisionMarketDepartmentController`.

## Mục tiêu

Port màn ERP sang HRM (menu Bán hàng › Kế hoạch › Phiếu phân chia thị trường › Theo phòng ban) và đổi cách chia:
Đơn vị (cả phòng HOẶC 1 bộ phận) → Tỉnh/TP (SL NV tối đa / Không giới hạn) → Khu vực kinh doanh (nhận trọn phường/xã) → Hãng xe (tất cả hoặc chọn hãng, không bắt buộc).

## Quyết định đã chốt (14/10/2026, user)

| # | Câu hỏi | Chốt |
| --- | --- | --- |
| 1 | Lưu dữ liệu | **Dùng lại 4 bảng ERP** `division_market_department*` + thêm cột (bộ phận; SL NV tối đa / không giới hạn ở tỉnh; `business_area_id` ở phường/xã). Khu vực lưu = bung toàn bộ phường/xã (kèm cờ hãng) ⇒ ERP phiếu nhân viên, báo cáo, hợp đồng vẫn đọc được. |
| 2 | 13 phiếu cũ (phường/xã lẻ) | **Tự gom theo khu vực**: phường/xã thuộc khu vực KD gom vào dòng khu vực; phường/xã chưa thuộc khu vực nào hiện dòng "Chưa thuộc khu vực" (chỉ xem, Sửa+Lưu thì bỏ). Chỉ xem không đổi dữ liệu. |
| 3 | Quyền | **4 quyền mới** (guard api, type 23 Bán hàng): Tạo (tạo/sửa/xoá) · Duyệt (Duyệt/Huỷ duyệt) · Xem tổng công ty · Xem công ty. Không quyền xem ⇒ chỉ phiếu mình lập (như ERP). Không phân quyền theo cấp khác. |
| 4 | Công ty cấu hình "theo tỉnh" | **Mọi công ty theo khu vực KD** — cấu hình `companies.market_division_type` không còn tác dụng với màn này. |

## Theo demo (khác ERP)

- Phân theo Phòng hoặc Bộ phận; loại trừ cấp giữa các phiếu ĐÃ DUYỆT cùng phòng (chặn Lưu & Duyệt). Bỏ ràng buộc "mỗi phòng 1 phiếu" của ERP.
- Trùng khu vực với đơn vị khác: chỉ cảnh báo ở dòng tỉnh, không chặn.
- SL NV tối đa theo tỉnh, ≤ số NV của đơn vị. Phiếu Đã duyệt khoá sửa/xoá; có Huỷ duyệt; Lưu và duyệt.
- Form là màn riêng (Tạo/Sửa/Chi tiết), In = popup xem trước, lịch sử dùng bảng chung `catalog_histories`.

## Không làm trong task này

- Phiếu phân chia theo nhân viên (vẫn ở ERP). ERP tự đồng bộ phường/xã sang phiếu nhân viên khi lưu phiếu phòng ban — HRM KHÔNG chạy job đó.
