# Plan — Siết quyền màn Danh sách nguyên nhân thất bại dự án

Phụ trách: @khoipv
Nhánh: `fix-bug-11092026` (cả `hrm-api` và `hrm-client`)
Ngày tạo: 14/09/2026

## Phase 1 — Điều tra (đã xong trước khi code)

- [x] 1.1 Xác định 2 quyền màn đang dùng: `Quản lý danh mục nguyên nhân thất bại dự án` (990) và
      `Xem danh mục nguyên nhân thất bại dự án` (1005)
- [x] 1.2 Chạy thử thật từng endpoint với tài khoản chỉ có quyền Xem (employee 13 — Super admin):
      POST / DELETE / lock / export đều **403**, dữ liệu không đổi → BE không fail-open
- [x] 1.3 Xác định nguyên nhân "vẫn sửa/xoá/khoá được": FE không ẩn 3 nút Sửa/Xoá/Khoá +
      route xem chi tiết không gắn `checkPermission` nên modal Sửa vẫn mở và nạp đủ dữ liệu

## Phase 2 — FE (`hrm-client`)

- [x] 2.1 `pages/assign/reason_project_failure/index.vue`: thêm `v-if="canManage"` cho nút
      **Khoá/Mở khoá** trong slot `#cell-status`
- [x] 2.2 Thêm `v-if="canManage"` cho nút **Sửa** trong slot `#cell-actions`
- [x] 2.3 Thêm `v-if="canManage"` cho nút **Xoá** trong slot `#cell-actions`

## Phase 3 — BE (`hrm-api`)

- [x] 3.1 `Modules/Assign/Routes/api.php`: gắn `checkPermission:Quản lý…|Xem…` cho
      `GET /assign/reason_project_failures/{reasonProjectFailure}` (show)
- [~] 3.2 ~~Gắn middleware cho `GET /assign/reason_project_failures/getAll`~~ — **HUỶ, cố ý không làm**:
      endpoint này là dropdown của `components/assign/prospective-project/CloseProjectModal.vue`
      (modal Đóng dự án tiềm năng). Route `POST /assign/prospective_projects/{id}/close` không gắn
      `checkPermission`, nên người đóng dự án có thể không có quyền danh mục này — gate vào là
      dropdown lý do rỗng, không đóng được dự án. Dữ liệu trả về chỉ là id + tên danh mục đang
      active, không nhạy cảm. Đã thử gắn rồi gỡ lại, route giữ nguyên như cũ.

## Phase 4 — Kiểm chứng

- [x] 4.1 `php -l` file route + parse SFC của `index.vue`
- [x] 4.2 Chạy lại bộ smoke test quyền: tài khoản chỉ Xem → show/getAll trả 403,
      index vẫn 200; tài khoản có quyền Quản lý → tất cả 200
- [ ] 4.3 User mở trình duyệt kiểm tra giao diện thực tế (nút Sửa/Xoá/Khoá biến mất khi chỉ có quyền Xem)

## Ghi chú

- KHÔNG đổi kiểu nút sang `V2BaseIconButton` ở nhánh này — nhánh `gop_db` đã chuẩn hoá riêng
  (`.plans/gop-db/reason-project-failure-list-page-standard/`), đụng vào sẽ khó merge.
- Nút **Tạo mới** và **Import Excel** vốn đã gate bằng `canManage`, giữ nguyên.


## Kết quả kiểm chứng (14/09/2026)

`php -l` route sạch; template + `<script>` của `index.vue` parse sạch bằng `vue-template-compiler`
+ `@babel/parser` (5 chỗ `v-if="canManage"`: Tạo mới, Import, Khoá/Mở khoá, Sửa, Xoá).

Smoke test qua HTTP kernel (JWT thật, mỗi tài khoản 1 tiến trình riêng):

| Tài khoản | `GET /` | `GET /{id}` | `GET /getAll` | `GET /export` |
| --- | --- | --- | --- | --- |
| emp 25 — không có quyền nào của màn | 403 | **403** (trước khi sửa: 200) | 200 (cố ý) | — |
| emp 13 — chỉ quyền Xem | 200 | 200 | 200 | 403 |
| emp 100 — role Admin_TPE (có quyền Quản lý) | 200 | 200 | 200 | 200 |

Trước đó đã xác nhận BE vốn KHÔNG fail-open: với tài khoản chỉ có quyền Xem, `POST /`,
`DELETE /{id}`, `GET /{id}/lock` đều trả 403 và dữ liệu không đổi (test trên 1 bản ghi tạm
id 999001, đã xoá sau khi test).

### Checkpoint — 14/09/2026

Vừa hoàn thành: Phase 1–4 (trừ 4.3). FE ẩn 3 nút Sửa/Xoá/Khoá khi không có quyền quản lý;
BE gate route xem chi tiết.
Đang làm dở: không có.
Bước tiếp theo: user mở `/assign/reason_project_failure` bằng tài khoản chỉ có quyền Xem để
xác nhận 3 nút đã biến mất.
Blocked:

## Phase 5 — Màn Lý do hủy cuộc họp (`/assign/meeting_cancel_reason`) — 14/09/2026

Cùng hệ thống nút, cùng kiểu lỗi. Check kỹ thì thấy **thêm 1 chỗ hở so với màn trước**: nút
**Xuất Excel** không gate trong khi BE `/export` đòi quyền Quản lý.

- [x] 5.1 FE `pages/assign/meeting_cancel_reason/index.vue`: `v-if="canManage"` cho nút
      **Khoá/Mở khoá**, **Sửa**, **Xoá**
- [x] 5.2 FE cùng file: `v-if="canManage"` cho nút **Xuất Excel** (BE `/export` chỉ nhận quyền
      Quản lý — giữ BE nguyên, 14/15 màn danh mục trong `api.php` đều theo convention này)
- [x] 5.3 FE `pages/assign/reason_project_failure/index.vue`: gate nốt nút **Xuất Excel** cho
      đồng bộ (sót ở Phase 2)
- [x] 5.4 BE `Modules/Assign/Routes/api.php`: gắn `checkPermission:Quản lý…|Xem…` cho
      `GET /assign/meeting_cancel_reasons/{meetingCancelReason}` (show)
- [~] 5.5 ~~Gate `GET /meeting_cancel_reasons/getAll`~~ — **HUỶ, cố ý không làm**: dropdown của
      `pages/assign/meeting/components/CancelMeetingModal.vue`. File route đã có sẵn comment giải
      thích đúng lý do này, giữ nguyên.
- [x] 5.6 Kiểm: nút **Xem** giữ nguyên không gate (ai vào được màn cũng có 1 trong 2 quyền, route
      `show` nay nhận cả 2); modal chế độ Xem (`isShow=true`) vốn đã ẩn nút Lưu + disable input
- [ ] 5.7 User mở trình duyệt xác nhận

### Kiểm chứng Phase 5

Bản ghi tạm id 999002 + quyền 1183 cấp tạm cho emp 25 (`employee_has_permissions`) — **đã xoá cả
hai sau khi test**, `meeting_cancel_reasons` và `employee_has_permissions` trở lại nguyên trạng.

| Tài khoản | `GET /` | `GET /{id}` | `getAll` | `export` | `POST /` | `lock` | `DELETE` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| emp 62 — không quyền nào của màn | 403 | **403** (trước: 200) | 200 (cố ý) | — | — | — | — |
| emp 25 — chỉ quyền Xem | 200 | 200 | 200 | **403** | **403** | **403** | **403** |
| emp 13 — Super admin (có cả 1182+1183) | 200 | 200 | 200 | 200 | — | — | — |

Bản ghi test sau 3 lệnh ghi: `status` không đổi, không bị xoá → BE fail-closed.

Parse lại 2 file FE bằng `vue-template-compiler` + `@babel/parser`: sạch, mỗi file 6 chỗ
`v-if="canManage"`. (Grep `can[A-Za-z]*=true` có khớp `let canShow = true` — đó là cờ điều khiển
mở modal, không phải cờ quyền.)

⚠️ **Lưu ý khi test màn này**: role **Super admin có CẢ quyền 1182 (Quản lý)** — khác màn nguyên
nhân thất bại (chỉ có 1005/Xem). Muốn thử vai "chỉ xem" phải bỏ tick quyền Quản lý danh mục lý do
hủy cuộc họp khỏi role đang dùng, nếu không nút vẫn hiện là đúng.

### Checkpoint — 14/09/2026 (lần 2)

Vừa hoàn thành: Phase 5 — màn Lý do hủy cuộc họp (4 nút + route show) + gate nốt nút Xuất Excel
của màn nguyên nhân thất bại.
Đang làm dở: không có.
Bước tiếp theo: user mở cả 2 màn bằng tài khoản chỉ có quyền Xem để xác nhận.
Blocked:
