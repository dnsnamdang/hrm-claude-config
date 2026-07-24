# Lịch sử phân ca (shift-assignment-history)

Người phụ trách: @khoipv
Nguồn yêu cầu: `HRM_Lịch sử (bổ sung ở nhiều phân hệ)_v1.3_040426.xlsx` — sheet "Lịch sử phân ca"
Spec đầy đủ: `docs/superpowers/specs/2026-07-15-shift-assignment-history-design.md`

## Mục tiêu

Màn hình riêng `/timesheet/timeworking/shift-history` ghi nhận mọi thay đổi phân ca từ 2 nguồn: **Phân ca chi tiết** (`shift_details` + `shift_detail_employees`) và **Phân ca tổng hợp** (`shift_detail_employee_dates`). Theo dõi được cả NV nghỉ việc / ca / bảng phân ca đã xóa (denormalize toàn bộ tên/mã tại thời điểm log).

## Kiến trúc đã chốt

- **Event-log tách dòng sẵn tại BE** (không full-snapshot FE diff như các màn history trước): mỗi dòng log = 1 tổ hợp **(ca cũ → ca mới)** + nhóm NV tương ứng; ghi đè Có ⟺ có ca cũ.
- 2 bảng mới: `shift_assignment_history` (sự kiện + JSON snapshot NV) + `shift_assignment_history_employees` (bảng con NV kèm snapshot company/department/part — phục vụ lọc index + scope quyền theo cấp).
- Ghi log tại **6 điểm mutation**: `WorkShiftDetailService::store/update/delete` (nguồn Phân ca chi tiết) + thêm/phân ca theo ngày/xóa ô ca ở màn tổng hợp (`ShiftDetailEmployeeDateService` + controller). Bọc try/catch — không bao giờ fail luồng phân ca. Snapshot chụp đồng bộ trước khi dispatch job materialize.
- API: `GET timesheet/shift-assignment-histories` (lọc 11 tiêu chí server-side + phân trang, sort mới→cũ) + `GET .../{id}/export-employees` (Excel on-demand từ snapshot, không lưu S3 lúc ghi).
- Phân quyền: dùng lại 3 quyền `Phân ca theo công ty/phòng ban/bộ phận` — scope theo cấp qua bảng con; dòng log hiển thị nguyên vẹn.
- FE: màn danh sách theo skill `list-page` (V2BaseFilterPanel, auto-search, filterStateMixin key `timesheet_shift_history`), bảng 11 cột; cột NV: <20 hiển thị danh sách, ≥20 hiển thị số lượng + nút tải Excel. Menu sidebar mới dưới "Danh mục ca làm việc".

## Quyết định lớn

- Bỏ sự kiện "NV nghỉ việc" (spec dòng 8) — luồng tự xóa ca khi nghỉ việc không tồn tại trong code.
- Chỉ làm sheet "Lịch sử phân ca"; sheet "LS phân ca theo từng nhân viên" đợt sau.
- 3 mâu thuẫn spec đã xử lý: ghi đè Có ⟺ có ca cũ; spec dòng 5 = hiển thị metadata sau sửa (không phải event riêng, đổi mỗi tên bảng không log); xóa bảng vẫn lưu DS NV bị ảnh hưởng.
- Không backfill; migration chờ user đồng ý mới chạy.
