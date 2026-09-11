# Plan — Chuẩn hoá màn Danh sách dự án tiền khả thi theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-prospective-project-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `ProspectiveProjectService::index()` — whitelist `SORTABLE_COLUMNS` (13 khoá) +
      `applySort()` chốt `id desc` ở cuối (trước là `orderBy($request->sort_field, ...)` trần)
- [x] 1.2 `ProspectiveProjectService::index()` — subquery `creator_name` / `updater_name`
      (`employeeNameSql()`, KHÔNG leftJoin)
- [x] 1.3 `ProspectiveProject` — `STATUS_COLORS` + `PARENT_STATUS_COLORS` theo bảng 9 mã màu chuẩn,
      `resolveStatusColor()` + accessor `status_color`
- [x] 1.4 `ProspectiveProjectResource` — trả `creator_name`, `updater_name`, `status_color`,
      `status_text`; `created_at`/`updated_at` đổi `d-m-Y` → `d/m/Y H:i`; 2 cột ngày nghiệp vụ
      `d/m/Y`; **bỏ khoá trùng `customer_need_solution_date`** đang ghi đè bản đã format
- [x] 1.5 Gỡ N+1: đọc nhân sự/phòng ban qua quan hệ (+ quan hệ mới `solutionEmployee`), eager load
      đủ 12 quan hệ, `canDelete()` dùng lại `children_count` → **147 → 56 query / 10 dòng**
- [x] 1.6 3 danh mục cứng (Quy mô · Phân loại đầu tư · Nguồn vốn) + tên loại dự án chuyển từ FE
      và blade về hằng trên Entity, Resource trả `*_text`
- [x] 1.7 `ExportColumnRegistry::COLUMNS['prospective_projects']` — 32 cột
- [x] 1.8 `ProspectiveProjectController::export()` — `DynamicExport` + `resolve()`, `.xls` → `.xlsx`,
      ép `tree = false` để file phẳng có cả dự án con

## Phase 2 — Frontend (`pages/assign/prospective-projects/index.vue`)

- [x] 2.1 Tách cột gộp `projectInfo` → `projectCode` (link `.v2-cell-link`, sticky + locked,
      sortable) + `projectName` (chữ thường, `text-wrap clamp-2` + `:title`)
- [x] 2.2 Tách 5 dòng phụ thành cột riêng: NV KD phụ trách · Phòng ban · Bộ phận · Ngày tạo ·
      Ngày cập nhật; thêm Người tạo · Người cập nhật
- [x] 2.3 Cột `actions` cuối bảng + `V2BaseRowActions` (Sửa, Xóa là 2 nút chính; Tạo giải pháp,
      Tạo yêu cầu làm GP vào `⋮`); bỏ hành động "Xem" + gỡ dãy icon dưới tên dự án
- [x] 2.4 Trạng thái: `V2BaseBadge` + `:color="item.status_color"`, key `progress` → `projectStatus`
      để dời về ngay trước Hành động; bỏ `getProgressClass()` + 5 rule CSS `.pj-status-*`
- [x] 2.5 `columnCustomizationMixin` (`columnScreenKey: 'prospective_projects'`) thay ~80 dòng
      merge tự viết
- [x] 2.6 Xuất Excel: `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` dùng `downloadExcel`
      và `$safeLoadingStart/Finish`; nút màu `success`, khoá bằng `:interactable`
- [x] 2.7 Bỏ sạch `'—'`; bỏ in đậm trong ô (kể cả `font-weight: 600` của dòng dự án cha)
- [x] 2.8 Bật `fixed-layout` + khai `width`/`minWidth` cho ĐỦ 29 cột theo 4 bậc; ô tham chiếu ghép
      `MÃ - Tên` cùng 1 dòng qua `joinCodeName()`
- [x] 2.9 `created()`: `loadData()` bắn đầu tiên; thêm `loadSeq`; khôi phục bộ lọc trước khi gọi;
      watcher reset trang 1; `handleSort` chỉ đổi `filters`; `handleReset` không gọi API 2 lần
- [x] 2.10 Giữ nguyên cây cha – con (nút mở rộng ở ô STT, `treeTableData`, `getRowClass`)
- [x] 2.11 Xóa dự án bọc `$safeLoadingStart/Finish`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel) — OK
- [x] 3.2 Đối chiếu tự động: 29/29 cột đủ `width`+`minWidth`, có slot hoặc khoá khớp API, map được
      sang cột xuất file; `exportFields` FE ↔ registry BE **32 = 32, cùng thứ tự**; 32/32 khoá có
      thật trong Resource
- [x] 3.3 Smoke test API qua HTTP kernel: `index` 200 (trả đủ trường mới) · sort 3 khoá đổi đúng
      thứ tự · key lạ + chuỗi tiêm SQL rơi về mặc định · `export` 200 (109 KB, chữ ký `504b`) ·
      `export?fields=...` chỉ ra đúng 3 cột, key lạ bị loại
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi (user chốt 2026-09-07)

- **Bộ lọc giữ nguyên** khuôn cũ (`V2BaseFilterPanel`) — không chuyển `V2BaseSmartFilterPanel`,
  không đổi placeholder / trường tìm nhanh. Hệ quả: 3 quy tắc của skill chưa áp cho màn này —
  tiêu đề panel riêng, `.text-muted` (đang là màu ĐỎ) trong dropdown gợi ý khách hàng, và ô lọc
  gõ tay chưa chờ Enter (`ignoredFields` vẫn chỉ có `keyword`).
- Hành động **"Lịch sử"** — cần audit log cho `prospective_projects` (skill `entity-history`).
- `is_form_complete` / `is_can_create_request_solution` còn 1-2 query mỗi dòng.

## Phase 4 — Tinh chỉnh theo phản hồi user (2026-09-07)

- [x] 4.1 Cột **Khách hàng** + **Khách hàng cuối** `240px` → **`260px`** — đỉnh bậc L (220-260px)
      của skill mục 15b: 2 ô này ngoài "MÃ - Tên" còn dòng phụ "Người liên hệ: tên • SĐT" nên
      không để mức giữa như ô tham chiếu 1 dòng (Giải pháp giữ 240px)
- [x] 4.2 Dòng phụ trong ô bảng (Người liên hệ, SĐT PM) đổi sang **xám #6b7280** — `.project-sub`
      ở `v2-styles.scss` chỉ khai cỡ chữ, KHÔNG khai màu nên đang thừa hưởng màu chữ đậm của ô,
      đọc ngang hàng với nội dung chính. Đè màu trong `<style scoped>` của màn, không sửa file
      dùng chung; không dùng `.text-muted` (4 file scss toàn cục ép class đó thành ĐỎ #dc3545)
- [x] 4.3 Cột `projectCode` `170px` → **`210px`** để hiện ĐỦ mã, không cắt bằng "…": mã dự án dài
      tới **26 ký tự** (`HN_KDTM.UD.0042.2026.DA002`, đo trên dữ liệu thật) và là chuỗi liền không
      có chỗ ngắt. Vượt bậc M (170-190px) của skill mục 15b là **có chủ ý**.
      ~~Ghim cột Tên dự án TKT~~ — đã thử rồi **bỏ** theo yêu cầu user cùng ngày; cột Tên trở lại
      đúng skill mục 3 (không `sticky`, không `locked`, user tự ẩn / đổi vị trí được).
      Nhóm ghim trái còn `STT(60) → Mã dự án(210)` = **270px**.
- [x] 4.4 Gộp **NV KD phụ trách + Phòng ban + Bộ phận** thành MỘT cột `mainSaleInfo`
      ("Tên NV - Phòng ban - Bộ phận" trên 1 dòng, 260px, `clamp-2` + `:title`) — user đổi ý so với
      lựa chọn "tách hết" lúc đầu. 3 giá trị luôn đi cùng nhau, để riêng thì bảng dài thêm ~550px
      mà đọc rời từng cột không có nghĩa. Bảng 29 → **27 cột**.
      **File xuất giữ NGUYÊN 3 cột riêng** (lọc/tổng hợp trên Excel cần tách); popup Chọn trường
      tick sẵn "NV KD phụ trách", Phòng ban / Bộ phận tick thêm nếu cần.
- [x] 4.5 Kiểm lại: compile SFC OK; 27/27 cột đủ `width`+`minWidth` và map được sang cột xuất file;
      nhóm ghim liền nhau ở đầu bảng

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (8 việc BE) + Phase 2 (11 việc FE) + 3.1/3.2/3.3 + Phase 4 (3 tinh chỉnh
theo phản hồi user: bề rộng cột Khách hàng, màu dòng phụ, bề rộng cột Mã — cột Tên thử ghim rồi bỏ).
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/prospective-projects` (task 3.4).
Blocked: không.

## Cập nhật 2026-09-07 — Đồng bộ MÀU CHỮ trong ô bảng với màn mẫu `/assign/customers`

- [x] Mọi ô dữ liệu đổi từ `class="field-line"` trần sang **`class="field-line text-dark font-weight-normal"`**
      — đúng như màn mẫu `/assign/customers` và `/assign/solutions` đang dùng. `.field-line` trần
      chỉ có `color: #475569` (xám) nên chữ nhạt hơn hẳn các màn khác, nhìn cạnh nhau là lộ.
- [x] Dòng phụ trong ô (Người liên hệ, SĐT PM…) gắn thêm class **`v2-hint`** (`color: #6b7280`)
      khai trong `<style scoped>` của màn — cùng cách làm với màn Giải pháp, thay cho việc đè màu
      thẳng vào `.project-sub`.
- [x] Kiểm lại 4 màn: customers 18 ô chuẩn · solutions 21 · prospective-projects 10 · product-project 13;
      không còn ô nào dùng `.field-line` trần (trừ 1 chỗ có chủ ý ở màn khách hàng: người không có
      quyền xem thì mã KH là chữ thường, không phải link).
