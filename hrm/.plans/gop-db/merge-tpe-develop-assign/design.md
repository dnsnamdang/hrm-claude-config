# Merge `tpe-develop-assign` → `gop_db`

Gộp toàn bộ thay đổi của nhánh `tpe-develop-assign` vào nhánh `gop_db` (23 xung đột BE, 22 xung đột FE).

## Nguyên tắc xử lý xung đột
1. **Logic** theo `tpe-develop-assign`, **UI/khung màn** theo `gop_db` (quy tắc đã chốt trước đó).
2. Ràng buộc thường trực của `gop_db` thắng: không `mysql2`/`DB_CONNECTION_SECOND`, bảng HRM trùng tên dùng tiền tố `hrm_*`.
3. Hai bên cùng thêm code ở một chỗ → giữ **cả hai**, không chọn một.
4. Xung đột "cả file" phải kiểm tra line ending trước — phần lớn là do một nhánh đổi LF/CRLF, không phải khác nội dung.

## Quyết định đã chốt
- **Màn Danh mục Quận/Huyện: giữ bản `gop_db`** (user chốt 2026-09-14). Lý do: đồng bộ với 3 danh mục địa lý anh em (provinces/wards/hamlets), dùng `V2BaseDataTable` + `V2BaseSmartFilterPanel` + `base-confirm-modal` chung, có ghi lịch sử thay đổi; bản tpe đồng bộ sang `TpDistrict` (mysql2 — nhánh gop_db cấm) và tự chế 3 confirm modal riêng.
  - Hệ quả: **mất** nghiệp vụ Khoá/Mở khoá riêng và `canDelete()` (chặn xoá khi còn phường/xã, hồ sơ nhân sự, khách hàng đang dùng) của bản tpe. Ở bản gop_db, "Xóa" = khoá mềm (`status` → 0). Cần bổ sung sau thì mở task riêng.
- **Thuật ngữ**: theo tpe — "issue" → **Vấn đề**, "task" → **nhiệm vụ** ở chữ hiển thị (không đổi tên biến/route/component).
- **Line ending**: ghi theo line ending của nhánh đích (`gop_db`) để diff merge chỉ chứa thay đổi thật.
