# Dự án cha - dự án con (Redmine #10882)

**Phụ trách:** @cuong61n · **Branch:** `tpe-develop-assign` (cả 2 repo)
**Spec chi tiết:** [docs/superpowers/specs/2026-07-27-du-an-cha-con-design.md](../../docs/superpowers/specs/2026-07-27-du-an-cha-con-design.md)
**URD:** https://docs.google.com/document/d/1-Unvkpd76Gs7wNYMoUKCkgFRvHNihKRKM2O7FXEzLHY/edit

## Mục tiêu

Gom nhiều dự án TKT nhỏ (theo khoa/phòng của khách hàng) về dưới một "dự án cha" đại diện gói thầu tổng, để sale chính / PM theo dõi tập trung ngân sách và tiến độ.

## Scope

Task gốc #10882 gồm 3 khối lớn, chia 3 phase:

| Phase | Nội dung | Trạng thái |
|---|---|---|
| **1** | Dự án cha - con: loại dự án, form cha rút gọn, kế thừa/khóa trường, tree view danh sách, màn chi tiết cha 3 tab, đóng cascade | **XONG** (code + test) |
| **2** | Báo giá tổng: gộp báo giá con đã duyệt, Section kéo-thả, luồng duyệt 1 cấp, In/Excel + khoá GG/tiền tệ/bảng giá ở báo giá con | **Đang làm** — [spec](../../docs/superpowers/specs/2026-07-28-bao-gia-tong-design.md) |
| 3 | Hợp đồng tổng + ràng buộc loại trừ + đồng bộ trạng thái cha theo API ERP | Chưa bắt đầu (phụ thuộc API ERP) |

## Quyết định lớn (Phase 2)

- **Dùng lại bảng `quotations`** + cờ `is_summary`, không tạo bảng báo giá riêng. Section = `quotation_groups` (đã có `parent_id` + `sort_order`), dòng hàng snapshot vào `quotation_product_prices` (`bom_list_product_id` nullable, đã có 315 dòng NULL sẵn). Nhờ đó tái dùng được ngay: `calculateTotals`, `calculateValidityDate` (đã đúng công thức MIN của URD), mẫu in, xuất Excel, lịch sử.
- **Luồng duyệt 1 cấp** (Đang tạo → Chờ duyệt → Đã duyệt/Từ chối), người duyệt là **TP**. KHÔNG tính cấp tự động theo giá trị/TSLN, KHÔNG đồng bộ ERP, KHÔNG cascade đổi trạng thái dự án — 2 thứ sau sẽ đẩy sai trạng thái dự án cha và gây trùng dữ liệu ERP.
- **Không theo dõi báo giá nguồn thay đổi.** User tự tạo bản mới; tạo bản mới là các bản cũ cùng dự án cha **Hết hiệu lực ngay**.
- Bảng phụ mới duy nhất: `quotation_total_sources` (truy vết nguồn ↔ Section).
- Phạm vi trạng thái tới **Trúng thầu**; "Đã tạo hợp đồng" để Phase 3.
- Báo giá của dự án con: **kế thừa + khoá cứng** Giảm giá / Tiền tệ / Bảng giá từ dự án cha (DB hiện có 0 báo giá thuộc dự án con → không ảnh hưởng dữ liệu cũ).

**Rủi ro chính Phase 2:** dùng chung bảng `quotations` nghĩa là phải rà loại `is_summary = 1` khỏi mọi luồng báo giá cũ (danh sách Quản lý báo giá, hàng đợi duyệt giá, tab báo giá dự án con, view hàng hoá dự án, report, đồng bộ ERP). Đúng loại lỗi đã gặp ở Phase 1 khi dự án cha lọt vào báo cáo.

## Các quyết định lớn (Phase 1)

- **3 loại dự án:** độc lập (luồng cũ, mặc định) / cha / con. UI = checkbox "Là dự án cha" + select "Dự án cha"; để trống cả 2 = độc lập.
- **Enum trạng thái riêng cho cha:** 1=Đang tạo, 2=Đang thực hiện, 7=Trình duyệt hợp đồng, 8=Thương thảo DA/HĐ, 9=HĐ đủ điều kiện thực hiện, 10=Nghiệm thu & Thanh lý, 11=Đóng/Hủy, 12=Kết thúc & lưu trữ. Id trùng số với enum dự án thường nhưng khác tên ⇒ mọi chỗ render tên phải phân nhánh theo `is_parent_project`.
- **Form cha rút gọn:** ẩn hết trường ngoài URD (Ứng dụng, Ngành/LVKH, Nguồn vốn, ngày GP, form template, địa chỉ, ưu tiên, giai đoạn).
- **Mã cha riêng:** `{Mã phòng}.{Năm}.DAC{seq}` → `KD.2026.DAC001`, chuỗi đếm riêng.
- **Kế thừa cha → con (read-only ở con):** khách hàng, KH thụ hưởng cuối, giảm giá, tiền tệ, bảng giá (`price_type_id`). Sale chính kế thừa nhưng cho chọn lại.
- **Chặn cứng:** tổng ngân sách con > ngân sách cha; timeline con ngoài khung cha.
- **Đổi loại dự án / đổi cha:** chỉ khi ở trạng thái "Đang tạo" (cha thêm điều kiện chưa có con).
- **Đóng cha:** điều kiện như hiện tại (mọi trạng thái trừ đã đóng) + cascade gọi `closeProject()` cho từng con, bỏ qua check quyền khi cascade.
- **Danh sách:** tree view, phân trang theo dòng cấp 1, con lazy load khi expand.
- **Phân quyền:** dùng chung quyền dự án TKT, không thêm permission mới.

## Lưu ý kỹ thuật

- `prospective_projects.parent_id` **đã tồn tại** nhưng chỉ dùng để chặn xóa (`ProspectiveProject.php:292`). Không có API, không có logic kế thừa.
- FE `RelatedSection.vue:29-40` đã có sẵn UI "Chọn dự án cha" nhưng nguồn dữ liệu là **mock hardcode** ở `add.vue:236-244` → thay bằng API thật, giữ nguyên vị trí.
- Migration DDL **không** bọc `DB::transaction`.

## Không làm ở Phase 1

Báo giá tổng, tab Báo giá ở màn cha, khóa 3 trường trên màn báo giá con (→ Phase 2). Hợp đồng tổng, trigger trạng thái 7→12 theo ERP (→ Phase 3).
