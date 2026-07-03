# Design: Cập nhật luồng triển khai Dự án TKT

## Mục đích
Bổ sung 3 cách triển khai dự án TKT (`implementation_type`), thay đổi luồng giải pháp + báo giá theo từng loại.

## Scope tổng thể (4 Phase)

| Phase | Nội dung | Trạng thái |
|-------|---------|-----------|
| **A** | KD tự triển khai: tạo báo giá từ BOM (bỏ PricingRequest) + permission xem giá vốn + lock giá bán ERP | Done |
| **B** | Type 2: Phân quyền XD giá theo phòng/công ty + lọc duyệt BG theo dept/company | Đang làm |
| **C** | Báo giá trực tiếp (không GP, không BOM) — Type 1 tạo BG từ tab Dự án, form gộp sản phẩm+giá | Đang làm |
| **D** | (Dự phòng cho yêu cầu mở rộng) | Chưa làm |

## Hiện trạng đã implement

### DB + Entity
- Field `implementation_type` (tinyint, default=3) trên `prospective_projects`
- Constants: SELF=1, BY_DEPT=2, CROSS_DEPT=3
- FE: radio chọn trên form tạo/sửa dự án (ProjectInfoSection.vue)
- Lock: không đổi type khi đã có Solution/RequestSolution

### Type 1 (Tự triển khai) — đã có
- Chặn tạo YC làm GP (RequestSolutionService:185)
- KD tạo Solution: pm_id=self, has_modules=false, skip duyệt PM/Leader → nhảy "Đang triển khai"
- Hồ sơ phê duyệt GP: submit → auto approved
- Tiến trình dự án: dựa trên Solution status, không cần RequestSolution

### Type 2 (Triển khai theo phòng) — đã có
- Lock receive_dept = phòng KD phụ trách
- DS YC làm GP filter theo phòng
- Solution canReceive() check phòng

## Quyết định thiết kế
1. Giá niêm yết = giá Bán lẻ (price_type_id=1) từ bảng `product_unit_prices` trên ERP DB
2. Join: BomListProduct.erp_product_id → products.id → product_units(is_base=1) → product_unit_prices(price_type_id=1)
3. Permission-based ẩn giá vốn (không phụ thuộc implementation_type)
4. Lock giá bán hàng ERP áp dụng tất cả type (không chỉ type 1)
5. Hàng tạm = BomListProduct có erp_product_id = NULL → user toàn quyền giá

# Phương án triển khai dự án — Tự triển khai / Theo phòng / Liên phòng ban

**Người phụ trách:** @dnsnamdang
**Ngày tạo:** 2026-05-23
**Spec chi tiết:** `docs/superpowers/specs/2026-05-23-project-implementation-types-design.md`

---

## Mục tiêu

Bổ sung 3 phương án triển khai cho Dự án tiềm năng (TKT):

| Type | Tên | Ghi chú |
|---|---|---|
| 1 | Tự triển khai | KD tự làm GP + báo giá, không qua YC làm GP |
| 2 | Triển khai theo Phòng | Vẫn qua YC làm GP, phòng nhận = phòng của KD (lock) |
| 3 | Liên phòng ban | Luồng hiện tại — mặc định |

**Phase 1 scope** (feature này): chỉ tới bước **KD tạo Hồ sơ trình duyệt (auto-approve)**. Phần báo giá (pricing/quotation) cho type=1, type=2 tách phase sau.

## Scope phase 1

- Thêm field `prospective_projects.implementation_type` (tinyint default 3, lock sau khi có Solution/RS).
- Type=1:
  - KD tạo Solution trực tiếp từ màn dự án — bỏ qua RequestSolution.
  - Ép `has_modules=false`, `pm_id = KD`, `status = 7 Đang triển khai` ngay.
  - Hồ sơ trình duyệt: tạo = auto-approve, không qua bước duyệt.
  - `syncStatusBySolution` branch riêng cho type=1 (không phụ thuộc RequestSolution).
- Type=2:
  - Auto-fill `receive_dept = phòng người tạo dự án` + lock.
  - Filter list `RequestSolution` mở rộng: type=2 cho phép user cùng `receive_dept` (có permission `Tiếp nhận yêu cầu làm giải pháp`) nhìn thấy.
  - Các bước sau giống type=3.
- Type=3: giữ nguyên.
- Null-safe toàn bộ chỗ truy cập `solution->requestSolution->X` (do type=1 có `request_solution_id = null`).

## Quyết định lớn

1. **Lock `implementation_type`** sau khi có Solution hoặc RequestSolution — tránh xung đột nghiệp vụ.
2. **Type=1 ép `has_modules=false`** — luôn là "Solution không có hạng mục", KD tự làm hết, không có tab Module Review.
3. **Phòng của Solution type=1** = phòng người tạo dự án (`prospective_project.created_by` → employee.department_id).
4. **`internal_need_gp_date` type=1**: nhập tay khi tạo Solution (form thêm field).
5. **Quyền xem Solution type=1**: giữ logic hiện tại (`pm_id == auth` || `created_by == auth`) — không can thiệp, chỉ thêm null-safe cho nhánh `requestSolution`.
6. **Type=2 permission**: tái dùng `"Tiếp nhận yêu cầu làm giải pháp"`, không tạo permission mới. Cần gán cho ít nhất 1 user mỗi phòng KD.
7. **Type=1 Review Profile auto-approve**: vẫn cần BOM tổng hợp Hoàn thành để submit, nhưng skip bước "chờ TP duyệt" — tạo = `approved` ngay, Solution → `11 Đã duyệt GP`, ProspectiveProject → `5 Đã duyệt GP`.
8. **Phase 2 (sau)**: báo giá cho type=1, type=2 — quyền KD tự tạo báo giá từ BOM, ẩn giá vốn/tỷ suất, lấy bảng giá niêm yết từ ERP. Lúc đó mới bổ sung mapping các trạng thái `15 Chờ làm giá` / `13 Đã duyệt giá` / `17 Chốt GP` vào `syncStatusBySolution()`.

## Bảng nhảy trạng thái type=1

| Sự kiện | RequestSolution | Solution | ProspectiveProject |
|---|---|---|---|
| Tạo dự án (chọn type=1) | — | — | `1 Đang tạo` |
| Bổ sung thông tin | — | — | `2 Thu thập TT dự án` |
| KD tạo Solution | — | `7 Đang triển khai` | `4 Đang làm GP` |
| KD tạo Hồ sơ TĐ (có BOM hoàn thành) | — | `11 Đã duyệt GP` (skip 9) | `5 Đã duyệt GP` |

> **Phase 1 dừng ở đây**. Các trạng thái liên quan giá (`15 Chờ làm giá` / `13 Đã duyệt giá` / `17 Chốt GP`) tách qua phase báo giá — bỏ qua mapping ở `syncStatusBySolution()` cho type=1.

## Bảng nhảy trạng thái type=2

Giống type=3, chỉ khác lúc tạo `RequestSolution`: `receive_dept` lock = phòng KD.