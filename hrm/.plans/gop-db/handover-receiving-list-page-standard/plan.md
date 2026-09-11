# Plan — Chuẩn hoá màn "Phiếu bàn giao chờ tiếp nhận" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-handover-receiving-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `HandoverService::receivingHandovers()` **MỚI** — trả PHIẾU thay vì từng công việc:
      `whereHas('items', $itemFilter)` + 4 `withCount` dùng lại đúng closure đó
      (`my_total_items` / `my_accepted_items` / `my_rejected_items` / `my_pending_items`)
- [x] 1.2 Giữ nguyên 4 bộ lọc theo công việc (dự án / giải pháp / hạng mục Task-Issue 2 nhánh) +
      3 bộ lọc theo phiếu (mã, lý do, người bàn giao) + ô tìm nhanh (mã phiếu **hoặc** tên người
      bàn giao — trước chỉ tìm theo tên)
- [x] 1.3 Whitelist `RECEIVING_SORTABLE_COLUMNS` (7 khoá) + chốt `id desc`; mặc định `approved_at desc`
- [x] 1.4 `ReceivingHandoverResource` **MỚI** — không đụng `HandoverResource` (đang dùng ở
      `/assign/handover` và `/assign/handover/pending`)
- [x] 1.5 `HandoverItemController::receiving()` đổi sang gọi `receivingHandovers()` +
      `ReceivingHandoverResource`
- [x] 1.6 `receivingExport()` + route `assign/handovers/receiving/export` +
      `ExportColumnRegistry['handover_receiving']` 15 cột

## Phase 2 — Frontend (`pages/assign/handover/receiving.vue`)

- [x] 2.1 **Bỏ đoạn gom `handover_id` bằng JS** trong `loadData()` — BE đã trả thẳng phiếu
- [x] 2.2 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (6 mục)
- [x] 2.3 Ô **Giải pháp** bỏ `disabled` cứng, thành ô chọn thật lọc theo Dự án; cascade
      Dự án → Giải pháp → Hạng mục viết lại bằng watcher (trước dùng `@input="onProjectChange"`
      tự đoán giải pháp theo dự án)
- [x] 2.4 Options bộ lọc đổi `{value,label}` → `{id,name}` cho đúng khuôn panel mới
- [x] 2.5 Cột `handoverCode` là `nuxt-link` (trước `<a href="javascript:void(0)">`), `sticky` +
      `locked`; gỡ nút thao tác khỏi ô Mã phiếu
- [x] 2.6 Cột `actions` cuối bảng + `V2BaseRowActions`: **Tiếp nhận** (điều hướng) + Lịch sử
- [x] 2.7 Thêm 6 cột: Phòng ban · Ghi chú · Người tạo phiếu · Ngày tạo (và tách 4 con số công việc
      của tôi vào 1 ô); bật `fixed-layout` + khai `width` = `minWidth` cho đủ 14 cột
- [x] 2.8 **Thêm sắp xếp** — bảng nhận `@sort` + `sortBy`/`sortDirection` (màn này trước KHÔNG sắp
      xếp được cột nào)
- [x] 2.9 `columnCustomizationMixin` + `ColumnCustomizationModal` (lần đầu bật/tắt được cột)
- [x] 2.10 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` — **thay nút Xuất Excel chết**
      (bản cũ gọi lại API danh sách rồi hiện toast "đang phát triển")
- [x] 2.11 `filterStateMixin` — giữ bộ lọc khi vào màn tiếp nhận rồi quay lại
- [x] 2.12 Thêm `loadSeq` + `suppressFilterWatch`; nút toolbar chuyển từ slot `toolbar` sang
      `actions` + `left-actions` (giữ ô "Tổng", nay lấy `pagination.total` thay vì
      `tableData.length` — con số cũ chỉ đếm số dòng của TRANG hiện tại)
- [x] 2.13 Dùng lại popup `HandoverHistoryModal` vừa tạo ở màn danh sách phiếu bàn giao
- [x] 2.14 Bỏ sạch `'—'` / `font-weight-bold` / `style` màu nội tuyến trong ô

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel) — OK
- [x] 3.2 Đối chiếu tự động: 14/14 cột đủ `width` = `minWidth`, có slot render, map được sang cột
      xuất file; `exportFields` FE ↔ registry BE **15 = 15, cùng thứ tự**; 0 chỗ
      `'—'`/`'N/A'`/`v-html`/`.status-pill`/`javascript:void(0)`
- [x] 3.3 Smoke test: 2 bảng đều rỗng nên dựng **4 phiếu + 7 công việc giả trong transaction rồi
      ROLLBACK**. Kết quả: đúng **2 phiếu** lọt danh sách (phiếu của người nhận khác và phiếu chưa
      duyệt bị loại đúng); 4 con số đếm đúng việc CỦA TÔI (`3 = 1 nhận / 1 từ chối / 1 chờ` và
      `2 = 0/0/2`); 2 khoá sort đổi đúng thứ tự + key lạ về mặc định; lọc `code` / `reason` /
      `keyword` / `prospective_project_id` / `solution_id` đều ăn; export .xlsx **9 dòng = 2 dữ
      liệu + 7 dòng khung**, 16 cột, `fields=` lọc còn 3 cột đúng thứ tự tick; rollback xong 2
      bảng về lại 0 dòng
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- `/assign/handover/pending` (Chờ tôi duyệt) — chưa chuẩn hoá, vẫn dùng `HandoverResource`.
- Màn tiếp nhận chi tiết `_id/receive.vue` giữ nguyên.
- `HandoverService::receiving()` (trả từng công việc) **vẫn còn** nhưng không còn nơi gọi —
  giữ lại phòng khi cần danh sách theo công việc.

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (6 việc BE) + Phase 2 (14 việc FE) + 3.1→3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/handover/receiving` (task 3.4).
Blocked: không — nhưng 2 bảng `handovers`/`handover_items` đang rỗng nên cần tạo dữ liệu thật để nhìn.
