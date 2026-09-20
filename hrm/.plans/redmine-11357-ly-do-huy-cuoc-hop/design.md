# Design — Redmine #11357: Danh mục Lý do hủy cuộc họp + ràng buộc thời gian Hoàn thành/Hủy

- **Redmine**: http://quanly.dnsmedia.vn/issues/11357
- **Người phụ trách**: @khoipv — **Nhánh**: `fix-bug-11092026` (cả hrm-api + hrm-client)
- **Spec đầy đủ**: `docs/superpowers/specs/2026-09-12-redmine-11357-ly-do-huy-cuoc-hop-design.md`

## Mục tiêu

1. Danh mục **Lý do hủy cuộc họp** (CRUD + khóa/mở khóa + import/export Excel), seed 3 bản ghi.
2. Nút **[Hoàn thành]** chỉ bật khi `now >= giờ bắt đầu` cuộc họp.
3. Nút **[Hủy]** chỉ bật khi `now < giờ bắt đầu`.
4. Popup hủy: **bắt buộc chọn lý do** từ danh mục + ghi chú tùy chọn; lưu lý do / thời điểm hủy / người hủy.

## Scope

| Trong phạm vi | Ngoài phạm vi |
| --- | --- |
| Danh mục mới `meeting_cancel_reasons` (BE + FE + menu + 2 permission) | Thêm nút Hoàn thành/Hủy vào màn danh sách `/assign/meeting` |
| 3 cột mới trên `meetings`: `cancel_reason_id`, `cancelled_at`, `cancelled_by` | Thêm nút vào drawer `/assign/my-todo` (đang chỉ-đọc) |
| Guard thời gian ở `update()` (Hoàn thành) và `changeStatus()` (Hủy) | Sửa job auto-hủy #11014 |
| Popup hủy mới có dropdown bắt buộc | Báo cáo thống kê theo lý do hủy |
| Thêm prop optional `*_disabled` / `*_tooltip` vào `V2Footer.vue` | Phân quyền danh mục theo cấp tổ chức |

## Quyết định lớn (chốt với user 2026-09-12)

| # | Quyết định |
| --- | --- |
| 1 | **Chỉ áp ràng buộc ở chỗ đã có nút** = `MeetingForm.vue`. Không thêm nút mới ở màn khác |
| 2 | Thêm FK `cancel_reason_id`, **giữ `cancel_reason` cũ làm ghi chú**. Hiển thị ghép `Tên lý do — ghi chú` |
| 3 | Job auto-hủy #11014 **không đụng** — `cancel_reason_id = null`, text cũ giữ nguyên |
| 4 | Quá giờ bắt đầu thì **chặn cứng** việc hủy, không có permission vượt rào |
| 5 | **Chặn xóa** lý do đã có meeting dùng → chỉ cho Khóa |
| 6 | Danh mục **global**, không phân quyền theo cấp (giống `reason_project_failures`) |
| 7 | **Làm đủ Import + Export Excel** như danh mục mẫu |
| 8 | Nút bị chặn thì **làm mờ + tooltip**, không ẩn |
| 9 | Được phép thêm **prop optional** vào `V2Footer.vue` (file dùng chung), mặc định tắt |

## Bẫy đã nhận diện

- Relation phải đặt tên `cancel_reason_ref`, KHÔNG đặt `cancel_reason` — trùng tên **cột** sẽ bị Eloquent che.
- Route `/getAll` phải khai TRƯỚC `/{id}`, nếu không bị wildcard nuốt.
- Cờ `can_complete` / `can_cancel` mặc định **`false`** (fail-closed). FE phải AND thêm `can_manage`.
- FE **không tự tính giờ** — đọc cờ BE trả về, tránh lệch đồng hồ máy client.
- Tooltip trên nút `disabled`: Bootstrap không bắn event → phải bọc `<span v-b-tooltip>` bên ngoài.
- Select trong modal BẮT BUỘC dùng `V2BaseSelectInModal`.
