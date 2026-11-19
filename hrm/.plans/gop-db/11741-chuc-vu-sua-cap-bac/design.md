# #11741 — DM chức vụ: cảnh báo khi sửa cấp bậc (@cuong61n)

Redmine: http://quanly.dnsmedia.vn/issues/11741 · Nhánh `fix-11741-chuc-vu-sua-cap-bac` (từ `gop_db`, cả 2 repo)
Worktree: đã xoá sau khi push (16/10/2026)

## Bug gốc
Sửa cấp bậc chức vụ sau khi đã ban hành QĐ → QĐ bổ nhiệm tạo sau lấy cấp bậc mới từ chức vụ
(`InfoFormComponent.vue` → API `all-working-positions-have-rank` đọc `working_position_ranks` hiện hành).

## Quyết định đã chốt (16/10/2026)
- "Sửa cấp bậc" = cấp bậc cũ ≠ mới, kể cả khi đổi Nhóm chức vụ/ngạch lương (đổi nhóm tự reset cấp bậc).
- 2 loại QĐ được kiểm: (1) QĐ ban hành/thay đổi định biên `/decision/manpower-planning`,
  (2) QĐ ban hành quy chế lương và hỗ trợ `/decision/regulations/salary` (hiện hành: `/regulations/salary`). Link trong task (salary-change) là sai.
- Có dùng QĐ + dùng định biên: QĐ định biên đang hiệu lực chứa cặp (chức vụ, cấp bậc cũ) → confirm; "Có" → lưu + QĐ chuyển **Hết hiệu lực** (`decisions.status = 8`), hết hiệu lực **cả QĐ**. Định biên đang áp dụng ở phòng **giữ nguyên**.
- QĐ đang hiệu lực = QĐ mà `department_manpowers.decision_id` đang trỏ tới và còn chứa cặp đó (QĐ đã bị QĐ sau thay thế không tính).
- QĐ quy chế lương (hướng B): **chỉ cảnh báo, KHÔNG cho hết hiệu lực** — vì mỗi công ty chỉ 1 QĐ `is_using`, hết hiệu lực là cả công ty mất quy chế lương. Áp khi có dùng QĐ (không phụ thuộc định biên) → chặn đúng bug gốc ở trường hợp "dùng QĐ, không dùng định biên".
- Không dùng QĐ + dùng định biên: cặp đã định biên ở phòng nào → confirm liệt kê `mã phòng - tên phòng`; "Có" → chỉ lưu, HCNS tự định biên lại.
- Cấu hình: dùng QĐ = `master_settings.category='use_decision'`; dùng định biên = `general_regulations.using_manpower` theo công ty (chức vụ là danh mục dùng chung → xét theo company_id của từng dòng định biên / QĐ).
- Popup xác nhận dùng `$confirm` (base-confirm-modal), chữ nút theo skill. Popup sửa chức vụ cũ (`b-modal`) giữ nguyên, chỉ chèn bước xác nhận.
