# Plan — Màn danh mục "Lý do hủy cuộc họp"

Màn: `/assign/meeting_cancel_reason` · Quyền 1182 (Quản lý) / 1183 (Xem)
Phụ trách: @khoipv · Nhánh: `fix-bug-11092026` (cả `hrm-api` + `hrm-client`)
Design: `design.md` cùng thư mục

Hồ sơ thư mục này (1 danh mục = 1 thư mục):

| Tài liệu | Nội dung |
| --- | --- |
| `design.md` | Thiết kế màn: dựng màn, siết quyền, các quyết định + bẫy |
| `plan.md` (file này) | Từng giai đoạn, checklist, kết quả đo |
| `testcase - Danh mục lý do hủy cuộc họp.xlsx` | 159 TC cho QA (P0 52%) |
| `gen_testcase.py` | Generator sinh ra file Excel trên |

Liên quan: `.plans/redmine-11357-ly-do-huy-cuoc-hop/` — phần còn lại của issue (ràng buộc
**Hoàn thành/Hủy** theo giờ + popup hủy ở màn Cuộc họp) và **toàn bộ lịch sử thi công #11357** ·
`.plans/reason-project-failure-permission-gate/` — màn cùng khuôn.

---

## Giai đoạn A — Dựng màn danh mục (Redmine #11357, 12/09/2026)

Làm cùng đợt với phần ràng buộc thời gian của issue; checklist chi tiết + 5 checkpoint của đợt này
nằm ở `.plans/redmine-11357-ly-do-huy-cuoc-hop/plan.md` (Phase 1/2/4/8). Tóm tắt phần thuộc màn:

- [x] A.1 BE: migration tạo bảng `meeting_cancel_reasons` + seed 3 bản ghi idempotent
- [x] A.2 BE: entity / service / FormRequest / resource / controller 10 action (`destroy()` chặn khi
      lý do đã có meeting dùng) / export class + blade
- [x] A.3 BE: routes trong `Modules/Assign/Routes/api.php` (`/getAll` khai TRƯỚC `/{id}`) +
      permission 1182 / 1183 vào `PermissionsTableSeeder.php`
- [x] A.4 FE: `pages/assign/meeting_cancel_reason/index.vue` + `components/modal/meeting-cancel-reason-modal.vue`
      (dựng trên `V2BaseModal`, ô nhập `V2Base*`) + `store/actions.js` + mục menu cuối nhóm Danh mục
- [x] A.5 FE: nút Xóa làm mờ + tooltip khi `is_can_delete === false`
- [x] A.6 Kiểm thử Playwright logic **Xóa** (nút mờ + tooltip khi lý do đang dùng, API chặn 400,
      xóa lý do chưa dùng thành công) và **Khóa/Mở khóa** (nút Sửa mờ khi khóa, dropdown popup hủy
      loại lý do đã khóa, meeting cũ vẫn hiện tên lý do đã khóa)

## Giai đoạn B — Siết quyền (14/09/2026)

Tài khoản chỉ có quyền Xem vẫn thấy và bấm được các nút thao tác. Điều tra: BE fail-closed, lỗi nằm
ở FE không ẩn nút + route `show` không gắn `checkPermission` + 403 bị nuốt tại chỗ. Xem `design.md` mục 3.

- [x] B.1 Đo thật từng endpoint với tài khoản chỉ có quyền Xem: `POST /`, `DELETE /{id}`,
      `GET /{id}/lock`, `GET /export` đều **403**, dữ liệu không đổi → BE không fail-open
- [x] B.2 FE `index.vue`: `v-if="canManage"` cho nút **Khoá/Mở khoá** (slot `#cell-status`)
- [x] B.3 FE `index.vue`: `v-if="canManage"` cho nút **Sửa** và nút **Xoá** (slot `#cell-actions`)
- [x] B.4 FE `index.vue`: `v-if="canManage"` cho nút **Xuất Excel** — chỗ hở THÊM so với màn Nguyên
      nhân thất bại dự án; BE `/export` chỉ nhận quyền Quản lý nên nút này vốn luôn 403 với người chỉ Xem
- [x] B.5 Giữ nguyên nút **Xem** (không gate) và nút **Tạo mới** / **Import Excel** (vốn đã gate)
- [x] B.6 BE `Modules/Assign/Routes/api.php`: gắn `checkPermission:Quản lý…|Xem…` cho
      `GET /assign/meeting_cancel_reasons/{meetingCancelReason}` (show)
- [~] B.7 ~~Gate `GET /assign/meeting_cancel_reasons/getAll`~~ — **HUỶ, cố ý không làm**: dropdown
      của `CancelMeetingModal.vue`; ai hủy được cuộc họp thì phải chọn được lý do. File route đã có
      sẵn comment giải thích, giữ nguyên.
- [~] B.8 ~~Nới `/export` thành `Quản lý|Xem`~~ — **HUỶ**: 14/15 màn danh mục trong `api.php` theo
      convention "export chỉ quyền Quản lý"; muốn nới thì sửa đồng loạt, không sửa lẻ màn này.
- [x] B.9 `php -l` file route + parse SFC `index.vue` (`vue-template-compiler` + `@babel/parser`)
- [x] B.10 Smoke test quyền qua HTTP thật (bảng dưới)
- [ ] B.11 User mở trình duyệt xác nhận 4 nút biến mất khi chỉ có quyền Xem

### Kết quả đo (14/09/2026)

Bản ghi tạm id 999002 + quyền 1183 cấp tạm cho emp 25 (`employee_has_permissions`) — **đã xoá cả
hai sau khi test**, `meeting_cancel_reasons` và `employee_has_permissions` trở lại nguyên trạng.

| Tài khoản | `GET /` | `GET /{id}` | `getAll` | `export` | `POST /` | `lock` | `DELETE` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| emp 62 — không quyền nào của màn | 403 | **403** (trước: 200) | 200 (cố ý) | — | — | — | — |
| emp 25 — chỉ quyền Xem | 200 | 200 | 200 | **403** | **403** | **403** | **403** |
| emp 13 — Super admin (có cả 1182+1183) | 200 | 200 | 200 | 200 | — | — | — |

Bản ghi test sau 3 lệnh ghi: `status` không đổi, không bị xoá → BE fail-closed.

Parse lại `index.vue`: sạch, 6 chỗ `v-if="canManage"` (Tạo mới, Import, Xuất Excel, Khoá/Mở khoá,
Sửa, Xoá). (Grep `can[A-Za-z]*=true` có khớp `let canShow = true` — đó là cờ mở modal, không phải
cờ quyền.)

⚠️ **Lưu ý khi test màn này**: role **Super admin có CẢ quyền 1182 (Quản lý)** — khác màn Nguyên
nhân thất bại dự án (role test chỉ có 1005/Xem). Muốn thử vai "chỉ xem" phải bỏ tick quyền Quản lý
danh mục lý do hủy cuộc họp khỏi role đang dùng, nếu không nút vẫn hiện là **đúng**.

## Giai đoạn C — Sửa file mẫu import (15/09/2026)

- [x] C.1 Đổi tên sheet trong `hrm-client/static/Mau_import_LyDoHuyCuocHop.xlsx` từ `DM_NNthatbai`
      (copy nhầm từ mẫu Nguyên nhân thất bại dự án) thành `DM_lydohuycuochop` — sửa ở cả
      `xl/workbook.xml` và `docProps/app.xml`
- [ ] C.2 User bấm "Tải file mẫu" ở màn, mở bằng Excel xác nhận tên tab, rồi thử import lại file vừa tải

Theo convention `DM_` + tên không dấu viết liền của các mẫu khác trong `hrm-client/static/`. Nội
dung file giữ nguyên: header `STT / Lý do hủy cuộc họp * / Trạng thái * / Mô tả` + 3 dòng ví dụ;
11 file trong gói xlsx còn nguyên, `<definedNames/>` rỗng nên không có công thức nào trỏ tên sheet
cũ. `hrm-client/utils/import-helper.js:43` đọc sheet tên `Data` nếu có, không thì lấy sheet đầu
tiên → đổi tên không ảnh hưởng luồng import. Không đụng code BE/FE.

## Giai đoạn D — Tài liệu testcase (18/09/2026)

- [x] D.1 Đọc lại code màn (controller, service, request, resource, routes + quyền, export/blade,
      `index.vue`, `meeting-cancel-reason-modal.vue`, menu sidebar)
- [x] D.2 Viết generator `gen_testcase.py` dùng engine chung
      `.claude/skills/testcase-documenter/assets/tc_engine.py`
- [x] D.3 Sinh `testcase - Danh mục lý do hủy cuộc họp.xlsx` (159 TC, P0 52%, bộ kiểm tra thuật ngữ
      in `OK - sach`)
- [ ] D.4 QA chạy thử, phản hồi các ca còn thiếu / sai nhãn màn hình

Nội dung file theo chuẩn skill `testcase-documenter`: đủ 9 mục mô tả, 2 khối summary DNS/TP, header
17 cột ở dòng 17, 11 ca phân quyền (`TC-ROLE-01..11`, gồm 6 ca gọi thẳng chức năng bỏ qua giao diện)
và 12 section đánh số La Mã (I–XII), trong đó **section X** kiểm tra ảnh hưởng ngược sang màn Cuộc
họp (ô chọn lý do chỉ lấy lý do Hoạt động, cuộc họp cũ vẫn hiện tên lý do đã khóa, đổi tên lý do thì
cuộc họp cũ hiện tên mới).

⚠️ File Excel **sinh lại được** — sửa thì sửa `gen_testcase.py` rồi chạy lại
(`python .plans/danh-muc-ly-do-huy-cuoc-hop/gen_testcase.py`), đừng sửa tay file Excel.

Nếu cần testcase cho popup "Hủy cuộc họp" ở màn Cuộc họp (phần còn lại của #11357) thì tạo file
riêng trong `.plans/redmine-11357-ly-do-huy-cuoc-hop/`, không nhét vào file này.

---

## Checkpoint

### Checkpoint — 14/09/2026

Vừa hoàn thành: Giai đoạn B (trừ B.11) — 4 nút + route `show`.
Đang làm dở: không có.
Bước tiếp theo: user mở màn bằng tài khoản chỉ có quyền Xem (nhớ bỏ tick 1182) để xác nhận.
Blocked:

### Checkpoint — 18/09/2026

Đã commit trên nhánh `fix-bug-11092026`: `hrm-api` `6c76378aa`, `hrm-client` `53dee118d`, cây sạch.
Mục STATUS chuyển sang **Hoàn thành**. Hồ sơ màn danh mục gom về thư mục này: phần siết quyền (tách
khỏi `reason-project-failure-permission-gate`), phần dựng màn + file mẫu import + tài liệu testcase
(tách khỏi `redmine-11357-ly-do-huy-cuoc-hop`).
Đang làm dở: không có.
Bước tiếp theo: user xác nhận trên trình duyệt (B.11, C.2) · gửi file testcase cho QA (D.4).
Blocked:
