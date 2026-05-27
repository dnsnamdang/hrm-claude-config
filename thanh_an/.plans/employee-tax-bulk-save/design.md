# Tab Thuế TNCN — Lưu cả bảng 1 lần

**Phụ trách:** @khoipv — 2026-05-26
**Spec chi tiết:** `docs/superpowers/specs/2026-05-26-employee-tax-bulk-save-design.md`

## Mục tiêu
Thay pattern edit per-row (bút chì → Lưu/Hủy từng dòng, gọi POST/PUT 1 row mỗi lần) bằng **1 nút Lưu chung** dưới bảng, lưu toàn bộ tập dòng trong 1 request transaction.

## Quyết định lớn
- FE: tất cả dòng luôn ở chế độ edit (bỏ field `edit`, bỏ icon bút chì)
- Nút Xóa giữ hành vi cũ — gọi DELETE single ngay (không gom vào nút Lưu)
- BE: thêm endpoint mới `POST human/employee_tax/bulk` với transaction. Giữ endpoint POST/PUT/DELETE single cũ
- Validate chồng lấn + chỉ 1 row open chạy **trên payload**, không query DB
- Nút Lưu tab Thuế TNCN độc lập, không gộp vào nút Lưu chính của form `employee_info/edit`

## Scope
- FE: `EmployeeTaxTab.vue`
- BE: route + controller `bulk()` + `BulkEmployeeTaxRequest` (mới) + service `bulkSave()`
- Không đổi schema DB
