# print-template-decision-type — Tóm tắt

**Mục tiêu:** Màn thêm/sửa mẫu in (`/decision/category/print_templates`) khi chọn loại "Quyết định" sẽ hiện thêm select "Loại quyết định"; chọn loại nào thì panel biến chỉ hiện biến chung + biến riêng của loại đó. Lưu loại quyết định vào DB.

**Vấn đề hiện tại:** Loại "Quyết định" gộp biến của ~19 loại quyết định con → panel quá nhiều biến. Nguyên nhân: nhóm `GROUP_THONG_TIN_CHUNG` trong `PrintTemplateVariable` chứa lẫn biến đặc thù.

**Quyết định chính:**
- Lưu `sub_type` (cột mới, string nullable) vào `print_templates` — cơ chế sub-type tổng quát cho mọi loại mẫu in có nhiều bộ biến.
- Áp dụng cho 2 loại: **Quyết định** (sub-type = `Decision::TYPE`, đủ 21 loại) và **Hợp đồng lao động** (sub-type = HĐLĐ chính / Phụ lục HĐLĐ — vì type 1 dùng chung cho cả 2, 6 biến trước/sau chỉ thuộc Phụ lục).
- Tổ chức lại biến theo từng loại: `DECISION_COMMON_VARIABLES` + `DECISION_TYPE_VARIABLES[*]`; `LABOR_CONTRACT_COMMON_VARIABLES` + `LABOR_CONTRACT_SUB_TYPE_VARIABLES[*]` → thêm biến mới = thêm 1 dòng vào đúng block. Bỏ `TRINH_DO` khỏi HĐLĐ (dùng `TRINH_DO_HOC_VAN`).
- FE: select phụ "Loại quyết định"/"Loại hợp đồng" hiện khi type là 1 hoặc 2; options nạp theo loại qua `get-sub-types`.
- Giữ nguyên permission, giữ Select2/CKEditor (không ép V2Base).

**Phạm vi:** BE Module Human (migration + Model + PrintTemplateVariable + PrintTemplateVariableController + PrintTemplateRequest + route). FE add.vue + _id/edit.vue. Không đụng logic `print()` của controller quyết định, không lọc mẫu in khi tạo quyết định (cột để dành), không git.

**Spec chi tiết:** `docs/superpowers/specs/2026-06-30-print-template-decision-type-design.md`
