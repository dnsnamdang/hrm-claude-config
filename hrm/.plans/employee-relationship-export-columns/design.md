# Design — Chọn cột khi xuất Excel màn employee-relationships

Người phụ trách: @khoipv · Ngày: 2026-06-09 · Quy mô: nhỏ (1 phase, FE-only)

## Mục tiêu
Thêm chức năng chọn cột khi xuất Excel ở màn `human/employee-relationships`, theo pattern màn `human/employee_info` (modal "Xuất excel" với multi-select cột + "Chọn tất cả").

## Scope
- **FE-only.** Backend đã sẵn sàng hoàn toàn (không sửa).
  - Controller `EmployeeController::exportEmployeeRelationships` đã nhận `visible_fields[]`.
  - Blade `resources/views/exports/employee_relationship_report.blade.php` đã render đủ 14 cột tuỳ chọn theo `$visibleFields`.

## Quyết định chính
1. **Cơ chế:** modal chọn cột riêng khi bấm "Xuất excel" (giống employee_info), độc lập với "Tuỳ chỉnh cột" của bảng. Trước đây export bám theo cột đang hiển thị trên bảng (`this.visibleFields`) → nay **decouple**, export theo lựa chọn trong modal.
2. **Nguồn cột:** 14 cột tuỳ chọn trong "Tuỳ chỉnh cột" (`this.fields` của page), không hardcode.
3. **Mặc định:** modal bắt đầu **trống** (chưa tick cột nào).
4. **Cột cố định** luôn xuất: STT, Phòng/Nhân viên, MST nhân viên, Họ tên người thân, Ngày sinh, Mối quan hệ.
5. **Style:** mirror legacy style của module (Bootstrap `b-modal` + Select2 + nút `btn`), KHÔNG ép V2Base (cả trang dùng style cũ + yêu cầu tham khảo employee_info dùng style này).
6. **Edge case:** không tick cột nào vẫn cho xuất (file chỉ 6 cột cố định) — giống employee_info, không chặn.

## Thay đổi
- **Mới:** `pages/human/employee-relationships/components/ExportRelationshipModal.vue` — modal chọn cột, emit `export` kèm mảng key.
- **Sửa:** `pages/human/employee-relationships/index.vue`
  - Nút "Xuất excel" → mở modal.
  - Đăng ký + render modal (`:fields="fields" @export="exportEx"`).
  - `exportEx(selectedKeys)` dùng `selectedKeys` thay cho `this.visibleFields`.

## Spec chi tiết
`docs/superpowers/specs/2026-06-09-employee-relationship-export-columns-design.md`
