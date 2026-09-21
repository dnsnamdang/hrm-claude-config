# Design — Màn danh mục "Lý do hủy cuộc họp"

Màn: `/assign/meeting_cancel_reason` · Menu **Giao việc ▸ Danh mục** (đặt cuối nhóm)
Quyền: **1182** `Quản lý danh mục lý do hủy cuộc họp` / **1183** `Xem danh mục lý do hủy cuộc họp`
Phụ trách: @khoipv · Nhánh: `fix-bug-11092026` (cả `hrm-api` + `hrm-client`)

> Thư mục này là **hồ sơ của riêng màn danh mục**: dựng màn → siết quyền → tài liệu testcase.
> Phần còn lại của Redmine #11357 (ràng buộc **Hoàn thành/Hủy** theo giờ + popup hủy ở màn Cuộc họp)
> theo dõi ở `.plans/redmine-11357-ly-do-huy-cuoc-hop/`.
> Màn cùng khuôn **Nguyên nhân thất bại dự án**: `.plans/reason-project-failure-permission-gate/`.

## 1. Màn làm gì

CRUD lý do hủy cuộc họp + khóa/mở khóa + import/export Excel. Dữ liệu của màn là nguồn cho dropdown
**bắt buộc chọn** ở popup hủy cuộc họp (`CancelMeetingModal.vue`), lưu xuống `meetings.cancel_reason_id`.

## 2. Dựng màn — Redmine #11357 (12/09/2026)

Bảng `meeting_cancel_reasons`, seed 3 bản ghi idempotent ngay trong migration. Màn dựng theo khuôn
danh mục **Nguyên nhân thất bại dự án**.

Quyết định đã chốt với user (phần thuộc màn danh mục):

| # | Quyết định |
| --- | --- |
| 1 | **Chặn xóa** lý do đã có meeting dùng → chỉ cho Khóa (nút Xóa làm mờ + tooltip, không ẩn) |
| 2 | Danh mục **global**, không phân quyền theo cấp tổ chức (giống `reason_project_failures`) |
| 3 | **Làm đủ Import + Export Excel** như danh mục mẫu |
| 4 | Lý do đã khóa: không hiện trong dropdown popup hủy, nhưng meeting cũ vẫn hiển thị đúng tên |

Bẫy đã nhận diện khi dựng:

- Route `/getAll` phải khai **TRƯỚC** `/{id}`, nếu không bị wildcard nuốt.
- Modal danh mục đời cũ (`reason-project-failure-modal.vue`) **không** phải khuôn để copy — nó tự
  khai `b-modal` + `<textarea>` thô. Popup mới dựng trên `V2BaseModal`, ô nhập dùng `V2Base*`
  (`V2BaseTextarea`, `V2BaseSelectInModal`, `V2BaseLabel required`, `V2BaseError`).
- 2 popup confirm (Xóa · Khóa/Mở khóa) theo skill button-convention: **Khóa đỏ, Mở khóa KHÔNG đỏ**
  (là thao tác khôi phục).

Spec đầy đủ của issue: `docs/superpowers/specs/2026-09-12-redmine-11357-ly-do-huy-cuoc-hop-design.md`.

## 3. Siết quyền (14/09/2026)

### Vấn đề

Tài khoản chỉ có quyền **Xem** vào màn vẫn thấy và bấm được: Khoá/Mở khoá, Sửa, Xoá và **Xuất Excel**.

### Kết luận điều tra

BE **không** fail-open: mọi route ghi (`POST /`, `DELETE /{id}`, `lock`) và cả `export` đều đã gắn
`checkPermission:Quản lý danh mục lý do hủy cuộc họp`, trả 403 đúng và dữ liệu không suy suyển (đo
bằng JWT thật trên DB local). Cảm giác "vẫn làm được" đến từ tầng giao diện:

1. `index.vue` chỉ dùng cờ `canManage` để ẩn **Tạo mới** và **Import Excel**; các nút
   **Khoá/Mở khoá · Sửa · Xoá · Xuất Excel** trong bảng không gate.
2. Route `GET /assign/meeting_cancel_reasons/{id}` (xem chi tiết) không gắn `checkPermission`, nên
   modal Sửa mở ra và nạp đủ dữ liệu, gõ sửa thoải mái — tới lúc bấm Lưu mới 403.
3. Lỗi 403 bị nuốt tại chỗ (`if (status === 403) return`), modal không tự đóng → nhìn như thao tác
   đã chạy.

Điểm **khác** màn Nguyên nhân thất bại dự án: ở màn này nút **Xuất Excel** cũng hở (màn kia hở y
hệt nhưng phát hiện muộn hơn, đã gate nốt bên đó).

### Quyết định

- **FE**: `v-if="canManage"` cho 4 nút **Khoá/Mở khoá · Sửa · Xoá · Xuất Excel**. Giữ nguyên kiểu
  nút `<button>` inline, KHÔNG refactor sang `V2BaseIconButton` ở nhánh này (nhánh `gop_db` đang
  chuẩn hoá list-page riêng, đụng vào sẽ khó merge).
- **BE**: gắn `checkPermission:Quản lý…|Xem…` cho route `show`.
- **Giữ BE `/export` chỉ nhận quyền Quản lý**, FE ẩn nút cho khớp. Lý do: 14/15 màn danh mục trong
  `Modules/Assign/Routes/api.php` đều gắn export bằng đúng quyền "Quản lý danh mục …"; nới thành
  `Quản lý|Xem` là mở rộng quyền và lệch convention. Muốn nới thì sửa đồng loạt cả 15 màn.
- **Cố ý KHÔNG gate `GET /meeting_cancel_reasons/getAll`**: đó là dropdown của
  `pages/assign/meeting/components/CancelMeetingModal.vue` — ai hủy được cuộc họp thì phải chọn
  được lý do, không bắt buộc có quyền quản trị danh mục. File route đã có sẵn comment giải thích.
- Nút **Xem** không gate: ai vào được màn cũng có 1 trong 2 quyền, và route `show` nay nhận cả 2.
  Modal ở chế độ Xem (`isShow=true`) vốn đã ẩn nút Lưu + disable input.
- Cờ quyền fail-closed: `canManage` đọc từ `hasAPermission(...)`, không hard-code.

## 4. Phạm vi thay đổi theo repo

| Đợt | Repo | File |
| --- | --- | --- |
| Dựng màn (#11357) | `hrm-api` | migration `2026_09_12_000001_create_meeting_cancel_reasons_table.php` · entity/service/request/resource/controller/export + blade · routes · `PermissionsTableSeeder` (1182/1183) |
| Dựng màn (#11357) | `hrm-client` | `pages/assign/meeting_cancel_reason/index.vue` · `components/modal/meeting-cancel-reason-modal.vue` · `store/actions.js` · `components/menu-sidebar.js` |
| Siết quyền | `hrm-client` | `pages/assign/meeting_cancel_reason/index.vue` — 4 chỗ `v-if="canManage"` (Khoá, Sửa, Xoá, Xuất Excel) |
| Siết quyền | `hrm-api` | `Modules/Assign/Routes/api.php` — route `show` thêm middleware |

Siết quyền: không migration, không quyền mới, không đụng hàm dùng chung.

## 5. Tài liệu testcase (18/09/2026)

`testcase - Danh mục lý do hủy cuộc họp.xlsx` sinh bằng `gen_testcase.py` (engine chung
`.claude/skills/testcase-documenter/assets/tc_engine.py`) — sinh lại được, sửa thì sửa generator
rồi chạy lại, đừng sửa tay file Excel.

Chi tiết từng bước + kết quả đo: `plan.md` cùng thư mục.
