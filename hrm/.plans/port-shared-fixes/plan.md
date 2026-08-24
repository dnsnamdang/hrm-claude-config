# Plan — port-shared-fixes

Nhánh: `feature/port-shared-fixes` (hrm-client, từ `origin/tpe-develop-assign`).

## Đợt 1 — Select & ô nhập liệu

### FE
- [x] Rà toàn bộ chênh lệch component dùng chung giữa 2 nhánh (52 file / ~4.900 dòng), phân loại theo rủi ro
- [x] Kiểm an toàn: 8 component select/input — không prop nào bị bỏ, không event nào bị bỏ, không default nào đổi
- [x] Thêm mới `utils/select2-focus-search.js`, `utils/mixins/v2ValidateMixin.js`
- [x] Lấy nguyên từ gop_db: `V2BaseSelect`, `V2BaseSelectInModal`, `V2BaseSelectRemote`, `V2BaseInput`, `V2BaseTextarea`, `V2BaseCodeInput`, `V2BaseDatePicker`, `common/Select2InModal`
- [x] `assets/scss/v2-styles.scss` — rule khoá/focus dùng chung + `.v2-cell-link`
- [x] Giữ `.field-line` ở `font-weight: 600` (user chốt: tách việc bỏ in đậm bảng thành PR riêng) → SCSS chỉ THÊM, không xoá dòng nào của tpe
- [x] `CustomerForm.vue` — chèn guard `if (this.readonly) return` vào 2 handler còn thiếu (`toggleGroupDropdown`, `toggleScopeDropdown`); 9 handler còn lại tpe đã có sẵn
- [x] Kiểm: 9 template compile sạch, `v2-styles.scss` compile sạch
- [ ] Chạy thật rà màn `/assign/customers/{id}/edit` + vài màn form khác

### Ghi chú
- KHÔNG port `V2BaseRejectApproveModal.vue`: bản gop_db có typo `::rows="3"`, bản tpe đang đúng.
- 🔒 cho danh mục đã khoá chưa chạy được ở Nhóm khách hàng vì BE tpe (`CustomerService::customerGroups`) chưa có `include_ids` / `is_locked` — bản gop_db viết riêng cho DB gộp (không có cột `code`) nên không bê nguyên được.

## Đợt 2 — Lịch sử màn chi tiết (FE + BE)

Nhánh `feature/port-shared-fixes` ở CẢ 2 repo.

### BE (hrm-api)
- [x] Thêm `app/Services/HistoryPerformerOptions.php` — nguồn duy nhất cho danh mục Người thực hiện
- [x] `SystemLogService`: hằng `GROUP_*` / `ACTION_GROUP_LABELS` / `ACTION_GROUP_MAP` + `groupOfAction()`
- [x] `SystemLogService`: log trả thêm `action_group`, `actor_id`, `actor_dept_code`
- [x] `SystemLogService::getFilterOptions()` + `performerOptions()` — suy công ty từ `created_by` của bản ghi theo 9 loại đối tượng (bản gop_db chỉ suy cho 'customer', các loại khác trả toàn bộ nhân sự)
- [x] `SystemLogController::filterOptions()` + route `GET /assign/system-logs/{type}/{id}/filter-options`
- [x] KHÔNG port nhánh `customer` (customerLogs / CustomerHistory / CUSTOMER_FIELD_LABELS) — là tính năng riêng của gop_db, kéo theo entity + migration mới
- [x] Kiểm thật bằng tinker trên báo giá 260: 3 nhóm hành động, 779 người thực hiện, log có đủ 3 trường mới

### FE (hrm-client)
- [x] Lấy nguyên `components/assign/SystemInfoSection.vue` từ gop_db — props là superset, 10 màn đang dùng chỉ truyền `entity-type` + `entity-id`
- [x] Kiểm: template compile sạch; nhánh hiển thị thay đổi dạng danh sách (`hasListChange`) tự tắt vì BE tpe không trả `removed/added/changed`

## Đợt 2c — Lịch sử màn chi tiết hiện đủ nội dung thay đổi (BE, CHƯA PUSH)

Triệu chứng: khối Lịch sử ở màn chi tiết chỉ hiện tên hành động, trong khi popup Lịch sử ngoài
màn danh sách hiện đủ. Nguyên nhân: 2 chỗ đọc 2 nguồn — popup đọc thẳng cột `meta`, khối chi tiết
đi qua `SystemLogService` mà hàm map của từng loại lại trả `changes = []`.

- [x] `quotation`: thêm `quotationMetaChanges()` — meta.changes / discount / services / products.modified
- [x] `bom-list`: thêm `bomListMetaChanges()` — meta.changes / products (added,removed,modified) / success,failed
- [x] Gom 3 helper dùng chung `metaLabelChanges()` / `metaListChange()` / `metaModifiedProducts()`
- [x] `save_draft` + `imported` vào nhóm "Thay đổi thông tin" (trước rơi vào "Thay đổi trạng thái")
- [x] KHÔNG phải sửa FE — component đã hỗ trợ sẵn cả 2 dạng (thay đổi đơn và dạng danh sách)
- [x] Rà 9 loại đối tượng, đo thật bằng tinker

### Kết quả rà từng loại

| Loại | Nguồn lịch sử | Trạng thái |
| --- | --- | --- |
| quotation | `quotation_histories.meta` | ĐÃ SỬA |
| bom-list | `bom_list_logs.meta` | ĐÃ SỬA |
| task / issue | snapshot JSON, tự so sánh | vốn đã đầy đủ |
| prospective-project | `prospective_project_status_logs` | đủ với dữ liệu đang có (bảng chỉ có status_from/to, không có note) |
| handover | `handover_logs` | `meta` LUÔN null (mọi lời gọi `createLog()` đều không truyền meta) → không có gì để thêm |
| meeting / request-solution / project-item | KHÔNG có bảng log, chỉ dựng từ cột audit | chỉ ra được "Tạo mới" / "Chỉnh sửa gần nhất", `changes` luôn rỗng — muốn đầy đủ phải làm tính năng ghi lịch sử (bảng mới + hook trong service) |

## Đợt 2d — Lỗi 423 khi lưu bản ghi đang dùng danh mục đã khoá (BE, CHƯA PUSH)

Triệu chứng: `/assign/meeting/25/edit` bấm Lưu → 423 "Dữ liệu đã được thay đổi hoặc chuyển trạng
thái bởi người dùng khác".

Nguyên nhân: guard đầu hàm `update()` chặn MỌI giá trị danh mục đang ở trạng thái Ngừng hoạt động,
kể cả giá trị bản ghi đã chọn từ trước. Meeting 25 dùng loại "Meeting với khách hàng" (`id=1`,
`status=2`) → mở màn Sửa, không đụng vào ô Loại meeting, bấm Lưu vẫn dính 423 vĩnh viễn.
Vi phạm quy tắc thường trực trong CLAUDE.md: *danh mục bị khoá vẫn phải dùng được ở bản ghi đang
dùng nó*.

- [x] `MeetingController::update()` — chỉ chặn khi `meeting_type_id` / `application_id` KHÁC giá trị
      bản ghi đang giữ; dời `find($identifier)` lên đầu hàm để có giá trị cũ mà so
- [x] `ProspectiveProjectController::update()` — cùng lỗi với `application_id` và `project_phase_id`
- [x] Đổi thông báo 423 thành đúng nguyên nhân ("Loại meeting đã ngừng hoạt động, vui lòng chọn loại
      khác") thay vì câu chung chung gây hiểu nhầm là xung đột dữ liệu
- [x] `store()` giữ nguyên — tạo mới thì chặn danh mục đã khoá là đúng

Số bản ghi đang bị kẹt trên DB hiện tại: **5 meeting** + **24 dự án TKT**.

## Đợt 2e — Lịch sử thay đổi cho Lịch meeting (tính năng mới, CHƯA PUSH)

Meeting KHÔNG có bảng log nào → khối Lịch sử chỉ dựng được từ cột audit ("Tạo mới" / "Chỉnh sửa
gần nhất", `changes` luôn rỗng). Làm mới theo skill `entity-history`, biến thể **subset-diff**.

User chốt: track **đầy đủ mọi bảng con**; **không backfill** dữ liệu cũ.

### BE (hrm-api)
- [x] Migration `meeting_history` (đã chạy) — `old_value`/`new_value` JSON subset + cột `note` cho lý do
- [x] Entity `Meeting/MeetingHistory` (extends `BaseModel`)
- [x] `MeetingHistoryService` — snapshot GIÁ TRỊ HIỂN THỊ (tên loại/trạng thái, không lưu id):
      16 trường chính + 5 bảng con (thành phần công ty / khách hàng / biên bản / dự án gắn kèm / tệp)
- [x] `__key` bảng con dùng KHOÁ TỰ NHIÊN (id nhân viên, nội dung biên bản) vì `sync*()` xoá sạch rồi
      tạo lại → dùng id dòng sẽ thành "xoá hết + thêm hết" sau mỗi lần lưu
- [x] Ghi log ở 3 điểm: `store()` (create), `update()` (update / change_status), `changeStatus()` (kèm lý do hủy)
- [x] `SystemLogService::meetingLogs()` đọc bảng mới, meeting cũ rơi về `auditRows()` như trước
- [x] Verify 8 kịch bản theo skill §7 — xem bảng dưới; đã dọn sạch log test

### FE (hrm-client)
- [x] `pages/assign/meeting/components/MeetingHistoryModal.vue` — vỏ modal bọc `SystemInfoSection`
- [x] Màn danh sách: thêm hành động "Lịch sử" (`ri-history-line`, không gắn permission riêng)
- [x] Màn chi tiết đã có sẵn khối Lịch sử → đủ 2 nơi theo skill §5.1

### Kết quả verify

| Kịch bản | Kết quả |
| --- | --- |
| Không đổi gì | 0 log |
| Đổi 2 trường 1 lần lưu | 1 dòng, 2 khoá |
| Thêm 1 thành viên | chỉ 1 dòng `+` |
| Sửa 1 cột của thành viên | chỉ 1 dòng `~` đúng cột đó |
| Xoá thành viên | chỉ 1 dòng `-` |
| Đổi trạng thái + lý do hủy | action `change_status`, nhóm `status`, note = lý do |
| Thứ tự | mới → cũ |

## Đợt 3+ — chờ chốt tiếp
- [ ] Nhóm V2Base khác: DataTable, FilterPanel, Pagination, TitleSubInfo, Button, Footer, ImportTable, ImportModal
- [ ] Nhóm modal: base-confirm-modal, column-customization-modal, V2BaseModal (mới), 5 modal sửa `rows="3"` → `:rows="3"`
- [ ] Nhóm mixin/util mới
- [ ] BE: `customerGroups` hỗ trợ `include_ids` + `is_locked` (viết lại cho tpe, giữ cột `code`)

## Đợt 2b — Đưa lên nhánh chung + gỡ conflict PR sang gop_db

- [x] Merge `feature/port-shared-fixes` vào `tpe-develop-assign` và push (cả 2 repo)
- [x] Đo conflict PR `tpe-develop-assign` → `gop_db`: 6 file (FE 2 / BE 4) — 9 file chép nguyên văn từ gop_db tự gộp sạch
- [x] Nhánh `feature/sync-shared-fixes-gopdb` (từ `origin/gop_db`, cả 2 repo): merge `tpe-develop-assign`, lấy `--ours` cho 6 file → cây kết quả giống hệt gop_db, 0 dòng đổi
- [x] BE: commit riêng ghép cải tiến `performerOptions` (suy công ty theo bản ghi cho MỌI loại, gop_db chỉ suy cho 'customer')
- [x] Xác nhận `merge-base --is-ancestor`: sau khi merge 2 nhánh này vào gop_db thì PR tpe → gop_db sạch
- [ ] User merge `feature/sync-shared-fixes-gopdb` vào `gop_db` (2 PR: hrm-client + hrm-api)

### Checkpoint — 2026-08-17
Vừa hoàn thành: đợt 1 (select & ô nhập, 13 file FE) + đợt 2 (lịch sử, 1 file FE + 4 file BE). Chưa commit ở cả 2 repo.
Đang làm dở: chưa chạy thật trên trình duyệt (BE đã verify bằng tinker).
Bước tiếp theo: user build FE rà màn `/assign/customers/{id}/edit` và `/assign/quotations/260`; chốt đợt 3.
Blocked: không.
