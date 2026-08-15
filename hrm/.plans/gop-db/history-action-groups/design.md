# Design — Chuẩn hoá bộ lọc "Loại hoạt động" của Lịch sử

Nhánh: `gop_db` (worktree `gop_db-api` + `gop_db-client`) · @dnsnamdang · 2026-08-15

## Vấn đề

Khối/popup **Lịch sử** dùng chung cho **10 màn** (khách hàng, task, issue, phiếu bàn giao, meeting,
BOM, dự án TKT, YCGP, hạng mục dự án), nhưng dropdown "Loại hoạt động" thì **mỗi màn một danh mục**
vì lấy theo action riêng của từng entity:

| Loại | Action đang có |
| --- | --- |
| Khách hàng | Tạo khách hàng · Chỉnh sửa thông tin · Cập nhật ảnh/tài liệu/video · Khóa khách hàng · Mở khóa khách hàng |
| Task / Issue | Tạo mới · Chỉnh sửa · Đổi trạng thái |
| Phiếu bàn giao | Tạo phiếu · Gửi duyệt · Duyệt · Từ chối · Gửi duyệt lại · Nghiệm thu hạng mục · Từ chối hạng mục · Hoàn tất |

Nhãn còn gắn tên đối tượng ("Tạo **khách hàng**") nên không đối chiếu được giữa các màn.

## Quyết định

**Bộ lọc cố định đúng 3 nhóm, giống hệt nhau ở mọi màn** (user chốt 2026-08-15):

| value | Nhãn |
| --- | --- |
| `create` | Tạo mới |
| `update` | Thay đổi thông tin |
| `status` | Thay đổi trạng thái |

Điểm mấu chốt: **nhóm chỉ dùng cho BỘ LỌC, nhãn chi tiết từng dòng vẫn giữ nguyên trên timeline**
(vẫn hiện "Khóa khách hàng", "Duyệt", "Từ chối"…). Nhờ vậy đồng nhất được dropdown mà **không màn
nào mất khả năng lọc và không mất thông tin** — kể cả Phiếu bàn giao có 7 hành động nghiệp vụ riêng
(tất cả đều là chuyển trạng thái → gom vào `status`).

Ánh xạ đặt **một chỗ duy nhất** ở `SystemLogService` (`ACTION_GROUP_MAP` + `groupOfAction()`),
`finalize()` gắn `action_group` cho mọi dòng log nên tự áp cho cả 10 loại. Action **chưa khai** mặc
định vào `status` → entity mới thêm sau vẫn lọc được ngay, không phải sửa map.

## Bẫy đã tránh

Bỏ nhánh `if ($type !== 'customer') return [...]` trong `getFilterOptions()` thì phần `performers`
cũng chạy cho 9 loại còn lại, mà `performerOptions()` **không suy được công ty** cho các loại đó
→ liệt kê **toàn bộ 783 nhân viên** hệ thống. Vì vậy chỉ mở cố định phần `actions`, còn `performers`
vẫn giữ nguyên: chỉ trả cho `customer`, loại khác trả rỗng để FE tự suy từ log như cũ.

## Đã ghi vào tài sản chung

- `.claude/skills/entity-history/SKILL.md` §0a — bảng 3 nhóm, ánh xạ, cảnh báo `performers`, checklist.
- `CLAUDE.md` — nguyên tắc mới: **bản ghi đã khoá thì không cho sửa/xoá, chặn ở BE (423) chứ không chỉ ẩn nút FE**.
