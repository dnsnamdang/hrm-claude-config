# Design tóm tắt — Gói thầu gộp nhiều báo giá

> Phụ trách: @khoipv · 2026-07-07 · Đánh giá lại toàn diện: 2026-07-08 · Chưa code
> Spec đầy đủ: `docs/superpowers/specs/2026-07-07-bid-package-multi-quotation-design.md`

## Mục tiêu
Cho phép **1 gói thầu tạo từ NHIỀU báo giá cùng khách hàng** (hiện đang khóa 1 gói thầu ↔ 1 báo giá qua `bid_packages.quotation_id`).

## Quyết định lớn
- Nhiều báo giá **cùng KH**, **khác dự toán được** (báo giá ↔ dự toán đang 1-1).
- **Không có báo giá chính** — các báo giá ngang hàng.
- Chọn nhiều báo giá **trong form thêm gói thầu** (ô báo giá → multi-select, chặn khác KH).
- Tính "nhiều báo giá" **chỉ ở khâu gói thầu**. Thầu → HĐ **giữ logic cũ**.
- Đường **ngoài thầu** (báo giá → HĐ trực tiếp) **giữ nguyên 1-1**, không sửa.

## Mô hình dữ liệu
- Bảng nối mới `bid_package_quotations (bid_package_id, quotation_id, project_id)` — index, **không FK**, **không** `is_primary`.
- `bid_packages.quotation_id/project_id` = **NULL** với gói thầu gộp; giữ đơn với gói thầu 1 báo giá (tương thích ngược).
- HĐ từ gói thầu gộp: `quotation_id = NULL`, nối qua `bid_package_id`.
- **Đề xuất mới (chờ chốt)**: ghi bảng nối cho MỌI gói thầu mới + **backfill** dữ liệu cũ → mọi query chỉ join bảng nối 1 kiểu, khỏi fallback 2 nhánh.

## Kết quả đánh giá lại 2026-07-08 (quét code 3 agent)
**Hướng bảng nối + NULL vẫn đúng**, được củng cố: (1) đã có tiền lệ gói thầu không báo giá (nhảy thầu `project_type==3`); (2) luồng tạo HĐ từ gói thầu **tự khớp không cần sửa** — BE fill từ request, FE lấy nguyên `bid_package.quotation_id` (NULL → HĐ tự null).

**Phạm vi BE lớn hơn bản đầu:**
- 🔴 Vòng đời trạng thái phải lặp N báo giá + N dự toán ở **6 điểm** (bản đầu chỉ ghi 2): tạo/giao NV (`updateStatus`), **phân công lập HĐ** (`assignEmployeeCreateContract:734,744-749`), **kết xuất thầu** (`BidPackageController:162-177`), **hủy/trượt thầu** (`:247-265`), xóa (`delete` — vá luôn lỗ hổng không revert).
- 🔴 FE: `addQuotation` hiện **ghi đè** groups (L950) → phải append/merge; `QuotationModal` chọn đơn → multi.
- ⚠️ **3 kết luận "không phải sửa" của bản đầu là SAI**: `lifecycleReport` (gt_agg GROUP BY project_id → đếm thiếu), related-data báo giá/dự toán (query cột đơn → không thấy gói gộp), `report-project-contract` (whereIn quotation_id → mất mã thầu/HĐ).
- 🟠 Mới phát hiện: dashboard Category (9 chỗ `whereHas('project')` → undercount), filter theo báo giá/dự toán ở 4 màn, `saleProductReport` nhánh theo dự toán, popup `saleProductBgBidPackages`, reverse resource (tên NV lập thầu), `quotation_products` phải trả union.
- 🟢 Vẫn không sửa: luồng tạo HĐ (cả 2 đường), từ chối lập gói thầu, Contract*Resource, Vuex store.

## Đã chốt 2026-07-08 (spec mục 5b)
- **Gộp bảng hàng hóa: APPEND tách nhóm** nguyên trạng theo từng báo giá — không hợp nhất nhóm trùng tên, không cộng dồn SL; badge mã BG trên header nhóm; cảnh báo mềm khi trùng mặt hàng; bỏ bớt BG = gỡ trọn nhóm theo `group.quotation_id`.
- **`price_type_min/max_id` khác nhau giữa các BG**: để TRỐNG + cảnh báo, không chặn.
- Rule field header khi gộp: customer = BG đầu, project = NULL (>1 BG), union productIds/array_product_id, cộng sum_product_qty, gộp supplier_auths.

## Còn treo (6 quyết định — xem spec mục 7)
Bỏ bớt báo giá → revert 7 · chặn khác KH · **backfill bảng nối (đề xuất CÓ)** · **chỉ áp dụng bid_type==1 (đề xuất đúng)** · **ContractAssignEmployee.quotation_id khi gộp** · **phạm vi sửa nhóm 🟠 (1 đợt hay 2 đợt)**.
