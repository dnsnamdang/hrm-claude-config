# Dashboard Kinh doanh — Tóm tắt

> Spec đầy đủ: `docs/superpowers/specs/2026-06-28-sale-dashboard-design.md`
> Phụ trách: @manhcuong

## Mục tiêu
Trang tổng quan phân hệ Kinh doanh (`Modules/Sale` + `pages/sale/dashboard`), dữ liệu tự co giãn theo cấp quyền user.

## Các khối
1. **4 KPI card** (chỉ con số + link): Báo giá chờ duyệt, Hợp đồng chờ duyệt (→ màn approval), Doanh số HĐ đã duyệt (trong kỳ), Tỉ lệ chốt.
2. **Doanh số theo thời gian** — bar nhóm theo tháng, 2 series (Báo giá vs Hợp đồng đã duyệt, đo `total_amount` status=3 theo `approved_at`).
3. **Tỉ lệ chuyển đổi Báo giá→HĐ** — số lượng + giá trị + %.
4. **Top 10 khách hàng** — bar ngang theo tổng giá trị HĐ đã duyệt.

## Bộ lọc
Khoảng ngày (mặc định đầu năm → hôm nay) + Công ty/Phòng (`V2BaseCompanyDepartmentFilter`), giới hạn trong phạm vi quyền.

## Quyết định chốt
- **A.** Permission MỚI `1123 — Xem dashboard kinh doanh` (gate route + menu).
- **B.** Logic scope theo cấp viết RIÊNG cho Dashboard (nhân bản pattern `getListForUser`, KHÔNG sửa hàm chung).
- 1 endpoint tổng hợp `GET /v1/sale/dashboard` trả tất cả khối; tính bằng SQL aggregate.

## Phạm vi loại trừ (YAGNI)
Không export, không drill-down, không realtime/cache, không chart phân bố trạng thái.
