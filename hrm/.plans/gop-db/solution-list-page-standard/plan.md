# Plan — Chuẩn hoá màn Danh sách làm giải pháp theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `SolutionService::index()` — thêm `SORTABLE_COLUMNS` (whitelist), bỏ `orderBy($request->sort_field)` trần
- [x] 1.2 `SolutionService::index()` — subquery `creator_name` / `updater_name` (chỉ fullname, KHÔNG kèm mã NV, không leftJoin)
- [x] 1.3 `SolutionResource` — trả `creator_name`, `updater_name`; `created_at`/`updated_at` format `d/m/Y H:i`
- [x] 1.4 `ExportColumnRegistry::COLUMNS['solutions']` — khai bộ cột xuất file
- [x] 1.5 `SolutionController::export()` — chuyển sang `DynamicExport` + `ExportColumnRegistry::resolve()`, đuôi `.xlsx`

## Phase 2 — Frontend (`hrm-client/pages/assign/solutions/index.vue`)

- [x] 2.1 Panel lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` + schema `filterFields` (18 ô), bỏ `title`/`subtitle`
- [x] 2.2 Placeholder chuẩn (`Chọn <trường>` / `Nhập <trường>`), quick search liệt kê đúng trường BE tìm
- [x] 2.3 `ignoredFields` computed dùng `textFilterKeys()`; deep watcher reset `currentPage = 1`
- [x] 2.4 Tách cột `solutionCode` (link `.v2-cell-link`, sticky+locked) / `solutionName` (chữ thường)
- [x] 2.5 Cột `actions` cuối bảng + `V2BaseRowActions` (Sửa, Xóa chính; Quản lý, Duyệt vào `⋮`); bỏ "Xem"
- [x] 2.6 Thêm cột `createdByName`, `createdAt`, `updatedByName`, `updatedAt`; đổi `status` → `solutionStatus` đứng trước Hành động
- [x] 2.7 Mặc định 8 cột hiện, còn lại `isVisible: false`
- [x] 2.8 Thay logic merge cột tự viết bằng `columnCustomizationMixin` (`columnScreenKey: 'solutions'`)
- [x] 2.9 Bỏ hết `'—'` (list + BE resource), bỏ `.text-muted` (đang là màu ĐỎ), bỏ `font-weight-bold` trong ô
- [x] 2.10 Xuất Excel: `exportFieldsMixin` + `ExportFieldsModal`, dùng `$safeLoadingStart/Finish`
- [x] 2.11 Thứ tự request khi vào màn: `loadData()` chạy đầu tiên; options bộ lọc hoãn tới khi mở panel
- [x] 2.12 Căn lề + `width` theo bảng quy tắc (STT 48px, Trạng thái 130px, Hành động 140px)

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE (`vue-template-compiler` + babel parse)
- [x] 3.2 Smoke test API `index` / `export` qua HTTP kernel trong tinker
- [ ] 3.3 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Phase 4 — Phân bổ độ rộng cột (bảng nhiều cột chữ dài)

Vấn đề: `table-layout: auto` + `width: 100%` -> bảng ép vừa khung, toàn bộ phần thiếu chỗ dồn vào
mấy cột `text-wrap` (Dự án, Yêu cầu làm GP, Khách hàng cuối) làm chúng bị bóp xuống 4-6 dòng, trong
khi cột dữ liệu ngắn nhưng TIÊU ĐỀ dài lại bị ghim rộng vì `thead th` cũng `white-space: nowrap`.

- [x] 4.1 `V2BaseDataTable` — thêm prop `fixedLayout` (opt-in, mặc định `false`): bật
      `table-layout: fixed` + `min-width` = tổng `width` khai báo, cho tiêu đề cột xuống dòng,
      ô dữ liệu tràn thì cắt bằng `text-overflow: ellipsis`
- [x] 4.2 `V2BaseDataTable` — hỗ trợ `cellClass: 'clamp-2'`: ô chữ dài kẹp tối đa 2 dòng rồi `…`
- [x] 4.3 `pages/assign/solutions/index.vue` — bật `fixed-layout`, khai `width` cho ĐỦ 24 cột theo
      4 bậc (S 130-150 / M 170-190 / L 220-260 / XL 300)
- [x] 4.4 `pages/assign/solutions/index.vue` — cột chữ dài dùng `text-wrap clamp-2` + `:title` để
      hover xem đủ nội dung bị cắt
- [x] 4.5 Gộp "MÃ - Tên" vào CÙNG 1 DÒNG ở các ô có cả 2 giá trị (Khách hàng, Yêu cầu làm GP,
      Khách hàng cuối) qua helper `joinCodeName()` — tách 2 dòng làm ô cao gấp đôi trong khi cột
      vẫn còn chỗ ngang
- [x] 4.6 Ghi quy tắc thành mục **15b** trong `.claude/skills/list-page/SKILL.md` (chẩn đoán, 5 bước
      bắt buộc, bảng 4 bậc bề rộng, 3 cái bẫy)
- [ ] 4.7 Compile FE + user mở trình duyệt kiểm tra; nếu đạt -> nhân rộng `fixedLayout` cho các màn
      danh sách khác (đợt sau, ngoài phạm vi task này)

## Nợ lại (ngoài phạm vi đợt này)

- [ ] Hành động "Lịch sử" — cần làm audit log cho `solutions` theo skill `entity-history`

## Việc phát sinh (làm thêm trong lúc chuẩn hoá)

- [x] `Solution::STATUSES` — sửa 4 mã màu lệch bảng 9 mã chuẩn (skill list-page mục 3c-2):
      Chờ Leader duyệt `#EA580C` → `#D97706` · Đã duyệt giá `#059669` → `#16A34A` ·
      Chờ làm giá `#0891B2` → `#D97706` · Chốt giải pháp `#4F46E5` → `#7C3AED`
- [x] Bỏ `loadRequestSolutionsCanCreate()` — gọi API 1.000 bản ghi mỗi lần vào màn nhưng kết quả
      (`canCreateSolutionFromRequest`) không được dùng ở đâu trong template
- [x] Thêm `employee_id` vào `initialStateForm` — `V2BaseCompanyDepartmentFilter` ghi vào khoá này
      (ô "PM phụ trách") mà bộ lọc chưa khai sẵn nên Vue 2 không theo dõi được
- [x] `mergeKnownFilters()` khi khôi phục bộ lọc đã lưu — bản lưu cũ còn `solution_department_id` /
      `solution_employee_id` (2 ô đã bỏ) sẽ lọc ngầm nếu spread nguyên object
- [x] `handleReset` tự gọi `loadData()` + cờ bỏ qua watcher 1 lần — `keyword` nằm trong
      `ignoredFields` nên nếu chỉ dựa vào watcher, bấm "Làm mới" sau khi gõ từ khoá sẽ không nạp lại

### Checkpoint — 2026-09-05
Vừa hoàn thành: Phase 1 (BE) + Phase 2 (FE) + 3.1/3.2 (compile FE, smoke test API index/export qua HTTP kernel — 200, sort whitelist chạy, file .xlsx dựng được, key `fields` lạ bị lọc).
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra màn `/assign/solutions` (task 3.3).
Blocked: hành động "Lịch sử" — cần audit log cho `solutions` (skill `entity-history`), user chốt để đợt sau.

## Phase 4 — Áp skill `button-convention` (bổ sung 2026-09-05, user nhắc)

- [x] 4.1 Xuất Excel: thêm `status="success"` (nhóm Xuất = xanh lá)
- [x] 4.2 Khoá nút lúc đang xuất bằng `:interactable="!exporting"` thay `:disabled` (prop `disabled` không có tác dụng trên V2BaseButton)
- [x] 4.3 Hành động "Quản lý giải pháp" đổi icon `ri-settings-3-line` → `ri-folder-user-line` (icon bánh răng chỉ dành cho cấu hình/cài đặt thật)
- [x] 4.4 Lệnh GHI (Xóa) bọc `$safeLoadingStart()` + `$safeLoadingFinish()` trong `finally`

## Cập nhật 2026-09-05 — MẶC ĐỊNH HIỆN HẾT CỘT (user chốt)

- [x] Bỏ toàn bộ `isVisible: false` trong `allColumns` — vào màn là thấy đủ cột, ai thấy rộng quá
      thì tự tắt bớt ở popup "Cấu hình cột hiển thị" (cấu hình lưu riêng theo từng người).

⚠️ Đây là **ngoại lệ có chủ ý** so với `list-page` mục 6 (mặc định 7 cột). Lệnh user thắng skill;
skill vẫn ghi luật cũ nên muốn đổi thì phải qua PR (CLAUDE.md: skill là tài sản chung).

## Cập nhật 2026-09-05 (2) — Áp mục 15b của skill `list-page` (bề rộng cột)

Skill vừa được bổ sung **mục 15b "Bề rộng cột — màn nhiều cột, có cả chữ dài lẫn chữ ngắn"** (chốt
cùng ngày) sau khi tôi đọc skill lần đầu → lần chỉnh bề rộng trước đó (đoán tay từng cột) là SAI cách.

- [x] Bật prop `fixed-layout` trên `V2BaseDataTable`
- [x] Khai `width` + `minWidth` cho **đủ mọi cột** theo 4 bậc S (130-150) · M (170-190) · L (220-260) · XL (300)
- [x] Cột chữ dài dùng `cellClass: 'text-wrap clamp-2'` + `:title` trên thẻ trong slot (kẹp 2 dòng, hover xem đủ)
- [x] Ô đối tượng THAM CHIẾU (Khách hàng · Yêu cầu làm GP · Khách hàng cuối) ghép **"MÃ - Tên" cùng 1 dòng**
      qua helper `joinCodeName()` thay vì 2 `<div>` — ô cao gấp đôi mà cột vẫn còn chỗ ngang, và `clamp-2`
      thành vô nghĩa vì nội dung đã ăn đủ 2 dòng (mục 15b bước 4)
