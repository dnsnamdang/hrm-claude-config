# Tách/gộp phân hệ ERP + HRM theo Sơ đồ tổng thể v1.6

**Người phụ trách:** @junfoke — 2026-07-30

## Mục tiêu

Quy hoạch lại toàn bộ phân hệ của ERP + HRM theo `Sơ đồ tổng thể phần mềm_v1.6_24072026.png`,
rồi dựng base cho các phân hệ mới ở cả BE (`hrm-api`) và FE (`hrm-client`).

Giai đoạn 1 (đã xong): khung phân hệ, menu, gán link các màn HRM đã có, màn chọn phân hệ.
Giai đoạn 2 (chưa làm): di chuyển code màn sang route mới.

## Scope

- **24 phân hệ** theo sơ đồ, chia 5 nhóm (Lõi hệ thống / Nhân sự / Văn phòng số /
  Sản xuất - cung ứng / Kinh doanh - tài chính) + 1 card ERP.
- **17 phân hệ mới**: master-data, admin, insurance, tax, recruitment, kpi, legal, asset,
  iso, operation, production, sale, purchase, warehouse, transport, customer-care, finance.
- 7 phân hệ cũ giữ nguyên: human, timesheet, rice, payroll, decision, training, assign.
- Không đưa E-learning vào (đang xây dựng).

## Quyết định chính

- **Tên nhóm và tên phân hệ lấy đúng sơ đồ**, không đặt lại (Danh mục chung — không phải
  "Danh mục dùng chung"; Quyết định — không phải "Ban hành văn bản nội bộ"; Bảo hiểm xã hội; Đào tạo).
- **Registry trung tâm** `components/subsystems.js` là nguồn duy nhất khai báo phân hệ.
  `resolveSubsystem(path)` tìm phân hệ theo **link có trong menu trước**, rồi mới xét slug —
  nhờ đó menu phân hệ mới trỏ được vào route cũ mà vẫn hiển thị đúng menu.
  Bất biến: **mỗi link chỉ thuộc đúng 1 phân hệ**.
- **Phân hệ cũ giữ menu ngang, phân hệ mới đi menu dọc hết.** Màn nào chuyển sang phân hệ mới
  thì đổi luôn `layout` của page.
- Tạo layout riêng `layouts/subsystem.vue` thay vì dùng `default-sidebar`, vì 2 layout nạp bộ
  SCSS khác nhau — 26 màn chuyển từ human/decision sang cần `custom.scss` + `custom-form.scss`.
- **Quản lý hàng hoá / Kho / Vận chuyển / Mua hàng giữ nguyên bên ERP** (không gộp), nhưng vẫn
  dựng base rỗng trên HRM để đủ card theo sơ đồ.
- `assign` tách đôi: Dự án TKT → `sale`; giao việc/công tác/task/meeting ở lại `assign`.
- Bảo hiểm tách khỏi `decision` → `insurance`.
- Icon phân hệ dùng **SVG tự vẽ**, không dùng icon font (dự án nạp 2 bản Remix Icon xung đột).

## Spec chi tiết

docs/superpowers/specs/2026-07-30-tach-phan-he-erp-hrm-design.md

## Nguồn dữ liệu

| Nguồn | Vai trò |
| --- | --- |
| `Sơ đồ tổng thể phần mềm_v1.6_24072026.png` | Chuẩn tên nhóm + tên phân hệ |
| `Bảng xử lý và test dữ liệu gộp cổng + sơ đồ tách phân hệ.xlsx` | Sheet `Gộp phân hệ ERP-HRM` (611 dòng) |
| `D:\CompanyProject\Document\erp-menu-inventory.xlsx` | 304 chức năng ERP chuyển sang HRM đợt này |
| `TanPhatDev/resources/views/layouts/topmenubar.blade.php` | Menu ERP thật (không phải `sidebar.blade.php`) |
