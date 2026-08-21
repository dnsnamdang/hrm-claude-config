# Thiết kế lại màn Quản lý phân quyền HRM

> Tóm tắt. Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-14-thiet-ke-lai-phan-quyen-design.md`
> Nhánh: `gop_db` (cả hrm-api + hrm-client).

## Mục tiêu

Thiết kế lại màn quản lý phân quyền, đưa về phân hệ **"Quản trị hệ thống"** (`admin`, type 10 — đã khai sẵn ở `subsystems.js` nhưng menu còn placeholder). Giải quyết 4 pain hiện tại:
- Quá nhiều quyền (617 permission, phần lớn là "xem theo cấp" nở ra nhiều dòng).
- Giao diện xấu (cây checkbox 3 tầng, không rõ ràng).
- Không có tìm kiếm quyền.
- Không có nhóm/gom quyền tốt.

## Phân rã theo phase

- **Phase 1 (đang làm) — UI, KHÔNG đụng DB/BE cốt lõi.** Thiết kế lại 2 màn (danh sách chức vụ + form phân quyền), đưa vào menu Quản trị hệ thống. Giữ nguyên schema (`role_has_permissions.company_id`, spatie, seeder). FE chỉ gửi `permission_ids` cho **1 công ty** (của người đăng nhập) thay vì mảng nhiều công ty.
- **Phase 2 (sau) — BE.** Chuẩn hóa 617 permission thành (tài nguyên × hành động), tách module `Administration` riêng, thêm bảng danh mục nhóm quyền. Cần migration → tính riêng, chưa làm.

## Hiện trạng (2026-08-14)

**Đã xong: MOCKUP tương tác hoàn chỉnh** trong bộ demo kế toán (không phải code hrm-client thật), verify bằng Playwright:
- `.plans/demo-man-hinh-ke-toan/demo/phan-quyen.html`
- `.plans/demo-man-hinh-ke-toan/demo/assets/permissions.js` (toàn bộ logic 2 màn)
- `assets/app.js` (thêm menu "Quản trị hệ thống → Phân quyền"), `index.html` (thêm card)

Chưa port vào `hrm-client` thật — đó là việc của phần "IMPLEMENT" trong plan.

## Các quyết định thiết kế chốt qua brainstorming

1. **Phân quyền theo ngữ cảnh 1 công ty.** Bỏ cơ chế 1 form hiển thị tab nhiều công ty. Mỗi chức vụ vẫn có thể có quyền ở nhiều công ty, nhưng người quản trị **chỉ phân cho công ty của mình** (cố định theo user, không cho chọn).
2. **Mô hình quyền = Loại × Phạm vi:**
   - **Xem** và **Duyệt** → có **Phạm vi** = chọn 1 cấp trong `Tổng công ty → Công ty → Phòng ban → Bộ phận` (thứ tự trái→phải), **cấp cao bao hàm cấp thấp**. Duyệt **mặc định Công ty**. Mỗi chức năng chỉ hiện các cấp nó hỗ trợ.
   - **Thao tác** (Thêm mới, Sửa, Xóa, Quản lý…) → chỉ **bật/tắt**, không phạm vi.
   - Trong 1 nhóm, xếp theo loại: **Xem → Thao tác → Duyệt**.
3. **Layout form phân quyền:** phân hệ = **card (accordion)** → các chức năng bên trong = **bảng** (`Loại | Tên quyền | Phạm vi`). Phạm vi dùng **select** (gọn); Thao tác dùng **checkbox** — đều canh phải cột Phạm vi.
4. **Bộ lọc phân tầng 1 hàng:** Nhóm phân hệ → Phân hệ → Chức năng (đổ dây) + **Loại quyền** (Xem/Thao tác/Duyệt) + tìm nhanh.
5. **Panel "Quyền đã phân" (tỷ lệ 8:4, bên phải):** header chỉ "N quyền đã phân"; **chip tổng hợp số quyền theo phân hệ**; danh sách gom theo Phân hệ → Nhóm với badge cấp/loại. Nút **Lưu phân quyền** đặt ở **cuối form** (footer).
6. **Màn danh sách chức vụ:** bảng chuẩn, cột **"Quyền đang có"** là nút bấm → **popup** liệt kê quyền đang có (có bộ lọc Phân hệ/Chức năng/Loại + chip tổng hợp theo phân hệ). Giữ: Phân quyền hàng loạt, Lịch sử thay đổi, Xuất Excel.

## Ảnh hưởng BE (Phase 1)

- Giữ nguyên: bảng `roles`, `permissions` (cột `type` + `group`), pivot `role_has_permissions(company_id)`, `company_roles`, `RoleController`, `PermissionController`, `Role::syncPermissionsByCompany`.
- Điều chỉnh nhỏ: `store` chỉ nhận/ghi `permissions` cho **1 company_id** (của user), thay vì mảng nhiều công ty. Cần xác nhận cách xác định "công ty của user" (từ `DEFAULT_USER`/token).
- Gate dữ liệu nhạy cảm giữ nguyên nguyên tắc fail-closed (không hard-code cờ quyền `= true`).

## Rủi ro / cần làm rõ trước khi implement thật

- Cách map `display_name` → loại (Xem/Thao tác/Duyệt) và các cấp phạm vi trên **dữ liệu thật 617 permission** (mockup đang mô hình hóa sạch cho phân hệ Chấm công). Dữ liệu thật có nhiều bản "bare"/"theo công ty" trùng lặp → cần metadata hoặc quy ước parse tên. Đây là ranh giới dễ trượt sang Phase 2.
- "Công ty của user" khi phân quyền: 1 hay nhiều? Nếu user thuộc nhiều công ty thì UX chọn thế nào (hiện mockup cố định 1).
- Quyền "Phân ca theo cấp" (action có hậu tố cấp) — theo quy ước "chỉ Xem/Duyệt có phạm vi" thì các action-theo-cấp này cần được xử lý/gộp ở Phase 2.
