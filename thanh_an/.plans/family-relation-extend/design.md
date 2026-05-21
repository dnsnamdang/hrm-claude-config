# Mở rộng mối quan hệ gia đình — Ông, Bà, Khác

> Spec chi tiết: `docs/superpowers/specs/2026-05-21-family-relation-extend-design.md`

## Mục tiêu

Thêm 3 loại mối quan hệ mới (Ông, Bà, Khác) vào phần Thông tin gia đình. Khi chọn "Khác", hiện ô text để nhập mối quan hệ tự do.

## Scope

- DB: thêm cột `relation_other_text` vào `employee_relationships` + `employee_relationship_tmps`
- BE: cập nhật constant, fillable, service, validation
- FE: cập nhật dropdown + thêm conditional text input trong 3 file EmployeeInfoForm.vue

## Quyết định thiết kế

- Giữ `relation` kiểu TINYINT (9=Ông, 10=Bà, 11=Khác) — backward compatible
- Thêm field `relation_other_text VARCHAR(255)` riêng cho "Khác" — không đổi kiểu dữ liệu cũ
- Pattern tham khảo: "Nguồn tiếp nhận" trong sale/project/add (nhưng đơn giản hơn, không cần watcher 2 chiều)
