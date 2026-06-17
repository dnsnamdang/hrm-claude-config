# timesheet-detail-note — Design (tóm tắt)

**Mục tiêu:** Hiển thị cột "Ghi chú" trong modal Chi tiết → tab "Dữ liệu chấm công", lấy từ `timesheets.note` (ghi chú nhập khi chấm công trên app mobile, web chưa show).

**Phạm vi:**
- Chỉ modal `TimeSheetDetailModal.vue` (cột cuối, sau "Hình ảnh").
- BE trả thêm field `note` trong `TimekeeperListResource`.
- KHÔNG migration (cột `note` đã có). KHÔNG đổi màn list độc lập.

**Thay đổi:**
| Layer | File | Sửa |
| ----- | ---- | --- |
| BE | `Modules/Timesheet/Transformers/TimekeeperResource/TimekeeperListResource.php` | Thêm `'note' => $guide->note` vào mảng push |
| FE | `components/modals/TimeSheetDetailModal.vue` | Thêm `{ key: 'note', label: 'Ghi chú' }` cuối mảng `fields` |

**Edge case:** chấm bằng máy / app không nhập → ô trống.

**Spec chi tiết:** `docs/superpowers/specs/2026-06-15-timesheet-detail-note-design.md`
