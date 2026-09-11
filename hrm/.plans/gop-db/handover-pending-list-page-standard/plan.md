# Plan — Chuẩn hoá màn "Phiếu bàn giao chờ duyệt" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-08-handover-pending-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `HandoverService::pending()` gọi `applyHandoverSort()` (whitelist 13 khoá + chốt `id desc`) thay
      `orderBy('created_at','desc')` chốt cứng — màn trước KHÔNG sắp xếp được cột nào
- [x] 1.2 Bộ lọc "Ngày gửi duyệt từ/đến" lọc trên **`submitted_at`** thay vì `updated_at`
- [x] 1.3 `HandoverController::pendingExport()` + route `assign/handovers/pending/export`
      (đặt TRƯỚC route `/{handover}`), dùng `DynamicExport` + registry `handovers`, nhận `fields=`

## Phase 2 — Frontend (`pages/assign/handover/pending.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (8 mục, bỏ `title`/`subtitle`)
- [x] 2.2 Ô **Giải pháp** bỏ `disabled` cứng, thành ô chọn thật lọc theo Dự án; cascade
      Dự án → Giải pháp → Hạng mục viết lại bằng watcher (bỏ `@input="onProjectChange"` tự đoán
      giải pháp theo dự án)
- [x] 2.3 Options bộ lọc đổi `{value,label}` → `{id,name}` cho đúng khuôn panel mới
- [x] 2.4 Cột `handoverCode` là `nuxt-link` (sticky + locked), gỡ nút thao tác khỏi ô Mã phiếu
- [x] 2.5 Cột `actions` **cuối bảng** + `V2BaseRowActions`: **Duyệt** (điều hướng) + **Lịch sử**
      (dùng lại `HandoverHistoryModal`); bỏ "Xem & Duyệt" gộp trong ô mã
- [x] 2.6 **Thêm sắp xếp** — bảng nhận `@sort` + `sortBy`/`sortDirection` (trước không sort được)
- [x] 2.7 Bật `fixed-layout` + khai `width` = `minWidth` cho đủ **15 cột**; thêm 6 cột: Phòng ban ·
      Ghi chú · Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật
- [x] 2.8 **BỎ HẲN** 3 cột luôn rỗng ở trạng thái Chờ duyệt (Người duyệt · Ngày duyệt · Lý do từ
      chối) và 3 khoá đếm `accepted/rejected/pending_items`; cột "Công việc" chỉ còn tổng số
- [x] 2.9 `columnCustomizationMixin` (`columnScreenKey: 'handover_pending'`) + `ColumnCustomizationModal`
- [x] 2.10 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` — thay nút Xuất Excel chết
- [x] 2.11 `filterStateMixin` — giữ bộ lọc khi vào chi tiết rồi quay lại
- [x] 2.12 Deep watcher auto-search + `ignoredFields` computed (`textFilterKeys`); `handleSort`/
      `handleReset` không gọi `loadData()`; `suppressFilterWatch` chặn gọi trùng
- [x] 2.13 `loadSeq` chống response về trễ; `$safeLoadingStart/Finish`
- [x] 2.14 Nút toolbar chuyển từ slot `#toolbar` sang `#actions` + `#left-actions` (giữ ô "Tổng")
- [x] 2.15 Bỏ sạch `'—'` (7 chỗ) + `font-weight-bold` (3 chỗ) + `javascript:void(0)`; ô dữ liệu
      dùng `field-line text-dark font-weight-normal`; bỏ import chết `V2BaseTitleSubInfo` và
      `statusOptions` không dùng

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel)
- [x] 3.2 Đối chiếu tự động: 15 cột đủ `width` = `minWidth` + có slot render; `exportFields` FE ↔
      registry BE khớp; 0 chỗ `'—'` / `font-weight-bold` / `javascript:void(0)` / `field-line` trần
- [x] 3.3 Smoke test API bằng phiếu giả trong transaction rồi `ROLLBACK` (bảng `handovers` rỗng):
      danh sách (phiếu Nháp bị loại đúng) · sort 2 khoá asc/desc + key lạ · **lọc `submitted_at` 2 chiều** ·
      lọc `reason` · tìm nhanh theo mã và theo tên người bàn giao · export `fields=`.
      ⚠️ 3 bộ lọc qua `items` (người tiếp nhận / dự án / giải pháp / hạng mục) **chưa thử** — phải
      dựng thêm Task/Issue giả mới chạy được; câu lọc giữ nguyên như bản cũ, không đụng tới
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Màn chi tiết `_id/index.vue` (nơi thực sự bấm Duyệt / Từ chối) — giữ nguyên.
- `HandoverService::pendingFilterOptions()` — giữ nguyên cấu trúc trả về, FE tự đổi tên khoá.

### Checkpoint — 2026-09-08
Vừa hoàn thành: Phase 1 (3 việc BE) + Phase 2 (15 việc FE) + 3.1 → 3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/handover/pending` (task 3.4).
Blocked: không — nhưng bảng `handovers` đang RỖNG trên DB dev nên cần tạo phiếu thật để nhìn.
