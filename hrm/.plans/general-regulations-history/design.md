# Lịch sử chỉnh sửa tab Chung — Quy định chung

Người phụ trách: @khoipv
Trạng thái: Design APPROVED (2026-07-10) — chờ implement
Spec đầy đủ: `docs/superpowers/specs/2026-07-10-general-regulations-history-design.md`

## Mục tiêu

Bổ sung lịch sử chỉnh sửa cho **tab "Chung"** màn Quy định chung (`/timesheet/setting/general`), theo mẫu "Lịch sử thay đổi tài khoản" của màn `/human/employee` (`EmployeeHistoryModal`).

## Quyết định lớn (đã chốt với user)

1. **Chỉ track 14 trường tab Chung** — KHÔNG log `profit_margin_threshold` (màn Cấu hình duyệt giá lưu qua cùng endpoint) hay cột khác.
2. **UI = nút "Lịch sử thay đổi" mở modal timeline** (giống EmployeeHistoryModal), không làm section inline cuối tab.
3. **Không permission riêng** — endpoint chỉ `auth:api` + scope company, giống các route general-regulations hiện có.
4. **Bảng log riêng `general_regulation_history`, ghi trong Service** (không Observer) — theo convention project.
5. **old_value/new_value = JSON chỉ gồm trường thay đổi** (diff ở BE, khác mẫu employee lưu full snapshot) — vì `note_email` là HTML dài, full snapshot phình bảng; FE render thẳng không cần diffJson.

## Kiến trúc tóm tắt

- **DB**: bảng `general_regulation_history` (general_regulation_id, company_id, action='update', old_value/new_value text JSON subset, changed_by, changed_at) — migration Timesheet, không FK cứng.
- **BE**: `GeneralRegulationService::save()` chụp 14 trường trước/sau, diff có chuẩn hoá kiểu → insert log khi có thay đổi; method `histories()` + `GeneralRegulationController::histories()` + route `GET general-regulations/histories` — trả changed_at (d/m/Y H:i:s) + changed_at_raw + changed_by_name.
- **FE**: nút lịch sử trên `components/setting/general/General.vue` + modal mới `GeneralHistoryModal.vue` (copy pattern EmployeeHistoryModal): timeline cũ (đỏ) → mới (xanh), FIELD_LABELS 14 trường, format giá trị (Bật/Tắt, nhãn radio nghỉ tuần, loại bản đồ, note_email strip HTML cắt 100 ký tự), bộ lọc client-side Trường/Người/Từ-Đến ngày, gọi `apiGetMethod`.

## Lưu ý edge

- Tab Chung auto-save theo blur → mỗi dòng log thường 1-2 trường.
- POST từ màn Cấu hình duyệt giá → diff rỗng → không log.
- Không log create khi record tự tạo lần đầu.
- Diff ép kiểu (numeric/boolean/rỗng) tránh log rác `"5" → 5`.
