# Plan — Chuẩn hoá màn "Quản lý Issue" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-08-issue-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `IssueService::SORTABLE_COLUMNS` — whitelist 5 khoá cột FE (`issueCode`, `deadline`,
      `detectedAt`, `updatedAt`, `createdAt`) + chốt `issues.id desc`; key lạ về
      mặc định `created_at desc`
- [x] 1.2 Ô tìm nhanh thêm **người tạo** bằng `EXISTS` (không `join` — giữ câu COUNT phân trang nhẹ)
- [x] 1.3 `IssueResource` bổ sung `issue_type_text`, `detected_from_text`, `due_status_text`,
      `due_status_color`; sửa `updated_by_name` chỉ còn **TÊN** (bỏ `MÃ - `)
- [x] 1.4 `Issue::STATUS_DATA` sửa 3 mã màu về bảng 9 màu chuẩn (closed `#6B7280`,
      completed `#16A34A`, rejected `#DC2626`, reopened `#D97706`)
- [x] 1.5 `ExportColumnRegistry['issues']` 25 cột + `IssueController::export()` chuyển sang
      `DynamicExport` (nhận `fields=a,b,c`, lọc qua whitelist)

## Phase 2 — Frontend (`pages/assign/issues/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (13 mục, bỏ `title`/`subtitle`,
      placeholder "Chọn <tên trường>"); nhóm `org` khai `resetKeys` 3 khoá
- [x] 2.2 Thêm ô lọc **Loại issue** (BE đã nhận `issue_type` từ trước, FE chưa có)
- [x] 2.3 Tách cột "Mã-Tên issue" → `issueCode` (button `.v2-cell-link` mở modal Xem, `sticky` +
      `locked`) + `issueTitle`; gỡ nút thao tác khỏi ô này
- [x] 2.4 Cột `actions` **cuối bảng** + `V2BaseRowActions`: Sửa · Xóa + menu `⋮` (Xử lý · Lịch sử);
      **bỏ "Xem"**
- [x] 2.5 Bật `fixed-layout` + khai `width` = `minWidth` cho đủ **25 cột**; ô ghép "MÃ - Tên" của
      đối tượng tham chiếu (giải pháp) trên **1 dòng**
- [x] 2.6 Thêm 6 cột: Tình trạng hạn · Version giải pháp · Nhãn · Người cập nhật · Ngày cập nhật ·
      **Ngày tạo** (cột bắt buộc, trước không có); `createdName` → `createdByName`
- [x] 2.7 `columnCustomizationMixin` thay `getFields`/`updateColumns`/`defaultTableColumns` viết tay
- [x] 2.8 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` (trước tải thẳng file)
- [x] 2.9 `ignoredFields` thành computed dùng `textFilterKeys`; `handleSort`/`handleReset` **không**
      gọi `loadData()` (deep watcher lo) + `suppressFilterWatch` chặn gọi trùng
- [x] 2.10 `loadSeq` chống response về trễ; `$nuxt.$loading` → `$safeLoadingStart/Finish`
- [x] 2.11 Thứ tự request: `loadData()` bắn TRƯỚC (trước đây `await getFields()` chặn ~1 request);
      options bộ lọc hoãn tới khi mở panel (`filterOptionsLoaded`)
- [x] 2.12 Bỏ sạch `'—'` (21 chỗ) + `font-weight-bold` (12 chỗ); ô dữ liệu dùng
      `field-line text-dark font-weight-normal` (18 ô); bỏ `v-html` dựng chuỗi "Trong hạn / Quá hạn"
- [x] 2.13 4 nút lọc nhanh + 2 pill Tổng/Quá hạn: chuyển từ slot `#toolbar` sang `#left-actions`;
      nhóm nút sang `#actions`
- [x] 2.14 Bỏ 3 hàm map nhãn ở FE (`getIssueTypeLabel`, `getDetectedFromLabel`, in-hạn/quá-hạn
      dựng bằng `v-html`) — dùng chữ + màu BE trả

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel)
- [x] 3.2 Đối chiếu tự động: mọi cột đủ `width` = `minWidth` + có slot render; `exportFields` FE ↔
      registry BE khớp; 0 chỗ `'—'` / `font-weight-bold` / `javascript:void(0)` / `field-line` trần
- [x] 3.3 Smoke test API bằng dữ liệu giả trong transaction rồi `ROLLBACK` (bảng `issues` rỗng):
      danh sách · sort whitelist · lọc `issue_type` · tìm theo người tạo · export `fields=`
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Modal `CreateIssueModal.vue` (Tạo / Sửa / Xem / Xử lý) — giữ nguyên.
- 3 màn Issue khác dùng `IssueResource` chung: `assign/solutions/{id}` (tab Issue),
  `assign/solution-modules/{id}`, `assign/my-jobs` — chỉ hưởng phần BE bổ sung, không đổi giao diện.
- Sắp xếp theo độ khớp (skill mục 3b) — chưa màn `assign/*` nào làm, để cả loạt làm sau.

### Checkpoint — 2026-09-08
Vừa hoàn thành: Phase 1 (5 việc BE) + Phase 2 (14 việc FE) + 3.1 → 3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/issues` (task 3.4).
Blocked: không — nhưng bảng `issues` đang RỖNG trên DB dev nên cần tạo issue thật để nhìn.
